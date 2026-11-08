"""Timeline, frame composition and render loop shared by all episodes."""
import json, os, sys, subprocess
import cairo
from engine import core
import re
from engine.core import W, H, FPS, TOTAL, LEAD, C, ease, seg, rgba, caption

def split_caption(text, maxc=130):
    sents = re.split(r'(?<=[.?!])\s+', text.strip())
    out = []
    for s in sents:
        while len(s) > 190:
            m = len(s) // 2
            cands = [x.end() for x in re.finditer(r', | and | but ', s)]
            cut = min(cands, key=lambda c: abs(c - m)) if cands else m
            out.append(s[:cut].strip()); s = s[cut:].strip()
        out.append(s)
    merged = []
    for s in out:
        if merged and len(merged[-1]) + 1 + len(s) <= maxc: merged[-1] += ' ' + s
        else: merged.append(s)
    return merged

def chunk_times(text, b):
    parts = split_caption(text); n = len(text); pos = 0; res = []
    for p in parts:
        s0 = LEAD + b['vo'] * pos / n - 0.05
        pos += len(p) + 1
        res.append([max(s0, .15), None, p])
    for j, c in enumerate(res):
        c[1] = res[j + 1][0] if j + 1 < len(res) else b['D'] - .05
    return [tuple(c) for c in res]

class Episode:
    def __init__(self, num, here, beats, captions, scenes, bg, extra, nocap=('end',), chunk_caps=False):
        self.num, self.here, self.beats, self.captions = num, here, beats, captions
        self.scenes, self.bg, self.extra, self.nocap = scenes, bg, extra, set(nocap)
        self.chunk_caps = chunk_caps
        core.EP = num

    def timeline(self):
        d = json.load(open(os.path.join(self.here, 'vo/durs.json')))
        base = {k: LEAD + d[k] + self.extra.get(k, 0) for k, _ in self.beats}
        tail = (TOTAL - sum(base.values())) / len(self.beats)
        tl, t0 = [], 0.
        for i, (k, txt) in enumerate(self.beats):
            D = round((base[k] + tail) * FPS) / FPS
            text = self.captions.get(k, txt)
            b = dict(i=i, k=k, start=t0, D=D, vo=d[k], text=text, narr=txt)
            b['chunks'] = chunk_times(text, b) if self.chunk_caps else None
            tl.append(b)
            t0 += D
        return tl

    def frame(self, ctx, b, t, prev_bg, next_bg):
        k, D = b['k'], b['D']
        core.BEAT = b
        ctx.save(); self.scenes[k](ctx, t, D); ctx.restore()
        core.BEAT = b
        if k not in self.nocap:
            if b['chunks']:
                for j, (s0, e0, txt) in enumerate(b['chunks']):
                    last = j == len(b['chunks']) - 1
                    a = ease(seg(t, s0, s0 + .25)) * (1 - ease(seg(t, (D - .45) if last else (e0 - .2), (D - .05) if last else e0)))
                    caption(ctx, txt, a)
            else:
                caption(ctx, b['text'], ease(seg(t, .15, .6)) * (1 - ease(seg(t, D - .45, D - .05))))
        FD = .45
        if prev_bg != self.bg[k] and t < FD:
            rgba(ctx, C['birch'], 1 - ease(t / FD)); ctx.paint()
        if next_bg is not None and next_bg != self.bg[k] and t > D - FD:
            rgba(ctx, C['birch'], ease((t - (D - FD)) / FD)); ctx.paint()

    def render_beat(self, b, prev_bg, next_bg, out):
        surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
        ctx = cairo.Context(surf)
        n = int(round(b['D'] * FPS))
        tmp = out.replace('.mp4', '.part.mp4')
        p = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'bgra', '-s', f'{W}x{H}',
                              '-r', str(FPS), '-i', '-', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '20',
                              '-pix_fmt', 'yuv420p', '-r', str(FPS), tmp], stdin=subprocess.PIPE)
        for f in range(n):
            ctx.save(); self.frame(ctx, b, f / FPS, prev_bg, next_bg); ctx.restore()
            surf.flush(); p.stdin.write(bytes(surf.get_data()))
        p.stdin.close()
        if p.wait() == 0: os.replace(tmp, out)
        else: raise SystemExit('ffmpeg failed ' + out)

    def main(self, argv):
        tl = self.timeline(); mode = argv[1]
        if mode == 'still':
            k, tt = argv[2], float(argv[3])
            b = next(x for x in tl if x['k'] == k)
            surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); ctx = cairo.Context(surf)
            self.frame(ctx, b, tt if tt >= 0 else b['D'] + tt, self.bg[k], self.bg[k]); surf.write_to_png(argv[4])
        elif mode == 'tl':
            for b in tl: print(b['i'], b['k'], round(b['start'], 2), round(b['D'], 2))
            print('total', round(sum(b['D'] for b in tl), 2))
        elif mode == 'render':
            idxs = [int(x) for x in argv[2].split(',')]
            os.makedirs('parts', exist_ok=True)
            for i in idxs:
                prev_bg = self.bg[tl[i - 1]['k']] if i > 0 else None
                next_bg = self.bg[tl[i + 1]['k']] if i < len(tl) - 1 else None
                self.render_beat(tl[i], prev_bg, next_bg, f'parts/{i:02d}.mp4')
                print('done', i, flush=True)
