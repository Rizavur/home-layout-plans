# Scandinavian / Nordic furniture family: light oak, slim tapered splayed legs, raised airy forms, soft rounded shapes.
import math
import planlib as P

_loft = P._loft


def _ring(x, y, z, r, n=8):
    return [(x + r * math.cos(2 * math.pi * k / n), y + r * math.sin(2 * math.pi * k / n), z) for k in range(n)]


def _leg(it, top, bot, rt, rb, m='oak', n=8):
    """Tapered (and possibly splayed) round leg: top=(x,y,z) wide end, bot=(x,y,z) narrow foot. Horizontal rings."""
    _loft(it, _ring(bot[0], bot[1], bot[2], rb, n), _ring(top[0], top[1], top[2], rt, n), m)


def _rod(it, p, q, r, m='blksteel', n=6):
    """Thin straight rod between 3D points p and q (rings perpendicular to the rod)."""
    d = (q[0] - p[0], q[1] - p[1], q[2] - p[2]); L = math.sqrt(d[0] ** 2 + d[1] ** 2 + d[2] ** 2) or 1.0
    d = (d[0] / L, d[1] / L, d[2] / L)
    a = (0.0, 0.0, 1.0) if abs(d[2]) < 0.9 else (1.0, 0.0, 0.0)
    e1 = (d[1] * a[2] - d[2] * a[1], d[2] * a[0] - d[0] * a[2], d[0] * a[1] - d[1] * a[0])
    l1 = math.sqrt(sum(v * v for v in e1)); e1 = tuple(v / l1 for v in e1)
    e2 = (d[1] * e1[2] - d[2] * e1[1], d[2] * e1[0] - d[0] * e1[2], d[0] * e1[1] - d[1] * e1[0])
    def ring(o):
        return [tuple(o[i] + r * (math.cos(2 * math.pi * k / n) * e1[i] + math.sin(2 * math.pi * k / n) * e2[i]) for i in range(3)) for k in range(n)]
    _loft(it, ring(p), ring(q), m)


# ======================================================================== sofa
def sofa(c, it, face, cx, cy, W, D, nseat, armL=True, armR=True, chaise=None, body='sofa', cush='sofa2', pil=('pil1', 'pil2')):
    T = c.LF(face, cx, cy)
    fv = {'+x': (1.0, 0.0), '-x': (-1.0, 0.0), '+y': (0.0, 1.0), '-y': (0.0, -1.0)}[face]
    Rv = (-fv[1], fv[0], 0.0); F = (fv[0], fv[1], 0.0)
    u0, u1 = -W / 2.0, W / 2.0
    zl = 180                      # leg height: raised, airy
    zf = 300                      # top of the thin seat frame
    zs = 440                      # seat cushion top
    arm = 85; back = 140

    def leg_at(u, v, su, sv):
        t = T(u, v); b = T(u + su * 22, v + sv * 22)
        _leg(it, (t[0], t[1], zl), (b[0], b[1], 0), 19, 11, 'oak', 10)

    # tapered splayed oak legs
    for (u, v, su, sv) in ((u0 + 75, -75, -1, 1), (u1 - 75, -75, 1, 1), (u0 + 75, -D + 75, -1, -1), (u1 - 75, -D + 75, 1, -1)):
        leg_at(u, v, su, sv)
    if W > 2000:
        leg_at(0, -D + 75, 0, -1)
    # thin upholstered frame / seat base, slim back frame
    P.soft_slab(c, it, c.LP(T, c.RRECT(u0 + 4, u1 - 4, -D + 4, -4, 30, 4)), zl, zf, body, 14, 2)
    P.soft_slab(c, it, c.LP(T, c.RRECT(u0, u1, -D, -D + back, 30, 4)), zf - 10, 660, body, 30, 3, False)
    s0, s1 = u0, u1
    if armL:
        P.soft_slab(c, it, c.LP(T, c.RRECT(u0, u0 + arm, -D, 0, 36, 4)), zf - 10, 610, body, 36, 3, False); s0 = u0 + arm
    if armR:
        P.soft_slab(c, it, c.LP(T, c.RRECT(u1 - arm, u1, -D, 0, 36, 4)), zf - 10, 610, body, 36, 3, False); s1 = u1 - arm
    # chaise extension (frame + legs)
    if chaise is not None:
        c0, c1, Lc = chaise
        P.soft_slab(c, it, c.LP(T, c.RRECT(c0 + 4, c1 - 4, -40, Lc - 4, 30, 4)), zl, zf, body, 14, 2)
        for (u, su) in ((c0 + 75, -1), (c1 - 75, 1)):
            leg_at(u, Lc - 75, su, 1)
    # neat boxy seat cushions
    L = (s1 - s0) / float(nseat)
    for i in range(nseat):
        a = s0 + i * L
        P.soft_slab(c, it, c.LP(T, c.RRECT(a + 4, a + L - 4, -D + back + 4, -6, 30, 4)), zf, zs, cush, 22, 2)
        # separate back cushion, leaning back ~10 deg, resting on the seat
        o = T(a + L / 2.0, -D + back + 80)
        P.cushion3d(c, it, (o[0], o[1], zs + 205), Rv, P._vec_tilt(F, 10), L - 12, 410, 160, cush, 0.35, 0.012)
        # buttons on the seat cushion front-centre line
        for fr in (0.33, 0.67):
            p = T(a + L / 2.0, -D + back + (D - back) * fr)
            c.CYL(it, p[0], p[1], 11, zs - 3, zs + 3, body, 8)
    if chaise is not None:
        c0, c1, Lc = chaise
        P.soft_slab(c, it, c.LP(T, c.RRECT(c0 + 4, c1 - 4, -2, Lc - 6, 30, 4)), zf, zs, cush, 22, 2)
    # two scatter pillows leaning on the back cushions, near the ends
    span = s1 - s0
    off = 300 if span > 1300 else span * 0.3
    for (uc, m, rot) in ((s0 + off, pil[0], 1), (s1 - off, pil[1], -1)):
        o = T(uc, -D + back + 230)
        P.cushion3d(c, it, (o[0], o[1], zs + 200), Rv, P._vec_tilt(F, 16), 420, 420, 130, m, 0.55)


# ======================================================================== bed
def bed(c, it, x0, x1, y0, y1, head, npil, deco=True):
    RRECT, PRZ = c.RRECT, c.PRZ
    s = 1 if head == '+x' else -1
    hbx = x1 if s > 0 else x0
    bx0, bx1 = (x0, x1 - 60) if s > 0 else (x0 + 60, x1)
    # softly rounded upholstered headboard on an oak back panel (vertical plane, extruded away from the wall)
    U = (0.0, 1.0, 0.0); V = (0.0, 0.0, 1.0); Wd = (-float(s), 0.0, 0.0)
    c.PR3(it, RRECT(y0 - 25, y1 + 25, 0, 1080, 140, 6), (hbx, 0, 0), U, V, Wd, 0, 22, 'oak')
    c.PR3(it, RRECT(y0 - 5, y1 + 5, 330, 1060, 125, 6), (hbx, 0, 0), U, V, Wd, 22, 70, 'headb')
    c.PR3(it, RRECT(y0 + 15, y1 - 15, 350, 1040, 110, 6), (hbx, 0, 0), U, V, Wd, 70, 82, 'headb')
    # oak frame on tapered legs, clear gap below
    zl = 210; zr = 320
    for (xx, yy, sx, sy) in ((bx0 + 70, y0 + 70, -1, -1), (bx0 + 70, y1 - 70, -1, 1), (bx1 - 70, y0 + 70, 1, -1), (bx1 - 70, y1 - 70, 1, 1)):
        _leg(it, (xx, yy, zl), (xx + sx * 18, yy + sy * 18, 0), 24, 14, 'oak', 10)
    if (y1 - y0) > 1300:
        ym = (y0 + y1) / 2.0
        for xx in (bx0 + 70, bx1 - 70):
            _leg(it, (xx, ym, zl), (xx, ym, 0), 24, 14, 'oak', 10)
    P.soft_slab(c, it, RRECT(bx0, bx1, y0, y1, 40, 4), zl, zr, 'oak', 10, 2)
    # mattress
    P.soft_slab(c, it, RRECT(bx0 + 12, bx1 - 12, y0 + 12, y1 - 12, 60, 5), zr, 530, 'linen', 40, 3)
    # puffy duvet over the foot ~70 %, falling over sides and foot
    Lb = bx1 - bx0
    if s > 0: dx0, dx1 = bx0 - 25, bx0 + Lb * 0.70
    else: dx0, dx1 = bx1 - Lb * 0.70, bx1 + 25
    P.soft_slab(c, it, RRECT(dx0, dx1, y0 - 25, y1 + 25, 70, 5), 500, 640, 'duvet', 60, 4)
    P.soft_slab(c, it, RRECT(dx0, dx1, y0 - 28, y0 - 2, 12, 2), 360, 560, 'duvet', 10, 2)
    P.soft_slab(c, it, RRECT(dx0, dx1, y1 + 2, y1 + 28, 12, 2), 360, 560, 'duvet', 10, 2)
    fx = dx0 if s > 0 else dx1 - 26
    P.soft_slab(c, it, RRECT(fx, fx + 26, y0 - 25, y1 + 25, 12, 2), 360, 560, 'duvet', 10, 2)
    # soft roll at the turned-down edge
    tb = (dx1 - 150, dx1 + 10) if s > 0 else (dx0 - 10, dx0 + 150)
    P.soft_slab(c, it, RRECT(tb[0], tb[1], y0 - 22, y1 + 22, 60, 4), 560, 650, 'duvet', 40, 3)
    # upright pillows leaning against the headboard
    F = (-float(s), 0.0, 0.0); Up = (0.0, 1.0, 0.0) if s > 0 else (0.0, -1.0, 0.0)
    Wb = y1 - y0; pw = (Wb - 60) / float(npil)
    for i in range(npil):
        yc = y0 + 30 + pw * (i + 0.5)
        P.cushion3d(c, it, (hbx - s * 170, yc, 790), Up, P._vec_tilt(F, 14), pw - 40, 520, 160, 'linen2', 0.55)
        P.cushion3d(c, it, (hbx - s * 300, yc, 740), Up, P._vec_tilt(F, 18), pw - 70, 440, 150, 'linen2', 0.55)
    if deco:
        yc = (y0 + y1) / 2.0
        if npil == 2:
            P.cushion3d(c, it, (hbx - s * 420, yc, 690), Up, P._vec_tilt(F, 18), 560, 300, 130, 'pil1', 0.55)
        else:
            P.cushion3d(c, it, (hbx - s * 420, yc, 690), Up, P._vec_tilt(F, 18), 360, 260, 120, 'pil1', 0.55)
        # folded throw across the foot
        tx = (bx0 + 120, bx0 + 480) if s > 0 else (bx1 - 480, bx1 - 120)
        P.soft_slab(c, it, RRECT(tx[0], tx[1], y0 - 32, y1 + 32, 16, 3), 636, 662, 'throw', 10, 2)
        c.B(it, tx[0], tx[1], y0 - 42, y0 - 30, 420, 662, 'throw'); c.B(it, tx[0], tx[1], y1 + 30, y1 + 42, 420, 662, 'throw')


# ======================================================================== dining
def dining_table(c, it, x0, x1, y0, y1):
    RRECT = c.RRECT
    # thin oak top with a bevelled underside edge
    c.PRZ(it, RRECT(x0 + 14, x1 - 14, y0 + 14, y1 - 14, 46, 5), 734, 742, 'oak')
    c.PRZ(it, RRECT(x0 + 6, x1 - 6, y0 + 6, y1 - 6, 54, 5), 742, 747, 'oak')
    P.soft_slab(c, it, RRECT(x0, x1, y0, y1, 60, 5), 747, 758, 'oak', 4, 2, False)
    # slim apron set well back
    ins = 150
    c.PRZ(it, RRECT(x0 + ins, x1 - ins, y0 + ins - 20, y0 + ins, 4, 1), 690, 734, 'oak')
    c.PRZ(it, RRECT(x0 + ins, x1 - ins, y1 - ins, y1 - ins + 20, 4, 1), 690, 734, 'oak')
    c.PRZ(it, RRECT(x0 + ins - 20, x0 + ins, y0 + ins, y1 - ins, 4, 1), 690, 734, 'oak')
    c.PRZ(it, RRECT(x1 - ins, x1 - ins + 20, y0 + ins, y1 - ins, 4, 1), 690, 734, 'oak')
    # four splayed, tapered round legs set in from the corners
    for (sx, sy) in ((-1, -1), (1, -1), (-1, 1), (1, 1)):
        xt = (x0 + 160) if sx < 0 else (x1 - 160); yt = (y0 + 155) if sy < 0 else (y1 - 155)
        _leg(it, (xt, yt, 734), (xt + sx * 55, yt + sy * 45, 0), 30, 17, 'oak', 12)


def dchair(c, it, cx, cy, back):
    """Moulded one-piece shell chair on splayed oak dowel legs with black wire cross-bracing."""
    bd = {'-y': (0, -1), '+y': (0, 1), '-x': (-1, 0), '+x': (1, 0)}[back]
    px, py = -bd[1], bd[0]
    def L(u, v, z=0.0):            # u = sideways, v = towards the back
        return (cx + px * u + bd[0] * v, cy + py * u + bd[1] * v, z)
    zs = 430
    # legs (top under the seat, splayed out to the footprint)
    tops = {}; mids = {}
    for (su, sv) in ((-1, -1), (1, -1), (-1, 1), (1, 1)):
        t = L(su * 135, sv * 125, zs - 15); b = L(su * 205, sv * 200, 0)
        _leg(it, t, b, 15, 10, 'oak', 8)
        f = 0.40   # brace height fraction from the floor
        mids[(su, sv)] = (b[0] + (t[0] - b[0]) * f, b[1] + (t[1] - b[1]) * f, (t[2]) * f)
    # black steel cross braces: side rails + an X
    _rod(it, mids[(-1, -1)], mids[(-1, 1)], 4); _rod(it, mids[(1, -1)], mids[(1, 1)], 4)
    _rod(it, mids[(-1, -1)], mids[(1, 1)], 4); _rod(it, mids[(1, -1)], mids[(-1, 1)], 4)
    # steel mounting plate
    c.PRZ(it, [L(u, v)[:2] for (u, v) in ((-150, -140), (150, -140), (150, 140), (-150, 140))], zs - 15, zs, 'blksteel')
    # seat pan: rounded, slightly dished (raised side/front edges)
    seat = [L(u, v)[:2] for (u, v) in c.RRECT(-230, 230, -215, 205, 110, 5)]
    P.soft_slab(c, it, seat, zs, zs + 26, 'seat', 10, 2)
    rim = [L(u, v)[:2] for (u, v) in c.RRECT(-230, 230, -215, 205, 110, 5)]
    c.SLABH(it, rim, c.inset(rim, 26), zs + 20, zs + 38, 'seat', 'seat')
    # back shell: curved band lofted from the rear of the seat, flaring wider and leaning back
    oc = L(0, -60)
    th = math.atan2(bd[1], bd[0])
    levels = [(zs + 20, 0.0), (zs + 110, 0.0), (zs + 200, 0.0), (zs + 290, 0.0), (zs + 360, 0.0), (zs + 400, 1.0)]
    rings = []
    for (z, rnd) in levels:
        h = (z - zs - 20) / 380.0
        sh = (z - zs) * math.tan(math.radians(11))
        R = 270 + 20 * h
        span = math.radians(52 - 6 * h - rnd * 4)
        ro = R + 7; ri = R - 7
        o = (oc[0] + bd[0] * sh, oc[1] + bd[1] * sh)
        n = 8
        outer = [(o[0] + ro * math.cos(th - span + 2 * span * k / n), o[1] + ro * math.sin(th - span + 2 * span * k / n), z) for k in range(n + 1)]
        inner = [(o[0] + ri * math.cos(th + span - 2 * span * k / n), o[1] + ri * math.sin(th + span - 2 * span * k / n), z) for k in range(n + 1)]
        rings.append(outer + inner)
    for k in range(len(rings) - 1): _loft(it, rings[k], rings[k + 1], 'seat')


# ======================================================================== living
def coffee_table(c, it, cx, cy, a, b, ztop):
    """Oval oak tray-top table on four splayed tapered legs, with a thin raised rim."""
    A = min(a - 20, 500.0); Bb = min(b - 20, 360.0)
    top = c.ELL(cx, cy, A, Bb, 48)
    c.PRZ(it, c.ELL(cx, cy, A - 10, Bb - 10, 48), ztop - 28, ztop - 18, 'oak')
    c.PRZ(it, top, ztop - 18, ztop, 'oak')
    c.SLABH(it, top, c.ELL(cx, cy, A - 16, Bb - 16, 48), ztop, ztop + 16, 'oak', 'oak')
    # under-frame ring
    c.SLABH(it, c.ELL(cx, cy, A * 0.62, Bb * 0.62, 32), c.ELL(cx, cy, A * 0.62 - 22, Bb * 0.62 - 22, 32), ztop - 70, ztop - 28, 'oak', 'oak')
    for k in range(4):
        ang = math.pi / 4 + k * math.pi / 2
        ux, uy = math.cos(ang), math.sin(ang)
        t = (cx + ux * A * 0.6, cy + uy * Bb * 0.6, ztop - 28)
        bt = (cx + ux * A * 0.82, cy + uy * Bb * 0.82, 0)
        _leg(it, t, bt, 24, 13, 'oak', 10)


def floor_lamp(c, it, x, y):
    """Tripod floor lamp: three splayed oak legs, ivory drum shade with a glowing underside."""
    apex = 1180
    for k in range(3):
        ang = math.radians(90 + 120 * k)
        fx, fy = x + 215 * math.cos(ang), y + 215 * math.sin(ang)
        tx, ty = x + 22 * math.cos(ang), y + 22 * math.sin(ang)
        _leg(it, (tx, ty, apex + 40), (fx, fy, 0), 15, 10, 'oak', 8)
    c.CYL(it, x, y, 34, apex - 20, apex + 70, 'oak', 14)          # turned joint collar
    c.CYL(it, x, y, 9, apex + 70, 1380, 'blksteel', 8)            # short stem
    c.CYL(it, x, y, 200, 1380, 1720, 'artbg', 32)                  # drum shade
    c.CYL(it, x, y, 188, 1384, 1390, 'lightw', 28)                 # glowing diffuser
    c.CYL(it, x, y, 202, 1378, 1386, 'artbg', 32)                  # lower shade rim


def lounge_chair(c, it, cx, cy, face_deg, body='cush', base='walnut'):
    """Scandinavian armchair: upholstered bucket shell on four splayed oak legs, slim oak armrests."""
    a = math.radians(face_deg)
    fx, fy = math.cos(a), math.sin(a); rx, ry = -fy, fx
    def L(u, v, z=0.0):       # u = sideways, v = forward
        return (cx + rx * u + fx * v, cy + ry * u + fy * v, z)
    zs = 380
    for (su, sv) in ((-1, -1), (1, -1), (-1, 1), (1, 1)):
        t = L(su * 215, sv * 200, zs - 40); b = L(su * 270, sv * 265, 0)
        _leg(it, t, b, 21, 12, 'oak', 10)
    # oak seat frame
    c.PRZ(it, [L(u, v)[:2] for (u, v) in c.RRECT(-260, 260, -260, 250, 60, 4)], zs - 50, zs - 10, 'oak')
    # bucket shell (back + sides) – thick lofted band wrapping round, lower towards the front
    oc = L(0, 20); th = math.atan2(-fy, -fx)
    levels = [(zs - 10, 0), (zs + 120, 0), (zs + 250, 0), (zs + 350, 0), (zs + 395, 1), (zs + 415, 2)]
    rings = []
    for (z, rnd) in levels:
        h = max(0.0, (z - zs) / 415.0)
        sh = max(0.0, z - zs) * math.tan(math.radians(9))
        span = math.radians(100 - 38 * h ** 1.2)
        ro = 300 - rnd * 12; ri = 236 + rnd * 12
        o = (oc[0] - fx * sh, oc[1] - fy * sh)
        n = 14
        outer = [(o[0] + ro * math.cos(th - span + 2 * span * k / n), o[1] + ro * math.sin(th - span + 2 * span * k / n), z) for k in range(n + 1)]
        inner = [(o[0] + ri * math.cos(th + span - 2 * span * k / n), o[1] + ri * math.sin(th + span - 2 * span * k / n), z) for k in range(n + 1)]
        rings.append(outer + inner)
    for k in range(len(rings) - 1): _loft(it, rings[k], rings[k + 1], body)
    # seat cushion
    P.soft_slab(c, it, [L(u, v)[:2] for (u, v) in c.RRECT(-240, 240, -210, 250, 90, 5)], zs - 10, zs + 90, body, 35, 3)
    # slim oak armrests floating outside the shell on angled dowel posts
    za = zs + 215
    for su in (-1, 1):
        u = su * 318
        c.PRZ(it, [L(uu, vv)[:2] for (uu, vv) in c.RRECT(u - 22, u + 22, -110, 240, 18, 3)], za, za + 24, 'oak')
        _rod(it, L(u, 200, za + 2), L(su * 235, 205, zs - 35), 14, 'oak', 8)
        _rod(it, L(u, -70, za + 2), L(su * 235, -200, zs - 35), 13, 'oak', 8)


def nightstand(c, it, x0, x1, y0, y1):
    """White drawer box with oak top on tapered splayed oak legs; round oak knobs."""
    xm, ym = (x0 + x1) / 2.0, (y0 + y1) / 2.0
    for (sx, sy) in ((-1, -1), (1, -1), (-1, 1), (1, 1)):
        xt = xm + sx * ((x1 - x0) / 2.0 - 45); yt = ym + sy * ((y1 - y0) / 2.0 - 45)
        _leg(it, (xt, yt, 240), (xt + sx * 14, yt + sy * 14, 0), 16, 10, 'oak', 8)
    P.soft_slab(c, it, c.RRECT(x0 + 10, x1 - 10, y0 + 10, y1 - 10, 22, 3), 240, 498, 'white', 8, 2)
    P.soft_slab(c, it, c.RRECT(x0, x1, y0, y1, 26, 3), 498, 522, 'oak', 6, 2)
    for (xe, sgn) in ((x0 + 10, -1), (x1 - 10, 1)):
        xa, xb = sorted([xe, xe + sgn * 2])
        c.B(it, xa, xb, y0 + 22, y1 - 22, 368, 372, 'greige')       # drawer seam
        c.B(it, xa, xb, y0 + 22, y0 + 24, 260, 480, 'greige'); c.B(it, xa, xb, y1 - 24, y1 - 22, 260, 480, 'greige')
        for zc in (433, 305):
            for k in range(3):
                d0 = xe + sgn * (2 + 6 * k); d1 = xe + sgn * (2 + 6 * (k + 1))
                r = 14 - 3 * k
                _loft(it, [(d0, ym + r * math.cos(2 * math.pi * j / 10), zc + r * math.sin(2 * math.pi * j / 10)) for j in range(10)],
                          [(d1, ym + (r - 2) * math.cos(2 * math.pi * j / 10), zc + (r - 2) * math.sin(2 * math.pi * j / 10)) for j in range(10)], 'oak')


# ======================================================================== lights
def _dome(c, it, x, y, zb, R, H, shade='white'):
    """Metal dome shade: open bottom at zb with radius R, height H, glowing disc underneath, small oak cap."""
    n = 24; steps = 6; rings = []
    for k in range(steps + 1):
        t = k / float(steps)
        ang = t * math.pi / 2 * 0.92
        r = R * math.cos(ang) if k else R
        rr = max(R * 0.22, r)
        z = zb + H * math.sin(ang) / math.sin(math.pi / 2 * 0.92)
        rings.append(_ring(x, y, z, rr, n))
    _loft(it, _ring(x, y, zb - 6, R + 4, n), _ring(x, y, zb, R + 4, n), shade)     # rolled rim
    for k in range(steps): _loft(it, rings[k], rings[k + 1], shade)
    c.CYL(it, x, y, R * 0.22, zb + H, zb + H + 6, shade, 16)
    c.CYL(it, x, y, R - 12, zb + 4, zb + 8, 'lightw', n)
    c.CYL(it, x, y, R * 0.18, zb + H + 6, zb + H + 50, 'oak', 12)               # oak socket cap
    return zb + H + 50


def dining_pendant(c, it, x0, x1, yc):
    n = 3; L = x1 - x0
    for i in range(n):
        x = x0 + L * (i + 0.5) / n
        top = _dome(c, it, x, yc, 1680, 175, 170, 'white')
        c.CYL(it, x, yc, 3, top, 2550, 'blksteel', 6)
        c.CYL(it, x, yc, 40, 2535, 2550, 'white', 16)


def bedside_pendant(c, it, cx, cy):
    top = _dome(c, it, cx, cy, 1120, 115, 110, 'white')
    c.CYL(it, cx, cy, 3, top, 2550, 'blksteel', 6)
    c.CYL(it, cx, cy, 36, 2535, 2550, 'white', 16)
