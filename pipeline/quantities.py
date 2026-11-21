"""Item list with bounding boxes for each plan (used for the cost estimate).
python3 quantities.py plan_d  -> prints name, layer, bbox; quantities.items(plan) returns the list."""
import sys, json, math
import export


import planlib
_L = {}
_setup = planlib.setup
def _cap(L, LQ):
    _L['L'] = L; _L['down'] = {}; _L['cove'] = {}
    c = _setup(L, LQ)
    dl, sl = c.downlights, c.SLABH
    def downlights(it, pts, z):
        _L['down'][it['name']] = _L['down'].get(it['name'], 0) + len(pts); return dl(it, pts, z)
    def slabh(it, o, h, z0, z1, m, mh):
        if mh == 'cove' and h:
            per = sum(math.dist(h[i], h[(i + 1) % len(h)]) for i in range(len(h)))
            _L['cove'][it['name']] = _L['cove'].get(it['name'], 0) + per
        return sl(it, o, h, z0, z1, m, mh)
    c.downlights = downlights; c.SLABH = slabh
    return c
planlib.setup = _cap
export.planlib.setup = _cap


def names(modname):
    """All item names with their layers (including items made only of extrusions, which have no boxes)."""
    export.build_plan(modname)
    return [(it['name'], it['layer']) for it in _L['L']['ITEMS']]


def extras():
    """After items()/names(): downlight counts and cove perimeters (mm) per item, LED strip length (mm) per item."""
    led = {}
    for it in _L['L']['ITEMS']:
        for b in it['boxes'].get('led', []):
            dx, dy = abs(b[1] - b[0]), abs(b[3] - b[2])
            led[it['name']] = led.get(it['name'], 0) + max(dx, dy)
    return dict(_L['down']), dict(_L['cove']), led


def items(modname):
    chunks, mats, boxes, mod = export.build_plan(modname)
    import core
    st_items = []
    L = None
    # build_plan leaves the item list on the planlib layer table; collect boxes per item name from the returned boxes
    agg = {}
    for (name, b, layer) in boxes:
        x0, x1, y0, y1, z0, z1 = b[:6]
        a = agg.setdefault((name, layer), [1e9, -1e9, 1e9, -1e9, 1e9, -1e9])
        a[0] = min(a[0], x0, x1); a[1] = max(a[1], x0, x1); a[2] = min(a[2], y0, y1); a[3] = max(a[3], y0, y1); a[4] = min(a[4], z0, z1); a[5] = max(a[5], z0, z1)
    hide = set()
    modes = getattr(mod, 'MODES', {})
    if modes: hide = set(list(modes.values())[0]['hide'])
    out = []
    for (name, layer), a in agg.items():
        out.append({'name': name, 'layer': layer, 'hidden': layer in hide, 'x0': a[0], 'x1': a[1], 'y0': a[2], 'y1': a[3], 'z0': a[4], 'z1': a[5]})
    return out, mod


if __name__ == '__main__':
    its, mod = items(sys.argv[1])
    for i in sorted(its, key=lambda d: (d['layer'], d['name'])):
        print('%-62s %-16s %s x%5d-%5d y%5d-%5d z%4d-%4d' % (i['name'][:62], i['layer'][:16], 'H' if i['hidden'] else ' ', i['x0'], i['x1'], i['y0'], i['y1'], i['z0'], i['z1']))
