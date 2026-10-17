"""Generates the RASOLV "made with one prompt" reel voiceover + word timings.
Kokoro (local open-weights TTS), voice af_heart, "Rasolv" forced to rah-ZOLV. Each line sits at START on the 120 BPM
timeline in index.html; vo.py asserts every line fits its slot. Word timings are estimated from the audio
(pauses snapped to punctuation, words spread by syllable weight — same method as ../bilingual/vo.py).
Writes out/vo/NN.wav, out/vo/lines.json (for score.py), captions.js (for index.html), out/rasolv_reel.srt.
Usage: python3 vo.py <kokoro-v1.0.onnx> <voices-v1.0.bin> [voice] [speed]"""
import sys, json, os, re
import numpy as np, soundfile as sf

# (start, caption text, spoken text or None)
LINES = [
    (0.10,  "Nobody animated this video.", None),
    (1.80,  "No After Effects. No keyframes. No motion designer.", None),
    (5.50,  "Kinetic type.", None),          # montage: one label per 1 s card
    (6.50,  "3D camera.", "Three D camera."),
    (7.50,  "Particles.", None),
    (8.50,  "Morphs.", None),
    (9.50,  "Data.", None),
    (10.50, "Glitch.", None),
    (12.00, "So... how was this made?", None),
    (17.00, "One prompt. In Claude Code.", None),
    (18.90, "It wrote the animation, the music, this voice... and rendered every frame.", None),
    (23.00, "This is how motion graphics get made now.", None),
    (25.50, "Want the exact prompt? Comment PROMPT, and we'll DM it to you.", "Want the exact prompt? Comment, prompt, and we'll DM it to you."),
    (29.30, "Follow RASOLV for more.", "Follow Rasolv for more."),
]
DURATION = 31.5
BRAND = "ɹɑːzˈɑːlv"   # "rah-ZOLV", rhymes with "resolve" — same phonemes as ../vo.py
PUNCT = r"[.,;:!?…]$"


def syllables(w):
    w = re.sub(r"[^a-z]", "", w.lower())
    n = len(re.findall(r"[aeiouy]+", w)) - (1 if w.endswith("e") and not w.endswith("le") else 0)
    return max(1, n)


def word_times(audio, sr, words):
    """[(start, end)] per word relative to the clip: punctuation breaks snap to the nearest real pause,
    words inside a phrase are spread by syllable weight (same method as ../bilingual/vo.py)."""
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
    wts = np.array([syllables(w) + 0.6 + (1.5 if re.search(PUNCT, w) else 0) for w in words], float)
    cum = np.concatenate([[0], np.cumsum(wts)]) / wts.sum() * total
    breaks, bounds, last = [], [0.0], 0.0
    for k, w in enumerate(words[:-1]):
        if not re.search(PUNCT, w): continue
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


def trim(a, sr):
    env = np.abs(a) > 0.01
    s = int(np.argmax(env)); e = len(a) - int(np.argmax(env[::-1]))
    return a[max(0, s - int(0.02 * sr)): min(len(a), e + int(0.06 * sr))]


def main():
    from kokoro_onnx import Kokoro
    from kokoro_onnx.tokenizer import Tokenizer
    model, voices = sys.argv[1], sys.argv[2]
    voice = sys.argv[3] if len(sys.argv) > 3 else "af_heart"
    speed = float(sys.argv[4]) if len(sys.argv) > 4 else 1.1
    k, tok = Kokoro(model, voices), Tokenizer()
    os.makedirs("out/vo", exist_ok=True)
    meta, caps, srt = [], [], []
    for i, (start, text, spoken) in enumerate(LINES):
        ph = tok.phonemize(spoken or text, "en-us").replace("ɹˈæsɑːlv", BRAND)
        audio, sr = k.create(ph, voice=voice, speed=speed, is_phonemes=True)
        a = trim(np.asarray(audio, dtype=np.float32), sr)
        sf.write(f"out/vo/{i:02d}.wav", a, sr)
        words = text.split()
        wt = word_times(a, sr, words)
        dur = len(a) / sr
        end = LINES[i + 1][0] if i + 1 < len(LINES) else DURATION
        assert start + dur < end - 0.1, f"line {i} ({dur:.2f}s) overruns the next line at {end}"
        meta.append({"i": i, "start": start, "dur": round(dur, 3), "sr": sr, "text": text})
        caps.append({"start": start, "end": round(start + dur, 3), "text": text,
                     "words": [[w, round(start + a0, 3), round(start + a1, 3)] for w, (a0, a1) in zip(words, wt)]})
        srt.append(f"{i + 1}\n{srt_ts(start)} --> {srt_ts(start + dur + 0.2)}\n{text}\n")
        print(f"{i:2d} {start:6.2f}+{dur:4.2f} (slot {end - start:4.2f})  {text}")
    json.dump({"voice": voice, "speed": speed, "duration": DURATION, "lines": meta}, open("out/vo/lines.json", "w"), indent=1)
    open("captions.js", "w").write("// generated by vo.py — word-timed voiceover lines\nwindow.CAPTIONS = "
                                   + json.dumps(caps) + ";\nwindow.DURATION = " + str(DURATION) + ";\n")
    open("out/rasolv_reel.srt", "w").write("\n".join(srt))

main()
