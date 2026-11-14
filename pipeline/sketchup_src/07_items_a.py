# build_model call 7 of 10
LB = session_state['L']; LQ = session_state['LQ']
ARC = LB['ARC']; B = LB['B']; CYL = LB['CYL']; CYLY = LB['CYLY']; PR3 = LB['PR3']; PRZ = LB['PRZ']; RRECT = LB['RRECT']; SLABH = LB['SLABH']; V = LB['V']
aircon = LB['aircon']; bed = LB['bed']; build_fixtures = LB['build_fixtures']; cabinet = LB['cabinet']; curtain = LB['curtain']
downlights = LB['downlights']; fan = LB['fan']; item = LB['item']; lever = LB['lever']; nightstand = LB['nightstand']; run_box = LB['run_box']; ITEMS = LB['ITEMS']
RR = LQ['RR']; puff = LQ['puff']; sofa2 = LQ['sofa2']; chair2 = LQ['chair2']; station = LQ['station']; desk_long = LQ['desk_long']
dchair_lux = LQ['dchair_lux']; curtain_full = LQ['curtain_full']; wave = LQ['wave']
ITEMS[:] = []
build_fixtures()
wm = 'greige'; whm = 'gold'
it = item('Study_Partitions_TV_Wall_and_Half_Glass', 'Partitions')
B(it, 2250, 2400, 1170, 3870, 0, 2650, 'wallp')
B(it, 1250, 2250, 3720, 3870, 0, 1000, 'wallp')
B(it, 250, 1250, 3720, 3870, 2100, 2650, 'wallp')
B(it, 1250, 2250, 3785, 3805, 1000, 2650, 'glass')
B(it, 1250, 2250, 3775, 3815, 1000, 1030, 'metal'); B(it, 1250, 2250, 3775, 3815, 2620, 2650, 'metal')
for xm in (1250, 1745, 2225):
    B(it, xm, xm + 25, 3775, 3815, 1030, 2620, 'metal')
it = item('Study_Sliding_Door_Fluted_Glass', 'Partitions')
B(it, 250, 2250, 3875, 3905, 2100, 2120, 'metal')
B(it, 270, 1275, 3880, 3898, 10, 2095, 'fglass')
B(it, 270, 300, 3879, 3899, 10, 2095, 'charcoal'); B(it, 1245, 1275, 3879, 3899, 10, 2095, 'charcoal')
B(it, 300, 1245, 3879, 3899, 10, 40, 'charcoal'); B(it, 300, 1245, 3879, 3899, 2065, 2095, 'charcoal')
B(it, 1220, 1235, 3899, 3919, 900, 1250, 'gold'); B(it, 1220, 1235, 3860, 3879, 900, 1250, 'gold')
it = item('Study_Desk_Two_Workstations_Facing_TV_Wall', 'Furniture')
desk_long(it, '+x', 1657, 2600, 2160, 585, [-1000, 1000])
station(it, '+x', 1657, 2100, 585); station(it, '+x', 1657, 3150, 585)
cabinet(it, '-x', 1520, 3680, 1900, 350, 1500, 2150, 4, 'white', 0, None, 'bar', hm='gold')
B(it, 1925, 1945, 1540, 3660, 1494, 1500, 'led')
it = item('Study_Chairs_x2', 'Furniture'); chair2(it, '+x', 1250, 2100); chair2(it, '+x', 1250, 3150)
it = item('Aircon_Study', 'Aircon'); aircon(it, 'x', 250, 1, 2300, 3200)
it = item('Curtains_Study', 'Curtains'); curtain_full(it, 250, 2250, 1375, 300, 300, 5, 2640)
it = item('False_Ceiling_Study', 'False_Ceiling')
SLABH(it, [(250, 1510), (2250, 1510), (2250, 3720), (250, 3720), (250, 3250), (480, 3250), (480, 2250), (250, 2250)], RRECT(650, 1950, 1800, 3450, 200, 6), 2550, 2650, 'fceil', 'cove')
downlights(it, [(2080, 2100), (2080, 3150), (400, 1700), (400, 3500), (1300, 1660), (1300, 3600)], 2550)
it = item('Entry_Wall_Flush_Cladding', 'Furniture')
B(it, 250, 290, 3870, 6300, 0, 2650, 'wallp')
it = item('TV_Feature_Wall_Marble_with_Fluted_Walnut_Flanks', 'Furniture')
B(it, 2400, 2440, 1700, 3640, 0, 2650, 'marble')
for (y0, y1) in ((1380, 1697), (3643, 3870)):
    B(it, 2400, 2430, y0, y1, 0, 2650, 'walnut')
    y = y0 + 12.0
    while y < y1 - 8:
        CYL(it, 2430, y, 10, 0, 2650, 'walnut2', 8); y += 22
B(it, 2400, 2436, 1697, 1700, 0, 2650, 'led'); B(it, 2400, 2436, 3640, 3643, 0, 2650, 'led')
B(it, 2440, 2443, 1800, 3540, 830, 1820, 'cove')
it = item('TV_75_inch', 'Furniture'); B(it, 2443, 2473, 1840, 3500, 860, 1795, 'screen')
dx = 2150
it = item('TV_Console_Walnut_Fluted_Travertine_Niche_Marble_Waterfall', 'Furniture')
PRZ(it, RR(290 + dx, 720 + dx, 1720, 2420, 110, (1, 0, 0, 0)), 240, 480, 'walnut')
PRZ(it, RR(290 + dx, 720 + dx, 2920, 3600, 110, (0, 0, 0, 0)), 240, 480, 'walnut')
B(it, 290 + dx, 720 + dx, 2420, 2920, 240, 262, 'walnut'); B(it, 290 + dx, 720 + dx, 2420, 2920, 458, 480, 'walnut')
B(it, 290 + dx, 302 + dx, 2420, 2920, 262, 458, 'traver'); B(it, 600 + dx, 640 + dx, 2440, 2900, 452, 458, 'led')
for (a0, a1) in ((1830, 2405), (2935, 3590)):
    y = a0
    while y < a1:
        CYL(it, 720 + dx, y, 13, 262, 456, 'walnut2', 8); y += 30
B(it, 718 + dx, 726 + dx, 1830, 2410, 456, 460, 'gold'); B(it, 718 + dx, 726 + dx, 2930, 3600, 456, 460, 'gold')
PRZ(it, RR(290 + dx, 735 + dx, 1712, 3620, 115, (1, 0, 0, 0)), 480, 500, 'marble')
B(it, 290 + dx, 735 + dx, 3600, 3620, 0, 480, 'marble')
B(it, 640 + dx, 670 + dx, 1780, 2400, 234, 240, 'led'); B(it, 640 + dx, 670 + dx, 2940, 3580, 234, 240, 'led')
PRZ(it, RRECT(420 + dx, 520 + dx, 2250, 3090, 40, 4), 500, 572, 'screen')
CYL(it, 470 + dx, 2670, 70, 270, 400, 'ceramic', 18); CYL(it, 470 + dx, 2670, 40, 400, 450, 'ceramic', 14)
CYL(it, 520 + dx, 1950, 85, 500, 780, 'ceramic', 20); CYL(it, 520 + dx, 1950, 40, 780, 840, 'ceramic', 14)
B(it, 420 + dx, 640 + dx, 3250, 3480, 500, 540, 'artbg'); B(it, 440 + dx, 620 + dx, 3270, 3460, 540, 570, 'art2'); CYL(it, 530 + dx, 3365, 55, 570, 660, 'gold', 16)
it = item('Living_3_Seater_Sofa_along_Wall', 'Furniture')
sofa2(it, '-x', 4461, 2700, 2400, 1000, 3, True, True, None)
it = item('Living_2_Seater_Sofa_by_Window', 'Furniture')
sofa2(it, '+y', 3780, 2220, 1300, 780, 2, True, True, None, 'sofa', 'sofa2', ('rug1', 'art2'))
it = item('Living_Round_Coffee_Table_Travertine_Fluted', 'Furniture')
cx, cy = 3724, 3000
CYL(it, cx, cy, 420, 362, 400, 'traver', 48); CYL(it, cx, cy, 410, 358, 362, 'gold', 48)
CYL(it, cx, cy, 255, 0, 358, 'walnut', 36)
for k in range(36):
    a = 2 * math.pi * k / 36
    CYL(it, cx + 262 * math.cos(a), cy + 262 * math.sin(a), 16, 0, 358, 'walnut2', 8)
B(it, cx - 150, cx + 90, cy - 120, cy + 40, 400, 440, 'artbg'); B(it, cx - 130, cx + 70, cy - 100, cy + 20, 440, 465, 'art1')
CYL(it, cx + 170, cy + 120, 100, 400, 450, 'ceramic', 20)
it = item('Living_Rug', 'Decor')
PRZ(it, RRECT(2950, 4500, 1950, 3950, 150, 6), 0, 8, 'rug1'); PRZ(it, RRECT(3070, 4380, 2070, 3830, 100, 6), 8, 10, 'rug2')
it = item('Wall_Art_Above_Sofa_Framed_Abstract', 'Decor')
B(it, 5510, 5550, 1960, 3560, 1100, 1125, 'gold'); B(it, 5510, 5550, 1960, 3560, 1875, 1900, 'gold')
B(it, 5510, 5550, 1960, 1985, 1125, 1875, 'gold'); B(it, 5510, 5550, 3535, 3560, 1125, 1875, 'gold')
B(it, 5520, 5550, 1985, 3535, 1125, 1875, 'artbg')
Xo = (5520, 200, 0); Uy = (0, 1, 0); Vz = (0, 0, 1); Wx = (-1, 0, 0)
PR3(it, [(1950, 1180), (2450, 1180)] + [(2200 + 250 * math.cos(math.pi * k / 12.0), 1560 + 250 * math.sin(math.pi * k / 12.0)) for k in range(13)], Xo, Uy, Vz, Wx, 0, 5, 'art1')
PR3(it, [(2690 + 210 * math.cos(2 * math.pi * k / 32), 1520 + 210 * math.sin(2 * math.pi * k / 32)) for k in range(32)], Xo, Uy, Vz, Wx, 3, 9, 'art3')
PR3(it, [(2880, 1160), (3230, 1160), (3230, 1640), (2880, 1640)], Xo, Uy, Vz, Wx, 0, 4, 'art2')
it = item('Curtains_Living_Ends_Only', 'Curtains'); curtain_full(it, 2400, 5550, 1375, 360, 360, 5, 2640)
it = item('Entry_Tall_Storage_Wall_with_Display_Niche', 'Furniture')
cabinet(it, '-y', 290, 2356, 5715, 585, 0, 900, 4, wm, 100, None, 'bar', hm=whm)
B(it, 290, 2356, 6280, 6300, 920, 1300, 'walnut'); B(it, 290, 310, 5715, 6300, 900, 1300, wm); B(it, 2336, 2356, 5715, 6300, 900, 1300, wm)
B(it, 310, 2336, 5710, 6280, 900, 920, 'marble'); B(it, 340, 2306, 5730, 5750, 1294, 1300, 'led')
cabinet(it, '-y', 290, 2356, 5715, 585, 1300, 2650, 4, wm, 0, [2250], 'bar', hm=whm)
CYL(it, 700, 6000, 90, 920, 1180, 'ceramic', 18); CYL(it, 1300, 6050, 120, 920, 960, 'gold', 20); B(it, 1800, 2100, 5900, 6150, 920, 990, 'artbg')
it = item('Entry_Low_Console_with_Marble_Top', 'Furniture')
cabinet(it, '+x', 4760, 5700, 875, 585, 150, 820, 2, wm, 0, None, 'bar', hm=whm)
B(it, 290, 890, 4750, 5710, 820, 845, 'marble'); B(it, 340, 820, 4800, 5660, 144, 150, 'led')
CYL(it, 580, 4980, 70, 845, 1150, 'ceramic', 18); B(it, 450, 700, 5300, 5550, 845, 880, 'artbg')
it = item('Entry_Half_Glass_Screen', 'Partitions')
B(it, 2356, 2520, 6230, 6300, 0, 1000, 'wallp'); B(it, 2356, 2520, 6255, 6275, 1000, 2100, 'glass')
B(it, 2356, 2520, 6250, 6280, 2100, 2120, 'metal'); B(it, 2500, 2520, 6250, 6280, 1000, 2100, 'metal')
it = item('Dining_Table_Rectangular_Marble_Walnut', 'Furniture')
PRZ(it, RRECT(5305, 7005, 5215, 6005, 25, 3), 715, 755, 'marble')
PRZ(it, RRECT(5375, 6935, 5285, 5935, 20, 3), 690, 715, 'walnut')
for x0 in (5495, 6735):
    PRZ(it, RRECT(x0, x0 + 80, 5345, 5875, 30, 3), 15, 690, 'walnut')
    PRZ(it, RRECT(x0 - 10, x0 + 90, 5335, 5885, 30, 3), 0, 15, 'gold')
it = item('Dining_Chairs_Curved_Back_x8', 'Furniture')
for cx in (5632, 6156, 6680):
    dchair_lux(it, cx, 5050, '-y'); dchair_lux(it, cx, 6170, '+y')
dchair_lux(it, 5140, 5610, '-x'); dchair_lux(it, 7170, 5610, '+x')
it = item('Dining_Linear_Pendant', 'Lighting')
PRZ(it, RRECT(5505, 6805, 5585, 5635, 25, 4), 1650, 1690, 'brass'); B(it, 5525, 6785, 5593, 5627, 1645, 1650, 'lightw')
CYL(it, 5950, 5610, 3, 1690, 2550, 'metal', 6); CYL(it, 6650, 5610, 3, 1690, 2650, 'metal', 6)
CYL(it, 5950, 5610, 40, 2540, 2550, 'brass', 12); CYL(it, 6650, 5610, 40, 2640, 2650, 'brass', 12)
it = item('Ceiling_Fan_Dining_42in', 'Lighting'); fan(it, 7200, 4800, 2300, 2650, 530)
it = item('Dry_Pantry_Full_Width_Cabinet_and_Full_Height_Mirror', 'Furniture')
cabinet(it, '-x', 5540, 6690, 7920, 480, 0, 850, 2, wm, 100, None, 'bar', hm=whm)
cabinet(it, '-x', 5010, 5537, 7920, 480, 480, 850, 1, wm, 0, None, 'bar', hm=whm)
B(it, 7920, 8400, 5010, 5030, 0, 480, wm); B(it, 7920, 8400, 5517, 5537, 0, 480, wm)
B(it, 7930, 8390, 5030, 5517, 470, 480, 'charcoal'); B(it, 7970, 8370, 5040, 5507, 466, 470, 'led')
B(it, 8250, 8390, 5140, 5400, 0, 420, 'metal'); B(it, 8246, 8250, 5190, 5350, 300, 380, 'smoke'); B(it, 8160, 8250, 5170, 5370, 0, 12, 'metal')
CYL(it, 8115, 5270, 160, 0, 92, 'metal', 32); CYL(it, 8115, 5270, 153, 92, 95, 'charcoal2', 32)
B(it, 7910, 8400, 5010, 6690, 850, 880, 'sintered')
B(it, 8378, 8400, 5040, 6660, 900, 2615, 'mirror')
B(it, 8370, 8400, 5020, 5040, 880, 2635, 'gold'); B(it, 8370, 8400, 6660, 6680, 880, 2635, 'gold'); B(it, 8370, 8400, 5040, 6660, 2615, 2635, 'gold')
for (nm, cx, cy) in (('Living_near_Sofas', 3800, 2850), ('Bedroom3', 6800, 1500), ('Bedroom2', 9900, 1800), ('Master', 13100, 2560)):
    it = item('Ceiling_Fan_with_Light_' + nm, 'Lighting'); fan(it, cx, cy, 2280)
it = item('Ceiling_Lights', 'Lighting')
for (cx, cy) in ((5600, 8050), (7000, 8050), (8400, 8050), (2700, 7400), (9300, 4450), (10800, 4450), (9300, 5800), (12000, 5800), (925, 7600)):
    CYL(it, cx, cy, 200, 2615, 2650, 'lightw', 32)
it = item('Aircon_Bedroom3', 'Aircon'); aircon(it, 'y', 3800, -1, 7450, 8350)
it = item('Aircon_Bedroom2', 'Aircon'); aircon(it, 'y', 3800, -1, 8750, 9650)
it = item('Aircon_Master', 'Aircon'); aircon(it, 'x', 10250, 1, 4000, 4900)
it = item('Aircon_Hall_on_Beam_serves_Living_and_Dining', 'Aircon'); aircon(it, 'x', 5550, -1, 4000, 4900)
WA = wave(3950, 2950, 1150, 950, 0.4, 0.14)
WB = wave(3950, 2950, 880, 680, 2.3, 0.16)
it = item('False_Ceiling_Living_Organic_Wave_Cove', 'False_Ceiling')
SLABH(it, [(2400, 1510), (5550, 1510), (5550, 3950), (5300, 3950), (5300, 4400), (2400, 4400)], WA, 2550, 2650, 'fceil', 'cove')
SLABH(it, WA, WB, 2600, 2650, 'fceil', 'cove')
downlights(it, [(2560, 1700), (3500, 1680), (4400, 1680), (5330, 1750), (5380, 3200), (2520, 3000), (2600, 4220), (3500, 4250), (4400, 4250)], 2550)
it = item('False_Ceiling_Entry_Zone', 'False_Ceiling')
SLABH(it, [(250, 3870), (2400, 3870), (2400, 4400), (5300, 4400), (5300, 4950), (5550, 4950), (5550, 6700), (3740, 6700), (3740, 6300), (250, 6300)],
      RRECT(800, 3300, 4300, 5500, 250, 6), 2550, 2650, 'fceil', 'cove')
downlights(it, [(500, 4100), (2050, 4100), (3500, 4100), (4500, 4600), (4500, 5600), (3700, 6100), (4400, 6500), (5100, 6400), (1300, 5900)], 2550)
it = item('False_Ceiling_Dining_Coffer', 'False_Ceiling')
SLABH(it, [(5850, 3900), (7920, 3900), (7920, 6700), (5850, 6700)], RRECT(6000, 7750, 4400, 6500, 150, 6), 2550, 2650, 'fceil', 'cove')
downlights(it, [(6950, 4080), (7850, 5300), (7850, 6000), (6000, 6600), (7000, 6600)], 2550)
rooms = (
    ('False_Ceiling_Bedroom3', [(5850, 350), (8400, 350), (8400, 3530), (7440, 3530), (7440, 3200), (6240, 3200), (6240, 2300), (5850, 2300)], RRECT(6550, 7850, 900, 2750, 300, 8),
     [(6200, 650), (7100, 650), (8000, 650), (8100, 1700), (8100, 2700), (6050, 1300)]),
    ('False_Ceiling_Bedroom2', [(8700, 350), (11350, 350), (11350, 3200), (9700, 3200), (9700, 3530), (8700, 3530)], RRECT(9250, 10800, 850, 2700, 300, 8),
     [(9000, 650), (10000, 650), (11000, 650), (11050, 1800), (8980, 1800), (8980, 3100)]),
    ('False_Ceiling_Master', [(11450, 350), (13750, 350), (13750, 1247), (14350, 1247), (14350, 4400), (12400, 4400), (12400, 5000), (10550, 5000), (10550, 3900), (11450, 3900)], RRECT(12000, 13650, 1150, 3750, 350, 8),
     [(11750, 700), (12700, 700), (13400, 700), (14000, 1600), (14000, 2560), (14000, 3500), (11750, 2000), (11750, 3300), (11000, 4450)]),
)
for nm, outer, hole, dl in rooms:
    it = item(nm, 'False_Ceiling'); SLABH(it, outer, hole, 2560, 2650, 'fceil', 'cove'); downlights(it, dl, 2560)
it = item('LED_Strips_Under_Carpentry_Warm_3000K', 'LED_Strips')
for b in ((6195, 6215, 2330, 2717), (6195, 6215, 2780, 3167), (6273, 7410, 3225, 3245), (9730, 11320, 3225, 3245), (13775, 13795, 380, 1217),
          (12430, 14320, 4425, 4445), (2035, 2055, 7483, 8220), (7945, 7965, 5560, 6670), (310, 2336, 5740, 5760)):
    B(it, b[0], b[1], b[2], b[3], 94, 100, 'led')
B(it, 9882, 9895, 6260, 6740, 1194, 1200, 'led'); B(it, 9965, 9978, 6260, 6740, 1594, 1600, 'led')
result = {'items': len(ITEMS)}
