import math
import planlib as P, blocks as K, views_common as VC
def build(c):
    B, CYL, PRZ, RRECT, SLABH = c.B, c.CYL, c.PRZ, c.RRECT, c.SLABH
    K.fixtures(c)
    it = c.item('Living_West_Wall_Cladding', 'Furniture'); B(it, 250, 290, 1170, 6300, 0, 2650, 'wallp')
    # ---- Living from the screenshot ----
    it = c.item('Living_Window_Seats_x3_Modular', 'Furniture')
    for cx in (1150, 2450, 3750): c.sofa2(it, '+y', cx, 2400, 1050, 800, 1, False, False, None, 'sofa', 'sofa2', ('pil1', 'pil2'))
    it = c.item('Living_West_Sofa_Facing_East', 'Furniture'); c.sofa2(it, '+x', 1580, 3520, 1700, 950, 2, True, True, None, 'sofa', 'sofa2', ('pil2', 'pil1'))
    it = c.item('Living_East_Long_Sofa_Facing_West', 'Furniture'); c.sofa2(it, '-x', 4480, 2770, 2400, 950, 3, True, True, None, 'sofa', 'sofa2', ('pil1', 'pil2'))
    it = c.item('Living_Round_Coffee_Table_Travertine', 'Furniture')
    cx, cy = 2880, 3350
    CYL(it, cx, cy, 400, 362, 400, 'traver', 48); CYL(it, cx, cy, 390, 358, 362, 'gold', 48); CYL(it, cx, cy, 240, 0, 358, 'walnut', 36)
    for k in range(32): a = 2 * math.pi * k / 32; CYL(it, cx + 246 * math.cos(a), cy + 246 * math.sin(a), 15, 0, 358, 'walnut2', 8)
    CYL(it, cx + 120, cy - 60, 90, 400, 450, 'ceramic', 20); B(it, cx - 200, cx + 20, cy - 40, cy + 120, 400, 440, 'artbg')
    it = c.item('Living_Rug', 'Decor'); PRZ(it, RRECT(1300, 4400, 2250, 4450, 150, 6), 0, 8, 'rug1'); PRZ(it, RRECT(1420, 4280, 2370, 4330, 100, 6), 8, 10, 'rug2')
    # angled corner TV wall with full-height storage behind the TV (fixed to west wall; free-standing 50 mm off the shelter wall)
    X2, Y1, YS = 2222, 4511, 6250
    ang = math.degrees(math.atan2(YS - Y1, X2 - 290)); L = math.hypot(X2 - 290, YS - Y1)
    tx, ty = (290 + X2) / 2.0, (Y1 + YS) / 2.0
    tri = [(290, Y1), (X2, YS), (290, YS)]
    it = c.item('Living_Corner_TV_Wall_with_Storage_Behind', 'Furniture')
    PRZ(it, c.inset(tri, 45), 0, 100, 'charcoal'); PRZ(it, tri, 100, 2550, K.WM)
    for s in (-1, 1):
        for k in range(2):
            du = s * (L / 2.0 - 225 - k * 0) if k == 0 else None
        du = s * (L / 2.0 - 230)
        P.rbox(c, it, tx, ty, 446, 20, ang, 100, 2550, K.WM, du, -10)                       # end-bay full-height doors
        P.rbox(c, it, tx, ty, 14, 25, ang, 950, 1550, 'gold', du - s * 190, -32)              # bar handles
    P.rbox(c, it, tx, ty, L - 920, 22, ang, 100, 2000, 'marble', 0, -11)                     # marble backdrop to the TV
    P.rbox(c, it, tx, ty, L - 920, 6, ang, 1994, 2000, 'led', 0, -25)
    for s in (-1, 1): P.rbox(c, it, tx, ty, (L - 920) / 2.0 - 3, 20, ang, 2003, 2550, K.WM, s * (L - 920) / 4.0, -10)   # top flap doors
    P.rbox(c, it, tx, ty, 1600, 380, ang, 300, 520, 'walnut', 0, -210); P.rbox(c, it, tx, ty, 1620, 390, ang, 520, 540, 'marble', 0, -212)   # floating console drawers
    P.rbox(c, it, tx, ty, 1560, 6, ang, 294, 300, 'led', 0, -210)
    for s in (-1, 1): P.rbox(c, it, tx, ty, 8, 300, ang, 410, 418, 'gold', s * 400, -210)
    P.rbox(c, it, tx, ty, 80, 80, ang, 540, 760, 'ceramic', 600, -230)
    it = c.item('TV_75_inch', 'Furniture'); P.rbox(c, it, tx, ty, 1660, 30, ang, 900, 1835, 'screen', 0, -40)
    it = c.item('Living_Floor_Lamp', 'Lighting'); P.floor_lamp(c, it, 560, 2700)
    it = c.item('Curtains_Living', 'Curtains'); c.curtain_full(it, 290, 5550, 1375, 420, 420, 6, 2540)
    it = c.item('Living_Wall_Art_Marble_Diptych', 'Decor'); P.painting(c, it, 'x', 5550, -1, 1990, 2730, 1300, 2150, 'artm'); P.painting(c, it, 'x', 5550, -1, 2790, 3530, 1300, 2150, 'artm')
    # entrance half-glass partition (same as Plan B)
    it = c.item('Entry_Glass_Partition_Flush_with_Shelter_Wall', 'Partitions')
    x0, x1, y0, y1 = 2080, 2600, 6300, 6420
    B(it, x0, x1, y0, y1, 0, 60, 'charcoal'); B(it, x0, x1, y0, y1, 60, 950, 'wallp'); B(it, x0 - 2, x1 + 6, y0 - 6, y1 + 6, 950, 975, 'marble')
    B(it, x0, x1 - 10, y0 - 4, y0, 930, 936, 'led'); B(it, x0, x1 - 10, y1, y1 + 4, 930, 936, 'led')
    B(it, x1 - 40, x1, y0, y1, 975, 2550, 'frame'); B(it, x0, x0 + 30, y0, y1, 975, 2550, 'frame'); B(it, x0, x1, y0 + 40, y0 + 80, 2510, 2550, 'frame')
    B(it, x0 + 30, x1 - 40, y0 + 52, y0 + 68, 975, 2510, 'fglass'); B(it, 1850, 2600, 6300, 6420, 2550, 2650, 'wallp')
    WA = c.wave(2900, 3300, 1700, 1050, 0.4, 0.14); WB = c.wave(2900, 3300, 1300, 720, 2.3, 0.16)
    it = c.item('False_Ceiling_Living_Organic_Wave_Cove', 'False_Ceiling')
    SLABH(it, [(290, 1510), (5550, 1510), (5550, 3950), (5300, 3950), (5300, 4950), (5550, 4950), (5550, 5000), (5100, 5000), (5100, 6700), (3740, 6700), (3740, 6420), (2600, 6420), (2600, 6300), (290, 6300)], WA, 2550, 2650, 'fceil', 'cove')
    c.downlights(it, [(470, 2000), (1800, 1680), (2700, 1680), (3600, 1680), (4500, 1680), (5320, 1750), (5320, 3600), (600, 4300), (1500, 5200), (3900, 5000), (4500, 5600), (3700, 6150), (4400, 6500), (2600, 5900)], 2550)
    K.dining9(c); K.foyer(c, 'square'); K.curtains_bed(c)
    # bedroom 3 options from Plan A
    PRZ_ = PRZ
    it = c.item('OptA_Bedroom3_Queen_Bed', 'Option_A_Bedroom3_Bed'); P.bed2(c, it, 5850, 7850, 700, 2230, '-x', 2)
    P.painting(c, it, 'x', 5850, 1, 850, 2100, 1300, 2000, 'artw'); PRZ_(it, RRECT(6450, 8250, 500, 2500, 60, 4), 0, 10, 'rug2')
    it = c.item('OptB_Bedroom3_Two_Standing_Desks', 'Option_B_Bedroom3_Desks')
    for cy in (1200, 2300): P.sdesk(c, it, '+x', 7950, cy, 1050, 585); c.station(it, '+x', 7950, cy, 585); c.chair2(it, '+x', 7550, cy)
    PRZ_(it, RRECT(6400, 7700, 900, 2600, 60, 4), 0, 10, 'rug2')
    K.bedrooms(c, br3='none'); K.fans_ac(c, (2880, 3350))
    K.lights(c, ((5600, 8050), (7000, 8050), (8400, 8050), (2700, 7400), (9300, 4450), (10800, 4450), (9300, 5800), (12000, 5800), (925, 7600)))
    K.ceil_rooms(c); K.led(c, [(7945, 7965, 5560, 6670)])
    K.kitchen_closed(c, 'Kitchen_Closed'); K.kitchen_common(c); K.kitchen_open(c, 'Kitchen_Open'); K.kitchen_glass(c); K.yard_baths(c)
    K.power_common(c, [('f', 1900, 0, 4700, 0), ('f', 2880, 0, 3350, 0), ('x', 290, 1, 2700, 300), ('x', 5550, -1, 2000, 300), ('x', 4940, 1, 7200, 1150), ('x', 8535, -1, 1750, 1050, True)])
    K.trunking_common(c, [])
MODES = {}
for k, v in VC.KMODES.items(): MODES[k] = {'label': v['label'] + ' · BR3 queen bed', 'hide': v['hide'] + ['Option_B_Bedroom3_Desks']}
MODES['br3desk'] = {'label': 'Bedroom 3 as study (open kitchen)', 'hide': VC.KMODES['open']['hide'] + ['Option_A_Bedroom3_Bed']}
VIEWS = VC.HEAD + [
 ('Living – lounge seating from the TV corner', (1750, 4950, 1600), (3300, 2500, 700), 80, ''),
 ('Living – angled TV wall with storage behind', (3600, 2700, 1500), (1256, 5380, 1200), 75, ''),
 ('TV corner – cabinets around and behind the TV', (3100, 3800, 1550), (1256, 5380, 1300), 72, ''),
 ('Living – window seats', (2900, 4600, 1600), (2700, 1600, 700), 80, ''),
 ('Living – wave ceiling over the seating', (4300, 4800, 1250), (2900, 3300, 2600), 88, ''),
 ('Entrance partition – from foyer', (3150, 7900, 1550), (2250, 6300, 1250), 62, ''),
 ('Dining – table for 8 outside kitchen', (4300, 4100, 1600), (7000, 6000, 700), 80, ''),
 ('Dining – from pantry end', (7950, 4300, 1600), (4500, 6200, 800), 80, ''),
 ('Bedroom 3 – queen bed', (8350, 3450, 1650), (5850, 1450, 1200), 88, '', 'open'),
 ('Bedroom 3 – as study (2 standing desks)', (6450, 2950, 1650), (8550, 1300, 700), 85, '', 'br3desk'),
 ('Bedroom 3 – towards the door', (6150, 700, 1600), (8100, 3300, 1000), 85, '', 'open'),
] + VC.KITCHEN_OPEN_VIEWS + VC.tail(False)
LABELS = VC.COMMON_LABELS + [('Living', 2880, 3000), ('Dining', 6150, 5600), ('Dry pantry', 8150, 5850), ('Bedroom 3', 7000, 1500)]
DIMS = [((1280, 5355), (2880, 3350), 'TV → coffee table ≈ 2560'), ((2600, 6360), (3740, 6360), 'Clear way in from foyer ≈ 1140'), ((5150, 5050), (7150, 5050), 'Table 2000 × 1000'), ((4600, 4700), (4600, 3900), 'Walkway to bedrooms ≈ 800')]
INFO = ("Plan E. Living room: three modular seats along the window, a sofa on each side, a round travertine coffee table "
        "and an angled corner TV wall: the TV sits on a marble panel above a floating walnut console, with full-height cabinets behind it, reached through the doors at both ends and the flap doors above (deep corner storage). It is fixed to the west wall and stands 50 mm off the shelter wall – nothing fixed to the shelter. Entrance half-glass partition as in Plan B. "
        "Dining moves outside the kitchen, so Plan A's study room is dropped; bedroom 3 keeps Plan A's two options (queen bed or 2 standing desks – see the option menu). "
        "Everything else follows Plan A. Kitchen: closed or open with bi-fold glass; removing the kitchen front wall must be confirmed with HDB / your ID. "
        "Power points and trunking are indicative.")
