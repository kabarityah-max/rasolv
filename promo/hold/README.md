# RASOLV — "You're on hold" story reel

88-second vertical (1080×1920, 30 fps) explainer in the flat-vector parable style of the "a man moved five bricks
around a New York street corner" reel: a grey world, one accent colour, a crowd of pawn figures, a **YOU** pawn in the
foreground, a counter in the corner, bold headline + monospace subline, a dark caption pill whose words light up as they
are spoken — and the same two-act structure: a true story about a trick, then the twist that the viewer just fell for
the same trick, then the call to action.

**Story:** four wordless seconds of tinny hold music over a phone on a pedestal, `ON HOLD: 0:03` ticking → *Why is
there music on hold?* → New York, 1962: Alfred Levy's factory, a loose wire on a steel beam turns the building into a
radio antenna, callers on hold hear a station and stop hanging up (nobody waited less; they just stopped noticing) →
patented 1966 → sixty years later it plays on every support line (the crowd, all on their phones) → *What did it fix?
Nothing. The trick: fill the silence* → the second trick, in the dark: the sign **YOUR CALL IS IMPORTANT TO US**
(*Important: keep waiting*) → *A tune nobody chose. A line nobody means.* → *This video opened the same way: four
seconds of hold music, no words. You stayed* (you, still holding at 1:07) → *So here's your exit*: the hold music is
cut by a hang-up click, the RASOLV aperture opens → *Rasolv doesn't put you on hold. A real expert is already on it.
Live updates. Answers in minutes.* → *Which one gets you? The tune, or the answer?* → RASOLV · Vision that solves ·
Download Rasolv.

The hold-music origin story (Alfred Levy, the loose wire, the 1966 patent) is the commonly told account; the sublines
hedge it ("by Levy's account") the way the reference hedges Barnum. "Maya · Billing / Solved · 4 min" on the answer
card is an illustrative placeholder, as in the other promos.

| file | what it does |
|---|---|
| `vo.py` | Narration script (`LINES`, with per-line pauses) + Kokoro TTS (voice `am_michael` at 0.97×, "Rasolv" forced to *rah-ZOLV*). Estimates word timings from the audio and writes `captions.js` (captions + scene timeline), `out/vo/*.wav`, `out/rasolv_hold.srt`. |
| `index.html` | The whole film as a deterministic `render(t)`: street / dark hall / pair / recap / end scenes, crowd, hold timer, headlines, caption pill, aperture logo. Open it in a browser to preview it looping. |
| `render.js` | Playwright renders frames (SCALE=2 for 4K) and pipes them to ffmpeg. `--stills <dir> t1,t2` for previews. |
| `score.py` | Synthesised soundtrack: bossa "muzak" through a telephone band-pass (the diegetic hook; muffled in the hall, back for the recap, killed by the hang-up), felt-piano + pad underscore (D minor in the dark), warm RASOLV bed after the click, sound design, voice with ducking. |
| `build.sh` | Runs everything → `out/rasolv_hold.mp4` (loudness-normalised to −14 LUFS). |

```bash
KOKORO_DIR=/path/to/kokoro ./build.sh          # full build (voice + video + audio)
SKIP_VO=1 ./build.sh                            # reuse voiceover/captions
SCALE=2 OUT=rasolv_hold_4k SKIP_VO=1 ./build.sh # 2160x3840
```

To change the narration, edit `LINES` in `vo.py` and rebuild: scene cuts, headlines (`HL` in `index.html`) and the
music cues are keyed to the line and word timings, so everything re-aligns automatically.
