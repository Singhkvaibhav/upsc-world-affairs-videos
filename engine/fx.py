"""Premium finishing layer for World Affairs: ink-wipe transitions, keyword pop-ups, film grain, moving light."""
import math, random, cairo
import numpy as np
from engine import core
from engine.core import W, H, seg, ease, eoc, eob, lerp, T
from engine.riso import R, rgba, txt, tw, face, rrect

_grain = []
def _grains():
    if _grain: return _grain
    rng = np.random.default_rng(11)
    for k in range(6):
        n = (rng.normal(0, 1, (H//2, W//2))*28 + 128).clip(0, 255).astype(np.uint8)
        a = np.dstack([n, n, n, np.full_like(n, 255)])
        s = cairo.ImageSurface.create_for_data(bytearray(a.tobytes()), cairo.FORMAT_ARGB32, W//2, H//2, (W//2)*4)
        _grain.append(s)
    return _grain

INK = {'teal': R['teal'], 'coral': R['coral'], 'violet': R['violet'], 'char': R['char']}

def sticker(ctx, label, ink, t, t0, life=2.8):
    p_in = seg(t, t0, t0 + .45); p_out = seg(t, t0 + life, t0 + life + .3)
    if p_in <= 0 or p_out >= 1: return
    s = eob(p_in, 2.2) * (1 - eoc(p_out)); a = ease(p_in*2) * (1 - p_out)
    rot = -.05 + .025*math.sin((t - t0)*3.2)*(1 - p_in*.6)
    face(ctx, 46, 'black'); w = ctx.text_extents(label).x_advance + 56; h = 78
    x, y = W - 90 - w/2, 895
    ctx.save(); ctx.translate(x, y); ctx.rotate(rot); ctx.scale(max(s, .01), max(s, .01))
    # offset print shadow in the second ink, then the block
    ctx.set_operator(cairo.OPERATOR_MULTIPLY)
    rgba(ctx, R['coral'] if ink != R['coral'] else R['teal'], .55*a); rrect(ctx, -w/2 + 7, -h/2 + 7, w, h, 8); ctx.fill()
    rgba(ctx, ink, a); rrect(ctx, -w/2, -h/2, w, h, 8); ctx.fill()
    ctx.set_operator(cairo.OPERATOR_OVER)
    txt(ctx, label, 0, 16, 46, R['paper'], a, 'black', 'c')
    ctx.restore()

def wipe_out(ctx, p):
    """bands sweep in from the left and cover the frame (end of a segment)"""
    e = lerp(-500, W + 700, eoc(p)); _bands(ctx, cover_left_of=e)

def wipe_in(ctx, p):
    """bands sweep off to the right, revealing the new segment"""
    s = lerp(-700, W + 500, ease(p)); _bands(ctx, cover_right_of=s)

def _skew(y): return (y - H/2)*.32

def _bands(ctx, cover_left_of=None, cover_right_of=None):
    ctx.save()
    def poly(x0, x1):
        ctx.move_to(x0 + _skew(0), 0); ctx.line_to(x1 + _skew(0), 0); ctx.line_to(x1 + _skew(H), H); ctx.line_to(x0 + _skew(H), H); ctx.close_path()
    if cover_left_of is not None:
        e = cover_left_of
        poly(-2000, e - 150); rgba(ctx, R['teal']); ctx.fill()
        poly(e - 150, e); rgba(ctx, R['coral']); ctx.fill()
        poly(e - 170, e - 150); rgba(ctx, R['paper']); ctx.fill()
    else:
        s = cover_right_of
        poly(s + 150, W + 2000); rgba(ctx, R['teal']); ctx.fill()
        poly(s, s + 150); rgba(ctx, R['coral']); ctx.fill()
        poly(s + 150, s + 170); rgba(ctx, R['paper']); ctx.fill()
    ctx.restore()

def _hand(pts, seed, amp=4):
    r = random.Random(seed)
    return [(x + r.uniform(-amp, amp), y + r.uniform(-amp, amp)) for x, y in pts]

def marker(ctx, kind, x, y, w, h, p, a=1., seed=0):
    """explainer-style marker annotation drawn on live: circle, underline or arrow (coral marker)"""
    if p <= 0 or a <= 0: return
    if kind == 'circle':
        n = 60; pts = [(x + w/2*1.04*math.cos(-1.9 + 2*math.pi*1.08*i/n), y + h/2*math.sin(-1.9 + 2*math.pi*1.08*i/n)) for i in range(n+1)]
    elif kind == 'underline':
        pts = [(x + w*i/20, y + 3*math.sin(i*.9 + seed)) for i in range(21)]
    else:   # arrow from (x, y) to (x+w, y+h), slightly curved
        pts = [(x + w*s + 40*math.sin(math.pi*s)*(h/(abs(w)+abs(h)+1)), y + h*s - 40*math.sin(math.pi*s)*(w/(abs(w)+abs(h)+1))) for s in [i/24 for i in range(25)]]
    pts = _hand(pts, seed, 2.5)
    m = max(2, int(len(pts)*min(p, 1)))
    ctx.save(); ctx.set_operator(cairo.OPERATOR_MULTIPLY)
    ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.set_line_join(cairo.LINE_JOIN_ROUND)
    ctx.set_line_width(8); rgba(ctx, R['coral'], .9*a)
    ctx.move_to(*pts[0])
    for q in pts[1:m]: ctx.line_to(*q)
    ctx.stroke()
    if kind == 'arrow' and p >= 1:
        (x1, y1), (x0, y0) = pts[-1], pts[-4]
        ang = math.atan2(y1 - y0, x1 - x0)
        for d in (2.6, -2.6):
            ctx.move_to(x1, y1); ctx.line_to(x1 + 34*math.cos(ang + d), y1 + 34*math.sin(ang + d))
        ctx.stroke()
    ctx.restore()

def make_post(groups, keys, annots=None):
    annots = annots or {}
    def group(k): return groups.get(k, k)
    def post(ctx, b, t, tl):
        core.BEAT = b; D = b['D']; i = b['i']
        # marker annotations, drawn on as the narration reaches them
        for j, (phrase, kind, x, y, w, h) in enumerate(annots.get(b['k'], [])):
            t0 = T(phrase)
            marker(ctx, kind, x, y, w, h, seg(t, t0, t0 + .55), 1 - ease(seg(t, D - .5, D - .2)), seed=j + 7*i)
        # keyword pop-ups
        for phrase, label, ink in keys.get(b['k'], []):
            sticker(ctx, label, INK[ink], t, T(phrase) - .05)
        # moving light + vignette
        lx = W*(.3 + .4*math.sin((b['start'] + t)*.05)); ly = H*.25
        g = cairo.RadialGradient(lx, ly, 50, lx, ly, 1100)
        g.add_color_stop_rgba(0, 1, .97, .9, .10); g.add_color_stop_rgba(1, 1, 1, 1, 0)
        ctx.save(); ctx.set_operator(cairo.OPERATOR_SCREEN); ctx.set_source(g); ctx.paint(); ctx.restore()
        v = cairo.RadialGradient(W/2, H/2, 500, W/2, H/2, 1250)
        v.add_color_stop_rgba(0, 0, 0, 0, 0); v.add_color_stop_rgba(1, .12, .1, .08, .22)
        ctx.save(); ctx.set_source(v); ctx.paint(); ctx.restore()
        # film grain (changes every frame)
        gs = _grains()[int((b['start'] + t)*30) % 6]
        ctx.save(); ctx.scale(2, 2); ctx.set_operator(cairo.OPERATOR_OVERLAY)
        ctx.set_source_surface(gs, 0, 0); ctx.paint_with_alpha(.10); ctx.restore()
        # ink-wipe transitions between segments
        TD = .34
        if i + 1 < len(tl) and group(tl[i+1]['k']) != group(b['k']) and t > D - TD:
            wipe_out(ctx, seg(t, D - TD, D))
        if i > 0 and group(tl[i-1]['k']) != group(b['k']) and t < TD:
            wipe_in(ctx, seg(t, 0, TD))
    return post
