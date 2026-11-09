"""Run one episode defined in ./ep.py (EP, TITLE, NAME, BEATS=[(id, narration, scene_fn)], CAPTIONS, EXTRA).
usage (inside episodes/epNN): python3 ../../engine/cli.py tts <voice.onnx> | tl | still <beat> <t> <out.png> | render <i,j,..> | audio | check"""
import importlib.util, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
HERE = os.getcwd()
spec = importlib.util.spec_from_file_location('ep', os.path.join(HERE, 'ep.py'))
ep = importlib.util.module_from_spec(spec); spec.loader.exec_module(ep)
from engine import core
if hasattr(ep, 'TOTAL'): core.TOTAL = float(ep.TOTAL)   # specials can run longer than 300 s
CODE = getattr(ep, 'CODE', None) or f'Wa{ep.EP:02d}'
from engine.runner import Episode
beats = [(k, n) for k, n, _ in ep.BEATS]
scenes = {k: f for k, _, f in ep.BEATS}
bg = {k: f.bg for k, _, f in ep.BEATS}
extra = dict(hook=1.5, tip=3.0, end=3.5); extra.update(getattr(ep, 'EXTRA', {}))
HI = getattr(ep, 'HI', None)   # bilingual episode: {beat: Hindi narration}; captions become subtitle files
post = None
if hasattr(ep, 'KEYS') or hasattr(ep, 'GROUPS'):
    from engine.fx import make_post
    post = make_post(getattr(ep, 'GROUPS', {}), getattr(ep, 'KEYS', {}), getattr(ep, 'ANNOT', {}))
E = Episode(ep.EP, HERE, beats, getattr(ep, 'CAPTIONS', {}), scenes, bg, extra,
            nocap=tuple(scenes) if HI else (), chunk_caps=True, post=post,
            crf=str(getattr(ep, 'CRF', 20)), preset=getattr(ep, 'PRESET', 'veryfast'))
cmd = sys.argv[1]
if cmd == 'tts':
    from engine import tts; os.makedirs('vo', exist_ok=True)
    V = getattr(ep, 'VOICE_EN', {})   # optional per-episode delivery: length, noise, gaps
    tts.run(beats, sys.argv[2], 'vo', V.get('length', 1.22), V.get('noise', (0.55, 0.7)), V.get('gaps', (0.55, 0.35)))
elif cmd == 'tts-hi':
    from engine import tts; os.makedirs('vo_hi', exist_ok=True)
    V = getattr(ep, 'VOICE_HI', {})
    tts.run([(k, HI[k]) for k, _ in beats], sys.argv[2], 'vo_hi', V.get('length', 1.0), V.get('noise', (0.55, 0.7)), V.get('gaps', (0.55, 0.35)))
elif cmd == 'audio' and HI:
    from engine.bimix import build2
    build2(E.timeline(), getattr(ep, 'FX', []), HI, CODE, getattr(ep, 'TENSION', None))
elif cmd == 'audio':
    from engine.audiomix import build
    fx = [('chime', 'tip', 0.4), ('click', 'end', 3.2)]
    build(E.timeline(), [f for f in fx if any(k == f[1] for k, _ in beats)], f'ep{ep.EP:02d}.srt')
elif cmd == 'check':
    import cairo
    from engine.core import W, H
    tl = E.timeline(); bad = 0
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); ctx = cairo.Context(surf)
    for i, b in enumerate(tl):
        for tt in (2.0, b['D']/2, b['D']-1):
            try:
                E.frame(ctx, b, tt, bg[b['k']], bg[b['k']])
            except Exception as e:
                bad += 1; print('FAIL', b['k'], round(tt, 1), repr(e)); break
    print('check', 'FAILED' if bad else 'ok', len(tl), 'beats'); sys.exit(1 if bad else 0)
else:
    E.main([sys.argv[0]] + sys.argv[1:])
