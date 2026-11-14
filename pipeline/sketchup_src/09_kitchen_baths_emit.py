# build_model call 9 of 10
LB = session_state['L']; LQ = session_state['LQ']
B = LB['B']; CYL = LB['CYL']; CYLY = LB['CYLY']; PRZ = LB['PRZ']; RRECT = LB['RRECT']; V = LB['V']; item = LB['item']; cabinet = LB['cabinet']
wc = LB['wc']; shower_set = LB['shower_set']; ITEMS = LB['ITEMS']; MATS = LB['MATS']; item_faces = LB['item_faces']
krun = LQ['krun']; vanity_ledge = LQ['vanity_ledge']
F = session_state['fns']
it = item('Kitchen_Tall_Larder_Dry_Goods_with_Microwave_and_Door_Pocket', 'Kitchen')
cabinet(it, '+y', 4940, 5413, 7500, 600, 0, 2650, 1, 'white', 100, [1350, 2250], 'bar', hm='gold')
cabinet(it, '+y', 5417, 5890, 7500, 600, 0, 1350, 1, 'white', 100, None, 'bar', hm='gold')
B(it, 5417, 5890, 6920, 7460, 1350, 1753, 'white')
B(it, 5440, 5867, 7460, 7498, 1368, 1735, 'appl'); B(it, 5462, 5770, 7497, 7500, 1400, 1700, 'glassblk'); B(it, 5790, 5850, 7497, 7500, 1400, 1700, 'screen')
cabinet(it, '+y', 5417, 5890, 7500, 600, 1753, 2650, 1, 'white', 0, [2250], 'bar', hm='gold')
B(it, 4940, 5890, 6800, 6900, 2250, 2650, 'white')
it = item('Kitchen_Base_Drawers_Dining_Wall', 'Kitchen')
krun(it, '+y', 7400, 600, 0, 870, 150, [(5890, 6540, 'drawers4'), (6540, 7190, 'drawers'), (7190, 7840, 'drawers')], 'top')
it = item('Kitchen_Wall_Cabinets_Dining_Wall', 'Kitchen')
krun(it, '+y', 7150, 350, 1500, 2250, 0, [(5890, 6540, 'door2'), (6540, 7190, 'door2'), (7190, 7840, 'door2')], 'bottom')
krun(it, '+y', 7150, 300, 2253, 2650, 0, [(5890, 6540, 'flat'), (6540, 7190, 'flat'), (7190, 7840, 'flat')], 'bottom')
it = item('Sintered_Stone_Top_and_Backsplash_Dining_Wall', 'Kitchen')
B(it, 5890, 7840, 6800, 7420, 870, 900, 'sintered'); B(it, 5890, 7840, 6800, 6815, 900, 1500, 'sintered')
it = item('Kitchen_Appliance_Garage_Kettle_Rice_Cooker_Toaster', 'Kitchen')
B(it, 7190, 7208, 6815, 7150, 900, 1494, 'white'); B(it, 7822, 7840, 6815, 7150, 900, 1494, 'white')
B(it, 7208, 7822, 6815, 6830, 900, 1494, 'walnut'); B(it, 7208, 7822, 6830, 7150, 1474, 1494, 'white')
B(it, 7230, 7800, 7120, 7140, 1468, 1474, 'led')
for xs in (7300, 7520, 7720):
    B(it, xs - 35, xs + 35, 6830, 6836, 1180, 1250, 'appl')
CYL(it, 7300, 6960, 82, 900, 1130, 'steel', 20); CYL(it, 7300, 6960, 60, 1130, 1150, 'metal', 16); B(it, 7375, 7395, 6945, 6975, 960, 1110, 'metal')
CYL(it, 7500, 6975, 135, 900, 1120, 'appl', 24); CYL(it, 7500, 6975, 120, 1120, 1150, 'appl', 24); B(it, 7470, 7530, 7105, 7115, 1000, 1050, 'screen')
PRZ(it, RRECT(7650, 7800, 6870, 7110, 30, 3), 900, 1090, 'steel'); B(it, 7690, 7760, 6880, 6900, 1090, 1092, 'screen'); B(it, 7690, 7760, 6960, 6980, 1090, 1092, 'screen')
it = item('Kitchen_Base_Hob_Oven_Sink_Dishwasher', 'Kitchen')
krun(it, '-y', 8700, 600, 0, 870, 150, [(4810, 5410, 'drawers4'), (5410, 6010, 'drawers'), (6010, 6610, 'skip'), (6610, 6790, 'door'), (6790, 7390, 'door2'), (7390, 7840, 'door')], 'top')
V(it, 6820, 7360, 8760, 9220, 700, 870, 'white')
B(it, 6013, 6607, 8700, 8720, 150, 230, 'white'); B(it, 6013, 6607, 8700, 8720, 233, 867, 'glassblk'); B(it, 6080, 6540, 8680, 8700, 800, 812, 'steel')
B(it, 6100, 6520, 8698, 8700, 300, 700, 'smoke')
B(it, 7393, 7837, 8696, 8698, 820, 860, 'metal')
it = item('Sintered_Stone_Top_and_Backsplash_Hob_Wall', 'Kitchen')
B(it, 4810, 7840, 8680, 9300, 870, 900, 'sintered'); V(it, 6840, 7340, 8780, 9200, 870, 900, 'sintered')
B(it, 4810, 7840, 9285, 9300, 900, 1500, 'sintered')
it = item('Kitchen_Wall_Cabinets_Hob_Wall', 'Kitchen')
krun(it, '-y', 8950, 350, 1500, 2250, 0, [(4810, 5410, 'door2'), (5410, 6010, 'door2')], 'bottom')
krun(it, '-y', 8950, 350, 1500, 2250, 0, [(6610, 7225, 'door'), (7225, 7840, 'door')], 'bottom')
krun(it, '-y', 8950, 350, 2253, 2650, 0, [(4810, 5410, 'flat'), (5410, 6010, 'flat'), (6010, 6610, 'flat'), (6610, 7225, 'flat'), (7225, 7840, 'flat')], 'bottom')
krun(it, '-y', 8950, 350, 1563, 2250, 0, [(6010, 6610, 'flat')], 'bottom')
krun(it, '-y', 8600, 700, 1900, 2650, 0, [(3990, 4400, 'door'), (4400, 4810, 'door')], 'bottom')
it = item('Kitchen_Sink_and_Tap', 'Kitchen')
B(it, 6820, 7360, 8760, 9220, 700, 870, 'steel'); V(it, 6840, 7340, 8780, 9200, 720, 870, 'steel')
B(it, 7070, 7110, 9220, 9260, 900, 1250, 'chrome'); B(it, 7075, 7105, 9000, 9260, 1220, 1250, 'chrome'); B(it, 7075, 7105, 9000, 9030, 1150, 1220, 'chrome')
it = item('Kitchen_Induction_Hob', 'Kitchen')
B(it, 6020, 6600, 8780, 9230, 900, 906, 'glassblk')
for (x, y) in ((6170, 8900), (6450, 8900), (6170, 9110), (6450, 9110)): CYL(it, x, y, 90, 906, 907, 'steel', 20)
it = item('Kitchen_Cooker_Hood', 'Kitchen')
B(it, 6010, 6610, 8900, 9300, 1500, 1560, 'steel'); B(it, 6060, 6560, 8895, 8900, 1515, 1545, 'metal')
it = item('Kitchen_LED_Under_Wall_Cabinets', 'LED_Strips')
B(it, 5910, 7180, 7100, 7120, 1494, 1500, 'led')
B(it, 4830, 6000, 8980, 9000, 1494, 1500, 'led'); B(it, 6620, 7820, 8980, 9000, 1494, 1500, 'led')
it = item('Kitchen_Door_Frame_and_Track', 'Kitchen')
B(it, 3990, 4010, 6700, 6850, 0, 2130, 'metal'); B(it, 3990, 4940, 6700, 6850, 2130, 2250, 'white')
B(it, 3990, 5890, 6852, 6898, 2105, 2130, 'metal')
for (nm, lay, x0) in (('Kitchen_Sliding_Door_CLOSED', 'Kitchen_Door_Closed', 3995), ('Kitchen_Sliding_Door_OPEN_in_pocket', 'Kitchen_Door_Open', 4925)):
    it = item(nm, lay)
    x1 = x0 + 960
    B(it, x0, x0 + 45, 6860, 6890, 10, 2100, 'charcoal'); B(it, x1 - 45, x1, 6860, 6890, 10, 2100, 'charcoal')
    B(it, x0 + 45, x1 - 45, 6860, 6890, 10, 100, 'charcoal'); B(it, x0 + 45, x1 - 45, 6860, 6890, 2010, 2100, 'charcoal')
    B(it, x0 + 45, x1 - 45, 6869, 6881, 100, 2010, 'fglass')
    B(it, x0 + 12, x0 + 30, 6855, 6860, 850, 1250, 'gold'); B(it, x0 + 12, x0 + 30, 6890, 6895, 850, 1250, 'gold')
it = item('Fridge', 'Kitchen')
B(it, 4000, 4800, 8600, 9280, 0, 20, 'metal'); B(it, 4000, 4800, 8600, 9280, 20, 1800, 'silver')
B(it, 4000, 4398, 8580, 8600, 1000, 1800, 'silver'); B(it, 4402, 4800, 8580, 8600, 1000, 1800, 'silver'); B(it, 4000, 4800, 8580, 8600, 60, 996, 'silver')
B(it, 4370, 4385, 8545, 8580, 1150, 1650, 'steel'); B(it, 4415, 4430, 8545, 8580, 1150, 1650, 'steel'); B(it, 4300, 4500, 8545, 8580, 900, 915, 'steel')
it = item('Gas_Water_Heater_Wall_Mounted', 'Kitchen')
B(it, 8035, 8535, 6950, 7370, 1550, 2300, 'appl'); B(it, 8200, 8240, 7050, 7090, 1450, 1550, 'steel'); B(it, 8330, 8370, 7050, 7090, 1450, 1550, 'steel')
for (nm, y0, y1, fy, s) in (('Dryer', 6960, 7560, 7560, 1), ('Washing_Machine', 8690, 9290, 8690, -1)):
    it = item(nm, 'Kitchen')
    B(it, 8660, 9260, y0, y1, 0, 850, 'appl')
    CYLY(it, 8960, 430, 170, fy, fy + s * 25, 'steel', 28); CYLY(it, 8960, 430, 130, fy + s * 25, fy + s * 30, 'screen', 28)
    zz = sorted([fy, fy + s * 5])
    B(it, 8700, 8900, zz[0], zz[1], 740, 820, 'steel')
it = item('Yard_Pipe_Boxup', 'Kitchen'); B(it, 7940, 8630, 8650, 9300, 0, 2650, 'white')
it = item('Yard_Cabinets_and_Tabletops', 'Kitchen')
cabinet(it, '+y', 7940, 8640, 7560, 610, 0, 870, 1, 'white', 150, None, 'bar', base='mortar_y')
B(it, 7940, 9290, 6950, 7580, 870, 900, 'quartz'); B(it, 8640, 9290, 8670, 9300, 870, 900, 'quartz')
cabinet(it, '+y', 8640, 9290, 7300, 350, 1500, 2650, 1, 'white', 0, [2250], 'bar')
cabinet(it, '-y', 8640, 9290, 8950, 350, 1500, 2650, 1, 'white', 0, [2250], 'bar')
it = item('Steigen_Ceiling_Drying_Rack', 'Kitchen')
for yc in (7420, 8830):
    B(it, 8770, 9230, yc - 40, yc + 40, 2630, 2650, 'steel')
    for xc in (8800, 9200):
        B(it, xc - 15, xc + 15, yc - 10, yc + 10, 2320, 2630, 'steel')
    B(it, 8780, 9220, yc - 15, yc + 15, 2290, 2320, 'steel')
for xc in (8830, 8915, 9000, 9085, 9170):
    CYLY(it, xc, 2280, 15, 7380, 8870, 'steel', 12)
it = item('Common_Bath_WC', 'Sanitary'); wc(it, '-x', 10820, 5480)
it = item('Common_Bath_Vanity_3_Mirror_Cabinets_with_Display_Ledge', 'Sanitary')
vanity_ledge(it, '-y', 8800, 9880, 6850, 460, 8800, 9880, 1150, 2230, [(9000, 'diffuser'), (9150, 'candle'), (9720, 'plant')], 3)
it = item('Common_Bath_Shower_Set', 'Sanitary'); shower_set(it, 'x', 10820, -1, 6520)
it = item('Ensuite_WC', 'Sanitary'); wc(it, '+x', 10920, 6380)
it = item('Ensuite_Vanity_5_Mirror_Cabinets_with_Display_Ledge', 'Sanitary')
vanity_ledge(it, '+x', 5110, 6080, 10920, 440, 5100, 6850, 1150, 2230, [(5280, 'diffuser'), (5430, 'candle'), (6650, 'plant')], 5)
it = item('Ensuite_Shower_Set', 'Sanitary'); shower_set(it, 'y', 6850, -1, 12720)
LAY = dict((L.get_name(), L) for L in model.get_layers())
mats = {}
for k, v in MATS.items(): mats[k] = get_or_create_material(v[0], v[1], v[2], v[3], v[4])
parents = {}
for g in model.get_entities().get_groups():
    if g.get_name() in ('Doors', 'Windows'): parents[g.get_name()] = g
cnt = 0; nf = 0; errs = []
for it in ITEMS:
    lay = it['layer']
    if lay not in parents:
        pg = Group(); model.get_entities().add_group(pg); pg.set_name(lay); pg.set_layer(LAY[lay]); parents[lay] = pg
    ig = Group(); parents[lay].get_entities().add_group(ig); ig.set_name(it['name']); ig.set_layer(LAY[lay])
    try:
        r, p = item_faces(it, F['vx_mesh'], F['vx_clusters'])
        for m, fs in r.items():
            if len(fs) > 0:
                F['su_fill'](it['name'] + '_' + m, fs, mats, ig.get_entities(), LAY[lay]); nf += len(fs)
        for m, fs in p.items():
            gr = F['su_fill'](it['name'] + '_' + m + '_round', fs, mats, ig.get_entities(), LAY[lay]); nf += len(fs)
            try: soften_by_angle(gr, 25.0)
            except Exception as e: pass
    except Exception as e:
        errs.append([it['name'], str(e)[:150]])
    cnt += 1
result = {'items': cnt, 'faces': nf, 'errs': errs}
