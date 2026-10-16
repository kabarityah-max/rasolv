#!/usr/bin/env bash
# Builds the RASOLV "on hold" story reel: 1080x1920 vertical, 30 fps, voiceover + captions, original score.
#   KOKORO_DIR must contain kokoro-v1.0.onnx + voices-v1.0.bin (github.com/thewh1teagle/kokoro-onnx releases)
#   SKIP_VO=1 reuses out/vo + captions.js. VOICE / SPEED pick the Kokoro voice (default am_michael @ 0.97).
#   SCALE=2 renders 2160x3840. OUT names the output file (default rasolv_hold).
set -euo pipefail
cd "$(dirname "$0")"
export NODE_PATH="${NODE_PATH:-$(npm root -g)}"
mkdir -p out
if [ "${SKIP_VO:-0}" != 1 ]; then python3 vo.py "$KOKORO_DIR/kokoro-v1.0.onnx" "$KOKORO_DIR/voices-v1.0.bin" "${VOICE:-am_michael}" "${SPEED:-0.97}"; fi
FPS=${FPS:-30}; DUR=$(python3 -c "import json;print(json.load(open('out/vo/lines.json'))['duration'])")
TOTAL=$(python3 -c "print(round($DUR*$FPS))"); WORKERS=${WORKERS:-4}; CHUNK=$(( (TOTAL + WORKERS - 1) / WORKERS ))
for ((i=0; i<WORKERS; i++)); do
  s=$((i*CHUNK)); e=$(( (i+1)*CHUNK < TOTAL ? (i+1)*CHUNK : TOTAL ))
  node render.js "out/seg$i.mp4" $FPS $s $e &
done
python3 score.py out/mix.wav
wait
: > out/list.txt; for ((i=0; i<WORKERS; i++)); do echo "file 'seg$i.mp4'" >> out/list.txt; done
ffmpeg -y -v error -f concat -safe 0 -i out/list.txt -i out/mix.wav \
  -af "loudnorm=I=-14:TP=-1.0:LRA=9" -c:v copy -c:a aac -b:a 256k -ar 48000 -shortest -movflags +faststart out/${OUT:-rasolv_hold}.mp4
echo "done: out/${OUT:-rasolv_hold}.mp4 (+ out/rasolv_hold.srt)"
