#!/usr/bin/env bash
# Builds the A&W Tanger "2 Can Dine" staff video: 1080x1920 vertical, 60fps, voiceover + captions, original score.
#   KOKORO_DIR must contain kokoro-v1.0.onnx + voices-v1.0.bin (github.com/thewh1teagle/kokoro-onnx releases)
#   Set SKIP_VO=1 to reuse the existing out/vo + captions.js. VOICE / SPEED pick the Kokoro voice (default af_bella @ 1.2).
set -euo pipefail
cd "$(dirname "$0")"
export NODE_PATH="${NODE_PATH:-$(npm root -g)}"
mkdir -p out
if [ "${SKIP_VO:-0}" != 1 ]; then python3 vo.py "$KOKORO_DIR/kokoro-v1.0.onnx" "$KOKORO_DIR/voices-v1.0.bin" "${VOICE:-af_bella}" "${SPEED:-1.2}"; fi
FPS=60; DUR=$(python3 -c "import json;print(json.load(open('out/vo/lines.json'))['duration'])")
TOTAL=$(python3 -c "print(round($DUR*$FPS))"); WORKERS=${WORKERS:-4}; CHUNK=$(( (TOTAL + WORKERS - 1) / WORKERS ))
for ((i=0; i<WORKERS; i++)); do
  s=$((i*CHUNK)); e=$(( (i+1)*CHUNK < TOTAL ? (i+1)*CHUNK : TOTAL ))
  node render.js "out/seg$i.mp4" $FPS $s $e &
done
python3 score.py out/mix.wav
wait
: > out/list.txt; for ((i=0; i<WORKERS; i++)); do echo "file 'seg$i.mp4'" >> out/list.txt; done
ffmpeg -y -v error -f concat -safe 0 -i out/list.txt -i out/mix.wav \
  -af "loudnorm=I=-14:TP=-1.0:LRA=7" -c:v copy -c:a aac -b:a 320k -ar 48000 -shortest -movflags +faststart out/${OUT:-aw_2candine_staff_v3}.mp4
echo "done: out/${OUT:-aw_2candine_staff_v3}.mp4 (+ out/aw_2candine.srt)"
