# Views shared by every plan (same camera = easy comparison between plans)
HEAD = [
 ('Overview', (-3500, 14500, 15500), (7300, 4800, 0), 40, 'top'),
 ('Plan (annotated)', (7300, 4800, 60000), (7300, 4799, 0), 11.5, 'plan'),
 ('CMP 1 · Living from dining side', (5000, 4300, 1650), (2400, 2300, 900), 80, ''),
 ('CMP 2 · Living from window side', (3300, 1700, 1650), (5400, 3800, 700), 85, ''),
 ('CMP 3 · Hall towards kitchen', (4300, 4100, 1600), (7000, 6000, 700), 80, ''),
 ('CMP 4 · Hall from the foyer', (3000, 8050, 1600), (1500, 5200, 1150), 70, ''),
]
def tail(br3_view=True):
    v = [
     ('Foyer – from main door', (2700, 8000, 1650), (2400, 5000, 900), 88, ''),
     ('Foyer – towards the main door', (2850, 6560, 1600), (2750, 8600, 1000), 82, ''),
     ('Foyer – shoe bench', (2450, 6620, 1550), (3700, 7700, 800), 72, ''),
     ('Foyer – curved bench close-up', (2350, 6450, 1350), (3650, 6950, 520), 72, ''),
     ('Household shelter', (1350, 6800, 1700), (450, 8400, 500), 88, ''),
    ]
    if br3_view: v += [('Bedroom 3 – queen bed and painting', (8350, 3450, 1650), (5850, 1450, 1200), 88, ''),
                       ('Bedroom 3 – towards the door', (6150, 700, 1600), (8100, 3300, 1000), 85, '')]
    v += [
     ('Bedroom 2 – kids floor bed', (9200, 3300, 1600), (11300, 1700, 900), 78, ''),
     ('Bedroom 2 – towards the door', (9800, 650, 1600), (10300, 3500, 900), 85, ''),
     ('Master – bed, painting, wall lights', (11950, 2560, 1550), (14350, 2560, 1450), 85, ''),
     ('Master – organic wave mirror', (13300, 2300, 1500), (11450, 850, 1050), 70, ''),
     ('Master – from the bedside', (14050, 4050, 1600), (11800, 1300, 1000), 85, ''),
     ('Common bathroom', (9100, 5300, 1600), (9350, 6800, 1250), 80, ''),
     ('Ensuite', (12150, 5300, 1650), (10950, 6700, 650), 85, ''),
     ('Service yard', (8300, 8450, 1650), (8900, 7000, 900), 85, ''),
     ('Service yard – towards the kitchen', (9150, 7650, 1500), (7600, 8400, 900), 85, ''),
     ('NIGHT · Living', (5000, 4300, 1650), (1500, 2500, 1000), 85, 'night'),
     ('NIGHT · Master bedroom', (11950, 2560, 1550), (14350, 2560, 1450), 85, 'night'),
     ('SERVICES · Power points + aircon trunking', (-2500, 13500, 13000), (7300, 4800, 0), 40, 'services'),
    ]
    return v
KITCHEN_OPEN_VIEWS = [
 ('OPEN kitchen – glass folded away', (5800, 4300, 1650), (6300, 8500, 900), 80, '', 'open'),
 ('OPEN kitchen – glass closed (cooking)', (5800, 4300, 1650), (6300, 8500, 900), 80, '', 'open_glass'),
 ('OPEN kitchen – counter and tall units', (5300, 7300, 1650), (7700, 7100, 1100), 80, '', 'open'),
 ('OPEN kitchen – stove side top cabinets', (6000, 7550, 1650), (6200, 9300, 1400), 80, '', 'open'),
 ('OPEN kitchen – towards dining and living', (6600, 8550, 1600), (4800, 4600, 1000), 85, '', 'open'),
 ('Kitchen (closed) – inside', (4300, 7150, 1650), (7800, 9250, 800), 88, '', 'closed'),
 ('Kitchen (closed) – towards the door', (7300, 8600, 1600), (4300, 6800, 1000), 85, '', 'closed'),
 ('Kitchen (closed) – door shut', (3000, 5200, 1600), (4600, 6900, 1100), 70, '', 'closed_door'),
]
KMODES = {
    'open': {'label': 'Open kitchen – glass folded away', 'hide': ['Kitchen_Closed', 'Kitchen_Door_Closed', 'Kitchen_Door_Open', 'Kitchen_Glass_Closed']},
    'open_glass': {'label': 'Open kitchen – glass closed', 'hide': ['Kitchen_Closed', 'Kitchen_Door_Closed', 'Kitchen_Door_Open', 'Kitchen_Glass_Open']},
    'closed': {'label': 'Closed kitchen (door open)', 'hide': ['Kitchen_Door_Closed', 'Kitchen_Open', 'Kitchen_Glass_Open', 'Kitchen_Glass_Closed']},
    'closed_door': {'label': 'Closed kitchen (door shut)', 'hide': ['Kitchen_Door_Open', 'Kitchen_Open', 'Kitchen_Glass_Open', 'Kitchen_Glass_Closed']},
}
COMMON_LABELS = [('Kitchen', 5900, 8000), ('Service yard', 8900, 8000), ('Foyer', 2700, 7500), ('Household shelter', 900, 7600),
 ('Bedroom 2 (kids)', 10000, 1800), ('Master bedroom', 12900, 2600), ('Common bath', 9900, 6000), ('Ensuite', 12000, 6000)]
