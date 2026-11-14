"""Preview a furniture family.  Usage: python3 style_test.py <family>
Builds plans C and B with that family and renders check images to /tmp/style_<family>_sheet.png (also returns the list)."""
import sys, subprocess, json, glob, os
from PIL import Image
fam = sys.argv[1]
SHOTS = [('plan_c', ['Compare 1 – living from dining', 'Living – sofas', 'Dining – table for 8', 'Master – bed', 'Bedroom 3 – bed and painting']), ('plan_b', ['Lounge – from living'])]
EXTRA = {  # close-ups: (name, eye, target, fov)
 'plan_c': [('zz sofa close', (3900, 4300, 1500), (2000, 2700, 450), 60), ('zz dining close', (4300, 4700, 1500), (6150, 5600, 700), 60), ('zz bed close', (11900, 4000, 1500), (13400, 2560, 500), 60), ('zz dining side', (6150, 3900, 1250), (6150, 5600, 650), 60)],
 'plan_b': [('zz lounge chairs', (2600, 4700, 1400), (1200, 5550, 400), 60)]}
ims = []
for plan, names in SHOTS:
    r = subprocess.run([sys.executable, 'export.py', plan, fam], capture_output=True, text=True)
    if r.returncode: print(r.stderr[-3000:]); sys.exit(1)
    js = '/tmp/st_%s_%s.json' % (fam, plan); D = json.load(open(js))
    have = [v['name'] for v in D['views']]
    for (n, e, t, f) in EXTRA.get(plan, []): D['views'].append({'name': n, 'eye': list(e), 'target': list(t), 'fov': f, 'tag': '', 'mode': None})
    json.dump(D, open(js, 'w'))
    want = [n for n in names if n in have] + [x[0] for x in EXTRA.get(plan, [])]
    d = '/tmp/st_%s_%s' % (fam, plan); os.makedirs(d, exist_ok=True)
    for f in glob.glob(d + '/r_*.png'): os.remove(f)
    r = subprocess.run([sys.executable, os.path.abspath('render.py'), js, '|'.join(want), '560'], capture_output=True, text=True, cwd=d)
    if r.returncode: print(r.stderr[-3000:]); sys.exit(1)
    ims += [Image.open(f) for f in sorted(glob.glob(d + '/r_*.png'))]
w, h = ims[0].size; cols = 3; rows = (len(ims) + cols - 1) // cols
sheet = Image.new('RGB', (w * cols, h * rows), 'white')
for i, im in enumerate(ims): sheet.paste(im, ((i % cols) * w, (i // cols) * h))
out = '/tmp/style_%s_sheet.png' % fam; sheet.save(out); print(out, len(ims), 'views')
