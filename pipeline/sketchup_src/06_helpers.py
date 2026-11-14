# build_model call 6 of 10
LB = session_state['L']
ARC = LB['ARC']; B = LB['B']; CYL = LB['CYL']; CYLY = LB['CYLY']; PR3 = LB['PR3']; PRZ = LB['PRZ']; RRECT = LB['RRECT']; V = LB['V']
cabinet = LB['cabinet']; run_box = LB['run_box']; run_void = LB['run_void']; wall_front = LB['wall_front']

def hbar(it, face, c, front, z, L, m='gold'):
    run_box(it, face, c - L / 2.0, c + L / 2.0, front, -20, 2, z, z + 14, m)

def krun(it, face, front, depth, z0, z1, kick, segs, hpos, base='mortar_k', m='white', carcass=True):
    a0 = segs[0][0]; a1 = segs[-1][1]
    zc = z0 + kick
    if carcass:
        run_box(it, face, a0, a1, front, 20, depth, zc, z1, m)
    if kick > 0:
        run_box(it, face, a0, a1, front, 40, depth, z0, zc, base)
    for (s0, s1, kind) in segs:
        if kind == 'skip':
            continue
        if kind == 'drawers' or kind == 'drawers4':
            nd = 4 if kind == 'drawers4' else 3
            hs = [0.18, 0.22, 0.28, 0.32] if nd == 4 else [0.26, 0.34, 0.40]
            zb = zc
            for k in range(nd):
                zt = zb + (z1 - zc) * hs[k]
                run_box(it, face, s0 + 1.5, s1 - 1.5, front, 2, 20, zb + (3 if k > 0 else 0), zt, m)
                hbar(it, face, (s0 + s1) / 2.0, front, zt - 50, min(s1 - s0 - 160, 380))
                zb = zt
            continue
        n = 2 if kind == 'door2' else 1
        w = (s1 - s0 - 3 * (n - 1)) / float(n)
        for i in range(n):
            u0 = s0 + i * (w + 3) + (1.5 if i == 0 else 0); u1 = u0 + w - (1.5 if i == n - 1 else 0)
            run_box(it, face, u0, u1, front, 2, 20, zc, z1, m)
            if kind == 'flat':
                continue
            L = min(u1 - u0 - 120, 380)
            zh = (z1 - 55) if hpos == 'top' else (zc + 40)
            hbar(it, face, (u0 + u1) / 2.0, front, zh, L)

def RR(x0, x1, y0, y1, r, c=(1, 1, 1, 1), n=6):
    pts = []
    spec = [((x1 - r, y0 + r), 270, (x1, y0)), ((x1 - r, y1 - r), 0, (x1, y1)), ((x0 + r, y1 - r), 90, (x0, y1)), ((x0 + r, y0 + r), 180, (x0, y0))]
    for k in range(4):
        cc, a, corner = spec[k]
        if c[k]:
            pts += ARC(cc[0], cc[1], r, a, a + 90, n)[:-1]
        else:
            pts.append(corner)
    return pts

def LF(face, cx, cy):
    f = {'+x': (1.0, 0.0), '-x': (-1.0, 0.0), '+y': (0.0, 1.0), '-y': (0.0, -1.0)}[face]
    R = (-f[1], f[0])
    def T(u, v):
        return (cx + u * R[0] + v * f[0], cy + u * R[1] + v * f[1])
    return T

def LP(T, pts):
    return [T(u, v) for (u, v) in pts]

def ELL(cu, cv, a, b, n=20):
    return [(cu + a * math.cos(2 * math.pi * k / n), cv + b * math.sin(2 * math.pi * k / n)) for k in range(n)]

def inset(pts, d):
    n = len(pts); cx = sum([p[0] for p in pts]) / n; cy = sum([p[1] for p in pts]) / n
    out = []
    for (x, y) in pts:
        L = math.sqrt((x - cx) ** 2 + (y - cy) ** 2) or 1.0
        out.append((x - (x - cx) / L * d, y - (y - cy) / L * d))
    return out

def puff(it, poly, z0, z1, m, crown=12, d=14):
    PRZ(it, poly, z0, z1 - crown, m)
    PRZ(it, inset(poly, d), z1 - crown, z1, m)

def sofa2(it, face, cx, cy, W, D, nseat, armL=True, armR=True, chaise=None, body='sofa', cush='sofa2', pil=('art2', 'rug1')):
    T = LF(face, cx, cy)
    u0 = -W / 2.0; u1 = W / 2.0; arm = 170; back = 220
    for (u, v) in ((u0 + 60, -60), (u1 - 60, -60), (u0 + 60, -D + 60), (u1 - 60, -D + 60)):
        p = T(u, v); CYL(it, p[0], p[1], 22, 0, 110, 'walnut', 12)
    puff(it, LP(T, RRECT(u0, u1, -D, 0, 50, 5)), 110, 380, body, 10, 8)
    puff(it, LP(T, RRECT(u0, u1, -D, -D + back, 70, 5)), 380, 720, body, 14, 10)
    s0 = u0; s1 = u1
    if armL:
        puff(it, LP(T, RRECT(u0, u0 + arm, -D, 0, 75, 5)), 380, 640, body, 18, 14); s0 = u0 + arm
    if armR:
        puff(it, LP(T, RRECT(u1 - arm, u1, -D, 0, 75, 5)), 380, 640, body, 18, 14); s1 = u1 - arm
    L = (s1 - s0) / float(nseat)
    for i in range(nseat):
        a = s0 + i * L
        puff(it, LP(T, RRECT(a + 6, a + L - 6, -D + back + 10, -15, 70, 5)), 380, 520, cush, 18, 14)
        puff(it, LP(T, RRECT(a + 10, a + L - 10, -D + back - 30, -D + back + 170, 90, 5)), 520, 860, cush, 26, 18)
    if chaise is not None:
        c0, c1, Lc = chaise
        puff(it, LP(T, RRECT(c0, c1, -30, Lc, 50, 5)), 110, 380, body, 10, 8)
        puff(it, LP(T, RRECT(c0 + 6, c1 - 6, -20, Lc - 15, 70, 5)), 380, 520, cush, 18, 14)
        for (u, v) in ((c0 + 60, Lc - 60), (c1 - 60, Lc - 60)):
            p = T(u, v); CYL(it, p[0], p[1], 22, 0, 110, 'walnut', 12)
        PRZ(it, LP(T, RRECT(c0 + 60, c1 - 60, Lc - 520, Lc - 120, 30, 3)), 520, 545, 'throw')
    pa = s0 + 40; pb = s1 - 40
    puff(it, LP(T, RRECT(pa, pa + 430, -D + back + 150, -D + back + 290, 60, 4)), 520, 920, pil[0], 30, 20)
    puff(it, LP(T, RRECT(pb - 430, pb, -D + back + 150, -D + back + 290, 60, 4)), 520, 920, pil[0], 30, 20)
    puff(it, LP(T, RRECT(pa + 300, pa + 680, -D + back + 260, -D + back + 380, 60, 4)), 520, 860, pil[1], 28, 18)

def chair2(it, face, cx, cy):
    T = LF(face, cx, cy)
    for k in range(5):
        a = 2 * math.pi * k / 5 + 0.3
        ca = math.cos(a); sa = math.sin(a); pu = -sa; pv = ca
        quad = [(pu * 28, pv * 28), (ca * 310 + pu * 16, sa * 310 + pv * 16), (ca * 310 - pu * 16, sa * 310 - pv * 16), (-pu * 28, -pv * 28)]
        PRZ(it, LP(T, quad), 70, 95, 'metal')
        p = T(ca * 300, sa * 300)
        CYL(it, p[0], p[1], 26, 8, 60, 'metal', 14); CYL(it, p[0], p[1], 10, 60, 72, 'chrome', 8)
    p = T(0, 0)
    CYL(it, p[0], p[1], 48, 70, 130, 'metal', 18); CYL(it, p[0], p[1], 24, 130, 420, 'chrome', 14)
    PRZ(it, LP(T, RRECT(-120, 120, -120, 110, 30, 3)), 420, 450, 'metal')
    PRZ(it, LP(T, RRECT(-245, 245, -225, 245, 90, 5)), 450, 470, 'metal')
    puff(it, LP(T, RRECT(-240, 240, -220, 240, 100, 6)), 470, 540, 'mesh', 16, 16)
    def arcband(r0, r1, a0, a1):
        out = []
        for k in range(15):
            a = math.radians(a0 + (a1 - a0) * k / 14.0)
            out.append((r1 * math.cos(a), 150 + r1 * math.sin(a)))
        for k in range(15):
            a = math.radians(a1 - (a1 - a0) * k / 14.0)
            out.append((r0 * math.cos(a), 150 + r0 * math.sin(a)))
        return out
    PRZ(it, LP(T, arcband(395, 425, 232, 308)), 640, 1170, 'mesh')
    PRZ(it, LP(T, arcband(392, 430, 232, 308)), 1170, 1190, 'metal')
    PRZ(it, LP(T, arcband(392, 430, 232, 308)), 620, 640, 'metal')
    PRZ(it, LP(T, arcband(380, 398, 250, 290)), 720, 860, 'mesh2')
    PRZ(it, LP(T, RRECT(-28, 28, -300, -255, 12, 3)), 450, 640, 'metal')
    for s in (-1, 1):
        PRZ(it, LP(T, RRECT(s * 255 - 15, s * 255 + 15, -70, -20, 10, 3)), 470, 680, 'metal')
        PRZ(it, LP(T, RRECT(s * 255 - 38, s * 255 + 38, -170, 120, 30, 4)), 680, 705, 'mesh')

def station(it, face, cx, cy, D):
    T = LF(face, cx, cy)
    f = {'+x': (1.0, 0.0, 0.0), '-x': (-1.0, 0.0, 0.0), '+y': (0.0, 1.0, 0.0), '-y': (0.0, -1.0, 0.0)}[face]
    Rv = (-f[1], f[0], 0.0)
    PRZ(it, LP(T, RRECT(-120, 120, D - 230, D - 60, 50, 5)), 750, 760, 'metal')
    PRZ(it, LP(T, RRECT(-22, 22, D - 140, D - 110, 10, 3)), 760, 1060, 'metal')
    o = T(0, D - 105)
    PR3(it, RRECT(-312, 312, 900, 1265, 14, 4), (o[0], o[1], 0), Rv, (0.0, 0.0, 1.0), f, 0, 14, 'screen')
    PR3(it, RRECT(-140, 140, 960, 1180, 40, 4), (o[0], o[1], 0), Rv, (0.0, 0.0, 1.0), f, 14, 38, 'metal')
    puff(it, LP(T, RRECT(-215, 215, 150, 285, 14, 3)), 750, 772, 'kbd', 4, 6)
    PRZ(it, LP(T, RRECT(260, 430, 120, 330, 18, 3)), 750, 752, 'charcoal')
    m0 = ELL(345, 220, 32, 56, 20); m1 = ELL(345, 216, 28, 48, 20); m2 = ELL(345, 210, 20, 34, 16)
    PRZ(it, LP(T, m0), 752, 766, 'mouse'); PRZ(it, LP(T, m1), 766, 778, 'mouse'); PRZ(it, LP(T, m2), 778, 785, 'mouse')
    p = T(-420, 250); CYL(it, p[0], p[1], 40, 750, 850, 'ceramic', 16)

def desk_long(it, face, cx, cy, W, D, legs):
    T = LF(face, cx, cy)
    puff(it, LP(T, RRECT(-W / 2.0, W / 2.0, 0, D, 22, 4)), 722, 750, 'oak', 4, 3)
    for u in legs:
        PRZ(it, LP(T, RRECT(u - 32, u + 32, D / 2.0 - 45, D / 2.0 + 45, 14, 3)), 40, 700, 'metal')
        PRZ(it, LP(T, RRECT(u - 30, u + 30, 40, D - 40, 26, 4)), 0, 40, 'metal')
        PRZ(it, LP(T, RRECT(u - 24, u + 24, 70, D - 70, 12, 3)), 700, 722, 'metal')
    PRZ(it, LP(T, RRECT(legs[0], legs[-1], D / 2.0 - 25, D / 2.0 + 25, 10, 3)), 660, 700, 'metal')

def vanity_ledge(it, face, a0, a1, wall, depth, ma0, ma1, mz0, mz1, decor, nd):
    fr = wall_front(face, wall, depth)
    cabinet(it, face, a0, a1, fr, depth, 350, 730, 2, 'white', 0, None, 'bar')
    run_box(it, face, a0, a1, fr, -10, depth, 730, 850, 'ceramic')
    am = (a0 + a1) / 2.0
    run_void(it, face, am - 210, am + 210, fr, 70, 380, 760, 850, 'ceramic')
    run_box(it, face, am - 20, am + 20, fr, depth - 90, depth - 50, 850, 1080, 'chrome')
    run_box(it, face, am - 15, am + 15, fr, depth - 220, depth - 50, 1050, 1080, 'chrome')
    run_box(it, face, a0 + 30, a1 - 30, fr, 30, 50, 344, 350, 'led')
    fr2 = wall_front(face, wall, 150)
    zb = mz0 + 160
    run_box(it, face, ma0, ma1, fr2, 6, 150, zb, mz1, 'white')
    L = (ma1 - ma0 - 3 * (nd - 1)) / float(nd)
    for i in range(nd):
        u0 = ma0 + i * (L + 3)
        run_box(it, face, u0, u0 + L, fr2, 0, 6, zb + 3, mz1 - 3, 'mirror')
    run_box(it, face, ma0, ma1, fr2, 0, 150, mz0, mz0 + 20, 'marble')
    run_box(it, face, ma0, ma0 + 18, fr2, 6, 150, mz0 + 20, zb, 'white')
    run_box(it, face, ma1 - 18, ma1, fr2, 6, 150, mz0 + 20, zb, 'white')
    run_box(it, face, ma0 + 30, ma1 - 30, fr2, 15, 30, zb - 6, zb, 'led')
    run_box(it, face, ma0 + 30, ma1 - 30, fr2, 15, 30, mz0 - 6, mz0, 'led')
    z = mz0 + 20
    for (a, kind) in decor:
        if face == '+x': x, y = fr2 - 80, a
        elif face == '-x': x, y = fr2 + 80, a
        elif face == '+y': x, y = a, fr2 - 80
        else: x, y = a, fr2 + 80
        if kind == 'diffuser':
            CYL(it, x, y, 35, z, z + 95, 'smoke', 16); CYL(it, x, y, 14, z + 95, z + 105, 'metal', 10)
            for (dx, dy) in ((-6, 0), (5, 5), (4, -6)):
                B(it, x + dx - 2, x + dx + 2, y + dy - 2, y + dy + 2, z + 105, zb - 12, 'oak')
        if kind == 'candle':
            CYL(it, x, y, 40, z, z + 70, 'ceramic', 16); CYL(it, x, y, 34, z + 70, z + 72, 'cove', 12)
        if kind == 'plant':
            CYL(it, x, y, 45, z, z + 60, 'charcoal', 16); CYL(it, x, y, 55, z + 60, z + 115, 'art1', 12)

def dchair_lux(it, cx, cy, back):
    bd = {'-y': (0, -1), '+y': (0, 1), '-x': (-1, 0), '+x': (1, 0)}[back]
    for sx in (-1, 1):
        for sy in (-1, 1):
            CYL(it, cx + sx * 185, cy + sy * 175, 15, 0, 430, 'gold', 10)
    PRZ(it, RRECT(cx - 230, cx + 230, cy - 220, cy + 220, 70, 4), 430, 445, 'gold')
    PRZ(it, RRECT(cx - 235, cx + 235, cy - 225, cy + 225, 90, 5), 445, 505, 'seat')
    th = math.degrees(math.atan2(bd[1], bd[0]))
    oc = (cx - bd[0] * 20, cy - bd[1] * 20)
    outer = ARC(oc[0], oc[1], 255, th - 80, th + 80, 14)
    inner = ARC(oc[0], oc[1], 200, th + 80, th - 80, 14)
    PRZ(it, outer + inner, 505, 840, 'seat')
    o2 = ARC(oc[0], oc[1], 258, th - 80, th + 80, 14); i2 = ARC(oc[0], oc[1], 197, th + 80, th - 80, 14)
    PRZ(it, o2 + i2, 840, 852, 'gold')

def curtain_full(it, x0, x1, y0, stack_l, stack_r, pleats, ztop):
    B(it, x0, x1, y0 + 40, y0 + 70, ztop - 20, ztop, 'steel')
    for (s0, s1) in ((x0 + 10, x0 + 10 + stack_l), (x1 - 10 - stack_r, x1 - 10)):
        w = (s1 - s0) / float(pleats)
        for i in range(pleats):
            off = 0 if i % 2 == 0 else 45
            B(it, s0 + i * w, s0 + (i + 1) * w, y0 + 20 + off, y0 + 80 + off, 20, ztop - 25, 'curtain')

def wave(cx, cy, a, b, ph, amp, n=96):
    pts = []
    for k in range(n):
        t = 2 * math.pi * k / n
        c = math.cos(t); s = math.sin(t)
        x = (abs(c) ** 0.6) * (1 if c >= 0 else -1); yv = (abs(s) ** 0.6) * (1 if s >= 0 else -1)
        w = 1 + amp * (math.sin(2 * t + ph) * 0.35 + math.sin(4 * t + 1.7 * ph) * 0.45 + math.sin(6 * t + ph * 0.5) * 0.2)
        pts.append((round(cx + a * x * w, 1), round(cy + b * yv * w, 1)))
    return pts

session_state['LQ'] = {'hbar': hbar, 'krun': krun, 'RR': RR, 'LF': LF, 'LP': LP, 'ELL': ELL, 'inset': inset, 'puff': puff, 'sofa2': sofa2, 'chair2': chair2,
                       'station': station, 'desk_long': desk_long, 'vanity_ledge': vanity_ledge, 'dchair_lux': dchair_lux, 'curtain_full': curtain_full, 'wave': wave}
result = {'ok': 1}
