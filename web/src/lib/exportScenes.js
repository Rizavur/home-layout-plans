// "All scenes ZIP": renders every scene of the open plan and packs each image with its ChatGPT prompt.
import { buildPrompt } from '../config/prompts.js';
import { PLANS, THEMES, CEILINGS } from '../config/data.js';
import { optionsForView } from './viewOptions.js';
import { makeZip, downloadBlob, slug } from './zip.js';

const SKIP_TAGS = ['plan', 'services', 'top'];
const twoFrames = () => new Promise((r) => requestAnimationFrame(() => requestAnimationFrame(r)));

/**
 * @param {import('../engine/Viewer.js').Viewer} viewer
 * @param {{ planKey: string, opts: object, theme: string, lighting: string, onProgress: (text: string) => void }} p
 */
export async function exportAllScenes(viewer, { planKey, opts, theme, lighting, onProgress }) {
  const plan = viewer.plan;
  const enc = new TextEncoder();
  const files = []; let allPrompts = '';
  const indices = plan.views.map((v, i) => i).filter((i) => !SKIP_TAGS.includes(plan.views[i].tag));
  for (let n = 0; n < indices.length; n++) {
    const view = plan.views[indices[n]];
    onProgress(`Rendering ${n + 1} / ${indices.length}…`);
    viewer.setOptions(optionsForView(view, opts, plan.modes));
    viewer.showView(view, { instant: true });
    await twoFrames();
    const url = await viewer.capture('image/jpeg');
    const image = new Uint8Array(await (await fetch(url)).arrayBuffer());
    const prompt = buildPrompt({
      viewName: view.name, fromAbove: viewer.isAboveCeiling(), theme, family: viewer.family(),
      ceiling: viewer.ceilingDesign(), lighting: view.tag === 'night' ? 'night' : lighting,
    });
    const base = `${String(n + 1).padStart(2, '0')}-${slug(view.name)}`;
    files.push({ name: `${base}.jpg`, data: image }, { name: `${base}.txt`, data: enc.encode(prompt + '\n') });
    allPrompts += `=== ${base}.jpg  (${view.name}) ===\n${prompt}\n\n`;
  }
  const title = PLANS.find((p) => p.key === planKey).title;
  const readme = `Lakeside View Plans – ${title}\nTheme: ${THEMES[theme].name}   Ceiling: ${CEILINGS[viewer.ceilingDesign()]}\n\n`
    + 'How to use: open a new ChatGPT chat, attach one .jpg and paste the matching .txt prompt (same number), then send.\n'
    + 'One image per chat works best. Ask for tweaks afterwards, e.g. "warmer light" or "keep the sofa exactly where it is".\n\n'
    + allPrompts;
  files.unshift({ name: '00-README-all-prompts.txt', data: enc.encode(readme) });
  downloadBlob(makeZip(files), `lakeside-plan-${planKey}-${slug(THEMES[theme].name)}-${viewer.ceilingDesign()}.zip`);
}
