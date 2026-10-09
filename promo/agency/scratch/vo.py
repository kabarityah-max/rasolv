"""Generates the RASOLV cinematic film voiceover with Kokoro (local open-weights TTS) and the word-timed captions.
Each line is synthesised separately and placed at START[i] on the timeline. Word timings are estimated
from the audio itself: the longest internal silences are matched to the punctuation breaks, then words
inside each phrase are spread by syllable weight.
Writes out/vo/NN.wav, out/vo/lines.json (for score.py), captions.js (for index.html), out/rasolv_cinema.srt.
Usage: python3 vo.py <kokoro-v1.0.onnx> <voices-v1.0.bin> [voice]"""
import sys, json, os, re
import numpy as np, soundfile as sf

# (start time on the timeline, caption text, spoken text)
LINES = [(0.35, 'This entire video? Built by Claude Code.', None),
    (3.87, 'Every frame, written as code. Rendered with HyperFrames.', 'Every frame, written as code. Rendered with Hyper Frames.'),
    (7.62, 'With our agency, RASOLV, we can do the same for you.', 'With our agency, Rasolv, we can do the same for you.'),
    (11.37, 'Motion graphics that never sit still.', None),
    (13.245, 'Liquid glass, in real time.', None),
    (15.12, 'Maps that fly to your customers.', None),
    (18.87, 'Your product, in 3D. Spinning on the beat.', 'Your product, in three D. Spinning on the beat.'),
    (22.62, 'Live data. Orbiting. Counting. Alive.', None),
    (26.37, 'Training films. Launch films. Brand stories.', None),
    (30.12, 'Voiceover, music and captions. All generated.', None),
    (33.87, 'Every cut lands on the beat.', None),
    (37.62, 'Then five critics tear it apart.', None),
    (41.37, 'Under seventy-five? Rejected.', None),
    (45.12, 'Brief in. Video out. Hours, not weeks.', None),
    (48.87, "Wherever your customers are, we're one tap away.", None),
    (54.375, "RASOLV. Vision that solves. Let's build yours.", "Rasolv. Vision that solves. Let's build yours.")]
BRAND = "ɹɑːzˈɑːlv"   # "rah-ZOLV", rhymes with "resolve" — same phonemes as ../vo.py


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
    from kokoro_onnx.tokenizer import Tokenizer
    model, voices = sys.argv[1], sys.argv[2]
    voice = sys.argv[3] if len(sys.argv) > 3 else "af_heart"
    k, tok = Kokoro(model, voices), Tokenizer()
    os.makedirs("vo", exist_ok=True)
    meta, caps, srt = [], [], []
    for i, (start, text, spoken) in enumerate(LINES):
        ph = tok.phonemize(spoken or text, "en-us").replace("ɹˈæsɑːlv", BRAND)
        audio, sr = k.create(ph, voice=voice, speed=float(os.environ.get("SPEED","1.12")), is_phonemes=True)
        a = np.asarray(audio, dtype=np.float32)
        env = np.abs(a) > 0.01
        s = int(np.argmax(env)); e = len(a) - int(np.argmax(env[::-1]))
        a = a[max(0, s - int(0.02 * sr)): min(len(a), e + int(0.06 * sr))]
        sf.write(f"vo/{i:02d}.wav", a, sr)
        words = text.split()
        wt = word_times(a, sr, words)
        dur = len(a) / sr
        end = LINES[i + 1][0] if i + 1 < len(LINES) else start + dur + 1
        assert start + dur < end + 0.25, f"line {i} ({dur:.2f}s) overruns the next line"
        meta.append({"i": i, "start": start, "dur": round(dur, 3), "sr": sr, "text": text})
        caps.append({"start": start, "end": round(start + dur + 0.35, 3),
                     "words": [[w, round(start + a0, 3), round(start + a1, 3)] for w, (a0, a1) in zip(words, wt)]})
        srt.append(f"{i + 1}\n{srt_ts(start)} --> {srt_ts(start + dur + 0.2)}\n{text}\n")
        print(f"{i} {start:6.2f}+{dur:4.2f}  {text}  /{ph}/")
    json.dump({"voice": voice, "lines": meta}, open("scratch/lines.json", "w"), indent=1)
    open("assets/captions.js", "w").write("// generated by vo.py — word-timed captions\nwindow.CAPTIONS = " + json.dumps(caps) + ";\n")
    open("scratch/agency.srt", "w").write("\n".join(srt))

main()
