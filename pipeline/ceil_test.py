"""Preview a false-ceiling concept.  Usage: python3 ceil_test.py <name>   ('wave' = the current default)
Builds plans C and B with that concept and writes /tmp/ceil_<name>_sheet.png:
 tile 1 = reflected ceiling plan of the whole flat seen from BELOW (mirrored left-right vs the floor plan; furniture hidden),
 then living, dining, hall, bedroom views in plan C, and plan B's living/lounge."""
import sys, subprocess, json, glob, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import render
from PIL import Image
name = sys.argv[1]
HIDE_RCP = ('Floor', 'Furniture', 'Decor', 'Kitchen', 'Kitchen_Open', 'Kitchen_Closed', 'Sanitary', 'Curtains', 'Fixtures', 'Partitions', 'Kitchen_Glass_Open', 'Kitchen_Glass_Closed', 'Toilet_Pipe_Boxups', 'Doors', 'Aircon', 'Windows')
EXTRA = {
 'plan_c': [('rcp', (7300, 4500, -30000), (7300, 4800, 2600), 34, HIDE_RCP), ('rcp living', (3000, 3300, -9000), (3000, 3400, 2600), 46, HIDE_RCP), ('rcp bedrooms', (10000, 2300, -12000), (10000, 2400, 2600), 46, HIDE_RCP),
            ('living up', (4700, 4250, 1250), (2300, 2300, 2650), 80, ()), ('living wide', (5200, 4300, 1500), (1500, 2300, 2100), 75, ()),
            ('dining up', (6000, 6500, 1200), (6900, 4800, 2650), 80, ()), ('hall up', (2300, 6150, 1300), (4600, 4900, 2650), 80, ()),
            ('master up', (11800, 4200, 1300), (13200, 2300, 2650), 80, ()), ('bed2 up', (9000, 3300, 1300), (10200, 1500, 2650), 80, ()), ('study up', (500, 6150, 1300), (1300, 5100, 2650), 85, ())],
 'plan_b': [('rcp living B', (3000, 3900, -11000), (3000, 4000, 2600), 46, HIDE_RCP), ('lounge up', (2300, 6100, 1300), (1100, 4900, 2650), 80, ())]}
ims = []
for plan in ('plan_c', 'plan_b'):
    r = subprocess.run([sys.executable, 'export.py', plan, 'lux', name], capture_output=True, text=True)
    if r.returncode: print(r.stderr[-3000:]); sys.exit(1)
    D = json.load(open('/tmp/st_%s_%s.json' % (name, plan))); mode = list(D['modes'].keys())[0]
    for i, (n, e, t, f, hide) in enumerate(EXTRA[plan]):
        out = '/tmp/ceil_%s_%s_%02d.png' % (name, plan, i)
        render.render(D, {'name': n, 'eye': list(e), 'target': list(t), 'fov': f, 'tag': ''}, mode, out, 560, 347, hide_extra=hide)
        ims.append(Image.open(out))
w, h = ims[0].size; cols = 3; rows = (len(ims) + cols - 1) // cols
sheet = Image.new('RGB', (w * cols, h * rows), 'white')
for i, im in enumerate(ims): sheet.paste(im, ((i % cols) * w, (i // cols) * h))
out = '/tmp/ceil_%s_sheet.png' % name; sheet.save(out); print(out, len(ims), 'views')
