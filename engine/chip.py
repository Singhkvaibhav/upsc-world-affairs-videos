"""Chip and memory explainer scenes (GPUs, matrix maths, HBM, supply chain) in the riso briefing style.
Reusable for any episode on semiconductors. Each factory returns f(ctx, t, D) with .bg."""
import math, random, cairo
from engine import core
from engine.core import W, H, seg, ease, eoc, eob, lerp, T
from engine.riso import R, rgba, riso, halftone, rrect, txt, inktext, para, camera, pop, fadein, cable, credit, bg_sheet, bg_board, tw, wrap
from engine.brief import _bg, outro, tag, token, figure

def _c(x): return T(x) if isinstance(x, str) else x

def mix(c1, c2, k): return tuple(lerp(c1[i], c2[i], k) for i in range(3))

# ---------- props ----------
def chip_pkg(ctx, x, y, s, a, t, reveal=0., label='GPU'):
    """a chip package seen from above: pins, lid; reveal fades the lid to show a die full of cores"""
    if a <= 0: return
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    for k in range(9):
        for sgn in (-1, 1):
            rgba(ctx, R['grey'], a); ctx.rectangle(-112 + k*28, sgn*134 - 10, 12, 20); ctx.fill()
            ctx.rectangle(sgn*134 - 10, -112 + k*28, 20, 12); ctx.fill()
    riso(ctx, lambda: rrect(ctx, -125, -125, 250, 250, 16), R['char'], a)
    riso(ctx, lambda: rrect(ctx, -95, -95, 190, 190, 8), R['over'], a)
    # die cores
    n = 12; cs = 190/n
    for i in range(n):
        for j in range(n):
            on = .5 + .5*math.sin(t*5 + i*.7 + j*.45)
            rgba(ctx, mix(R['teal'], R['tealpale'], on), a*reveal)
            ctx.rectangle(-95 + i*cs + 1.5, -95 + j*cs + 1.5, cs - 3, cs - 3); ctx.fill()
    if reveal < 1:
        riso(ctx, lambda: rrect(ctx, -100, -100, 200, 200, 10), R['grey'], a*(1 - reveal))
        txt(ctx, label, 0, 14, 40, R['paper'], a*(1 - reveal), 'black', 'c')
    ctx.restore()

def core_grid(ctx, x, y, cols, rows, cell, gap, t, a, lit=0., wave_t=None, idle=.18):
    """thousands of small cores; lit 0..1 brings them all on, with a travelling shimmer"""
    for i in range(cols):
        for j in range(rows):
            sh = .5 + .5*math.sin(t*6 - i*.35 - j*.2)
            k = idle + (1 - idle)*lit*(.65 + .35*sh)
            rgba(ctx, mix(R['mist'], R['teal'], k), a)
            ctx.rectangle(x + i*(cell + gap), y + j*(cell + gap), cell, cell); ctx.fill()

def particles(ctx, path_fn, n, t, speed, a, ink, r=6, jam=0., seed=0):
    """dots travelling along path_fn(s)->(x, y); jam>0 bunches them up and slows them"""
    rr = random.Random(seed)
    for k in range(n):
        off = rr.random()
        v = speed*(1 - .85*jam)
        s = (off + t*v) % 1
        if jam > 0: s = s**(1 + 3*jam)*.82
        x, y = path_fn(s)
        rgba(ctx, ink, a*(.6 + .4*rr.random())); ctx.arc(x, y + rr.uniform(-8, 8)*(1 - jam*.5), r, 0, 2*math.pi); ctx.fill()

def panel(ctx, x, y, w, h, a, head=None, ink=None):
    riso(ctx, lambda: rrect(ctx, x, y, w, h, 18), R['paper'], a)
    rgba(ctx, R['char'], .8*a); ctx.set_line_width(3); rrect(ctx, x, y, w, h, 18); ctx.stroke()
    if head:
        riso(ctx, lambda: rrect(ctx, x, y, w, 70, 18), ink or R['teal'], a)
        txt(ctx, head, x + 28, y + 48, 32, R['paper'], a, 'black')

def net(ctx, x, y, w, h, t, a, p=1., glow=0.):
    """a small neural network: 4 layers of nodes with edges drawing in"""
    layers = [4, 6, 6, 3]
    pts = [[(x + li*w/(len(layers) - 1), y + (j + .5)*h/n) for j in range(n)] for li, n in enumerate(layers)]
    ctx.save(); ctx.set_line_width(2)
    for li in range(len(layers) - 1):
        q = seg(p, li/3, (li + 1)/3)
        for (x0, y0) in pts[li]:
            for (x1, y1) in pts[li + 1]:
                rgba(ctx, R['grey'], .5*a*q); ctx.move_to(x0, y0); ctx.line_to(lerp(x0, x1, q), lerp(y0, y1, q)); ctx.stroke()
    ctx.restore()
    for li, col in enumerate(pts):
        for j, (px, py) in enumerate(col):
            g = .5 + .5*math.sin(t*5 - li*1.2 + j)
            riso(ctx, lambda: ctx.arc(px, py, 13, 0, 2*math.pi), mix(R['teal'], R['coral'], glow*g), a*ease(seg(p, li/4, li/4 + .2)))

# ---------- scenes ----------
def gpu_workers(cpu_cue, gpu_cue, all_cue, title='WHAT IS A GPU?'):
    def f(ctx, t, D):
        bg_sheet(ctx); a_out = outro(t, D)
        cable(ctx, t, title, a_out, core.EP)
        # 1) fly into a chip
        fi = seg(t, .2, 3.0); fa = (1 - ease(seg(t, 2.6, 3.3)))*a_out
        if fa > 0:
            z = lerp(.7, 4.2, ease(fi)**1.6)
            chip_pkg(ctx, W/2, 540, z, fa*fadein(t, .1, .4), t, reveal=ease(seg(t, .9, 2.0)))
        sa = ease(seg(t, 2.9, 3.6))*a_out
        if sa <= 0: return
        ctx.save(); camera(ctx, t, D, (1.0, 1.035), cy=520)
        tc, tg, ta = _c(cpu_cue), _c(gpu_cue), _c(all_cue)
        # CPU side
        qa = ease(seg(t, max(tc, 3), max(tc, 3) + .6))*sa
        if qa > 0:
            panel(ctx, 110, 170, 760, 640, qa, 'CPU', R['coral'])
            for k in range(4):
                cx, cy = 230 + (k % 2)*300, 300 + (k//2)*230
                active = int((t*1.1) % 4) == k
                riso(ctx, lambda: rrect(ctx, cx, cy, 220, 180, 14), R['coral'] if active else R['coralpale'], qa, seed=k)
                figure(ctx, cx + 110, cy + 150, .7, R['char'] if active else R['grey'], qa, t, gesture=1 if active else 0, seed=k)
                if active:
                    pr = (t*1.1) % 1
                    riso(ctx, lambda: rrect(ctx, cx + 20, cy + 16, 180*pr, 14, 6), R['paper'], qa)
            txt(ctx, 'A FEW CLEVER WORKERS · ONE JOB AFTER ANOTHER', 490, 780, 24, R['char'], qa, 'bold', 'c', mono=True)
        # GPU side
        qg = ease(seg(t, max(tg, 3), max(tg, 3) + .6))*sa
        if qg > 0:
            panel(ctx, 1010, 170, 800, 640, qg, 'GPU', R['teal'])
            lit = ease(seg(t, ta, ta + .5))
            core_grid(ctx, 1050, 270, 46, 28, 12, 4, t, qg, lit=lit)
            txt(ctx, 'THOUSANDS OF WORKERS · ALL AT ONCE', 1410, 780, 24, R['char'], qg, 'bold', 'c', mono=True)
        ctx.restore()
    return _bg(f, 'sheet')

def _scene_px(i, j, cols, rows, t):
    """colour of one pixel in a little animated landscape"""
    u, v = i/cols, j/rows
    sx, sy = .25 + .5*((t*.08) % 1), .3
    if (u - sx)**2*3 + (v - sy)**2*5 < .012: return R['coral']
    hill = .62 + .08*math.sin(u*9 + 1) + .05*math.sin(u*23)
    if v > hill + .12: return R['teal']
    if v > hill: return R['tealpale']
    return mix(R['paper'], R['coralpale'], v*1.2)

def pixels(ai_cue):
    def f(ctx, t, D):
        bg_sheet(ctx); a_out = outro(t, D)
        cable(ctx, t, 'WHY GRAPHICS NEEDED IT', a_out, core.EP)
        ctx.save(); camera(ctx, t, D, (1.0, 1.04), cy=520)
        a = fadein(t, .2, .5)*a_out
        mx, my, mw, mh = 140, 190, 980, 560
        riso(ctx, lambda: rrect(ctx, mx - 24, my - 24, mw + 48, mh + 48, 22), R['char'], a)
        riso(ctx, lambda: rrect(ctx, mx + mw/2 - 60, my + mh + 24, 120, 70, 4), R['char'], a)
        cols, rows = 49, 28; cw, ch = mw/cols, mh/rows
        p = seg(t, .8, 1.3)
        frame_t = math.floor(t*6)/6       # the whole picture refreshes at once, many times a second
        for i in range(cols):
            for j in range(rows):
                c = _scene_px(i, j, cols, rows, frame_t) if p > 0 else R['char']
                rgba(ctx, c, a*(.25 + .75*ease(p)) if p > 0 else a); ctx.rectangle(mx + i*cw + .6, my + j*ch + .6, cw - 1.2, ch - 1.2); ctx.fill()
        if p > 0: tag(ctx, mx + mw/2, my - 60, 'EVERY PIXEL, AT ONCE', R['teal'], ease(p)*a, 26, align='c')
        tc = _c(ai_cue); q = seg(t, tc, tc + 1.4)
        if q > 0:
            qa = ease(q*2)*a_out
            net(ctx, 1320, 260, 420, 420, t, qa, p=ease(q), glow=1)
            tag(ctx, 1530, 760, 'AI: THE SAME KIND OF MATHS', R['coral'], qa, 26, align='c')
            ctx.save(); ctx.set_line_width(8); rgba(ctx, R['coral'], qa); ctx.set_line_cap(cairo.LINE_CAP_ROUND)
            ctx.move_to(1150, 470); ctx.line_to(1150 + 110*eoc(q), 470); ctx.stroke(); ctx.restore()
        ctx.restore()
    return _bg(f, 'sheet')

def matrix_race(par_cue, go_cue):
    def f(ctx, t, D):
        bg_sheet(ctx); a_out = outro(t, D)
        cable(ctx, t, 'THE MATHS INSIDE AI', a_out, core.EP)
        ctx.save(); camera(ctx, t, D, (1.0, 1.03), cy=520)
        a = fadein(t, .2, .5)*a_out
        rr = random.Random(4)
        A = [[rr.randint(1, 9) for _ in range(4)] for _ in range(4)]
        B = [[rr.randint(1, 9) for _ in range(4)] for _ in range(4)]
        Cm = [[sum(A[i][k]*B[k][j] for k in range(4)) for j in range(4)] for i in range(4)]
        def grid(x, y, M, ink, s=46, show=None, pulse=0):
            for i in range(4):
                for j in range(4):
                    on = 1 if show is None else show(i, j)
                    riso(ctx, lambda: rrect(ctx, x + j*(s + 6), y + i*(s + 6), s, s, 6), mix(R['mist'], ink, .25 + .75*on), a)
                    if on > 0: txt(ctx, str(M[i][j]), x + j*(s + 6) + s/2, y + i*(s + 6) + s*.66, 22 if M[i][j] < 100 else 18, R['paper'] if on > .5 else R['char'], a*on, 'bold', 'c', mono=True)
        tg = _c(go_cue)
        for lane, (y0, name, ink) in enumerate(((210, 'CPU · ONE SUM AT A TIME', R['coral']), (560, 'GPU · ALL SUMS AT ONCE', R['teal']))):
            txt(ctx, name, 120, y0 - 26, 28, ink, a, 'bold', mono=True)
            grid(120, y0, A, R['char'])
            txt(ctx, '×', 360, y0 + 130, 70, R['char'], a, 'black', 'c')
            grid(420, y0, B, R['char'])
            txt(ctx, '=', 660, y0 + 130, 70, R['char'], a, 'black', 'c')
            if lane == 0:
                done = max(0, (t - 1.2)*2.2)
                show = lambda i, j: 1 if i*4 + j < done else 0
            else:
                show = lambda i, j: ease(seg(t, tg, tg + .35))
            grid(720, y0, Cm, ink, show=show)
            # race clock
            el = min(16, max(0, (t - 1.2)*2.2)) if lane == 0 else (min(1, max(0, t - tg)))
            txt(ctx, f'{min(int(el), 16)}/16 DONE' if lane == 0 else ('16/16 DONE' if t > tg + .35 else '0/16 DONE'), 1020, y0 + 120, 30, ink, a, 'bold', mono=True)
        # zoom-out: the real thing is billions of times bigger
        tp = _c(par_cue); q = seg(t, tp, tp + .6)
        if q > 0:
            ctx.save(); ctx.translate(1530, 450); ctx.rotate(-.05); ctx.scale(eob(q, 1.8), eob(q, 1.8))
            riso(ctx, lambda: rrect(ctx, -260, -110, 520, 220, 18), R['violet'] if False else R['teal'], ease(q*2)*a_out, second=R['coral'])
            inktext(ctx, 'PARALLEL', 0, -10, 76, R['paper'], ease(q*2)*a_out, align='c')
            inktext(ctx, 'COMPUTING', 0, 70, 60, R['paper'], ease(q*2)*a_out, align='c')
            ctx.restore()
        ctx.restore()
    return _bg(f, 'sheet')

def train_infer(train_cue, infer_cue):
    def f(ctx, t, D):
        bg_sheet(ctx); a_out = outro(t, D)
        cable(ctx, t, 'TWO JOBS FOR A GPU', a_out, core.EP)
        ctx.save(); camera(ctx, t, D, (1.0, 1.03), cy=520)
        tt, ti = _c(train_cue), _c(infer_cue)
        qa = ease(seg(t, tt, tt + .6))*a_out
        if qa > 0:
            panel(ctx, 100, 170, 840, 660, qa, 'TRAINING · LEARNING', R['coral'])
            # data pile -> network
            for k in range(30):
                rr = random.Random(k); px, py = 160 + rr.uniform(0, 160), 520 + rr.uniform(0, 220)
                riso(ctx, lambda: rrect(ctx, px, py, 26, 18, 3), R['coralpale'], qa)
            txt(ctx, 'DATA', 240, 780, 26, R['coral'], qa, 'bold', 'c', mono=True)
            particles(ctx, lambda s: (lerp(330, 560, s), 620 - 160*math.sin(s*math.pi)), 22, t, .5, qa, R['coral'], r=6, seed=2)
            net(ctx, 560, 300, 300, 300, t, qa, p=ease(seg(t, tt, tt + 1.4)), glow=.6)
            # many GPUs + weeks
            for k in range(16):
                on = .5 + .5*math.sin(t*7 + k)
                riso(ctx, lambda: rrect(ctx, 560 + (k % 8)*38, 640 + (k//8)*38, 30, 30, 4), mix(R['tealpale'], R['teal'], on), qa)
            pg = int((t*3) % 7)
            txt(ctx, f'WEEK {1 + int(t/2) % 9}', 910, 295, 26, R['coral'], qa, 'bold', 'r', mono=True)
            txt(ctx, 'THOUSANDS OF GPUs', 720, 800, 22, R['char'], qa*.8, 'bold', 'c', mono=True)
        qi = ease(seg(t, ti, ti + .6))*a_out
        if qi > 0:
            panel(ctx, 1000, 170, 820, 660, qi, 'INFERENCE · ANSWERING', R['teal'])
            # question bubble
            riso(ctx, lambda: rrect(ctx, 1060, 290, 520, 110, 26), R['tealpale'], qi)
            txt(ctx, 'Why does AI need GPUs?', 1090, 358, 32, R['char'], qi, 'bold')
            aq = seg(t, ti + 1.0, ti + 1.5)
            if aq > 0:
                riso(ctx, lambda: rrect(ctx, 1240, 450, 520, 240, 26), R['teal'], ease(aq)*qi)
                n = int(max(0, t - ti - 1.5)*8)
                if n < 4:
                    for k in range(3):
                        rgba(ctx, R['paper'], qi*(.4 + .6*(math.sin(t*8 - k) > 0))); ctx.arc(1300 + k*36, 570, 10, 0, 2*math.pi); ctx.fill()
                else:
                    for k in range(4):
                        L = min(1, (n - 4 - k*6)/6)
                        if L > 0: riso(ctx, lambda: rrect(ctx, 1280, 490 + k*48, 440*L*(.6 if k == 3 else 1), 22, 8), R['paper'], qi)
        ctx.restore()
    return _bg(f, 'sheet')

def _use_icon(ctx, kind, x, y, t, a, ink):
    if kind == 'games':
        riso(ctx, lambda: rrect(ctx, x - 110, y - 50, 220, 110, 50), ink, a, second=R['coral'])
        rgba(ctx, R['paper'], a); ctx.rectangle(x - 76, y - 6, 44, 12); ctx.fill(); ctx.rectangle(x - 60, y - 22, 12, 44); ctx.fill()
        for k, (dx, dy) in enumerate(((54, -10), (78, 12))):
            rgba(ctx, R['paper'], a*(.6 + .4*math.sin(t*4 + k))); ctx.arc(x + dx, y + dy, 11, 0, 2*math.pi); ctx.fill()
    elif kind == 'chat':
        riso(ctx, lambda: (rrect(ctx, x - 110, y - 70, 220, 120, 30)), ink, a, second=R['coral'])
        riso(ctx, lambda: (ctx.move_to(x - 60, y + 40), ctx.line_to(x - 80, y + 90), ctx.line_to(x - 20, y + 45), ctx.close_path()), ink, a)
        for k in range(3):
            rgba(ctx, R['paper'], a*(.4 + .6*(math.sin(t*6 - k) > 0))); ctx.arc(x - 40 + k*40, y - 10, 11, 0, 2*math.pi); ctx.fill()
    elif kind == 'weather':
        ctx.save(); ctx.translate(x - 20, y - 20); ctx.rotate(t*.8)
        ctx.set_line_width(8); rgba(ctx, R['coral'], a); ctx.set_line_cap(cairo.LINE_CAP_ROUND)
        for k in range(3):
            ctx.arc(0, 0, 30 + k*22, k*2.1, k*2.1 + 3.6); ctx.stroke()
        ctx.restore()
        riso(ctx, lambda: (ctx.arc(x + 10, y + 30, 50, math.pi, 0), ctx.arc(x + 70, y + 40, 38, math.pi*1.2, .2), ctx.line_to(x + 108, y + 78), ctx.line_to(x - 40, y + 78), ctx.close_path()), ink, a)
    elif kind == 'medicine':
        pts = [(x - 60, y - 30), (x, y - 70), (x + 60, y - 30), (x + 60, y + 40), (x, y + 80), (x - 60, y + 40)]
        ctx.save(); ctx.translate(x, y); ctx.rotate(.3*math.sin(t*.7)); ctx.translate(-x, -y)
        rgba(ctx, R['char'], a); ctx.set_line_width(6)
        for i in range(6):
            ctx.move_to(*pts[i]); ctx.line_to(*pts[(i + 1) % 6]); ctx.stroke()
        ctx.move_to(*pts[2]); ctx.line_to(x + 120, y - 70); ctx.stroke()
        for i, (px, py) in enumerate(pts + [(x + 120, y - 70)]):
            riso(ctx, lambda: ctx.arc(px, py, 20, 0, 2*math.pi), ink if i % 2 else R['coral'], a)
        ctx.restore()

def uses(tiles, title='WHERE GPUs WORK'):
    """tiles: [(icon, title, cue)]"""
    def f(ctx, t, D):
        bg_sheet(ctx); a_out = outro(t, D)
        cable(ctx, t, title, a_out, core.EP)
        ctx.save(); camera(ctx, t, D, (1.0, 1.04), cy=520)
        w, gap = 400, 40; x0 = W/2 - (4*w + 3*gap)/2
        for i, (ic, ti, cue) in enumerate(tiles):
            t0 = _c(cue); q = seg(t, t0, t0 + .6)
            if q <= 0: continue
            x = x0 + i*(w + gap); y = 230; s = eob(q, 1.7); a = ease(q*1.6)*a_out
            ink = R['teal'] if i % 2 == 0 else R['over']
            ctx.save(); ctx.translate(x + w/2, y + 260); ctx.scale(s, s); ctx.translate(-(x + w/2), -(y + 260))
            panel(ctx, x, y, w, 520, a)
            _use_icon(ctx, ic, x + w/2, y + 210, t, a, ink)
            inktext(ctx, ti, x + w/2, y + 430, 46, ink, a, align='c', second=R['coral'])
            ctx.restore()
        ctx.restore()
    return _bg(f, 'sheet')

def memory_wall(wall_cue):
    def f(ctx, t, D):
        bg_sheet(ctx); a_out = outro(t, D)
        cable(ctx, t, 'THE MEMORY WALL', a_out, core.EP)
        ctx.save(); camera(ctx, t, D, (1.0, 1.05), cy=520, pan=(-30, 0))
        a = fadein(t, .2, .5)*a_out
        # memory on the left
        for k in range(4):
            riso(ctx, lambda: rrect(ctx, 120, 300 + k*90, 260, 70, 8), R['coralpale'], a, seed=k)
            for m in range(8):
                rgba(ctx, R['coral'], a*.8); ctx.rectangle(136 + m*30, 318 + k*90, 18, 34); ctx.fill()
        txt(ctx, 'MEMORY', 250, 720, 34, R['coral'], a, 'black', 'c')
        # narrow road
        riso(ctx, lambda: rrect(ctx, 380, 470, 760, 60, 0), R['mist'], a)
        rgba(ctx, R['grey'], a); ctx.set_line_width(3); ctx.set_dash([24, 18], -t*20); ctx.move_to(380, 500); ctx.line_to(1140, 500); ctx.stroke(); ctx.set_dash([])
        tw_ = _c(wall_cue); jam = ease(seg(t, .8, 3.5))
        particles(ctx, lambda s: (lerp(390, 1130, s), 500), 34, t, .25, a, R['coral'], r=11, jam=jam, seed=5)
        # GPU with idle workers
        panel(ctx, 1150, 230, 640, 560, a, 'GPU · WAITING', R['teal'])
        core_grid(ctx, 1190, 330, 38, 26, 11, 5, t, a, lit=.15*(1 - jam), idle=.1)
        dots = '.'*(1 + int(t*2) % 3)
        txt(ctx, 'WAITING FOR DATA' + dots, 1470, 760, 26, R['char'], a, 'bold', 'c', mono=True)
        q = seg(t, tw_, tw_ + .45)
        if q > 0:
            dy = -400*(1 - eob(q, 1.3)); qa = ease(q*2)*a_out
            for r_ in range(6):
                for c_ in range(3):
                    off = 30 if r_ % 2 else 0
                    riso(ctx, lambda: rrect(ctx, 820 + off + c_*62 - 60, 330 + r_*58 + dy, 56, 50, 4), R['char'], qa, seed=r_*3 + c_)
            tag(ctx, 880, 270 + dy, 'THE MEMORY WALL', R['coral'], qa, 34, align='c')
        ctx.restore()
    return _bg(f, 'sheet')

def dram_nand(dram_cue, off_cue, nand_cue):
    def f(ctx, t, D):
        bg_sheet(ctx); a_out = outro(t, D)
        cable(ctx, t, 'TWO KINDS OF MEMORY', a_out, core.EP)
        ctx.save(); camera(ctx, t, D, (1.0, 1.03), cy=520)
        td, to, tn = _c(dram_cue), _c(off_cue), _c(nand_cue)
        off = ease(seg(t, to, to + .6))
        for side, (t0, name, sub, ink, x) in enumerate(((td, 'DRAM', 'FAST WORKING MEMORY', R['coral'], 140), (tn, 'NAND FLASH', 'STORAGE · LIKE YOUR PHONE', R['teal'], 1000))):
            q = ease(seg(t, t0, t0 + .6))*a_out
            if q <= 0: continue
            panel(ctx, x, 200, 780, 600, q)
            inktext(ctx, name, x + 390, 300, 76, ink, q, align='c', second=R['coral'] if ink == R['teal'] else R['teal'])
            txt(ctx, sub, x + 390, 352, 26, R['char'], q, 'bold', 'c', mono=True)
            for i in range(10):
                for j in range(4):
                    if side == 0:
                        fall = off*(1 + (i*7 + j*3) % 5*.25)
                        ya = 1 - ease(min(1, fall))
                        on = .5 + .5*math.sin(t*12 + i + j*2)
                        if ya > 0: riso(ctx, lambda: rrect(ctx, x + 70 + i*66, 420 + j*70 + 220*fall**2, 52, 52, 6), mix(R['coralpale'], R['coral'], on), q*ya, seed=i*4 + j)
                    else:
                        on = .5 + .5*math.sin(t*2 + i + j*2)
                        riso(ctx, lambda: rrect(ctx, x + 70 + i*66, 420 + j*70, 52, 52, 6), mix(R['tealpale'], R['teal'], on), q, seed=i*4 + j)
            if side == 0 and off > 0:
                tag(ctx, x + 390, 740, 'POWER OFF → FORGETS', R['char'], off*q, 26, align='c')
            if side == 1 and t > to:
                tag(ctx, x + 390, 740, 'SLOWER · REMEMBERS', R['char'], ease(seg(t, tn + .8, tn + 1.2))*q, 26, align='c')
        # power switch
        if t > to - .5:
            sa = ease(seg(t, to - .5, to))*a_out
            riso(ctx, lambda: rrect(ctx, 880, 120, 160, 60, 30), R['char'], sa)
            riso(ctx, lambda: ctx.arc(lerp(1010, 910, off), 150, 24, 0, 2*math.pi), R['coral'] if off < .5 else R['grey'], sa)
            txt(ctx, 'ON' if off < .5 else 'OFF', 960, 215, 22, R['char'], sa, 'bold', 'c', mono=True)
        ctx.restore()
    return _bg(f, 'sheet')

def hbm_tower(tower_cue, wires_cue, beside_cue, road_cue):
    def f(ctx, t, D):
        bg_sheet(ctx); a_out = outro(t, D)
        cable(ctx, t, 'HBM · HIGH BANDWIDTH MEMORY', a_out, core.EP)
        ctx.save(); camera(ctx, t, D, (1.0, 1.05), cy=560)
        a = fadein(t, .2, .5)*a_out
        tt, tw_, tb, tr = _c(tower_cue), _c(wires_cue), _c(beside_cue), _c(road_cue)
        # base (interposer)
        riso(ctx, lambda: rrect(ctx, 260, 760, 1400, 46, 8), R['char'], a)
        txt(ctx, 'SAME PACKAGE', 960, 845, 22, R['grey'], a, 'bold', 'c', mono=True)
        # GPU die
        riso(ctx, lambda: rrect(ctx, 760, 470, 420, 290, 12), R['teal'], a, second=R['coral'])
        core_grid(ctx, 790, 500, 24, 15, 11, 5, t, a, lit=ease(seg(t, tr, tr + .6)), idle=.3)
        txt(ctx, 'GPU', 970, 740, 30, R['paper'], a, 'black', 'c')
        # towers either side
        for side, bx in enumerate((370, 1290)):
            for k in range(8):
                tk = tt + .1 + k*.18 + side*.08
                q = seg(t, tk, tk + .35)
                if q <= 0: continue
                y = 712 - k*44 - 260*(1 - eob(q, 1.4))
                def slab():
                    ctx.move_to(bx, y); ctx.line_to(bx + 220, y); ctx.line_to(bx + 260, y - 24); ctx.line_to(bx + 40, y - 24); ctx.close_path()
                    ctx.rectangle(bx, y, 220, 36)
                riso(ctx, slab, R['coral'] if k % 2 else R['over'], ease(q*2)*a, seed=k + side*9)
            wq = ease(seg(t, tw_, tw_ + .8))
            if wq > 0:
                for m in range(6):
                    xx = bx + 30 + m*34
                    rgba(ctx, R['paper'], a*wq*(.6 + .4*math.sin(t*8 + m))); ctx.rectangle(xx, 712 + 36 - 360*wq, 5, 360*wq); ctx.fill()
        if t > tt + .5:
            tag(ctx, 490, 300, 'DRAM CHIPS, STACKED', R['over'], ease(seg(t, tt + .5, tt + .9))*a, 24, align='c')
        if t > tw_:
            tag(ctx, 1420, 300, 'WIRES THROUGH THE SILICON', R['char'], ease(seg(t, tw_ + .3, tw_ + .7))*a, 24, align='c')
        # data highway
        rq = ease(seg(t, tr, tr + .8))
        if rq > 0:
            for side, (x0, x1) in enumerate(((610, 760), (1180, 1290))):
                riso(ctx, lambda: rrect(ctx, x0, 560 - 60*rq, x1 - x0, 120*rq, 6), R['tealpale'], a*rq)
                for lane in range(5):
                    particles(ctx, lambda s, lane=lane: (lerp(x0, x1, s) if side == 0 else lerp(x1, x0, s), 520 + lane*20), 6, t, 1.6, a*rq, R['teal'], r=5, seed=lane + side*10)
            tag(ctx, 960, 420, 'SHORT DISTANCE · WIDE ROAD', R['teal'], rq*a, 28, align='c')
        ctx.restore()
    return _bg(f, 'sheet')

def makers(cues, tip_cue, quote_cue, quote, who):
    """three HBM makers as tokens, then demand vs supply with an attributed quote"""
    def f(ctx, t, D):
        bg_board(ctx); a_out = outro(t, D)
        cable(ctx, t, 'WHO MAKES HBM', a_out, core.EP)
        ctx.save(); camera(ctx, t, D, (1.0, 1.04), cy=480)
        tq = _c(quote_cue); shift = ease(seg(t, tq - .3, tq + .5))
        items = [('SK HYNIX', 'SOUTH KOREA', R['teal']), ('SAMSUNG', 'SOUTH KOREA', R['teal']), ('MICRON', 'UNITED STATES', R['coral'])]
        for i, (nm, ctry, ink) in enumerate(items):
            t0 = _c(cues[i]); q = seg(t, t0, t0 + .55)
            if q <= 0: continue
            x = lerp(480 + i*480, 260 + i*210, shift); y = lerp(470, 300, shift); r = lerp(150, 90, shift)
            s = eob(q, 1.8)
            ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
            token(ctx, 0, 0, nm, ink, ease(q*2)*a_out, r=r, size=int(lerp(40, 26, shift)))
            ctx.restore()
            tag(ctx, x, y + r + 50, ctry, ink, ease(q*2)*a_out*(1 - .3*shift), int(lerp(26, 18, shift)), align='c')
        q = seg(t, tq, tq + .7)
        if q > 0:
            qa = ease(q*1.5)*a_out
            # demand vs supply bars
            for k, (lab, hgt, ink) in enumerate((('DEMAND', 330, R['coral']), ('SUPPLY', 220, R['teal']))):
                h = hgt*eoc(seg(t, tq + .2 + k*.2, tq + 1.2 + k*.2))
                riso(ctx, lambda: rrect(ctx, 220 + k*170, 800 - h, 130, h, 6), ink, qa, seed=k)
                txt(ctx, lab, 285 + k*170, 840, 22, R['char'], qa, 'bold', 'c', mono=True)
            riso(ctx, lambda: rrect(ctx, 760, 520, 1040, 300, 18), R['paper'], qa)
            rgba(ctx, R['char'], qa); ctx.set_line_width(3); rrect(ctx, 760, 520, 1040, 300, 18); ctx.stroke()
            txt(ctx, '“', 790, 620, 120, R['coral'], qa, 'black')
            para(ctx, quote, 860, 590, 34, R['char'], 900, qa, weight='bold')
            txt(ctx, who, 1770, 795, 22, R['grey'], qa, 'bold', 'r', mono=True)
        ctx.restore()
    return _bg(f, 'sheet')

def supply_board(stations, lanes, title='WHO MAKES WHAT'):
    """stations: [(x, y, place, [lines], ink, cue)], lanes: [(i, j)]; schematic, no boundaries"""
    def f(ctx, t, D):
        bg_board(ctx); a_out = outro(t, D)
        cable(ctx, t, title, a_out, core.EP)
        ctx.save(); camera(ctx, t, D, (1.0, 1.05), cy=500)
        # ocean washes (schematic)
        for k, (cx, cy, r) in enumerate(((520, 520, 420), (1350, 480, 380))):
            halftone(ctx, lambda: ctx.arc(cx, cy, r, 0, 2*math.pi), R['river'], .25*a_out, step=14, r=2)
        for i, j in lanes:
            ti, tj = _c(stations[i][5]), _c(stations[j][5]); t0 = max(ti, tj)
            p = eoc(seg(t, t0, t0 + 1.0))
            if p <= 0: continue
            x0, y0 = stations[i][:2]; x1, y1 = stations[j][:2]; mx, my = (x0 + x1)/2, min(y0, y1) - 180
            bez = lambda s: ((1-s)**2*x0 + 2*(1-s)*s*mx + s*s*x1, (1-s)**2*y0 + 2*(1-s)*s*my + s*s*y1)
            ctx.save(); ctx.set_line_width(4); ctx.set_dash([14, 12], -t*30); rgba(ctx, R['river'], a_out)
            ctx.move_to(x0, y0)
            for k in range(1, int(40*p) + 1): ctx.line_to(*bez(k/40))
            ctx.stroke(); ctx.restore()
            if p >= 1:
                for k in range(3):
                    s = (t*.12 + k/3) % 1; sx, sy = bez(s)
                    riso(ctx, lambda: rrect(ctx, sx - 14, sy - 8, 28, 16, 5), R['char'], a_out)
        for i, (x, y, place, lines, ink, cue) in enumerate(stations):
            t0 = _c(cue); q = seg(t, t0, t0 + .6)
            if q <= 0: continue
            qa = ease(q*2)*a_out
            rgba(ctx, ink, (1 - seg(t, t0, t0 + 1.4))*a_out); ctx.set_line_width(3); ctx.arc(x, y, 20 + 70*seg(t, t0, t0 + 1.4), 0, 2*math.pi); ctx.stroke()
            riso(ctx, lambda: ctx.arc(x, y, 22*eob(q, 2), 0, 2*math.pi), ink, qa, second=R['coral'] if ink == R['teal'] else R['teal'])
            tag(ctx, x, y - 64, place, ink, qa, 26, align='c')
            for k, l in enumerate(lines):
                txt(ctx, l, x, y + 64 + k*36, 26, R['char'], ease(seg(t, t0 + .3 + k*.2, t0 + .7 + k*.2))*a_out, 'bold', 'c', mono=True)
        ctx.restore()
        credit(ctx, 'SCHEMATIC · NOT TO SCALE · BOUNDARIES NOT SHOWN', a_out)
    return _bg(f, 'board')
