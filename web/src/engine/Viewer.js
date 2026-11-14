// The 3D engine: owns the three.js scene, loads plan models, applies themes / visibility options,
// moves the camera between scenes and takes screenshots. React talks to it through the public methods below.
//
// Units: millimetres. Plan coordinates (x east, y south, z up) map to three.js as (x, z, y).
import * as THREE from 'three';
import { RoomEnvironment } from 'three/addons/environments/RoomEnvironment.js';
import { toCreasedNormals } from 'three/addons/utils/BufferGeometryUtils.js';
import { Navigator } from './navigation.js';
import { textureFor, addBoxUVs } from './textures.js';
import { THEMES, planUrl } from '../config/data.js';

const DAY_BG = 0xeae6df, NIGHT_BG = 0x14120f;
const CEILING_HEIGHT = 2600;     // camera above this = looking from above (plan views)
const MOBILE = Math.min(window.innerWidth, window.innerHeight) < 700 || /Mobi|Android|iPhone|iPad/.test(navigator.userAgent);
// warm point lights switched on for the night mood: [x, y(plan), z]
const NIGHT_LIGHT_SPOTS = [[3200, 2900, 2300], [1150, 5100, 2300], [6150, 5600, 2300], [12900, 2600, 2300], [10000, 1800, 2300],
  [7000, 1500, 2300], [5900, 8000, 2300], [2700, 7400, 2300], [9900, 6000, 2300], [12000, 6000, 2300]];

/** Decode a base64 string of little-endian int16 vertex coordinates. */
function decodePositions(b64) {
  const bin = atob(b64); const bytes = new Uint8Array(bin.length);
  for (let i = 0; i < bin.length; i++) bytes[i] = bin.charCodeAt(i);
  const q = new Int16Array(bytes.buffer); const pos = new Float32Array(q.length);
  for (let i = 0; i < q.length; i++) pos[i] = q[i];
  return pos;
}

const planCache = {};
async function fetchJson(file) {
  if (!planCache[file]) {
    const r = await fetch(planUrl(file), { cache: 'no-cache' });
    if (!r.ok) throw new Error(`HTTP ${r.status}`);
    planCache[file] = await r.json();
  }
  return planCache[file];
}

export class Viewer {
  /**
   * @param {HTMLElement} container  element the canvas is added to (the stage)
   * @param {HTMLElement} labelsEl   element that holds the room-name / dimension labels
   * @param {{ onTool?: (t: string) => void, onLoading?: (text: string|null) => void }} events
   */
  constructor(container, labelsEl, events = {}) {
    this.container = container; this.labelsEl = labelsEl;
    this.events = { onTool: () => {}, onLoading: () => {}, ...events };
    this.plan = null;            // plan data (views, modes, labels, dims, info, ...)
    this.planKey = null;
    this.hq = true;
    this.opts = { mode: 'open', fc: true, lab: false, pwr: false, ac: false, cur: true, night: false };
    this.viewTag = '';
    this.theme = 'lux'; this.ceiling = 'wave';
    this.dirty = true;
    this._setupRenderer(); this._setupScene();
    this.nav = new Navigator(this.camera, this.renderer.domElement, () => this.invalidate(), (t) => this.events.onTool(t));
    this._startLoop();
  }

  invalidate() { this.dirty = true; }

  // ---------------------------------------------------------------- setup
  _setupRenderer() {
    // preserveDrawingBuffer keeps the last frame so screenshots work in every browser (Safari clears it otherwise)
    const r = this.renderer = new THREE.WebGLRenderer({ antialias: true, logarithmicDepthBuffer: true, preserveDrawingBuffer: true });
    r.setPixelRatio(Math.min(window.devicePixelRatio, MOBILE ? 1.25 : 1.5));
    r.outputColorSpace = THREE.SRGBColorSpace;
    r.toneMapping = THREE.ACESFilmicToneMapping; r.toneMappingExposure = 1.0;
    r.shadowMap.enabled = true; r.shadowMap.type = THREE.PCFSoftShadowMap;
    r.shadowMap.autoUpdate = false;     // the model is static: recompute shadows only when something changes
    r.domElement.id = 'gl';
    this.container.prepend(r.domElement);
  }

  _setupScene() {
    const scene = this.scene = new THREE.Scene();
    try { const pm = new THREE.PMREMGenerator(this.renderer); this.envTex = pm.fromScene(new RoomEnvironment(), 0.04).texture; pm.dispose(); }
    catch (e) { this.envTex = null; }
    this.camera = new THREE.PerspectiveCamera(60, 1, 30, 400000);
    this.hemi = new THREE.HemisphereLight(0xfff6ea, 0xa89a86, 0.55); scene.add(this.hemi);
    const sun = this.sun = new THREE.DirectionalLight(0xffe9cc, 2.6);
    sun.position.set(7300 - 5500, 9000, 4800 - 9500); sun.target.position.set(7300, 0, 4800);
    scene.add(sun, sun.target);
    sun.castShadow = true; sun.shadow.mapSize.set(2048, 2048);
    Object.assign(sun.shadow.camera, { left: -11000, right: 11000, top: 11000, bottom: -11000, near: 100, far: 40000 });
    Object.assign(sun.shadow, { bias: -0.0004, normalBias: 12, radius: 3 });
    this.fill = new THREE.DirectionalLight(0xdfe8ff, 0.25); this.fill.position.set(9000, 6000, 12000); scene.add(this.fill);
    this.amb = new THREE.AmbientLight(0xffffff, 0.12); scene.add(this.amb);
    this.nightLights = NIGHT_LIGHT_SPOTS.map(([x, z, y]) => {
      const L = new THREE.PointLight(0xffc27a, 0, 5200, 1.2); L.position.set(x, y, z); L.visible = false; scene.add(L); return L;
    });
    this.root = new THREE.Group(); scene.add(this.root);           // the model, one group per layer
    this.dimGroup = new THREE.Group(); scene.add(this.dimGroup);   // dimension lines
    this.lineMat = new THREE.LineBasicMaterial({ color: 0xc0631a });
    this.layers = {}; this.materials = {}; this.emissive = [];
    this.loadedVariants = new Set(); this.activeFamily = 'lux'; this.activeCeiling = 'wave';
    this.labelEls = [];
  }

  _startLoop() {
    let lastAbove = null;
    this.renderer.setAnimationLoop((now) => {
      if (!this.plan) return;
      if (this.nav.update(now)) this.dirty = true;
      if (!this.dirty) return;                       // nothing changed: skip the frame (saves battery)
      this.dirty = false;
      const above = this.isAboveCeiling();
      if (above !== lastAbove) { lastAbove = above; this.applyVisibility(); }
      this.renderer.render(this.scene, this.camera);
      if (this.opts.lab) this._placeLabels();
    });
    this._onVisible = () => this.invalidate();
    document.addEventListener('visibilitychange', this._onVisible);
  }

  // ---------------------------------------------------------------- plans and models
  /** Load a plan ('a'..'f') and build its model. Resolves with the plan data. */
  async loadPlan(key) {
    this.events.onLoading(`Loading ${key.toUpperCase()}…`);
    let data;
    try { data = await fetchJson(key); }
    catch (e) { this.events.onLoading(`Could not load this plan (${e.message}). Please reload the page.`); throw e; }
    this.plan = data; this.planKey = key;
    this.opts.mode = data.modes.open ? 'open' : Object.keys(data.modes)[0];
    this._rebuild();
    await this._ensureVariants();
    this.events.onLoading(null);
    return data;
  }

  _rebuild() {
    this._clearModel();
    // v = 1: default furniture (swapped by other furniture families); v = 2: default false ceiling (swapped by other designs)
    for (const ch of this.plan.chunks) this._addChunk(ch, ch.v === 1 ? 'lux' : ch.v === 2 ? 'c:wave' : null);
    for (const [a, b] of this.plan.dims) {
      const g = new THREE.BufferGeometry().setFromPoints([new THREE.Vector3(a[0], 60, a[1]), new THREE.Vector3(b[0], 60, b[1])]);
      this.dimGroup.add(new THREE.Line(g, this.lineMat));
    }
    this.applyVisibility();
  }

  _clearModel() {
    this.root.traverse((o) => o.geometry && o.geometry.dispose());
    Object.values(this.materials).forEach((m) => m.dispose());
    this.root.clear(); this.dimGroup.clear();
    this.layers = {}; this.materials = {}; this.emissive = [];
    this.loadedVariants = new Set(); this.activeFamily = 'lux'; this.activeCeiling = 'wave';
  }

  _themeColour(name) { return THEMES[this.theme]?.m[name] || this.plan.mats[name].c; }

  _material(name) {
    if (this.materials[name]) return this.materials[name];
    const m = this.plan.mats[name]; const rgb = this._themeColour(name);
    const colour = new THREE.Color().setRGB(rgb[0] / 255, rgb[1] / 255, rgb[2] / 255, THREE.SRGBColorSpace);
    const glassy = m.a < 0.99;
    const shiny = /Mirror|Chrome|Glass|Screen|Hob_Black/.test(name);
    const metal = /Chrome|Steel|Gold|Brass|Silver|Metal_Black|Frame_Alum/.test(name);
    const polished = /Marble|Sintered|Quartz|Ceramic|Lacquer/.test(name);
    const roughness = shiny ? 0.08 : metal ? 0.32 : polished ? 0.28 : /Walnut|Oak|Travertine/.test(name) ? 0.6 : 0.9;
    const mat = new THREE.MeshStandardMaterial({
      color: colour, roughness, metalness: metal ? 0.75 : 0, side: THREE.DoubleSide, envMapIntensity: 0.8,
      transparent: glassy, opacity: glassy ? Math.max(0.16, m.a * 0.7) : 1, depthWrite: !glassy,
    });
    if (this.hq) { const tx = textureFor(name); if (tx) mat.map = tx[0]; }
    if (m.e) { mat.emissive = colour.clone(); mat.emissiveIntensity = 0.35; this.emissive.push(mat); }
    this.materials[name] = mat;
    return mat;
  }

  /** @param chunk {layer, mat, b64}  @param variant tag of a swappable group ('lux', 'japandi', 'c:wave', ...) or null */
  _addChunk(chunk, variant) {
    let g = new THREE.BufferGeometry();
    g.setAttribute('position', new THREE.BufferAttribute(decodePositions(chunk.b64), 3));
    try { g = toCreasedNormals(g, Math.PI / 5); } catch (e) { g.computeVertexNormals(); }
    const tx = this.hq ? textureFor(chunk.mat) : null; if (tx) addBoxUVs(g, tx[1]);
    const info = this.plan.mats[chunk.mat];
    const mesh = new THREE.Mesh(g, this._material(chunk.mat));
    if (info.a < 0.99) { mesh.renderOrder = 2; mesh.castShadow = false; } else mesh.castShadow = this.hq;
    mesh.receiveShadow = this.hq && !info.e;
    if (variant) { mesh.userData.variant = variant; mesh.visible = this._variantVisible(variant); }
    if (!this.layers[chunk.layer]) { const grp = new THREE.Group(); grp.name = chunk.layer; this.layers[chunk.layer] = grp; this.root.add(grp); }
    this.layers[chunk.layer].add(mesh);
  }

  // ---------------------------------------------------------------- themes, furniture families, ceilings
  /** Furniture family the current theme uses (falls back to the default if this plan lacks it). */
  family() { const f = THEMES[this.theme]?.fam || 'lux'; return this.plan?.families?.includes(f) ? f : 'lux'; }
  /** Ceiling design in use (falls back to the default if this plan lacks it). */
  ceilingDesign() { return this.plan?.ceils?.includes(this.ceiling) ? this.ceiling : 'wave'; }
  _variantVisible(tag) { return tag.startsWith('c:') ? tag === 'c:' + this.activeCeiling : tag === this.activeFamily; }

  setTheme(key) {
    this.theme = key;
    if (!this.plan) return;
    for (const [name, mat] of Object.entries(this.materials)) {
      if (!this.plan.mats[name]) continue;
      const c = this._themeColour(name);
      mat.color.setRGB(c[0] / 255, c[1] / 255, c[2] / 255, THREE.SRGBColorSpace);
      if (this.plan.mats[name].e) mat.emissive.copy(mat.color);
    }
    this.invalidate(); this._ensureVariants();
  }

  setCeiling(key) { this.ceiling = key; if (this.plan) this._ensureVariants(); }

  /** Load (once) and show the furniture family and ceiling design that the current choices need. */
  async _ensureVariants() {
    const key = this.planKey, fam = this.family(), ceil = this.ceilingDesign();
    if (fam !== 'lux' && !(await this._loadVariant(fam, fam))) return;
    if (ceil !== 'wave' && !(await this._loadVariant('ceil_' + ceil, 'c:' + ceil))) return;
    if (this.planKey !== key || fam !== this.family() || ceil !== this.ceilingDesign()) return;   // changed meanwhile
    this.activeFamily = fam; this.activeCeiling = ceil;
    this.root.traverse((o) => { if (o.userData.variant) o.visible = this._variantVisible(o.userData.variant); });
    this.renderer.shadowMap.needsUpdate = true; this.invalidate();
  }

  async _loadVariant(file, tag) {
    if (this.loadedVariants.has(tag)) return true;
    const key = this.planKey; let data;
    this.events.onLoading('Loading…');
    try { data = await fetchJson(`${key}.${file}`); } catch (e) { this.events.onLoading(null); return false; }
    this.events.onLoading(null);
    if (this.planKey !== key) return false;
    if (!this.loadedVariants.has(tag)) {
      for (const k in data.mats) if (!this.plan.mats[k]) this.plan.mats[k] = data.mats[k];
      this.loadedVariants.add(tag);
      for (const ch of data.chunks) this._addChunk(ch, tag);
    }
    return true;
  }

  /** High-quality rendering (textures, shadows, reflections). Rebuilds the model. */
  setHQ(on) { this.hq = on; if (this.plan) { this._rebuild(); this._ensureVariants(); } }

  // ---------------------------------------------------------------- visibility and lighting
  /** @param {Partial<{mode, fc, lab, pwr, ac, cur, night}>} opts */
  setOptions(opts) { Object.assign(this.opts, opts); this.applyVisibility(); }

  isAboveCeiling() { return this.camera.position.y > CEILING_HEIGHT; }

  applyVisibility() {
    if (!this.plan) return;
    const o = this.opts, tag = this.viewTag;
    const planLike = tag === 'top' || tag === 'plan' || tag === 'services';
    const hide = new Set(['Beams_Highlight', 'Structural_Highlight', ...(this.plan.modes[o.mode]?.hide || [])]);
    if (planLike || this.isAboveCeiling()) hide.add('Ceiling');
    if (!o.fc || planLike) { hide.add('False_Ceiling'); hide.add('Lighting'); }
    if (!o.pwr) hide.add('Power_Points');
    if (!o.ac) hide.add('Aircon_Trunking');
    if (!o.cur || tag === 'plan') hide.add('Curtains');
    for (const [name, grp] of Object.entries(this.layers)) grp.visible = !hide.has(name);
    this.dimGroup.visible = o.lab;

    const n = o.night, hq = this.hq;
    this.scene.background = new THREE.Color(n ? NIGHT_BG : DAY_BG);
    this.scene.environment = hq ? this.envTex : null;
    this.hemi.intensity = n ? 0.04 : hq ? 0.55 : 1.1;
    this.sun.intensity = n ? 0 : hq ? 2.6 : 1.4; this.sun.castShadow = hq;
    this.fill.intensity = n ? 0.02 : 0.25;
    this.amb.intensity = n ? 0.04 : hq ? 0.12 : 0.3;
    for (const L of this.nightLights) { L.intensity = n ? 0.9 : 0; L.visible = n; }
    for (const m of Object.values(this.materials)) m.envMapIntensity = n ? 0.08 : 0.8;
    for (const m of this.emissive) m.emissiveIntensity = n ? 2.4 : 0.35;
    this.renderer.toneMappingExposure = n ? 1.25 : 1.0;
    this.renderer.shadowMap.needsUpdate = true;
    this._buildLabels();
    this.invalidate();
  }

  // ---------------------------------------------------------------- labels
  _buildLabels() {
    this.labelsEl.innerHTML = ''; this.labelEls = [];
    if (!this.opts.lab || !this.plan) return;
    const add = (text, cls, p) => {
      const e = document.createElement('div'); e.className = cls; e.textContent = text;
      this.labelsEl.appendChild(e); this.labelEls.push([e, p]);
    };
    for (const [t, x, y] of this.plan.labels) add(t, 'lbl', new THREE.Vector3(x, 150, y));
    for (const [a, b, t] of this.plan.dims) add(t + ' mm', 'lbl dim', new THREE.Vector3((a[0] + b[0]) / 2, 80, (a[1] + b[1]) / 2));
  }
  _placeLabels() {
    const w = this.container.clientWidth, h = this.container.clientHeight, p = new THREE.Vector3();
    for (const [e, pos] of this.labelEls) {
      p.copy(pos).project(this.camera);
      const vis = p.z < 1 && Math.abs(p.x) < 1.1 && Math.abs(p.y) < 1.1;
      e.style.display = vis ? '' : 'none';
      if (vis) { e.style.left = ((p.x + 1) / 2 * w) + 'px'; e.style.top = ((1 - p.y) / 2 * h) + 'px'; }
    }
  }

  // ---------------------------------------------------------------- camera
  _fovFor(view) {
    const aspect = this.container.clientWidth / Math.max(1, this.container.clientHeight);
    let vf = Math.min(view.fov * 0.78, 78);
    if (aspect < 1) {   // portrait screens: keep the horizontal field of view
      const hf = Math.min(view.fov, 95) * Math.PI / 180;
      vf = Math.min(100, 2 * Math.atan(Math.tan(hf / 2) / aspect) * 180 / Math.PI);
    }
    return vf;
  }

  /** Move the camera to a scene. Plan views look straight down from high above. */
  showView(view, { instant = false } = {}) {
    this.viewTag = view.tag || '';
    const eye = new THREE.Vector3(view.eye[0], view.eye[2], view.eye[1]);
    const target = new THREE.Vector3(view.target[0], view.target[2], view.target[1]);
    if (view.tag === 'plan') eye.set(view.target[0], 80000, view.target[1] + 1);
    this.camera.up.set(0, 1, 0);
    this.currentView = view;
    this.nav.flyTo(eye, target, this._fovFor(view), instant ? 0 : 900, () => {
      this.nav.controls.update();
      // walk-around scenes start in look mode, overviews in orbit mode
      this.nav.setTool(view.eye[2] < 5000 && view.tag !== 'plan' ? 'look' : 'orbit', true);
      this.applyVisibility();
    });
    this.applyVisibility();
  }

  setTool(tool) { this.nav.setTool(tool); }
  zoomExtents() { this.nav.zoomExtents(new THREE.Box3().setFromObject(this.root)); this.applyVisibility(); }

  resize() {
    const w = this.container.clientWidth, h = this.container.clientHeight;
    if (!w || !h) return;
    this.renderer.setSize(w, h, false);
    this.camera.aspect = w / h;
    if (this.currentView) this.camera.fov = this._fovFor(this.currentView);
    this.camera.updateProjectionMatrix(); this.invalidate();
  }

  // ---------------------------------------------------------------- screenshots
  /** Copy the canvas into a 2D canvas; reports whether the frame looks blank (all one colour). */
  _grab() {
    const src = this.renderer.domElement;
    const cv = document.createElement('canvas'); cv.width = src.width; cv.height = src.height;
    const cx = cv.getContext('2d');
    cx.fillStyle = '#eae6df'; cx.fillRect(0, 0, cv.width, cv.height); cx.drawImage(src, 0, 0);
    const d = cx.getImageData(0, 0, cv.width, cv.height).data;
    const step = Math.max(4, Math.floor(d.length / 4 / 400)) * 4;
    let lo = 765, hi = 0;
    for (let i = 0; i < d.length; i += step) { const v = d[i] + d[i + 1] + d[i + 2]; lo = Math.min(lo, v); hi = Math.max(hi, v); }
    return { canvas: cv, blank: hi - lo < 12 };
  }

  /** Screenshot of the current view as a data URL ('image/png' or 'image/jpeg'). */
  async capture(type = 'image/png') {
    const nextFrame = () => new Promise((r) => requestAnimationFrame(() => r()));
    let shot = null;
    for (let attempt = 0; attempt < 4; attempt++) {
      this.renderer.render(this.scene, this.camera); shot = this._grab(); if (!shot.blank) break;   // Chrome / Firefox
      this.invalidate(); await nextFrame(); await nextFrame(); shot = this._grab(); if (!shot.blank) break;   // Safari
    }
    return type === 'image/jpeg' ? shot.canvas.toDataURL('image/jpeg', 0.92) : shot.canvas.toDataURL('image/png');
  }

  dispose() {
    this.renderer.setAnimationLoop(null);
    document.removeEventListener('visibilitychange', this._onVisible);
    this.nav.dispose(); this._clearModel(); this.renderer.dispose(); this.renderer.domElement.remove();
  }
}
