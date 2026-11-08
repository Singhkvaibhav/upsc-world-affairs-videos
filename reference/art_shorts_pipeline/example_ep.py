from engine.art import *
EP = 4; TITLE = "Three_Temple_Styles"; NAME = "Three temple styles"
SPEC = dict(
    unfold=dict(motifs=['temple_nagara', 'temple_dravida'], q='Why?'),
    look=[dict(kind='anatomy', motif='temple_nagara', labels=[('garbhagriha', 'sanctum'), ('mandapa', 'mandapa'), ('tower', 'tower')]),
          dict(kind='anatomy', motif='temple_nagara', labels=[('shikhara', 'shikhara'), ('amalaka', 'amalaka'), ('kalasha', 'kalasha'), ('raised platform', 'platform')]),
          dict(kind='anatomy', motif='temple_dravida', labels=[('vimana', 'vimana'), ('shikhara', 'shikhara'), ('gopuram', 'gopuram'), ('water tank', 'tank'), ('high wall', 'wall')]),
          dict(kind='print', motifs=['temple_vesara', 'three_towers'], captions=['Vesara · star platform', 'Pattadakal: side by side'], cues=['Vesara', 'Pattadakal'])],
    compare=dict(left='Nagara', right='Dravida', lmot='temple_nagara', rmot='temple_dravida',
                 rows=[('Tower shape', 'curves', 'steps'), ('Tower name', 'shikhara', 'vimana'), ('Gateway', 'rare', 'grand gopurams'), ('Boundary wall', 'usually absent', 'high walls'), ('Crown', 'amalaka + kalasha', 'small domed shikhara')],
                 cues=['The tower:', 'Its name', 'The gateway', 'The boundary wall', 'The crown']),
    where=[('Khajuraho', 24.85, 79.92, 1), ('Konark', 19.89, 86.09, 1), ('Thanjavur', 10.78, 79.13, 1), ('Pattadakal', 15.95, 75.82, 1), ('Belur-Halebidu', 13.17, 75.86, 1)],
    spot=dict(items=[('temple_nagara', 'Nagara'), ('temple_dravida', 'Dravida'), ('temple_vesara', 'Vesara')]),
    short=dict(open=['three_towers']),
)
if not V: BEATS, CAPTIONS, EXTRA, EVENTS = build_long(EP, SPEC)
