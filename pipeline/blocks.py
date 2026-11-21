# Room blocks shared across plans (rebuild of the 11 Nov v2 blocks).
import math
import planlib as P
WM = 'greige'; WHM = 'gold'

def fixtures(c):
    c.build_fixtures()

def kitchen_front_wall(c, lay='Kitchen_Closed'):
    it = c.item('Kitchen_Front_Wall_x4940_7840_removable', lay); c.B(it, 4940, 7840, 6700, 6800, 0, 2250, 'wallk')

def foyer(c, corner='round'):
    B, PRZ, ARC, CYL, RRECT, cabinet = c.B, c.PRZ, c.ARC, c.CYL, c.RRECT, c.cabinet
    it = c.item('Foyer_Cabinet_Run_with_Display', 'Furniture')
    if corner == 'round':
        cen = (1850, 6530); r = 230
        poly = [cen] + ARC(cen[0], cen[1], r, -90, 0, 10)
        PRZ(it, poly, 0, 100, 'charcoal')
        for zz in (100, 700, 1250, 1800, 2250): PRZ(it, poly, zz, zz + 25, 'marble' if zz == 700 else 'white')
        PRZ(it, poly, 2625, 2650, 'white'); B(it, 1850, 1870, 6300, 6530, 100, 2625, 'greige')
        CYL(it, 1960, 6440, 50, 125, 330, 'ceramic', 16); CYL(it, 1950, 6430, 45, 1275, 1420, 'gold', 16)
        PRZ(it, ARC(cen[0], cen[1], r + 6, -90, 0, 16) + ARC(cen[0], cen[1], r + 1, 0, -90, 16), 100, 2625, 'glass')
    elif corner == 'niche':
        # straight end panel flush with the study wall, open niche for keys and daily items (Plan C)
        B(it, 1850, 2080, 6300, 6530, 0, 100, 'charcoal'); B(it, 1850, 2080, 6300, 6530, 2560, 2650, WM)
        cabinet(it, '+x', 6300, 6530, 2080, 230, 100, 950, 1, WM, 0, None, None)
        cabinet(it, '+x', 6300, 6530, 2080, 230, 1350, 2560, 1, WM, 0, None, None)
        B(it, 1850, 1880, 6300, 6530, 950, 1350, 'walnut')
        B(it, 1880, 2080, 6300, 6318, 950, 1350, WM); B(it, 1880, 2080, 6512, 6530, 950, 1350, WM)
        B(it, 1880, 2080, 6318, 6512, 950, 975, 'marble'); B(it, 1880, 2080, 6318, 6512, 1332, 1350, WM)
        B(it, 2040, 2062, 6322, 6508, 1326, 1332, 'led')
        c.PRZ(it, c.RRECT(1915, 2045, 6335, 6445, 12, 3), 975, 985, 'gold')
        CYL(it, 1965, 6480, 22, 975, 1060, 'ceramic', 14)
    else:
        # square end column, flush with the new entrance partition (Plan B / E)
        B(it, 1850, 2080, 6300, 6530, 0, 100, 'charcoal'); B(it, 1850, 2080, 6300, 6530, 2560, 2650, WM)
        B(it, 1860, 2080, 6300, 6320, 100, 2560, WM); B(it, 1860, 1880, 6320, 6530, 100, 2560, WM)
        for zz in (700, 1450):
            B(it, 1880, 2080, 6320, 6530, zz, zz + 25, 'marble'); B(it, 1885, 2075, 6325, 6345, zz + 25 + 330 - 6, zz + 25 + 330, 'led')
        B(it, 2075, 2080, 6320, 6530, 100, 2560, 'glass')
        CYL(it, 1980, 6430, 55, 725, 900, 'ceramic', 16); CYL(it, 1975, 6425, 45, 1475, 1560, 'sculpt', 14)
    B(it, 1850, 2080, 6530, 6647, 0, 2650, WM); B(it, 1850, 2080, 6647, 7453, 2100, 2650, WM)
    for (a0, a1) in ((7453, 7850), (7853, 8250)): cabinet(it, '+x', a0, a1, 2080, 230, 0, 2650, 1, WM, 100, [2100], 'bar', hm=WHM)
    it = c.item('Shelter_Door_Concealed_Jib_Panel_Push_to_Open', 'Furniture')
    B(it, 2058, 2080, 6652, 7448, 12, 2096, WM); B(it, 1850, 1870, 6647, 6660, 0, 2100, 'white'); B(it, 1850, 1870, 7440, 7453, 0, 2100, 'white')
    it = c.item('Shelter_Jib_Panel_Full_Length_Mirror', 'Furniture')
    B(it, 2080, 2085, 6745, 7355, 215, 1985, 'mirror'); B(it, 2080, 2088, 6730, 6745, 200, 2000, 'gold'); B(it, 2080, 2088, 7355, 7370, 200, 2000, 'gold')
    B(it, 2080, 2088, 6745, 7355, 200, 215, 'gold'); B(it, 2080, 2088, 6745, 7355, 1985, 2000, 'gold')
    it = c.item('Shelter_Door_Handles', 'Doors'); c.lever(it, 'x', 1745, 1, 6780, 1000, 1, 'steel')
    # Shoe bench (y 6700-7150) + shoe cabinet with grab-and-go niche (y 7150-7550), clear of the DB box (y 7550-8250).
    # Open, floating shoe bench with a curved end (no side boards), y 6718-7140, wall-hung from x 3740.
    it = c.item('Foyer_Shoe_Bench_Curved', 'Furniture')
    R = 360                                                                                                 # radius of the rounded open end
    seat = P._dedupe([(3740, 7140), (3330, 7140)] + c.ARC(3330 + R, 6718 + R, R, 180, 270, 18) + [(3740, 6718)])
    P.soft_slab(c, it, seat, 400, 440, 'walnut', 12, 2)                                                       # seat board
    P.soft_slab(c, it, P._offset(seat, -12), 440, 495, 'fabric', 22, 3)                                      # seat cushion
    B(it, 3345, 3360, 6718 + R, 7130, 394, 400, 'led')                                                       # glow under the floating seat
    shelf = P._offset(seat, -40)
    P.soft_slab(c, it, shelf, 120, 138, 'walnut', 6, 2)                                                       # floating shoe tray
    B(it, 3720, 3740, 6718, 7140, 500, 1950, 'walnut'); B(it, 3700, 3720, 6760, 7110, 650, 1050, 'fabric') # timber back + padded back rest
    # short upper cabinet (1950-2650) whose open end is curved like the seat – no flat side panel facing the hall
    top = P._dedupe([(3740, 7150), (3300, 7150)] + c.ARC(3300 + R, 6700 + R, R, 180, 270, 18) + [(3740, 6700)])
    c.PRZ(it, top, 1950, 2650, 'white')
    c.PRZ(it, P._offset(top, -25), 1944, 1950, 'led')                                                        # soft light onto the bench
    B(it, 3296, 3300, 6930, 6936, 1960, 2640, 'reveal'); B(it, 3296, 3300, 6700 + R, 7150, 2290, 2296, 'reveal')   # door lines
    for (cx, cy, z) in ((3560, 6900, 138), (3560, 7040, 138), (3480, 6800, 0)):
        c.PRZ(it, c.RRECT(cx - 140, cx + 140, cy - 45, cy + 45, 30, 3), z, z + 90, 'charcoal')               # a few pairs of shoes
    it = c.item('Foyer_Shoe_Cabinet_with_Grab_and_Go_Niche', 'Furniture')
    cabinet(it, '-x', 7150, 7550, 3290, 450, 150, 1000, 1, 'white', 0, None, None)          # floating shoe cabinet, slipper gap below
    B(it, 3320, 3350, 7160, 7540, 144, 150, 'led')
    B(it, 3290, 3740, 7150, 7168, 1000, 1350, 'white'); B(it, 3290, 3740, 7532, 7550, 1000, 1350, 'white')
    B(it, 3720, 3740, 7168, 7532, 1018, 1350, 'walnut'); B(it, 3285, 3720, 7168, 7532, 1000, 1018, 'marble'); B(it, 3320, 3350, 7180, 7520, 1344, 1350, 'led')
    cabinet(it, '-x', 7150, 7550, 3290, 450, 1350, 2650, 1, 'white', 0, [2100], None)
    PRZ(it, RRECT(3420, 3620, 7200, 7380, 20, 3), 1018, 1030, 'gold'); CYL(it, 3560, 7460, 36, 1018, 1180, 'sculpt', 12)
    it = c.item('Foyer_DB_Box_Access_Door', 'Furniture')
    B(it, 3310, 3490, 7550, 7568, 0, 2650, 'white'); B(it, 3310, 3490, 8232, 8250, 0, 2650, 'white')       # side panels clear of the DB box
    B(it, 3290, 3310, 7553, 8247, 6, 2644, 'white')                                                       # flush push-to-open door
    B(it, 3286, 3290, 7553, 7556, 6, 2644, 'reveal'); B(it, 3286, 3290, 8244, 8247, 6, 2644, 'reveal')
    it = c.item('Foyer_Entry_Runner_Rug', 'Decor'); PRZ(it, RRECT(2250, 3150, 6450, 8150, 40, 4), 0, 10, 'rug2')
    it = c.item('Shelter_Freestanding_Cabinets_not_fixed_to_walls', 'Furniture'); cabinet(it, '+x', 6570, 8630, 610, 350, 0, 2300, 4, 'white', 80, [1900], 'bar')
    # Helper's tri-fold mattress, 800 x 1850 x 100 mm (a little smaller than a standard single), laid out for the night.
    # Room left: ~110 mm to the (now 350 deep) cabinet fronts and ~80 mm to the east wall; it folds to 800 x 617 x 300 mm and stands by the cabinets by day.
    it = c.item('Shelter_Helper_Trifold_Mattress_800x1850_laid_out', 'Furniture')
    MX0, MX1, MY0, MY1 = 720, 1520, 6700, 8550
    seg = (MY1 - MY0) / 3.0
    for k in range(3):
        y0, y1 = MY0 + k * seg + (3 if k else 0), MY0 + (k + 1) * seg - (3 if k < 2 else 0)
        P.soft_slab(c, it, c.RRECT(MX0, MX1, y0, y1, 30, 4), 0, 100, 'matf', 30, 3)
    for k in (1, 2): B(it, MX0 + 20, MX1 - 20, MY0 + k * seg - 3, MY0 + k * seg + 3, 8, 92, 'charcoal')    # fold seams
    it = c.item('Shelter_Helper_Pillow_and_Folded_Blanket', 'Decor')
    P.soft_slab(c, it, c.RRECT(MX0 + 90, MX1 - 90, MY0 + 50, MY0 + 400, 70, 5), 100, 230, 'linen2', 55, 3)
    P.soft_slab(c, it, c.RRECT(MX0 + 30, MX1 - 30, MY1 - 560, MY1 - 60, 40, 4), 100, 160, 'duvet', 25, 2)

def dining9(c):
    B, PRZ, RRECT, CYL = c.B, c.PRZ, c.RRECT, c.CYL
    # 2000 x 1000 table for 8 (3 + 3 + ends); ~810 mm walkway kept on the north side to the bedrooms
    chairs = [(x, 4880, '-y') for x in (5500, 6150, 6800)] + [(x, 6320, '+y') for x in (5500, 6150, 6800)] + [(4940, 5600, '-x'), (7360, 5600, '+x')]
    P.dining_set(c, (5150, 7150, 5100, 6100), chairs)
    it = c.item('Dining_Centrepiece_Vase_and_Bowl', 'Decor')
    CYL(it, 6000, 5610, 110, 758, 800, 'ceramic', 24); CYL(it, 6320, 5610, 65, 758, 1050, 'ceramic', 20); CYL(it, 6320, 5610, 32, 1050, 1110, 'ceramic', 14)
    it = c.item('Dining_Linear_Pendant', 'Lighting')
    P.dining_pendant(c, it, 5505, 6805, 5600)
    # Cooling: an aircon on the walkway beam just north of the pantry mirror, blowing across the table,
    # and a bladeless tower fan in the corner by the kitchen (no ceiling fan: beam + pendant over the table).
    it = c.item('Dining_Aircon_on_Walkway_Beam', 'Aircon'); P.wall_aircon(c, it, '-x', 8400, 4000, 4900, 2250)
    it = c.item('Dining_Bladeless_Tower_Fan', 'Furniture'); P.bladeless_fan(c, it, 7720, 6480, 6150, 5600)
    it = c.item('Dry_Pantry_on_Toilet_Wall_Cabinet_Mirror_Robot_Bay', 'Furniture')
    c.cabinet(it, '-x', 5540, 6690, 7920, 480, 0, 850, 2, WM, 100, None, 'bar', hm=WHM)
    c.cabinet(it, '-x', 5010, 5537, 7920, 480, 480, 850, 1, WM, 0, None, 'bar', hm=WHM)
    B(it, 7920, 8400, 5010, 5030, 0, 480, WM); B(it, 7920, 8400, 5517, 5537, 0, 480, WM)
    B(it, 7930, 8390, 5030, 5517, 470, 480, 'charcoal'); B(it, 7970, 8370, 5040, 5507, 466, 470, 'led')
    B(it, 8250, 8390, 5140, 5400, 0, 420, 'metal'); CYL(it, 8115, 5270, 160, 0, 92, 'metal', 32); CYL(it, 8115, 5270, 153, 92, 95, 'charcoal2', 32)
    B(it, 7910, 8400, 5010, 6690, 850, 880, 'sintered'); B(it, 8378, 8400, 5040, 6660, 900, 2615, 'mirror')
    B(it, 8370, 8400, 5020, 5040, 880, 2635, 'gold'); B(it, 8370, 8400, 6660, 6680, 880, 2635, 'gold'); B(it, 8370, 8400, 5040, 6660, 2615, 2635, 'gold')
    it = c.item('False_Ceiling_Dining_Coffer', 'False_Ceiling')
    c.SLABH(it, [(5850, 3900), (7920, 3900), (7920, 6700), (5850, 6700)], RRECT(6000, 7750, 4400, 6500, 150, 6), 2550, 2650, 'fceil', 'cove')
    c.downlights(it, [(6950, 4080), (7850, 5300), (7850, 6000), (6000, 6600), (7000, 6600)], 2550)

def bedrooms(c, br3='bed'):
    # br3: 'bed' adds queen bed, painting and rug; anything else leaves bedroom 3 joinery only
    B, PRZ, RRECT, CYL, cabinet = c.B, c.PRZ, c.RRECT, c.CYL, c.cabinet
    # Bedroom 3 joinery
    it = c.item('Bedroom3_L_Wardrobe', 'Furniture')
    cabinet(it, '+x', 2300, 2747, 6240, 590, 0, 450, 1, WM, 100, None, 'bar', hm=WHM)
    cabinet(it, '+x', 2300, 2747, 6240, 590, 1100, 2650, 1, WM, 0, [2250], 'bar', hm=WHM)
    cabinet(it, '+x', 2750, 3197, 6240, 590, 0, 2650, 1, WM, 100, [2250], 'bar', hm=WHM)
    B(it, 5650, 6240, 3200, 3800, 0, 2650, WM); cabinet(it, '-y', 6243, 7440, 3200, 600, 0, 2650, 2, WM, 100, [2250], 'bar', hm=WHM)
    it = c.item('Bedroom3_Bedside_Nook_Open_to_Room', 'Furniture')
    B(it, 5650, 5670, 2300, 2727, 450, 1100, 'charcoal2'); B(it, 5650, 6240, 2727, 2747, 450, 1100, WM)
    B(it, 5670, 6240, 2300, 2727, 450, 475, 'marble'); B(it, 5670, 6240, 2300, 2727, 1080, 1100, WM); B(it, 5690, 6220, 2315, 2712, 1076, 1080, 'led')
    CYL(it, 5950, 2500, 70, 475, 520, 'gold', 16); CYL(it, 5950, 2500, 10, 520, 820, 'gold', 8); CYL(it, 5950, 2500, 110, 820, 980, 'artbg', 20)
    if br3 == 'bed':
        it = c.item('Bedroom3_Queen_Bed', 'Furniture'); P.bed2(c, it, 5850, 7850, 700, 2230, '-x', 2)
        it = c.item('Bedroom3_Painting_above_Bed', 'Decor'); P.painting(c, it, 'x', 5850, 1, 850, 2100, 1300, 2000, 'artw')
        it = c.item('Bedroom3_Rug', 'Decor'); PRZ(it, RRECT(6450, 8250, 500, 2500, 60, 4), 0, 10, 'rug2')
    # Bedroom 2 (kids floor bed)
    kids_floor_bed(c)
    it = c.item('Bedroom2_Painting_above_Bed', 'Decor'); P.painting(c, it, 'x', 11350, -1, 940, 1840, 950, 1550, 'artw')
    it = c.item('Bedroom2_Kids_Rug', 'Decor'); PRZ(it, RRECT(9200, 10200, 1100, 2600, 60, 4), 0, 10, 'rug2')
    it = c.item('Bedroom2_Wardrobe', 'Furniture'); cabinet(it, '-y', 9700, 11350, 3200, 600, 0, 2650, 3, WM, 100, [2250], 'bar', hm=WHM)
    # Master
    it = c.item('Master_King_Bed', 'Furniture'); P.bed2(c, it, 12300, 14350, 1640, 3490, '+x', 2)
    it = c.item('Master_Painting_above_Bed', 'Decor'); P.painting(c, it, 'x', 14350, -1, 1950, 3180, 1350, 2050, 'artm')
    it = c.item('Master_Rug', 'Decor'); PRZ(it, RRECT(11850, 13600, 1150, 3950, 60, 4), 0, 10, 'rug1'); PRZ(it, RRECT(11950, 13500, 1250, 3850, 50, 4), 10, 12, 'rug2')
    it = c.item('Master_Bedside_Tables', 'Furniture'); c.nightstand(it, 13950, 14350, 1250, 1620); c.nightstand(it, 13950, 14350, 3510, 3880)
    it = c.item('Master_Tall_Cabinet', 'Furniture'); cabinet(it, '-x', 350, 1247, 13750, 600, 0, 2650, 2, WM, 100, [2250], 'bar', hm=WHM)
    it = c.item('Master_Wardrobe', 'Furniture'); cabinet(it, '-y', 12400, 14350, 4400, 600, 0, 2650, 4, WM, 100, [2250], 'bar', hm=WHM)
    it = c.item('Master_Bedside_Wall_Sconces', 'Lighting')
    for cy in (1435, 3695): P.bedside_sconce(c, it, 14350, cy, -1)
    it = c.item('Master_Organic_Wave_Mirror_Backlit', 'Decor')
    mp = []
    N = 120
    for k in range(N):
        t = 2 * math.pi * k / N; co = math.cos(t); s = math.sin(t)
        ru = 470 * (1 + 0.07 * math.sin(3 * t + 0.6) + 0.045 * math.sin(5 * t + 1.3)); rv = 990 * (1 + 0.035 * math.sin(2 * t + 0.2) + 0.03 * math.sin(4 * t + 2.1))
        mp.append((840 + ru * (abs(co) ** 0.8) * (1 if co >= 0 else -1), 1070 + rv * (abs(s) ** 0.9) * (1 if s >= 0 else -1)))
    gl = [(840 + (u - 840) * 1.07, 1070 + (v - 1070) * 1.035) for (u, v) in mp]
    O2 = (11450, 0, 0)
    c.PR3(it, gl, O2, (0, 1, 0), (0, 0, 1), (1, 0, 0), 0, 2, 'cove'); c.PR3(it, mp, O2, (0, 1, 0), (0, 0, 1), (1, 0, 0), 22, 28, 'mirror')
    c.PR3(it, [(840 + (u - 840) * 0.55, 1070 + (v - 1070) * 0.6) for (u, v) in mp], O2, (0, 1, 0), (0, 0, 1), (1, 0, 0), 2, 22, 'charcoal')

def curtains_bed(c):
    # track fixed under the window beam (beam y 0-350, underside 2250) - curtains sit inside the recess
    for (nm, x0, x1) in (('Curtains_Bedroom3', 5850, 8150), ('Curtains_Bedroom2', 9150, 11350), ('Curtains_Master', 11450, 14350)):
        it = c.item(nm, 'Curtains'); c.curtain_full(it, x0, x1, 180, 300, 300, 5, 2245)

def fans_ac(c, living_fan):
    for (nm, cx, cy) in (('Living_near_Sofas',) + tuple(living_fan), ('Bedroom3', 6800, 1500), ('Bedroom2', 9900, 1800), ('Master', 13100, 2560)):
        it = c.item('Ceiling_Fan_with_Light_' + nm, 'Lighting'); c.fan(it, cx, cy, 2280, 2550)
    it = c.item('Aircon_Bedroom3', 'Aircon'); P.aircon2(c, it, 'y', 3800, -1, 7450, 8350, 2240)
    it = c.item('Aircon_Bedroom2', 'Aircon'); P.aircon2(c, it, 'y', 3800, -1, 8750, 9650, 2240)
    it = c.item('Aircon_Master', 'Aircon'); P.aircon2(c, it, 'x', 10250, 1, 4000, 4900, 2240)
    it = c.item('Aircon_Hall_on_Beam_serves_Living_and_Dining', 'Aircon'); P.aircon2(c, it, 'x', 5550, -1, 4000, 4900, 2240)

def lights(c, pts):
    it = c.item('Ceiling_Lights', 'Lighting')
    for (cx, cy) in pts: c.CYL(it, cx, cy, 200, 2615, 2650, 'lightw', 32)

def ceil_rooms(c):
    rooms = (
        ('False_Ceiling_Bedroom3', [(5850, 350), (8400, 350), (8400, 3530), (7440, 3530), (7440, 3200), (6240, 3200), (6240, 2300), (5850, 2300)], c.RRECT(6550, 7850, 900, 2750, 300, 8), [(6200, 650), (7100, 650), (8000, 650), (8100, 1700), (8100, 2700), (6050, 1300)]),
        ('False_Ceiling_Bedroom2', [(8700, 350), (11350, 350), (11350, 3200), (9700, 3200), (9700, 3530), (8700, 3530)], c.RRECT(9250, 10800, 850, 2700, 300, 8), [(9000, 650), (10000, 650), (11000, 650), (11050, 1800), (8980, 1800), (8980, 3100)]),
        ('False_Ceiling_Master', [(11450, 350), (13750, 350), (13750, 1247), (14350, 1247), (14350, 4400), (12400, 4400), (12400, 5000), (10550, 5000), (10550, 3900), (11450, 3900)], c.RRECT(12000, 13650, 1150, 3750, 350, 8), [(11750, 700), (12700, 700), (13400, 700), (14000, 1600), (14000, 2560), (14000, 3500), (11750, 2000), (11750, 3300), (11000, 4450)]),
    )
    for nm, outer, hole, dl in rooms:
        it = c.item(nm, 'False_Ceiling'); c.SLABH(it, outer, hole, 2560, 2650, 'fceil', 'cove'); c.downlights(it, dl, 2560)

def led(c, extra):
    it = c.item('LED_Strips_Under_Carpentry_Warm_3000K', 'LED_Strips')
    for b in [(6195, 6215, 2330, 2717), (6195, 6215, 2780, 3167), (6273, 7410, 3225, 3245), (9730, 11320, 3225, 3245), (13775, 13795, 380, 1217), (12430, 14320, 4425, 4445), (2035, 2055, 7483, 8220)] + list(extra):
        c.B(it, b[0], b[1], b[2], b[3], 94, 100, 'led')

# ---------------- Kitchen ----------------
def kitchen_closed(c, lay='Kitchen_Closed'):
    B, cabinet, krun, CYL, PRZ, RRECT = c.B, c.cabinet, c.krun, c.CYL, c.PRZ, c.RRECT
    kitchen_front_wall(c, lay)
    it = c.item('Kitchen_Tall_Larder_Dry_Goods_with_Microwave_and_Door_Pocket', lay)
    cabinet(it, '+y', 4940, 5413, 7500, 600, 0, 2650, 1, 'white', 100, [1350, 2250], 'bar', hm='gold')
    cabinet(it, '+y', 5417, 5890, 7500, 600, 0, 1350, 1, 'white', 100, None, 'bar', hm='gold')
    B(it, 5417, 5890, 6920, 7460, 1350, 1753, 'white'); B(it, 5440, 5867, 7460, 7498, 1368, 1735, 'appl'); B(it, 5462, 5770, 7497, 7500, 1400, 1700, 'glassblk')
    cabinet(it, '+y', 5417, 5890, 7500, 600, 1753, 2650, 1, 'white', 0, [2250], 'bar', hm='gold')
    it = c.item('Kitchen_Base_Drawers_Dining_Wall', lay)
    krun(it, '+y', 7400, 600, 0, 870, 150, [(5890, 6540, 'drawers4'), (6540, 7190, 'drawers'), (7190, 7840, 'drawers')], 'top')
    it = c.item('Kitchen_Wall_Cabinets_Dining_Wall', lay)
    krun(it, '+y', 7150, 350, 1500, 2650, 0, [(5890, 6540, 'door2'), (6540, 7190, 'door2'), (7190, 7840, 'door2')], 'bottom')
    it = c.item('Sintered_Stone_Top_and_Backsplash_Dining_Wall', lay)
    B(it, 5890, 7840, 6800, 7420, 870, 900, 'sintered'); B(it, 5890, 7840, 6800, 6815, 900, 1500, 'sintered')
    it = c.item('Kitchen_Appliance_Garage', lay)
    B(it, 7190, 7208, 6815, 7150, 900, 1494, 'white'); B(it, 7822, 7840, 6815, 7150, 900, 1494, 'white'); B(it, 7208, 7822, 6815, 6830, 900, 1494, 'walnut')
    B(it, 7208, 7822, 6830, 7150, 1474, 1494, 'white'); CYL(it, 7300, 6960, 82, 900, 1130, 'steel', 20); CYL(it, 7500, 6975, 135, 900, 1120, 'appl', 24)
    it = c.item('Kitchen_LED_Dining_Wall', 'LED_Strips' if lay == 'Kitchen' else lay); B(it, 5910, 7180, 7100, 7120, 1494, 1500, 'led')
    it = c.item('Kitchen_Door_Frame_and_Track', lay)
    B(it, 3990, 4010, 6700, 6850, 0, 2130, 'metal'); B(it, 3990, 4940, 6700, 6850, 2130, 2250, 'white'); B(it, 3990, 5890, 6852, 6898, 2105, 2130, 'metal')
    for (nm, dl, x0) in (('Kitchen_Sliding_Door_CLOSED', 'Kitchen_Door_Closed', 3995), ('Kitchen_Sliding_Door_OPEN_in_pocket', 'Kitchen_Door_Open', 4925)):
        it = c.item(nm, dl); x1 = x0 + 960
        B(it, x0, x0 + 45, 6860, 6890, 10, 2100, 'charcoal'); B(it, x1 - 45, x1, 6860, 6890, 10, 2100, 'charcoal')
        B(it, x0 + 45, x1 - 45, 6860, 6890, 10, 100, 'charcoal'); B(it, x0 + 45, x1 - 45, 6860, 6890, 2010, 2100, 'charcoal')
        B(it, x0 + 45, x1 - 45, 6869, 6881, 100, 2010, 'fglass'); B(it, x0 + 12, x0 + 30, 6855, 6860, 850, 1250, 'gold'); B(it, x0 + 12, x0 + 30, 6890, 6895, 850, 1250, 'gold')

def kitchen_common(c, stack=False):
    """stack=True: washer and dryer stacked in the south-east yard corner, freeing the space under the north yard counter."""
    B, V, cabinet, krun, CYL, CYLY, PRZ, RRECT = c.B, c.V, c.cabinet, c.krun, c.CYL, c.CYLY, c.PRZ, c.RRECT
    it = c.item('Kitchen_Base_Hob_Oven_Sink_Dishwasher', 'Kitchen')
    krun(it, '-y', 8700, 600, 0, 870, 150, [(4810, 5410, 'drawers4'), (5410, 6010, 'drawers'), (6010, 6610, 'skip'), (6610, 6790, 'door'), (6790, 7390, 'door2'), (7390, 7840, 'door')], 'top')
    V(it, 6820, 7360, 8760, 9220, 700, 870, 'white')
    B(it, 6013, 6607, 8700, 8720, 150, 230, 'white'); B(it, 6013, 6607, 8700, 8720, 233, 867, 'glassblk'); B(it, 6080, 6540, 8680, 8700, 800, 812, 'steel'); B(it, 6100, 6520, 8698, 8700, 300, 700, 'smoke')
    it = c.item('Sintered_Stone_Top_and_Backsplash_Hob_Wall', 'Kitchen')
    B(it, 4810, 7840, 8680, 9300, 870, 900, 'sintered'); V(it, 6840, 7340, 8780, 9200, 870, 900, 'sintered'); B(it, 4810, 7840, 9285, 9300, 900, 1500, 'sintered')
    it = c.item('Kitchen_Wall_Cabinets_Stove_Side_KEPT', 'Kitchen')
    # wall cabinets on the hob / oven wall: tall doors all the way to the ceiling
    krun(it, '-y', 8950, 350, 1500, 2650, 0, [(4810, 5410, 'door2'), (5410, 6010, 'door2')], 'bottom')
    krun(it, '-y', 8950, 350, 1500, 2650, 0, [(6610, 7225, 'door'), (7225, 7840, 'door')], 'bottom')
    krun(it, '-y', 8950, 350, 1563, 2650, 0, [(6010, 6610, 'door2')], 'bottom')                     # above the cooker hood
    krun(it, '-y', 8600, 700, 1900, 2650, 0, [(3990, 4400, 'door'), (4400, 4810, 'door')], 'bottom')
    it = c.item('Kitchen_Sink_and_Tap', 'Kitchen')
    B(it, 6820, 7360, 8760, 9220, 700, 870, 'steel'); V(it, 6840, 7340, 8780, 9200, 720, 870, 'steel')
    B(it, 7070, 7110, 9220, 9260, 900, 1250, 'chrome'); B(it, 7075, 7105, 9000, 9260, 1220, 1250, 'chrome')
    it = c.item('Kitchen_Induction_Hob', 'Kitchen'); B(it, 6020, 6600, 8780, 9230, 900, 906, 'glassblk')
    for (x, y) in ((6170, 8900), (6450, 8900), (6170, 9110), (6450, 9110)): CYL(it, x, y, 90, 906, 907, 'steel', 20)
    it = c.item('Kitchen_Ducted_Hood_in_Upper_Cabinets', 'Kitchen')
    B(it, 6010, 6610, 8900, 9300, 1500, 1560, 'steel'); B(it, 6060, 6560, 8895, 8900, 1515, 1545, 'metal')
    it = c.item('Kitchen_Hood_Duct_to_Yard_indicative', 'Aircon_Trunking'); B(it, 6250, 6370, 9150, 9270, 1560, 2640, 'trunk'); B(it, 6250, 8700, 9150, 9270, 2540, 2640, 'trunk')
    it = c.item('Kitchen_LED_Under_Wall_Cabinets', 'LED_Strips'); B(it, 4830, 6000, 8980, 9000, 1494, 1500, 'led'); B(it, 6620, 7820, 8980, 9000, 1494, 1500, 'led')
    it = c.item('Fridge', 'Kitchen')
    B(it, 4000, 4800, 8600, 9280, 0, 20, 'metal'); B(it, 4000, 4800, 8600, 9280, 20, 1800, 'silver'); B(it, 4000, 4398, 8580, 8600, 1000, 1800, 'silver'); B(it, 4402, 4800, 8580, 8600, 1000, 1800, 'silver'); B(it, 4000, 4800, 8580, 8600, 60, 996, 'silver')
    it = c.item('Gas_Water_Heater_Wall_Mounted', 'Kitchen'); B(it, 8035, 8535, 6950, 7370, 1550, 2300, 'appl')
    if stack:
        it = c.item('Washer_and_Dryer_Stacked', 'Kitchen')
        for (z0, z1) in ((0, 850), (880, 1730)):
            B(it, 8660, 9260, 8690, 9290, z0, z1, 'appl')
            CYLY(it, 8960, z0 + 430, 170, 8690, 8665, 'steel', 28); CYLY(it, 8960, z0 + 430, 130, 8665, 8660, 'screen', 28)
        B(it, 8650, 9270, 8680, 9290, 850, 880, 'steel')                                   # stacking kit with pull-out shelf
    else:
        for (nm, y0, y1, fy, s) in (('Dryer', 6960, 7560, 7560, 1), ('Washing_Machine', 8690, 9290, 8690, -1)):
            it = c.item(nm, 'Kitchen'); B(it, 8660, 9260, y0, y1, 0, 850, 'appl')
            CYLY(it, 8960, 430, 170, fy, fy + s * 25, 'steel', 28); CYLY(it, 8960, 430, 130, fy + s * 25, fy + s * 30, 'screen', 28)
    it = c.item('Yard_Pipe_Boxup', 'Kitchen'); B(it, 7940, 8630, 8650, 9300, 0, 2650, 'white')
    it = c.item('Yard_Cabinets_and_Tabletops', 'Kitchen')
    cabinet(it, '+y', 7940, 8640, 7560, 610, 0, 870, 1, 'white', 150, None, 'bar', base='mortar_y')
    B(it, 7940, 9290, 6950, 7580, 870, 900, 'quartz')
    if not stack: B(it, 8640, 9290, 8670, 9300, 870, 900, 'quartz')
    cabinet(it, '+y', 8640, 9290, 7300, 350, 1500, 2650, 1, 'white', 0, [2250], 'bar'); cabinet(it, '-y', 8640, 9290, 8950, 350, 1800 if stack else 1500, 2650, 1, 'white', 0, [2250], 'bar')
    it = c.item('Steigen_Ceiling_Drying_Rack', 'Kitchen')
    for yc in (7420, 8830):
        B(it, 8770, 9230, yc - 40, yc + 40, 2630, 2650, 'steel')
        for xc in (8800, 9200): B(it, xc - 15, xc + 15, yc - 10, yc + 10, 2320, 2630, 'steel')
    for xc in (8830, 8915, 9000, 9085, 9170): CYLY(it, xc, 2280, 15, 7380, 8870, 'steel', 12)

def kitchen_open(c, lay='Kitchen_Open'):
    B, cabinet, krun, CYL, PRZ, RRECT = c.B, c.cabinet, c.krun, c.CYL, c.PRZ, c.RRECT
    it = c.item('KitchenOpen_Counter_facing_Dining_Fluted_Walnut_Back', lay)
    krun(it, '+y', 7400, 600, 0, 870, 150, [(4940, 5540, 'drawers4'), (5540, 6140, 'drawers'), (6140, 6740, 'door2'), (6740, 7240, 'drawers')], 'top')
    B(it, 4940, 7240, 6705, 6800, 150, 870, 'white'); B(it, 4940, 7240, 6720, 6800, 0, 150, 'mortar_k')
    B(it, 4940, 7240, 6700, 6712, 100, 870, 'walnut')
    x = 4955.0
    while x < 7230:
        CYL(it, x, 6700, 9, 100, 870, 'walnut2', 6); x += 22
    B(it, 4930, 7250, 6690, 7420, 870, 900, 'sintered')
    PRZ(it, RRECT(5300, 5600, 6950, 7150, 30, 3), 900, 915, 'oak'); CYL(it, 6600, 7000, 140, 900, 980, 'ceramic', 24)
    it = c.item('KitchenOpen_Tall_Units_at_Yard_End_Larder_Microwave', lay)
    # full depth to the old wall line (flush with the counter's back) and full height to the ceiling
    cabinet(it, '+y', 7244, 7840, 7400, 700, 0, 1300, 1, 'white', 100, None, 'bar', hm='gold')
    B(it, 7244, 7840, 6700, 7380, 1300, 1720, 'white'); B(it, 7270, 7815, 7380, 7398, 1330, 1690, 'appl'); B(it, 7300, 7620, 7397, 7400, 1370, 1660, 'glassblk')
    cabinet(it, '+y', 7244, 7840, 7400, 700, 1720, 2250, 1, 'white', 0, None, 'bar', hm='gold')
    cabinet(it, '+y', 7244, 7840, 7400, 550, 2253, 2650, 1, 'white', 0, None, None)
    # finished back facing the dining / dry pantry side: fluted walnut like the counter
    B(it, 7244, 7840, 6700, 6712, 100, 2250, 'walnut')
    x = 7259.0
    while x < 7830: CYL(it, x, 6700, 9, 100, 2250, 'walnut2', 6); x += 22
    B(it, 7244, 7840, 6712, 6730, 0, 100, 'mortar_k')
    it = c.item('KitchenOpen_LED_Plinth', lay); B(it, 4960, 7220, 6712, 6730, 94, 100, 'led')

def kitchen_glass(c):
    it = c.item('Kitchen_Glass_Track_and_Head', 'Kitchen_Open'); c.B(it, 3990, 7240, 6735, 6765, 2215, 2250, 'metal')
    it = c.item('Kitchen_Bifold_Glass_CLOSED', 'Kitchen_Glass_Closed')
    P.bifold(c, it, 4950, 7230, 6750, 905, 2215, 4, 'closed'); P.bifold(c, it, 4000, 4930, 6750, 5, 2215, 2, 'closed', glass='fglass')
    it = c.item('Kitchen_Bifold_Glass_FOLDED_AWAY', 'Kitchen_Glass_Open')
    P.bifold(c, it, 4950, 7230, 6750, 905, 2215, 4, 'open', '+x'); P.bifold(c, it, 4000, 4930, 6750, 5, 2215, 2, 'open', '-x', glass='fglass')

def yard_baths(c):
    B, CYL = c.B, c.CYL
    it = c.item('Common_Bath_WC', 'Sanitary'); c.wc(it, '-x', 10820, 5480)
    it = c.item('Common_Bath_Vanity_3_Mirror_Cabinets_with_Display_Ledge', 'Sanitary')
    c.vanity_ledge(it, '-y', 8800, 9880, 6850, 460, 8800, 9880, 1150, 2230, [(9000, 'diffuser'), (9150, 'candle')], 3)
    it = c.item('Common_Bath_Shower_Set', 'Sanitary'); c.shower_set(it, 'x', 10820, -1, 6520)
    it = c.item('Ensuite_WC', 'Sanitary'); c.wc(it, '+x', 10920, 6380)
    it = c.item('Ensuite_Vanity_5_Mirror_Cabinets_with_Display_Ledge', 'Sanitary')
    c.vanity_ledge(it, '+x', 5110, 6080, 10920, 440, 5100, 6850, 1150, 2230, [(5280, 'diffuser'), (5430, 'candle')], 5)
    it = c.item('Ensuite_Shower_Set', 'Sanitary'); c.shower_set(it, 'y', 6850, -1, 12720)
    it = c.item('Bath_Towels_and_Mats', 'Decor')
    B(it, 9950, 10450, 5250, 5800, 0, 12, 'towel'); B(it, 11050, 11550, 5250, 5800, 0, 12, 'towel')
    B(it, 10790, 10820, 5650, 6100, 1100, 1700, 'towel'); B(it, 10920, 10950, 5300, 5800, 1100, 1700, 'towel')

def power_common(c, extra=()):
    it = c.item('Power_Points_Indicative', 'Power_Points')
    pts = [('x', 5850, 1, 560, 600), ('x', 5850, 1, 2380, 600),            # bedroom 3 bedsides
           ('x', 14350, -1, 1300, 650), ('x', 14350, -1, 3820, 650),       # master bedsides
           ('y', 350, 1, 10900, 350), ('x', 11350, -1, 700, 350),          # bedroom 2
           ('y', 9285, -1, 5100, 1150), ('y', 9285, -1, 5700, 1150), ('y', 9285, -1, 7600, 1150),  # kitchen backsplash
           ('x', 8378, -1, 5300, 1100)]                                    # pantry
    for p in list(pts) + list(extra): P.power_point(c, it, p[0], p[1], p[2], p[3], p[4], *(p[5:] if len(p) > 5 else ()))

def trunking_common(c, extra=()):
    it = c.item('Aircon_Trunking_Indicative_to_Yard', 'Aircon_Trunking')
    P.trunking(c, it, [(5340, 4450), (5340, 6600), (7890, 6600), (7890, 7000)])
    P.trunking(c, it, [(7900, 3700), (7900, 3950), (10360, 3950), (10360, 4450)])
    P.trunking(c, it, [(9200, 3700), (9200, 3950)])
    P.trunking(c, it, [(7900, 3950), (7900, 4400), (5340, 4400)])
    for pts in extra: P.trunking(c, it, pts)


def kids_floor_bed(c):
    """Kids' floor bed after the reference photo: one-piece upholstered boucle shell (sage green) with a tall rounded
    headboard, arms that step down along the sides, a soft low rim, an inset mattress, mustard-stripe bedding."""
    B, PRZ, RRECT, CYL = c.B, c.PRZ, c.RRECT, c.CYL
    x0, x1, y0, y1 = 10290, 11310, 380, 2400          # head at y0 – headboard ~75 mm clear of the curtains
    T = 150                                            # wall thickness
    it = c.item('Bedroom2_Kids_Upholstered_Floor_Bed', 'Furniture')
    # base tray
    P.soft_slab(c, it, RRECT(x0 + 20, x1 - 20, y0 + 20, y1 - 20, 120, 6), 0, 140, 'boucle_g', 40, 3)
    # headboard: rounded-top panel in the x-z plane, extruded along y
    hb = []
    H = 760; rr = 230
    hb += [(x0, 0), (x1, 0)]
    for k in range(0, 9): a_ = math.radians(90 * k / 8.0); hb.append((x1 - rr + rr * math.cos(a_), H - rr + rr * math.sin(a_)))
    for k in range(0, 9): a_ = math.radians(90 + 90 * k / 8.0); hb.append((x0 + rr + rr * math.cos(a_), H - rr + rr * math.sin(a_)))
    c.PR3(it, hb, (0, y0, 0), (1, 0, 0), (0, 0, 1), (0, 1, 0), 0, T, 'boucle_g')
    c.PR3(it, [(x + (0 if x in (x0, x1) else 0), max(0, z - 12)) for (x, z) in hb], (0, y0 + T, 0), (1, 0, 0), (0, 0, 1), (0, 1, 0), 0, 18, 'boucle_g')
    # side walls with a stepped 'arm' near the head: profile in the y-z plane, extruded along x
    def h(y):
        d = y - y0
        if d < 620: return 470
        if d > 980: return 300
        t = (d - 620) / 360.0
        return 300 + 170 * (0.5 + 0.5 * math.cos(math.pi * t))
    for (xs, ) in ((x0,), (x1 - T,)):
        prof = [(y0 + T, 0), (y1, 0), (y1, 230)]
        for k in range(6): a_ = math.radians(90 * k / 5.0); prof.append((y1 - 70 + 70 * math.sin(a_), 230 + 70 * math.sin(a_) * 0 + 70 * (1 - math.cos(a_)) * 0 + (70 * math.sin(a_))))
        prof = [(y0 + T, 0), (y1, 0)]
        ys = [y1 - 2 + 0] + [y1 - 70 + 70 * math.cos(math.radians(90 * k / 5.0)) for k in range(6)]
        prof.append((y1, 230))
        for k in range(6):
            a_ = math.radians(90 * k / 5.0); prof.append((y1 - 70 + 70 * math.cos(a_), 230 + 70 * math.sin(a_)))
        yy = y1 - 80
        while yy > y0 + T:
            prof.append((yy, h(yy))); yy -= 40
        prof.append((y0 + T, h(y0 + T)))
        c.PR3(it, prof, (xs, 0, 0), (0, 1, 0), (0, 0, 1), (1, 0, 0), 0, T, 'boucle_g')
        # rounded top edge (soft roll) along the arm and rim
        # continuous soft roll along the top edge, following the stepped profile (lofted rings)
        def ring(yv):
            zc = h(yv) - 2; return [(xs + T / 2.0 + (T / 2.0) * math.cos(2 * math.pi * k / 16), yv, zc + (T / 2.0) * math.sin(2 * math.pi * k / 16)) for k in range(16)]
        yy = y0 + T
        while yy < y1 - 70:
            yn = min(y1 - 70, yy + 30); P._loft(it, ring(yy), ring(yn), 'boucle_g'); yy = yn
    # foot rim
    prof = [(x0 + T, 0), (x1 - T, 0), (x1 - T, 230), (x0 + T, 230)]
    c.PR3(it, prof, (0, y1 - T, 0), (1, 0, 0), (0, 0, 1), (0, 1, 0), 0, T, 'boucle_g')
    c.CYL  # noqa
    rim = [(x0 + T + 0.0, y1 - T / 2.0)]
    c.PR3(it, [(y1 - T / 2.0 + (T / 2.0) * math.cos(2 * math.pi * k / 14), 230 + (T / 2.0) * math.sin(2 * math.pi * k / 14)) for k in range(14)], (x0 + T, 0, 0), (0, 1, 0), (0, 0, 1), (1, 0, 0), 0, x1 - x0 - 2 * T, 'boucle_g')
    # mattress + bedding
    P.soft_slab(c, it, RRECT(x0 + T + 5, x1 - T - 5, y0 + T + 5, y1 - T - 5, 50, 5), 140, 320, 'linen', 35, 3)
    yd0 = y0 + T + (y1 - y0 - 2 * T) * 0.42
    P.soft_slab(c, it, RRECT(x0 + T, x1 - T, yd0, y1 - T, 30, 4), 300, 360, 'mustard', 22, 2)
    P.soft_slab(c, it, RRECT(x0 + T + 2, x1 - T - 2, yd0, yd0 + 130, 25, 4), 350, 385, 'linen2', 14, 2)
    for k in range(6):
        yy = yd0 + 180 + k * 150
        if yy < y1 - T - 40: B(it, x0 + T + 10, x1 - T - 10, yy, yy + 22, 359, 361, 'linen2')
    P.cushion3d(c, it, ((x0 + x1) / 2.0, y0 + T + 120, 470), (1.0, 0.0, 0.0), P._vec_tilt((0.0, 1.0, 0.0), 26), 640, 430, 150, 'mustard', 0.5)
    P.cushion3d(c, it, ((x0 + x1) / 2.0, y0 + T + 230, 430), (1.0, 0.0, 0.0), P._vec_tilt((0.0, 1.0, 0.0), 18), 600, 380, 140, 'linen2', 0.5)
