# RASOLV cinematic film (4K, dark style, voiceover + captions)

45-second 16:9 dark cinematic brand film, modelled on the "Multimercial"-style After Effects reel:
told around the RASOLV app — report a problem, a real expert picks it up, live updates, solved in minutes:
**"What if getting help wasn't a waiting game… but one tap away?" + phone → orange light beams build the
aperture logo ("real experts · real answers · in minutes") → glass sphere rises, Billing / Orders / Accounts /
Tech / Refunds icons orbit the logo and collapse into a focus reticle → issue chips inside the sphere (the
categories light up as they're spoken, "Payment failed" becomes the reported problem) → live ticket chips
(Ticket #4821, experts reviewing, reply countdown, LIVE updates) with a tap on "Maya Haddad · Billing expert"
and "Refund issued in 4 min" → dots link into a ring ("an expert is on it") → "One app. Every answer. Your data
stays yours." + categories → Tap. / Track. / Solved. word beats with a giant ring hit → RGB-glitch logo →
spaced RASOLV wordmark.**

3840×2160, 60 fps, H.264 + AAC 320 kbps, −14 LUFS. Captions burned in (word highlight) and in `out/rasolv_cinema.srt`.

Same pipeline as `../film/`: `vo.py` (Kokoro voice `af_heart`, "Rasolv" forced to *rah-ZOLV*, writes
`captions.js`), `index.html` (deterministic `render(t)`), `render.js` (Playwright → 4K frames → ffmpeg),
`score.py` (original D-minor score at 112.5 bpm + sound design + VO ducking), `build.sh`.

```bash
KOKORO_DIR=/path/to/kokoro ./build.sh   # full build
SKIP_VO=1 ./build.sh                     # reuse voiceover/captions
```

Names, ticket numbers and timings (Maya Haddad, #4821, 4.9★, refund in 4 min) mirror the main promo and are
illustrative — swap in real ones before publishing.
