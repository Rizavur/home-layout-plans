// Camera navigation, modelled on SketchUp's tools:
//   look  – stand still and turn your head (drag), zoom the lens (scroll / pinch), walk with W A S D / arrows
//   orbit – rotate around a target (three.js OrbitControls), pan – slide the view, zoom – drag to dolly
// Also animates smooth camera flights between scenes.
import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';

const WALK_STEP_MM = 25;   // per frame while a walk key is held

function ease(k) { return k < 0.5 ? 4 * k * k * k : 1 - Math.pow(-2 * k + 2, 3) / 2; }

const typingIn = (e) => ['SELECT', 'INPUT', 'TEXTAREA'].includes(e.target.tagName);

export class Navigator {
  /**
   * @param {THREE.PerspectiveCamera} camera
   * @param {HTMLElement} dom   the canvas
   * @param {() => void} invalidate  ask for a redraw
   * @param {(tool: string) => void} onTool  told whenever the active tool changes
   */
  constructor(camera, dom, invalidate, onTool) {
    this.camera = camera; this.dom = dom; this.invalidate = invalidate; this.onTool = onTool;
    this.controls = new OrbitControls(camera, dom);
    Object.assign(this.controls, { enableDamping: true, dampingFactor: 0.12, screenSpacePanning: true, zoomSpeed: 0.9 });
    this.controls.addEventListener('change', invalidate);
    this.nav = 'look';          // what is driving the camera: 'look' | 'orbit' | 'tween'
    this.tool = 'look';         // the tool button that is highlighted
    this.look = { yaw: 0, pitch: 0, pointers: new Map(), lastPinch: 0 };
    this.tween = null;
    this.keys = new Set();
    this._listen();
  }

  // ---------- look-around ----------
  lookDir() {
    const { yaw, pitch } = this.look;
    return new THREE.Vector3(Math.sin(yaw) * Math.cos(pitch), Math.sin(pitch), Math.cos(yaw) * Math.cos(pitch));
  }
  syncLookFromCamera() {
    const d = new THREE.Vector3().subVectors(this.controls.target, this.camera.position).normalize();
    this.look.yaw = Math.atan2(d.x, d.z);
    this.look.pitch = Math.asin(Math.max(-1, Math.min(1, d.y)));
  }
  applyLook() { this.camera.lookAt(this.camera.position.clone().add(this.lookDir())); this.invalidate(); }
  zoomLens(factor) {
    this.camera.fov = Math.max(20, Math.min(100, this.camera.fov * factor));
    this.camera.updateProjectionMatrix(); this.invalidate();
  }
  /** Where the camera is looking at, whichever mode drives it. */
  currentTarget() {
    return this.nav === 'look' ? this.camera.position.clone().add(this.lookDir().multiplyScalar(1500)) : this.controls.target.clone();
  }

  // ---------- tools ----------
  /** @param {'look'|'orbit'|'pan'|'zoom'} tool  @param {boolean} fromView  true when a scene just set the camera */
  setTool(tool, fromView = false) {
    const was = this.nav; this.tool = tool;
    const c = this.controls;
    if (tool === 'look') {
      this.nav = 'look'; this.syncLookFromCamera(); c.enabled = false; this.applyLook();
    } else {
      this.nav = 'orbit';
      // leaving look mode by hand: orbit around the point we were looking at
      if (!fromView && was === 'look') c.target.copy(this.currentTargetFromLook());
      c.enabled = true;
      c.mouseButtons = {
        LEFT: tool === 'pan' ? THREE.MOUSE.PAN : tool === 'zoom' ? THREE.MOUSE.DOLLY : THREE.MOUSE.ROTATE,
        MIDDLE: THREE.MOUSE.ROTATE,
        RIGHT: tool === 'pan' ? THREE.MOUSE.ROTATE : THREE.MOUSE.PAN,
      };
      c.touches = { ONE: tool === 'pan' ? THREE.TOUCH.PAN : THREE.TOUCH.ROTATE, TWO: THREE.TOUCH.DOLLY_PAN };
      c.zoomToCursor = true;
      c.update();
    }
    this.onTool(tool);
  }
  currentTargetFromLook() { return this.camera.position.clone().add(this.lookDir().multiplyScalar(1500)); }

  /** Frame a bounding box (SketchUp "Zoom extents"). */
  zoomExtents(box) {
    if (box.isEmpty()) return;
    const centre = box.getCenter(new THREE.Vector3());
    const size = box.getSize(new THREE.Vector3()).length();
    const dir = this.nav === 'look' ? this.lookDir() : new THREE.Vector3().subVectors(this.controls.target, this.camera.position).normalize();
    if (dir.y > -0.25) { dir.y = -0.6; dir.normalize(); }
    const dist = size / (2 * Math.tan(this.camera.fov * Math.PI / 360)) * 0.9;
    this.controls.target.copy(centre);
    this.camera.position.copy(centre.clone().addScaledVector(dir, -dist));
    this.setTool(this.tool === 'look' ? 'orbit' : this.tool, true);
  }

  // ---------- camera flights between scenes ----------
  flyTo(eye, target, fov, ms, done) {
    if (ms <= 0) {
      this.camera.position.copy(eye); this.controls.target.copy(target);
      this.camera.fov = fov; this.camera.updateProjectionMatrix(); this.camera.lookAt(target);
      done(); return;
    }
    const p0 = this.camera.position.clone();
    this.tween = {
      p0, t0: this.currentTarget(), f0: this.camera.fov, p1: eye, t1: target, f1: fov, start: performance.now(), ms, done,
      lift: Math.min(2500, p0.distanceTo(eye) * 0.25),   // arc over walls when travelling far
    };
    this.nav = 'tween'; this.controls.enabled = false; this.invalidate();
  }
  stepTween(now) {
    const tw = this.tween; if (!tw) return false;
    const k = Math.min(1, (now - tw.start) / tw.ms), e = ease(k);
    this.camera.position.lerpVectors(tw.p0, tw.p1, e); this.camera.position.y += Math.sin(Math.PI * e) * tw.lift;
    const tg = new THREE.Vector3().lerpVectors(tw.t0, tw.t1, e);
    this.controls.target.copy(tg);
    this.camera.fov = tw.f0 + (tw.f1 - tw.f0) * e; this.camera.updateProjectionMatrix(); this.camera.lookAt(tg);
    if (k >= 1) { this.tween = null; tw.done(); }
    return true;
  }

  // ---------- per-frame update ----------
  /** Advance flights / walking / orbit damping. Returns true if the camera moved. */
  update(now) {
    let moved = this.stepTween(now);
    if (!moved) moved = this.walkStep();
    if (this.nav === 'orbit' && this.controls.update()) moved = true;   // damping still settling
    return moved;
  }
  walkStep() {
    const k = this.keys; if (k.size === 0) return false;
    if (this.nav !== 'look') this.syncLookFromCamera();
    const f = new THREE.Vector3(Math.sin(this.look.yaw), 0, Math.cos(this.look.yaw));
    const r = new THREE.Vector3(-f.z, 0, f.x), v = new THREE.Vector3();
    if (k.has('w') || k.has('arrowup')) v.add(f);
    if (k.has('s') || k.has('arrowdown')) v.sub(f);
    if (k.has('d') || k.has('arrowright')) v.add(r);
    if (k.has('a') || k.has('arrowleft')) v.sub(r);
    if (v.lengthSq() === 0) return false;
    const step = v.normalize().multiplyScalar(WALK_STEP_MM);
    this.camera.position.add(step);
    if (this.nav === 'look') this.applyLook(); else { this.controls.target.add(step); this.controls.update(); }
    return true;
  }

  // ---------- input ----------
  _listen() {
    const el = this.dom, look = this.look;
    const on = (t, n, f, o) => { t.addEventListener(n, f, o); (this._off ||= []).push(() => t.removeEventListener(n, f, o)); };
    on(el, 'pointerdown', (e) => {
      if (this.nav !== 'look') return;
      el.setPointerCapture(e.pointerId); look.pointers.set(e.pointerId, [e.clientX, e.clientY]); look.lastPinch = 0;
    });
    on(el, 'pointermove', (e) => {
      if (this.nav !== 'look' || !look.pointers.has(e.pointerId)) return;
      const prev = look.pointers.get(e.pointerId); look.pointers.set(e.pointerId, [e.clientX, e.clientY]);
      if (look.pointers.size === 1) {
        const radPerPx = (this.camera.fov * Math.PI / 180) / Math.max(1, el.clientHeight);   // follows the lens
        look.yaw += (e.clientX - prev[0]) * radPerPx;
        look.pitch = Math.max(-1.45, Math.min(1.45, look.pitch - (e.clientY - prev[1]) * radPerPx));
        this.applyLook();
      } else if (look.pointers.size === 2) {
        const [a, b] = [...look.pointers.values()]; const dist = Math.hypot(a[0] - b[0], a[1] - b[1]);
        if (look.lastPinch) this.zoomLens(look.lastPinch / dist);
        look.lastPinch = dist;
      }
    });
    const end = (e) => { look.pointers.delete(e.pointerId); look.lastPinch = 0; };
    on(el, 'pointerup', end); on(el, 'pointercancel', end);
    on(el, 'wheel', (e) => { if (this.nav !== 'look') return; e.preventDefault(); this.zoomLens(Math.exp(e.deltaY * 0.0012)); }, { passive: false });
    on(window, 'keydown', (e) => { if (!typingIn(e) && !e.metaKey && !e.ctrlKey) this.keys.add(e.key.toLowerCase()); });
    on(window, 'keyup', (e) => this.keys.delete(e.key.toLowerCase()));
    on(window, 'blur', () => this.keys.clear());
  }
  dispose() { (this._off || []).forEach((f) => f()); this.controls.dispose(); }
}
