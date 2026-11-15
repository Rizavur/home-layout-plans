// Groups scenes by room for the side panel, and turns scene names into short labels.
// A scene name looks like "Living – TV wall": the part before " – " is the area.

import type { View } from '../types';

export const ROOMS: [string, RegExp][] = [
  ['Overview & compare', /^(Overview|Plan|Compare|Services)/],
  ['Living room', /^(Living|Night – living)/],
  ['Lounge & hall', /^(Lounge|Hall|Entry|Entrance|TV corner)/],
  ['Study', /^Study|Study door/],
  ['Dining & dry pantry', /^(Dining|Dry pantry)/],
  ['Kitchen', /kitchen/i],
  ['Foyer & household shelter', /^(Foyer|Household shelter)/],
  ['Bedroom 3', /^Bedroom 3/],
  ['Bedroom 2 (kids)', /^Bedroom 2/],
  ['Master bedroom', /^(Master|Night – master)/],
  ['Bathrooms', /(bathroom|Ensuite)/i],
  ['Service yard', /^Service yard/],
];

/** Which room group a scene belongs to. */
export function roomOf(name: string): string {
  for (const [group, re] of ROOMS) if (re.test(name)) return group;
  return 'Other';
}

const AREA_PREFIX = /^(Living|Lounge|Study nook|Study room|Study|Dining|Foyer|Master|Bedroom [23]|Open kitchen|Closed kitchen|Kitchen|Hall|Entrance screen|Night|Compare \d) – /;

/** "Living – TV wall" -> "TV wall" (the room is already shown as the group / heading). */
export function shortName(name: string): string {
  const s = name.replace(AREA_PREFIX, '');
  return s.charAt(0).toUpperCase() + s.slice(1);
}

/** Scenes grouped by room, in panel order: [[group, [viewIndex, ...]], ...] */
export function groupViews(views: View[]): [string, number[]][] {
  const groups = new Map<string, number[]>(ROOMS.map(([g]) => [g, []]));
  views.forEach((v, i) => {
    const g = roomOf(v.name);
    if (!groups.has(g)) groups.set(g, []);
    groups.get(g)!.push(i);
  });
  return [...groups].filter(([, idx]) => idx.length);
}
