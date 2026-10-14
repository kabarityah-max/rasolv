"""Two-voice dialogue for the RASOLV for Business ad (founder + Claude Code), via Kokoro (local open-weights TTS).
Each line is synthesised separately and placed at its start time on the 128 BPM timeline.
Writes out/vo/NN.wav, out/vo/lines.json (for score.py) and captions.js (word-timed captions + per-line mouth
envelopes at 60 Hz for the founder's lip sync) and out/rasolv_business.srt.
Usage: python3 vo.py <kokoro-v1.0.onnx> <voices-v1.0.bin>"""
import sys, json, os, re
import numpy as np, soundfile as sf

VOICES = {'F': ('am_onyx', 1.0), 'C': ('af_heart', 1.06)}   # founder, Claude Code

# (start, speaker, caption text, spoken text)
LINES = [
    (0.75,  'F', "What does one hour of waiting cost your business?", None),
    (5.75,  'F', "Usually… this customer.", "Usually... this customer."),
    (7.65,  'F', "Everyone has AI.", "Everyone has A.I."),
    (9.55,  'C', "Most people ask me for bullet points.", None),
    (11.75, 'F', "We don't.", None),
    (14.15, 'C', "Sorted. Who's angry. Who's urgent.", None),
    (16.95, 'F', "Straight to a real expert.", None),
    (18.80, 'C', "Not one hour.", None),
    (19.75, 'C', "Four minutes.", None),
    (20.75, 'F', "Know why they complain.", None),
    (22.60, 'C', "Your data stays yours.", None),
    (24.45, 'F', "Everyone has AI. Not everyone knows how to use it.", "Everyone has A.I. Not everyone knows how to use it."),
    (27.55, 'C', "He does.", None),
]

# ---- word-timing helpers (same as ../cinema/vo.py) ----
def syllables(w):
    w = re.sub(r"[^a-z]", "", w.lower())
    n = len(re.findall(r"[aeiouy]+", w)) - (1 if w.endswith("e") and not w.endswith("le") else 0)
    return max(1, n)


def word_times(audio, sr, words):
    """Return [(start, end)] per word, seconds relative to the clip start. Each punctuation break is snapped
    to the real pause nearest to where syllable counts predict it; words inside a phrase are spread by syllables."""
    hop = int(sr * 0.01)
    rms = np.array([np.sqrt(np.mean(audio[i:i + hop] ** 2)) for i in range(0, len(audio) - hop, hop)])
    quiet = rms < max(0.004, rms.max() * 0.04)
    gaps, i = [], 0
    while i < len(quiet):  # internal silent runs of >= 30 ms
        if quiet[i]:
            j = i
            while j < len(quiet) and quiet[j]: j += 1
            if i > 0 and j < len(quiet) and j - i >= 3: gaps.append((i * 0.01, j * 0.01))
            i = j
        else: i += 1
    total = len(audio) / sr
    wts = np.array([syllables(w) + 0.6 + (1.5 if re.search(r"[.,;:!?]$", w) else 0) for w in words], float)
    cum = np.concatenate([[0], np.cumsum(wts)]) / wts.sum() * total
    breaks, bounds, last = [], [0.0], 0.0
    for k, w in enumerate(words[:-1]):
        if not re.search(r"[.,;:!?]$", w): continue
        exp = cum[k + 1]
        cands = [g for g in gaps if g[0] > last + 0.08 and abs((g[0] + g[1]) / 2 - exp) < 0.45]
        if not cands: continue
        g = min(cands, key=lambda g: abs((g[0] + g[1]) / 2 - exp) - 0.4 * (g[1] - g[0]))
        breaks.append(k); bounds += [g[0], g[1]]; last = g[1]
    bounds.append(total)
    segs, s0 = [], 0
    for b in breaks + [len(words) - 1]:
        segs.append(list(range(s0, b + 1))); s0 = b + 1
    out = [None] * len(words)
    for si, idx in enumerate(segs):
        a, b = bounds[2 * si], bounds[2 * si + 1]
        ww = np.array([syllables(words[k]) + 0.6 for k in idx], float)
        edges = a + (b - a) * np.concatenate([[0], np.cumsum(ww) / ww.sum()])
        for n, k in enumerate(idx): out[k] = (float(edges[n]), float(edges[n + 1]))
    return out


def srt_ts(t):
    ms = int(round(t * 1000)); h, ms = divmod(ms, 3600000); m, ms = divmod(ms, 60000); s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"



def main():
    from kokoro_onnx import Kokoro
    k = Kokoro(sys.argv[1], sys.argv[2])
    os.makedirs("out/vo", exist_ok=True)
    meta, caps, srt = [], [], []
    for i, (start, who, text, spoken) in enumerate(LINES):
        voice, speed = VOICES[who]
        audio, sr = k.create(spoken or text, voice=voice, speed=speed, lang="en-us")
        a = np.asarray(audio, dtype=np.float32)
        env = np.abs(a) > 0.01
        s = int(np.argmax(env)); e = len(a) - int(np.argmax(env[::-1]))
        a = a[max(0, s - int(0.02 * sr)): min(len(a), e + int(0.06 * sr))]
        sf.write(f"out/vo/{i:02d}.wav", a, sr)
        dur = len(a) / sr
        nxt = [L[0] for L in LINES[i + 1:]]
        if nxt and start + dur > nxt[0] - 0.05: print(f"!! line {i} ({dur:.2f}s) overruns the next line")
        words = text.split()
        wt = word_times(a, sr, words)
        hop = sr // 60
        mouth = [float(np.sqrt(np.mean(a[j:j + hop] ** 2))) for j in range(0, len(a), hop)]
        mx = max(mouth) or 1
        meta.append({"i": i, "start": start, "dur": round(dur, 3), "sr": sr, "who": who, "text": text})
        caps.append({"start": start, "end": round(start + dur + 0.3, 3), "who": who,
                     "mouth": [round(min(1, m / mx * 1.3), 2) for m in mouth],
                     "words": [[w, round(start + a0, 3), round(start + a1, 3)] for w, (a0, a1) in zip(words, wt)]})
        srt.append(f"{i + 1}\n{srt_ts(start)} --> {srt_ts(start + dur + 0.2)}\n{'Founder' if who == 'F' else 'Claude Code'}: {text}\n")
        print(f"{i:2d} {who} {start:6.2f}+{dur:4.2f} → {start + dur:6.2f}  {text}")
    json.dump({"lines": meta}, open("out/vo/lines.json", "w"), indent=1)
    open("captions.js", "w").write("// generated by vo.py — word-timed captions + mouth envelopes\nwindow.CAPTIONS = " + json.dumps(caps) + ";\n")
    open("out/rasolv_business.srt", "w").write("\n".join(srt))


main()
