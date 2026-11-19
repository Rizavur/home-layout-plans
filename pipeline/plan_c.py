import math
import planlib as P, blocks as K, views_common as VC
def build(c):
    B, CYL, PRZ, RRECT, SLABH, RR = c.B, c.CYL, c.PRZ, c.RRECT, c.SLABH, c.RR
    K.fixtures(c)
    # ---- Living: TV and sofas SWAPPED (TV on east wall, sofas on west) ----
    it = c.item('Living_West_Wall_Cladding', 'Furniture'); B(it, 250, 290, 1170, 6300, 0, 2650, 'wallp')
    it = c.item('TV_Wall_East_Acoustic_Backing', 'Furniture'); B(it, 5525, 5550, 1520, 3820, 0, 2650, 'acoustic')
    it = c.item('TV_Feature_Wall_East_Marble_with_Fluted_Walnut_Flanks', 'Furniture')
    B(it, 5485, 5525, 1700, 3640, 0, 2650, 'marble')
    for (y0, y1) in ((1520, 1697), (3643, 3820)):
        B(it, 5495, 5525, y0, y1, 0, 2650, 'walnut'); y = y0 + 12.0
        while y < y1 - 8: CYL(it, 5495, y, 10, 0, 2650, 'walnut2', 8); y += 22
    B(it, 5482, 5485, 1800, 3540, 830, 1820, 'cove')
    it = c.item('TV_75_inch', 'Furniture'); B(it, 5452, 5482, 1840, 3500, 860, 1795, 'screen')
    it = c.item('TV_Console_Walnut_Fluted_Marble_Top', 'Furniture')
    PRZ(it, RR(5050, 5485, 1720, 3600, 110, (0, 0, 0, 1)), 240, 480, 'walnut'); y = 1830
    while y < 3590: CYL(it, 5050, y, 13, 262, 456, 'walnut2', 8); y += 30
    PRZ(it, RR(5035, 5485, 1712, 3620, 115, (0, 0, 0, 1)), 480, 500, 'marble'); B(it, 5035, 5485, 3600, 3620, 0, 480, 'marble'); B(it, 5100, 5130, 1780, 3580, 234, 240, 'led')
    CYL(it, 5250, 1950, 85, 500, 780, 'ceramic', 20); CYL(it, 5240, 3365, 55, 500, 640, 'sculpt', 16)
    it = c.item('Living_L_Sofa_West_Side_Facing_TV', 'Furniture'); c.sofa2(it, '+x', 1330, 2745, 2390, 1000, 3, True, False, (395, 1195, 800), 'sofa', 'sofa2', ('pil1', 'pil2'))
    it = c.item('Living_Loveseat_by_Window', 'Furniture'); c.sofa2(it, '+y', 2900, 2250, 1600, 820, 2, True, True, None, 'sofa', 'sofa2', ('pil2', 'pil1'))
    it = c.item('Living_Coffee_Table_Travertine_Pebble', 'Furniture'); P.ppebble(c, it, 2950, 2990, 520, 380, 0.7, 400, 'traver', 'walnut', True); CYL(it, 3150, 2950, 100, 400, 450, 'ceramic', 20)
    it = c.item('Living_Wall_Art_Marble_Diptych_above_Sofa', 'Decor'); P.painting(c, it, 'x', 290, 1, 1990, 2730, 1050, 1950, 'artm'); P.painting(c, it, 'x', 290, 1, 2790, 3530, 1050, 1950, 'artm')
    it = c.item('Curtains_Living', 'Curtains'); c.curtain_full(it, 290, 5550, 1375, 420, 420, 6, 2540)
    it = c.item('Living_Floor_Lamp', 'Lighting'); P.floor_lamp(c, it, 1750, 1700)
    # ---- Study by the shelter ----
    it = c.item('Study_North_Half_Glass_Wall_Framed', 'Partitions')
    B(it, 290, 1980, 4300, 4400, 0, 1000, 'wallp'); B(it, 290, 1988, 4292, 4408, 1000, 1020, 'marble')
    B(it, 290, 330, 4300, 4400, 1020, 2550, 'frame'); B(it, 1940, 1980, 4300, 4400, 1020, 2550, 'frame'); B(it, 1115, 1155, 4330, 4370, 1020, 2550, 'frame')
    B(it, 330, 1940, 4330, 4370, 2510, 2550, 'frame'); B(it, 330, 1115, 4342, 4358, 1020, 2510, 'glass'); B(it, 1155, 1940, 4342, 4358, 1020, 2510, 'glass'); B(it, 290, 2080, 4300, 4400, 2550, 2650, 'wallp')
    it = c.item('Study_East_Wall_Flush_with_Shelter', 'Partitions')
    B(it, 1980, 2080, 4300, 5300, 0, 2650, 'wallp'); B(it, 1980, 2080, 5300, 6200, 2100, 2650, 'wallp'); B(it, 1980, 2080, 6200, 6300, 0, 2650, 'wallp')
    it = c.item('Study_Sliding_Door_Fluted_Glass', 'Partitions')
    B(it, 2085, 2115, 4400, 6260, 2080, 2100, 'metal'); B(it, 2090, 2108, 5290, 6230, 10, 2075, 'fglass')
    B(it, 2089, 2109, 5290, 5320, 10, 2075, 'charcoal'); B(it, 2089, 2109, 6200, 6230, 10, 2075, 'charcoal'); B(it, 2089, 2109, 5320, 6200, 10, 40, 'charcoal'); B(it, 2089, 2109, 5320, 6200, 2045, 2075, 'charcoal')
    it = c.item('Study_Two_Standing_Desks_on_West_Wall', 'Furniture')
    for cy in (4875, 5825): P.sdesk(c, it, '-x', 890, cy, 850, 585); c.station(it, '-x', 890, cy, 585)
    c.cabinet(it, '+x', 4440, 6240, 640, 350, 1650, 2550, 4, 'white', 0, None, 'bar', hm='gold'); B(it, 610, 630, 4460, 6220, 1644, 1650, 'led')
    it = c.item('Study_Chairs_x2', 'Furniture'); c.chair2(it, '-x', 1290, 4875); c.chair2(it, '-x', 1290, 5825)
    it = c.item('Aircon_Study_on_East_Wall', 'Aircon'); P.aircon2(c, it, 'x', 1980, -1, 4500, 5200, 2230)
    it = c.item('False_Ceiling_Study', 'False_Ceiling'); SLABH(it, [(290, 4400), (1980, 4400), (1980, 6300), (290, 6300)], RRECT(800, 1830, 4700, 6000, 150, 6), 2550, 2650, 'fceil', 'cove')
    c.downlights(it, [(500, 4550), (500, 6150), (1830, 6150), (1400, 4550)], 2550)
    WA = c.wave(3100, 2960, 1780, 960, 0.4, 0.14); WB = c.wave(3100, 2960, 1380, 640, 2.3, 0.16)
    it = c.item('False_Ceiling_Living_Organic_Wave_Cove', 'False_Ceiling')
    SLABH(it, [(290, 1510), (5550, 1510), (5550, 3950), (5300, 3950), (5300, 4400), (2080, 4400), (2080, 4300), (290, 4300)], WA, 2550, 2650, 'fceil', 'cove')
    c.downlights(it, [(470, 2200), (470, 2850), (470, 3500), (1800, 1680), (2700, 1680), (3600, 1680), (4500, 1680), (2700, 4250), (3600, 4250), (4500, 4250), (5320, 1750), (5320, 3600)], 2550)
    it = c.item('False_Ceiling_Hall_Zone', 'False_Ceiling')
    SLABH(it, [(2080, 4400), (5300, 4400), (5300, 4950), (5550, 4950), (5550, 5000), (5100, 5000), (5100, 6700), (3740, 6700), (3740, 6300), (2080, 6300)],
          [(3000 + 600 * math.cos(2 * math.pi * k / 48), 5350 + 600 * math.sin(2 * math.pi * k / 48)) for k in range(48)], 2550, 2650, 'fceil', 'cove')
    c.downlights(it, [(2100, 4600), (2100, 6100), (3900, 4600), (4500, 5600), (3700, 6150), (4400, 6500)], 2550)
    K.dining9(c); K.foyer(c, 'niche'); K.curtains_bed(c); K.bedrooms(c, 'bed'); K.fans_ac(c, (3000, 2800))
    K.lights(c, ((5600, 8050), (7000, 8050), (8400, 8050), (2700, 7400), (9300, 4450), (10800, 4450), (9300, 5800), (12000, 5800), (925, 7600)))
    K.ceil_rooms(c); K.led(c, [(7945, 7965, 5560, 6670)])
    K.kitchen_closed(c, 'Kitchen_Closed'); K.kitchen_common(c); K.kitchen_open(c, 'Kitchen_Open'); K.kitchen_glass(c); K.yard_baths(c)
    K.power_common(c, [('x', 5452, -1, 2350, 300, True), ('x', 5452, -1, 3050, 300), ('x', 290, 1, 1600, 300), ('x', 290, 1, 4100, 300),
                       ('x', 296, 1, 4600, 1050, True), ('x', 296, 1, 5500, 1050), ('x', 4940, 1, 7200, 1150)])
    K.trunking_common(c, [[(1870, 4850), (1870, 4400), (5340, 4400)]])
MODES = VC.KMODES
VIEWS = VC.HEAD + [
 ('Living – TV wall now on the east side', (1500, 2700, 1350), (5500, 2700, 950), 75, ''),
 ('Living – sofas on the west side', (4800, 4100, 1600), (600, 2400, 800), 80, ''),
 ('Living – organic wave ceiling', (4300, 4200, 1250), (2700, 2700, 2650), 88, ''),
 ('Study – two standing desks', (1600, 5350, 1650), (300, 5350, 1200), 85, ''),
 ('Study – from living through half glass', (2600, 3000, 1600), (900, 5500, 1000), 70, ''),
 ('Study – wall flush with shelter cabinets, sliding door', (3500, 5000, 1600), (2100, 6000, 1200), 75, ''),
 ('Hall – key niche by the study door', (3150, 5900, 1500), (2050, 6420, 1150), 60, ''),
 ('Dining – table for 8 outside kitchen', (4300, 4100, 1600), (7000, 6000, 700), 80, ''),
 ('Dining – from pantry end', (7950, 4300, 1600), (4500, 6200, 800), 80, ''),
] + VC.KITCHEN_OPEN_VIEWS + VC.tail(True)
LABELS = VC.COMMON_LABELS + [('Living', 3000, 2600), ('Study', 1130, 5300), ('Dining', 6150, 5600), ('Dry pantry', 8150, 5850), ('Bedroom 3', 7000, 1500)]
DIMS = [((1330, 2745), (5452, 2745), 'Sofa → TV ≈ 4120'), ((290, 5300), (1980, 5300), 'Study width 1690'), ((5150, 5050), (7150, 5050), 'Table 2000 × 1000'), ((4600, 4700), (4600, 3900), 'Walkway to bedrooms ≈ 800')]
INFO = ("Plan C. Changes: the TV and sofas are swapped – the marble TV wall, 75\" TV and console now sit on the east wall (bedroom 3 side, with an acoustic "
        "backing layer), and the L-sofa with chaise sits on the west side facing it, with the marble diptych above. Sofa users now face away from the study glass. "
        "Study by the shelter, its wall now flush with the shelter cabinet fronts, and a straight key niche at the end of the cabinet run; dining outside the kitchen. Kitchen: closed or open, open keeps the stove-side top cabinets "
        "with a ducted hood, tall units at the yard end and bi-fold glass to close it. Removing the kitchen front wall must be confirmed with HDB / your ID. "
        "Power points and trunking are indicative.")
