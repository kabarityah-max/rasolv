# RASOLV "Two clocks" teaser (30 s, 9:16, 4K60)

Teaser for the bilingual film (`../bilingual/`). Script and caption copy: `CONCEPT.md`.

A split screen, two clocks from 00:00. **Left (grey):** a tired face lit by a phone on speaker, hold music, a
window going from dusk to dark, a call screen where nothing happens. **Right (orange `#FF6E05`):** a thumb types
"Charged twice for my order. Need a refund." and sends. "Charged twice" and "refund" light up, Maya · Billing
joins at 00:06, Maya works the case at her desk, and live updates stack (00:31 / 01:48 / 03:59). The right clock
stops at **4:00**. The left one keeps going, takes the frame and races to **40:00**. Then a hard cut to black and
one beat of true silence, and *Stop waiting. Someone real is **already on it.*** types in. The seam slides back in
and folds into the aperture mark: **RASOLV · One picture. Two languages. · Thu Oct 22 · 8pm [TZ] · Set a reminder**
(pulses once) · *Get the RASOLV app.* · VISION THAT SOLVES · رؤية تحُلّ.

The stereo field follows the split: the hold music and dull tick sit left, the bright tick and update pops sit right.
"Example story. Times vary." is on screen from the 4:00 stop until the cut to black.

| file | what it does |
|---|---|
| `vo.py` | The 7 VO lines (Kokoro `af_heart`, "Rasolv" forced to *rah-ZOLV*), each placed on its beat. Asserts every line ends before the next starts. Writes `out/vo/` and `out/rasolv_twoclocks.srt`. |
| `index.html` | The film as a deterministic `render(t)` timeline (1080×1920 CSS px). Open it in a browser to preview it looping. Beat times are in `T`, and what the clocks read is in `STORY_R` / `STORY_L`. |
| `render.js` | Playwright renders frames, piped to ffmpeg (`SCALE=2` gives 2160×3840, `SCALE=1` gives 1080×1920). `--stills <dir> t1,t2` for previews. |
| `score.py` | Sound design + bed, synced to the same beats, with the VO mixed on top and ducking. |
| `build.sh` | Runs everything and writes `out/rasolv_twoclocks_4k.mp4`. |

```bash
KOKORO_DIR=/path/to/kokoro ./build.sh         # full build
TZ_LABEL=GST SKIP_VO=1 ./build.sh             # set the premiere time zone on the end card ([TZ] by default)
SKIP_VO=1 SCALE=1 FPS=30 OUT=draft ./build.sh # fast 1080p draft
```

**Before posting:** the release files carry the literal placeholder `[TZ]` on the end card. Re-render with
`TZ_LABEL=…` once the market is set (or change `PREMIERE` in `index.html`). The name Maya and the times are
illustrative, as the on-screen disclaimer says.

## Download

- `release/rasolv_twoclocks_4k.mp4`: 2160×3840, 60 fps, H.264 + AAC 320k, -14 LUFS
- `release/rasolv_twoclocks_1080p.mp4`: 1080×1920 copy for upload
- `release/rasolv_twoclocks.srt`: VO captions
