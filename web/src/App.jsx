// The whole app: home page + 3D viewer. State lives here; the 3D engine (engine/Viewer.js) does the drawing.
import { useCallback, useEffect, useRef, useState } from 'react';
import { Viewer } from './engine/Viewer.js';
import { PLANS, THEMES, CEILINGS, isNarrow } from './config/data.js';
import { roomOf, shortName } from './config/rooms.js';
import { buildPrompt } from './config/prompts.js';
import { optionsForView, startView } from './lib/viewOptions.js';
import { exportAllScenes } from './lib/exportScenes.js';
import { slug } from './lib/zip.js';
import { useStoredState } from './lib/useStoredState.js';
import Landing from './components/Landing.jsx';
import TopBar from './components/TopBar.jsx';
import Stepper from './components/Stepper.jsx';
import Toolbar, { ToolHint } from './components/Toolbar.jsx';
import SidePanel from './components/SidePanel.jsx';
import AiRenderDialog from './components/AiRenderDialog.jsx';
import Icon from './components/Icon.jsx';

const DEFAULT_OPTIONS = { mode: 'open', fc: true, lab: false, pwr: false, ac: false, cur: true, night: false };
const PLAN_HASH = /^#([a-z])(?:-(\d+))?$/;   // #c or #c-12 (plan C, scene 12)

export default function App() {
  // ---- 3D engine
  const stageRef = useRef(null), labelsRef = useRef(null), viewerRef = useRef(null);
  // ---- what is open
  const [landing, setLanding] = useState(true);
  const [planKey, setPlanKey] = useState(null);
  const [plan, setPlan] = useState(null);
  const [viewIndex, setViewIndex] = useState(0);
  const [opts, setOpts] = useState(DEFAULT_OPTIONS);
  const [tool, setTool] = useState('look');
  const [loading, setLoading] = useState(null);
  // ---- remembered choices
  const [theme, setTheme] = useStoredState('theme', 'lux', (v) => !!THEMES[v]);
  const [ceiling, setCeiling] = useStoredState('ceil', 'wave', (v) => !!CEILINGS[v]);
  const [hq, setHq] = useStoredState('hq', true, (v) => typeof v === 'boolean');
  // ---- layout
  const [panelOpen, setPanelOpen] = useState(false);       // narrow screens: slide-over panel
  const [panelHidden, setPanelHidden] = useState(false);   // wide screens: panel hidden for a bigger view
  const [fullView, setFullView] = useState(false);
  // ---- AI render
  const [aiImage, setAiImage] = useState(null);
  const [lighting, setLighting] = useState('day');

  // refs give event handlers the latest values without re-binding them
  const live = useRef({}); live.current = { plan, planKey, viewIndex, opts, theme, lighting };

  // ---------------------------------------------------------------- engine lifecycle
  useEffect(() => {
    const v = new Viewer(stageRef.current, labelsRef.current, { onTool: setTool, onLoading: setLoading });
    v.hq = hq; v.theme = theme; v.ceiling = ceiling;
    viewerRef.current = v;
    const ro = new ResizeObserver(() => v.resize()); ro.observe(stageRef.current);
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
  const goView = useCallback((i, { instant = false } = {}) => {
    const { plan: p, opts: o, planKey: key } = live.current; if (!p) return;
    const view = p.views[i];
    const next = optionsForView(view, o, p.modes);
    setOpts(next); viewerRef.current.setOptions(next);
    viewerRef.current.showView(view, { instant });
    setViewIndex(i);
    try { history.replaceState(null, '', `#${key}-${i}`); } catch (e) { /* ignore */ }
    if (isNarrow()) setPanelOpen(false);
  }, []);

  const stepView = useCallback((d) => {
    const { plan: p, viewIndex: i } = live.current; if (!p) return;
    goView((i + d + p.views.length) % p.views.length);
  }, [goView]);

  const openPlan = useCallback(async (key, where = {}) => {
    setLanding(false);
    let data;
    try { data = await viewerRef.current.loadPlan(key); } catch (e) { return; }
    const opts0 = { ...live.current.opts, mode: data.modes.open ? 'open' : Object.keys(data.modes)[0] };
    live.current = { ...live.current, plan: data, planKey: key, opts: opts0 };
    setPlan(data); setPlanKey(key); setOpts(opts0);
    if (!isNarrow()) setPanelOpen(true);
    goView(startView(data.views, where), { instant: true });
  }, [goView]);

  // switching plans keeps the same scene when the other plan has it (e.g. the Compare views)
  const switchPlan = (key) => {
    if (key === planKey) return;
    openPlan(key, { viewName: plan?.views[viewIndex]?.name });
  };

  const goHome = () => { setLanding(true); try { history.replaceState(null, '', '#plans'); } catch (e) { /* ignore */ } };

  // ---------------------------------------------------------------- URL: #c-12 opens plan C at scene 12
  useEffect(() => {
    const route = () => {
      const m = PLAN_HASH.exec(location.hash || '');
      if (m && PLANS.some((p) => p.key === m[1])) {
        if (m[1] !== live.current.planKey) openPlan(m[1], { viewIndex: m[2] != null ? +m[2] : null });
      } else setLanding(true);
    };
    route();
    addEventListener('hashchange', route);
    return () => removeEventListener('hashchange', route);
  }, [openPlan]);

  // ---------------------------------------------------------------- panels and full view
  const togglePanel = () => (isNarrow() ? setPanelOpen((o) => !o) : setPanelHidden((h) => !h));

  // ---------------------------------------------------------------- AI render
  const promptFor = (light) => {
    const v = viewerRef.current, { plan: p, viewIndex: i, theme: t } = live.current;
    return buildPrompt({ viewName: p.views[i].name, fromAbove: v.isAboveCeiling(), theme: t, family: v.family(), ceiling: v.ceilingDesign(), lighting: light });
  };
  const openAiRender = async () => {
    if (!plan) return;
    const url = await viewerRef.current.capture('image/png');
    const blob = await (await fetch(url)).blob();
    setAiImage({ url, blob, fileName: `plan-${planKey}-${slug(plan.views[viewIndex].name)}.png` });
  };
  const exportZip = async () => {
    setAiImage(null);
    const { plan: p, planKey: key, viewIndex: keep, opts: o, theme: t, lighting: l } = live.current; if (!p) return;
    try { await exportAllScenes(viewerRef.current, { planKey: key, opts: o, theme: t, lighting: l, onProgress: setLoading }); }
    finally { setLoading(null); goView(keep, { instant: true }); }
  };

  // ---------------------------------------------------------------- keyboard shortcuts
  useEffect(() => {
    const onKey = (e) => {
      if (['SELECT', 'INPUT', 'TEXTAREA'].includes(e.target.tagName) || e.metaKey || e.ctrlKey || e.altKey) return;
      if (!live.current.plan || landing) return;
      const k = e.key.toLowerCase(), v = viewerRef.current;
      if (k === 'z' && e.shiftKey) { v.zoomExtents(); e.preventDefault(); }
      else if (k === 'o') v.setTool('orbit');
      else if (k === 'h') v.setTool('pan');
      else if (k === 'z') v.setTool('zoom');
      else if (k === 'l') v.setTool('look');
      else if (k === 'f') setFullView((f) => !f);
      else if (k === 'escape') setFullView(false);
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
      <Landing visible={landing} onOpenPlan={(k) => openPlan(k)} onCompare={() => openPlan('a', { viewName: 'Compare 1 – living from dining' })} />
      <button id="exitFull" className="glass" title="Exit full view (F or Esc)" onClick={() => setFullView(false)}><Icon name="exitFull" /> Exit full view</button>
      <AiRenderDialog open={!!aiImage} image={aiImage} onClose={() => setAiImage(null)} makePrompt={promptFor}
        lighting={lighting} onLighting={setLighting} onZip={exportZip} />
      <div id="app">
        <div id="stage" ref={stageRef} onPointerDown={() => { if (isNarrow()) setPanelOpen(false); }}>
          <div id="loading" style={{ display: loading ? 'flex' : 'none' }}>{loading}</div>
          <TopBar planKey={planKey} room={view ? roomOf(view.name) : ''} title={view ? shortName(view.name) : ''}
            onHome={goHome} onPlan={switchPlan} onFullView={() => setFullView(true)} onTogglePanel={togglePanel}
            panelShown={isNarrow() ? panelOpen : !panelHidden} />
          <div id="labels" ref={labelsRef} />
          <Stepper index={viewIndex} total={plan?.views.length || 0} onStep={stepView} />
          <Toolbar tool={tool} onTool={(t) => viewerRef.current.setTool(t)} onFit={() => viewerRef.current.zoomExtents()}
            onAiRender={openAiRender} onZip={exportZip} />
          <ToolHint tool={tool} />
        </div>
        <SidePanel open={panelOpen} title={planTitle} plan={plan} theme={theme} onTheme={setTheme} ceiling={ceiling} onCeiling={setCeiling}
          opts={opts} onOption={(o) => setOpts((cur) => ({ ...cur, ...o }))} hq={hq} onHq={setHq}
          viewIndex={viewIndex} onView={goView} onClose={() => setPanelOpen(false)} />
      </div>
    </>
  );
}
