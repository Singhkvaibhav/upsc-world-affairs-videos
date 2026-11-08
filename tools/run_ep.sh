#!/usr/bin/env bash
# usage: bash tools/run_ep.sh NN  -> check, tts, render (2 workers), audio, mux, copy to output/, commit + push
set -e
cd "$(dirname "$0")/../episodes/ep$1"
CLI="python3 ../../engine/cli.py"
mkdir -p vo stills; $CLI tts ../../voice/en-us-lessac-medium.onnx > tts.log 2>&1
$CLI check > check.log 2>&1 || { cat check.log; exit 2; }
n=$($CLI tl | grep -c '^[0-9]')
rm -rf parts; mkdir -p parts
for w in 0 1 2; do
  L=$(seq -s, $w 3 $((n-1))); [ -n "$L" ] && $CLI render $L > parts_w$w.log 2>&1 &
done
wait
[ $(ls parts/[0-9]*.mp4 | wc -l) -eq $n ] || { echo "missing parts"; exit 3; }
ls parts/[0-9]*.mp4 | sed "s|^|file '$PWD/|;s|$|'|" > parts/list.txt
ffmpeg -y -loglevel error -f concat -safe 0 -i parts/list.txt -c copy video.mp4
$CLI audio > audio.log 2>&1
ffmpeg -y -loglevel error -i video.mp4 -i mix.wav -c:v copy -c:a aac -b:a 192k -movflags +faststart -shortest final.mp4
TITLE=$(python3 -c "import re;print(re.search(r'TITLE\s*=\s*\"([^\"]+)\"',open('ep.py').read()).group(1))")
cd ../..
cp episodes/ep$1/final.mp4 output/Ep$1_$TITLE.mp4; cp episodes/ep$1/ep$1.srt output/Ep$1.srt
python3 tools/youtube_meta.py $((10#$1)) > /dev/null 2>&1 || true
rm -f .git/index.lock
git add -A engine tools episodes output
git commit -q -m "Add Episode ${1#0}: ${TITLE//_/ } (video + captions)

Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_0147ogfa1xrQmwRVeDBDE2iF"
for i in 1 2 3 4; do git push -q origin claude/videos-ep02-11 && break; sleep $((2**i)); done
echo "EP$1 delivered"
