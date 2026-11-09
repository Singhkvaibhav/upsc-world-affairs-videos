import os, sys, math, cairo
sys.path.insert(0, '../..'); sys.path.insert(0, '.')
from engine import core
core.TOTAL = 690.
from engine.riso import R, rgba, riso, halftone, rrect, txt, inktext, bg_sheet
from engine.chip import chip_pkg
from engine.brief import tag
W, H = 1920, 1080
s = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); ctx = cairo.Context(s)
bg_sheet(ctx)
def band():
    ctx.move_to(-100, 820)
    for x in range(-100, W+120, 40): ctx.line_to(x, 760 + 60*math.sin(x*.004))
    ctx.line_to(W+120, 1100); ctx.line_to(-100, 1100); ctx.close_path()
halftone(ctx, band, R['teal'], .6, step=13, r=3.4)
ctx.save(); ctx.translate(1440, 520); ctx.rotate(-.1); chip_pkg(ctx, 0, 0, 2.1, 1, 1.3, reveal=1); ctx.restore()
mx, my = 1350, 450
rgba(ctx, R['coral']); ctx.set_line_width(30); ctx.arc(mx, my, 210, 0, 2*math.pi); ctx.stroke()
ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.set_line_width(56); ctx.move_to(mx+150, my+150); ctx.line_to(mx+330, my+330); ctx.stroke()
halftone(ctx, lambda: ctx.arc(mx, my, 195, 0, 2*math.pi), R['coral'], .4, step=10, r=2.4)
txt(ctx, 'NVIDIA · JENSEN HUANG', 110, 200, 54, R['coral'], 1, 'bold', mono=True)
inktext(ctx, 'HONEY', 100, 430, 230, R['teal'], 1, second=R['coral'])
inktext(ctx, 'TRAP?', 100, 650, 230, R['coral'], 1, second=R['teal'])
for i, w_ in enumerate(['GPUs', 'HBM MEMORY', 'AI BUILDOUT', 'INDIA']):
    tag(ctx, 110 + [0, 200, 520, 870][i], 790, w_, R['char'], 1, 40)
txt(ctx, 'GyaanXstudios', W-80, H-60, 40, R['char'], 1, 'black', 'r')
s.write_to_png('WaSP01_thumb.png')
print('ok')
