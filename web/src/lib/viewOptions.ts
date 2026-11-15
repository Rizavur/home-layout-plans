// What a scene switches on or off when you open it.
//   night scenes   -> night mood on (and off again for other scenes)
//   services views -> power points and aircon trunking on
//   some scenes    -> a particular layout option (e.g. open kitchen, wall bed down)
import type { Mode, View, ViewOptions } from '../types';

export function optionsForView(view: View, current: ViewOptions, modes: Record<string, Mode>): ViewOptions {
  const next: ViewOptions = { ...current, night: view.tag === 'night' };
  if (view.mode && modes[view.mode]) next.mode = view.mode;
  if (view.tag === 'services') { next.pwr = true; next.ac = true; }
  return next;
}

/** Index of the scene to open first: a named scene, a scene number, or the plan view. */
export interface StartAt { viewName?: string; viewIndex?: number | null }

export function startView(views: View[], { viewName, viewIndex }: StartAt = {}): number {
  if (viewIndex != null && views[viewIndex]) return viewIndex;
  if (viewName) { const j = views.findIndex((v) => v.name === viewName); if (j >= 0) return j; }
  return Math.max(0, views.findIndex((v) => v.tag === 'plan'));
}
