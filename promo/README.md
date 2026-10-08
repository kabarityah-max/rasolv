# RASOLV promo video

4K vertical (2160×3840, 60 fps, H.264 High@5.2 + 320 kbps AAC), ~19.6 s. Dark cinematic style:
orange brand glow → 3D phone with a RASOLV live activity → camera push into the app UI →
agents list → dive into the send button → beat drop with kinetic type → logo reveal.

| File | What it does |
|---|---|
| `index.html` | The whole animation as a deterministic `render(t)` timeline. Open it in a browser to preview it looping. |
| `render.js` | Playwright renders each frame at 2× device scale (4K) and pipes PNGs into ffmpeg. |
| `music.py` | Original 125 BPM track (pads, arp, bass, drums, riser, drop at 9.6 s, logo impact) + sound design + voiceover mix with ducking. Fully synthesised, so it's royalty-free. |
| `vo.py` | Generates the voiceover with Kokoro (open-weights TTS, voice `af_heart`). Output WAVs are committed in `vo/`. |
| `build.sh` | Runs everything; output lands in `out/rasolv_promo_4k.mp4`. |
| `v1.html`, `v1_sfx.py` | The first (light, Uber-style) version, kept for reference. |

Voiceover script (edit `LINES` in `vo.py`, then re-time `VO_AT` in `music.py` and `PHRASES` in `index.html`):

1. Something broke. And you need it fixed... now.
2. With Rasolv, a real expert is already on it.
3. Live updates. Real people. Answers in minutes.
4. Support that actually solves.
5. One app. Every answer.
6. Your data stays yours.
7. Rasolv. Vision that solves.

"Rasolv" is pronounced *rah-ZOLV* (set via the `BRAND` phonemes in `vo.py`).

To regenerate the voice: download `kokoro-v1.0.onnx` and `voices-v1.0.bin` from
https://github.com/thewh1teagle/kokoro-onnx/releases (model-files-v1.0), `pip install kokoro-onnx soundfile scipy`,
then `python3 vo.py kokoro-v1.0.onnx voices-v1.0.bin af_heart`.

Brand: orange `#FF6E05`, ink `#070707`, white; Rubik (bundled in `fonts/`). The aperture mark is drawn
procedurally by `aperture()` so the iris can open on reveals; `brand-reference.png` is the brand sheet.

## Download

`promo/release/rasolv_promo_4k.mp4` — the final 4K60 video (H.264 32 Mb/s, ~79 MB; SSIM 0.995 vs. the
lossless-ish render master that `build.sh` produces in `out/`).
