// "All scenes ZIP": renders every scene of the open plan and packs each image with its ChatGPT prompt.
import { buildPrompt } from '../config/prompts';
import { PLANS, THEMES, CEILINGS } from '../config/data';
import { optionsForView } from './viewOptions';
import { makeZip, downloadBlob, slug, type ZipEntry } from './zip';
import type { Viewer } from '../engine/Viewer';
import type { Lighting, ViewOptions } from '../types';

const SKIP_TAGS: string[] = ['plan', 'services', 'top'];
const twoFrames = (): Promise<void> => new Promise((r) => requestAnimationFrame(() => requestAnimationFrame(() => r())));

export interface ExportInput {
  planKey: string;
  opts: ViewOptions;
  theme: string;
  lighting: Lighting;
  onProgress: (text: string) => void;
}

export async function exportAllScenes(viewer: Viewer, { planKey, opts, theme, lighting, onProgress }: ExportInput): Promise<void> {
  const plan = viewer.plan!;
  const enc = new TextEncoder();
  const files: ZipEntry[] = []; let allPrompts = '';
  const indices = plan.views.map((_v, i) => i).filter((i) => !SKIP_TAGS.includes(plan.views[i].tag));
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
  const title = PLANS.find((p) => p.key === planKey)?.title ?? planKey;
  const readme = `Lakeside View Plans – ${title}\nTheme: ${THEMES[theme].name}   Ceiling: ${CEILINGS[viewer.ceilingDesign()]}\n\n`
    + 'How to use: open a new ChatGPT chat, attach one .jpg and paste the matching .txt prompt (same number), then send.\n'
    + 'One image per chat works best. Ask for tweaks afterwards, e.g. "warmer light" or "keep the sofa exactly where it is".\n\n'
    + allPrompts;
  files.unshift({ name: '00-README-all-prompts.txt', data: enc.encode(readme) });
  downloadBlob(makeZip(files), `lakeside-plan-${planKey}-${slug(THEMES[theme].name)}-${viewer.ceilingDesign()}.zip`);
}
