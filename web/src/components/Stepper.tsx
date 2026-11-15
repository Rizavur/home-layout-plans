import Icon from './Icon';

/** Prev / Next through the scenes of the open plan. */
interface StepperProps { index: number; total: number; onStep: (delta: number) => void }

export default function Stepper({ index, total, onStep }: StepperProps) {
  return (
    <div id="stepper" className="glass">
      <button id="prevView" title="Previous view ( [ )" onClick={() => onStep(-1)}><Icon name="chevronLeft" size={16} /> Prev</button>
      <span className="count">{total ? `${index + 1} / ${total}` : ''}</span>
      <button id="nextView" title="Next view ( ] )" onClick={() => onStep(1)}>Next <Icon name="chevronRight" size={16} /></button>
    </div>
  );
}
