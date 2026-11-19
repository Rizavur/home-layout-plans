// Shapes of the data the Python pipeline writes (data/plan_<key>.json, plans.json, themes.json).

/** [x, y, z] in millimetres, plan coordinates (x east, y south, z up). */
export type Vec3 = [number, number, number];
/** [x, y] in millimetres, plan coordinates. */
export type Vec2 = [number, number];

export type ViewTag = '' | 'top' | 'plan' | 'services' | 'night';

/** A saved camera position ("scene"). */
export interface View {
  name: string;
  eye: Vec3;
  target: Vec3;
  fov: number;
  tag: ViewTag;
  /** layout option the scene switches to, e.g. 'open' kitchen */
  mode: string | null;
}

/** A layout option (e.g. "Open kitchen – glass folded away"): which model layers it hides. */
export interface Mode { label: string; hide: string[] }

/** Material: colour [r, g, b] 0–255, opacity a 0–1, e = glows. */
export interface Material { c: Vec3; a: number; e?: boolean | number }

/** A batch of triangles of one material on one layer. */
export interface Chunk {
  layer: string;
  mat: string;
  /** base64 of little-endian int16 positions (x, z, y per vertex) */
  b64: string;
  n?: number;
  /** 0 = always shown, 1 = default furniture (swapped per style), 2 = default false ceiling (swapped per design) */
  v?: 0 | 1 | 2;
}

export interface PlanData {
  chunks: Chunk[];
  mats: Record<string, Material>;
  views: View[];
  modes: Record<string, Mode>;
  modeLabel?: string;
  /** room names: [text, x, y] */
  labels: [string, number, number][];
  /** dimension lines: [start, end, text] */
  dims: [Vec2, Vec2, string][];
  info: string;
  /** furniture styles available for this plan, besides the default */
  families?: string[];
  /** false-ceiling designs available for this plan, besides the default */
  ceils?: string[];
}

/** Variant file (furniture style or ceiling design): only the swapped pieces. */
export interface VariantData { chunks: Chunk[]; mats: Record<string, Material> }

export interface PlanSummary { key: string; short: string; title: string; bullets: string[]; /** optional card background tint on the home page */ tint?: 'red' | 'green' }

export interface Theme {
  name: string;
  /** three swatch colours shown on the button */
  sw: [string, string, string];
  /** furniture style this theme uses */
  fam: string;
  /** material name -> colour override */
  m: Record<string, Vec3>;
}

/** What the viewer shows. */
export interface ViewOptions {
  mode: string;
  /** false ceiling and lights */
  fc: boolean;
  /** room names and dimensions */
  lab: boolean;
  /** power points */
  pwr: boolean;
  /** aircon trunking */
  ac: boolean;
  /** curtains */
  cur: boolean;
  /** night mood */
  night: boolean;
  /** timber slats lining the false-ceiling recesses */
  wood: boolean;
}

export type Tool = 'look' | 'orbit' | 'pan' | 'zoom' | 'tape';
export type Lighting = 'day' | 'golden' | 'night';
