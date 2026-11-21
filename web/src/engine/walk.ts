// 360° walk: stand at a few fixed points in the flat (one per room), drag to look all around, and click the
// circles on the floor to step to the next point - like street-view maps.
//
// At each point the view is either drawn live (realistic mode) or, when a path-traced 360° photo of that point has
// been rendered and saved before, that panorama is shown instead: no heavy rendering on this device.
import * as THREE from 'three';
import type { Viewer } from './Viewer';
import { PANO_BASE, publishedManifest, type PanoManifest } from '../lib/github';

export const EYE_HEIGHT = 1550;
export type WalkPoint = { name: string; x: number; y: number };

export interface WalkEvents {
  /** the current point changed, a panorama started/stopped showing, or the walk started/ended */
  onChange: () => void;
}

const LOS_SKIP = new Set(['Decor', 'Lighting', 'Ceiling', 'False_Ceiling', 'Ceiling_Wood', 'Curtains', 'Power_Points', 'Aircon_Trunking', 'Sanitary']);

const slugify = (s: string) => s.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '');
/** small stable hash of a string (FNV-1a), as 7 base-36 digits */
function hash(s: string): string { let h = 0x811c9dc5; for (let i = 0; i < s.length; i++) { h ^= s.charCodeAt(i); h = Math.imul(h, 0x01000193); } return (h >>> 0).toString(36).padStart(7, '0'); }

export class Walk {
  active = false;
  idx = 0;
  points: WalkPoint[] = [];
  /** points you can step to from here (in sight, not too far) */
  near: number[] = [];
  manifest: PanoManifest = {};
  /** the saved panorama shown at the current point, if any */
  panoTex: THREE.Texture | null = null;
  panoScene = new THREE.Scene();
  private spots: HTMLElement;
  private loading = '';
  private texCache = new Map<string, THREE.Texture>();

  constructor(private v: Viewer, private events: WalkEvents) {
    this.spots = document.createElement('div'); this.spots.className = 'walk-spots'; v.container.appendChild(this.spots);
    void this.refreshManifest();
  }

  async refreshManifest(): Promise<void> { this.manifest = await publishedManifest(); this._loadPano(); }

  /** Key of the current look (plan, theme, ceiling design, layout option, day/night): a panorama only matches its own look. */
  setupKey(): string {
    const v = this.v; return [v.planKey, v.theme, v.ceiling, v.opts.mode, v.opts.night ? 'night' : 'day'].join('|');
  }
  /** Path in the repository for the current point's panorama. */
  filePath(i = this.idx): string { return `pano/${this.v.planKey}/${hash(this.setupKey())}/${slugify(this.points[i].name)}.jpg`; }
  savedCount(): number { const m = this.manifest[this.setupKey()] || {}; return this.points.filter((p) => m[p.name]).length; }
  hasSaved(i = this.idx): boolean { return !!(this.manifest[this.setupKey()] || {})[this.points[i]?.name]; }

  /** Start the walk at the point nearest the camera (or the living room). */
  enter(): void {
    const plan = this.v.plan; if (!plan) return;
    this.points = (plan.pano || plan.labels).map(([name, x, y]) => ({ name, x, y }));
    if (!this.points.length) return;
    const c = this.v.camera.position;
    let best = this.points.findIndex((p) => /^Living/.test(p.name)); if (best < 0) best = 0;
    if (c.y < 2600) best = this.points.reduce((b, p, i) => (Math.hypot(p.x - c.x, p.y - c.z) < Math.hypot(this.points[b].x - c.x, this.points[b].y - c.z) ? i : b), 0);
    this.active = true;
    this.go(best, true);
  }

  exit(): void {
    this.active = false; this.panoTex = null; this.spots.innerHTML = ''; this.v.invalidate(); this.events.onChange();
  }

  /** Step to point i, keeping the direction you are looking in. */
  go(i: number, instant = false): void {
    const p = this.points[i]; if (!p) return;
    const from = this.points[this.idx];
    this.idx = i; this.panoTex = null; this.spots.innerHTML = '';
    const v = this.v, nav = v.nav;
    let dir = nav.nav === 'look' ? nav.lookDir() : new THREE.Vector3().subVectors(nav.controls.target, v.camera.position).normalize();
    if (!instant && from && from !== p) dir = new THREE.Vector3(p.x - from.x, 0, p.y - from.y).normalize();   // face the way you walked
    dir.y = Math.max(-0.2, Math.min(0.1, dir.y)); dir.normalize();
    const eye = new THREE.Vector3(p.x, EYE_HEIGHT, p.y);
    v.viewTag = ''; v.currentView = null;
    v.flyToFlat(eye, eye.clone().addScaledVector(dir, 1500), 75, instant ? 0 : 650, () => {
      nav.setTool('look', true); v.applyVisibility();
      this._neighbours(); this._loadPano(); this.events.onChange();
    });
    v.applyVisibility();
    this.events.onChange();
  }

  /** At the point (not moving between points or walking off with the keys)? */
  atPoint(): boolean {
    const p = this.points[this.idx]; if (!this.active || !p) return false;
    const c = this.v.camera.position;
    return this.v.nav.nav !== 'tween' && Math.abs(c.x - p.x) < 2 && Math.abs(c.z - p.y) < 2 && Math.abs(c.y - EYE_HEIGHT) < 2;
  }

  /** Show the saved panorama for this point (fetched once, then cached). */
  private _loadPano(): void {
    if (!this.active) return;
    const rel = (this.manifest[this.setupKey()] || {})[this.points[this.idx]?.name];
    if (!rel) { this.panoTex = null; return; }
    const url = PANO_BASE + rel, idx = this.idx;
    const cached = this.texCache.get(url);
    if (cached) { this.panoTex = cached; this.v.invalidate(); this.events.onChange(); return; }
    if (this.loading === url) return;
    this.loading = url;
    new THREE.TextureLoader().setCrossOrigin('anonymous').load(url, (t) => {
      this.loading = '';
      t.colorSpace = THREE.SRGBColorSpace; t.mapping = THREE.EquirectangularReflectionMapping;
      this.texCache.set(url, t);
      if (this.idx === idx && this.active) { this.panoTex = t; this.v.invalidate(); this.events.onChange(); }
    }, undefined, () => { this.loading = ''; });
  }

  /** Use a panorama that was just rendered on this device (before it is published). */
  showLocal(i: number, blobUrl: string): void {
    new THREE.TextureLoader().load(blobUrl, (t) => {
      t.colorSpace = THREE.SRGBColorSpace; t.mapping = THREE.EquirectangularReflectionMapping;
      const rel = (this.manifest[this.setupKey()] || {})[this.points[i].name];
      if (rel) this.texCache.set(PANO_BASE + rel, t);
      if (this.idx === i) { this.panoTex = t; this.v.invalidate(); this.events.onChange(); }
    });
  }

  /** Draw the saved panorama (instead of the 3D model) when standing at the point. */
  render(): boolean {
    if (!this.panoTex || !this.atPoint()) return false;
    this.panoScene.background = this.panoTex;
    this.v.renderer.render(this.panoScene, this.v.camera);
    return true;
  }

  /** Points in sight from here: no wall, cabinet or fridge in the way at chest height, within 12 m. */
  private _neighbours(): void {
    const v = this.v, here = this.points[this.idx];
    const targets: THREE.Object3D[] = [];
    for (const [name, g] of Object.entries(v.layers)) {
      if (!g.visible || LOS_SKIP.has(name)) continue;
      g.traverse((o) => {
        const m = o as THREE.Mesh;
        if (m.isMesh && !(m.material as THREE.Material).transparent) targets.push(m);
      });
    }
    const ray = new THREE.Raycaster();
    const near: [number, number][] = [];
    this.points.forEach((p, i) => {
      if (i === this.idx) return;
      const d = Math.hypot(p.x - here.x, p.y - here.y);
      if (d > 12000 || d < 300) return;
      const o = new THREE.Vector3(here.x, 1250, here.y), dir = new THREE.Vector3(p.x - here.x, 0, p.y - here.y).normalize();
      ray.set(o, dir); ray.far = d;
      if (!ray.intersectObjects(targets, false).length) near.push([i, d]);
    });
    if (!near.length) {   // shut in (e.g. a bathroom): offer the closest points anyway
      this.points.forEach((p, i) => { if (i !== this.idx) near.push([i, Math.hypot(p.x - here.x, p.y - here.y)]); });
      near.sort((a, b) => a[1] - b[1]); near.splice(2);
    }
    this.near = near.map(([i]) => i);
    this.spots.innerHTML = '';
    for (const i of this.near) {
      const b = document.createElement('button'); b.className = 'walk-spot'; b.title = 'Go to ' + this.points[i].name;
      b.innerHTML = '<i></i><span></span>'; (b.querySelector('span') as HTMLElement).textContent = this.points[i].name;
      b.onclick = (e) => { e.stopPropagation(); this.go(i); };
      b.dataset.i = String(i);
      this.spots.appendChild(b);
    }
    this.place();
  }

  /** Keep the floor circles under the points they lead to. */
  place(): void {
    if (!this.active) return;
    const cam = this.v.camera, w = this.v.container.clientWidth, h = this.v.container.clientHeight;
    const moving = !this.atPoint();
    this.spots.style.opacity = moving ? '0' : '1';
    for (const el of Array.from(this.spots.children) as HTMLElement[]) {
      const p = this.points[+el.dataset.i!];
      const q = new THREE.Vector3(p.x, 30, p.y).project(cam);
      const behind = q.z > 1 || q.z < -1;
      el.style.display = behind ? 'none' : '';
      const d = Math.hypot(p.x - cam.position.x, p.y - cam.position.z);
      el.style.transform = `translate(${(q.x * 0.5 + 0.5) * w}px, ${(-q.y * 0.5 + 0.5) * h}px) translate(-50%, -50%) scale(${Math.max(0.45, Math.min(1.25, 2600 / d))})`;
    }
  }

  dispose(): void { this.spots.remove(); this.texCache.forEach((t) => t.dispose()); }
}
