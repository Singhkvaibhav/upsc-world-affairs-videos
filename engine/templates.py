"""Generic scene templates (TOWN, TIMELINE, STAMP, BOARD, CARDS, AURORA, UPSC CARD).
Layers are f(ctx, t, D); `scene()` stacks them on a background. Time args accept seconds or a narration phrase."""
from engine.core import *
from engine import town as tw
from engine import units as un

BGS = {'paper': lambda ctx, t: bg_paper(ctx), 'desk': lambda ctx, t: bg_desk(ctx)}
ACC = [C['pine'], C['navyl'], C['berry'], hx('9C7A3C'), C['pinel'], hx('7A8FA6')]

def scene(bg, *layers, tag=True):
    flat = []
    for L in layers: flat += getattr(L, 'layers', [L])   # a nested scene contributes its layers, not its background
    def f(ctx, t, D):
        BGS[bg](ctx, t)
        if tag: corner(ctx)
        for L in flat: L(ctx, t, D)
    f.bg = bg; f.layers = flat
    return f

def wrap_s(ctx, s, size, maxw, bold=False, serif=True):
    font(ctx, size, bold, serif)
    lines, cur = [], ''
    for w_ in s.split():
        tt = (cur+' '+w_).strip()
        if ctx.text_extents(tt).x_advance > maxw and cur: lines.append(cur); cur = w_
        else: cur = tt
    if cur: lines.append(cur)
    return lines

def pop(ctx, x, y, p, draw):
    """scale-in about (x, y)"""
    if p <= 0: return
    ctx.save(); ctx.translate(x, y); ctx.scale(p, p); ctx.translate(-x, -y); draw(); ctx.restore()

# ---------------- TOWN ----------------
def town(ep, build=(.6, 3.2), glow=None, night=0., over=None, under=None, kw=None, fog=.9):
    cur = [k for k, v in tw.ORDER.items() if v == ep][0]
    prior = {k for k, v in tw.ORDER.items() if v < ep}
    kw = kw or {}
    def prog(t, rng, default):
        if rng is None: return default
        q = seg(t, T(rng[0]), T(rng[1]))
        return rng[2] + (rng[3]-rng[2])*q if len(rng) > 2 else q
    def f(ctx, t, D):
        bg_land(ctx, t, night=night); fogbands(ctx, t, fog)
        if under: under(ctx, t, D)
        P, G = prog(t, build, 1.), prog(t, glow, 0.)
        for grp in (tw.BACK, None, tw.FRONT):
            if grp is None: square_ground(ctx); continue
            for nm, fn in grp:
                if nm in prior: fn(ctx, 1, 1, t)
                elif nm == cur: fn(ctx, P, G, t, **{a: (v(t) if callable(v) else v) for a, v in kw.items()})
        stone(ctx, 960, 745, 1, engraved="FOUNDATION · EP 1")
        if over: over(ctx, t, D)
    f.bg = 'land'
    return f

def town2(ep, build=None, glow=None, night=0., over=None, under=None, fog=.9):
    """TOWN scene for Units 2-10. The unit's piece grows across the unit's episodes: P = (episode index + p) / episode count.
    build=(t0, t1, p0, p1) maps scene time to p (None = piece stays at p=0..); glow likewise (0..1)."""
    u = un.unit_of(ep); a, b = un.UNITS[u]; n = b-a+1; idx = ep-a
    def prog(t, rng, default):
        if rng is None: return default
        q = seg(t, T(rng[0]), T(rng[1]))
        return rng[2] + (rng[3]-rng[2])*q if len(rng) > 2 else q
    def f(ctx, t, D):
        bg_land(ctx, t, night=night); fogbands(ctx, t, fog)
        p = prog(t, build, 0.); P = (idx+p)/n; G = prog(t, glow, 0.)
        un.draw_sky(ctx, u, P, t)
        if under: under(ctx, t, D)
        un.draw_far(ctx, u, P, G, t)
        for grp in (tw.BACK, None, tw.FRONT):
            if grp is None: square_ground(ctx); continue
            for nm, fn in grp: fn(ctx, 1, 1, t)
        un.draw_front(ctx, u, P, G, t)
        stone(ctx, 960, 745, 1, engraved="FOUNDATION · EP 1")
        if over: over(ctx, t, D)
    f.bg = 'land'
    return f

def HOOK(ep, name):
    return town2(ep, build=(1.0, 5.0, 0., .5), over=title_over(name, f"EPISODE {ep}", y=230))
def END(ep, **kw):
    return town2(ep, build=(.8, 4.0, .5, 1.), glow=(1.0, 4.0), **kw)

# ---------------- layers ----------------
def head(s, at=0, y=150, size=64, col=None):
    def f(ctx, t, D):
        text(ctx, s, W/2, y, size, col or C['navy'], ease(seg(t, T(at), T(at)+.8)), bold=True)
    return f

def title_over(s, sub, y=250, col=None):
    """series title card text fading in/out over a TOWN opening"""
    def f(ctx, t, D):
        a = ease(seg(t, .5, 1.5))*(1-ease(seg(t, 5, 6)))
        text(ctx, SERIES_TITLE+"  ·  "+sub, W/2, y-70, 24, col or C['pinel'], a, bold=True)
        text(ctx, s, W/2, y+20, 78, col or C['navy'], a, bold=True)
    return f

def TL(items, y=240, x0=240, x1=1680, t0=.7, gap=1.0):
    """items: (year, sub, cue) – markers light in turn; line fills between them"""
    def f(ctx, t, D):
        n = len(items)
        xs = [x0 + (x1-x0)*(i/(n-1) if n > 1 else .5) for i in range(n)]
        ts = [T(it[2]) if len(it) > 2 and it[2] is not None else t0+i*gap for i, it in enumerate(items)]
        rgba(ctx, C['fog'], 1); rrect(ctx, x0-50, y-3, x1-x0+100, 6, 3); ctx.fill()
        for i in range(1, n):
            q = ease(seg(t, ts[i]-.5, ts[i]))
            if q > 0: rgba(ctx, C['pine'], 1); ctx.rectangle(xs[i-1], y-3, (xs[i]-xs[i-1])*q, 6); ctx.fill()
        for i, it in enumerate(items):
            lit = ease(seg(t, ts[i], ts[i]+.5))
            latest = lit > 0 and (i == n-1 or t < ts[i+1])
            r = 15 + 8*math.sin(lit*math.pi)
            paper(ctx, lambda: ctx.arc(xs[i], y, r+ (4 if latest else 0), 0, 2*math.pi), lerpc(C['fogd'], C['berry'] if latest else C['pine'], lit), 1, sh=3)
            text(ctx, str(it[0]), xs[i], y-38, 46, lerpc(C['fogd'], C['navy'], lit), .45+.55*lit, bold=True)
            if len(it) > 1 and it[1]: text(ctx, it[1], xs[i], y+58, 26, C['ink'], lit)
    return f

def stamp_fit(ctx, cx, cy, top, mid, bot, col, p, rot, scale=1.):
    if p <= 0: return
    s = lerp(1.5, 1, eoc(p))*scale; a = ease(p*1.6)
    def wid(txt, size, bold=False): font(ctx, size, bold); return ctx.text_extents(txt).x_advance
    sz, ts, bs = 70, 34, 30
    while wid(mid, sz, True) > 1100 and sz > 40: sz -= 4
    while wid(top, ts, True) > 1100 and ts > 22: ts -= 2
    while wid(bot, bs) > 1100 and bs > 18: bs -= 2
    w = min(1400, max(600, wid(mid, sz, True)+120, wid(top, ts, True)+100, wid(bot, bs)+100)); h = 300
    ctx.save(); ctx.translate(cx, cy); ctx.rotate(rot); ctx.scale(s, s)
    paper(ctx, lambda: rrect(ctx, -w/2, -h/2, w, h, 26), C['paper'], a, sh=10)
    rgba(ctx, col, a); ctx.set_line_width(6); rrect(ctx, -w/2+20, -h/2+20, w-40, h-40, 20); ctx.stroke()
    text(ctx, top, 0, -60, ts, col, a, bold=True); text(ctx, mid, 0, 30, sz, col, a, bold=True); text(ctx, bot, 0, 95, bs, C['ink'], a)
    ctx.restore()

def ST(top, mid, bot, col, cue=.5, x=960, y=600, rot=-.04, dur=.6, scale=1.):
    def f(ctx, t, D): stamp_fit(ctx, x, y, top, mid, bot, col, seg(t, T(cue), T(cue)+dur), rot, scale)
    return f

def BD(title, pills, y=330, w=1200, x=960, at=.3, cues=None, gapt=.8, size=34, cols=None):
    """paper board with a title and label pills that appear one by one"""
    def f(ctx, t, D):
        font(ctx, size)
        ws = [ctx.text_extents(p)[4]+60 for p in pills]
        rows, cur, cw = [], [], 0
        for i, wd in enumerate(ws):
            if cur and cw+wd+16 > w-80: rows.append(cur); cur, cw = [], 0
            cur.append(i); cw += wd+16
        rows.append(cur)
        rh = size*1.7+22; th = 80 if title else 30
        h = th + rh*len(rows) + 40
        a = ease(seg(t, T(at), T(at)+.6))
        if a <= 0: return
        paper(ctx, lambda: rrect(ctx, x-w/2, y, w, h, 24), C['paper'], a, sh=10, sha=.18)
        if title: text(ctx, title, x, y+58, 44, C['navy'], a, bold=True)
        for ri, row in enumerate(rows):
            tot = sum(ws[i]+16 for i in row)-16; cx = x - tot/2
            for i in row:
                ct = T(cues[i]) if cues else T(at)+.7+i*gapt
                pp = eob(seg(t, ct, ct+.5))
                col = (cols[i] if cols else ACC[i % len(ACC)])
                pop(ctx, cx+ws[i]/2, y+th+ri*rh+rh/2, pp, lambda: label(ctx, pills[i], cx+ws[i]/2, y+th+ri*rh+rh/2, size, 1, fg=C['paper'], bg=col))
                cx += ws[i]+16
    return f

def CD(cards, area=(120, 215, 1800, 990), cols=None, at=.4, cues=None, gapt=.45, gap=28, maxh=360):
    """cards: (title, [lines], optional colour). Grid fills the area; each card pops in turn."""
    def f(ctx, t, D):
        n = len(cards)
        c = cols or (n if n <= 3 else 2 if n == 4 else 3 if n <= 6 else 4)
        r = -(-n//c); ax0, ay0, ax1, ay1 = area
        cw = (ax1-ax0-gap*(c-1))/c; ch = min((ay1-ay0-gap*(r-1))/r, maxh)
        gh = r*ch+(r-1)*gap; oy = ay0 + (ay1-ay0-gh)/2 - 10
        ts_ = 54 if cw > 560 else 48 if cw > 380 else 38
        for i, cd in enumerate(cards):
            ct = T(cues[i]) if cues else T(at)+i*gapt
            pp = eob(seg(t, ct, ct+.5))
            if pp <= 0: continue
            col = cd[2] if len(cd) > 2 else ACC[i % len(ACC)]
            x, y = ax0+(i % c)*(cw+gap), oy+(i//c)*(ch+gap)
            def draw():
                paper(ctx, lambda: rrect(ctx, x, y, cw, ch, 20), C['paper'], 1, sh=9, sha=.18)
                rgba(ctx, col, 1); rrect(ctx, x+16, y+14, cw-32, 10, 5); ctx.fill()
                tt = ts_; 
                while tt > 22:
                    tl_ = wrap(ctx, cd[0], tt, cw-40, True)
                    ls = tt*0.7; lines = []
                    for ln in cd[1]: lines += wrap(ctx, ln, ls, cw-44)
                    need = 44+len(tl_)*tt*1.2+len(lines)*ls*1.35+16
                    if need <= ch or ls <= 20: break
                    tt -= 2; ts_2 = tt
                    ls = tt*0.7
                tl_ = wrap(ctx, cd[0], tt, cw-40, True); ls = tt*0.7
                lines = []
                for ln in cd[1]: lines += wrap(ctx, ln, ls, cw-44)
                yy = y+34+tt
                for s_ in tl_: text(ctx, s_, x+cw/2, yy, tt, C['navy'], 1, bold=True); yy += tt*1.2
                yy += ls*0.35
                for s_ in lines: text(ctx, s_, x+cw/2, yy+ls*0.6, ls, C['ink'], 1); yy += ls*1.35
            pop(ctx, x+cw/2, y+ch/2, pp, draw)
    return f

def AU(rows, head_=None, foot=None, t0=2.4, gapt=1.0, ys=None):
    """memory-tip scene. rows: list of rows of (big, small, cue)."""
    def f(ctx, t, D):
        bg_night(ctx, t); aurora(ctx, t, ease(seg(t, 0, 2.2)))
        if head_:
            text(ctx, head_, W/2, 175, 50, (1, 1, 1), ease(seg(t, .8, 1.8)), bold=True, glow=C['aur'])
        yy = ys or ([620] if len(rows) == 1 else [440, 700] if len(rows) == 2 else [380, 560, 740])
        idx = 0
        for ri, row in enumerate(rows):
            n = len(row); cell = 1740/n
            sz = 92 if n <= 3 else 76 if n <= 4 else 64
            for i, it in enumerate(row):
                big, small = it[0], it[1] if len(it) > 1 else ''
                ct = T(it[2]) if len(it) > 2 and it[2] is not None else t0+idx*gapt; idx += 1
                a = ease(seg(t, ct, ct+.8)); x = W/2 + (i-(n-1)/2)*cell
                s2 = sz; font(ctx, s2, True)
                while ctx.text_extents(big).x_advance > cell*.92 and s2 > 30: s2 -= 4; font(ctx, s2, True)
                text(ctx, big, x, yy[ri], s2, (1, 1, 1), a, bold=True, glow=C['aur'] if i % 2 == 0 else C['vio'])
                if small: text(ctx, small, x, yy[ri]+56, 34, C['aur'] if i % 2 == 0 else C['vio'], a*.95, bold=True)
        if foot:
            ft, fc = foot[0], foot[1]
            text(ctx, ft, W/2, 850, 46, C['aur'], ease(seg(t, T(fc), T(fc)+.8)), bold=True)
    f.bg = 'night'
    return f

def FIG(x, y, name, role, cue, col=None, s=2.0, w=250):
    """generic paper figure with a nameplate above it (never a likeness)"""
    def f(ctx, t, D):
        p = eob(seg(t, T(cue), T(cue)+.6))
        if p <= 0: return
        person(ctx, x, y, s*p, col or C['navyl'], 1)
        pw = max(w, 15.5*len(name)+50)
        ctx.save(); ctx.translate(x, y-110*s*.5-60); ctx.scale(p, p)
        paper(ctx, lambda: rrect(ctx, -pw/2, -38, pw, 76, 12), C['paper'], 1, sh=5)
        text(ctx, name, 0, -4, 26, C['navy'], 1, bold=True); text(ctx, role, 0, 24, 21, C['ink'], 1)
        ctx.restore()
    return f

def PILL(s, x, y, cue, col=None, size=38):
    def f(ctx, t, D):
        p = eob(seg(t, T(cue), T(cue)+.6))
        pop(ctx, x, y, p, lambda: label(ctx, s, x, y, size, 1, fg=C['paper'], bg=col or C['berry'], pad=24))
    return f

def carve(ctx, s, x, y, size, p, align='l', col=None, bold=True, serif=False):
    """text carved into stone, revealed left-to-right by p"""
    if p <= 0: return
    font(ctx, size, bold, serif); w = ctx.text_extents(s).x_advance
    x0 = x if align == 'l' else x-w/2 if align == 'c' else x-w
    ctx.save(); ctx.rectangle(x0-10, y-size*1.1, (w+20)*p, size*1.5); ctx.clip()
    text(ctx, s, x+2, y+3, size, (1, 1, 1), .38, bold=bold, align=align, serif=serif)
    text(ctx, s, x, y, size, col or hx('4A5560'), .95, bold=bold, align=align, serif=serif)
    ctx.restore()

def WALL(items, box=(200, 190, 1720, 830), at=.2, glow=0.):
    """big stone wall; items: (text, x, y, size, cue, align, colour)"""
    def f(ctx, t, D):
        x0, y0, x1, y1 = box; a = ease(seg(t, T(at), T(at)+.7))
        if a <= 0: return
        paper(ctx, lambda: rrect(ctx, x0, y0, x1-x0, y1-y0, 16), hx('B4BABD'), a, sh=12, sha=.2)
        ctx.save(); rrect(ctx, x0, y0, x1-x0, y1-y0, 16); ctx.clip()
        rgba(ctx, (1, 1, 1), .22*a); ctx.set_line_width(3)
        for j in range(1, int((y1-y0)/90)+1):
            y = y0+j*90; ctx.move_to(x0, y); ctx.line_to(x1, y)
            for i in range(int((x1-x0)/220)+1): ctx.move_to(x0+i*220+(j % 2)*110, y-90); ctx.line_to(x0+i*220+(j % 2)*110, y)
        ctx.stroke(); ctx.restore()
        for (s, x, y, size, cue, align, col) in items:
            carve(ctx, s, x, y, size, ease(seg(t, T(cue), T(cue)+1.3)), align, col)
    return f

# ---------------- split building ----------------
def split_building(split_cue, left, right, ribbon=None, rcue=None, cols=None):
    def f(ctx, t, D):
        k = ease(seg(t, T(split_cue), T(split_cue)+1.1)) if split_cue is not None else 1.
        dx = 250*k
        for side, sx in ((0, -1), (1, 1)):
            ctx.save(); ctx.rectangle(0 if side == 0 else 960, 0, 960, H); ctx.clip()
            ctx.translate(sx*dx, 0); building(ctx, 960, 880, 560, 380, p=1, col=(cols[side] if cols else None))
            ctx.restore()
        sc = T(split_cue) if split_cue is not None else -5
        label(ctx, left, 960-dx-5, 925, 34, ease(seg(t, sc+.9, sc+1.7)), fg=C['paper'], bg=(cols[0] if cols else C['pine']))
        label(ctx, right, 960+dx+5, 925, 34, ease(seg(t, sc+1.2, sc+2.0)), fg=C['paper'], bg=(cols[1] if cols else C['navyl']))
        if ribbon: label(ctx, ribbon, 960, 380, 38, ease(seg(t, T(rcue), T(rcue)+.7)), fg=C['paper'], bg=C['berry'])
    return f


# ---------------- UPSC CARD ----------------
def PRELIMS(stmt=None, ans=True, ans_cue=.55, rows=None, chips=None, sub="Statement-based questions"):
    """stmt: statement with a True/False toggle. rows: [(question, answer, q_cue, a_cue)] matching grid."""
    def f(ctx, t, D):
        bg_desk(ctx); corner(ctx)
        dy = lerp(H+200, 0, eoc(seg(t, 0, .9)))
        if stmt:
            card(ctx, 360, 180+dy, 1200, 560)
            label(ctx, "PRELIMS", W/2, 250+dy, 30, 1, fg=C['paper'], bg=C['pine'])
            text(ctx, sub, W/2, 345+dy, 40, C['navy'], 1, bold=True)
            ls = wrap_s(ctx, "“"+stmt+"”", 38, 1040)
            for i, s_ in enumerate(ls): text(ctx, s_, W/2, 440+dy+i*52, 38, C['ink'], 1, serif=True)
            ta = T(ans_cue); k = eoc(seg(t, ta, ta+.6))
            on = lerp(.5, 1. if ans else 0., k)
            ty = 440+dy+len(ls)*52+30
            toggle(ctx, 960-70, ty, on)
            text(ctx, "False", 960-92, ty+44, 32, C['berry'] if (not ans and k > .5) else C['fogd'], 1, align='r', bold=(not ans and k > .5))
            text(ctx, "True", 960+92, ty+44, 32, C['pine'] if (ans and k > .5) else C['fogd'], 1, align='l', bold=(ans and k > .5))
        else:
            n = len(rows); ch = 150+n*150
            card(ctx, 260, 150+dy, 1400, ch)
            label(ctx, "PRELIMS", W/2, 215+dy, 30, 1, fg=C['paper'], bg=C['pine'])
            for i, (q, a_, qc, ac) in enumerate(rows):
                y = 290+dy+i*150; qa = ease(seg(t, T(qc), T(qc)+.5))
                ls = wrap_s(ctx, q, 38, 1000)
                for j, s_ in enumerate(ls): text(ctx, s_, 320, y+j*48+(14 if len(ls) == 1 else -8), 38, C['ink'], qa, serif=True, align='l')
                pp = eob(seg(t, T(ac), T(ac)+.5))
                pop(ctx, 1480, y+10, pp, lambda: label(ctx, a_, 1480, y+10, 36, 1, fg=C['paper'], bg=ACC[i % len(ACC)], pad=24))
                if i < n-1: rgba(ctx, C['fog'], .8); ctx.rectangle(320, y+80, 1260, 2); ctx.fill()
        for i, s_ in enumerate(chips or []):
            pp = eob(seg(t, D-6+i*.8, D-5.3+i*.8))
            pop(ctx, 660+i*300, 880, pp, lambda: label(ctx, s_, 660+i*300, 880, 48, 1, fg=C['paper'], bg=C['navyl'], pad=26))
    f.bg = 'desk'
    return f

def MAINS(q, hint=None, chips=None, cues=None, spacing=400):
    def f(ctx, t, D):
        bg_desk(ctx); corner(ctx)
        dy = lerp(H+200, 0, eoc(seg(t, 0, .9)))
        card(ctx, 360, 160+dy, 1200, 600)
        label(ctx, "MAINS", W/2, 230+dy, 30, 1, fg=C['paper'], bg=C['berry'])
        ls = wrap_s(ctx, q, 44, 1040, True); y = 330
        for s_ in ls: text(ctx, s_, W/2, y+dy, 44, C['navy'], 1, bold=True, serif=True); y += 56
        if hint:
            for s_ in wrap_s(ctx, hint, 34, 1040): text(ctx, s_, W/2, y+14+dy, 34, C['ink'], 1, serif=True); y += 44
        for i in range(max(2, int((730-y-20)//56))):
            rgba(ctx, C['fog'], 1); ctx.rectangle(460, y+50+i*56+dy, 1000, 3); ctx.fill()
        n = len(chips or [])
        for i, (w_, col) in enumerate(chips or []):
            ct = T(cues[i]) if cues else 4.5+i*.8
            pp = eob(seg(t, ct, ct+.6)); x = W/2 + (i-(n-1)/2)*spacing
            pop(ctx, x, 870, pp, lambda: label(ctx, w_, x, 870, 34, 1, fg=C['paper'], bg=col, pad=22))
    f.bg = 'desk'
    return f

# ---------------- quick builders (cues spread across the narration) ----------------
def LIST(title, pills, y=300, w=1500, size=34, cols=None):
    return scene('paper', BD(title, pills, y=y, w=w, cues=spread(len(pills)), size=size, cols=cols))

def GRID(title, cards, cols=None, maxh=360, area=None, cues=None):
    layers = ([head(title, 0, y=150, size=56)] if title else []) + [CD(cards, cols=cols, cues=cues or spread(len(cards)), maxh=maxh, area=area or (120, 215 if title else 170, 1800, 985))]
    return scene('paper', *layers)

def TIPS(rows, head_=None, foot=None, ys=None, a=.2, b=.92):
    """memory-tip scene: rows of (big, small); items appear in order across the narration"""
    n = sum(len(r) for r in rows); sp = spread(n, a, b); k = 0; out = []
    for r in rows:
        row = []
        for it in r: row.append((it[0], it[1] if len(it) > 1 else '', sp[k])); k += 1
        out.append(row)
    return AU(out, head_=head_, foot=foot, ys=ys)

def QA(rows):
    """Prelims matching rows [(question, answer)]"""
    sp = spread(2*len(rows), .15, .92)
    return PRELIMS(rows=[(q, a, sp[2*i], sp[2*i+1]) for i, (q, a) in enumerate(rows)])
