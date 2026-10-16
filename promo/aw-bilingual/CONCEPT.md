# A&W Tanger — "Two combos. Two languages. One team." (EN + AR staff video concept)

Same DNA as `../aw2candine/` (1080×1920, 60 fps, dark cinematic, real food photos, kinetic type, whip cuts,
120 bpm score, word-highlighted captions), rebuilt as a **bilingual duet**: every beat is said in English,
then echoed in Arabic, and the screen *flips* between the two.

## The idea: THE FLIP

Each headline lives on a card. English slams in on the downbeat, exactly like v3. On the next downbeat the
card whips 180° around its vertical axis (a half-beat, with a light sweep and a riq/shaker hit) and the Arabic
side faces camera: text flows right-to-left, the orange accent bar jumps from the left edge to the right edge,
pills and stamps mirror sides. The food photo behind keeps moving, so the flip feels like turning a menu
board, not a cut. Two voices, never overlapping: the English voice we already have (`af_bella`) and an Arabic
voice answering her. Price, photos and the "2 Can Dine" lockup stay shared, so the rhythm is
**photo → EN card → flip → AR card → whip to next scene**.

Captions sit in two stacked rows (EN above, AR below, same width). The row being spoken does the
word-by-word highlight; the other row dims to 50%. Both languages are therefore always on screen, so a
staff member who only reads one of them never loses the thread.

Runtime: about 42–45 s (v3 was ~22 s). Each scene gets 2 bars EN + flip + 2 bars AR.

## Script (caption text · spoken text)

| # | scene | English | Arabic (MSA, plural imperative for the team) |
|---|---|---|---|
| 1 | hook | **2 Can Dine.** Two combos, just $17.99. | **2 Can Dine.** وجبتان كومبو بـ 17.99$ فقط. |
| 2 | ask | Say it to every guest: is someone joining you today? | قولوها لكل ضيف: هل سينضم إليك أحد اليوم؟ |
| 3 | one | Ordering one combo? Make it two. | يطلب كومبو واحداً؟ اجعلوها اثنين. |
| 4 | same | Ring it right. Same protein? Use the coupon. | سجّلوها صح. نفس البروتين؟ استخدموا الكوبون. |
| 5 | mixed | Beef and chicken mixed? Manual override. In-store only. | لحم ودجاج معاً؟ تعديل يدوي. داخل المطعم فقط. |
| 6 | addons | Then add one more. Onion rings. Small gravy. Apple turnover. Or upsize the drink. | ثم أضيفوا واحداً: حلقات البصل. مرق صغير. فطيرة التفاح. أو كبّروا المشروب. |
| 7 | outro | Mention it. Add one. Ring it right. Let's go, team! | اذكروها. أضيفوا واحداً. سجّلوها صح. يلا يا فريق! |

Spoken Arabic overrides (for the TTS, like the `spoken` column in `vo.py`):
- "2 Can Dine" → «تو كان داين» (keep the promo name in English).
- "A&W" → «إيه آند دبليو».
- "17.99$" → «سبعةَ عشرَ دولاراً وتسعةٍ وتسعين سنتاً» (or the shorter «سبعتعش وتسعة وتسعين» if the team prefers a
  colloquial voice).
- «يلا» is colloquial on purpose: it is the natural energy of "Let's go!" and every Arabic speaker reads it.

Big on-screen Arabic headlines (short, like the EN "Ring it right" / "Make it two"):
hook «وجبتان بـ 17.99$» · ask «قولوها لكل ضيف» · one «اجعلوها اثنين» with the ×2 badge · same «سجّلوها صح» ·
mixed stamps «تعديل يدوي» / «داخل المطعم فقط» · addons «أضيفوا واحداً» · outro «يلا يا فريق!».

## Two more ways to cut it (same code, a build flag)

1. **Separate language versions** (`LANG=en` / `LANG=ar`, ~25 s each). The Arabic render is fully mirrored
   (RTL layout, accents on the right) with small English captions underneath; the English render is v3 with
   small Arabic captions. Best for WhatsApp staff groups where 25 s is the attention budget.
2. **Mirror split** (one render, ~25 s). The frame splits on a diagonal: English top-left, Arabic bottom-right,
   both animating in sync, one voice alternating per scene. Striking, but denser to read; a good alternate for
   the back-of-house screen.

Recommendation: build the Flip as the hero (one file for the whole team, memorable gimmick) and ship the two
separate versions from the same timeline for chat groups.

## Production notes (what changes vs. v3)

- **Arabic voice.** Kokoro has no Arabic. Use `edge-tts` (free): `ar-LB-LaylaNeural` (warm female, pairs
  well with `af_bella`) or `ar-SA-HamedNeural` (male, makes the duet contrast obvious). edge-tts emits
  WordBoundary events, so Arabic caption timing comes straight from the engine instead of the English
  syllable heuristic in `word_times()`. Higgsfield `generate_audio` is the alternative if a premium voice is
  wanted.
- **Font.** The bundled `../fonts/Rubik.woff2` is Latin-only (checked: 0 Arabic glyphs). Download the full
  Rubik from Google Fonts, which includes Arabic at weights 300–900 and keeps the brand look exactly.
  Fallback pairing: Cairo or Tajawal ExtraBold for headlines.
- **RTL typography.** `dir="rtl"` on Arabic elements, `letter-spacing: 0` (negative tracking breaks the
  joined letters), no uppercase transform, line-height ~1.15 because Arabic ascenders and descenders are
  taller, and Western digits throughout (17.99) for a Canadian audience.
- **Timeline.** Keep the 0.25 s grid. `vo.py` lays lines as EN, AR, EN, AR with the flip occupying the gap;
  `captions.js` carries a `lang` field per line so `index.html` can mirror the layout and the score can place
  the shaker hit on every flip.
- **Review.** Have a native Arabic-speaking team member read the table once before synthesis; the one
  judgment call is MSA (neutral, chosen here) versus a Levantine or Moroccan colloquial voice.
