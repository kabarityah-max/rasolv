# RASOLV for Business — "What does one hour of waiting cost?"

30 s ad aimed at business owners. The founder (animated, from `founder-reference.png`) and the RASOLV
AI agent present it as a double act. Vertical 1080×1920 master (Reels / TikTok / Stories), 16:9 cut-down
for LinkedIn / YouTube.

**Promise:** your customers get a human in minutes; you get the whole picture.

## Characters

- **Founder (you)** — stylised semi-real animated version of the reference photo: buzz cut, short beard,
  navy textured blazer over a white tee, steady brown eyes. Calm, direct, slightly dry. Speaks to camera.
- **The Agent** — RASOLV's own AI, not a third-party brand. A floating orange (`#FF6E05`) aperture orb
  whose iris opens/narrows as it "talks"; text chips spin out of it. Quick, confident, a little cheeky.

Example business: a restaurant chain (ties in with existing A&W Tanger work). Swap for e-commerce /
telecom by changing the message texts only.

## Script

| # | Time | Visual | Dialogue / on-screen |
|---|---|---|---|
| 1 | 0.0–3.0 | Black. A loud clock tick. A wait timer races `0:00:00 → 1:00:00`; beside it a loss ticker counts up: `−1 order`, `★☆☆☆☆`, `−1 customer`, `Refund requested`. Founder steps into the light. | **Founder (to camera):** "What does one hour of waiting cost your business?" |
| 2 | 3.0–6.0 | Quick insert: customer phone — `where is my order` → `HUMAN!!!` → `cancel my order`. Agent orb pops in beside the founder with an iris snap; the timer freezes. | **Founder:** "Usually… this customer." **Agent:** "Not on my watch." **Founder:** "Show them." |
| 3 | 6.0–11.0 | Wall of incoming messages floods the frame. Agent sorts them into lanes; chips light up: *Orders · Billing · Tech*, *Urgent*, *Frustrated*. | **Agent:** "Orders, billing, tech. I read every message — who's angry, who's urgent." |
| 4 | 11.0–15.0 | Orange routing lines snap to staff cards: "Maya · Billing expert", "Youssef · Orders". Card shows "Answer drafted ✓". | **Founder:** "Then it hands off to a real expert on your team — answer already drafted." |
| 5 | 15.0–19.0 | Back to the customer phone: LIVE badge, "Refund issued in 4 min", ★★★★★. | **Agent:** "Not one hour. Four minutes. And your team never starts from zero." |
| 6 | 19.0–24.0 | Insights card builds: "38% of complaints this week: late delivery — Branch 4". Founder taps it. | **Founder:** "And it tells you *why* they're complaining — before it costs you." |
| 7 | 24.0–27.0 | Lock closes over the dashboard. | **Agent:** "Your data stays yours." |
| 8 | 27.0–30.0 | Founder + Agent side by side; aperture iris opens → RASOLV wordmark. | **Founder:** "RASOLV. Your customers get a human. You get the whole picture." Super: *Book a demo* |

## Alternate hooks (A/B test the first 3 s)

1. "What does one hour of waiting cost your business?" (chosen)
2. "Every time a customer types 'HUMAN!!!', you're about to lose them."
3. "Your customers aren't angry about the problem. They're angry about the wait."
4. "You have 312 unanswered messages. We have zero."

## To confirm before publishing

- [ ] Product claims: AI triage by intent/urgency, drafted answers, live updates, complaint insights by
      branch, data privacy — keep only what RASOLV actually ships.
- [ ] Numbers (4 min, 38%, 312) and names (Maya, Youssef) are illustrative — replace with real ones.
- [ ] CTA: "Book a demo" vs. a URL / QR.
- [ ] Founder voice: own recording (recommended) or generated.

## Production plan

Same deterministic pipeline as `../cinema/`: `index.html` `render(t)` timeline → `render.js` (Playwright →
frames → ffmpeg) → `score.py` (original score + SFX + VO ducking) → `vo.py` (Kokoro; two voices: founder,
agent). Founder rendered as a stylised vector character drawn from the reference photo, with simple
mouth/blink/head-tilt rigs synced to the VO timings. Brand: orange `#FF6E05`, ink `#070707`, Rubik.
