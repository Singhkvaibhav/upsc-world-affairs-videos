"""Risograph briefing style: two inks overprinted on off-white paper, halftone dots, misregistration.
Shared drawing helpers for India and the World, Simply Briefed."""
import cairo, math, random
import numpy as np
from engine import core
from engine.core import W, H, cl, seg, ease, eoc, eob, lerp, hx

R = {k: hx(v) for k, v in dict(
    paper='F3EFE6', teal='1F6F78', coral='E2603F', over='6B4A4F', char='26282B', mist='D7DCDA',
    river='4E8FB0', violet='5B4B9A', tealpale='BFD8D6', coralpale='F4C9B8', grey='8A8F91').items()}

FONT_HEAD = 'Inter Display'          # with weight black via face name below
_cache = {}

# ---------- paper ----------
def _grain():
    if 'grain' in _cache: return _cache['grain']
    rng = np.random.default_rng(5)
    n = rng.normal(0, 1, (H, W)).astype(np.float32)
    # soft fibres
    k = np.ones(5, np.float32)/5
    n = np.apply_along_axis(lambda r: np.convolve(r, k, 'same'), 1, n)*0.6 + rng.normal(0, 1, (H, W))*0.4
    a = np.clip(n*10+0, -40, 40)
    base = np.array([int(c*255) for c in R['paper']], np.float32)
    img = np.clip(base[None, None, :] + a[..., None]*np.array([.30, .28, .25]), 0, 255).astype(np.uint8)
    # vignette
    yy, xx = np.mgrid[0:H, 0:W]
    v = ((xx-W/2)/(W*.75))**2 + ((yy-H/2)/(H*.75))**2
    img = (img*(1-np.clip(v, 0, 1)[..., None]*0.10)).astype(np.uint8)
    bgra = np.zeros((H, W, 4), np.uint8)
    bgra[..., 0], bgra[..., 1], bgra[..., 2], bgra[..., 3] = img[..., 2], img[..., 1], img[..., 0], 255
    surf = cairo.ImageSurface.create_for_data(bytearray(bgra.tobytes()), cairo.FORMAT_ARGB32, W, H, W*4)
    _cache['grain'] = surf
    return surf

def bg_sheet(ctx):
    ctx.set_source_surface(_grain(), 0, 0); ctx.paint()

def bg_board(ctx):
    ctx.set_source_surface(_grain(), 0, 0); ctx.paint()
    rgba(ctx, R['mist'], .45); ctx.paint()
    rgba(ctx, R['grey'], .25)
    for x in range(40, W, 60):
        for y in range(40, H, 60):
            ctx.arc(x, y, 1.6, 0, 2*math.pi); ctx.fill()

# ---------- colour + ink ----------
def rgba(ctx, c, a=1.): ctx.set_source_rgba(c[0], c[1], c[2], a)

def mis(seed, settle=1.):
    """misregistration offset for a shape: random 1-2 px, multiplied by (1-settle) extra on entrance"""
    r = random.Random(seed)
    base = (r.uniform(-2, 2), r.uniform(-1.5, 1.5))
    k = 1 + 10*(1-settle)
    return base[0]*k, base[1]*k

def riso(ctx, path, ink, a=1., seed=0, settle=1., second=None):
    """flat ink fill, multiplied onto the page; optional second ink offset slightly (overprint)."""
    if a <= 0: return
    ctx.save()
    # paper-coloured shapes sit on top (OVER); inks multiply like real overprinting
    if ink != R['paper']: ctx.set_operator(cairo.OPERATOR_MULTIPLY)
    ctx.new_path(); path(); rgba(ctx, ink, a); ctx.fill()
    if second is not None:
        dx, dy = mis(seed, settle)
        ctx.translate(dx, dy); ctx.new_path(); path(); rgba(ctx, second, a*.9); ctx.fill()
    ctx.restore()

def halftone(ctx, path, ink, a=1., step=11, r=2.6, angle=.4):
    """dot pattern clipped to path"""
    if a <= 0: return
    key = ('ht', step, round(r, 1), round(angle, 2))
    if key not in _cache:
        s = cairo.ImageSurface(cairo.FORMAT_ARGB32, W+200, H+200); c = cairo.Context(s)
        c.translate((W+200)/2, (H+200)/2); c.rotate(angle); c.set_source_rgba(0, 0, 0, 1)
        for x in range(-1300, 1300, step):
            for y in range(-1300, 1300, step):
                c.arc(x, y, r, 0, 2*math.pi); c.fill()
        _cache[key] = s
    ctx.save(); ctx.new_path(); path(); ctx.clip()
    ctx.set_operator(cairo.OPERATOR_MULTIPLY); rgba(ctx, ink, a)
    ctx.mask_surface(_cache[key], -100, -100); ctx.restore()

def rrect(ctx, x, y, w, h, r):
    core.rrect(ctx, x, y, w, h, r)

# ---------- type ----------
def face(ctx, size, weight='reg', mono=False, italic=False):
    if mono:
        ctx.select_font_face('DejaVu Sans Mono', cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD if weight != 'reg' else cairo.FONT_WEIGHT_NORMAL)
    elif weight == 'black':
        ctx.select_font_face('Inter Display Black', cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    else:
        ctx.select_font_face('Inter', cairo.FONT_SLANT_ITALIC if italic else cairo.FONT_SLANT_NORMAL,
                             cairo.FONT_WEIGHT_BOLD if weight == 'bold' else cairo.FONT_WEIGHT_NORMAL)
    ctx.set_font_size(size)

def tw(ctx, s, size, weight='reg', mono=False):
    face(ctx, size, weight, mono); return ctx.text_extents(s).x_advance

def txt(ctx, s, x, y, size, col, a=1., weight='reg', align='l', mono=False, multiply=False):
    if a <= 0 or not s: return 0
    face(ctx, size, weight, mono)
    e = ctx.text_extents(s)
    xx = x - (e.x_advance/2 if align == 'c' else e.x_advance if align == 'r' else 0)
    ctx.save()
    if multiply: ctx.set_operator(cairo.OPERATOR_MULTIPLY)
    ctx.move_to(xx, y); rgba(ctx, col, a); ctx.show_text(s); ctx.restore()
    return e.x_advance

def inktext(ctx, s, x, y, size, ink, a=1., settle=1., seed=0, weight='black', align='l', second=None):
    """big headline type in ink with overprint ghost that settles into register"""
    if a <= 0: return
    face(ctx, size, weight)
    e = ctx.text_extents(s)
    xx = x - (e.x_advance/2 if align == 'c' else e.x_advance if align == 'r' else 0)
    ctx.save()
    if ink != R['paper']: ctx.set_operator(cairo.OPERATOR_MULTIPLY)
    if second is not None:
        dx, dy = mis(seed, settle)
        ctx.move_to(xx+dx+3, y+dy+2); ctx.text_path(s); rgba(ctx, second, .35*a); ctx.fill()
    ctx.move_to(xx, y); ctx.text_path(s); rgba(ctx, ink, a); ctx.fill()
    ctx.restore()
    return e.x_advance

def wrap(ctx, s, size, maxw, weight='reg', mono=False):
    face(ctx, size, weight, mono)
    words, lines, cur = s.split(), [], ''
    for w_ in words:
        t = (cur+' '+w_).strip()
        if ctx.text_extents(t).x_advance > maxw and cur: lines.append(cur); cur = w_
        else: cur = t
    if cur: lines.append(cur)
    return lines

def para(ctx, s, x, y, size, col, maxw, a=1., lh=1.32, weight='reg', align='l', mono=False):
    for i, l in enumerate(wrap(ctx, s, size, maxw, weight, mono)):
        txt(ctx, l, x, y+i*size*lh, size, col, a, weight, align, mono)
    return len(wrap(ctx, s, size, maxw, weight, mono))

def typed(s, p):
    """typewriter reveal: portion of string shown at progress p"""
    n = int(round(len(s)*cl(p)))
    return s[:n]

# ---------- motion ----------
def spring(x, k=1.7):
    return eob(x, k)

def camera(ctx, t, D, zoom=(1.0, 1.035), pan=(0, 0), cx=W/2, cy=H/2, depth=1.0):
    """slow push-in/pan over the beat; depth <1 for background layers (parallax)"""
    p = ease(t/max(D, .01)) if D else 0
    z = 1 + (lerp(zoom[0], zoom[1], p)-1)*depth
    ctx.translate(cx + pan[0]*p*depth, cy + pan[1]*p*depth)
    ctx.scale(z, z); ctx.translate(-cx, -cy)

def pop(t, t0, dur=.55):
    """spring entrance progress (can exceed 1 slightly)"""
    return spring(seg(t, t0, t0+dur))

def fadein(t, t0, dur=.4): return ease(seg(t, t0, t0+dur))

# ---------- cable bar (top) ----------
def cable(ctx, t, line, a=1., ep=1):
    if a <= 0: return
    rgba(ctx, R['char'], .85*a); ctx.rectangle(70, 104, W-140, 2.5); ctx.fill()
    s = typed(line, seg(t, .1, 1.3))
    txt(ctx, s, 70, 86, 22, R['char'], .85*a, 'bold', mono=True)
    tag = f'WORLD AFFAIRS · EP {ep}'
    txt(ctx, tag, W-70, 86, 22, R['teal'], .9*a, 'bold', align='r', mono=True)

def credit(ctx, s, a=1.):
    txt(ctx, s, W-70, H-150, 18, R['grey'], a, mono=True, align='r')
