"""Voiceover for the RASOLV "on hold" story (same format as the "five bricks" parable reel): Kokoro TTS, calm male
narrator, lines laid back-to-back with per-line pauses, word timings estimated from the audio for the caption pill.
Writes out/vo/NN.wav, out/vo/lines.json (for score.py), captions.js (for index.html), out/rasolv_hold.srt.
Usage: python3 vo.py <kokoro-v1.0.onnx> <voices-v1.0.bin> [voice] [speed]"""
import sys, json, os, re
import numpy as np, soundfile as sf

# (scene id, pause before the line in seconds, caption text, spoken text override)
LINES = [
    ("open",  4.0,  "You're on hold.", None),
    ("tune",  0.8,  "That tune has a birthday.", None),
    ("year",  0.9,  "Nineteen sixty-two.", None),
    ("levy",  0.6,  "Alfred Levy runs a factory. And his phones have a problem.", None),
    ("wire",  0.7,  "A loose wire is touching a steel beam.", None),
    ("ant",   0.6,  "The whole building becomes a radio antenna.", None),
    ("hear",  0.6,  "So anyone put on hold... hears a radio station.", "So anyone put on hold, hears a radio station."),
    ("stop",  0.7,  "And they stop hanging up.", None),
    ("less",  0.8,  "Nobody waited less. They just stopped noticing.", None),
    ("pat",   0.7,  "Levy patents it. Music on hold.", None),
    ("now",   0.8,  "Sixty years later, it plays on every support line on earth.", None),
    ("what",  0.9,  "What did it fix?", None),
    ("noth",  1.0,  "Nothing.", None),
    ("trick", 0.8,  "The trick: fill the silence. People stay to be polite.", "The trick? Fill the silence. People stay to be polite."),
    ("then",  0.9,  "Then, the second trick.", None),
    ("imp",   0.6,  "A voice. “Your call is important to us.”", "A voice. Your call is important to us."),
    ("every", 0.6,  "Said to everyone. By no one.", None),
    ("means", 0.8,  "Important just means: keep waiting.", "Important just means, keep waiting."),
    ("pair",  0.9,  "A tune nobody chose. A line nobody means.", None),
    ("same",  0.9,  "This video opened the same way. Four seconds of hold music. No words.", None),
    ("stay",  0.8,  "You stayed.", None),
    ("exit",  1.0,  "So here's your exit.", None),
    ("ras",   0.7,  "Rasolv doesn't put you on hold.", None),
    ("exp",   0.5,  "A real expert is already on it. Live updates. Answers in minutes.", None),
    ("which", 0.9,  "Which one gets you? The tune... or the answer?", "Which one gets you? The tune, or the answer?"),
    ("logo",  0.9,  "Rasolv. Vision that solves.", None),
]
BRAND = "ɹɑːzˈɑːlv"   # "rah-ZOLV", rhymes with "resolve" — same phonemes as ../vo.py
TAIL = 3.0           # logo hold after the last line


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
    wts = np.array([syllables(w) + 0.6 + (1.5 if re.search(r"[.,;:!?…”]$", w) else 0) for w in words], float)
    cum = np.concatenate([[0], np.cumsum(wts)]) / wts.sum() * total
    breaks, bounds, last = [], [0.0], 0.0
    for k, w in enumerate(words[:-1]):
        if not re.search(r"[.,;:!?…”]$", w): continue
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
    voice = sys.argv[3] if len(sys.argv) > 3 else "am_michael"
    speed = float(sys.argv[4]) if len(sys.argv) > 4 else 0.97
    k, tok = Kokoro(model, voices), Tokenizer()
    os.makedirs("out/vo", exist_ok=True)
    meta, caps, srt, t = [], [], [], 0.0
    for i, (scene, gap, text, spoken) in enumerate(LINES):
        ph = tok.phonemize(spoken or text, "en-us").replace("ɹˈæsɑːlv", BRAND).replace("ɹˈæsɑlv", BRAND)
        audio, sr = k.create(ph, voice=voice, speed=speed, is_phonemes=True)
        a = np.asarray(audio, dtype=np.float32)
        env = np.abs(a) > 0.01
        s = int(np.argmax(env)); e = len(a) - int(np.argmax(env[::-1]))
        a = a[max(0, s - int(0.02 * sr)): min(len(a), e + int(0.06 * sr))]
        sf.write(f"out/vo/{i:02d}.wav", a, sr)
        start = round(t + gap, 2)
        dur = len(a) / sr
        words = text.split()
        wt = word_times(a, sr, words)
        meta.append({"i": i, "scene": scene, "start": start, "dur": round(dur, 3), "sr": sr, "text": text})
        caps.append({"scene": scene, "start": start, "end": round(start + dur + 0.45, 3),
                     "words": [[w, round(start + a0, 3), round(start + a1, 3)] for w, (a0, a1) in zip(words, wt)]})
        srt.append(f"{i + 1}\n{srt_ts(start)} --> {srt_ts(start + dur + 0.2)}\n{text}\n")
        print(f"{i:2d} {scene:6s} {start:6.2f}+{dur:4.2f}  {text}   /{ph}/")
        t = start + dur
    total = round(t + TAIL, 2)
    json.dump({"voice": voice, "speed": speed, "duration": total, "lines": meta}, open("out/vo/lines.json", "w"), indent=1)
    open("captions.js", "w").write("// generated by vo.py — word-timed captions + scene timeline\nwindow.CAPTIONS = "
                                   + json.dumps(caps, ensure_ascii=False) + ";\nwindow.DURATION = " + str(total) + ";\n")
    open("out/rasolv_hold.srt", "w").write("\n".join(srt))
    print("duration", total)

main()
