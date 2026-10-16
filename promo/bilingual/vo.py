"""Generates the bilingual (English + Arabic) RASOLV film voiceover and the word-timed captions.
English lines: Kokoro (local open-weights TTS, voice af_heart, "Rasolv" forced to rah-ZOLV).
Arabic lines:  Piper "ar_JO-kareem-medium" through sherpa-onnx (local open weights). The spoken text carries
full tashkeel so the phonemizer gets the vowels right; the caption shows the plain text.
Each line is placed at START[i] on the cinema timeline (same scene timing as ../cinema). Word timings are
estimated from the audio (pauses snapped to punctuation, words spread by syllable weight).
Writes out/vo/NN.wav, out/vo/lines.json (for score.py), captions.js (for index.html), out/rasolv_bilingual.srt.
Usage: python3 vo.py <kokoro-v1.0.onnx> <voices-v1.0.bin> <piper-ar-model-dir> [en_voice] [ar_speed]"""
import sys, json, os, re
import numpy as np, soundfile as sf

# (start, lang, caption text, spoken text or None, translation shown on screen in the other language)
LINES = [
    (0.5,  "en", "What if getting help wasn't a waiting game...", None,
                 "ماذا لو لم يكن طلب المساعدة انتظاراً…"),
    (4.4,  "en", "...but one tap away?", None,
                 "…بل نقرة واحدة؟"),
    (8.9,  "ar", "تعرّف على رازولف. ذكاء يرى الصورة كاملة.", "تَعَرَّفْ عَلَى رَازُولْف. ذَكَاءٌ يَرَى الصُّورَةَ كَامِلَةً.",
                 "Meet RASOLV. AI that sees the whole picture."),
    (13.9, "ar", "يقرأ مشكلتك في ثوانٍ. النية، المشاعر، السجل، الإلحاح.", "يَقْرَأُ مُشْكِلَتَكَ فِي ثَوَانٍ. النِّيَّة، المَشَاعِر، السِّجِلّ، الإِلْحَاح.",
                 "It reads your problem in seconds. Intent, sentiment, history, urgency."),
    (19.6, "en", "Then hands it to the right expert, with the answer ready.", None,
                 "ثم يسلّمها للخبير المناسب، والإجابة جاهزة."),
    (24.8, "en", "So nothing slips. And no one waits.", None,
                 "فلا شيء يضيع. ولا أحد ينتظر."),
    (28.3, "ar", "تطبيق واحد. كل الإجابات. وبياناتك تبقى لك.", "تَطْبِيقٌ وَاحِد. كُلُّ الإِجَابَات. وَبَيَانَاتُكَ تَبْقَى لَك.",
                 "One app. Every answer. And your data stays yours."),
    (33.0, "en", "See it.", None, "شوف."),
    (34.6, "ar", "قرّر.", "قَرِّرْ.", "Decide it."),
    (36.2, "en", "Solve it.", None, "حُلّ."),
    (41.7, "en", "RASOLV. Vision that solves.", "Rasolv. Vision that solves.", "رازولف. رؤية تحُلّ."),
    (44.3, "ar", "رازولف. رؤية تحُلّ.", "رَازُولْف. رُؤْيَةٌ تَحُلّ.", "RASOLV. Vision that solves."),
]
DURATION = 47.5
BRAND = "ɹɑːzˈɑːlv"   # "rah-ZOLV", rhymes with "resolve" — same phonemes as ../vo.py
PUNCT = r"[.,;:!?،؛؟…]$"
AR_DIAC = re.compile(r"[ً-ْٰ]")


def syllables(w):
    if re.search(r"[؀-ۿ]", w):
        letters = re.sub(r"[^ء-ي]", "", w)
        return max(1, round(len(letters) / 2.2))
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
    import sherpa_onnx
    model, voices, ar_dir = sys.argv[1], sys.argv[2], sys.argv[3]
    en_voice = sys.argv[4] if len(sys.argv) > 4 else "af_heart"
    ar_speed = float(sys.argv[5]) if len(sys.argv) > 5 else 1.18
    k, tok = Kokoro(model, voices), Tokenizer()
    ar_model = next(f for f in os.listdir(ar_dir) if f.endswith(".onnx"))
    ar = sherpa_onnx.OfflineTts(sherpa_onnx.OfflineTtsConfig(model=sherpa_onnx.OfflineTtsModelConfig(
        vits=sherpa_onnx.OfflineTtsVitsModelConfig(model=f"{ar_dir}/{ar_model}", tokens=f"{ar_dir}/tokens.txt",
                                                   data_dir=f"{ar_dir}/espeak-ng-data"), num_threads=4)))
    os.makedirs("out/vo", exist_ok=True)
    meta, caps, srt = [], [], []
    for i, (start, lang, text, spoken, tr) in enumerate(LINES):
        if lang == "en":
            ph = tok.phonemize(spoken or text, "en-us").replace("ɹˈæsɑːlv", BRAND)
            audio, sr = k.create(ph, voice=en_voice, speed=1.0, is_phonemes=True)
            a = np.asarray(audio, dtype=np.float32)
        else:
            g = ar.generate(spoken or text, sid=0, speed=ar_speed)
            a, sr = np.asarray(g.samples, dtype=np.float32), g.sample_rate
        a = trim(a, sr)
        sf.write(f"out/vo/{i:02d}.wav", a, sr)
        words = text.split()
        wt = word_times(a, sr, words)
        dur = len(a) / sr
        end = LINES[i + 1][0] if i + 1 < len(LINES) else DURATION
        assert start + dur < end - 0.15, f"line {i} ({dur:.2f}s) overruns the next line at {end}"
        meta.append({"i": i, "lang": lang, "start": start, "dur": round(dur, 3), "sr": sr, "text": text})
        caps.append({"lang": lang, "start": start, "end": round(start + dur + 0.35, 3), "tr": tr,
                     "words": [[w, round(start + a0, 3), round(start + a1, 3)] for w, (a0, a1) in zip(words, wt)]})
        srt.append(f"{i + 1}\n{srt_ts(start)} --> {srt_ts(start + dur + 0.2)}\n{text}\n{tr}\n")
        print(f"{i} {lang} {start:6.2f}+{dur:4.2f} (slot {end - start:4.2f})  {text}")
    json.dump({"en_voice": en_voice, "ar_speed": ar_speed, "duration": DURATION, "lines": meta}, open("out/vo/lines.json", "w"), indent=1, ensure_ascii=False)
    open("captions.js", "w").write("// generated by vo.py — word-timed bilingual captions\nwindow.CAPTIONS = "
                                   + json.dumps(caps, ensure_ascii=False) + ";\nwindow.DURATION = " + str(DURATION) + ";\n")
    open("out/rasolv_bilingual.srt", "w").write("\n".join(srt))

main()
