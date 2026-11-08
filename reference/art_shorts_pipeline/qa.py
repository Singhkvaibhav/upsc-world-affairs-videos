#!/usr/bin/env python3
"""QA over output/: for each episode (default: every episode marked done in scripts/episode_plan.md, or the numbers given)
check the long video (1920x1080, 30 fps, H.264 + AAC, 300 s), the Short (1080x1920, 30 fps, 40-58 s), the SRT, the YouTube text and
thumbnail, and flag long black/frozen/silent stretches and bad filenames."""
import glob, json, os, re, subprocess, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); OUT = os.path.join(ROOT, 'output')
probs = []
def sh(*a): return subprocess.run(a, capture_output=True, text=True)
def probe(v):
    j = json.loads(sh('ffprobe', '-v', 'error', '-show_streams', '-show_format', '-of', 'json', v).stdout or '{}')
    st = {s['codec_type']: s for s in j.get('streams', [])}; return st.get('video'), st.get('audio'), float(j.get('format', {}).get('duration', 0))
def chk(n, v, size, lo, hi, what):
    vs, au, d = probe(v)
    if not vs or not au: probs.append((n, f'{what}: missing video or audio stream')); return
    if (vs['width'], vs['height']) != size or vs['codec_name'] != 'h264' or vs.get('pix_fmt') != 'yuv420p': probs.append((n, f"{what}: {vs['codec_name']} {vs['width']}x{vs['height']} {vs.get('pix_fmt')}"))
    if eval(vs['r_frame_rate']) != 30: probs.append((n, f"{what}: fps {vs['r_frame_rate']}"))
    if au['codec_name'] != 'aac': probs.append((n, f'{what}: audio not aac'))
    if not (lo <= d <= hi): probs.append((n, f'{what}: duration {d:.2f}s'))
    if os.path.getsize(v) > 90e6: probs.append((n, f'{what}: size {os.path.getsize(v)/1e6:.0f} MB'))
    r = sh('ffmpeg', '-v', 'info', '-i', v, '-vf', 'scale=240:-2,blackdetect=d=4:pix_th=0.03,freezedetect=n=-50dB:d=40', '-af', 'silencedetect=n=-45dB:d=12', '-f', 'null', '-')
    for line in r.stderr.splitlines():
        if 'black_start' in line or 'freeze_start' in line or 'silence_start' in line: probs.append((n, f'{what}: ' + line.split(']')[-1].strip()[:70]))
if len(sys.argv) > 1: eps = [int(a) for a in sys.argv[1:]]
else: eps = [int(m.group(1)) for m in re.finditer(r'^\| (\d+) \|.*\| done \|$', open(os.path.join(ROOT, 'scripts', 'episode_plan.md')).read(), re.M)]
for n in eps:
    nn = f'{n:02d}'; vids = glob.glob(f'{OUT}/Art{nn}_*.mp4')
    if len(vids) != 1: probs.append((n, f'expected 1 video, found {len(vids)}')); continue
    if re.search(r'Art\d+_\.mp4$', vids[0]): probs.append((n, 'empty title in filename'))
    chk(n, vids[0], (1920, 1080), 299, 301, 'long')
    sv = f'{OUT}/shorts/Art{nn}_short.mp4'
    if not os.path.exists(sv): probs.append((n, 'missing Short'))
    else: chk(n, sv, (1080, 1920), 40, 58, 'short')
    srt = f'{OUT}/Art{nn}.srt'
    if not os.path.exists(srt) or os.path.getsize(srt) < 500: probs.append((n, 'srt missing/short'))
    for f in (f'{OUT}/youtube/Art{nn}.txt', f'{OUT}/youtube/Art{nn}_thumb.png'):
        if not os.path.exists(f): probs.append((n, f'missing {os.path.basename(f)}'))
for n, p in probs: print(f'Art{n:02d}: {p}')
print('QA problems:', len(probs), 'in', len(eps), 'episodes')
