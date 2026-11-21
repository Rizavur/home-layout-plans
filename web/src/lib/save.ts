// Saving a file in a way that works on phones too.
// iPhone / iPad Safari ignore <a download> for images (or open them in a dead tab), so on touch devices the image goes to
// the share sheet instead ("Save Image" puts it in Photos). Must run straight from a tap: no awaits before calling it.

const isTouch = () => matchMedia('(pointer: coarse)').matches || /iPhone|iPad|iPod|Android/.test(navigator.userAgent);

function toBlob(data: Blob | string): Blob {
  if (typeof data !== 'string') return data;
  const [head, b64] = data.split(','); const mime = /:(.*?);/.exec(head)?.[1] || 'application/octet-stream';
  const bin = atob(b64), arr = new Uint8Array(bin.length);
  for (let i = 0; i < bin.length; i++) arr[i] = bin.charCodeAt(i);
  return new Blob([arr], { type: mime });
}

export function saveFile(data: Blob | string, name: string): void {
  const blob = toBlob(data), clean = name.replace(/[\\/:*?"<>|]/g, '');
  const file = new File([blob], clean, { type: blob.type });
  const nav = navigator as Navigator & { canShare?: (d: object) => boolean };
  if (isTouch() && nav.share && nav.canShare?.({ files: [file] })) {
    nav.share({ files: [file], title: clean }).catch((e: Error) => { if (e.name !== 'AbortError') anchor(blob, clean); });
    return;
  }
  anchor(blob, clean);
}

function anchor(blob: Blob, name: string): void {
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a'); a.href = url; a.download = name; a.rel = 'noopener';
  document.body.appendChild(a); a.click(); a.remove();
  setTimeout(() => URL.revokeObjectURL(url), 60000);
}
