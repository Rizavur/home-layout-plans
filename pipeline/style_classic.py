# Furniture family: MODERN CLASSIC / PARISIAN (also suits an Art Deco palette).
# Rolled arms, deep button tufting, turned legs, wingback headboard, pedestal bases, brass lanterns.
import math
import planlib as P

_loft = P._loft
FACE = {'+x': (1.0, 0.0), '-x': (-1.0, 0.0), '+y': (0.0, 1.0), '-y': (0.0, -1.0)}


# ----------------------------------------------------------------- helpers
def _ring(x, y, z, r, n, ph=0.0):
    return [(x + r * math.cos(2 * math.pi * k / n + ph), y + r * math.sin(2 * math.pi * k / n + ph), z) for k in range(n)]


def lathe(c, it, x, y, prof, m, n=12):
    """Turned part: prof = [(z, r), ...] bottom->top; equal z gives a step."""
    for (z0, r0), (z1, r1) in zip(prof, prof[1:]):
        if z1 - z0 < 0.5: continue
        if abs(r0 - r1) < 0.5: c.CYL(it, x, y, r0, z0, z1, m, n)
        else: _loft(it, _ring(x, y, z0, max(r0, 1), n), _ring(x, y, z1, max(r1, 1), n), m)


def _norm(v):
    L = math.sqrt(sum(a * a for a in v)) or 1.0
    return tuple(a / L for a in v)


def _cross(a, b):
    return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])


def hcyl(c, it, A, Bp, r, m, n=12, r2=None):
    """Cylinder (or cone if r2) between two 3D points."""
    d = (Bp[0] - A[0], Bp[1] - A[1], Bp[2] - A[2]); L = math.sqrt(sum(a * a for a in d))
    if L < 0.5: return
    W = _norm(d)
    U = _cross(W, (0.0, 0.0, 1.0))
    if math.sqrt(sum(a * a for a in U)) < 1e-3: U = (1.0, 0.0, 0.0)
    U = _norm(U); V = _cross(W, U)
    if r2 is None:
        pts = [(r * math.cos(2 * math.pi * k / n), r * math.sin(2 * math.pi * k / n)) for k in range(n)]
        c.PR3(it, pts, A, U, V, W, 0, L, m)
    else:
        def rg(P0, rr): return [(P0[0] + rr * (math.cos(2 * math.pi * k / n) * U[0] + math.sin(2 * math.pi * k / n) * V[0]),
                                 P0[1] + rr * (math.cos(2 * math.pi * k / n) * U[1] + math.sin(2 * math.pi * k / n) * V[1]),
                                 P0[2] + rr * (math.cos(2 * math.pi * k / n) * U[2] + math.sin(2 * math.pi * k / n) * V[2])) for k in range(n)]
        _loft(it, rg(A, r), rg(Bp, r2), m)


def sweep(c, it, path, r, m, n=10):
    """Tube of radius r swept along a 3D polyline (rings perpendicular to the local tangent)."""
    rings = []
    for i, p in enumerate(path):
        q0 = path[max(i - 1, 0)]; q1 = path[min(i + 1, len(path) - 1)]
        W = _norm((q1[0] - q0[0], q1[1] - q0[1], q1[2] - q0[2]))
        U = _cross(W, (0.0, 0.0, 1.0))
        if math.sqrt(sum(a * a for a in U)) < 1e-3: U = (1.0, 0.0, 0.0)
        U = _norm(U); V = _cross(W, U)
        rings.append([(p[0] + r * (math.cos(2 * math.pi * k / n) * U[0] + math.sin(2 * math.pi * k / n) * V[0]),
                       p[1] + r * (math.cos(2 * math.pi * k / n) * U[1] + math.sin(2 * math.pi * k / n) * V[1]),
                       p[2] + r * (math.cos(2 * math.pi * k / n) * U[2] + math.sin(2 * math.pi * k / n) * V[2])) for k in range(n)])
    for k in range(len(rings) - 1): _loft(it, rings[k], rings[k + 1], m)


def sphere(c, it, x, y, z, r, m, n=12, k=5):
    prof = []
    for i in range(k + 1):
        a = -math.pi / 2 + math.pi * i / k
        prof.append((z + r * math.sin(a), max(r * math.cos(a), 2)))
    lathe(c, it, x, y, prof, m, n)


def tuft(c, it, O, U, V, N, pts_uv, m, btn='gold', s=1.0, depth=16, bsz=9):
    """Diamond button tufting on a face. O origin, U/V in-face unit axes, N outward normal.
    pts_uv = list of diamond centres (u, v, hu, hv): half sizes hu, hv."""
    def P3(u, v, t): return (O[0] + u * U[0] + v * V[0] + t * N[0], O[1] + u * U[1] + v * V[1] + t * N[1], O[2] + u * U[2] + v * V[2] + t * N[2])
    btns = set()
    for (u, v, hu, hv) in pts_uv:
        lo = [P3(u + hu, v, 0), P3(u, v + hv, 0), P3(u - hu, v, 0), P3(u, v - hv, 0)]
        k = 0.45
        hi = [P3(u + hu * k, v, depth), P3(u, v + hv * k, depth), P3(u - hu * k, v, depth), P3(u, v - hv * k, depth)]
        _loft(it, lo, hi, m)
        for b in ((u + hu, v), (u - hu, v), (u, v + hv), (u, v - hv)): btns.add((round(b[0], 1), round(b[1], 1)))
    for (u, v) in btns:
        sq = [(-bsz, -bsz), (bsz, -bsz), (bsz, bsz), (-bsz, bsz)]
        sq = [(a * 0.7071 - b * 0.7071, a * 0.7071 + b * 0.7071) for (a, b) in sq]
        c.PR3(it, sq, P3(u, v, 0), U, V, N, -2, 7, btn)


def diamond_grid(u0, u1, v0, v1, su, sv):
    """Diamond centres filling [u0,u1]x[v0,v1]: rows every sv, staggered by su/2. Returns (u, v, su/2, sv)."""
    nu = max(1, int(round((u1 - u0) / su))); su = (u1 - u0) / float(nu)
    nv = max(1, int(round((v1 - v0) / sv))); sv = (v1 - v0) / float(nv)
    out = []
    for j in range(nv + 1):
        v = v0 + j * sv
        if j % 2 == 0: us = [u0 + su * (i + 0.5) for i in range(nu)]
        else: us = [u0 + su * i for i in range(1, nu)]
        for u in us:
            if 0 < j < nv: out.append((u, v, su / 2.0, sv))
    return out


def turned_leg(c, it, x, y, h, m='walnut', cap='brass', r=22, n=10):
    """Short turned bun / baluster leg with a brass cap at the floor."""
    k = h / 140.0
    lathe(c, it, x, y, [(0, r * 0.7), (18 * k, r * 0.7)], cap, n)
    lathe(c, it, x, y, [(18 * k, r * 0.62), (40 * k, r * 0.95), (70 * k, r * 1.08), (95 * k, r * 0.78), (112 * k, r * 0.7),
                        (124 * k, r * 1.0), (h, r * 1.0)], m, n)


# ----------------------------------------------------------------- sofa
def sofa(c, it, face, cx, cy, W, D, nseat, armL=True, armR=True, chaise=None, body='sofa', cush='sofa2', pil=('pil1', 'pil2')):
    T = c.LF(face, cx, cy); fv = FACE[face]
    F = (fv[0], fv[1], 0.0); R = (-fv[1], fv[0], 0.0); Z = (0.0, 0.0, 1.0)
    def P3(u, v, z): p = T(u, v); return (p[0], p[1], z)
    LP, RR = c.LP, c.RRECT
    u0, u1 = -W / 2.0, W / 2.0
    back = 215; arm = 200; zb = 150; zd = 375; zs = 470
    # turned legs
    legs = [(u0 + 75, -75), (u1 - 75, -75), (u0 + 75, -D + 75), (u1 - 75, -D + 75)]
    if chaise is not None: legs += [(chaise[0] + 75, chaise[2] - 75), (chaise[1] - 75, chaise[2] - 75)]
    for (u, v) in legs:
        p = T(u, v); turned_leg(c, it, p[0], p[1], zb + 5, 'walnut', 'brass', 21, 10)
    # base (skirt-less) with a bead line
    P.soft_slab(c, it, LP(T, RR(u0 + 12, u1 - 12, -D + 12, -12, 40, 4)), zb, zd, body, 28, 2)
    # back panel + rolled top
    vb = -D + back
    P.soft_slab(c, it, LP(T, RR(u0 + 8, u1 - 8, -D + 8, vb - 12, 40, 4)), zb + 20, 730, body, 20, 2, False)
    hcyl(c, it, P3(u0 + 14, vb - 80, 728), P3(u1 - 14, vb - 80, 728), 80, body, 18)
    hcyl(c, it, P3(u0 + 14, -D + 80, 712), P3(u1 - 14, -D + 80, 712), 72, body, 12)
    s0 = u0 + 12; s1 = u1 - 12
    # scrolled arms
    for (on, ua, sgn) in ((armL, u0, 1), (armR, u1, -1)):
        if not on: continue
        um = ua + sgn * 98
        a0, a1 = sorted((ua + sgn * 14, ua + sgn * (arm - 18)))
        P.soft_slab(c, it, LP(T, RR(a0, a1, -D + 20, -14, 30, 3)), zb + 20, 680, body, 20, 2, False)
        hcyl(c, it, P3(um, -D + 110, 690), P3(um, -16, 690), 94, body, 18)
        hcyl(c, it, P3(um, -16, 690), P3(um, -1, 690), 99, body, 18)                  # scroll face
        hcyl(c, it, P3(um, -4, 690), P3(um, 2, 690), 22, 'brass', 10)                 # brass rosette
        # front arm panel (scroll drops to the base)
        P.soft_slab(c, it, LP(T, RR(a0 - 6, a1 + 6, -40, -2, 12, 2)), zb + 10, 640, body, 12, 2, False)
        # tufting on the inner arm face
        if sgn > 0: s0 = ua + arm
        else: s1 = ua - arm
        fu = ua + sgn * (arm - 18)
        O = P3(fu, 0, 0); N = (R[0] * sgn, R[1] * sgn, 0.0)
        gr = diamond_grid(min(-60, -D + back + 60) * 1.0, -60, zs + 15, 610, 125, 62)
        tuft(c, it, O, F, Z, N, [(v, z, hu, hv) for (v, z, hu, hv) in gr], body, 'gold', depth=12)
    # tufting on the inside back
    O = P3(0, vb, 0)
    gr = diamond_grid(s0 + 20, s1 - 20, zs + 20, 700, 135, 70)
    tuft(c, it, O, R, Z, F, gr, body, 'gold', depth=20, bsz=10)
    # plump seat cushions
    L = (s1 - s0) / float(nseat)
    for i in range(nseat):
        a = s0 + i * L
        P.soft_slab(c, it, LP(T, RR(a + 4, a + L - 4, vb + 4, -6, 55, 5)), zd, zs, cush, 48, 3)
    if chaise is not None:
        c0, c1, Lc = chaise
        P.soft_slab(c, it, LP(T, RR(c0 + 12, c1 - 12, -40, Lc - 12, 40, 4)), zb, zd, body, 28, 2)
        P.soft_slab(c, it, LP(T, RR(c0 + 4, c1 - 4, -20, Lc - 8, 55, 5)), zd, zs, cush, 48, 3)
        # piped front roll on the chaise end
        hcyl(c, it, P3(c0 + 10, Lc - 40, zd - 20), P3(c1 - 10, Lc - 40, zd - 20), 30, body, 10)
    # scatter pillows + bolster
    Fn = (F[0], F[1], 0.0)
    spots = [(s0 + 300, pil[0], 6), (s1 - 300, pil[1], -6)] if (s1 - s0) > 1100 else [((s0 + s1) / 2.0, pil[0], 0)]
    for (uc, m, rot) in spots:
        o = T(uc, vb + 110)
        U = (R[0] * math.cos(math.radians(rot)), R[1] * math.cos(math.radians(rot)), math.sin(math.radians(rot)))
        P.cushion3d(c, it, (o[0], o[1], zs + 205), U, P._vec_tilt(Fn, 16), 430, 430, 150, m, 0.6)
    if armL or armR:
        ub = s0 + 95 if armL else s1 - 95
        A = P3(ub, vb + 40, zs + 90); Bp = P3(ub, vb + 520, zs + 90)
        hcyl(c, it, A, Bp, 88, pil[1], 14)
        hcyl(c, it, P3(ub, vb + 30, zs + 90), P3(ub, vb + 42, zs + 90), 30, 'brass', 10)
        hcyl(c, it, P3(ub, vb + 518, zs + 90), P3(ub, vb + 530, zs + 90), 30, 'brass', 10)


# ----------------------------------------------------------------- bed
def bed(c, it, x0, x1, y0, y1, head, npil, deco=True):
    RR, PRZ = c.RRECT, c.PRZ
    s = 1 if head == '+x' else -1
    hbx = x1 if s > 0 else x0
    hbt = 120                                     # headboard thickness
    fx = hbx - s * hbt                            # headboard front face
    def X(d): return hbx - s * d                  # distance from the wall -> x
    ya, yb = y0 - 38, y1 + 38                     # headboard incl. wings
    wt = 80                                       # wing thickness
    # --- central headboard panel: arched top (camel back), upholstered
    ym = (y0 + y1) / 2.0; hw = (yb - ya) / 2.0 - wt
    prof = [(-hw, 0)]
    for k in range(13):
        t = -1 + 2 * k / 12.0
        prof.append((t * hw, 1150 + 100 * math.cos(t * math.pi / 2) ** 1.5))
    prof.append((hw, 0))
    O = (hbx, ym, 0.0); U = (0.0, 1.0, 0.0); V = (0.0, 0.0, 1.0); Nf = (-s * 1.0, 0.0, 0.0)
    c.PR3(it, prof, O, U, V, Nf, 0, hbt, 'headb')
    # piped edge around the arch
    sweep(c, it, [(X(hbt - 8), ym + p[0], p[1]) for p in prof[1:-1]], 15, 'headb', 8)
    # diamond tufting on the front face
    gr = diamond_grid(-hw + 70, hw - 70, 640, 1110, 150, 78)
    tuft(c, it, (fx, ym, 0.0), U, V, Nf, gr, 'headb', 'gold', depth=18, bsz=8)
    # --- wings returning forward
    wd = hbt + 150
    wprof = [(0, 0), (wd, 0), (wd, 780)]
    for k in range(1, 9):
        a = (math.pi / 2) * k / 8.0
        wprof.append((wd - wd * 0.85 * (1 - math.cos(a)), 780 + 370 * math.sin(a)))
    wprof.append((0, 1150))
    for (yw0, yw1) in ((ya, ya + wt), (yb - wt, yb)):
        c.PR3(it, wprof, (hbx, yw0, 0.0), (-s * 1.0, 0.0, 0.0), (0.0, 0.0, 1.0), (0.0, 1.0, 0.0), 0, yw1 - yw0, 'headb')
        yc = (yw0 + yw1) / 2.0
        sweep(c, it, [(X(p[0]), yc, p[1]) for p in wprof[2:-1]], 22, 'headb', 8)
    # --- upholstered base with piped edge, turned feet
    bi = 46                                         # base inset at the sides (clears the wings)
    bx0, bx1 = (x0, fx) if s > 0 else (fx, x1)
    by0, by1 = y0 + bi, y1 - bi
    for (xx, yy) in ((bx0 + 70, by0 + 70), (bx0 + 70, by1 - 70), (bx1 - 70, by0 + 70), (bx1 - 70, by1 - 70)):
        turned_leg(c, it, xx, yy, 120, 'walnut', 'brass', 26, 10)
    base = RR(bx0, bx1, by0, by1, 40, 4)
    P.soft_slab(c, it, base, 120, 360, 'headb', 26, 2)
    PRZ(it, c.inset(base, -5), 344, 356, 'leather3')
    PRZ(it, c.inset(base, -5), 124, 134, 'leather3')
    # mattress
    P.soft_slab(c, it, RR(bx0 + 12, bx1 - 12, by0 + 10, by1 - 10, 60, 5), 356, 570, 'linen', 45, 3)
    L = bx1 - bx0
    if s > 0: dx0, dx1 = bx0 - 28, bx0 + L * 0.66
    else: dx0, dx1 = bx1 - L * 0.66, bx1 + 28
    P.soft_slab(c, it, RR(dx0, dx1, by0 - 28, by1 + 28, 40, 5), 550, 618, 'duvet', 30, 2)
    c.B(it, dx0, dx1, by0 - 30, by0 - 8, 290, 560, 'duvet'); c.B(it, dx0, dx1, by1 + 8, by1 + 30, 290, 560, 'duvet')
    fxx = dx0 if s > 0 else dx1 - 22
    c.B(it, fxx, fxx + 22, by0 - 28, by1 + 28, 290, 560, 'duvet')
    tb = (dx1 - 140, dx1) if s > 0 else (dx0, dx0 + 140)
    P.soft_slab(c, it, RR(tb[0], tb[1], by0 - 26, by1 + 26, 30, 4), 606, 646, 'linen2', 18, 2)
    if deco:
        tx = (bx0 + 110, bx0 + 470) if s > 0 else (bx1 - 470, bx1 - 110)
        PRZ(it, RR(tx[0], tx[1], by0 - 40, by1 + 40, 18, 3), 618, 640, 'throw')
        c.B(it, tx[0], tx[1], by0 - 46, by0 - 32, 360, 640, 'throw'); c.B(it, tx[0], tx[1], by1 + 32, by1 + 46, 360, 640, 'throw')
    # pillows: upright euro shams, sleeping pillows, bolster
    Fd = (-s * 1.0, 0.0, 0.0); Uy = (0.0, 1.0 if s > 0 else -1.0, 0.0)
    Wd = by1 - by0; pw = (Wd - 50) / float(npil)
    for i in range(npil):
        yc = by0 + 25 + pw * (i + 0.5)
        P.cushion3d(c, it, (X(hbt + 95), yc, 570 + 235), Uy, P._vec_tilt(Fd, 12), pw - 60, 470, 160, 'linen2', 0.5)
        P.cushion3d(c, it, (X(hbt + 250), yc, 570 + 150), Uy, P._vec_tilt(Fd, 38), pw - 80, 420, 150, 'linen2', 0.5)
    bxp = X(hbt + 450); r = 95
    hcyl(c, it, (bxp, by0 + 90, 570 + r - 10), (bxp, by1 - 90, 570 + r - 10), r, 'pil1', 14)
    for yy in (by0 + 80, by1 - 100):
        hcyl(c, it, (bxp, yy, 570 + r - 10), (bxp, yy + 20, 570 + r - 10), r * 0.45, 'gold', 10)
    if deco:
        P.cushion3d(c, it, (X(hbt + 360), ym, 570 + 250), Uy, P._vec_tilt(Fd, 20), 420, 420, 140, 'pil2', 0.6)


# ----------------------------------------------------------------- dining
def dining_table(c, it, x0, x1, y0, y1):
    RR, PRZ = c.RRECT, c.PRZ
    # ogee / stepped edge: full slab, then three receding steps below
    P.soft_slab(c, it, RR(x0, x1, y0, y1, 30, 4), 738, 758, 'marble', 6, 2, False)
    for (za, zb_, d) in ((729, 738, 7), (720, 729, 3), (710, 720, 16)):
        PRZ(it, RR(x0 + d, x1 - d, y0 + d, y1 - d, max(30 - d, 6), 4), za, zb_, 'marble')
    PRZ(it, RR(x0 + 150, x1 - 150, y0 + 150, y1 - 150, 20, 3), 690, 710, 'walnut')
    ym = (y0 + y1) / 2.0; Wt = y1 - y0
    rb = min(300, Wt * 0.3)
    xs = (x0 + (x1 - x0) * 0.25, x1 - (x1 - x0) * 0.25)
    for xp in xs:
        lathe(c, it, xp, ym, [(0, rb), (22, rb), (22, rb - 18), (50, rb - 22), (50, rb - 40), (70, rb - 55),
                              (110, rb - 120), (150, 120), (175, 100)], 'walnut', 24)
        lathe(c, it, xp, ym, [(175, 96), (200, 96)], 'brass', 24)
        lathe(c, it, xp, ym, [(200, 82), (240, 90), (300, 96), (380, 88), (480, 72), (560, 64)], 'walnut', 20)
        lathe(c, it, xp, ym, [(560, 80), (584, 80)], 'brass', 20)
        lathe(c, it, xp, ym, [(584, 70), (612, 90), (640, 135), (665, 160), (690, 160)], 'walnut', 20)
    # low stretcher between the plinths
    xa, xb = xs[0] + rb - 70, xs[1] - rb + 70
    hcyl(c, it, (xa, ym, 120), (xb, ym, 120), 30, 'walnut', 10)
    hcyl(c, it, ((xa + xb) / 2 - 30, ym, 120), ((xa + xb) / 2 + 30, ym, 120), 38, 'brass', 10)


def dchair(c, it, cx, cy, back):
    bd = {'-y': (0, -1), '+y': (0, 1), '-x': (-1, 0), '+x': (1, 0)}[back]
    face = {(0, -1): '+y', (0, 1): '-y', (-1, 0): '+x', (1, 0): '-x'}[bd]
    T = c.LF(face, cx, cy)
    f = (-bd[0], -bd[1]); r = (-f[1], f[0])
    def P3(u, v, z): p = T(u, v); return (p[0], p[1], z)
    # front legs: tapered, brass caps
    for su in (-1, 1):
        p = T(su * 190, 195)
        lathe(c, it, p[0], p[1], [(0, 13), (28, 13)], 'brass', 8)
        lathe(c, it, p[0], p[1], [(28, 14), (300, 19), (360, 24), (380, 24)], 'walnut', 8)
        sphere(c, it, p[0], p[1], 372, 26, 'walnut', 8, 3)
    # back legs raked backwards
    for su in (-1, 1):
        b = T(su * 185, -238); t = T(su * 182, -200)
        _loft(it, _ring(b[0], b[1], 0, 13, 8), _ring(t[0], t[1], 400, 20, 8), 'walnut')
    # seat: walnut rail + bowed fully upholstered seat
    pts = [(-222, -220), (222, -220)] + [(222 - 444 * k / 8.0, 200 + 30 * math.cos((-1 + 2 * k / 8.0) * math.pi / 2)) for k in range(9)]
    c.PRZ(it, c.LP(T, c.inset(pts, -4)), 385, 425, 'walnut')
    P.soft_slab(c, it, c.LP(T, pts), 425, 485, 'seat', 26, 2)
    # back: walnut frame band with an arched medallion top, upholstered panel set into it, leaning back ~8 deg
    Rc = 520.0                                   # plan curvature radius of the back
    oc = (0.0, -200.0 + Rc - 0.0)                # centre of curvature (in front)
    levels = [(500, 175), (600, 186), (700, 190), (780, 180), (840, 150), (880, 105), (900, 40)]
    def ring(z, half, r0, r1, n=6):
        sh = (z - 500) * math.tan(math.radians(8))
        sp = half / Rc
        out = []
        for k in range(n + 1):
            a = -sp + 2 * sp * k / n
            out.append(P3(oc[0] + r1 * math.sin(a), oc[1] - r1 * math.cos(a) - sh, z))
        for k in range(n + 1):
            a = sp - 2 * sp * k / n
            out.append(P3(oc[0] + r0 * math.sin(a), oc[1] - r0 * math.cos(a) - sh, z))
        return out
    fr = [ring(z, h + 18, Rc - 2, Rc + 34) for (z, h) in levels]
    for k in range(len(fr) - 1): _loft(it, fr[k], fr[k + 1], 'walnut')
    top = levels[-1][0]
    pl = [(z, h) for (z, h) in levels]
    pl[0] = (512, pl[0][1]); pl[-1] = (top - 12, pl[-1][1])
    pn = [ring(z, max(h - 6, 10), Rc - 22, Rc + 48) for (z, h) in pl]
    for k in range(len(pn) - 1): _loft(it, pn[k], pn[k + 1], 'seat')
    # posts joining the back legs to the frame
    for su in (-1, 1):
        a = T(su * 182, -200); bpt = T(su * 180, -204 - 0)
        _loft(it, _ring(a[0], a[1], 400, 18, 6), _ring(bpt[0], bpt[1], 520, 16, 6), 'walnut')


# ----------------------------------------------------------------- living
def coffee_table(c, it, cx, cy, a, b, ztop):
    A = min(a - 20, 520); Bb = min(b - 20, 360)
    top = c.RRECT(cx - A, cx + A, cy - Bb, cy + Bb, 150, 6)
    P.soft_slab(c, it, c.inset(top, 6), ztop - 32, ztop, 'marble', 6, 2, False)
    c.SLABH(it, top, c.inset(top, 10), ztop - 36, ztop + 16, 'brass', 'brass')          # gallery rim
    c.SLABH(it, c.inset(top, 30), c.inset(top, 48), ztop - 80, ztop - 36, 'brass', 'brass')  # apron
    # legs: slim turned brass with ball feet
    for (sx, sy) in ((-1, -1), (1, -1), (1, 1), (-1, 1)):
        x = cx + sx * (A - 95); y = cy + sy * (Bb - 80)
        lathe(c, it, x, y, [(0, 16), (8, 22), (26, 22), (34, 12), (300, 12), (310, 18), (320, 12), (ztop - 80, 14)], 'brass', 10)
    # lower shelf: smoked glass in a brass frame
    sh = c.RRECT(cx - A + 70, cx + A - 70, cy - Bb + 55, cy + Bb - 55, 110, 6)
    c.SLABH(it, sh, c.inset(sh, 14), 108, 128, 'brass', 'brass')
    c.PRZ(it, c.inset(sh, 12), 114, 122, 'smoke')


def floor_lamp(c, it, x, y):
    lathe(c, it, x, y, [(0, 175), (22, 175), (22, 150), (44, 150), (44, 118), (60, 100), (80, 40), (95, 26)], 'brass', 28)
    prof = [(95, 14)]
    for (zk, rk) in ((420, 13), (440, 26), (470, 13), (900, 12), (915, 22), (930, 12), (1260, 11), (1280, 24), (1300, 18), (1330, 10), (1360, 10)):
        prof.append((zk, rk))
    lathe(c, it, x, y, prof, 'brass', 12)
    # pleated empire shade
    n = 48
    def pring(z, r): return [(x + (r - (7 if k % 2 else 0)) * math.cos(2 * math.pi * k / n), y + (r - (7 if k % 2 else 0)) * math.sin(2 * math.pi * k / n), z) for k in range(n)]
    _loft(it, pring(1340, 222), pring(1665, 128), 'artbg')
    c.CYL(it, x, y, 223, 1336, 1346, 'brass', 32); c.CYL(it, x, y, 129, 1660, 1668, 'brass', 24)
    c.CYL(it, x, y, 205, 1343, 1347, 'lightw', 28)
    sphere(c, it, x, y, 1690, 14, 'brass', 10, 4)
    lathe(c, it, x, y, [(1600, 5), (1680, 5)], 'brass', 6)


def lounge_chair(c, it, cx, cy, face_deg, body='cush', base='walnut'):
    a = math.radians(face_deg); f = (math.cos(a), math.sin(a)); rgt = (-f[1], f[0])
    def L2(u, v): return (cx + rgt[0] * u + f[0] * v, cy + rgt[1] * u + f[1] * v)
    for k in range(4):
        ang = a + math.pi / 4 + k * math.pi / 2
        turned_leg(c, it, cx + 275 * math.cos(ang), cy + 275 * math.sin(ang), 175, base, 'brass', 22, 10)
    seat = [L2(355 * math.cos(2 * math.pi * k / 28), 345 * math.sin(2 * math.pi * k / 28)) for k in range(28)]
    P.soft_slab(c, it, seat, 170, 390, body, 30, 2)
    c.PRZ(it, c.inset(seat, -4), 176, 186, 'brass' if base != 'walnut' else base)
    cus = [L2(275 * math.cos(2 * math.pi * k / 24), 70 + 270 * math.sin(2 * math.pi * k / 24)) for k in range(24)]
    P.soft_slab(c, it, cus, 390, 480, body, 40, 3)
    # wraparound back: segments around the rear, height sweeping down to the arms, rolled top
    th0 = a + math.pi                      # direction of the back
    span = math.radians(128); N = 18
    ro, ri, rr = 380, 285, 52
    def hgt(t): return 610 + 200 * math.cos(t / span * math.pi / 2) ** 1.3
    tops = []
    for k in range(N + 1):
        t = -span + 2 * span * k / N
        tops.append((t, hgt(t)))
    outer = []; inner = []
    for (t, h) in tops:
        q = th0 + t
        outer.append((cx + ro * math.cos(q), cy + ro * math.sin(q)))
        inner.append((cx + ri * math.cos(q), cy + ri * math.sin(q)))
    c.PRZ(it, outer + inner[::-1], 300, 600, body)
    for k in range(N):
        (t0, h0), (t1, h1) = tops[k], tops[k + 1]
        if min(h0, h1) <= 601: continue
        lo = [outer[k] + (600,), outer[k + 1] + (600,), inner[k + 1] + (600,), inner[k] + (600,)]
        hi = [outer[k] + (h0,), outer[k + 1] + (h1,), inner[k + 1] + (h1,), inner[k] + (h0,)]
        _loft(it, lo, hi, body)
    rm = (ro + ri) / 2.0
    sweep(c, it, [(cx + rm * math.cos(th0 + t), cy + rm * math.sin(th0 + t), h) for (t, h) in tops], rr, body, 12)
    # scroll ends of the arms
    for t in (-span, span):
        q = th0 + t; rm = (ro + ri) / 2.0; h = hgt(t)
        sphere(c, it, cx + rm * math.cos(q), cy + rm * math.sin(q), h, rr, body, 10, 4)
    # button tufting on the inner back
    for (z, off) in ((560, 0.0), (650, 0.5), (740, 0.0)):
        for k in range(-3, 4):
            t = (k + off) * math.radians(19)
            if abs(t) > math.radians(70) or hgt(t) < z + 40: continue
            q = th0 + t
            A3 = (cx + (ri + 3) * math.cos(q), cy + (ri + 3) * math.sin(q), z)
            B3 = (cx + (ri - 6) * math.cos(q), cy + (ri - 6) * math.sin(q), z)
            hcyl(c, it, A3, B3, 9, 'gold', 6)


def nightstand(c, it, x0, x1, y0, y1):
    RR, PRZ = c.RRECT, c.PRZ
    xm = (x0 + x1) / 2.0
    # turned bun feet
    for (xx, yy) in ((x0 + 45, y0 + 45), (x0 + 45, y1 - 45), (x1 - 45, y0 + 45), (x1 - 45, y1 - 45)):
        lathe(c, it, xx, yy, [(0, 16), (10, 16)], 'brass', 10)
        lathe(c, it, xx, yy, [(10, 18), (30, 26), (50, 27), (68, 20), (80, 22), (90, 22)], 'walnut', 10)
    cb = (x0 + 18, x1 - 18, y0 + 14, y1 - 14)
    PRZ(it, RR(cb[0] - 6, cb[1] + 6, cb[2] - 6, cb[3] + 6, 6, 2), 90, 112, 'greige')          # plinth moulding
    PRZ(it, RR(cb[0], cb[1], cb[2], cb[3], 4, 2), 112, 488, 'greige')
    PRZ(it, RR(cb[0] - 6, cb[1] + 6, cb[2] - 6, cb[3] + 6, 6, 2), 488, 500, 'greige')         # top moulding
    P.soft_slab(c, it, RR(x0, x1, y0, y1, 12, 3), 500, 528, 'marble', 6, 2)
    # drawers on both x faces (the wall hides one)
    for (xf, sg) in ((cb[0], -1), (cb[1], 1)):
        for (z0, z1) in ((130, 300), (312, 474)):
            a0, a1 = sorted((xf, xf + sg * 8)); b0, b1 = sorted((xf + sg * 8, xf + sg * 14))
            c.B(it, a0, a1, cb[2] + 22, cb[3] - 22, z0, z1, 'greige')
            c.B(it, b0, b1, cb[2] + 50, cb[3] - 50, z0 + 26, z1 - 26, 'greige')
            # brass ring pull
            yc = (y0 + y1) / 2.0; zc = (z0 + z1) / 2.0 + 18
            xo = xf + sg * 14
            hcyl(c, it, (xo, yc, zc), (xo + sg * 6, yc, zc), 13, 'brass', 8)
            n = 8; rr = 22; zr = zc - rr + 4
            for k in range(n):
                q0 = 2 * math.pi * k / n; q1 = 2 * math.pi * (k + 1) / n
                hcyl(c, it, (xo + sg * 8, yc + rr * math.cos(q0), zr + rr * math.sin(q0)),
                     (xo + sg * 8, yc + rr * math.cos(q1), zr + rr * math.sin(q1)), 3.5, 'brass', 5)


# ----------------------------------------------------------------- lighting
def _lantern(c, it, x, y, zb, s=1.0):
    """Hexagonal brass-and-glass lantern with a glowing globe; bottom at zb, returns top z."""
    n = 6; R = 105 * s; H = 290 * s
    def hx(z, r): return [(x + r * math.cos(2 * math.pi * k / n), y + r * math.sin(2 * math.pi * k / n)) for k in range(n)]
    lathe(c, it, x, y, [(zb - 30 * s, 6 * s), (zb - 10 * s, 18 * s), (zb, 60 * s)], 'brass', 6)
    c.PRZ(it, hx(zb, R + 10 * s), zb, zb + 20 * s, 'brass')
    c.PRZ(it, hx(zb, R - 6 * s), zb + 20 * s, zb + 20 * s + H, 'glass')
    for (px, py) in hx(0, R):
        c.CYL(it, px, py, 5 * s, zb + 20 * s, zb + 20 * s + H, 'brass', 6)
    zt = zb + 20 * s + H
    c.PRZ(it, hx(zt, R + 12 * s), zt, zt + 18 * s, 'brass')
    _loft(it, [(p[0], p[1], zt + 18 * s) for p in hx(0, R + 6 * s)], [(p[0], p[1], zt + 95 * s) for p in hx(0, 26 * s)], 'brass')
    sphere(c, it, x, y, zt + 108 * s, 16 * s, 'brass', 8, 4)
    sphere(c, it, x, y, zb + 20 * s + H * 0.45, 62 * s, 'lightw', 14, 6)
    lathe(c, it, x, y, [(zb + 20 * s, 14 * s), (zb + 20 * s + H * 0.45 - 60 * s, 14 * s)], 'brass', 8)
    return zt + 124 * s


def dining_pendant(c, it, x0, x1, yc):
    L = x1 - x0
    xs = [x0 + L * 0.17, x0 + L * 0.5, x1 - L * 0.17]
    c.PRZ(it, c.RRECT(x0 + L * 0.1, x1 - L * 0.1, yc - 45, yc + 45, 40, 4), 2530, 2550, 'brass')   # canopy
    for x in xs:
        zt = _lantern(c, it, x, yc, 1665, 1.0)
        c.CYL(it, x, yc, 4, zt, 2530, 'brass', 6)
        c.CYL(it, x, yc, 10, zt, zt + 30, 'brass', 8)


def bedside_pendant(c, it, cx, cy):
    c.CYL(it, cx, cy, 55, 2535, 2550, 'brass', 20)
    c.CYL(it, cx, cy, 4, 1300, 2535, 'brass', 6)
    lathe(c, it, cx, cy, [(1255, 26), (1285, 30), (1300, 18)], 'brass', 16)
    # fluted glass bell
    n = 40
    def fl(z, r): return [(cx + (r - (6 if k % 2 else 0)) * math.cos(2 * math.pi * k / n), cy + (r - (6 if k % 2 else 0)) * math.sin(2 * math.pi * k / n), z) for k in range(n)]
    prof = [(1120, 118), (1150, 112), (1190, 96), (1225, 72), (1250, 44), (1258, 28)]
    for (z0, r0), (z1, r1) in zip(prof, prof[1:]): _loft(it, fl(z0, r0), fl(z1, r1), 'lightw')
    c.CYL(it, cx, cy, 120, 1114, 1122, 'brass', 32)
