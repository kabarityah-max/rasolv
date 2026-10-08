#!/usr/bin/env bash
# Builds the 4K (2160x3840, 60fps) Resolve promo: renders frames in parallel, synthesises audio, muxes.
set -euo pipefail
cd "$(dirname "$0")"
export NODE_PATH="${NODE_PATH:-$(npm root -g)}"
mkdir -p out
FPS=60; TOTAL=840; WORKERS=${WORKERS:-3}; CHUNK=$(( (TOTAL + WORKERS - 1) / WORKERS ))
for ((i=0; i<WORKERS; i++)); do
  s=$((i*CHUNK)); e=$(( (i+1)*CHUNK < TOTAL ? (i+1)*CHUNK : TOTAL ))
  node render.js "out/seg$i.mp4" $FPS $s $e &
done
wait
python3 sfx.py out/audio.wav
: > out/list.txt; for ((i=0; i<WORKERS; i++)); do echo "file 'seg$i.mp4'" >> out/list.txt; done
ffmpeg -y -v error -f concat -safe 0 -i out/list.txt -i out/audio.wav \
  -c:v copy -c:a aac -b:a 320k -ar 48000 -shortest -movflags +faststart out/resolve_promo_4k.mp4
echo "done: out/resolve_promo_4k.mp4"
