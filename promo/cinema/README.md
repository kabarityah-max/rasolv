# RASOLV cinematic film (4K, dark style, voiceover + captions)

45-second 16:9 dark cinematic brand film, modelled on the "Multimercial"-style After Effects reel:
**typed hook + floating phone → orange light beams build the aperture logo → glass sphere rises, channels
orbit the logo and collapse into a focus reticle → keyword chips inside the sphere (intent / sentiment /
history / urgency light up as they're spoken) → metric chips with live counters and a cursor click →
dots link into a square that bends into a ring ("no one waits.") → "Trusted by teams…" + industries →
See. / Decide. / Solve. word beats with a giant ring hit → RGB-glitch logo → spaced RASOLV wordmark.**

3840×2160, 60 fps, H.264 + AAC 320 kbps, −14 LUFS. Captions burned in (word highlight) and in `out/rasolv_cinema.srt`.

Same pipeline as `../film/`: `vo.py` (Kokoro voice `af_heart`, "Rasolv" forced to *rah-ZOLV*, writes
`captions.js`), `index.html` (deterministic `render(t)`), `render.js` (Playwright → 4K frames → ffmpeg),
`score.py` (original D-minor score at 112.5 bpm + sound design + VO ducking), `build.sh`.

```bash
KOKORO_DIR=/path/to/kokoro ./build.sh   # full build
SKIP_VO=1 ./build.sh                     # reuse voiceover/captions
```

The metric values (−62% first response, +38% CSAT, 4 min resolution, …) are illustrative placeholders, and the
industry row lists sectors, not customers — swap in real numbers/logos before publishing.
