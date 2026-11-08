"""Scene templates for India and the World, Simply Briefed.
Each template returns a scene function f(ctx, t, D) with an attribute .bg."""
import math, random, cairo
from engine import core
from engine.core import W, H, cl, seg, ease, eoc, eob, lerp, T
from engine.riso import (R, rgba, riso, halftone, rrect, txt, inktext, wrap, para, typed, camera, pop, fadein,
                         cable, credit, bg_sheet, bg_board, tw, face)

ASOF = 'AS OF NOV 2026'

def _bg(f, name):
    f.bg = name; return f

def outro(t, D, k=.35):
    return 1 - ease(seg(t, D - k, D))

# ---------- small props ----------
def figure(ctx, x, y, s, ink, a=1., t=0., gesture=0., seed=0):
    """generic paper figure: body + head, idle breathing, optional raised hand"""
    if a <= 0: return
    br = 1 + .012*math.sin(t*2.2 + seed)
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s*br)
    riso(ctx, lambda: rrect(ctx, -34, -96, 68, 100, 30), ink, a, seed=seed+1)
    hx = 3*math.sin(t*.9 + seed)
    riso(ctx, lambda: ctx.arc(hx, -122, 22, 0, 2*math.pi), R['char'], a*.9)
    if gesture > 0:
        ang = lerp(.3, -1.2, eob(gesture))
        ctx.save(); ctx.translate(26, -80); ctx.rotate(ang)
        riso(ctx, lambda: rrect(ctx, -7, -58, 14, 62, 7), ink, a, seed=seed+2)
        ctx.restore()
    ctx.restore()

def podium(ctx, x, y, a=1.):
    riso(ctx, lambda: (ctx.move_to(x-60, y), ctx.line_to(x+60, y), ctx.line_to(x+45, y-110), ctx.line_to(x-45, y-110), ctx.close_path()), R['grey'], a*.7)

def token(ctx, x, y, name, ink, a=1., r=56, size=24, sub=None, dim=False):
    if a <= 0: return
    if dim:
        riso(ctx, lambda: ctx.arc(x, y, r, 0, 2*math.pi), R['mist'], a)
        rgba(ctx, R['grey'], a); ctx.set_line_width(2); ctx.arc(x, y, r, 0, 2*math.pi); ctx.stroke()
        txt(ctx, name, x, y+size*.36, size, R['char'], .7*a, 'bold', 'c')
        return
    riso(ctx, lambda: ctx.arc(x, y, r, 0, 2*math.pi), ink, a*.95, seed=hash(name) % 97)
    txt(ctx, name, x, y+size*.36, size, R['paper'], a, 'bold', 'c')
    if sub: txt(ctx, sub, x, y+r+30, 18, R['char'], a*.8, 'reg', 'c', mono=True)

def tag(ctx, x, y, s, ink, a=1., size=24, mono=True, pad=16, align='l'):
    if a <= 0: return 0
    w = tw(ctx, s, size, 'bold', mono) + pad*2; h = size*1.8
    x0 = x - (w/2 if align == 'c' else w if align == 'r' else 0)
    riso(ctx, lambda: rrect(ctx, x0, y-h/2, w, h, 6), ink, a)
    txt(ctx, s, x0+pad, y+size*.36, size, R['paper'], a, 'bold', mono=mono)
    return w

# ---------- HEADLINE ----------
def headline(lines, kicker, question=None, motif=None):
    """lines: [(text, ink)], big words landing one by one"""
    def f(ctx, t, D):
        bg_sheet(ctx)
        a_out = outro(t, D)
        ctx.save(); camera(ctx, t, D, (1.0, 1.04), depth=.5)
        # halftone river band motif behind
        def band():
            ctx.move_to(-100, 820)
            for x in range(-100, W+120, 40):
                ctx.line_to(x, 700 + 60*math.sin(x*.004 + t*.6))
            ctx.line_to(W+120, 1100); ctx.line_to(-100, 1100); ctx.close_path()
        halftone(ctx, band, R['teal'], .55*fadein(t, .1, .8)*a_out, step=13, r=3.2)
        if motif: motif(ctx, t, D, a_out)
        ctx.restore()
        ctx.save(); camera(ctx, t, D, (1.0, 1.06))
        cable(ctx, t, f'BRIEFING · {ASOF}', a_out, core.EP)
        txt(ctx, typed(kicker, seg(t, .6, 1.6)), 140, 250, 30, R['coral'], a_out, 'bold', mono=True)
        y = 420; k = 0
        for li, (s, ink) in enumerate(lines):
            x = 130
            for wi, word in enumerate(s.split()):
                t0 = .9 + k*.32; k += 1
                p = seg(t, t0, t0+.5)
                if p <= 0: continue
                sc = lerp(1.35, 1, eob(p, 1.4))
                ww = tw(ctx, word+' ', 150, 'black')
                ctx.save(); ctx.translate(x, y); ctx.scale(sc, sc)
                inktext(ctx, word, 0, 0, 150, ink, ease(p*2)*a_out, settle=eoc(p), seed=li*10+wi, second=R['coral'] if ink == R['teal'] else R['teal'])
                ctx.restore()
                x += ww
            y += 165
        if question:
            q0 = T(question[1]) if len(question) > 1 else D - 3
            p = seg(t, q0, q0+.6)
            txt(ctx, question[0], 136, y+40, 44, R['char'], ease(p)*a_out, 'bold')
            rgba(ctx, R['coral'], ease(p)*a_out); ctx.rectangle(136, y+62, 900*eoc(p), 6); ctx.fill()
        ctx.restore()
    return _bg(f, 'sheet')

# ---------- TIMELINE ----------
def timeline(markers, focus, title=None):
    """markers: [(label_year, caption, ink, cue_phrase_or_time, x)], focus: (x_from, x_to) camera centre range"""
    def f(ctx, t, D):
        bg_sheet(ctx)
        a_out = outro(t, D)
        cable(ctx, t, f'BACKSTORY · {ASOF}', a_out, core.EP)
        p = ease(seg(t, .2, D-.5))
        cx = lerp(focus[0], focus[1], p)
        ctx.save(); ctx.translate(W/2 - cx, 0)
        # parallax halftone hills
        ctx.save(); ctx.translate((cx - W/2)*.35, 0)
        def hills():
            ctx.move_to(-2000, 1000)
            for x in range(-2000, 6000, 60): ctx.line_to(x, 860 + 40*math.sin(x*.003))
            ctx.line_to(6000, 1200); ctx.line_to(-2000, 1200); ctx.close_path()
        halftone(ctx, hills, R['tealpale'], .9*a_out, step=12, r=2.4)
        ctx.restore()
        y = 560
        xmax = max(m[4] for m in markers) + 300
        draw = eoc(seg(t, 0, 1.2))
        rgba(ctx, R['char'], a_out); ctx.rectangle(-400, y-3, (xmax+400)*max(draw, .0), 6); ctx.fill()
        for i, (yr, cap, ink, cue, x) in enumerate(markers):
            t0 = T(cue) if isinstance(cue, str) else cue
            q = seg(t, t0, t0+.55)
            if q <= 0:
                riso(ctx, lambda: ctx.arc(x, y, 9, 0, 2*math.pi), R['grey'], .5*a_out); continue
            r = 26*eob(q, 2)
            riso(ctx, lambda: ctx.arc(x, y, r, 0, 2*math.pi), ink, a_out, seed=i, second=R['coral'] if ink == R['teal'] else None)
            up = i % 2 == 0
            yy = y - 90 if up else y + 120
            inktext(ctx, yr, x, yy, 84, ink, ease(q*1.5)*a_out, settle=eoc(q), seed=i, align='c', second=R['coral'] if ink == R['teal'] else R['teal'])
            lines = wrap(ctx, cap, 30, 380, 'bold')
            for j, l in enumerate(lines):
                txt(ctx, l, x, (yy - 110 - (len(lines)-1-j)*40) if up else (yy + 60 + j*40), 30, R['char'], ease(seg(t, t0+.25, t0+.7))*a_out, 'bold', 'c')
        ctx.restore()
    return _bg(f, 'sheet')

# ---------- STANDS ----------
def stands(cards, show_from):
    """cards: [(head, [lines], ink)], show_from: [cue for each card]"""
    def f(ctx, t, D):
        bg_sheet(ctx)
        a_out = outro(t, D)
        cable(ctx, t, f'WHERE THEY STAND · {ASOF}', a_out, core.EP)
        ctx.save(); camera(ctx, t, D, (1.0, 1.03))
        n = len(cards); cw = 760; gap = 80
        x0 = W/2 - (n*cw + (n-1)*gap)/2
        for i, (head, lines, ink) in enumerate(cards):
            c0 = show_from[i]; t0 = T(c0) if isinstance(c0, str) else c0
            q = seg(t, t0, t0+.6)
            if q <= 0: continue
            x = x0 + i*(cw+gap); y = 200 + 60*(1-eob(q, 1.5))
            a = ease(q*1.6)*a_out
            riso(ctx, lambda: rrect(ctx, x, y, cw, 640, 18), R['paper'], a)
            rgba(ctx, ink, a); ctx.set_line_width(5); rrect(ctx, x, y, cw, 640, 18); ctx.stroke()
            riso(ctx, lambda: rrect(ctx, x, y, cw, 96, 18), ink, a, seed=i)
            txt(ctx, head, x+40, y+64, 44, R['paper'], a, 'black')
            figure(ctx, x+cw-90, y+300, .85, ink, a, t, gesture=seg(t, t0+.5, t0+1.2), seed=i)
            podium(ctx, x+cw-90, y+340, a)
            yy = y + 170
            for j, l in enumerate(lines):
                lq = fadein(t, t0 + .5 + j*.9, .5)
                rgba(ctx, ink, lq*a); ctx.rectangle(x+40, yy-26, 8, 8); ctx.fill()
                nl = para(ctx, l, x+66, yy, 32, R['char'], cw-260, lq*a, weight='bold' if j == 0 else 'reg')
                yy += nl*42 + 34
        ctx.restore()
    return _bg(f, 'sheet')

# ---------- STAKES ----------
def _icon(ctx, kind, x, y, t, a, ink):
    if kind == 'shield':
        def p():
            ctx.move_to(x, y-90); ctx.curve_to(x+70, y-70, x+80, y-60, x+80, y-60)
            ctx.curve_to(x+80, y+20, x+40, y+70, x, y+95); ctx.curve_to(x-40, y+70, x-80, y+20, x-80, y-60)
            ctx.curve_to(x-80, y-60, x-70, y-70, x, y-90); ctx.close_path()
        riso(ctx, p, ink, a)
        halftone(ctx, p, R['paper'], .0, step=9, r=2)
    elif kind == 'turbine':
        riso(ctx, lambda: (ctx.move_to(x-8, y), ctx.line_to(x+8, y), ctx.line_to(x+5, y+100), ctx.line_to(x-5, y+100), ctx.close_path()), R['char'], a*.8)
        ang = t*1.6
        for k in range(3):
            ctx.save(); ctx.translate(x, y); ctx.rotate(ang + k*2*math.pi/3)
            riso(ctx, lambda: (ctx.move_to(0, 0), ctx.curve_to(18, -30, 14, -80, 0, -95), ctx.curve_to(-8, -60, -10, -20, 0, 0)), ink, a, second=R['coral'])
            ctx.restore()
        riso(ctx, lambda: ctx.arc(x, y, 10, 0, 2*math.pi), R['char'], a)
    elif kind == 'rivers':
        for k, (dx, ink2, lab) in enumerate(((-55, R['coral'], 'China'), (55, R['teal'], 'India'))):
            pass
        # upstream -> downstream arrow with flowing dashes
        ctx.save(); ctx.set_line_width(14); ctx.set_line_cap(cairo.LINE_CAP_ROUND)
        ctx.set_dash([26, 18], -t*60)
        rgba(ctx, R['river'], a); ctx.move_to(x-90, y-70); ctx.curve_to(x-20, y-60, x+10, y+40, x+90, y+60); ctx.stroke()
        ctx.restore()
        riso(ctx, lambda: (ctx.move_to(x+90, y+30), ctx.line_to(x+120, y+66), ctx.line_to(x+78, y+88), ctx.close_path()), R['river'], a)
        tag(ctx, x-110, y-110, 'UPSTREAM: CHINA', R['coral'], a, 16)
        tag(ctx, x+10, y+120, 'DOWNSTREAM: INDIA', R['teal'], a, 16)

def stakes(tiles):
    """tiles: [(icon, title, line, ink, cue)]"""
    def f(ctx, t, D):
        bg_sheet(ctx)
        a_out = outro(t, D)
        cable(ctx, t, f"INDIA'S STAKE · {ASOF}", a_out, core.EP)
        ctx.save(); camera(ctx, t, D, (1.0, 1.035))
        tw_, gap = 520, 60; x0 = W/2 - (3*tw_ + 2*gap)/2
        for i, (ic, title, line, ink, cue) in enumerate(tiles):
            t0 = T(cue) if isinstance(cue, str) else cue
            q = seg(t, t0, t0+.6)
            if q <= 0: continue
            x = x0 + i*(tw_+gap); y = 220
            s = eob(q, 1.6); a = ease(q*1.6)*a_out
            ctx.save(); ctx.translate(x+tw_/2, y+300); ctx.scale(s, s); ctx.translate(-(x+tw_/2), -(y+300))
            riso(ctx, lambda: rrect(ctx, x, y, tw_, 600, 18), R['paper'], a)
            rgba(ctx, ink, a); ctx.set_line_width(4); rrect(ctx, x, y, tw_, 600, 18); ctx.stroke()
            txt(ctx, f'0{i+1}', x+30, y+60, 30, ink, a, 'bold', mono=True)
            _icon(ctx, ic, x+tw_/2, y+200, t, a, ink)
            inktext(ctx, title, x+tw_/2, y+390, 52, ink, a, settle=eoc(q), seed=i, align='c', second=R['coral'] if ink == R['teal'] else R['teal'])
            para(ctx, line, x+tw_/2, y+450, 28, R['char'], tw_-70, a, align='c')
            ctx.restore()
        ctx.restore()
    return _bg(f, 'sheet')

# ---------- EXAM ----------
def statement(num, stmt, verdict, reason, flip_cue):
    def f(ctx, t, D):
        bg_sheet(ctx)
        a_out = outro(t, D)
        cable(ctx, t, 'EXAM DESK · PRELIMS', a_out, core.EP)
        ctx.save(); camera(ctx, t, D, (1.0, 1.03))
        q = pop(t, .2, .6); a = ease(seg(t, .2, .6))*a_out
        tf = T(flip_cue) if isinstance(flip_cue, str) else flip_cue
        fl = seg(t, tf, tf+.5)
        sx = abs(math.cos(math.pi*fl)) if fl < 1 else 1
        back = fl >= .5
        cx, cy, cw, ch = W/2, 520, 1300, 560
        ctx.save(); ctx.translate(cx, cy + 60*(1-q)); ctx.scale(max(sx, .02), 1); ctx.translate(-cx, -cy)
        ink = R['teal'] if verdict == 'TRUE' else R['coral']
        if not back:
            riso(ctx, lambda: rrect(ctx, cx-cw/2, cy-ch/2, cw, ch, 20), R['paper'], a)
            rgba(ctx, R['char'], a); ctx.set_line_width(4); rrect(ctx, cx-cw/2, cy-ch/2, cw, ch, 20); ctx.stroke()
            txt(ctx, f'STATEMENT {num}', cx-cw/2+50, cy-ch/2+80, 30, R['teal'], a, 'bold', mono=True)
            para(ctx, stmt, cx-cw/2+50, cy-ch/2+170, 50, R['char'], cw-100, a, weight='bold')
            pulse = .5 + .5*math.sin(t*5)
            txt(ctx, 'TRUE  or  FALSE ?', cx, cy+ch/2-60, 34, R['grey'], a*(.6+.4*pulse), 'bold', 'c', mono=True)
        else:
            riso(ctx, lambda: rrect(ctx, cx-cw/2, cy-ch/2, cw, ch, 20), ink, a, second=R['coral'] if ink == R['teal'] else R['teal'], settle=seg(t, tf+.5, tf+1.2))
            inktext(ctx, verdict, cx, cy-40, 170, R['paper'], a, weight='black', align='c')
            para(ctx, reason, cx, cy+80, 38, R['paper'], cw-140, a, align='c', weight='bold')
        ctx.restore()
        ctx.restore()
    return _bg(f, 'sheet')

def mains(question, frame, cues):
    def f(ctx, t, D):
        bg_sheet(ctx)
        a_out = outro(t, D)
        cable(ctx, t, 'EXAM DESK · MAINS', a_out, core.EP)
        ctx.save(); camera(ctx, t, D, (1.0, 1.03))
        a = fadein(t, .2, .5)*a_out
        riso(ctx, lambda: rrect(ctx, 150, 170, W-300, 210, 18), R['teal'], a, second=R['coral'], settle=seg(t, .2, 1))
        para(ctx, question, 200, 250, 44, R['paper'], W-420, a, weight='bold')
        for i, (head, line) in enumerate(frame):
            t0 = T(cues[i]) if isinstance(cues[i], str) else cues[i]
            q = seg(t, t0, t0+.55)
            if q <= 0: continue
            y = 470 + i*150; x = 150 + 80*(1-eob(q, 1.5))
            aa = ease(q*1.6)*a_out
            riso(ctx, lambda: ctx.arc(x+45, y+40, 42, 0, 2*math.pi), R['coral'], aa, second=R['teal'])
            txt(ctx, str(i+1), x+45, y+56, 44, R['paper'], aa, 'black', 'c')
            txt(ctx, head, x+120, y+38, 40, R['char'], aa, 'bold')
            txt(ctx, line, x+120, y+86, 30, R['char'], aa*.85)
        ctx.restore()
    return _bg(f, 'sheet')

# ---------- WATCH ----------
def watch(items, cues):
    def f(ctx, t, D):
        bg_sheet(ctx)
        a_out = outro(t, D)
        cable(ctx, t, f'WATCHLIST · {ASOF}', a_out, core.EP)
        ctx.save(); camera(ctx, t, D, (1.0, 1.04))
        inktext(ctx, 'WHAT TO WATCH', 150, 260, 110, R['teal'], fadein(t, .1, .5)*a_out, settle=seg(t, .1, .9), second=R['coral'])
        for i, (head, sub) in enumerate(items):
            t0 = T(cues[i]) if isinstance(cues[i], str) else cues[i]
            q = seg(t, t0, t0+.55)
            if q <= 0: continue
            y = 380 + i*165; aa = ease(q*1.6)*a_out
            x = 150 + 60*(1-eob(q))
            inktext(ctx, f'0{i+1}', x, y+80, 96, R['coral'], aa, settle=eoc(q), seed=i, second=R['teal'])
            txt(ctx, head, x+170, y+40, 44, R['char'], aa, 'bold')
            txt(ctx, sub, x+170, y+90, 30, R['char'], aa*.8, mono=True)
        ctx.restore()
    return _bg(f, 'sheet')

# ---------- official map of India ----------
_MAP = {}
def india_map(ctx, cx, cy, h, a=1.):
    """the official outline of India (Survey of India depiction, from engine/data/india_official.png), recoloured"""
    if a <= 0: return
    if 'img' not in _MAP:
        import os
        _MAP['img'] = cairo.ImageSurface.create_from_png(os.path.join(os.path.dirname(__file__), 'data', 'india_official.png'))
    img = _MAP['img']; s = h/img.get_height()
    ctx.save(); ctx.translate(cx - img.get_width()*s/2, cy - h/2); ctx.scale(s, s)
    ctx.set_source_surface(img, 0, 0); ctx.paint_with_alpha(a); ctx.restore()

def map_point(cx, cy, h, px, py, src_w=1392, src_h=1760):
    """screen position of a point given in the map image's pixels"""
    s = h/src_h
    return cx - src_w*s/2 + px*s, cy - h/2 + py*s
