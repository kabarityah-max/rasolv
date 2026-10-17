"""Synthesises the "Carousel" soundtrack — a sparse pad score + sound design (clock ticks while people wait, belt hum,
bag clunks, footsteps while they walk, whooshes on scene changes, a riser into the twist) — and mixes in the
voiceover (out/vo/NN.wav, placed per out/vo/lines.json) with sidechain ducking. Fully synthesised, royalty-free.
Usage: python3 score.py out/mix.wav"""
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


# ---------- score: slow pad, A minor → F → C → G, one chord per ~6.4 s ----------
CHORDS = [[45, 57, 60, 64, 69], [41, 53, 60, 65, 69], [48, 55, 60, 64, 67], [43, 55, 59, 62, 67]]
BAR = 6.4
tt = np.arange(N) / SR
pad = np.zeros(N)
for k in range(int(DUR / BAR) + 1):
    ch = CHORDS[k % 4]; t0 = k * BAR; n = int(SR * (BAR + 2.5)); t = np.arange(n) / SR
    e = np.minimum(t / 1.6, 1) * np.clip((BAR + 2.5 - t) / 2.5, 0, 1)
    sig = sum(np.sin(2 * np.pi * hz(m) * t + rng.uniform(0, 6)) * (.5 if m < 50 else .22) +
              .08 * np.sin(2 * np.pi * hz(m) * 2.003 * t) for m in ch) * e
    i = int(t0 * SR); sig = sig[: N - i]; pad[i:i + len(sig)] += sig
pad = band(pad, hi=1800)
# the music thins out under the reveal ("they made the walk longer") and opens up for the twist
lvl = np.interp(tt, [0, S("houston"), S("fix"), S("fix") + 1, S("video") - 2, S("video"), DUR - 3, DUR],
                [.25, .55, .55, .8, .8, 1.0, 1.0, .0])
music.add(pad * lvl * .16, 0)

# soft piano-ish motif on each act (plucked sine with harmonics)
def pluck(m, d=1.8):
    n = int(SR * d); t = np.arange(n) / SR
    return sum(np.sin(2 * np.pi * hz(m) * h * t) / h ** 1.6 for h in (1, 2, 3, 4)) * env(n, .004, .5)
for t0, notes in [(S("houston"), [69, 72, 76]), (S("obvious"), [67, 71, 74]), (S("closer"), [64, 69, 72]),
                  (S("fix"), [72, 76, 79]), (S("hate"), [69, 72, 76]), (S("video"), [76, 79, 84]),
                  (S("which"), [69, 72, 76, 81])]:
    for j, m in enumerate(notes): music.add(pluck(m), t0 + j * .18, .09, pan=-.3 + .3 * j)

# ---------- sound design ----------
def tick(hi):
    n = int(SR * .05); x = band(rng.normal(0, 1, n), lo=2500 if hi else 1600, hi=7000) * env(n, .0005, .006)
    return x
def clunk():
    n = int(SR * .35); t = np.arange(n) / SR
    return (np.sin(2 * np.pi * (90 + 60 * np.exp(-t / .02)) * t) * env(n, .001, .08) +
            band(rng.normal(0, 1, n), lo=300, hi=2000) * env(n, .001, .02) * .5)
def step():
    n = int(SR * .18); t = np.arange(n) / SR
    return np.sin(2 * np.pi * (70 + 50 * np.exp(-t / .015)) * t) * env(n, .002, .05) + band(rng.normal(0, 1, n), lo=800, hi=4000) * env(n, .001, .012) * .3
def blip(f):
    n = int(SR * .16); t = np.arange(n) / SR
    return np.sin(2 * np.pi * f * t) * env(n, .002, .04)
def whoosh(d=.9, up=True):
    n = int(SR * d); t = np.arange(n) / SR; x = rng.normal(0, 1, n)
    out = np.zeros(n); blk = int(SR * .02)
    for s in range(0, n, blk):
        f = s / n; c = 400 + 4000 * (f if up else 1 - f)
        out[s:s + blk] = band(x[max(0, s - blk):s + 2 * blk], lo=c * .5, hi=c)[(s - max(0, s - blk)):(s - max(0, s - blk)) + blk][:len(out[s:s + blk])]
    return out * np.sin(np.pi * t / d) ** 2
def boom():
    n = int(SR * 3); t = np.arange(n) / SR
    return np.sin(2 * np.pi * (38 + 40 * np.exp(-t / .06)) * t) * env(n, .002, .9) + band(rng.normal(0, 1, n), hi=600) * env(n, .002, .3) * .3

# clock: tick-tock while people wait (the hall + the measured "standing"), and on the standing pawn
for a, b in [(.3, S("walk1")), (S("stand7"), S("fix") - .2), (S("hate") - .1, E("stand") + .3)]:
    k = 0; t = np.ceil(a)
    while t < b: sfx.add(tick(k % 2 == 0), t, .2, pan=-.4); t += 1; k += 1

# belt hum in the hall
hum = band(rng.normal(0, 1, N), hi=140) * 2.2 + .25 * np.sin(2 * np.pi * 55 * tt) * (1 + .2 * np.sin(2 * np.pi * .3 * tt))
hall = np.clip(np.minimum((tt - 0) / .6, 1), 0, 1) * (tt < S("closer") + .3) + ((tt > S("zero") - .3) & (tt < E("nobody") + .3))
music.add(band(hum * hall, hi=300) * .09, 0)

# bags dropping onto the belt (sparse, then busy once the handlers arrive)
t = S("houston") - 1.2
while t < S("closer"):
    sfx.add(clunk(), t, .16, pan=rng.uniform(-.2, .2)); t += 1.15 if t > S("hire") + .4 else 2.9
t = S("zero") - .2
while t < E("nobody"): sfx.add(clunk(), t, .12); t += 1.2

# "!" pops over the crowd, twice; then they pop away
for base, n_ in [(S("complain"), 12), (S("still"), 7)]:
    for j in range(n_): sfx.add(blip(rng.uniform(900, 1400)), base + rng.uniform(0, .9), .05, pan=rng.uniform(-.7, .7))
for j in range(10): sfx.add(blip(rng.uniform(500, 700)), S("zero") + .2 + rng.uniform(0, 1.3), .05, pan=rng.uniform(-.7, .7))

# footsteps wherever someone walks
for a, b, rate in [(S("walk1"), E("walk1"), .38), (S("six"), E("six") + .4, .3), (S("zero") - .3, S("zero") + .5, .28),
                   (S("hate") - .1, E("stand") + .3, .42), (S("which") + 2.2, E("which") + .5, .42)]:
    t, k = a, 0
    while t < b: sfx.add(step(), t, .22, pan=.25 if k % 2 else -.05); t += rate; k += 1

# transitions
for t0 in [S("closer"), S("fix"), S("zero") - .3, S("hate") - .3, S("bag") - .3, S("which") - .3]:
    sfx.add(whoosh(.8), t0 - .4, .12)
# into the twist: riser, then a low hit on "You stayed."
n = int(SR * 2.2); r = band(rng.normal(0, 1, n), lo=900, hi=6000) * (np.arange(n) / n) ** 2
sfx.add(r, S("video") - 2.2, .1)
sfx.add(boom(), S("video") - .02, .35)
sfx.add(boom(), S("stayed") - .02, .3)
sfx.add(clunk(), S("bag") + .95, .45)                       # your bag lands
sfx.add(boom(), E("which") + 1.8, .5)                         # wordmark
for j, m in enumerate([57, 64, 69, 72]): music.add(pluck(m, 3), E("which") + 1.8 + j * .05, .1)

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
