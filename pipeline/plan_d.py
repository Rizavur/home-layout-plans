import math
import planlib as P, blocks as K, views_common as VC
def build(c):
    B, CYL, PRZ, RRECT, SLABH, RR = c.B, c.CYL, c.PRZ, c.RRECT, c.SLABH, c.RR
    K.fixtures(c)
    # ---- v13 hall joinery (rebuilt from its dimensions) ----
    it = c.item('TV_Feature_Wall_Seamless_Marble', 'Furniture'); B(it, 250, 296, 1665, 3535, 0, 2650, 'marble')
    it = c.item('Joinery_TV_Wall_Tall_Cabinet_and_Display_Bay', 'Furniture')
    c.cabinet(it, '+x', 3538, 4500, 650, 400, 0, 2650, 2, K.WM, 100, [2250], 'bar', hm='gold')
    c.cabinet(it, '+x', 5000, 5840, 650, 400, 0, 2650, 2, K.WM, 100, [2250], 'bar', hm='gold')
    B(it, 250, 650, 4500, 5000, 0, 900, K.WM); B(it, 250, 650, 4500, 5000, 2250, 2650, K.WM); B(it, 250, 270, 4500, 5000, 900, 2250, 'walnut')
    for z in (900, 1350, 1800): B(it, 270, 650, 4500, 5000, z, z + 25, 'marble'); B(it, 280, 640, 4510, 4520, z + 445 - 6 if z < 1800 else 2244, z + 445 if z < 1800 else 2250, 'led')
    CYL(it, 450, 4750, 70, 925, 1150, 'ceramic', 18); CYL(it, 450, 4750, 60, 1375, 1450, 'sculpt', 16)
    it = c.item('Joinery_Living_Tall_Cabinets_with_Corner_Niche', 'Furniture')
    c.cabinet(it, '-y', 700, 2060, 5842, 458, 0, 2650, 3, K.WM, 100, [2250], 'bar', hm='gold')
    B(it, 250, 700, 5842, 6300, 0, 450, K.WM); B(it, 250, 700, 5842, 6300, 2100, 2650, K.WM); B(it, 250, 700, 6280, 6300, 450, 2100, 'walnut')
    for z in (450, 1000, 1550): B(it, 270, 700, 5842, 6280, z, z + 25, 'marble')
    B(it, 650, 700, 5842, 6300, 450, 2100, K.WM); CYL(it, 470, 6060, 80, 475, 700, 'ceramic', 18); CYL(it, 470, 6060, 50, 1025, 1180, 'gold', 14)
    # ---- Living (A layout, TV on the seamless marble wall) ----
    it = c.item('TV_75_inch', 'Furniture'); B(it, 296, 326, 1750, 3410, 860, 1795, 'screen')
    it = c.item('TV_Console_Walnut_Fluted_Marble_Top', 'Furniture')
    PRZ(it, RR(296, 720, 1630, 3510, 110, (1, 0, 0, 0)), 240, 480, 'walnut'); y = 1740
    while y < 3500: CYL(it, 720, y, 13, 262, 456, 'walnut2', 8); y += 30
    PRZ(it, RR(296, 735, 1622, 3530, 115, (1, 0, 0, 0)), 480, 500, 'marble'); B(it, 640, 670, 1690, 3490, 234, 240, 'led')
    CYL(it, 520, 1860, 85, 500, 780, 'ceramic', 20); CYL(it, 530, 3275, 55, 500, 640, 'sculpt', 16)
    it = c.item('Living_L_Sofa_Boucle_with_Chaise', 'Furniture'); c.sofa2(it, '-x', 4420, 2745, 2390, 1000, 3, False, True, (-1195, -395, 800), 'sofa', 'sofa2', ('pil1', 'pil2'))
    it = c.item('Living_Loveseat_by_Window', 'Furniture'); c.sofa2(it, '+y', 3100, 2250, 1600, 820, 2, True, True, None, 'sofa', 'sofa2', ('pil2', 'pil1'))
    it = c.item('Living_Coffee_Table_Travertine_Pebble', 'Furniture'); P.ppebble(c, it, 2900, 2990, 520, 380, 0.7, 400, 'traver', 'walnut', True)
    it = c.item('Living_Wall_Art_Marble_Diptych', 'Decor'); P.painting(c, it, 'x', 5550, -1, 1990, 2730, 1050, 1950, 'artm'); P.painting(c, it, 'x', 5550, -1, 2790, 3530, 1050, 1950, 'artm')
    it = c.item('Curtains_Living', 'Curtains'); c.curtain_full(it, 290, 5550, 1375, 420, 420, 6, 2540)
    it = c.item('Living_Floor_Lamp', 'Lighting'); P.floor_lamp(c, it, 5150, 1700)
    WA = c.wave(3100, 2960, 1780, 960, 0.4, 0.14); WB = c.wave(3100, 2960, 1380, 640, 2.3, 0.16)
    it = c.item('False_Ceiling_Living_Organic_Wave_Cove', 'False_Ceiling')
    SLABH(it, [(296, 1510), (5550, 1510), (5550, 3950), (5300, 3950), (5300, 4400), (650, 4400), (650, 3538), (296, 3538)], WA, 2550, 2650, 'fceil', 'cove')
    c.downlights(it, [(470, 2200), (470, 2850), (1800, 1680), (2700, 1680), (3600, 1680), (4500, 1680), (1800, 4250), (2700, 4250), (3600, 4250), (4500, 4250), (5320, 1750), (5320, 3600)], 2550)
    it = c.item('False_Ceiling_Hall_around_Tall_Cabinets', 'False_Ceiling')
    SLABH(it, [(650, 4400), (5300, 4400), (5300, 4950), (5550, 4950), (5550, 5000), (5100, 5000), (5100, 6700), (3740, 6700), (3740, 6300), (2060, 6300), (2060, 5842), (650, 5842)],
          [(2950 + 600 * math.cos(2 * math.pi * k / 48), 5150 + 600 * math.sin(2 * math.pi * k / 48)) for k in range(48)], 2550, 2650, 'fceil', 'cove')
    c.downlights(it, [(900, 4600), (900, 5600), (1700, 5650), (4000, 4600), (4500, 5600), (3700, 6150), (4400, 6500), (2500, 6100)], 2550)
    K.dining9(c); K.foyer(c, 'round'); K.curtains_bed(c); K.bedrooms(c, br3='study')
    # ---- Bedroom 3 as the study: 2 x 1000 standing desks facing the window ----
    it = c.item('Bedroom3_Study_Two_Standing_Desks_Facing_Window', 'Furniture')
    for cx in (6450, 7550): P.sdesk(c, it, '-y', 1000, cx, 1000, 585); c.station(it, '-y', cx, 1000, 585)
    it = c.item('Bedroom3_Study_Chairs_x2', 'Furniture'); c.chair2(it, '-y', 6450, 1400); c.chair2(it, '-y', 7550, 1400)
    it = c.item('D1_Bedroom3_Study_Rug', 'D1_Study_Only'); PRZ(it, RRECT(6100, 7900, 1150, 2250, 100, 6), 0, 8, 'rug1'); PRZ(it, RRECT(6200, 7800, 1250, 2150, 80, 6), 8, 10, 'rug2')
    it = c.item('D2_Wall_Bed_Super_Single_FOLDED', 'D2_WallBed_Folded'); P.wallbed_folded(c, it, 8100, 8550, 1730, 2750)
    it = c.item('D2_Wall_Bed_Super_Single_DOWN', 'D2_WallBed_Down'); P.wallbed_down(c, it, 8100, 8550, 1730, 2750, 6450)
    K.fans_ac(c, (3700, 2800))
    K.lights(c, ((5600, 8050), (7000, 8050), (8400, 8050), (2700, 7400), (9300, 4450), (10800, 4450), (9300, 5800), (12000, 5800), (925, 7600)))
    K.ceil_rooms(c); K.led(c, [(7945, 7965, 5560, 6670)])
    K.kitchen_closed(c, 'Kitchen_Closed'); K.kitchen_common(c, stack=True); K.kitchen_open(c, 'Kitchen_Open'); K.kitchen_glass(c); K.yard_baths(c)
    # ---- Helper's tri-fold mattress in the service yard. Stacking the washer and dryer frees the space under the north counter.
    # Laid out: 800 wide x 1675 long x 100 mm, head at the washer, feet under the counter (open space x 8450-9290, 870 high).
    # By day it folds to 800 x 560 x 300 mm and slides under the counter.
    MX0, MX1, MY0, MY1 = 8470, 9270, 6965, 8640
    it = c.item('Yard_Trifold_Mattress_Folded_under_Counter', 'Yard_Mattress_Day')
    for k in range(3): P.soft_slab(c, it, c.RRECT(MX0, MX1, 6990, 7550, 30, 3), k * 100, k * 100 + 98, 'matf', 25, 2)
    it = c.item('Yard_Trifold_Mattress_800x1675_Head_at_Washer_Feet_under_Counter', 'Yard_Mattress_Night')
    seg = (MY1 - MY0) / 3.0
    for k in range(3):
        y0, y1 = MY0 + k * seg + (3 if k else 0), MY0 + (k + 1) * seg - (3 if k < 2 else 0)
        P.soft_slab(c, it, c.RRECT(MX0, MX1, y0, y1, 30, 4), 0, 100, 'matf', 30, 3)
    for k in (1, 2): c.B(it, MX0 + 20, MX1 - 20, MY0 + k * seg - 3, MY0 + k * seg + 3, 8, 92, 'charcoal')
    P.soft_slab(c, it, c.RRECT(MX0 + 90, MX1 - 90, MY1 - 400, MY1 - 40, 70, 5), 100, 230, 'linen2', 55, 3)      # pillow at the washer end
    P.soft_slab(c, it, c.RRECT(MX0 + 30, MX1 - 30, MY0 + 30, MY0 + 900, 40, 4), 100, 150, 'duvet', 25, 2)    # blanket over the feet end
    K.power_common(c, [('x', 296, 1, 2300, 300, True), ('x', 296, 1, 3000, 300), ('y', 350, 1, 6450, 1050, True), ('y', 350, 1, 7550, 1050), ('x', 8550, -1, 3100, 650), ('x', 4940, 1, 7200, 1150)])
    K.trunking_common(c, [[(360, 2750), (360, 3500), (700, 3500), (700, 4400), (5340, 4400)]])
D2 = ['D2_WallBed_Folded', 'D2_WallBed_Down']
MODES = {}
for k, v in VC.KMODES.items():
    MODES[k] = {'label': v['label'] + ' · D1 desks only', 'hide': v['hide'] + D2 + ['Yard_Mattress_Night']}
MODES['d2f'] = {'label': 'D2 · wall bed FOLDED (open kitchen)', 'hide': VC.KMODES['open']['hide'] + ['D1_Study_Only', 'D2_WallBed_Down', 'Yard_Mattress_Night']}
MODES['d2d'] = {'label': 'D2 · wall bed DOWN (open kitchen)', 'hide': VC.KMODES['open']['hide'] + ['D1_Study_Only', 'D2_WallBed_Folded', 'Yard_Mattress_Night']}
MODES['mat'] = {'label': 'Night · helper mattress laid out in the yard (open kitchen)', 'hide': VC.KMODES['open']['hide'] + D2 + ['Yard_Mattress_Day']}
VIEWS = VC.HEAD + [
 ('Living – sofas, pebble table, rug', (5300, 4400, 1650), (300, 1300, 700), 88, ''),
 ('Living – seamless marble TV wall', (3900, 2580, 1350), (296, 2580, 950), 75, ''),
 ('Hall – tall cabinets with display bay', (3400, 4000, 1600), (500, 5600, 1200), 80, ''),
 ('Hall – corner niche towards shelter', (3000, 4700, 1600), (900, 6200, 1200), 75, ''),
 ('Dining – table for 8 outside kitchen', (4300, 4100, 1600), (7000, 6000, 700), 80, ''),
 ('Dining – from pantry end', (7950, 4300, 1600), (4500, 6200, 800), 80, ''),
 ('D1 Bedroom 3 study – desks facing window', (7950, 3150, 1650), (6700, 500, 1000), 85, '', 'open'),
 ('D1 Bedroom 3 study – from window side', (7000, 1450, 1650), (6800, 3400, 900), 85, '', 'open'),
 ('D2 Bedroom 3 – wall bed FOLDED', (6250, 2050, 1600), (8550, 2240, 1200), 80, '', 'd2f'),
 ('D2 Bedroom 3 – desks with wall bed folded', (7950, 3150, 1650), (6700, 500, 1000), 85, '', 'd2f'),
 ('D2 Bedroom 3 – wall bed DOWN', (6050, 1500, 1700), (8300, 2400, 500), 80, '', 'd2d'),
 ('D2 Bedroom 3 – wall bed DOWN from door', (8200, 3500, 1650), (6900, 1800, 400), 85, '', 'd2d'),
 ('Yard – stacked washer and dryer', (8250, 7750, 1550), (8960, 9100, 1000), 80, ''),
 ('Yard – folded mattress under the counter', (8700, 8500, 1350), (8870, 7250, 300), 80, ''),
 ('Yard – mattress laid out at night', (8150, 8450, 2250), (8900, 7650, 0), 88, '', 'mat'),
 ('Yard – mattress, feet under the counter', (8870, 8560, 1700), (8870, 7100, 150), 88, '', 'mat'),
] + VC.KITCHEN_OPEN_VIEWS + VC.tail(False)
LABELS = VC.COMMON_LABELS + [('Living', 2900, 2600), ('Dining', 6150, 5600), ('Dry pantry', 8150, 5850), ('Bedroom 3 = study', 7000, 2000)]
DIMS = [((9285, 6965), (9285, 8640), 'Helper mattress 800 × 1675 (night)'), ((6450, 2750), (6450, 3200), 'Bed down → wardrobe ≈ 450'), ((5850, 1400), (8550, 1400), 'Bedroom 3 width 2700'), ((5150, 5050), (7150, 5050), 'Table 2000 × 1000'), ((4600, 4700), (4600, 3900), 'Walkway to bedrooms ≈ 800')]
INFO = ("Plan D. No study room – bedroom 3 is the study with two 1000 mm standing desks facing the window. D1 = desks only; D2 adds a fold-down "
        "super-single wall bed on the east wall (choose D2 in the option menu to see it folded or down). Hall tall cabinets and the seamless marble TV wall as in the earlier design "
        "(rebuilt from their dimensions, so details are simplified). Kitchen: closed or open with bi-fold glass; open keeps the stove-side top cabinets and a ducted hood. "
        "Removing the kitchen front wall must be confirmed with HDB / your ID. Power points and trunking are indicative."
        " Service yard: washer and dryer stacked in one corner, so the helper's 10 cm tri-fold mattress (800 × 1675) folds away under the yard counter by day and is laid out at night with the head at the washer and the feet under the counter – see the 'Night · helper mattress' option.")
