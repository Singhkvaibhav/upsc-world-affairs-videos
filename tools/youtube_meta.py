#!/usr/bin/env python3
"""Build YouTube upload metadata for finished episodes: output/youtube/EpNN.txt (title, description with chapters, tags) and EpNN_thumb.png (1280x720).
usage: python3 tools/youtube_meta.py [NN ...]   (default: every episode that has a video in output/)"""
import glob, os, re, subprocess, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'output'); YT = os.path.join(OUT, 'youtube'); os.makedirs(YT, exist_ok=True)
LABEL = dict(hook='Intro', tip='Memory tip', prelims='How UPSC asks it: Prelims', mains='How UPSC asks it: Mains', end='Recap and next episode', title='Intro', book='What a constitution is',
             upsc='How UPSC asks it', framework='The framework', stone='Recap', next='Next time')

def run(ep_dir, args):
    if os.path.exists(os.path.join(ep_dir, 'ep.py')):
        cmd = ['python3', '../../engine/cli.py'] + args
    else:
        cmd = ['python3', 'render.py'] + args
    return subprocess.run(cmd, cwd=ep_dir, capture_output=True, text=True).stdout

def stamp(s): return f"{int(s//60)}:{int(s%60):02d}"

def build(n):
    nn = f"{n:02d}"; ep_dir = os.path.join(ROOT, 'episodes', f'ep{nn}')
    vids = glob.glob(os.path.join(OUT, f'Ep{nn}_*.mp4'))
    if not vids or not os.path.exists(os.path.join(ep_dir, 'vo', 'durs.json')): return False
    name = os.path.basename(vids[0])[5:-4].replace('_', ' ')
    m = re.search(r'NAME\s*=\s*"([^"]+)"', open(os.path.join(ep_dir, 'ep.py')).read()) if os.path.exists(os.path.join(ep_dir, 'ep.py')) else None
    if m: name = m.group(1)
    rows = [l.split() for l in run(ep_dir, ['tl']).splitlines() if re.match(r'^\d+ ', l)]
    chapters, part = [], 0
    for i, r in enumerate(rows):
        k, start = r[1], float(r[2]) + (0 if i == 0 else 0.5)
        if k in LABEL: lab = LABEL[k]
        else: part += 1; lab = f'Part {part}'
        chapters.append((0 if i == 0 else start, lab))
    # YouTube needs each chapter >= 10 s: merge short ones into the previous
    keep = []
    for t, lab in chapters:
        if keep and t - keep[-1][0] < 10: continue
        keep.append((t, lab))
    title = f"Indian Polity, Simply Drawn · Episode {n}: {name}"
    desc = [f"Episode {n} of Indian Polity, Simply Drawn: a calm, five-minute animated explainer for UPSC aspirants.", f"Topic: {name}.", "",
            "Chapters:"] + [f"{stamp(t)} {lab}" for t, lab in keep] + ["",
            "Each episode ends with a memory tip and how UPSC asks the topic in Prelims and Mains.", "",
            "#UPSC #IndianPolity #CivilServices #Polity #Constitution #UPSCPrelims #UPSCMains"]
    tags = "UPSC, Indian Polity, Indian Constitution, UPSC Prelims, UPSC Mains, civil services, polity explained, " + name
    open(os.path.join(YT, f'Ep{nn}.txt'), 'w').write(f"TITLE: {title}\n\nDESCRIPTION:\n" + "\n".join(desc) + f"\n\nTAGS: {tags}\n\nCAPTIONS FILE: Ep{nn}.srt\nTHUMBNAIL: Ep{nn}_thumb.png\n")
    png = os.path.join(YT, f'Ep{nn}_full.png')
    first = rows[0][1] if rows else 'hook'
    scene = 'title' if n == 1 else first
    run(ep_dir, ['still', scene, '3.6' if n != 1 else '3', png])
    if os.path.exists(png):
        subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', png, '-vf', 'scale=1280:720', os.path.join(YT, f'Ep{nn}_thumb.png')])
        os.remove(png)
    return True

if __name__ == '__main__':
    eps = [int(a) for a in sys.argv[1:]] or sorted(int(re.match(r'Ep(\d+)_', os.path.basename(p)).group(1)) for p in glob.glob(os.path.join(OUT, 'Ep*_*.mp4')))
    for n in eps: print(n, 'ok' if build(n) else 'skipped')
