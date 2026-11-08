"""Town pieces for Units 2-10. Unit 2 sits around the square; Units 3-9 stand on the far ridge (screen y~600);
Unit 10 is the sky-wide aurora. Each piece takes P = unit progress 0..1 (grows across the unit's episodes)."""
from engine.core import *
from engine.town import glowdot

UNITS = {2: (12, 24), 3: (25, 31), 4: (32, 42), 5: (43, 49), 6: (50, 54), 7: (55, 60), 8: (61, 65), 9: (66, 75), 10: (76, 88)}
def unit_of(ep):
    for u, (a, b) in UNITS.items():
        if a <= ep <= b: return u

RY = 604   # ridge baseline

def rights(ctx, P, g=1, t=0):
    """Unit 2: six lanterns around the square, a writ post box, a duties notice board"""
    for i in range(6):
        pp = eob(seg(P, i*.075, i*.075+.12))
        if pp <= 0: continue
        x = 700+i*125; h = 125*pp
        paper(ctx, lambda: ctx.rectangle(x-4, 835-h, 8, h), C['ink'], 1, sh=2)
        if pp > .8:
            glowdot(ctx, x, 835-h-8, 85, g*(.85+.15*math.sin(t*3+i)))
            paper(ctx, lambda: rrect(ctx, x-15, 835-h-34, 30, 36, 6), lerpc(C['paper'], C['gold'], g), 1, sh=2)
    pb = eob(seg(P, .55, .75))
    if pb > 0:
        x = 1470
        paper(ctx, lambda: rrect(ctx, x-22, 835-64*pb, 44, 64*pb, 8), C['berry'], 1, sh=4)
        rgba(ctx, C['ink'], .8); ctx.rectangle(x-14, 835-48*pb, 28, 5); ctx.fill()
    nb = eob(seg(P, .8, .98))
    if nb > 0:
        x = 450
        for dx in (-34, 34): paper(ctx, lambda: ctx.rectangle(x+dx-3, 835-70*nb, 6, 70*nb), C['woodd'], 1, sh=2)
        paper(ctx, lambda: rrect(ctx, x-52, 835-92*nb, 104, 50*nb, 6), C['wood'], 1, sh=4)
        text(ctx, "DUTIES", x, 835-60*nb, 15, C['ink'], nb, bold=True)

def rb(ctx, cx, P, g=1, t=0):
    r = eoc(seg(P, 0, .45))
    if r <= 0: return
    w, h = 250, 66
    paper(ctx, lambda: ctx.rectangle(cx-w/2, RY-h*r, w, h*r), C['sand'], 1, sh=4)
    d = eob(seg(P, .45, .8))
    if d > 0:
        paper(ctx, lambda: ctx.rectangle(cx-30, RY-h-34*d, 60, 34*d+2), hx('C9A97A'), 1, sh=0)
        paper(ctx, lambda: ctx.arc(cx, RY-h-34*d, 46*d, math.pi, 2*math.pi), hx('B8C2BA'), 1, sh=3)
    f = seg(P, .8, 1)
    if f > 0:
        rgba(ctx, C['ink'], f); ctx.rectangle(cx-1.5, RY-h-34-46-34*f, 3, 34*f); ctx.fill()
        paper(ctx, lambda: (ctx.move_to(cx+1.5, RY-h-114), ctx.line_to(cx+26, RY-h-106), ctx.line_to(cx+1.5, RY-h-98), ctx.close_path()), C['gold'], f, sh=0)
    if g > 0 and r >= 1:
        for k in (-80, -40, 40, 80): glowdot(ctx, cx+k, RY-30, 26, g*.5)

def parl(ctx, cx, P, g=1, t=0):
    for side, col, (a, b) in ((-1, C['pine'], (0, .4)), (1, C['berry'], (.3, .7))):
        r = eoc(seg(P, a, b))
        if r > 0:
            paper(ctx, lambda: rrect(ctx, cx+side*75-55, RY-84*r, 110, 84*r, 6), col, 1, sh=4)
            if r >= 1:
                for k in range(3): rgba(ctx, C['paper'], .55); ctx.rectangle(cx+side*75-40+k*30, RY-60, 18, 30); ctx.fill()
    d = eob(seg(P, .65, 1))
    if d > 0:
        paper(ctx, lambda: ctx.rectangle(cx-34, RY-70*d, 68, 70*d), C['paper'], 1, sh=4)
        paper(ctx, lambda: ctx.arc(cx, RY-70*d, 40*d, math.pi, 2*math.pi), C['far'], 1, sh=3)
        if g > 0: glowdot(ctx, cx, RY-35, 40, g*.5)

def court(ctx, cx, P, g=1, t=0):
    b = eoc(seg(P, 0, .25))
    if b <= 0: return
    paper(ctx, lambda: ctx.rectangle(cx-110, RY-14*b, 220, 14*b), C['fogd'], 1, sh=3)
    for i in range(5):
        c = eob(seg(P, .2+i*.08, .55+i*.08))
        if c > 0: paper(ctx, lambda: ctx.rectangle(cx-92+i*46-9, RY-14-80*c, 18, 80*c), C['paper'], 1, sh=3)
    r = eob(seg(P, .6, .9))
    if r > 0:
        paper(ctx, lambda: (ctx.move_to(cx-110, RY-94), ctx.line_to(cx+110, RY-94), ctx.line_to(cx, RY-94-48*r), ctx.close_path()), C['far'], r, sh=3)
        rgba(ctx, C['gold'], r); ctx.set_line_width(3); ctx.move_to(cx-16, RY-106); ctx.line_to(cx+16, RY-106); ctx.move_to(cx, RY-98); ctx.line_to(cx, RY-120); ctx.stroke()

def halls(ctx, cx, P, g=1, t=0):
    for i, dx in enumerate((-90, 0, 90)):
        pp = eob(seg(P, i*.25, i*.25+.4))
        if pp <= 0: continue
        x = cx+dx
        paper(ctx, lambda: ctx.rectangle(x-32, RY-52*pp, 64, 52*pp), [C['paper'], C['birch'], C['paper']][i], 1, sh=3)
        paper(ctx, lambda: (ctx.move_to(x-40, RY-52*pp), ctx.line_to(x+40, RY-52*pp), ctx.line_to(x, RY-52*pp-30*pp), ctx.close_path()), [C['pinel'], C['navyl'], C['berry']][i], 1, sh=2)

def village(ctx, cx, P, g=1, t=0):
    for i, dx in enumerate((-80, -22, 36)):
        pp = eob(seg(P, i*.15, i*.15+.35))
        if pp <= 0: continue
        x = cx+dx
        paper(ctx, lambda: ctx.rectangle(x-24, RY-34*pp, 48, 34*pp), C['tan'], 1, sh=3)
        paper(ctx, lambda: (ctx.move_to(x-30, RY-34*pp), ctx.line_to(x+30, RY-34*pp), ctx.line_to(x, RY-34*pp-24*pp), ctx.close_path()), C['berry'], 1, sh=2)
    h = eob(seg(P, .5, 1))
    if h > 0:
        x = cx+110
        paper(ctx, lambda: ctx.rectangle(x-36, RY-84*h, 72, 84*h), C['paper'], 1, sh=4)
        paper(ctx, lambda: ctx.rectangle(x-14, RY-84*h-30*h, 28, 30*h+2), C['paper'], 1, sh=3)
        paper(ctx, lambda: (ctx.move_to(x-18, RY-84*h-30*h), ctx.line_to(x+18, RY-84*h-30*h), ctx.line_to(x, RY-84*h-50*h), ctx.close_path()), C['pine'], 1, sh=2)
        if g > 0: glowdot(ctx, x, RY-45, 36, g*.5)

def watch(ctx, cx, P, g=1, t=0):
    for i, (dx, hh) in enumerate(((-44, 100), (0, 130), (44, 90))):
        pp = eoc(seg(P, i*.2, i*.2+.45))
        if pp <= 0: continue
        x = cx+dx; h = hh*pp
        paper(ctx, lambda: ctx.rectangle(x-12, RY-h, 24, h), C['paper'], 1, sh=3)
        if pp >= 1:
            paper(ctx, lambda: (ctx.move_to(x-18, RY-h), ctx.line_to(x+18, RY-h), ctx.line_to(x, RY-h-22), ctx.close_path()), C['navyl'], 1, sh=2)
            glowdot(ctx, x, RY-h+22, 26, g*.9)
            paper(ctx, lambda: ctx.rectangle(x-5, RY-h+14, 10, 14), lerpc(C['fog'], C['gold'], g), 1, sh=0)

def roads(ctx, P, g=1, t=0):
    reach = 40+1840*eoc(seg(P, 0, .8))
    ctx.save(); ctx.rectangle(0, RY-30, reach, 60); ctx.clip()
    paper(ctx, lambda: (ctx.move_to(-10, RY+2), *[ctx.line_to(x, RY+2+5*math.sin(x*.01)) for x in range(0, 1940, 40)], ctx.line_to(1940, RY+16), ctx.line_to(-10, RY+16), ctx.close_path()), C['tan'], 1, sh=3)
    for bx in (330, 1040, 1450):
        paper(ctx, lambda: (ctx.move_to(bx-50, RY+16), ctx.curve_to(bx-30, RY-22, bx+30, RY-22, bx+50, RY+16), ctx.close_path()), C['woodd'], 1, sh=3)
    ctx.restore()

FAR = {7: ('roads', None), 3: ('rb', 175), 4: ('parl', 450), 6: ('halls', 705), 8: ('village', 880), 9: ('watch', 1150), 5: ('court', 1560)}
FN = dict(roads=roads, rb=rb, parl=parl, halls=halls, village=village, watch=watch, court=court)

def draw_far(ctx, u, P, g, t):
    """ridge pieces: earlier units complete, current unit by progress P"""
    for k in (7, 3, 4, 6, 8, 9, 5):
        if k > 9 or k > u and not (u == 10): continue
        nm, x = FAR[k]
        pk, gk = (P, g) if k == u else (1., 1.)
        if k > u: continue
        if nm == 'roads': roads(ctx, pk, gk, t)
        else: FN[nm](ctx, x, pk, gk, t)

def draw_sky(ctx, u, P, t):
    if u == 10 and P > 0: aurora(ctx, t, .9*ease(P*1.4), y0=190, amp=.9)

def draw_front(ctx, u, P, g, t):
    if u == 2: rights(ctx, P, g, t)
    elif u > 2: rights(ctx, 1., 1., t)
