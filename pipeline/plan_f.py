import math
import planlib as P, blocks as K, views_common as VC
def build(c):
    B, CYL, PRZ, RRECT, SLABH, RR = c.B, c.CYL, c.PRZ, c.RRECT, c.SLABH, c.RR
    K.fixtures(c)
    # ---- TV wall and one tall storage cabinet south of it ----
    it = c.item('TV_Feature_Wall_Seamless_Marble', 'Furniture'); B(it, 250, 296, 1665, 3535, 0, 2650, 'marble')
    it = c.item('Living_Tall_Storage_Cabinet', 'Furniture')
    c.cabinet(it, '+x', 3538, 4400, 650, 400, 0, 2650, 2, K.WM, 100, [2250], 'bar', hm='gold')
    # ---- Open study nook by the west wall (no walls: shares light with the living room) ----
    it = c.item('Study_Nook_Two_Standing_Desks_on_West_Wall', 'Furniture')
    for cy in (4875, 5825): P.sdesk(c, it, '-x', 890, cy, 850, 585); c.station(it, '-x', 890, cy, 585)
    it = c.item('Study_Nook_Wall_Cabinets_and_Shelf', 'Furniture')
    c.cabinet(it, '+x', 4440, 6240, 640, 350, 1650, 2550, 4, 'white', 0, None, 'bar', hm='gold'); B(it, 610, 630, 4460, 6220, 1644, 1650, 'led')
    B(it, 296, 520, 4440, 6240, 1380, 1405, 'walnut')
    for (cy, h) in ((4700, 220), (5050, 180), (5950, 240)): B(it, 330, 500, cy, cy + 40 + h // 6, 1405, 1405 + h, 'linen2')
    CYL(it, 420, 6100, 60, 1405, 1560, 'ceramic', 16)
    it = c.item('Study_Nook_Chairs_x2', 'Furniture'); c.chair2(it, '-x', 1290, 4875); c.chair2(it, '-x', 1290, 5825)
    it = c.item('Study_Nook_Rug', 'Decor'); PRZ(it, RRECT(950, 1850, 4500, 6200, 80, 5), 0, 8, 'rug1')
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
    it = c.item('Living_Rug', 'Decor'); PRZ(it, RRECT(1600, 4550, 1700, 3950, 150, 6), 0, 8, 'rug1'); PRZ(it, RRECT(1720, 4430, 1820, 3830, 100, 6), 8, 10, 'rug2')
    it = c.item('Living_Wall_Art_Marble_Diptych', 'Decor'); P.painting(c, it, 'x', 5550, -1, 1990, 2730, 1050, 1950, 'artm'); P.painting(c, it, 'x', 5550, -1, 2790, 3530, 1050, 1950, 'artm')
    it = c.item('Curtains_Living', 'Curtains'); c.curtain_full(it, 290, 5550, 1375, 420, 420, 6, 2540)
    it = c.item('Living_Floor_Lamp', 'Lighting'); P.floor_lamp(c, it, 5150, 1700)
    WA = c.wave(3100, 2960, 1780, 960, 0.4, 0.14); WB = c.wave(3100, 2960, 1380, 640, 2.3, 0.16)
    it = c.item('False_Ceiling_Living_Organic_Wave_Cove', 'False_Ceiling')
    SLABH(it, [(296, 1510), (5550, 1510), (5550, 3950), (5300, 3950), (5300, 4400), (650, 4400), (650, 3538), (296, 3538)], WA, 2550, 2650, 'fceil', 'cove')
    c.downlights(it, [(470, 2200), (470, 2850), (1800, 1680), (2700, 1680), (3600, 1680), (4500, 1680), (1800, 4250), (2700, 4250), (3600, 4250), (4500, 4250), (5320, 1750), (5320, 3600)], 2550)
    it = c.item('False_Ceiling_Hall_around_Tall_Cabinets', 'False_Ceiling')
    SLABH(it, [(650, 4400), (5300, 4400), (5300, 4950), (5550, 4950), (5550, 5000), (5100, 5000), (5100, 6700), (3740, 6700), (3740, 6300), (296, 6300), (296, 4400)],
          [(2950 + 600 * math.cos(2 * math.pi * k / 48), 5300 + 600 * math.sin(2 * math.pi * k / 48)) for k in range(48)], 2550, 2650, 'fceil', 'cove')
    c.downlights(it, [(1000, 4875), (1000, 5825), (1900, 4600), (1900, 6150), (4000, 4600), (4500, 5600), (3700, 6150), (4400, 6500)], 2550)
    K.dining9(c); K.foyer(c, 'square'); K.curtains_bed(c); K.bedrooms(c, 'bed')
    K.fans_ac(c, (3700, 2800))
    K.lights(c, ((5600, 8050), (7000, 8050), (8400, 8050), (2700, 7400), (9300, 4450), (10800, 4450), (9300, 5800), (12000, 5800), (925, 7600)))
    K.ceil_rooms(c); K.led(c, [(7945, 7965, 5560, 6670)])
    K.kitchen_closed(c, 'Kitchen_Closed'); K.kitchen_common(c); K.kitchen_open(c, 'Kitchen_Open'); K.kitchen_glass(c); K.yard_baths(c)
    K.power_common(c, [('x', 296, 1, 2300, 300, True), ('x', 296, 1, 3000, 300), ('x', 296, 1, 4600, 1050, True), ('x', 296, 1, 5500, 1050), ('x', 8550, -1, 3100, 650), ('x', 4940, 1, 7200, 1150)])
    K.trunking_common(c, [[(360, 2750), (360, 3500), (700, 3500), (700, 4400), (5340, 4400)]])

MODES = VC.KMODES
VIEWS = VC.HEAD + [
 ('Living – sofas', (5300, 4400, 1650), (300, 1300, 700), 88, ''),
 ('Living – marble TV wall', (3900, 2580, 1350), (296, 2580, 950), 75, ''),
 ('Study nook – desks for two', (2300, 5350, 1650), (300, 5350, 1150), 85, ''),
 ('Study nook – from the sofa', (3600, 2600, 1300), (900, 5400, 1000), 70, ''),
 ('Dining – table for 8', (4300, 4100, 1600), (7000, 6000, 700), 80, ''),
 ('Dining – from pantry', (7950, 4300, 1600), (4500, 6200, 800), 80, ''),
] + VC.KITCHEN_OPEN_VIEWS + VC.tail(True)
LABELS = VC.COMMON_LABELS + [('Living', 2900, 2600), ('Study nook', 1200, 5350), ('Dining', 6150, 5600), ('Dry pantry', 8150, 5850), ('Bedroom 3', 7000, 1500)]
DIMS = [((296, 5350), (2060, 5350), 'Study nook 1760 deep'), ((5150, 5050), (7150, 5050), 'Table 2000 × 1000'), ((4600, 4700), (4600, 3900), 'Walkway to bedrooms ≈ 800')]
INFO = ("Plan F – open study nook. Instead of a closed study room, two standing desks sit against the west wall in an open nook beside the living room, "
        "with wall cabinets and a lit shelf above and a reading chair. Bedroom 3 stays a proper guest bedroom, the dining table for 8 sits outside an open kitchen "
        "(bi-fold glass to close it when cooking), and the living room keeps the marble TV wall with a tall storage cabinet. "
        "Nothing is fixed to the household shelter walls. Removing the kitchen front wall must be confirmed with HDB / your ID. Power points and trunking are indicative.")
