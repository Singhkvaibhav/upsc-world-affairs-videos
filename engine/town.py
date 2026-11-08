"""Town pieces: one small prop function per episode. Signature: piece(ctx, p, g, t, **kw)
p = build progress 0..1, g = glow / 'alive' amount 0..1, t = scene time (for gentle motion)."""
from engine.core import *

def glowdot(ctx, x, y, r, g, col=None):
    if g <= 0: return
    col = col or C['gold']
    gr = cairo.RadialGradient(x, y, 2, x, y, r)
    gr.add_color_stop_rgba(0, *col, .75*g); gr.add_color_stop_rgba(1, *col, 0)
    ctx.set_source(gr); ctx.arc(x, y, r, 0, 2*math.pi); ctx.fill()

# ---- Ep2: old paved road from the left edge into the square ----
def road(ctx, p, g=1, t=0, **k):
    if p <= 0: return
    reach = lerp(-20, 600, eoc(p))
    ctx.save(); ctx.rectangle(-30, 700, reach+30, 300); ctx.clip()
    def band():
        ctx.move_to(-30, 800); ctx.line_to(590, 796); ctx.line_to(640, 822); ctx.line_to(540, 884); ctx.line_to(-30, 884); ctx.close_path()
    paper(ctx, band, C['tan'], 1, sh=5)
    rng = random.Random(4)
    for r_ in range(4):
        y = 810+r_*18
        x = -30 + (r_ % 2)*27
        while x < 600:
            rgba(ctx, C['woodd'], .75); rrect(ctx, x, y, 50, 14, 4); ctx.fill()
            x += 54
    ctx.restore()

# ---- Ep3: lamp posts ----
LAMPX = [250+70*i for i in range(5)]
def lamps(ctx, p, g=1, t=0, **k):
    for i, x in enumerate(LAMPX):
        pp = eob(seg(p, i*.12, .45+i*.12))
        if pp <= 0: continue
        h = 150*pp
        paper(ctx, lambda: ctx.rectangle(x-4, 800-h, 8, h), C['ink'], 1, sh=3)
        if pp > .8:
            gg = g*(0.85+.15*math.sin(t*3+i))
            glowdot(ctx, x, 640, 90, gg)
            paper(ctx, lambda: rrect(ctx, x-14, 622, 28, 34, 6), lerpc(C['paper'], C['gold'], g), 1, sh=3)
            paper(ctx, lambda: (ctx.move_to(x-18, 622), ctx.line_to(x, 604), ctx.line_to(x+18, 622), ctx.close_path()), C['ink'], 1, sh=0)

# ---- Ep4: notice board with the blueprint pinned ----
def blueprint(ctx, cx, cy, w, h, a=1., roll=0.):
    """blueprint sheet; roll>0 draws it partly rolled up (0 = flat)."""
    sw = w*(1-roll)
    paper(ctx, lambda: rrect(ctx, cx-w/2, cy-h/2, max(sw, 1), h, 4), hx('CFE0EA'), a, sh=6)
    if sw > 30:
        ctx.save(); ctx.rectangle(cx-w/2, cy-h/2, sw, h); ctx.clip()
        rgba(ctx, (1, 1, 1), .55*a); ctx.set_line_width(2)
        for i in range(1, 8):
            ctx.move_to(cx-w/2+i*w/8, cy-h/2); ctx.line_to(cx-w/2+i*w/8, cy+h/2)
            ctx.move_to(cx-w/2, cy-h/2+i*h/8); ctx.line_to(cx+w/2, cy-h/2+i*h/8)
        ctx.stroke()
        rgba(ctx, (1, 1, 1), .85*a); ctx.set_line_width(3)
        ctx.rectangle(cx-w*.3, cy-h*.2, w*.24, h*.3); ctx.rectangle(cx+w*.04, cy-h*.28, w*.26, h*.42); ctx.stroke()
        ctx.restore()
    if roll > 0:
        rx = cx-w/2+sw
        paper(ctx, lambda: rrect(ctx, rx-8, cy-h/2-6, 34*roll+14, h+12, 14), hx('B9D0DD'), a, sh=6)

def noticeboard(ctx, p, g=1, t=0, **k):
    x, by = 1790, 810
    r = eoc(seg(p, 0, .5))
    if r > 0:
        hh = 170*r
        for dx in (-70, 70): paper(ctx, lambda: ctx.rectangle(x+dx-5, by-hh, 10, hh), C['woodd'], 1, sh=3)
        paper(ctx, lambda: rrect(ctx, x-95, by-hh-20, 190, 130*r, 8), C['wood'], 1, sh=6)
        rgba(ctx, C['woodd'], 1); rrect(ctx, x-95, by-hh-20, 190, 130*r, 8); ctx.set_line_width(5); ctx.stroke()
    q = seg(p, .5, 1)
    if q > 0:
        s = lerp(3.2, 1, eoc(q)); cx = lerp(960, x, eoc(q)); cy = lerp(520, by-hh+45, eoc(q))
        blueprint(ctx, cx, cy, 150*s, 100*s, 1)
        if q > .95: paper(ctx, lambda: ctx.arc(x, by-hh-12, 6, 0, 2*math.pi), C['berry'], 1, sh=2)

# ---- Ep5: Assembly hall ----
def hall(ctx, p, g=1, t=0, door=0., **k):
    cx, by, w, h = 1520, 812, 300, 190
    wp = eoc(seg(p, 0, .55))
    if wp > 0:
        paper(ctx, lambda: ctx.rectangle(cx-w/2, by-h*wp, w, h*wp), C['paper'], 1, sh=6)
    rp = eob(seg(p, .55, .85))
    if rp > 0:
        paper(ctx, lambda: (ctx.move_to(cx-w/2-22, by-h), ctx.line_to(cx+w/2+22, by-h), ctx.line_to(cx, by-h-95*rp), ctx.close_path()), C['far'], rp, sh=5)
        paper(ctx, lambda: ctx.arc(cx, by-h-95*rp+8, 28*rp, math.pi, 2*math.pi), C['pinell'], rp, sh=0)
    dp = eob(seg(p, .85, 1))
    if dp > 0:
        for dx in (-95, 95):
            wcol = lerpc(C['fog'], C['gold'], g)
            glowdot(ctx, cx+dx, by-100, 70, g)
            paper(ctx, lambda: rrect(ctx, cx+dx-22, by-130, 44, 56*dp, 6), wcol, 1, sh=2)
        dw = 70 + 40*door
        paper(ctx, lambda: rrect(ctx, cx-dw/2, by-110*dp, dw, 110*dp, 28), lerpc(C['pine'], C['gold'], door*.8) if door else C['pine'], 1, sh=3)
        if door > 0: glowdot(ctx, cx, by-50, 120, door)

# ---- Ep6: signpost ----
SIGNS = ["UK", "USA", "Ireland", "Canada", "Australia", "Germany", "USSR", "France"]
def signpost(ctx, p, g=1, t=0, **k):
    x, by = 620, 808
    h = 300*eoc(seg(p, 0, .3))
    if h <= 0: return
    paper(ctx, lambda: ctx.rectangle(x-7, by-h, 14, h), C['woodd'], 1, sh=4)
    for i, nm in enumerate(SIGNS):
        pp = eob(seg(p, .3+i*.08, .55+i*.08))
        if pp <= 0: continue
        y = by-h+14+i*33; d = 1 if i % 2 == 0 else -1
        L = 105*pp
        def board():
            ctx.move_to(x, y); ctx.line_to(x+d*(L-18), y); ctx.line_to(x+d*L, y+14); ctx.line_to(x+d*(L-18), y+28); ctx.line_to(x, y+28); ctx.close_path()
        paper(ctx, board, [C['pinel'], C['navyl'], C['berry'], C['gold']][i % 4], 1, sh=3)
        if g > 0 and pp > .9:
            text(ctx, nm, x+d*(L/2-8), y+20, 16, C['paper'], g, bold=True)
    if p >= 1: glowdot(ctx, x, by-h, 80, g*.5, C['paper'])

# ---- Ep7: clock tower with balance scale ----
def tower(ctx, p, g=1, t=0, **k):
    cx, by, w, h = 1275, 716, 120, 300
    r = eoc(seg(p, 0, .7))
    if r > 0:
        paper(ctx, lambda: ctx.rectangle(cx-w/2, by-h*r, w, h*r), C['paper'], 1, sh=6)
        paper(ctx, lambda: ctx.rectangle(cx-w/2-8, by-14, w+16, 14), C['fog'], 1, sh=3)
    tp = eob(seg(p, .7, 1))
    if tp > 0:
        top = by-h
        paper(ctx, lambda: (ctx.move_to(cx-w/2-8, top), ctx.line_to(cx+w/2+8, top), ctx.line_to(cx, top-70*tp), ctx.close_path()), C['pine'], 1, sh=4)
        # clock face
        fy = top+62
        paper(ctx, lambda: ctx.arc(cx, fy, 36, 0, 2*math.pi), C['birch'], 1, sh=3)
        ang = t*(2.2 if g >= 1 else 0.0)
        for L_, sp, wd in ((24, 1, 4), (16, 1/12, 5)):
            a_ = ang*sp-math.pi/2 + (0 if sp == 1 else 1.0)
            rgba(ctx, C['ink'], 1); ctx.set_line_width(wd); ctx.move_to(cx, fy); ctx.line_to(cx+L_*math.cos(a_), fy+L_*math.sin(a_)); ctx.stroke()
        # balance scale on top
        sy = top-70*tp-20
        rgba(ctx, C['ink'], 1); ctx.set_line_width(5); ctx.move_to(cx, sy); ctx.line_to(cx, sy+30); ctx.stroke()
        tilt = (1-g)*.35*math.sin(t*1.8) if tp > .9 else 0
        ctx.save(); ctx.translate(cx, sy); ctx.rotate(tilt)
        rgba(ctx, C['gold'], 1); ctx.set_line_width(6); ctx.move_to(-62, 0); ctx.line_to(62, 0); ctx.stroke()
        for dx in (-62, 62):
            ctx.save(); ctx.translate(dx, 0); ctx.rotate(-tilt)
            rgba(ctx, C['ink'], .6); ctx.set_line_width(2); ctx.move_to(0, 0); ctx.line_to(-22, 24); ctx.move_to(0, 0); ctx.line_to(22, 24); ctx.stroke()
            paper(ctx, lambda: ctx.arc(0, 24, 24, 0, math.pi), C['gold'], 1, sh=0)
            ctx.restore()
        ctx.restore()
        paper(ctx, lambda: ctx.arc(cx, sy, 6, 0, 2*math.pi), C['gold'], 1, sh=0)

# ---- Ep8: Preamble wall (blank stone wall beside the foundation stone) ----
def wall(ctx, p, g=1, t=0, **k):
    cx, by, w, h = 820, 708, 190, 118
    r = eoc(p)
    if r <= 0: return
    hh = h*r
    paper(ctx, lambda: rrect(ctx, cx-w/2, by-hh, w, hh, 8), hx('B4BABD'), 1, sh=8)
    ctx.save(); ctx.rectangle(cx-w/2, by-hh, w, hh); ctx.clip()
    rgba(ctx, (1, 1, 1), .28); ctx.set_line_width(2)
    for j in range(5):
        y = by-j*26
        ctx.move_to(cx-w/2, y); ctx.line_to(cx+w/2, y)
        for i in range(4): ctx.move_to(cx-w/2+i*50+(j % 2)*25, y); ctx.line_to(cx-w/2+i*50+(j % 2)*25, y-26)
    ctx.stroke(); ctx.restore()
    if g > 0:
        glowdot(ctx, cx, by-h/2, 150, g*.5, C['gold'])
        if p >= 1:
            for i, yy in enumerate((by-92, by-72, by-52)):
                rgba(ctx, C['ink'], .45*g); ctx.rectangle(cx-70+(i % 2)*8, yy, 140-(i % 2)*16, 4); ctx.fill()

# ---- Ep9: boundary stones ring ----
RING = [(960+900*math.cos(a), 800+104*math.sin(a)) for a in [i*2*math.pi/30 for i in range(30)]]
def stones(ctx, p, g=1, t=0, **k):
    for i, (x, y) in enumerate(RING):
        if x < 300: continue   # keep the gate clear
        pp = eob(seg(p, i/30*.7, i/30*.7+.3))
        if pp <= 0: continue
        s = pp*(1+.25*g*math.sin(t*3+i)**2)
        if g > 0: glowdot(ctx, x, y-6, 36, g*.6)
        paper(ctx, lambda: rrect(ctx, x-13*s, y-18*s, 26*s, 18*s, 5), hx('A9B0B4'), 1, sh=3)

# ---- Ep10: gate with a name board ----
def gate(ctx, p, g=1, t=0, name="BHARAT", **k):
    x, by = 130, 892
    r = eoc(seg(p, 0, .6))
    if r <= 0: return
    hh = 215*r
    for dx in (-85, 85):
        paper(ctx, lambda: ctx.rectangle(x+dx-11, by-hh, 22, hh), C['woodd'], 1, sh=4)
    ar = eob(seg(p, .6, .85))
    if ar > 0:
        paper(ctx, lambda: rrect(ctx, x-110, by-hh-6, 220, 26*ar, 8), C['woodd'], ar, sh=4)
        for sx in (-1, 1):
            ang = -.0*sx
            paper(ctx, lambda: ctx.rectangle(x+sx*30-3, by-hh+20, 6, 30*ar), C['woodd'], ar, sh=0)
    nb = eob(seg(p, .85, 1))
    if nb > 0:
        glowdot(ctx, x, by-hh+78, 130, g)
        paper(ctx, lambda: rrect(ctx, x-70, by-hh+48, 140, 56, 10), lerpc(C['wood'], C['paper'], g), nb, sh=4)
        text(ctx, name, x, by-hh+86, 28, lerpc(C['fogd'], C['pine'], g), nb, bold=True)

# ---- Ep11: map board ----
BLOBS = [((985, 505), [(-70, -30), (-30, -60), (30, -45), (55, -5), (20, 40), (-40, 50), (-75, 10)], 'pinel'),
         ((1090, 560), [(-45, -35), (10, -50), (50, -10), (35, 40), (-20, 55), (-50, 15)], 'gold'),
         ((930, 590), [(-50, -25), (0, -45), (45, -20), (50, 20), (0, 45), (-45, 25)], 'berry'),
         ((1040, 610), [(-30, -25), (30, -30), (45, 10), (5, 35), (-35, 20)], 'navyl')]
def mapboard(ctx, p, g=1, t=0, **k):
    cx, by = 1070, 712
    r = eoc(seg(p, 0, .4))
    if r <= 0: return
    hh = 250*r
    for dx in (-110, 110): paper(ctx, lambda: ctx.rectangle(cx+dx-6, by-hh+150, 12, hh-150+0), C['woodd'], 1, sh=3)
    paper(ctx, lambda: rrect(ctx, cx-150, by-hh, 300, 210*r, 10), C['wood'], 1, sh=7)
    paper(ctx, lambda: rrect(ctx, cx-136, by-hh+14, 272, 182*r, 6), C['birch'], 1, sh=0)
    for i, ((bx, by_), pts, col) in enumerate(BLOBS):
        pp = eob(seg(p, .4+i*.13, .6+i*.13))
        if pp <= 0: continue
        def blob():
            ctx.move_to(bx+(cx-1020)+pts[0][0]*pp*.9, by_+pts[0][1]*pp*.9+(by-712))
            for (qx, qy) in pts[1:]: ctx.line_to(bx+(cx-1020)+qx*pp*.9, by_+qy*pp*.9+(by-712))
            ctx.close_path()
        paper(ctx, blob, C[col], .9, sh=2)
    if g > 0 and p >= 1: glowdot(ctx, cx, by-hh+105, 200, g*.35)

BACK = [('hall', hall), ('board', noticeboard), ('tower', tower), ('wall', wall), ('map', mapboard)]
FRONT = [('road', road), ('lamps', lamps), ('sign', signpost), ('gate', gate), ('stones', stones)]
ORDER = {'road': 2, 'lamps': 3, 'board': 4, 'hall': 5, 'sign': 6, 'tower': 7, 'wall': 8, 'stones': 9, 'gate': 10, 'map': 11}
ALL = dict(BACK+FRONT)
