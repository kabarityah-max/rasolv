"""Generates the RASOLV "support receipt" short's voiceover with Kokoro (local open-weights TTS) and word-timed captions.
Lines are laid back-to-back with a short gap, each start snapped to the 120 bpm half-beat grid so scene cuts land on the
music. Caption words wrapped in *stars* get the selection-box highlight in index.html.
Writes out/vo/NN.wav, out/vo/lines.json (for score.py), captions.js (for index.html), out/rasolv_receipt.srt.
Usage: python3 vo.py <kokoro-v1.0.onnx> <voices-v1.0.bin> [voice] [speed]"""
import sys, json, os, re, math
import numpy as np, soundfile as sf

# (scene id, gap before line in seconds, caption text, spoken text)
LINES = [
    ("hook",     0.40, "Bad customer support is quietly *billing* you.", None),
    ("intro",    0.25, "Let's add it up. The *fix* is at the end.", None),
    ("hold",     0.30, "First, the hold queue. *47* minutes of elevator music.", "First, the hold queue. Forty-seven minutes of elevator music."),
    ("bot",      0.25, "Then a chatbot that answers everything except *your* question.", None),
    ("transfer", 0.25, "Transferred. Explain it all again. And *again.*", None),
    ("ticket",   0.25, "Then a ticket: we'll reply in *3-5* business days.", "Then a ticket. We'll reply in three to five business days."),
    ("refund",   0.25, "And your refund? Still *pending.*", None),
    ("per",      0.30, "And that's not one bill. It's *per* problem.", "And that's not one bill. It's per... problem."),
    ("year",     0.25, "A dozen problems a year, and you've lost *weeks.*", None),
    ("fix",      0.35, "So here's the fix.", None),
    ("rasolv",   0.30, "Rasolv. Describe it once. *AI* sees the whole picture,", "Rasolv. Describe it once. A.I. sees the whole picture,"),
    ("match",    0.10, "and a real *expert* is on it in seconds.", None),
    ("solve",    0.25, "Live updates. Solved in *minutes.*", None),
    ("clear",    0.25, "Every line on that bill? *Gone.*", None),
    ("outro",    0.35, "Rasolv. Vision that solves.", None),
]
GRID = 0.25          # half a beat at 120 bpm
TAIL = 2.6           # logo hold after the last line
BRAND = "ɹɑːzˈɑːlv"   # "rah-ZOLV", rhymes with "resolve" — same phonemes as ../vo.py


def syllables(w):
    w = re.sub(r"[^a-z]", "", w.lower())
    n = len(re.findall(r"[aeiouy]+", w)) - (1 if w.endswith("e") and not w.endswith("le") else 0)
    return max(1, n)


def word_times(audio, sr, words):
    """[(start, end)] per word relative to the clip: punctuation breaks snap to the nearest real pause,
    words inside a phrase are spread by syllable weight (same method as ../cinema/vo.py)."""
    hop = int(sr * 0.01)
    rms = np.array([np.sqrt(np.mean(audio[i:i + hop] ** 2)) for i in range(0, len(audio) - hop, hop)])
    quiet = rms < max(0.004, rms.max() * 0.04)
    gaps, i = [], 0
    while i < len(quiet):
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
    from kokoro_onnx.tokenizer import Tokenizer
    model, voices = sys.argv[1], sys.argv[2]
    voice = sys.argv[3] if len(sys.argv) > 3 else "af_heart"
    speed = float(sys.argv[4]) if len(sys.argv) > 4 else 1.1
    k, tok = Kokoro(model, voices), Tokenizer()
    os.makedirs("out/vo", exist_ok=True)
    meta, caps, srt, t = [], [], [], 0.0
    for i, (scene, gap, text, spoken) in enumerate(LINES):
        plain = text.replace("*", "")
        ph = tok.phonemize(spoken or plain, "en-us").replace("ɹˈæsɑːlv", BRAND)
        audio, sr = k.create(ph, voice=voice, speed=speed, is_phonemes=True)
        a = np.asarray(audio, dtype=np.float32)
        env = np.abs(a) > 0.01
        s = int(np.argmax(env)); e = len(a) - int(np.argmax(env[::-1]))
        a = a[max(0, s - int(0.02 * sr)): min(len(a), e + int(0.06 * sr))]
        sf.write(f"out/vo/{i:02d}.wav", a, sr)
        start = math.ceil((t + gap) / GRID) * GRID
        dur = len(a) / sr
        raw = text.split()
        words = [w.replace("*", "") for w in raw]
        wt = word_times(a, sr, words)
        meta.append({"i": i, "scene": scene, "start": start, "dur": round(dur, 3), "sr": sr, "text": plain})
        caps.append({"scene": scene, "start": start, "end": round(start + dur + 0.3, 3),
                     "words": [[w, round(start + a0, 3), round(start + a1, 3), int(r.startswith("*"))]
                               for w, r, (a0, a1) in zip(words, raw, wt)]})
        srt.append(f"{i + 1}\n{srt_ts(start)} --> {srt_ts(start + dur + 0.2)}\n{plain}\n")
        print(f"{i:2d} {scene:8s} {start:6.2f}+{dur:4.2f}  {plain}")
        t = start + dur
    total = math.ceil((t + TAIL) / 0.5) * 0.5
    json.dump({"voice": voice, "speed": speed, "duration": total, "lines": meta}, open("out/vo/lines.json", "w"), indent=1)
    open("captions.js", "w").write("// generated by vo.py — word-timed captions + scene timeline\nwindow.CAPTIONS = "
                                   + json.dumps(caps) + ";\nwindow.DURATION = " + str(total) + ";\n")
    open("out/rasolv_receipt.srt", "w").write("\n".join(srt))
    print("duration", total)

main()
