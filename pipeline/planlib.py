# Shared building blocks for the layout plans (browser-viewer rebuild).
import math
class Ctx:
    pass

def _offset(pts, d):
    """Offset a closed polygon by d mm (d > 0 grows it, d < 0 shrinks it), mitred and clamped."""
    n = len(pts); ar = sum(pts[i][0] * pts[(i + 1) % n][1] - pts[(i + 1) % n][0] * pts[i][1] for i in range(n))
    sg = 1 if ar > 0 else -1; out = []
    for i in range(n):
        p0, p1, p2 = pts[i - 1], pts[i], pts[(i + 1) % n]
        def nrm(a, b):
            dx, dy = b[0] - a[0], b[1] - a[1]; L = math.hypot(dx, dy) or 1.0
            return (dy / L * sg, -dx / L * sg)
        n1, n2 = nrm(p0, p1), nrm(p1, p2); bx, by = n1[0] + n2[0], n1[1] + n2[1]; bl = math.hypot(bx, by)
        if bl < 1e-6: bx, by, bl = n1[0], n1[1], 1.0
        bx, by = bx / bl, by / bl; cosh = max(0.35, bx * n1[0] + by * n1[1])
        out.append((round(p1[0] + bx * d / cosh, 1), round(p1[1] + by * d / cosh, 1)))
    return out

def _dedupe(pts):
    out = []
    for p in pts:
        if not out or abs(p[0] - out[-1][0]) + abs(p[1] - out[-1][1]) > 0.5: out.append(p)
    if len(out) > 2 and abs(out[0][0] - out[-1][0]) + abs(out[0][1] - out[-1][1]) <= 0.5: out.pop()
    return out

CEIL = 'wave'      # false-ceiling concept: 'wave' (default) or the name of a ceil_<name>.py module
def pip(pt, poly):
    """Point-in-polygon test."""
    x, y = pt; ins = False; n = len(poly)
    for i in range(n):
        x0, y0 = poly[i]; x1, y1 = poly[(i + 1) % n]
        if (y0 > y) != (y1 > y) and x < (x1 - x0) * (y - y0) / (y1 - y0) + x0: ins = not ins
    return ins

def bbox(poly):
    xs = [p[0] for p in poly]; ys = [p[1] for p in poly]; return min(xs), max(xs), min(ys), max(ys)

def cove(c, raw, it, outer, hole, z0, z1, wall_gap=True):
    """Standard recessed cove: the dropped ceiling `outer` (underside z0) with one recess `hole` up to z1.
    Builds the 50 mm lip, hidden LED pocket, light wash on the recessed soffit and the shadow gap at the walls."""
    outer, hole = _dedupe(outer), _dedupe(hole)
    it.setdefault('_holes', []).append(hole)
    zl = z0 + 50
    raw(it, outer, hole, z0, zl, 'fceil', 'fceil')                    # lip (white edge, no glow)
    raw(it, outer, _offset(hole, 80), zl, z1, 'fceil', 'cove')        # glowing back face of the light pocket
    raw(it, _offset(hole, 60), _offset(hole, 25), zl, zl + 4, 'led', 'led')   # LED strip lying on the lip
    raw(it, hole, _offset(hole, -140), z1 - 3, z1 - 1, 'glow1', 'glow1')     # light wash on the soffit
    raw(it, _offset(hole, -140), _offset(hole, -360), z1 - 3, z1 - 1, 'glow2', 'glow2')
    if wall_gap: raw(it, outer, _offset(outer, -15), z0 - 2, z0, 'reveal', 'reveal')      # shadow gap line at the walls

def fceil_slab(c, _orig, it, outer, hole, z0, z1, m, mh):
    if m != 'fceil' or mh != 'cove' or not hole:
        return _orig(it, outer, hole, z0, z1, m, mh)
    n0 = len(it.get('_holes', []))
    if CEIL != 'wave':
        import importlib
        importlib.import_module('ceil_' + CEIL).build(c, _orig, it, _dedupe(outer), _dedupe(hole), z0, z1)
    else:
        cove(c, _orig, it, outer, hole, z0, z1)
    # optional timber slats lining the recess (own layer, switched on/off in the viewer)
    wood_recess(c, it['name'], it.get('_holes', [])[n0:], z1)


def _clip(poly, axis, val, keep_above):
    """Clip a polygon to one side of the line x = val (axis 0) or y = val (axis 1)."""
    out = []
    inside = (lambda p: p[axis] >= val) if keep_above else (lambda p: p[axis] <= val)
    for i in range(len(poly)):
        a, b = poly[i - 1], poly[i]
        if inside(b):
            if not inside(a): out.append(_cross(a, b, axis, val))
            out.append(b)
        elif inside(a): out.append(_cross(a, b, axis, val))
    return out

def _cross(a, b, axis, val):
    t = (val - a[axis]) / ((b[axis] - a[axis]) or 1e-9)
    return (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)

def _area(poly):
    return abs(sum(poly[i - 1][0] * poly[i][1] - poly[i][0] * poly[i - 1][1] for i in range(len(poly)))) / 2

def wood_recess(c, name, holes, z1, slat=80, gap=15):
    """Timber slats (80 mm, 15 mm dark gaps) lining each ceiling recess, running along its long side."""
    if not holes: return
    it = c.item(name + '_Wood_Slats', 'Ceiling_Wood')
    for h in holes:
        inner = _offset(_dedupe(h), -30)
        if len(inner) < 3 or _area(inner) < 40000: continue
        c.PRZ(it, inner, z1 - 6, z1 - 4, 'charcoal')                        # dark backing seen through the gaps
        x0, x1, y0, y1 = bbox(inner)
        axis = 1 if (x1 - x0) >= (y1 - y0) else 0                          # slats run along the long side
        lo, hi = (y0, y1) if axis == 1 else (x0, x1)
        v = lo
        while v < hi:
            piece = _clip(_clip(inner, axis, v, True), axis, min(hi, v + slat), False)
            if len(piece) >= 3 and _area(piece) > 400: c.PRZ(it, _dedupe(piece), z1 - 14, z1 - 6, 'walnut')
            v += slat + gap

def trimless_downlights(c, it, pts, z):
    for (x, y) in pts:
        if any(pip((x, y), _offset(h, 110)) for h in it.get('_holes', [])): continue      # would hang in a recess
        c.CYL(it, x, y, 42, z - 2, z, 'reveal', 20); c.CYL(it, x, y, 34, z - 3, z - 2, 'lightw', 20)

STYLE = 'lux'      # furniture family: lux | japandi | scandi | midcentury | industrial | classic
def _sty(name):
    """Return the furniture builder `name` from style_<STYLE>.py, or None to use the default (lux) one."""
    if STYLE == 'lux': return None
    import importlib
    return getattr(importlib.import_module('style_' + STYLE), name, None)

def dining_pendant(c, it, x0, x1, yc):
    """Pendant over the dining table: spans x0..x1 at y=yc, hangs from the 2550 false ceiling, underside ~1645."""
    f = _sty('dining_pendant')
    if f: return f(c, it, x0, x1, yc)
    c.PRZ(it, c.RRECT(x0, x1, yc - 25, yc + 25, 25, 4), 1650, 1690, 'brass'); c.B(it, x0 + 20, x1 - 20, yc - 17, yc + 17, 1645, 1650, 'lightw')
    for x in (x0 + (x1 - x0) * 0.34, x0 + (x1 - x0) * 0.88):
        c.CYL(it, x, yc, 3, 1690, 2550, 'metal', 6)

def bedside_pendant(c, it, cx, cy):
    f = _sty('bedside_pendant')
    if f: return f(c, it, cx, cy)
    CYL = c.CYL
    CYL(it, cx, cy, 45, 2550, 2560, 'gold', 16); CYL(it, cx, cy, 4, 1330, 2550, 'metal', 8); CYL(it, cx, cy, 35, 1300, 1330, 'gold', 16)
    for (z0, z1, rr) in ((1100, 1130, 70), (1130, 1170, 105), (1170, 1240, 122), (1240, 1280, 105), (1280, 1300, 70)): CYL(it, cx, cy, rr, z0, z1, 'lightw', 20)


def _ring(cx, cy, z, r, n=20):
    return [(cx + r * math.cos(2 * math.pi * k / n), cy + r * math.sin(2 * math.pi * k / n), z) for k in range(n)]

def _frustum(it, cx, cy, z0, r0, z1, r1, m, n=20):
    _loft(it, _ring(cx, cy, z0, r0, n), _ring(cx, cy, z1, r1, n), m)

def bedside_sconce(c, it, wx, cy, side=-1, z=1250):
    """Wall-mounted bedside light. wx = wall face x, side = direction into the room (-1 = towards smaller x).
    The style follows the active furniture family."""
    CYL, B = c.CYL, c.B
    S = STYLE
    plate, armm = {'japandi': ('oak', 'oak'), 'scandi': ('white', 'oak'), 'midcentury': ('brass', 'brass'),
                   'industrial': ('blksteel', 'blksteel'), 'classic': ('brass', 'brass')}.get(S, ('gold', 'gold'))
    reach = 190; sx = wx + side * reach                         # shade centre x
    # wall plate (rounded, in the y-z plane)
    c.PR3(it, c.RRECT(-42, 42, -70, 70, 40, 5), (wx, cy, z + 120), (0, 1, 0), (0, 0, 1), (side, 0, 0), 0, 14, plate)
    # arm: horizontal rod out from the plate, then a short drop to the shade
    a0, a1 = sorted((wx + side * 14, sx)); B(it, a0, a1, cy - 6, cy + 6, z + 114, z + 126, armm)
    CYL(it, sx, cy, 6, z + 60, z + 126, armm, 8)
    if S == 'japandi':        # small paper cylinder lantern
        _frustum(it, sx, cy, z - 110, 62, z - 95, 74, 'paper'); _frustum(it, sx, cy, z - 95, 74, z + 35, 74, 'paper'); _frustum(it, sx, cy, z + 35, 74, z + 55, 60, 'paper')
        CYL(it, sx, cy, 30, z + 55, z + 62, 'oak', 12)
    elif S == 'scandi':       # white metal dome facing down
        _frustum(it, sx, cy, z - 70, 100, z - 20, 90, 'white'); _frustum(it, sx, cy, z - 20, 90, z + 30, 55, 'white'); _frustum(it, sx, cy, z + 30, 55, z + 60, 18, 'white')
        CYL(it, sx, cy, 92, z - 66, z - 62, 'lightw', 20)
    elif S == 'midcentury':   # opal globe with a brass cap
        for (z0, z1, r) in ((-95, -75, 45), (-75, -45, 78), (-45, 0, 92), (0, 30, 80), (30, 50, 52)): CYL(it, sx, cy, r, z + z0, z + z1, 'lightw', 18)
        CYL(it, sx, cy, 34, z + 50, z + 62, 'brass', 14)
    elif S == 'industrial':   # black metal cone shade
        _frustum(it, sx, cy, z - 80, 105, z + 30, 40, 'blksteel'); CYL(it, sx, cy, 40, z + 30, z + 62, 'blksteel', 14)
        CYL(it, sx, cy, 96, z - 76, z - 72, 'lightw', 20)
    elif S == 'classic':      # pleated empire fabric shade with brass trim
        _frustum(it, sx, cy, z - 90, 105, z + 40, 70, 'artbg', 28); CYL(it, sx, cy, 106, z - 94, z - 88, 'brass', 28)
        CYL(it, sx, cy, 98, z - 86, z - 82, 'lightw', 20); CYL(it, sx, cy, 18, z + 40, z + 62, 'brass', 10)
    else:                     # modern lux: opal cylinder with champagne-brass rings
        CYL(it, sx, cy, 62, z - 100, z + 50, 'lightw', 20); CYL(it, sx, cy, 66, z - 104, z - 96, 'gold', 20); CYL(it, sx, cy, 66, z + 46, z + 62, 'gold', 20)

def setup(L, LQ):
    c = Ctx()
    for k, v in L.items(): setattr(c, k, v)
    for k, v in LQ.items(): setattr(c, k, v)
    M = L['MATS']
    M['onyx'] = ('Onyx_Backlit_Honey', 238, 214, 168, 255)
    M['artm'] = ('Art_Marble_Gold_Vein', 232, 229, 223, 255)
    M['artw'] = ('Art_Abstract_Sand_Wash', 214, 196, 170, 255)
    M['power'] = ('Power_Point_White', 250, 250, 250, 255)
    M['pwrmark'] = ('Power_Point_Marker_Orange', 240, 120, 40, 255)
    M['trunk'] = ('Aircon_Trunking_Indicative', 120, 170, 230, 255)
    M['acoustic'] = ('Acoustic_Panel_Felt_Greige', 160, 152, 142, 255)
    M['wallk'] = ('Wall_Paint_White', 243, 243, 241, 255)
    M['pil1'] = ('Cushion_Linen_Taupe', 196, 182, 160, 255)
    M['pil2'] = ('Cushion_Velvet_Caramel', 170, 120, 80, 255)
    M['towel'] = ('Towel_Oat_Cotton', 226, 216, 198, 255)
    M['sculpt'] = ('Sculpture_Bronze', 140, 105, 70, 255)
    M['display'] = ('Monitor_Display_Blue_Grey', 46, 62, 86, 255)
    M['leather2'] = ('Leather_Cognac_Dining', 168, 104, 64, 255)
    M['boucle_g'] = ('Boucle_Sage_Green', 120, 140, 108, 255)
    M['mustard'] = ('Bedding_Mustard_Stripe', 208, 164, 92, 255)
    M['leather3'] = ('Leather_Cognac_Piping', 122, 72, 42, 255)
    M['glow1'] = ('Cove_Wash_Warm', 255, 238, 212, 255)
    M['glow2'] = ('Cove_Wash_Soft', 252, 246, 236, 255)
    M['reveal'] = ('Shadow_Gap_Reveal', 112, 110, 106, 255)
    _sl = c.SLABH; c.SLABH = lambda it, o, h, z0, z1, m, mh: fceil_slab(c, _sl, it, o, h, z0, z1, m, mh)
    c.downlights = lambda it, pts, z: trimless_downlights(c, it, pts, z)
    c.station = lambda it, face, cx, cy, D: station3(c, it, face, cx, cy, D)
    M['blksteel'] = ('Black_Steel_Powdercoat', 34, 34, 36, 255)
    M['cane'] = ('Rattan_Cane_Natural', 206, 176, 128, 255)
    M['paper'] = ('Paper_Shade_Washi', 250, 244, 228, 255)
    M['oakd'] = ('Oak_Smoked_Mid', 150, 112, 76, 255)
    c.sofa2 = lambda *a, **k: (_sty('sofa') or sofa3)(c, *a, **k)
    _ns = c.nightstand
    c.nightstand = lambda it, x0, x1, y0, y1: (_sty('nightstand')(c, it, x0, x1, y0, y1) if _sty('nightstand') else _ns(it, x0, x1, y0, y1))
    return c

# ---------- small helpers ----------
def aircon2(c, it, axis, wall, s, a0, a1, z0=2300):
    B = c.B
    if axis == 'y':
        B(it, a0, a1, wall, wall + s * 215, z0, z0 + 300, 'appl'); B(it, a0 + 40, a1 - 40, wall + s * 205, wall + s * 220, z0 + 15, z0 + 45, 'metal')
    else:
        B(it, wall, wall + s * 215, a0, a1, z0, z0 + 300, 'appl'); B(it, wall + s * 205, wall + s * 220, a0 + 40, a1 - 40, z0 + 15, z0 + 45, 'metal')

def painting(c, it, axis, plane, side, a0, a1, z0, z1, mat='artm'):
    """Framed canvas on a wall. axis='x' -> wall plane x=plane, canvas spans y a0..a1. side = direction into room."""
    B = c.B
    t = 35
    if axis == 'x':
        p0, p1 = sorted([plane, plane + side * t]); q0, q1 = sorted([plane, plane + side * (t - 8)])
        B(it, p0, p1, a0, a1, z0, z0 + 22, 'gold'); B(it, p0, p1, a0, a1, z1 - 22, z1, 'gold')
        B(it, p0, p1, a0, a0 + 22, z0 + 22, z1 - 22, 'gold'); B(it, p0, p1, a1 - 22, a1, z0 + 22, z1 - 22, 'gold')
        B(it, q0, q1, a0 + 22, a1 - 22, z0 + 22, z1 - 22, mat)
        # soft gold veins
        L = a1 - a0; H = z1 - z0
        for (f0, f1, g) in ((0.15, 0.55, 0.35), (0.45, 0.9, 0.62), (0.05, 0.4, 0.8)):
            u0 = a0 + L * f0; u1 = a0 + L * f1; zz = z0 + H * g
            vx = plane + side * (t - 7)
            pts = [(u0, zz), ((u0 + u1) / 2, zz + H * 0.08), (u1, zz + H * 0.02), (u1, zz + H * 0.02 + 6), ((u0 + u1) / 2, zz + H * 0.08 + 7), (u0, zz + 6)]
            c.PR3(it, pts, (vx, 0, 0), (0, 1, 0), (0, 0, 1), (side, 0, 0), 0, 2, 'gold')
    else:
        p0, p1 = sorted([plane, plane + side * t]); q0, q1 = sorted([plane, plane + side * (t - 8)])
        B(it, a0, a1, p0, p1, z0, z0 + 22, 'gold'); B(it, a0, a1, p0, p1, z1 - 22, z1, 'gold')
        B(it, a0, a0 + 22, p0, p1, z0 + 22, z1 - 22, 'gold'); B(it, a1 - 22, a1, p0, p1, z0 + 22, z1 - 22, 'gold')
        B(it, a0 + 22, a1 - 22, q0, q1, z0 + 22, z1 - 22, mat)
        L = a1 - a0; H = z1 - z0
        for (f0, f1, g) in ((0.15, 0.55, 0.35), (0.45, 0.9, 0.62), (0.05, 0.4, 0.8)):
            u0 = a0 + L * f0; u1 = a0 + L * f1; zz = z0 + H * g
            vy = plane + side * (t - 7)
            pts = [(u0, zz), ((u0 + u1) / 2, zz + H * 0.08), (u1, zz + H * 0.02), (u1, zz + H * 0.02 + 6), ((u0 + u1) / 2, zz + H * 0.08 + 7), (u0, zz + 6)]
            c.PR3(it, pts, (0, vy, 0), (1, 0, 0), (0, 0, 1), (0, side, 0), 0, 2, 'gold')

def pillow(c, it, cx, cy, w, d, z0, h, m, along='y'):
    """Soft pillow with a rounded, lens-like profile: footprint w (across bed) x d, height h."""
    if along == 'y':
        base = c.RRECT(cx - d / 2, cx + d / 2, cy - w / 2, cy + w / 2, min(w, d) * 0.42, 6)
    else:
        base = c.RRECT(cx - w / 2, cx + w / 2, cy - d / 2, cy + d / 2, min(w, d) * 0.42, 6)
    n = 6; R = min(w, d) * 0.45
    for i in range(n):
        t0 = i / float(n); t1 = (i + 1) / float(n)
        ins = R * (1 - math.sqrt(max(0.0, 1 - t0 * t0)))
        poly = base if ins < 0.5 else c.inset(base, ins)
        c.PRZ(it, poly, z0 + h * (1 - math.cos(t0 * math.pi / 2)) * 0 + h * t0, z0 + h * t1, m)

def bed2(c, it, x0, x1, y0, y1, head, npil, deco=True):
    f = _sty('bed')
    if f and head in ('+x', '-x'): return f(c, it, x0, x1, y0, y1, head, npil, deco)
    if head in ('+x', '-x'): return bed3(c, it, x0, x1, y0, y1, head, npil, deco)
    """Bed with a simple low upholstered headboard and natural pillows. head: '+x','-x','+y','-y' = side of headboard."""
    B = c.B; RRECT = c.RRECT; PRZ = c.PRZ
    hb = 70
    if head in ('+x', '-x'):
        hx0, hx1 = (x1 - hb, x1) if head == '+x' else (x0, x0 + hb)
        bx0, bx1 = (x0, x1 - hb) if head == '+x' else (x0 + hb, x1)
        PRZ(it, RRECT(hx0, hx1, y0 - 20, y1 + 20, 30, 4), 0, 1050, 'headb')
        B(it, bx0 + 60, bx1 - 60, y0 + 60, y1 - 60, 0, 120, 'metal')
        PRZ(it, RRECT(bx0, bx1, y0, y1, 40, 4), 120, 330, 'headb')
        PRZ(it, RRECT(bx0 + 10, bx1 - 10, y0 + 12, y1 - 12, 60, 5), 330, 540, 'linen')
        L = bx1 - bx0
        if head == '+x':
            PRZ(it, RRECT(bx0 - 20, bx0 + L * 0.7, y0 - 20, y1 + 20, 30, 4), 400, 575, 'duvet'); PRZ(it, RRECT(bx0 + L * 0.06, bx0 + L * 0.3, y0 - 25, y1 + 25, 25, 4), 575, 600, 'throw')
            px = bx1 - 300; px2 = bx1 - 470
        else:
            PRZ(it, RRECT(bx1 - L * 0.7, bx1 + 20, y0 - 20, y1 + 20, 30, 4), 400, 575, 'duvet'); PRZ(it, RRECT(bx1 - L * 0.3, bx1 - L * 0.06, y0 - 25, y1 + 25, 25, 4), 575, 600, 'throw')
            px = bx0 + 300; px2 = bx0 + 470
        W = y1 - y0; pw = (W - 80) / float(npil)
        for i in range(npil):
            cy = y0 + 40 + pw * (i + 0.5)
            pillow(c, it, px, cy, pw - 40, 420, 540, 170, 'linen2', 'y')
            if deco: pillow(c, it, px2, cy, min(pw - 120, 450), 300, 555, 150, 'pil1' if i % 2 == 0 else 'pil2', 'y')
    else:
        hy0, hy1 = (y1 - hb, y1) if head == '+y' else (y0, y0 + hb)
        by0, by1 = (y0, y1 - hb) if head == '+y' else (y0 + hb, y1)
        PRZ(it, RRECT(x0 - 20, x1 + 20, hy0, hy1, 30, 4), 0, 1050, 'headb')
        B(it, x0 + 60, x1 - 60, by0 + 60, by1 - 60, 0, 120, 'metal')
        PRZ(it, RRECT(x0, x1, by0, by1, 40, 4), 120, 330, 'headb')
        PRZ(it, RRECT(x0 + 12, x1 - 12, by0 + 10, by1 - 10, 60, 5), 330, 540, 'linen')
        L = by1 - by0
        if head == '+y':
            PRZ(it, RRECT(x0 - 20, x1 + 20, by0 - 20, by0 + L * 0.7, 30, 4), 400, 575, 'duvet'); py = by1 - 300; py2 = by1 - 470
        else:
            PRZ(it, RRECT(x0 - 20, x1 + 20, by1 - L * 0.7, by1 + 20, 30, 4), 400, 575, 'duvet'); py = by0 + 300; py2 = by0 + 470
        W = x1 - x0; pw = (W - 80) / float(npil)
        for i in range(npil):
            cx = x0 + 40 + pw * (i + 0.5)
            pillow(c, it, cx, py, pw - 40, 420, 540, 170, 'linen2', 'x')
            if deco: pillow(c, it, cx, py2, min(pw - 120, 450), 300, 555, 150, 'pil1' if i % 2 == 0 else 'pil2', 'x')

def sdesk(c, it, face, front, ca, W, D=585):
    """Standing desk (shown at sitting height 750). front = user edge coordinate; ca = centre along the wall."""
    T = c.LF(face, *( (front, ca) if face in ('+x', '-x') else (ca, front) ))
    c.puff(it, c.LP(T, c.RRECT(-W / 2.0, W / 2.0, 0, D, 18, 3)), 722, 750, 'oak', 3, 3)
    for u in (-W / 2.0 + 90, W / 2.0 - 90):
        c.PRZ(it, c.LP(T, c.RRECT(u - 35, u + 35, D / 2.0 - 30, D / 2.0 + 30, 8, 2)), 40, 705, 'metal')
        c.PRZ(it, c.LP(T, c.RRECT(u - 26, u + 26, D / 2.0 - 22, D / 2.0 + 22, 6, 2)), 300, 706, 'steel')
        c.PRZ(it, c.LP(T, c.RRECT(u - 35, u + 35, 30, D - 30, 14, 3)), 0, 40, 'metal')
    c.PRZ(it, c.LP(T, c.RRECT(-W / 2.0 + 90, W / 2.0 - 90, D / 2.0 - 30, D / 2.0 + 30, 6, 2)), 690, 722, 'metal')
    p = T(W / 2.0 - 160, 80); c.B(it, p[0] - 30, p[0] + 30, p[1] - 30, p[1] + 30, 750, 756, 'charcoal')

def floor_lamp(c, it, x, y):
    f = _sty('floor_lamp')
    if f: return f(c, it, x, y)
    c.CYL(it, x, y, 160, 0, 20, 'metal', 24); c.CYL(it, x, y, 12, 20, 1400, 'gold', 10)
    c.CYL(it, x, y, 220, 1400, 1700, 'artbg', 32); c.CYL(it, x, y, 200, 1395, 1400, 'lightw', 28)

def lounge_chair(c, it, cx, cy, face_deg, body='cush', base='walnut'):
    """Low curved lounge chair; face_deg = direction the sitter faces (plan degrees, 0=+x, 90=+y)."""
    f = _sty('lounge_chair')
    if f: return f(c, it, cx, cy, face_deg, body, base)
    a = math.radians(face_deg)
    fx, fy = math.cos(a), math.sin(a)
    for k in range(4):
        ang = a + math.pi / 4 + k * math.pi / 2
        c.CYL(it, cx + 260 * math.cos(ang), cy + 260 * math.sin(ang), 18, 0, 120, 'gold', 10)
    seat = [(cx + 380 * math.cos(2 * math.pi * k / 28), cy + 380 * math.sin(2 * math.pi * k / 28)) for k in range(28)]
    c.PRZ(it, seat, 120, 300, base); c.puff(it, seat, 300, 430, body, 16, 14)
    th = math.degrees(a) + 180
    bc = (cx - fx * 40, cy - fy * 40)
    outer = c.ARC(bc[0], bc[1], 420, th - 95, th + 95, 18); inner = c.ARC(bc[0], bc[1], 300, th + 95, th - 95, 18)
    c.PRZ(it, outer + inner, 300, 760, body)
    o2 = c.ARC(bc[0], bc[1], 420, th - 70, th + 70, 14); i2 = c.ARC(bc[0], bc[1], 320, th + 70, th - 70, 14)
    c.PRZ(it, o2 + i2, 760, 800, body)

def power_point(c, it, axis, plane, side, a, z, data=False):
    B = c.B
    if axis == 'x':
        x0, x1 = sorted([plane, plane + side * 10]); x2, x3 = sorted([plane + side * 10, plane + side * 14])
        B(it, x0, x1, a - 43, a + 43, z - 43, z + 43, 'power'); B(it, x2, x3, a - 18, a + 18, z - 18, z + 18, 'pwrmark')
        if data: B(it, x0, x1, a + 50, a + 136, z - 43, z + 43, 'power'); B(it, x2, x3, a + 80, a + 106, z - 13, z + 13, 'trunk')
    elif axis == 'y':
        y0, y1 = sorted([plane, plane + side * 10]); y2, y3 = sorted([plane + side * 10, plane + side * 14])
        B(it, a - 43, a + 43, y0, y1, z - 43, z + 43, 'power'); B(it, a - 18, a + 18, y2, y3, z - 18, z + 18, 'pwrmark')
        if data: B(it, a + 50, a + 136, y0, y1, z - 43, z + 43, 'power'); B(it, a + 80, a + 106, y2, y3, z - 13, z + 13, 'trunk')
    else:  # floor box at (plane, a)
        B(it, plane - 60, plane + 60, a - 60, a + 60, 0, 6, 'steel'); B(it, plane - 20, plane + 20, a - 20, a + 20, 6, 9, 'pwrmark')

def trunking(c, it, pts, z=2570):
    for i in range(len(pts) - 1):
        (x0, y0), (x1, y1) = pts[i], pts[i + 1]
        if x0 == x1: c.B(it, x0 - 45, x0 + 45, min(y0, y1) - 45, max(y0, y1) + 45, z, z + 60, 'trunk')
        else: c.B(it, min(x0, x1) - 45, max(x0, x1) + 45, y0 - 45, y0 + 45, z, z + 60, 'trunk')

def bifold(c, it, x0, x1, yc, z0, z1, n, state, stack_end='+x', glass='glass'):
    """Bi-fold glass partition along x at y=yc. state 'closed' = drawn across; 'open' = folded stack at one end."""
    B = c.B
    w = (x1 - x0) / float(n); t = 22; fr = 28
    if state == 'closed':
        for i in range(n):
            a = x0 + i * w + 2; b = x0 + (i + 1) * w - 2
            B(it, a, b, yc - t / 2, yc + t / 2, z0, z0 + fr, 'metal'); B(it, a, b, yc - t / 2, yc + t / 2, z1 - fr, z1, 'metal')
            B(it, a, a + fr, yc - t / 2, yc + t / 2, z0 + fr, z1 - fr, 'metal'); B(it, b - fr, b, yc - t / 2, yc + t / 2, z0 + fr, z1 - fr, 'metal')
            B(it, a + fr, b - fr, yc - 4, yc + 4, z0 + fr, z1 - fr, glass)
            hz = (z0 + z1) / 2.0
            if i % 2 == 1: B(it, a + 6, a + 20, yc + t / 2, yc + t / 2 + 25, hz - 120, hz + 120, 'gold')
    else:
        for i in range(n):
            xx = (x1 - 10 - i * (t + 8)) if stack_end == '+x' else (x0 + 10 + i * (t + 8))
            a, b = sorted([xx, xx - t if stack_end == '+x' else xx + t])
            y0, y1 = yc - t / 2, yc - t / 2 + w - 10
            B(it, a, b, y0, y1, z0, z0 + fr, 'metal'); B(it, a, b, y0, y1, z1 - fr, z1, 'metal')
            B(it, a, b, y0, y0 + fr, z0 + fr, z1 - fr, 'metal'); B(it, a, b, y1 - fr, y1, z0 + fr, z1 - fr, 'metal')
            B(it, a + 7, b - 7, y0 + fr, y1 - fr, z0 + fr, z1 - fr, glass)

def blob(cx, cy, a, b, ph, amp, n=48):
    return [(cx + a * (1 + amp * (0.6 * math.sin(2 * (2 * math.pi * k / n) + ph) + 0.4 * math.sin(3 * (2 * math.pi * k / n) + 2 * ph))) * math.cos(2 * math.pi * k / n),
             cy + b * (1 + amp * (0.6 * math.sin(2 * (2 * math.pi * k / n) + ph) + 0.4 * math.sin(3 * (2 * math.pi * k / n) + 2 * ph))) * math.sin(2 * math.pi * k / n)) for k in range(n)]

def ppebble(c, it, cx, cy, a, b, ph, ztop, mtop, mbase, fl=True):
    f = _sty('coffee_table')
    if f: return f(c, it, cx, cy, a, b, ztop)
    top = blob(cx, cy, a, b, ph, 0.08, 56)
    c.PRZ(it, top, ztop - 38, ztop, mtop); c.PRZ(it, c.inset(top, 8), ztop - 42, ztop - 38, 'gold')
    base = blob(cx, cy, a * 0.62, b * 0.62, ph, 0.08, 40); c.PRZ(it, base, 0, ztop - 42, mbase)
    if fl:
        for (x, y) in base: c.CYL(it, x, y, 16, 0, ztop - 42, mbase + '2', 8)

def rbox(c, it, cx, cy, L, T, ang, z0, z1, m, du=0.0, dv=0.0):
    """Box rotated in plan: length L along angle ang (deg), thickness T, offset du (along) / dv (across) from centre."""
    a = math.radians(ang); ux, uy = math.cos(a), math.sin(a); vx, vy = -uy, ux
    ox, oy = cx + ux * du + vx * dv, cy + uy * du + vy * dv
    pts = [(ox + ux * su * L / 2 + vx * sv * T / 2, oy + uy * su * L / 2 + vy * sv * T / 2) for (su, sv) in ((-1, -1), (1, -1), (1, 1), (-1, 1))]
    c.PRZ(it, pts, z0, z1, m)

def wallbed_folded(c, it, x0, x1, y0, y1):
    B = c.B
    B(it, x0, x1, y0, y1, 0, 60, 'charcoal'); B(it, x0 + 20, x1, y0, y0 + 20, 60, 2170, 'greige'); B(it, x0 + 20, x1, y1 - 20, y1, 60, 2170, 'greige')
    B(it, x0 + 20, x1, y0, y1, 2150, 2170, 'greige'); B(it, x0, x0 + 22, y0 + 3, y1 - 3, 60, 2147, 'greige')
    B(it, x0 - 4, x0, y0 + 60, y1 - 60, 1150, 1170, 'gold')
    for z in (700, 1400): B(it, x0 - 2, x0, y0 + 20, y1 - 20, z, z + 3, 'charcoal')

def wallbed_down(c, it, x0, x1, y0, y1, foot):
    B, PRZ, RRECT = c.B, c.PRZ, c.RRECT
    B(it, x0, x1, y0, y1, 0, 60, 'charcoal'); B(it, x0 + 20, x1, y0, y0 + 20, 60, 2170, 'greige'); B(it, x0 + 20, x1, y1 - 20, y1, 60, 2170, 'greige')
    B(it, x0 + 20, x1, y0, y1, 2150, 2170, 'greige'); B(it, x1 - 20, x1, y0 + 20, y1 - 20, 60, 2150, 'greige')
    B(it, foot, x0 + 40, y0 + 25, y1 - 25, 330, 352, 'greige')        # fold-down panel (underside of bed)
    B(it, foot, foot + 40, y0 + 60, y1 - 60, 0, 330, 'metal')         # fold-out legs
    soft_slab(c, it, RRECT(foot + 10, x0 + 30, y0 + 40, y1 - 40, 60, 5), 352, 560, 'linen', 40, 3)
    dx1 = foot + (x0 - foot) * 0.7
    soft_slab(c, it, RRECT(foot - 20, dx1, y0 + 10, y1 - 10, 30, 4), 540, 600, 'duvet', 25, 2)
    B(it, foot - 20, dx1, y0 - 4, y0 + 18, 320, 570, 'duvet'); B(it, foot - 20, dx1, y1 - 18, y1 + 4, 320, 570, 'duvet'); B(it, foot - 44, foot - 20, y0 + 10, y1 - 10, 320, 570, 'duvet')
    soft_slab(c, it, RRECT(dx1 - 110, dx1, y0 + 12, y1 - 12, 25, 4), 590, 625, 'linen2', 15, 2)
    cushion3d(c, it, (x0 - 170, (y0 + y1) / 2.0, 760), (0.0, -1.0, 0.0), _vec_tilt((-1.0, 0.0, 0.0), 26), (y1 - y0) - 260, 460, 160, 'linen2', 0.5)


def station2(c, it, face, cx, cy, D):
    """Workstation: monitor screen faces the user (user sits at v<0 looking along the face direction)."""
    T = c.LF(face, cx, cy)
    f = {'+x': (1.0, 0.0, 0.0), '-x': (-1.0, 0.0, 0.0), '+y': (0.0, 1.0, 0.0), '-y': (0.0, -1.0, 0.0)}[face]
    Rv = (-f[1], f[0], 0.0)
    sv = D - 150                                  # screen plane (front face, towards the user)
    c.PRZ(it, c.LP(T, c.RRECT(-120, 120, sv - 60, sv + 110, 50, 5)), 750, 760, 'metal')          # foot
    c.PRZ(it, c.LP(T, c.RRECT(-22, 22, sv + 45, sv + 75, 10, 3)), 760, 1060, 'metal')            # neck BEHIND the screen
    o = T(0, sv)
    c.PR3(it, c.RRECT(-312, 312, 900, 1265, 14, 4), (o[0], o[1], 0), Rv, (0.0, 0.0, 1.0), f, 0, 16, 'screen')       # bezel/body
    c.PR3(it, c.RRECT(-300, 300, 912, 1253, 10, 4), (o[0], o[1], 0), Rv, (0.0, 0.0, 1.0), f, -2, 0, 'display')      # lit display face
    c.PR3(it, c.RRECT(-140, 140, 960, 1180, 40, 4), (o[0], o[1], 0), Rv, (0.0, 0.0, 1.0), f, 16, 45, 'charcoal')    # back housing
    c.puff(it, c.LP(T, c.RRECT(-215, 215, 150, 285, 14, 3)), 750, 772, 'kbd', 4, 6)
    c.PRZ(it, c.LP(T, c.RRECT(260, 430, 120, 330, 18, 3)), 750, 752, 'charcoal')
    m0 = c.ELL(345, 220, 32, 56, 20); m1 = c.ELL(345, 216, 28, 48, 20)
    c.PRZ(it, c.LP(T, m0), 752, 766, 'mouse'); c.PRZ(it, c.LP(T, m1), 766, 778, 'mouse')
    p = T(-420, 250); c.CYL(it, p[0], p[1], 40, 750, 850, 'ceramic', 16)

# ======================= realism upgrade =======================
def soft_slab(c, it, poly, z0, z1, m, r=40, n=3, bottom=True):
    """Prism with rounded (quarter-circle) top and optionally bottom edges."""
    r = min(r, (z1 - z0) / 2.0 - 1)
    if r < 4: c.PRZ(it, poly, z0, z1, m); return
    zb = z0 + (r if bottom else 0); zt = z1 - r
    c.PRZ(it, poly, zb, zt, m)
    for k in range(n):
        a0 = (k / float(n)) * math.pi / 2; a1 = ((k + 1) / float(n)) * math.pi / 2
        ins = r * (1 - math.cos(a1 * 0.999 + a0 * 0.001))
        ins = r * (1 - math.cos((a0 + a1) / 2))
        p = c.inset(poly, ins) if ins > 0.5 else poly
        c.PRZ(it, p, zt + r * math.sin(a0), zt + r * math.sin(a1), m)
        if bottom: c.PRZ(it, p, zb - r * math.sin(a1), zb - r * math.sin(a0), m)

def _pillow_outline(w, h, pinch, n_edge=8, corner=0.10):
    """Square-ish outline with gently concave sides and softly pinched corners (local u,v)."""
    pts = []
    hw, hh = w / 2.0, h / 2.0
    rc = min(w, h) * corner
    corners = [(hw, -hh), (hw, hh), (-hw, hh), (-hw, -hh)]
    for i in range(4):
        (ax, ay), (bx, by) = corners[i], corners[(i + 1) % 4]
        L = math.hypot(bx - ax, by - ay); ux, uy = (bx - ax) / L, (by - ay) / L
        nx, ny = -uy, ux                         # inward normal (outline is counter-clockwise)
        for k in range(n_edge):
            t = k / float(n_edge)
            d = rc + (L - 2 * rc) * t if k else rc * 0.55
            px, py = ax + ux * d, ay + uy * d
            sag = pinch * min(w, h) * math.sin(math.pi * max(0.0, min(1.0, (d - rc) / max(1.0, L - 2 * rc))))
            pts.append((px + nx * sag, py + ny * sag))
    return pts

def cushion3d(c, it, O, U, V, w, h, t, m, crown=0.5, pinch=None):
    """Stuffed cushion lofted as smooth curved surfaces: full in the middle, thin at the seam."""
    W = (U[1] * V[2] - U[2] * V[1], U[2] * V[0] - U[0] * V[2], U[0] * V[1] - U[1] * V[0])
    if pinch is None: pinch = 0.06 if abs(w - h) < 0.25 * max(w, h) else 0.035
    base = _pillow_outline(w, h, pinch)
    def P3(u, v, tt):
        return (O[0] + u * U[0] + v * V[0] + tt * W[0], O[1] + u * U[1] + v * V[1] + tt * W[1], O[2] + u * U[2] + v * V[2] + tt * W[2])
    N = 6
    rings = []
    for k in range(N + 1):
        th = (k / float(N)) * math.radians(82)
        sc = math.cos(th) ** (0.55 + 0.6 * (1 - crown))       # outline scale
        tt = (t / 2.0) * math.sin(th)                          # height above the seam
        rings.append((sc, tt))
    for side in (1, -1):
        for k in range(N):
            (s0, t0), (s1, t1) = rings[k], rings[k + 1]
            lo = [P3(u * s0, v * s0, side * t0) for (u, v) in base]
            hi = [P3(u * s1, v * s1, side * t1) for (u, v) in base]
            it['prisms'].append((3, (lo, hi), 0, 0, m))
    # seam piping
    lo = [P3(u * 1.004, v * 1.004, -4) for (u, v) in base]; hi = [P3(u * 1.004, v * 1.004, 4) for (u, v) in base]
    it['prisms'].append((3, (lo, hi), 0, 0, m))

def _vec_tilt(f, ang):
    """unit 'up' vector tilted backwards (away from facing direction f) by ang degrees"""
    s, co = math.sin(math.radians(ang)), math.cos(math.radians(ang))
    return (-f[0] * s, -f[1] * s, co)

def sofa3(c, it, face, cx, cy, W, D, nseat, armL=True, armR=True, chaise=None, body='sofa', cush='sofa2', pil=('art2', 'rug1')):
    T = c.LF(face, cx, cy)
    fv = {'+x': (1.0, 0.0), '-x': (-1.0, 0.0), '+y': (0.0, 1.0), '-y': (0.0, -1.0)}[face]
    Rv = (-fv[1], fv[0], 0.0); F = (fv[0], fv[1], 0.0)
    u0 = -W / 2.0; u1 = W / 2.0; arm = 160; back = 200
    for (u, v) in ((u0 + 70, -70), (u1 - 70, -70), (u0 + 70, -D + 70), (u1 - 70, -D + 70)):
        p = T(u, v); c.CYL(it, p[0], p[1], 20, 30, 120, 'walnut', 12); c.CYL(it, p[0], p[1], 14, 0, 30, 'walnut', 12)
    soft_slab(c, it, c.LP(T, c.RRECT(u0 + 10, u1 - 10, -D + 10, -10, 40, 5)), 120, 370, body, 25, 2)
    soft_slab(c, it, c.LP(T, c.RRECT(u0, u1, -D, -D + back, 60, 5)), 330, 780, body, 70, 3, False)
    s0, s1 = u0, u1
    if armL: soft_slab(c, it, c.LP(T, c.RRECT(u0, u0 + arm, -D, 0, 60, 5)), 330, 650, body, 70, 3, False); s0 = u0 + arm
    if armR: soft_slab(c, it, c.LP(T, c.RRECT(u1 - arm, u1, -D, 0, 60, 5)), 330, 650, body, 70, 3, False); s1 = u1 - arm
    L = (s1 - s0) / float(nseat)
    for i in range(nseat):
        a = s0 + i * L
        soft_slab(c, it, c.LP(T, c.RRECT(a + 5, a + L - 5, -D + back + 5, -5, 70, 5)), 370, 530, cush, 55, 3)
        # back cushion, leaning back ~12 deg
        o = T(a + L / 2.0, -D + back + 95)
        cushion3d(c, it, (o[0], o[1], 720), Rv, _vec_tilt(F, 12), L - 14, 400, 190, cush, 0.35, 0.015)
    if chaise is not None:
        c0, c1, Lc = chaise
        soft_slab(c, it, c.LP(T, c.RRECT(c0, c1, -40, Lc, 40, 5)), 120, 370, body, 25, 2)
        soft_slab(c, it, c.LP(T, c.RRECT(c0 + 5, c1 - 5, -30, Lc - 5, 70, 5)), 370, 530, cush, 55, 3)
        for (u, v) in ((c0 + 70, Lc - 70), (c1 - 70, Lc - 70)):
            p = T(u, v); c.CYL(it, p[0], p[1], 20, 30, 120, 'walnut', 12); c.CYL(it, p[0], p[1], 14, 0, 30, 'walnut', 12)
        PRZ = c.PRZ
        p0 = c.LP(T, c.RRECT(c0 + 50, c1 - 50, Lc - 560, Lc - 160, 20, 3)); PRZ(it, p0, 530, 552, 'throw')
        PRZ(it, c.LP(T, c.RRECT(c0 + 40, c0 + 60, Lc - 560, Lc - 160, 8, 2)), 300, 552, 'throw')
    # throw pillows leaning on the back cushions
    spots = ((s0 + 260, 470, pil[0], 8), (s1 - 260, 470, pil[0], -8), (s0 + 560, 400, pil[1], 4)) if (s1 - s0) > 1300 else (((s0 + s1) / 2.0, 450, pil[0], 0),)
    for (uc, sz, m, rot) in spots:
        if uc > s1 - 200 or uc < s0 + 200: continue
        o = T(uc, -D + back + 260)
        cushion3d(c, it, (o[0], o[1], 530 + sz / 2.0 - 30), Rv, _vec_tilt(F, 18), sz, sz, 150, m, 0.55)

def headboard_tufted(c, it, axis, x0, x1, y0, y1, z1, m='headb'):
    """Channel-tufted headboard: vertical rounded channels."""
    if axis == 'x':      # headboard thin in x, spans y
        n = max(4, int((y1 - y0) / 150)); w = (y1 - y0) / float(n)
        c.B(it, x0, x1, y0, y1, 0, z1 - 30, m)
        for i in range(n):
            ya = y0 + i * w
            soft_slab(c, it, c.RRECT(x0 - 5, x1 + 5, ya + 6, ya + w - 6, 40, 4), 250, z1, m, 40, 2, True) if False else None
            c.CYLY  # noqa
        for i in range(n):
            ya = y0 + i * w + w / 2.0
            xc = x1 if (x1 - x0) > 0 else x0
        return
    else:
        c.B(it, x0, x1, y0, y1, 0, z1 - 30, m)

def channel_headboard(c, it, plane_x, side, ya, yb, z0, z1, depth=70, m='headb'):
    """Channel tufting for a headboard on a wall at x=plane_x, protruding towards 'side' (+1/-1), spanning y ya..yb."""
    n = max(4, int(round((yb - ya) / 160.0))); w = (yb - ya) / float(n)
    xb0, xb1 = sorted([plane_x, plane_x + side * (depth - 30)])
    c.B(it, xb0, xb1, ya, yb, z0, z1, m)
    for i in range(n):
        y0 = ya + i * w + 4; y1 = ya + (i + 1) * w - 4
        prof = [(y0 + (y1 - y0) * (0.5 + 0.5 * math.cos(math.pi * k / 8.0)), 30 * math.sin(math.pi * k / 8.0)) for k in range(9)]
        pts = [(plane_x + side * (depth - 30 + d), y) for (y, d) in prof]
        pts = pts + [(plane_x + side * (depth - 31), y0)]
        c.PRZ(it, pts, z0 + 20, z1 - 20, m)
    c.PRZ(it, [(xb0, ya), (xb1 + (side > 0) * 30, ya), (xb1 + (side > 0) * 30, yb), (xb0, yb)] if side > 0 else [(xb0 - 30, ya), (xb1, ya), (xb1, yb), (xb0 - 30, yb)], z1 - 20, z1, m)

def bed3(c, it, x0, x1, y0, y1, head, npil, deco=True):
    """Realistic bed: tufted headboard, upholstered base, soft mattress, draped duvet, leaning pillows. head '+x' or '-x'."""
    B, PRZ, RRECT = c.B, c.PRZ, c.RRECT
    s = 1 if head == '+x' else -1                # direction towards the headboard
    hbx = x1 if s > 0 else x0                    # headboard (wall side) x
    bx0, bx1 = (x0, x1 - 70) if s > 0 else (x0 + 70, x1)
    channel_headboard(c, it, hbx, -s, y0 - 30, y1 + 30, 0, 1150, 70, 'headb')
    for (xx, yy) in ((bx0 + 80, y0 + 80), (bx0 + 80, y1 - 80), (bx1 - 80, y0 + 80), (bx1 - 80, y1 - 80)):
        c.CYL(it, xx, yy, 22, 0, 110, 'walnut', 12)
    soft_slab(c, it, RRECT(bx0, bx1, y0, y1, 50, 5), 110, 330, 'headb', 30, 2)
    soft_slab(c, it, RRECT(bx0 + 15, bx1 - 15, y0 + 15, y1 - 15, 70, 5), 330, 560, 'linen', 45, 3)
    L = bx1 - bx0
    # duvet: covers foot 72% with soft rolled edge, drapes down both sides and the foot
    if s > 0: dx0, dx1 = bx0 - 30, bx0 + L * 0.72
    else: dx0, dx1 = bx1 - L * 0.72, bx1 + 30
    soft_slab(c, it, RRECT(dx0, dx1, y0 - 30, y1 + 30, 40, 5), 540, 610, 'duvet', 30, 2)
    B(it, dx0, dx1, y0 - 32, y0 - 8, 300, 560, 'duvet'); B(it, dx0, dx1, y1 + 8, y1 + 32, 300, 560, 'duvet')
    fx = dx0 if s > 0 else dx1 - 24
    B(it, fx, fx + 24, y0 - 30, y1 + 30, 300, 560, 'duvet')
    # folded turn-down band at the head end of the duvet
    tb = (dx1 - 120, dx1) if s > 0 else (dx0, dx0 + 120)
    soft_slab(c, it, RRECT(tb[0], tb[1], y0 - 28, y1 + 28, 30, 4), 600, 640, 'linen2', 18, 2)
    # throw across the foot
    tx = (bx0 + 120, bx0 + 520) if s > 0 else (bx1 - 520, bx1 - 120)
    PRZ(it, RRECT(tx[0], tx[1], y0 - 40, y1 + 40, 20, 3), 610, 632, 'throw')
    B(it, tx[0], tx[1], y0 - 46, y0 - 32, 380, 632, 'throw'); B(it, tx[0], tx[1], y1 + 32, y1 + 46, 380, 632, 'throw')
    # pillows leaning on the headboard
    F = (-s, 0.0, 0.0); U = (0.0, 1.0, 0.0)
    if s < 0: U = (0.0, -1.0, 0.0)
    W = y1 - y0; pw = (W - 60) / float(npil)
    for i in range(npil):
        yc = y0 + 30 + pw * (i + 0.5)
        cushion3d(c, it, (hbx - s * 230, yc, 760), U, _vec_tilt(F, 28), pw - 30, 500, 170, 'linen2', 0.5)
        cushion3d(c, it, (hbx - s * 330, yc, 730), U, _vec_tilt(F, 22), pw - 50, 480, 160, 'linen2', 0.5)
        if deco:
            cushion3d(c, it, (hbx - s * 440, yc, 740), U, _vec_tilt(F, 16), min(pw - 160, 440), 400, 140, 'pil1' if i % 2 == 0 else 'pil2', 0.55)

def keyboard(c, it, T):
    """Low-profile keyboard with key grid (T = local frame, user at v<0 side)."""
    c.puff(it, c.LP(T, c.RRECT(-218, 218, 150, 288, 10, 3)), 750, 762, 'kbd', 2, 3)
    rows = [(160, 14), (183, 14), (206, 13), (229, 12), (252, 11)]
    for (j, (v, n)) in enumerate(rows):
        kw = (420 - 4 * (n - 1)) / float(n) if j else 26
        u = -210
        for k in range(n):
            w = kw if j else 26
            c.PRZ(it, c.LP(T, c.RRECT(u, u + w - 2, v, v + 19, 3, 2)), 762, 769, 'charcoal'); u += w + 2
    # space-bar row (nearest the user)
    c.PRZ(it, c.LP(T, c.RRECT(-210, -140, 272, 284, 3, 2)), 762, 768, 'charcoal'); c.PRZ(it, c.LP(T, c.RRECT(-130, 90, 266, 284, 3, 2)), 762, 768, 'charcoal')
    c.PRZ(it, c.LP(T, c.RRECT(100, 210, 266, 284, 3, 2)), 762, 768, 'charcoal')

def mouse(c, it, T):
    c.PRZ(it, c.LP(T, c.RRECT(240, 395, 115, 335, 20, 4)), 750, 753, 'charcoal')      # mouse pad
    for (z0, z1, a, b) in ((753, 760, 31, 55), (760, 768, 30, 53), (768, 776, 27, 48), (776, 782, 22, 40), (782, 786, 14, 28)):
        c.PRZ(it, c.LP(T, c.ELL(318, 228 - (b - 55) * 0.3, a, b, 22)), z0, z1, 'mouse')
    c.PRZ(it, c.LP(T, c.RRECT(316, 320, 175, 205, 1, 1)), 781, 787, 'charcoal')     # button split / wheel

def station3(c, it, face, cx, cy, D):
    T = c.LF(face, cx, cy)
    f = {'+x': (1.0, 0.0, 0.0), '-x': (-1.0, 0.0, 0.0), '+y': (0.0, 1.0, 0.0), '-y': (0.0, -1.0, 0.0)}[face]
    Rv = (-f[1], f[0], 0.0)
    sv = D - 150
    c.PRZ(it, c.LP(T, c.RRECT(-110, 110, sv - 40, sv + 110, 40, 5)), 750, 758, 'metal')
    c.PRZ(it, c.LP(T, c.RRECT(-24, 24, sv + 50, sv + 80, 10, 3)), 758, 1070, 'metal')
    o = T(0, sv)
    c.PR3(it, c.RRECT(-312, 312, 900, 1265, 10, 4), (o[0], o[1], 0), Rv, (0.0, 0.0, 1.0), f, 0, 14, 'screen')
    c.PR3(it, c.RRECT(-304, 304, 914, 1257, 6, 3), (o[0], o[1], 0), Rv, (0.0, 0.0, 1.0), f, -2, 0, 'display')
    c.PR3(it, c.RRECT(-200, 200, 940, 1200, 60, 5), (o[0], o[1], 0), Rv, (0.0, 0.0, 1.0), f, 14, 40, 'charcoal')
    keyboard(c, it, T); mouse(c, it, T)
    # mug (left of the keyboard, on a coaster) and a notebook – all within the narrowest (850 mm) desk
    p = T(-300, 215)
    c.CYL(it, p[0], p[1], 48, 750, 754, 'walnut', 18); c.CYL(it, p[0], p[1], 38, 754, 850, 'ceramic', 18); c.CYL(it, p[0], p[1], 32, 846, 851, 'walnut', 14)
    hp = T(-300 - 50, 215); c.CYL(it, hp[0], hp[1], 12, 780, 825, 'ceramic', 8)
    c.PRZ(it, c.LP(T, c.RRECT(-395, -240, 315, 390, 4, 2)), 750, 760, 'artbg')

# ---------------- dining ----------------
def _loft(it, lo, hi, m):
    it['prisms'].append((3, (lo, hi), 0, 0, m))

def dining_table(c, it, x0, x1, y0, y1):
    """Marble top with eased edge on a recessed walnut frame and two sculpted trestle legs with brass shoes."""
    RRECT = c.RRECT
    soft_slab(c, it, RRECT(x0, x1, y0, y1, 30, 4), 725, 758, 'marble', 9, 2)
    c.PRZ(it, RRECT(x0 + 90, x1 - 90, y0 + 90, y1 - 90, 20, 3), 700, 725, 'walnut')
    W = y1 - y0; ym = (y0 + y1) / 2.0
    for xl in (x0 + 260, x1 - 260):
        # tapered trestle: wide foot, narrow neck, flaring top
        def ring(z, hx, hy): return [(xl - hx, ym - hy, z), (xl + hx, ym - hy, z), (xl + hx, ym + hy, z), (xl - hx, ym + hy, z)]
        hy_base = W / 2.0 - 110
        _loft(it, ring(0, 50, hy_base), ring(18, 50, hy_base), 'gold')
        _loft(it, ring(18, 45, hy_base - 10), ring(90, 40, hy_base - 40), 'walnut')
        _loft(it, ring(90, 40, hy_base - 40), ring(420, 32, 110), 'walnut')
        _loft(it, ring(420, 32, 110), ring(700, 40, hy_base - 20), 'walnut')
    c.PRZ(it, RRECT(x0 + 260, x1 - 260, ym - 30, ym + 30, 10, 2), 600, 640, 'walnut')      # stretcher

def place_setting(c, it, px, py):
    c.CYL(it, px, py, 170, 758, 761, 'rug2', 28)                 # woven placemat
    c.CYL(it, px, py, 130, 761, 768, 'ceramic', 28); c.CYL(it, px, py, 95, 768, 770, 'ceramic2', 24)
    c.CYL(it, px + 160, py - 140, 32, 761, 860, 'glass', 14)
    c.B(it, px - 180, px - 168, py - 80, py + 80, 761, 764, 'steel'); c.B(it, px + 168, px + 180, py - 80, py + 80, 761, 764, 'steel')

def dchair3(c, it, cx, cy, back):
    """Upholstered dining chair: tapered walnut legs with brass caps, soft seat, curved upholstered back with rounded top."""
    bd = {'-y': (0, -1), '+y': (0, 1), '-x': (-1, 0), '+x': (1, 0)}[back]
    for sx in (-1, 1):
        for sy in (-1, 1):
            x, y = cx + sx * 180, cy + sy * 170
            _loft(it, [(x + 20 * math.cos(2 * math.pi * k / 10), y + 20 * math.sin(2 * math.pi * k / 10), 25) for k in range(10)],
                      [(x + 13 * math.cos(2 * math.pi * k / 10), y + 13 * math.sin(2 * math.pi * k / 10), 400) for k in range(10)], 'walnut')
            c.CYL(it, x, y, 15, 0, 25, 'gold', 10)
    c.PRZ(it, c.RRECT(cx - 215, cx + 215, cy - 205, cy + 205, 50, 4), 400, 425, 'walnut')
    soft_slab(c, it, c.RRECT(cx - 235, cx + 235, cy - 225, cy + 225, 90, 6), 425, 495, 'seat', 28, 3)
    th = math.degrees(math.atan2(bd[1], bd[0])); oc = (cx - bd[0] * 30, cy - bd[1] * 30)
    def band(r0, r1, sp, n=16): return c.ARC(oc[0], oc[1], r1, th - sp, th + sp, n) + c.ARC(oc[0], oc[1], r0, th + sp, th - sp, n)
    c.PRZ(it, band(205, 262, 78), 470, 800, 'seat')
    for (k, (z0, z1)) in enumerate(((800, 815), (815, 828), (828, 836))):
        e = (k + 1) * 6
        c.PRZ(it, band(205 + e, 262 - e, 78 - (k + 1) * 1.5), z0, z1, 'seat')
    c.PRZ(it, band(260, 266, 70), 600, 615, 'gold')          # brass trim line on the back

def dining_set(c, table, chairs, pendant=None):
    it = c.item('Dining_Table_Marble_Walnut_Trestle', 'Furniture'); (_sty('dining_table') or dining_table)(c, it, *table)
    it = c.item('Dining_Chairs_Upholstered_Walnut', 'Furniture')
    for (cx, cy, back) in chairs: (_sty('dchair') or dchair4)(c, it, cx, cy, back)
    it = c.item('Dining_Place_Settings', 'Decor')
    for (cx, cy, back) in chairs:
        bd = {'-y': (0, -1), '+y': (0, 1), '-x': (-1, 0), '+x': (1, 0)}[back]
        place_setting(c, it, cx - bd[0] * 400, cy - bd[1] * 400)

def dchair4(c, it, cx, cy, back):
    """Armless leather dining chair (like the reference photo): slim splayed black legs, piped seat,
    tall shell back that wraps round and leans back slightly."""
    M = c.MATS if hasattr(c, 'MATS') else None
    bd = {'-y': (0, -1), '+y': (0, 1), '-x': (-1, 0), '+x': (1, 0)}[back]
    px, py = -bd[1], bd[0]                        # sideways
    # legs: thin black tapered tubes, splayed ~30 mm
    for (sx, sb) in ((-1, -1), (1, -1), (-1, 1), (1, 1)):
        tx = cx + px * sx * 175 + bd[0] * sb * 170; ty = cy + py * sx * 175 + bd[1] * sb * 170
        bx = tx + px * sx * 28 + bd[0] * sb * 30; by = ty + py * sx * 28 + bd[1] * sb * 30
        _loft(it, [(bx + 9 * math.cos(2 * math.pi * k / 10), by + 9 * math.sin(2 * math.pi * k / 10), 0) for k in range(10)],
                  [(tx + 13 * math.cos(2 * math.pi * k / 10), ty + 13 * math.sin(2 * math.pi * k / 10), 425) for k in range(10)], 'metal')
    # seat: frame, cushion with piping
    seat = c.RRECT(cx - 225, cx + 225, cy - 228, cy + 228, 60, 5)
    c.PRZ(it, c.inset(seat, 12), 410, 432, 'metal')
    soft_slab(c, it, seat, 432, 505, 'leather2', 24, 3)
    c.PRZ(it, [(x + (x - cx) * 0.012, y + (y - cy) * 0.012) for (x, y) in seat], 466, 471, 'leather3')
    # back shell: lofted curved band, tilted back 9 deg, narrowing slightly towards a rounded top
    oc = (cx - bd[0] * 105, cy - bd[1] * 105)
    th = math.atan2(bd[1], bd[0])
    levels = [(485, 0), (560, 0), (640, 0), (720, 0), (800, 0), (850, 0), (872, 1), (884, 2), (890, 3)]
    rings = []
    for (z, rnd) in levels:
        sh = (z - 485) * math.tan(math.radians(9))
        span = math.radians(41 - (z - 485) / 405.0 * 7)
        ro = 335 - rnd * 6; ri = 295 + rnd * 6
        o = (oc[0] + bd[0] * sh, oc[1] + bd[1] * sh)
        n = 14
        outer = [(o[0] + ro * math.cos(th - span + 2 * span * k / n), o[1] + ro * math.sin(th - span + 2 * span * k / n), z) for k in range(n + 1)]
        inner = [(o[0] + ri * math.cos(th + span - 2 * span * k / n), o[1] + ri * math.sin(th + span - 2 * span * k / n), z) for k in range(n + 1)]
        rings.append(outer + inner)
    for k in range(len(rings) - 1): _loft(it, rings[k], rings[k + 1], 'leather2')
    # vertical stitch line down the back
    sh = 0
    _loft(it, [(oc[0] + bd[0] * 337 + px * a, oc[1] + bd[1] * 337 + py * a, 520) for a in (-3, 3, 3, -3)][:2] + [(oc[0] + bd[0] * 339 + px * 3, oc[1] + bd[1] * 339 + py * 3, 520), (oc[0] + bd[0] * 339 - px * 3, oc[1] + bd[1] * 339 - py * 3, 520)],
              [(oc[0] + bd[0] * (337 + 52) + px * a, oc[1] + bd[1] * (337 + 52) + py * a, 840) for a in (-3, 3)] + [(oc[0] + bd[0] * (339 + 52) + px * 3, oc[1] + bd[1] * (339 + 52) + py * 3, 840), (oc[0] + bd[0] * (339 + 52) - px * 3, oc[1] + bd[1] * (339 + 52) - py * 3, 840)], 'leather3')
