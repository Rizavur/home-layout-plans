"""Build the data the website shows.

    python3 build.py            rebuild every plan
    python3 build.py c f        rebuild only plans C and F

For each plan this runs export.py (geometry -> JSON), moves the JSON files into ../data/,
re-renders the home-page preview into ../prev/ when the plan changed, and writes
../data/plans.json (plan list for the home page) and ../data/themes.json (interior themes).
It then rebuilds the web bundle (web/build.mjs), which embeds plans/themes and a cache-busting build id.
"""
import glob, json, os, shutil, subprocess, sys
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, '..', 'data')
PREV = os.path.join(HERE, '..', 'prev')

# The plans shown on the home page, in order. Each plan is built by plan_<key>.py.
PLANS = [
 {'key': 'a', 'short': 'Plan A', 'title': 'Plan A – Original layout', 'bullets': ['Dining for 7 by the household shelter', 'Study room beside the kitchen (desks or single bed)', 'Bedroom 3: queen bed or 2 standing desks', 'Closed kitchen · improvements only']},
 {'key': 'b', 'short': 'Plan B', 'title': 'Plan B – Lounge and open kitchen', 'bullets': ['Study behind the TV wall, desks on the west wall', 'Lounge with a sofa outside the study, onyx feature wall', 'New entrance glass partition in line with the shelter', 'Open or closed kitchen with bi-fold glass']},
 {'key': 'c', 'short': 'Plan C', 'title': 'Plan C – Study by the shelter', 'bullets': ['TV wall moved to the east wall', 'Sofas on the west side, art above', 'Study by the shelter, flush with the cabinets, key niche', 'Open or closed kitchen with bi-fold glass'], 'tint': 'green'},
 {'key': 'd', 'short': 'Plan D', 'title': 'Plan D – Bedroom 3 as study', 'bullets': ['No study room – bedroom 3 is the study', 'D1 desks only · D2 with fold-down wall bed', 'Tall hall cabinets and marble TV wall', 'Open or closed kitchen with bi-fold glass'], 'tint': 'green'},
 {'key': 'e', 'short': 'Plan E', 'title': 'Plan E – U-shaped lounge', 'bullets': ['U-shaped lounge seating, round coffee table', 'Angled corner TV wall with storage behind', 'Dining outside the kitchen, rest like Plan A', 'Open or closed kitchen with bi-fold glass'], 'tint': 'red'},
 {'key': 'f', 'short': 'Plan F', 'title': 'Plan F – Open study nook', 'bullets': ['Open study nook for two by the west wall, no extra walls', 'Bedroom 3 kept as a guest bedroom', 'Dining for 8 beside an open kitchen', 'Marble TV wall with tall storage'], 'tint': 'red'},
 {'key': 'g', 'short': 'Plan G', 'title': 'Plan G – Maid room and study', 'bullets': ['Study wall carried to the window: maid room + study', 'TV on the maid-room feature wall, hidden door', 'L-sofa on the bedroom wall, chaise to the dining side', 'Open or closed kitchen with bi-fold glass'], 'tint': 'red'},
]

# Interior themes: base themes plus the extra ones, in the order shown in the side panel.
ORDER = ['lux', 'japandi', 'nordic', 'midcentury', 'industrial', 'classic', 'wabisabi', 'minimal', 'coastal', 'boho', 'deco', 'dark']


def build_themes():
    themes = json.load(open(os.path.join(HERE, 'themes.json')))
    themes.update(json.load(open(os.path.join(HERE, 'themes_extra.json'))))
    return {k: themes[k] for k in ORDER if k in themes}


def _costs():
    """Per-plan cost summary written by estimate.py (renovation, furniture & appliances, total), if there is one."""
    try: return json.load(open(os.path.join(DATA, 'costs.json')))['summary']
    except Exception: return {}


def build_plan(key):
    print('plan', key.upper())
    subprocess.run([sys.executable, 'export.py', 'plan_' + key], cwd=HERE, check=True)
    for f in glob.glob(os.path.join(HERE, 'plan_%s.json' % key)) + glob.glob(os.path.join(HERE, 'plan_%s.*.json' % key)):
        shutil.move(f, os.path.join(DATA, os.path.basename(f)))
    # home-page preview: the annotated plan view, seen from above
    out = os.path.join(PREV, 'plan_%s.jpg' % key)
    subprocess.run([sys.executable, 'render.py', os.path.join(DATA, 'plan_%s.json' % key), 'Plan view', '1200'], cwd=HERE, check=True, capture_output=True)
    shot = glob.glob(os.path.join(HERE, 'r_*.png'))[0]
    Image.open(shot).convert('RGB').save(out, quality=82, optimize=True)
    for f in glob.glob(os.path.join(HERE, 'r_*.png')): os.remove(f)


if __name__ == '__main__':
    os.makedirs(DATA, exist_ok=True); os.makedirs(PREV, exist_ok=True)
    keys = sys.argv[1:] or [p['key'] for p in PLANS]
    for k in keys: build_plan(k)
    PLANS_OUT = [dict(p, cost=_costs().get(p['key'])) for p in PLANS]
    json.dump(PLANS_OUT, open(os.path.join(DATA, 'plans.json'), 'w'), indent=1, ensure_ascii=False)
    json.dump(build_themes(), open(os.path.join(DATA, 'themes.json'), 'w'), separators=(',', ':'))
    # rebuild the web bundle too: it embeds plans/themes and the cache-busting build id
    subprocess.run(['node', 'build.mjs'], cwd=os.path.join(HERE, '..', 'web'), check=True)
    print('done (data + web bundle)')
