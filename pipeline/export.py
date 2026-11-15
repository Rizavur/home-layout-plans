import json, base64, struct, sys, importlib, math
import core, mesh, planlib
EMISSIVE = {'Paper_Shade_Washi', 'Cove_Wash_Warm', 'Cove_Wash_Soft', 'LED_Strip_Warm_3000K', 'Cove_Light_Warm', 'Light_Diffuser_Opal', 'Onyx_Backlit_Honey'}

import re as _re
_MAP = [
    (r'^CMP (\d) · ', r'Compare \1 – '), (r'^NIGHT · ', 'Night – '), (r'^SERVICES · Power points \+ aircon trunking', 'Services – power points and aircon trunking'),
    (r'^OPEN kitchen', 'Open kitchen'), (r'^Kitchen \(closed\)', 'Closed kitchen'),
    (r'^D1 Bedroom 3 study – ', 'Bedroom 3 D1 – '), (r'^D2 Bedroom 3 – ', 'Bedroom 3 D2 – '),
    (r'Option ([AB]) ', r'option \1, '), (r'\bDOWN\b', 'down'), (r'\bFOLDED\b', 'folded'),
]
_KEEP = ('TV', 'D1', 'D2')
_SIMPLE = {'Bedroom 2 – kids floor bed': 'Bedroom 2 – kids bed', 'Bedroom 3 D1 – desks facing window': 'Bedroom 3 – desks only', 'Bedroom 3 D1 – from window side': 'Bedroom 3 – desks only, from window', 'Bedroom 3 D2 – desks with wall bed folded': 'Bedroom 3 – desks, wall bed up', 'Bedroom 3 D2 – wall bed down': 'Bedroom 3 – wall bed down', 'Bedroom 3 D2 – wall bed down from door': 'Bedroom 3 – wall bed down, from door', 'Bedroom 3 D2 – wall bed folded': 'Bedroom 3 – wall bed up', 'Bedroom 3 – as study (2 standing desks)': 'Bedroom 3 – study desks', 'Bedroom 3 – option A, queen bed': 'Bedroom 3 – queen bed', 'Bedroom 3 – option B, two standing desks': 'Bedroom 3 – standing desks', 'Bedroom 3 – queen bed and painting': 'Bedroom 3 – bed and painting', 'Closed kitchen – door shut': 'Closed kitchen – from dining', 'Kitchen – door shut': 'Kitchen – from dining', 'Compare 1 – living from dining side': 'Compare 1 – living from dining', 'Compare 3 – hall towards kitchen': 'Compare 3 – hall to kitchen', 'Compare 4 – hall from the foyer': 'Compare 4 – hall from entrance', 'Dining – coffer ceiling and fan': 'Dining – ceiling and fan', 'Dining – false ceiling, pendant, fan': 'Dining – ceiling and lights', 'Dining – from pantry end': 'Dining – from pantry', 'Dining – table for 7 by the shelter': 'Dining – table for 7', 'Dining – table for 8 outside kitchen': 'Dining – table for 8', 'Dry pantry – mirror and robot bay': 'Dry pantry – mirror and robot vacuum', 'Entrance partition – from foyer': 'Entrance screen – from entrance', 'Entrance partition – from lounge': 'Entrance screen – from lounge', 'Foyer – shoe bench': 'Foyer – shoe bench and cabinet', 'Foyer – shoe cabinet': 'Foyer – shoe cabinet', 'Hall – corner niche towards shelter': 'Hall – corner niche', 'Hall – tall cabinets with display bay': 'Hall – tall cabinets', 'Hall – key niche by the study door': 'Hall – key niche', 'Living – TV wall and console': 'Living – TV wall', 'Living – TV wall now on the east side': 'Living – TV wall', 'Living – angled TV wall with storage behind': 'Living – angled TV wall', 'Living – lounge seating from the TV corner': 'Living – sofas from TV', 'Living – organic wave ceiling': 'Living – ceiling', 'Living – seamless marble TV wall': 'Living – marble TV wall', 'Living – sofas on the west side': 'Living – sofas', 'Living – sofas, pebble table, rug': 'Living – sofas', 'Living – wave ceiling over the seating': 'Living – ceiling', 'Lounge – backlit onyx feature wall': 'Lounge – onyx wall', 'Lounge – from living room': 'Lounge – from living', 'Lounge – pendant and dome ceiling': 'Lounge – ceiling', 'Master – bed, painting, wall lights': 'Master – bed', 'Master – organic wave mirror': 'Master – mirror', 'Night – master bedroom': 'Night – master', 'Open kitchen – counter and tall units': 'Open kitchen – counter', 'Open kitchen – glass closed (cooking)': 'Open kitchen – glass closed', 'Open kitchen – glass folded away': 'Open kitchen – glass open', 'Open kitchen – stove side top cabinets': 'Open kitchen – stove side', 'Plan (annotated)': 'Plan view', 'Services – power points and aircon trunking': 'Services – power and aircon', 'Study door – clear approach from the lounge': 'Study – door from lounge', 'Study room – option A, two standing desks': 'Study – desks', 'Study room – option B, single bedroom': 'Study – single bed', 'Study – from living through glass': 'Study – from living', 'Study – from living through half glass': 'Study – from living', 'Study – towards half-glass wall': 'Study – glass wall', 'Study – two standing desks': 'Study – desks', 'Study – wall flush with shelter cabinets, sliding door': 'Study – sliding door', 'TV corner – cabinets around and behind the TV': 'Living – TV cabinets'}
def norm_name(n):
    for a, b in _MAP: n = _re.sub(a, b, n)
    if ' – ' in n:
        head, tail = n.split(' – ', 1)
        w = tail.split(' ', 1)[0]
        if w not in _KEEP and not (len(w) > 1 and w.isupper()): tail = tail[:1].lower() + tail[1:]
        n = head + ' – ' + tail
    return _SIMPLE.get(n, n)

def build_plan(modname, style='lux', only=None, ceil='wave'):
    planlib.STYLE = style; planlib.CEIL = ceil; SIG = {}
    core.CAPTURE[:] = []
    st = core.new_state(); core.run_shell(st)
    L = st['L']; LQ = st['LQ']
    c = planlib.setup(L, LQ)
    L['ITEMS'][:] = []
    mod = importlib.import_module(modname)
    mod.build(c)
    M = L['MATS']
    chunks = {}   # (layer, matname) -> list of floats
    mats = {}
    def add(layer, rgba, faces):
        key = (layer, rgba[0])
        mats[rgba[0]] = list(rgba[1:])
        arr = chunks.setdefault(key, [])
        for (outer, holes) in faces:
            for (A, Bp, C) in mesh.triangulate(outer, holes):
                for p in (A, Bp, C): arr.extend((p[0], p[2], -p[1]))
    for cap in (core.CAPTURE if only is None else []):
        lay = cap['layer'] or 'Walls_and_Beams'
        if cap['name'] == 'Beams_Highlight' or cap['name'] == 'Structural_Highlight': continue
        byrgba = {}
        for (rgba, o, h) in cap['faces']: byrgba.setdefault(rgba, []).append((o, h))
        for rgba, fs in byrgba.items(): add(lay, rgba, fs)
    boxes = []
    for idx, it in enumerate(L['ITEMS']):
        r, p = L['item_faces'](it, st['fns']['vx_mesh'], st['fns']['vx_clusters'])
        SIG[idx] = hash(repr((sorted((m, repr(fs)) for m, fs in r.items()), sorted((m, repr(fs)) for m, fs in p.items()))))
        var = 'v' if (only is not None or (VARIABLE is not None and idx in VARIABLE)) else ''
        if only is None and CVAR is not None and idx in CVAR: var = 'c'
        if only is not None and idx not in only: continue
        for m, fs in list(r.items()) + list(p.items()):
            if m not in M: raise KeyError(m)
            add(it['layer'] + ('|' + var if var else ''), M[m], [(f[3], f[4]) for f in fs])
        for m, bs in it['boxes'].items():
            if m in ('glass', 'fglass', 'led', 'cove', 'lightw', 'rug1', 'rug2'): continue
            for b in bs: boxes.append((it['name'], b, it['layer']))
    build_plan.sig = SIG
    return chunks, mats, boxes, mod
VARIABLE = None
CVAR = None
CEILS = ['crescent', 'arc', 'pill', 'island']
FAMILIES = ['japandi', 'scandi', 'midcentury', 'industrial', 'classic']
def pack(chunks, mats, mod):
    out = []
    ntri = 0
    for (layer, mname), arr in sorted(chunks.items()):
        q = [int(round(v)) for v in arr]
        ntri += len(q) // 9
        var = {'|v': 1, '|c': 2}.get(layer[-2:], 0); layer = layer[:-2] if var else layer
        out.append({'layer': layer, 'v': var, 'mat': mname, 'n': len(q) // 3, 'b64': base64.b64encode(struct.pack('<%dh' % len(q), *q)).decode()})
    M = {}
    for k, v in mats.items(): M[k] = {'c': v[:3], 'a': v[3] / 255.0, 'e': k in EMISSIVE}
    return {'chunks': out, 'mats': M}, ntri
def cam_check(views, boxes, mod):
    bad = []
    for v in views:
        e = v[1]
        if e[2] > 5000: continue
        hid = set(mod.MODES[v[5] if len(v) > 5 and v[5] else list(mod.MODES.keys())[0]]['hide'])
        for nm, b, lay in boxes:
            if lay in hid: continue
            if b[0] - 120 < e[0] < b[1] + 120 and b[2] - 120 < e[1] < b[3] + 120 and b[4] - 120 < e[2] < b[5] + 120:
                bad.append((v[0], nm, b)); break
    return bad
if __name__ == '__main__':
    modname = sys.argv[1]
    import os
    if len(sys.argv) > 2:      # test mode: full model in one furniture family -> /tmp/st_<family>_<plan>.json
        chunks, mats, boxes, mod = build_plan(modname, sys.argv[2], ceil=(sys.argv[3] if len(sys.argv) > 3 else 'wave')); data, ntri = pack(chunks, mats, mod)
        data['views'] = [{'name': norm_name(v[0]), 'eye': v[1], 'target': v[2], 'fov': v[3], 'tag': v[4], 'mode': (v[5] if len(v) > 5 else None)} for v in mod.VIEWS]; data['modes'] = mod.MODES
        open('/tmp/st_%s_%s.json' % (sys.argv[3] if len(sys.argv) > 3 else sys.argv[2], modname), 'w').write(json.dumps(data)); sys.exit()
    fams = [f for f in FAMILIES if os.path.exists('style_%s.py' % f)]
    build_plan(modname); base = dict(build_plan.sig); sigs = {}
    for f in fams: build_plan(modname, f); sigs[f] = dict(build_plan.sig)
    VARIABLE = set(i for f in fams for i in base if sigs[f].get(i) != base[i])
    for f in fams:
        chunks, mats, boxes, mod = build_plan(modname, f, only=VARIABLE); fd, nt = pack(chunks, mats, mod)
        open('%s.%s.json' % (modname, f), 'w').write(json.dumps(fd, separators=(',', ':'))); print(' family', f, 'triangles', nt)
    import glob
    ceils = [c for c in CEILS if os.path.exists('ceil_%s.py' % c)]; csig = {}
    for cn in ceils: build_plan(modname, ceil=cn); csig[cn] = dict(build_plan.sig)
    cvar = set(i for cn in ceils for i in base if csig[cn].get(i) != base[i])
    for cn in ceils:
        chunks, mats, boxes, mod = build_plan(modname, only=cvar, ceil=cn); fd, nt = pack(chunks, mats, mod)
        open('%s.ceil_%s.json' % (modname, cn), 'w').write(json.dumps(fd, separators=(',', ':'))); print(' ceiling', cn, 'triangles', nt)
    CVAR = cvar
    chunks, mats, boxes, mod = build_plan(modname)
    data, ntri = pack(chunks, mats, mod)
    print('triangles', ntri, 'chunks', len(data['chunks']))
    bad = cam_check(mod.VIEWS, boxes, mod)
    for b in bad: print('CAMERA CLASH', b)
    data['views'] = [{'name': norm_name(v[0]), 'eye': v[1], 'target': v[2], 'fov': v[3], 'tag': v[4], 'mode': (v[5] if len(v) > 5 else None)} for v in mod.VIEWS]
    data['modeLabel'] = getattr(mod, 'MODE_LABEL', 'Layout option'); data['labels'] = mod.LABELS; data['dims'] = mod.DIMS; data['info'] = mod.INFO; data['modes'] = mod.MODES; data['hideDefault'] = []; data['families'] = fams; data['ceils'] = ceils
    s = json.dumps(data, separators=(',', ':'))
    open(modname + '.json', 'w').write(s)
    print('json MB', len(s) / 1e6)
