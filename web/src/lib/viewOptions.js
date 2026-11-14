// What a scene switches on or off when you open it.
//   night scenes   -> night mood on (and off again for other scenes)
//   plan views     -> room names & dimensions on
//   services views -> power points and aircon trunking on
//   some scenes    -> a particular layout option (e.g. open kitchen, wall bed down)
export function optionsForView(view, current, modes) {
  const next = { ...current, night: view.tag === 'night' };
  if (view.mode && modes[view.mode]) next.mode = view.mode;
  if (view.tag === 'plan') next.lab = true;
  if (view.tag === 'services') { next.pwr = true; next.ac = true; }
  return next;
}

/** Index of the scene to open first: a named scene, a scene number, or the plan view. */
export function startView(views, { viewName, viewIndex } = {}) {
  if (viewIndex != null && views[viewIndex]) return viewIndex;
  if (viewName) { const j = views.findIndex((v) => v.name === viewName); if (j >= 0) return j; }
  return Math.max(0, views.findIndex((v) => v.tag === 'plan'));
}
