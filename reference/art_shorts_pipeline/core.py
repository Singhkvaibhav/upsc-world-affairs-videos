import cairo, math, random, os

EP = 1  # episode number shown in the corner tag; set by the runner
SERIES = "ART & CULTURE"  # corner tag: "ART & CULTURE · EP N"
SERIES_TITLE = "ART AND CULTURE, SIMPLY SEEN"  # title card

# Frame size is chosen per run: ART_VERTICAL=1 renders the 1080x1920 Shorts (about 52 s)
VERTICAL = bool(os.environ.get('ART_VERTICAL'))
W, H, FPS = (1080, 1920, 30) if VERTICAL else (1920, 1080, 30)
TOTAL = 52.0 if VERTICAL else 300.0
LEAD = 0.9

def hx(h):
    h = h.lstrip('#'); return tuple(int(h[i:i+2], 16)/255 for i in (0, 2, 4))

C = {k: hx(v) for k, v in dict(
    birch='F2EEE6', paper='FAF7F1', fog='C9CDD1', fogd='8E969C', pine='2F4F43', pinel='5E7F6E',
    pinell='8FA89C', far='B9C6C4', navy='1F2A3A', navyl='34435A', berry='B23A48', aur='7FE0B0',
    vio='A68BF0', wood='E6D7BF', woodd='CDB894', sand='D9B98A', tan='D8C6A2', ink='2A3340',
    sky='DCE3E6', gold='C9A45C',
    cotton='EFE6D3', cottond='E2D6BC', indigo='24345E', indigol='3E5486', madder='A63A2E', turmeric='D9A62B',
    leaf='5E7B3A', inkb='22201D', zari='D8B45A', thread='6B5A3E').items()}

# ---------- easing ----------
def cl(x, a=0., b=1.): return max(a, min(b, x))
def seg(t, a, b): return cl((t - a) / (b - a)) if b > a else float(t >= a)
def ease(x): x = cl(x); return x*x*(3-2*x)
def eoc(x): x = cl(x); return 1-(1-x)**3
def eob(x, s=1.6):
    x = cl(x); x -= 1; return x*x*((s+1)*x+s)+1
def lerp(a, b, x): return a+(b-a)*x

# ---------- drawing helpers ----------
def rgba(ctx, c, a=1.): ctx.set_source_rgba(c[0], c[1], c[2], a)

def rrect(ctx, x, y, w, h, r):
    r = min(r, w/2, h/2)
    ctx.new_sub_path()
    ctx.arc(x+w-r, y+r, r, -math.pi/2, 0); ctx.arc(x+w-r, y+h-r, r, 0, math.pi/2)
    ctx.arc(x+r, y+h-r, r, math.pi/2, math.pi); ctx.arc(x+r, y+r, r, math.pi, 1.5*math.pi)
    ctx.close_path()

def paper(ctx, path, col, a=1., sh=7, sha=0.14):
    if a <= 0: return
    ctx.new_path()
    if sh:
        ctx.save(); ctx.translate(0, sh); ctx.new_path(); path(); rgba(ctx, (0.12, 0.16, 0.2), sha*a); ctx.fill(); ctx.restore()
    ctx.new_path(); path(); rgba(ctx, col, a); ctx.fill()

def font(ctx, size, bold=False, serif=False):
    ctx.select_font_face("DejaVu Serif" if serif else "Inter", cairo.FONT_SLANT_NORMAL,
                         cairo.FONT_WEIGHT_BOLD if bold else cairo.FONT_WEIGHT_NORMAL)
    ctx.set_font_size(size)

def text(ctx, s, x, y, size, col, a=1., bold=False, align='c', serif=False, glow=None):
    if a <= 0: return
    font(ctx, size, bold, serif)
    e = ctx.text_extents(s)
    xx = x - (e.x_advance/2 if align == 'c' else e.x_advance if align == 'r' else 0)
    if glow:
        for w, ga in ((26, .06), (16, .1), (8, .18)):
            ctx.move_to(xx, y); ctx.text_path(s); ctx.set_line_width(w)
            ctx.set_line_join(cairo.LINE_JOIN_ROUND); rgba(ctx, glow, ga*a); ctx.stroke()
    ctx.move_to(xx, y); rgba(ctx, col, a); ctx.show_text(s)
    return e.x_advance

def wrap(ctx, s, size, maxw, bold=False):
    font(ctx, size, bold)
    words, lines, cur = s.split(), [], ''
    for w_ in words:
        t = (cur+' '+w_).strip()
        if ctx.text_extents(t).x_advance > maxw and cur: lines.append(cur); cur = w_
        else: cur = t
    if cur: lines.append(cur)
    return lines

def label(ctx, s, x, y, size, a=1., fg=None, bg=None, pad=14):
    """pill label centered at x, baseline-ish y"""
    if a <= 0: return
    fg = fg or C['ink']; bg = bg or C['paper']
    font(ctx, size); e = ctx.text_extents(s)
    w, h = e.x_advance+pad*2, size*1.7
    paper(ctx, lambda: rrect(ctx, x-w/2, y-h/2, w, h, h/2), bg, a, sh=4, sha=.12)
    text(ctx, s, x, y+size*0.36, size, fg, a)

def heading(ctx, num, s, a):
    # top heading like "1 · Creates"
    if a <= 0: return
    y = 150
    if num:
        paper(ctx, lambda: ctx.arc(860-0, y-16, 0, 0, 0), C['pine'], 0)
    text(ctx, (f"{num}  ·  " if num else '') + s, W/2, y, 64, C['navy'], a, bold=True)

# ---------- backgrounds ----------
def shrink(ctx):
    ctx.translate(W/2, 90); ctx.scale(.85, .85); ctx.translate(-W/2, -90)

def grad(ctx, top, bot, a=1.):
    g = cairo.LinearGradient(0, 0, 0, H)
    g.add_color_stop_rgba(0, *top, a); g.add_color_stop_rgba(1, *bot, a)
    ctx.set_source(g); ctx.paint()

def hill(ctx, base, amp, f1, f2, ph, col, shift=0, a=1.):
    def p():
        ctx.move_to(-20, H+20)
        for x in range(-20, W+41, 40):
            xx = x+shift
            ctx.line_to(x, base - amp*(0.6*math.sin(xx*f1+ph) + 0.4*math.sin(xx*f2+ph*1.7)))
        ctx.line_to(W+40, H+20); ctx.close_path()
    paper(ctx, p, col, a, sh=8, sha=.10)

def tree(ctx, x, y, s, a=1.):
    # birch: white trunk with dark marks, simple pine-ish canopy dots
    rgba(ctx, C['paper'], a); ctx.rectangle(x-4*s, y-90*s, 8*s, 90*s); ctx.fill()
    rgba(ctx, C['ink'], .55*a)
    for k in range(4):
        ctx.rectangle(x-4*s, y-(20+18*k)*s, 5*s, 2.5*s); ctx.fill()
    paper(ctx, lambda: ctx.arc(x, y-100*s, 26*s, 0, 2*math.pi), C['pinell'], a, sh=4)

def fogbands(ctx, t, a=1.):
    for i in range(4):
        x = ((t*18*(1+i*.3) + i*600) % (W+1200)) - 600
        y = 640 + i*90
        g = cairo.RadialGradient(x, y, 10, x, y, 520)
        g.add_color_stop_rgba(0, 1, 1, 1, .55*a); g.add_color_stop_rgba(1, 1, 1, 1, 0)
        ctx.save(); ctx.translate(x, y); ctx.scale(1, .22); ctx.translate(-x, -y)
        ctx.set_source(g); ctx.arc(x, y, 520, 0, 2*math.pi); ctx.fill(); ctx.restore()

def bg_land(ctx, t, pan=0., night=0.):
    grad(ctx, C['sky'], C['birch'])
    if night > 0: grad(ctx, C['navy'], C['navyl'], night)
    # pale sun
    rgba(ctx, (1, 1, 1), .5*(1-night)); ctx.arc(1420, 300, 90, 0, 2*math.pi); ctx.fill()
    hill(ctx, 640, 60, .0031, .0072, .4, C['far'], pan*.3)
    hill(ctx, 760, 50, .0042, .0093, 1.9, C['pinell'], pan*.6)
    for i, x in enumerate((150, 230, 1650, 1730, 1810)):
        tree(ctx, x - (pan*.6) % 1 * 0, 790 + (i % 2)*20, 1.0 + .2*(i % 3))
    hill(ctx, 900, 36, .0051, .0121, 3.1, C['pinel'], pan)
    if night > 0:
        rgba(ctx, C['navy'], .35*night); ctx.paint()

def bg_paper(ctx):
    grad(ctx, C['paper'], C['birch'])
    g = cairo.RadialGradient(W/2, H/2, 300, W/2, H/2, 1200)
    g.add_color_stop_rgba(0, 0, 0, 0, 0); g.add_color_stop_rgba(1, .2, .2, .15, .10)
    ctx.set_source(g); ctx.paint()
    shrink(ctx)
    rgba(ctx, C['fog'], .7); ctx.rectangle(-400, 860, W+800, 3); ctx.fill()

def bg_desk(ctx):
    grad(ctx, C['wood'], hx('DDCBAE'))
    rng = random.Random(3)
    for i in range(0, H, 135):
        rgba(ctx, C['woodd'], .35); ctx.rectangle(0, i, W, 2); ctx.fill()
        for k in range(6):
            x = rng.uniform(0, W); rgba(ctx, C['woodd'], .18)
            ctx.save(); ctx.translate(x, i+rng.uniform(30, 100)); ctx.scale(rng.uniform(60, 160), 3)
            ctx.arc(0, 0, 1, 0, 2*math.pi); ctx.restore(); ctx.fill()
    g = cairo.RadialGradient(W/2, H/2, 400, W/2, H/2, 1200)
    g.add_color_stop_rgba(0, 0, 0, 0, 0); g.add_color_stop_rgba(1, .2, .12, .05, .18)
    ctx.set_source(g); ctx.paint()
    shrink(ctx)

def stars(ctx, t, a=1.):
    rng = random.Random(7)
    for i in range(140):
        x, y = rng.uniform(0, W), rng.uniform(0, 620); r = rng.uniform(.8, 2.2)
        tw = .5+.5*math.sin(t*rng.uniform(.8, 2)+i)
        rgba(ctx, (1, 1, 1), a*(.3+.5*tw)); ctx.arc(x, y, r, 0, 2*math.pi); ctx.fill()

def bg_night(ctx, t):
    grad(ctx, hx('121A28'), C['navyl'])
    stars(ctx, t)
    hill(ctx, 900, 40, .0042, .0093, 1.9, hx('1A2633'))
    hill(ctx, 980, 30, .0051, .0121, 3.1, hx('152029'))

def aurora(ctx, t, a=1., y0=260, amp=1.):
    if a <= 0: return
    for k in range(3):
        pts = []
        for x in range(-60, W+61, 30):
            y = y0 + k*55 + amp*(70*math.sin(x*.0035 + t*.5 + k*1.3) + 28*math.sin(x*.011 - t*.7 + k))
            pts.append((x, y))
        # curtain
        for (x, y) in pts[::1]:
            g = cairo.LinearGradient(0, y, 0, y+230)
            mix = x/W
            col = tuple(lerp(C['aur'][i], C['vio'][i], mix) for i in range(3))
            g.add_color_stop_rgba(0, *col, .16*a*(.7+.3*math.sin(t*1.3+x*.01+k)))
            g.add_color_stop_rgba(1, *col, 0)
            ctx.set_source(g); ctx.rectangle(x-15, y, 30, 230); ctx.fill()
        lg = cairo.LinearGradient(0, 0, W, 0)
        lg.add_color_stop_rgba(0, *C['aur'], 1); lg.add_color_stop_rgba(1, *C['vio'], 1)
        for w, ga in ((40, .07), (18, .14), (5, .5)):
            ctx.move_to(*pts[0])
            for p in pts[1:]: ctx.line_to(*p)
            ctx.set_line_width(w); ctx.set_line_cap(cairo.LINE_CAP_ROUND)
            ctx.save(); ctx.push_group(); ctx.set_source(lg); ctx.stroke(); ctx.pop_group_to_source()
            ctx.paint_with_alpha(ga*a); ctx.restore()

# ---------- props ----------
def person(ctx, x, y, s, col, a=1., robe=False, seated=False):
    if a <= 0: return
    bh = (30 if seated else 44)*s
    paper(ctx, lambda: rrect(ctx, x-18*s, y-bh, 36*s, bh+6*s, 16*s), C['ink'] if robe else col, a, sh=4)
    if robe:
        rgba(ctx, (1, 1, 1), a); ctx.move_to(x-5*s, y-bh+3*s); ctx.line_to(x, y-bh+16*s); ctx.line_to(x+5*s, y-bh+3*s); ctx.close_path(); ctx.fill()
    paper(ctx, lambda: ctx.arc(x, y-bh-14*s, 12*s, 0, 2*math.pi), hx('C99B78'), a, sh=3)

PCOLS = [C['pinel'], C['berry'], C['navyl'], C['gold'], C['pine'], hx('7A8FA6'), hx('B98B6E')]

def building(ctx, cx, by, w, h, p=1., a=1., doors=True, col=None, dome=False):
    """paper civic building assembling with progress p"""
    col = col or C['paper']
    if a <= 0: return
    # base
    pb = eoc(seg(p, 0, .25))
    paper(ctx, lambda: ctx.rectangle(cx-w/2-20, by-18*pb, w+40, 18*pb), C['fogd'], a)
    # columns
    n = 6; cw = w/(n*2-1)
    for i in range(n):
        pc = eob(seg(p, .2+i*.05, .5+i*.05))
        x = cx-w/2+i*2*cw
        ch = (h-60)*pc
        paper(ctx, lambda: ctx.rectangle(x, by-18-ch, cw, ch), col, a, sh=5)
    # roof
    pr = eob(seg(p, .55, .8))
    ry = by-18-(h-60) - 140*(1-pr)
    if pr > 0:
        def roof():
            ctx.move_to(cx-w/2-30, ry); ctx.line_to(cx+w/2+30, ry); ctx.line_to(cx, ry-70); ctx.close_path()
        paper(ctx, roof, C['far'], a*pr)
        paper(ctx, lambda: ctx.rectangle(cx-w/2-30, ry, w+60, 16), C['fog'], a*pr, sh=3)
        if dome:
            paper(ctx, lambda: ctx.arc(cx, ry-60, 46, math.pi, 2*math.pi), col, a*pr)
    if doors:
        for i in range(3):
            pd = eob(seg(p, .8+i*.05, .95+i*.05))
            dx = cx-w/2+(1+i*2)*cw*1.66 - cw*0.33
            dx = cx + (i-1)*w*0.33
            dh = 110*pd
            paper(ctx, lambda: rrect(ctx, dx-32, by-18-dh, 64, dh, 30), [C['pine'], C['navyl'], C['berry']][i], a, sh=3)

def book(ctx, cx, cy, w, h, openp=0., col=None, a=1., thick=24, pages_col=None):
    col = col or C['pine']
    if a <= 0: return
    if openp <= 0.001:
        paper(ctx, lambda: rrect(ctx, cx-w/2, cy-h/2, w, h, 10), col, a, sh=10)
        rgba(ctx, C['gold'], .8*a); ctx.rectangle(cx-w/2+28, cy-h/2+40, w-56, 3); ctx.fill()
        ctx.rectangle(cx-w/2+28, cy+h/2-43, w-56, 3); ctx.fill()
        return
    o = ease(openp)
    # back cover
    paper(ctx, lambda: rrect(ctx, cx-w*o-14, cy-h/2-10, w*(1+o)+28, h+20, 12), col, a, sh=10)
    # right page block
    paper(ctx, lambda: rrect(ctx, cx, cy-h/2, w-6, h, 6), pages_col or C['paper'], a, sh=0)
    # left page (opening)
    paper(ctx, lambda: rrect(ctx, cx-w*o+6, cy-h/2, w*o-6, h, 6), pages_col or C['paper'], a, sh=0)
    rgba(ctx, C['fog'], a); ctx.rectangle(cx-1.5, cy-h/2, 3, h); ctx.fill()
    for i in range(7):
        rgba(ctx, C['fog'], a*o*.9)
        ctx.rectangle(cx+30, cy-h/2+50+i*34, w-80, 4); ctx.fill()
        if w*o > 90: ctx.rectangle(cx-w*o+36, cy-h/2+50+i*34, w*o-80, 4); ctx.fill()

def hourglass(ctx, cx, cy, s, p, a=1.):
    hw, hh = 110*s, 170*s
    def glass():
        ctx.move_to(cx-hw, cy-hh); ctx.line_to(cx+hw, cy-hh); ctx.line_to(cx+12, cy)
        ctx.line_to(cx+hw, cy+hh); ctx.line_to(cx-hw, cy+hh); ctx.line_to(cx-12, cy); ctx.close_path()
    paper(ctx, glass, (1, 1, 1), .55*a, sh=6)
    # top sand
    lvl = 1-p
    if lvl > .02:
        ty = cy - hh*lvl*.9
        x = hw*(cy-ty)/hh*.95+10
        rgba(ctx, C['sand'], a); ctx.move_to(cx-x, ty); ctx.line_to(cx+x, ty); ctx.line_to(cx+10, cy-6); ctx.line_to(cx-10, cy-6); ctx.close_path(); ctx.fill()
        ctx.rectangle(cx-2, cy-6, 4, hh-6); ctx.fill()
    # bottom pile
    ph = hh*.85*p
    rgba(ctx, C['sand'], a)
    ctx.move_to(cx-hw+8, cy+hh); ctx.curve_to(cx-hw*.5, cy+hh-ph*.3, cx-20, cy+hh-ph, cx, cy+hh-ph)
    ctx.curve_to(cx+20, cy+hh-ph, cx+hw*.5, cy+hh-ph*.3, cx+hw-8, cy+hh); ctx.close_path(); ctx.fill()
    for yy in (cy-hh-14, cy+hh):
        paper(ctx, lambda: rrect(ctx, cx-hw-30, yy, 2*hw+60, 16, 6), C['woodd'], a, sh=4)

def corner(ctx, a=1.):
    ctx.save(); ctx.identity_matrix()
    text(ctx, f"{SERIES}  ·  EP {EP}", 70, 80, 22, C['fogd'], .9*a, bold=True, align='l')
    ctx.restore()

def caption(ctx, s, a):
    if a <= 0: return
    lines = wrap(ctx, s, 34, 1480)
    lh = 46; bw = 0
    font(ctx, 34)
    for l in lines: bw = max(bw, ctx.text_extents(l).x_advance)
    bh = lh*len(lines)+28; bw += 60
    y0 = H-60-bh
    rrect(ctx, W/2-bw/2, y0, bw, bh, 22); rgba(ctx, C['paper'], .86*a); ctx.fill()
    for i, l in enumerate(lines):
        text(ctx, l, W/2, y0+14+lh*i+34, 34, C['ink'], a)

def square_ground(ctx, a=1.):
    def g():
        ctx.move_to(560, 820); ctx.line_to(760, 700); ctx.line_to(1160, 700); ctx.line_to(1360, 820); ctx.close_path()
    paper(ctx, g, C['tan'], a, sh=6)
    ctx.set_dash([18, 12]); ctx.set_line_width(3); rgba(ctx, C['woodd'], a)
    ctx.move_to(700, 800); ctx.line_to(820, 722); ctx.line_to(1100, 722); ctx.line_to(1220, 800); ctx.close_path(); ctx.stroke()
    ctx.set_dash([])

def stone(ctx, cx, cy, a=1., outline=False, engraved=None):
    if outline:
        ctx.set_dash([14, 10]); ctx.set_line_width(4); rgba(ctx, C['ink'], .6*a)
        rrect(ctx, cx-130, cy-60, 260, 120, 18); ctx.stroke(); ctx.set_dash([]); return
    paper(ctx, lambda: rrect(ctx, cx-130, cy-60, 260, 120, 18), hx('A9B0B4'), a, sh=10, sha=.2)
    rgba(ctx, (1, 1, 1), .25*a); ctx.rectangle(cx-110, cy-48, 220, 6); ctx.fill()
    if engraved:
        text(ctx, engraved, cx, cy+12, 26, C['ink'], .75*a, bold=True)

def stamp(ctx, cx, cy, top, mid, bot, col, p, rot):
    if p <= 0: return
    s = lerp(1.5, 1, eoc(p)); a = ease(p*1.6)
    ctx.save(); ctx.translate(cx, cy); ctx.rotate(rot); ctx.scale(s, s)
    paper(ctx, lambda: rrect(ctx, -300, -150, 600, 300, 26), C['paper'], a, sh=10)
    rgba(ctx, col, a); ctx.set_line_width(6); rrect(ctx, -280, -130, 560, 260, 20); ctx.stroke()
    text(ctx, top, 0, -60, 34, col, a, bold=True)
    text(ctx, mid, 0, 30, 70, col, a, bold=True)
    text(ctx, bot, 0, 95, 30, C['ink'], a)
    ctx.restore()

def card(ctx, x, y, w, h, a=1., col=None):
    paper(ctx, lambda: rrect(ctx, x, y, w, h, 18), col or C['paper'], a, sh=12, sha=.2)

def slide_in(t, a, b):
    return lerp(H+200, 0, eoc(seg(t, a, b)))

def toggle(ctx, x, y, on, a=1.):
    paper(ctx, lambda: rrect(ctx, x, y, 140, 64, 32), lerpc(C['fog'], C['pinel'], on), a, sh=3)
    paper(ctx, lambda: ctx.arc(x+32+76*on, y+32, 24, 0, 2*math.pi), C['paper'], a, sh=3)

def lerpc(a, b, x): return tuple(lerp(a[i], b[i], x) for i in range(3))

def town_silhouette(ctx, a):
    if a <= 0: return
    col = C['fogd']
    rgba(ctx, col, .5*a)
    xs = [(520, 70, 90), (620, 60, 120), (700, 90, 70), (1180, 70, 100), (1280, 80, 80), (1380, 60, 110)]
    for x, w, h in xs:
        ctx.rectangle(x, 800-h, w, h); ctx.move_to(x-6, 800-h); ctx.line_to(x+w/2, 800-h-40); ctx.line_to(x+w+6, 800-h); ctx.close_path()
    ctx.fill()
    ctx.rectangle(840, 640, 240, 160); ctx.fill(); ctx.arc(960, 640, 90, math.pi, 2*math.pi); ctx.fill()

# ---------- narration cues ----------
BEAT = {}   # current beat dict, set by the runner before each scene call

def cue(phrase, lead=-0.25):
    """Time (s, within the beat) at which `phrase` starts being spoken (char-proportional estimate)."""
    txt = BEAT['narr']; i = txt.find(phrase)
    if i < 0: raise ValueError(f"cue phrase not in narration: {phrase!r}")
    return LEAD + BEAT['vo'] * i / len(txt) + lead

def T(x):
    return cue(x) if isinstance(x, str) else x() if callable(x) else x

def spread(n, a=.1, b=.88):
    """n cue times spread evenly across the spoken narration (for lists that follow the narration in order)"""
    return [(lambda i=i: LEAD + BEAT['vo']*(a+(b-a)*i/max(n-1, 1)) - .2) for i in range(n)]
