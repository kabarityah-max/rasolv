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

## Script

| # | Time | Visual | Dialogue / on-screen |
|---|---|---|---|
| 1 | 0.0–3.0 | Black. A loud clock tick. A wait timer races `0:00:00 → 1:00:00`; beside it a loss ticker counts up: `−1 order`, `★☆☆☆☆`, `−1 customer`, `Refund requested`. Founder steps into the light. | **Founder (to camera):** "What does one hour of waiting cost your business?" |
| 2 | 3.0–6.0 | Quick insert: customer phone — `where is my order` → `HUMAN!!!` → `cancel my order`. | **Founder:** "Usually… this customer." |
| 3 | 6.0–10.0 | Split screen. Left: a generic business owner typing into an AI chat `make my customer service better pls` → a wall of bland bullet points. Right: a terminal snaps open beside the founder and Claude Code pops out. | **Founder:** "And you already have AI. So does everyone." **Claude Code:** "Most people ask me for bullet points." |
| 4 | 10.0–12.0 | Founder cracks his knuckles, steps up to the terminal. Super: **Same AI. Different hands.** | **Founder:** "We don't." |
| 5 | 12.0–17.0 | Wall of incoming messages floods the frame. Claude Code sorts them into lanes; chips light up: *Orders · Billing · Tech*, *Urgent*, *Frustrated*. | **Claude Code:** "Orders, billing, tech. Who's angry, who's urgent — sorted." |
| 6 | 17.0–21.0 | Orange routing lines snap to staff cards: "Maya · Billing expert", "Youssef · Orders". Card shows "Answer drafted ✓". Customer phone: LIVE, "Refund issued in 4 min", ★★★★★. | **Founder:** "A real expert on your team, answer ready." **Claude Code:** "Not one hour. Four minutes." |
| 7 | 21.0–25.0 | Insights card builds: "38% of complaints this week: late delivery — Branch 4". Lock closes over the dashboard. | **Founder:** "Plus *why* they're complaining — and your data stays yours." |
| 8 | 25.0–30.0 | Founder + Claude Code side by side. Aperture iris opens → RASOLV wordmark; small line under it: *Built with Claude Code*. | **Founder:** "Everyone has AI. Not everyone knows how to use it." **Claude Code:** "He does." Super: **RASOLV** · *Book a demo* |

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

Same deterministic pipeline as `../cinema/`: `index.html` `render(t)` timeline → `render.js` (Playwright →
frames → ffmpeg) → `score.py` (original score + SFX + VO ducking) → `vo.py` (Kokoro; two voices: founder,
Claude Code). Founder rendered as a stylised vector character drawn from the reference photo, with simple
mouth/blink/head-tilt rigs synced to the VO timings. Brand: orange `#FF6E05`, ink `#070707`, Rubik.
