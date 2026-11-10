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
  8  PARAMETER COVERAGE - flexes the driving parameters and reports what
     actually followed. This is the one that matters: the model is only
     parametric to the extent this number is high.
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

# parameter, nominal, test value
FLEX = (('build_x', '230 mm', '300 mm'),
        ('build_y', '235 mm', '305 mm'),
        ('upright_h', '500 mm', '570 mm'))


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

        # 1 / 2 - the print surface and the nozzles agree
        for tag in ('A', 'B'):
            h = find('Hotend V6 %s' % tag, 'C - Toolhead %s' % tag)
            z = h[0][3][4] if h else None
            chk('nozzle %s at bed_top' % tag,
                z is not None and abs(z - bed_top) < 0.05,
                'nozzle z=%.2f  bed_top=%.2f' % (z if z is not None else -1, bed_top))
        pei = find('PEI spring steel', 'D - Y and bed')
        chk('PEI top at bed_top', pei and abs(pei[0][3][5] - bed_top) < 0.05,
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
        chk('all brackets touch the frame', not floating,
            '%d brackets, floating: %s' % (n, floating or 'none'))

        # 4 - rails land on a slot, not between two
        ao = root.allOccurrences
        beam = next((ao.item(i) for i in range(ao.count)
                     if ao.item(i).name.split(':')[0] == 'X beam 2040'
                     and ao.item(i).bRepBodies.count), None)
        if beam:
            centres = slot_centres(beam, lambda v: P(26.0, 20.7, v / 10.0), 167.0, 209.0)
            xr = find('MGN12 rail 520', 'B - X gantry')
            xc = (xr[0][3][4] + xr[0][3][5]) / 2.0 if xr else -1
            chk('X rail centred on a beam slot',
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
        chk('interference is the known set only', sorted(vols) == EXPECTED_INTERFERENCE,
            '%d found: %s' % (res.count, sorted(vols, reverse=True)))

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

        # 7 - parking
        bx0 = pv('frame_w') / 2 - pv('build_x') / 2
        bx1 = pv('frame_w') / 2 + pv('build_x') / 2
        for tag in ('A', 'B'):
            h = find('Hotend V6 %s' % tag, 'C - Toolhead %s' % tag)
            nx = (h[0][3][0] + h[0][3][1]) / 2.0
            chk('toolhead %s parks clear of the build area' % tag,
                nx < bx0 - 1 or nx > bx1 + 1,
                'nozzle x=%.1f, build area %.1f..%.1f' % (nx, bx0, bx1))

        # 8 - the one that matters: does anything follow the parameters?
        def snap():
            return {'%s|%d' % (p[0], p[2]): p[3] for p in part_list(root)}

        coverage = {}
        for pname, nominal, test in FLEX:
            base = snap()
            up.itemByName(pname).expression = test
            des.computeAll()
            adsk.doEvents()
            after = snap()
            moved, pinned = set(), set()
            for k, a in base.items():
                b = after.get(k)
                if b is None:
                    continue
                (moved if max(abs(b[i] - a[i]) for i in range(6)) > 0.5
                 else pinned).add(k.split('|')[0])
            up.itemByName(pname).expression = nominal
            des.computeAll()
            adsk.doEvents()
            total = len(moved) + len(pinned)
            pct = 100.0 * len(moved) / total if total else 0.0
            coverage[pname] = pct
            chk('parameter coverage: %s' % pname, pct > 90.0,
                '%.0f%% followed (%d of %d parts)' % (pct, len(moved), total))

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
        if ui:
            ui.messageBox(text, 'IDEX model checks')
    except Exception:
        if app.userInterface:
            app.userInterface.messageBox('Failed:\n%s' % traceback.format_exc())
