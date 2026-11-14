# build_model call 10 of 10
apply_preset(model, style_preset('INTERIOR_ROOM', desktop=True))
K = ShadowInfoKey
si = model.get_shadow_info()
si[K['CITY']] = TypedValue(string_value='Singapore (Jurong West)'); si[K['COUNTRY']] = TypedValue(string_value='Singapore')
si[K['LATITUDE']] = TypedValue(double_value=1.346); si[K['LONGITUDE']] = TypedValue(double_value=103.705)
si[K['TZOFFSET']] = TypedValue(double_value=8.0); si[K['NORTH_ANGLE']] = TypedValue(double_value=0.0)
si[K['DISPLAY_SHADOWS']] = TypedValue(bool_value=False); si[K['USE_SUN_FOR_ALL_SHADING']] = TypedValue(bool_value=True)
si[K['LIGHT']] = TypedValue(int_value=85); si[K['DARK']] = TypedValue(int_value=45); si[K['SHADOW_TIME_EPOCH']] = TypedValue(int_value=1794045600)
LAY = dict((L.get_name(), L) for L in model.get_layers())
H = ['Ceiling', 'Beams_Highlight', 'Structural_Highlight']
DEF = H + ['Kitchen_Door_Closed']
TOP = DEF + ['False_Ceiling', 'Lighting']
def P(p): return SUPoint3D(mm(p[0]), mm(-p[1]), mm(p[2]))
V = [
 ('01 Overview', (-3500, 14500, 15500), (7300, 4800, 0), 40, TOP),
 ('02 Plan', (7300, 4800, 60000), (7300, 4799, 0), 11.5, TOP + ['Aircon', 'Curtains']),
 ('03 Living - sofas, coffee table, TV wall', (5000, 4300, 1650), (2400, 2300, 900), 80, DEF),
 ('04 Living - from TV towards sofas and dining', (2700, 1700, 1650), (5400, 3800, 700), 85, DEF),
 ('05 Living - TV wall, 75in TV and console', (5000, 2700, 1350), (2440, 2700, 950), 70, DEF),
 ('06 Living - organic wave ceiling and fan', (5200, 4300, 1250), (3800, 2800, 2650), 88, DEF),
 ('07 Study - two desks and top cabinets', (600, 3500, 1650), (2250, 2100, 1000), 80, DEF),
 ('08 Study - towards half-glass wall and sliding door', (2100, 1700, 1600), (500, 3800, 900), 80, DEF),
 ('09 Study - from living through half glass', (3400, 5000, 1600), (1200, 2600, 1100), 70, DEF),
 ('10 Entry - tall storage wall, console, half-glass screen', (3200, 4300, 1600), (500, 6000, 1000), 75, DEF),
 ('11 Dining - table for 8', (4300, 4100, 1600), (7000, 6000, 700), 80, DEF),
 ('12 Dining - from pantry end', (8000, 4300, 1600), (4500, 6200, 800), 80, DEF),
 ('13 Dining - coffer ceiling, pendant and fan', (4500, 4000, 1300), (6800, 5600, 2500), 85, DEF),
 ('14 Dry pantry - mirror and robot bay', (5300, 4600, 1550), (8400, 6000, 1300), 75, DEF),
 ('15 Foyer - from main door', (2700, 8150, 1650), (2400, 5000, 900), 88, DEF),
 ('16 Foyer - glass display and shelter mirror', (2900, 5900, 1500), (1900, 6500, 1100), 70, DEF),
 ('17 Foyer - shoe bench', (2250, 5900, 1550), (3600, 7150, 650), 72, DEF),
 ('18 Foyer - grab-and-go niche', (2300, 7300, 1500), (3700, 7800, 1150), 70, DEF),
 ('19 Household shelter', (1500, 6650, 1750), (450, 8400, 500), 88, DEF),
 ('20 Bedroom 3', (8350, 3500, 1650), (5800, 300, 800), 88, DEF),
 ('21 Bedroom 3 - bedside nook', (6950, 1500, 1350), (5800, 2550, 750), 75, DEF),
 ('22 Bedroom 2 - kids floor bed', (9200, 3300, 1600), (11000, 1300, 300), 75, DEF),
 ('23 Master - organic wave mirror', (13300, 2300, 1500), (11450, 850, 1050), 70, DEF),
 ('24 Master - bed and pendants', (12100, 2560, 1550), (14350, 2560, 1200), 85, DEF),
 ('25 Kitchen', (4150, 6950, 1650), (7800, 9250, 800), 88, DEF),
 ('26 Kitchen - reverse', (7650, 8300, 1650), (4100, 7000, 900), 88, DEF),
 ('27 Kitchen door - CLOSED', (3000, 5200, 1600), (4600, 6900, 1100), 70, H + ['Kitchen_Door_Open']),
 ('28 Kitchen door - OPEN (slid into pocket)', (3000, 5200, 1600), (4600, 6900, 1100), 70, DEF),
 ('29 Kitchen - larder, microwave, appliance garage', (7700, 8100, 1650), (5200, 7000, 900), 80, DEF),
 ('30 Kitchen - hob, oven, sink, dishwasher', (6000, 7300, 1650), (6500, 9250, 800), 80, DEF),
 ('31 Common bathroom', (9000, 5250, 1600), (10200, 6850, 900), 80, DEF),
 ('32 Common bathroom - shower niche', (10700, 5300, 1600), (9950, 6500, 1100), 80, DEF),
 ('33 Ensuite', (12250, 5200, 1650), (10950, 6700, 650), 85, DEF),
 ('34 Ensuite - towards shower', (11100, 5300, 1650), (12900, 6750, 600), 85, DEF),
 ('35 Service yard - dryer and water heater', (8300, 8550, 1650), (8900, 7000, 900), 85, DEF),
 ('36 Service yard - washer and drying rack', (8300, 7650, 1650), (8900, 9250, 900), 85, DEF),
]
scs = []
for v in V:
    sc = Scene(); sc.set_name(v[0]); scs.append(sc)
model.add_scenes(scs)
for sc, v in zip(scs, V):
    c = Camera(); c.set_orientation(P(v[1]), P(v[2]), SUVector3D(0, 0, 1)); c.enable_perspective(); c.set_perspective_frustum_fov(float(v[3]))
    sc.set_use_camera(True); sc.set_camera(c); sc.set_use_hidden_layers(True)
    for n in v[4]: sc.add_layer(LAY[n])
    sc.set_use_shadow_info(True)
si[K['DISPLAY_SHADOWS']] = TypedValue(bool_value=True)
D = [
 ('37 SUNLIGHT - whole flat from above, 10am', (-3500, 14500, 15500), (7300, 4800, 0), 40, TOP, 1794045600),
 ('38 SUNLIGHT - living and study, 10am', (5000, 4300, 1650), (2400, 2300, 900), 80, DEF, 1794045600),
 ('39 SUNLIGHT - whole flat from above, 4pm', (-3500, 14500, 15500), (7300, 4800, 0), 40, TOP, 1794067200),
]
for v in D:
    si[K['SHADOW_TIME_EPOCH']] = TypedValue(int_value=v[5])
    sc = Scene(); sc.set_name(v[0]); model.add_scenes([sc])
    c = Camera(); c.set_orientation(P(v[1]), P(v[2]), SUVector3D(0, 0, 1)); c.enable_perspective(); c.set_perspective_frustum_fov(float(v[3]))
    sc.set_use_camera(True); sc.set_camera(c); sc.set_use_hidden_layers(True)
    for n in v[4]: sc.add_layer(LAY[n])
    sc.set_use_shadow_info(True)
si[K['DISPLAY_SHADOWS']] = TypedValue(bool_value=False)
si[K['SHADOW_TIME_EPOCH']] = TypedValue(int_value=1794045600)
LAY['Kitchen_Door_Closed'].set_visibility(False)
result = {'scenes': len(model.get_scenes())}
