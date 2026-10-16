# RASOLV bilingual film — English + Arabic (4K, voiceover in both languages + captions)

47.5-second 16:9 dark cinematic brand film, built from `../cinema/` with one rule added: **the voice alternates
language by act (EN → AR → EN → AR), and the headline on screen is always the language you are not hearing.**
Both languages are therefore on screen and in your ear in every act.

**Hook (EN voice)** — the Arabic line «ماذا لو لم يكن طلب المساعدة انتظاراً… بل نقرة واحدة؟» writes itself in
orange light, word by word, right-to-left → **Meet RASOLV (AR voice)** — beams build the aperture, English
"AI that sees the whole picture" → **Sphere + signal chips (AR voice)** — bilingual chips (intent · النية …)
light up as the Arabic words are spoken → **Hand-off (EN voice)** — Maya Haddad · Billing expert · خبيرة الفواتير,
AI match 98%, LIVE updates · تحديثات مباشرة, Refund issued in 4 min · رد المبلغ خلال 4 دقائق → ring «ولا أحد ينتظر.»
→ **Promise (AR voice)** — "One app. Every answer. Your data stays yours." + bilingual categories → **Beats** —
"See it." / «شوف.», «قرّر.» / "Decide.", "Solve it." / «حُلّ.» with the giant ring hit → RGB-glitch logo →
**RASOLV · VISION THAT SOLVES**, answered by **رازولف · رؤية تحُلّ**.

Captions: the spoken language with word highlight, the other language in a smaller row beneath (dropped where
that line is already the headline). Sidecar `out/rasolv_bilingual.srt` carries both languages.

| file | what it does |
|---|---|
| `vo.py` | Script in both languages. English lines: Kokoro `af_heart` ("Rasolv" forced to *rah-ZOLV*). Arabic lines: Piper `ar_JO-kareem-medium` via sherpa-onnx, spoken text fully vowelled (tashkeel) for clean pronunciation, captions plain. Writes `captions.js` (word timings + translations) and the `.srt`. |
| `index.html` | The film as a deterministic `render(t)` timeline. Chip hot-times and the "your data" beat are read from the Arabic word timings in `captions.js`. |
| `render.js` | Playwright → frames → ffmpeg (`SCALE=2` 4K, `SCALE=1` Full HD). `--stills <dir> t1,t2` for previews. |
| `score.py` | The cinema score (D minor, 112.5 bpm) extended to 47.5 s with a second wordmark hit for the Arabic lockup and risers on each language switch; VO mixed with sidechain ducking. |
| `build.sh` | Runs everything → `out/rasolv_bilingual_4k.mp4`. |

```bash
KOKORO_DIR=/path/to/kokoro ARTTS_DIR=/path/to/vits-piper-ar_JO-kareem-medium ./build.sh   # full build
SKIP_VO=1 ./build.sh                                   # reuse voiceover/captions
SKIP_VO=1 SCALE=1 FPS=30 OUT=draft ./build.sh          # fast Full HD draft
AR_SPEED=1.1 ... ./build.sh                            # slower Arabic voice (lines must still fit their slots; vo.py asserts)
```

Models: Kokoro from github.com/thewh1teagle/kokoro-onnx (releases, model-files-v1.0); the Arabic voice from
github.com/k2-fsa/sherpa-onnx (releases, `tts-models/vits-piper-ar_JO-kareem-medium.tar.bz2`).
`pip install kokoro-onnx sherpa-onnx soundfile scipy`. The Arabic font is Rubik's Arabic subset from Google
Fonts (`../fonts/Rubik-Arabic.woff2`); Arabic text never gets letter-spacing (it breaks the joined letters).

The Arabic voice is an open-weights medium-quality model (Jordanian-accented MSA). To swap in a premium voice,
drop replacement WAVs over `out/vo/02,03,06,08,11.wav` and rerun with `SKIP_VO=1` (timings come from the audio).
Names and numbers (Maya Haddad, 98%, 4 min) are illustrative, as in `../cinema/`.
