import math
def _norm(poly):
    nx = ny = nz = 0.0
    n = len(poly)
    for i in range(n):
        a = poly[i]; b = poly[(i + 1) % n]
        nx += (a[1] - b[1]) * (a[2] + b[2]); ny += (a[2] - b[2]) * (a[0] + b[0]); nz += (a[0] - b[0]) * (a[1] + b[1])
    return nx, ny, nz
def _area2(p):
    s = 0.0
    for i in range(len(p)):
        a = p[i]; b = p[(i + 1) % len(p)]; s += a[0] * b[1] - b[0] * a[1]
    return s
def _clean(idx, P):
    out = []
    for i in idx:
        if out and P[out[-1]] == P[i]: continue
        out.append(i)
    while len(out) > 1 and P[out[0]] == P[out[-1]]: out.pop()
    return out
def _segint(p1, p2, p3, p4):
    def o(a, b, c): return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])
    d1 = o(p3, p4, p1); d2 = o(p3, p4, p2); d3 = o(p1, p2, p3); d4 = o(p1, p2, p4)
    return ((d1 > 0 and d2 < 0) or (d1 < 0 and d2 > 0)) and ((d3 > 0 and d4 < 0) or (d3 < 0 and d4 > 0))
def _bridge(ring, hole, P):
    # connect hole's rightmost vertex to a visible ring vertex
    hi = max(range(len(hole)), key=lambda k: (P[hole[k]][0], -P[hole[k]][1]))
    hp = P[hole[hi]]
    cands = sorted(range(len(ring)), key=lambda k: (P[ring[k]][0] - hp[0]) ** 2 + (P[ring[k]][1] - hp[1]) ** 2)
    edges = [(P[ring[k]], P[ring[(k + 1) % len(ring)]]) for k in range(len(ring))]
    edges += [(P[hole[k]], P[hole[(k + 1) % len(hole)]]) for k in range(len(hole))]
    best = cands[0]
    for k in cands:
        q = P[ring[k]]
        if q[0] < hp[0] - 1e-9 and k != cands[-1]:
            pass
        ok = True
        for (a, b) in edges:
            if a == q or b == q or a == hp or b == hp: continue
            if _segint(hp, q, a, b): ok = False; break
        if ok:
            best = k; break
    hr = hole[hi:] + hole[:hi]
    return ring[:best + 1] + hr + [hr[0], ring[best]] + ring[best + 1:]
def _pit(p, a, b, c):
    d1 = (p[0] - b[0]) * (a[1] - b[1]) - (a[0] - b[0]) * (p[1] - b[1])
    d2 = (p[0] - c[0]) * (b[1] - c[1]) - (b[0] - c[0]) * (p[1] - c[1])
    d3 = (p[0] - a[0]) * (c[1] - a[1]) - (c[0] - a[0]) * (p[1] - a[1])
    neg = d1 < 0 or d2 < 0 or d3 < 0; pos = d1 > 0 or d2 > 0 or d3 > 0
    return not (neg and pos)
def triangulate(outer, holes):
    if len(outer) < 3: return []
    n = _norm(outer); ax = max(range(3), key=lambda k: abs(n[k]))
    u, v = [(1, 2), (2, 0), (0, 1)][ax]
    pts3 = list(outer) + [p for h in holes for p in h]
    P = [(p[u], p[v]) for p in pts3]
    flip = n[ax] < 0
    if flip: P = [(x, -y) for (x, y) in P]
    ring = _clean(list(range(len(outer))), P)
    if _area2([P[i] for i in ring]) < 0: ring.reverse()
    off = len(outer)
    hs = []
    for h in holes:
        hi = _clean(list(range(off, off + len(h))), P); off += len(h)
        if len(hi) < 3: continue
        if _area2([P[i] for i in hi]) > 0: hi.reverse()
        hs.append(hi)
    hs.sort(key=lambda h: -max(P[i][0] for i in h))
    for h in hs: ring = _bridge(ring, h, P)
    tris = []
    V = ring[:]
    guard = 0
    while len(V) > 3 and guard < 100000:
        guard += 1
        found = False
        m = len(V)
        for i in range(m):
            ia, ib, ic = V[i - 1], V[i], V[(i + 1) % m]
            a, b, c = P[ia], P[ib], P[ic]
            cr = (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])
            if cr <= 1e-9:
                if abs(cr) <= 1e-9 and (a == b or b == c or True):
                    # collinear: drop middle vertex if it lies between
                    if abs(cr) <= 1e-9 and min(a[0], c[0]) - 1e-9 <= b[0] <= max(a[0], c[0]) + 1e-9 and min(a[1], c[1]) - 1e-9 <= b[1] <= max(a[1], c[1]) + 1e-9 and P[ia] != P[ic]:
                        V.pop(i); found = True; break
                continue
            ok = True
            for j in V:
                if j in (ia, ib, ic): continue
                q = P[j]
                if q == a or q == b or q == c: continue
                if _pit(q, a, b, c): ok = False; break
            if ok:
                tris.append((ia, ib, ic)); V.pop(i); found = True; break
        if not found:
            # fallback: fan the rest
            for i in range(1, len(V) - 1): tris.append((V[0], V[i], V[i + 1]))
            V = []
            break
    if len(V) == 3: tris.append((V[0], V[1], V[2]))
    out = []
    for (i, j, k) in tris:
        A, Bp, C = pts3[i], pts3[j], pts3[k]
        if flip: out.append((A, C, Bp))
        else: out.append((A, Bp, C))
    # ensure winding matches original normal
    res = []
    for (A, Bp, C) in out:
        cx = ((Bp[1] - A[1]) * (C[2] - A[2]) - (Bp[2] - A[2]) * (C[1] - A[1]), (Bp[2] - A[2]) * (C[0] - A[0]) - (Bp[0] - A[0]) * (C[2] - A[2]), (Bp[0] - A[0]) * (C[1] - A[1]) - (Bp[1] - A[1]) * (C[0] - A[0]))
        if cx[0] * n[0] + cx[1] * n[1] + cx[2] * n[2] < 0: res.append((A, C, Bp))
        else: res.append((A, Bp, C))
    return res
