#!/usr/bin/env bash
# usage (from an episode folder): bash ../../tools_sheet.sh out.png "scene t" "scene t" ... (2-4 stills -> 2x2 contact sheet)
out=$1; shift; i=0; ins=()
mkdir -p stills
for s in "$@"; do set -- $s; python3 render.py still $1 $2 stills/chk_$i.png || exit 1; ins+=(-i stills/chk_$i.png); i=$((i+1)); done
while [ $i -lt 4 ]; do ins+=(-i stills/chk_0.png); i=$((i+1)); done
ffmpeg -y -loglevel error "${ins[@]}" -filter_complex "[0]scale=960:540[a];[1]scale=960:540[b];[2]scale=960:540[c];[3]scale=960:540[d];[a][b][c][d]xstack=inputs=4:layout=0_0|960_0|0_540|960_540" $out
