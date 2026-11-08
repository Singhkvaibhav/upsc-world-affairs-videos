#!/usr/bin/env python3
"""usage: python3 tools/deliver.py NN [NN ...]
Copies a rendered episode (episodes/epNN/final.mp4, s/final.mp4) into output/, writes the YouTube text and thumbnail,
runs the QA check for it and marks it done in scripts/episode_plan.md."""
import importlib.util, os, re, shutil, subprocess, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, ROOT)
OUT = os.path.join(ROOT, 'output'); YT = os.path.join(OUT, 'youtube'); SH = os.path.join(OUT, 'shorts')
for d in (OUT, YT, SH): os.makedirs(d, exist_ok=True)
SERIES = 'Art and Culture, Simply Seen'
LABELS = dict(unfold='Intro', look0='Look closely', compare='Side by Side', where='Where to see it', tip='Memory tip', spot_intro='Spot the Style', patch='New patch and next episode')
def stamp(s): return f"{int(s//60)}:{int(s%60):02d}"

def deliver(n):
    nn = f'{n:02d}'; d = os.path.join(ROOT, 'episodes', f'ep{nn}')
    spec = importlib.util.spec_from_file_location('ep', os.path.join(d, 'ep.py')); ep = importlib.util.module_from_spec(spec); spec.loader.exec_module(ep)
    from engine import art
    md = art.parse_md(n); meta = md['meta']
    shutil.copy(os.path.join(d, 'final.mp4'), os.path.join(OUT, f'Art{nn}_{ep.TITLE}.mp4'))
    shutil.copy(os.path.join(d, f'ep{nn}.srt'), os.path.join(OUT, f'Art{nn}.srt'))
    shutil.copy(os.path.join(d, 's', 'final.mp4'), os.path.join(SH, f'Art{nn}_short.mp4'))
    tl = subprocess.run(['python3', '../../engine/cli.py', 'tl'], cwd=d, capture_output=True, text=True).stdout.splitlines()
    rows = [l.split() for l in tl if re.match(r'^\d+ ', l)]
    ch = [(0 if i == 0 else float(r[2]), LABELS[r[1]]) for i, r in enumerate(rows) if r[1] in LABELS]
    gl = art.meta_gloss(meta); tip = ' · '.join(art.meta_tip(meta))
    title = f"{ep.NAME} | {SERIES} · Episode {n}"
    short_title = f"{ep.NAME}: can you spot the style? #Shorts"
    txt = [f"TITLE: {title}", "", "DESCRIPTION:",
           f"Episode {n} of {SERIES}: a calm five-minute animated explainer on {ep.NAME.lower()} for UPSC Art and Culture. Look closely at the parts, compare two styles side by side, learn a memory tip stitched in gold, then test yourself in Spot the Style.",
           "", f"Memory tip: {tip}", "", "Chapters:"] + [f"{stamp(t)} {lab}" for t, lab in ch] + ["", "Glossary:"] + [f"- {a}: {b}" for a, b in gl] + [
           "", "Every episode adds one patch to the culture quilt.", "", "#UPSC #ArtAndCulture #IndianCulture #UPSCPrelims #CivilServices",
           "", "TAGS: UPSC, Art and Culture, Indian art, Indian culture, UPSC Prelims, UPSC Mains, civil services, " + ep.NAME, "",
           "SHORT TITLE: " + short_title, "SHORT DESCRIPTION:",
           f"Can you spot the style? Memory tip: {tip}. Full episode on the channel. #Shorts #UPSC #ArtAndCulture", "",
           f"CAPTIONS FILE: Art{nn}.srt", f"THUMBNAIL: Art{nn}_thumb.png"]
    open(os.path.join(YT, f'Art{nn}.txt'), 'w').write('\n'.join(txt)+'\n')
    art.make_thumb(os.path.join(YT, f'Art{nn}_thumb.png'), n, ep.NAME, ep.SPEC['unfold']['motifs'])
    plan = os.path.join(ROOT, 'scripts', 'episode_plan.md'); s = open(plan).read()
    s = re.sub(r'^(\| %d \|.*\| )[^|]*( \|)$' % n, r'\1done\2', s, flags=re.M); open(plan, 'w').write(s)

if __name__ == '__main__':
    for a in sys.argv[1:]: deliver(int(a)); print('delivered', a)
