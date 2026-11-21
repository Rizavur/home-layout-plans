import Icon from './Icon';
import LandingBackground from './LandingBackground';
import { PLANS, previewUrl } from '../config/data';

/** Home page: one card per plan with its plan-view preview. */
import type { PointerEvent } from 'react';

interface LandingProps {
  visible: boolean;
  onOpenPlan: (key: string) => void;
  onCompare: () => void;
}

const sgd = (n: number) => 'S$' + Math.round(n).toLocaleString('en-SG');
const SHEET = 'https://claude.ai/artifact/TrfCXRvmeacHoa4r6398DU';

/** Estimated cost per plan: renovation (lower rate of two contractor quotes) plus furniture & appliances. */
function CostSummary() {
  const rows = PLANS.filter((p) => p.cost);
  if (!rows.length) return null;
  const low = Math.min(...rows.map((p) => p.cost!.total));
  return (
    <section className="costs">
      <div className="chead">
        <h2 className="ctitle">Estimated cost</h2>
        <a className="btn ghost" href={SHEET} target="_blank" rel="noreferrer">Itemised breakdown <span className="arr"><Icon name="arrowRight" size={16} /></span></a>
      </div>
      <div className="ctable">
        <table>
          <thead><tr><th>Plan</th><th>Renovation</th><th>Furniture &amp; appliances</th><th>Total</th></tr></thead>
          <tbody>{rows.map((p) => (
            <tr key={p.key} className={p.cost!.total === low ? 'low' : ''}>
              <td>{p.title.replace(' – ', ' · ')}</td><td>{sgd(p.cost!.reno)}</td><td>{sgd(p.cost!.items)}</td><td><b>{sgd(p.cost!.total)}</b></td>
            </tr>))}</tbody>
        </table>
      </div>
      <p className="cnote">Renovation uses the lower rate of two contractor quotes for each kind of work, with quantities measured from each plan's model (its first layout option). Furniture and appliances are mid-range Singapore retail prices. Optional extras not included: invisible grilles, Wi-Fi access points and fridge kerb, about {sgd(rows[0].cost!.optional)}.</p>
    </section>
  );
}

export default function Landing({ visible, onOpenPlan, onCompare }: LandingProps) {
  // spotlight that follows the pointer across a card
  const track = (e: PointerEvent<HTMLDivElement>) => {
    const card = (e.target as HTMLElement).closest<HTMLElement>('.card'); if (!card) return;
    const r = card.getBoundingClientRect();
    card.style.setProperty('--mx', `${e.clientX - r.left}px`); card.style.setProperty('--my', `${e.clientY - r.top}px`);
  };
  return (
    <div id="landing" className={visible ? '' : 'hidden'}>
      <LandingBackground active={visible} />
      <div id="vignette" /><div id="grain" />
      <div className="lwrap">
        <div className="topline">
          <h1 className="site">Lakeside View Plans</h1>
          <button className="btn ghost" onClick={onCompare}>Compare living rooms <span className="arr"><Icon name="arrowRight" size={16} /></span></button>
        </div>
        <div id="cards" onPointerMove={track}>
          {PLANS.map((p, n) => (
            <button key={p.key} className={p.tint ? `card tint-${p.tint}` : 'card'} style={{ animationDelay: `${0.25 + n * 0.08}s` }} onClick={() => onOpenPlan(p.key)}>
              <div className="shot"><img src={previewUrl(p.key)} alt={`${p.title} – plan view`} decoding="async" /></div>
              <div className="body">
                <span className="tag mono">{p.short}</span>
                <h3>{p.title.replace(/^Plan [A-Z] – /, '')}</h3>
                <ul>{p.bullets.map((b) => <li key={b}>{b}</li>)}</ul>
                {p.cost && <div className="cost mono"><span>Est. total</span><b>{sgd(p.cost.total)}</b></div>}
                <span className="go">Open plan <span className="arr"><Icon name="arrowRight" size={16} /></span></span>
              </div>
            </button>
          ))}
        </div>
        <CostSummary />
        <p className="fine">Browser mock-ups – furniture is simplified compared with the SketchUp files. Power points and aircon trunking are indicative only. Removing the kitchen front wall (open-kitchen options) must be confirmed with HDB / your ID.</p>
      </div>
    </div>
  );
}
