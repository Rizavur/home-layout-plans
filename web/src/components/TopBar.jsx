import Icon from './Icon.jsx';
import { PLANS } from '../config/data.js';

/** Top of the viewer: home, plan letters, current scene, full view, and the button that shows / hides the side panel. */
export default function TopBar({ planKey, room, title, onHome, onPlan, onFullView, onTogglePanel, panelShown }) {
  return (
    <div id="topbar">
      <button id="homeBtn" className="glass" title="All plans" onClick={onHome}><Icon name="home" size={19} /></button>
      <div id="planPills" className="glass">
        {PLANS.map((p) => (
          <button key={p.key} title={p.title} className={p.key === planKey ? 'on' : ''} onClick={() => onPlan(p.key)}>{p.key.toUpperCase()}</button>
        ))}
      </div>
      <div id="titleWrap" className="glass">
        <div id="viewRoom">{room}</div>
        {/* key restarts the little swap animation whenever the scene changes */}
        <div id="title" key={title} className="swap">{title}</div>
      </div>
      <button id="fullBtn" className="glass" title="Full view (F)" onClick={onFullView}><Icon name="fullView" /></button>
      <button id="toggle" className={'glass' + (panelShown ? ' on' : '')} onClick={onTogglePanel}><Icon name="menu" /> Views</button>
    </div>
  );
}
