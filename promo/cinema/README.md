# RASOLV cinematic film (4K, dark style, voiceover + captions)

45-second 16:9 dark cinematic brand film, modelled on the "Multimercial"-style After Effects reel:
AI-powered, told around the RASOLV app:
**"What if getting help wasn't a waiting game… but one tap away?" + phone → orange light beams build the
aperture logo ("AI that sees the whole picture") → glass sphere rises, Billing / Orders / Accounts / Tech icons
orbit the logo and collapse into a focus reticle → AI signal chips inside the sphere (intent / sentiment /
history / urgency light up as they're spoken) → hand-off chips: AI match 98%, a tap on "Maya Haddad · Billing
expert", "answer drafted", reply countdown, LIVE updates, "Refund issued in 4 min" → dots link into a ring
("no one waits.") → "One app. Every answer. Your data stays yours." + categories → See. / Decide. / Solve.
word beats with a giant ring hit → RGB-glitch logo → spaced RASOLV wordmark.**

3840×2160, 60 fps, H.264 + AAC 320 kbps, −14 LUFS. Captions burned in (word highlight) and in `out/rasolv_cinema.srt`.

Same pipeline as `../film/`: `vo.py` (Kokoro voice `af_heart`, "Rasolv" forced to *rah-ZOLV*, writes
`captions.js`), `index.html` (deterministic `render(t)`), `render.js` (Playwright → 4K frames → ffmpeg),
`score.py` (original D-minor score at 112.5 bpm + sound design + VO ducking), `build.sh`.

```bash
KOKORO_DIR=/path/to/kokoro ./build.sh   # full build
SKIP_VO=1 ./build.sh                     # reuse voiceover/captions
SCALE=1 OUT=rasolv_cinema_1080p SKIP_VO=1 ./build.sh   # Full HD (1920x1080), ~4x faster
```

Names and numbers (Maya Haddad, AI match 98%, 4.9★, refund in 4 min) mirror the main promo and are
illustrative — swap in real ones before publishing.
