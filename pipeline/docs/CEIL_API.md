# False-ceiling concept modules (ceil_<name>.py)

The flat is a 5-room HDB. Every room that has a false ceiling is built by ONE call that your module replaces:

    def build(c, raw, it, outer, hole, z0, z1):
        """outer = plan polygon [(x, y), ...] of the whole dropped ceiling of this room/zone (can be L-shaped / concave).
        hole  = the recess polygon the DEFAULT design uses (an organic blob in the living room, rounded rectangles elsewhere,
                a circle in plan B's lounge). Treat it as "the zone where the feature goes": the ceiling fan / pendant hangs
                at its centre, and downlights are placed outside it. Use P.bbox(hole) -> (x0, x1, y0, y1) and its centre.
        z0 = underside of the dropped ceiling (2550 or 2560), z1 = structural soffit (2650): the recess is only 90-100 mm deep."""

Coordinates: plan mm, x east, y south, z up. Read planlib.py `cove`, `fceil_slab`, `_offset`, `pip`, `bbox` first.

## Building blocks
    import planlib as P, math
    P.cove(c, raw, it, outer, hole2, z0, z1)      the complete standard treatment for ONE recess polygon hole2 inside outer:
                                                  white lip, hidden LED pocket, warm light wash on the recessed soffit, shadow gap at walls.
                                                  => the simplest concept is: compute a new curved polygon and call P.cove once.
    raw(it, outer, hole, z0, z1, mat, mat_hole_edge)   plain slab with exactly ONE hole (hole is required; both polygons simple, hole strictly inside outer,
                                                  keep >= 120 mm between hole and the outer edge). mat_hole_edge colours the vertical faces of the hole.
    c.PRZ(it, poly, z0, z1, mat)                  solid prism (floating panels, light strips, trims);  c.CYL(it, cx, cy, r, z0, z1, mat, n)
    c.RRECT(x0, x1, y0, y1, r, n) / c.ARC(cx, cy, r, a0deg, a1deg, n) / c.ELL(cx, cy, a, b, n) -> polygons;  P._offset(poly, d) grows(+)/shrinks(-) a polygon
    it.setdefault('_holes', []).append(poly)      register any open recess so downlights that would fall inside it are dropped (P.cove does this itself)
    Materials: 'fceil' (white ceiling), 'cove' (warm glowing surface), 'led' (bright LED line), 'glow1' / 'glow2' (strong / soft light wash, emissive),
               'reveal' (dark shadow-gap line), 'gold' (brass trim), 'walnut' / 'oak' (timber), 'lightw' (opal diffuser, glowing). No other keys.

## Rules
- Only ONE true recess (hole) per build call – the slab primitive supports a single hole. Extra shapes (a second crescent, a floating panel, a light
  line) must be added as thin prisms/strips ON the ceiling surface or INSIDE the recess, not as extra holes.
- Keep the feature inside the bounding box of `hole` (shrunk a little) so it never reaches walls, wardrobes, curtain pelmets or downlights; in an
  L-shaped `outer` the bbox of `hole` is always safely inside.
- The ceiling fan (or pendant) hangs at the centre of bbox(hole): the recess or feature must look deliberate around it (fan roughly centred in or
  framed by the shape, never half on a lip edge). Fan blade radius ~650 in bedrooms/living.
- Rooms vary a lot: living ~5.2 x 2.9 m zone with a hole bbox ~3.5 x 1.9 m; dining 1.75 x 2.1 m; bedrooms ~1.3-1.6 x 1.8-2.6 m; study 1.0 x 1.3 m;
  lounge circle r~600. Scale the shape to the bbox; for very small or very elongated boxes simplify (fewer curves) rather than squeeze.
- Curves: use >= 24 segments on big arcs so they look smooth; polygons must not self-intersect; consecutive points >= 5 mm apart.
- Keep it buildable and calm: this is plasterboard with LED strip. Simple, elegant curves – not busy.
- Edit ONLY your own ceil_<name>.py.

## Testing
    python3 ceil_test.py <name>     -> /tmp/ceil_<name>_sheet.png  (12 tiles; compare with /tmp/ceil_wave_sheet.png = current default)
Tiles 1-3 and 11 are reflected ceiling plans seen from BELOW (so they are mirrored left-right relative to plan x; furniture hidden) – best for judging
the shapes. The others look up from inside the rooms. Open the sheet with the Read tool and LOOK; iterate at least 3 rounds. Check: the shape reads
clearly in every room, glow is visible, nothing missing (a room whose recess vanished = the slab failed, usually a hole touching/crossing outer or a
self-intersecting polygon), no z-fighting slivers, fans framed sensibly. The preview is flat-shaded and low-res; the real viewer is smoother.
