import json, base64, struct, sys, zlib, math
import numpy as np
def load(js):
    D = json.load(open(js)); return D
def png(path, img):
    h, w, _ = img.shape
    raw = b''.join(b'\x00' + img[y].tobytes() for y in range(h))
    def chunk(t, d): return struct.pack('>I', len(d)) + t + d + struct.pack('>I', zlib.crc32(t + d) & 0xffffffff)
    open(path, 'wb').write(b'\x89PNG\r\n\x1a\n' + chunk(b'IHDR', struct.pack('>IIBBBBB', w, h, 8, 2, 0, 0, 0)) + chunk(b'IDAT', zlib.compress(raw, 6)) + chunk(b'IEND', b''))
def render(D, view, mode, out, W=640, H=400, hide_extra=()):
    hide = set(['Ceiling', 'Ceiling_Wood', 'Beams_Highlight', 'Structural_Highlight', 'Power_Points', 'Aircon_Trunking'] + D['modes'][mode]['hide'] + list(hide_extra))
    if view['tag'] in ('top', 'plan', 'services'): hide |= {'False_Ceiling', 'Lighting'}
    if view['tag'] == 'services': hide -= {'Power_Points', 'Aircon_Trunking'}
    eye = np.array([view['eye'][0], view['eye'][2], view['eye'][1]], float); tgt = np.array([view['target'][0], view['target'][2], view['target'][1]], float)
    if view['tag'] == 'plan': eye = np.array([tgt[0], 60000.0, tgt[2] + 1])
    f = tgt - eye; f /= np.linalg.norm(f); up = np.array([0, 1.0, 0])
    r = np.cross(f, up); r /= np.linalg.norm(r); u = np.cross(r, f)
    vf = min(view['fov'] * 0.78, 78) * math.pi / 180; fy = 1 / math.tan(vf / 2); fx = fy * H / W
    zbuf = np.full((H, W), np.inf); img = np.zeros((H, W, 3), np.uint8); img[:] = (243, 240, 234)
    light = np.array([-0.35, 0.8, -0.5]); light /= np.linalg.norm(light)
    for ch in D['chunks']:
        if ch['layer'] in hide: continue
        m = D['mats'][ch['mat']]
        q = np.frombuffer(base64.b64decode(ch['b64']), dtype='<i2').astype(float).reshape(-1, 3, 3)
        col = np.array(m['c'], float); alpha = m['a']
        n = np.cross(q[:, 1] - q[:, 0], q[:, 2] - q[:, 0]); nl = np.linalg.norm(n, axis=1) + 1e-9; n = n / nl[:, None]
        rel = q - eye
        cz = rel @ f; cx = rel @ r; cy = rel @ u
        for t in range(q.shape[0]):
            zs = cz[t]
            if (zs < 30).any(): continue
            px = (cx[t] / zs * fx + 1) * W / 2; py = (1 - cy[t] / zs * fy) * H / 2
            x0 = max(int(px.min()), 0); x1 = min(int(px.max()) + 1, W - 1); y0 = max(int(py.min()), 0); y1 = min(int(py.max()) + 1, H - 1)
            if x0 > x1 or y0 > y1: continue
            xs, ys = np.meshgrid(np.arange(x0, x1 + 1) + 0.5, np.arange(y0, y1 + 1) + 0.5)
            (ax, bx, cxx), (ay, by, cyy) = px, py
            den = (by - cyy) * (ax - cxx) + (cxx - bx) * (ay - cyy)
            if abs(den) < 1e-9: continue
            w0 = ((by - cyy) * (xs - cxx) + (cxx - bx) * (ys - cyy)) / den; w1 = ((cyy - ay) * (xs - cxx) + (ax - cxx) * (ys - cyy)) / den; w2 = 1 - w0 - w1
            ins = (w0 >= 0) & (w1 >= 0) & (w2 >= 0)
            if not ins.any(): continue
            iz = w0 / zs[0] + w1 / zs[1] + w2 / zs[2]; z = 1 / np.where(iz == 0, 1e-9, iz)
            sub = zbuf[y0:y1 + 1, x0:x1 + 1]
            vis = ins & (z < sub)
            if not vis.any(): continue
            nn = n[t]
            if nn @ (eye - q[t, 0]) < 0: nn = -nn
            shade = 0.55 + 0.45 * max(0.0, float(nn @ light)) + 0.1 * nn[1]
            c = np.clip(col * shade, 0, 255)
            if m['e']: c = np.clip(col * 1.05, 0, 255)
            reg = img[y0:y1 + 1, x0:x1 + 1]
            if alpha < 0.99:
                reg[vis] = (reg[vis] * 0.65 + c * 0.35).astype(np.uint8)
            else:
                reg[vis] = c.astype(np.uint8); sub[vis] = z[vis]
    png(out, img)
if __name__ == '__main__':
    D = load(sys.argv[1]); names = sys.argv[2].split('|'); W = int(sys.argv[3]) if len(sys.argv) > 3 else 560
    for i, v in enumerate(D['views']):
        if v['name'] in names or str(i) in names:
            render(D, v, v['mode'] or ('open' if 'open' in D['modes'] else list(D['modes'])[0]), 'r_%02d.png' % i, W, int(W * 0.62)); print('r_%02d.png' % i, v['name'])
