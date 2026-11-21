// The 3D engine: owns the three.js scene, loads plan models, applies themes / visibility options,
// moves the camera between scenes and takes screenshots. React talks to it through the public methods below.
//
// Units: millimetres. Plan coordinates (x east, y south, z up) map to three.js as (x, z, y).
import * as THREE from 'three';
import { toCreasedNormals } from 'three/addons/utils/BufferGeometryUtils.js';
import { EffectComposer } from 'three/addons/postprocessing/EffectComposer.js';
import { RenderPass } from 'three/addons/postprocessing/RenderPass.js';
import { GTAOPass } from 'three/addons/postprocessing/GTAOPass.js';
import { OutputPass } from 'three/addons/postprocessing/OutputPass.js';
import { PhotoRenderer } from './photo';
import { Navigator } from './navigation';
import { textureFor, addBoxUVs, setTextureLoadCallback } from './textures';
import { TapeMeasure } from './tape';
import { THEMES, planUrl } from '../config/data';
import type { Chunk, PlanData, Tool, VariantData, View, ViewOptions, ViewTag } from '../types';

const DAY_BG = 0xeae6df, NIGHT_BG = 0x14120f;
const CEILING_HEIGHT = 2600;     // camera above this = looking from above (plan views)
const MOBILE = Math.min(window.innerWidth, window.innerHeight) < 700 || /Mobi|Android|iPhone|iPad/.test(navigator.userAgent);
// warm point lights switched on for the night mood: [x, y(plan), z]
const NIGHT_LIGHT_SPOTS: [number, number, number][] = [[3200, 2900, 2300], [1150, 5100, 2300], [6150, 5600, 2300], [12900, 2600, 2300], [10000, 1800, 2300],
  [7000, 1500, 2300], [5900, 8000, 2300], [2700, 7400, 2300], [9900, 6000, 2300], [12000, 6000, 2300]];

/**
 * Soft light of a bright room, as an equirectangular map: warm white above, brighter band at window height,
 * and a light floor below - so ceilings and the undersides of things get bounce light like in a real room.
 */
function interiorEnvironment(): THREE.DataTexture {
  const w = 128, h = 64, d = new Float32Array(w * h * 4);
  for (let j = 0; j < h; j++) {
    const s = Math.sin((0.5 - (j + 0.5) / h) * Math.PI);                 // +1 straight up, -1 straight down
    const window = Math.exp(-Math.pow((s - 0.15) / 0.28, 2)) * 0.35;       // daylight from the windows
    const up = [0.56, 0.545, 0.525], down = [0.47, 0.445, 0.41];
    for (let i = 0; i < w; i++) {
      const side = 0.85 + 0.15 * Math.cos((i / w) * Math.PI * 2);          // one side of the room a bit brighter
      const o = (j * w + i) * 4, base = s >= 0 ? up : down;
      d[o] = (base[0] + window * 1.0) * side; d[o + 1] = (base[1] + window * 1.0) * side; d[o + 2] = (base[2] + window * 1.05) * side; d[o + 3] = 1;
    }
  }
  const t = new THREE.DataTexture(d, w, h, THREE.RGBAFormat, THREE.FloatType);
  t.mapping = THREE.EquirectangularReflectionMapping; t.needsUpdate = true;
  return t;
}

/** Decode a base64 string of little-endian int16 vertex coordinates. */
function decodePositions(b64: string): Float32Array {
  const bin = atob(b64); const bytes = new Uint8Array(bin.length);
  for (let i = 0; i < bin.length; i++) bytes[i] = bin.charCodeAt(i);
  const q = new Int16Array(bytes.buffer); const pos = new Float32Array(q.length);
  for (let i = 0; i < q.length; i++) pos[i] = q[i];
  return pos;
}

const planCache: Record<string, unknown> = {};
async function fetchJson<T>(file: string): Promise<T> {
  if (!planCache[file]) {
    const r = await fetch(planUrl(file), { cache: 'no-cache' });
    if (!r.ok) throw new Error(`HTTP ${r.status}`);
    planCache[file] = await r.json();
  }
  return planCache[file] as T;
}

export interface ViewerEvents {
  /** the active navigation tool changed */
  onTool: (tool: Tool) => void;
  /** show a loading message, or null to hide it */
  onLoading: (text: string | null) => void;
  /** photo (path tracing) progress: samples so far, or null when it stopped */
  onPhoto: (samples: number | null, target: number) => void;
}

export class Viewer {
  container: HTMLElement;
  labelsEl: HTMLElement;
  events: ViewerEvents;
  /** the open plan (views, modes, labels, dims, info, ...) */
  plan: PlanData | null = null;
  planKey: string | null = null;
  /** realistic rendering: textures, soft shadows, ambient occlusion, reflections (off = light mode for older devices) */
  hq = true;
  /** the running photo (path tracing), if any */
  photo: PhotoRenderer | null = null;
  private composer: EffectComposer | null = null;
  /** time of the last camera movement; ambient occlusion is added once the view has been still for a moment */
  private lastMove = 0;
  private aoDone = false;
  opts: ViewOptions = { mode: 'open', fc: true, lab: false, pwr: false, ac: false, cur: true, night: false, wood: false };
  viewTag: ViewTag = '';
  currentView: View | null = null;
  theme = 'lux';
  ceiling = 'wave';
  dirty = true;
  // three.js objects (created in _setupRenderer / _setupScene)
  renderer!: THREE.WebGLRenderer;
  scene!: THREE.Scene;
  camera!: THREE.PerspectiveCamera;
  envTex: THREE.Texture | null = null;
  hemi!: THREE.HemisphereLight;
  sun!: THREE.DirectionalLight;
  fill!: THREE.DirectionalLight;
  amb!: THREE.AmbientLight;
  nightLights: THREE.PointLight[] = [];
  root!: THREE.Group;
  dimGroup!: THREE.Group;
  lineMat!: THREE.LineBasicMaterial;
  layers: Record<string, THREE.Group> = {};
  materials: Record<string, THREE.MeshStandardMaterial> = {};
  emissive: THREE.MeshStandardMaterial[] = [];
  loadedVariants = new Set<string>();
  activeFamily = 'lux';
  activeCeiling = 'wave';
  labelEls: [HTMLElement, THREE.Vector3][] = [];
  nav: Navigator;
  tape: TapeMeasure;
  tapeLayer: HTMLElement;
  private _onVisible = (): void => this.invalidate();

  /**
   * @param container  element the canvas is added to (the stage)
   * @param labelsEl   element that holds the room-name / dimension labels
   */
  constructor(container: HTMLElement, labelsEl: HTMLElement, events: Partial<ViewerEvents> = {}) {
    this.container = container; this.labelsEl = labelsEl;
    this.events = { onTool: () => {}, onLoading: () => {}, onPhoto: () => {}, ...events };
    setTextureLoadCallback(() => { this.aoDone = false; this.invalidate(); });
    this._setupRenderer(); this._setupScene();
    this.nav = new Navigator(this.camera, this.renderer.domElement, () => this.invalidate(), (t) => { this.tape?.setActive(t === 'tape'); this.events.onTool(t); });
    this.tapeLayer = document.createElement('div'); this.tapeLayer.className = 'tape-labels'; this.container.appendChild(this.tapeLayer);
    this.tape = new TapeMeasure(this.scene, this.camera, this.renderer.domElement, this.root, this.tapeLayer, () => this.invalidate());
    this._startLoop();
  }

  invalidate(): void { this.dirty = true; }

  // ---------------------------------------------------------------- setup
  private _setupRenderer(): void {
    // preserveDrawingBuffer keeps the last frame so screenshots work in every browser (Safari clears it otherwise)
    const r = this.renderer = new THREE.WebGLRenderer({ antialias: true, preserveDrawingBuffer: true });
    r.setPixelRatio(Math.min(window.devicePixelRatio, MOBILE ? 1.25 : 1.5));
    r.outputColorSpace = THREE.SRGBColorSpace;
    r.toneMapping = THREE.ACESFilmicToneMapping; r.toneMappingExposure = 1.0;
    r.shadowMap.enabled = true; r.shadowMap.type = THREE.PCFSoftShadowMap;
    r.shadowMap.autoUpdate = false;     // the model is static: recompute shadows only when something changes
    r.domElement.id = 'gl';
    this.container.prepend(r.domElement);
  }

  private _setupScene(): void {
    const scene = this.scene = new THREE.Scene();
    try { const pm = new THREE.PMREMGenerator(this.renderer); const eq = interiorEnvironment(); this.envTex = pm.fromEquirectangular(eq).texture; eq.dispose(); pm.dispose(); }
    catch { this.envTex = null; }
    this.camera = new THREE.PerspectiveCamera(60, 1, 30, 400000);
    this.hemi = new THREE.HemisphereLight(0xfff6ea, 0xa89a86, 0.55); scene.add(this.hemi);
    const sun = this.sun = new THREE.DirectionalLight(0xffe9cc, 2.6);
    sun.position.set(7300 - 5500, 9000, 4800 - 9500); sun.target.position.set(7300, 0, 4800);
    scene.add(sun, sun.target);
    sun.castShadow = true; sun.shadow.mapSize.set(MOBILE ? 2048 : 4096, MOBILE ? 2048 : 4096);
    Object.assign(sun.shadow.camera, { left: -11000, right: 11000, top: 11000, bottom: -11000, near: 100, far: 40000 });
    Object.assign(sun.shadow, { bias: -0.0003, normalBias: 10, radius: 3 });
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

  private _startLoop(): void {
    let lastAbove: boolean | null = null;
    this.renderer.setAnimationLoop((now) => {
      if (!this.plan) return;
      const moved = this.nav.update(now);
      if (this.photo) {                               // photo mode: every frame goes to the path tracer
        if (moved) { this.stopPhoto(); return; }
        if (this.photo.tick()) this.events.onPhoto(this.photo.samples, this.photo.target);
        else if (this.photo.samples >= this.photo.target) this.events.onPhoto(this.photo.target, this.photo.target);
        return;
      }
      if (moved) { this.dirty = true; this.lastMove = now; this.aoDone = false; }
      // realistic mode: once the camera has been still for a moment, redraw once with ambient occlusion
      const wantAO = this.hq && !this.aoDone && now - this.lastMove > 180;
      if (!this.dirty && !wantAO) return;             // nothing changed: skip the frame (saves battery)
      this.dirty = false;
      const above = this.isAboveCeiling();
      if (above !== lastAbove) { lastAbove = above; this.applyVisibility(); }
      this._updateClipping();
      if (wantAO) { this._renderFinal(); this.aoDone = true; }
      else { this.renderer.render(this.scene, this.camera); if (!this.hq) this.aoDone = true; }
      if (this.opts.lab) this._placeLabels();
      this.tape.place(this.container.clientWidth, this.container.clientHeight);
    });
    document.addEventListener('visibilitychange', this._onVisible);
  }

  /** Near/far planes that follow the camera height: tight indoors (sharp depth for ambient occlusion), wide for overviews. */
  private _updateClipping(): void {
    const y = Math.abs(this.camera.position.y);
    const near = y < 4000 ? 20 : Math.min(2000, y * 0.01), far = y < 4000 ? 60000 : Math.max(60000, y * 5);
    if (near !== this.camera.near || far !== this.camera.far) { this.camera.near = near; this.camera.far = far; this.camera.updateProjectionMatrix(); }
  }

  /** The finished frame: ambient occlusion in realistic mode when looking at rooms, a plain render otherwise. */
  private _renderFinal(): void {
    if (!this.hq || this.isAboveCeiling() || MOBILE) { this.renderer.render(this.scene, this.camera); return; }
    if (!this.composer) {
      const w = this.container.clientWidth || 800, h = this.container.clientHeight || 600;
      const rt = new THREE.WebGLRenderTarget(w, h, { type: THREE.HalfFloatType, samples: 4 });
      const c = this.composer = new EffectComposer(this.renderer, rt);
      c.setPixelRatio(this.renderer.getPixelRatio()); c.setSize(w, h);
      c.addPass(new RenderPass(this.scene, this.camera));
      const ao = new GTAOPass(this.scene, this.camera, w, h);
      ao.updateGtaoMaterial({ radius: 420, distanceExponent: 1.6, thickness: 260, scale: 1.0, samples: 16 });
      ao.updatePdMaterial({ lumaPhi: 10, depthPhi: 2, normalPhi: 3, radius: 6, rings: 2, samples: 16 });
      ao.blendIntensity = 0.85;
      c.addPass(ao); c.addPass(new OutputPass());
    }
    this.composer.render();
  }

  // ---------------------------------------------------------------- photo (path tracing)
  /** Start path tracing the current view. Progress is reported through events.onPhoto. */
  async startPhoto(): Promise<void> {
    if (this.photo || !this.plan) return;
    this.nav.flyTo(this.camera.position.clone(), this.nav.controls.target.clone(), this.camera.fov, 0, () => {});   // stop any glide
    const p = new PhotoRenderer(this.renderer, this.scene, this.camera, { hemi: this.hemi, amb: this.amb, fill: this.fill }, this.opts.night, MOBILE);
    this.events.onLoading('Preparing the photo…');
    await new Promise((r) => setTimeout(r, 60));          // let the message paint before the heavy setup
    try { await p.start(); }
    catch (e) { p.stop(); this.events.onLoading(null); this.events.onPhoto(null, 0); this.invalidate(); throw e; }
    this.events.onLoading(null);
    this.photo = p; this.events.onPhoto(0, p.target);
  }

  /** Stop path tracing and go back to the normal view. */
  stopPhoto(): void {
    if (!this.photo) return;
    this.photo.stop(); this.photo = null; this.aoDone = false;
    this.renderer.shadowMap.needsUpdate = true; this.events.onPhoto(null, 0); this.invalidate();
  }

  // ---------------------------------------------------------------- plans and models
  /** Load a plan ('a'..'f') and build its model. Resolves with the plan data. */
  async loadPlan(key: string): Promise<PlanData> {
    this.events.onLoading(`Loading ${key.toUpperCase()}…`);
    let data: PlanData;
    try { data = await fetchJson<PlanData>(key); }
    catch (e) { this.events.onLoading(`Could not load this plan (${(e as Error).message}). Please reload the page.`); throw e; }
    this.plan = data; this.planKey = key; this.tape?.clear();
    this.opts.mode = data.modes.open ? 'open' : Object.keys(data.modes)[0];
    this._rebuild();
    await this._ensureVariants();
    this.events.onLoading(null);
    return data;
  }

  private _rebuild(): void {
    const plan = this.plan!;
    this._clearModel();
    // v = 1: default furniture (swapped by other furniture families); v = 2: default false ceiling (swapped by other designs)
    for (const ch of plan.chunks) this._addChunk(ch, ch.v === 1 ? 'lux' : ch.v === 2 ? 'c:wave' : null);
    for (const [a, b] of plan.dims) {
      const g = new THREE.BufferGeometry().setFromPoints([new THREE.Vector3(a[0], 60, a[1]), new THREE.Vector3(b[0], 60, b[1])]);
      this.dimGroup.add(new THREE.Line(g, this.lineMat));
    }
    this.applyVisibility();
  }

  private _clearModel(): void {
    this.root.traverse((o) => { if ((o as THREE.Mesh).geometry) (o as THREE.Mesh).geometry.dispose(); });
    Object.values(this.materials).forEach((m) => m.dispose());
    this.root.clear(); this.dimGroup.clear();
    this.layers = {}; this.materials = {}; this.emissive = [];
    this.loadedVariants = new Set(); this.activeFamily = 'lux'; this.activeCeiling = 'wave';
  }

  private _themeColour(name: string): [number, number, number] { return THEMES[this.theme]?.m[name] || this.plan!.mats[name].c; }

  /** Set a material's colour from the theme, brightened by its texture's gain so patterns don't darken the colour. */
  private _applyColour(mat: THREE.MeshStandardMaterial, name: string): void {
    const c = this._themeColour(name), g = (mat.userData.gain as number) || 1;
    mat.color.setRGB(c[0] / 255, c[1] / 255, c[2] / 255, THREE.SRGBColorSpace).multiplyScalar(g);
  }

  private _material(name: string): THREE.MeshStandardMaterial {
    if (this.materials[name]) return this.materials[name];
    const m = this.plan!.mats[name]; const rgb = this._themeColour(name);
    const colour = new THREE.Color().setRGB(rgb[0] / 255, rgb[1] / 255, rgb[2] / 255, THREE.SRGBColorSpace);
    const glassy = m.a < 0.99;
    const shiny = /Mirror|Chrome|Glass|Screen|Hob_Black/.test(name);
    const metal = /Chrome|Steel|Gold|Brass|Silver|Metal_Black|Frame_Alum/.test(name);
    const polished = /Marble|Sintered|Quartz|Ceramic|Lacquer/.test(name);
    const lacquer = /Lacquer|Joinery|Lux_Charcoal|Lux_Greige|Door_Matt|Appliance|Fridge/.test(name);
    let roughness = shiny ? 0.06 : metal ? 0.3 : polished ? 0.25 : lacquer ? 0.55 : /Walnut|Oak|Travertine/.test(name) ? 0.6 : 0.9;
    const frosted = /Fluted|Frosted|Opal/.test(name);
    const mat = new THREE.MeshStandardMaterial({
      color: colour, roughness, metalness: metal ? 0.8 : 0, side: THREE.DoubleSide, envMapIntensity: 0.9,
      transparent: glassy, opacity: glassy ? (frosted ? 0.82 : Math.max(0.12, m.a * 0.55)) : 1, depthWrite: !glassy,
    });
    mat.name = name;
    if (frosted) { mat.roughness = 0.4; mat.emissive = colour.clone(); mat.emissiveIntensity = 0.22; }   // frosted glass glows with the light passing through it
    if (this.hq) {
      const tx = textureFor(name);
      if (tx) {
        mat.map = tx.map; mat.userData.gain = tx.gain; roughness = tx.rough; mat.roughness = roughness;
        if (tx.normalMap) { mat.normalMap = tx.normalMap; mat.normalScale.set(tx.normalScale, tx.normalScale); }
        this._applyColour(mat, name);
      }
    }
    if (m.e) { mat.emissive = colour.clone(); mat.emissiveIntensity = 0.35; this.emissive.push(mat); }
    this.materials[name] = mat;
    return mat;
  }

  /** @param variant  tag of a swappable group ('lux', 'japandi', 'c:wave', ...) or null */
  private _addChunk(chunk: Chunk, variant: string | null): void {
    let g = new THREE.BufferGeometry();
    g.setAttribute('position', new THREE.BufferAttribute(decodePositions(chunk.b64), 3));
    try { g = toCreasedNormals(g, Math.PI / 5); } catch { g.computeVertexNormals(); }
    const tx = this.hq ? textureFor(chunk.mat) : null; if (tx) addBoxUVs(g, tx.mm);
    const info = this.plan!.mats[chunk.mat];
    const mesh = new THREE.Mesh(g, this._material(chunk.mat));
    if (info.a < 0.99) { mesh.renderOrder = 2; mesh.castShadow = false; } else mesh.castShadow = this.hq;
    mesh.receiveShadow = this.hq && !info.e;
    if (variant) { mesh.userData.variant = variant; mesh.visible = this._variantVisible(variant); }
    if (!this.layers[chunk.layer]) { const grp = new THREE.Group(); grp.name = chunk.layer; this.layers[chunk.layer] = grp; this.root.add(grp); }
    this.layers[chunk.layer].add(mesh);
  }

  // ---------------------------------------------------------------- themes, furniture families, ceilings
  /** Furniture family the current theme uses (falls back to the default if this plan lacks it). */
  family(): string { const f = THEMES[this.theme]?.fam || 'lux'; return this.plan?.families?.includes(f) ? f : 'lux'; }
  /** Ceiling design in use (falls back to the default if this plan lacks it). */
  ceilingDesign(): string { return this.plan?.ceils?.includes(this.ceiling) ? this.ceiling : 'wave'; }
  private _variantVisible(tag: string): boolean { return tag.startsWith('c:') ? tag === 'c:' + this.activeCeiling : tag === this.activeFamily; }

  setTheme(key: string): void {
    this.theme = key;
    const plan = this.plan; if (!plan) return;
    for (const [name, mat] of Object.entries(this.materials)) {
      if (!plan.mats[name]) continue;
      this._applyColour(mat, name);
      if (plan.mats[name].e) { const c = this._themeColour(name); mat.emissive.setRGB(c[0] / 255, c[1] / 255, c[2] / 255, THREE.SRGBColorSpace); }
    }
    this.invalidate(); void this._ensureVariants();
  }

  setCeiling(key: string): void { this.ceiling = key; if (this.plan) void this._ensureVariants(); }

  /** Load (once) and show the furniture family and ceiling design that the current choices need. */
  private async _ensureVariants(): Promise<void> {
    const key = this.planKey, fam = this.family(), ceil = this.ceilingDesign();
    if (fam !== 'lux' && !(await this._loadVariant(fam, fam))) return;
    if (ceil !== 'wave' && !(await this._loadVariant('ceil_' + ceil, 'c:' + ceil))) return;
    if (this.planKey !== key || fam !== this.family() || ceil !== this.ceilingDesign()) return;   // changed meanwhile
    this.activeFamily = fam; this.activeCeiling = ceil;
    this.root.traverse((o) => { if (o.userData.variant) o.visible = this._variantVisible(o.userData.variant); });
    this.renderer.shadowMap.needsUpdate = true; this.invalidate();
  }

  private async _loadVariant(file: string, tag: string): Promise<boolean> {
    if (this.loadedVariants.has(tag)) return true;
    const key = this.planKey; let data: VariantData;
    this.events.onLoading('Loading…');
    try { data = await fetchJson<VariantData>(`${key}.${file}`); } catch { this.events.onLoading(null); return false; }
    this.events.onLoading(null);
    if (this.planKey !== key || !this.plan) return false;
    if (!this.loadedVariants.has(tag)) {
      for (const k in data.mats) if (!this.plan.mats[k]) this.plan.mats[k] = data.mats[k];
      this.loadedVariants.add(tag);
      for (const ch of data.chunks) this._addChunk(ch, tag);
    }
    return true;
  }

  /** High-quality rendering (textures, shadows, reflections). Rebuilds the model. */
  setHQ(on: boolean): void { this.hq = on; if (this.plan) { this._rebuild(); void this._ensureVariants(); } }

  // ---------------------------------------------------------------- visibility and lighting
  setOptions(opts: Partial<ViewOptions>): void { Object.assign(this.opts, opts); this.applyVisibility(); }

  isAboveCeiling(): boolean { return this.camera.position.y > CEILING_HEIGHT; }

  applyVisibility(): void {
    if (!this.plan) return;
    const o = this.opts, tag = this.viewTag;
    const planLike = tag === 'top' || tag === 'plan' || tag === 'services';
    const hide = new Set(['Beams_Highlight', 'Structural_Highlight', ...(this.plan.modes[o.mode]?.hide || [])]);
    if (planLike || this.isAboveCeiling()) hide.add('Ceiling');
    if (!o.fc || planLike) { hide.add('False_Ceiling'); hide.add('Lighting'); }
    if (!o.wood || !o.fc || planLike) hide.add('Ceiling_Wood');
    if (!o.pwr) hide.add('Power_Points');
    if (!o.ac) hide.add('Aircon_Trunking');
    if (!o.cur || tag === 'plan') hide.add('Curtains');
    for (const [name, grp] of Object.entries(this.layers)) grp.visible = !hide.has(name);
    this.dimGroup.visible = o.lab;

    const n = o.night, hq = this.hq;
    this.scene.background = new THREE.Color(n ? NIGHT_BG : DAY_BG);
    this.scene.environment = hq ? this.envTex : null;
    // realistic mode lights the rooms mostly with the soft environment (like daylight bouncing around a room)
    this.hemi.intensity = n ? 0.04 : hq ? 0.25 : 1.1;
    this.sun.intensity = n ? 0 : hq ? 3.0 : 1.4; this.sun.castShadow = hq;
    this.fill.intensity = n ? 0.02 : hq ? 0.12 : 0.25;
    this.amb.intensity = n ? 0.04 : hq ? 0.0 : 0.3;
    for (const L of this.nightLights) { L.intensity = n ? 0.9 : 0; L.visible = n; }
    for (const m of Object.values(this.materials)) m.envMapIntensity = n ? 0.08 : 1.05;
    for (const m of this.emissive) m.emissiveIntensity = n ? 2.4 : 0.35;
    this.renderer.toneMappingExposure = n ? 1.25 : 1.0;
    this.renderer.shadowMap.needsUpdate = true;
    this._buildLabels();
    this.aoDone = false;
    this.invalidate();
  }

  // ---------------------------------------------------------------- labels
  private _buildLabels(): void {
    this.labelsEl.innerHTML = ''; this.labelEls = [];
    if (!this.opts.lab || !this.plan) return;
    const add = (text: string, cls: string, p: THREE.Vector3) => {
      const e = document.createElement('div'); e.className = cls; e.textContent = text;
      this.labelsEl.appendChild(e); this.labelEls.push([e, p]);
    };
    for (const [t, x, y] of this.plan.labels) add(t, 'lbl', new THREE.Vector3(x, 150, y));
    for (const [a, b, t] of this.plan.dims) add(t + ' mm', 'lbl dim', new THREE.Vector3((a[0] + b[0]) / 2, 80, (a[1] + b[1]) / 2));
  }
  private _placeLabels(): void {
    const w = this.container.clientWidth, h = this.container.clientHeight, p = new THREE.Vector3();
    for (const [e, pos] of this.labelEls) {
      p.copy(pos).project(this.camera);
      const vis = p.z < 1 && Math.abs(p.x) < 1.1 && Math.abs(p.y) < 1.1;
      e.style.display = vis ? '' : 'none';
      if (vis) { e.style.left = ((p.x + 1) / 2 * w) + 'px'; e.style.top = ((1 - p.y) / 2 * h) + 'px'; }
    }
  }

  // ---------------------------------------------------------------- camera
  private _fovFor(view: View): number {
    const aspect = this.container.clientWidth / Math.max(1, this.container.clientHeight);
    let vf = Math.min(view.fov * 0.78, 78);
    if (aspect < 1) {   // portrait screens: keep the horizontal field of view
      const hf = Math.min(view.fov, 95) * Math.PI / 180;
      vf = Math.min(100, 2 * Math.atan(Math.tan(hf / 2) / aspect) * 180 / Math.PI);
    }
    return vf;
  }

  /** Move the camera to a scene. Plan views look straight down from high above. */
  showView(view: View, { instant = false }: { instant?: boolean } = {}): void {
    this.viewTag = view.tag || '';
    const eye = new THREE.Vector3(view.eye[0], view.eye[2], view.eye[1]);
    const target = new THREE.Vector3(view.target[0], view.target[2], view.target[1]);
    if (view.tag === 'plan') eye.set(view.target[0], 80000, view.target[1] + 1);
    this.camera.up.set(0, 1, 0);
    this.currentView = view;
    this.nav.flyTo(eye, target, this._fovFor(view), instant ? 0 : 900, () => {
      this.nav.controls.update();
      // walk-around scenes start in look mode, overviews in orbit mode
      const keepTape = this.nav.tool === 'tape';   // stay in tape-measure mode when stepping through scenes
      this.nav.setTool(keepTape ? 'tape' : view.eye[2] < 5000 && view.tag !== 'plan' ? 'look' : 'orbit', true);
      this.applyVisibility();
    });
    this.applyVisibility();
  }

  setTool(tool: Tool): void { this.nav.setTool(tool); }
  /** Remove all tape measurements. */
  clearMeasurements(): void { this.tape.clear(); }
  zoomExtents(): void { this.nav.zoomExtents(new THREE.Box3().setFromObject(this.root)); this.applyVisibility(); }

  resize(): void {
    const w = this.container.clientWidth, h = this.container.clientHeight;
    if (!w || !h) return;
    this.renderer.setSize(w, h, false);
    this.camera.aspect = w / h;
    if (this.currentView) this.camera.fov = this._fovFor(this.currentView);
    this.camera.updateProjectionMatrix();
    if (this.composer) { this.composer.setPixelRatio(this.renderer.getPixelRatio()); this.composer.setSize(w, h); }
    this.aoDone = false; this.invalidate();
  }

  // ---------------------------------------------------------------- screenshots
  /** Copy the canvas into a 2D canvas; reports whether the frame looks blank (all one colour). */
  private _grab(): { canvas: HTMLCanvasElement; blank: boolean } {
    const src = this.renderer.domElement;
    const cv = document.createElement('canvas'); cv.width = src.width; cv.height = src.height;
    const cx = cv.getContext('2d')!;
    cx.fillStyle = '#eae6df'; cx.fillRect(0, 0, cv.width, cv.height); cx.drawImage(src, 0, 0);
    const d = cx.getImageData(0, 0, cv.width, cv.height).data;
    const step = Math.max(4, Math.floor(d.length / 4 / 400)) * 4;
    let lo = 765, hi = 0;
    for (let i = 0; i < d.length; i += step) { const v = d[i] + d[i + 1] + d[i + 2]; lo = Math.min(lo, v); hi = Math.max(hi, v); }
    return { canvas: cv, blank: hi - lo < 12 };
  }

  /** Screenshot of the current view as a data URL ('image/png' or 'image/jpeg'). */
  async capture(type: 'image/png' | 'image/jpeg' = 'image/png'): Promise<string> {
    const nextFrame = (): Promise<void> => new Promise((r) => requestAnimationFrame(() => r()));
    let shot = this._grab();
    for (let attempt = 0; attempt < 4; attempt++) {
      if (!this.photo) this._renderFinal(); shot = this._grab(); if (!shot.blank) break;   // Chrome / Firefox
      this.invalidate(); await nextFrame(); await nextFrame(); shot = this._grab(); if (!shot.blank) break;   // Safari
    }
    return type === 'image/jpeg' ? shot.canvas.toDataURL('image/jpeg', 0.92) : shot.canvas.toDataURL('image/png');
  }

  dispose(): void {
    this.stopPhoto();
    this.renderer.setAnimationLoop(null);
    document.removeEventListener('visibilitychange', this._onVisible);
    this.tape.dispose(); this.nav.dispose(); this._clearModel(); this.renderer.dispose(); this.renderer.domElement.remove();
  }
}
