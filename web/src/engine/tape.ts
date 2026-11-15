// Tape measure (like SketchUp's): click a point on the model, then a second point; the distance shows in mm.
// Points snap to a nearby corner of the surface you clicked. Measurements stay until cleared (Esc).
import * as THREE from 'three';

const SNAP_MM = 60;          // snap to a triangle corner closer than this
const COLOR = 0xff6a3d;

interface Measurement { a: THREE.Vector3; b: THREE.Vector3; line: THREE.Line; dots: THREE.Mesh[]; label: HTMLElement }

export class TapeMeasure {
  active = false;
  /** first point of the measurement being made */
  start: { p: THREE.Vector3; dot: THREE.Mesh } | null = null;
  /** finished measurements */
  items: Measurement[] = [];
  /** live line while choosing the second point */
  preview: { line: THREE.Line; label: HTMLElement; b?: THREE.Vector3 } | null = null;
  group = new THREE.Group();
  lineMat = new THREE.LineBasicMaterial({ color: COLOR, depthTest: false, transparent: true });
  dotMat = new THREE.MeshBasicMaterial({ color: COLOR, depthTest: false, transparent: true });
  dotGeo = new THREE.SphereGeometry(1, 12, 8);
  ray = new THREE.Raycaster();
  private _down: [number, number] | null = null;
  private _raf = 0;
  private _off: (() => void)[] = [];

  /**
   * @param model    what can be measured
   * @param overlay  element that holds the distance labels
   */
  constructor(scene: THREE.Scene, private camera: THREE.PerspectiveCamera, private canvas: HTMLCanvasElement,
    private model: THREE.Object3D, private overlay: HTMLElement, private invalidate: () => void) {
    this.group.renderOrder = 10; scene.add(this.group);
    const on = (n: string, f: (e: PointerEvent) => void) => {
      canvas.addEventListener(n, f as EventListener); this._off.push(() => canvas.removeEventListener(n, f as EventListener));
    };
    on('pointerdown', (e) => { if (this.active && e.button === 0) this._down = [e.clientX, e.clientY]; });
    on('pointerup', (e) => {
      if (!this.active || e.button !== 0 || !this._down) return;
      const moved = Math.hypot(e.clientX - this._down[0], e.clientY - this._down[1]); this._down = null;
      if (moved < 6) this._click(e);
    });
    on('pointermove', (e) => {
      if (!this.active || !this.start || this._raf) return;
      this._raf = requestAnimationFrame(() => { this._raf = 0; this._hover(e); });
    });
  }

  setActive(on: boolean): void { this.active = on; this.canvas.style.cursor = on ? 'crosshair' : ''; if (!on) this._cancelPreview(); }

  /** Remove every measurement. */
  clear(): void {
    this._cancelPreview();
    for (const m of this.items) { m.label.remove(); }
    this.items = []; this.group.clear(); this.invalidate();
  }

  // point on the model under the pointer (snapped to a nearby corner), or null
  private _pick(e: PointerEvent): THREE.Vector3 | null {
    const r = this.canvas.getBoundingClientRect();
    const ndc = new THREE.Vector2(((e.clientX - r.left) / r.width) * 2 - 1, -((e.clientY - r.top) / r.height) * 2 + 1);
    this.ray.setFromCamera(ndc, this.camera);
    const hit = this.ray.intersectObject(this.model, true).find((h) => h.object.visible && this._shown(h.object) && h.face);
    if (!hit) return null;
    const p = hit.point.clone();
    const pos = (hit.object as THREE.Mesh).geometry.attributes.position as THREE.BufferAttribute; let best: THREE.Vector3 | null = null, bestD = SNAP_MM;
    for (const i of [hit.face!.a, hit.face!.b, hit.face!.c]) {
      const v = new THREE.Vector3().fromBufferAttribute(pos, i).applyMatrix4(hit.object.matrixWorld);
      const d = v.distanceTo(p); if (d < bestD) { bestD = d; best = v; }
    }
    return best || p;
  }
  private _shown(o: THREE.Object3D): boolean { for (let x: THREE.Object3D | null = o; x; x = x.parent) if (!x.visible) return false; return true; }

  private _dot(p: THREE.Vector3): THREE.Mesh {
    const s = Math.max(12, this.camera.position.distanceTo(p) * 0.006);
    const m = new THREE.Mesh(this.dotGeo, this.dotMat); m.position.copy(p); m.scale.setScalar(s); m.renderOrder = 11; return m;
  }
  private _line(a: THREE.Vector3, b: THREE.Vector3): THREE.Line { const g = new THREE.BufferGeometry().setFromPoints([a, b]); const l = new THREE.Line(g, this.lineMat); l.renderOrder = 10; return l; }
  private _label(text: string): HTMLElement { const d = document.createElement('div'); d.className = 'lbl tape'; d.textContent = text; this.overlay.appendChild(d); return d; }

  private _click(e: PointerEvent): void {
    const p = this._pick(e); if (!p) return;
    if (!this.start) {
      this.start = { p, dot: this._dot(p) }; this.group.add(this.start.dot);
    } else {
      this._cancelPreview(true);
      const a = this.start.p, b = p;
      const item: Measurement = { a, b, line: this._line(a, b), dots: [this.start.dot, this._dot(b)], label: this._label(fmt(a.distanceTo(b))) };
      this.group.add(item.line, item.dots[1]);
      this.items.push(item); this.start = null;
    }
    this.invalidate();
  }

  private _hover(e: PointerEvent): void {
    const p = this._pick(e); if (!p || !this.start) return;
    if (!this.preview) { this.preview = { line: this._line(this.start.p, p), label: this._label('') }; this.group.add(this.preview.line); }
    this.preview.line.geometry.setFromPoints([this.start.p, p]);
    this.preview.b = p; this.preview.label.textContent = fmt(this.start.p.distanceTo(p));
    this.invalidate();
  }

  private _cancelPreview(keepStart = false): void {
    if (this.preview) { this.group.remove(this.preview.line); this.preview.label.remove(); this.preview = null; }
    if (!keepStart && this.start) { this.group.remove(this.start.dot); this.start = null; }
    this.invalidate();
  }

  /** Keep the distance labels next to their lines (called every drawn frame). */
  place(width: number, height: number): void {
    const put = (el: HTMLElement, a: THREE.Vector3, b: THREE.Vector3) => {
      const m = a.clone().add(b).multiplyScalar(0.5).project(this.camera);
      const vis = m.z < 1 && Math.abs(m.x) < 1.2 && Math.abs(m.y) < 1.2;
      el.style.display = vis ? '' : 'none';
      if (vis) { el.style.left = ((m.x + 1) / 2 * width) + 'px'; el.style.top = ((1 - m.y) / 2 * height) + 'px'; }
    };
    for (const m of this.items) put(m.label, m.a, m.b);
    if (this.preview?.b && this.start) put(this.preview.label, this.start.p, this.preview.b);
  }

  dispose(): void { this._off.forEach((f) => f()); this.clear(); }
}

/** 2345.6 -> "2,346 mm" */
function fmt(mm: number): string { return `${Math.round(mm).toLocaleString('en-SG')} mm`; }
