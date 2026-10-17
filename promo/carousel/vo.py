"""Generates the "Carousel" film voiceover with Kokoro (local open-weights TTS) and the word-timed captions.
Lines are laid end to end: each starts GAP seconds (or its own pause) after the previous one ends, so the audio
sets the timeline. index.html keys every scene off the line ids in captions.js, so re-timing is automatic.
Word timings are estimated from the audio (silences matched to punctuation, words spread by syllable weight).
Writes out/vo/NN.wav, out/vo/lines.json (for score.py), captions.js (for index.html), out/rasolv_carousel.srt.
Usage: python3 vo.py <kokoro-v1.0.onnx> <voices-v1.0.bin> [voice] [speed]"""
import sys, json, os, re
import numpy as np, soundfile as sf

OPEN = 3.4      # silent cold open: a suitcase going round, no words
GAP = 0.32
# (id, pause before this line, caption text)
LINES = [
    ("you",      0,    "You're watching a suitcase go round."),
    ("houston",  0,    "At a Houston airport, passengers watched this every day."),
    ("complain", 0,    "And they complained."),
    ("long",     0,    "The wait at baggage claim was too long."),
    ("obvious",  0.5,  "So the airport did the obvious thing."),
    ("hire",     0,    "It hired more baggage handlers."),
    ("eight",    0,    "The wait fell to eight minutes,"),
    ("bench",    0,    "well within industry benchmarks."),
    ("still",    0.2,  "The complaints didn't stop."),
    ("closer",   0.5,  "So they looked closer."),
    ("walk1",    0,    "One minute walking from the gate."),
    ("stand7",   0,    "Seven minutes standing at the belt."),
    ("pct",      0,    "Almost ninety percent of the trip, doing nothing."),
    ("fix",      0.5,  "So they made the walk longer."),
    ("gates",    0,    "They moved the arrival gates away from the main terminal,"),
    ("outer",    0,    "and sent the bags to the outermost carousel."),
    ("six",      0,    "Passengers now walked six times longer."),
    ("zero",     0.2,  "Complaints dropped to near zero."),
    ("nobody",   0.4,  "Nobody sped up the bags."),
    ("hate",     0,    "People don't hate waiting."),
    ("stand",    0,    "They hate standing still."),
    ("video",    0.6,  "This video did the same thing."),
    ("open",     0,    "It opened on a suitcase going round."),
    ("nowords",  0,    "No words."),
    ("never",    0,    "Then it never stood still."),
    ("stayed",   0.2,  "You stayed."),
    ("bag",      0.6,  "So here's your bag."),
    ("which",    0.5,  "Which one gets you: the faster bags, or the longer walk?"),
]
TAIL = 5.6      # end card after the last line


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
    model, voices = sys.argv[1], sys.argv[2]
    voice = sys.argv[3] if len(sys.argv) > 3 else "am_michael"
    speed = float(sys.argv[4]) if len(sys.argv) > 4 else 0.98
    k = Kokoro(model, voices)
    os.makedirs("out/vo", exist_ok=True)
    meta, caps, srt, cue = [], [], [], {}
    t = OPEN
    for i, (lid, pause, text) in enumerate(LINES):
        audio, sr = k.create(text, voice=voice, speed=speed, lang="en-us")
        a = np.asarray(audio, dtype=np.float32)
        env = np.abs(a) > 0.01
        s = int(np.argmax(env)); e = len(a) - int(np.argmax(env[::-1]))
        a = a[max(0, s - int(0.02 * sr)): min(len(a), e + int(0.06 * sr))]
        sf.write(f"out/vo/{i:02d}.wav", a, sr)
        start = round(t + pause, 3)
        dur = len(a) / sr
        words = text.split()
        wt = word_times(a, sr, words)
        cue[lid] = [start, round(start + dur, 3), [round(start + w0, 3) for w0, _ in wt]]
        meta.append({"i": i, "id": lid, "start": start, "dur": round(dur, 3), "sr": sr, "text": text})
        caps.append({"id": lid, "start": start, "end": round(start + dur + 0.25, 3),
                     "words": [[w, round(start + a0, 3), round(start + a1, 3)] for w, (a0, a1) in zip(words, wt)]})
        srt.append(f"{i + 1}\n{srt_ts(start)} --> {srt_ts(start + dur + 0.2)}\n{text}\n")
        print(f"{i:2d} {lid:9s} {start:6.2f}+{dur:4.2f}  {text}")
        t = start + dur + GAP
    duration = round(t - GAP + TAIL, 2)
    json.dump({"voice": voice, "duration": duration, "lines": meta}, open("out/vo/lines.json", "w"), indent=1)
    open("captions.js", "w").write("// generated by vo.py — word-timed captions + scene cues\n"
                                   f"window.DURATION = {duration};\nwindow.CUE = {json.dumps(cue)};\n"
                                   f"window.CAPTIONS = {json.dumps(caps)};\n")
    open("out/rasolv_carousel.srt", "w").write("\n".join(srt))
    print("duration", duration)

main()
