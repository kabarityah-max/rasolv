#!/usr/bin/env bash
# Builds the "Two clocks" RASOLV teaser: 30 s, 9:16, 4K (2160x3840) 60fps, voiceover + supers, original sound design.
#   KOKORO_DIR must contain kokoro-v1.0.onnx + voices-v1.0.bin (github.com/thewh1teagle/kokoro-onnx releases)
#   Set SKIP_VO=1 to reuse the existing out/vo. SCALE=1 renders 1080x1920. TZ_LABEL sets the premiere time zone on the end card.
#   WORKERS defaults to 2: each 4K x264 encoder needs ~2 GB, so more parallel workers can run a 16 GB box out of memory.
set -euo pipefail
cd "$(dirname "$0")"
export NODE_PATH="${NODE_PATH:-$(npm root -g)}"
mkdir -p out
if [ "${SKIP_VO:-0}" != 1 ]; then python3 vo.py "$KOKORO_DIR/kokoro-v1.0.onnx" "$KOKORO_DIR/voices-v1.0.bin" "${VOICE:-af_heart}"; fi
FPS=${FPS:-60}; TOTAL=$(python3 -c "print(round(30.0*$FPS))"); WORKERS=${WORKERS:-2}; CHUNK=$(( (TOTAL + WORKERS - 1) / WORKERS ))
for ((i=0; i<WORKERS; i++)); do
  s=$((i*CHUNK)); e=$(( (i+1)*CHUNK < TOTAL ? (i+1)*CHUNK : TOTAL ))
  node render.js "out/seg$i.mp4" $FPS $s $e &
done
python3 score.py out/mix.wav
wait
: > out/list.txt; for ((i=0; i<WORKERS; i++)); do echo "file 'seg$i.mp4'" >> out/list.txt; done
ffmpeg -y -v error -f concat -safe 0 -i out/list.txt -i out/mix.wav \
  -af "loudnorm=I=-14:TP=-1.0:LRA=7" -c:v copy -c:a aac -b:a 320k -ar 48000 -shortest -movflags +faststart out/${OUT:-rasolv_twoclocks_4k}.mp4
echo "done: out/${OUT:-rasolv_twoclocks_4k}.mp4 (+ out/rasolv_twoclocks.srt)"
