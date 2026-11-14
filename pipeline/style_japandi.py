"""Japandi furniture family: low, calm, light oak, slats, linen, paper lanterns."""
import math
import planlib as P

soft_slab = P.soft_slab
cushion3d = P.cushion3d
_loft = P._loft
_tilt = P._vec_tilt


# ---------------------------------------------------------------- small helpers
def _sub(a, b): return (a[0] - b[0], a[1] - b[1], a[2] - b[2])
def _add(a, b): return (a[0] + b[0], a[1] + b[1], a[2] + b[2])
def _mul(a, s): return (a[0] * s, a[1] * s, a[2] * s)
def _cross(a, b): return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])
def _norm(a):
    L = math.sqrt(a[0] ** 2 + a[1] ** 2 + a[2] ** 2) or 1.0
    return (a[0] / L, a[1] / L, a[2] / L)

def _frame(p0, p1, up=(0.0, 0.0, 1.0)):
    d = _norm(_sub(p1, p0))
    s = _cross(d, up)
    if math.sqrt(s[0] ** 2 + s[1] ** 2 + s[2] ** 2) < 1e-6: s = _cross(d, (1.0, 0.0, 0.0))
    s = _norm(s); u = _norm(_cross(s, d))
    return d, s, u

def _beam(it, p0, p1, a, b, m, a1=None, b1=None, up=(0.0, 0.0, 1.0)):
    """Rectangular bar from 3D point p0 to p1, section a (sideways) x b (up-ish), optionally tapering to a1 x b1."""
    a1 = a if a1 is None else a1; b1 = b if b1 is None else b1
    d, s, u = _frame(p0, p1, up)
    def ring(p, aa, bb):
        return [_add(_add(p, _mul(s, sa * aa / 2.0)), _mul(u, sb * bb / 2.0)) for (sa, sb) in ((-1, -1), (1, -1), (1, 1), (-1, 1))]
    _loft(it, ring(p0, a, b), ring(p1, a1, b1), m)

def _rod(it, p0, p1, r0, r1, m, n=10):
    """Round (optionally tapered) rod between two 3D points."""
    d, s, u = _frame(p0, p1)
    def ring(p, r):
        return [_add(_add(p, _mul(s, r * math.cos(2 * math.pi * k / n))), _mul(u, r * math.sin(2 * math.pi * k / n))) for k in range(n)]
    _loft(it, ring(p0, r0), ring(p1, r1), m)

def _lantern(c, it, cx, cy, zb, zt, R, m='paper', n=20, slices=10, rib=True):
    """Paper lantern made of stacked cylinders following an ellipse profile (zb..zt, max radius R)."""
    H = zt - zb; zc = (zb + zt) / 2.0
    for k in range(slices):
        z0 = zb + H * k / float(slices); z1 = zb + H * (k + 1) / float(slices)
        t = ((z0 + z1) / 2.0 - zc) / (H / 2.0)
        r = R * math.sqrt(max(0.02, 1 - t * t)) * 0.98 + R * 0.02
        c.CYL(it, cx, cy, max(r, R * 0.25), z0, z1, m, n)
    if rib:   # thin bamboo/wire ribs that read as the akari spiral
        for k in (2, 4, 6, 8):
            z = zb + H * k / 10.0; t = (z - zc) / (H / 2.0)
            r = R * math.sqrt(max(0.0, 1 - t * t)) + 3
            c.CYL(it, cx, cy, r, z - 2, z + 2, 'greige', n)
    c.CYL(it, cx, cy, R * 0.32, zb - 6, zb, 'metal', 12)          # bottom wire ring
    c.CYL(it, cx, cy, R * 0.28, zt, zt + 8, 'metal', 12)          # top wire ring


# ---------------------------------------------------------------- sofa
def sofa(c, it, face, cx, cy, W, D, nseat, armL=True, armR=True, chaise=None, body='sofa', cush='sofa2', pil=('pil1', 'pil2')):
    """Low oak platform sofa with loose boxy linen cushions and low slatted wooden arm rails."""
    T = c.LF(face, cx, cy); LP = c.LP; RR = c.RRECT
    fv = {'+x': (1.0, 0.0), '-x': (-1.0, 0.0), '+y': (0.0, 1.0), '-y': (0.0, -1.0)}[face]
    Rv = (-fv[1], fv[0], 0.0); F = (fv[0], fv[1], 0.0)
    u0 = -W / 2.0; u1 = W / 2.0
    zp0, zp1 = 150, 215                        # oak platform
    # recessed dark plinth + oak platform with a soft edge (sticks out as a ledge)
    c.PRZ(it, LP(T, RR(u0 + 90, u1 - 90, -D + 90, -90, 20, 3)), 0, zp0, 'oakd')
    soft_slab(c, it, LP(T, RR(u0, u1, -D, 0, 28, 4)), zp0, zp1, 'oak', 12, 2)
    # low oak back board behind the cushions
    soft_slab(c, it, LP(T, RR(u0 + 10, u1 - 10, -D, -D + 45, 18, 3)), zp1, 470, 'oak', 14, 2, False)
    arm = 70
    s0, s1 = u0 + 40, u1 - 40
    for (on, a, b) in ((armL, u0, u0 + arm), (armR, u1 - arm, u1)):
        if not on: continue
        # side frame: two posts, top rail and vertical slats
        for v in (-D + 10, -70):
            c.PRZ(it, LP(T, RR(a + 8, b - 8, v, v + 55, 8, 2)), zp1, 520, 'oak')
        soft_slab(c, it, LP(T, RR(a, b, -D + 5, -55, 18, 3)), 520, 555, 'oak', 12, 2)
        n = 5; v0 = -D + 65; v1 = -70
        for k in range(n):
            vv = v0 + (v1 - v0) * (k + 0.5) / n
            c.PRZ(it, LP(T, RR(a + 20, b - 20, vv - 16, vv + 16, 4, 1)), zp1, 520, 'oak')
        if a == u0: s0 = b + 10
        else: s1 = a - 10
    # seat cushions (boxy, loose) sitting on the platform
    L = (s1 - s0) / float(nseat)
    vb = -D + 50
    for i in range(nseat):
        a = s0 + i * L
        soft_slab(c, it, LP(T, RR(a + 6, a + L - 6, vb, -45, 30, 4)), zp1, 420, cush, 32, 2)
        o = T(a + L / 2.0, vb + 95)
        cushion3d(c, it, (o[0], o[1], 572), Rv, _tilt(F, 9), L - 16, 310, 170, cush, 0.25, 0.012)
    if chaise is not None:
        c0, c1, Lc = chaise
        c.PRZ(it, LP(T, RR(c0 + 90, c1 - 90, -100, Lc - 90, 20, 3)), 0, zp0, 'oakd')
        soft_slab(c, it, LP(T, RR(c0, c1, -40, Lc, 28, 4)), zp0, zp1, 'oak', 12, 2)
        soft_slab(c, it, LP(T, RR(max(c0 + 40, s0) + 6, min(c1 - 40, s1) - 6, -30, Lc - 45, 30, 4)), zp1, 420, cush, 32, 2)
        # folded linen throw over the chaise end
        c.PRZ(it, LP(T, RR(max(c0 + 40, s0) + 30, min(c1 - 40, s1) - 30, Lc - 480, Lc - 140, 10, 2)), 420, 436, 'throw')
    # two scatter pillows leaning on the back cushions
    spots = ((s0 + 280, pil[0], 6), (s1 - 280, pil[1], -6)) if (s1 - s0) > 1000 else (((s0 + s1) / 2.0, pil[0], 0),)
    for (uc, m, rot) in spots:
        o = T(uc, vb + 230)
        cushion3d(c, it, (o[0], o[1], 420 + 200), Rv, _tilt(F, 20), 420, 400, 130, m, 0.5)


# ---------------------------------------------------------------- bed
def bed(c, it, x0, x1, y0, y1, head, npil, deco=True):
    """Low oak platform bed with a slatted oak headboard, low mattress, folded-back duvet, flat pillows."""
    RR = c.RRECT; PRZ = c.PRZ
    s = 1 if head == '+x' else -1
    hbx = x1 if s > 0 else x0
    hb = 60
    bx0, bx1 = (x0, x1 - hb) if s > 0 else (x0 + hb, x1)
    # headboard: dark backing panel + vertical oak slats + top cap
    ya, yb = y0 - 30, y1 + 30
    if s > 0: px0, px1, sx0, sx1 = hbx - 18, hbx, hbx - hb, hbx - 18
    else: px0, px1, sx0, sx1 = hbx, hbx + 18, hbx + 18, hbx + hb
    c.B(it, px0, px1, ya, yb, 140, 930, 'oakd')
    n = int((yb - ya) / 75.0); w = (yb - ya) / float(n)
    for i in range(n):
        yy0 = ya + i * w + 12; yy1 = ya + (i + 1) * w - 12
        c.B(it, sx0, sx1, yy0, yy1, 140, 930, 'oak')
    soft_slab(c, it, RR(min(px0, sx0) - 5, max(px1, sx1), ya - 10, yb + 10, 10, 2), 930, 960, 'oak', 10, 2, False)
    # platform: recessed dark plinth + oak deck extending as a ledge
    PRZ(it, RR(bx0 + 140, bx1 - 140, y0 + 140, y1 - 140, 20, 3), 0, 140, 'oakd')
    soft_slab(c, it, RR(bx0, bx1, y0, y1, 30, 4), 140, 230, 'oak', 14, 2)
    e = 120
    mx0, mx1 = (bx0 + e, bx1 - 10) if s > 0 else (bx0 + 10, bx1 - e)
    my0, my1 = y0 + e, y1 - e
    soft_slab(c, it, RR(mx0, mx1, my0, my1, 50, 5), 230, 450, 'linen', 40, 3)
    L = mx1 - mx0
    # duvet covering the foot ~65 %, draped over the sides, folded back at the top
    if s > 0: dx0, dx1 = mx0 - 25, mx0 + L * 0.66
    else: dx0, dx1 = mx1 - L * 0.66, mx1 + 25
    soft_slab(c, it, RR(dx0, dx1, my0 - 25, my1 + 25, 30, 4), 440, 490, 'duvet', 20, 2)
    c.B(it, dx0, dx1, my0 - 27, my0 - 8, 300, 470, 'duvet'); c.B(it, dx0, dx1, my1 + 8, my1 + 27, 300, 470, 'duvet')
    fx = dx0 if s > 0 else dx1 - 20
    c.B(it, fx, fx + 20, my0 - 25, my1 + 25, 300, 470, 'duvet')
    tb = (dx1 - 170, dx1 + 10) if s > 0 else (dx0 - 10, dx0 + 170)
    soft_slab(c, it, RR(tb[0], tb[1], my0 - 22, my1 + 22, 30, 4), 480, 520, 'duvet', 16, 2)
    # folded linen throw across the foot
    if deco:
        tx = (mx0 + 140, mx0 + 470) if s > 0 else (mx1 - 470, mx1 - 140)
        PRZ(it, RR(tx[0], tx[1], my0 - 30, my1 + 30, 12, 2), 490, 506, 'throw')
        c.B(it, tx[0], tx[1], my0 - 36, my0 - 26, 380, 506, 'throw'); c.B(it, tx[0], tx[1], my1 + 26, my1 + 36, 380, 506, 'throw')
    # pillows lying flat
    Wm = my1 - my0; pw = (Wm - 40) / float(npil)
    pxc = (mx1 - 280) if s > 0 else (mx0 + 280)
    U = (0.0, 1.0, 0.0); V = (1.0, 0.0, 0.0)
    for i in range(npil):
        yc = my0 + 20 + pw * (i + 0.5)
        cushion3d(c, it, (pxc, yc, 450 + 62), U, V, pw - 50, 440, 120, 'linen2', 0.45)
        if deco:   # small lumbar cushion lying in front, slightly propped
            cushion3d(c, it, (pxc - s * 300, yc, 450 + 85), U, (s * 0.87, 0.0, 0.5), min(pw - 240, 380), 240, 100, 'pil1' if i % 2 == 0 else 'pil2', 0.5)


# ---------------------------------------------------------------- dining
def dining_table(c, it, x0, x1, y0, y1):
    """Solid oak plank top on two oak trestle frames joined by a low through-tenoned stretcher."""
    RR = c.RRECT
    soft_slab(c, it, RR(x0, x1, y0, y1, 40, 4), 716, 758, 'oak', 14, 3)
    W = y1 - y0; ym = (y0 + y1) / 2.0
    ins = 300
    xs = (x0 + ins, x1 - ins)
    for xl in xs:
        # foot and top bearer with softly tapered ends
        hw = W / 2.0 - 120
        c.PRZ(it, [(xl - 45, ym - hw), (xl + 45, ym - hw), (xl + 45, ym + hw), (xl - 45, ym + hw)], 20, 85, 'oak')
        c.PRZ(it, RR(xl - 40, xl + 40, ym - hw + 20, ym + hw - 20, 12, 2), 0, 20, 'oak')
        c.PRZ(it, RR(xl - 40, xl + 40, ym - hw - 20, ym + hw + 20, 20, 3), 660, 716, 'oak')
        # twin posts, slightly tapered
        for sy in (-1, 1):
            yp = ym + sy * (hw - 110)
            _loft(it, [(xl - 34, yp - 40, 85), (xl + 34, yp - 40, 85), (xl + 34, yp + 40, 85), (xl - 34, yp + 40, 85)],
                      [(xl - 30, yp - 34, 660), (xl + 30, yp - 34, 660), (xl + 30, yp + 34, 660), (xl - 30, yp + 34, 660)], 'oak')
    # low stretcher with through tenons and wedges (Japanese joinery)
    c.PRZ(it, RR(xs[0] - 90, xs[1] + 90, ym - 28, ym + 28, 6, 2), 200, 270, 'oak')
    for xl, sx in ((xs[0], -1), (xs[1], 1)):
        c.PRZ(it, RR(xl + sx * 58 - 8, xl + sx * 58 + 8, ym - 34, ym + 34, 2, 1), 190, 280, 'oakd')
    # a cross slat between the posts at mid-height (shoji-like)
    for xl in xs:
        hw = W / 2.0 - 120
        c.PRZ(it, RR(xl - 22, xl + 22, ym - hw + 110, ym + hw - 110, 4, 1), 200, 270, 'oak')


def dchair(c, it, cx, cy, back):
    """Wishbone-style oak chair: tapered round legs, steam-bent top rail, Y splat, cane seat."""
    bd = {'-y': (0.0, -1.0), '+y': (0.0, 1.0), '-x': (-1.0, 0.0), '+x': (1.0, 0.0)}[back]
    pv = (-bd[1], bd[0])
    def Q(s, b, z): return (cx + pv[0] * s + bd[0] * b, cy + pv[1] * s + bd[1] * b, z)
    zs = 440
    # legs
    for sx in (-1, 1):
        _rod(it, Q(sx * 205, -205, 0), Q(sx * 192, -192, zs), 13, 17, 'oak', 8)          # front
        _rod(it, Q(sx * 200, 215, 0), Q(sx * 205, 108, 742), 13, 15, 'oak', 8)           # rear, rising to the top rail
        _rod(it, Q(sx * 200, -195, 170), Q(sx * 202, 195, 170), 8, 8, 'oak', 6)           # side stretcher
    _rod(it, Q(-196, -190, 140), Q(196, -190, 140), 8, 8, 'oak', 6)                       # front stretcher
    # seat: oak frame with woven cane inset
    corners = [Q(-215, -215, 0), Q(215, -215, 0), Q(205, 200, 0), Q(-205, 200, 0)]
    poly = [(p[0], p[1]) for p in corners]
    c.PRZ(it, poly, zs - 35, zs, 'oak')
    c.PRZ(it, c.inset(poly, 26), zs, zs + 10, 'cane')
    # steam-bent top rail: plan arc that wraps round to the sides
    th = math.degrees(math.atan2(bd[1], bd[0]))
    oc = (cx + bd[0] * 30, cy + bd[1] * 30)
    sp = 100
    band = c.ARC(oc[0], oc[1], 252, th - sp, th + sp, 14) + c.ARC(oc[0], oc[1], 222, th + sp, th - sp, 14)
    c.PRZ(it, band, 742, 762, 'oak')
    band2 = c.ARC(oc[0], oc[1], 247, th - sp + 3, th + sp - 3, 14) + c.ARC(oc[0], oc[1], 227, th + sp - 3, th - sp + 3, 14)
    c.PRZ(it, band2, 762, 770, 'oak')
    # Y splat
    _beam(it, Q(0, 196, zs - 5), Q(0, 228, 590), 34, 16, 'oak', 30, 16)
    for sx in (-1, 1):
        _beam(it, Q(0, 228, 590), Q(sx * 80, 255, 745), 28, 14, 'oak', 24, 14)


def coffee_table(c, it, cx, cy, a, b, ztop):
    """Low soft-cornered oak table with a lower shelf on four chunky round legs."""
    RR = c.RRECT
    A, Bb = a - 30, b - 30
    top = RR(cx - A, cx + A, cy - Bb, cy + Bb, Bb * 0.55, 8)
    soft_slab(c, it, top, ztop - 42, ztop, 'oak', 16, 3)
    shelf = RR(cx - A + 80, cx + A - 80, cy - Bb + 70, cy + Bb - 70, Bb * 0.45, 6)
    soft_slab(c, it, shelf, 90, 120, 'oak', 8, 2)
    for sx in (-1, 1):
        for sy in (-1, 1):
            x = cx + sx * (A - 130); y = cy + sy * (Bb - 105)
            c.CYL(it, x, y, 42, 0, 14, 'oak', 16)
            c.CYL(it, x, y, 46, 14, ztop - 42, 'oak', 16)


# ---------------------------------------------------------------- lighting
def floor_lamp(c, it, x, y):
    """Paper lantern on a slim oak tripod."""
    zb, zt = 1060, 1700
    for k in range(3):
        a = math.radians(90 + 120 * k)
        _rod(it, (x + 200 * math.cos(a), y + 200 * math.sin(a), 0), (x + 30 * math.cos(a), y + 30 * math.sin(a), zb + 20), 13, 10, 'oak', 8)
    c.CYL(it, x, y, 40, zb - 30, zb + 20, 'oak', 12)                 # collar
    c.CYL(it, x, y, 10, zb + 20, zt - 40, 'metal', 6)                 # stem inside the shade
    H = zt - zb
    # tall cylinder lantern with rounded top/bottom shoulders
    R = 175
    prof = [(0.00, 0.70), (0.03, 0.88), (0.07, 0.97), (0.12, 1.0), (0.88, 1.0), (0.93, 0.97), (0.97, 0.88), (1.00, 0.70)]
    for k in range(len(prof) - 1):
        z0 = zb + H * prof[k][0]; z1 = zb + H * prof[k + 1][0]
        r = R * (prof[k][1] + prof[k + 1][1]) / 2.0
        c.CYL(it, x, y, r, z0, z1, 'paper', 24)
    for k in range(1, 8):
        z = zb + H * (0.12 + 0.76 * k / 8.0)
        c.CYL(it, x, y, R + 2, z - 2, z + 2, 'greige', 24)
    c.CYL(it, x, y, R * 0.7 + 3, zt, zt + 6, 'oak', 16)


def dining_pendant(c, it, x0, x1, yc):
    """Row of three round paper lanterns on thin black cords."""
    n = 3
    sizes = (165, 195, 165)
    for i in range(n):
        x = x0 + (x1 - x0) * (i + 0.5) / n
        R = sizes[i]
        zb = 1690 if i != 1 else 1650
        zt = zb + R * 1.9
        _lantern(c, it, x, yc, zb, zt, R)
        c.CYL(it, x, yc, 3, zt + 8, 2550, 'metal', 6)
        c.CYL(it, x, yc, 40, 2538, 2550, 'metal', 16)


def bedside_pendant(c, it, cx, cy):
    """One small round paper lantern."""
    zb, zt = 1120, 1380
    _lantern(c, it, cx, cy, zb, zt, 140, n=18, slices=8)
    c.CYL(it, cx, cy, 3, zt + 8, 2550, 'metal', 6)
    c.CYL(it, cx, cy, 35, 2540, 2550, 'metal', 14)


# ---------------------------------------------------------------- lounge chair
def lounge_chair(c, it, cx, cy, face_deg, body='cush', base='walnut'):
    """Low oak-frame easy chair with visible flat wooden arms and loose cushions."""
    a = math.radians(face_deg)
    f = (math.cos(a), math.sin(a)); pv = (-f[1], f[0])
    def Q(s, b, z): return (cx + pv[0] * s - f[0] * b, cy + pv[1] * s - f[1] * b, z)   # b>0 = towards the back
    def poly(pts): return [(Q(s, b, 0)[0], Q(s, b, 0)[1]) for (s, b) in pts]
    def rr(s0, s1, b0, b1, r, n=3): return poly(c.RRECT(s0, s1, b0, b1, r, n))
    for sx in (-1, 1):
        sa = sx * 285
        # legs
        _rod(it, Q(sa, -255, 0), Q(sa, -250, 555), 20, 22, 'oak', 10)
        _rod(it, Q(sa, 250, 0), Q(sa, 245, 330), 20, 22, 'oak', 10)
        # side seat rail and flat arm
        _beam(it, Q(sa, -275, 280), Q(sa, 265, 280), 34, 50, 'oak')
        soft_slab(c, it, rr(sa - 32, sa + 32, -280, 175, 30), 555, 585, 'oak', 10, 2)
        _rod(it, Q(sa, 150, 330), Q(sa, 165, 555), 14, 14, 'oak', 8)            # rear arm support
        _rod(it, Q(sa, -250, 120), Q(sa, 250, 120), 12, 12, 'oak', 8)           # low side stretcher
        # leaning back post
        _beam(it, Q(sx * 255, 250, 300), Q(sx * 255, 300, 800), 40, 34, 'oak')
    for bb in (-255, 250):
        _beam(it, Q(-285, bb, 290), Q(285, bb, 290), 30, 40, 'oak')
    _beam(it, Q(-275, 297, 770), Q(275, 297, 770), 30, 50, 'oak')               # back top rail
    # loose cushions
    soft_slab(c, it, rr(-248, 248, -280, 235, 40, 4), 305, 430, body, 34, 2)
    F = (f[0], f[1], 0.0); U = (pv[0], pv[1], 0.0)
    o = Q(0, 205, 620)
    cushion3d(c, it, o, U, _tilt(F, 14), 470, 420, 140, body, 0.35, 0.02)


# ---------------------------------------------------------------- nightstand
def nightstand(c, it, x0, x1, y0, y1):
    """Open oak bedside table: top, one drawer, open shelf, four legs."""
    RR = c.RRECT
    soft_slab(c, it, RR(x0, x1, y0, y1, 14, 3), 495, 525, 'oak', 8, 2)
    for (x, y) in ((x0 + 26, y0 + 26), (x1 - 26, y0 + 26), (x0 + 26, y1 - 26), (x1 - 26, y1 - 26)):
        c.PRZ(it, RR(x - 20, x + 20, y - 20, y + 20, 8, 2), 0, 495, 'oak')
    # drawer box
    c.B(it, x0 + 22, x1 - 22, y0 + 22, y1 - 22, 395, 495, 'oak')
    for (xa, xb) in ((x0 + 18, x0 + 22), (x1 - 22, x1 - 18)):
        c.B(it, xa, xb, y0 + 50, y1 - 50, 405, 485, 'oakd')                     # drawer front (both sides: symmetric)
    for xp in (x0 + 12, x1 - 18):
        c.B(it, xp, xp + 6, (y0 + y1) / 2.0 - 45, (y0 + y1) / 2.0 + 45, 455, 466, 'oakd')   # finger pull
    # open shelf
    c.B(it, x0 + 22, x1 - 22, y0 + 22, y1 - 22, 150, 175, 'oak')
