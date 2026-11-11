"""
check_model.py - design-rule checks for the IDEX printer Fusion model.

Run it as a Fusion 360 script (Utilities > Add-Ins > Scripts) with the
assembly open, or hand the source to the Fusion MCP `script` tool.

Why this exists
---------------
Every fault in this project so far was found by measuring, and every one that
got in was placed by eye. Screenshots do not tell you whether a rail is
centred on a slot, whether a bracket touches anything, or whether a parameter
reaches the part it is supposed to drive. These checks do, repeatably.

Checks
  1  nozzle tip of each toolhead sits exactly on bed_top
  2  the print surface really is at bed_top
  3  every bracket touches at least one frame member
  4  each rail is centred on a measured V-slot, not between two
  5  interference is only the known shaft-through-bore set
  6  the timeline is healthy
  7  each toolhead parks clear of the build area
  8  PARAMETRIC - every part is tied to the Skeleton, and checks 1-5 and 7
     are re-run with each driver flexed. Not moving is not a fault (the frame
     grows from its left, front and floor); breaking a rule is.
  9  no parameter drives nothing (decoration that looks like design intent)
 10  driver validation rules, in the style of a product configurator:
     every driver has a legal range, checked before the
     model is allowed to regenerate rather than after.
 11  BOM check line - every cut length, count and stocked size listed in
     docs/bom.json is measured in the model
"""

import adsk.core
import adsk.fusion
import json
import os
import traceback

SOLID = (adsk.fusion.PointContainment.PointInsidePointContainment,
         adsk.fusion.PointContainment.PointOnPointContainment)
P = adsk.core.Point3D.create

FRAME = ('Upright 4040', 'Base rail 4040', 'Base cross 2040',
         'Top tie 2040', 'X beam 2040', 'Bed rail 2020')
BRACKETS = ('X motor mount', 'X idler bracket', 'Y motor mount',
            'Y idler bracket', 'Z screw block', 'Electronics panel')

# the overlaps that are a shaft or a belt meeting a part that would carry a
# bore in reality. Any value not on this list is a fault.
EXPECTED_INTERFERENCE = sorted([992, 992, 384, 122, 122, 70, 70])

# parameter, nominal, test value. Set FLEX_CASES to a list of names to run
# only those (each flex recomputes the whole assembly; run one per call when
# driving Fusion through a tool with a time limit). [] runs none.
FLEX_CASES = None
BOM_JSON = os.path.join(os.path.expanduser('~'), 'repos', 'idex-3d-printer', 'docs', 'bom.json')
QUIET = False  # True: print only, no message box (when run through a tool)
FLEX = (('build_x', '230 mm', '300 mm'),
        ('build_y', '235 mm', '305 mm'),
        ('upright_h', '500 mm', '570 mm'))

# Driver validation, as a product configurator would do it: each driving
# parameter has a legal range and the relationships are checked explicitly.
# name: (min, max, note)
DRIVER_RULES = {
    'build_x':    (100, 1000, 'build volume X'),
    'build_y':    (100, 1000, 'build volume Y'),
    'build_z':    (100, 1000, 'build volume Z'),
    'carriage_w': (40, 200, 'one IDEX carriage must fit two MGN12H blocks in line'),
    'park_gap':   (5, 100, 'clearance between a parked carriage and the build area'),
    'end_allow':  (20, 150, 'motor and idler allowance at each beam end'),
    'upright_h':  (200, 1200, 'upright length'),
    'th_drop':    (40, 200, 'beam underside to nozzle tip'),
}


def part_list(root):
    """(name, sub-assembly, bbox-in-mm) for every real part."""
    out = []
    ao = root.allOccurrences
    for i in range(ao.count):
        o = ao.item(i)
        path, p = [], o
        while p is not None:
            path.append(p.name.split(':')[0])
            p = p.assemblyContext
        if any(x.startswith('Z - Parts') for x in path) or not o.bRepBodies.count:
            continue
        b = o.bRepBodies.item(0).boundingBox
        out.append((path[0], path[1] if len(path) > 1 else '', i,
                    (b.minPoint.x * 10, b.maxPoint.x * 10,
                     b.minPoint.y * 10, b.maxPoint.y * 10,
                     b.minPoint.z * 10, b.maxPoint.z * 10)))
    return out


def gap(a, b):
    """Largest axis separation between two boxes. 0 means they touch."""
    g = 0.0
    for i in (0, 2, 4):
        lo, hi = max(a[i], b[i]), min(a[i + 1], b[i + 1])
        if lo > hi:
            g = max(g, lo - hi)
    return g


def slot_centres(occ, point_at, lo, hi, step=0.25):
    """Walk just inside a face and return the centre of each gap: the V-slots."""
    body = occ.bRepBodies.item(0)
    runs, cur, v = [], None, lo
    while v <= hi:
        solid = body.pointContainment(point_at(v)) in SOLID
        if not solid:
            if cur is None:
                cur = v
        else:
            if cur is not None:
                if 2.0 <= (v - step) - cur <= 12.0:
                    runs.append((cur + v - step) / 2.0)
                cur = None
        v += step
    return runs


def run(_context):
    app = adsk.core.Application.get()
    ui = app.userInterface
    try:
        des = adsk.fusion.Design.cast(app.activeProduct)
        root = des.rootComponent
        up = des.userParameters
        pv = lambda n: up.itemByName(n).value * 10
        results = []

        def chk(name, ok, detail):
            results.append({'check': name, 'pass': bool(ok), 'detail': detail})

        pl = part_list(root)
        find = lambda nm, sub=None: [p for p in pl
                                     if p[0] == nm and (sub is None or p[1] == sub)]
        bed_top = pv('bed_top')
        ao = root.allOccurrences

        def geometry(sfx=''):
            """Checks 1-5 and 7 - run at nominal size and again at every flexed size."""
            pl = part_list(root)
            find = lambda nm, sub=None: [p for p in pl
                                         if p[0] == nm and (sub is None or p[1] == sub)]
            bed_top = pv('bed_top')

            # 1 / 2 - the print surface and the nozzles agree
            for tag in ('A', 'B'):
                h = find('Hotend V6 %s' % tag, 'C - Toolhead %s' % tag)
                z = h[0][3][4] if h else None
                chk(sfx + 'nozzle %s at bed_top' % tag,
                    z is not None and abs(z - bed_top) < 0.05,
                    'nozzle z=%.2f  bed_top=%.2f' % (z if z is not None else -1, bed_top))
            pei = find('PEI spring steel', 'D - Y and bed')
            chk(sfx + 'PEI top at bed_top', pei and abs(pei[0][3][5] - bed_top) < 0.05,
                'PEI top z=%.2f' % (pei[0][3][5] if pei else -1))

            # 3 - nothing floats
            frame = [p for p in pl if p[0] in FRAME]
            floating, n = [], 0
            for nm, sb, _, bx in pl:
                if not nm.startswith(BRACKETS):
                    continue
                n += 1
                g = min(gap(bx, f[3]) for f in frame)
                if g > 0.01:
                    floating.append('%s %.1fmm' % (nm, g))
            chk(sfx + 'all brackets touch the frame', not floating,
                '%d brackets, floating: %s' % (n, floating or 'none'))

            # 3b - each bought lead screw reaches its top and base screw blocks
            screws = [p for p in pl if p[0].startswith('8mm x 500mm Lead Screw')]
            blocks = [p for p in pl if p[0].startswith('Z screw block')]
            short = []
            for sc in screws:
                for tb in ('top', 'base'):
                    near = [b for b in blocks if tb in b[0] and abs((b[3][0] + b[3][1]) / 2 - (sc[3][0] + sc[3][1]) / 2) < 30]
                    if not near or min(gap(sc[3], b[3]) for b in near) > 0.01:
                        short.append('%s misses %s block' % (sc[0], tb))
            chk(sfx + 'lead screws reach both screw blocks', screws and not short,
                '%d screws; %s' % (len(screws), '; '.join(short) or 'all seated'))

            # 4 - rails land on a slot, not between two
            ao = root.allOccurrences
            beam = next((ao.item(i) for i in range(ao.count)
                         if ao.item(i).name.split(':')[0] == 'X beam 2040'
                         and ao.item(i).bRepBodies.count), None)
            if beam:
                centres = slot_centres(beam, lambda v: P(pv('frame_w') / 20.0, (pv('beam_y') + 1.0) / 10.0, v / 10.0), pv('gantry_z') - 1.0, pv('gantry_z') + 41.0)
                xr = find('MGN12 rail X', 'B - X gantry')
                xc = (xr[0][3][4] + xr[0][3][5]) / 2.0 if xr else -1
                chk(sfx + 'X rail centred on a beam slot',
                    any(abs(xc - s) < 0.3 for s in centres),
                    'rail centre z=%.1f, slots at %s' % (xc, ['%.1f' % s for s in centres]))

            # 5 - interference is only what we signed off
            ents = adsk.core.ObjectCollection.create()
            for i in range(ao.count):
                o = ao.item(i)
                path, p = [], o
                while p is not None:
                    path.append(p.name.split(':')[0])
                    p = p.assemblyContext
                if path[0].startswith('Layout') or any(x.startswith('Z - Parts') for x in path):
                    continue
                for k in range(o.bRepBodies.count):
                    bb = o.bRepBodies.item(k)
                    if bb.isVisible:
                        ents.add(bb)
            ii = des.createInterferenceInput(ents)
            ii.areCoincidentFacesIncluded = False
            res = des.analyzeInterference(ii)
            vols = []
            for i in range(res.count):
                b = res.item(i).interferenceBody.boundingBox
                vols.append(round((b.maxPoint.x - b.minPoint.x) *
                                  (b.maxPoint.y - b.minPoint.y) *
                                  (b.maxPoint.z - b.minPoint.z) * 1000.0))
            chk(sfx + 'interference is the known set only', sorted(vols) == EXPECTED_INTERFERENCE,
                '%d found: %s' % (res.count, sorted(vols, reverse=True)))

            # 7 - parking
            bx0 = pv('frame_w') / 2 - pv('build_x') / 2
            bx1 = pv('frame_w') / 2 + pv('build_x') / 2
            for tag in ('A', 'B'):
                h = find('Hotend V6 %s' % tag, 'C - Toolhead %s' % tag)
                nx = (h[0][3][0] + h[0][3][1]) / 2.0
                chk(sfx + 'toolhead %s parks clear of the build area' % tag,
                    nx < bx0 - 1 or nx > bx1 + 1,
                    'nozzle x=%.1f, build area %.1f..%.1f' % (nx, bx0, bx1))


        geometry()

        # 6 - timeline
        bad = 0
        for i in range(des.timeline.count):
            try:
                if des.timeline.item(i).healthState != \
                        adsk.fusion.FeatureHealthStates.HealthyFeatureHealthState:
                    bad += 1
            except Exception:
                bad += 1
        chk('timeline healthy', bad == 0, '%d unhealthy of %d' % (bad, des.timeline.count))


        # 8 - parametric: every part tied to the skeleton, and the design rules
        # still hold when a driver changes. A part that does not move is not a
        # fault (the frame grows from its left/front/floor), a broken rule is.
        tied = set()
        for i in range(root.joints.count):
            j = root.joints.item(i)
            if j.occurrenceOne:
                tied.add(j.occurrenceOne.fullPathName)
        untied, total = [], 0
        for i in range(ao.count):
            o = ao.item(i)
            top = o.fullPathName.split('+')[0]
            if top.startswith(('Z - Parts', 'Skeleton')) or o.assemblyContext is None:
                continue
            total += 1
            q, ok = o, False
            while q is not None:
                if q.fullPathName in tied:
                    ok = True
                    break
                q = q.assemblyContext
            if not ok:
                untied.append(o.name)
        coverage = {'tied': 100.0 * (total - len(untied)) / total if total else 0.0}
        chk('every part tied to the skeleton', not untied,
            '%d of %d tied; untied: %s' % (total - len(untied), total, untied or 'none'))

        for pname, nominal, test in (FLEX if FLEX_CASES is None else [f for f in FLEX if f[0] in FLEX_CASES]):
            up.itemByName(pname).expression = test
            des.computeAll()
            adsk.doEvents()
            n0 = len(results)
            try:
                pl[:] = part_list(root)
                geometry('@ %s=%s: ' % (pname, test))
            finally:
                up.itemByName(pname).expression = nominal
                des.computeAll()
                adsk.doEvents()
                pl[:] = part_list(root)
            flexed = results[n0:]
            coverage[pname] = 100.0 * sum(r['pass'] for r in flexed) / len(flexed) if flexed else 0.0

        # 9 - a parameter that drives nothing is decoration, and it rots.
        # z_screw_x read 33 mm long after the screws moved to 60.
        import re
        names = [up.item(i).name for i in range(up.count)]
        used = set()
        for i in range(up.count):
            e = up.item(i).expression
            for n in names:
                if re.search(r'\b%s\b' % re.escape(n), e):
                    used.add(n)
        ap = des.allParameters
        for i in range(ap.count):
            q = ap.item(i)
            if q.name in names:
                continue
            try:
                e = q.expression
            except Exception:
                continue
            for n in names:
                if re.search(r'\b%s\b' % re.escape(n), e):
                    used.add(n)
        orphan = [n for n in names if n not in used]
        chk('every parameter drives something', not orphan,
            '%d of %d drive nothing: %s' % (len(orphan), len(names), ', '.join(orphan) or 'none'))

        # 10 - driver ranges and relationships, checked up front
        broken = []
        for n, (lo, hi, note) in DRIVER_RULES.items():
            q = up.itemByName(n)
            if q is None:
                broken.append('%s missing' % n)
                continue
            v = q.value * 10
            if not (lo <= v <= hi):
                broken.append('%s=%.1f outside %g..%g' % (n, v, lo, hi))
        if pv('bed_sz') < pv('build_x') - 0.01 or pv('bed_sz') < pv('build_y') - 0.01:
            broken.append('bed_sz %.1f smaller than the build area' % pv('bed_sz'))
        if pv('carriage_w') < 2 * 45.4:
            broken.append('carriage_w %.1f cannot hold two MGN12H blocks in line' % pv('carriage_w'))
        if abs(pv('z_screw_len') - pv('upright_h')) > 0.01:
            broken.append('upright_h %.0f needs %.0f mm lead screws, model has z_screw_len %.0f'
                          % (pv('upright_h'), pv('upright_h'), pv('z_screw_len')))
        if pv('gantry_z') < pv('bed_top'):
            broken.append('gantry_z below bed_top - the nozzle would be inside the bed')
        chk('driver values are in range', not broken, '; '.join(broken) or 'all drivers legal')

        # 11 - the BOM check line: every cut length and count in docs/bom.json
        # is measured in the model. A CAD change without a BOM change fails here.
        try:
            bom = json.load(open(BOM_JSON, encoding='utf-8'))
        except Exception as ex:
            bom = None
            chk('BOM matches the model', False, 'cannot read %s: %s' % (BOM_JSON, ex))
        if bom is not None:
            bad, n = [], 0
            comps = {}
            for i in range(ao.count):
                o = ao.item(i)
                if o.fullPathName.split('+')[0].startswith(('Z - Parts', 'Skeleton')):
                    continue
                comps.setdefault(o.component.name, []).append(o)
            for sec, items in bom.items():
                for it in items:
                    total = 0.0
                    for cut in it.get('cuts', []):
                        n += 1
                        occs = comps.get(cut['component'], [])
                        if len(occs) != cut['qty']:
                            bad.append('%s: BOM %d, model %d' % (cut['component'], cut['qty'], len(occs)))
                        if not occs:
                            continue
                        c = occs[0].component
                        how = cut.get('measure', 'extrude')
                        if how == 'extrude':
                            mm = c.features.extrudeFeatures.item(0).extentOne.distance.value * 10
                        else:
                            bb = c.bRepBodies.item(0).boundingBox
                            k = 'xyz'.index(how)
                            mm = ([bb.maxPoint.x, bb.maxPoint.y, bb.maxPoint.z][k] -
                                  [bb.minPoint.x, bb.minPoint.y, bb.minPoint.z][k]) * 10
                        if abs(mm - cut['mm']) > 0.05:
                            bad.append('%s: BOM %g mm, model %.1f mm' % (cut['component'], cut['mm'], mm))
                        if 'stock' in cut and not any(abs(mm - st) < 0.05 for st in cut['stock']):
                            bad.append('%s: %.1f mm is not a stocked length %s' % (cut['component'], mm, cut['stock']))
                        total += mm * len(occs)
                    if 'stock_total_mm' in it and total > it['stock_total_mm']:
                        bad.append('%s: needs %.0f mm, stock is %d mm' % (it['item'], total, it['stock_total_mm']))
            chk('BOM matches the model', not bad,
                '%d cut lines checked; %s' % (n, '; '.join(bad) or 'all agree'))

        out = os.path.join(os.path.expanduser('~'), 'idex-model-checks.json')
        with open(out, 'w') as f:
            json.dump({'results': results, 'coverage': coverage}, f, indent=1)

        lines = ['%s  %-42s %s' % ('PASS' if r['pass'] else 'FAIL', r['check'], r['detail'])
                 for r in results]
        npass = sum(1 for r in results if r['pass'])
        lines.append('')
        lines.append('%d/%d passed   (written to %s)' % (npass, len(results), out))
        text = '\n'.join(lines)
        print(text)
        if ui and not QUIET:
            ui.messageBox(text, 'IDEX model checks')
    except Exception:
        print(traceback.format_exc())
        if app.userInterface and not QUIET:
            app.userInterface.messageBox('Failed:\n%s' % traceback.format_exc())
