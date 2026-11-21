"""Cost estimate for every plan.

Renovation: unit rates from the two contractor quotes (Q1 = first contractor quote, Q2 = second contractor quote), always the lower
of the two for the same kind of work; quantities measured from each plan's 3D model (default layout option).
Furniture & appliances: Singapore retail prices (mid-range), Nov 2026.

python3 estimate.py   -> writes ../data/costs.json (full breakdown) and prints the totals
"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import quantities

FT = 304.8

# ---------------------------------------------------------------- renovation rates (lower of the two quotes)
R = {
    'haulage':        (1500, 'lump', 'Q1 #1 haulage & debris (Q2 only quotes it inside hacking)'),
    'cleaning':       (500, 'lump', 'Q2 #47 whole-house cleaning (Q1 #2 $600)'),
    'floor_tiles':    (8100, 'lump', 'Q2 #5 + #5a + #6: tiles $6,000 + resin grout $1,600 + skirting $500 (Q1 #3 $10,000)'),
    'plinth':         (400, 'lump', 'Q1 #4 = Q2 #10'),
    'kerb_washer':    (300, 'lump', 'Q2 #29d (Q1 #5 $400)'),
    'remove_yard':    (500, 'lump', 'Q1 #6 (Lakeside scope)'),
    'cb_wall':        (950, 'lump', 'Q1 #7 (Lakeside scope)'),
    'mb_overlay':     (950, 'lump', 'Q1 #8 (Lakeside scope)'),
    'hack_wall':      (950, 'lump', 'Q2 #52 wall demolition incl. PE endorsement'),
    'wardrobe':       (270, 'ft', 'Q2 #11/#12 $3,100 / 11.5 ft, $3,780 / 14 ft (Q1 $290/ft)'),
    'l_surcharge':    (550, 'lump', 'Q1 #16 L-shape corner surcharge'),
    'tall':           (270, 'ft', 'Full-height casement cabinet at the wardrobe rate, Q2 #12 (Q2 tall shoe/kitchen $337/ft)'),
    'half':           (170, 'ft', 'Q1 #13 $950 / 1.7 m incl. laminate top'),
    'top':            (168, 'ft', 'Q2 #30 $420 / 2.5 ft (Q2 #18 $200/ft)'),
    'mirror_cab':     (180, 'ft', 'Q1 #19 $1,620 / 9 ft (Q2 $200/ft)'),
    'vanity':         (350, 'ft', 'Q2 #19 $700 / 2 ft with integrated basin'),
    'kitchen_tb':     (305, 'ft', 'Q1 #22 $2,900 / 9.5 ft (Q2 $337/ft)'),
    'sint_tb':        (178, 'ft', 'Q2 #29a top + backing $1,560 / 8.75 ft (Q1 top + backsplash $240/ft)'),
    'sint_top':       (120, 'ft', 'Q1 #23 $1,140 / 9.5 ft'),
    'tv_feature':     (338, 'ft', 'Q2 #24 $2,700 / 8 ft TV console + backdrop + strip light'),
    'tile_feature':   (680, 'lump', 'Q2 #24aa marble-look tile on the feature wall'),
    'fluted':         (400, 'ft', 'Q2 #15 $3,200 / 8 ft fluted feature wall'),
    'backing':        (1000, 'lump', 'Q2 #23b laminate backing panel'),
    'partition':      (71, 'ft', 'Q2 #21 $600 / 8.5 ft full-height 2-sided partition'),
    'fixed_glass':    (400, 'panel', 'Q1 #29 aluminium-framed fixed glass'),
    'mirror':         (600, 'lump', 'Q1 #14 mirror with laminate frame (Q2 #54 $1,900)'),
    'db_door':        (300, 'lump', 'Q1 #10 DB door in matching laminate'),
    'hs_feature':     (2800, 'lump', 'Q2 #27 HS feature wall with casement storage (Q1 #11 $4,000)'),
    'pipe_box':       (450, 'lump', 'Q2 #49 box up pipes'),
    'bedroom_door':   (400, 'each', 'Q2 #35/#36 laminate swing door (Q1 $500)'),
    'toilet_door':    (400, 'each', 'Q2 #37 aluminium slide & swing (Q1 $500)'),
    'kitchen_bifold': (2100, 'lump', 'Q1 #27 slide & fold aluminium door + window at kitchen entrance'),
    'kitchen_slide':  (1300, 'lump', 'Q2 #39 glass pocket sliding door'),
    'glass_slide':    (1200, 'panel', 'Q2 #31a $4,800 / 4 slim-frame fluted glass panels'),
    'yard_door':      (800, 'lump', 'Q1 #28 sliding door to yard'),
    'yard_glass':     (400, 'lump', 'Q1 #29 fixed glass beside the yard door'),
    'yard_window':    (900, 'lump', 'Q1 #30 yard sliding window'),
    'shower_screen':  (600, 'each', 'Q1 #31 tempered glass shower screen'),
    'plumbing':       (560, 'lump', 'Q1 #32 + #33 $280 + $280 (Q2 #45 $700)'),
    'electrical':     (2000, 'lump', 'Q1 #34 electrical A&A estimate (Q2 A&A $3,300)'),
    'downlight':      (20, 'each', 'Q2 #58 downlight housing'),
    'led':            (12, 'm', 'Q2 #63 COB strip light'),
    'driver':         (9, 'm', 'Q2 #64 drivers $420 / 46 m'),
    'profile':        (10, 'm', 'Q2 #65 strip housing $330 / 33 m'),
    'fceil':          (640, 'zone', 'Q2 #33 $3,200 / 5 zones incl. curtain pelmets (Q1 $4,200)'),
    'aircon5':        (7000, 'set', 'Q2 #32 Mitsubishi Starmex, 2 x System 3, 5 fan coils (Q1 $7,500)'),
    'aircon_extra':   (1400, 'unit', 'Pro-rata of Q2 #32 ($7,000 / 5) per extra fan coil'),
    'painting':       (1600, 'lump', 'Q2 #46 Nippon Vinilex 5000, whole house'),
    'grille_living':  (1000, 'lump', 'Q2 #50 invisible grille, living'),
    'grille_beds':    (1600, 'lump', 'Q2 #56 invisible grilles, 3 bedrooms'),
    'wifi':           (2100, 'lump', 'Q2 #66 5 access points, PoE switch, controller, set-up'),
    'fridge_kerb':    (200, 'lump', 'Q2 #28b kerb with tiles for fridge'),
}

# ---------------------------------------------------------------- furniture & appliance prices (SGD, Nov 2026)
F = {
    'washer':     (860, 'LG 9 kg front-load FB1209S6M, Harvey Norman'),
    'dryer':      (1140, 'Midea 9 kg heat-pump dryer, Courts'),
    'stack_kit':  (60, 'Stacking kit (estimate)'),
    'fridge':     (1450, 'Panasonic 497 L 2-door NR-BW530XMMS, Courts'),
    'hob':        (800, '60 cm induction hob (estimate, mid-range)'),
    'hood':       (504, 'Samsung 60 cm telescopic hood (launch price)'),
    'oven':       (578, 'Fujioh 70 L built-in oven FV-EL61'),
    'dishwasher': (910, 'Bosch Series 2 60 cm fully integrated, Courts'),
    'microwave':  (200, 'Countertop microwave (estimate)'),
    'heater':     (650, 'Rubine BENE 10FE gas heater $400 + BTO installation $250'),
    'tv75':       (1299, 'LG 75-inch UHD 4K, Harvey Norman'),
    'sofa_l':     (2497, 'Castlery Lena L-shape sectional'),
    'sofa_3':     (1199, 'Castlery Adams 3-seater'),
    'sofa_2':     (999, '2-seater / loveseat (estimate)'),
    'sofa_mod':   (749, 'Castlery Tovi armless module'),
    'coffee':     (500, 'Coffee table (estimate)'),
    'side_table': (379, 'Castlery Lavine marble side table'),
    'dining_tbl': (1599, 'Castlery Kelsey marble dining table 180 cm'),
    'dining_ch':  (330, 'Castlery Kelsey leather chair (from the 4-chair set price)'),
    'stool':      (150, 'Counter stool (estimate)'),
    'king_bed':   (1299, 'Castlery Dalton king bed frame'),
    'king_mat':   (1340, 'Princebed Imperial Deluxe pocketed spring, king'),
    'queen_bed':  (1099, 'Castlery Joseph queen bed frame'),
    'queen_mat':  (990, 'Princebed Imperial Deluxe, queen'),
    'ss_bed':     (600, 'Upholstered super-single floor bed (estimate)'),
    'ss_mat':     (810, 'Princebed Imperial Deluxe, super single'),
    'single_bed': (300, 'Single bed frame (estimate)'),
    'single_mat': (730, 'Princebed Imperial Deluxe, single'),
    'trifold':    (122, 'Princebed Para Foam 3-fold single, 4 inch'),
    'bedside':    (449, 'Castlery Vento bedside table'),
    'desk':       (599, 'TTRacing Titus electric standing desk'),
    'chair':      (350, 'Mid-range ergonomic chair'),
    'monitor':    (449, 'Acer DA271K 27-inch 4K'),
    'fan':        (299, 'Fanztec 52-inch DC ceiling fan with LED, Courts'),
    'fan_less':   (499, 'Bladeless tower fan (estimate)'),
    'pendant':    (350, 'Dining linear pendant (estimate)'),
    'pend_clust': (600, 'Sculptural pendant cluster (estimate)'),
    'floor_lamp': (200, 'Floor lamp (estimate)'),
    'sconce':     (120, 'Wall sconce (estimate)'),
    'ceil_light': (100, 'Ceiling light (estimate)'),
    'curtain':    (400, 'Day + night curtains per window (S$280-750 range)'),
    'wc':         (300, 'Toilet bowl (S$200-400 range)'),
    'shower':     (350, 'Rain shower set (estimate)'),
    'basin_tap':  (150, 'Basin mixer (estimate)'),
    'sink_tap':   (400, 'Kitchen sink + tap (estimate)'),
    'bath_acc':   (200, 'Bathroom accessories, both bathrooms (estimate)'),
    'rack':       (350, 'Ceiling drying rack (estimate)'),
    'robot':      (600, 'Robot vacuum for the pantry bay (estimate)'),
    'art':        (150, 'Wall art (estimate)'),
}


def L(it):
    """Length of an item along its longer side, ft."""
    return max(it['x1'] - it['x0'], it['y1'] - it['y0']) / FT


def estimate(key):
    its, mod = quantities.items('plan_' + key)
    down, cove, led = quantities.extras()
    names = [n for n, _ in quantities.names('plan_' + key)]
    hide = set(list(getattr(mod, 'MODES', {}).values())[0]['hide']) if getattr(mod, 'MODES', None) else set()
    layers = dict(quantities.names('plan_' + key))
    shown = [n for n in names if layers.get(n) not in hide]
    by = {i['name']: i for i in its if i['layer'] not in hide}
    has = lambda n: n in shown
    reno, furn = [], []

    def add(cat, item, rate, qty=1, note=''):
        r, unit, src = R[rate]
        reno.append({'cat': cat, 'item': item, 'qty': round(qty, 1), 'unit': unit, 'rate': r, 'amount': int(r * round(qty, 1) + 0.5), 'source': src, 'note': note})

    def buy(cat, item, k, qty=1, note=''):
        p, src = F[k]
        if qty: furn.append({'cat': cat, 'item': item, 'qty': qty, 'price': p, 'amount': p * qty, 'source': src, 'note': note})

    # ---- preliminaries & tiling (Lakeside scope)
    add('Preliminaries', 'Haulage and clearing of debris', 'haulage')
    add('Preliminaries', 'General cleaning (end of works)', 'cleaning')
    add('Tiling & masonry', '60 x 60 polished homogeneous floor tiles, skirting, resin grout – living, dining, 3 bedrooms (and study/hall areas)', 'floor_tiles')
    add('Tiling & masonry', 'Cement plinth for kitchen cabinets', 'plinth')
    add('Tiling & masonry', 'Kerb for washer and dryer', 'kerb_washer')
    add('Tiling & masonry', 'Remove existing yard door/window, make good', 'remove_yard')
    add('Tiling & masonry', 'Brick partition with alcove at common bathroom', 'cb_wall')
    add('Tiling & masonry', 'Overlay master bathroom floor', 'mb_overlay')
    open_k = has('KitchenOpen_Counter_facing_Dining_Fluted_Walnut_Back')
    if open_k:
        add('Tiling & masonry', 'Remove kitchen front wall for the open kitchen (needs HDB approval)', 'hack_wall')

    # ---- carpentry: bedrooms
    mw = L(by['Master_Wardrobe']) + L(by['Master_Tall_Cabinet'])
    add('Carpentry – bedrooms', 'Master wardrobe + tall cabinet, full height', 'wardrobe', mw)
    add('Carpentry – bedrooms', 'Bedroom 2 wardrobe, full height', 'wardrobe', L(by['Bedroom2_Wardrobe']))
    b3 = by['Bedroom3_L_Wardrobe']; b3l = ((b3['x1'] - b3['x0']) + (b3['y1'] - b3['y0']) - 600) / FT
    add('Carpentry – bedrooms', 'Bedroom 3 L-shaped wardrobe, full height', 'wardrobe', b3l)
    add('Carpentry – bedrooms', 'L-shape corner surcharge (bedroom 3)', 'l_surcharge')
    add('Carpentry – bedrooms', 'Bedroom 3 bedside nook, half height', 'half', L(by['Bedroom3_Bedside_Nook_Open_to_Room']))
    if 'Maid_Room_Wardrobe' in by: add('Carpentry – bedrooms', 'Maid room wardrobe, full height', 'wardrobe', L(by['Maid_Room_Wardrobe']))

    # ---- carpentry: foyer, shelter, living
    add('Carpentry – foyer & shelter', 'Shoe cabinet with niche + curved shoe bench and top cabinet', 'tall', L(by['Foyer_Shoe_Cabinet_with_Grab_and_Go_Niche']) + L(by['Foyer_Shoe_Bench_Curved']))
    add('Carpentry – foyer & shelter', 'DB box door in matching laminate', 'db_door')
    add('Carpentry – foyer & shelter', 'Shelter feature wall: concealed jib panel + cabinet run with display', 'hs_feature')
    add('Carpentry – foyer & shelter', 'Full-length mirror on the shelter jib panel', 'mirror')
    add('Carpentry – foyer & shelter', 'Freestanding cabinets inside the shelter (not fixed)', 'tall', L(by['Shelter_Freestanding_Cabinets_not_fixed_to_walls']))
    tvw = [n for n in by if n.startswith('TV_Feature_Wall')]
    if tvw:
        add('Carpentry – living', 'TV feature wall with console (%s)' % tvw[0].replace('TV_Feature_Wall_', '').replace('_', ' ').lower(), 'tv_feature', L(by[tvw[0]]))
        add('Carpentry – living', 'Marble-look tile on TV feature wall', 'tile_feature')
    if has('Living_Corner_TV_Wall_with_Storage_Behind'):
        add('Carpentry – living', 'Angled corner TV wall with console', 'tv_feature', 8.5)
        add('Carpentry – living', 'Full-height storage behind the angled TV wall', 'tall', 8.5)
        add('Carpentry – living', 'Marble-look tile on TV feature wall', 'tile_feature')
    for n, label in (('Joinery_Living_Tall_Cabinets_with_Corner_Niche', 'Living tall cabinets with corner niche'),
                     ('Joinery_TV_Wall_Tall_Cabinet_and_Display_Bay', 'Tall cabinet and display bay beside the TV'),
                     ('Living_Tall_Storage_Cabinet', 'Living tall storage cabinet'),
                     ('Study_Full_Height_Cabinet_Sliding_Doors', 'Study full-height cabinet')):
        if n in by: add('Carpentry – living', label, 'tall', L(by[n]))
    if 'Lounge_Feature_Wall_Backlit_Onyx_with_Fluted_Walnut' in by:
        add('Carpentry – living', 'Lounge feature wall, fluted walnut (backlit onyx panel extra)', 'fluted', L(by['Lounge_Feature_Wall_Backlit_Onyx_with_Fluted_Walnut']), 'Onyx slab not in either quote')

    # ---- study fit-out (wall cabinets over the desks)
    for n in ('Study_Two_Standing_Desks_on_West_Wall', 'Study_Nook_Wall_Cabinets_and_Shelf'):
        if n in by: add('Carpentry – study', 'Wall cabinets over the desks', 'top', L(by[n]))

    # ---- dining / pantry
    add('Carpentry – dining', 'Dry pantry: half-height cabinet with top (1.7 m)', 'half', 5.6)
    add('Carpentry – dining', 'Pantry mirror with frame', 'mirror')

    # ---- kitchen & yard
    base = L(by['Kitchen_Base_Hob_Oven_Sink_Dishwasher']); upper = L(by['Kitchen_Wall_Cabinets_Stove_Side_KEPT'])
    add('Kitchen & yard', 'Hob/sink wall: top + bottom cabinets', 'kitchen_tb', base)
    add('Kitchen & yard', 'Extra wall cabinets over the fridge', 'top', max(0, upper - base))
    add('Kitchen & yard', 'Sintered stone top + backsplash, hob/sink wall', 'sint_tb', base)
    if open_k:
        add('Kitchen & yard', 'Counter facing dining, half height', 'half', L(by['KitchenOpen_Counter_facing_Dining_Fluted_Walnut_Back']))
        add('Kitchen & yard', 'Sintered stone top for the counter', 'sint_top', L(by['KitchenOpen_Counter_facing_Dining_Fluted_Walnut_Back']))
        add('Kitchen & yard', 'Fluted laminate back panel on the counter', 'backing')
        tu = by['KitchenOpen_Tall_Units_at_Yard_End_Larder_Microwave']; add('Kitchen & yard', 'Tall units at the yard end (larder, microwave)', 'tall', (tu['x1'] - tu['x0']) / FT)
    else:
        dw = L(by['Kitchen_Base_Drawers_Dining_Wall'])
        add('Kitchen & yard', 'Dining-wall top + bottom cabinets', 'kitchen_tb', dw)
        add('Kitchen & yard', 'Sintered stone top + backsplash, dining wall', 'sint_tb', dw)
        add('Kitchen & yard', 'Tall larder with microwave', 'tall', L(by['Kitchen_Tall_Larder_Dry_Goods_with_Microwave_and_Door_Pocket']))
    add('Kitchen & yard', 'Yard: top + bottom cabinet', 'kitchen_tb', 2.3)
    add('Kitchen & yard', 'Yard: top cabinet over gas heater', 'top', 2.1)
    add('Kitchen & yard', 'Yard: sintered stone tops', 'sint_top', 4.4)
    add('Kitchen & yard', 'Box up yard pipes', 'pipe_box')

    # ---- bathrooms
    cv = L(by['Common_Bath_Vanity_3_Mirror_Cabinets_with_Display_Ledge']); ev = L(by['Ensuite_Vanity_5_Mirror_Cabinets_with_Display_Ledge'])
    add('Bathrooms', 'Common bath vanity with integrated basin', 'vanity', cv)
    add('Bathrooms', 'Common bath mirror cabinets', 'mirror_cab', cv)
    add('Bathrooms', 'Ensuite vanity with integrated basin', 'vanity', ev)
    add('Bathrooms', 'Ensuite mirror cabinets', 'mirror_cab', ev)
    add('Bathrooms', 'Tempered glass shower screen, master bathroom', 'shower_screen')

    # ---- partitions & glass
    for n, label in (('Study_Partition_Walls', 'Study partition walls'), ('Study_TV_Partition_Half_Wall_and_Framed_Glass', 'Study partition (half wall + glass)'),
                     ('Study_East_Wall_Flush_with_Shelter', 'Study wall flush with shelter'), ('Study_North_Half_Glass_Wall_Framed', 'Study half-glass wall'),
                     ('West_Rooms_East_Wall_Window_to_Shelter', 'New wall from window to shelter'), ('Maid_Room_and_Study_Dividing_Wall', 'Maid room / study dividing wall')):
        if n in by:
            it = by[n]; ln = ((it['x1'] - it['x0']) + (it['y1'] - it['y0'])) / FT if 'Partition_Walls' in n or 'Half_Wall' in n else L(it)
            add('Partitions & glass', label, 'partition', ln)
    if 'Study_TV_Partition_Half_Wall_and_Framed_Glass' in by: add('Partitions & glass', 'Framed glass panels on the study half wall', 'fixed_glass', 2)
    if 'Study_North_Half_Glass_Wall_Framed' in by: add('Partitions & glass', 'Framed glass panels on the study half wall', 'fixed_glass', 2)
    if 'Entry_Glass_Partition_Flush_with_Shelter_Wall' in by: add('Partitions & glass', 'Entrance partition with glass', 'fixed_glass', 1)

    # ---- doors & windows
    add('Doors & windows', 'Bedroom doors (master, bedroom 2, bedroom 3)', 'bedroom_door', 3)
    if has('Maid_Room_Concealed_Door_Fluted_Walnut'): add('Doors & windows', 'Maid room door (concealed in fluted wall)', 'bedroom_door', 1)
    add('Doors & windows', 'Bathroom doors', 'toilet_door', 2)
    add('Doors & windows', 'Kitchen bi-fold glass (open kitchen)' if open_k else 'Kitchen sliding pocket door (closed kitchen)', 'kitchen_bifold' if open_k else 'kitchen_slide')
    sd = 2 if 'Study_Sliding_Doors_Fluted_Glass' in by else 1 if 'Study_Sliding_Door_Fluted_Glass' in by else 0
    if sd: add('Doors & windows', 'Study sliding door, fluted glass', 'glass_slide', sd)
    add('Doors & windows', 'Sliding door to yard (no bottom track)', 'yard_door')
    add('Doors & windows', 'Fixed glass beside the yard door', 'yard_glass')
    add('Doors & windows', 'Yard sliding window', 'yard_window')

    # ---- ceilings, lighting, electrical, aircon, plumbing, painting
    zones = len([n for n in shown if layers.get(n) == 'False_Ceiling'])
    add('Ceilings & lighting', 'False ceiling zones with curtain pelmets (%d zones)' % zones, 'fceil', zones, 'Curved cove designs may cost more')
    nd = sum(down.values()); add('Ceilings & lighting', 'Downlight housings', 'downlight', nd)
    cm = sum(cove.values()) / 1000; lm = sum(v for k, v in led.items()) / 1000
    add('Ceilings & lighting', 'LED strips: coves and carpentry (%.0f m + %.0f m)' % (cm, lm), 'led', cm + lm)
    add('Ceilings & lighting', 'LED drivers', 'driver', cm + lm)
    add('Ceilings & lighting', 'Aluminium profiles for carpentry LED strips', 'profile', lm)
    add('Electrical & plumbing', 'Electrical additions & alterations incl. fitting installation', 'electrical')
    add('Electrical & plumbing', 'Install sanitary fittings, taps, sink, washer', 'plumbing')
    fcu = len([n for n in shown if layers.get(n) in ('Aircon', 'Fixtures') and ('Aircon' in n)])
    add('Air-conditioning', 'Mitsubishi Starmex system, 5 fan coils', 'aircon5')
    if fcu > 5: add('Air-conditioning', 'Extra fan coils (%d units in total)' % fcu, 'aircon_extra', fcu - 5)
    add('Painting', 'Whole-house painting', 'painting')

    # ---- optional extras (not in the Lakeside scope; listed, not in the total)
    opt = []
    for k, label in (('grille_living', 'Invisible grille, living'), ('grille_beds', 'Invisible grilles, 3 bedrooms'), ('wifi', 'Wi-Fi access points + set-up'), ('fridge_kerb', 'Kerb for fridge')):
        r, unit, src = R[k]; opt.append({'cat': 'Optional', 'item': label, 'qty': 1, 'unit': unit, 'rate': r, 'amount': r, 'source': src, 'note': ''})

    # ---------------------------------------------------------------- furniture & appliances
    buy('Appliances', 'Washing machine', 'washer'); buy('Appliances', 'Dryer', 'dryer')
    if has('Washer_and_Dryer_Stacked'): buy('Appliances', 'Stacking kit', 'stack_kit')
    buy('Appliances', 'Fridge', 'fridge'); buy('Appliances', 'Induction hob', 'hob'); buy('Appliances', 'Cooker hood', 'hood')
    buy('Appliances', 'Built-in oven', 'oven'); buy('Appliances', 'Dishwasher', 'dishwasher'); buy('Appliances', 'Microwave', 'microwave')
    buy('Appliances', 'Gas water heater (installed)', 'heater'); buy('Appliances', '75-inch TV', 'tv75')
    if has('Dry_Pantry_on_Toilet_Wall_Cabinet_Mirror_Robot_Bay'): buy('Appliances', 'Robot vacuum', 'robot')
    sofas = {'Living_L_Sofa_Boucle_with_Chaise': 'sofa_l', 'Living_L_Sofa_West_Side_Facing_TV': 'sofa_l', 'Living_L_Sofa_on_Bedroom_Wall_Chaise_to_Dining': 'sofa_l',
             'Living_Loveseat_by_Window': 'sofa_2', 'Living_2_Seater_Sofa_by_Window': 'sofa_2', 'Living_3_Seater_Sofa_along_Wall': 'sofa_3',
             'Lounge_Sofa_outside_Study': 'sofa_3', 'Living_West_Sofa_Facing_East': 'sofa_2', 'Living_East_Long_Sofa_Facing_West': 'sofa_3'}
    for n, k in sofas.items():
        if has(n): buy('Living & dining', n.replace('Living_', '').replace('Lounge_', 'Lounge ').replace('_', ' '), k)
    if has('Living_Window_Seats_x3_Modular'): buy('Living & dining', 'Window seat modules', 'sofa_mod', 3)
    if any(has(n) for n in ('Living_Coffee_Table_Travertine_Pebble', 'Living_Round_Coffee_Table_Travertine', 'Living_Round_Coffee_Table_Travertine_Fluted')): buy('Living & dining', 'Coffee table', 'coffee')
    if has('Lounge_Side_Table_Sculpture'): buy('Living & dining', 'Lounge side table', 'side_table')
    buy('Living & dining', 'Dining table', 'dining_tbl')
    buy('Living & dining', 'Dining chairs', 'dining_ch', 7 if key == 'a' else 8)
    if open_k: buy('Living & dining', 'Counter stools', 'stool', 3)
    buy('Bedrooms', 'King bed frame (master)', 'king_bed'); buy('Bedrooms', 'King mattress', 'king_mat')
    buy('Bedrooms', 'Bedside tables (master)', 'bedside', 2)
    q3 = has('Bedroom3_Queen_Bed') or has('OptA_Bedroom3_Queen_Bed')
    if q3: buy('Bedrooms', 'Queen bed frame (bedroom 3)', 'queen_bed'); buy('Bedrooms', 'Queen mattress', 'queen_mat')
    buy('Bedrooms', 'Super-single floor bed (bedroom 2)', 'ss_bed'); buy('Bedrooms', 'Super-single mattress', 'ss_mat')
    if has('Maid_Room_Single_Bed'): buy('Bedrooms', 'Single bed frame (maid room)', 'single_bed'); buy('Bedrooms', 'Single mattress (maid room)', 'single_mat')
    buy('Bedrooms', 'Helper tri-fold mattress (shelter)', 'trifold')
    desks = 2 if any(has(n) for n in ('Study_Two_Standing_Desks_on_West_Wall', 'Bedroom3_Study_Two_Standing_Desks_Facing_Window', 'Study_Nook_Two_Standing_Desks_on_West_Wall', 'OptA_Study_Two_Standing_Desks')) else 0
    buy('Study', 'Electric standing desks', 'desk', desks); buy('Study', 'Ergonomic chairs', 'chair', desks); buy('Study', '27-inch 4K monitors', 'monitor', desks)
    fans = len([n for n in shown if n.startswith('Ceiling_Fan')])
    buy('Lighting & fans', 'Ceiling fans with light', 'fan', fans); buy('Lighting & fans', 'Bladeless tower fan (dining)', 'fan_less')
    buy('Lighting & fans', 'Dining pendant', 'pendant')
    if has('Lounge_Sculptural_Pendant_Cluster'): buy('Lighting & fans', 'Lounge pendant cluster', 'pend_clust')
    buy('Lighting & fans', 'Floor lamps', 'floor_lamp', len([n for n in shown if n.endswith('Floor_Lamp')]))
    buy('Lighting & fans', 'Bedside wall sconces', 'sconce', 2)
    if has('Study_Ceiling_Light'): buy('Lighting & fans', 'Study ceiling light', 'ceil_light')
    buy('Soft furnishing & decor', 'Day + night curtains', 'curtain', len([n for n in shown if n.startswith('Curtains_')]))
    buy('Soft furnishing & decor', 'Wall art', 'art', 4)
    buy('Sanitary & fittings', 'Toilet bowl (master bathroom)', 'wc'); buy('Sanitary & fittings', 'Rain shower sets', 'shower', 2)
    buy('Sanitary & fittings', 'Basin mixers', 'basin_tap', 2); buy('Sanitary & fittings', 'Kitchen sink and tap', 'sink_tap')
    buy('Sanitary & fittings', 'Bathroom accessories', 'bath_acc'); buy('Sanitary & fittings', 'Ceiling drying rack', 'rack')

    tot = lambda rows: sum(r['amount'] for r in rows)
    return {'reno': reno, 'optional': opt, 'furn': furn, 'reno_total': tot(reno), 'optional_total': tot(opt), 'furn_total': tot(furn)}


if __name__ == '__main__':
    out = {'generated': 'Nov 2026', 'rates': {k: {'rate': v[0], 'unit': v[1], 'source': v[2]} for k, v in R.items()},
           'prices': {k: {'price': v[0], 'source': v[1]} for k, v in F.items()}, 'plans': {}}
    for k in 'abcdefg':
        out['plans'][k] = estimate(k)
        p = out['plans'][k]
        print(k, 'reno', p['reno_total'], 'optional', p['optional_total'], 'furniture', p['furn_total'], 'total', p['reno_total'] + p['furn_total'])
    out['summary'] = {k: {'reno': p['reno_total'], 'items': p['furn_total'], 'appliances': sum(l['amount'] for l in p['furn'] if l['cat'] == 'Appliances'), 'furniture': sum(l['amount'] for l in p['furn'] if l['cat'] != 'Appliances'), 'total': p['reno_total'] + p['furn_total'], 'optional': p['optional_total']} for k, p in out['plans'].items()}
    json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', 'costs.json'), 'w'), indent=1)
