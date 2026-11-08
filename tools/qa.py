#!/usr/bin/env python3
"""QA over output/: every episode 2-88 must have video (1080p30 H.264 + AAC, ~300 s), SRT, YouTube metadata and thumbnail;
also flags long frozen/black stretches and silent stretches, empty captions and bad filenames."""
import glob, json, os, re, subprocess, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); OUT = os.path.join(ROOT, 'output')
probs = []
def sh(*a): return subprocess.run(a, capture_output=True, text=True)
for n in range(2, 89):
    nn = f'{n:02d}'; vids = glob.glob(f'{OUT}/Ep{nn}_*.mp4')
    if len(vids) != 1: probs.append((n, f'expected 1 video, found {len(vids)}')); continue
    v = vids[0]
    if re.search(r'Ep\d+_\.mp4$', v): probs.append((n, 'empty title in filename'))
    j = json.loads(sh('ffprobe', '-v', 'error', '-show_streams', '-show_format', '-of', 'json', v).stdout or '{}')
    st = {s['codec_type']: s for s in j.get('streams', [])}
    vs, au = st.get('video'), st.get('audio')
    if not vs or not au: probs.append((n, 'missing video or audio stream')); continue
    if (vs['width'], vs['height']) != (1920, 1080) or vs['codec_name'] != 'h264' or vs.get('pix_fmt') != 'yuv420p': probs.append((n, f"video {vs['codec_name']} {vs['width']}x{vs['height']} {vs.get('pix_fmt')}"))
    if eval(vs['r_frame_rate']) != 30: probs.append((n, f"fps {vs['r_frame_rate']}"))
    if au['codec_name'] != 'aac': probs.append((n, 'audio not aac'))
    d = float(j['format']['duration'])
    if abs(d - 300) > 1.0: probs.append((n, f'duration {d:.2f}s'))
    if os.path.getsize(v) > 90e6: probs.append((n, f'size {os.path.getsize(v)/1e6:.0f} MB'))
    srt = f'{OUT}/Ep{nn}.srt'
    if not os.path.exists(srt) or os.path.getsize(srt) < 500: probs.append((n, 'srt missing/short'))
    for f in (f'{OUT}/youtube/Ep{nn}.txt', f'{OUT}/youtube/Ep{nn}_thumb.png'):
        if not os.path.exists(f): probs.append((n, f'missing {os.path.basename(f)}'))
    r = sh('ffmpeg', '-v', 'info', '-i', v, '-vf', 'scale=320:180,blackdetect=d=6:pix_th=0.03,freezedetect=n=-50dB:d=40', '-af', 'silencedetect=n=-45dB:d=12', '-f', 'null', '-')
    for line in r.stderr.splitlines():
        if 'black_start' in line or 'freeze_start' in line or 'silence_start' in line:
            probs.append((n, line.split(']')[-1].strip()[:70]))
for n, p in probs: print(f'Ep{n:02d}: {p}')
print('QA problems:', len(probs))
