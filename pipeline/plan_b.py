import math
import planlib as P, blocks as K, views_common as VC
WM = 'greige'

def build(c):
    B, CYL, PRZ, RRECT, SLABH = c.B, c.CYL, c.PRZ, c.RRECT, c.SLABH
    K.fixtures(c)
    # ---------- Study (9 Nov position) ----------
    it = c.item('Study_TV_Partition_Half_Wall_and_Framed_Glass', 'Partitions')
    B(it, 2250, 2400, 1170, 3870, 0, 2650, 'wallp'); B(it, 1250, 2250, 3720, 3870, 0, 1000, 'wallp')
    B(it, 250, 1250, 3720, 3870, 2100, 2650, 'wallp'); B(it, 1250, 2250, 3720, 3870, 2550, 2650, 'wallp')
    B(it, 1250, 2250, 3712, 3878, 1000, 1020, 'marble')
    B(it, 1250, 1290, 3720, 3870, 1020, 2550, 'frame'); B(it, 2210, 2250, 3720, 3870, 1020, 2550, 'frame'); B(it, 1730, 1770, 3775, 3815, 1050, 2510, 'frame')
    B(it, 1290, 2210, 3775, 3815, 2510, 2550, 'frame'); B(it, 1290, 2210, 3775, 3815, 1020, 1050, 'frame')
    B(it, 1290, 1730, 3787, 3803, 1050, 2510, 'glass'); B(it, 1770, 2210, 3787, 3803, 1050, 2510, 'glass')
    it = c.item('Study_Sliding_Door_Fluted_Glass', 'Partitions')
    B(it, 250, 2250, 3875, 3905, 2080, 2100, 'metal'); B(it, 270, 1275, 3880, 3898, 10, 2075, 'fglass')
    B(it, 270, 300, 3879, 3899, 10, 2075, 'charcoal'); B(it, 1245, 1275, 3879, 3899, 10, 2075, 'charcoal'); B(it, 300, 1245, 3879, 3899, 10, 40, 'charcoal'); B(it, 300, 1245, 3879, 3899, 2045, 2075, 'charcoal')
    B(it, 1220, 1235, 3899, 3919, 900, 1250, 'gold'); B(it, 1220, 1235, 3860, 3879, 900, 1250, 'gold')
    it = c.item('Study_Two_Standing_Desks_Facing_Partition', 'Furniture')
    for cy in (2050, 3150): P.sdesk(c, it, '+x', 1657, cy, 1050, 585); c.station(it, '+x', 1657, cy, 585)
    c.cabinet(it, '-x', 1520, 3680, 1900, 350, 1500, 2550, 4, 'white', 0, None, 'bar', hm='gold'); B(it, 1925, 1945, 1540, 3660, 1494, 1500, 'led')
    it = c.item('Study_Chairs_x2', 'Furniture'); c.chair2(it, '+x', 1250, 2050); c.chair2(it, '+x', 1250, 3150)
    it = c.item('Aircon_Study', 'Aircon'); P.aircon2(c, it, 'x', 250, 1, 2300, 3200, 2230)
    it = c.item('Curtains_Study', 'Curtains'); c.curtain_full(it, 250, 2250, 1375, 300, 300, 5, 2540)
    it = c.item('False_Ceiling_Study', 'False_Ceiling')
    SLABH(it, [(250, 1510), (2250, 1510), (2250, 3720), (250, 3720), (250, 3250), (480, 3250), (480, 2250), (250, 2250)], RRECT(650, 1850, 1800, 3450, 200, 6), 2550, 2650, 'fceil', 'cove')
    c.downlights(it, [(2080, 1700), (400, 1700), (400, 3500), (1300, 1660), (1300, 3600)], 2550)
    # ---------- Living ----------
    it = c.item('TV_Feature_Wall_Marble_with_Fluted_Walnut_Flanks', 'Furniture')
    B(it, 2400, 2440, 1700, 3640, 0, 2650, 'marble')
    for (y0, y1) in ((1380, 1697), (3643, 3870)):
        B(it, 2400, 2430, y0, y1, 0, 2650, 'walnut'); y = y0 + 12.0
        while y < y1 - 8: CYL(it, 2430, y, 10, 0, 2650, 'walnut2', 8); y += 22
    B(it, 2440, 2443, 1800, 3540, 830, 1820, 'cove')
    it = c.item('TV_75_inch', 'Furniture'); B(it, 2443, 2473, 1840, 3500, 860, 1795, 'screen')
    dx = 2150
    it = c.item('TV_Console_Walnut_Fluted_Marble_Top', 'Furniture')
    PRZ(it, c.RR(290 + dx, 720 + dx, 1720, 3600, 110, (1, 0, 0, 0)), 240, 480, 'walnut')
    y = 1830
    while y < 3590: CYL(it, 720 + dx, y, 13, 262, 456, 'walnut2', 8); y += 30
    PRZ(it, c.RR(290 + dx, 735 + dx, 1712, 3620, 115, (1, 0, 0, 0)), 480, 500, 'marble'); B(it, 290 + dx, 735 + dx, 3600, 3620, 0, 480, 'marble')
    B(it, 640 + dx, 670 + dx, 1780, 3580, 234, 240, 'led')
    CYL(it, 520 + dx, 1950, 85, 500, 780, 'ceramic', 20); CYL(it, 520 + dx, 1950, 40, 780, 840, 'ceramic', 14); CYL(it, 530 + dx, 3365, 55, 500, 640, 'sculpt', 16)
    it = c.item('Living_3_Seater_Sofa_along_Wall', 'Furniture'); c.sofa2(it, '-x', 4461, 2700, 2400, 1000, 3, True, True, None, 'sofa', 'sofa2', ('pil1', 'pil2'))
    it = c.item('Living_2_Seater_Sofa_by_Window', 'Furniture'); c.sofa2(it, '+y', 3780, 2220, 1300, 780, 2, True, True, None, 'sofa', 'sofa2', ('pil2', 'pil1'))
    it = c.item('Living_Round_Coffee_Table_Travertine_Fluted', 'Furniture')
    cx, cy = 3724, 3000
    CYL(it, cx, cy, 420, 362, 400, 'traver', 48); CYL(it, cx, cy, 410, 358, 362, 'gold', 48); CYL(it, cx, cy, 255, 0, 358, 'walnut', 36)
    for k in range(36):
        a = 2 * math.pi * k / 36; CYL(it, cx + 262 * math.cos(a), cy + 262 * math.sin(a), 16, 0, 358, 'walnut2', 8)
    B(it, cx - 150, cx + 90, cy - 120, cy + 40, 400, 440, 'artbg'); CYL(it, cx + 170, cy + 120, 100, 400, 450, 'ceramic', 20)
    it = c.item('Living_Rug', 'Decor'); PRZ(it, RRECT(2950, 4500, 1950, 3950, 150, 6), 0, 8, 'rug1'); PRZ(it, RRECT(3070, 4380, 2070, 3830, 100, 6), 8, 10, 'rug2')
    it = c.item('Living_Wall_Art_Marble_Diptych', 'Decor')
    P.painting(c, it, 'x', 5550, -1, 1990, 2730, 1050, 1950, 'artm'); P.painting(c, it, 'x', 5550, -1, 2790, 3530, 1050, 1950, 'artm')
    it = c.item('Curtains_Living', 'Curtains'); c.curtain_full(it, 2400, 5550, 1375, 360, 360, 5, 2540)
    it = c.item('Living_Floor_Lamp', 'Lighting'); P.floor_lamp(c, it, 2990, 1600)
    # ---------- NEW: hall lounge (cabinets removed) – kept south of a clear path to the study door ----------
    LX, LY = 1225, 5500          # lounge centre
    it = c.item('Lounge_Feature_Wall_Backlit_Onyx_with_Fluted_Walnut', 'Furniture')
    B(it, 250, 290, 3870, 6300, 0, 2650, 'wallp')
    B(it, 290, 330, 4850, 6150, 120, 2420, 'onyx')
    B(it, 290, 336, 4846, 4850, 120, 2420, 'led'); B(it, 290, 336, 6150, 6154, 120, 2420, 'led')
    for (y0, y1) in ((4560, 4840), (6160, 6260)):
        B(it, 290, 310, y0, y1, 0, 2550, 'walnut'); y = y0 + 12.0
        while y < y1 - 8: CYL(it, 310, y, 9, 0, 2550, 'walnut2', 8); y += 20
    B(it, 290, 400, 4850, 6150, 0, 120, 'charcoal'); B(it, 290, 400, 4850, 6150, 120, 135, 'marble'); B(it, 300, 390, 4860, 6140, 2420, 2430, 'charcoal')
    it = c.item('Lounge_Chairs_Side_Table_Sculpture', 'Furniture')
    P.lounge_chair(c, it, 850, 5300, 30, 'cush'); P.lounge_chair(c, it, 1650, 5800, 210, 'leather')
    CYL(it, 1550, 5100, 230, 0, 20, 'gold', 32); CYL(it, 1550, 5100, 60, 20, 480, 'traver', 20); CYL(it, 1550, 5100, 250, 480, 520, 'traver', 36)
    CYL(it, 1500, 5060, 60, 520, 700, 'ceramic', 18); CYL(it, 1620, 5150, 45, 520, 760, 'sculpt', 14)
    it = c.item('Lounge_Round_Rug', 'Decor'); PRZ(it, [(LX + 760 * math.cos(2 * math.pi * k / 64), LY + 700 * math.sin(2 * math.pi * k / 64)) for k in range(64)], 0, 8, 'rug1')
    PRZ(it, [(LX + 680 * math.cos(2 * math.pi * k / 64), LY + 620 * math.sin(2 * math.pi * k / 64)) for k in range(64)], 8, 10, 'rug2')
    it = c.item('Lounge_Sculptural_Pendant_Cluster', 'Lighting')
    for (dx_, dy_, zb) in ((0, 0, 1700), (180, -120, 1850), (-160, 140, 1950), (120, 200, 2050)):
        x, y = LX + dx_, LY + dy_
        CYL(it, x, y, 3, zb + 120, 2650, 'metal', 6); CYL(it, x, y, 120, zb, zb + 120, 'onyx', 20); CYL(it, x, y, 90, zb - 10, zb, 'lightw', 16)
    it = c.item('Lounge_Floor_Lamp', 'Lighting'); P.floor_lamp(c, it, 530, 6020)
    # ---------- NEW: entrance glass partition flush with shelter wall ----------
    it = c.item('Entry_Glass_Partition_Flush_with_Shelter_Wall', 'Partitions')
    x0, x1, y0, y1 = 2080, 2600, 6300, 6420
    B(it, x0, x1, y0, y1, 0, 60, 'charcoal'); B(it, x0, x1, y0, y1, 60, 950, 'wallp'); B(it, x0 - 2, x1 + 6, y0 - 6, y1 + 6, 950, 975, 'marble')
    B(it, x0, x1 - 10, y0 - 4, y0, 930, 936, 'led'); B(it, x0, x1 - 10, y1, y1 + 4, 930, 936, 'led')
    B(it, x1 - 40, x1, y0, y1, 975, 2550, 'frame'); B(it, x0, x0 + 30, y0, y1, 975, 2550, 'frame'); B(it, x0, x1, y0 + 40, y0 + 80, 2510, 2550, 'frame')
    B(it, x0 + 30, x1 - 40, y0 + 52, y0 + 68, 975, 2510, 'fglass')
    B(it, 1850, 2600, 6300, 6420, 2550, 2650, 'wallp')
    # ---------- shared rooms ----------
    K.dining9(c); K.foyer(c, corner='square'); K.curtains_bed(c); K.bedrooms(c, 'bed'); K.fans_ac(c, (3800, 2850))
    K.lights(c, ((5600, 8050), (7000, 8050), (8400, 8050), (2700, 7400), (9300, 4450), (10800, 4450), (9300, 5800), (12000, 5800), (925, 7600)))
    WA = c.wave(3950, 2950, 1150, 950, 0.4, 0.14); WB = c.wave(3950, 2950, 880, 680, 2.3, 0.16)
    it = c.item('False_Ceiling_Living_Organic_Wave_Cove', 'False_Ceiling')
    SLABH(it, [(2400, 1510), (5550, 1510), (5550, 3950), (5300, 3950), (5300, 4400), (2400, 4400)], WA, 2550, 2650, 'fceil', 'cove')
    c.downlights(it, [(2560, 1700), (3500, 1680), (4400, 1680), (5330, 1750), (5380, 3200), (2520, 3000), (2600, 4220), (3500, 4250), (4400, 4250)], 2550)
    it = c.item('False_Ceiling_Hall_with_Lounge_Dome', 'False_Ceiling')
    dome = [(1225 + 650 * math.cos(2 * math.pi * k / 48), 5500 + 620 * math.sin(2 * math.pi * k / 48)) for k in range(48)]
    SLABH(it, [(290, 3870), (2400, 3870), (2400, 4400), (5300, 4400), (5300, 4950), (5550, 4950), (5550, 6700), (3740, 6700), (3740, 6420), (2600, 6420), (2600, 6300), (290, 6300)], dome, 2550, 2650, 'fceil', 'cove')
    c.downlights(it, [(700, 4300), (1500, 4300), (2200, 4100), (3500, 4100), (4500, 4600), (4500, 5600), (3700, 6100), (4400, 6500), (2900, 5800), (2300, 5300)], 2550)
    K.ceil_rooms(c); K.led(c, [(7945, 7965, 5560, 6670)])
    # ---------- kitchen: closed + open + folding glass ----------
    K.kitchen_closed(c, 'Kitchen_Closed'); K.kitchen_common(c); K.kitchen_open(c, 'Kitchen_Open'); K.kitchen_glass(c)
    K.yard_baths(c)
    # ---------- improvements ----------
    K.power_common(c, [('x', 2248, -1, 1800, 1050), ('x', 2248, -1, 2550, 1050, True), ('x', 2248, -1, 3400, 1050),   # study desks
                       ('x', 2443, 1, 2350, 300, True), ('x', 2443, 1, 3050, 300),                                     # TV wall
                       ('f', 1225, 0, 5500, 0), ('x', 310, 1, 4700, 300),                                              # lounge
                       ('x', 4940, 1, 7200, 1150)])
    K.trunking_common(c, [[(360, 2750), (360, 3950), (2400, 3950), (2400, 4400), (5340, 4400)]])

HIDE_DEF = ['Ceiling', 'Beams_Highlight', 'Structural_Highlight', 'Kitchen_Door_Closed', 'Kitchen_Open', 'Kitchen_Glass_Open', 'Kitchen_Glass_Closed', 'Power_Points', 'Aircon_Trunking']
MODES = {
    'closed': {'label': 'Closed kitchen (door open)', 'hide': ['Kitchen_Door_Closed', 'Kitchen_Open', 'Kitchen_Glass_Open', 'Kitchen_Glass_Closed']},
    'closed_door': {'label': 'Closed kitchen (door shut)', 'hide': ['Kitchen_Door_Open', 'Kitchen_Open', 'Kitchen_Glass_Open', 'Kitchen_Glass_Closed']},
    'open': {'label': 'Open kitchen – glass folded away', 'hide': ['Kitchen_Closed', 'Kitchen_Door_Closed', 'Kitchen_Door_Open', 'Kitchen_Glass_Closed']},
    'open_glass': {'label': 'Open kitchen – glass closed', 'hide': ['Kitchen_Closed', 'Kitchen_Door_Closed', 'Kitchen_Door_Open', 'Kitchen_Glass_Open']},
}
VIEWS = [
 ('Overview', (-3500, 14500, 15500), (7300, 4800, 0), 40, 'top'),
 ('Plan (annotated)', (7300, 4800, 60000), (7300, 4799, 0), 11.5, 'plan'),
 ('CMP 1 · Living from dining side', (5000, 4300, 1650), (2400, 2300, 900), 80, ''),
 ('CMP 2 · Living from window side', (3300, 1700, 1650), (5400, 3800, 700), 85, ''),
 ('CMP 3 · Hall towards kitchen', (4300, 4100, 1600), (7000, 6000, 700), 80, ''),
 ('CMP 4 · Hall from the foyer', (3000, 8050, 1600), (1500, 5200, 1150), 70, ''),
 ('Living – TV wall and console', (5150, 2700, 1450), (2440, 2700, 950), 70, ''),
 ('Living – organic wave ceiling', (5100, 4050, 1250), (3950, 2950, 2600), 88, ''),
 ('Lounge – backlit onyx feature wall', (3400, 4500, 1550), (300, 5600, 1200), 68, ''),
 ('Lounge – from living room', (3300, 3300, 1600), (900, 5300, 900), 75, ''),
 ('Lounge – pendant and dome ceiling', (2300, 4300, 1300), (1225, 5500, 2600), 85, ''),
 ('Study door – clear approach from the lounge', (2350, 4450, 1600), (700, 3880, 1100), 75, ''),
 ('Entrance partition – from foyer', (3150, 7900, 1550), (2250, 6300, 1250), 62, ''),
 ('Entrance partition – from lounge', (1300, 4300, 1600), (2350, 6360, 1100), 75, ''),
 ('Study – two standing desks', (550, 2600, 1650), (2250, 2600, 1100), 80, ''),
 ('Study – towards half-glass wall', (1000, 1650, 1600), (1700, 3850, 1100), 80, ''),
 ('Study – from living through glass', (2500, 5000, 1600), (1500, 2600, 1100), 70, ''),
 ('Dining – table for 8', (4300, 4100, 1600), (7000, 6000, 700), 80, ''),
 ('Dining – from pantry end', (7950, 4300, 1600), (4500, 6200, 800), 80, ''),
 ('Dining – coffer ceiling and fan', (4500, 4000, 1300), (6800, 5600, 2500), 85, ''),
] + VC.KITCHEN_OPEN_VIEWS + [v if not v[0].startswith('NIGHT · Living') else ('NIGHT · Living and lounge', (5000, 4300, 1650), (1500, 4300, 1000), 85, 'night') for v in VC.tail(True)]
LABELS = [
 ('Living', 3900, 2600), ('Lounge (feature space)', 1225, 5600), ('Clear path to study door', 900, 4300), ('Study', 1250, 2600), ('Dining', 6150, 5600), ('Dry pantry', 8150, 5850),
 ('Kitchen', 5900, 8000), ('Service yard', 8900, 8000), ('Foyer', 2700, 7500), ('Household shelter', 900, 7600), ('Bedroom 3', 7000, 1500),
 ('Bedroom 2 (kids)', 10000, 1800), ('Master bedroom', 12900, 2600), ('Common bath', 9900, 6000), ('Ensuite', 12000, 6000),
]
DIMS = [
 ((2600, 6360), (3740, 6360), 'Clear way in from foyer ≈ 1140'),
 ((5150, 5050), (7150, 5050), 'Table 2000 × 1000'), ((4600, 4700), (4600, 3900), 'Walkway to bedrooms ≈ 800'),
 ((700, 3880), (700, 4780), 'Clear in front of study door ≈ 900'),
 ((5850, 2700), (8400, 2700), 'Bedroom 3 width 2550'),
]
INFO = ("Plan B. Changes: hall cabinets removed – the zone is now a lounge (set back to keep a ~900 mm clear path to the study door) with a backlit onyx feature wall, two lounge chairs, "
        "side table, sculpture, round rug, dome cove ceiling and pendant cluster. New entrance partition sits in line with the household-shelter wall face "
        "(x 2080–2600), freestanding with a shadow gap – nothing fixed to the shelter. Kitchen: closed or open version; open keeps the stove-side top cabinets "
        "with a ducted hood, tall units at the yard end, a counter facing dining and bi-fold glass that can close the kitchen. "
        "Note: removing the kitchen front wall must be confirmed with HDB / your ID. Power points and aircon trunking are indicative only.")
