"""Synthesises the "Show Your Work" soundtrack in the same style as ../carousel/score.py — a sparse, slow pad score
(F minor, one chord per ~6.4 s) with a soft plucked motif on each act, plus quiet sound design (a tick for every
airline checked, soft result pops, a clock while the blind pawn waits, step chimes in the app, whooshes on scene
changes, a riser into the twist, a low hit on the logo) — and mixes in the voiceover (out/vo/NN.wav per
out/vo/lines.json) with sidechain ducking. Fully synthesised, royalty-free. Usage: python3 score.py out/mix.wav"""
import sys, json, wave
import numpy as np
import soundfile as sf
from scipy.signal import resample_poly

SR = 48000
META = json.load(open("out/vo/lines.json"))
DUR = META["duration"]
N = int(SR * DUR)
C = {l["id"]: (l["start"], l["start"] + l["dur"]) for l in META["lines"]}
S = lambda i: C[i][0]
E = lambda i: C[i][1]
rng = np.random.default_rng(5)
tt = np.arange(N) / SR


class Bus:
    def __init__(self): self.L = np.zeros(N); self.R = np.zeros(N)

    def add(self, sig, t, gain=1.0, pan=0.0):
        i = int(round(t * SR))
        if i >= N: return
        if i < 0: sig = sig[-i:]; i = 0
        sig = sig[: N - i]
        self.L[i:i + len(sig)] += sig * gain * np.sqrt(0.5 * (1 - pan))
        self.R[i:i + len(sig)] += sig * gain * np.sqrt(0.5 * (1 + pan))


music, sfx, voice = Bus(), Bus(), Bus()


def env(n, a, d):
    t = np.arange(n) / SR
    return np.minimum(t / max(a, 1e-4), 1) * np.exp(-t / d)


def band(x, lo=None, hi=None):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR); g = np.ones_like(f)
    if hi: g *= 1 / (1 + (f / hi) ** 4)
    if lo: g *= 1 / (1 + (lo / np.maximum(f, 1e-3)) ** 4)
    return np.fft.irfft(X * g, len(x))


def reverb(x, seconds=2.8, damp=4000):
    n = int(SR * seconds); t = np.arange(n) / SR
    ir = band(rng.normal(0, 1, n) * np.exp(-t / (seconds / 6.5)), hi=damp); ir[: int(SR * .015)] = 0
    ir /= np.sqrt(np.sum(ir ** 2))
    m = 1 << (len(x) + n - 1).bit_length()
    return np.fft.irfft(np.fft.rfft(x, m) * np.fft.rfft(ir, m), m)[: len(x)]


def hz(semi): return 440 * 2 ** ((semi - 69) / 12)   # midi → Hz


def hz(semi): return 440 * 2 ** ((semi - 69) / 12)   # midi → Hz


# ---------- score: slow pad, F minor → Db → Ab → Eb, one chord per 6.4 s ----------
CHORDS = [[41, 53, 56, 60, 65], [37, 49, 56, 60, 65], [44, 56, 60, 63, 68], [39, 51, 55, 58, 63]]
BAR = 6.4
pad = np.zeros(N)
for k in range(int(DUR / BAR) + 1):
    ch = CHORDS[k % 4]; t0 = k * BAR; n = int(SR * (BAR + 2.5)); t = np.arange(n) / SR
    e = np.minimum(t / 1.6, 1) * np.clip((BAR + 2.5 - t) / 2.5, 0, 1)
    sig = sum(np.sin(2 * np.pi * hz(m) * t + rng.uniform(0, 6)) * (.5 if m < 50 else .22) +
              .08 * np.sin(2 * np.pi * hz(m) * 2.003 * t) for m in ch) * e
    i = int(t0 * SR); sig = sig[: N - i]; pad[i:i + len(sig)] += sig
pad = band(pad, hi=1600)
# quiet under the story, a little fuller for the twist, warm under RASOLV, out at the end
lvl = np.interp(tt, [0, S("hook"), S("labor"), S("video") - 1.5, S("video"), S("rasolv"), DUR - 2.5, DUR],
                [.3, .45, .45, .35, .7, .75, .75, 0])
music.add(pad * lvl * .11, 0)

def pluck(m, d=1.8):
    n = int(SR * d); t = np.arange(n) / SR
    return sum(np.sin(2 * np.pi * hz(m) * h * t) / h ** 1.6 for h in (1, 2, 3, 4)) * env(n, .004, .5)
for t0, notes in [(S("harvard"), [65, 68, 72]), (S("same"), [63, 67, 70]), (S("rated"), [68, 72, 75]),
                  (S("labor"), [65, 68, 72]), (S("hate"), [61, 65, 68]), (S("video"), [72, 75, 80]),
                  (S("rasolv"), [68, 72, 77])]:
    for j, m in enumerate(notes): music.add(pluck(m), t0 + j * .18, .065, pan=-.3 + .3 * j)

# ---------- sound design ----------
def blip(f, d=.14):
    n = int(SR * d); t = np.arange(n) / SR
    return np.sin(2 * np.pi * f * t) * env(n, .002, .04)
def click():
    n = int(SR * .03); return band(rng.normal(0, 1, n), lo=2500, hi=8000) * env(n, .0003, .004)
def tick(hi):
    n = int(SR * .05); return band(rng.normal(0, 1, n), lo=2500 if hi else 1600, hi=7000) * env(n, .0005, .006)
def whoosh(d=.8):
    n = int(SR * d); t = np.arange(n) / SR
    return band(rng.normal(0, 1, n), lo=400, hi=3500) * np.sin(np.pi * t / d) ** 2
def boom():
    n = int(SR * 3); t = np.arange(n) / SR
    return np.sin(2 * np.pi * (38 + 40 * np.exp(-t / .06)) * t) * env(n, .002, .9) + band(rng.normal(0, 1, n), hi=600) * env(n, .002, .3) * .3
def chime(m, d=1.2):
    n = int(SR * d); t = np.arange(n) / SR
    return (np.sin(2 * np.pi * hz(m) * t) + .3 * np.sin(2 * np.pi * hz(m) * 2.76 * t) * np.exp(-t / .15)) * env(n, .002, .35)

# a soft click for every airline checked (cold open + site B)
for a, b, total in [(.3, S("liked") + .4, 48 * .4), (S("but") + .2, S("same") + .1, 48)]:
    for k in range(1, int(total)):
        sfx.add(click(), a + (b - a) * k / total, .07, pan=.3)
for base in (S("instant") + .9, S("same") + .15):                  # results appear
    for k in range(4): sfx.add(blip(1100 + 90 * k), base + k * .18, .035)
for k in range(5): sfx.add(blip(880 * 2 ** (k * 3 / 12)), S("liked") + .1 + k * .15 * .8, .04)
for k in range(2): sfx.add(blip(520 + 260 * k, .3), S("rated") + .2 + k * .35, .035)
sfx.add(blip(1200, .25), S("blind") + .2, .04)                     # "!"
k = 0; t = np.ceil(S("hate"))                                        # clock while the blind pawn waits
while t < E("blind") + .3: sfx.add(tick(k % 2 == 0), t, .16, pan=-.4); t += 1; k += 1
for c in ("harvard", "hate", "rasolv"): sfx.add(whoosh(), S(c) - .5, .09)
n = int(SR * 2.2); r = band(rng.normal(0, 1, n), lo=900, hi=6000) * (np.arange(n) / n) ** 2
sfx.add(r, S("video") - 2.2, .08)
sfx.add(boom(), S("video") - .02, .3)
for t0 in (S("rasolv") + .1, S("expert"), S("expert") + .9, S("live")): sfx.add(chime(84), t0, .04, pan=.2)
c0 = S("cta") + .9
sfx.add(boom(), c0, .45)
for j, m in enumerate([53, 60, 65, 68]): music.add(pluck(m, 3), c0 + j * .05, .08)

# ---------- voice + mix ----------
vo = np.zeros(N)
for l in META["lines"]:
    a, sr = sf.read(f"out/vo/{l['i']:02d}.wav", dtype="float32")
    if a.ndim > 1: a = a.mean(1)
    if sr != SR: a = resample_poly(a, SR, sr)
    i = int(l["start"] * SR); a = a[: N - i]; vo[i:i + len(a)] += a
voice.add(vo, 0, 1.0)
# sidechain: duck music/sfx under the voice
envv = np.convolve(np.abs(vo), np.ones(int(SR * .05)) / int(SR * .05), "same")
duck = 1 - .45 * np.clip(envv / (envv.max() * .25 + 1e-9), 0, 1)
duck = np.convolve(duck, np.ones(int(SR * .12)) / int(SR * .12), "same")

wetL, wetR = reverb(music.L + .5 * sfx.L), reverb(music.R + .5 * sfx.R)
L = (music.L + sfx.L + .35 * wetL) * duck + voice.L + .06 * reverb(voice.L, 1.2)
R = (music.R + sfx.R + .35 * wetR) * duck + voice.R + .06 * reverb(voice.R, 1.2)
fade = np.clip((DUR - tt) / 1.0, 0, 1) * np.clip(tt / .3, 0, 1)
mix = np.stack([L * fade, R * fade], 1)
mix /= np.abs(mix).max() / .89
out = wave.open(sys.argv[1] if len(sys.argv) > 1 else "out/mix.wav", "wb")
out.setnchannels(2); out.setsampwidth(2); out.setframerate(SR)
out.writeframes((mix * 32767).astype("<i2").tobytes()); out.close()
print("mix written", DUR, "s")
