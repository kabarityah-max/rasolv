# RASOLV for Business — "Don't lose them at HUMAN!!!"

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
| 1 | 0.0–3.0 | Customer phone, thumb typing: `where is my order` → `HUMAN!!!` → `AGENT!!!` → `cancel my order`. Hard cut to founder. | **Founder:** "Every time a customer types this… you're about to lose them." |
| 2 | 3.0–6.0 | Agent orb pops in beside him with an iris snap. | **Agent:** "Not on my watch." **Founder:** "Show them." |
| 3 | 6.0–11.0 | Wall of incoming messages floods the frame. Agent sorts them into lanes; chips light up: *Orders · Billing · Tech*, *Urgent*, *Frustrated*. | **Agent:** "Orders, billing, tech. I read every message — who's angry, who's urgent." |
| 4 | 11.0–15.0 | Orange routing lines snap to staff cards: "Maya · Billing expert", "Youssef · Orders". Card shows "Answer drafted ✓". | **Founder:** "Then it hands off to a real expert on your team — answer already drafted." |
| 5 | 15.0–19.0 | Back to the customer phone: LIVE badge, "Refund issued in 4 min", ★★★★★. | **Agent:** "Your customer never waits. Your team never starts from zero." |
| 6 | 19.0–24.0 | Insights card builds: "38% of complaints this week: late delivery — Branch 4". Founder taps it. | **Founder:** "And it tells you *why* they're complaining — before it costs you." |
| 7 | 24.0–27.0 | Lock closes over the dashboard. | **Agent:** "Your data stays yours." |
| 8 | 27.0–30.0 | Founder + Agent side by side; aperture iris opens → RASOLV wordmark. | **Founder:** "RASOLV. Your customers get a human. You get the whole picture." Super: *Book a demo* |

## Alternate hooks (A/B test the first 3 s)

1. "Every time a customer types 'HUMAN!!!', you're about to lose them." (default)
2. "Your customers aren't angry about the problem. They're angry about the wait."
3. "You have 312 unanswered messages. We have zero."
4. "What does one hour of waiting cost your business?"

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
