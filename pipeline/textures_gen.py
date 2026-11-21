"""Generates the tileable material textures used by the viewer's realistic mode (assets/tex/*.jpg).

Every texture is a *detail* map: the colour still comes from the theme, the texture multiplies it.
Each map is tileable because all noise is built in the frequency domain (FFT), which wraps by construction.
Run:  python3 textures_gen.py      (writes ../assets/tex and prints the mean brightness of each map)
"""
import json, os
import numpy as np
from PIL import Image

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'assets', 'tex')
rng = np.random.default_rng(7)


def noise(n, lo, hi, aniso=(1.0, 1.0), seed=None):
    """Band-limited periodic noise (zero mean, unit std). lo/hi = frequency band in cycles per tile."""
    r = np.random.default_rng(seed) if seed is not None else rng
    w = r.standard_normal((n, n))
    fy = np.fft.fftfreq(n)[:, None] * n * aniso[1]
    fx = np.fft.fftfreq(n)[None, :] * n * aniso[0]
    f = np.sqrt(fx * fx + fy * fy)
    filt = np.exp(-(f / hi) ** 2) * (1 - np.exp(-(f / max(lo, 1e-3)) ** 2))
    a = np.real(np.fft.ifft2(np.fft.fft2(w) * filt))
    return (a - a.mean()) / (a.std() + 1e-9)


def fbm(n, base, octaves=5, gain=0.5, aniso=(1, 1), seed=None):
    a = np.zeros((n, n)); amp = 1.0; f = base
    for k in range(octaves):
        a += amp * noise(n, f * 0.5, f, aniso, None if seed is None else seed + k); amp *= gain; f *= 2
    return a / a.std()


def save(name, a, q=88):
    Image.fromarray(np.clip(a * 255, 0, 255).astype(np.uint8)).save(os.path.join(OUT, name + '.jpg'), quality=q)
    return float(a.mean())


def normal_map(name, h, strength):
    gx = (np.roll(h, -1, 1) - np.roll(h, 1, 1)) * strength
    gy = (np.roll(h, -1, 0) - np.roll(h, 1, 0)) * strength
    nz = 1.0 / np.sqrt(gx * gx + gy * gy + 1)
    rgb = np.stack([-gx * nz, gy * nz, nz], -1) * 0.5 + 0.5
    im = Image.fromarray(np.clip(rgb * 255, 0, 255).astype(np.uint8))
    if im.width > 512: im = im.resize((512, 512), Image.LANCZOS)
    im.save(os.path.join(OUT, name + '_n.jpg'), quality=85)


def veins(n, scale, width, warp, seed):
    """Long flowing veins: zero crossings of a noise field stretched along one direction, with finer wobble added."""
    base = noise(n, scale * 0.3, scale, aniso=(0.25, 1.0), seed=seed + 100)      # elongated -> long veins
    wob = fbm(n, scale * 3, 3, 0.5, seed=seed)
    thick = 0.6 + 0.4 * np.tanh(fbm(n, 2, 3, seed=seed + 7))                       # vein width varies along its length
    field = base + warp * 0.25 * wob
    return np.exp(-(field / (width * thick)) ** 2)


meta = {}
N = 1024

# ---------------- stone ----------------
cloud = fbm(N, 2, 6, 0.55, seed=1)
v1 = veins(N, 2, 0.07, 0.9, 11); v2 = veins(N, 4, 0.035, 0.6, 21)
marble = 0.975 - 0.025 * np.clip(cloud, -2, 2) - 0.42 * v1 - 0.16 * v2 - 0.06 * veins(N, 3, 0.25, 0.5, 15)
meta['marble'] = save('marble', np.clip(marble, 0, 1))
v3 = veins(N, 3, 0.05, 1.1, 31)
sint = 0.93 - 0.04 * np.clip(fbm(N, 3, 6, seed=2), -2, 2) - 0.28 * v3 - 0.10 * veins(N, 6, 0.03, 0.7, 41)
meta['sintered'] = save('sintered', np.clip(sint, 0, 1))
quartz = 0.96 - 0.02 * np.clip(fbm(N, 8, 4, seed=3), -2, 2) - 0.05 * (rng.random((N, N)) > 0.985)
meta['quartz'] = save('quartz', np.clip(quartz, 0, 1))
# travertine: horizontal bands with small pits
band = fbm(N, 3, 5, 0.6, aniso=(1.0, 0.12), seed=4)
pits = noise(N, 60, 140, seed=5); pits = (pits > 2.3).astype(float)
trav = 0.90 + 0.05 * np.clip(band, -2, 2) - 0.18 * pits
meta['travertine'] = save('travertine', np.clip(trav, 0, 1)); normal_map('travertine', -pits * 0.6 + 0.02 * band, 2.0)

# ---------------- wood (grain runs along u) ----------------
def wood(seed, rings, contrast, fine):
    """Vertical grain: growth rings vary across x, streaks and pores are long along y."""
    xx = np.mgrid[0:N, 0:N][1] / N
    warp = fbm(N, 1, 4, 0.5, aniso=(0.15, 1.0), seed=seed)
    ring = np.sin(2 * np.pi * (rings * xx + 0.6 * warp))
    ring = np.sign(ring) * np.abs(ring) ** 0.6
    streak = fbm(N, 12, 4, 0.55, aniso=(0.05, 1.0), seed=seed + 7)
    pores = noise(N, 150, 350, aniso=(0.04, 1.0), seed=seed + 9)
    a = 0.82 + contrast * (0.6 * ring + 0.4 * np.clip(streak, -2, 2) * 0.6) - fine * np.clip(pores, 0, 3) * 0.035
    return np.clip(a, 0, 1), ring * 0.3 + pores * 0.04
w, h = wood(60, 5, 0.14, 1.0); meta['walnut'] = save('walnut', w); normal_map('walnut', h, 1.2)
w, h = wood(70, 8, 0.08, 0.6); meta['oak'] = save('oak', np.clip(w + 0.1, 0, 1)); normal_map('oak', h, 1.0)

# ---------------- tiles ----------------
def tiles(cols, rows, grout_px, var, seed, stone):
    a = np.ones((N, N)) * 0.96
    r = np.random.default_rng(seed)
    th, tw = N // rows, N // cols
    for j in range(rows):
        for i in range(cols):
            a[j * th:(j + 1) * th, i * tw:(i + 1) * tw] += r.normal(0, var)
    a += stone * np.clip(fbm(N, 3, 5, seed=seed + 1), -2.5, 2.5)
    g = np.zeros((N, N))
    for j in range(rows + 1):
        y = (j * th) % N; g[max(0, y - grout_px // 2):y + (grout_px + 1) // 2, :] = 1; g[-grout_px // 2:, :] = 1 if j == 0 else g[-grout_px // 2:, :]
    for i in range(cols + 1):
        x = (i * tw) % N; g[:, max(0, x - grout_px // 2):x + (grout_px + 1) // 2] = 1
    g[:, -(grout_px // 2 or 1):] = 1; g[-(grout_px // 2 or 1):, :] = 1
    a = a * (1 - g) + 0.80 * g
    return np.clip(a, 0, 1), -g
t, g = tiles(2, 2, 3, 0.008, 80, 0.005); meta['tile600'] = save('tile600', t); normal_map('tile600', g * 1.0, 1.5)
t, g = tiles(4, 2, 3, 0.012, 81, 0.008); meta['tile300x600'] = save('tile300x600', t); normal_map('tile300x600', g * 1.0, 1.5)
t, g = tiles(4, 4, 3, 0.015, 82, 0.012); meta['tile300'] = save('tile300', t); normal_map('tile300', g * 1.0, 1.5)

# ---------------- paint (barely visible roller texture) ----------------
p = 0.99 - 0.004 * np.clip(fbm(N, 4, 5, 0.6, seed=90), -2, 2) - 0.006 * np.clip(noise(N, 150, 400, seed=91), -2, 2)
meta['paint'] = save('paint', np.clip(p, 0, 1)); normal_map('paint', noise(N, 150, 400, seed=91) * 0.02, 1.0)

# ---------------- fabrics (512) ----------------
N = 512
yy, xx = np.mgrid[0:N, 0:N]
weave = 0.5 * (np.sin(2 * np.pi * xx / N * 96) * np.sign(np.sin(2 * np.pi * yy / N * 48)) + 1)
fab = 0.88 + 0.07 * weave + 0.012 * np.clip(fbm(N, 8, 4, seed=100), -2, 2)
meta['fabric'] = save('fabric', np.clip(fab, 0, 1)); normal_map('fabric', weave * 0.25 + 0.05 * fbm(N, 30, 3, seed=101), 1.6)
loops = noise(N, 40, 70, seed=110)
bou = 0.86 + 0.07 * np.tanh(loops) + 0.01 * np.clip(fbm(N, 6, 4, seed=111), -2, 2)
meta['boucle'] = save('boucle', np.clip(bou, 0, 1)); normal_map('boucle', np.tanh(loops) * 0.5, 2.2)
rugn = noise(N, 60, 120, seed=120)
rug = 0.82 + 0.09 * np.tanh(rugn) + 0.02 * np.clip(fbm(N, 4, 4, seed=121), -2, 2)
meta['rug'] = save('rug', np.clip(rug, 0, 1)); normal_map('rug', np.tanh(rugn) * 0.6, 2.0)
cell = noise(N, 50, 110, seed=130)
lea = 0.92 + 0.012 * np.clip(fbm(N, 4, 4, seed=131), -2, 2) - 0.03 * np.abs(cell) ** 0.5
meta['leather'] = save('leather', np.clip(lea, 0, 1)); normal_map('leather', -np.abs(cell) * 0.2, 1.4)

# chair mesh: open diamond knit, dark strands with light gaps
d1 = np.abs(np.sin(np.pi * (xx + yy) / N * 40)); d2 = np.abs(np.sin(np.pi * (xx - yy) / N * 40))
strand = np.clip(1.6 - (d1 * d2) ** 0.35 * 1.9, 0, 1)
mesh = 0.55 + 0.45 * (1 - strand) * 0.0 + 0.45 * strand
meta['mesh'] = save('mesh', np.clip(0.62 + 0.38 * strand, 0, 1)); normal_map('mesh', strand * 0.6, 2.0)

json.dump({k: round(v, 3) for k, v in meta.items()}, open(os.path.join(OUT, 'means.json'), 'w'), indent=1)
print(json.dumps(meta, indent=1))
