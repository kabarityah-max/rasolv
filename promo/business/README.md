# RASOLV for Business — "What does one hour of waiting cost?"

30-second vertical ad (1080×1920, 60 fps, H.264 + AAC 320 kbps, −14 LUFS) for business owners. Fully coded — no
AI-generated footage. The founder (a stylised vector character drawn from `founder-reference.png`) and Claude Code
(a pixel character living in a terminal) present it as a double act. Script and shot list: `SCRIPT.md`.

**Edge:** *Everyone has AI. Not everyone knows how to use it.* — *Same AI. Different hands.*

Cut on a 128 BPM grid (16 bars = 30 s): clock-tick cold open → ECU eyes as the orange key light snaps on →
"HUMAN!!!" phone → silhouette → whip pan to an owner drowning in AI bullet points → Claude Code pops out of a
terminal → low-angle dolly "We don't." → dead black → **drop: SAME AI. DIFFERENT HANDS.** → sort / route / "Not one
hour. Four minutes." / Branch-4 insight / lock → backlit hero shot → RASOLV iris + *Built with Claude Code*.

| File | What it does |
|---|---|
| `index.html` | The whole film as a deterministic `render(t)` timeline (founder rig with blink + VO-driven lip sync, Claude Code character, all shots, shake/whip/flash post). Open it in a browser to preview it looping. |
| `vo.py` | Two-voice dialogue with Kokoro (founder `am_onyx`, Claude Code `af_heart`); writes `captions.js` (word-timed captions + 60 Hz mouth envelopes) and `out/rasolv_business.srt`. |
| `score.py` | Original 128 BPM score + sound design synced to the cuts, VO mixed with ducking. Shares instruments with `../cinema/score.py`. Royalty-free. |
| `render.js` | Playwright → frames → ffmpeg. `SCALE=2` for 4K (2160×3840). `node render.js --stills <dir> 1.0,2.5` for preview stills. |
| `build.sh` | Runs everything → `out/rasolv_business.mp4`. |

```bash
KOKORO_DIR=/path/to/kokoro ./build.sh   # full build
SKIP_VO=1 ./build.sh                     # reuse voiceover/captions
SCALE=2 OUT=rasolv_business_4k SKIP_VO=1 ./build.sh
```

To swap in the founder's own voice: replace `out/vo/NN.wav` for the `F` lines (same start times in `vo.py`),
re-run the caption/mouth step, then `SKIP_VO=1 ./build.sh`.

Names and numbers (Maya, Youssef, Sara, 4 min, 38 %, Branch 4) are illustrative. Claude Code appears as "Built with
Claude Code" — check Anthropic's brand guidelines before publishing and avoid implying endorsement.

## Download

`promo/business/release/rasolv_business.mp4`
