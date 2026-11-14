# build_model call 1 of 10 (clean=true)
def vx_mesh(boxes, voids, matfn, extra):
    xs = {}
    ys = {}
    zs = {}
    for b in list(boxes) + list(voids):
        xs[b[0]] = 1
        xs[b[1]] = 1
        ys[b[2]] = 1
        ys[b[3]] = 1
        zs[b[4]] = 1
        zs[b[5]] = 1
    for e in extra or []:
        if e[0] == 0:
            xs[e[1]] = 1
        if e[0] == 1:
            ys[e[1]] = 1
        if e[0] == 2:
            zs[e[1]] = 1
    C = [sorted(xs.keys()), sorted(ys.keys()), sorted(zs.keys())]
    n = [len(C[0]) - 1, len(C[1]) - 1, len(C[2]) - 1]
    ix = [dict(((v, i) for i, v in enumerate(C[a]))) for a in range(3)]
    occ = [0] * (n[0] * n[1] * n[2])

    def fillb(b, val):
        i0 = ix[0][b[0]]
        i1 = ix[0][b[1]]
        j0 = ix[1][b[2]]
        j1 = ix[1][b[3]]
        k0 = ix[2][b[4]]
        k1 = ix[2][b[5]]
        for i in range(i0, i1):
            for j in range(j0, j1):
                base = (i * n[1] + j) * n[2]
                for k in range(k0, k1):
                    occ[base + k] = val
    for b in boxes:
        fillb(b, 1)
    for b in voids:
        fillb(b, 0)
    mid = [[(C[a][i] + C[a][i + 1]) * 0.5 for i in range(n[a])] for a in range(3)]
    groups = {}
    for i in range(n[0]):
        for j in range(n[1]):
            for k in range(n[2]):
                if not occ[(i * n[1] + j) * n[2] + k]:
                    continue
                cell = (i, j, k)
                sc = (mid[0][i], mid[1][j], mid[2][k])
                for a in range(3):
                    for s in (-1, 1):
                        q = [i, j, k]
                        q[a] += s
                        if 0 <= q[a] < n[a]:
                            if occ[(q[0] * n[1] + q[1]) * n[2] + q[2]]:
                                continue
                            ec = [mid[0][q[0]], mid[1][q[1]], mid[2][q[2]]]
                        else:
                            ec = None
                        mat = matfn(sc, ec, a, s)
                        p = cell[a] + (1 if s > 0 else 0)
                        u = cell[(a + 1) % 3]
                        v = cell[(a + 2) % 3]
                        key = (a, p, s, mat)
                        if key not in groups:
                            groups[key] = []
                        groups[key].append((u, v))
    faces = []
    for key in sorted(groups.keys(), key=lambda t: (t[0], t[1], t[2], str(t[3]))):
        a, p, s, mat = key
        for outer, holes in vx_trace(groups[key]):

            def to3(l):
                pts = []
                for u, v in l:
                    c = [0, 0, 0]
                    c[a] = C[a][p]
                    c[(a + 1) % 3] = C[(a + 1) % 3][u]
                    c[(a + 2) % 3] = C[(a + 2) % 3][v]
                    pts.append((c[0], c[1], c[2]))
                if s < 0:
                    pts.reverse()
                return pts
            faces.append((mat, a, s, to3(outer), [to3(h) for h in holes]))
    return faces

def vx_trace(cells):
    E = {}
    for u, v in cells:
        for e in (((u, v), (u + 1, v)), ((u + 1, v), (u + 1, v + 1)), ((u + 1, v + 1), (u, v + 1)), ((u, v + 1), (u, v))):
            r = (e[1], e[0])
            if r in E:
                del E[r]
            else:
                E[e] = 1
    out = {}
    for p0, p1 in E.keys():
        if p0 not in out:
            out[p0] = []
        out[p0].append(p1)
    loops = []
    while len(out) > 0:
        start = sorted(out.keys())[0]
        loop = [start]
        cur = start
        prev_d = None
        while True:
            cands = out[cur]
            if len(cands) == 1 or prev_d is None:
                nxt = cands[0]
            else:
                dx, dy = prev_d
                pref = [(-dy, dx), (dx, dy), (dy, -dx)]
                nxt = None
                for d in pref:
                    for c in cands:
                        if (c[0] - cur[0], c[1] - cur[1]) == d and nxt is None:
                            nxt = c
                if nxt is None:
                    nxt = cands[0]
            cands.remove(nxt)
            if len(cands) == 0:
                del out[cur]
            prev_d = (nxt[0] - cur[0], nxt[1] - cur[1])
            cur = nxt
            if cur == start:
                break
            loop.append(cur)
        loops.append(loop)

    def area(l):
        s = 0
        for i in range(len(l)):
            a = l[i]
            b = l[(i + 1) % len(l)]
            s += a[0] * b[1] - b[0] * a[1]
        return s * 0.5

    def inside(pt, l):
        c = False
        x, y = pt
        for i in range(len(l)):
            a = l[i]
            b = l[(i + 1) % len(l)]
            if (a[1] > y) != (b[1] > y):
                xi = a[0] + (y - a[1]) * (b[0] - a[0]) / (b[1] - a[1])
                if xi > x:
                    c = not c
        return c
    outers = []
    holes = []
    for l in loops:
        A = area(l)
        if A > 0:
            outers.append([l, A, []])
        else:
            holes.append(l)
    for h in holes:
        a = h[0]
        b = h[1]
        dx = b[0] - a[0]
        dy = b[1] - a[1]
        pt = ((a[0] + b[0]) * 0.5 - dy * 0.25, (a[1] + b[1]) * 0.5 + dx * 0.25)
        best = None
        for o in outers:
            if inside(pt, o[0]) and (best is None or o[1] < best[1]):
                best = o
        if best is not None:
            best[2].append(h)
    return [(o[0], o[2]) for o in outers]

def su_fill(name, faces, mats, parent=None, layer=None, scale=None):
    g = GeometryInput()
    vid = {}
    verts = []

    def vi(p):
        if p not in vid:
            vid[p] = len(verts)
            verts.append(SUPoint3D(mm(p[0]), mm(p[1]), mm(p[2])))
        return vid[p]
    idx = []
    for mat, a, s, outer, holes in faces:
        idx.append((mat, [vi(p) for p in outer], [[vi(p) for p in h] for h in holes]))
    g.set_vertices(verts)
    for mat, o, hs in idx:
        L = LoopInput()
        for i in o:
            L.add_vertex_index(i)
        fi, g = g.add_face(L)
        for h in hs:
            H = LoopInput()
            for i in h:
                H.add_vertex_index(i)
            g = g.face_add_inner_loop(fi, H)
        m = mats[mat]
        g = g.face_set_front_material(fi, [], m)
        g = g.face_set_back_material(fi, [], m)
    grp = Group()
    (parent if parent is not None else model.get_entities()).add_group(grp)
    grp.get_entities().fill(g, weld_vertices=True)
    grp.set_name(name)
    if layer is not None:
        grp.set_layer(layer)
    return grp

def su_edges(name, segs, parent=None, layer=None, mat=None):
    g = GeometryInput()
    vid = {}
    verts = []
    es = []

    def vi(p):
        if p not in vid:
            vid[p] = len(verts)
            verts.append(SUPoint3D(mm(p[0]), mm(p[1]), mm(p[2])))
        return vid[p]
    for p, q in segs:
        es.append((vi(p), vi(q)))
    g.set_vertices(verts)
    for i, j in es:
        ei, g = g.add_edge(i, j)
        if mat is not None:
            g = g.edge_set_material(ei, mat)
    grp = Group()
    (parent if parent is not None else model.get_entities()).add_group(grp)
    grp.get_entities().fill(g, weld_vertices=True)
    grp.set_name(name)
    if layer is not None:
        grp.set_layer(layer)
    return grp

def vx_clusters(boxes):
    par = list(range(len(boxes)))

    def f(i):
        while par[i] != i:
            par[i] = par[par[i]]
            i = par[i]
        return i
    for i in range(len(boxes)):
        for j in range(i + 1, len(boxes)):
            a = boxes[i]
            b = boxes[j]
            if a[0] <= b[1] and b[0] <= a[1] and (a[2] <= b[3]) and (b[2] <= a[3]) and (a[4] <= b[5]) and (b[4] <= a[5]):
                ri = f(i)
                rj = f(j)
                if ri != rj:
                    par[ri] = rj
    out = {}
    for i in range(len(boxes)):
        r = f(i)
        if r not in out:
            out[r] = []
        out[r].append(boxes[i])
    return list(out.values())

def vx_build(name, boxes, mats, matname, parent, layer):
    faces = []
    for cl in vx_clusters(boxes):
        faces += vx_mesh(cl, [], lambda sc, ec, a, s: matname, [])
    return su_fill(name, faces, mats, parent, layer)
D = {'ceil': [[0, 1850, -8900, -1020, 2650, 2800], [1850, 9410, -8600, -1020, 2650, 2800], [3740, 9410, -9550, -8600, 2650, 2800], [5550, 14600, -1020, 0, 2650, 2800], [9410, 13410, -6950, -1020, 2650, 2800], [13410, 14600, -5250, -1020, 2650, 2800]]}
MC = {'paint': ('Wall_Paint_White', 243, 243, 241, 255), 'wt_toilet': ('Wall_Toilet_Tile_300x600', 205, 206, 207, 255), 'wt_kitchen': ('Wall_Kitchen_Tile_300x600', 223, 224, 223, 255), 'f_cream': ('Floor_Homogeneous_Cream_600x600', 226, 221, 210, 255), 'f_kitchen': ('Floor_Kitchen_Tile_600x600', 214, 211, 205, 255), 'f_yard': ('Floor_Yard_Shelter_Tile_300x300', 206, 205, 201, 255), 'f_toilet': ('Floor_Toilet_Tile_300x600', 150, 152, 154, 255), 'slab': ('Concrete_Slab', 185, 185, 182, 255), 'ceil': ('Ceiling_Paint_White', 248, 248, 246, 255)}
mats = {}
for k, v in MC.items():
    mats[k] = get_or_create_material(v[0], v[1], v[2], v[3], v[4])
LN = ['Walls_and_Beams', 'Floor', 'Ceiling', 'Windows', 'Doors', 'Fixtures', 'Toilet_Pipe_Boxups', 'Beams_Highlight', 'Structural_Highlight', 'Tile_Joints', 'Furniture', 'Kitchen', 'Sanitary', 'Curtains', 'Aircon', 'Lighting', 'False_Ceiling', 'Decor', 'Partitions', 'LED_Strips', 'Kitchen_Door_Closed', 'Kitchen_Door_Open']
lays = []
for n in LN:
    L = Layer()
    L.set_name(n)
    lays.append(L)
model.add_layers(lays)
LAY = dict(((L.get_name(), L) for L in model.get_layers()))
su_fill('Ceiling_Slab', vx_mesh(D['ceil'], [], lambda sc, ec, a, s: 'ceil', []), mats, None, LAY['Ceiling'])
session_state['fns'] = {'vx_mesh': vx_mesh, 'vx_trace': vx_trace, 'su_fill': su_fill, 'su_edges': su_edges, 'vx_clusters': vx_clusters, 'vx_build': vx_build}
session_state['mats_def'] = MC
result = {'ok': 1, 'layers': len(model.get_layers())}
