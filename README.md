# Lakeside View Plans

A 3D viewer for six layout plans (A–F) of a 5-room HDB flat. Live at **https://rizavur.github.io/home-layout-plans/**.

## How the repo is organised

```
pipeline/   Python that builds every plan's 3D model  →  writes data/ and prev/
web/        React app (the website)                    →  builds index.html and assets/
data/       generated: plan models (JSON), plan list, themes      ┐ served by
prev/       generated: plan-view pictures for the home page       │ GitHub Pages
assets/     generated: app.js / app.css bundle                    │ from the repo
index.html  generated: page shell                                 ┘ root
```

Never edit the generated files by hand – change the source and rebuild.

## Changing a plan (furniture, walls, ceilings…)

Everything is in millimetres; plan coordinates are x = east, y = south, z = up.

| File | What it holds |
|---|---|
| `pipeline/plan_a.py` … `plan_f.py` | One file per plan: its rooms, furniture, scenes (`VIEWS`), labels, dimensions and description |
| `pipeline/blocks.py` | Rooms shared by most plans (bedrooms, foyer, kitchen, dining…) |
| `pipeline/planlib.py` | Furniture builders (sofas, beds, tables, lights…) and the false-ceiling cove |
| `pipeline/style_*.py` | Furniture designs per style (Japandi, Scandinavian, Mid-century, Industrial, Classic) – see `docs/STYLE_API.md` |
| `pipeline/ceil_*.py` | False-ceiling designs (crescent, arc, pill, island) – see `docs/CEIL_API.md` |
| `pipeline/themes*.json` | Interior colour themes and which furniture style each uses |
| `pipeline/build.py` | The plan list shown on the home page, and the build script |
| `pipeline/sketchup_src/` | The original SketchUp scripts the shell (walls, windows, doors) comes from |

Rebuild (needs Python 3 with Pillow):

```bash
cd pipeline
python3 build.py          # all plans  (or: python3 build.py c f  for just C and F)
```

## Changing the website

The app is React + TypeScript, bundled with esbuild. three.js is loaded from a CDN (see the import map in `web/index.html`).

| File | What it does |
|---|---|
| `web/src/App.tsx` | App state: open plan, scene, options, panels; wires the UI to the 3D engine |
| `web/src/engine/Viewer.ts` | 3D engine: loads models, themes, visibility, lighting, camera moves, screenshots |
| `web/src/engine/navigation.ts` | Look-around / orbit / pan / zoom tools, walking keys, camera flights |
| `web/src/engine/textures.ts` | Material textures for realistic mode (`assets/tex`, made by `pipeline/textures_gen.py`) |
| `web/src/engine/photo.ts` | Photo button: path-traces the current view (three-gpu-pathtracer from the CDN) |
| `web/src/engine/walk.ts` | 360° walk: room points, floor circles to step between them, showing saved 360° photos |
| `web/src/engine/context.ts` | The world outside the windows: neighbouring blocks, courtyard, trees, skyline, cloudy sky (from the site plan) |
| `web/src/lib/github.ts` | Saves rendered 360° photos into this repo (`pano/`) with a GitHub token kept in the browser |
| `web/src/engine/tape.ts` | Tape measure tool |
| `web/src/types.ts` | Types for the plan data and viewer options |
| `web/src/components/` | UI pieces: `Landing`, `TopBar`, `Stepper`, `Toolbar`, `SidePanel`, `ViewList`, `AiRenderDialog`, `Icon` |
| `web/src/config/` | Room grouping, ceiling names, AI prompt text, data paths |
| `web/src/lib/` | ZIP writer, "all scenes" export, scene options, localStorage helper |
| `web/src/styles.css` | All styling |

```bash
cd web
npm install
npm run dev       # rebuilds on save, serves http://localhost:8000
npm run typecheck # TypeScript check
npm run build     # production build into ../assets and ../index.html
```

Commit the rebuilt files and push – GitHub Pages serves the repo root.

## Rendering modes

- **Realistic rendering** (side panel, on by default): textured materials, soft daylight from an interior light map, sun shadows,
  and ambient occlusion added once the camera stops moving (skipped on phones). Turn it off for a light mode on older devices.
- **Photo** (toolbar): path traces the current view in the browser – real bounce light, sky through the windows, glass and
  reflections. The image sharpens over a few hundred passes; moving the camera cancels it. Needs WebGL 2.
- **360° walk** (toolbar): stand at a point in each room, drag to look all around, click the circles on the floor to move.
  Where a 360° photo of that point has been saved, it is shown instead of the live 3D view (nothing heavy to render).
- **Rendering 360° photos once**: in the 360° walk, pick a quality and *Render this point* or *Render missing*. On a machine
  with a good graphics card the path tracer renders an equirectangular photo per point. With a GitHub key saved (key button:
  a fine-grained token with *Contents: read and write* on this repo only) each photo is committed to `pano/<plan>/…` with
  `pano/index.json`; GitHub Pages publishes it a minute later and every device then just shows the photo. Without a key
  the photo is downloaded. A saved photo belongs to one look: plan, theme, ceiling design, layout option, day or night.
  After photos have been saved from the browser, run `git pull` before pushing from another clone.
- **Look-around gestures** follow 360-viewer conventions: mouse and touch both drag the scene (it stays under the pointer),
  touch flicks carry on and slow down, pinch or scroll zooms the lens; the mouse cursor is an open / closed hand.
- **Outside the windows**: the neighbouring blocks, courtyard and trees are laid out from the development's site plan
  (8th storey), only while the camera is inside the flat.
- Textures are tileable detail maps: the theme supplies the colour, so every theme keeps working. Regenerate them with
  `cd pipeline && python3 textures_gen.py`.

## Keyboard shortcuts

O orbit · H pan · Z zoom · L look around · T tape measure · Shift+Z fit · W A S D / arrows walk · [ ] previous / next scene · F full view · Esc exit full view

## Notes

- Nothing may be fixed to the household-shelter walls or door.
- Removing the kitchen front wall (open-kitchen options) must be confirmed with HDB / your ID.
- Power points and aircon trunking are indicative only.
