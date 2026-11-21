import { useRef, useState } from 'react';
import Icon from './Icon';
import type { Viewer } from '../engine/Viewer';
import { saveFile } from '../lib/save';
import { checkToken, getToken, savePanorama, setToken, REPO } from '../lib/github';

interface WalkBarProps {
  viewer: Viewer | null;
  /** bumps whenever the walk changes, so this bar redraws */
  version: number;
  planShort: string;
}

const QUALITY = {
  draft: { label: 'Draft · 2K, 96 passes', width: 2048, samples: 96 },
  standard: { label: 'Standard · 4K, 256 passes', width: 4096, samples: 256 },
  high: { label: 'High · 6K, 512 passes', width: 6144, samples: 512 },
} as const;
type Quality = keyof typeof QUALITY;

/**
 * 360° walk controls: the room points, and rendering path-traced 360° photos once (on a strong machine) and saving
 * them to the site's repository, after which every device just shows the saved photo.
 */
export default function WalkBar({ viewer, version, planShort }: WalkBarProps) {
  const [quality, setQuality] = useState<Quality>('standard');
  const [job, setJob] = useState<{ point: string; n: number; of: number; done: number; total: number } | null>(null);
  const [msg, setMsg] = useState('');
  const [keyOpen, setKeyOpen] = useState(false);
  const [keyText, setKeyText] = useState(getToken());
  const cancel = useRef(false);
  const [pending, setPending] = useState<{ blob: Blob; name: string } | null>(null);
  const lastBlob = useRef<Blob | null>(null);
  void version;
  const w = viewer?.walk;
  if (!viewer || !w || !w.active) return null;
  const here = w.points[w.idx];
  const total = w.points.length, saved = w.savedCount();

  const render = async (which: number[]) => {
    cancel.current = false; setMsg('');
    const q = QUALITY[quality];
    for (let k = 0; k < which.length; k++) {
      const i = which[k], p = w.points[i];
      if (i !== w.idx) { w.go(i, true); await new Promise((r) => setTimeout(r, 80)); }
      setJob({ point: p.name, n: k + 1, of: which.length, done: 0, total: q.samples });
      const blob = await viewer.bakePanorama(p.x, p.y, q.width, q.samples, (done, tot) => setJob((j) => (j ? { ...j, done, total: tot } : j)), () => cancel.current);
      if (!blob) { setJob(null); setMsg('Stopped.'); return; }
      const url = URL.createObjectURL(blob); lastBlob.current = blob;
      if (getToken()) {
        try {
          setJob((j) => (j ? { ...j, done: j.total } : j)); setMsg(`Saving ${p.name}…`);
          w.manifest = await savePanorama(w.filePath(i), blob, w.setupKey(), p.name, `360° photo: ${planShort} – ${p.name}`);
          w.showLocal(i, url);
          setMsg(`Saved ${p.name}. Other devices show it in about a minute.`);
        } catch (e) {
          setMsg(`Could not save to GitHub (${(e as Error).message}). Use Save below to keep it.`);
          download(url, p.name);
        }
      } else {
        download(url, p.name);
        setMsg('Ready to save. Add a GitHub key (key button) to save 360° photos for every device.');
      }
    }
    setJob(null);
  };
  // the render finished long after the tap, so phones need a fresh tap to save: keep it for the Save button
  const download = (url: string, name: string) => { void url; setPending({ blob: lastBlob.current!, name: `${planShort} – ${name} (360).jpg` }); };
  const missing = w.points.map((_, i) => i).filter((i) => !w.hasSaved(i));

  const saveKey = async () => {
    setToken(keyText);
    if (!keyText) { setKeyOpen(false); setMsg('GitHub key removed from this browser.'); return; }
    try { const name = await checkToken(); setKeyOpen(false); setMsg(`Key works – 360° photos will be saved to ${name}.`); }
    catch (e) { setMsg((e as Error).message); }
  };

  return (
    <div id="walkBar" className="glass">
      <div className="wb-head">
        <div className="wb-title">
          <span className="mono tag">360° walk</span>
          <b>{here?.name}</b>
          <span className={w.panoTex ? 'wb-chip on' : 'wb-chip'}>{w.panoTex ? 'Saved 360° photo' : 'Live 3D view'}</span>
        </div>
        <button className="wb-x" title="Leave the 360° walk" onClick={() => w.exit()}><Icon name="close" size={16} /></button>
      </div>
      <div className="wb-points">
        {w.points.map((p, i) => (
          <button key={p.name} className={(i === w.idx ? 'on ' : '') + (w.hasSaved(i) ? 'saved' : '')} onClick={() => w.go(i)} disabled={!!job}>{p.name}</button>
        ))}
      </div>
      {job ? (
        <div className="wb-job">
          <div className="wb-jt"><b>Rendering {job.point}</b><span>{job.of > 1 ? `point ${job.n} of ${job.of} · ` : ''}{job.done} / {job.total} passes</span></div>
          <div className="pb-bar"><i style={{ width: Math.round(job.done / Math.max(1, job.total) * 100) + '%' }} /></div>
          <button className="wb-btn" onClick={() => { cancel.current = true; }}>Stop</button>
        </div>
      ) : (
        <div className="wb-actions">
          <select value={quality} onChange={(e) => setQuality(e.target.value as Quality)} title="Size and number of passes of the 360° photo">
            {Object.entries(QUALITY).map(([k, q]) => <option key={k} value={k}>{q.label}</option>)}
          </select>
          <button className="wb-btn" onClick={() => void render([w.idx])} title="Path-trace a 360° photo from this point"><Icon name="camera" size={15} /> Render this point</button>
          <button className="wb-btn" onClick={() => void render(missing.length ? missing : w.points.map((_, i) => i))} title="Render every point that has no saved 360° photo yet">
            <Icon name="globe" size={15} /> Render {missing.length ? `${missing.length} missing` : 'all again'}
          </button>
          <button className={'wb-btn icon' + (getToken() ? ' ok' : '')} onClick={() => setKeyOpen((o) => !o)} title="GitHub key for saving 360° photos"><Icon name="key" size={15} /></button>
          <span className="wb-count">{saved}/{total} saved for this look</span>
        </div>
      )}
      {keyOpen && !job && (
        <div className="wb-key">
          <p>Saving needs a GitHub fine-grained token with <b>Contents: read and write</b> on <span className="mono">{REPO}</span> only. It stays in this browser.</p>
          <div className="wb-keyrow">
            <input type="password" value={keyText} placeholder="github_pat_…" onChange={(e) => setKeyText(e.target.value)} />
            <button className="wb-btn" onClick={() => void saveKey()}><Icon name="cloudUp" size={15} /> Save key</button>
          </div>
        </div>
      )}
      {msg && <p className="wb-msg">{msg}</p>}
      {pending && <div className="wb-actions"><button className="wb-btn" onClick={() => { saveFile(pending.blob, pending.name); setPending(null); }}><Icon name="download" size={15} /> Save {pending.name.split(' – ').pop()}</button></div>}
      <p className="wb-hint">Drag to look around · click a circle on the floor to walk there. Saved photos match this plan's theme, ceiling, layout option and day/night.</p>
    </div>
  );
}
