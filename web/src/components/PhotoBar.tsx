import Icon from './Icon';

interface PhotoBarProps {
  /** samples traced so far and the target, or null when no photo is running */
  progress: { samples: number; target: number } | null;
  onSave: () => void;
  onClose: () => void;
}

/** Progress of a path-traced photo, with Save and Close. Moving the camera also closes it. */
export default function PhotoBar({ progress, onSave, onClose }: PhotoBarProps) {
  if (!progress) return null;
  const pct = Math.min(100, Math.round(progress.samples / Math.max(1, progress.target) * 100));
  const done = progress.samples >= progress.target;
  return (
    <div id="photoBar" className="glass">
      <div className="pb-txt">
        <b>{done ? 'Photo ready' : 'Rendering photo…'}</b>
        <span>{done ? 'Save it, or move the camera to go back' : `${progress.samples} / ${progress.target} passes · keep still, it sharpens as it goes`}</span>
        <div className="pb-bar"><i style={{ width: pct + '%' }} /></div>
      </div>
      <button className="pb-save" onClick={onSave} title="Save the image"><Icon name="download" size={16} /> Save</button>
      <button className="pb-close" onClick={onClose} title="Back to the normal view"><Icon name="close" size={16} /></button>
    </div>
  );
}
