#!/usr/bin/env bash
# usage (from an episode folder): bash ../../tools/render_ep.sh  -> renders all beats with 2 workers, then assembles video.mp4
n=$(python3 render.py tl | grep -c '^[0-9]')
ev=$(seq -s, 0 2 $((n-1))); od=$(seq -s, 1 2 $((n-1)))
rm -f parts/*.mp4
python3 render.py render $ev > parts_even.log 2>&1 &
python3 render.py render $od > parts_odd.log 2>&1 &
wait
[ $(ls parts/[0-9]*.mp4 | wc -l) -eq $n ] || { echo "missing parts"; exit 1; }
ls parts/[0-9]*.mp4 | sed "s|^|file '$PWD/|;s|$|'|" > parts/list.txt
ffmpeg -y -loglevel error -f concat -safe 0 -i parts/list.txt -c copy video.mp4 && echo "video.mp4 ok"
