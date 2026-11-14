import { useEffect, useState } from 'react';
import { groupViews, roomOf, shortName } from '../config/rooms.js';

/** Scenes grouped by room. One group is open at a time; it follows the current scene. */
export default function ViewList({ views, current, onSelect }) {
  const groups = groupViews(views);
  const currentGroup = views[current] ? roomOf(views[current].name) : null;
  const [open, setOpen] = useState(currentGroup);
  useEffect(() => { setOpen(currentGroup); }, [currentGroup]);
  return (
    <div className="views" id="views">
      {groups.map(([group, indices]) => (
        <div key={group} className={'vgroup' + (open === group ? ' open' : '')}>
          <button className="vhead" onClick={() => setOpen(open === group ? null : group)}>
            <span>{group}</span><em>{indices.length}</em>
          </button>
          <div className="vlist"><div className="inner">
            {indices.map((i) => (
              <button key={i} title={views[i].name} className={i === current ? 'on' : ''} onClick={() => onSelect(i)}>{shortName(views[i].name)}</button>
            ))}
          </div></div>
        </div>
      ))}
    </div>
  );
}
