import { useEffect, useState } from 'react';
import Icon from './Icon.jsx';

const TOOLS = [
  { id: 'orbit', icon: 'orbit', label: 'Orbit', key: 'O', title: 'Orbit (O)' },
  { id: 'pan', icon: 'pan', label: 'Pan', key: 'H', title: 'Pan (H)' },
  { id: 'zoom', icon: 'zoom', label: 'Zoom', key: 'Z', title: 'Zoom (Z)' },
  { id: 'look', icon: 'eye', label: 'Look', key: 'L', title: 'Look around (L)' },
];

const HINTS = {
  look: 'Look around (L): drag to turn your head · scroll to zoom the lens · W A S D / arrows to walk',
  orbit: 'Orbit (O): drag to rotate · scroll to zoom · right-drag or Shift-drag to pan',
  pan: 'Pan (H): drag to slide the view · scroll to zoom · right-drag to orbit',
  zoom: 'Zoom (Z): drag up/down to zoom · scroll also zooms towards the cursor',
};

/** Navigation tools (like SketchUp) plus the AI render buttons, bottom right. */
export default function Toolbar({ tool, onTool, onFit, onAiRender, onZip }) {
  return (
    <div id="tools" className="glass">
      {TOOLS.map((t) => (
        <button key={t.id} title={t.title} className={tool === t.id ? 'on' : ''} onClick={() => onTool(t.id)}>
          <Icon name={t.icon} size={17} /> <span className="t">{t.label}</span> <kbd>{t.key}</kbd>
        </button>
      ))}
      <button title="Zoom extents (Shift+Z)" onClick={onFit}><Icon name="fit" size={17} /> <span className="t">Fit</span> <kbd>⇧Z</kbd></button>
      <button className="ai" title="Photo-real render with AI" onClick={onAiRender}><Icon name="sparkles" size={17} /> <span className="t">AI render</span></button>
      <button className="ai" title="Download every scene of this plan with its ChatGPT prompt (ZIP)" onClick={onZip}><Icon name="archive" size={17} /> <span className="t">All scenes ZIP</span></button>
    </div>
  );
}

/** Short how-to for the active tool; fades out after a few seconds. */
export function ToolHint({ tool }) {
  const [shown, setShown] = useState(false);
  useEffect(() => { setShown(true); const t = setTimeout(() => setShown(false), 6000); return () => clearTimeout(t); }, [tool]);
  return <div id="hint" className="glass" style={{ opacity: shown ? 1 : 0 }}>{HINTS[tool] || ''}</div>;
}
