# A&W Tanger — "2 Can Dine" staff video (v3)

25-second vertical (1080×1920, 60 fps) staff reminder, rebuilt from the flat-vector v2 in the same dark
cinematic style as `../cinema/`: real food photography (`img/`), kinetic type, whip/flash cuts, light sweeps,
film grain, word-highlighted captions, a new voice and an upbeat 120 bpm score.

Scenes (each cut lands on the beat, a half-beat before its voice line):
**2 Can Dine · two combos $17.99** (combo trays) → **Say it to every guest** — "Is someone joining you today?"
(burger) → **Ordering one? Make it two. ×2** (two trays) → **Ring it right**: same protein → COUPON,
mixed beef + chicken → MANUAL OVERRIDE, IN-STORE ONLY → **Then add one more**: onion rings, small gravy,
apple turnover, upsize the drink (photo tiles pop in as they're named) → **Mention it. Add one. Ring it right.
Let's go, team!** → 2 Can Dine $17.99 lockup.

Same pipeline as `../cinema/`: `vo.py` (Kokoro `af_bella` at 1.2× speed; lays the lines back-to-back on the
beat grid and writes `captions.js`, which also drives the scene timeline), `index.html` (deterministic
`render(t)`), `render.js` (Playwright → frames → ffmpeg), `score.py` (Bb–F–Gm–Eb groove + sound design +
voice ducking), `build.sh`.

```bash
KOKORO_DIR=/path/to/kokoro ./build.sh                 # full build
SKIP_VO=1 ./build.sh                                  # reuse voiceover/captions
KOKORO_DIR=... VOICE=am_michael SPEED=1.15 ./build.sh  # try another voice
```
