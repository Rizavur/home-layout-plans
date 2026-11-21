// The world outside the windows: the neighbouring blocks, the landscaped courtyard eight storeys below,
// trees, roads, distant estates and a sky with clouds. Laid out from the development's site plan
// (1 site-plan pixel = 261.4 mm), relative to the flat's south-east corner (plan x = 0, y = 0).
// Plan +x points real west and plan +y real north (the flat's living room faces south, towards plan y < 0).
//
// Only shown when the camera is inside the flat; plan and overview shots keep the plain background.
import * as THREE from 'three';
import { mergeGeometries } from 'three/addons/utils/BufferGeometryUtils.js';

/** height of the flat's floor above the ground */
export const FLOOR_HEIGHT = 20600;
const STOREY = 2800, BAY = 4500;
const PX = 261.4, OX = 518, OY = 250;
/** site-plan pixel -> plan mm */
const sx = (cx: number) => (OX - cx) * PX;
const sy = (cy: number) => (OY - cy) * PX;

interface Block { x0: number; x1: number; y0: number; y1: number; storeys: number; rot?: number; tint?: number; low?: boolean }

// footprints read off the site plan: [x0, x1, y0, y1] in site-plan pixels, storeys
const SITE: [number, number, number, number, number, number?][] = [
  // our block: mirror flat across the lift lobby, lift core, wing to the north, slab to the east, 2-room wing to the west
  [540, 612, 205, 250, 17], [527, 541, 200, 252, 18], [535, 552, 168, 205, 17], [490, 625, 128, 172, 17], [625, 668, 135, 238, 17],
  [380, 455, 155, 195, 12], [372, 448, 196, 232, 12], [455, 462, 205, 245, 17],
  // block south across the courtyard
  [460, 552, 318, 378, 17], [430, 546, 392, 458, 17], [315, 415, 310, 385, 17], [415, 446, 330, 382, 17],
  // block to the south-east
  [583, 668, 345, 398, 17], [618, 715, 400, 452, 11], [765, 845, 262, 330, 11], [700, 775, 295, 350, 11],
  // further south-east
  [1065, 1290, 520, 700, 17], [850, 1000, 750, 860, 17], [1100, 1250, 760, 850, 17], [1020, 1080, 800, 950, 11],
];
// older estates and the school beyond the site (lower, greyer)
const ESTATE: [number, number, number, number, number, number][] = [
  [60, 330, 600, 660, 12, 18], [60, 300, 740, 800, 12, 18], [330, 560, 700, 760, 12, -25], [430, 640, 820, 880, 12, -25],
  [150, 300, 880, 940, 12, 0], [620, 700, 560, 760, 12, 5], [40, 260, 420, 470, 12, 18], [70, 470, 30, 100, 4, 0], [280, 420, 105, 150, 4, 0],
];

function blocks(): Block[] {
  const b: Block[] = SITE.map(([a, c, d, e, s]) => ({ x0: sx(c), x1: sx(a), y0: sy(e), y1: sy(d), storeys: s }));
  for (const [a, c, d, e, s, r] of ESTATE) b.push({ x0: sx(c), x1: sx(a), y0: sy(e), y1: sy(d), storeys: s, rot: r, tint: 1, low: s < 6 });
  // the floors of our own block directly above and below the flat (the flat itself sits in the gap)
  b.push({ x0: 0, x1: 14600, y0: 0, y1: 9550, storeys: -1 });
  return b;
}

/** Facade texture of a modern HDB block: four 4.5 m bays by six storeys, painted panels, glazing, ledges. */
function facadeCanvas(estate: boolean, night: boolean): HTMLCanvasElement {
  const W = 512, H = 640, c = document.createElement('canvas'); c.width = W; c.height = H;
  const g = c.getContext('2d')!;
  const wall = estate ? '#d9d4ca' : '#eeebe4', accent = estate ? '#b9b2a6' : '#c9d3d6', glass = night ? '#1b1d22' : '#59636b';
  g.fillStyle = night ? '#2b2a28' : wall; g.fillRect(0, 0, W, H);
  const bw = W / 4, sh = H / 6;
  let seed = estate ? 7 : 3;
  const rnd = () => { seed = (seed * 16807) % 2147483647; return seed / 2147483647; };
  for (let s = 0; s < 6; s++) {
    const y = s * sh;
    for (let k = 0; k < 4; k++) {
      const x = k * bw;
      if (!estate && (k === 1 || k === 2)) { g.fillStyle = night ? '#3a3a38' : accent; g.fillRect(x + 4, y + 4, bw - 8, sh - 10); }
      const wide = k % 2 === 0;
      const wx = x + (wide ? 14 : 34), ww = wide ? bw - 28 : bw - 68, wy = y + sh * 0.26, wh = sh * 0.5;
      const lit = night && rnd() < 0.45;
      g.fillStyle = lit ? (rnd() < 0.5 ? '#ffd9a0' : '#f4efe4') : glass; g.fillRect(wx, wy, ww, wh);
      if (!night) { g.fillStyle = 'rgba(255,255,255,0.18)'; g.fillRect(wx, wy, ww, wh * 0.35); }
      g.fillStyle = night ? '#55524c' : '#f7f6f2'; g.fillRect(wx - 2, wy - 2, ww + 4, 3); g.fillRect(wx - 2, wy + wh, ww + 4, 3);
      for (let m = 1; m < 3; m++) g.fillRect(wx + (ww * m) / 3 - 1, wy, 2.5, wh);
      // aircon ledge with a condenser on some bays
      if (k === 3) {
        g.fillStyle = night ? '#3c3b38' : '#d8d6d0'; g.fillRect(x + 6, y + sh * 0.78, bw - 12, sh * 0.12);
        g.fillStyle = night ? '#4a4844' : '#bfbcb5'; g.fillRect(x + 20, y + sh * 0.62, bw * 0.4, sh * 0.16);
      }
    }
    // floor slab line
    g.fillStyle = night ? '#252422' : (estate ? '#c4beb3' : '#dcd9d2'); g.fillRect(0, y + sh - 6, W, 6);
  }
  return c;
}

/** Canvas -> plain RGBA data texture (the path tracer handles data textures reliably; canvas textures got mixed up). */
function canvasTexture(c: HTMLCanvasElement): THREE.DataTexture {
  const src = c.getContext('2d')!.getImageData(0, 0, c.width, c.height).data, w = c.width, h = c.height;
  const d = new Uint8Array(w * h * 4);
  for (let j = 0; j < h; j++) d.set(src.subarray((h - 1 - j) * w * 4, (h - j) * w * 4), j * w * 4);   // first row = bottom
  const t = new THREE.DataTexture(d, w, h, THREE.RGBAFormat, THREE.UnsignedByteType);
  t.colorSpace = THREE.SRGBColorSpace; t.wrapS = t.wrapT = THREE.RepeatWrapping;
  t.magFilter = THREE.LinearFilter; t.minFilter = THREE.LinearMipmapLinearFilter; t.generateMipmaps = true; t.anisotropy = 4;
  t.needsUpdate = true; return t;
}

/** Box with world-scaled UVs on the walls (one texture repeat = 4 bays x 6 storeys). */
function blockGeometry(b: Block): THREE.BufferGeometry {
  const w = b.x1 - b.x0, d = b.y1 - b.y0;
  const z0 = -FLOOR_HEIGHT, h = b.storeys * STOREY + 3600;     // ground-floor void deck is taller
  const g = new THREE.BoxGeometry(w, h, d);
  const uv = g.attributes.uv as THREE.BufferAttribute;
  // BoxGeometry face order: +x, -x, +y, -y, +z, -z (4 vertices each)
  const faceW = [d, d, w, w, w, w];
  for (let f = 0; f < 6; f++) for (let k = 0; k < 4; k++) {
    const i = f * 4 + k;
    if (f === 2 || f === 3) { uv.setXY(i, 0, 0); continue; }      // roof / underside: no facade
    uv.setXY(i, uv.getX(i) * faceW[f] / (4 * BAY), uv.getY(i) * h / (6 * STOREY));
  }
  g.translate((b.x0 + b.x1) / 2, z0 + h / 2, (b.y0 + b.y1) / 2);
  if (b.rot) {
    const c = new THREE.Vector3((b.x0 + b.x1) / 2, 0, (b.y0 + b.y1) / 2);
    g.translate(-c.x, 0, -c.z); g.rotateY(THREE.MathUtils.degToRad(b.rot)); g.translate(c.x, 0, c.z);
  }
  return g;
}

/** Our own block above and below the flat: two boxes leaving the flat's storey open. */
function ownBlock(): THREE.BufferGeometry[] {
  const w = 14600, d = 9550, out: THREE.BufferGeometry[] = [];
  for (const [y0, y1] of [[-FLOOR_HEIGHT, -160], [2860, 17 * STOREY + 3600 - FLOOR_HEIGHT]]) {
    const g = new THREE.BoxGeometry(w, y1 - y0, d);
    const uv = g.attributes.uv as THREE.BufferAttribute;
    const faceW = [d, d, w, w, w, w];
    for (let f = 0; f < 6; f++) for (let k = 0; k < 4; k++) {
      const i = f * 4 + k; if (f === 2 || f === 3) { uv.setXY(i, 0, 0); continue; }
      uv.setXY(i, uv.getX(i) * faceW[f] / (4 * BAY), uv.getY(i) * (y1 - y0) / (6 * STOREY) + (y0 + FLOOR_HEIGHT) / (6 * STOREY));
    }
    g.translate(w / 2, (y0 + y1) / 2, d / 2); out.push(g);
  }
  return out;
}

/** Low-poly trees (trunk + two-lobed canopy), merged into one mesh per material. */
function trees(): { crowns: THREE.BufferGeometry; trunks: THREE.BufferGeometry } {
  let seed = 11; const rnd = () => { seed = (seed * 16807) % 2147483647; return seed / 2147483647; };
  const spots: [number, number, number][] = [];
  // courtyard and site edges (site-plan pixels), avoiding the blocks
  const zones: [number, number, number, number, number][] = [
    [380, 560, 255, 315, 26], [560, 720, 250, 340, 14], [300, 460, 395, 470, 10], [560, 740, 455, 520, 12], [260, 320, 150, 400, 16],
    [330, 470, 120, 150, 10], [640, 760, 90, 230, 14], [740, 1000, 360, 420, 10], [900, 1100, 640, 740, 14], [320, 430, 470, 520, 8],
  ];
  const inBlock = (x: number, y: number) => SITE.some(([a, c, d, e]) => x > a - 6 && x < c + 6 && y > d - 6 && y < e + 6) || (x > 340 && x < 455 && y > 250 && y < 300);
  for (const [a, c, d, e, n] of zones) {
    for (let k = 0, tries = 0; k < n && tries < n * 20; tries++) {
      const x = a + rnd() * (c - a), y = d + rnd() * (e - d);
      if (inBlock(x, y)) continue;
      spots.push([sx(x), sy(y), 0.75 + rnd() * 0.6]); k++;
    }
  }
  const crowns: THREE.BufferGeometry[] = [], trunks: THREE.BufferGeometry[] = [];
  const base = new THREE.IcosahedronGeometry(1, 1);
  for (const [x, y, s] of spots) {
    const h = 9000 * s, r = 3600 * s;
    const t = new THREE.CylinderGeometry(160 * s, 240 * s, h * 0.6, 6); t.translate(x, -FLOOR_HEIGHT + h * 0.3, y); trunks.push(t);
    for (const [dx, dy, dz, k] of [[0, 0, 0, 1], [r * 0.45, -r * 0.2, r * 0.3, 0.7], [-r * 0.4, -r * 0.25, -r * 0.35, 0.65]]) {
      const c = base.clone(); c.scale(r * k, r * 0.72 * k, r * k);
      c.translate(x + dx, -FLOOR_HEIGHT + h * 0.72 + dy, y + dz); crowns.push(c);
    }
  }
  return { crowns: mergeGeometries(crowns), trunks: mergeGeometries(trunks) };
}

/** Flat ground pieces: lawn, driveways and paths, the road along the north-east, playground pits. */
function ground(): { geo: THREE.BufferGeometry; mat: string }[] {
  const flat = (pts: [number, number][], lift: number) => {
    const shape = new THREE.Shape(pts.map(([x, y]) => new THREE.Vector2(sx(x), -sy(y))));
    const g = new THREE.ShapeGeometry(shape); g.rotateX(-Math.PI / 2); g.translate(0, -FLOOR_HEIGHT + lift, 0); return g;
  };
  const rect = (a: number, c: number, d: number, e: number, lift: number) => flat([[a, d], [c, d], [c, e], [a, e]], lift);
  const out: { geo: THREE.BufferGeometry; mat: string }[] = [];
  const big = new THREE.PlaneGeometry(3000000, 3000000); big.rotateX(-Math.PI / 2); big.translate(0, -FLOOR_HEIGHT - 50, 0);
  out.push({ geo: big, mat: 'field' });
  // the site's lawn
  out.push({ geo: flat([[250, 400], [355, 135], [660, 60], [730, 90], [800, 230], [1010, 420], [1150, 650], [1000, 960], [880, 960], [880, 680], [740, 540], [560, 480], [250, 400]], 30), mat: 'lawn' });
  // driveway loop and paths
  for (const [a, c, d, e] of [[300, 600, 470, 495], [575, 600, 300, 495], [330, 470, 300, 318], [600, 900, 480, 520], [255, 300, 150, 470], [330, 640, 105, 125], [640, 670, 90, 200]] as const)
    out.push({ geo: rect(a, c, d, e, 60), mat: 'paving' });
  out.push({ geo: flat([[700, 0], [790, 0], [1000, 280], [1250, 560], [1400, 640], [1400, 760], [1230, 620], [960, 330], [730, 60]], 50), mat: 'road' });
  for (const [cx, cy, r] of [[438, 290, 26], [525, 290, 14], [470, 255, 14]] as const) {
    const pts: [number, number][] = []; for (let k = 0; k < 20; k++) pts.push([cx + r * Math.cos(k / 20 * Math.PI * 2), cy + r * 0.7 * Math.sin(k / 20 * Math.PI * 2)]);
    out.push({ geo: flat(pts, 80), mat: 'sand' });
  }
  // linkways (covered walkways) and the precinct pavilion roofs
  return out;
}

/** Equirectangular sky with clouds. scale = radiance of the horizon (path tracer ~4.5, raster background ~1). */
export function skyData(night: boolean, scale: number, w = 1024, h = 512): THREE.DataTexture {
  const d = new Float32Array(w * h * 4);
  let seed = 5; const rnd = () => { seed = (seed * 16807) % 2147483647; return seed / 2147483647; };
  // value-noise lattice for clouds
  const G = 64, lat = new Float32Array(G * G); for (let i = 0; i < lat.length; i++) lat[i] = rnd();
  const vn = (x: number, y: number) => {
    const xi = Math.floor(x), yi = Math.floor(y), fx = x - xi, fy = y - yi;
    const a = lat[((yi % G + G) % G) * G + ((xi % G + G) % G)], b = lat[((yi % G + G) % G) * G + (((xi + 1) % G + G) % G)];
    const c = lat[(((yi + 1) % G + G) % G) * G + ((xi % G + G) % G)], e = lat[(((yi + 1) % G + G) % G) * G + (((xi + 1) % G + G) % G)];
    const sx2 = fx * fx * (3 - 2 * fx), sy2 = fy * fy * (3 - 2 * fy);
    return (a * (1 - sx2) + b * sx2) * (1 - sy2) + (c * (1 - sx2) + e * sx2) * sy2;
  };
  const zen = night ? [0.012, 0.016, 0.03] : [0.36, 0.52, 0.86], hor = night ? [0.03, 0.03, 0.04] : [0.92, 0.95, 1.0];
  const gnd = night ? [0.01, 0.01, 0.01] : [0.35, 0.36, 0.33];
  for (let j = 0; j < h; j++) {
    const el = (0.5 - (j + 0.5) / h) * Math.PI, s = Math.sin(el);
    for (let i = 0; i < w; i++) {
      let c: number[];
      if (s >= 0) {
        const t = Math.pow(s, 0.5); c = hor.map((v, k) => v * (1 - t) + zen[k] * t);
        if (!night && s > 0.02) {
          // clouds projected on a flat cloud layer: bigger near the horizon
          const az = (i / w) * Math.PI * 2, dist = 1 / Math.max(0.08, s);
          const px = Math.cos(az) * dist * 3, py = Math.sin(az) * dist * 3;
          let n = 0, amp = 0.5, f = 1; for (let o = 0; o < 5; o++) { n += amp * vn(px * f + 17, py * f + 9); amp *= 0.5; f *= 2.1; }
          const cov = Math.max(0, Math.min(1, (n - 0.5) * 3.2)) * Math.min(1, s * 6);
          const shade = 0.86 + 0.14 * Math.min(1, (n - 0.5) * 2);
          c = c.map((v, k) => v * (1 - cov) + [1.0, 0.99, 0.97][k] * shade * cov);
        }
      } else { const t = Math.min(1, -s * 8); c = hor.map((v, k) => v * (1 - t) + gnd[k] * t); }
      const o = (j * w + i) * 4; d[o] = c[0] * scale; d[o + 1] = c[1] * scale; d[o + 2] = c[2] * scale; d[o + 3] = 1;
    }
  }
  const t = new THREE.DataTexture(d, w, h, THREE.RGBAFormat, THREE.FloatType);
  t.mapping = THREE.EquirectangularReflectionMapping; t.minFilter = THREE.LinearFilter; t.magFilter = THREE.LinearFilter; t.needsUpdate = true;
  return t;
}

/** Distant skyline ring: low HDB-like slabs 500 m - 1.5 km away, in the haze. */
function skyline(): THREE.BufferGeometry {
  let seed = 23; const rnd = () => { seed = (seed * 16807) % 2147483647; return seed / 2147483647; };
  const gs: THREE.BufferGeometry[] = [];
  for (let k = 0; k < 90; k++) {
    const a = rnd() * Math.PI * 2, r = 500000 + rnd() * 900000;
    const w = 30000 + rnd() * 50000, d = 12000 + rnd() * 6000, hgt = (10 + Math.floor(rnd() * 16)) * STOREY + (rnd() < 0.08 ? 60000 : 0);
    const g = new THREE.BoxGeometry(w, hgt, d); g.rotateY(rnd() * Math.PI);
    g.translate(7000 + Math.cos(a) * r, -FLOOR_HEIGHT + hgt / 2, 4800 + Math.sin(a) * r); gs.push(g);
  }
  return mergeGeometries(gs);
}

export class Outdoors {
  group = new THREE.Group();
  private facade: THREE.MeshStandardMaterial;
  private estate: THREE.MeshStandardMaterial;
  private lit: { day: THREE.Texture[]; night: THREE.Texture[] };
  daySky: THREE.DataTexture | null = null;
  nightSky: THREE.DataTexture | null = null;

  constructor() {
    this.group.name = 'Outdoors';
    const tex = [facadeCanvas(false, false), facadeCanvas(true, false), facadeCanvas(false, true), facadeCanvas(true, true)].map(canvasTexture);
    this.lit = { day: [tex[0], tex[1]], night: [tex[2], tex[3]] };
    this.facade = new THREE.MeshStandardMaterial({ map: tex[0], roughness: 0.85, emissive: 0xffffff, emissiveIntensity: 0, emissiveMap: tex[2] });
    this.estate = new THREE.MeshStandardMaterial({ map: tex[1], roughness: 0.9, emissive: 0xffffff, emissiveIntensity: 0, emissiveMap: tex[3] });
    this.facade.name = 'Outdoor_Facade'; this.estate.name = 'Outdoor_Facade_Estate';
    const add = (g: THREE.BufferGeometry, m: THREE.Material | THREE.Material[]) => { const mesh = new THREE.Mesh(g, m); mesh.castShadow = false; mesh.receiveShadow = false; this.group.add(mesh); return mesh; };
    for (const b of blocks()) {
      if (b.storeys < 0) { for (const g of ownBlock()) add(g, this.facade); continue; }
      const m = b.tint ? this.estate : this.facade;
      add(blockGeometry(b), m);            // one material per mesh (the path tracer mixes up multi-material meshes); roofs sample a plain wall texel
    }
    const mats: Record<string, THREE.MeshStandardMaterial> = {
      field: new THREE.MeshStandardMaterial({ color: 0x7d8a63, roughness: 1, name: 'Outdoor_Field' }),
      lawn: new THREE.MeshStandardMaterial({ color: 0x6f8f4a, roughness: 1, name: 'Outdoor_Lawn' }),
      paving: new THREE.MeshStandardMaterial({ color: 0xc9c5bc, roughness: 0.95, name: 'Outdoor_Paving' }),
      road: new THREE.MeshStandardMaterial({ color: 0x6b6b6a, roughness: 0.95, name: 'Outdoor_Road' }),
      sand: new THREE.MeshStandardMaterial({ color: 0xc7b59a, roughness: 1, name: 'Outdoor_Playground' }),
    };
    for (const { geo, mat } of ground()) add(geo, mats[mat]);
    const t = trees();
    add(t.crowns, new THREE.MeshStandardMaterial({ color: 0x4f6e36, roughness: 0.95, flatShading: true, name: 'Outdoor_Tree_Crown' }));
    add(t.trunks, new THREE.MeshStandardMaterial({ color: 0x5b4a3a, roughness: 1, name: 'Outdoor_Tree_Trunk' }));
    add(skyline(), new THREE.MeshStandardMaterial({ color: 0xc8cdd2, roughness: 1, name: 'Outdoor_Skyline' }));
    this.group.visible = false;
  }

  /** Day or night look: lit windows at night. */
  setNight(n: boolean): void {
    this.facade.emissiveIntensity = n ? 1.4 : 0; this.estate.emissiveIntensity = n ? 1.1 : 0;
    this.facade.map = n ? this.lit.night[0] : this.lit.day[0]; this.estate.map = n ? this.lit.night[1] : this.lit.day[1];
    this.facade.needsUpdate = this.estate.needsUpdate = true;
  }

  /** Sky for the raster view (horizon about 1.0). */
  sky(night: boolean): THREE.DataTexture {
    if (night) return (this.nightSky ||= skyData(true, 1.0, 512, 256));
    return (this.daySky ||= skyData(false, 1.0));
  }
}
