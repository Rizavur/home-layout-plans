# Furniture family modules (style_<family>.py)

Each family file defines Python functions that REPLACE the default ("lux") furniture when that family is active.
The defaults live in planlib.py (sofa3, bed3, dining_table, dchair4, ppebble, floor_lamp, lounge_chair,
dining_pendant, bedside_pendant) – read them first, they show the conventions and the level of detail expected.

## Coordinates
Plan millimetres. x = east, y = south, z = up (floor = 0). Ceiling (false ceiling underside) = 2550.

## Functions to define (exact names and signatures)
    sofa(c, it, face, cx, cy, W, D, nseat, armL=True, armR=True, chaise=None, body='sofa', cush='sofa2', pil=('pil1','pil2'))
        face = direction the sitter looks (+x,-x,+y,-y). Read sofa3 in planlib.py for the frame:
        use T = c.LF(face, cx, cy); T(u, v) maps local (u across, v forward) to plan (x, y); the sofa occupies
        u in [-W/2, W/2], v in [-D, 0] (back of sofa at v=-D, front edge at v=0). chaise=(u0,u1,len) extends the seat
        forward to v=+len between u0..u1 (L-sofa). nseat = seat cushions. armL/armR = which ends have arms.
        body/cush/pil are MATERIAL KEYS to use for frame upholstery / seat+back cushions / the two scatter pillows.
        Seat height ~430, overall height 750-850. Must stay inside the footprint (plus chaise).
    bed(c, it, x0, x1, y0, y1, head, npil, deco=True)
        Footprint box x0..x1, y0..y1. head is '+x' or '-x' = the side where the headboard is (it is against a wall
        at that x). npil = 1 (single) or 2 (two sleeping pillows side by side across y). deco = add scatter cushion / throw.
        Mattress top ~500-560. Headboard may be up to 1250 high and may overhang y by <= 40 each side.
    dining_table(c, it, x0, x1, y0, y1)
        Top surface MUST be at z = 758 exactly (place settings sit on it) and cover the whole x0..x1, y0..y1 rectangle
        (corner radius <= 60 ok; no oval/round tops). Legs/base must leave knee room: chairs sit centred ~230 mm outside
        each long edge and at both short ends.
    dchair(c, it, cx, cy, back)
        Dining chair centred at (cx, cy); back = side where the backrest is ('-y','+y','-x','+x'); sitter faces the opposite way.
        Footprint about 470 x 480, seat top ~470-490, total height 800-900.
    coffee_table(c, it, cx, cy, a, b, ztop)
        Fits within cx±a, cy±b (a=520, b=380 typically). Solid top surface at z = ztop (400) that covers at least
        cx±320, cy±200 (a bowl sits on it).
    floor_lamp(c, it, x, y)            base centred at (x, y), ~1600-1750 tall, footprint radius <= 230 (it stands near walls).
    lounge_chair(c, it, cx, cy, face_deg, body='cush', base='walnut')
        Accent armchair, footprint radius <= 430 around (cx, cy). face_deg = plan angle the sitter faces (0=+x, 90=+y). body = upholstery key.
    nightstand(c, it, x0, x1, y0, y1)  box footprint 400 x 370, top at 500-540. (Wall is at one of the x sides – keep it symmetric.)
    dining_pendant(c, it, x0, x1, yc)  light(s) over the dining table: spread along x0..x1 (about 1300 long) centred on y=yc,
        suspended from z=2550, lowest point no lower than 1600. Use 'lightw' (glowing) for diffusers / bulbs.
    bedside_pendant(c, it, cx, cy)     one small hanging light at (cx, cy) from z=2550, shade bottom around z=1100-1150.

## Geometry helpers (c = context)
    c.B(it, x0, x1, y0, y1, z0, z1, mat)            axis-aligned box  (KEEP FOR BIG SIMPLE PARTS ONLY – prefer prisms)
    c.CYL(it, cx, cy, r, z0, z1, mat, n=32)         vertical cylinder (n sides; use 8-16 for small parts)
    c.PRZ(it, pts, z0, z1, mat)                     vertical prism from a plan polygon [(x, y), ...]
    c.RRECT(x0, x1, y0, y1, r, n=8) -> pts          rounded rectangle polygon;  c.ARC(cx, cy, r, a0deg, a1deg, n) -> pts
    c.ELL(cu, cv, a, b, n) -> pts (ellipse);  c.inset(pts, d) -> pts (shrink towards centroid)
    c.LF(face, cx, cy) -> T;  T(u, v) -> (x, y);  c.LP(T, pts) -> transformed pts
    c.PR3(it, pts2d, O, U, V, W, t0, t1, mat)       prism in an arbitrary frame: polygon pts in (U,V) plane at origin O (3-vectors), extruded along W from t0..t1
    P._loft(it, lo, hi, mat)                        loft between two rings of 3D points [(x,y,z),...] with the SAME point count & order
                                                    (tapered legs, splayed legs, leaning backs, curved shells). Rings must be convex-ish & planar.
    P.soft_slab(c, it, poly, z0, z1, mat, r=40, n=3, bottom=True)   prism with rounded top (and bottom) edges – mattresses, seat cushions, table tops
    P.cushion3d(c, it, O, U, V, w, h, t, mat, crown=0.5)            stuffed pillow: centre O (3-vector), U/V unit 3-vectors in the pillow plane, size w x h, thickness t
    P.rbox(c, it, cx, cy, L, T, ang_deg, z0, z1, mat, du=0, dv=0)   box rotated in plan
    P.channel_headboard(...)  (see planlib) ;  `import planlib as P`, `import math`
Keep triangle count sensible: a sofa <= ~3000 triangles, a dining chair <= ~500 (8 chairs!), bed <= ~3000.

## Material keys (colours are re-tinted per theme, so use the keys by MEANING)
    upholstery: the body/cush/pil args for sofas; 'headb' (bed frame/headboard fabric), 'duvet', 'linen' (sheets), 'linen2' (white pillows),
                'pil1','pil2' (scatter cushions), 'throw', 'seat' (fabric dining seat), 'leather2' (dining-chair leather), 'leather3' (darker leather / piping),
                'leather' (caramel leather), 'cush' (cream boucle)
    wood: 'walnut' (dark), 'walnut2' (fluted dark), 'oak' (light oak), 'oakd' (mid smoked oak)
    stone: 'marble', 'traver' (travertine), 'sintered', 'quartz';  ceramic: 'ceramic'
    metal: 'gold'/'brass' (same champagne brass), 'metal' (black), 'blksteel' (black powder-coated steel), 'steel' (brushed), 'chrome'
    other: 'cane' (rattan/cane weave), 'paper' (glowing paper lampshade), 'lightw' (glowing opal diffuser), 'glass', 'smoke' (smoked glass),
           'artbg' (ivory fabric lampshade), 'charcoal', 'greige', 'white', 'rug1','rug2'
Do NOT invent new keys (KeyError). Do not edit planlib.py, blocks.py, export.py, plan_*.py or any other shared file – only your own style_<family>.py.

## Testing
    python3 style_test.py <family>      -> writes /tmp/style_<family>_sheet.png (11 views: living, dining, bedrooms, lounge, close-ups)
Open the sheet with the Read tool and LOOK at it; iterate until every piece reads clearly as the intended design, nothing floats,
nothing pokes through walls/floor, chairs face the table, pillows sit on the bed, and the pieces look clearly different from
/tmp/style_lux_sheet.png (the default family). The preview renderer is flat-shaded and low-res; the real viewer is smoother.
A missing function simply falls back to the default, so add them one at a time and test as you go.
