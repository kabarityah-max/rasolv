"""Generates the "Two clocks" teaser voiceover (Kokoro, local open-weights TTS; "Rasolv" forced to rah-ZOLV).
Each line is placed at its START on the timeline; vo.py asserts every line ends before the next one starts.
Writes out/vo/NN.wav, out/vo/lines.json (for score.py) and out/rasolv_twoclocks.srt.
Usage: python3 vo.py <kokoro-v1.0.onnx> <voices-v1.0.bin> [voice] [speed]"""
import sys, json, os
import numpy as np, soundfile as sf

# (start, caption, spoken text or None, speed factor) — beats follow the 30 s script, one line per scene.
# The read is low and calm; only the two lines with the tightest slots (the black card and the close) are nudged quicker.
LINES = [
    (0.2,   "Two clocks. Same refund. Only one finishes.", None, 1.0),
    (3.4,   "Rasolv reads the problem in seconds.", None, 1.0),
    (8.3,   "Then a real person takes it. Maya, in billing.", None, 1.0),
    (15.25, "Four minutes. Done.", None, 1.0),
    (19.2,  "Over here? Forty minutes. And still no word.", None, 1.0),
    (23.2,  "Stop waiting. Someone real is already on it.", None, 1.15),
    (26.0,  "One picture. Two languages. Our film drops Thursday, 8pm.", None, 1.2),
]
DURATION = 30.0
BRAND = "ɹɑːzˈɑːlv"   # "rah-ZOLV", rhymes with "resolve" — same phonemes as ../vo.py


def srt_ts(t):
    ms = int(round(t * 1000)); h, ms = divmod(ms, 3600000); m, ms = divmod(ms, 60000); s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def trim(a, sr):
    env = np.abs(a) > 0.01
    s = int(np.argmax(env)); e = len(a) - int(np.argmax(env[::-1]))
    return a[max(0, s - int(0.02 * sr)): min(len(a), e + int(0.06 * sr))]


def say(k, tok, text, voice, speed):
    ph = tok.phonemize(text, "en-us").replace("ɹˈæsɑːlv", BRAND)
    audio, sr = k.create(ph, voice=voice, speed=speed, is_phonemes=True)
    return trim(np.asarray(audio, dtype=np.float32), sr), sr


def main():
    from kokoro_onnx import Kokoro
    from kokoro_onnx.tokenizer import Tokenizer
    voice = sys.argv[3] if len(sys.argv) > 3 else "af_heart"
    speed = float(sys.argv[4]) if len(sys.argv) > 4 else 0.97
    k, tok = Kokoro(sys.argv[1], sys.argv[2]), Tokenizer()
    os.makedirs("out/vo", exist_ok=True)
    meta, srt = [], []
    for i, (start, text, spoken, sp) in enumerate(LINES):
        a, sr = say(k, tok, spoken or text, voice, speed * sp)
        sf.write(f"out/vo/{i:02d}.wav", a, sr)
        dur = len(a) / sr
        end = LINES[i + 1][0] if i + 1 < len(LINES) else DURATION
        assert start + dur < end - 0.1, f"line {i} ({dur:.2f}s) overruns {end}"
        meta.append({"i": i, "start": start, "dur": round(dur, 3), "sr": sr, "text": text})
        srt.append(f"{i + 1}\n{srt_ts(start)} --> {srt_ts(start + dur + 0.2)}\n{text}\n")
        print(f"{i} {start:6.2f}+{dur:4.2f} (slot {end - start:4.2f})  {text}")
    json.dump({"voice": voice, "speed": speed, "duration": DURATION, "lines": meta}, open("out/vo/lines.json", "w"), indent=1)
    open("out/rasolv_twoclocks.srt", "w").write("\n".join(srt))

main()
