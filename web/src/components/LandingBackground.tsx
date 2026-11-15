import { useEffect, useRef } from 'react';

// Slowly flowing blue/teal light behind the home page (a tiny WebGL shader).
// Half resolution and ~30 fps; pauses while the viewer is open or the tab is hidden.
const VERTEX = 'attribute vec2 p;void main(){gl_Position=vec4(p,0.,1.);}';
const FRAGMENT = `precision mediump float;uniform vec2 r;uniform float t;uniform vec2 m;
float h(vec2 p){return fract(sin(dot(p,vec2(127.1,311.7)))*43758.5453);}
float n(vec2 p){vec2 i=floor(p),f=fract(p);f=f*f*(3.-2.*f);return mix(mix(h(i),h(i+vec2(1,0)),f.x),mix(h(i+vec2(0,1)),h(i+vec2(1,1)),f.x),f.y);}
float fbm(vec2 p){float v=0.,a=.5;for(int i=0;i<5;i++){v+=a*n(p);p=p*2.03+vec2(1.7,9.2);a*=.5;}return v;}
void main(){vec2 uv=(gl_FragCoord.xy-.5*r)/r.y;vec2 q=uv+(m-.5)*.18;float T=t*.05;
  vec2 w=vec2(fbm(q*1.6+T),fbm(q*1.6-T+4.));float f=fbm(q*1.3+w*1.8+vec2(T*1.5,-T));
  float band=smoothstep(.28,.85,f)*smoothstep(1.35,.05,length(uv-vec2(.38,.18)+(m-.5)*.25));
  vec3 c1=vec3(.62,.80,1.),c2=vec3(.36,.42,.95),c3=vec3(.16,.62,.62);
  vec3 col=mix(c3,mix(c2,c1,smoothstep(.45,.85,w.x)),smoothstep(.3,.75,f));
  col*=band*1.5;col+=pow(band,4.)*.35;col+=vec3(.012,.012,.016);
  col+=(h(gl_FragCoord.xy+t)-.5)*.025;gl_FragColor=vec4(col,1.);}`;

export default function LandingBackground({ active }: { active: boolean }) {
  const ref = useRef<HTMLCanvasElement>(null);
  const activeRef = useRef(active);
  activeRef.current = active;
  const kickRef = useRef<() => void>(() => {});

  useEffect(() => {
    const cv = ref.current!;
    const gl = cv.getContext('webgl', { antialias: false, alpha: false, powerPreference: 'low-power' });
    if (!gl) { cv.style.background = 'radial-gradient(60% 50% at 70% 30%, #1d3550, #08080a)'; return undefined; }
    const shader = (type: number, src: string): WebGLShader => { const s = gl.createShader(type)!; gl.shaderSource(s, src); gl.compileShader(s); return s; };
    const prog = gl.createProgram()!;
    gl.attachShader(prog, shader(gl.VERTEX_SHADER, VERTEX)); gl.attachShader(prog, shader(gl.FRAGMENT_SHADER, FRAGMENT));
    gl.linkProgram(prog); gl.useProgram(prog);
    gl.bindBuffer(gl.ARRAY_BUFFER, gl.createBuffer());
    gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([-1, -1, 3, -1, -1, 3]), gl.STATIC_DRAW);
    const loc = gl.getAttribLocation(prog, 'p'); gl.enableVertexAttribArray(loc); gl.vertexAttribPointer(loc, 2, gl.FLOAT, false, 0, 0);
    const uR = gl.getUniformLocation(prog, 'r'), uT = gl.getUniformLocation(prog, 't'), uM = gl.getUniformLocation(prog, 'm');
    const still = matchMedia('(prefers-reduced-motion: reduce)').matches;
    let mx = 0.5, my = 0.5, tx = 0.5, ty = 0.5, last = 0, raf = 0; const t0 = performance.now();
    const onMove = (e: PointerEvent) => { tx = e.clientX / innerWidth; ty = 1 - e.clientY / innerHeight; };
    const size = () => {
      const s = 0.5 * Math.min(devicePixelRatio || 1, 2);
      cv.width = Math.max(2, innerWidth * s | 0); cv.height = Math.max(2, innerHeight * s | 0); gl.viewport(0, 0, cv.width, cv.height);
    };
    const frame = (now: number) => {
      raf = 0;
      if (!activeRef.current || document.hidden) return;
      raf = requestAnimationFrame(frame);
      if (now - last < 33) return; last = now;
      mx += (tx - mx) * 0.05; my += (ty - my) * 0.05;
      gl.uniform2f(uR, cv.width, cv.height); gl.uniform1f(uT, still ? 20 : (now - t0) / 1000 + 20); gl.uniform2f(uM, mx, my);
      gl.drawArrays(gl.TRIANGLES, 0, 3);
    };
    const kick = () => { if (!raf) raf = requestAnimationFrame(frame); };
    kickRef.current = kick;
    addEventListener('pointermove', onMove); addEventListener('resize', size); document.addEventListener('visibilitychange', kick);
    size(); kick();
    return () => {
      cancelAnimationFrame(raf);
      removeEventListener('pointermove', onMove); removeEventListener('resize', size); document.removeEventListener('visibilitychange', kick);
    };
  }, []);

  useEffect(() => { if (active) kickRef.current(); }, [active]);

  return <canvas id="fx" ref={ref} />;
}
