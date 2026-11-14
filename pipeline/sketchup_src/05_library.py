# build_model call 5 of 10
F = session_state['fns']
ITEMS = []
def item(name, layer):
    it = {'name': name, 'layer': layer, 'boxes': {}, 'voids': {}, 'prisms': [], 'slabs': []}
    ITEMS.append(it)
    return it
def B(it, x0, x1, y0, y1, z0, z1, m):
    if x1 < x0: x0, x1 = x1, x0
    if y1 < y0: y0, y1 = y1, y0
    if z1 < z0: z0, z1 = z1, z0
    if m not in it['boxes']: it['boxes'][m] = []
    it['boxes'][m].append([round(x0, 1), round(x1, 1), round(y0, 1), round(y1, 1), round(z0, 1), round(z1, 1)])
def V(it, x0, x1, y0, y1, z0, z1, m):
    if m not in it['voids']: it['voids'][m] = []
    it['voids'][m].append([x0, x1, y0, y1, z0, z1])
def CYL(it, cx, cy, r, z0, z1, m, n=32):
    pts = [(cx + r * math.cos(2 * math.pi * k / n), cy + r * math.sin(2 * math.pi * k / n)) for k in range(n)]
    it['prisms'].append((2, pts, z0, z1, m))
def PRZ(it, pts, z0, z1, m):
    it['prisms'].append((2, pts, z0, z1, m))
def CYLY(it, cx, cz, r, y0, y1, m, n=32):
    pts = [(cx + r * math.cos(2 * math.pi * k / n), cz + r * math.sin(2 * math.pi * k / n)) for k in range(n)]
    it['prisms'].append((1, pts, y0, y1, m))
def ARC(cx, cy, r, a0, a1, n=12):
    return [(cx + r * math.cos(math.radians(a0 + (a1 - a0) * k / float(n))), cy + r * math.sin(math.radians(a0 + (a1 - a0) * k / float(n)))) for k in range(n + 1)]
def RRECT(x0, x1, y0, y1, r, n=8):
    return ARC(x1 - r, y0 + r, r, 270, 360, n)[:-1] + ARC(x1 - r, y1 - r, r, 0, 90, n)[:-1] + ARC(x0 + r, y1 - r, r, 90, 180, n)[:-1] + ARC(x0 + r, y0 + r, r, 180, 270, n)[:-1]
def SLABH(it, outer, hole, z0, z1, m, mh):
    it['slabs'].append((outer, hole, z0, z1, m, mh))
def PR3(it, pts, O, U, Vv, W, t0, t1, m):
    lo = [(O[0] + u * U[0] + v * Vv[0] + t0 * W[0], O[1] + u * U[1] + v * Vv[1] + t0 * W[1], O[2] + u * U[2] + v * Vv[2] + t0 * W[2]) for (u, v) in pts]
    hi = [(O[0] + u * U[0] + v * Vv[0] + t1 * W[0], O[1] + u * U[1] + v * Vv[1] + t1 * W[1], O[2] + u * U[2] + v * Vv[2] + t1 * W[2]) for (u, v) in pts]
    it['prisms'].append((3, (lo, hi), 0, 0, m))
def downlights(it, pts, z):
    for (x, y) in pts: CYL(it, x, y, 45, z - 4, z, 'lightw', 12)
def run_box(it, face, a0, a1, front, d0, d1, z0, z1, m):
    if face == '+x': B(it, front - d1, front - d0, a0, a1, z0, z1, m)
    if face == '-x': B(it, front + d0, front + d1, a0, a1, z0, z1, m)
    if face == '+y': B(it, a0, a1, front - d1, front - d0, z0, z1, m)
    if face == '-y': B(it, a0, a1, front + d0, front + d1, z0, z1, m)
def cabinet(it, face, a0, a1, front, depth, z0, z1, ndoors, m='white', kick=100, tiers=None, handle=None, hm='steel', gap=3, base=None):
    zc = z0 + kick
    run_box(it, face, a0, a1, front, 20, depth, zc, z1, m)
    if kick > 0 and base is None: run_box(it, face, a0 + 20, a1 - 20, front, 60, depth, z0, zc, m)
    if kick > 0 and base is not None: run_box(it, face, a0, a1, front, 40, depth, z0, zc, base)
    zs = [zc] + (tiers or []) + [z1]
    L = (a1 - a0 - gap * (ndoors - 1)) / float(ndoors)
    for t in range(len(zs) - 1):
        zb = zs[t] + (gap if t > 0 else 0); zt = zs[t + 1]
        for i in range(ndoors):
            u0 = a0 + i * (L + gap); u1 = u0 + L
            run_box(it, face, u0, u1, front, 2, 20, zb, zt, m)
            if handle == 'bar':
                hu = (u1 - 40) if i % 2 == 0 else (u0 + 25)
                if t == len(zs) - 2 and len(zs) > 2 and zt - zb < 600:
                    hz0 = zb + 40; hz1 = zb + 60
                    run_box(it, face, u0 + L * 0.3, u1 - L * 0.3, front, -25, 2, hz0, hz1, hm)
                else:
                    hz = min(zb + 1100, (zb + zt) / 2.0) if zt - zb > 1200 else ((zb + 60) if zb > 1200 else (zt - 260))
                    run_box(it, face, hu, hu + 15, front, -25, 2, hz, hz + 200, hm)
def bed(it, x0, x1, y0, y1, head_x_side, pillow_n):
    hb = 80
    if head_x_side > 0: hx0, hx1, bx0, bx1 = x1 - hb, x1, x0, x1 - hb
    else: hx0, hx1, bx0, bx1 = x0, x0 + hb, x0 + hb, x1
    B(it, hx0, hx1, y0, y1, 0, 1100, 'headb')
    B(it, bx0 + 40, bx1 - 40, y0 + 40, y1 - 40, 0, 80, 'metal')
    B(it, bx0, bx1, y0, y1, 80, 330, 'headb')
    B(it, bx0 + 10, bx1 - 10, y0 + 15, y1 - 15, 330, 560, 'linen')
    L = bx1 - bx0
    if head_x_side > 0: B(it, bx0 - 15, bx0 + L * 0.72, y0 - 15, y1 + 15, 380, 585, 'duvet')
    else: B(it, bx1 - L * 0.72, bx1 + 15, y0 - 15, y1 + 15, 380, 585, 'duvet')
    W = (y1 - y0 - 60 - 40 * (pillow_n - 1)) / float(pillow_n)
    for i in range(pillow_n):
        yy = y0 + 30 + i * (W + 40)
        if head_x_side > 0: B(it, bx1 - 480, bx1 - 30, yy, yy + W, 560, 690, 'linen')
        else: B(it, bx0 + 30, bx0 + 480, yy, yy + W, 560, 690, 'linen')
def fan(it, cx, cy, mz, ceil=2650, rb=650):
    CYL(it, cx, cy, 70, ceil - 50, ceil, 'appl', 24)
    CYL(it, cx, cy, 13, mz + 140, ceil - 50, 'appl', 10)
    CYL(it, cx, cy, 120, mz, mz + 140, 'appl', 28)
    CYL(it, cx, cy, 140, mz - 50, mz, 'lightw', 28)
    for k in range(3):
        a = 2 * math.pi * k / 3 + 0.5
        ca = math.cos(a); sa = math.sin(a); px = -sa; py = ca
        pts = [(cx + ca * 110 + px * 55, cy + sa * 110 + py * 55), (cx + ca * rb + px * 70, cy + sa * rb + py * 70),
               (cx + ca * (rb + 10), cy + sa * (rb + 10)), (cx + ca * rb - px * 70, cy + sa * rb - py * 70), (cx + ca * 110 - px * 55, cy + sa * 110 - py * 55)]
        PRZ(it, pts, mz + 50, mz + 62, 'walnut')
def aircon(it, axis, wall, s, a0, a1):
    if axis == 'y':
        B(it, a0, a1, wall, wall + s * 215, 2300, 2600, 'appl')
        B(it, a0 + 40, a1 - 40, wall + s * 205, wall + s * 220, 2315, 2345, 'metal')
        B(it, a0 + 20, a1 - 20, wall + s * 215, wall + s * 218, 2400, 2560, 'appl')
    else:
        B(it, wall, wall + s * 215, a0, a1, 2300, 2600, 'appl')
        B(it, wall + s * 205, wall + s * 220, a0 + 40, a1 - 40, 2315, 2345, 'metal')
        B(it, wall + s * 215, wall + s * 218, a0 + 20, a1 - 20, 2400, 2560, 'appl')
def curtain(it, x0, x1, y0, stack_l, stack_r, pleats=6):
    B(it, x0, x1, y0 + 40, y0 + 70, 2225, 2245, 'steel')
    for (s0, s1) in ((x0 + 10, x0 + 10 + stack_l), (x1 - 10 - stack_r, x1 - 10)):
        w = (s1 - s0) / float(pleats)
        for i in range(pleats):
            off = 0 if i % 2 == 0 else 45
            B(it, s0 + i * w, s0 + (i + 1) * w, y0 + 20 + off, y0 + 80 + off, 20, 2220, 'curtain')
def lever(it, axis, plane, side, u, z, toward, m='gold'):
    if axis == 'y':
        B(it, u - 25, u + 25, plane, plane + side * 10, z - 25, z + 25, m)
        B(it, u - 10, u + 10, plane + side * 10, plane + side * 55, z - 10, z + 10, m)
        B(it, u, u + toward * 130, plane + side * 40, plane + side * 60, z - 10, z + 10, m)
    else:
        B(it, plane, plane + side * 10, u - 25, u + 25, z - 25, z + 25, m)
        B(it, plane + side * 10, plane + side * 55, u - 10, u + 10, z - 10, z + 10, m)
        B(it, plane + side * 40, plane + side * 60, u, u + toward * 130, z - 10, z + 10, m)
def wc(it, face, wall, cy):
    s = 1 if face == '+x' else -1
    B(it, wall, wall + s * 180, cy - 180, cy + 180, 380, 800, 'ceramic')
    B(it, wall + s * 120, wall + s * 520, cy - 120, cy + 120, 0, 300, 'ceramic')
    B(it, wall + s * 170, wall + s * 650, cy - 185, cy + 185, 300, 390, 'ceramic')
    B(it, wall + s * 180, wall + s * 640, cy - 180, cy + 180, 390, 415, 'ceramic2')
    B(it, wall + s * 60, wall + s * 120, cy - 25, cy + 25, 800, 815, 'chrome')
def run_void(it, face, a0, a1, front, d0, d1, z0, z1, m):
    tmp = {'boxes': {}}
    run_box(tmp, face, a0, a1, front, d0, d1, z0, z1, m)
    for b in tmp['boxes'][m]: V(it, b[0], b[1], b[2], b[3], b[4], b[5], m)
def wall_front(face, wall, depth):
    if face == '+x': return wall + depth
    if face == '-x': return wall - depth
    if face == '+y': return wall + depth
    return wall - depth
def shower_set(it, axis, wall, s, u):
    if axis == 'x':
        B(it, wall, wall + s * 60, u - 90, u + 90, 1000, 1130, 'chrome')
        B(it, wall + s * 30, wall + s * 50, u - 10, u + 10, 1130, 2050, 'chrome')
        B(it, wall + s * 30, wall + s * 330, u - 12, u + 12, 2050, 2075, 'chrome')
        CYL(it, wall + s * 330, u, 125, 2040, 2055, 'chrome', 24)
    else:
        B(it, u - 90, u + 90, wall, wall + s * 60, 1000, 1130, 'chrome')
        B(it, u - 10, u + 10, wall + s * 30, wall + s * 50, 1130, 2050, 'chrome')
        B(it, u - 12, u + 12, wall + s * 30, wall + s * 330, 2050, 2075, 'chrome')
        CYL(it, u, wall + s * 330, 125, 2040, 2055, 'chrome', 24)
def nightstand(it, x0, x1, y0, y1):
    B(it, x0, x1, y0, y1, 150, 520, 'greige'); B(it, x0, x1, y0, y1, 520, 532, 'gold')
    B(it, x0 + 3, x1 - 3, y0 + 3, y1 - 3, 335, 337, 'charcoal')
def build_fixtures():
    it = item('Door_Handles', 'Doors')
    for s, pl in ((-1, 3830), (1, 3870)):
        lever(it, 'y', pl, s, 7620, 1000, 1)
        lever(it, 'y', pl, s, 9580, 1000, -1)
    for s, pl in ((-1, 10180), (1, 10220)):
        lever(it, 'x', pl, s, 4780, 1000, -1)
    for s, pl in ((-1, 8270), (1, 8320)):
        lever(it, 'y', pl, s, 2480, 1000, 1)
    for s, pl in ((-1, 1705), (1, 1745)):
        lever(it, 'x', pl, s, 6780, 1000, 1)
    for s, pl in ((-1, 5030), (1, 5070)):
        B(it, 9740, 9780, pl, pl + s * 45, 980, 1020, 'steel')
        B(it, 11450, 11490, pl, pl + s * 45, 980, 1020, 'steel')
    for s, pl in ((-1, 7868), (1, 7912)):
        B(it, pl + s * 0, pl + s * 50, 7760, 7775, 900, 915, 'steel'); B(it, pl, pl + s * 50, 7760, 7775, 1285, 1300, 'steel')
        B(it, pl + s * 50, pl + s * 70, 7755, 7780, 880, 1320, 'steel')
    it = item('Yard_Casement_Windows', 'Windows')
    F0, F1 = 9320, 9390
    B(it, F0, F1, 7100, 7150, 1000, 2400, 'frame'); B(it, F0, F1, 9150, 9200, 1000, 2400, 'frame')
    B(it, F0, F1, 7150, 9150, 1000, 1050, 'frame'); B(it, F0, F1, 7150, 9150, 2350, 2400, 'frame')
    p = (2000 - 150) / 4.0
    edges = []
    y = 7150
    for i in range(4):
        edges.append((y, y + p)); y += p
        if i < 3:
            B(it, F0, F1, y, y + 50, 1050, 2350, 'frame'); y += 50
    for i, (a, b) in enumerate(edges):
        if i in (0, 3):
            B(it, F0 + 5, F1 - 5, a + 2, a + 42, 1052, 2348, 'frame'); B(it, F0 + 5, F1 - 5, b - 42, b - 2, 1052, 2348, 'frame')
            B(it, F0 + 5, F1 - 5, a + 42, b - 42, 1052, 1092, 'frame'); B(it, F0 + 5, F1 - 5, a + 42, b - 42, 2308, 2348, 'frame')
            B(it, 9351, 9359, a + 42, b - 42, 1092, 2308, 'glass')
            hy = (b - 70) if i == 0 else (a + 50)
            B(it, F0 - 60, F0, hy, hy + 20, 1650, 1780, 'steel')
        else:
            B(it, 9351, 9359, a, b, 1050, 2350, 'glass')
MATS = {'white': ('Joinery_White_Matt', 238, 236, 231, 255), 'oak': ('Light_Oak', 190, 155, 110, 255), 'fabric': ('Sofa_Fabric_Grey', 140, 140, 138, 255),
        'fabric2': ('Cushion_Fabric_Light_Grey', 168, 167, 163, 255), 'metal': ('Metal_Black', 35, 35, 37, 255), 'steel': ('Brushed_Steel', 165, 167, 170, 255),
        'linen': ('Bed_Linen_White', 244, 243, 239, 255), 'duvet': ('Duvet_Warm_Grey', 200, 196, 188, 255), 'headb': ('Headboard_Fabric_Beige', 196, 184, 166, 255),
        'ceramic': ('Ceramic_White', 250, 250, 250, 255), 'ceramic2': ('Ceramic_Seat_White', 242, 242, 242, 255), 'mirror': ('Mirror', 205, 218, 224, 255),
        'quartz': ('Quartz_Top_White', 230, 229, 225, 255), 'glassblk': ('Hob_Black_Glass', 25, 25, 28, 255), 'appl': ('Appliance_White', 236, 236, 234, 255),
        'silver': ('Fridge_Silver', 188, 190, 193, 255), 'screen': ('Screen_Black', 18, 18, 20, 255), 'curtain': ('Curtain_Light_Grey', 214, 212, 206, 255),
        'seat': ('Dining_Seat_Velvet_Taupe', 142, 126, 112, 255), 'chrome': ('Chrome', 200, 202, 206, 255), 'frame': ('Window_Frame_Aluminium_Black', 58, 60, 63, 255),
        'glass': ('Glass', 175, 205, 218, 85), 'lightw': ('Light_Diffuser_Opal', 252, 252, 248, 255),
        'mortar_k': ('Mortar_Base_Kitchen_Tile', 214, 211, 205, 255), 'mortar_y': ('Mortar_Base_Yard_Tile', 206, 205, 201, 255),
        'art1': ('Art_Canvas_Sage', 152, 163, 140, 255), 'art2': ('Art_Canvas_Sand', 205, 185, 150, 255), 'art3': ('Art_Canvas_Terracotta', 176, 120, 95, 255),
        'fceil': ('False_Ceiling_White', 248, 248, 246, 255), 'cove': ('Cove_Light_Warm', 255, 240, 210, 255),
        'rug1': ('Rug_Border_Taupe', 150, 136, 118, 255), 'rug2': ('Rug_Field_Oatmeal', 204, 194, 176, 255),
        'gold': ('Champagne_Gold_Brushed', 196, 168, 116, 255), 'marble': ('Marble_Calacatta_White', 236, 233, 228, 255), 'charcoal': ('Lux_Charcoal_Matt', 58, 56, 55, 255),
        'charcoal2': ('Lux_Charcoal_Fluted', 74, 71, 69, 255), 'greige': ('Lux_Greige', 150, 142, 134, 255), 'smoke': ('Smoked_Glass', 88, 90, 94, 150),
        'fglass': ('Fluted_Glass_Frosted', 214, 222, 224, 165), 'artbg': ('Art_Canvas_Ivory', 234, 228, 218, 255)}
MATS['brass'] = MATS['gold']
MATS['wallp'] = ('Wall_Paint_Partition', 243, 243, 241, 255)
MATS['sintered'] = ('Sintered_Stone_Grey_Veined', 200, 197, 192, 255)
MATS['leather'] = ('Leather_Caramel', 176, 105, 60, 255)
MATS['cush'] = ('Boucle_Cushion_Cream', 240, 236, 226, 255)
MATS['led'] = ('LED_Strip_Warm_3000K', 255, 214, 140, 255)
MATS['walnut'] = ('Walnut_Veneer_Dark', 96, 66, 48, 255)
MATS['walnut2'] = ('Walnut_Fluted_Dark', 82, 56, 41, 255)
MATS['traver'] = ('Travertine_Honed_Warm', 214, 200, 178, 255)
MATS['sofa'] = ('Sofa_Boucle_Greige', 198, 190, 178, 255)
MATS['sofa2'] = ('Sofa_Cushion_Oat', 216, 208, 194, 255)
MATS['throw'] = ('Throw_Knit_Taupe', 150, 132, 112, 255)
MATS['mesh'] = ('Chair_Mesh_Charcoal', 62, 63, 66, 255)
MATS['mesh2'] = ('Chair_Lumbar_Grey', 110, 111, 114, 255)
MATS['kbd'] = ('Keyboard_Space_Grey', 92, 94, 98, 255)
MATS['mouse'] = ('Mouse_Soft_White', 232, 232, 230, 255)
MATS['linen2'] = ('Pillow_White', 250, 250, 248, 255)
def su_b(b): return [b[0], b[1], -b[3], -b[2], b[4], b[5]]
def newell(l):
    nx = 0.0; ny = 0.0; nz = 0.0
    for i in range(len(l)):
        a = l[i]; b = l[(i + 1) % len(l)]
        nx += (a[1] - b[1]) * (a[2] + b[2]); ny += (a[2] - b[2]) * (a[0] + b[0]); nz += (a[0] - b[0]) * (a[1] + b[1])
    return (nx, ny, nz)
def orient(l, d):
    n = newell(l)
    if n[0] * d[0] + n[1] * d[1] + n[2] * d[2] < 0: l = list(reversed(l))
    return l
def prism_faces(ax, pts, a0, a1, m):
    if ax == 3:
        lo = [(round(p[0], 2), round(-p[1], 2), round(p[2], 2)) for p in pts[0]]; hi = [(round(p[0], 2), round(-p[1], 2), round(p[2], 2)) for p in pts[1]]
        allp = lo + hi; n_ = float(len(allp))
        c = (sum([p[0] for p in allp]) / n_, sum([p[1] for p in allp]) / n_, sum([p[2] for p in allp]) / n_)
        def ctr(l): return (sum([p[0] for p in l]) / len(l) - c[0], sum([p[1] for p in l]) / len(l) - c[1], sum([p[2] for p in l]) / len(l) - c[2])
        out = [(m, 0, 0, orient(hi, ctr(hi)), []), (m, 0, 0, orient(lo, ctr(lo)), [])]
        k = len(lo)
        for i in range(k):
            q = [lo[i], lo[(i + 1) % k], hi[(i + 1) % k], hi[i]]
            out.append((m, 0, 0, orient(q, ctr(q)), []))
        return out
    def P(u, v, w):
        if ax == 2: return (round(u, 2), round(-v, 2), round(w, 2))
        return (round(u, 2), round(-w, 2), round(v, 2))
    axd = (0, 0, 1) if ax == 2 else (0, -1, 0)
    out = []
    lo = [P(u, v, a0) for (u, v) in pts]; hi = [P(u, v, a1) for (u, v) in pts]
    out.append((m, 0, 0, orient(hi, axd), [])); out.append((m, 0, 0, orient(lo, (-axd[0], -axd[1], -axd[2])), []))
    cu = sum([p[0] for p in pts]) / len(pts); cv = sum([p[1] for p in pts]) / len(pts)
    k = len(pts)
    for i in range(k):
        (u0, v0) = pts[i]; (u1, v1) = pts[(i + 1) % k]
        q = [P(u0, v0, a0), P(u1, v1, a0), P(u1, v1, a1), P(u0, v0, a1)]
        c = P(cu, cv, (a0 + a1) / 2.0); mm_ = P((u0 + u1) / 2.0, (v0 + v1) / 2.0, (a0 + a1) / 2.0)
        out.append((m, 0, 0, orient(q, (mm_[0] - c[0], mm_[1] - c[1], mm_[2] - c[2])), []))
    return out
def slab_faces(outer, hole, z0, z1, m, mh):
    def P(u, v, w): return (round(u, 2), round(-v, 2), round(w, 2))
    out = []
    top = orient([P(u, v, z1) for (u, v) in outer], (0, 0, 1)); toph = orient([P(u, v, z1) for (u, v) in hole], (0, 0, -1))
    bot = orient([P(u, v, z0) for (u, v) in outer], (0, 0, -1)); both = orient([P(u, v, z0) for (u, v) in hole], (0, 0, 1))
    out.append((m, 0, 0, top, [toph])); out.append((m, 0, 0, bot, [both]))
    for (pts, mat, sgn) in ((outer, m, 1), (hole, mh, -1)):
        k = len(pts)
        ar = 0.0
        for i in range(k):
            ar += pts[i][0] * pts[(i + 1) % k][1] - pts[(i + 1) % k][0] * pts[i][1]
        sg = sgn * (1 if ar > 0 else -1)
        for i in range(k):
            (u0, v0) = pts[i]; (u1, v1) = pts[(i + 1) % k]
            q = [P(u0, v0, z0), P(u1, v1, z0), P(u1, v1, z1), P(u0, v0, z1)]
            nx = sg * (v1 - v0); ny = -sg * (u1 - u0)
            out.append((mat, 0, 0, orient(q, (nx, -ny, 0)), []))
    return out
def item_faces(it, vx_mesh, vx_clusters):
    res = {}
    for m, bs in it['boxes'].items():
        sb = [su_b(b) for b in bs]
        vs = [su_b(v) for v in it['voids'].get(m, [])]
        faces = []
        if vs:
            faces = vx_mesh(sb, vs, lambda sc, ec, a, s: m, [])
        else:
            for cl in vx_clusters(sb): faces += vx_mesh(cl, [], lambda sc, ec, a, s: m, [])
        res[m] = faces
    pf = {}
    for (ax, pts, a0, a1, m) in it['prisms']:
        if m not in pf: pf[m] = []
        pf[m] += prism_faces(ax, pts, a0, a1, m)
    for (o, h, z0, z1, m, mh) in it.get('slabs', []):
        if m not in pf: pf[m] = []
        pf[m] += slab_faces(o, h, z0, z1, m, mh)
    return res, pf
session_state['L'] = {'ARC': ARC, 'B': B, 'CYL': CYL, 'CYLY': CYLY, 'PR3': PR3, 'PRZ': PRZ, 'RRECT': RRECT, 'SLABH': SLABH, 'V': V, 'aircon': aircon, 'bed': bed, 'build_fixtures': build_fixtures, 'cabinet': cabinet, 'curtain': curtain, 'downlights': downlights, 'fan': fan, 'item': item, 'item_faces': item_faces, 'lever': lever, 'nightstand': nightstand, 'run_box': run_box, 'run_void': run_void, 'shower_set': shower_set, 'wall_front': wall_front, 'wc': wc, 'ITEMS': ITEMS, 'MATS': MATS}
result = {'ok': 1}
