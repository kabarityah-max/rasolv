# RASOLV for Business — "What does one hour of waiting cost?"

30 s ad aimed at business owners. The founder (animated, from `founder-reference.png`) and Claude Code
present it as a double act. Vertical 1080×1920 master (Reels / TikTok / Stories), 16:9 cut-down
for LinkedIn / YouTube.

**Promise:** everyone has AI — not everyone knows how to use it. RASOLV does: we turn Claude Code into
fast, human support for your business, better than your competitors (or you) would on your own.

**Edge (the line the whole ad builds to):** *Same AI. Different hands.*

## Characters

- **Founder (you)** — stylised semi-real animated version of the reference photo: buzz cut, short beard,
  navy textured blazer over a white tee, steady brown eyes. Calm, direct, slightly dry. Speaks to camera.
- **Claude Code** — the AI co-host, because Claude Code is what the RASOLV team builds with. Shown as
  the Claude Code terminal coming alive: a small orange pixel character living in a dark terminal window,
  with replies typing out in monospace as it speaks. Quick, confident, a little cheeky.
  *Brand note:* frame it as "Built with Claude Code" (true) — avoid wording or visuals that suggest
  Anthropic endorses or partners with RASOLV, and check Anthropic's brand guidelines before publishing.

Example business: a restaurant chain (ties in with existing A&W Tanger work). Swap for e-commerce /
telecom by changing the message texts only.

## Look & pace

- **Cinematic:** shallow depth of field, anamorphic orange flares, film grain, motion blur, ink-black
  shadows with a single orange (`#FF6E05`) key light. Low angles and slow push-ins on the founder; macro
  ECUs on screens, thumbs, digits.
- **Fast:** cut on the beat. 128 BPM → 1 beat = 0.47 s, 1 bar = 1.875 s, 16 bars = 30 s. ~30 shots, none
  longer than 2 bars except the hero shot. Whip pans, speed ramps, smash cuts, glitch transitions.
- **Sound arc:** clock tick (cold) → heartbeat riser → hard silence → **beat drop on the tagline** →
  driving montage → sub-bass hit + silence on the logo.
- **Lines are short.** Nobody speaks more than ~8 words at a time; VO rides over the cuts.

## Shot list

| Bars | Time | Shot | Sound / dialogue |
|---|---|---|---|
| **ACT 1 — THE COST** | | | |
| 1 | 0.0–1.9 | ECU second hand ticking · smash cut ECU wait timer digits blurring `0:00:00 → 1:00:00` · micro-cuts on each tick: `−1 order` / `★☆☆☆☆` / cart empties / shop door swings shut | Tick… tick… **Founder (VO, low):** "What does one hour of waiting…" |
| 2 | 1.9–3.8 | Dark. Orange key light snaps on — ECU founder's eyes open, slow push-in | **Founder:** "…cost your business?" |
| 3 | 3.8–5.6 | Macro: a thumb hammering `HUMAN!!!` `HUMAN!!!` — handheld shake, each tap a hit · glitch · `cancel my order` → send-whoosh | Heartbeat riser |
| 4 | 5.6–7.5 | Hard silence. Founder in silhouette, half-lit | **Founder:** "Usually… this customer." |
| **ACT 2 — THE EDGE** | | | |
| 5 | 7.5–9.4 | Whip pan → owner at a laptop typing `make my business better pls` · speed-ramp on an endless scroll of bland AI bullet points | **Founder:** "Everyone has AI." |
| 6 | 9.4–11.3 | Whip pan back → terminal snaps open in the dark, Claude Code pops out, cursor blinking | **Claude Code:** "Most people ask me for bullet points." |
| 7 | 11.3–13.1 | Low-angle dolly-in: founder steps into frame, cracks knuckles, orange flare across lens | **Founder:** "We don't." — riser cuts dead |
| 8 | 13.1 | **DROP.** Super slams full-frame: **SAME AI. DIFFERENT HANDS.** | Beat drop + impact |
| **ACT 3 — WHAT WE DO FOR YOU** (cut every beat) | | | |
| 8–9 | 13.1–16.9 | Messages flood toward camera · Claude Code slices them into lanes · chips slam on, one per beat: `ORDERS` `BILLING` `URGENT` `FRUSTRATED` | **Claude Code:** "Sorted. Who's angry. Who's urgent." |
| 10 | 16.9–18.8 | Orange routing lines whip across frame → staff cards snap: `Maya · Billing`, `Youssef · Orders` · macro hands typing · `Answer drafted ✓` | **Founder:** "Straight to a real expert." |
| 11 | 18.8–20.6 | Customer phone: `LIVE` pulse → `Refund issued in 4 min` → five stars stamp on, one per beat | **Claude Code:** "Not one hour." *(stutter cut)* "Four minutes." |
| 12 | 20.6–22.5 | Rack focus onto insights card: `38% of complaints: late delivery — Branch 4`, Branch 4 flares orange | **Founder:** "Know *why* they complain." |
| 13 | 22.5–24.4 | Steel lock clamps shut over the dashboard — metallic hit | **Claude Code:** "Your data stays yours." |
| **ACT 4 — HERO** | | | |
| 14–15 | 24.4–28.1 | Slow-mo after a hit: founder + Claude Code side by side, backlit orange, low angle, 180° orbit, sparks/dust in the light | **Founder:** "Everyone has AI. Not everyone knows how to use it." **Claude Code:** "He does." |
| 16 | 28.1–30.0 | Aperture iris opens → **RASOLV** wordmark · small: *Built with Claude Code* · *Book a demo* | Sub-bass hit → silence |

## Alternate hooks (A/B test the first 3 s)

1. "What does one hour of waiting cost your business?" (chosen)
2. "Every time a customer types 'HUMAN!!!', you're about to lose them."
3. "Your customers aren't angry about the problem. They're angry about the wait."
4. "You have 312 unanswered messages. We have zero."
5. "Everyone has AI. Not everyone knows how to use it." (also works as a cold open)

## To confirm before publishing

- [ ] Product claims: AI triage by intent/urgency, drafted answers, live updates, complaint insights by
      branch, data privacy — keep only what RASOLV actually ships.
- [ ] Numbers (4 min, 38%, 312) and names (Maya, Youssef) are illustrative — replace with real ones.
- [ ] CTA: "Book a demo" vs. a URL / QR.
- [ ] Founder voice: own recording (recommended) or generated.

## Production plan

Cinematic build (recommended): AI-generated live shots of the founder (Higgsfield, from the reference
photo) for the face/hero shots, with the screens, chips, terminal and type composited in code.

Code-only fallback: same deterministic pipeline as `../cinema/`: `index.html` `render(t)` timeline → `render.js` (Playwright →
frames → ffmpeg) → `score.py` (original score + SFX + VO ducking) → `vo.py` (Kokoro; two voices: founder,
Claude Code). Founder rendered as a stylised vector character drawn from the reference photo, with simple
mouth/blink/head-tilt rigs synced to the VO timings. Brand: orange `#FF6E05`, ink `#070707`, Rubik.
