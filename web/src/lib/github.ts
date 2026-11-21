// Saves rendered 360° panoramas into the site's GitHub repository, so every device can show them without rendering.
// Each save is one commit holding the image and the updated pano/index.json. GitHub Pages republishes the site
// a minute or so later.
//
// Needs a fine-grained personal access token with "Contents: read and write" on this one repository.
// The token is kept in this browser only (localStorage).

export const REPO = 'Rizavur/home-layout-plans';
const BRANCH = 'main';
const API = `https://api.github.com/repos/${REPO}`;
/** Where saved panoramas are served from (the public site), so every copy of the site shares them. */
export const PANO_BASE = 'https://rizavur.github.io/home-layout-plans/';
const TOKEN_KEY = 'lvp.githubToken';

/** manifest: setup key -> point name -> file path (with a version query) */
export type PanoManifest = Record<string, Record<string, string>>;

export function getToken(): string { try { return localStorage.getItem(TOKEN_KEY) || ''; } catch { return ''; } }
export function setToken(t: string): void { try { if (t) localStorage.setItem(TOKEN_KEY, t.trim()); else localStorage.removeItem(TOKEN_KEY); } catch { /* ignore */ } }

async function gh<T>(path: string, init: RequestInit = {}): Promise<T> {
  const r = await fetch(API + path, {
    ...init,
    headers: { Accept: 'application/vnd.github+json', Authorization: `Bearer ${getToken()}`, 'X-GitHub-Api-Version': '2022-11-28', ...(init.headers || {}) },
  });
  if (!r.ok) {
    let msg = `${r.status}`;
    try { msg += ' ' + ((await r.json()) as { message?: string }).message; } catch { /* ignore */ }
    throw new Error(`GitHub: ${msg}`);
  }
  return r.json() as Promise<T>;
}

/** Check the token can write to the repository. */
export async function checkToken(): Promise<string> {
  const repo = await gh<{ full_name: string; permissions?: { push?: boolean } }>('');
  if (repo.permissions && !repo.permissions.push) throw new Error('This token cannot write to ' + repo.full_name);
  return repo.full_name;
}

function blobToBase64(b: Blob): Promise<string> {
  return new Promise((res, rej) => {
    const fr = new FileReader();
    fr.onload = () => res(String(fr.result).split(',')[1]); fr.onerror = () => rej(fr.error);
    fr.readAsDataURL(b);
  });
}
const utf8ToBase64 = (s: string) => btoa(unescape(encodeURIComponent(s)));

/** Read the current manifest straight from the repository (fresher than the published site). */
async function repoManifest(): Promise<PanoManifest> {
  try {
    const f = await gh<{ content: string }>(`/contents/pano/index.json?ref=${BRANCH}`);
    return JSON.parse(decodeURIComponent(escape(atob(f.content.replace(/\n/g, ''))))) as PanoManifest;
  } catch { return {}; }
}

/** Commit one panorama image and its manifest entry. Returns the updated manifest. */
export async function savePanorama(path: string, image: Blob, key: string, point: string, message: string): Promise<PanoManifest> {
  const ref = await gh<{ object: { sha: string } }>(`/git/ref/heads/${BRANCH}`);
  const head = await gh<{ tree: { sha: string } }>(`/git/commits/${ref.object.sha}`);
  const img = await gh<{ sha: string }>('/git/blobs', { method: 'POST', body: JSON.stringify({ content: await blobToBase64(image), encoding: 'base64' }) });
  const manifest = await repoManifest();
  (manifest[key] ||= {})[point] = `${path}?v=${Date.now().toString(36)}`;
  const man = await gh<{ sha: string }>('/git/blobs', { method: 'POST', body: JSON.stringify({ content: utf8ToBase64(JSON.stringify(manifest, null, 1)), encoding: 'base64' }) });
  const tree = await gh<{ sha: string }>('/git/trees', { method: 'POST', body: JSON.stringify({
    base_tree: head.tree.sha,
    tree: [{ path, mode: '100644', type: 'blob', sha: img.sha }, { path: 'pano/index.json', mode: '100644', type: 'blob', sha: man.sha }],
  }) });
  const commit = await gh<{ sha: string }>('/git/commits', { method: 'POST', body: JSON.stringify({ message, tree: tree.sha, parents: [ref.object.sha] }) });
  await gh(`/git/refs/heads/${BRANCH}`, { method: 'PATCH', body: JSON.stringify({ sha: commit.sha }) });
  return manifest;
}

/** The published manifest (what other devices see). */
export async function publishedManifest(): Promise<PanoManifest> {
  try {
    const r = await fetch(PANO_BASE + 'pano/index.json?t=' + Date.now(), { cache: 'no-store' });
    return r.ok ? (await r.json()) as PanoManifest : {};
  } catch { return {}; }
}
