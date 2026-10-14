# RASOLV "support receipt" short (vertical 4K, 43.5 s)

`RASOLV_Support_Receipt.mp4`: 2160×3840 (4K), 60 fps, H.264 High@5.2 two-pass at ~5.2 Mb/s + AAC 160 kbps,
−14 LUFS, 29.6 MB (SSIM 0.996 vs. the 4K render master). An explainer short in the "running invoice" format: a receipt
prints and keeps adding up what bad customer support costs you, a countdown pill promises "the fix · at the end", and
RASOLV clears the bill.

**Bad customer support is quietly *billing* you** (lock screen fills with support notifications, receipt starts
printing) → **the fix is at the end** (countdown pill) → **hold queue, 47 min** (call timer racing) → **chatbot loop**
→ **transferred ×3, explain it again** → **ticket: 3–5 business days** (days crossed off) → **refund still pending**
→ **PER PROBLEM** stamp → **a dozen problems a year → 7 weeks + $1,548** (problem grid lights up) → **So here's the fix**
(pill hits 0s) → **RASOLV app**: describe it once, AI signal chips, AI match 98% to Maya Haddad · Billing expert → **live
updates, solved in 4 minutes** → every receipt line struck out, **SOLVED**, total 4 min · $0 → aperture logo, wordmark,
"Vision that solves.", "Get help in minutes →".

Scenes alternate dark and light. The headline caption reveals word by word, and the keyword in each line gets an
orange selection box (marked with `*stars*` in `vo.py`).

Same pipeline as `../aw2candine/`: `vo.py` (Kokoro `af_heart` at 1.1×, "Rasolv" forced to *rah-ZOLV*, writes
`captions.js`, which drives the timeline), `index.html` (deterministic `render(t)`), `render.js` (Playwright → frames
→ ffmpeg), `score.py` (A-minor groove while the bill grows, a stop on "the fix", C-major groove for RASOLV, plus
printer/stamp/typing sound design and voice ducking), `build.sh`.

```bash
KOKORO_DIR=/path/to/kokoro ./build.sh   # full build
SKIP_VO=1 ./build.sh                     # reuse voiceover/captions (1080x1920)
SCALE=2 SKIP_VO=1 OUT=rasolv_receipt_4k_master ./build.sh   # 4K master (2160x3840)
```

Delivery file under 30 MB from the 4K master (two-pass):

```bash
cd out && M=rasolv_receipt_4k_master.mp4
X="-c:v libx264 -preset slower -b:v 5200k -maxrate 9000k -bufsize 18000k -profile:v high -level:v 5.2 -pix_fmt yuv420p -tune animation"
ffmpeg -y -i $M $X -pass 1 -an -f null /dev/null
ffmpeg -y -i $M $X -pass 2 -c:a aac -b:a 160k -movflags +faststart ../RASOLV_Support_Receipt.mp4
```

All the numbers (47 min, $129, 7 weeks, 98%, 4 min) and names are illustrative. Swap in real ones before publishing.
