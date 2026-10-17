# RASOLV — "Nobody animated this video" (one-prompt reel)

31.5 s vertical reel (1080×1920, 60 fps, H.264 + 320 kbps AAC, −14 LUFS) for Reels / TikTok / Shorts. The video is
the proof: it flexes six motion-graphics techniques, then reveals it was made from a single prompt in Claude Code,
and ends on a comment-to-DM CTA.

| t (s) | beat | on screen |
|---|---|---|
| 0.0 – 1.7 | **Hook** | NOBODY / ANIMATED / THIS / VIDEO. slam in word by word with the voice, over the aperture iris, with shockwave rings and camera shake. Frame 0 is already sharp, so it works as the thumbnail. |
| 1.7 – 5.5 | **Stakes** | "// made without": *No After Effects*, *No keyframes*, *No motion designer* cards slide in and get struck out. Orange disc wipe into the drop. |
| 5.5 – 11.5 | **Flex montage** (1 s per card, on the beat) | 01 kinetic type (11 echo layers) · 02 3D camera (RASOLV app on a phone, depth chips, grid floor) · 03 particles (2,400 → the RASOLV mark) · 04 morphs · 05 data viz (counter, bars, line) · 06 glitch. A `FRAME 0000 / 1890` HUD runs on top and seeds the question. |
| 11.5 – 13.3 | **Suspense** | Freeze, tape stop, desaturate, fade to black, heartbeat: "So… how was this **made?**" |
| 13.3 – 17.0 | **Reveal** | A terminal opens out of the cursor. The prompt types itself, then Enter, Working…, ✓ index.html, ✓ score.py, ✓ vo.py, ◐ render. |
| 17.0 – 22.9 | **Payoff** | Drop: **ONE PROMPT.** + "in Claude Code". A checklist ticks as the voice names each part: animation ✓, music ✓, this voice ✓, every frame (render bar 0 → 1890). |
| 22.9 – 25.3 | **Thesis** | "this is how MOTION GRAPHICS get made in **2026**" (the year spins in like a slot machine). |
| 25.3 – 29.2 | **CTA** | WANT THE EXACT PROMPT? "PROMPT" gets typed into a comment box and sent ♥, a paper plane flies off, and a DM notification lands: *RASOLV: Here's your prompt ✦*. |
| 29.2 – 31.5 | **Outro** | The aperture logo opens, then RASOLV · Vision That Solves, a **+ Follow for more** button, and "comment PROMPT → we'll DM it". |

Everything sits inside the platform safe zone (y 220–1500, x 70–1010), clear of the caption and button overlays.

## The prompt (send this when people comment PROMPT)

> Make a 30-second vertical (1080×1920, 60fps) motion-graphics reel for my brand RASOLV (orange #FF6E05 on near-black,
> Rubik font, hexagonal aperture logo). Build it as a deterministic HTML/JS timeline, a `render(t)` function, and
> render every frame with Playwright → ffmpeg.
> Structure: (1) a 1-second hook: "NOBODY ANIMATED THIS VIDEO." slamming in word by word with camera shake, synced to
> the voice; (2) "No After Effects. No keyframes. No motion designer." as cards that get struck out; (3) a beat-synced
> montage, 1 second per technique, each labelled: kinetic type, 3D camera, particles forming my logo, shape morphs,
> data viz, glitch; (4) a suspense freeze: "So… how was this made?"; (5) the reveal: a terminal typing this prompt,
> then "ONE PROMPT. In Claude Code." and a checklist (animation, music, voice, every frame); (6) "this is how motion
> graphics get made in 2026"; (7) the CTA: "Comment PROMPT and we'll DM it to you", with a comment being typed and a
> DM notification landing; (8) logo + follow.
> Write an original 120 BPM score and sound design in Python (numpy, no samples), generate the voiceover with an
> open TTS model, time every cut to the voice's word timings, duck the music under the voice, and master to −14 LUFS.

## Files

| file | what it does |
|---|---|
| `vo.py` | Voiceover script → Kokoro `af_heart` at 1.1× ("Rasolv" forced to *rah-ZOLV*). Writes `out/vo/*.wav`, `captions.js` (word timings that drive the picture) and `out/rasolv_reel.srt`. |
| `index.html` | The reel as a deterministic `render(t)` timeline. Open it in a browser to preview it looping. |
| `render.js` | Playwright → PNG frames → ffmpeg (`SCALE=1` 1080×1920, `SCALE=2` 2160×3840). `--stills <dir> t1,t2` for preview stills. |
| `score.py` | Original 120 BPM D-minor score + sound design (instruments shared with `../bilingual/score.py`), cue times read from `captions.js`, voice mixed in with sidechain ducking. |
| `build.sh` | Runs everything → `out/rasolv_prompt_reel.mp4`. |

```bash
KOKORO_DIR=/path/to/kokoro ./build.sh     # full build (voice + picture + score)
SKIP_VO=1 ./build.sh                      # reuse the voiceover
SKIP_VO=1 SCALE=2 OUT=rasolv_prompt_reel_4k ./build.sh   # 4K master
```

Fonts: Rubik (`../fonts/Rubik.woff2`) and JetBrains Mono (`../fonts/JetBrainsMono-*.woff2`, OFL, see
`../fonts/JetBrainsMono-OFL.txt`). The release file is `release/rasolv_prompt_reel.mp4`.

**Caption to post with it:**
Nobody animated this. One prompt → a full motion-graphics reel: animation, music, voice, render. 🎬
Comment **PROMPT** and we'll DM you the exact prompt. Follow @rasolv for more.
