"""Episode 1 — The Indus Waters Treaty in abeyance (bilingual: English + Hindi)."""
import math, random, cairo
from engine import core
from engine.core import W, H, seg, ease, eoc, eob, lerp, T
from engine.riso import R, rgba, riso, halftone, rrect, txt, inktext, para, camera, pop, fadein, cable, credit, bg_board, bg_sheet, tw
from engine.brief import india_map, map_point, _bg, outro, headline, timeline, stands, stakes, statement, mains, watch, tag, figure, token
from engine.web import passport_stamp, relations_web

EP = 1
TITLE = 'The_Indus_Waters_Treaty_in_Abeyance'
NAME = 'The Indus Waters Treaty in abeyance'
EXTRA = {'hook': .5, 'tip': 1.0, 'end': 2.0}
VOICE_EN = {'length': 0.98, 'noise': (0.72, 0.85), 'gaps': (0.38, 0.22)}   # brighter, more energetic delivery
VOICE_HI = {'length': 0.86, 'noise': (0.72, 0.85), 'gaps': (0.38, 0.22)}
CRF, PRESET = 17, 'medium'                                                # premium encode

# ---------- schematic river board (no boundaries; swapped for the official Survey of India map when supplied) ----------
RIVERS = {   # name: (points, side)
    'Indus':  ([(430, 250), (520, 470), (590, 650), (610, 800), (470, 900), (300, 1010)], 'west'),
    'Jhelum': ([(690, 270), (720, 420), (800, 560), (880, 640)], 'west'),
    'Chenab': ([(920, 255), (930, 430), (900, 600), (790, 720), (640, 800)], 'west'),
    'Ravi':   ([(1090, 275), (1060, 450), (960, 600), (850, 690)], 'east'),
    'Beas':   ([(1250, 285), (1230, 420), (1160, 540)], 'east'),
    'Sutlej': ([(1440, 270), (1340, 440), (1160, 560), (960, 700), (680, 790)], 'east'),
}

def _path(ctx, pts, p=1.):
    n = len(pts) - 1; upto = p*n
    ctx.move_to(*pts[0])
    for i in range(1, n+1):
        if i <= upto: ctx.line_to(*pts[i])
        else:
            f = upto - (i-1)
            if f > 0: ctx.line_to(lerp(pts[i-1][0], pts[i][0], f), lerp(pts[i-1][1], pts[i][1], f))
            break

def river_board(ctx, t, a, grow_from, light, dim=1.):
    """grow_from: time rivers start drawing; light: dict side->highlight progress"""
    # mountains
    def ridge():
        ctx.move_to(250, 330)
        for k in range(26):
            x = 250 + k*55
            ctx.line_to(x+27, 210 + 30*math.sin(k*1.7)); ctx.line_to(x+55, 330)
        ctx.close_path()
    riso(ctx, ridge, R['tealpale'], a*dim)
    halftone(ctx, ridge, R['teal'], .35*a*dim, step=10, r=2.2)
    txt(ctx, 'HIMALAYA', 1590, 300, 22, R['grey'], a*dim, 'bold', mono=True)
    # sea
    def sea():
        ctx.move_to(0, 930); ctx.curve_to(180, 950, 300, 1000, 380, H); ctx.line_to(0, H); ctx.close_path()
    riso(ctx, sea, R['river'], .55*a*dim); halftone(ctx, sea, R['river'], .5*a*dim, step=9, r=2)
    txt(ctx, 'ARABIAN SEA', 40, 1000, 22, R['paper'], a*dim, 'bold', mono=True)
    for i, (name, (pts, side)) in enumerate(RIVERS.items()):
        p = eoc(seg(t, grow_from + i*.25, grow_from + i*.25 + 1.4))
        if p <= 0: continue
        hl = light.get(side, 0)
        ink = R['teal'] if side == 'east' else R['coral']
        col = tuple(lerp(R['river'][j], ink[j], hl) for j in range(3))
        ctx.save(); ctx.set_line_join(cairo.LINE_JOIN_ROUND); ctx.set_line_cap(cairo.LINE_CAP_ROUND)
        ctx.set_line_width(16 if name == 'Indus' else 12); rgba(ctx, col, a*dim)
        _path(ctx, pts, p); ctx.stroke()
        # flowing dashes
        ctx.set_line_width(4); ctx.set_dash([18, 26], -t*70); rgba(ctx, R['paper'], .75*a*dim)
        _path(ctx, pts, p); ctx.stroke(); ctx.restore()
        if p > .3:
            la = ease(seg(t, grow_from + i*.25 + .5, grow_from + i*.25 + .9))*a*dim
            x, y = pts[0]
            tag(ctx, x, y - 30, name.upper(), col, la, 22, align='c')

MAP_H = 860
def s_rivers(ctx, t, D):
    bg_board(ctx); a = outro(t, D)
    # 1) fly in on the official map of India towards the Indus basin
    mp = ease(seg(t, .4, 4.0)); ma = (1 - ease(seg(t, 3.3, 4.3)))*a
    if ma > 0:
        fx, fy = map_point(W/2, 580, MAP_H, 388, 332)
        z = lerp(1, 3.0, mp)
        ctx.save(); ctx.translate(lerp(fx, W/2, mp), lerp(fy, 560, mp)); ctx.scale(z, z); ctx.translate(-fx, -fy)
        india_map(ctx, W/2, 580, MAP_H, ma*fadein(t, 0, .4))
        pq = seg(t, .6, 1.1)
        if pq > 0:
            rgba(ctx, R['coral'], ma*(1-seg(t, .6, 2.2))); ctx.set_line_width(3/z); ctx.arc(fx, fy, (20+80*seg(t, .6, 2.2))/z*1.6, 0, 2*math.pi); ctx.stroke()
            riso(ctx, lambda: ctx.arc(fx, fy, 10*eob(pq, 2)/max(z*.6, 1), 0, 2*math.pi), R['coral'], ma)
        ctx.restore()
        tag(ctx, W/2 + 40, 470, 'INDUS BASIN', R['coral'], ease(seg(t, 1.0, 1.4))*ma, 26)
        txt(ctx, 'MAP: OFFICIAL BOUNDARIES OF INDIA (SURVEY OF INDIA DEPICTION)', W-70, 140, 18, R['grey'], ma, mono=True, align='r')
    cable(ctx, t, 'WHAT IS HAPPENING · SIX RIVERS', a, EP)
    ba = ease(seg(t, 3.5, 4.5))*a
    if ba <= 0: return
    a = ba
    ctx.save(); camera(ctx, t, D, (1.0, 1.05), cy=600)
    le = ease(seg(t, T('The three eastern rivers'), T('The three eastern rivers') + .8))
    lw = ease(seg(t, T('The three western ones'), T('The three western ones') + .8))
    river_board(ctx, t, a, 4.0, {'east': le, 'west': lw})
    q = pop(t, T('The three eastern rivers') + .6)
    if q > 0: tag(ctx, 1370, 640, 'EASTERN RIVERS → INDIA', R['teal'], ease(seg(t, T('The three eastern rivers')+.6, T('The three eastern rivers')+1))*a, 30)
    q2 = seg(t, T('The three western ones') + .6, T('The three western ones') + 1)
    if q2 > 0: tag(ctx, 100, 560, 'WESTERN RIVERS → PAKISTAN', R['coral'], ease(q2)*a, 30)
    q3 = seg(t, T('in limited ways'), T('in limited ways') + .5)
    if q3 > 0: tag(ctx, 100, 640, 'INDIA: LIMITED USE, E.G. RUN-OF-RIVER HYDROPOWER', R['char'], ease(q3)*a, 20)
    ctx.restore()
    credit(ctx, 'SCHEMATIC RIVERS · NOT TO SCALE', a)
s_rivers.bg = 'board'

def s_ladder(ctx, t, D):
    bg_board(ctx); a = outro(t, D)
    cable(ctx, t, 'HOW DISPUTES ARE SETTLED', a, EP)
    river_board(ctx, 100, a, 0, {'east': 1, 'west': 1}, dim=.25)
    steps = [('PERMANENT INDUS COMMISSION', 'one commissioner from each country', 'Permanent Indus Commission'),
             ('NEUTRAL EXPERT', 'for technical differences', 'Step two'),
             ('COURT OF ARBITRATION', 'for legal disputes', 'Step three')]
    ctx.save(); camera(ctx, t, D, (1.0, 1.04))
    for i, (head, sub, cue) in enumerate(steps):
        t0 = T(cue); q = seg(t, t0, t0 + .6)
        if q <= 0: continue
        x = 300 + i*440; y = 720 - i*170 + 80*(1 - eob(q, 1.5)); aa = ease(q*1.6)*a
        ink = [R['teal'], R['over'], R['coral']][i]
        riso(ctx, lambda: rrect(ctx, x, y, 560, 150, 14), ink, aa, second=R['coral'] if i == 0 else None, settle=eoc(q))
        txt(ctx, f'STEP {i+1}', x+30, y+44, 22, R['paper'], aa, 'bold', mono=True)
        txt(ctx, head, x+30, y+92, 32, R['paper'], aa, 'black')
        txt(ctx, sub, x+30, y+130, 22, R['paper'], aa*.9)
        if i == 0:
            figure(ctx, x+440, y-10, .55, R['teal'], aa, t, seed=1); figure(ctx, x+510, y-10, .55, R['coral'], aa, t, seed=2)
    ctx.restore()
s_ladder.bg = 'board'

# ---------- Chenab close-up: flushing, projects, the award ----------
CHENAB = [(-50, 520), (300, 470), (700, 560), (1100, 500), (1500, 590), (1980, 540)]

def chenab(ctx, t, a, dim=1.):
    ctx.save(); ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.set_line_join(cairo.LINE_JOIN_ROUND)
    ctx.set_line_width(70); rgba(ctx, R['river'], a*dim); _path(ctx, CHENAB); ctx.stroke()
    ctx.set_line_width(6); ctx.set_dash([30, 40], -t*90); rgba(ctx, R['paper'], .7*a*dim); _path(ctx, CHENAB); ctx.stroke()
    ctx.restore()
    txt(ctx, 'CHENAB  →  flows downstream', 1080, 440, 26, R['river'], a*dim, 'bold', mono=True)

def dam(ctx, x, y, a, t, flushing, name):
    riso(ctx, lambda: rrect(ctx, x-18, y-90, 36, 180, 6), R['char'], a)
    if flushing > 0:
        rr = random.Random(int(x))
        for k in range(30):
            ph = (t*0.9 + rr.random()) % 1
            px = x + 20 + ph*300; py = y + rr.uniform(-25, 25) + 8*math.sin(ph*9)
            rgba(ctx, (0.55, 0.42, 0.3), .6*a*flushing*(1-ph)); ctx.arc(px, py, rr.uniform(3, 7), 0, 2*math.pi); ctx.fill()
    tag(ctx, x, y + 140, name, R['char'], a, 20, align='c')

def s_since(ctx, t, D):
    bg_board(ctx); a = outro(t, D)
    cable(ctx, t, 'SINCE APRIL 2025', a, EP)
    ctx.save(); camera(ctx, t, D, (1.0, 1.06), pan=(-40, 0))
    chenab(ctx, t, a)
    fl = ease(seg(t, T('flushed sediment'), T('flushed sediment') + .6))
    dam(ctx, 620, 545, a*fadein(t, .3), t, fl, 'DAM ON THE CHENAB'); dam(ctx, 1050, 505, a*fadein(t, .5), t, fl, 'DAM ON THE CHENAB')
    if fl > 0: tag(ctx, 820, 330, 'SEDIMENT FLUSHING', R['over'], fl*a, 26, align='c')
    for i, (nm, x, y) in enumerate((('PAKAL DUL', 1380, 380), ('RATLE', 1650, 700))):
        cue = T('Pakal Dul') if i == 0 else T('Ratle')
        q = seg(t, cue, cue + .6)
        if q <= 0: continue
        r = 24*eob(q, 2)
        riso(ctx, lambda: ctx.arc(x, y, r, 0, 2*math.pi), R['teal'], a, second=R['coral'])
        # ripple
        rgba(ctx, R['teal'], (1-seg(t, cue, cue+1.2))*a); ctx.set_line_width(3); ctx.arc(x, y, 24 + 60*seg(t, cue, cue+1.2), 0, 2*math.pi); ctx.stroke()
        tag(ctx, x, y - 60, nm + ' · HYDROPOWER', R['teal'], ease(q)*a, 24, align='c')
    ctx.restore()
    credit(ctx, 'SCHEMATIC · NOT TO SCALE', a)
s_since.bg = 'board'

def s_award(ctx, t, D):
    bg_board(ctx); a = outro(t, D)
    cable(ctx, t, 'COURT OF ARBITRATION · 31 AUG 2026', a, EP)
    ctx.save(); camera(ctx, t, D, (1.04, 1.0))
    chenab(ctx, t, a, dim=.35)
    # Ratle pin with sticker
    x, y = 1650, 700
    riso(ctx, lambda: ctx.arc(x, y, 24, 0, 2*math.pi), R['teal'], a*.6)
    tag(ctx, x, y - 60, 'RATLE', R['teal'], a*.6, 24, align='c')
    cq = seg(t, T('limited some construction'), T('limited some construction') + .5)
    if cq > 0:
        ctx.save(); ctx.translate(x, y + 70); ctx.rotate(-.08); ctx.scale(eob(cq, 2), eob(cq, 2))
        tag(ctx, 0, 0, 'SOME WORK LIMITED FOR NOW', R['coral'], a, 22, align='c'); ctx.restore()
    # tribunal assembles
    bx, by = 560, 760; p = seg(t, .4, 2.2)
    riso(ctx, lambda: rrect(ctx, bx-260, by, 520, 30, 4), R['char'], a*ease(seg(p, 0, .2)))
    for k in range(5):
        h = 260*eob(seg(p, .15 + k*.08, .45 + k*.08))
        riso(ctx, lambda: rrect(ctx, bx-220 + k*100, by-h, 44, h, 4), R['teal'], a, seed=k)
    rp = eob(seg(p, .6, .9))
    if rp > 0:
        riso(ctx, lambda: (ctx.move_to(bx-280, by-260-40*(1-rp)), ctx.line_to(bx+280, by-260-40*(1-rp)), ctx.line_to(bx, by-380-40*(1-rp)), ctx.close_path()), R['coral'], a*rp, second=R['teal'])
    tq = seg(t, T('issued an interim award'), T('issued an interim award') + .5)
    if tq > 0: tag(ctx, bx, by + 90, 'INTERIM AWARD · 31 AUG 2026', R['char'], ease(tq)*a, 26, align='c')
    lq = seg(t, T("Its message"), T("Its message") + .6)
    if lq > 0:
        riso(ctx, lambda: rrect(ctx, 960, 180, 840, 200, 14), R['paper'], ease(lq)*a)
        rgba(ctx, R['char'], ease(lq)*a); ctx.set_line_width(3); rrect(ctx, 960, 180, 840, 200, 14); ctx.stroke()
        txt(ctx, 'THE AWARD SAID', 990, 228, 22, R['coral'], ease(lq)*a, 'bold', mono=True)
        para(ctx, "India's grounds were not enough to suspend the treaty", 990, 285, 36, R['char'], 780, ease(lq)*a, weight='bold')
    ctx.restore()
s_award.bg = 'board'

def _motif_hook(ctx, t, D, a):
    # the treaty: a paper sheet from 1960 with six river ribbons, and a coral PAUSE stamped on it
    q = eob(seg(t, .5, 1.3), 1.3)
    if q <= 0: return
    ctx.save(); ctx.translate(1400, 560 + 80*(1-q)); ctx.rotate(.06 + .01*math.sin(t*.7))
    riso(ctx, lambda: rrect(ctx, -270, -340, 540, 660, 10), R['paper'], a)
    rgba(ctx, R['char'], .8*a); ctx.set_line_width(3); rrect(ctx, -270, -340, 540, 660, 10); ctx.stroke()
    txt(ctx, 'INDUS WATERS TREATY', -230, -280, 26, R['teal'], a, 'bold', mono=True)
    txt(ctx, 'KARACHI · 19 SEPTEMBER 1960', -230, -246, 18, R['grey'], a, mono=True)
    for k in range(6):
        ink = R['coral'] if k < 3 else R['teal']
        ctx.save(); ctx.set_line_width(9); ctx.set_line_cap(cairo.LINE_CAP_ROUND); rgba(ctx, ink, .85*a)
        x = -180 + k*72; ctx.move_to(x, -190)
        ctx.curve_to(x + 30*math.sin(t + k), -60, x - 30*math.sin(t*.8 + k), 60, x + 10, 200); ctx.stroke(); ctx.restore()
    p = seg(t, 2.2, 2.55)
    if p > 0:
        s = lerp(1.8, 1, eoc(p)); aa = ease(p*2)*a
        ctx.save(); ctx.translate(40, 20); ctx.rotate(-.12); ctx.scale(s, s)
        riso(ctx, lambda: ctx.arc(0, 0, 150, 0, 2*math.pi), R['coral'], .9*aa)
        riso(ctx, lambda: (rrect(ctx, -55, -70, 38, 140, 6), rrect(ctx, 17, -70, 38, 140, 6)), R['paper'], aa)
        ctx.restore()
        txt(ctx, 'IN ABEYANCE', 40, 240, 34, R['coral'], aa, 'black', 'c')
    ctx.restore()

# ---------- beats ----------
_TL = [('1951', 'Talks begin, with the World Bank as broker', R['teal'], 'nine long years', 300),
       ('1960', 'Signed in Karachi: Nehru and Ayub Khan', R['coral'], 'signed the treaty in Karachi', 860),
       ('1965', 'War: the treaty survives', R['teal'], 99, 1420), ('1971', 'War: the treaty survives', R['teal'], 99, 1980),
       ('1999', 'Kargil: the treaty survives', R['teal'], 99, 2540), ('2025', 'After Pahalgam: held in abeyance', R['coral'], 99, 3100),
       ('2026', 'Court of Arbitration award', R['char'], 99, 3660)]
_TL2 = [(y, c, i, (-5 if y in ('1951', '1960') else {'1965': 'wars of 1965', '1971': 'and 1971', '1999': 'Kargil', '2025': 'in April 2025'}.get(y, 99)), x) for y, c, i, _, x in _TL]
_STANDS = [('INDIA SAYS', ['In abeyance until Pakistan credibly and irrevocably abjures its support for cross-border terrorism', 'The court was set up in breach of the treaty; it has no jurisdiction', 'India has never appeared before it'], R['teal']),
           ('PAKISTAN SAYS', ['The treaty remains fully in force and binding', 'India must comply with the treaty and its dispute decisions'], R['coral'])]

BEATS = [
 ('hook', "On the twenty-third of April 2025, India put the 1960 Indus Waters Treaty on hold. Then, on the thirty-first of August 2026, a Court of Arbitration said India's reasons were not enough to suspend it. India's answer? Rejected, the very same day. So why does this treaty matter so much for India? Let's find out.",
  headline([('A TREATY', R['teal']), ('ON HOLD', R['coral'])], 'INDUS WATERS TREATY · 1960',
           question=('Why does it matter for India?', 'So why does this treaty'), motif=_motif_hook)),
 ('back1', "Rewind to 1960. After nine long years of talks, brokered by the World Bank, Prime Minister Jawaharlal Nehru and Pakistan's President Ayub Khan signed the treaty in Karachi, that September.",
  timeline(_TL, (700, 1000))),
 ('back2', "And here's what makes it remarkable. It survived the wars of 1965 and 1971. It survived Kargil in 1999. But in April 2025, after a terror attack in Pahalgam killed twenty-six people, India took a step it had never taken before: it announced the treaty would be held in abeyance.",
  timeline(_TL2, (1000, 3000))),
 ('rivers', "So what does the treaty actually do? It splits six rivers. The three eastern rivers, the Ravi, the Beas and the Sutlej, are India's to use without limits. The three western ones, the Indus, the Jhelum and the Chenab, go to Pakistan. India can still use them, but only in limited ways, like run-of-the-river hydropower.", s_rivers),
 ('ladder', "It also built a system to settle disputes. Step one: the Permanent Indus Commission, with one commissioner from each country. Step two: a Neutral Expert. Step three: a Court of Arbitration.", s_ladder),
 ('since', "So, what has India done since? From April 2025, it has flushed sediment from its dams on the Chenab, and put hydropower projects like Pakal Dul and Ratle on the fast track.", s_since),
 ('award', "Then came the twist. On the thirty-first of August 2026, the Court of Arbitration issued an interim award. Its message: India's grounds were not enough to suspend the treaty. And for now, it limited some construction at Ratle.", s_award),
 ('india', "So, who says what? India's position is firm: the treaty stays in abeyance until Pakistan credibly and irrevocably abjures its support for cross-border terrorism. India says this court was set up in breach of the treaty, has no jurisdiction, and India has never appeared before it.",
  stands(_STANDS, ["India's position", 999])),
 ('pak', "Pakistan sees it the other way. It says the award shows the treaty is fully in force and binding, and that India must comply.",
  stands(_STANDS, [-5, 'Pakistan sees'])),
 ('stakes', "Now, why should you care? Because three big things are at stake for India. One: security. India ties this treaty directly to cross-border terrorism. Two: energy. Fuller use of the western rivers means more hydropower for Jammu and Kashmir. And three: precedent. On the Brahmaputra, India is the downstream country, below China. So how river treaties are read matters to India too.",
  stakes([('shield', 'SECURITY', 'Tied to cross-border terrorism', R['teal'], 'One: security'),
          ('turbine', 'ENERGY', 'More hydropower for Jammu and Kashmir', R['coral'], 'Two: energy'),
          ('rivers', 'PRECEDENT', 'Downstream of China on the Brahmaputra', R['over'], 'And three: precedent')])),
 ('tip', "Okay, memory time! Here's your passport stamp. East is R-B-S: Ravi, Beas, Sutlej, for India. West is I-J-C: Indus, Jhelum, Chenab, for Pakistan. And the year? Nineteen sixty, with the World Bank as broker.",
  passport_stamp(['EAST  RBS → INDIA', 'WEST  IJC → PAKISTAN', '1960 · WORLD BANK'], EP, 'East is', ['East is', 'West is', 'And the year'], 'INDUS WATERS')),
 ('q1', "Exam desk! True or false: the treaty gives India unrestricted use of the Chenab. Think about it. False! The Chenab is a western river. India's unrestricted rights are on the Ravi, Beas and Sutlej.",
  statement(1, 'The Indus Waters Treaty gives India unrestricted use of the Chenab.', 'FALSE', "The Chenab is a western river. India's unrestricted rights: Ravi, Beas, Sutlej.", 'False!')),
 ('q2', "Next one: the treaty was brokered by the World Bank. True! Easy marks, if you remember the stamp.",
  statement(2, 'The Indus Waters Treaty was brokered by the World Bank.', 'TRUE', 'After about nine years of talks, signed in 1960.', 'True!')),
 ('mains', "And for Mains, practise this one: can water be an instrument of foreign policy? Discuss with reference to the Indus Waters Treaty. Build your answer in three parts. First, the treaty and its record. Second, India's security argument and Pakistan's legal argument. Third, the options ahead, from renegotiation to restoration.",
  mains('Can water be an instrument of foreign policy? Discuss with reference to the Indus Waters Treaty.',
        [('The treaty and its record', '1960, World Bank, survived three wars'),
         ('The two arguments', "India's security argument · Pakistan's legal argument"),
         ('The options ahead', 'From renegotiation to restoration')],
        ['First, the treaty', "Second, India's", 'Third, the options'])),
 ('watch', "As of November 2026, here's what to watch. Number one: does the Permanent Indus Commission meet again? Number two: India's hydropower projects on the Chenab, as they come online. And number three: the Neutral Expert's decision on Ratle, expected in July 2027.",
  watch([('Does the Permanent Indus Commission meet again?', 'OPEN QUESTION'),
         ('Hydropower projects on the Chenab', 'AS THEY COME ONLINE'),
         ("The Neutral Expert's decision on Ratle", 'EXPECTED JULY 2027')],
        ['Number one', 'Number two', 'And number three'])),
 ('end', "And with that, a new thread joins our relations web: India and Pakistan, Indus Waters, in abeyance. Next briefing: India and Pakistan after Pahalgam. To catch it when it's out, subscribe to Gyaan-X Studios.",
  relations_web(EP, 'a new thread', 'INDIA AND PAKISTAN AFTER PAHALGAM', 'Next briefing', 'subscribe')),
]

# scenes in the same group continue without a wipe
GROUPS = {'back1': 'tl', 'back2': 'tl', 'india': 'st', 'pak': 'st'}

# keyword pop-ups, synced to the English narration: beat -> [(phrase, label, ink)]
KEYS = {
 'hook': [('on hold', 'ON HOLD SINCE APR 2025', 'coral'), ('Rejected', 'REJECTED', 'teal')],
 'back1': [('nine long years', '9 YEARS OF TALKS', 'teal')],
 'back2': [('twenty-six people', '26 LIVES LOST', 'coral'), ('never taken before', 'A FIRST', 'teal')],
 'rivers': [('without limits', 'UNRESTRICTED', 'teal'), ('limited ways', 'LIMITED USE', 'coral')],
 'since': [('fast track', 'FAST-TRACKED', 'teal')],
 'award': [('the twist', 'THE TWIST', 'coral')],
 'stakes': [('three big things', '3 THINGS AT STAKE', 'coral')],
 'tip': [('And the year', 'RBS EAST · IJC WEST', 'violet')],
 'q2': [('Easy marks', 'EASY MARKS', 'teal')],
}

# explainer marker annotations (screen coordinates): beat -> [(phrase, kind, x, y, w, h)]
ANNOT = {
 'hook': [('on hold', 'underline', 130, 615, 640, 0)],
 'rivers': [('without limits', 'circle', 1590, 640, 500, 100), ('limited ways', 'arrow', 560, 700, 300, -180)],
 'award': [('Its message', 'underline', 990, 356, 520, 0), ('limited some construction', 'circle', 1650, 770, 420, 90)],
 'stakes': [('Brahmaputra', 'circle', 1540, 420, 330, 280)],
 'tip': [('And the year', 'underline', 1010, 505, 470, 0), ('And the year', 'underline', 990, 612, 520, 0)],
 'watch': [('July 2027', 'underline', 318, 814, 350, 0)],
 'since': [('Ratle', 'circle', 1640, 680, 230, 230)],
}

# Hindi narration, beat by beat (English terms written in Devanagari so the Hindi voice says them clearly)
HI = {
 'hook': "तेईस अप्रैल 2025 को, भारत ने 1960 की सिंधु जल संधि को स्थगित कर दिया। फिर इकतीस अगस्त 2026 को, एक कोर्ट ऑफ़ आर्बिट्रेशन ने कहा कि भारत के कारण इसे निलंबित करने के लिए काफ़ी नहीं हैं। और भारत का जवाब? उसी दिन ख़ारिज! तो यह संधि भारत के लिए इतनी अहम क्यों है? चलिए समझते हैं।",
 'back1': "चलिए 1960 में चलते हैं। विश्व बैंक की मध्यस्थता में, लगभग नौ साल की लंबी बातचीत के बाद, प्रधानमंत्री जवाहरलाल नेहरू और पाकिस्तान के राष्ट्रपति अयूब ख़ान ने उस सितंबर कराची में इस संधि पर हस्ताक्षर किए।",
 'back2': "और इसकी सबसे ख़ास बात? यह 1965 और 1971 के युद्धों में भी बनी रही। 1999 के करगिल संघर्ष में भी। लेकिन अप्रैल 2025 में, पहलगाम के आतंकी हमले में छब्बीस लोगों की जान जाने के बाद, भारत ने वह कदम उठाया जो पहले कभी नहीं उठाया था: उसने घोषणा की कि संधि स्थगित रखी जाएगी।",
 'rivers': "तो यह संधि असल में करती क्या है? यह छह नदियों को बाँटती है। तीन पूर्वी नदियाँ, यानी रावी, ब्यास और सतलुज, भारत के बिना रोक-टोक इस्तेमाल के लिए हैं। तीन पश्चिमी नदियाँ, यानी सिंधु, झेलम और चिनाब, पाकिस्तान को मिलीं। भारत इनका भी इस्तेमाल कर सकता है, लेकिन सीमित तरीक़ों से, जैसे रन-ऑफ़-द-रिवर पनबिजली।",
 'ladder': "संधि ने विवाद सुलझाने की एक व्यवस्था भी बनाई। पहला कदम: स्थायी सिंधु आयोग, यानी परमानेंट इंडस कमीशन, जिसमें दोनों देशों का एक-एक आयुक्त होता है। दूसरा कदम: एक तटस्थ विशेषज्ञ। तीसरा कदम: एक कोर्ट ऑफ़ आर्बिट्रेशन।",
 'since': "तो तब से भारत ने क्या किया है? अप्रैल 2025 से, भारत ने चिनाब पर बने अपने बाँधों से गाद निकाली है, और पाकल दुल और रतले जैसी पनबिजली परियोजनाओं को तेज़ रफ़्तार दी है।",
 'award': "और फिर आया बड़ा मोड़। इकतीस अगस्त 2026 को, कोर्ट ऑफ़ आर्बिट्रेशन ने एक अंतरिम फ़ैसला दिया। उसका संदेश: संधि को निलंबित करने के लिए भारत के आधार काफ़ी नहीं हैं। और फ़िलहाल, उसने रतले में कुछ निर्माण पर रोक लगाई।",
 'india': "तो किसका क्या कहना है? भारत का रुख़ दृढ़ है: संधि तब तक स्थगित रहेगी, जब तक पाकिस्तान सीमा-पार आतंकवाद को अपना समर्थन विश्वसनीय और अपरिवर्तनीय रूप से छोड़ नहीं देता। भारत का कहना है कि यह कोर्ट संधि का उल्लंघन करके बनाया गया, इसका कोई अधिकार-क्षेत्र नहीं है, और भारत कभी इसके सामने पेश नहीं हुआ।",
 'pak': "पाकिस्तान इसे दूसरी तरह देखता है। उसका कहना है कि यह फ़ैसला दिखाता है कि संधि पूरी तरह लागू और बाध्यकारी है, और भारत को इसका पालन करना चाहिए।",
 'stakes': "अब सवाल यह, कि आपको इसकी परवाह क्यों करनी चाहिए? क्योंकि भारत के लिए तीन बड़ी चीज़ें दाँव पर हैं। एक: सुरक्षा। भारत इस संधि को सीधे सीमा-पार आतंकवाद से जोड़ता है। दो: ऊर्जा। पश्चिमी नदियों के बेहतर इस्तेमाल से जम्मू-कश्मीर को ज़्यादा पनबिजली मिल सकती है। और तीन: मिसाल। ब्रह्मपुत्र पर भारत, चीन के नीचे, निचले हिस्से का देश है। इसलिए नदी समझौतों को कैसे पढ़ा जाता है, यह भारत के लिए भी मायने रखता है।",
 'tip': "तो चलिए, याद करने का समय! यह रहा आपका पासपोर्ट स्टैम्प। पूरब है आर-बी-एस: रावी, ब्यास, सतलुज, भारत के लिए। पश्चिम है आई-जे-सी: इंडस यानी सिंधु, झेलम, चिनाब, पाकिस्तान के लिए। और साल? उन्नीस सौ साठ, विश्व बैंक की मध्यस्थता में।",
 'q1': "परीक्षा डेस्क! सही या ग़लत: संधि भारत को चिनाब के बिना रोक-टोक इस्तेमाल का अधिकार देती है। सोचिए। ग़लत! चिनाब एक पश्चिमी नदी है। भारत के पूरे अधिकार रावी, ब्यास और सतलुज पर हैं।",
 'q2': "अगला: इस संधि में विश्व बैंक ने मध्यस्थता की थी। सही! स्टैम्प याद है, तो ये नंबर पक्के।",
 'mains': "और मेन्स के लिए, यह सवाल अभ्यास कीजिए: क्या पानी विदेश नीति का एक साधन हो सकता है? सिंधु जल संधि के संदर्भ में चर्चा कीजिए। जवाब तीन हिस्सों में बनाइए। पहला, संधि और उसका रिकॉर्ड। दूसरा, भारत का सुरक्षा तर्क और पाकिस्तान का क़ानूनी तर्क। तीसरा, आगे के विकल्प, पुनर्वार्ता से लेकर बहाली तक।",
 'watch': "नवंबर 2026 की स्थिति में, आगे इन बातों पर नज़र रखिए। नंबर एक: क्या स्थायी सिंधु आयोग की फिर से बैठक होती है? नंबर दो: चिनाब पर भारत की पनबिजली परियोजनाएँ, जैसे-जैसे वे शुरू होती हैं। और नंबर तीन: रतले पर तटस्थ विशेषज्ञ का फ़ैसला, जो जुलाई 2027 में आने की उम्मीद है।",
 'end': "और इसके साथ, हमारे रिलेशन्स वेब में एक नया धागा जुड़ता है: भारत और पाकिस्तान, सिंधु जल, स्थगित। अगली ब्रीफ़िंग: पहलगाम के बाद भारत और पाकिस्तान। इसे आते ही देखने के लिए, ज्ञान-एक्स स्टूडियोज़ को सब्सक्राइब कीजिए।",
}

# sound: whoosh on every wipe, blip on every pop-up, stamp, riser, verdict dings, pluck
_order = [k for k, _, _ in BEATS]
FX = [('whoosh', k, -.25, .22) for i, k in enumerate(_order) if i and GROUPS.get(k, k) != GROUPS.get(_order[i-1], _order[i-1])]
FX += [('blip', k, ph, .16) for k, items in KEYS.items() for ph, _, _ in items]
FX += [('whoosh', k, ph, .06) for k, items in ANNOT.items() for ph, *_ in items]   # soft marker swish
FX += [('tick', 'hook', .15, .12), ('riser', 'tip', 'East is', .2), ('stamp', 'tip', 'East is', .5),
       ('ding', 'q1', 'False!', .3), ('ding', 'q2', 'True!', .3), ('pluck', 'end', 'a new thread', .35)]
