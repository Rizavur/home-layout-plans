// Photo mode: path-traces the current view in the browser (three-gpu-pathtracer, loaded from the CDN on first use).
// Real bounce light, soft sky light through the windows, glass and reflections. The image sharpens as samples add up.
//
// While a photo is running the normal render loop hands every frame to `tick()`; moving the camera cancels it.
import * as THREE from 'three';
import { FullScreenQuad } from 'three/addons/postprocessing/Pass.js';
import { skyData } from './context';

type PathTracer = {
  bounces: number; filteredGlossyFactor: number; minSamples: number; fadeDuration: number; renderScale: number;
  tiles: THREE.Vector2; samples: number; renderToCanvas: boolean;
  renderToCanvasCallback: (target: THREE.WebGLRenderTarget, renderer: THREE.WebGLRenderer, quad: FullScreenQuad) => void;
  setScene(scene: THREE.Scene, camera: THREE.Camera): void;
  renderSample(): void; reset(): void; dispose(): void;
};

interface Swap { mesh: THREE.Mesh; material: THREE.Material | THREE.Material[] }

/**
 * Window "portals": an area light just inside each window pane, glowing like the sky behind it.
 * The tracer aims samples at lights, so rooms lit through windows clear up far faster than with the sky alone.
 */
function windowPortals(scene: THREE.Scene, centre: THREE.Vector3, eye: THREE.Vector3): THREE.RectAreaLight[] {
  const boxes: THREE.Box3[] = [];
  scene.traverseVisible((o) => {
    const mesh = o as THREE.Mesh;
    if (!mesh.isMesh || mesh.parent?.name !== 'Windows' || (mesh.material as THREE.Material).name !== 'Glass') return;
    const p = mesh.geometry.attributes.position.array as Float32Array;
    for (let t = 0; t < p.length; t += 9) {
      const b = new THREE.Box3();
      for (let k = 0; k < 3; k++) b.expandByPoint(new THREE.Vector3(p[t + k * 3], p[t + k * 3 + 1], p[t + k * 3 + 2]));
      boxes.push(b);
    }
  });
  // merge panes of the same window (same plane, gaps smaller than a frame)
  const merged: THREE.Box3[] = [];
  for (const b of boxes) {
    const grown = b.clone().expandByScalar(90);
    const hit = merged.find((m) => m.intersectsBox(grown));
    if (hit) hit.union(b); else merged.push(b.clone());
  }
  for (let again = true; again;) {      // boxes merged later may now touch each other
    again = false;
    for (let i = 0; i < merged.length && !again; i++) for (let j = i + 1; j < merged.length; j++) {
      if (merged[i].clone().expandByScalar(90).intersectsBox(merged[j])) { merged[i].union(merged[j]); merged.splice(j, 1); again = true; break; }
    }
  }
  // the tracer picks one light at random per sample, so only use the windows near the camera (its room)
  merged.sort((a, b) => a.distanceToPoint(eye) - b.distanceToPoint(eye));
  const near = merged.filter((b, i) => i < 4 && b.distanceToPoint(eye) < 7000);
  const lights: THREE.RectAreaLight[] = [];
  for (const b of near) {
    const size = b.getSize(new THREE.Vector3()), mid = b.getCenter(new THREE.Vector3());
    const thinX = size.x < size.z;                                  // pane lies in the y-z plane (faces x) or the x-y plane (faces z)
    const w = thinX ? size.z : size.x, h = size.y;
    if (w < 200 || h < 200) continue;
    const inward = thinX ? new THREE.Vector3(Math.sign(centre.x - mid.x) || 1, 0, 0) : new THREE.Vector3(0, 0, Math.sign(centre.z - mid.z) || 1);
    const L = new THREE.RectAreaLight(0xfff4e8, 3.2, w, h);
    L.position.copy(mid).addScaledVector(inward, 60);
    L.lookAt(L.position.clone().add(inward));
    scene.add(L); lights.push(L);
  }
  return lights;
}

/** Equirectangular sky (float RGBA): bright warm horizon, soft blue zenith, dim ground. Linear radiance. */
function skyTexture(night: boolean): THREE.DataTexture {
  const w = 256, h = 128, data = new Float32Array(w * h * 4);
  const zen = night ? [0.010, 0.012, 0.02] : [2.6, 2.8, 3.2];
  const hor = night ? [0.020, 0.018, 0.02] : [4.8, 4.6, 4.3];
  const gnd = night ? [0.004, 0.004, 0.004] : [1.2, 1.15, 1.05];
  for (let j = 0; j < h; j++) {
    const el = (0.5 - (j + 0.5) / h) * Math.PI;          // +pi/2 at the top row
    const s = Math.sin(el);
    for (let i = 0; i < w; i++) {
      let c: number[];
      if (s >= 0) { const t = Math.pow(s, 0.45); c = hor.map((v, k) => v * (1 - t) + zen[k] * t); }
      else { const t = Math.min(1, -s * 6); c = hor.map((v, k) => v * (1 - t) * 0.6 + gnd[k] * t); }
      const o = (j * w + i) * 4; data[o] = c[0]; data[o + 1] = c[1]; data[o + 2] = c[2]; data[o + 3] = 1;
    }
  }
  const t = new THREE.DataTexture(data, w, h, THREE.RGBAFormat, THREE.FloatType);
  t.mapping = THREE.EquirectangularReflectionMapping; t.minFilter = THREE.LinearFilter; t.magFilter = THREE.LinearFilter;
  t.needsUpdate = true;
  return t;
}

export class PhotoRenderer {
  private tracer: PathTracer | null = null;
  private swaps: Swap[] = [];
  private tangents: THREE.BufferGeometry[] = [];
  private saved: { env: THREE.Texture | null; bg: THREE.Color | THREE.Texture | null; hemi: number; amb: number; fill: number; exposure: number } | null = null;
  private sky: THREE.DataTexture | null = null;
  private portals: THREE.RectAreaLight[] = [];
  private denoise: FullScreenQuad | null = null;
  target: number;

  /** set for a 360° panorama: an equirectangular camera standing at this point */
  private equirectAt: THREE.Vector3 | null = null;

  constructor(private renderer: THREE.WebGLRenderer, private scene: THREE.Scene, private camera: THREE.PerspectiveCamera,
              private lights: { hemi: THREE.Light; amb: THREE.Light; fill: THREE.Light }, private night: boolean, mobile: boolean,
              opts: { equirectAt?: THREE.Vector3; samples?: number } = {}) {
    this.target = opts.samples || (mobile ? 200 : 500);
    this.equirectAt = opts.equirectAt || null;
  }

  get samples(): number { return this.tracer ? Math.floor(this.tracer.samples) : 0; }

  /** Load the path tracer, swap in physically based materials and build the acceleration structure (blocks for a moment). */
  async start(): Promise<void> {
    const mod = await import('three-gpu-pathtracer') as unknown as { WebGLPathTracer: new (r: THREE.WebGLRenderer) => PathTracer; EquirectCamera: new () => THREE.Camera };
    const scene = this.scene;
    // three 0.160 scenes have no background/environment rotation, which the path tracer reads (also from its own scenes)
    const proto = THREE.Scene.prototype as unknown as Record<string, unknown>;
    for (const key of ['backgroundRotation', 'environmentRotation']) {
      if (!(key in new THREE.Scene())) {
        Object.defineProperty(proto, key, {
          configurable: true,
          get(this: Record<string, unknown>) { return (this['_' + key] ||= new THREE.Euler()); },
          set(this: Record<string, unknown>, v: unknown) { this['_' + key] = v; },
        });
      }
    }

    this.saved = { env: scene.environment, bg: scene.background as THREE.Color | THREE.Texture | null, hemi: this.lights.hemi.intensity,
      amb: this.lights.amb.intensity, fill: this.lights.fill.intensity, exposure: this.renderer.toneMappingExposure };
    this.sky = this.night ? skyTexture(true) : skyData(false, 4.4, 1024, 512);
    scene.environment = this.sky; scene.background = this.sky;
    // ambient / hemisphere / fill lights are fakes for the raster view: the sky does that job now
    this.lights.hemi.intensity = 0; this.lights.amb.intensity = 0; this.lights.fill.intensity = 0;
    this.renderer.toneMappingExposure = this.night ? 1.6 : 1.1;

    const physical: Record<string, THREE.Material> = {};
    scene.traverseVisible((o) => {
      const mesh = o as THREE.Mesh;
      if (!mesh.isMesh) return;
      const m = mesh.material as THREE.MeshStandardMaterial;
      if (Array.isArray(m) || !m.isMeshStandardMaterial) return;
      let rep = physical[m.uuid];
      if (!rep) {
        const name = m.name || '';
        if (m.transparent && m.opacity < 1) {
          // glass: real transmission instead of see-through alpha
          const frosted = /Fluted|Frosted|Smoked|Opal|Curtain/.test(name);
          rep = new THREE.MeshPhysicalMaterial({ color: m.color, transmission: 1, ior: 1.5, thickness: 0, roughness: frosted ? (/Curtain/.test(name) ? 0.7 : 0.35) : 0.0, metalness: 0, side: THREE.DoubleSide });
        } else if (/Mirror/.test(name)) {
          rep = new THREE.MeshStandardMaterial({ color: 0xffffff, metalness: 1, roughness: 0.02, side: THREE.DoubleSide });
        } else {
          const c = m.clone(); c.normalMap = null; c.envMap = null; c.transparent = false; c.opacity = 1;   // the tracer needs tangents for normal maps; skip them
          if (!this.night && c.emissiveMap) { c.emissiveMap = null; c.emissive.set(0); c.emissiveIntensity = 0; }   // lit windows of the neighbours: night only
          rep = c;
        }
        rep.name = name;
        physical[m.uuid] = rep;
      }
      this.swaps.push({ mesh, material: mesh.material });
      mesh.material = rep;
      const g = mesh.geometry;
      if (!g.attributes.tangent) { g.setAttribute('tangent', new THREE.BufferAttribute(new Float32Array(g.attributes.position.count * 4), 4)); this.tangents.push(g); }
    });

    if (!this.night) {
      // the flat only (not the neighbourhood outside), so each window light faces into the rooms
      const box = new THREE.Box3();
      for (const ch of this.scene.children) if (ch.name !== 'Outdoors' && ch.visible) box.expandByObject(ch);
      this.portals = windowPortals(this.scene, box.getCenter(new THREE.Vector3()), this.equirectAt || this.camera.position);
    }
    const t = new mod.WebGLPathTracer(this.renderer);
    t.bounces = 5; t.filteredGlossyFactor = 0.5; t.minSamples = 1; t.fadeDuration = 0; t.renderScale = 1;
    t.tiles.set(2, 2); t.renderToCanvas = true;
    // edge-aware denoise on screen: strong while the image is young, lighter as passes add up
    const Denoise = (mod as unknown as { DenoiseMaterial: new (p: object) => THREE.ShaderMaterial }).DenoiseMaterial;
    this.denoise = new FullScreenQuad(new Denoise({ map: null, blending: THREE.CustomBlending, premultipliedAlpha: this.renderer.getContextAttributes().premultipliedAlpha }));
    t.renderToCanvasCallback = (target, renderer, quad) => {
      const q = this.denoise!, m = q.material as THREE.ShaderMaterial & Record<string, number | THREE.Texture | null>;
      const k = Math.min(1, t.samples / this.target);
      m.sigma = 4.5 - 2.5 * k; m.kSigma = 1.0; m.threshold = 0.06 - 0.03 * k;
      m.opacity = (quad.material as THREE.Material).opacity;
      const auto = renderer.autoClear; renderer.autoClear = false;
      m.map = target.texture; q.render(renderer); renderer.autoClear = auto;
    };
    let cam: THREE.Camera = this.camera;
    if (this.equirectAt) { cam = new mod.EquirectCamera(); cam.position.copy(this.equirectAt); cam.updateMatrixWorld(true); }
    t.setScene(this.scene, cam);
    this.tracer = t;
  }

  /** Trace one more sample. Returns false once the target sample count is reached. */
  tick(): boolean {
    if (!this.tracer) return false;
    if (this.tracer.samples >= this.target) return false;
    this.tracer.renderSample();
    return true;
  }

  /** Put the scene back the way the raster view expects it. */
  stop(): void {
    for (const s of this.swaps) s.mesh.material = s.material;
    for (const g of this.tangents) g.deleteAttribute('tangent');
    this.swaps = []; this.tangents = [];
    if (this.saved) {
      this.scene.environment = this.saved.env; this.scene.background = this.saved.bg;
      this.lights.hemi.intensity = this.saved.hemi; this.lights.amb.intensity = this.saved.amb; this.lights.fill.intensity = this.saved.fill;
      this.renderer.toneMappingExposure = this.saved.exposure;
    }
    for (const L of this.portals) L.removeFromParent();
    this.portals = [];
    this.denoise?.dispose(); this.denoise = null;
    try { this.tracer?.dispose(); } catch { /* never fully set up */ }
    this.tracer = null; this.sky?.dispose(); this.sky = null;
  }
}
