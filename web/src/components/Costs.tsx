import { useEffect, useRef, useState } from 'react';
import Icon from './Icon';
import { PLANS } from '../config/data';

/** Estimated cost per plan on the home page. Click an amount to see its itemised breakdown below the table. */

type Section = 'reno' | 'furniture' | 'appliances' | 'optional' | 'total';
interface Line { cat: string; item: string; qty: number; unit?: string; rate?: number; price?: number; amount: number; source: string; note: string }
interface PlanCost { reno: Line[]; furn: Line[]; optional: Line[] }
interface CostData { plans: Record<string, PlanCost> }

const SECTIONS: { key: Section; label: string }[] = [
  { key: 'reno', label: 'Renovation' },
  { key: 'furniture', label: 'Furniture' },
  { key: 'appliances', label: 'Appliances' },
  { key: 'total', label: 'Total' },
  { key: 'optional', label: 'Optional extras' },
];

export const sgd = (n: number) => 'S$' + Math.round(n).toLocaleString('en-SG');
const fmtQty = (n: number) => (Number.isInteger(n) ? String(n) : n.toFixed(1));

/** The lines that make up one section of a plan's cost, as [group title, lines] pairs. */
function groups(p: PlanCost, s: Section): [string, Line[]][] {
  const furniture = p.furn.filter((l) => l.cat !== 'Appliances');
  const appliances = p.furn.filter((l) => l.cat === 'Appliances');
  const byCat = (lines: Line[]) => {
    const m = new Map<string, Line[]>();
    lines.forEach((l) => { if (!m.has(l.cat)) m.set(l.cat, []); m.get(l.cat)!.push(l); });
    return [...m.entries()];
  };
  if (s === 'reno') return byCat(p.reno);
  if (s === 'furniture') return byCat(furniture);
  if (s === 'appliances') return [['Appliances', appliances]];
  if (s === 'optional') return [['Optional extras – not in the total', p.optional]];
  return [...byCat(p.reno), ...byCat(furniture), ['Appliances', appliances]];
}
const sum = (lines: Line[]) => lines.reduce((a, l) => a + l.amount, 0);

export default function Costs() {
  const rows = PLANS.filter((p) => p.cost);
  const [sel, setSel] = useState<{ plan: string; section: Section } | null>(null);
  const [data, setData] = useState<CostData | null>(null);
  const [err, setErr] = useState(false);
  const panel = useRef<HTMLDivElement>(null);

  // the itemised lines are only loaded once something is selected
  useEffect(() => {
    if (!sel || data) return;
    fetch('data/costs.json', { cache: 'no-cache' }).then((r) => r.json()).then(setData).catch(() => setErr(true));
  }, [sel, data]);

  const pick = (plan: string, section: Section) => {
    const same = sel && sel.plan === plan && sel.section === section;
    setSel(same ? null : { plan, section });
    if (!same && !sel) setTimeout(() => panel.current?.scrollIntoView({ behavior: 'smooth', block: 'start' }), 60);
  };

  if (!rows.length) return null;
  const low = Math.min(...rows.map((p) => p.cost!.total));
  const cell = (key: string, s: Section, v: number, bold = false) => {
    const on = sel?.plan === key && sel.section === s;
    return (
      <td className={on ? 'on' : ''}>
        <button className="amt" onClick={() => pick(key, s)} aria-pressed={on}>{bold ? <b>{sgd(v)}</b> : sgd(v)}</button>
      </td>
    );
  };
  const plan = sel && PLANS.find((p) => p.key === sel.plan);
  const pc = sel && data?.plans[sel.plan];
  const gs = pc ? groups(pc, sel!.section) : [];
  const showRate = sel?.section !== 'total';

  return (
    <section className="costs">
      <div className="chead"><h2 className="ctitle">Estimated cost</h2><span className="chint">Click any amount for the itemised breakdown</span></div>
      <div className="ctable">
        <table>
          <thead><tr><th>Plan</th>{SECTIONS.map((s) => <th key={s.key}>{s.label}</th>)}</tr></thead>
          <tbody>{rows.map((p) => {
            const c = p.cost!;
            return (
              <tr key={p.key} className={(c.total === low ? 'low ' : '') + (sel?.plan === p.key ? 'cur' : '')}>
                <td><button className="pname" onClick={() => pick(p.key, 'total')}>{p.title.replace(' – ', ' · ')}</button></td>
                {cell(p.key, 'reno', c.reno)}{cell(p.key, 'furniture', c.furniture)}{cell(p.key, 'appliances', c.appliances)}
                {cell(p.key, 'total', c.total, true)}{cell(p.key, 'optional', c.optional)}
              </tr>
            );
          })}</tbody>
        </table>
      </div>
      <p className="cnote">Renovation uses the lower rate of two contractor quotes for each kind of work, with quantities measured from each plan's model (its first layout option). Furniture and appliances are mid-range Singapore retail prices. Total = renovation + furniture + appliances; optional extras (invisible grilles, Wi-Fi access points, fridge kerb) are not included.</p>

      <div ref={panel} className={sel ? 'cpanel open' : 'cpanel'}>
        {sel && plan && (
          <>
            <div className="cphead">
              <div>
                <span className="tag mono">{plan.short}</span>
                <h3>{plan.title.replace(/^Plan [A-Z] – /, '')}</h3>
              </div>
              <button className="iconbtn" onClick={() => setSel(null)} aria-label="Close breakdown"><Icon name="close" size={18} /></button>
            </div>
            <div className="cptabs">
              <div className="seg">{SECTIONS.map((s) => (
                <button key={s.key} className={sel.section === s.key ? 'on' : ''} onClick={() => setSel({ plan: sel.plan, section: s.key })}>{s.label}</button>
              ))}</div>
              <div className="seg plans">{rows.map((p) => (
                <button key={p.key} className={sel.plan === p.key ? 'on' : ''} onClick={() => setSel({ plan: p.key, section: sel.section })}>{p.key.toUpperCase()}</button>
              ))}</div>
            </div>
            {!pc && <p className="cnote">{err ? 'Could not load the breakdown.' : 'Loading…'}</p>}
            {pc && (
              <div className="ctable lines">
                <table>
                  <thead>{showRate
                    ? <tr><th>Item</th><th>Qty</th><th>Rate</th><th>Amount</th><th className="src">Source</th></tr>
                    : <tr><th>Category</th><th /><th>Amount</th><th className="src" /></tr>}</thead>
                  {gs.map(([g, lines]) => (
                    <tbody key={g}>
                      <tr className="grp"><td colSpan={showRate ? 3 : 2}>{g}</td><td>{sgd(sum(lines))}</td><td className="src" /></tr>
                      {sel.section !== 'total' && lines.map((l, i) => (
                        <tr key={i}>
                          <td>{l.item}{l.note && <span className="lnote">{l.note}</span>}</td>
                          <td>{fmtQty(l.qty)}{l.unit && l.unit !== 'lump' ? ' ' + l.unit : ''}</td>
                          <td>{sgd(l.rate ?? l.price ?? 0)}</td>
                          <td>{sgd(l.amount)}</td>
                          <td className="src">{l.source}</td>
                        </tr>
                      ))}
                    </tbody>
                  ))}
                  <tfoot><tr><td colSpan={showRate ? 3 : 2}>{SECTIONS.find((s) => s.key === sel.section)!.label}</td><td>{sgd(gs.reduce((a, [, l]) => a + sum(l), 0))}</td><td className="src" /></tr></tfoot>
                </table>
              </div>
            )}
          </>
        )}
      </div>
    </section>
  );
}
