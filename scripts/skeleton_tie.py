"""Tie parts to the Skeleton without moving them.

Run inside Fusion (script tool):
    exec(open(r'...\scripts\skeleton_tie.py').read())
    BASELINE = r'...\before.json'
    tie_all(SPEC)        # SPEC: {occurrence path: (modes, xbase, ybase, zbase)}

For each part:
  1. Its anchor point p is read from the part's current world box per axis
     ('o' = the part's own origin, 'min' / 'mid' / 'max' of its box).
  2. Each coordinate becomes a Skeleton construction plane at
     `<base expression> + <offset>`, the offset being whatever makes the plane
     land on p today. Planes are shared between parts with the same expression.
  3. An anchor point sits at the three planes' intersection.
  4. A seat (joint origin) is added to the Skeleton on that anchor, oriented to
     the part's current rotation and offset to the part's origin. The seat is
     checked in world coordinates before anything is jointed.
  5. A rigid joint ties the part's own origin to the seat. The part's transform
     is compared before/after; any movement aborts the whole run (Fusion rolls
     a failed script back).

Seats live on the Skeleton, so referenced (read-only) bought parts tie the same
way as native ones. Units: Fusion API is cm; everything printed is mm.
"""
import itertools
import adsk.core, adsk.fusion

VIS = adsk.core.ValueInput.createByString


def _des():
    return adsk.fusion.Design.cast(adsk.core.Application.get().activeProduct)


def _skel():
    root = _des().rootComponent
    return [o for o in root.occurrences if o.name.startswith('Skeleton')][0]


def _occ(path):
    for o in _des().rootComponent.allOccurrences:
        if o.fullPathName.replace('+', '/') == path:
            return o
    raise Exception('no occurrence ' + path)


def _base_box(path):
    """World box in cm from the baseline (live boxes go stale inside a script)."""
    import json
    v = json.load(open(BASELINE))[path]
    return [x / 10 for x in v[:3]], [x / 10 for x in v[3:]]


def _eval(expr):
    """Value of a length expression in cm, via a scratch parameter."""
    up = _des().userParameters
    p = up.itemByName('_tie_eval')
    if p is None:
        p = up.add('_tie_eval', VIS(expr), 'mm', 'scratch - deleted after tie run')
    else:
        p.expression = expr
    return p.value


def _expr(base, offset_mm):
    off = round(offset_mm, 3)
    if abs(off) < 0.0005:
        return base
    if base.strip() == '0 mm':
        return '%s mm' % ('%.3f' % off).rstrip('0').rstrip('.')
    b = base if base.replace('_', '').isalnum() else '( %s )' % base
    return '%s %s %s mm' % (b, '+' if off > 0 else '-', ('%.3f' % abs(off)).rstrip('0').rstrip('.'))


def _plane(axis, expr):
    s = _skel().component
    name = '%s: %s' % (axis, expr)
    for i in range(s.constructionPlanes.count):
        pl = s.constructionPlanes.item(i)
        if pl.name == name:
            return pl
    base = {'X': s.yZConstructionPlane, 'Y': s.xZConstructionPlane, 'Z': s.xYConstructionPlane}[axis]
    pi = s.constructionPlanes.createInput()
    pi.setByOffset(base, VIS(expr))
    pl = s.constructionPlanes.add(pi)
    pl.name = name
    return pl


def _same(v, w, tol=1e-6):
    return abs(v.x - w.x) < tol and abs(v.y - w.y) < tol and abs(v.z - w.z) < tol


def _rot_diff(a, b):
    return max(abs(a.getCell(r, c) - b.getCell(r, c)) for r in range(3) for c in range(3))


def _full_diff(a, b):
    return max(abs(a.getCell(r, c) - b.getCell(r, c)) for r in range(3) for c in range(4))


def _seat_and_joint(name, anchor, o, m0):
    """Find a seat on `anchor` that holds `o` at exactly m0, joint it, return the joint.

    JointOrigin.geometry does not report flip/angle/axis settings, so each
    candidate seat is proven by jointing and comparing the part's rotation.
    """
    root = _des().rootComponent
    sko = _skel(); s = sko.component
    axes = [s.xConstructionAxis, s.yConstructionAxis, s.zConstructionAxis]
    combos = [(None, None)] + list(itertools.permutations(range(3), 2))
    pg = adsk.fusion.JointGeometry.createByPoint(
        o.component.originConstructionPoint.createForAssemblyContext(o))
    tried = 0
    for (zi, xi), flip, ang in itertools.product(combos, (False, True), (0, 90, 180, 270)):
        ji = s.jointOrigins.createInput(adsk.fusion.JointGeometry.createByPoint(anchor))
        if zi is not None:
            ji.zAxisEntity = axes[zi]
            ji.xAxisEntity = axes[xi]
        ji.isFlipped = flip
        if ang:
            ji.angle = VIS('%d deg' % ang)
        try:
            jo = s.jointOrigins.add(ji)
        except Exception:
            continue
        tried += 1
        jin = root.joints.createInput(pg, jo.createForAssemblyContext(sko))
        jin.setAsRigidJointMotion()
        try:
            j = root.joints.add(jin)
        except Exception:
            jo.deleteMe(); continue
        if _rot_diff(o.transform2, m0) < 1e-5:
            break
        j.deleteMe(); jo.deleteMe()
    else:
        raise Exception('no seat orientation holds %s (%d tried)' % (name, tried))
    jo.name = 'seat ' + name
    j.name = '%s -> skeleton' % name
    # offset the seat from the anchor to the part origin; the axis convention
    # is proven the same way, by the part landing back on m0
    m1 = o.transform2
    d = [m0.getCell(r, 3) - m1.getCell(r, 3) for r in range(3)]
    local = [sum(m1.getCell(r, c) * d[r] for r in range(3)) for c in range(3)]
    for vec in (local, d, [-x for x in local], [-x for x in d]):
        jo.offsetX.expression = '%.4f mm' % (vec[0] * 10)
        jo.offsetY.expression = '%.4f mm' % (vec[1] * 10)
        jo.offsetZ.expression = '%.4f mm' % (vec[2] * 10)
        _des().computeAll()
        if _full_diff(o.transform2, m0) < 1e-5:
            return j
    raise Exception('seat offset convention not found for ' + name)


def tie(path, modes, xb, yb, zb):
    des = _des(); root = des.rootComponent
    sko = _skel(); s = sko.component
    o = _occ(path)
    m0 = o.transform2
    T = m0.translation
    if isinstance(modes, str):
        modes = [modes] * 3 if ',' not in modes else modes.split(',')
    mn, mx = _base_box(path) if any(m != 'o' for m in modes) else (None, None)
    target = []
    for k, mode in enumerate(modes):
        if mode == 'o':
            target.append([T.x, T.y, T.z][k])
        else:
            target.append({'min': mn[k], 'max': mx[k], 'mid': (mn[k] + mx[k]) / 2}[mode])
    planes, exprs = [], []
    for k, (axis, base) in enumerate(zip('XYZ', (xb, yb, zb))):
        e = _expr(base, (target[k] - _eval(base)) * 10)
        if abs(_eval(e) - target[k]) > 1e-4:
            raise Exception('%s %s: %s evaluates to %.3f, want %.3f' % (path, axis, e, _eval(e) * 10, target[k] * 10))
        exprs.append(e); planes.append(_plane(axis, e))
    short = path.split('/')[-1]
    pi = s.constructionPoints.createInput()
    pi.setByThreePlanes(*planes)
    ap = s.constructionPoints.add(pi)
    ap.name = 'a ' + short
    _seat_and_joint(short, ap, o, m0)
    d = _full_diff(o.transform2, m0)
    if d > 1e-5:
        raise Exception('%s moved by %.4f when jointed' % (path, d * 10))
    print('  tied %-48s at (%s | %s | %s)' % (path, exprs[0], exprs[1], exprs[2]))


def tie_all(spec):
    for path, v in spec.items():
        tie(path, *v)
    p = _des().userParameters.itemByName('_tie_eval')
    if p:
        p.deleteMe()
    _des().computeAll()
