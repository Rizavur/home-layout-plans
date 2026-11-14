// Procedural textures drawn on canvases: subtle tile joints, marble veins, wood grain and fabric noise.
// The colour still comes from the material; a texture only adds pattern on top (white = no change).
import * as THREE from 'three';

function canvas(n) {
  const c = document.createElement('canvas');
  c.width = c.height = n;
  return [c, c.getContext('2d')];
}

// small deterministic random generator so textures look the same on every load
function random(seed) {
  let s = seed;
  return () => { s = (s * 16807) % 2147483647; return (s - 1) / 2147483646; };
}

function tiles(n, cols, rows, grout, base) {
  const [c, g] = canvas(n); const r = random(7);
  g.fillStyle = base; g.fillRect(0, 0, n, n);
  for (let i = 0; i < 2600; i++) { g.fillStyle = `rgba(0,0,0,${r() * 0.025})`; g.fillRect(r() * n, r() * n, 2 + r() * 6, 2 + r() * 6); }
  g.strokeStyle = grout; g.lineWidth = Math.max(1.5, n / 400);
  for (let i = 0; i <= cols; i++) { g.beginPath(); g.moveTo(i * n / cols, 0); g.lineTo(i * n / cols, n); g.stroke(); }
  for (let j = 0; j <= rows; j++) { g.beginPath(); g.moveTo(0, j * n / rows); g.lineTo(n, j * n / rows); g.stroke(); }
  return c;
}

function marble(n, vein, seed) {
  const [c, g] = canvas(n); const r = random(seed);
  g.fillStyle = '#ffffff'; g.fillRect(0, 0, n, n);
  for (let k = 0; k < 14; k++) {
    g.strokeStyle = vein.replace('A', (0.05 + r() * 0.16).toFixed(3)); g.lineWidth = 0.6 + r() * 2.4; g.beginPath();
    let x = r() * n, y = 0; g.moveTo(x, y);
    while (y < n) { x += (r() - 0.45) * 40; y += 10 + r() * 30; g.lineTo(x, y); }
    g.stroke();
  }
  return c;
}

function grain(n, dark, seed) {
  const [c, g] = canvas(n); const r = random(seed);
  g.fillStyle = '#ffffff'; g.fillRect(0, 0, n, n);
  for (let i = 0; i < 260; i++) {
    const y = r() * n;
    g.strokeStyle = `rgba(${dark},${(0.04 + r() * 0.12).toFixed(3)})`; g.lineWidth = 0.5 + r() * 2.5; g.beginPath(); g.moveTo(0, y);
    for (let x = 0; x <= n; x += 32) g.lineTo(x, y + Math.sin(x / 70 + i) * 3 + (r() - 0.5) * 2);
    g.stroke();
  }
  return c;
}

function noise(n, amount, seed, blob) {
  const [c, g] = canvas(n); const r = random(seed);
  g.fillStyle = '#ffffff'; g.fillRect(0, 0, n, n);
  for (let i = 0; i < n * n / (blob * blob) * 2.2; i++) {
    g.fillStyle = `rgba(0,0,0,${(r() * amount).toFixed(3)})`; g.beginPath(); g.arc(r() * n, r() * n, blob * (0.4 + r()), 0, 7); g.fill();
  }
  return c;
}

// material-name pattern -> [draw function, size of one texture repeat in mm]
const RULES = [
  [/^Floor_Homogeneous/, () => tiles(1024, 2, 2, 'rgba(120,112,100,.55)', '#ffffff'), 1200],
  [/^Floor_Kitchen/, () => tiles(1024, 2, 2, 'rgba(110,104,96,.6)', '#ffffff'), 1200],
  [/^Floor_Yard|^Floor_Toilet/, () => tiles(1024, 4, 2, 'rgba(90,90,90,.55)', '#ffffff'), 1200],
  [/^Wall_Toilet|^Wall_Kitchen/, () => tiles(1024, 4, 2, 'rgba(120,120,120,.45)', '#ffffff'), 1200],
  [/Marble|Art_Marble/, () => marble(1024, 'rgba(90,92,100,A)', 11), 1600],
  [/Sintered/, () => marble(1024, 'rgba(60,60,64,A)', 23), 1400],
  [/Walnut|Oak/, () => grain(1024, '40,22,10', 5), 900],
  [/Travertine/, () => grain(1024, '120,90,50', 9), 1200],
  [/Rug|Throw/, () => noise(512, 0.10, 3, 3), 400],
  [/Sofa|Boucle|Cushion|Headboard|Duvet|Linen|Pillow|Velvet|Curtain|Felt|Leather/, () => noise(512, 0.07, 4, 2), 300],
];

const cache = {};

/** Texture for a material name, or null. Returns [THREE.Texture, mm per repeat]. */
export function textureFor(name) {
  if (name in cache) return cache[name];
  let result = null;
  for (const [re, draw, mm] of RULES) {
    if (!re.test(name)) continue;
    const t = new THREE.CanvasTexture(draw());
    t.wrapS = t.wrapT = THREE.RepeatWrapping; t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = 8;
    result = [t, mm];
    break;
  }
  cache[name] = result;
  return result;
}

/** Box-project UVs onto a triangle soup: each triangle uses the plane its normal faces most. */
export function addBoxUVs(geometry, mm) {
  const p = geometry.attributes.position.array;
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
