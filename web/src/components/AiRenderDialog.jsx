import { useEffect, useState } from 'react';
import Icon from './Icon.jsx';
import { LIGHTING } from '../config/prompts.js';

/** Briefly swap a button's label, e.g. "Copied". */
function useFlash() {
  const [flash, setFlash] = useState(null);
  const show = (id, text) => { setFlash({ id, text }); setTimeout(() => setFlash(null), 1600); };
  const label = (id, normal) => (flash?.id === id ? flash.text : normal);
  return [show, label];
}

/**
 * Screenshot of the current scene + a ready-made prompt for ChatGPT.
 * @param {{ open, onClose, image: {url, blob, fileName}|null, makePrompt: (lighting) => string, lighting, onLighting, onZip }} props
 */
export default function AiRenderDialog({ open, onClose, image, makePrompt, lighting, onLighting, onZip }) {
  const [prompt, setPrompt] = useState('');
  const [flash, label] = useFlash();
  useEffect(() => { if (open) setPrompt(makePrompt(lighting)); }, [open, lighting]);   // eslint-disable-line react-hooks/exhaustive-deps

  if (!open || !image) return null;
  const file = new File([image.blob], image.fileName, { type: 'image/png' });
  const canShare = !!(navigator.canShare && navigator.canShare({ files: [file] }));

  const copyPrompt = async () => {
    try { await navigator.clipboard.writeText(prompt); flash('prompt', 'Copied'); } catch (e) { flash('prompt', 'Press Ctrl+C'); }
  };
  const copyImage = async () => {
    try { await navigator.clipboard.write([new ClipboardItem({ 'image/png': image.blob })]); flash('img', 'Copied'); } catch (e) { flash('img', 'Use Download'); }
  };
  const download = () => {
    const a = document.createElement('a'); a.href = URL.createObjectURL(image.blob); a.download = image.fileName; a.click();
    setTimeout(() => URL.revokeObjectURL(a.href), 4000);
  };
  const share = async () => { try { await navigator.share({ files: [file], text: prompt }); } catch (e) { /* cancelled */ } };

  return (
    <div id="aiModal" className="open" onPointerDown={(e) => { if (e.target.id === 'aiModal') onClose(); }}>
      <div className="aibox">
        <header>
          <div><div className="sub">AI render</div><h3>Photo-real image with ChatGPT</h3></div>
          <button className="iconbtn" title="Close" onClick={onClose}><Icon name="close" /></button>
        </header>
        <div className="aigrid">
          <div className="aishot">
            <img src={image.url} alt="Screenshot of the current view" />
            <div className="aiact">
              <button onClick={copyImage}><Icon name="photo" size={16} /> {label('img', 'Copy image')}</button>
              <button onClick={download}><Icon name="download" size={16} /> Download</button>
              {canShare && <button onClick={share}><Icon name="share" size={16} /> Share</button>}
            </div>
          </div>
          <div className="aitext">
            <label className="ailbl">Lighting
              <select value={lighting} onChange={(e) => onLighting(e.target.value)}>
                {Object.entries(LIGHTING).map(([k, [name]]) => <option key={k} value={k}>{name}</option>)}
              </select>
            </label>
            <textarea id="aiPrompt" spellCheck="false" value={prompt} onChange={(e) => setPrompt(e.target.value)} />
            <div className="aiact">
              <button className="pri" onClick={copyPrompt}><Icon name="clipboard" size={16} /> {label('prompt', 'Copy prompt')}</button>
              <button onClick={onZip}><Icon name="archive" size={16} /> All scenes (ZIP)</button>
              <a className="btnlink" href="https://chatgpt.com/" target="_blank" rel="noopener noreferrer"><Icon name="external" size={16} /> Open ChatGPT</a>
            </div>
            <ol className="aisteps">
              <li>Copy or download the image and paste it into a new ChatGPT chat.</li>
              <li>Copy the prompt, paste it in the same message and send.</li>
              <li>Ask for tweaks in follow-up messages, e.g. "warmer light" or "add a plant".</li>
            </ol>
          </div>
        </div>
      </div>
    </div>
  );
}
