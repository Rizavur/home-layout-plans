# build_model call 8 of 10
LB = session_state['L']; LQ = session_state['LQ']
ARC = LB['ARC']; B = LB['B']; CYL = LB['CYL']; CYLY = LB['CYLY']; PR3 = LB['PR3']; PRZ = LB['PRZ']; RRECT = LB['RRECT']
bed = LB['bed']; cabinet = LB['cabinet']; item = LB['item']; lever = LB['lever']; nightstand = LB['nightstand']; ITEMS = LB['ITEMS']
puff = LQ['puff']
wm = 'greige'; whm = 'gold'
it = item('Foyer_Cabinet_Run_with_Rounded_Glass_Display', 'Furniture')
cen = (1850, 6530); r = 230
poly = [cen] + ARC(cen[0], cen[1], r, -90, 0, 10)
PRZ(it, poly, 0, 100, 'charcoal')
for zz in (100, 700, 1250, 1800, 2250):
    PRZ(it, poly, zz, zz + 25, 'marble' if zz == 700 else 'white')
PRZ(it, poly, 2625, 2650, 'white')
B(it, 1850, 1870, 6300, 6530, 100, 2625, 'greige')
for zz in (690, 1240, 1790, 2240):
    PRZ(it, [(1870, 6530)] + ARC(cen[0], cen[1], r - 15, -85, 0, 10)[:-1] + [(2065, 6530)], zz, zz + 4, 'led')
CYL(it, 1960, 6440, 50, 125, 330, 'ceramic', 16); CYL(it, 1950, 6430, 45, 1275, 1420, 'gold', 16)
PRZ(it, ARC(cen[0], cen[1], r + 6, -90, 0, 16) + ARC(cen[0], cen[1], r + 1, 0, -90, 16), 100, 2625, 'glass')
B(it, 1850, 1856, 6294, 6300, 100, 2625, 'gold'); B(it, 2080, 2086, 6530, 6536, 100, 2625, 'gold')
B(it, 1850, 2080, 6530, 6647, 0, 2650, wm); B(it, 1850, 2080, 6647, 7453, 2100, 2650, wm)
for (a0, a1) in ((7453, 7850), (7853, 8250)):
    cabinet(it, '+x', a0, a1, 2080, 230, 0, 2650, 1, wm, 100, [2100], 'bar', hm=whm)
it = item('Shelter_Door_Concealed_Jib_Panel_Push_to_Open', 'Furniture')
B(it, 2058, 2080, 6652, 7448, 12, 2096, wm)
B(it, 1850, 1870, 6647, 6660, 0, 2100, 'white'); B(it, 1850, 1870, 7440, 7453, 0, 2100, 'white')
it = item('Shelter_Jib_Panel_Full_Length_Mirror', 'Furniture')
B(it, 2080, 2085, 6745, 7355, 215, 1985, 'mirror')
B(it, 2080, 2088, 6730, 6745, 200, 2000, 'gold'); B(it, 2080, 2088, 7355, 7370, 200, 2000, 'gold')
B(it, 2080, 2088, 6745, 7355, 200, 215, 'gold'); B(it, 2080, 2088, 6745, 7355, 1985, 2000, 'gold')
it = item('Shelter_Door_Handles', 'Doors'); lever(it, 'x', 1745, 1, 6780, 1000, 1, 'steel')
it = item('Foyer_Shoe_Cabinet_with_Grab_and_Go_Niche_and_Bench', 'Furniture')
cabinet(it, '-x', 7400, 8250, 3290, 450, 300, 1000, 2, 'white', 0, None, None)
B(it, 3290, 3740, 7400, 7418, 1000, 1350, 'white'); B(it, 3290, 3740, 8232, 8250, 1000, 1350, 'white')
B(it, 3720, 3740, 7418, 8232, 1018, 1350, 'walnut'); B(it, 3285, 3720, 7418, 8232, 1000, 1018, 'marble')
B(it, 3320, 3350, 7430, 8220, 1344, 1350, 'led')
cabinet(it, '-x', 7400, 8250, 3290, 450, 1350, 2650, 2, 'white', 0, [2100], None)
PRZ(it, RRECT(3420, 3640, 7480, 7700, 20, 3), 1018, 1030, 'gold'); CYL(it, 3530, 7600, 12, 1030, 1042, 'metal', 8)
CYL(it, 3500, 7880, 90, 1018, 1050, 'ceramic', 20); CYL(it, 3560, 8130, 45, 1018, 1100, 'charcoal', 14); CYL(it, 3560, 8130, 55, 1100, 1190, 'art1', 12)
B(it, 3700, 3720, 7780, 7800, 1180, 1220, 'gold')
B(it, 3320, 3350, 7410, 8230, 294, 300, 'led'); B(it, 3310, 3490, 7550, 8250, 0, 300, 'charcoal')
cabinet(it, '-x', 6700, 7397, 3290, 450, 1500, 2650, 1, 'white', 0, [2100], None)
B(it, 3290, 3740, 7380, 7400, 0, 1500, 'white'); B(it, 3720, 3740, 6700, 7380, 450, 1500, 'greige')
PRZ(it, [(3740, 6700), (3740, 7380), (3290, 7380)] + ARC(3510, 6920, 220, 180, 270, 8), 380, 450, 'charcoal')
PRZ(it, [(3730, 6710), (3730, 7370), (3300, 7370)] + ARC(3510, 6920, 210, 180, 270, 8), 450, 520, 'fabric2')
B(it, 3290, 3740, 6700, 6720, 1480, 1500, 'led')
for yy in (6900, 7150):
    B(it, 3690, 3720, yy - 10, yy + 10, 1250, 1270, 'gold'); B(it, 3660, 3690, yy - 10, yy + 10, 1250, 1330, 'gold')
it = item('Shelter_Freestanding_Cabinets_not_fixed_to_walls', 'Furniture')
cabinet(it, '+x', 6570, 8630, 650, 390, 0, 2300, 4, 'white', 80, [1900], 'bar')
it = item('Shelter_Foldable_Single_Mattress_shown_unfolded_900x1900', 'Furniture')
for (y0, y1) in ((6680, 7310), (7315, 7945), (7950, 8580)):
    B(it, 680, 1580, y0, y1, 0, 120, 'linen')
B(it, 720, 1540, 6700, 7080, 120, 200, 'linen')
it = item('Bedroom3_Queen_Bed', 'Furniture'); bed(it, 5850, 7790, 700, 2250, -1, 2)
it = item('Bedroom3_L_Wardrobe', 'Furniture')
cabinet(it, '+x', 2300, 2747, 6240, 590, 0, 450, 1, wm, 100, None, 'bar', hm=whm)
cabinet(it, '+x', 2300, 2747, 6240, 590, 1100, 2650, 1, wm, 0, [2250], 'bar', hm=whm)
cabinet(it, '+x', 2750, 3197, 6240, 590, 0, 2650, 1, wm, 100, [2250], 'bar', hm=whm)
B(it, 5650, 6240, 3200, 3800, 0, 2650, wm)
cabinet(it, '-y', 6243, 7440, 3200, 600, 0, 2650, 2, wm, 100, [2250], 'bar', hm=whm)
it = item('Bedroom3_Bedside_Nook_Open_to_Bed', 'Furniture')
B(it, 5650, 5670, 2300, 2727, 450, 1100, 'charcoal2'); B(it, 5650, 6240, 2727, 2747, 450, 1100, wm)
B(it, 5670, 6240, 2300, 2727, 450, 475, 'marble'); B(it, 6232, 6240, 2300, 2727, 450, 475, 'gold')
B(it, 5670, 6240, 2300, 2727, 1080, 1100, wm); B(it, 5690, 6220, 2315, 2712, 1076, 1080, 'led')
it = item('Bedroom2_Kids_Floor_Bed_Upholstered_with_Bolsters', 'Furniture')
PRZ(it, RRECT(10330, 11270, 830, 2770, 80, 5), 0, 40, 'walnut')
puff(it, RRECT(10290, 11310, 790, 2810, 100, 6), 40, 230, 'leather', 14, 10)
puff(it, RRECT(10380, 11130, 920, 2690, 50, 5), 230, 400, 'linen', 12, 8)
CYLY(it, 11205, 470, 105, 900, 2700, 'cush', 20)
PR3(it, [(855 + 95 * math.cos(2 * math.pi * k / 20), 470 + 95 * math.sin(2 * math.pi * k / 20)) for k in range(20)], (10380, 0, 0), (0, 1, 0), (0, 0, 1), (1, 0, 0), 0, 720, 'cush')
PR3(it, [(2745 + 80 * math.cos(2 * math.pi * k / 20), 440 + 80 * math.sin(2 * math.pi * k / 20)) for k in range(20)], (10380, 0, 0), (0, 1, 0), (0, 0, 1), (1, 0, 0), 0, 720, 'cush')
puff(it, RRECT(10440, 11060, 990, 1380, 80, 6), 400, 500, 'linen2', 40, 30)
puff(it, RRECT(10400, 11100, 1900, 2660, 40, 4), 400, 445, 'duvet', 12, 10)
puff(it, RRECT(10400, 11100, 1900, 2180, 40, 4), 445, 480, 'duvet', 12, 10)
CYL(it, 10560, 2420, 75, 480, 590, 'art2', 16); CYL(it, 10560, 2420, 58, 590, 690, 'art2', 16)
CYL(it, 10520, 2420, 18, 680, 715, 'art2', 8); CYL(it, 10600, 2420, 18, 680, 715, 'art2', 8)
it = item('Bedroom2_Kids_Rug', 'Decor'); PRZ(it, RRECT(9200, 10200, 1100, 2600, 60, 4), 0, 10, 'rug2')
it = item('Bedroom2_Wardrobe', 'Furniture'); cabinet(it, '-y', 9700, 11350, 3200, 600, 0, 2650, 3, wm, 100, [2250], 'bar', hm=whm)
it = item('Master_King_Bed', 'Furniture'); bed(it, 12320, 14350, 1640, 3490, 1, 2)
it = item('Master_Bedside_Tables', 'Furniture'); nightstand(it, 13950, 14350, 1250, 1620); nightstand(it, 13950, 14350, 3510, 3880)
it = item('Master_Tall_Cabinet', 'Furniture'); cabinet(it, '-x', 350, 1247, 13750, 600, 0, 2650, 2, wm, 100, [2250], 'bar', hm=whm)
it = item('Master_Wardrobe', 'Furniture'); cabinet(it, '-y', 12400, 14350, 4400, 600, 0, 2650, 4, wm, 100, [2250], 'bar', hm=whm)
it = item('Master_Bedside_Pendant_Sidelights', 'Lighting')
for cy in (1435, 3695):
    cx = 14140
    CYL(it, cx, cy, 45, 2550, 2560, 'gold', 16); CYL(it, cx, cy, 4, 1330, 2550, 'metal', 8); CYL(it, cx, cy, 35, 1300, 1330, 'gold', 16)
    for (z0, z1, rr) in ((1100, 1130, 70), (1130, 1170, 105), (1170, 1240, 122), (1240, 1280, 105), (1280, 1300, 70)):
        CYL(it, cx, cy, rr, z0, z1, 'lightw', 20)
it = item('Master_Organic_Wave_Mirror_Backlit', 'Decor')
mp = []
N = 120
for k in range(N):
    t = 2 * math.pi * k / N
    c = math.cos(t); s = math.sin(t)
    ru = 470 * (1 + 0.07 * math.sin(3 * t + 0.6) + 0.045 * math.sin(5 * t + 1.3))
    rv = 990 * (1 + 0.035 * math.sin(2 * t + 0.2) + 0.03 * math.sin(4 * t + 2.1))
    mp.append((840 + ru * (abs(c) ** 0.8) * (1 if c >= 0 else -1), 1070 + rv * (abs(s) ** 0.9) * (1 if s >= 0 else -1)))
gl = [(840 + (u - 840) * 1.07, 1070 + (v - 1070) * 1.035) for (u, v) in mp]
bev = [(840 + (u - 840) * 0.975, 1070 + (v - 1070) * 0.988) for (u, v) in mp]
mnt = [(840 + (u - 840) * 0.55, 1070 + (v - 1070) * 0.6) for (u, v) in mp]
O2 = (11450, 0, 0); Uy2 = (0, 1, 0); Vz3 = (0, 0, 1); Wx2 = (1, 0, 0)
PR3(it, gl, O2, Uy2, Vz3, Wx2, 0, 2, 'cove')
PR3(it, mnt, O2, Uy2, Vz3, Wx2, 2, 22, 'charcoal')
PR3(it, mp, O2, Uy2, Vz3, Wx2, 22, 28, 'mirror')
PR3(it, bev, O2, Uy2, Vz3, Wx2, 28, 30, 'mirror')
result = {'items': len(ITEMS)}
