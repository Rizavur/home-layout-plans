// Data produced by the Python pipeline (pipeline/build.py) and bundled into the app.
import plans from '../../../data/plans.json';
import themes from '../../../data/themes.json';

/** Plans shown on the home page: [{ key, short, title, bullets }] */
export const PLANS = plans;

/** Interior themes: { key: { name, sw: [3 swatch colours], fam: furniture family, m: { material: [r, g, b] } } } */
export const THEMES = themes;

/** False-ceiling designs. 'wave' is built into every plan; the others load on demand. */
export const CEILINGS = {
  wave: 'Organic wave',
  crescent: 'Crescent',
  arc: 'Sweeping arc',
  pill: 'Soft pill',
  island: 'Floating island',
};

/** Where plan data and previews live, relative to the page. */
export const planUrl = (file) => `data/plan_${file}.json?v=${__BUILD__}`;
export const previewUrl = (key) => `prev/plan_${key}.jpg?v=${__BUILD__}`;

/** Narrow screens (phones, small tablets in portrait) get the slide-over panel. */
export const isNarrow = () => window.innerWidth <= 860;
