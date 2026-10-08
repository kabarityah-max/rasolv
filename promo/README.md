# Resolve promo video

4K vertical (2160×3840, 60 fps, H.264 High@5.2 + 320 kbps AAC) UI motion promo for Resolve,
modelled on the "Uber"-style motion-graphics reel: keyword flashes → circle wipe → logo type-in
morphing into the app icon → category chips → issue picker → New Ticket card → Assigning Agent →
Ticket Resolved → rating → brand outro.

- `index.html` – the whole animation as a deterministic `render(t)` timeline. Open it in a browser to preview it looping.
- `render.js` – Playwright renders each frame at 2× device scale (4K) and pipes PNGs into ffmpeg.
- `sfx.py` – synthesises the soundtrack (pad, pulse, whooshes, clicks, chimes) synced to the timeline.
- `build.sh` – runs everything; output lands in `out/resolve_promo_4k.mp4`.

Edit copy/colours in `index.html` (`WORDS`, `LABELS`, `ENTRIES`, the card markup) and re-run `./build.sh`.
