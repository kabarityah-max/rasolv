# RASOLV — "Show Your Work" (vertical TikTok explainer)

~55-second 9:16 TikTok (1080×1920, 60 fps) in the same storytelling and animation language as `../carousel/`
(the airport film): grey pawns with one orange accent, mono read-outs, a "YOU" silhouette in the foreground with
karaoke caption pills, a title + small mono source line per beat, and a twist where the video admits it used the
trick on you. Same pace and sound as Carousel too: a silent cold open, Kokoro `am_michael` at 0.98× with the same
gaps, slow crossfades, and a quiet pad-and-pluck score under the voice. The difference is a fully **on-brand ending**: the film leaves the grey world for RASOLV ink
and orange, shows the app working live, then opens the aperture iris onto the Rubik wordmark, "Vision that solves"
and an orange **Get RASOLV · link in bio** button.

**The story** (Ryan Buell & Michael Norton, Harvard Business School, "The Labor Illusion: How Operational
Transparency Increases Perceived Value", *Management Science*, 2011): two flight searches return the same flights.
One answers instantly; the other makes you wait but shows each airline being checked. People rated the one that
showed its work higher, even with waits of up to a minute.

**Beats**: a lone site checking airlines, *made to wait… and they liked it more* (stars land) → Site A instant vs.
Site B checking AIRLINE 01…48 → *Same flights* (=) → rating bars, B higher; B's timer rolls to 1:00 → *The labor
illusion* (VISIBLE EFFORT) → *People don't hate waiting. They hate waiting blind.* (spinner pawn with "!" vs. a
pawn watching steps tick) → **twist:** the video replays itself in a phone frame and the STEP read-out
that has run in the top corner all along comes forward ("A counter that never stopped." "You never asked.") →
**That's how RASOLV works**: the app with a real expert, steps ticking live → aperture + wordmark
+ CTA.

| file | what it does |
|---|---|
| `vo.py` | The script. Lines laid end to end (Carousel pacing); writes `captions.js` (word timings + a `CUE` per line id), `out/vo/`, and `out/rasolv_show_your_work.srt`. "Rasolv" is spoken rah-ZOLV. |
| `index.html` | The film as a deterministic canvas `render(t)`; every scene keys off the `CUE` ids. Includes a canvas port of the aperture mark from `../index.html`. Open in a browser to preview. |
| `render.js` | Playwright → frames → ffmpeg (`SCALE=1` 1080×1920, `SCALE=2` 2160×3840). `--stills <dir> t1,t2` for previews. |
| `score.py` | Carousel-style score: slow F-minor pad, a plucked motif per act, quiet sound design (airline ticks, result pops, a clock, app chimes, riser into the twist, logo hit), VO ducking. Royalty-free. |
| `build.sh` | Runs everything → `out/rasolv_show_your_work_master.mp4`. |

```bash
KOKORO_DIR=/path/to/kokoro ./build.sh                  # full build (1080x1920, 60 fps)
SKIP_VO=1 FPS=30 OUT=draft ./build.sh                  # fast draft, reusing the voiceover
```

TikTok safe zones: titles sit below the top tabs, captions at y≈1376 (above the caption/username block), and
nothing important runs under the right-hand action column. Release file: `release/rasolv_show_your_work_1080p.mp4`
(+ `release/rasolv_show_your_work.srt` for TikTok's caption upload, if you want the auto-captions off).
