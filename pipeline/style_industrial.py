"""INDUSTRIAL LOFT furniture family: black powder-coated steel frames, thick smoked-oak slabs,
leather / boxy upholstery with straps, exposed structure and metal factory shades."""
import math
import planlib as P

ST = 'blksteel'


# ---------------------------------------------------------------- helpers
def _sub(a, b): return (a[0] - b[0], a[1] - b[1], a[2] - b[2])
def _add(a, b): return (a[0] + b[0], a[1] + b[1], a[2] + b[2])
def _mul(a, s): return (a[0] * s, a[1] * s, a[2] * s)
def _cross(a, b): return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])
def _nrm(a):
    L = math.sqrt(a[0] ** 2 + a[1] ** 2 + a[2] ** 2) or 1.0
    return (a[0] / L, a[1] / L, a[2] / L)


def _basis(d):
    """two unit vectors e1, e2 with e1 x e2 = d (d unit)"""
    up = (0.0, 0.0, 1.0) if abs(d[2]) < 0.9 else (1.0, 0.0, 0.0)
    e1 = _nrm(_cross(d, up)); e2 = _cross(d, e1)
    return e1, e2


def _ring(o, d, r, n, ph=0.0):
    e1, e2 = _basis(d)
    return [_add(o, _add(_mul(e1, r * math.cos(ph + 2 * math.pi * k / n)), _mul(e2, r * math.sin(ph + 2 * math.pi * k / n)))) for k in range(n)]


def _bar(it, a, b, r, m, n=4):
    """tube from 3D point a to b; n=4 gives a square tube of half-width r"""
    d = _nrm(_sub(b, a))
    if n == 4:
        rr, ph = r * math.sqrt(2), math.pi / 4
    else:
        rr, ph = r, 0.0
    P._loft(it, _ring(a, d, rr, n, ph), _ring(b, d, rr, n, ph), m)


def _rev(it, o, d, prof, m, n=24):
    """surface of revolution about axis d through o; prof = [(s, r), ...] along the axis"""
    rings = [_ring(_add(o, _mul(d, s)), d, r, n) for (s, r) in prof]
    for k in range(len(rings) - 1): P._loft(it, rings[k], rings[k + 1], m)


def _frame(cx, cy, fx, fy):
    """local frame: u = sideways (right-handed), v = forward (fx, fy)"""
    rx, ry = fy, -fx
    def Pt(u, v, z=0.0): return (cx + u * rx + v * fx, cy + u * ry + v * fy, z)
    return Pt, (rx, ry, 0.0), (fx, fy, 0.0)


def _lbox(c, it, Pt, u0, u1, v0, v1, z0, z1, m):
    pts = [Pt(u, v)[:2] for (u, v) in ((u0, v0), (u1, v0), (u1, v1), (u0, v1))]
    c.PRZ(it, pts, z0, z1, m)


def _lpoly(c, Pt, pts):
    return [Pt(u, v)[:2] for (u, v) in pts]


# ---------------------------------------------------------------- sofa
def sofa(c, it, face, cx, cy, W, D, nseat, armL=True, armR=True, chaise=None, body='sofa', cush='sofa2', pil=('pil1', 'pil2')):
    T = c.LF(face, cx, cy)
    o = T(0, 0); a1 = T(1, 0); f1 = T(0, 1)
    U3 = (a1[0] - o[0], a1[1] - o[1], 0.0); F3 = (f1[0] - o[0], f1[1] - o[1], 0.0)
    def Pt(u, v, z=0.0):
        p = T(u, v); return (p[0], p[1], z)
    def box(u0, u1, v0, v1, z0, z1, m): c.PRZ(it, c.LP(T, [(u0, v0), (u1, v0), (u1, v1), (u0, v1)]), z0, z1, m)
    u0, u1 = -W / 2.0, W / 2.0
    tb = 36; arm = 150; ZB = 150; bp = 120; ZS = 450
    # ---- exposed steel base: perimeter rails + square legs
    box(u0, u1, -D, -D + tb, ZB - 40, ZB, ST); box(u0, u1, -tb, 0, ZB - 40, ZB, ST)
    for (ua, ub) in ((u0, u0 + tb), (u1 - tb, u1)): box(ua, ub, -D, 0, ZB - 40, ZB, ST)
    nl = 2 + (1 if W > 1900 else 0)
    for k in range(nl):
        ul = u0 + (W - tb) * k / float(nl - 1)
        for (va, vb) in ((-D, -D + tb), (-tb, 0)): box(ul, ul + tb, va, vb, 0, ZB - 40, ST)
    # upholstered deck
    P.soft_slab(c, it, c.LP(T, c.RRECT(u0 + 8, u1 - 8, -D + 8, -8, 14, 2)), ZB, 300, body, 10, 2)
    # back: upholstered panel capped by a steel rail between two tall rear posts
    P.soft_slab(c, it, c.LP(T, c.RRECT(u0 + tb, u1 - tb, -D + 6, -D + 6 + bp, 14, 2)), 300, 770, body, 14, 2, False)
    box(u0, u1, -D, -D + tb, 770, 800, ST)
    for (ua, ub) in ((u0, u0 + tb), (u1 - tb, u1)): box(ua, ub, -D, -D + tb, 0, 800, ST)
    # ---- arms: steel side frame (visible loop) around a boxy upholstered block with a flat pad on top
    s0, s1 = u0, u1
    for (on, ua, sg) in ((armL, u0, 1), (armR, u1, -1)):
        if not on: continue
        ub = ua + sg * tb; ui = ua + sg * arm
        lo, hi = min(ua, ub), max(ua, ub)
        box(lo, hi, -tb, 0, 0, 600, ST)                     # front post
        box(lo, hi, -D, 0, 570, 600, ST)                    # top rail
        box(lo, hi, -D, 0, ZB - 40, ZB, ST)                 # bottom rail
        box(lo, hi, -D + tb, -tb, 355, 375, ST)             # mid rail
        il, ih = min(ub, ui), max(ub, ui)
        P.soft_slab(c, it, c.LP(T, c.RRECT(il, ih, -D + bp, -6, 12, 2)), ZB, 600, body, 10, 2, False)
        pl, ph = min(ua, ui), max(ua, ui)
        P.soft_slab(c, it, c.LP(T, c.RRECT(pl, ph, -D + tb + 4, -2, 14, 2)), 600, 648, body, 14, 2, True)
        if sg > 0: s0 = ui
        else: s1 = ui
    # ---- seat cushions: square, boxy, with a dark welt line
    vb = -D + 6 + bp
    L = (s1 - s0) / float(nseat)
    for i in range(nseat):
        a = s0 + i * L
        poly = c.LP(T, c.RRECT(a + 4, a + L - 4, vb + 4, -6, 18, 2))
        P.soft_slab(c, it, poly, 300, ZS, cush, 16, 2)
        ctr = T(a + L / 2.0, (vb - 6) / 2.0)
        c.PRZ(it, [(x + (x - ctr[0]) * 0.004, y + (y - ctr[1]) * 0.004) for (x, y) in poly], ZS - 22, ZS - 17, 'leather3')
    # ---- back cushions: boxy slabs leaning 10 deg, each belted with two leather straps
    tl = math.radians(10); sn, cs = math.sin(tl), math.cos(tl)
    V = (-F3[0] * sn, -F3[1] * sn, cs); Wn = (F3[0] * cs, F3[1] * cs, sn)
    H = 350; TH = 150
    for i in range(nseat):
        a = s0 + i * L; w = L - 10
        O = Pt(a + L / 2.0, vb + H * sn + 4, ZS)
        c.PR3(it, c.RRECT(-w / 2.0, w / 2.0, 0, H, 22, 2), O, U3, V, Wn, 0, TH, cush)
        for su in (-0.28, 0.28):
            uu = su * w
            c.PR3(it, [(uu - 22, 60), (uu + 22, 60), (uu + 22, H + 6), (uu - 22, H + 6)], O, U3, V, Wn, TH - 2, TH + 5, 'leather3')
            c.PR3(it, [(uu - 22, H - 4), (uu + 22, H - 4), (uu + 22, H + 6), (uu - 22, H + 6)], O, U3, V, Wn, -4, TH, 'leather3')
            c.PR3(it, [(uu - 26, 140), (uu + 26, 140), (uu + 26, 176), (uu - 26, 176)], O, U3, V, Wn, TH + 4, TH + 9, 'steel')   # buckle
    # ---- chaise
    if chaise is not None:
        c0, c1, Lc = chaise
        box(c0, c1, Lc - tb, Lc, ZB - 40, ZB, ST)
        for (ua, ub) in ((c0, c0 + tb), (c1 - tb, c1)):
            box(ua, ub, -tb, Lc, ZB - 40, ZB, ST)
            box(ua, ub, Lc - tb, Lc, 0, ZB - 40, ST)
        P.soft_slab(c, it, c.LP(T, c.RRECT(c0 + 8, c1 - 8, -20, Lc - 8, 14, 2)), ZB, 300, body, 10, 2)
        poly = c.LP(T, c.RRECT(c0 + 4, c1 - 4, -2, Lc - 6, 18, 2))
        P.soft_slab(c, it, poly, 300, ZS, cush, 16, 2)
        ctr = T((c0 + c1) / 2.0, (Lc - 8) / 2.0)
        c.PRZ(it, [(x + (x - ctr[0]) * 0.004, y + (y - ctr[1]) * 0.004) for (x, y) in poly], ZS - 22, ZS - 17, 'leather3')
    # ---- two scatter pillows
    span = s1 - s0
    spots = ((s0 + 300, pil[0], 6), (s1 - 300, pil[1], -6)) if span > 1100 else ((s0 + span * 0.3, pil[0], 4), (s0 + span * 0.7, pil[1], -4))
    for (uc, m, rot) in spots:
        sz = 440
        q = Pt(uc, vb + H * sn + TH + 95, 0)
        P.cushion3d(c, it, (q[0], q[1], ZS + sz / 2.0 - 25), U3, P._vec_tilt(F3, 16), sz, sz, 140, m, 0.5)


# ---------------------------------------------------------------- bed
def bed(c, it, x0, x1, y0, y1, head, npil, deco=True):
    B, PRZ, RRECT = c.B, c.PRZ, c.RRECT
    s = 1 if head == '+x' else -1
    hbx = x1 if s > 0 else x0
    hx0, hx1 = sorted([hbx, hbx - s * 45])
    ya, yb = y0 - 20, y1 + 20
    # headboard: steel frame with round vertical bars
    B(it, hx0, hx1, ya, ya + 50, 0, 1150, ST); B(it, hx0, hx1, yb - 50, yb, 0, 1150, ST)
    B(it, hx0, hx1, ya, yb, 1105, 1150, ST)
    B(it, hx0, hx1, ya, yb, 600, 640, ST)
    B(it, hx0, hx1, ya, yb, 230, 300, ST)
    xm = (hx0 + hx1) / 2.0
    n = int((yb - ya - 100) / 115)
    for k in range(n):
        yy = ya + 50 + (yb - ya - 100) * (k + 0.5) / n
        c.CYL(it, xm, yy, 10, 640, 1105, ST, 8)
    # base: thin steel side rails, square legs, low steel footboard rail
    bh0, bh1 = (x0, x1 - 45) if s > 0 else (x0 + 45, x1)
    foot = bh0 if s > 0 else bh1
    fx0, fx1 = sorted([foot, foot + s * 45])
    B(it, bh0, bh1, y0, y0 + 35, 230, 300, ST); B(it, bh0, bh1, y1 - 35, y1, 230, 300, ST)
    B(it, fx0, fx1, y0, y1, 230, 300, ST)
    B(it, fx0, fx1, y0, y0 + 45, 0, 430, ST); B(it, fx0, fx1, y1 - 45, y1, 0, 430, ST)
    B(it, fx0, fx1, y0, y1, 395, 430, ST)
    for k in (1, 2):
        yy = y0 + (y1 - y0) * k / 3.0
        B(it, fx0 + 10, fx1 - 10, yy - 9, yy + 9, 300, 395, ST)
    xmid = (bh0 + bh1) / 2.0
    for yy in (y0, y1 - 45):
        B(it, xmid - 22, xmid + 22, yy, yy + 45, 0, 230, ST)
    mx0, mx1 = (fx1 + 5, bh1 - 5) if s > 0 else (bh0 + 5, fx0 - 5)
    B(it, mx0, mx1, y0 + 35, y1 - 35, 280, 300, 'oakd')            # slat deck
    P.soft_slab(c, it, RRECT(mx0, mx1, y0 + 8, y1 - 8, 50, 4), 300, 545, 'linen', 40, 3)
    L = mx1 - mx0
    if s > 0: dx0, dx1 = mx0 - 20, mx0 + L * 0.7
    else: dx0, dx1 = mx1 - L * 0.7, mx1 + 20
    P.soft_slab(c, it, RRECT(dx0, dx1, y0 - 22, y1 + 22, 35, 4), 535, 595, 'duvet', 25, 2)
    B(it, dx0, dx1, y0 - 24, y0 - 4, 330, 560, 'duvet'); B(it, dx0, dx1, y1 + 4, y1 + 24, 330, 560, 'duvet')
    ffx = dx0 if s > 0 else dx1 - 20
    B(it, ffx, ffx + 20, y0 - 22, y1 + 22, 450, 560, 'duvet')
    tb = (dx1 - 110, dx1) if s > 0 else (dx0, dx0 + 110)
    P.soft_slab(c, it, RRECT(tb[0], tb[1], y0 - 20, y1 + 20, 25, 4), 585, 622, 'linen2', 15, 2)
    # knitted throw folded over the foot
    tx = (mx0 + 100, mx0 + 450) if s > 0 else (mx1 - 450, mx1 - 100)
    PRZ(it, RRECT(tx[0], tx[1], y0 - 30, y1 + 30, 15, 3), 595, 615, 'throw')
    B(it, tx[0], tx[1], y0 - 36, y0 - 26, 400, 615, 'throw'); B(it, tx[0], tx[1], y1 + 26, y1 + 36, 400, 615, 'throw')
    # pillows
    F = (-s, 0.0, 0.0); U = (0.0, 1.0, 0.0) if s > 0 else (0.0, -1.0, 0.0)
    Wd = y1 - y0; pw = (Wd - 60) / float(npil)
    for i in range(npil):
        yc = y0 + 30 + pw * (i + 0.5)
        P.cushion3d(c, it, (hbx - s * 215, yc, 745), U, P._vec_tilt(F, 26), pw - 30, 480, 160, 'linen2', 0.5)
        P.cushion3d(c, it, (hbx - s * 320, yc, 720), U, P._vec_tilt(F, 20), pw - 50, 460, 150, 'linen2', 0.5)
        if deco:
            P.cushion3d(c, it, (hbx - s * 425, yc, 725), U, P._vec_tilt(F, 14), min(pw - 180, 400), 380, 130, 'pil1' if i % 2 == 0 else 'pil2', 0.5)


# ---------------------------------------------------------------- dining table
def dining_table(c, it, x0, x1, y0, y1):
    B = c.B
    B(it, x0, x1, y0, y1, 698, 758, 'oakd')                          # 60 mm solid slab, square edges
    npl = 4 if (y1 - y0) > 900 else 3
    for k in range(1, npl):                                          # plank joints on top and both ends
        yy = y0 + (y1 - y0) * k / float(npl)
        B(it, x0 + 1, x1 - 1, yy - 1.5, yy + 1.5, 758, 758.6, 'walnut')
        B(it, x0 - 0.6, x0, yy - 1.5, yy + 1.5, 698, 758, 'walnut'); B(it, x1, x1 + 0.6, yy - 1.5, yy + 1.5, 698, 758, 'walnut')
    ym = (y0 + y1) / 2.0
    for xl in (x0 + 240, x1 - 240):
        a, b = xl - 22, xl + 22
        B(it, a, b, y0 + 70, y1 - 70, 650, 698, ST)                  # top cross bar
        B(it, a, b, y0 + 55, y1 - 55, 0, 45, ST)                     # floor bar
        for (ya, yb) in ((y0 + 70, y0 + 135), (y1 - 135, y1 - 70)):
            B(it, a, b, ya, yb, 45, 650, ST)                         # posts (flat bar 44 x 65)
        for (ya, yb) in ((y0 + 55, y0 + 120), (y1 - 120, y1 - 55)):
            B(it, a - 6, b + 6, ya, yb, 0, 6, 'charcoal')            # foot glides
        # X brace inside the end frame
        for (pa, pb) in (((y0 + 135, 80), (y1 - 135, 620)), ((y1 - 135, 80), (y0 + 135, 620))):
            _bar(it, (xl, pa[0], pa[1]), (xl, pb[0], pb[1]), 9, ST, 4)
    B(it, x0 + 262, x1 - 262, ym - 20, ym + 20, 330, 370, ST)       # stretcher
    for yy in (y0 + 110, y1 - 130):
        B(it, x0 + 262, x1 - 262, yy, yy + 20, 670, 698, ST)        # side aprons (angle)


# ---------------------------------------------------------------- dining chair (cafe / Tolix type)
def dchair(c, it, cx, cy, back):
    bd = {'-y': (0, -1), '+y': (0, 1), '-x': (-1, 0), '+x': (1, 0)}[back]
    Pt, R3, F3 = _frame(cx, cy, -bd[0], -bd[1])
    seat = _lpoly(c, Pt, c.RRECT(-205, 205, -195, 215, 45, 3))
    c.PRZ(it, seat, 418, 452, ST)                                     # pressed steel seat with deep skirt
    c.PRZ(it, c.inset(seat, 16), 452, 474, 'oakd')                    # timber seat pad
    def leg(su, sv, z):
        t = z / 430.0
        return Pt(su * (228 + (180 - 228) * t), sv * (225 + (178 - 225) * t), z)
    for su in (-1, 1):
        for sv in (-1, 1):
            _bar(it, leg(su, sv, 0), leg(su, sv, 425), 11, ST, 4)
    _bar(it, leg(-1, -1, 150), leg(1, 1, 150), 6, ST, 4); _bar(it, leg(1, -1, 150), leg(-1, 1, 150), 6, ST, 4)
    # back: two uprights, central flat splat, curved top hoop
    R = 330; vC = -262 + R; ha = math.asin(195.0 / R)
    endv = vC - R * math.cos(ha)
    for su in (-1, 1):
        _bar(it, Pt(su * 182, -180, 450), Pt(su * 192, endv, 770), 9, ST, 6)
    th = math.pi * 1.5
    def arc(rr, a0, a1, k=10): return [Pt(rr * math.cos(a0 + (a1 - a0) * i / k), vC + rr * math.sin(a0 + (a1 - a0) * i / k))[:2] for i in range(k + 1)]
    band = arc(R + 4, th - ha - 0.03, th + ha + 0.03) + arc(R - 4, th + ha + 0.03, th - ha - 0.03)
    c.PRZ(it, band, 765, 860, ST)
    band2 = arc(R + 3, th - ha, th + ha, 8) + arc(R - 3, th + ha, th - ha, 8)
    c.PRZ(it, band2, 585, 600, ST)
    lo = [Pt(-30, -186, 452), Pt(30, -186, 452), Pt(30, -178, 452), Pt(-30, -178, 452)]
    hi = [Pt(-30, -263, 768), Pt(30, -263, 768), Pt(30, -255, 768), Pt(-30, -255, 768)]
    P._loft(it, lo, hi, ST)


# ---------------------------------------------------------------- coffee table
def coffee_table(c, it, cx, cy, a, b, ztop):
    B = c.B
    A = a - 20; Bh = b - 40
    B(it, cx - A, cx + A, cy - Bh, cy + Bh, ztop - 55, ztop - 1, ST)          # steel angle frame
    B(it, cx - A + 14, cx + A - 14, cy - Bh + 14, cy + Bh - 14, ztop - 48, ztop, 'oakd')
    for k in (1, 2):
        yy = cy - Bh + 14 + (2 * Bh - 28) * k / 3.0
        B(it, cx - A + 16, cx + A - 16, yy - 1.5, yy + 1.5, ztop, ztop + 0.6, 'walnut')
    zw = 95
    for sx in (-1, 1):
        for sy in (-1, 1):
            lx0, lx1 = sorted([cx + sx * A, cx + sx * (A - 40)]); ly0, ly1 = sorted([cy + sy * Bh, cy + sy * (Bh - 40)])
            B(it, lx0, lx1, ly0, ly1, zw, ztop - 55, ST)
            wx, wy = (lx0 + lx1) / 2.0, (ly0 + ly1) / 2.0
            B(it, wx - 30, wx + 30, wy - 30, wy + 30, zw - 8, zw, ST)            # caster plate
            for dy in (-19, 15):
                B(it, wx - 8, wx + 8, wy + dy, wy + dy + 4, 40, zw - 8, ST)      # fork
            circ = [(40 * math.cos(2 * math.pi * k / 16), 41 + 40 * math.sin(2 * math.pi * k / 16)) for k in range(16)]
            c.PR3(it, circ, (wx, wy - 13, 0), (1, 0, 0), (0, 0, 1), (0, 1, 0), 0, 26, 'charcoal')
    # lower shelf: angle frame + welded steel mesh
    zs = 150
    B(it, cx - A + 40, cx + A - 40, cy - Bh, cy - Bh + 30, zs - 30, zs, ST); B(it, cx - A + 40, cx + A - 40, cy + Bh - 30, cy + Bh, zs - 30, zs, ST)
    B(it, cx - A, cx - A + 30, cy - Bh + 40, cy + Bh - 40, zs - 30, zs, ST); B(it, cx + A - 30, cx + A, cy - Bh + 40, cy + Bh - 40, zs - 30, zs, ST)
    sp = 55
    nx = int((2 * A - 60) / sp)
    for k in range(1, nx):
        xx = cx - A + 30 + (2 * A - 60) * k / float(nx)
        B(it, xx - 3, xx + 3, cy - Bh + 30, cy + Bh - 30, zs - 8, zs - 2, ST)
    ny = int((2 * Bh - 60) / sp)
    for k in range(1, ny):
        yy = cy - Bh + 30 + (2 * Bh - 60) * k / float(ny)
        B(it, cx - A + 30, cx + A - 30, yy - 3, yy + 3, zs - 14, zs - 8, ST)


# ---------------------------------------------------------------- floor lamp (tripod studio lamp)
def floor_lamp(c, it, x, y):
    for k in range(3):
        an = math.radians(90 + 120 * k)
        _bar(it, (x, y, 920), (x + 205 * math.cos(an), y + 205 * math.sin(an), 0), 11, ST, 6)
        fx, fy = x + 205 * math.cos(an), y + 205 * math.sin(an)
        c.CYL(it, fx, fy, 18, 0, 12, 'charcoal', 8)
    c.CYL(it, x, y, 26, 880, 960, ST, 12)
    c.CYL(it, x, y, 13, 960, 1420, ST, 10)
    c.CYL(it, x, y, 20, 1240, 1270, 'steel', 10)                  # height clamp
    # yoke + tilted cone shade (aims down-forward at 50 deg)
    dirv = (math.sqrt(0.5), math.sqrt(0.5))
    ea = math.radians(50)
    ax = (dirv[0] * math.cos(ea), dirv[1] * math.cos(ea), -math.sin(ea))
    O = (x, y, 1600.0)
    side = (-dirv[1], dirv[0], 0.0)
    yw = 128
    _bar(it, (x - side[0] * yw, y - side[1] * yw, 1420), (x + side[0] * yw, y + side[1] * yw, 1420), 10, ST, 4)
    for sg in (-1, 1):
        _bar(it, (x + sg * side[0] * yw, y + sg * side[1] * yw, 1410), (x + sg * side[0] * yw, y + sg * side[1] * yw, 1600), 10, ST, 4)
        _bar(it, (x + sg * side[0] * yw, y + sg * side[1] * yw, 1600), (x + sg * side[0] * (yw - 26), y + sg * side[1] * (yw - 26), 1600), 16, 'steel', 8)
    _rev(it, O, ax, [(-118, 22), (-100, 40), (-90, 62), (-60, 92), (-20, 112), (30, 130), (80, 146), (92, 150)], ST, 24)
    _rev(it, O, ax, [(-140, 14), (-118, 14)], ST, 10)
    _rev(it, O, ax, [(92.5, 141), (95, 141)], 'lightw', 24)


# ---------------------------------------------------------------- lounge chair (leather sling on steel tube)
def lounge_chair(c, it, cx, cy, face_deg, body='cush', base='walnut'):
    a = math.radians(face_deg)
    Pt, R3, F3 = _frame(cx, cy, math.cos(a), math.sin(a))
    tr = 13
    uf = 290
    def rear(z): return -228 - 62 * z / 800.0
    for su in (-1, 1):
        u = su * uf
        _bar(it, Pt(u, 255, 0), Pt(u, 255, 560), tr, ST, 8)              # front post
        _bar(it, Pt(u, rear(0), 0), Pt(u, rear(800), 800), tr, ST, 8)    # raked rear post
        _bar(it, Pt(u, 255 + tr, 560), Pt(u, rear(560), 560), tr, ST, 8)  # arm rail
        _bar(it, Pt(u, 255 + tr, 14), Pt(u, rear(0) - tr, 14), tr, ST, 8)  # floor skid
        # leather strap arm wrapped round the rail
        _lbox(c, it, Pt, u - 34, u + 34, rear(560) + 25, 275, 574, 592, 'leather')
        _lbox(c, it, Pt, u - 34, u + 34, 268, 284, 515, 592, 'leather')
        _lbox(c, it, Pt, u - 34, u + 34, rear(560) + 10, rear(560) + 26, 515, 592, 'leather')
    _bar(it, Pt(-uf, 255, 390), Pt(uf, 255, 390), tr, ST, 8)
    _bar(it, Pt(-uf, rear(790), 790), Pt(uf, rear(790), 790), tr, ST, 8)
    _bar(it, Pt(-uf, rear(170), 170), Pt(uf, rear(170), 170), tr, ST, 8)
    # sling: one leather sheet from front rail, sagging, then up to the top rail
    path = [(255, 395), (130, 352), (0, 322), (-130, 305), (-200, 310), (-232, 360), (-252, 520), (-270, 670), (-284, 790)]
    w = uf - tr - 4; t = 16
    rings = []
    for i, (v, z) in enumerate(path):
        p0 = path[max(0, i - 1)]; p1 = path[min(len(path) - 1, i + 1)]
        dv, dz = p1[0] - p0[0], p1[1] - p0[1]; L = math.hypot(dv, dz) or 1
        nv, nz = -dz / L, dv / L
        if nz < 0: nv, nz = -nv, -nz
        rings.append([Pt(-w, v - nv * t / 2, z - nz * t / 2), Pt(w, v - nv * t / 2, z - nz * t / 2), Pt(w, v + nv * t / 2, z + nz * t / 2), Pt(-w, v + nv * t / 2, z + nz * t / 2)])
    for k in range(len(rings) - 1): P._loft(it, rings[k], rings[k + 1], body)
    # loose seat cushion and back cushion
    q = Pt(0, 55, 0)
    tl = math.radians(5)
    P.cushion3d(c, it, (q[0], q[1], 385), R3, (F3[0] * math.cos(tl), F3[1] * math.cos(tl), math.sin(tl)), 530, 450, 120, body, 0.45)
    q = Pt(0, -205, 0)
    P.cushion3d(c, it, (q[0], q[1], 590), R3, P._vec_tilt(F3, 14), 500, 390, 110, body, 0.45)


# ---------------------------------------------------------------- nightstand
def nightstand(c, it, x0, x1, y0, y1):
    B = c.B
    t = 25
    for (xa, xb) in ((x0 + 5, x0 + 5 + t), (x1 - 5 - t, x1 - 5)):
        for (ya, yb) in ((y0 + 5, y0 + 5 + t), (y1 - 5 - t, y1 - 5)):
            B(it, xa, xb, ya, yb, 0, 495, ST)
            B(it, xa - 3, xb + 3, ya - 3, yb + 3, 0, 8, 'charcoal')
    for z0, z1 in ((470, 495), (110, 130)):
        B(it, x0 + 5, x1 - 5, y0 + 5, y0 + 5 + t, z0, z1, ST); B(it, x0 + 5, x1 - 5, y1 - 5 - t, y1 - 5, z0, z1, ST)
        B(it, x0 + 5, x0 + 5 + t, y0 + 5, y1 - 5, z0, z1, ST); B(it, x1 - 5 - t, x1 - 5, y0 + 5, y1 - 5, z0, z1, ST)
    B(it, x0, x1, y0, y1, 495, 530, 'oakd')                                 # timber top
    B(it, x0 + 5 + t, x1 - 5 - t, y0 + 5 + t, y1 - 5 - t, 130, 152, 'oakd')  # timber lower shelf
    # hanging steel drawer box under the top, with a pull bar on both long faces
    B(it, x0 + 35, x1 - 35, y0 + 35, y1 - 35, 340, 470, ST)
    B(it, x0 + 33, x1 - 33, y0 + 33, y1 - 33, 398, 402, 'charcoal')
    xm = (x0 + x1) / 2.0
    for (ya, yb) in ((y0 + 22, y0 + 33), (y1 - 33, y1 - 22)):
        B(it, xm - 55, xm + 55, ya, yb, 425, 440, 'steel')
    for (xa, xb) in ((x0 + 22, x0 + 33), (x1 - 33, x1 - 22)):
        B(it, xa, xb, (y0 + y1) / 2.0 - 55, (y0 + y1) / 2.0 + 55, 425, 440, 'steel')


# ---------------------------------------------------------------- pendants
def _factory_shade(c, it, x, y, zb, sc=1.0):
    """black steel factory/bell shade with its rim at z=zb and a glowing disc underneath"""
    prof = [(zb + 175 * sc, 18 * sc), (zb + 165 * sc, 34 * sc), (zb + 150 * sc, 48 * sc), (zb + 120 * sc, 66 * sc), (zb + 85 * sc, 100 * sc),
            (zb + 45 * sc, 140 * sc), (zb + 15 * sc, 162 * sc), (zb, 172 * sc)]
    for k in range(len(prof) - 1):
        z1, r1 = prof[k]; z0, r0 = prof[k + 1]
        lo = [(x + r0 * math.cos(2 * math.pi * i / 24), y + r0 * math.sin(2 * math.pi * i / 24), z0) for i in range(24)]
        hi = [(x + r1 * math.cos(2 * math.pi * i / 24), y + r1 * math.sin(2 * math.pi * i / 24), z1) for i in range(24)]
        P._loft(it, lo, hi, ST)
    c.CYL(it, x, y, 175 * sc, zb, zb + 6, ST, 24)                    # rolled rim
    c.CYL(it, x, y, 162 * sc, zb - 4, zb, 'lightw', 24)
    c.CYL(it, x, y, 24 * sc, zb + 175 * sc, zb + 210 * sc, 'steel', 12)  # socket collar


def dining_pendant(c, it, x0, x1, yc):
    L = x1 - x0
    zbar = 1990
    c.B(it, x0 + 20, x1 - 20, yc - 15, yc + 15, zbar - 30, zbar, ST)       # steel bar
    for xr in (x0 + 140, x1 - 140):
        c.CYL(it, xr, yc, 8, zbar, 2550, ST, 8)
        c.CYL(it, xr, yc, 55, 2535, 2550, ST, 16)
        c.CYL(it, xr, yc, 14, zbar, zbar + 30, ST, 8)
    for xs in (x0 + L / 6.0, x0 + L / 2.0, x1 - L / 6.0):
        zb = 1660
        c.CYL(it, xs, yc, 4, zb + 205, zbar - 30, 'charcoal', 6)
        c.CYL(it, xs, yc, 12, zbar - 45, zbar - 30, ST, 8)
        _factory_shade(c, it, xs, yc, zb, 1.0)


def bedside_pendant(c, it, cx, cy):
    CYL = c.CYL
    CYL(it, cx, cy, 40, 2535, 2550, ST, 16)
    CYL(it, cx, cy, 3, 1330, 2535, 'charcoal', 6)
    CYL(it, cx, cy, 24, 1290, 1335, 'steel', 12)                      # socket
    CYL(it, cx, cy, 60, 1282, 1292, ST, 16)                           # cage top ring plate
    # bulb (edison globe)
    for (z0, z1, r) in ((1150, 1170, 30), (1170, 1195, 50), (1195, 1235, 58), (1235, 1262, 48), (1262, 1290, 22)):
        CYL(it, cx, cy, r, z0, z1, 'lightw', 16)
    # wire cage: 8 bowed ribs + 2 rings, closed at the bottom
    prof = [(1287, 60), (1250, 82), (1195, 88), (1145, 74), (1118, 40), (1112, 6)]
    for k in range(8):
        an = 2 * math.pi * k / 8
        pts = [(cx + r * math.cos(an), cy + r * math.sin(an), z) for (z, r) in prof]
        for i in range(len(pts) - 1): _bar(it, pts[i], pts[i + 1], 3, ST, 4)
    for (z, r) in ((1250, 82), (1195, 88), (1145, 74)):
        n = 16
        for k in range(n):
            a0 = 2 * math.pi * k / n; a1 = 2 * math.pi * (k + 1) / n
            _bar(it, (cx + r * math.cos(a0), cy + r * math.sin(a0), z), (cx + r * math.cos(a1), cy + r * math.sin(a1), z), 3, ST, 4)
