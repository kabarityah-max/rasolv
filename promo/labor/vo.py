"""Generates the "Show Your Work" film voiceover with Kokoro (local open-weights TTS) and the word-timed captions.
TikTok cut: lines are laid end to end, and every line start is snapped up to the next eighth note of the drill beat
(BPM below), so the scene cuts in index.html land on the beat. index.html keys every scene off the line ids in
captions.js, so editing a line re-times everything. "Rasolv" is spoken rah-ZOLV (same phonemes as ../vo.py).
Writes out/vo/NN.wav, out/vo/lines.json (for score.py), captions.js (for index.html), out/rasolv_show_your_work.srt.
Usage: python3 vo.py <kokoro-v1.0.onnx> <voices-v1.0.bin> [voice] [speed]"""
import sys, json, os, re, math
import numpy as np, soundfile as sf

BPM = 142
GRID = 60 / BPM / 2   # eighth note
OPEN = 0.42           # one beat of drums before the first word
GAP = 0.12
BRAND = "ɹɑːzˈɑːlv"   # "rah-ZOLV", rhymes with "resolve"
# (id, pause before this line, caption text)
LINES = [
    ("hook",    0,    "This website made people wait."),
    ("liked",   0,    "And they liked it more."),
    ("harvard", 0.2,  "Harvard researchers built two flight searches."),
    ("instant", 0,    "One gave you results instantly."),
    ("slow",    0,    "The other made you wait."),
    ("but",     0,    "But it showed its work."),
    ("check",   0,    "Checking this airline. Then that one. Then the next."),
    ("same",    0,    "Same flights at the end."),
    ("rated",   0.15, "People rated the slow one higher."),
    ("minute",  0,    "Even when it took a full minute."),
    ("labor",   0.15, "It's called the labor illusion."),
    ("hate",    0.25, "People don't hate waiting."),
    ("blind",   0,    "They hate waiting blind."),
    ("video",   0.45, "This TikTok did the same thing."),
    ("steps",   0,    "Every step, on screen."),
    ("counter", 0,    "A counter that never stopped."),
    ("asked",   0,    "You never once asked how long it was."),
    ("rasolv",  0.4,  "That's how Rasolv works."),
    ("expert",  0,    "A real expert on your problem."),
    ("live",    0,    "Every step, live."),
    ("cta",     0.35, "Rasolv. Vision that solves."),
]
TAIL = 3.4      # end card after the last line


def syllables(w):
    w = re.sub(r"[^a-z]", "", w.lower())
    n = len(re.findall(r"[aeiouy]+", w)) - (1 if w.endswith("e") and not w.endswith("le") else 0)
    return max(1, n)


def word_times(audio, sr, words):
    """Return [(start, end)] per word, seconds relative to the clip start."""
    hop = int(sr * 0.01)
    rms = np.array([np.sqrt(np.mean(audio[i:i + hop] ** 2)) for i in range(0, len(audio) - hop, hop)])
    quiet = rms < max(0.004, rms.max() * 0.04)
    gaps, i = [], 0
    while i < len(quiet):  # internal silent runs of >= 60 ms
        if quiet[i]:
            j = i
            while j < len(quiet) and quiet[j]: j += 1
            if i > 0 and j < len(quiet) and j - i >= 6: gaps.append((i * 0.01, j * 0.01))
            i = j
        else: i += 1
    breaks = [k for k, w in enumerate(words[:-1]) if re.search(r"[.,;:!?]$", w)]
    total = len(audio) / sr
    gaps = [g for g in gaps if g[0] > 0.15 and g[1] < total - 0.2]     # ignore breaths at the clip edges
    # match each punctuation break to the pause nearest where the syllable count expects it
    cum = np.cumsum([syllables(w) + 0.6 for w in words]); cum /= cum[-1]
    chosen, kept = [], []
    for b in breaks:
        free = [g for g in gaps if g not in chosen and (not chosen or g[0] > chosen[-1][1])]
        if not free: continue
        g = min(free, key=lambda g: abs((g[0] + g[1]) / 2 - cum[b] * total))
        if abs((g[0] + g[1]) / 2 - cum[b] * total) > 0.2 * total: continue
        chosen.append(g); kept.append(b)
    gaps, breaks = chosen, kept
    bounds = [0.0] + [x for g in gaps for x in g] + [total]
    segs, s0 = [], 0
    for b in breaks + [len(words) - 1]:
        segs.append(list(range(s0, b + 1))); s0 = b + 1
    out = [None] * len(words)
    for si, idx in enumerate(segs):
        a, b = bounds[2 * si], bounds[2 * si + 1]
        wts = np.array([syllables(words[k]) + 0.6 for k in idx], float)
        edges = a + (b - a) * np.concatenate([[0], np.cumsum(wts) / wts.sum()])
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
    speed = float(sys.argv[4]) if len(sys.argv) > 4 else 1.1
    k, tok = Kokoro(model, voices), Tokenizer()
    os.makedirs("out/vo", exist_ok=True)
    meta, caps, srt, cue = [], [], [], {}
    t = OPEN
    for i, (lid, pause, text) in enumerate(LINES):
        ph = tok.phonemize(text, "en-us")
        if "Rasolv" in text:
            ph = re.sub(r"ɹ\S*s\S*lv", BRAND, ph); print("   phonemes:", ph)
        audio, sr = k.create(ph, voice=voice, speed=speed, is_phonemes=True)
        a = np.asarray(audio, dtype=np.float32)
        env = np.abs(a) > 0.01
        s = int(np.argmax(env)); e = len(a) - int(np.argmax(env[::-1]))
        a = a[max(0, s - int(0.02 * sr)): min(len(a), e + int(0.06 * sr))]
        sf.write(f"out/vo/{i:02d}.wav", a, sr)
        start = round(math.ceil((t + pause) / GRID - 1e-6) * GRID, 3)      # snap to the beat grid
        dur = len(a) / sr
        words = text.split()
        wt = word_times(a, sr, words)
        cue[lid] = [start, round(start + dur, 3), [round(start + w0, 3) for w0, _ in wt]]
        meta.append({"i": i, "id": lid, "start": start, "dur": round(dur, 3), "sr": sr, "text": text})
        caps.append({"id": lid, "start": start, "end": round(start + dur + 0.2, 3),
                     "words": [[w, round(start + a0, 3), round(start + a1, 3)] for w, (a0, a1) in zip(words, wt)]})
        srt.append(f"{i + 1}\n{srt_ts(start)} --> {srt_ts(start + dur + 0.2)}\n{text}\n")
        print(f"{i:2d} {lid:8s} {start:6.2f}+{dur:4.2f}  {text}")
        t = start + dur + GAP
    duration = round(math.ceil((t - GAP + TAIL) / (GRID * 2)) * GRID * 2, 3)
    json.dump({"voice": voice, "bpm": BPM, "duration": duration, "lines": meta}, open("out/vo/lines.json", "w"), indent=1)
    open("captions.js", "w").write("// generated by vo.py — word-timed captions + scene cues\n"
                                   f"window.DURATION = {duration};\nwindow.BPM = {BPM};\nwindow.CUE = {json.dumps(cue)};\n"
                                   f"window.CAPTIONS = {json.dumps(caps)};\n")
    open("out/rasolv_show_your_work.srt", "w").write("\n".join(srt))
    print("duration", duration)

main()
