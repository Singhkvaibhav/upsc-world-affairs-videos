"""The two recurring worlds: the briefing passport (memory tips) and the relations web (threads).
Both are drawn from a state, so any episode shows them exactly as they stand at that point."""
import math, random, cairo
from engine import core
from engine.core import W, H, seg, ease, eoc, eob, lerp, T
from engine.riso import R, rgba, riso, halftone, rrect, txt, inktext, typed, camera, fadein, cable, bg_sheet, bg_board, tw
from engine.brief import _bg, outro, token, tag

# ---------- state ----------
# Every stamp and thread so far, by episode. Add one entry per episode as it is made.
STAMPS = {
    1: ['EAST  RBS → INDIA', 'WEST  IJC → PAKISTAN', '1960 · WORLD BANK'],
}
PARTNERS = {   # loose direction around India; no map shapes
    'Pakistan': (-430, -60), 'China': (60, -330), 'Bangladesh': (420, -40), 'Nepal': (-60, -250),
    'US': (-760, -260), 'EU': (-560, -340), 'Russia': (-260, -380), 'Gulf': (-620, 120),
    'Japan': (720, -230), 'ASEAN': (560, 220), 'Africa': (-380, 330), 'Sri Lanka': (120, 330),
}
THREADS = {   # episode -> (partner, label); specials use a half number so they sort between episodes
    1: ('Pakistan', 'Indus Waters · in abeyance'),
    1.5: ('US', 'AI chips · compute and controls'),
}

# ---------- passport ----------
def passport_stamp(lines, ep, slam_cue, line_cues, title='', label=None):
    def f(ctx, t, D):
        bg_sheet(ctx)
        a_out = outro(t, D)
        cable(ctx, t, 'PASSPORT STAMP · MEMORY TIP', a_out, core.EP)
        ctx.save(); camera(ctx, t, D, (1.0, 1.045), cy=560)
        # open passport
        x0, y0, pw, ph = 330, 190, 1260, 760
        riso(ctx, lambda: rrect(ctx, x0-24, y0-20, pw+48, ph+40, 26), R['teal'], a_out, second=R['coral'])
        for side in (0, 1):
            xx = x0 + side*pw/2
            riso(ctx, lambda: rrect(ctx, xx+6, y0, pw/2-12, ph, 10), R['paper'], a_out)
            halftone(ctx, lambda: rrect(ctx, xx+6, y0, pw/2-12, ph, 10), R['tealpale'], .35*a_out, step=14, r=1.6, angle=.8)
            txt(ctx, f'PAGE {int(ep*2-1+side):02d}', xx+40, y0+ph-34, 18, R['grey'], a_out, mono=True)
        rgba(ctx, R['char'], .3*a_out); ctx.rectangle(x0+pw/2-1, y0, 2, ph); ctx.fill()
        # earlier stamps (faded small) on left page
        for e, ls in STAMPS.items():
            if e >= ep: continue
            rr = random.Random(e)
            cx, cy = x0 + 140 + rr.uniform(0, 300), y0 + 150 + rr.uniform(0, 400)
            ctx.save(); ctx.translate(cx, cy); ctx.rotate(rr.uniform(-.3, .3))
            rgba(ctx, R['violet'], .35*a_out); ctx.set_line_width(4); ctx.arc(0, 0, 70, 0, 2*math.pi); ctx.stroke()
            txt(ctx, f'EP {e}', 0, 8, 22, R['violet'], .35*a_out, 'bold', 'c', mono=True); ctx.restore()
        txt(ctx, 'INDIA AND THE WORLD', x0+60, y0+80, 26, R['teal'], a_out, 'bold', mono=True)
        txt(ctx, 'BRIEFING PASSPORT', x0+60, y0+116, 22, R['grey'], a_out, mono=True)
        # the stamp slam
        ts = T(slam_cue) if isinstance(slam_cue, str) else slam_cue
        p = seg(t, ts, ts+.35)
        if p > 0:
            sc = lerp(1.9, 1, eoc(p)); a = ease(p*2)*a_out
            cx, cy = x0 + pw*.72, y0 + ph*.47
            # splash dots after impact
            if p >= 1:
                rr = random.Random(9)
                for k in range(26):
                    ang = rr.uniform(0, 2*math.pi); d = rr.uniform(330, 400)
                    rgba(ctx, R['violet'], .5*a*rr.uniform(.4, 1)); ctx.arc(cx+math.cos(ang)*d*.95, cy+math.sin(ang)*d*.5, rr.uniform(2, 6), 0, 2*math.pi); ctx.fill()
            ctx.save(); ctx.translate(cx, cy); ctx.rotate(-.06); ctx.scale(sc, sc)
            ctx.set_operator(cairo.OPERATOR_MULTIPLY)
            rgba(ctx, R['violet'], a); ctx.set_line_width(9); rrect(ctx, -330, -230, 660, 460, 30); ctx.stroke()
            ctx.set_line_width(3); rrect(ctx, -308, -208, 616, 416, 22); ctx.stroke()
            txt(ctx, (label or f'EPISODE {ep}') + f' · {title}', 0, -160, 24, R['violet'], a, 'bold', 'c', mono=True)
            for i, l in enumerate(lines):
                c0 = line_cues[i]; t0 = T(c0) if isinstance(c0, str) else c0
                la = ease(seg(t, t0, t0+.3))*a
                txt(ctx, l, 0, -60 + i*110, 50 if i < 2 else 44, R['violet'], la, 'black', 'c')
            ctx.restore()
        ctx.restore()
    return _bg(f, 'sheet')

# ---------- relations web ----------
def relations_web(ep, draw_cue, next_line, next_cue, sub_cue=None, label=None):
    def f(ctx, t, D):
        bg_board(ctx)
        a_out = outro(t, D, .6)
        cable(ctx, t, f'RELATIONS WEB · AFTER {label or "EPISODE " + str(ep)}', a_out, core.EP)
        cx, cy = W/2, 560
        ctx.save(); camera(ctx, t, D, (1.08, 1.0), cx=cx, cy=cy)
        partner, tlabel = THREADS[ep]
        # existing threads from earlier episodes
        for e, (pn, lab) in THREADS.items():
            if e >= ep: continue
            px, py = PARTNERS[pn]; _thread(ctx, cx, cy, cx+px, cy+py, 1, R['grey'], .6*a_out)
        # partner tokens (dim unless involved)
        involved = {pn for e, (pn, _) in THREADS.items() if e <= ep}
        for i, (pn, (px, py)) in enumerate(PARTNERS.items()):
            bob = 4*math.sin(t*.8 + i)
            on = pn in involved
            token(ctx, cx+px, cy+py+bob, pn, R['teal'], a_out*fadein(t, .1+i*.05), r=58 if on else 46, size=22 if on else 18, dim=not on)
        # new thread draws in
        td = T(draw_cue) if isinstance(draw_cue, str) else draw_cue
        q = eoc(seg(t, td, td+1.2))
        px, py = PARTNERS[partner]
        if q > 0:
            _thread(ctx, cx, cy, cx+px, cy+py, q, R['coral'], a_out, w=7)
            if q > .7:
                mx, my = cx + px*.5, cy + py*.5 - 70
                tag(ctx, mx, my, tlabel.upper(), R['coral'], ease(seg(t, td+.8, td+1.2))*a_out, 22, align='c')
        token(ctx, cx, cy, 'INDIA', R['teal'], a_out, r=86, size=32)
        ctx.restore()
        tn = T(next_cue) if isinstance(next_cue, str) else next_cue
        nq = seg(t, tn, tn+.6)
        if nq > 0:
            a = ease(nq)*a_out
            riso(ctx, lambda: rrect(ctx, 0, 870, W*eoc(nq), 90, 0), R['char'], a)
            txt(ctx, 'NEXT BRIEFING  ·  ' + next_line, 80, 928, 34, R['paper'], a, 'bold', mono=True)
        if sub_cue:
            subscribe_card(ctx, t, T(sub_cue) if isinstance(sub_cue, str) else sub_cue, a_out)
    return _bg(f, 'board')

def _thread(ctx, x0, y0, x1, y1, p, ink, a, w=4):
    if a <= 0 or p <= 0: return
    mx, my = (x0+x1)/2, (y0+y1)/2 - 90
    ctx.save(); ctx.set_operator(cairo.OPERATOR_MULTIPLY)
    ctx.set_line_width(w); ctx.set_line_cap(cairo.LINE_CAP_ROUND); rgba(ctx, ink, a)
    n = 40; ctx.move_to(x0, y0)
    for i in range(1, int(n*p)+1):
        s = i/n
        x = (1-s)**2*x0 + 2*(1-s)*s*mx + s*s*x1; y = (1-s)**2*y0 + 2*(1-s)*s*my + s*s*y1
        ctx.line_to(x, y)
    ctx.stroke(); ctx.restore()


def subscribe_card(ctx, t, t0, a_out=1., x=1530, y=760):
    """the channel's end card: a small ink card, no platform logos"""
    q = seg(t, t0, t0 + .5)
    if q <= 0: return
    s = eob(q, 1.8); a = ease(q*2)*a_out
    ctx.save(); ctx.translate(x, y); ctx.rotate(-.03); ctx.scale(s, s)
    riso(ctx, lambda: rrect(ctx, -230, -62, 460, 124, 14), R['paper'], a)   # opaque base so nothing shows through
    riso(ctx, lambda: rrect(ctx, -230, -62, 460, 124, 14), R['coral'], a)
    # simple bell
    ctx.save(); ctx.translate(-170, 0); ctx.rotate(.18*math.sin((t - t0)*9)*max(0, 1 - (t - t0)/1.5))
    riso(ctx, lambda: (ctx.move_to(-22, 18), ctx.curve_to(-22, -30, 22, -30, 22, 18), ctx.close_path()), R['paper'], a)
    riso(ctx, lambda: ctx.arc(0, 24, 6, 0, 2*math.pi), R['paper'], a)
    ctx.restore()
    txt(ctx, 'SUBSCRIBE', -120, -6, 42, R['paper'], a, 'black')
    txt(ctx, 'GyaanXstudios', -120, 36, 24, R['paper'], a, 'bold', mono=True)
    ctx.restore()
