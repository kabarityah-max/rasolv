"""Generates the voiceover lines with Kokoro (local, open-weights TTS).
Usage: python3 vo.py <model.onnx> <voices.bin> [voice]   -> vo/line*.wav + vo/durations.json"""
import json, sys, os
import soundfile as sf
from kokoro_onnx import Kokoro
from kokoro_onnx.tokenizer import Tokenizer

LINES = [
    "Something broke. And you need it fixed... now.",
    "With Rasolv, a real expert is already on it.",
    "Live updates. Real people. Answers in minutes.",
    "Support that actually solves.",
    "One app. Every answer.",
    "Your data stays yours.",
    "Rasolv. Vision that solves.",
]
BRAND = "ɹɑːzˈɑːlv"   # "rah-ZOLV", rhymes with "resolve"

model, voices = sys.argv[1], sys.argv[2]
voice = sys.argv[3] if len(sys.argv) > 3 else "af_heart"
k, tok = Kokoro(model, voices), Tokenizer()
here = os.path.dirname(os.path.abspath(__file__))
out, durs = os.path.join(here, "vo"), []
os.makedirs(out, exist_ok=True)
for i, line in enumerate(LINES):
    ph = tok.phonemize(line, "en-us").replace("ɹˈæsɑːlv", BRAND)
    audio, sr = k.create(ph, voice=voice, speed=1.0, is_phonemes=True)
    sf.write(os.path.join(out, f"line{i}.wav"), audio, sr)
    durs.append(round(len(audio) / sr, 3))
    print(i, durs[-1], ph)
json.dump({"voice": voice, "sr": sr, "durations": durs, "lines": LINES}, open(os.path.join(out, "durations.json"), "w"), indent=1)
