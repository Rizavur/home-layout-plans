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
| `web/src/engine/textures.ts` | Procedural textures (tiles, marble, wood, fabric) |
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

## Keyboard shortcuts

O orbit · H pan · Z zoom · L look around · T tape measure · Shift+Z fit · W A S D / arrows walk · [ ] previous / next scene · F full view · Esc exit full view

## Notes

- Nothing may be fixed to the household-shelter walls or door.
- Removing the kitchen front wall (open-kitchen options) must be confirmed with HDB / your ID.
- Power points and aircon trunking are indicative only.
