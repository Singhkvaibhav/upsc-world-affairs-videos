#!/usr/bin/env bash
# usage (from an episode folder, after render_ep.sh): builds mix.wav + srt and muxes final.mp4
set -e
n=$(basename "$PWD" | sed 's/ep//')
python3 audio.py > audio.log 2>&1
ffmpeg -y -loglevel error -i video.mp4 -i mix.wav -c:v copy -c:a aac -b:a 192k -movflags +faststart -shortest final.mp4
echo "final.mp4 ok"
