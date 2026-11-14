# Mid-century modern furniture family (1950s-60s): warm walnut frames, tapered splayed legs,
# tufted bench cushions, bolsters, organic rounded tops, opal globe lights on brass.
import math
import planlib as P

_FV = {'+x': (1.0, 0.0), '-x': (-1.0, 0.0), '+y': (0.0, 1.0), '-y': (0.0, -1.0)}


# ---------------------------------------------------------------- helpers
def _ring(x, y, z, r, n=8):
    return [(x + r * math.cos(2 * math.pi * k / n), y + r * math.sin(2 * math.pi * k / n), z) for k in range(n)]


def _leg(it, top, bot, rt, rb, m='walnut', n=8, tip=None, tiph=0):
    """Tapered (optionally splayed) round leg from top=(x,y,z) radius rt to bot=(x,y,z) radius rb.
    tip = material of a ferrule of height tiph at the foot."""
    if tip and tiph > 0:
        f = tiph / float(top[2] - bot[2])
        mx, my = bot[0] + (top[0] - bot[0]) * f, bot[1] + (top[1] - bot[1]) * f
        mr = rb + (rt - rb) * f
        P._loft(it, _ring(bot[0], bot[1], bot[2], rb, n), _ring(mx, my, bot[2] + tiph, mr, n), tip)
        P._loft(it, _ring(mx, my, bot[2] + tiph, mr, n), _ring(top[0], top[1], top[2], rt, n), m)
    else:
        P._loft(it, _ring(bot[0], bot[1], bot[2], rb, n), _ring(top[0], top[1], top[2], rt, n), m)


def _globe(c, it, x, y, zc, r, m='lightw', n=16, sl=7):
    """Sphere from stacked cylinders."""
    for k in range(sl):
        a0 = -math.pi / 2 + math.pi * k / sl; a1 = -math.pi / 2 + math.pi * (k + 1) / sl
        rr = r * math.cos((a0 + a1) / 2) * 1.04
        c.CYL(it, x, y, rr, zc + r * math.sin(a0), zc + r * math.sin(a1), m, n)


def _rod(it, p0, p1, r, m, n=6):
    """Thin straight rod between two 3D points (any direction)."""
    d = [p1[i] - p0[i] for i in range(3)]; L = math.sqrt(sum(v * v for v in d)) or 1.0
    w = [v / L for v in d]
    a = (0.0, 0.0, 1.0) if abs(w[2]) < 0.9 else (1.0, 0.0, 0.0)
    u = (a[1] * w[2] - a[2] * w[1], a[2] * w[0] - a[0] * w[2], a[0] * w[1] - a[1] * w[0])
    ul = math.sqrt(sum(v * v for v in u)); u = [v / ul for v in u]
    v_ = (w[1] * u[2] - w[2] * u[1], w[2] * u[0] - w[0] * u[2], w[0] * u[1] - w[1] * u[0])
    def ring(p):
        return [tuple(p[i] + r * (math.cos(2 * math.pi * k / n) * u[i] + math.sin(2 * math.pi * k / n) * v_[i]) for i in range(3)) for k in range(n)]
    P._loft(it, ring(p0), ring(p1), m)


def _superell(cx, cy, a, b, e=4.0, n=40):
    pts = []
    for k in range(n):
        t = 2 * math.pi * k / n; ct, st = math.cos(t), math.sin(t)
        pts.append((cx + a * math.copysign(abs(ct) ** (2.0 / e), ct), cy + b * math.copysign(abs(st) ** (2.0 / e), st)))
    return pts


def _rect(x0, x1, y0, y1):
    return [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]


def _tufted(c, it, T, u0, u1, v0, v1, z0, z1, m, btn, cols, rows=2, gap=4):
    """Bench cushion with a grid of puffed panels separated by grooves and buttons at the crossings."""
    P.soft_slab(c, it, c.LP(T, c.RRECT(u0, u1, v0, v1, 45, 4)), z0, z1 - 14, m, 30, 2)
    du = (u1 - u0 - 30) / float(cols); dv = (v1 - v0 - 30) / float(rows)
    for i in range(cols):
        for j in range(rows):
            a0 = u0 + 15 + i * du + gap / 2.0; a1 = a0 + du - gap
            b0 = v0 + 15 + j * dv + gap / 2.0; b1 = b0 + dv - gap
            c.puff(it, c.LP(T, _rect(a0, a1, b0, b1)), z1 - 16, z1, m, 6, 14)
    for i in range(1, cols):
        for j in range(1, rows):
            p = T(u0 + 15 + i * du, v0 + 15 + j * dv); c.CYL(it, p[0], p[1], 11, z1 - 22, z1 - 9, btn, 6)


# ---------------------------------------------------------------- sofa
def sofa(c, it, face, cx, cy, W, D, nseat, armL=True, armR=True, chaise=None, body='sofa', cush='sofa2', pil=('pil1', 'pil2')):
    T = c.LF(face, cx, cy)
    fv = _FV[face]; F = (fv[0], fv[1], 0.0); Rv = (-fv[1], fv[0], 0.0)
    u0, u1 = -W / 2.0, W / 2.0
    arm = 95; zr0, zr1 = 175, 235          # wooden base rail
    s0 = u0 + (arm if armL else 0); s1 = u1 - (arm if armR else 0)
    # tapered, splayed walnut legs
    legs = [(u0 + 110, -90, -1, 1), (u1 - 110, -90, 1, 1), (u0 + 110, -D + 90, -1, -1), (u1 - 110, -D + 90, 1, -1)]
    if W > 1900: legs += [(0, -90, 0, 1), (0, -D + 90, 0, -1)]
    for (u, v, su, sv) in legs:
        a = T(u, v); b = T(u + su * 35, v + sv * 35)
        _leg(it, (a[0], a[1], zr0 + 2), (b[0], b[1], 0), 22, 12, 'walnut', 8)
    # walnut base rail / plinth frame, slightly tapered underside
    P._loft(it, [(x, y, zr0) for (x, y) in c.LP(T, c.RRECT(u0 + 18, u1 - 18, -D + 18, -12, 30, 3))],
            [(x, y, zr0 + 22) for (x, y) in c.LP(T, c.RRECT(u0 + 8, u1 - 8, -D + 8, -4, 34, 3))], 'walnut')
    c.PRZ(it, c.LP(T, c.RRECT(u0 + 8, u1 - 8, -D + 8, -4, 34, 3)), zr0 + 22, zr1, 'walnut')
    # upholstered deck
    c.PRZ(it, c.LP(T, _rect(s0 + 4, s1 - 4, -D + 30, -30)), zr1, 300, body)
    # wooden side frames: front + back posts, flat armrest board on top, upholstered inset panel
    for (on, ua, ub) in ((armL, u0, u0 + arm), (armR, u1 - arm, u1)):
        if not on: continue
        um = (ua + ub) / 2.0
        c.PRZ(it, c.LP(T, _rect(ua + 18, ub - 18, -D + 60, -60)), zr1, 520, body)        # inset fabric panel
        for (va, vb) in ((-80, -18), (-D + 18, -D + 80)):
            c.PRZ(it, c.LP(T, c.RRECT(ua + 10, ub - 10, va, vb, 10, 2)), zr1, 545, 'walnut')
        P.soft_slab(c, it, c.LP(T, c.RRECT(ua, ub, -D + 4, 8, 40, 4)), 545, 580, 'walnut', 8, 2)
        c.PRZ(it, c.LP(T, _rect(ua + 14, ub - 14, -D + 70, -70)), 520, 545, 'walnut')
    # tufted back: leaning panel with two rows of tufts on its face
    tilt = 10; V = P._vec_tilt(F, tilt); Wd = (F[0] * math.cos(math.radians(tilt)), F[1] * math.cos(math.radians(tilt)), math.sin(math.radians(tilt)))
    BH = 550; bth = 120; vb = -D + 30 + BH * math.sin(math.radians(tilt))
    o = T(0, vb); O = (o[0], o[1], 300)
    bu0, bu1 = s0 + 6, s1 - 6
    # T maps u to Rv direction; PR3 polygon coords (u, height)
    c.PR3(it, c.RRECT(bu0, bu1, 0, BH, 40, 3), O, Rv, V, Wd, 0, bth, body)
    c.PR3(it, c.RRECT(bu0 + 4, bu1 - 4, 4, BH - 4, 36, 3), O, Rv, V, Wd, bth, bth + 20, cush)
    ncol = max(3, int(round((bu1 - bu0) / 330.0)))
    du = (bu1 - bu0 - 40) / float(ncol)
    for i in range(ncol):
        for (h0, h1) in ((150, 340), (344, 532)):
            a0 = bu0 + 20 + i * du + 2; a1 = a0 + du - 4
            c.PR3(it, _rect(a0, a1, h0, h1), O, Rv, V, Wd, bth + 20, bth + 32, cush)
            c.PR3(it, _rect(a0 + 16, a1 - 16, h0 + 14, h1 - 14), O, Rv, V, Wd, bth + 32, bth + 40, cush)
    for i in range(1, ncol):
        u = bu0 + 20 + i * du
        c.PR3(it, c.RRECT(u - 10, u + 10, 332, 352, 8, 1), O, Rv, V, Wd, bth + 22, bth + 34, 'charcoal')
    # single long tufted bench seat cushion
    sv0 = -D + 30 + bth + 18
    _tufted(c, it, T, s0 + 6, s1 - 6, sv0, -10, 300, 440, cush, 'charcoal', max(3, int(round((s1 - s0) / 330.0))), 2)
    # chaise extension
    if chaise is not None:
        c0, c1, Lc = chaise
        for (u, su) in ((c0 + 90, -1), (c1 - 90, 1)):
            a = T(u, Lc - 90); b = T(u + su * 35, Lc - 55)
            _leg(it, (a[0], a[1], zr0 + 2), (b[0], b[1], 0), 22, 12, 'walnut', 8)
        P._loft(it, [(x, y, zr0) for (x, y) in c.LP(T, c.RRECT(c0 + 18, c1 - 18, -20, Lc - 12, 30, 3))],
                [(x, y, zr0 + 22) for (x, y) in c.LP(T, c.RRECT(c0 + 8, c1 - 8, -20, Lc - 4, 34, 3))], 'walnut')
        c.PRZ(it, c.LP(T, c.RRECT(c0 + 8, c1 - 8, -20, Lc - 4, 34, 3)), zr0 + 22, zr1, 'walnut')
        c.PRZ(it, c.LP(T, _rect(c0 + 30, c1 - 30, -30, Lc - 30)), zr1, 300, body)
        _tufted(c, it, T, c0 + 6, c1 - 6, -4, Lc - 10, 300, 440, cush, 'charcoal', 2, 3)
    # cylindrical bolsters against each arm
    rb = 95
    for (on, ub, sgn) in ((armL, s0 + 6, 1), (armR, s1 - 6, -1)):
        if not on: continue
        uc = ub + sgn * (rb + 4)
        o = T(uc, sv0 + 10); O2 = (o[0], o[1], 440 + rb - 6)
        circ = [(rb * math.cos(2 * math.pi * k / 14), rb * math.sin(2 * math.pi * k / 14)) for k in range(14)]
        Lb = -40 - (sv0 + 10)
        c.PR3(it, circ, O2, Rv, (0.0, 0.0, 1.0), F, 0, Lb, body)
        for t in (-6, Lb):
            c.PR3(it, [(x * 0.35, y * 0.35) for (x, y) in circ], O2, Rv, (0.0, 0.0, 1.0), F, t, t + 6, 'charcoal')
        for t in (Lb * 0.2, Lb * 0.8):
            c.PR3(it, [(x * 1.03, y * 1.03) for (x, y) in circ], O2, Rv, (0.0, 0.0, 1.0), F, t, t + 8, cush)
    # two scatter pillows leaning on the back
    span = s1 - s0
    spots = ((s0 + rb * 2 + 260, pil[0], 6), (s1 - rb * 2 - 260, pil[1], -6)) if span > 1300 else ((s0 + span * 0.32, pil[0], 6), (s1 - span * 0.32, pil[1], -6))
    for (uc, m, rot) in spots:
        o = T(uc, sv0 + 140)
        P.cushion3d(c, it, (o[0], o[1], 440 + 190), Rv, P._vec_tilt(F, 18), 420, 400, 140, m, 0.55)


# ---------------------------------------------------------------- bed
def bed(c, it, x0, x1, y0, y1, head, npil, deco=True):
    PRZ, RRECT = c.PRZ, c.RRECT
    s = 1 if head == '+x' else -1
    hbx = x1 if s > 0 else x0
    bx0, bx1 = (x0, x1 - 60) if s > 0 else (x0 + 60, x1)
    hf = hbx - s * 60                     # headboard front face
    ym = (y0 + y1) / 2.0
    # wide walnut panel headboard (overhangs the bed 40 mm each side) on its own tapered legs
    ha, hb = sorted([hbx, hbx - s * 45])
    hy0, hy1 = y0 - 40, y1 + 40
    for yy in (hy0 + 90, hy1 - 90):
        _leg(it, ((ha + hb) / 2.0, yy, 230), ((ha + hb) / 2.0 - s * 25, yy, 0), 20, 11, 'walnut', 8)
    P.soft_slab(c, it, RRECT(ha, hb, hy0, hy1, 18, 3), 220, 1150, 'walnut', 14, 2)
    # recessed horizontal reveal + vertical book-matched grooves (front face)
    xf = ha if s > 0 else hb             # front face x
    xg0, xg1 = sorted([xf, xf - s * 4])
    c.B(it, xg0, xg1, hy0 + 30, hy1 - 30, 1030, 1038, 'walnut2')
    n = 6
    for k in range(1, n):
        yy = hy0 + (hy1 - hy0) * k / float(n)
        c.B(it, xg0, xg1, yy - 4, yy + 4, 360, 1120, 'walnut2')
    # walnut platform frame on tapered splayed legs
    for (xx, sx) in ((bx0 + 120, -1), (bx1 - 120, 1)):
        for (yy, sy) in ((y0 + 120, -1), (y1 - 120, 1)):
            _leg(it, (xx, yy, 182), (xx + sx * 30, yy + sy * 30, 0), 24, 13, 'walnut', 8)
    P._loft(it, [(x, y, 180) for (x, y) in RRECT(bx0 + 25, bx1 - 25, y0 + 25, y1 - 25, 40, 3)],
            [(x, y, 205) for (x, y) in RRECT(bx0, bx1, y0, y1, 50, 3)], 'walnut')
    P.soft_slab(c, it, RRECT(bx0, bx1, y0, y1, 50, 3), 205, 360, 'walnut', 10, 2, False)
    # mattress
    P.soft_slab(c, it, RRECT(bx0 + 45, bx1 - 45, y0 + 45, y1 - 45, 60, 4), 330, 545, 'linen', 40, 3)
    L = bx1 - bx0
    # neat, tucked duvet with a folded linen turn-down
    if s > 0: dx0, dx1 = bx0 + 25, bx0 + L * 0.70
    else: dx0, dx1 = bx1 - L * 0.70, bx1 - 25
    P.soft_slab(c, it, RRECT(dx0, dx1, y0 + 22, y1 - 22, 40, 4), 530, 585, 'duvet', 22, 2)
    c.B(it, dx0, dx1, y0 + 18, y0 + 40, 380, 570, 'duvet'); c.B(it, dx0, dx1, y1 - 40, y1 - 18, 380, 570, 'duvet')
    fx = dx0 if s > 0 else dx1 - 22
    c.B(it, fx, fx + 22, y0 + 18, y1 - 18, 380, 570, 'duvet')
    tb = (dx1 - 150, dx1) if s > 0 else (dx0, dx0 + 150)
    P.soft_slab(c, it, RRECT(tb[0], tb[1], y0 + 20, y1 - 20, 22, 3), 575, 605, 'linen2', 12, 2)
    if deco:   # folded blanket stripe across the foot
        tx = (bx0 + 140, bx0 + 440) if s > 0 else (bx1 - 440, bx1 - 140)
        PRZ(it, RRECT(tx[0], tx[1], y0 + 12, y1 - 12, 16, 3), 583, 600, 'throw')
        c.B(it, tx[0], tx[1], y0 + 6, y0 + 18, 420, 600, 'throw'); c.B(it, tx[0], tx[1], y1 - 18, y1 - 6, 420, 600, 'throw')
    # pillows standing upright against the headboard
    F = (-s, 0.0, 0.0); U = (0.0, 1.0, 0.0) if s > 0 else (0.0, -1.0, 0.0)
    W = y1 - y0; pw = (W - 60) / float(npil)
    for i in range(npil):
        yc = y0 + 30 + pw * (i + 0.5)
        cushion3d = P.cushion3d
        cushion3d(c, it, (hf - s * 95, yc, 545 + 215), U, P._vec_tilt(F, 8), pw - 60, 430, 150, 'linen2', 0.5)
        cushion3d(c, it, (hf - s * 230, yc, 545 + 195), U, P._vec_tilt(F, 12), pw - 90, 400, 140, 'linen2', 0.5)
        if deco:
            cushion3d(c, it, (hf - s * 345, yc, 545 + 165), U, P._vec_tilt(F, 16), min(pw - 200, 380), 340, 120, 'pil1' if i % 2 == 0 else 'pil2', 0.55)


# ---------------------------------------------------------------- dining
def dining_table(c, it, x0, x1, y0, y1):
    RR = c.RRECT
    r = 55
    top = RR(x0, x1, y0, y1, r, 5)
    c.PRZ(it, top, 744, 758, 'walnut')                                   # thin visible edge
    P._loft(it, [(x, y, 724) for (x, y) in RR(x0 + 55, x1 - 55, y0 + 55, y1 - 55, r, 5)],
            [(x, y, 744) for (x, y) in top], 'walnut')                      # knife-edge bevel underneath
    c.PRZ(it, RR(x0 + 150, x1 - 150, y0 + 130, y1 - 130, 20, 3), 660, 724, 'walnut')   # set-back apron
    for (xx, sx) in ((x0 + 210, -1), (x1 - 210, 1)):
        for (yy, sy) in ((y0 + 175, -1), (y1 - 175, 1)):
            _leg(it, (xx, yy, 724), (xx + sx * 75, yy + sy * 55, 0), 32, 15, 'walnut', 10, 'brass', 35)


def dchair(c, it, cx, cy, back):
    bd = _FV[back]; px, py = -bd[1], bd[0]
    def W(s, d, z=0): return (cx + px * s + bd[0] * d, cy + py * s + bd[1] * d, z)
    # legs: tapered, splayed, walnut
    for (s, d) in ((-1, -1), (1, -1), (-1, 1), (1, 1)):
        top = W(s * 180, d * 175, 420); bot = W(s * 205, d * 205 + (12 if d > 0 else 0), 0)
        _leg(it, top, bot, 19, 11, 'walnut', 8)
    seat = c.RRECT(cx - 222, cx + 222, cy - 222, cy + 222, 60, 3)
    P._loft(it, [(x, y, 405) for (x, y) in c.inset(seat, 22)], [(x, y, 432) for (x, y) in c.inset(seat, 6)], 'walnut')
    P.soft_slab(c, it, c.inset(seat, 10), 432, 485, 'seat', 18, 2, False)
    # back posts rising from the rear legs to the band
    oc = W(0, 8)
    th = math.degrees(math.atan2(bd[1], bd[0]))
    for sg in (-1, 1):
        p0 = W(sg * 172, 172, 420); p1 = W(sg * 172, 200, 715)
        _rod(it, p0, p1, 15, 'walnut', 8)
    # curved wraparound backrest band, open below
    def band(r0, r1, sp, n=14):
        return c.ARC(oc[0], oc[1], r1, th - sp, th + sp, n) + c.ARC(oc[0], oc[1], r0, th + sp, th - sp, n)
    c.PRZ(it, band(244, 266, 62), 700, 805, 'walnut')
    c.PRZ(it, band(248, 262, 58), 805, 812, 'walnut')


def coffee_table(c, it, cx, cy, a, b, ztop):
    A = min(a - 10, 510); Bb = min(b - 10, 340)
    top = _superell(cx, cy, A, Bb, 3.2, 44)
    c.PRZ(it, top, ztop - 14, ztop, 'walnut')
    P._loft(it, [(x, y, ztop - 34) for (x, y) in _superell(cx, cy, A - 45, Bb - 40, 3.2, 44)], [(x, y, ztop - 14) for (x, y) in top], 'walnut')
    # thinner lower shelf
    sh = c.RRECT(cx - 395, cx + 395, cy - 235, cy + 235, 70, 4)
    c.PRZ(it, sh, 140, 158, 'walnut')
    c.PRZ(it, c.inset(sh, 6), 158, 160, 'smoke')
    for sx in (-1, 1):
        for sy in (-1, 1):
            top_ = (cx + sx * 330, cy + sy * 175, ztop - 34); bot = (cx + sx * 380, cy + sy * 228, 0)
            _leg(it, top_, bot, 24, 12, 'walnut', 8, 'brass', 45)


# ---------------------------------------------------------------- lighting
def floor_lamp(c, it, x, y):
    # walnut tripod
    for k in range(3):
        a = math.radians(90 + 120 * k)
        _leg(it, (x + 18 * math.cos(a), y + 18 * math.sin(a), 520), (x + 185 * math.cos(a), y + 185 * math.sin(a), 0), 17, 10, 'walnut', 8, 'brass', 30)
    c.CYL(it, x, y, 30, 470, 560, 'brass', 12)
    c.CYL(it, x, y, 10, 560, 1640, 'brass', 8)
    # three opal globes on short brass arms at staggered heights
    for (ang, zc, R) in ((20, 1180, 95), (150, 1420, 95), (270, 1650, 100)):
        a = math.radians(ang); gx, gy = x + 120 * math.cos(a), y + 120 * math.sin(a)
        _rod(it, (x, y, zc - R - 40), (gx, gy, zc - R - 40), 7, 'brass', 6)
        c.CYL(it, gx, gy, 7, zc - R - 47, zc - R + 4, 'brass', 6)
        c.CYL(it, gx, gy, 32, zc - R - 8, zc - R + 18, 'brass', 12)
        _globe(c, it, gx, gy, zc, R)
    c.CYL(it, x, y, 16, 1640, 1665, 'brass', 10)


def lounge_chair(c, it, cx, cy, face_deg, body='cush', base='walnut'):
    """Eames-style lounge chair: moulded walnut shells with leather cushions on a black swivel star base."""
    a = math.radians(face_deg); fx, fy = math.cos(a), math.sin(a); sx, sy = -fy, fx
    def Wp(s, d, z): return (cx + sx * s + fx * d, cy + sy * s + fy * d, z)
    shell = base if base in ('walnut', 'oakd', 'oak', 'walnut2') else 'walnut'
    # star base (5 tapered arms) + column
    for k in range(5):
        t = a + math.pi + 2 * math.pi * k / 5.0
        ux, uy = math.cos(t), math.sin(t); vx, vy = -uy, ux
        def rr(rad, hw, z): return [(cx + ux * rad + vx * hw, cy + uy * rad + vy * hw, z), (cx + ux * rad - vx * hw, cy + uy * rad - vy * hw, z)]
        lo = rr(40, 30, 30) + rr(320, 14, 30)[::-1]; hi = rr(40, 30, 95) + rr(320, 14, 45)[::-1]
        P._loft(it, lo, hi, 'metal')
        c.CYL(it, cx + ux * 305, cy + uy * 305, 20, 0, 30, 'metal', 8)
    c.CYL(it, cx, cy, 55, 60, 110, 'metal', 14); c.CYL(it, cx, cy, 30, 110, 290, 'chrome', 12)
    # seat shell, tilted back ~6 deg, with sides curling up
    sh_lo = [Wp(s, d, 300 + (d + 120) * 0.10) for (s, d) in c.RRECT(-275, 275, -120, 290, 70, 3)]
    sh_hi = [Wp(s, d, 322 + (d + 120) * 0.10) for (s, d) in c.RRECT(-285, 285, -125, 295, 75, 3)]
    P._loft(it, sh_lo, sh_hi, shell)
    cu_lo = [Wp(s, d, 322 + (d + 120) * 0.10) for (s, d) in c.RRECT(-262, 262, -110, 300, 70, 3)]
    cu_mid = [Wp(s, d, 395 + (d + 120) * 0.10) for (s, d) in c.RRECT(-262, 262, -110, 300, 70, 3)]
    cu_hi = [Wp(s, d, 415 + (d + 120) * 0.10) for (s, d) in c.RRECT(-238, 238, -95, 282, 55, 3)]
    P._loft(it, cu_lo, cu_mid, body); P._loft(it, cu_mid, cu_hi, body)
    P._loft(it, [Wp(s, d, 416 + (d + 120) * 0.10) for (s, d) in _rect(-238, 238, 90, 96)], [Wp(s, d, 418 + (d + 120) * 0.10) for (s, d) in _rect(-238, 238, 90, 96)], 'leather3')
    # back + headrest: curved shells (concave towards the sitter) leaning back 24 deg
    tilt = math.radians(28); up = (-fx * math.sin(tilt), -fy * math.sin(tilt), math.cos(tilt)); fw = (fx * math.cos(tilt), fy * math.cos(tilt), math.sin(tilt))
    base0 = Wp(0, -95, 330)
    def P3(s, t, w):
        return (base0[0] + sx * s + up[0] * t + fw[0] * w, base0[1] + sy * s + up[1] * t + fw[1] * w, base0[2] + up[2] * t + fw[2] * w)
    def band(t, hw, w0, w1, cur=70, n=10):
        outer = [P3(-hw + 2 * hw * k / n, t, w0 + cur * ((-hw + 2 * hw * k / n) / hw) ** 2) for k in range(n + 1)]
        inner = [P3(hw - 2 * hw * k / n, t, w1 + cur * ((hw - 2 * hw * k / n) / hw) ** 2) for k in range(n + 1)]
        return outer + inner
    for (t0, t1) in ((20, 450), (470, 690)):
        hwa, hwb = (300, 300) if t0 < 400 else (285, 260)
        # rounded ends: shrink first/last few mm
        P._loft(it, band(t0, hwa - 15, 0, 18), band(t0 + 15, hwa, 0, 18), shell)
        P._loft(it, band(t0 + 15, hwa, 0, 18), band(t1 - 15, hwb, 0, 18), shell)
        P._loft(it, band(t1 - 15, hwb, 0, 18), band(t1, hwb - 15, 0, 18), shell)
        # leather cushion on the front of the shell
        P._loft(it, band(t0 + 10, hwa - 48, 18, 40), band(t0 + 35, hwa - 38, 18, 95), body)
        P._loft(it, band(t0 + 35, hwa - 38, 18, 95), band(t1 - 35, hwb - 38, 18, 95), body)
        P._loft(it, band(t1 - 35, hwb - 38, 18, 95), band(t1 - 10, hwb - 48, 18, 40), body)
        # pleat crease
        tm = (t0 + t1) / 2.0
        P._loft(it, band(tm - 3, hwa - 40, 94, 98), band(tm + 3, hwa - 40, 94, 98), 'leather3')
    # armrests: dark arms from the back shell forward with padded tops
    for sg in (-1, 1):
        s = sg * 300
        p0 = Wp(s, -150, 560); p1 = Wp(s, 250, 545)
        _rod(it, (p0[0], p0[1], 545), (p1[0], p1[1], 530), 16, 'metal', 8)
        P._loft(it, [Wp(s + e, d, 556) for (e, d) in _rect(-34, 34, -140, 250)], [Wp(s + e, d, 590) for (e, d) in _rect(-30, 30, -130, 240)], body)
        q = Wp(s, 200, 0); c.CYL(it, q[0], q[1], 14, 380, 535, 'metal', 8)


def nightstand(c, it, x0, x1, y0, y1):
    xm = (x0 + x1) / 2.0; ym = (y0 + y1) / 2.0
    # tapered splayed legs, kept inside the footprint
    for (xx, sx) in ((x0 + 70, -1), (x1 - 70, 1)):
        for (yy, sy) in ((y0 + 65, -1), (y1 - 65, 1)):
            _leg(it, (xx, yy, 185), (xx + sx * 25, yy + sy * 22, 0), 17, 10, 'walnut', 8)
    # case: rounded top, sides, bottom; open shelf below one drawer
    P.soft_slab(c, it, c.RRECT(x0 + 2, x1 - 2, y0, y1, 22, 3), 500, 525, 'walnut', 6, 2)
    c.PRZ(it, c.RRECT(x0 + 8, x1 - 8, y0 + 4, y1 - 4, 12, 2), 180, 202, 'walnut')
    for (ya, yb) in ((y0 + 4, y0 + 24), (y1 - 24, y1 - 4)):
        c.B(it, x0 + 8, x1 - 8, ya, yb, 202, 500, 'walnut')
    c.B(it, xm - 8, xm + 8, y0 + 24, y1 - 24, 202, 345, 'walnut')        # centre back panel for the shelf
    c.B(it, x0 + 20, x1 - 20, y0 + 24, y1 - 24, 345, 360, 'walnut')       # drawer bottom / shelf ceiling
    # drawer box + fronts on both x faces (symmetric), with a recessed brass finger pull in the top edge
    c.B(it, x0 + 14, x1 - 14, y0 + 26, y1 - 26, 362, 494, 'walnut')
    for (xa, xb) in ((x0 + 8, x0 + 14), (x1 - 14, x1 - 8)):
        c.B(it, xa, xb, y0 + 27, y1 - 27, 364, 492, 'walnut')
        c.B(it, xa - 1, xb + 1, ym - 55, ym + 55, 470, 492, 'brass')
        c.B(it, xa - 2, xb + 2, ym - 45, ym + 45, 478, 492, 'charcoal')
    # a book on the open shelf
    c.B(it, xm + 30, x1 - 40, y0 + 70, y1 - 90, 202, 228, 'oakd')


def dining_pendant(c, it, x0, x1, yc):
    xm = (x0 + x1) / 2.0; L = x1 - x0
    # brass bar canopy with three opal globes on brass rods at slightly staggered drops
    c.PRZ(it, c.RRECT(x0 + 80, x1 - 80, yc - 30, yc + 30, 28, 4), 2530, 2550, 'brass')
    for (k, drop) in ((-1, 1830), (0, 1760), (1, 1830)):
        x = xm + k * L * 0.36
        R = 150
        c.CYL(it, x, yc, 5, drop + R + 30, 2530, 'brass', 6)
        c.CYL(it, x, yc, 45, drop + R - 10, drop + R + 30, 'brass', 14)
        c.CYL(it, x, yc, 55, drop + R - 16, drop + R - 10, 'brass', 14)
        _globe(c, it, x, yc, drop, R, 'lightw', 16, 8)


def bedside_pendant(c, it, cx, cy):
    c.CYL(it, cx, cy, 45, 2535, 2550, 'brass', 16)
    c.CYL(it, cx, cy, 5, 1340, 2535, 'brass', 6)
    c.CYL(it, cx, cy, 30, 1300, 1345, 'brass', 12)
    c.CYL(it, cx, cy, 38, 1292, 1300, 'brass', 12)
    _globe(c, it, cx, cy, 1215, 105, 'lightw', 18, 8)
