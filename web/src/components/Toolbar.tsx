import { useEffect, useState } from 'react';
import Icon from './Icon';
import type { Tool } from '../types';

const TOOLS: { id: Tool; icon: string; label: string; key: string; title: string }[] = [
  { id: 'orbit', icon: 'orbit', label: 'Orbit', key: 'O', title: 'Orbit (O)' },
  { id: 'pan', icon: 'pan', label: 'Pan', key: 'H', title: 'Pan (H)' },
  { id: 'zoom', icon: 'zoom', label: 'Zoom', key: 'Z', title: 'Zoom (Z)' },
  { id: 'look', icon: 'eye', label: 'Look', key: 'L', title: 'Look around (L)' },
  { id: 'tape', icon: 'tape', label: 'Tape', key: 'T', title: 'Tape measure (T)' },
];

const HINTS: Record<Tool, string> = {
  look: 'Look around (L): drag to turn your head · scroll to zoom the lens · W A S D / arrows to walk',
  orbit: 'Orbit (O): drag to rotate · scroll to zoom · right-drag or Shift-drag to pan',
  pan: 'Pan (H): drag to slide the view · scroll to zoom · right-drag to orbit',
  zoom: 'Zoom (Z): drag up/down to zoom · scroll also zooms towards the cursor',
  tape: 'Tape measure (T): click two points to measure · Esc clears · right-drag to orbit · scroll to zoom',
};

/** Navigation tools (like SketchUp) plus the photo and AI render buttons, bottom right. */
interface ToolbarProps {
  tool: Tool;
  onTool: (tool: Tool) => void;
  onFit: () => void;
  onAiRender: () => void;
  onZip: () => void;
  onPhoto: () => void;
}

export default function Toolbar({ tool, onTool, onFit, onAiRender, onZip, onPhoto }: ToolbarProps) {
  return (
    <div id="tools" className="glass">
      {TOOLS.map((t) => (
        <button key={t.id} title={t.title} className={tool === t.id ? 'on' : ''} onClick={() => onTool(t.id)}>
          <Icon name={t.icon} size={17} /> <span className="t">{t.label}</span> <kbd>{t.key}</kbd>
        </button>
      ))}
      <button title="Zoom extents (Shift+Z)" onClick={onFit}><Icon name="fit" size={17} /> <span className="t">Fit</span> <kbd>⇧Z</kbd></button>
      <button className="ai" title="Photo: path-trace this view in the browser (real light bounces, glass, reflections)" onClick={onPhoto}><Icon name="camera" size={17} /> <span className="t">Photo</span></button>
      <button className="ai" title="Photo-real render with AI" onClick={onAiRender}><Icon name="sparkles" size={17} /> <span className="t">AI render</span></button>
      <button className="ai" title="Download every scene of this plan with its ChatGPT prompt (ZIP)" onClick={onZip}><Icon name="archive" size={17} /> <span className="t">All scenes ZIP</span></button>
    </div>
  );
}

/** Short how-to for the active tool; fades out after a few seconds. */
export function ToolHint({ tool }: { tool: Tool }) {
  const [shown, setShown] = useState(false);
  useEffect(() => { setShown(true); const t = setTimeout(() => setShown(false), 6000); return () => clearTimeout(t); }, [tool]);
  return <div id="hint" className="glass" style={{ opacity: shown ? 1 : 0 }}>{HINTS[tool] || ''}</div>;
}
