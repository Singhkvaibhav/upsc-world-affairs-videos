#!/usr/bin/env bash
# usage: bash tools/fix_stamps.sh NN ...  -> re-render only the beats that use long stamp text, re-concat, re-mux with the existing mix.wav, copy to output/, commit + push
cd "$(dirname "$0")/.."
for nn in "$@"; do
  d=episodes/ep$nn; cd $d
  IDX=$(python3 - <<'PY'
import ast
t = ast.parse(open('ep.py').read()); out = []
beats = next(n for n in ast.walk(t) if isinstance(n, ast.Assign) and getattr(n.targets[0], 'id', '') == 'BEATS').value
for i, el in enumerate(beats.elts):
    for c in ast.walk(el):
        if isinstance(c, ast.Call) and getattr(c.func, 'id', None) == 'ST' and len(c.args) >= 3 and all(isinstance(a, ast.Constant) for a in c.args[:3]):
            top, mid, bot = [a.value for a in c.args[:3]]
            if len(bot) > 34 or len(top) > 24: out.append(i); break
print(','.join(map(str, out)))
PY
)
  [ -z "$IDX" ] && { cd ../..; continue; }
  CLI="python3 ../../engine/cli.py"
  L0=$(echo $IDX | tr ',' '\n' | awk 'NR%3==1' | paste -sd,); L1=$(echo $IDX | tr ',' '\n' | awk 'NR%3==2' | paste -sd,); L2=$(echo $IDX | tr ',' '\n' | awk 'NR%3==0' | paste -sd,)
  for L in "$L0" "$L1" "$L2"; do [ -n "$L" ] && $CLI render $L > /dev/null 2>&1 & done; wait
  ls parts/[0-9]*.mp4 | sed "s|^|file '$PWD/|;s|$|'|" > parts/list.txt
  ffmpeg -y -loglevel error -f concat -safe 0 -i parts/list.txt -c copy video.mp4
  ffmpeg -y -loglevel error -i video.mp4 -i mix.wav -c:v copy -c:a aac -b:a 192k -movflags +faststart -shortest final.mp4
  cd ../..
  f=$(ls output/Ep${nn}_*.mp4); cp episodes/ep$nn/final.mp4 "$f"
  rm -f .git/index.lock; git add -A output episodes tools engine
  git commit -q -m "Episode ${nn#0}: re-render stamp scenes so long text fits inside the stamp

Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_0147ogfa1xrQmwRVeDBDE2iF"
  for i in 1 2 3 4; do git push -q origin claude/videos-ep02-11 && break; sleep $((2**i)); done
  echo "FIXED $nn ($IDX)" >> queue.log
done
