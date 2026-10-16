#!/usr/bin/env bash
# Builds the bilingual (English + Arabic) RASOLV film: 4K UHD (3840x2160) 60fps, voiceover in both languages + captions, original score.
#   KOKORO_DIR must contain kokoro-v1.0.onnx + voices-v1.0.bin (github.com/thewh1teagle/kokoro-onnx releases)
#   ARTTS_DIR  must contain the Piper Arabic voice vits-piper-ar_JO-kareem-medium (github.com/k2-fsa/sherpa-onnx releases, tts-models)
#   Set SKIP_VO=1 to reuse the existing out/vo + captions.js. SCALE=1 renders Full HD (1920x1080).
set -euo pipefail
cd "$(dirname "$0")"
export NODE_PATH="${NODE_PATH:-$(npm root -g)}"
mkdir -p out
if [ "${SKIP_VO:-0}" != 1 ]; then python3 vo.py "$KOKORO_DIR/kokoro-v1.0.onnx" "$KOKORO_DIR/voices-v1.0.bin" "$ARTTS_DIR" "${VOICE:-af_heart}" "${AR_SPEED:-1.18}"; fi
FPS=${FPS:-60}; DUR=$(python3 -c "import json;print(json.load(open('out/vo/lines.json'))['duration'])")
TOTAL=$(python3 -c "print(round($DUR*$FPS))"); WORKERS=${WORKERS:-4}; CHUNK=$(( (TOTAL + WORKERS - 1) / WORKERS ))
for ((i=0; i<WORKERS; i++)); do
  s=$((i*CHUNK)); e=$(( (i+1)*CHUNK < TOTAL ? (i+1)*CHUNK : TOTAL ))
  node render.js "out/seg$i.mp4" $FPS $s $e &
done
python3 score.py out/mix.wav
wait
: > out/list.txt; for ((i=0; i<WORKERS; i++)); do echo "file 'seg$i.mp4'" >> out/list.txt; done
ffmpeg -y -v error -f concat -safe 0 -i out/list.txt -i out/mix.wav \
  -af "loudnorm=I=-14:TP=-1.0:LRA=7" -c:v copy -c:a aac -b:a 320k -ar 48000 -shortest -movflags +faststart out/${OUT:-rasolv_bilingual_4k}.mp4
echo "done: out/${OUT:-rasolv_bilingual_4k}.mp4 (+ out/rasolv_bilingual.srt)"
