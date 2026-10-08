# RASOLV film (4K, voiceover + captions)

38-second 16:9 product film for RASOLV, built in the style of the ClickUp-type UI motion reels:
**Messy → Emails. Chats. Tickets. → scattered tools → "makes it all make sense" → 3D Smart Inbox
(triage, priority sort, auto-routing) → first message to full resolution → AI orbit (drafts / patterns /
learning) → stats → logo lockup → search-bar end card.**

Output: 3840×2160, 60 fps, H.264 High, AAC 320 kbps, loudness-normalised to −14 LUFS. Captions are burned
in (word-by-word highlight) and also written as a sidecar `out/rasolv_film.srt`.

| file | what it does |
|---|---|
| `vo.py` | Voiceover script + synthesis with [Kokoro](https://github.com/thewh1teagle/kokoro-onnx) (local, open weights, voice `af_heart`). Places every line on the timeline, estimates word timings from the audio and writes `captions.js` + the `.srt`. |
| `index.html` | The whole film as a deterministic `render(t)` timeline (open it in a browser to preview). |
| `render.js` | Playwright renders 1920×1080 CSS at 2× device scale → 4K frames → ffmpeg. `--stills <dir> t1,t2` for previews. |
| `score.py` | Original score (100 bpm, F major) + synced sound design, mixes the VO with sidechain ducking. |
| `build.sh` | Runs everything → `out/rasolv_film_4k.mp4`. |

```bash
KOKORO_DIR=/path/to/kokoro ./build.sh        # full build (voice + video + audio)
SKIP_VO=1 ./build.sh                          # reuse existing voiceover/captions
VOICE=am_michael KOKORO_DIR=... ./build.sh    # different Kokoro voice
```

To change narration, edit `LINES` in `vo.py` (start time, caption text, optional spoken text; "Rasolv"
is forced to *rah-ZOLV* via the `BRAND` phonemes, matching `../vo.py`). The scene timings in `index.html` and cues in `score.py` are keyed to those start times.
The numbers shown in the film (4m resolution, 98% CSAT, 24 tickets) are illustrative placeholders.
