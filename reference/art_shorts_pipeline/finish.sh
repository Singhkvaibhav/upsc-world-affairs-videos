#!/usr/bin/env bash
# usage: bash tools/finish.sh NN  -> deliver, QA, then commit and push to main (stops if a scratch file is staged)
set -e
cd "$(dirname "$0")/.."
python3 tools/deliver.py $1; python3 tools/qa.py $((10#$1))
git add engine tools scripts episodes/ep$1/ep.py episodes/ep$1/short.py output .gitignore
bad=$(git diff --cached --diff-filter=AM --name-only | grep -E '(^|/)(vo|parts|stills)/|\.wav$|\.log$|\.part\.mp4$|video\.mp4$|final\.mp4$|sheet' || true)
[ -z "$bad" ] || { echo "scratch files staged: $bad"; exit 4; }
git status --short | head -20
git commit -q -m "${2:-Add Art and Culture episode $((10#$1)) with its Short}

Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_0147ogfc6vohDnwJ5QsLrq1q"
git fetch -q origin main && git rebase -q origin/main || true
for i in 1 2 3 4; do git push -q origin HEAD:main && break; sleep $((2**i)); done
echo "pushed EP$1"
