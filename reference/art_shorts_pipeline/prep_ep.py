#!/usr/bin/env python3
"""usage: python3 tools/prep_ep.py NN [NN ...]
Narration (tts) for the long video and the Short, scene check, then 4 long stills and 2 Short stills as one contact sheet:
episodes/epNN/stills/sheet.png. (Not a render of the video.)"""
import importlib.util, os, subprocess, sys
from PIL import Image
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, ROOT)
VOICE = os.path.join(ROOT, 'voice', 'en-us-lessac-medium.onnx')

def cli(d, args, vertical=False):
    env = dict(os.environ); env.pop('ART_VERTICAL', None)
    if vertical: env['ART_VERTICAL'] = '1'
    return subprocess.run(['python3', os.path.join(ROOT, 'engine', 'cli.py')] + args, cwd=d, env=env, capture_output=True, text=True)

def prep(n):
    nn = f'{n:02d}'; d = os.path.join(ROOT, 'episodes', f'ep{nn}'); os.makedirs(os.path.join(d, 'stills'), exist_ok=True)
    spec = importlib.util.spec_from_file_location('ep', os.path.join(d, 'ep.py')); ep = importlib.util.module_from_spec(spec); spec.loader.exec_module(ep)
    for v in (False, True):
        wd = os.path.join(d, 's') if v else d; os.makedirs(os.path.join(wd, 'vo'), exist_ok=True)
        r = cli(d, ['tts', VOICE], v)
        if r.returncode: print(nn, 'tts failed', r.stderr[-400:]); return False
        r = cli(d, ['check'], v)
        if r.returncode: print(nn, 'check failed', r.stdout[-600:]); return False
    tl = [l.split() for l in cli(d, ['tl']).stdout.splitlines() if l[:1].isdigit()]
    keys = [r[1] for r in tl]
    first_ana = next((f'look{i}' for i, sp in enumerate(ep.SPEC['look']) if sp['kind'] == 'anatomy'), 'look0')
    sel = [(first_ana, -3), ('compare', -3), ('where', -3), ('s1q', 3.5), ('patch', -2)]
    out = []
    for k, t in sel:
        p = os.path.join(d, 'stills', f'{k}.png'); r = cli(d, ['still', k, str(t), p])
        if r.returncode: print(nn, 'still failed', k, r.stderr[-300:]); return False
        out.append(p)
    shorts = []
    for k, t in (('tip_s', -1.5), ('sq', 3.5)):
        p = os.path.join(d, 'stills', f's_{k}.png'); r = cli(d, ['still', k, str(t), p], True)
        if r.returncode: print(nn, 'short still failed', k, r.stderr[-300:]); return False
        shorts.append(p)
    sheet = Image.new('RGB', (1920, 720), 'white')
    cells = [Image.open(p).convert('RGB').resize((640, 360)) for p in out]
    for i, c in enumerate(cells): sheet.paste(c, ((i % 3)*640, (i//3)*360))
    for j, p in enumerate(shorts):
        im = Image.open(p).convert('RGB'); w = int(im.width*360/im.height); sheet.paste(im.resize((w, 360)), (1280+j*(w+4), 360))
    sheet.save(os.path.join(d, 'stills', 'sheet.png'))
    open(os.path.join(d, 'vo', '.tts_ok'), 'w').write('ok')
    print(nn, 'prepped; narration', round(sum(float(r[3]) for r in tl), 0) if False else '')
    return True

if __name__ == '__main__':
    for a in sys.argv[1:]: prep(int(a))
