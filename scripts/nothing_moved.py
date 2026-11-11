"""Nothing-moved check for the skeleton rewire.

Compares every part's world bounding box with a baseline written before the
rewire started. Run inside Fusion (script tool). Set BASELINE to the baseline
JSON path. Prints every part that moved more than TOL mm and a one-line verdict.

    BASELINE = r'...\before.json'; DETAIL = r'...\before_detail.json'
    exec(open(r'...\scripts\nothing_moved.py').read()); nothing_moved()
"""
import json
import adsk.core, adsk.fusion

TOL = 0.05  # mm


def _box(o):
    b = o.boundingBox
    vals = [b.minPoint.x, b.minPoint.y, b.minPoint.z, b.maxPoint.x, b.maxPoint.y, b.maxPoint.z]
    if all(abs(v) < 1e-9 for v in vals):  # stale box straight after computeAll: rebuild from bodies
        mn = [1e9] * 3; mx = [-1e9] * 3
        for i in range(o.bRepBodies.count):
            bb = o.bRepBodies.item(i).boundingBox
            for k, v in enumerate([bb.minPoint.x, bb.minPoint.y, bb.minPoint.z]): mn[k] = min(mn[k], v)
            for k, v in enumerate([bb.maxPoint.x, bb.maxPoint.y, bb.maxPoint.z]): mx[k] = max(mx[k], v)
        vals = mn + mx
    return [round(v * 10, 2) for v in vals]


def _tf(o):
    m = o.transform2
    return [round(m.getCell(r, c) * (10 if c == 3 else 1), 3) for r in range(3) for c in range(4)]


def _vol(o):
    return round(sum(o.bRepBodies.item(i).volume for i in range(o.bRepBodies.count)) * 1000, 1)


def snapshot_detail(path):
    """Write transform + volume per baselined part (second baseline, for loose boxes)."""
    base = json.load(open(BASELINE))
    des = adsk.fusion.Design.cast(adsk.core.Application.get().activeProduct)
    out = {}
    for o in des.rootComponent.allOccurrences:
        key = o.fullPathName.replace('+', '/')
        if key in base:
            out[key] = {'tf': _tf(o), 'vol': _vol(o)}
    json.dump(out, open(path, 'w'), indent=0)
    print('detail baseline: %d parts written' % len(out))


def nothing_moved(baseline=None, verbose=True):
    """A part passes if its world box matches the baseline, or - for curved parts
    whose box Fusion reports loosely - if its transform AND volume both match."""
    base = json.load(open(baseline or BASELINE))
    try:
        detail = json.load(open(DETAIL))
    except Exception:
        detail = {}
    des = adsk.fusion.Design.cast(adsk.core.Application.get().activeProduct)
    now = {}
    for o in des.rootComponent.allOccurrences:
        key = o.fullPathName.replace('+', '/')
        if key in base:
            now[key] = _box(o)
    moved, missing = [], [k for k in base if k not in now]
    for k, v in now.items():
        d = max(abs(a - b) for a, b in zip(v, base[k]))
        if d > TOL and k in detail:
            o = [x for x in des.rootComponent.allOccurrences if x.fullPathName.replace('+', '/') == k][0]
            same_tf = max(abs(a - b) for a, b in zip(_tf(o), detail[k]['tf'])) < 0.01
            same_vol = abs(_vol(o) - detail[k]['vol']) < 0.5
            if same_tf and same_vol:
                continue
        if d > TOL:
            moved.append((d, k, base[k], v))
    moved.sort(reverse=True)
    if verbose:
        for d, k, b, v in moved:
            print('MOVED %.2f  %s\n      was %s\n      now %s' % (d, k, b, v))
        for k in missing:
            print('MISSING  %s' % k)
    print('nothing_moved: %d parts checked, %d moved, %d missing -> %s' % (
        len(now), len(moved), len(missing), 'PASS' if not moved and not missing else 'FAIL'))
    return not moved and not missing
