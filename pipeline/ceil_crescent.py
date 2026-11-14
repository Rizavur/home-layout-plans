"""CRESCENT false-ceiling concept: in every room the recess is one calm crescent moon (the area between two circular arcs,
tips softly rounded) lying along the long axis of the feature zone, its fat belly centred on the ceiling fan and its horns
opening towards the room interior.  The cove layers (pocket, LED, light wash) are built from exact parallel crescents
(outer radius +d, inner radius -d, tip radius +d) so the light pocket follows the shape cleanly right into the tips."""
import math
import planlib as P

MARGIN = 45          # keep the crescent this far inside bbox(hole)
TIP_R = 85           # radius of the rounded horn tips (at the lip)
COMPANION = True     # thin brass arc on the flat ceiling echoing the inner arc


def _arc(cx, cy, r, a0, a1, step=None, nmin=3, nmax=64):
    """points on a circle from angle a0 to a1 (radians, either direction), endpoints included."""
    L = abs(a1 - a0) * r
    n = int(max(nmin, min(nmax, L / (step or 40.0))))
    return [(cx + r * math.cos(a0 + (a1 - a0) * i / n), cy + r * math.sin(a0 + (a1 - a0) * i / n)) for i in range(n + 1)]


class Moon:
    """Crescent in local (u, v) coordinates: u along the long axis, v across it, horns pointing to +v.
    Outer circle centre (0, a) radius Ro; inner circle centre (0, b) radius Ri, b > a."""

    def __init__(self, h, s_o, s_i, v_tip):
        self.Ro = (h * h + s_o * s_o) / (2 * s_o); self.a = v_tip - s_o + self.Ro
        self.Ri = (h * h + s_i * s_i) / (2 * s_i); self.b = v_tip - s_i + self.Ri

    def poly(self, d=0.0, rtip=TIP_R):
        """crescent grown by d (d < 0 shrinks); None if it degenerates."""
        Ro, Ri, a, b = self.Ro + d, self.Ri - d, self.a, self.b
        r = rtip + d if rtip + d > 30 else 30.0
        d1, d2 = Ro - r, Ri + r
        fv = (a + b) / 2 + (d1 * d1 - d2 * d2) / (2 * (b - a))
        q = d1 * d1 - (fv - a) ** 2
        if q <= 0 or Ri <= 0: return None
        fu = math.sqrt(q)
        tho = math.atan2(fv - a, fu)                 # outer tangent point (right horn), seen from the outer centre
        thi = math.atan2(fv - b, fu)                 # inner tangent point (right horn), seen from the inner centre
        # thickness at the belly must stay positive
        if (b - Ri) - (a - Ro) < 2 * r + 10: return None
        pts = []
        pts += _arc(0, a, Ro, tho, -math.pi - tho, step=30, nmin=24, nmax=96)[:-1]          # outer arc round the back, right -> left
        # left horn fillet: from outer tangent to inner tangent, round the outside of the tip
        # outer tangent direction from left fillet centre = away from outer centre
        ao = math.atan2(fv - a, -fu); ai = math.atan2(b - fv, fu)
        pts += self._fillet(-fu, fv, r, ao, ai, -1)[:-1]
        # inner arc (concave), left -> right through the inner apex
        ph = math.atan2(fv - b, fu)
        pts += _arc(0, b, Ri, math.pi - ph, 2 * math.pi + ph, step=30, nmin=24, nmax=96)[:-1]
        ao = math.atan2(fv - a, fu); ai = math.atan2(b - fv, -fu)
        pts += self._fillet(fu, fv, r, ai, ao, +1)[:-1]
        return pts

    @staticmethod
    def _fillet(fx, fy, r, a0, a1, side):
        """fillet arc from a0 to a1 choosing the sweep whose midpoint lies further out along u (side=+1 right, -1 left)."""
        d = (a1 - a0) % (2 * math.pi)
        cands = (d, d - 2 * math.pi)
        best = max(cands, key=lambda s: side * math.cos(a0 + s / 2))
        return _arc(fx, fy, r, a0, a0 + best, step=12, nmin=6, nmax=16)


def _fan(c, hole):
    """centre of a ceiling fan already hung inside bbox(hole) (bedrooms, dining, plan B living);
    otherwise the centre of bbox(hole), where the spec says the fan / pendant hangs."""
    x0, x1, y0, y1 = P.bbox(hole); best = None
    for it in getattr(c, 'ITEMS', []):
        if 'Fan' not in it.get('name', '') or not it.get('prisms'): continue
        try:
            pts = it['prisms'][0][1]; fx0, fx1, fy0, fy1 = P.bbox(pts)
        except Exception:
            continue
        fx, fy = (fx0 + fx1) / 2, (fy0 + fy1) / 2
        if x0 < fx < x1 and y0 < fy < y1:
            dd = math.hypot(fx - (x0 + x1) / 2, fy - (y0 + y1) / 2)
            if best is None or dd < best[0]: best = (dd, fx, fy)
    return (best[1], best[2]) if best else ((x0 + x1) / 2, (y0 + y1) / 2)


def _sdist(pt, poly):
    """signed distance from pt to the polygon outline (+ inside)."""
    d = min(_segd(pt, poly[i - 1], poly[i]) for i in range(len(poly)))
    return d if P.pip(pt, poly) else -d


def _segd(p, a, b):
    dx, dy = b[0] - a[0], b[1] - a[1]; L2 = dx * dx + dy * dy or 1.0
    t = max(0.0, min(1.0, ((p[0] - a[0]) * dx + (p[1] - a[1]) * dy) / L2))
    return math.hypot(p[0] - a[0] - t * dx, p[1] - a[1] - t * dy)


def _design(c, hole, outer):
    x0, x1, y0, y1 = P.bbox(hole); cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    ox0, ox1, oy0, oy1 = P.bbox(outer); ocx, ocy = (ox0 + ox1) / 2, (oy0 + oy1) / 2
    xlong = (x1 - x0) >= (y1 - y0) - 1
    L, W = ((x1 - x0), (y1 - y0)) if xlong else ((y1 - y0), (x1 - x0))
    # default: horns open towards the room interior (centre of the dropped ceiling); if centred, towards +y / +x
    off = (ocy - cy) if xlong else (ocx - cx)
    sg0 = -1 if off < -100 else 1
    asp = L / W
    k = 0.40 if asp > 1.35 else 0.46                 # belly thickness / horn-to-horn length (fatter in square-ish zones)
    qi = 0.42 if asp > 1.35 else 0.30                # inner sagitta / belly thickness
    U, V = L / 2 - MARGIN, W / 2 - MARGIN
    t = min(2 * V / (1 + qi), k * (L - 2 * MARGIN))
    h = t / k / 2
    m = Moon(h, t * (1 + qi), t * qi, t * (1 + qi) / 2)   # v-extent centred on 0
    base = m.poly(0)
    us = [p[0] for p in base]; vs = [p[1] for p in base]
    s0 = min(1.0, U / max(-min(us), max(us)), V / max(-min(vs), max(vs)))
    umin, umax, vmin, vmax = min(us) * s0, max(us) * s0, min(vs) * s0, max(vs) * s0
    fx, fy = _fan(c, hole)
    best = None
    for sg in (sg0, -sg0):
        fu, fv = ((fx - cx), sg * (fy - cy)) if xlong else ((fy - cy), sg * (fx - cx))
        for sc in (1.0, 0.94, 0.88, 0.82, 0.76):
            lo_u, hi_u = -U - umin * sc, U - umax * sc
            lo_v, hi_v = -V - vmin * sc, V - vmax * sc
            for i in range(9):
                du = lo_u + (hi_u - lo_u) * i / 8
                for j in range(9):
                    dv = lo_v + (hi_v - lo_v) * j / 8
                    poly = [(du + u * s0 * sc, dv + v * s0 * sc) for u, v in base]
                    e = _sdist((fu, fv), poly)
                    belly = e > 0
                    tt = t * s0 * sc
                    # fan comfortably inside the belly, or clearly in the hollow
                    if belly: bad = max(0.0, 0.40 * tt - e)
                    else:
                        inside_inner = math.hypot(fu - du, fv - (dv + m.b * s0 * sc)) < m.Ri * s0 * sc
                        bad = max(0.0, 260 + e) if inside_inner else max(0.0, 320 + e) + 150
                    score = -4 * bad - 0.6 * math.hypot(du, dv) - (250 if sg != sg0 else 0) - 900 * (1 - sc) - (0 if belly else 40)
                    if best is None or score > best[0]: best = (score, sg, sc, du, dv)
    _, sg, sc, du, dv = best
    s = s0 * sc

    def to_world(pts):
        if xlong: return [(cx + du + u * s, cy + sg * (dv + v * s)) for u, v in pts]
        return [(cx + sg * (dv + v * s), cy + du + u * s) for u, v in pts]
    return m, to_world, s, (fx, fy)


def build(c, raw, it, outer, hole, z0, z1):
    m, W, s, fan = _design(c, hole, outer)
    C = lambda d: (lambda p: W(p) if p else None)(m.poly(d / s))
    hole2 = C(0)
    it.setdefault('_holes', []).append(hole2)
    zl = z0 + 50
    raw(it, outer, hole2, z0, zl, 'fceil', 'fceil')                     # 50 mm white lip
    raw(it, outer, C(80), zl, z1, 'fceil', 'cove')                       # glowing back face of the light pocket
    raw(it, C(60), C(25), zl, zl + 4, 'led', 'led')                      # LED strip on the lip
    g1 = C(-140)
    if g1:
        raw(it, hole2, g1, z1 - 3, z1 - 1, 'glow1', 'glow1')             # strong wash along the edge
        g2 = C(-360) or C(-250)
        if g2: raw(it, g1, g2, z1 - 3, z1 - 1, 'glow2', 'glow2')
    raw(it, outer, P._offset(outer, -15), z0 - 2, z0, 'reveal', 'reveal')   # shadow gap at the walls
    # the brass echo only where the fan hangs in the belly - in the hollow it would crowd the fan
    if COMPANION and P.pip(fan, hole2):
        _companion(c, it, m, W, s, z0)


def _companion(c, it, m, W, s, z0):
    """thin brass arc on the flat ceiling inside the hollow, concentric with the inner arc."""
    gap = 170 / s; w = 14 / s
    R = m.Ri - gap
    if R < 200: return
    span = 0.42                                       # half-angle of the brass arc around the inner apex (rad)
    a0, a1 = -math.pi / 2 - span, -math.pi / 2 + span
    o = _arc(0, m.b, R + w / 2, a0, a1, step=30, nmin=24)
    i = _arc(0, m.b, R - w / 2, a1, a0, step=30, nmin=24)
    poly = W(o + i)
    c.PRZ(it, poly, z0 - 4, z0, 'gold')
