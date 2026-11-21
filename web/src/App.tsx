// The whole app: home page + 3D viewer. State lives here; the 3D engine (engine/Viewer.js) does the drawing.
import { useCallback, useEffect, useRef, useState } from 'react';
import { Viewer } from './engine/Viewer';
import { PLANS, THEMES, CEILINGS, isNarrow } from './config/data';
import { roomOf, shortName } from './config/rooms';
import { buildPrompt } from './config/prompts';
import { optionsForView, startView } from './lib/viewOptions';
import { exportAllScenes } from './lib/exportScenes';
import { slug } from './lib/zip';
import { useStoredState } from './lib/useStoredState';
import Landing from './components/Landing';
import TopBar from './components/TopBar';
import Stepper from './components/Stepper';
import Toolbar, { ToolHint } from './components/Toolbar';
import PhotoBar from './components/PhotoBar';
import WalkBar from './components/WalkBar';
import SidePanel from './components/SidePanel';
import AiRenderDialog from './components/AiRenderDialog';
import Icon from './components/Icon';
import type { Screenshot } from './components/AiRenderDialog';
import type { Lighting, PlanData, Tool, ViewOptions } from './types';
import type { StartAt } from './lib/viewOptions';

const DEFAULT_OPTIONS: ViewOptions = { mode: 'open', fc: true, lab: false, pwr: false, ac: false, cur: true, night: false, wood: false };
const PLAN_HASH = /^#([a-z])(?:-(\d+))?$/;   // #c or #c-12 (plan C, scene 12)

export default function App() {
  // ---- 3D engine
  const stageRef = useRef<HTMLDivElement>(null), labelsRef = useRef<HTMLDivElement>(null), viewerRef = useRef<Viewer | null>(null);
  // ---- what is open
  const [landing, setLanding] = useState(true);
  const [planKey, setPlanKey] = useState<string | null>(null);
  const [plan, setPlan] = useState<PlanData | null>(null);
  const [viewIndex, setViewIndex] = useState(0);
  const [opts, setOpts] = useState(DEFAULT_OPTIONS);
  const [tool, setTool] = useState<Tool>('look');
  const [loading, setLoading] = useState<string | null>(null);
  const [photo, setPhoto] = useState<{ samples: number; target: number } | null>(null);
  const [walkVersion, setWalkVersion] = useState(0);
  // ---- remembered choices
  const [theme, setTheme] = useStoredState<string>('theme', 'lux', (v) => typeof v === 'string' && !!THEMES[v]);
  const [ceiling, setCeiling] = useStoredState<string>('ceil', 'wave', (v) => typeof v === 'string' && !!CEILINGS[v]);
  const [hq, setHq] = useStoredState<boolean>('hq', true, (v) => typeof v === 'boolean');
  // ---- layout
  const [panelOpen, setPanelOpen] = useState(false);       // narrow screens: slide-over panel
  const [panelHidden, setPanelHidden] = useState(false);   // wide screens: panel hidden for a bigger view
  const [fullView, setFullView] = useState(false);
  // ---- AI render
  const [aiImage, setAiImage] = useState<Screenshot | null>(null);
  const [lighting, setLighting] = useState<Lighting>('day');

  // refs give event handlers the latest values without re-binding them
  const live = useRef({ plan, planKey, viewIndex, opts, theme, lighting });
  live.current = { plan, planKey, viewIndex, opts, theme, lighting };

  // ---------------------------------------------------------------- engine lifecycle
  useEffect(() => {
    const v = new Viewer(stageRef.current!, labelsRef.current!, { onTool: setTool, onLoading: setLoading, onPhoto: (s, t) => setPhoto(s === null ? null : { samples: s, target: t }), onWalk: () => setWalkVersion((n) => n + 1) });
    v.hq = hq; v.theme = theme; v.ceiling = ceiling;
    viewerRef.current = v;
    (window as unknown as { __viewer?: Viewer }).__viewer = v;   // handy for debugging in the browser console
    const ro = new ResizeObserver(() => v.resize()); ro.observe(stageRef.current!);
    return () => { ro.disconnect(); v.dispose(); };
  }, []);   // eslint-disable-line react-hooks/exhaustive-deps

  useEffect(() => { viewerRef.current?.setTheme(theme); }, [theme]);
  useEffect(() => { viewerRef.current?.setCeiling(ceiling); }, [ceiling]);
  useEffect(() => { viewerRef.current?.setOptions(opts); }, [opts]);
  useEffect(() => {
    const v = viewerRef.current; if (!v || v.hq === hq) return;
    v.setHQ(hq); const { plan: p, viewIndex: i } = live.current; if (p) v.showView(p.views[i], { instant: true });
  }, [hq]);

  // page-level classes used by the stylesheet
  useEffect(() => {
    const b = document.body.classList;
    b.toggle('night', opts.night); b.toggle('full', fullView); b.toggle('nopanel', panelHidden);
  }, [opts.night, fullView, panelHidden]);

  // ---------------------------------------------------------------- scenes
  const goView = useCallback((i: number, { instant = false }: { instant?: boolean } = {}) => {
    const { plan: p, opts: o, planKey: key } = live.current; const v = viewerRef.current; if (!p || !v) return;
    const view = p.views[i];
    const next = optionsForView(view, o, p.modes);
    setOpts(next); v.setOptions(next);
    v.showView(view, { instant });
    setViewIndex(i);
    try { history.replaceState(null, '', `#${key}-${i}`); } catch { /* ignore */ }
    if (isNarrow()) setPanelOpen(false);
  }, []);

  const stepView = useCallback((d: number) => {
    const { plan: p, viewIndex: i } = live.current; if (!p) return;
    goView((i + d + p.views.length) % p.views.length);
  }, [goView]);

  const openPlan = useCallback(async (key: string, where: StartAt = {}) => {
    setLanding(false);
    let data: PlanData;
    try { data = await viewerRef.current!.loadPlan(key); } catch { return; }
    const opts0: ViewOptions = { ...live.current.opts, mode: data.modes.open ? 'open' : Object.keys(data.modes)[0] };
    live.current = { ...live.current, plan: data, planKey: key, opts: opts0 };
    setPlan(data); setPlanKey(key); setOpts(opts0);
    if (!isNarrow()) setPanelOpen(true);
    goView(startView(data.views, where), { instant: true });
  }, [goView]);

  // switching plans keeps the same scene when the other plan has it (e.g. the Compare views)
  const switchPlan = (key: string) => {
    if (key === planKey) return;
    openPlan(key, { viewName: plan?.views[viewIndex]?.name });
  };

  const goHome = () => { setLanding(true); try { history.replaceState(null, '', '#plans'); } catch { /* ignore */ } };

  // ---------------------------------------------------------------- URL: #c-12 opens plan C at scene 12
  useEffect(() => {
    const route = () => {
      const m = PLAN_HASH.exec(location.hash || '');
      if (m && PLANS.some((p) => p.key === m[1])) {
        if (m[1] !== live.current.planKey) void openPlan(m[1], { viewIndex: m[2] != null ? +m[2] : null });
      } else setLanding(true);
    };
    route();
    addEventListener('hashchange', route);
    return () => removeEventListener('hashchange', route);
  }, [openPlan]);

  // ---------------------------------------------------------------- panels and full view
  const togglePanel = () => (isNarrow() ? setPanelOpen((o) => !o) : setPanelHidden((h) => !h));

  // ---------------------------------------------------------------- AI render
  const promptFor = (light: Lighting): string => {
    const v = viewerRef.current!, { plan: p, viewIndex: i, theme: t } = live.current;
    if (!p) return '';
    return buildPrompt({ viewName: p.views[i].name, fromAbove: v.isAboveCeiling(), theme: t, family: v.family(), ceiling: v.ceilingDesign(), lighting: light });
  };
  const openAiRender = async () => {
    if (!plan || !planKey) return;
    const url = await viewerRef.current!.capture('image/png');
    const blob = await (await fetch(url)).blob();
    setAiImage({ url, blob, fileName: `plan-${planKey}-${slug(plan.views[viewIndex].name)}.png` });
  };
  const startPhoto = async () => {
    const v = viewerRef.current; if (!v) return;
    try { await v.startPhoto(); }
    catch (e) { console.error(e); alert('Photo mode could not start on this device (it needs WebGL 2). Try the AI render button instead.'); }
  };
  const savePhoto = async () => {
    const v = viewerRef.current; if (!v) return;
    const url = await v.capture('image/png');
    const name = `${PLANS.find((p) => p.key === planKey)?.short || 'Plan'} – ${plan?.views[viewIndex]?.name || 'view'} (photo).png`;
    const a = document.createElement('a'); a.href = url; a.download = name.replace(/[\\/:*?"<>|]/g, ''); a.click();
  };

  const exportZip = async () => {
    setAiImage(null);
    const { plan: p, planKey: key, viewIndex: keep, opts: o, theme: t, lighting: l } = live.current; if (!p || !key) return;
    try { await exportAllScenes(viewerRef.current!, { planKey: key, opts: o, theme: t, lighting: l, onProgress: setLoading }); }
    finally { setLoading(null); goView(keep, { instant: true }); }
  };

  // ---------------------------------------------------------------- keyboard shortcuts
  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      if (['SELECT', 'INPUT', 'TEXTAREA'].includes((e.target as HTMLElement).tagName) || e.metaKey || e.ctrlKey || e.altKey) return;
      const v = viewerRef.current;
      if (!live.current.plan || landing || !v) return;
      const k = e.key.toLowerCase();
      if (k === 'z' && e.shiftKey) { v.zoomExtents(); e.preventDefault(); }
      else if (k === 'o') v.setTool('orbit');
      else if (k === 'h') v.setTool('pan');
      else if (k === 'z') v.setTool('zoom');
      else if (k === 'l') v.setTool('look');
      else if (k === 't') v.setTool('tape');
      else if (k === 'f') setFullView((f) => !f);
      else if (k === 'escape') { v.clearMeasurements(); setFullView(false); }
      else if (k === ']' || k === 'pagedown') { stepView(1); e.preventDefault(); }
      else if (k === '[' || k === 'pageup') { stepView(-1); e.preventDefault(); }
    };
    addEventListener('keydown', onKey);
    return () => removeEventListener('keydown', onKey);
  }, [landing, stepView]);

  // ---------------------------------------------------------------- render
  const view = plan?.views[viewIndex];
  const planTitle = PLANS.find((p) => p.key === planKey)?.title || 'Plan';
  return (
    <>
      <Landing visible={landing} onOpenPlan={(k) => void openPlan(k)} onCompare={() => void openPlan('a', { viewName: 'Compare 1 – living from dining' })} />
      <button id="exitFull" className="glass" title="Exit full view (F or Esc)" onClick={() => setFullView(false)}><Icon name="exitFull" /> Exit full view</button>
      <AiRenderDialog open={!!aiImage} image={aiImage} onClose={() => setAiImage(null)} makePrompt={promptFor}
        lighting={lighting} onLighting={setLighting} onZip={() => void exportZip()} />
      <div id="app">
        <div id="stage" ref={stageRef} onPointerDown={() => { if (isNarrow()) setPanelOpen(false); }}>
          <div id="loading" style={{ display: loading ? 'flex' : 'none' }}>{loading}</div>
          <TopBar planKey={planKey} room={view ? roomOf(view.name) : ''} title={view ? shortName(view.name) : ''}
            onHome={goHome} onPlan={switchPlan} onFullView={() => setFullView(true)} onTogglePanel={togglePanel}
            panelShown={isNarrow() ? panelOpen : !panelHidden} />
          <div id="labels" ref={labelsRef} />
          <Stepper index={viewIndex} total={plan?.views.length || 0} onStep={stepView} />
          <Toolbar tool={tool} onTool={(t) => viewerRef.current?.setTool(t)} onFit={() => viewerRef.current?.zoomExtents()}
            onAiRender={() => void openAiRender()} onZip={() => void exportZip()} onPhoto={() => void startPhoto()} onWalk={() => viewerRef.current?.walk.enter()} />
          <ToolHint tool={tool} />
          <WalkBar viewer={viewerRef.current} version={walkVersion} planShort={PLANS.find((p) => p.key === planKey)?.short || 'Plan'} />
          <PhotoBar progress={photo} onSave={() => void savePhoto()} onClose={() => viewerRef.current?.stopPhoto()} />
        </div>
        <SidePanel open={panelOpen} title={planTitle} plan={plan} theme={theme} onTheme={setTheme} ceiling={ceiling} onCeiling={setCeiling}
          opts={opts} onOption={(o) => setOpts((cur) => ({ ...cur, ...o }))} hq={hq} onHq={setHq}
          viewIndex={viewIndex} onView={goView} onClose={() => setPanelOpen(false)} />
      </div>
    </>
  );
}
