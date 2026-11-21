// Material textures for realistic mode: tileable detail maps (assets/tex/*.jpg, made by pipeline/textures_gen.py).
// The colour still comes from the theme; a texture only adds pattern on top of it, so every theme keeps working.
// `gain` brightens the material colour to make up for the texture's average darkness (1 / mean brightness).
import * as THREE from 'three';
import MEANS from '../../../assets/tex/means.json';

interface Rule {
  re: RegExp;
  /** file stem in assets/tex */
  file: string;
  /** size of one texture repeat, mm */
  mm: number;
  /** mean brightness of the map (assets/tex/means.json, written by the generator) */
  mean: number;
  /** strength of the matching normal map (_n.jpg), 0 = none */
  normal: number;
  /** surface roughness for this kind of material */
  rough: number;
}

const RULES: Rule[] = [
  { re: /^Floor_Homogeneous|^Floor_Kitchen/, file: 'tile600', mm: 1200, mean: MEANS.tile600, normal: 0.6, rough: 0.22 },
  { re: /^Floor_Toilet|^Wall_Toilet|^Wall_Kitchen/, file: 'tile300x600', mm: 1200, mean: MEANS.tile300x600, normal: 0.6, rough: 0.3 },
  { re: /^Floor_Yard/, file: 'tile300', mm: 1200, mean: MEANS.tile300, normal: 0.6, rough: 0.5 },
  { re: /Marble/, file: 'marble', mm: 1600, mean: MEANS.marble, normal: 0, rough: 0.14 },
  { re: /Sintered/, file: 'sintered', mm: 1400, mean: MEANS.sintered, normal: 0, rough: 0.2 },
  { re: /Quartz/, file: 'quartz', mm: 1200, mean: MEANS.quartz, normal: 0, rough: 0.22 },
  { re: /Walnut/, file: 'walnut', mm: 900, mean: MEANS.walnut, normal: 0.25, rough: 0.55 },
  { re: /Oak/, file: 'oak', mm: 900, mean: MEANS.oak, normal: 0.25, rough: 0.6 },
  { re: /Travertine/, file: 'travertine', mm: 1200, mean: MEANS.travertine, normal: 0.5, rough: 0.7 },
  { re: /Rug|Throw/, file: 'rug', mm: 420, mean: MEANS.rug, normal: 0.8, rough: 1 },
  { re: /Boucle/, file: 'boucle', mm: 300, mean: MEANS.boucle, normal: 0.8, rough: 1 },
  { re: /Leather/, file: 'leather', mm: 400, mean: MEANS.leather, normal: 0.4, rough: 0.55 },
  { re: /Sofa|Cushion|Headboard|Duvet|Linen|Pillow|Velvet|Curtain|Felt|Fabric|Bedding|Towel|Chair_Lumbar/, file: 'fabric', mm: 260, mean: MEANS.fabric, normal: 0.6, rough: 1 },
  { re: /^Wall_Paint|^Ceiling_Paint|^False_Ceiling|Boxup_Board/, file: 'paint', mm: 2400, mean: MEANS.paint, normal: 0.06, rough: 0.92 },
];

export interface TextureInfo {
  map: THREE.Texture;
  normalMap: THREE.Texture | null;
  normalScale: number;
  /** mm per repeat */
  mm: number;
  /** colour multiplier that makes up for the texture's average darkness */
  gain: number;
  rough: number;
}

const loader = new THREE.TextureLoader();
const files: Record<string, THREE.Texture> = {};
const cache: Record<string, TextureInfo | null> = {};
let onLoad: () => void = () => {};

/** Called whenever a texture image finishes loading (so the viewer can redraw). */
export function setTextureLoadCallback(fn: () => void): void { onLoad = fn; }

function load(name: string, srgb: boolean): THREE.Texture {
  const key = name + (srgb ? '' : ':lin');
  if (files[key]) return files[key];
  const t = loader.load(`assets/tex/${name}.jpg?v=${__BUILD__}`, () => onLoad());
  t.wrapS = t.wrapT = THREE.RepeatWrapping; t.anisotropy = 8;
  t.colorSpace = srgb ? THREE.SRGBColorSpace : THREE.NoColorSpace;
  files[key] = t;
  return t;
}

/** Texture set for a material name, or null when the material has no pattern. */
export function textureFor(name: string): TextureInfo | null {
  if (name in cache) return cache[name];
  const r = RULES.find((x) => x.re.test(name));
  cache[name] = r ? {
    map: load(r.file, true), normalMap: r.normal ? load(r.file + '_n', false) : null, normalScale: r.normal,
    mm: r.mm, gain: 1 / r.mean, rough: r.rough,
  } : null;
  return cache[name];
}

/** Box-project UVs onto a triangle soup: each triangle uses the plane its normal faces most. */
export function addBoxUVs(geometry: THREE.BufferGeometry, mm: number): void {
  const p = geometry.attributes.position.array as Float32Array;
  const uv = new Float32Array(p.length / 3 * 2);
  for (let t = 0; t < p.length; t += 9) {
    const ax = p[t + 3] - p[t], ay = p[t + 4] - p[t + 1], az = p[t + 5] - p[t + 2];
    const bx = p[t + 6] - p[t], by = p[t + 7] - p[t + 1], bz = p[t + 8] - p[t + 2];
    const nx = Math.abs(ay * bz - az * by), ny = Math.abs(az * bx - ax * bz), nz = Math.abs(ax * by - ay * bx);
    for (let k = 0; k < 3; k++) {
      const i = t + k * 3, o = (t / 3 + k) * 2;
      if (ny >= nx && ny >= nz) { uv[o] = p[i] / mm; uv[o + 1] = p[i + 2] / mm; }
      else if (nx >= nz) { uv[o] = p[i + 2] / mm; uv[o + 1] = p[i + 1] / mm; }
      else { uv[o] = p[i] / mm; uv[o + 1] = p[i + 1] / mm; }
    }
  }
  geometry.setAttribute('uv', new THREE.BufferAttribute(uv, 2));
}
