import Icon from './Icon.jsx';
import ViewList from './ViewList.jsx';
import { THEMES, CEILINGS } from '../config/data.js';

const TOGGLES = [
  ['fc', 'False ceiling & lights'],
  ['lab', 'Room names & dimensions'],
  ['pwr', 'Power points'],
  ['ac', 'Aircon trunking'],
  ['cur', 'Curtains'],
  ['night', 'Night mood'],
];

/**
 * Right-hand panel: theme, false-ceiling design, layout option, what to show, scenes by room, notes.
 * `open` is for narrow screens (slide-over); on wide screens App hides the whole panel instead.
 */
export default function SidePanel({ open, title, plan, theme, onTheme, ceiling, onCeiling, opts, onOption, hq, onHq, viewIndex, onView, onClose }) {
  const ceilings = Object.entries(CEILINGS).filter(([k]) => k === 'wave' || plan?.ceils?.includes(k));
  return (
    <aside id="panel" className={open ? '' : 'closed'}>
      <header>
        <div><div className="sub">Layout</div><h1 id="panelTitle">{title}</h1></div>
        <button id="panelClose" title="Close" onClick={onClose}><Icon name="close" /></button>
      </header>
      <div id="scroll">
        <div className="sec">Theme</div>
        <div id="themes">
          {Object.entries(THEMES).map(([k, t]) => (
            <button key={k} className={k === theme ? 'on' : ''} onClick={() => onTheme(k)}>
              <span className="sw">{t.sw.map((c) => <i key={c} style={{ background: c }} />)}</span>{t.name}
            </button>
          ))}
        </div>

        <div className="sec">False ceiling</div>
        <div id="ceils">
          {ceilings.map(([k, name]) => <button key={k} className={k === ceiling ? 'on' : ''} onClick={() => onCeiling(k)}>{name}</button>)}
        </div>

        <div className="sec">{plan?.modeLabel || 'Layout option'}</div>
        <select id="mode" value={opts.mode} onChange={(e) => onOption({ mode: e.target.value })}>
          {plan && Object.entries(plan.modes).map(([k, m]) => <option key={k} value={k}>{m.label}</option>)}
        </select>

        <div className="sec">Show</div>
        <div className="switches">
          {TOGGLES.map(([k, label]) => (
            <label key={k} className="tg">{label}<input type="checkbox" checked={!!opts[k]} onChange={(e) => onOption({ [k]: e.target.checked })} /></label>
          ))}
          <label className="tg">High-quality rendering<input type="checkbox" checked={hq} onChange={(e) => onHq(e.target.checked)} /></label>
        </div>

        <div className="sec">Views by room</div>
        {plan && <ViewList views={plan.views} current={viewIndex} onSelect={onView} />}

        <div className="sec">About this plan</div>
        <div className="info" id="info">{plan?.info}</div>
      </div>
    </aside>
  );
}
