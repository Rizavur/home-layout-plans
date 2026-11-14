# Runs the original SketchUp build scripts outside SketchUp, capturing geometry.
import math, os
SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sketchup_src')
class _Ents:
    def __init__(s): s.groups = []
    def add_group(s, g): s.groups.append(g)
    def get_groups(s): return s.groups
    def get_faces(s): return []
class Group:
    def __init__(s): s.name = ''; s.layer = None; s.ents = _Ents()
    def set_name(s, n): s.name = n
    def get_name(s): return s.name
    def set_layer(s, L): s.layer = L
    def get_entities(s): return s.ents
class Layer:
    def __init__(s): s.name = ''
    def set_name(s, n): s.name = n
    def get_name(s): return s.name
class _Model:
    def __init__(s): s.layers = []; s.ents = _Ents()
    def add_layers(s, L): s.layers += L
    def get_layers(s): return s.layers
    def get_entities(s): return s.ents
def get_or_create_material(n, r, g, b, a=255): return (n, r, g, b, a)
CAPTURE = []   # dicts: name, layer, faces=[(rgba, outer, holes)]
def su_fill(name, faces, mats, parent=None, layer=None, scale=None):
    ln = layer.get_name() if layer is not None else ''
    CAPTURE.append({'name': name, 'layer': ln, 'faces': [(mats[f[0]], f[3], f[4]) for f in faces]})
    g = Group(); g.set_name(name); return g
def su_edges(*a, **k):
    g = Group(); return g
def run_shell(state):
    env = {'math': math, 'Group': Group, 'Layer': Layer, 'model': state['model'], 'get_or_create_material': get_or_create_material,
           'session_state': state, 'is_solid': lambda g: {'solid': True}, 'soften_by_angle': lambda *a: None}
    s1 = open(os.path.join(SRC, '01_fns_layers_ceiling.py')).read().replace('def su_fill(', 'def _o_su_fill(').replace('def su_edges(', 'def _o_su_edges(')
    env['su_fill'] = su_fill; env['su_edges'] = su_edges
    exec(s1, env)
    state['fns']['su_fill'] = su_fill; state['fns']['su_edges'] = su_edges
    s2 = open(os.path.join(SRC, '02_walls_floor.py')).read()
    # pull out kitchen front wall as its own removable piece
    s2 = s2.replace("[4940, 7840, -6800, -6700, 0, 2250], ", "")
    exec(s2, dict(env))
    exec(open(os.path.join(SRC, '04_windows_doors.py')).read(), dict(env))
    e5 = dict(env); exec(open(os.path.join(SRC, '05_library.py')).read(), e5)
    e6 = dict(env); exec(open(os.path.join(SRC, '06_helpers.py')).read(), e6)
    return e5, e6
def new_state():
    return {'model': _Model()}
