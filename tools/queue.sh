#!/usr/bin/env bash
# usage: bash tools/queue.sh 12 13 ...  -> for each episode, wait for episodes/epNN/ep.ready then run tools/run_ep.sh
cd "$(dirname "$0")/.."
for n in "$@"; do
  nn=$(printf %02d $n)
  until [ -f episodes/ep$nn/ep.ready ] || [ -f STOP_QUEUE ]; do sleep 15; done
  [ -f STOP_QUEUE ] && break
  bash tools/run_ep.sh $nn > episodes/ep$nn/run.log 2>&1 || echo "EP$nn FAILED" >> queue.log
  tail -1 episodes/ep$nn/run.log >> queue.log
done
