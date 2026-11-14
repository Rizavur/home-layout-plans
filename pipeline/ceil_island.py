"""FLOATING ISLAND false-ceiling concept.
A wide, softly rounded tray is cut into the dropped ceiling; inside it a white pebble-shaped panel floats just above the
main ceiling plane, with a warm halo of light spilling out of the gap all around it.

Geometry rule (same in every room, scaled to bbox(hole)):
  tray   = rounded rectangle filling bbox(hole) shrunk 60 mm, corner radius 36 % of the short side
           (short side < 1200 mm -> radius 50 % : a stadium / circle tray).
  island = super-ellipse pebble (exponent 2.6, or 2.0 for small zones) on the long axis, centred on the fan,
           one end ~14 % fuller than the other (egg taper), inset INSET mm from the tray edge.
           Underside z0 + 28, 40 mm thick.
  light  = LED strip on top of the island rim, glow1 wash on the soffit just outside the island, glow2 on the rest of
           the gap, softly lit ('cove') tray walls.
"""
import math
import planlib as P


def _rrect(x0, x1, y0, y1, r, n=10):
    r = max(5.0, min(r, (x1 - x0) / 2 - 0.5, (y1 - y0) / 2 - 0.5))
    pts = []
    for (cx, cy, a0) in ((x1 - r, y1 - r, 0), (x0 + r, y1 - r, 90), (x0 + r, y0 + r, 180), (x1 - r, y0 + r, 270)):
        for i in range(n + 1):
            a = math.radians(a0 + 90.0 * i / n)
            pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return P._dedupe([(round(x, 1), round(y, 1)) for x, y in pts])


def _pebble(cx, cy, A, B, horiz, p, k, n=72):
    """Super-ellipse with semi-axes A (long) x B (short), one end fuller (taper k). horiz: long axis along x."""
    pts = []
    for i in range(n):
        t = 2 * math.pi * i / n
        ct, st = math.cos(t), math.sin(t)
        u = math.copysign(abs(ct) ** (2.0 / p), ct)
        v = math.copysign(abs(st) ** (2.0 / p), st)
        lu, lv = A * u, B * v * (1 + k * u)
        pts.append((cx + lu, cy + lv) if horiz else (cx + lv, cy + lu))
    return P._dedupe([(round(x, 1), round(y, 1)) for x, y in pts])


def _inside(poly, region):
    return all(P.pip(q, region) for q in poly)


def build(c, raw, it, outer, hole, z0, z1):
    x0, x1, y0, y1 = P.bbox(hole)
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    W, H = x1 - x0, y1 - y0
    short = min(W, H)
    small = short < 1200

    # ---- tray (the one real recess) ----
    m = 60
    safe = P._offset(outer, -125)
    tray = None
    for _ in range(12):
        rr = (0.5 if small else 0.36) * (short - 2 * m)
        cand = _rrect(x0 + m, x1 - m, y0 + m, y1 - m, rr, 12)
        if _inside(cand, safe):
            tray = cand; break
        m += 40
    if tray is None:                      # fall back to the default recess rather than lose the room
        return P.cove(c, raw, it, outer, hole, z0, z1)
    tx0, tx1, ty0, ty1 = P.bbox(tray)
    tw, th = tx1 - tx0, ty1 - ty0

    # ---- island (floating pebble) ----
    inset = max(170, min(270, 0.15 * min(tw, th)))
    horiz = tw >= th
    p, k = (2.0, 0.12) if small else (2.6, 0.20)
    A = (max(tw, th) / 2 - inset)
    B = (min(tw, th) / 2 - inset) / (1 + k * 0.35)
    region = P._offset(tray, -(inset - 25))
    isl = _pebble(cx, cy, A, B, horiz, p, k)
    for _ in range(20):
        if _inside(isl, region): break
        A *= 0.97; B *= 0.97
        isl = _pebble(cx, cy, A, B, horiz, p, k)

    # ---- slab with the tray ----
    it.setdefault('_holes', []).append(tray)
    raw(it, outer, tray, z0, z1, 'fceil', 'fceil')                       # plain white tray walls
    raw(it, outer, P._offset(outer, -15), z0 - 2, z0, 'reveal', 'reveal')  # shadow gap at the walls

    # ---- light on the tray soffit, visible through the gap ----
    raw(it, P._offset(isl, 140), P._offset(isl, -60), z1 - 3, z1 - 1, 'glow1', 'glow1')
    raw(it, P._offset(tray, -2), P._offset(isl, 140), z1 - 3, z1 - 1, 'glow2', 'glow2')

    # ---- the floating island ----
    zi0, zi1 = z0 + 28, z0 + 68
    c.PRZ(it, isl, zi0, zi1, 'fceil')
    raw(it, isl, P._offset(isl, -12), zi0 - 1.5, zi0, 'reveal', 'reveal')   # crisp dark arris line on the island underside
    raw(it, P._offset(isl, -15), P._offset(isl, -50), zi1, zi1 + 4, 'led', 'led')   # LED strip on top of the rim
