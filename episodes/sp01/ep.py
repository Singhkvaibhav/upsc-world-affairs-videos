"""Special 1 — Nvidia, Jensen Huang and the honey-trap question (about 11.5 min, bilingual: English + Hindi)."""
import os, sys, math, random, cairo
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from engine import core
TOTAL = 690.0
core.TOTAL = TOTAL
from engine.core import W, H, seg, ease, eoc, eob, lerp, T
from engine.riso import R, rgba, riso, halftone, rrect, txt, inktext, para, camera, pop, fadein, cable, credit, bg_board, bg_sheet, tw, typed
from engine.brief import india_map, map_point, _bg, outro, headline, stands, stakes, statement, mains, watch, tag, figure, token, podium
from engine.web import passport_stamp, relations_web
from engine.chip import (chip_pkg, core_grid, particles, panel, net, mix, gpu_workers, pixels, matrix_race, train_infer, uses,
                         memory_wall, dram_nand, hbm_tower, makers, supply_board)
from text import EN, HI as _HI

EP = 'SPECIAL 1'
CODE = 'WaSP01'
TITLE = 'Nvidia_Jensen_Huang_and_the_Honey_Trap_Question'
NAME = 'Nvidia, Jensen Huang and the honey-trap question'
VOICE_EN = {'length': 0.98, 'noise': (0.72, 0.85), 'gaps': (0.38, 0.22)}
VOICE_HI = {'length': 0.86, 'noise': (0.72, 0.85), 'gaps': (0.38, 0.22)}
CRF, PRESET = 17, 'medium'
CH = 1.3   # extra seconds on beats that open with a chapter card
EXTRA = {'hook': .6, 'tip': 1.0, 'end': 2.5, 'life1': CH, 'gpu1': CH + 1.5, 'wave1': CH, 'mem1': CH, 'trap1': CH, 'build1': CH, 'stake1': CH}
TENSION = ('trap1', 'trap5')
HI = _HI
NARR = dict(EN)

def _c(x): return T(x) if isinstance(x, str) else x
def Ts(x):
    """soft cue: phrases spoken in another beat resolve to 999 (not in this beat)"""
    try: return T(x)
    except ValueError: return 999.

# ---------- chapter cards: a full-frame ink slam, then the scene slides out from under it ----------
def chapter(scene, num, title, sub):
    def f(ctx, t, D):
        scene(ctx, t, D)
        if t > 2.3: return
        p_in = seg(t, 0, .25); p_out = seg(t, 1.75, 2.25)
        y = -H*eoc(p_out)
        ctx.save(); ctx.translate(0, y)
        rgba(ctx, R['char']); ctx.rectangle(0, 0, W, H); ctx.fill()
        halftone(ctx, lambda: ctx.rectangle(0, 0, W, H), R['teal'], .35, step=16, r=2.6, angle=.7)
        rgba(ctx, R['coral']); ctx.rectangle(0, H - 26, W*eoc(seg(t, .1, 1.7)), 26); ctx.fill()
        txt(ctx, typed(f'CHAPTER {num}', seg(t, .1, .5)), 160, 380, 40, R['coral'], 1, 'bold', mono=True)
        words = title.split(); x = 150
        for i, w_ in enumerate(words):
            q = seg(t, .25 + i*.12, .55 + i*.12)
            if q <= 0: continue
            sc = lerp(1.6, 1, eob(q, 1.5))
            ww = tw(ctx, w_ + ' ', 150, 'black')
            ctx.save(); ctx.translate(x, 560); ctx.scale(sc, sc)
            ctx.move_to(0, 0); ctx.select_font_face('Inter Display Black', cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD); ctx.set_font_size(150)
            ctx.text_path(w_); rgba(ctx, R['paper'], ease(q*2)); ctx.fill(); ctx.restore()
            x += ww
        txt(ctx, sub, 160, 660, 36, R['tealpale'], ease(seg(t, .7, 1.1)), 'bold')
        ctx.restore()
    f.bg = scene.bg
    return f

# ---------- HOOK ----------
def _motif_hook(ctx, t, D, a):
    q = eob(seg(t, .4, 1.3), 1.3)
    if q <= 0: return
    cx, cy = 1580, 540
    ctx.save(); ctx.translate(cx, cy + 60*(1 - q)); ctx.rotate(-.08 + .02*math.sin(t*.6))
    chip_pkg(ctx, 0, 0, 1.3, a, t, reveal=ease(seg(t, 1.0, 2.0)), label='NVIDIA')
    ctx.restore()
    # a magnifying glass sweeps over the chip
    m = seg(t, 2.2, D)
    if m > 0:
        mx = cx + 170*math.cos(m*5.5); my = cy + 110*math.sin(m*7)
        ma = ease(seg(t, 2.2, 2.8))*a
        rgba(ctx, R['coral'], ma); ctx.set_line_width(16); ctx.arc(mx, my, 110, 0, 2*math.pi); ctx.stroke()
        ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.set_line_width(28); ctx.move_to(mx + 80, my + 80); ctx.line_to(mx + 190, my + 190); ctx.stroke()
        halftone(ctx, lambda: ctx.arc(mx, my, 100, 0, 2*math.pi), R['coral'], .35*ma, step=9, r=2)

# ---------- four questions ----------
def s_qs(ctx, t, D):
    bg_sheet(ctx); a_out = outro(t, D)
    cable(ctx, t, 'IN THIS SPECIAL · FOUR QUESTIONS', a_out, core.EP)
    ctx.save(); camera(ctx, t, D, (1.0, 1.04), cy=520)
    qs = [('WHO IS', 'JENSEN HUANG?', 'Who is Jensen', R['teal'], 'person'), ('WHAT IS', 'A GPU?', 'What is a GPU', R['coral'], 'chip'),
          ('WHY ARE', 'MEMORY MAKERS KEY?', 'Why are memory', R['over'], 'tower'), ('WHAT DOES IT MEAN FOR', 'AI AND INDIA?', 'And what could', R['teal'], 'web')]
    for i, (k1, k2, cue, ink, ic) in enumerate(qs):
        t0 = Ts(cue) - .1; q = seg(t, t0, t0 + .55)
        if q <= 0: continue
        x = 150 + (i % 2)*830; y = 170 + (i//2)*360; s = eob(q, 1.7); a = ease(q*2)*a_out
        cur = i == max([j for j, (_, _, c, _, _) in enumerate(qs) if t >= T(c) - .1] or [0])
        ctx.save(); ctx.translate(x + 380, y + 160); ctx.scale(s, s); ctx.rotate((-.02 if i % 2 else .02)*(1 - ease(q))); ctx.translate(-(x + 380), -(y + 160))
        riso(ctx, lambda: rrect(ctx, x, y, 760, 320, 20), ink if cur else R['paper'], a, second=R['coral'] if cur and ink != R['coral'] else None)
        rgba(ctx, ink, a); ctx.set_line_width(4); rrect(ctx, x, y, 760, 320, 20); ctx.stroke()
        fg = R['paper'] if cur else R['char']
        inktext(ctx, f'0{i+1}', x + 40, y + 120, 96, R['paper'] if cur else ink, a, weight='black')
        txt(ctx, k1, x + 40, y + 200, 30, fg, a, 'bold', mono=True)
        txt(ctx, k2, x + 40, y + 260, 50, fg, a, 'black')
        if ic == 'chip': chip_pkg(ctx, x + 640, y + 120, .35, a, t, reveal=1)
        elif ic == 'person': figure(ctx, x + 640, y + 200, .9, R['paper'] if cur else ink, a, t, seed=3)
        elif ic == 'tower':
            for k in range(6): riso(ctx, lambda: rrect(ctx, x + 580, y + 210 - k*28, 120, 22, 4), R['paper'] if cur else ink, a)
        else:
            for k in range(5):
                ang = k*1.25 + t*.4; px, py = x + 640 + 70*math.cos(ang), y + 130 + 60*math.sin(ang)
                rgba(ctx, R['paper'] if cur else ink, a); ctx.set_line_width(3); ctx.move_to(x + 640, y + 130); ctx.line_to(px, py); ctx.stroke()
                ctx.arc(px, py, 12, 0, 2*math.pi); ctx.fill()
            ctx.arc(x + 640, y + 130, 22, 0, 2*math.pi); ctx.fill()
        ctx.restore()
    ctx.restore()
s_qs.bg = 'sheet'

# ---------- life strip ----------
def _ico(ctx, kind, x, y, t, a, ink):
    if kind == 'home':
        riso(ctx, lambda: (ctx.move_to(x - 80, y), ctx.line_to(x, y - 70), ctx.line_to(x + 80, y), ctx.close_path()), R['coral'], a)
        riso(ctx, lambda: ctx.rectangle(x - 60, y, 120, 90), ink, a, second=R['coral'])
        riso(ctx, lambda: ctx.rectangle(x - 15, y + 40, 30, 50), R['paper'], a)
    elif kind == 'plane':
        px = x - 120 + 240*((t*.25) % 1)
        ctx.save(); ctx.translate(px, y - 10 + 8*math.sin(t*2))
        riso(ctx, lambda: (ctx.move_to(-70, 0), ctx.curve_to(-40, -16, 50, -16, 80, 0), ctx.curve_to(50, 14, -40, 14, -70, 0)), ink, a)
        riso(ctx, lambda: (ctx.move_to(-10, 0), ctx.line_to(20, -60), ctx.line_to(36, -60), ctx.line_to(26, 0), ctx.close_path()), R['coral'], a)
        ctx.restore()
        ctx.save(); ctx.set_dash([10, 10]); rgba(ctx, R['grey'], a); ctx.set_line_width(3); ctx.move_to(x - 140, y + 40); ctx.curve_to(x - 40, y - 40, x + 40, y - 40, x + 140, y + 40); ctx.stroke(); ctx.restore()
    elif kind == 'school':
        riso(ctx, lambda: ctx.rectangle(x - 110, y - 30, 220, 120), ink, a, second=R['coral'])
        riso(ctx, lambda: (ctx.move_to(x - 130, y - 30), ctx.line_to(x, y - 100), ctx.line_to(x + 130, y - 30), ctx.close_path()), R['over'], a)
        for k in range(4):
            rgba(ctx, R['paper'], a); ctx.rectangle(x - 90 + k*50, y + 5, 28, 30); ctx.fill()
        # mop
        ctx.save(); ctx.translate(x + 150, y + 40); ctx.rotate(.3*math.sin(t*3))
        rgba(ctx, R['char'], a); ctx.set_line_width(6); ctx.move_to(0, -90); ctx.line_to(0, 40); ctx.stroke()
        riso(ctx, lambda: rrect(ctx, -30, 36, 60, 22, 6), R['coral'], a); ctx.restore()
    elif kind == 'case':
        riso(ctx, lambda: rrect(ctx, x - 90, y - 40, 180, 120, 14), R['over'], a, second=R['coral'])
        rgba(ctx, R['char'], a); ctx.set_line_width(8); rrect(ctx, x - 30, y - 70, 60, 34, 10); ctx.stroke()
        txt(ctx, '$', x, y + 44, 40, R['paper'], a*.5, 'black', 'c')
    elif kind == 'cap':
        riso(ctx, lambda: (ctx.move_to(x - 120, y - 20), ctx.line_to(x, y - 70), ctx.line_to(x + 120, y - 20), ctx.line_to(x, y + 30), ctx.close_path()), R['char'], a)
        riso(ctx, lambda: (ctx.move_to(x - 70, y + 5), ctx.line_to(x - 70, y + 60), ctx.curve_to(x - 30, y + 90, x + 30, y + 90, x + 70, y + 60), ctx.line_to(x + 70, y + 5), ctx.line_to(x, y + 30), ctx.close_path()), ink, a)
        rgba(ctx, R['coral'], a); ctx.set_line_width(5); ctx.move_to(x + 100, y - 25); ctx.line_to(x + 100 + 6*math.sin(t*3), y + 50); ctx.stroke()
    elif kind == 'chip':
        chip_pkg(ctx, x, y + 10, .5, a, t, reveal=1)

LIFE = [  # (x, title, line, icon, cue)
    (360, '1963', 'Born in Tainan, Taiwan', 'home', 'born in Tainan'),
    (1000, '1973', 'Aged nine, sent to America', 'plane', 'in 1973'),
    (1640, 'KENTUCKY', 'Youngest pupil · cleaned the bathrooms', 'school', 'rural Kentucky'),
    (2280, 'TWO YEARS LATER', 'Parents follow, with very little money', 'case', 'His parents'),
    (2920, 'OREGON STATE', 'Electrical engineering', 'cap', 'Oregon State'),
    (3560, 'AMD · LSI LOGIC', 'Designing chips', 'chip', 'designed chips'),
]
def life_strip(span):
    def f(ctx, t, D):
        bg_sheet(ctx); a_out = outro(t, D)
        cable(ctx, t, 'CHAPTER 1 · THE MAN', a_out, core.EP)
        # camera follows the newest station that has appeared
        # camera eases from station to station as each is spoken
        times = [(Ts(cue) - .2, x) for (x, _, _, _, cue) in LIFE if Ts(cue) < 900]
        cx = LIFE[max(span[0] - 1, 0)][0]
        for (t0, x) in times:
            cx = lerp(cx, x, ease(seg(t, t0 - .3, t0 + .9)))
        ctx.save(); ctx.translate(W/2 - cx, 0)
        ctx.save(); ctx.translate((cx - W/2)*.4, 0)
        def hills():
            ctx.move_to(-2000, 1000)
            for x in range(-2000, 6000, 60): ctx.line_to(x, 880 + 40*math.sin(x*.003))
            ctx.line_to(6000, 1200); ctx.line_to(-2000, 1200); ctx.close_path()
        halftone(ctx, hills, R['tealpale'], .9*a_out, step=12, r=2.4)
        ctx.restore()
        y = 620
        rgba(ctx, R['char'], a_out); ctx.rectangle(-400, y - 3, 4600, 6); ctx.fill()
        for i, (x, ti, line, ic, cue) in enumerate(LIFE):
            t0 = Ts(cue)
            if t0 >= 900:
                if i < span[0]:   # stations from the previous beat stay lit
                    q = 1.
                else:
                    riso(ctx, lambda: ctx.arc(x, y, 9, 0, 2*math.pi), R['grey'], .5*a_out); continue
            else:
                q = seg(t, t0 - .2, t0 + .4)
            if q <= 0:
                riso(ctx, lambda: ctx.arc(x, y, 9, 0, 2*math.pi), R['grey'], .5*a_out); continue
            ink = R['coral'] if i % 2 else R['teal']; qa = ease(q*1.5)*a_out
            riso(ctx, lambda: ctx.arc(x, y, 24*eob(q, 2), 0, 2*math.pi), ink, qa, second=R['coral'] if ink == R['teal'] else R['teal'])
            _ico(ctx, ic, x, y - 230 - 30*(1 - eob(q, 1.4)), t, qa, ink)
            inktext(ctx, ti, x, y + 110, 64 if len(ti) < 10 else 44, ink, qa, settle=eoc(q), seed=i, align='c', second=R['coral'] if ink == R['teal'] else R['teal'])
            para(ctx, line, x, y + 170, 30, R['char'], 480, ease(seg(t, t0 + .1, t0 + .5)) * a_out if t0 < 900 else a_out, weight='bold', align='c')
        ctx.restore()
        # the podcast source card
        if span[0] == 0:
            tr = T('Joe Rogan'); q = seg(t, tr, tr + .5)
            if q > 0:
                qa = ease(q*2)*a_out
                ctx.save(); ctx.translate(1520, 210); ctx.rotate(.03); ctx.scale(eob(q, 1.8), eob(q, 1.8))
                riso(ctx, lambda: rrect(ctx, -330, -70, 660, 140, 16), R['over'], qa)
                riso(ctx, lambda: rrect(ctx, -300, -42, 40, 70, 20), R['paper'], qa)
                rgba(ctx, R['paper'], qa); ctx.set_line_width(5); ctx.arc(-280, -4, 34, 0, math.pi); ctx.stroke()
                txt(ctx, 'AS TOLD ON THE JOE ROGAN EXPERIENCE', -230, -10, 22, R['paper'], qa, 'bold', mono=True)
                txt(ctx, 'EPISODE #2422 · 3 DEC 2025', -230, 30, 22, R['coralpale'], qa, 'bold', mono=True)
                ctx.restore()
    return _bg(f, 'sheet')

# ---------- the Denny's booth, April 1993 ----------
def s_booth(ctx, t, D):
    bg_sheet(ctx); a_out = outro(t, D)
    cable(ctx, t, 'APRIL 1993 · A DINER BOOTH', a_out, core.EP)
    ctx.save(); camera(ctx, t, D, (1.0, 1.06), cy=560)
    a = fadein(t, .2, .5)*a_out
    # booth
    riso(ctx, lambda: rrect(ctx, 220, 300, 1000, 420, 40), R['coral'], a)
    riso(ctx, lambda: rrect(ctx, 250, 330, 940, 360, 30), R['coralpale'], a)
    riso(ctx, lambda: rrect(ctx, 200, 700, 1060, 60, 10), R['char'], a)
    names = [('JENSEN HUANG', 'Jensen'), ('CHRIS MALACHOWSKY', 'Chris Malachowsky'), ('CURTIS PRIEM', 'Curtis Priem')]
    for i, (nm, cue) in enumerate(names):
        x = 420 + i*300; q = seg(t, .4 + i*.25, .9 + i*.25)
        figure(ctx, x, 640, 1.2, R['teal'] if i == 0 else R['over'], ease(q*2)*a, t, gesture=seg(t, 3 + i, 3.6 + i) if i == 0 else 0, seed=i)
        nq = seg(t, Ts(cue) - .1, Ts(cue) + .3) if cue != 'Jensen' else seg(t, .9, 1.3)
        tag(ctx, x, 800, nm, R['char'], ease(nq)*a, 20, align='c')
    # napkin sketch
    nq = seg(t, T('sketched') - .3, T('sketched') + .4)
    if nq > 0:
        na = ease(nq*2)*a_out
        ctx.save(); ctx.translate(1520, 470); ctx.rotate(-.06)
        riso(ctx, lambda: rrect(ctx, -280, -260, 560, 520, 8), R['paper'], na)
        rgba(ctx, R['grey'], na*.5); ctx.set_line_width(2)
        for k in range(8): ctx.move_to(-260, -200 + k*55); ctx.line_to(260, -200 + k*55); ctx.stroke()
        p = seg(t, T('sketched'), T('sketched') + 2.5)
        rgba(ctx, R['teal'], na); ctx.set_line_width(6); ctx.set_line_cap(cairo.LINE_CAP_ROUND)
        pts = [(-150, -150), (150, -150), (150, 150), (-150, 150), (-150, -150)]
        n = p*4
        ctx.move_to(*pts[0])
        for i in range(1, 5):
            if n >= i: ctx.line_to(*pts[i])
            elif n > i - 1:
                fr = n - (i - 1); ctx.line_to(lerp(pts[i-1][0], pts[i][0], fr), lerp(pts[i-1][1], pts[i][1], fr)); break
        ctx.stroke()
        # a spinning wireframe cube: 3D graphics
        cq = seg(t, T('3D video games') - .4, T('3D video games') + .3)
        if cq > 0:
            ang = t*1.2; s3 = 80*eob(cq, 1.6)
            V = [(x_, y_, z_) for x_ in (-1, 1) for y_ in (-1, 1) for z_ in (-1, 1)]
            P = []
            for (x_, y_, z_) in V:
                x2 = x_*math.cos(ang) - z_*math.sin(ang); z2 = x_*math.sin(ang) + z_*math.cos(ang)
                y2 = y_*math.cos(.5) - z2*math.sin(.5)
                P.append((x2*s3, y2*s3))
            rgba(ctx, R['coral'], na); ctx.set_line_width(5)
            for i in range(8):
                for j in range(i + 1, 8):
                    if sum(V[i][k] != V[j][k] for k in range(3)) == 1:
                        ctx.move_to(*P[i]); ctx.line_to(*P[j]); ctx.stroke()
            txt(ctx, 'CHIPS FOR 3D GAMES', 0, 230, 30, R['char'], na, 'bold', 'c', mono=True)
        ctx.restore()
    sq = seg(t, T('he started Nvidia') - .1, T('he started Nvidia') + .4)
    if sq > 0:
        ctx.save(); ctx.translate(720, 200); ctx.rotate(-.04); ctx.scale(eob(sq, 2), eob(sq, 2))
        tag(ctx, 0, 0, 'NVIDIA · FOUNDED APRIL 1993', R['teal'], ease(sq*2)*a_out, 34, align='c'); ctx.restore()
    ctx.restore()
s_booth.bg = 'sheet'

# ---------- CUDA ----------
CODE_LINES = ['// 2006: CUDA', '__global__ void add(float *a, float *b, float *c) {', '    int i = threadIdx.x + blockIdx.x * blockDim.x;',
              '    c[i] = a[i] + b[i];', '}', 'add<<<4096, 256>>>(a, b, c);   // a million sums at once']
def s_cuda(ctx, t, D):
    bg_sheet(ctx); a_out = outro(t, D)
    cable(ctx, t, 'CHAPTER 3 · THE WAVE', a_out, core.EP)
    ctx.save(); camera(ctx, t, D, (1.0, 1.04), cy=500)
    tc = T('In 2006'); a = ease(seg(t, tc - .3, tc + .3))*a_out
    if a > 0:
        riso(ctx, lambda: rrect(ctx, 120, 180, 1060, 560, 18), R['char'], a)
        for k, col in enumerate((R['coral'], R['coralpale'], R['tealpale'])):
            rgba(ctx, col, a); ctx.arc(160 + k*34, 215, 10, 0, 2*math.pi); ctx.fill()
        n = (t - tc)*28; y = 300
        for i, l in enumerate(CODE_LINES):
            s = typed(l, n/len(l)) if n > 0 else ''
            n -= len(l)
            txt(ctx, s, 160, y + i*62, 26, R['tealpale'] if l.startswith('//') or '//' in s and i == 5 else R['paper'], a, mono=True)
            if 0 < n + len(l) <= len(l) and (int(t*3) % 2): rgba(ctx, R['coral'], a); ctx.rectangle(160 + tw(ctx, s, 26, mono=True), y + i*62 - 24, 14, 30); ctx.fill()
        tag(ctx, 650, 820, 'CUDA · 2006 · SOFTWARE FOR ANY KIND OF MATHS', R['teal'], ease(seg(t, tc + 1, tc + 1.5))*a_out, 26, align='c')
    tn = T('Nobody wanted it'); q = seg(t, tn, tn + .45)
    if q > 0:
        qa = ease(q*2)*a_out
        ctx.save(); ctx.translate(1530, 420); ctx.rotate(.06); ctx.scale(lerp(1.8, 1, eoc(q)), lerp(1.8, 1, eoc(q)))
        riso(ctx, lambda: rrect(ctx, -320, -170, 640, 340, 20), R['coral'], qa, second=R['teal'])
        txt(ctx, '“', -280, -40, 130, R['paper'], qa, 'black')
        inktext(ctx, 'Nobody', 0, -10, 90, R['paper'], qa, align='c')
        inktext(ctx, 'wanted it.', 0, 90, 80, R['paper'], qa, align='c')
        txt(ctx, 'JENSEN HUANG, ON JOE ROGAN', 0, 150, 20, R['paper'], qa, 'bold', 'c', mono=True)
        ctx.restore()
    ctx.restore()
s_cuda.bg = 'sheet'

# ---------- AlexNet and the moat ----------
def _gcard(ctx, x, y, t, a, k):
    riso(ctx, lambda: rrect(ctx, x, y, 300, 130, 14), R['char'], a, seed=k)
    for f_ in range(2):
        fx = x + 80 + f_*140; fy = y + 65
        riso(ctx, lambda: ctx.arc(fx, fy, 48, 0, 2*math.pi), R['grey'], a)
        ctx.save(); ctx.translate(fx, fy); ctx.rotate(t*12 + k)
        for b in range(5):
            ctx.rotate(2*math.pi/5); rgba(ctx, R['paper'], a*.8); ctx.move_to(0, 0); ctx.curve_to(10, -20, 30, -30, 40, -14); ctx.line_to(0, 0); ctx.fill()
        ctx.restore()
    rgba(ctx, R['coral'], a); ctx.rectangle(x + 20, y + 130, 260, 14); ctx.fill()
def s_alex(ctx, t, D):
    bg_sheet(ctx); a_out = outro(t, D)
    cable(ctx, t, '2012 · THE TWIST', a_out, core.EP)
    ctx.save(); camera(ctx, t, D, (1.0, 1.04), cy=520)
    tm = T("That's Nvidia's real moat"); sw = ease(seg(t, tm - .4, tm + .5))
    a1 = (1 - sw)*a_out
    if a1 > 0:
        a = fadein(t, .2, .5)*a1
        inktext(ctx, 'THE TWIST', 150, 260, 120, R['coral'], ease(seg(t, .2, .7))*a1, settle=seg(t, .2, 1), second=R['teal'])
        ta = T('AlexNet')
        for k in range(2):
            q = seg(t, ta + .3 + k*.3, ta + .8 + k*.3)
            if q > 0: _gcard(ctx, 150, 420 + k*190 + 40*(1 - eob(q)), t, ease(q*2)*a1, k)
        if t > ta + .3: txt(ctx, 'TWO NVIDIA GAMING CARDS', 300, 840, 24, R['char'], a, 'bold', 'c', mono=True)
        # image grid being recognised
        q = seg(t, ta - .4, ta + .4)
        if q > 0:
            qa = ease(q*2)*a1
            for i in range(4):
                for j in range(3):
                    x = 620 + i*170; y = 340 + j*160
                    rr = random.Random(i*3 + j)
                    riso(ctx, lambda: rrect(ctx, x, y, 150, 140, 10), mix(R['tealpale'], R['coralpale'], rr.random()), qa)
                    # simple shapes in each picture
                    sh = rr.randint(0, 2); ink = R['teal'] if sh == 0 else R['coral'] if sh == 1 else R['over']
                    if sh == 0: riso(ctx, lambda: ctx.arc(x + 75, y + 70, 40, 0, 2*math.pi), ink, qa)
                    elif sh == 1: riso(ctx, lambda: (ctx.move_to(x + 30, y + 110), ctx.line_to(x + 75, y + 30), ctx.line_to(x + 120, y + 110), ctx.close_path()), ink, qa)
                    else: riso(ctx, lambda: rrect(ctx, x + 35, y + 35, 80, 70, 8), ink, qa)
                    ok = seg(t, ta + 1 + (i*3 + j)*.12, ta + 1.2 + (i*3 + j)*.12)
                    if ok > 0:
                        riso(ctx, lambda: ctx.arc(x + 130, y + 20, 18*eob(ok, 2), 0, 2*math.pi), R['teal'], qa)
                        rgba(ctx, R['paper'], qa); ctx.set_line_width(4); ctx.move_to(x + 121, y + 20); ctx.line_to(x + 128, y + 27); ctx.line_to(x + 140, y + 12); ctx.stroke()
            tag(ctx, 950, 870, 'ALEXNET · IMAGES RECOGNISED', R['teal'], qa, 24, align='c')
        tk = T('Deep learning took off'); q = seg(t, tk, tk + .5)
        if q > 0:
            ctx.save(); ctx.translate(1600, 470); ctx.rotate(-.06); ctx.scale(eob(q, 2), eob(q, 2))
            riso(ctx, lambda: rrect(ctx, -200, -90, 400, 180, 18), R['teal'], ease(q*2)*a1, second=R['coral'])
            inktext(ctx, 'DEEP', 0, -8, 64, R['paper'], ease(q*2)*a1, align='c'); inktext(ctx, 'LEARNING', 0, 60, 52, R['paper'], ease(q*2)*a1, align='c')
            ctx.restore()
    if sw > 0:
        a = sw*a_out
        cx, cy = W/2 + 120, 520
        # moat: rings of water with flowing dashes, developers as dots outside
        for k in range(3):
            ctx.new_path(); rgba(ctx, R['river'], a*(.5 - k*.12)); ctx.set_line_width(36 - k*6); ctx.arc(cx, cy, 270 + k*40, 0, 2*math.pi); ctx.stroke()
        ctx.save(); ctx.new_path(); ctx.set_dash([20, 24], t*40); rgba(ctx, R['paper'], a*.8); ctx.set_line_width(4); ctx.arc(cx, cy, 290, 0, 2*math.pi); ctx.stroke(); ctx.restore()
        chip_pkg(ctx, cx, cy, 1.0, a, t, reveal=1)
        tag(ctx, cx, cy - 370, 'THE MOAT = CUDA SOFTWARE', R['teal'], a, 32, align='c')
        rr = random.Random(7)
        for k in range(140):
            ang = rr.uniform(0, 2*math.pi); d = rr.uniform(400, 520)
            px, py = cx + math.cos(ang + t*.05)*d*1.3, cy + math.sin(ang + t*.05)*d*.8
            if 100 < py < 900: rgba(ctx, R['coral'], a*.7); ctx.arc(px, py, 6, 0, 2*math.pi); ctx.fill()
        txt(ctx, 'MILLIONS OF DEVELOPERS', 300, 880, 26, R['coral'], a, 'bold', 'c', mono=True)
    ctx.restore()
s_alex.bg = 'sheet'

# ---------- 2016 -> 2022 -> 2025 ----------
def s_rise(ctx, t, D):
    bg_sheet(ctx); a_out = outro(t, D)
    cable(ctx, t, 'FROM A SMALL LAB TO $5 TRILLION', a_out, core.EP)
    stops = [(-210., 'In 2016'), (940., 'After ChatGPT'), (2140., 'And on the twenty-ninth')]
    cx = -210.
    for x_, cue in stops: cx = lerp(cx, x_, ease(seg(t, Ts(cue) - .6, Ts(cue) + .6)))
    ctx.save(); ctx.translate(-cx, 0)
    rgba(ctx, R['char'], a_out); ctx.rectangle(-200, 700, 3600, 6); ctx.fill()
    # 2016: a van delivers a box to a small lab
    t1 = T('In 2016')
    inktext(ctx, '2016', 300, 820, 80, R['teal'], fadein(t, t1 - .3)*a_out, second=R['coral'])
    vx = lerp(-100, 620, eoc(seg(t, t1 + .2, T('San Francisco') + .3)))
    riso(ctx, lambda: rrect(ctx, vx, 560, 220, 120, 14), R['coral'], a_out, second=R['teal'])
    riso(ctx, lambda: rrect(ctx, vx + 160, 590, 70, 60, 8), R['paper'], a_out)
    for wx in (vx + 50, vx + 170):
        riso(ctx, lambda: ctx.arc(wx, 690, 24, 0, 2*math.pi), R['char'], a_out)
    txt(ctx, 'DGX-1', vx + 80, 630, 26, R['paper'], a_out, 'black', 'c')
    riso(ctx, lambda: ctx.rectangle(880, 450, 300, 250), R['over'], a_out)
    riso(ctx, lambda: (ctx.move_to(860, 450), ctx.line_to(1030, 360), ctx.line_to(1200, 450), ctx.close_path()), R['char'], a_out)
    for k in range(3): rgba(ctx, R['paper'], a_out); ctx.rectangle(910 + k*90, 500, 50, 50); ctx.fill()
    to = T('That lab was OpenAI'); q = seg(t, to + .5, to + 1.0)
    tag(ctx, 1030, 330, 'A SMALL LAB · SAN FRANCISCO' if q <= 0 else 'OPENAI', R['char'] if q <= 0 else R['coral'], a_out, 30 if q <= 0 else 40, align='c')
    if q > 0:
        rgba(ctx, R['coral'], (1 - q)*a_out); ctx.set_line_width(6); ctx.arc(1030, 330, 60 + 200*q, 0, 2*math.pi); ctx.stroke()
    # 2022: ChatGPT bubble
    t2 = T('After ChatGPT'); q = seg(t, t2, t2 + .6)
    if q > 0:
        qa = ease(q*2)*a_out
        inktext(ctx, '30 NOV 2022', 1700, 820, 64, R['teal'], qa, second=R['coral'])
        riso(ctx, lambda: rrect(ctx, 1640, 420, 520, 180, 40), R['teal'], qa, second=R['coral'])
        txt(ctx, 'ChatGPT', 1900, 530, 64, R['paper'], qa, 'black', 'c')
        # demand: many hands reaching for chips
        for k in range(14):
            rr = random.Random(k); ang = rr.uniform(-2.6, -.5)
            r0 = 150 + 120*ease(seg(t, t2 + .6 + k*.05, t2 + 1.2 + k*.05))
            riso(ctx, lambda: ctx.arc(1900 + math.cos(ang)*r0*1.8, 330 + math.sin(ang)*r0*.6, 14, 0, 2*math.pi), R['coral'], qa*.8)
        txt(ctx, 'THE WORLD WANTS NVIDIA CHIPS', 1900, 680, 24, R['char'], qa, 'bold', 'c', mono=True)
    # 2025: $5 trillion counter
    t3 = T('And on the twenty-ninth'); q = seg(t, t3, t3 + .5)
    if q > 0:
        qa = ease(q*2)*a_out
        inktext(ctx, '29 OCT 2025', 3100, 820, 64, R['coral'], qa, second=R['teal'])
        v = 5*eoc(seg(t, T('five trillion') - 1.2, T('five trillion') + .2))
        inktext(ctx, f'${v:.1f}', 3100, 520, 230, R['teal'], qa, align='c', second=R['coral'])
        inktext(ctx, 'TRILLION', 3100, 630, 90, R['char'], qa, align='c')
        bq = seg(t, T('first company ever'), T('first company ever') + .4)
        if bq > 0:
            ctx.save(); ctx.translate(3100, 300); ctx.rotate(-.05); ctx.scale(eob(bq, 2), eob(bq, 2))
            tag(ctx, 0, 0, 'FIRST COMPANY EVER', R['coral'], ease(bq*2)*qa, 36, align='c'); ctx.restore()
    ctx.restore()
s_rise.bg = 'sheet'

# ---------- Sanand on the official map ----------
SANAND_PX = (198, 782)
def s_sanand(ctx, t, D):
    bg_board(ctx); a_out = outro(t, D)
    cable(ctx, t, "INDIA'S LINK · SANAND, GUJARAT", a_out, core.EP)
    mh = 900; mcx, mcy = 760, 560
    fx, fy = map_point(mcx, mcy, mh, *SANAND_PX)
    z = lerp(1.0, 2.3, ease(seg(t, .3, 3.2)))
    ctx.save(); ctx.translate(lerp(fx, 760, ease(seg(t, .3, 3.2))), lerp(fy, 560, ease(seg(t, .3, 3.2)))); ctx.scale(z, z); ctx.translate(-fx, -fy)
    india_map(ctx, mcx, mcy, mh, fadein(t, 0, .5)*a_out)
    pq = seg(t, T('Sanand') - .3, T('Sanand') + .3)
    if pq > 0:
        for k in range(2):
            rp = seg(t, T('Sanand') + k*.6, T('Sanand') + 1.6 + k*.6)
            rgba(ctx, R['coral'], (1 - rp)*a_out); ctx.set_line_width(3/z); ctx.arc(fx, fy, (14 + 70*rp)/z*1.4, 0, 2*math.pi); ctx.stroke()
        riso(ctx, lambda: ctx.arc(fx, fy, 12*eob(pq, 2)/z*1.5, 0, 2*math.pi), R['coral'], a_out)
    ctx.restore()
    txt(ctx, 'MAP: SURVEY OF INDIA (OFFICIAL DEPICTION)', W - 70, 140, 18, R['grey'], a_out, mono=True, align='r')
    tq = seg(t, T('Sanand') + .2, T('Sanand') + .7)
    if tq > 0:
        qa = ease(tq*2)*a_out
        ctx.save(); ctx.translate(1380, 400); ctx.scale(eob(tq, 1.6), eob(tq, 1.6))
        riso(ctx, lambda: rrect(ctx, -400, -230, 800, 470, 20), R['paper'], qa)
        rgba(ctx, R['char'], qa); ctx.set_line_width(3); rrect(ctx, -400, -230, 800, 470, 20); ctx.stroke()
        from engine.brief import _icon
        _icon(ctx, 'factory', -250, -60, t, qa, R['teal'])
        txt(ctx, 'MICRON · SANAND', -100, -130, 40, R['teal'], qa, 'black')
        txt(ctx, 'INAUGURATED 28 FEB 2026', -100, -80, 24, R['char'], qa, 'bold', mono=True)
        lines = [('FIRST PROJECT APPROVED UNDER', 'first project approved'), ('THE INDIA SEMICONDUCTOR MISSION', 'first project approved'), ('ASSEMBLES + TESTS MEMORY CHIPS', 'assembles and tests')]
        for k, (l, cue) in enumerate(lines):
            txt(ctx, l, -100, -10 + k*44, 24, R['char'], ease(seg(t, Ts(cue), Ts(cue) + .4))*qa, 'bold', mono=True)
        ctx.restore()
    # spies are interested: an eye opens
    eq = seg(t, T('spies are interested') - .2, T('spies are interested') + .5)
    if eq > 0:
        ea = ease(eq*2)*a_out; op = eob(eq, 1.5)
        ctx.save(); ctx.translate(1380, 800)
        riso(ctx, lambda: (ctx.move_to(-150, 0), ctx.curve_to(-60, -80*op, 60, -80*op, 150, 0), ctx.curve_to(60, 80*op, -60, 80*op, -150, 0)), R['char'], ea)
        riso(ctx, lambda: ctx.arc(10*math.sin(t*2), 0, 40*op, 0, 2*math.pi), R['coral'], ea)
        ctx.restore()
s_sanand.bg = 'board'

# ---------- honey trap: definition ----------
def s_define(ctx, t, D):
    bg_sheet(ctx); a_out = outro(t, D)
    halftone(ctx, lambda: ctx.rectangle(0, 0, W, H), R['coralpale'], .5*a_out, step=14, r=2.4)
    v = cairo.RadialGradient(W/2, H/2, 380, W/2, H/2, 1150); v.add_color_stop_rgba(0, 0, 0, 0, 0); v.add_color_stop_rgba(1, .1, .09, .1, .75*a_out)
    ctx.set_source(v); ctx.paint()
    cable(ctx, t, 'CHAPTER 5 · THE HONEY TRAP', a_out, core.EP)
    ctx.save(); camera(ctx, t, D, (1.0, 1.06), cy=520)
    # a heart-shaped key slides into a lock
    a = fadein(t, .3, .6)*a_out
    lx, ly = 1400, 520
    riso(ctx, lambda: rrect(ctx, lx - 150, ly - 40, 300, 270, 30), R['grey'], a)
    ctx.save(); rgba(ctx, R['grey'], a); ctx.set_line_width(36); ctx.arc(lx, ly - 40, 110, math.pi, 0); ctx.stroke(); ctx.restore()
    riso(ctx, lambda: (ctx.arc(lx, ly + 60, 26, 0, 2*math.pi), ctx.move_to(lx - 14, ly + 70), ctx.line_to(lx + 14, ly + 70), ctx.line_to(lx + 8, ly + 150), ctx.line_to(lx - 8, ly + 150), ctx.close_path()), R['char'], a)
    kp = eoc(seg(t, T('using a romantic') - .5, T('using a romantic') + 1.4))
    kx = lerp(500, lx - 70, kp)
    def heart(cx, cy, s):
        ctx.move_to(cx, cy + 30*s)
        ctx.curve_to(cx - 70*s, cy - 20*s, cx - 40*s, cy - 80*s, cx, cy - 40*s)
        ctx.curve_to(cx + 40*s, cy - 80*s, cx + 70*s, cy - 20*s, cx, cy + 30*s); ctx.close_path()
    hb = 1 + .06*math.sin(t*7)
    riso(ctx, lambda: heart(kx - 120, ly + 90, 1.3*hb), R['coral'], a, second=R['violet'] if False else R['teal'])
    riso(ctx, lambda: rrect(ctx, kx - 70, ly + 78, 150, 22, 6), R['coral'], a)
    for k in range(3): riso(ctx, lambda: ctx.rectangle(kx + 30 + k*22, ly + 98, 12, 18 + 8*(k % 2)), R['coral'], a)
    if kp >= 1:
        sh = seg(t, T('using a romantic') + 1.4, T('using a romantic') + 1.8)
        rgba(ctx, R['coral'], (1 - sh)*a); ctx.set_line_width(6); ctx.arc(lx, ly + 90, 60 + 200*sh, 0, 2*math.pi); ctx.stroke()
    # definition
    q = seg(t, T('A honey trap is'), T('A honey trap is') + .5)
    if q > 0:
        qa = ease(q*2)*a_out
        inktext(ctx, 'HONEY', 150, 360, 150, R['coral'], qa, settle=eoc(q), second=R['teal'])
        inktext(ctx, 'TRAP', 150, 510, 150, R['char'], qa, settle=eoc(q), second=R['coral'])
        para(ctx, 'An old intelligence tactic: using a romantic relationship to gain access to, or leverage over, someone powerful.', 150, 610, 34, R['char'], 820, ease(seg(t, T('an old intelligence'), T('an old intelligence') + .5))*a_out, weight='bold')
    ctx.restore()
s_define.bg = 'sheet'

# ---------- honey trap: the reported timeline, as a case board ----------
CASE = [  # (x, y, date, head, lines, cue, kind)
    (330, 360, 'JUNE 2024 · TAIPEI', 'Photographed together in a bar', ['Jensen Huang', 'Alice Huang (Huang Le)'], 'In June 2024', 'photo'),
    (1000, 330, 'ALICE HUANG · HUANG LE', 'Chinese citizen', ['Executive, Megaspeed', 'Not related to Jensen Huang'], 'also called Huang Le', 'person'),
    (1660, 380, 'MEGASPEED · SINGAPORE', 'Bought Nvidia chips', ['Rented out computing power'], 'a Singapore-based company', 'cloud'),
    (2330, 360, 'LATER IN 2024 · MALAYSIA', 'US officials grow suspicious', ['Nvidia equipment', 'still in its boxes'], 'Later in 2024', 'boxes'),
    (3000, 340, '29 OCT 2026 · NYT REPORT', 'US officials concluded:', ['"a Chinese intelligence asset"', 'REPORTED · NOT PROVEN'], 'On the twenty-ninth', 'paper'),
]
def case_board(first):
    def f(ctx, t, D):
        bg_board(ctx); a_out = outro(t, D)
        rgba(ctx, R['char'], .35*a_out); ctx.paint()
        cable(ctx, t, 'THE REPORTED TIMELINE', a_out, core.EP)
        # follow the newest card
        cx = CASE[first][0]
        for (x, y, d, h_, ls, cue, k) in CASE:
            tc = Ts(cue)
            if tc < 900: cx = lerp(cx, x, ease(seg(t, tc - .6, tc + .6)))
        ctx.save(); ctx.translate(W/2 - cx, 0)
        # string between cards
        vis = []
        for i, (x, y, d, h_, ls, cue, k) in enumerate(CASE):
            tc = Ts(cue); q = 1. if (tc >= 900 and i < first) else (seg(t, tc - .2, tc + .4) if tc < 900 else 0)
            vis.append(q)
        for i in range(len(CASE) - 1):
            if vis[i] > 0 and vis[i + 1] > 0:
                x0, y0 = CASE[i][0], CASE[i][1] - 40; x1, y1 = CASE[i + 1][0], CASE[i + 1][1] - 40
                p = min(vis[i + 1]*1.5, 1)
                rgba(ctx, R['coral'], .9*a_out); ctx.set_line_width(4)
                ctx.move_to(x0, y0); ctx.curve_to(x0 + 200, y0 + 80, x1 - 200, y1 + 80, lerp(x0, x1, p), lerp(y0, y1, p)); ctx.stroke()
        for i, (x, y, d, h_, ls, cue, k) in enumerate(CASE):
            q = vis[i]
            if q <= 0: continue
            qa = ease(q*2)*a_out; rot = (-.03, .025, -.02, .03, -.025)[i]
            ctx.save(); ctx.translate(x, y + 40*(1 - eob(q, 1.4))); ctx.rotate(rot)
            riso(ctx, lambda: rrect(ctx, -280, -40, 560, 520, 8), R['paper'], qa)
            riso(ctx, lambda: ctx.arc(0, -40, 16, 0, 2*math.pi), R['coral'], qa)
            # picture area
            riso(ctx, lambda: rrect(ctx, -240, 0, 480, 220, 6), R['mist'], qa)
            if k == 'photo':
                figure(ctx, -70, 200, 1.1, R['teal'], qa, t, seed=1); figure(ctx, 80, 200, 1.1, R['over'], qa, t, seed=2)
                rgba(ctx, R['char'], qa*.6); ctx.set_line_width(3); ctx.move_to(-240, 60); ctx.line_to(240, 60); ctx.stroke()
            elif k == 'person':
                figure(ctx, 0, 210, 1.3, R['over'], qa, t, seed=4)
            elif k == 'cloud':
                for m in range(6):
                    on = .5 + .5*math.sin(t*6 + m)
                    riso(ctx, lambda: rrect(ctx, -200 + m*68, 70, 50, 120, 6), mix(R['tealpale'], R['teal'], on), qa)
            elif k == 'boxes':
                for m in range(6):
                    bx = -210 + (m % 3)*140; by = 80 + (m//3)*70
                    riso(ctx, lambda: rrect(ctx, bx, by, 120, 62, 4), R['coralpale'], qa, seed=m)
                    rgba(ctx, R['coral'], qa); ctx.rectangle(bx + 52, by, 16, 62); ctx.fill()
            elif k == 'paper':
                for m in range(6): rgba(ctx, R['grey'], qa); ctx.rectangle(-210, 30 + m*30, 420 - (m % 3)*80, 12); ctx.fill()
                txt(ctx, 'THE NEW YORK TIMES', 0, 216, 18, R['char'], qa, 'bold', 'c', mono=True)
            txt(ctx, d, -240, 270, 24, R['coral'], qa, 'bold', mono=True)
            txt(ctx, h_, -240, 316, 30, R['char'], qa, 'bold')
            for j, l in enumerate(ls):
                bold = l.isupper()
                if bold: tag(ctx, -240, 370 + j*48, l, R['coral'], qa, 20)
                else: txt(ctx, l, -240, 370 + j*44, 28, R['char'], qa*.9)
            ctx.restore()
        ctx.restore()
        rgba(ctx, R['char'], .85*a_out); ctx.rectangle(0, 900, W, 50); ctx.fill()
        txt(ctx, 'SOURCE: REPORTS IN INDIAN PAPERS, CITING THE NEW YORK TIMES · ALLEGATIONS, NOT PROVEN · NO ONE CHARGED', W/2, 933, 20, R['paper'], a_out, 'bold', 'c', mono=True)
    return _bg(f, 'board')

# ---------- where each side stands: five equal cards ----------
SIDES = [
    ('NVIDIA', ['First: ordinary customer contact', 'Board, 8 Nov: "no reason to believe" secrets were compromised'], R['teal'], 'Nvidia first said', 'and the board said'),
    ('HUANG, TO STAFF', ['8 Nov: "I was unfaithful to my wife"'], R['over'], 'Huang wrote to staff', None),
    ('CHINA', ['Foreign Ministry: groundless slander'], R['coral'], "China's Foreign Ministry", None),
    ('MEGASPEED', ['Says it is investigating'], R['teal'], 'Megaspeed says', None),
    ('SINGAPORE', ['Did not investigate her over intelligence links'], R['over'], 'Singapore says', None),
]
def five_sides(ctx, t, D):
    bg_sheet(ctx); a_out = outro(t, D)
    cable(ctx, t, 'WHERE EACH SIDE STANDS', a_out, core.EP)
    ctx.save(); camera(ctx, t, D, (1.0, 1.03), cy=500)
    cw, gap = 334, 22; x0 = W/2 - (5*cw + 4*gap)/2
    for i, (head, lines, ink, cue, cue2) in enumerate(SIDES):
        tc = Ts(cue); q = 1. if tc >= 900 and i < 2 else (seg(t, tc - .1, tc + .5) if tc < 900 else 0)
        x = x0 + i*(cw + gap); y = 180 + 50*(1 - eob(q, 1.5))
        a = ease(q*1.6)*a_out
        riso(ctx, lambda: rrect(ctx, x, y, cw, 640, 16), R['paper'] if q > 0 else R['mist'], a_out*(.4 if q <= 0 else 1)*fadein(t, 0, .3))
        if q <= 0: continue
        rgba(ctx, ink, a); ctx.set_line_width(4); rrect(ctx, x, y, cw, 640, 16); ctx.stroke()
        riso(ctx, lambda: rrect(ctx, x, y, cw, 80, 16), ink, a, seed=i)
        txt(ctx, head, x + cw/2, y + 52, 26 if len(head) < 12 else 22, R['paper'], a, 'black', 'c')
        figure(ctx, x + cw/2, y + 250, .8, ink, a, t, gesture=seg(t, tc + .4, tc + 1.1) if tc < 900 else 1, seed=i)
        podium(ctx, x + cw/2, y + 300, a)
        yy = y + 370
        for j, l in enumerate(lines):
            lc = tc if j == 0 else (Ts(cue2) if cue2 else tc)
            la = ease(seg(t, lc + .3, lc + .8))*a_out if lc < 900 else a_out
            nl = para(ctx, l, x + cw/2, yy, 25, R['char'], cw - 40, la, weight='bold' if j == 0 else 'reg', align='c')
            yy += nl*33 + 24
    nq = seg(t, Ts('no one has been charged') - .2, Ts('no one has been charged') + .4)
    if nq > 0:
        ctx.save(); ctx.translate(W/2, 880); ctx.rotate(-.02); ctx.scale(eob(nq, 1.8), eob(nq, 1.8))
        tag(ctx, 0, 0, 'NOTHING PROVEN · NO ONE CHARGED', R['char'], ease(nq*2)*a_out, 34, align='c'); ctx.restore()
    ctx.restore()
five_sides.bg = 'sheet'

# ---------- the AI buildout ----------
def s_buildout(ctx, t, D):
    bg_sheet(ctx); a_out = outro(t, D)
    cable(ctx, t, 'CHAPTER 6 · THE FALLOUT', a_out, core.EP)
    ctx.save(); camera(ctx, t, D, (1.0, 1.05), cy=600)
    a = fadein(t, .3, .5)*a_out
    # data-centre racks rising
    for k in range(14):
        h = 120 + (k*37 % 5)*45
        g = eob(seg(t, .5 + k*.12, 1.3 + k*.12), 1.3)
        x = 120 + k*120
        riso(ctx, lambda: rrect(ctx, x, 820 - h*g, 96, h*g, 6), R['char'] if k % 3 else R['over'], a, seed=k)
        for m in range(int(h*g/30)):
            on = (math.sin(t*6 + k*1.7 + m*2.3) > .2)
            rgba(ctx, R['teal'] if on else R['grey'], a); ctx.rectangle(x + 14, 830 - h*g + m*30, 10, 8); ctx.fill()
            rgba(ctx, R['coral'] if (math.sin(t*4 + m + k) > .6) else R['grey'], a); ctx.rectangle(x + 32, 830 - h*g + m*30, 50, 4); ctx.fill()
    # crane
    rgba(ctx, R['coral'], a); ctx.set_line_width(8); ctx.move_to(1640, 820); ctx.line_to(1640, 260); ctx.line_to(1300, 260); ctx.stroke()
    hy = 300 + 150*(.5 + .5*math.sin(t*.8)); ctx.set_line_width(3); ctx.move_to(1380, 260); ctx.line_to(1380, hy); ctx.stroke()
    riso(ctx, lambda: rrect(ctx, 1340, hy, 80, 50, 4), R['char'], a)
    inktext(ctx, 'THE AI', 140, 240, 110, R['teal'], ease(seg(t, .4, .9))*a_out, second=R['coral'])
    inktext(ctx, 'BUILDOUT', 140, 360, 110, R['coral'], ease(seg(t, .6, 1.1))*a_out, second=R['teal'])
    bq = seg(t, T('on both sides') - .2, T('on both sides') + .4)
    if bq > 0:
        ctx.save(); ctx.translate(1000, 300); ctx.rotate(-.04); ctx.scale(eob(bq, 2), eob(bq, 2))
        tag(ctx, 0, 0, 'PRESSURE  vs  CUSHION', R['char'], ease(bq*2)*a_out, 40, align='c'); ctx.restore()
    ctx.restore()
s_buildout.bg = 'sheet'

PRESS = [('SHARES SLID', 'Nvidia\'s shares slid', 'build2'), ('ABOUT $270 BN AT RISK', 'two hundred and seventy', 'build2'), ('REVIEW COULD DELAY PLANS', 'others warned', 'build2'),
         ('HOUSE CHAIRS CALL HUANG', 'Three House committee', 'build3'), ('PRESSURE ON EXPORT RULES', 'tighten export rules', 'build3'), ('REMOTE-RENTAL LOOPHOLE', 'including the loophole', 'build3')]
CUSH = [('HARD TO REPLACE', 'hard to replace', 'build4'), ('S. KOREA: NO DELIVERY DISRUPTION', "South Korea's government", 'build4'), ('TSMC · SAMSUNG · SK HYNIX SHARES ROSE', 'And on Monday', 'build4')]
ORDER = ['build2', 'build3', 'build4']
def scale_scene(me):
    def f(ctx, t, D):
        bg_sheet(ctx); a_out = outro(t, D)
        cable(ctx, t, 'WHAT IT MEANS FOR THE AI BUILDOUT', a_out, core.EP)
        ctx.save(); camera(ctx, t, D, (1.0, 1.03), cy=520)
        mi = ORDER.index(me)
        def prog(cue, beat):
            bi = ORDER.index(beat)
            if bi < mi: return 1.
            if bi > mi: return 0.
            return seg(t, Ts(cue) - .1, Ts(cue) + .5)
        pl = [prog(c, b) for _, c, b in PRESS]; cu = [prog(c, b) for _, c, b in CUSH]
        wl = sum(min(1, p*2) for p in pl); wr = sum(min(1, p*2) for p in cu)*2   # cushion items weigh more each so the beam settles
        ang = .11*math.tanh((wl - wr)/3) + .01*math.sin(t*1.7)
        px, py = W/2, 330
        # stand
        riso(ctx, lambda: (ctx.move_to(px - 120, 860), ctx.line_to(px + 120, 860), ctx.line_to(px + 14, py), ctx.line_to(px - 14, py), ctx.close_path()), R['char'], a_out)
        ctx.save(); ctx.translate(px, py); ctx.rotate(-ang)
        riso(ctx, lambda: rrect(ctx, -580, -10, 1160, 20, 10), R['char'], a_out)
        ctx.restore()
        for side, (items, prog_, ink, name) in enumerate(((PRESS, pl, R['coral'], 'PRESSURE'), (CUSH, cu, R['teal'], 'CUSHION'))):
            sx = -560 if side == 0 else 560
            ex = px + sx*math.cos(ang); ey = py - sx*math.sin(ang)*(1 if side == 0 else 1)
            ey = py - sx*math.sin(ang)
            rgba(ctx, R['char'], a_out); ctx.set_line_width(3)
            ctx.move_to(ex, ey); ctx.line_to(ex - 220, ey + 140); ctx.move_to(ex, ey); ctx.line_to(ex + 220, ey + 140); ctx.stroke()
            riso(ctx, lambda: rrect(ctx, ex - 260, ey + 140, 520, 26, 10), ink, a_out)
            txt(ctx, name, ex, ey + 210, 34, ink, a_out, 'black', 'c')
            # items stack as cards above the pan
            k = 0
            for (lab, cue, b), p in zip(items, prog_):
                if p <= 0: continue
                col, row = (k % 2, k//2) if len(items) > 3 else (0, k); k += 1
                xo = (-150 + 300*col) if len(items) > 3 else 0
                yy = ey + 110 - row*48 - 300*(1 - eob(min(p*1.4, 1), 1.3))
                tag(ctx, ex + xo, yy, lab, ink, ease(min(p*2, 1))*a_out, 17, align='c')
        if me == 'build2':
            v = 270*eoc(seg(t, T('two hundred and seventy') - 1.0, T('two hundred and seventy') + .3))
            if v > 0:
                inktext(ctx, f'${int(v)} BN', W/2, 230, 110, R['coral'], ease(seg(t, T('two hundred and seventy') - 1.0, T('two hundred and seventy') - .6))*a_out, align='c', second=R['teal'])
                txt(ctx, 'AT RISK AT MONDAY\'S LOW · FRANKFURT TRADING · LSEG DATA', W/2, 280, 22, R['char'], a_out, 'bold', 'c', mono=True)
        ctx.restore()
    return _bg(f, 'sheet')

def s_rules(ctx, t, D):
    bg_sheet(ctx); a_out = outro(t, D)
    cable(ctx, t, 'THE REAL QUESTION', a_out, core.EP)
    ctx.save(); camera(ctx, t, D, (1.0, 1.08), cy=520)
    q = seg(t, .3, .8)
    inktext(ctx, 'NOT WHETHER AI NEEDS THESE CHIPS', W/2, 330, 72, R['grey'], ease(q*2)*a_out*(1 - .5*seg(t, T("It's who gets them") - .2, T("It's who gets them") + .3)), align='c')
    for i, (s, cue, ink) in enumerate((('WHO GETS THEM', "It's who gets them", R['teal']), ('ON WHOSE RULES', 'on whose rules', R['coral']))):
        p = seg(t, Ts(cue) - .1, Ts(cue) + .3)
        if p <= 0: continue
        sc = lerp(1.9, 1, eob(p, 1.3))
        ctx.save(); ctx.translate(W/2, 520 + i*170); ctx.scale(sc, sc)
        inktext(ctx, s, 0, 0, 150, ink, ease(p*2)*a_out, settle=eoc(p), seed=i, align='c', second=R['coral'] if ink == R['teal'] else R['teal'])
        ctx.restore()
    ctx.restore()
s_rules.bg = 'sheet'

# ---------- relations web end card ----------


# ---------- memory tip without the series passport: four letter tiles ----------
MICE = [('M', 'MONEY', 'Money'), ('I', 'IDEOLOGY', 'Ideology'), ('C', 'COMPROMISE', 'Compromise'), ('E', 'EGO', 'Ego')]
def s_mice(ctx, t, D):
    bg_sheet(ctx); a_out = outro(t, D)
    cable(ctx, t, 'MEMORY TIP · FOR ANY ESPIONAGE QUESTION', a_out, core.EP)
    ctx.save(); camera(ctx, t, D, (1.0, 1.04), cy=520)
    w, gap = 360, 50; x0 = W/2 - (4*w + 3*gap)/2
    tc = Ts('through the C')
    for i, (L, word, cue) in enumerate(MICE):
        t0 = Ts(cue) - .15 if i else Ts('MICE') - .1
        q = seg(t, t0, t0 + .5)
        if q <= 0: continue
        hot = i == 2 and t > tc
        x = x0 + i*(w + gap); y = 230
        fl = abs(math.cos(math.pi*min(1, q)*.5 + math.pi*.5)) if q < 1 else 1
        s_ = eob(q, 1.7)*(1 + .06*ease(seg(t, tc, tc + .4)) if i == 2 else eob(q, 1.7))
        ctx.save(); ctx.translate(x + w/2, y + 230); ctx.scale(s_*max(fl, .05), s_); ctx.translate(-(x + w/2), -(y + 230))
        ink = R['coral'] if hot else (R['teal'] if i % 2 == 0 else R['over'])
        riso(ctx, lambda: rrect(ctx, x, y, w, 460, 22), ink, ease(q*2)*a_out, seed=i)
        inktext(ctx, L, x + w/2, y + 290, 280, R['paper'], ease(q*2)*a_out, align='c')
        txt(ctx, word, x + w/2, y + 400, 36 if len(word) < 9 else 30, R['paper'], ease(seg(t, Ts(cue), Ts(cue) + .4))*a_out, 'black', 'c')
        ctx.restore()
    lq = seg(t, Ts('These are the four'), Ts('These are the four') + .5)
    if lq > 0: txt(ctx, 'THE FOUR CLASSIC LEVERS USED TO TURN A TARGET', W/2, 790, 30, R['char'], ease(lq)*a_out, 'bold', 'c', mono=True)
    hq = seg(t, tc + .2, tc + .6)
    if hq > 0:
        ctx.save(); ctx.translate(x0 + 2*(w + gap) + w/2, 170); ctx.rotate(-.04); ctx.scale(eob(hq, 2), eob(hq, 2))
        tag(ctx, 0, 0, 'HONEY TRAP = C', R['coral'], ease(hq*2)*a_out, 34, align='c'); ctx.restore()
    ctx.restore()
s_mice.bg = 'sheet'

# ---------- closing card without the series relations web ----------
from engine.web import subscribe_card
def s_close(ctx, t, D):
    bg_sheet(ctx); a_out = outro(t, D, .8)
    cable(ctx, t, 'SPECIAL 1 · AS OF 9 NOV 2026', a_out, core.EP)
    ctx.save(); camera(ctx, t, D, (1.0, 1.05), cy=480)
    chip_pkg(ctx, 1460, 430, 1.25, fadein(t, .2, .6)*a_out, t, reveal=1)
    items = [('THE MAN', R['teal']), ('THE MACHINE', R['coral']), ('THE MEMORY WALL', R['over']), ('THE HONEY TRAP', R['coral']), ('THE FALLOUT', R['teal'])]
    for i, (s_, ink) in enumerate(items):
        q = seg(t, .3 + i*.18, .8 + i*.18)
        if q > 0: tag(ctx, 160 + 60*(1 - eob(q)), 230 + i*96, f'0{i+1}  ' + s_, ink, ease(q*2)*a_out, 34)
    ctx.restore()
    tn = Ts('Next briefing'); nq = seg(t, tn, tn + .6)
    if nq > 0:
        a = ease(nq)*a_out
        riso(ctx, lambda: rrect(ctx, 0, 830, W*eoc(nq), 90, 0), R['char'], a)
        txt(ctx, 'NEXT BRIEFING  ·  SEMICONDUCTORS AND SPACE DIPLOMACY', 80, 888, 34, R['paper'], a, 'bold', mono=True)
    subscribe_card(ctx, t, Ts('subscribe'), a_out, x=1540, y=700)
s_close.bg = 'sheet'

# ---------- beats ----------
SC = {
 'hook': headline([('BOARD PROBES', R['teal']), ('ITS FOUNDER', R['coral'])], 'NVIDIA · 8 NOV 2026',
                  question=('A so-called honey trap?', 'a so-called honey trap'), motif=_motif_hook),
 'qs': s_qs,
 'life1': chapter(life_strip((0, 3)), 1, 'THE MAN', 'From cleaning bathrooms in Kentucky to founding Nvidia'),
 'life2': life_strip((3, 6)),
 'life3': s_booth,
 'gpu1': chapter(gpu_workers('A CPU', 'A GPU, a graphics', 'all work at the same time', 'CHAPTER 2 · THE MACHINE'), 2, 'THE MACHINE', 'What a GPU is, and why AI needs one'),
 'gpu2': pixels('AI needs it too'),
 'gpu3': matrix_race('Engineers call this', 'Each sum is easy'),
 'gpu4': train_infer('Training is', 'Inference is'),
 'gpu5': uses([('games', 'GAMES', 'games'), ('chat', 'CHATBOTS', 'chatbots'), ('weather', 'WEATHER', 'weather'), ('medicine', 'MEDICINE', 'medicines')]),
 'wave1': chapter(s_cuda, 3, 'THE WAVE', 'How a gaming-chip company came to rule AI'),
 'wave2': s_alex,
 'wave3': s_rise,
 'mem1': chapter(memory_wall('the memory wall'), 4, 'THE MEMORY WALL', 'Why SK Hynix, Samsung and Micron suddenly matter'),
 'mem2': dram_nand('DRAM is', 'power goes off', 'NAND flash'),
 'mem3': hbm_tower('Picture a tower', 'tiny vertical wires', 'right beside', 'Short distance'),
 'mem4': makers(['SK Hynix', 'Samsung', 'Micron'], 'Remember it as', 'and demand is so strong',
                'We still forecast that customer demand will remain higher than our supply capacity even beyond 2030.', 'SK HYNIX CEO KWAK NOH-JUNG · JULY 2026'),
 'chain1': supply_board([(380, 520, 'UNITED STATES', ['DESIGN · NVIDIA', 'MEMORY · MICRON'], R['coral'], 'Nvidia designs'),
                         (1500, 600, 'TAIWAN', ['MANUFACTURE · TSMC'], R['teal'], 'TSMC'),
                         (1420, 300, 'SOUTH KOREA', ['MEMORY · SK HYNIX · SAMSUNG'], R['over'], 'The memory comes')],
                        [(0, 1), (2, 1), (0, 2)]),
 'chain2': s_sanand,
 'trap1': chapter(s_define, 5, 'THE HONEY TRAP', 'What is alleged, by whom, and what each side says'),
 'trap2': case_board(0),
 'trap3': case_board(3),
 'trap4': five_sides,
 'trap5': five_sides,
 'build1': chapter(s_buildout, 6, 'THE FALLOUT', 'Does this slow the AI buildout?'),
 'build2': scale_scene('build2'),
 'build3': scale_scene('build3'),
 'build4': scale_scene('build4'),
 'build5': s_rules,
 'stake1': chapter(stakes([('chip', 'COMPUTE', 'IndiaAI: 45,000+ GPUs by June 2026', R['teal'], 'One: compute'),
                           ('factory', 'SANAND', 'Inside the memory supply chain', R['coral'], 999),
                           ('shield', 'SECURITY', 'Official Secrets Act, 1923: any person', R['over'], 999)]), 7, "INDIA'S STAKE", 'Compute, chips and security'),
 'stake2': stakes([('chip', 'COMPUTE', 'IndiaAI: 45,000+ GPUs by June 2026', R['teal'], -5),
                   ('factory', 'SANAND', 'Inside the memory supply chain', R['coral'], 'Two: manufacturing'),
                   ('shield', 'SECURITY', 'Official Secrets Act, 1923: any person', R['over'], 'And three: security')]),
 'tip': s_mice,
 'q1': statement(1, 'High Bandwidth Memory is made by stacking memory chips vertically and placing them right next to the processor.', 'TRUE', "That's how it beats the memory wall.", 'True.'),
 'q2': statement(2, 'CUDA is a chip made by Nvidia.', 'FALSE', 'CUDA is a software platform. That is the trap.', 'False.'),
 'q3': statement(3, "India's Official Secrets Act, 1923, applies only to government servants.", 'FALSE', 'It applies to any person.', 'False.'),
 'mains': mains('"Semiconductors have become instruments of geopolitics." Examine with reference to AI chips and India.',
                [('Why chips are strategic', 'AI runs on GPUs and memory; few makers, few countries'),
                 ('Export controls and espionage', 'Who gets chips, on whose rules; the risk of leaks'),
                 ("India's own capacity", 'IndiaAI compute · Micron Sanand · Semiconductor Mission')],
                ['why chips are strategic', 'how export controls', 'how India is building']),
 'watch': watch([("Huang's closed-door meeting with House committees", 'DATE TO BE CONFIRMED'),
                 ("Findings of Nvidia's board investigation", 'OPEN QUESTION'),
                 ('US rules on chip sales and remote access for China', 'OPEN QUESTION')],
                ['One:', 'Two:', 'And three:']),
 'end': s_close,
}
BEATS = [(k, n, SC[k]) for k, n in EN]

GROUPS = {'life1': 'life', 'life2': 'life', 'trap2': 'case', 'trap3': 'case', 'trap4': 'sides', 'trap5': 'sides',
          'build2': 'scale', 'build3': 'scale', 'build4': 'scale', 'stake1': 'stk', 'stake2': 'stk'}

KEYS = {
 'hook': [('independent investigation', 'BOARD PROBE · 8 NOV 2026', 'teal')],
 'life1': [('youngest pupil', 'AGE 9 · CLEANED BATHROOMS', 'coral')],
 'gpu1': [('thousands of simpler', 'THOUSANDS OF CORES', 'teal')],
 'gpu3': [('billions of times', 'BILLIONS OF TIMES', 'coral')],
 'gpu4': [('weeks', 'WEEKS OF TRAINING', 'coral')],
 'wave2': [('real moat', 'THE MOAT: SOFTWARE', 'teal')],
 'mem3': [('far more data', 'FAR MORE DATA PER SECOND', 'teal')],
 'mem4': [('Remember it as', 'KOREA ×2 · AMERICA ×1', 'violet')],
 'trap5': [('no one has been charged', 'NOT CHARGED', 'char')],
 'build2': [('two hundred and seventy', '~$270 BN', 'coral')],
 'stake1': [('forty-five thousand', '45,000+ GPUs', 'teal')],
 'q2': [("that's the trap", 'THE TRAP', 'coral')],
}

ANNOT = {
 'gpu1': [('all work at the same time', 'circle', 1410, 520, 820, 520)],
 'wave2': [('millions of developers', 'circle', 300, 870, 460, 70)],
 'mem3': [('right beside', 'arrow', 600, 300, 160, 200)],
 
 'q2': [("that's the trap", 'underline', 640, 640, 640, 0)],
 'chain2': [('assembles and tests', 'underline', 1280, 492, 470, 0)],
}

_order = [k for k, _ in EN]
FX = [('whoosh', k, -.25, .22) for i, k in enumerate(_order) if i and GROUPS.get(k, k) != GROUPS.get(_order[i-1], _order[i-1])]
FX += [('boom', k, .25, .55) for k in ('life1', 'gpu1', 'wave1', 'mem1', 'trap1', 'build1', 'stake1')]   # chapter slams (offset is from speech start)
FX += [('blip', k, ph, .16) for k, items in KEYS.items() for ph, _, _ in items]
FX += [('whoosh', k, ph, .06) for k, items in ANNOT.items() for ph, *_ in items]
FX += [('tick', 'hook', .15, .12), ('boom', 'hook', 'a so-called honey trap', .4),
       ('boom', 'wave3', 'five trillion', .45), ('ding', 'wave3', 'That lab was OpenAI', .25),
       ('stamp', 'mem1', 'the memory wall', .45), ('glitch', 'trap1', 'So, the allegation', .25),
       ('boom', 'build5', "It's who gets them", .45), ('riser', 'tip', 'MICE', .2), ('boom', 'tip', 'MICE', .4), ('ding', 'tip', 'through the C', .3),
       ('ding', 'q1', 'True.', .3), ('ding', 'q2', 'False.', .3), ('ding', 'q3', 'False.', .3), ('ding', 'end', 'subscribe', .2)]
