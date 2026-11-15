import math
import planlib as P, blocks as K, views_common as VC
def build(c):
    B, CYL, PRZ, RRECT, SLABH, RR = c.B, c.CYL, c.PRZ, c.RRECT, c.SLABH, c.RR
    K.fixtures(c)
    # ---- Living (8 Nov) ----
    it = c.item('Living_Dining_West_Wall_Flush_Cladding', 'Furniture'); B(it, 250, 290, 1170, 1520, 0, 2650, 'wallp'); B(it, 250, 290, 3820, 6300, 0, 2650, 'wallp')
    it = c.item('TV_Feature_Wall_Marble_with_Fluted_Walnut_Flanks', 'Furniture')
    B(it, 250, 290, 1700, 3640, 0, 2650, 'marble')
    for (y0, y1) in ((1520, 1697), (3643, 3820)):
        B(it, 250, 280, y0, y1, 0, 2650, 'walnut'); y = y0 + 12.0
        while y < y1 - 8: CYL(it, 280, y, 10, 0, 2650, 'walnut2', 8); y += 22
    B(it, 290, 293, 1800, 3540, 830, 1820, 'cove')
    it = c.item('TV_75_inch', 'Furniture'); B(it, 293, 323, 1840, 3500, 860, 1795, 'screen')
    it = c.item('TV_Console_Walnut_Fluted_Marble_Top', 'Furniture')
    PRZ(it, RR(290, 720, 1720, 3600, 110, (1, 0, 0, 0)), 240, 480, 'walnut'); y = 1830
    while y < 3590: CYL(it, 720, y, 13, 262, 456, 'walnut2', 8); y += 30
    PRZ(it, RR(290, 735, 1712, 3620, 115, (1, 0, 0, 0)), 480, 500, 'marble'); B(it, 290, 735, 3600, 3620, 0, 480, 'marble'); B(it, 640, 670, 1780, 3580, 234, 240, 'led')
    CYL(it, 520, 1950, 85, 500, 780, 'ceramic', 20); CYL(it, 530, 3365, 55, 500, 640, 'sculpt', 16)
    it = c.item('Living_L_Sofa_Boucle_with_Chaise', 'Furniture'); c.sofa2(it, '-x', 4420, 2745, 2390, 1000, 3, False, True, (-1195, -395, 800), 'sofa', 'sofa2', ('pil1', 'pil2'))
    it = c.item('Living_Loveseat_by_Window', 'Furniture'); c.sofa2(it, '+y', 3100, 2250, 1600, 820, 2, True, True, None, 'sofa', 'sofa2', ('pil2', 'pil1'))
    it = c.item('Living_Coffee_Table_Travertine_Pebble', 'Furniture'); P.ppebble(c, it, 2900, 2990, 520, 380, 0.7, 400, 'traver', 'walnut', True)
    CYL(it, 3100, 2950, 100, 400, 450, 'ceramic', 20)
    it = c.item('Living_Rug', 'Decor'); PRZ(it, RRECT(1600, 4550, 1700, 3950, 150, 6), 0, 8, 'rug1'); PRZ(it, RRECT(1720, 4430, 1820, 3830, 100, 6), 8, 10, 'rug2')
    it = c.item('Living_Wall_Art_Marble_Diptych', 'Decor'); P.painting(c, it, 'x', 5550, -1, 1990, 2730, 1050, 1950, 'artm'); P.painting(c, it, 'x', 5550, -1, 2790, 3530, 1050, 1950, 'artm')
    it = c.item('Curtains_Living', 'Curtains'); c.curtain_full(it, 290, 5550, 1375, 420, 420, 6, 2540)
    it = c.item('Living_Floor_Lamp', 'Lighting'); P.floor_lamp(c, it, 5150, 1700)
    # ---- Dining by the shelter ----
    # 1900 x 1000 table for 7
    chairs = [(x, 4335, '-y') for x in (700, 1300, 1900)] + [(x, 5795, '+y') for x in (700, 1300, 1900)] + [(2490, 5065, '+x')]
    P.dining_set(c, (340, 2240, 4565, 5565), chairs)
    it = c.item('Dining_Linear_Pendant', 'Lighting'); P.dining_pendant(c, it, 650, 1930, 5065)
    CYL(it, 790, 5065, 3, 1690, 2550, 'metal', 6); CYL(it, 1790, 5065, 3, 1690, 2550, 'metal', 6)
    it = c.item('Ceiling_Fan_Dining_42in', 'Lighting'); c.fan(it, 2950, 5300, 2300, 2550, 530)
    it = c.item('Dining_Wall_Aircon_West_Wall', 'Fixtures'); P.wall_aircon(c, it, '+x', 250, 4565, 5565, 2180)
    it = c.item('Dining_Bladeless_Tower_Fan', 'Furniture'); P.bladeless_fan(c, it, 2180, 6170, 1290, 5065)
    it = c.item('Dining_Centrepiece', 'Decor'); CYL(it, 1290, 5065, 110, 758, 800, 'ceramic', 24); CYL(it, 1290, 5065, 55, 800, 1020, 'ceramic', 18)
    # ---- Study room beside the kitchen, with options ----
    it = c.item('Study_Partition_Walls', 'Partitions')
    B(it, 5550, 5650, 5000, 6700, 0, 2650, 'wallp'); B(it, 5650, 5850, 5000, 5100, 0, 2250, 'wallp')
    B(it, 5850, 6280, 5000, 5100, 0, 2650, 'wallp'); B(it, 7600, 8400, 5000, 5100, 0, 2650, 'wallp'); B(it, 6280, 7600, 5000, 5100, 2100, 2650, 'wallp')
    it = c.item('Study_Sliding_Doors_Fluted_Glass', 'Partitions'); B(it, 6280, 7600, 5025, 5075, 2085, 2100, 'metal')
    for (a0, a1, y0) in ((6285, 6960, 5030), (6920, 7595, 5050)):
        B(it, a0, a1, y0, y0 + 18, 10, 2080, 'fglass'); B(it, a0, a0 + 30, y0 - 1, y0 + 19, 10, 2080, 'charcoal'); B(it, a1 - 30, a1, y0 - 1, y0 + 19, 10, 2080, 'charcoal')
        B(it, a0 + 30, a1 - 30, y0 - 1, y0 + 19, 10, 40, 'charcoal'); B(it, a0 + 30, a1 - 30, y0 - 1, y0 + 19, 2050, 2080, 'charcoal')
    it = c.item('Study_Full_Height_Cabinet_Sliding_Doors', 'Furniture')
    B(it, 7820, 8400, 5110, 6700, 100, 2650, K.WM); B(it, 7860, 8400, 5110, 6700, 0, 100, 'charcoal'); B(it, 7800, 7820, 5112, 5935, 100, 2620, K.WM); B(it, 7778, 7798, 5885, 6698, 100, 2620, K.WM)
    B(it, 7794, 7800, 5880, 5900, 850, 1650, 'gold'); B(it, 7772, 7778, 5905, 5925, 850, 1650, 'gold')
    it = c.item('Study_Ceiling_Light', 'Lighting'); CYL(it, 6975, 5900, 250, 2615, 2650, 'lightw', 32)
    it = c.item('Aircon_Study', 'Aircon'); P.aircon2(c, it, 'y', 5100, 1, 6400, 7300, 2340)
    it = c.item('OptA_Study_Two_Standing_Desks', 'Option_A_Study_Desks')
    for cx in (6170, 7250): P.sdesk(c, it, '+y', 6100, cx, 1000, 585); c.station(it, '+y', cx, 6100, 585)
    it = c.item('OptA_Study_Chairs_x2', 'Option_A_Study_Desks'); c.chair2(it, '+y', 6170, 5700); c.chair2(it, '+y', 7250, 5700)
    it = c.item('OptB_Study_as_Single_Bedroom', 'Option_B_Study_Single_Bed'); P.bed2(c, it, 5650, 7650, 5650, 6680, '-x', 1); c.nightstand(it, 5660, 6060, 5170, 5560)
    it = c.item('OptB_Study_Painting', 'Option_B_Study_Single_Bed'); P.painting(c, it, 'x', 5650, 1, 5800, 6550, 1250, 1800, 'artw')
    # ---- Dry pantry on study partition (8 Nov) ----
    it = c.item('Dry_Pantry_Full_Width_Cabinet_and_Mirror', 'Furniture')
    c.cabinet(it, '-x', 5530, 6700, 5100, 450, 0, 850, 2, K.WM, 100, None, 'bar', hm='gold'); c.cabinet(it, '-x', 5000, 5527, 5100, 450, 480, 850, 1, K.WM, 0, None, 'bar', hm='gold')
    B(it, 5100, 5550, 5000, 5020, 0, 480, K.WM); B(it, 5100, 5550, 5507, 5527, 0, 480, K.WM); B(it, 5110, 5540, 5020, 5507, 470, 480, 'charcoal')
    B(it, 5400, 5540, 5130, 5390, 0, 420, 'metal'); CYL(it, 5265, 5260, 160, 0, 92, 'metal', 32)
    B(it, 5090, 5550, 5000, 6700, 850, 880, 'sintered'); B(it, 5528, 5550, 5030, 6670, 900, 2615, 'mirror')
    B(it, 5520, 5550, 5010, 5030, 880, 2635, 'gold'); B(it, 5520, 5550, 6670, 6690, 880, 2635, 'gold'); B(it, 5520, 5550, 5030, 6670, 2615, 2635, 'gold')
    # ---- Bedroom 3 options ----
    it = c.item('OptA_Bedroom3_Queen_Bed', 'Option_A_Bedroom3_Bed'); P.bed2(c, it, 5850, 7850, 700, 2230, '-x', 2)
    P.painting(c, it, 'x', 5850, 1, 850, 2100, 1300, 2000, 'artw'); PRZ(it, RRECT(6450, 8250, 500, 2500, 60, 4), 0, 10, 'rug2')
    it = c.item('OptB_Bedroom3_Two_Standing_Desks', 'Option_B_Bedroom3_Desks')
    for cy in (1200, 2300): P.sdesk(c, it, '+x', 7950, cy, 1050, 585); c.station(it, '+x', 7950, cy, 585); c.chair2(it, '+x', 7550, cy)
    PRZ(it, RRECT(6400, 7700, 900, 2600, 60, 4), 0, 10, 'rug2')
    K.bedrooms(c, br3='none'); K.foyer(c, 'round'); K.curtains_bed(c); K.fans_ac(c, (3700, 2800))
    K.lights(c, ((5600, 8050), (7000, 8050), (8400, 8050), (2700, 7400), (7500, 4450), (9300, 4450), (10800, 4450), (9300, 5800), (12000, 5800), (925, 7600)))
    WA = c.wave(3100, 2960, 1780, 960, 0.4, 0.14); WB = c.wave(3100, 2960, 1380, 640, 2.3, 0.16)
    it = c.item('False_Ceiling_Living_Organic_Wave_Cove', 'False_Ceiling')
    SLABH(it, [(290, 1510), (5550, 1510), (5550, 3950), (5300, 3950), (5300, 4400), (290, 4400)], WA, 2550, 2650, 'fceil', 'cove')
    c.downlights(it, [(470, 2200), (470, 2850), (470, 3500), (1800, 1680), (2700, 1680), (3600, 1680), (4500, 1680), (1800, 4250), (2700, 4250), (3600, 4250), (4500, 4250), (5320, 1750), (5320, 3600)], 2550)
    it = c.item('False_Ceiling_Dining_and_Hall', 'False_Ceiling')
    SLABH(it, [(290, 4400), (2200, 4400), (2200, 6300), (290, 6300)], RRECT(420, 1860, 4600, 5530, 120, 6), 2550, 2650, 'fceil', 'cove')
    SLABH(it, [(2200, 4400), (5300, 4400), (5300, 4950), (5550, 4950), (5550, 5000), (5100, 5000), (5100, 6700), (3740, 6700), (3740, 6300), (2200, 6300)],
          [(2950 + 650 * math.cos(2 * math.pi * k / 48), 5300 + 650 * math.sin(2 * math.pi * k / 48)) for k in range(48)], 2550, 2650, 'fceil', 'cove')
    c.downlights(it, [(900, 4490), (1500, 4490), (900, 5700), (1500, 5700), (2400, 4550), (3600, 4550), (4500, 4600), (4500, 5600), (3700, 6150), (4400, 6500)], 2550)
    K.ceil_rooms(c); K.led(c, [(7825, 7845, 5140, 6670), (5125, 5145, 5560, 6670)])
    K.kitchen_closed(c, 'Kitchen'); K.kitchen_common(c); K.yard_baths(c)
    K.power_common(c, [('x', 293, 1, 2350, 300, True), ('x', 293, 1, 3050, 300), ('y', 6685, -1, 5900, 1050, True), ('y', 6685, -1, 7500, 1050), ('x', 8535, -1, 1750, 1050, True)])
    K.trunking_common(c, [[(6850, 5320), (6850, 4400)], [(360, 2750), (360, 4400), (5340, 4400)]])
MODES = {
    'optA': {'label': 'Option A – study room with 2 desks · bedroom 3 queen bed', 'hide': ['Option_B_Study_Single_Bed', 'Option_B_Bedroom3_Desks', 'Kitchen_Door_Closed']},
    'optB': {'label': 'Option B – study as single bedroom · bedroom 3 as study', 'hide': ['Option_A_Study_Desks', 'Option_A_Bedroom3_Bed', 'Kitchen_Door_Closed']},
    'optA_door': {'label': 'Option A – kitchen door shut', 'hide': ['Option_B_Study_Single_Bed', 'Option_B_Bedroom3_Desks', 'Kitchen_Door_Open']},
}
VIEWS = VC.HEAD + [
 ('Living – sofas, pebble table, rug', (5300, 4400, 1650), (300, 1300, 700), 88, ''),
 ('Living – TV wall and console', (3900, 2670, 1350), (290, 2670, 950), 75, ''),
 ('Living – organic wave ceiling', (4900, 4250, 1250), (2700, 2700, 2650), 88, ''),
 ('Dining – table for 7 by the shelter', (3300, 4200, 1550), (800, 5300, 700), 75, ''),
 ('Dining – from the shelter side', (1300, 6150, 1600), (1500, 3300, 900), 85, ''),
 ('Dining – false ceiling, pendant, fan', (4600, 4300, 1300), (1600, 5300, 2500), 85, ''),
 ('Dry pantry – mirror and robot bay', (2600, 4300, 1500), (5550, 5850, 1300), 72, ''),
 ('Study room – Option A two standing desks', (6950, 5300, 1650), (6950, 6700, 700), 90, '', 'optA'),
 ('Study room – Option B single bedroom', (7600, 5300, 1650), (5700, 6600, 600), 85, '', 'optB'),
 ('Bedroom 3 – Option A queen bed', (8350, 3450, 1650), (5850, 1450, 1200), 88, '', 'optA'),
 ('Bedroom 3 – Option B two standing desks', (6450, 2950, 1650), (8550, 1300, 700), 85, '', 'optB'),
 ('Kitchen (closed) – inside', (4300, 7150, 1650), (7800, 9250, 800), 88, '', 'optA'),
 ('Kitchen – towards the door', (7300, 8600, 1600), (4300, 6800, 1000), 85, '', 'optA'),
 ('Kitchen – from the service yard end', (7550, 8050, 1600), (3900, 7600, 1000), 85, '', 'optA'),
 ('Kitchen – door shut', (3000, 5200, 1600), (4600, 6900, 1100), 70, '', 'optA_door'),
] + VC.tail(False)
LABELS = VC.COMMON_LABELS + [('Living', 2900, 2600), ('Dining', 1150, 5065), ('Study room', 6950, 5900), ('Dry pantry', 5300, 5850), ('Bedroom 3', 7000, 1500)]
DIMS = [((2715, 5065), (5090, 5065), 'Dining chair → pantry ≈ 2370'), ((340, 4510), (2240, 4510), 'Table 1900 × 1000'), ((5650, 5900), (7800, 5900), 'Study room width 2150'), ((5850, 2700), (8400, 2700), 'Bedroom 3 width 2550')]
INFO = ("Plan A – the original layout. Dining table for 7 by the household shelter, study room beside the kitchen, closed kitchen. "
        "Use the option menu to switch between Option A (study room with 2 standing desks, bedroom 3 queen bed) and Option B (study room as a single bedroom, "
        "bedroom 3 with 2 standing desks). Only the improvements were added here: comparison views, annotated plan, power points, aircon trunking, night mood. "
        "Power points and trunking are indicative only.")
