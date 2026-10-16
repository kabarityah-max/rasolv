# RASOLV — "One picture. Two languages." (Arabic + English brand film concept)

Same world as `../cinema/` (dark cinematic, orange light beams building the aperture, glass sphere, AI signal
chips, expert hand-off, ring hits, RGB-glitch logo, original score) and the same pipeline (`vo.py` →
`captions.js`, deterministic `index.html`, Playwright → ffmpeg, `score.py`). Rebuilt so that Arabic and English
are not a translation of each other but two halves of one film.

Formats: 9:16 (1080×1920, Reels / TikTok / Shorts) as the primary, and 16:9 4K from the same timeline for
YouTube and LinkedIn. Runtime about 48 s.

## The idea

**The voice switches language by act, never by line.** Four acts, alternating English → Arabic → English →
Arabic, so a viewer never hears the same sentence twice and the film keeps the pace of the cinema cut. Whatever
language is being *spoken*, the other language is the *headline*: the giant kinetic type on screen is always
the language you are not hearing. Both languages are therefore on screen and in your ear in every act, and a
viewer who speaks only one of them follows the whole story.

**The signature: Arabic that writes itself in light.** English headlines type in with the hard, mechanical
cut-ins we already use. Arabic headlines are drawn by the same orange light pen that builds the aperture logo:
the stroke travels right-to-left and the letters join as they are drawn (SVG stroke animation on outlined
text), ending in a bloom. It uses the film's existing light-beam language, so the two scripts feel like one
system. The aperture iris spins clockwise in English acts and counter-clockwise in Arabic acts, and the phone
UI is genuinely right-to-left in Arabic acts (mirrored layout, Arabic labels), not just translated.

**The finale is bilingual on purpose.** The three ring hits land in both languages, alternating voices on
the beat, and the end card carries both wordmarks.

Captions run in two stacked rows (EN above, AR below) throughout; the spoken row does the word highlight,
the other sits at 50%.

## Script

| t (s) | act / voice | English | Arabic (MSA) |
|---|---|---|---|
| 0.5 | 1 · EN voice | What if getting help wasn't a waiting game... | ماذا لو لم يكن طلب المساعدة انتظاراً… |
| 4.4 | 1 · EN voice | ...but one tap away? | …بل نقرة واحدة؟ |
| 9.0 | 2 · AR voice | Meet RASOLV. AI that sees the whole picture. | تعرّف على رازولف. ذكاء اصطناعي يرى الصورة كاملة. |
| 14.3 | 2 · AR voice | It reads your problem in seconds. Intent, sentiment, history, urgency. | يقرأ مشكلتك في ثوانٍ. النية، المشاعر، السجل، الإلحاح. |
| 20.0 | 3 · EN voice | Then hands it to the right expert, with the answer ready. | ثم يسلّمها للخبير المناسب، والإجابة جاهزة. |
| 25.2 | 3 · EN voice | So nothing slips. And no one waits. | فلا شيء يضيع. ولا أحد ينتظر. |
| 29.5 | 4 · AR voice | One app. Every answer. And your data stays yours. | تطبيق واحد. كل الإجابات. وبياناتك تبقى لك. |
| 35.5 | finale · EN | See it. | شوف. |
| 37.1 | finale · AR | Decide it. | قرّر. |
| 38.7 | finale · EN | Solve it. | حُلّ. |
| 44.0 | finale · both | RASOLV. Vision that solves. | رازولف. رؤية تحُلّ. |

Act 1 headline (drawn in light while the EN voice speaks): «على بُعد نقرة» ("one tap away").
Act 2 headline (typed in while the AR voice speaks): **SEES THE WHOLE PICTURE**; sphere chips bilingual:
Intent / النية · Sentiment / المشاعر · History / السجل · Urgency / الإلحاح.
Act 3 hand-off card: **Maya Haddad · Billing expert / خبيرة الفواتير**, AI match 98%, «تم رد المبلغ خلال 4 دقائق»
under "Refund issued in 4 min".
Act 4 headline: **ONE APP. EVERY ANSWER.** with «بياناتك تبقى لك» drawn in light beneath.
Finale: ring hit 1 "SEE IT." + «شوف», hit 2 "DECIDE IT." + «قرّر», hit 3 "SOLVE IT." + «حُلّ», then the glitch
logo and a double wordmark: RASOLV above, «رازولف» below, tagline line "Vision that solves · رؤية تحُلّ".

Spoken overrides for the Arabic TTS:
- RASOLV → «رازولْف» (rah-ZOLV, matching the English phoneme override).
- "AI" → «ذكاء اصطناعي» (never the letters).
- «شوف» is colloquial on purpose; it is pan-dialect and punchier than MSA «انظر». Swap to «انظر» if the brand
  voice should stay strictly formal.
- Numbers stay Western digits (98%, 4 min) in both languages.

## Alternate cut from the same code

`LANG=en` / `LANG=ar` builds: one voice language for the whole film, the other language only in the caption
row, with the Arabic build fully mirrored (RTL layout, RTL phone UI). Same bilingual finale in both. Use these
when a platform audience is known to be single-language (an Arabic-only ad set, an English LinkedIn post).
Recommendation: the alternating film is the hero; ship the two single-voice builds alongside it.

## Production notes (what changes vs. `../cinema/`)

- **Arabic voice.** Kokoro has no Arabic. Use `edge-tts` (free): `ar-SA-HamedNeural` (male, warm, strong
  contrast with the English `af_heart`) or `ar-LB-LaylaNeural` (female). edge-tts emits WordBoundary events,
  so Arabic caption timing comes from the engine, not the English syllable heuristic in `word_times()`.
  Higgsfield `generate_audio` is the premium option.
- **Font.** `../fonts/Rubik.woff2` is Latin-only (0 Arabic glyphs). The full Rubik from Google Fonts includes
  Arabic at 300–900 and keeps the brand look exactly; the light-pen effect needs the Arabic headline outlined
  to SVG paths (opentype.js at build time) so the stroke can be animated.
- **RTL typography.** `dir="rtl"`, `letter-spacing: 0` for Arabic (negative tracking breaks the joined
  letters; the English wordmark keeps its spacing), no uppercase transform, line-height ~1.15, Arabic
  kashida-free so the drawn strokes stay clean.
- **Timeline.** `vo.py` gains a `lang` per line; `index.html` reads it to pick iris direction, headline
  language and LTR/RTL UI; `score.py` places a reversed-cymbal swell on each language switch.
- **Review.** A native Arabic speaker reads the table once before synthesis. The two judgment calls are
  «شوف» vs «انظر» and whether the brand name is shown in Arabic script on the end card at all.
