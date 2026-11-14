"""SOFT PILL false-ceiling concept: one clean stadium (or circle / squircle) recess per zone,
with a floating inner pill panel and a second soft halo inside the tray."""
import math
import planlib as P



def _stadium(cx, cy, L, W, along_x, n=28):
    """Stadium of overall length L and width W (ends fully round, r = W/2), CCW."""
    r = W / 2.0; s = max(0.0, L / 2.0 - r); pts = []
    for i in range(n + 1):                                  # +u end
        a = -math.pi / 2 + math.pi * i / n
        pts.append((s + r * math.cos(a), r * math.sin(a)))
    for i in range(n + 1):                                  # -u end
        a = math.pi / 2 + math.pi * i / n
        pts.append((-s + r * math.cos(a), r * math.sin(a)))
    if along_x:
        out = [(cx + u, cy + v) for u, v in pts]
    else:
        out = [(cx - v, cy + u) for u, v in pts]
    return P._dedupe(out)


def _squircle(cx, cy, a, b, e=2.6, n=64):
    out = []
    for i in range(n):
        t = 2 * math.pi * i / n; ct, st = math.cos(t), math.sin(t)
        out.append((cx + a * math.copysign(abs(ct) ** (2.0 / e), ct), cy + b * math.copysign(abs(st) ** (2.0 / e), st)))
    return P._dedupe(out)


def _shape(cx, cy, L, W, along_x):
    """Pill when elongated, circle/squircle when nearly square."""
    if L / W < 1.25:
        a = L / 2.0 if along_x else W / 2.0
        b = W / 2.0 if along_x else L / 2.0
        if abs(a - b) < 40:
            r = min(a, b); return _squircle(cx, cy, r, r, 2.0, 72)      # true circle
        return _squircle(cx, cy, a, b, 2.6, 72)
    return _stadium(cx, cy, L, W, along_x)


def _inside(poly, outer, margin=125):
    xs = [p for p in poly if not P.pip(p, P._offset(outer, -margin))]
    return not xs


def build(c, raw, it, outer, hole, z0, z1):
    x0, x1, y0, y1 = P.bbox(hole)
    cx, cy = (x0 + x1) / 2.0, (y0 + y1) / 2.0
    bw, bh = x1 - x0, y1 - y0
    along_x = bw >= bh
    Lb, Wb = (bw, bh) if along_x else (bh, bw)
    # shrink a little; big boxes get a calmer, proportionally larger margin
    m = 40 + 0.06 * max(0.0, Lb - 1500)
    L, W = Lb - 2 * m, Wb - 2 * m * (Wb / Lb) ** 0.5
    if Lb > 2600:                       # living room: do not fill edge to edge
        L *= 0.90; W *= 0.94
    if L / W > 2.6: L = 2.6 * W
    pill = _shape(cx, cy, L, W, along_x)
    # safety: shrink until comfortably inside outer
    k = 0
    while not _inside(pill, outer) and k < 12:
        L *= 0.95; W *= 0.95; pill = _shape(cx, cy, L, W, along_x); k += 1
    P.cove(c, raw, it, outer, pill, z0, z1)
    # --- inner detail: floating concentric pill panel ("tray in the tray") with its own soft halo
    inset = max(380.0, 0.30 * W)
    Li, Wi = L - 2 * inset, W - 2 * inset
    if Wi >= 300:
        inner = _shape(cx, cy, max(Li, Wi), Wi, along_x)
        zb = z1 - 35
        c.PRZ(it, inner, zb, zb + 18, 'fceil')                        # the floating panel
        raw(it, P._offset(inner, 8), inner, zb - 1, zb + 18, 'gold', 'gold')   # slim brass edge band
        c.PRZ(it, P._offset(inner, -40), zb + 18, z1 - 8, 'fceil')    # set-back hanger / LED carrier
        ring = P._offset(inner, 120)
        raw(it, ring, inner, z1 - 4, z1 - 3.5, 'glow1', 'glow1')      # bright halo hugging the panel
        raw(it, P._offset(inner, 220), ring, z1 - 4, z1 - 3.5, 'glow2', 'glow2')   # soft outer halo
