"""SWEEPING ARC false ceiling.

The recess is a "D" / segment shape fitted in the (slightly shrunk) bounding box of the default hole:
three straight sides of the box with softly rounded corners, and ONE long side replaced by a single
shallow circular arc, so each room reads as having one graceful curved cove line crossing the ceiling.

Rule: the arc sits on a LONG side of the box - the larger-y side when the box is wider than deep, the
larger-x side when it is deeper than wide.  It bows OUTWARD (convex D): the arc's apex touches the box
edge and its ends are pulled back by the sagitta, so the fan at the box centre always sits in the open
body of the recess, well clear of the lip.  A slim brass line traces the arc on the flat ceiling just
outside the lip when there is room for it.

All the offset rings of the cove (lip, LED pocket, light washes) are built from the exact analytic
offset of the D (lines move, the arc keeps its centre), so small rooms never get folded inner rings.
"""
import math, os
import planlib as P

MARGIN = 45          # shrink of the hole bbox
SAG = 0.19           # sagitta as a fraction of the arc-side length
SAG_H = 0.36         # ... but never more than this fraction of the box depth
BOW = os.environ.get('ARC_BOW', 'out')    # 'out' (convex D, chosen) or 'in' (concave, tested)
TRIM_GAP = 110       # brass line distance outside the arc lip
TRIM_W = 14


def _arcpts(cx, cy, r, a0, a1, n):
    return [(cx + r * math.cos(a0 + (a1 - a0) * i / n), cy + r * math.sin(a0 + (a1 - a0) * i / n)) for i in range(n + 1)]


class _D:
    """Base D geometry in a local frame: u along the arc side, v from the straight side (v=0) to the arc."""
    def __init__(self, W, H, s, r, rc, bow):
        self.c = W / 2.0; self.H = H; self.s = s; self.r = r; self.rc = rc; self.bow = bow
        self.R = (self.c ** 2 + s * s) / (2 * s)
        self.Cv = H - self.R if bow == 'out' else H - s + self.R      # circle centre (0, Cv)

    def poly(self, d=0.0):
        """Polygon of the D offset inward by d (d < 0 grows it). None if it collapses."""
        c = self.c - d; vb = d; rc = max(self.rc - d, 6.0); r = max(self.r - d, 6.0)
        Cv = self.Cv
        if self.bow == 'out':
            R = self.R - d; fu = c - r
            if c < 60 or R - r <= fu: return None
            fv = Cv + math.sqrt((R - r) ** 2 - fu ** 2)
            a_side_to_arc = math.atan2(fv - Cv, fu)                     # fillet tangent direction
            apex = Cv + R
        else:
            R = self.R + d; fu = c - r
            if c < 60: return None
            fv = Cv - math.sqrt((R + r) ** 2 - fu ** 2)
            a_side_to_arc = math.atan2(Cv - fv, -fu)
            apex = Cv - R
        if apex - vb < 80 or fv - vb < rc + 10: return None
        half = [(0.0, vb)]
        half += _arcpts(c - rc, vb + rc, rc, 1.5 * math.pi, 2 * math.pi, 8)     # plain corner
        half += _arcpts(fu, fv, r, 0.0, a_side_to_arc, 10)                      # fillet side -> arc
        na = max(24, int(self.c / 45))
        if self.bow == 'out':
            a0 = math.atan2(fv - Cv, fu); half += _arcpts(0.0, Cv, R, a0, math.pi / 2, na)
        else:
            a0 = math.atan2(fv - Cv, fu); half += _arcpts(0.0, Cv, R, a0, -math.pi / 2, na)
        right = half[:-1]
        left = [(-u, v) for (u, v) in reversed(half[1:])]
        pts = right + [half[-1]] + left
        out = []
        for p in pts:
            if not out or math.hypot(p[0] - out[-1][0], p[1] - out[-1][1]) >= 6: out.append(p)
        while len(out) > 3 and math.hypot(out[0][0] - out[-1][0], out[0][1] - out[-1][1]) < 6: out.pop()
        return out

    def arc_angles(self):
        """(R, a_start, a_end) of the main arc for the trim line."""
        c, r = self.c, self.r; fu = c - r; Cv = self.Cv
        if self.bow == 'out':
            fv = Cv + math.sqrt((self.R - r) ** 2 - fu ** 2); a = math.atan2(fv - Cv, fu); return self.R, a, math.pi - a
        fv = Cv - math.sqrt((self.R + r) ** 2 - fu ** 2); a = math.atan2(fv - Cv, fu); return self.R, a, -math.pi - a


def build(c, raw, it, outer, hole, z0, z1):
    x0, x1, y0, y1 = P.bbox(hole)
    x0 += MARGIN; x1 -= MARGIN; y0 += MARGIN; y1 -= MARGIN
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    bw, bh = x1 - x0, y1 - y0
    horiz = bw >= bh * 0.98                       # arc on a horizontal side (larger y) else vertical (larger x)
    W, H = (bw, bh) if horiz else (bh, bw)
    s = min(SAG * W, SAG_H * H)
    if BOW == 'in': s = min(s, 0.22 * H)          # keep the lip off the fan
    rc = max(90, min(190, 0.12 * min(W, H)))
    r = max(80, min(170, 0.10 * min(W, H)))
    D = _D(W, H, s, r, rc, BOW)

    def to_plan(u, v):                           # v=0 straight side, arc toward larger y / larger x
        return (cx + u, y0 + v) if horiz else (x0 + v, cy + u)

    def ring(d):
        p = D.poly(d)
        return [to_plan(u, v) for (u, v) in p] if p else None

    hole2 = ring(0)
    # --- the cove (same layers as P.cove, but with exact offsets of the D) ---
    it.setdefault('_holes', []).append(hole2)
    zl = z0 + 50
    raw(it, outer, hole2, z0, zl, 'fceil', 'fceil')                             # white lip
    raw(it, outer, ring(-80), zl, z1, 'fceil', 'cove')                           # glowing back face of the pocket
    raw(it, ring(-60), ring(-25), zl, zl + 4, 'led', 'led')                      # LED strip on the lip
    g1, g2 = ring(140), ring(360)
    if g1:
        raw(it, hole2, g1, z1 - 3, z1 - 1, 'glow1', 'glow1')                     # strong wash
        if g2: raw(it, g1, g2, z1 - 3, z1 - 1, 'glow2', 'glow2')                  # soft wash
    else:
        g1 = ring(min(W, H) * 0.3)
        if g1: raw(it, hole2, g1, z1 - 3, z1 - 1, 'glow1', 'glow1')
    raw(it, outer, P._offset(outer, -15), z0 - 2, z0, 'reveal', 'reveal')       # shadow gap at the walls

    # --- slim brass line tracing the arc on the flat ceiling, only where it stays calm and inside ---
    if W >= 1300:
        R, a0, a1 = D.arc_angles()
        am = (a0 + a1) / 2; span = (a1 - a0) * 0.86
        n = max(32, int(W / 70))
        sg = 1 if BOW == 'out' else -1
        ri, ro = R + sg * TRIM_GAP, R + sg * (TRIM_GAP + TRIM_W)
        inn = _arcpts(0.0, D.Cv, ri, am - span / 2, am + span / 2, n)
        out = _arcpts(0.0, D.Cv, ro, am + span / 2, am - span / 2, n)
        strip = [to_plan(u, v) for (u, v) in inn + out]
        safe = P._offset(outer, -60)
        if all(P.pip(p, safe) for p in strip):
            c.PRZ(it, strip, z0 - 3, z0, 'gold')
