# RASOLV — "Carousel" (vertical explainer film)

~75-second 9:16 film (1080×1920, 30 fps) in the same storytelling and animation language as the Barnum "brick man" film: grey pawn figures
with one orange accent, a mono counter above the stage, a "YOU" silhouette in the foreground with karaoke caption
pills, a title + small mono source line per beat, and a closing twist where the video admits it used the trick on you.

**The story** (true; reported by Alex Stone, "Why Waiting Is Torture", *The New York Times*, Aug 2012): passengers at
a Houston airport complained about the wait at baggage claim. The airport hired more handlers and cut the wait to
eight minutes, within industry benchmarks, but the complaints didn't stop. Looking closer: one minute walking from the
gate, seven minutes standing at the belt (~88% of the trip doing nothing). So they moved the arrival gates away from
the main terminal and sent bags to the outermost carousel. Passengers walked six times longer, and complaints dropped
to near zero.

**Beats** — cold open: a lone orange suitcase circling, no words, clock running → *Why were they so angry?* (crowd
fills in, "!" marks) → the obvious fix (handlers appear, bags flood the belt, counter rolls back to AVG WAIT 8:00) →
complaints flare again → the trip measured (WALK 1:00 / STANDING 7:00 bar, 88% pill) → the opposite fix (floor
plan: gates slide away, orange route to the outermost carousel, WALKING 1:00 → 6:00) → complaints pop away →
*People don't hate waiting. They hate standing still.* → **twist:** the video replays its own opening in a phone frame
("It opened on a suitcase going round. No words. Then it never stood still.") → *You stayed.* → "So here's your
bag." → *Which one gets you: the faster bags, or the longer walk?* → **DM RASOLV · Vision That Solves**.

| file | what it does |
|---|---|
| `vo.py` | The script. Kokoro `am_michael` (male narrator, like the reference). Lines are laid end to end, so the audio sets the timeline; writes `captions.js` (word timings + a `CUE` per line id), `out/vo/`, and `out/rasolv_carousel.srt`. |
| `index.html` | The film as a deterministic canvas `render(t)`; every scene keys off the `CUE` ids, so editing a line re-times everything. Open it in a browser to preview. |
| `render.js` | Playwright → frames → ffmpeg (`SCALE=1` 1080×1920, `SCALE=2` 2160×3840). `--stills <dir> t1,t2` for previews. |
| `score.py` | Original synthesised score (slow A-minor pad, plucked motif per act) + sound design (clock ticks while people wait, belt hum, bag clunks, footsteps while they walk, whooshes, riser into the twist) with VO ducking. |
| `build.sh` | Runs everything → `out/rasolv_carousel_4k.mp4`. |

```bash
KOKORO_DIR=/path/to/kokoro ./build.sh                  # full build (4K60)
SKIP_VO=1 SCALE=1 FPS=30 OUT=draft ./build.sh          # fast 1080x1920 draft, reusing the voiceover
```

Fonts: Space Grotesk + Space Mono (OFL, bundled in `../fonts/`).
