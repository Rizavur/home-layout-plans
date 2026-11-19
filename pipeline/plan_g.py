import math
import planlib as P, blocks as K, views_common as VC


def build(c):
    B, CYL, PRZ, RRECT, SLABH, RR = c.B, c.CYL, c.PRZ, c.RRECT, c.SLABH, c.RR
    K.fixtures(c)
    it = c.item('Living_West_Wall_Cladding', 'Furniture'); B(it, 250, 290, 1170, 6300, 0, 2650, 'wallp')

    # ---- New wall x 1980-2080 from the window to the shelter: maid room (north) + study (south) ----
    it = c.item('West_Rooms_East_Wall_Window_to_Shelter', 'Partitions')
    B(it, 1980, 2080, 1170, 3450, 0, 2650, 'wallp'); B(it, 1980, 2080, 3450, 4250, 2100, 2650, 'wallp')   # maid room door opening y 3450-4250
    B(it, 1980, 2080, 4250, 5300, 0, 2650, 'wallp'); B(it, 1980, 2080, 5300, 6200, 2100, 2650, 'wallp'); B(it, 1980, 2080, 6200, 6300, 0, 2650, 'wallp')
    it = c.item('Maid_Room_and_Study_Dividing_Wall', 'Partitions'); B(it, 290, 1980, 4300, 4400, 0, 2650, 'wallp')

    # ---- TV feature wall on the maid-room wall (faces the living room) ----
    it = c.item('TV_Feature_Wall_Marble_with_Fluted_Walnut_and_Hidden_Maid_Door', 'Furniture')
    B(it, 2080, 2120, 1500, 3360, 0, 2650, 'marble')
    for (y0, y1) in ((1380, 1497), (3363, 3450), (4250, 4300)):
        B(it, 2080, 2110, y0, y1, 0, 2650, 'walnut'); y = y0 + 12.0
        while y < y1 - 8: CYL(it, 2110, y, 10, 0, 2650, 'walnut2', 8); y += 22
    B(it, 2080, 2110, 3450, 4250, 2095, 2650, 'walnut'); y = 3462.0
    while y < 4242: CYL(it, 2110, y, 10, 2095, 2650, 'walnut2', 8); y += 22
    B(it, 2120, 2123, 1600, 3260, 830, 1820, 'cove')
    it = c.item('Maid_Room_Concealed_Door_Fluted_Walnut', 'Furniture')            # flush door that reads as part of the fluted wall
    B(it, 2082, 2108, 3456, 4244, 5, 2090, 'walnut'); y = 3470.0
    while y < 4236: CYL(it, 2108, y, 10, 5, 2090, 'walnut2', 8); y += 22
    B(it, 2112, 2122, 4150, 4165, 900, 1300, 'gold')
    it = c.item('TV_75_inch', 'Furniture'); B(it, 2123, 2153, 1600, 3260, 860, 1795, 'screen')
    it = c.item('TV_Console_Walnut_Fluted_Marble_Top', 'Furniture')
    PRZ(it, RR(2120, 2550, 1620, 3240, 110, (1, 0, 0, 0)), 240, 480, 'walnut'); y = 1730
    while y < 3230: CYL(it, 2550, y, 13, 262, 456, 'walnut2', 8); y += 30
    PRZ(it, RR(2120, 2565, 1612, 3260, 115, (1, 0, 0, 0)), 480, 500, 'marble'); B(it, 2120, 2565, 3240, 3260, 0, 480, 'marble'); B(it, 2470, 2500, 1680, 3220, 234, 240, 'led')
    CYL(it, 2350, 1800, 85, 500, 780, 'ceramic', 20); CYL(it, 2360, 3060, 55, 500, 640, 'sculpt', 16)

    # ---- Living: L-sofa on the bedroom-3 wall, chaise towards the dining side ----
    it = c.item('Living_L_Sofa_on_Bedroom_Wall_Chaise_to_Dining', 'Furniture')
    c.sofa2(it, '-x', 4500, 2650, 2400, 1000, 3, False, True, (-1200, -400, 800), 'sofa', 'sofa2', ('pil1', 'pil2'))
    it = c.item('Living_Coffee_Table_Travertine_Pebble', 'Furniture'); P.ppebble(c, it, 3450, 2430, 480, 360, 0.7, 400, 'traver', 'walnut', True); CYL(it, 3600, 2400, 100, 400, 450, 'ceramic', 20)
    it = c.item('Living_Wall_Art_Marble_Diptych_above_Sofa', 'Decor'); P.painting(c, it, 'x', 5550, -1, 1900, 2620, 1050, 1950, 'artm'); P.painting(c, it, 'x', 5550, -1, 2680, 3400, 1050, 1950, 'artm')
    it = c.item('Curtains_Living', 'Curtains'); c.curtain_full(it, 2080, 5550, 1375, 420, 420, 5, 2540)
    it = c.item('Living_Floor_Lamp', 'Lighting'); P.floor_lamp(c, it, 5300, 4050)
    WA = c.wave(3800, 2900, 1300, 950, 0.4, 0.14)
    it = c.item('False_Ceiling_Living_Organic_Wave_Cove', 'False_Ceiling')
    SLABH(it, [(2080, 1510), (5550, 1510), (5550, 3950), (5300, 3950), (5300, 4400), (2080, 4400)], WA, 2550, 2650, 'fceil', 'cove')
    c.downlights(it, [(2300, 1700), (3200, 1680), (4100, 1680), (5000, 1680), (5320, 3600), (2300, 4250), (3200, 4250), (4100, 4250), (2300, 3700)], 2550)

    # ---- Maid room (north half, has the window) ----
    it = c.item('Maid_Room_Single_Bed', 'Furniture'); P.bed2(c, it, 300, 1300, 2290, 4290, '+y', 1)
    it = c.item('Maid_Room_Wardrobe', 'Furniture'); c.cabinet(it, '-x', 1450, 2450, 1380, 600, 0, 2550, 2, 'white', 100, None, 'bar', hm='gold')
    it = c.item('Maid_Room_Wall_Shelf_and_Hooks', 'Furniture'); B(it, 290, 520, 1600, 2150, 1100, 1125, 'oak')
    for y in (3550, 3750, 3950): CYL(it, 1975, y, 12, 1600, 1610, 'gold', 8)
    it = c.item('Aircon_Maid_Room', 'Aircon'); P.aircon2(c, it, 'x', 1980, -1, 2550, 3350, 2230)
    it = c.item('Curtains_Maid_Room', 'Curtains'); c.curtain_full(it, 290, 1980, 1375, 300, 300, 4, 2540)
    it = c.item('False_Ceiling_Maid_Room', 'False_Ceiling'); SLABH(it, [(290, 1510), (1980, 1510), (1980, 4300), (290, 4300)], RRECT(700, 1580, 2000, 3800, 150, 6), 2550, 2650, 'fceil', 'cove')
    c.downlights(it, [(500, 1700), (1800, 1700), (1800, 4100)], 2550)

    # ---- Study (south half, by the shelter) – as Plan C ----
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

    it = c.item('False_Ceiling_Hall_Zone', 'False_Ceiling')
    SLABH(it, [(2080, 4400), (5300, 4400), (5300, 4950), (5550, 4950), (5550, 5000), (5100, 5000), (5100, 6700), (3740, 6700), (3740, 6300), (2080, 6300)],
          [(3000 + 600 * math.cos(2 * math.pi * k / 48), 5350 + 600 * math.sin(2 * math.pi * k / 48)) for k in range(48)], 2550, 2650, 'fceil', 'cove')
    c.downlights(it, [(2300, 4600), (2100, 6100), (3900, 4600), (4500, 5600), (3700, 6150), (4400, 6500)], 2550)
    K.dining9(c); K.foyer(c, 'niche'); K.curtains_bed(c); K.bedrooms(c, 'bed'); K.fans_ac(c, (3700, 2700))
    K.lights(c, ((5600, 8050), (7000, 8050), (8400, 8050), (2700, 7400), (9300, 4450), (10800, 4450), (9300, 5800), (12000, 5800), (925, 7600)))
    K.ceil_rooms(c); K.led(c, [(7945, 7965, 5560, 6670)])
    K.kitchen_closed(c, 'Kitchen_Closed'); K.kitchen_common(c); K.kitchen_open(c, 'Kitchen_Open'); K.kitchen_glass(c); K.yard_baths(c)
    K.power_common(c, [('x', 2153, 1, 2100, 300, True), ('x', 2153, 1, 2800, 300), ('x', 5520, -1, 1600, 300), ('x', 296, 1, 2000, 450, True),
                       ('x', 296, 1, 4600, 1050, True), ('x', 296, 1, 5500, 1050), ('x', 4940, 1, 7200, 1150)])
    K.trunking_common(c, [[(1870, 4850), (1870, 4400), (5340, 4400)], [(1870, 2950), (1870, 4400)]])


MODES = VC.KMODES
VIEWS = VC.HEAD + [
 ('Living – TV feature wall', (5000, 2500, 1350), (2100, 2450, 950), 75, ''),
 ('Living – L-sofa on the bedroom wall', (2600, 1700, 1600), (5300, 3500, 700), 85, ''),
 ('Living – from dining towards the TV', (5000, 4300, 1600), (2100, 2300, 900), 80, ''),
 ('Living – ceiling', (4900, 4200, 1250), (3600, 2700, 2650), 88, ''),
 ('Maid room – bed', (1750, 2650, 1650), (500, 3700, 500), 92, ''),
 ('Maid room – wardrobe and window', (1700, 4150, 1650), (1000, 1500, 1200), 92, ''),
 ('Maid room door – hidden in the fluted wall', (3500, 4100, 1550), (2080, 3850, 1100), 65, ''),
 ('Study – desks', (1600, 5350, 1650), (300, 5350, 1200), 85, ''),
 ('Study – sliding door from the hall', (3500, 5000, 1600), (2100, 6000, 1200), 75, ''),
 ('Hall – key niche', (3150, 5900, 1500), (2050, 6420, 1150), 60, ''),
 ('Dining – table for 8', (4300, 4100, 1600), (7000, 6000, 700), 80, ''),
 ('Dining – from pantry', (7950, 4300, 1600), (4500, 6200, 800), 80, ''),
] + VC.KITCHEN_OPEN_VIEWS + VC.tail(True)
LABELS = VC.COMMON_LABELS + [('Living', 3800, 2600), ('Maid room', 1130, 3000), ('Study', 1130, 5300), ('Dining', 6150, 5600), ('Dry pantry', 8150, 5850), ('Bedroom 3', 7000, 1500)]
DIMS = [((2153, 3700), (4500, 3700), 'TV → sofa front ≈ 2350'), ((290, 2000), (1980, 2000), 'Maid room 1690 × 2900'), ((290, 5300), (1980, 5300), 'Study 1690 × 1900'),
        ((5150, 5050), (7150, 5050), 'Table 2000 × 1000'), ((4600, 4700), (4600, 3900), 'Walkway to bedrooms ≈ 800')]
INFO = ("Plan G, based on Plan C. The study wall is carried all the way to the window, splitting the west side into a maid room (window end, about 1.7 × 2.9 m, single bed, "
        "wardrobe, aircon) and the study by the shelter (two standing desks, sliding door, as Plan C). The TV sits on the maid-room wall as a marble and fluted-walnut "
        "feature wall; the maid room door is hidden in the fluted panels next to the TV. The L-sofa sits against the bedroom 3 wall with its chaise towards the dining side. "
        "Kitchen: closed or open with bi-fold glass. A maid room without its own window opening onto the corridor must be checked with HDB / your ID. "
        "Power points and trunking are indicative.")
