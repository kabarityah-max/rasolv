"""Synthesises the "Show Your Work" soundtrack — an original 142 BPM drill beat (sliding 808s, half-time claps with
syncopated pickups, 16th hi-hats with triplet rolls, a dark F-minor bell and string line) plus sound design (a tick
for every airline checked, result pops, step chimes, whooshes on cuts, a riser and drop into RASOLV, a logo hit) —
and mixes in the voiceover (out/vo/NN.wav per out/vo/lines.json) with sidechain ducking. Fully synthesised, so it
is royalty-free. The drums stop for the twist ("This TikTok did the same thing") and drop back in on RASOLV;
index.html pulses on the same grid. Usage: python3 score.py out/mix.wav"""
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
rng = np.random.default_rng(11)
BEAT = 60 / META["bpm"]; STEP = BEAT / 4; BAR = BEAT * 4
T0 = 0.42                                    # the grid starts one beat in (vo.py OPEN)
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


# ---------- instruments ----------
def kick():
    n = int(SR * .35); t = np.arange(n) / SR
    return np.tanh(2.2 * np.sin(2 * np.pi * (48 + 110 * np.exp(-t / .03)) * t) * env(n, .001, .12))
def clap():
    n = int(SR * .3); x = band(rng.normal(0, 1, n), lo=900, hi=7000)
    t = np.arange(n) / SR
    e = sum(np.exp(-np.maximum(t - d, 0) / .008) * (t >= d) for d in (0, .011, .022)) + np.exp(-np.maximum(t - .03, 0) / .09) * (t >= .03)
    body_ = np.sin(2 * np.pi * 190 * t) * env(n, .001, .03) * .6
    return x * e * .5 + body_
def hat(open_=False):
    n = int(SR * (.28 if open_ else .05)); x = band(rng.normal(0, 1, n), lo=7000, hi=15000)
    return x * env(n, .0005, .09 if open_ else .012)
def eight08(notes, dur):
    """notes: [(t_rel, midi)] — glides 70 ms into each new note, one continuous sustained tone."""
    n = int(SR * dur); t = np.arange(n) / SR
    f = np.full(n, hz(notes[0][1]))
    for (a, m0), (b, m1) in zip(notes, notes[1:]):
        i = int(b * SR); g = int(.07 * SR)
        f[i:] = hz(m1); f[i:i + g] = np.linspace(hz(m0), hz(m1), len(f[i:i + g]))
    ph = 2 * np.pi * np.cumsum(f) / SR
    e = np.minimum(t / .004, 1) * np.exp(-t / 1.6) * np.clip((dur - t) / .05, 0, 1)
    return np.tanh(1.8 * np.sin(ph)) * e
def bell(m, d=1.6):
    n = int(SR * d); t = np.arange(n) / SR
    return (np.sin(2 * np.pi * hz(m) * t) + .5 * np.sin(2 * np.pi * hz(m) * 2.76 * t) * np.exp(-t / .2)
            + .25 * np.sin(2 * np.pi * hz(m) * 5.4 * t) * np.exp(-t / .06)) * env(n, .002, .45)
def string(ms, d):
    n = int(SR * d); t = np.arange(n) / SR
    e = np.minimum(t / .5, 1) * np.clip((d - t) / .4, 0, 1)
    x = sum(sum(np.sin(2 * np.pi * hz(m) * (1 + dt) * t + rng.uniform(0, 6)) for dt in (-.003, 0, .003)) for m in ms)
    return band(x, hi=2400) * e

drums, bass, keys = Bus(), Bus(), Bus()
drop_out, drop_in = S("video") - .05, S("rasolv")
on = lambda t: t < drop_out or t >= drop_in
# F minor: Fm – Db – Bbm – C (one chord per bar), 808 roots with drill slides
PROG = [(29, [53, 56, 60]), (25, [49, 53, 56]), (34, [46, 49, 53]), (24, [48, 52, 55])]
KICK = [0, 3, 6, 10, 14]
SLIDE = {0: 0, 3: 0, 6: 12, 10: 0, 14: 7}       # 808 note per kick step, semitones above the root
nbars = int((DUR - T0) / BAR) + 2
for b in range(nbars):
    t_bar = T0 + b * BAR
    if t_bar > DUR: break
    root, ch = PROG[b % 4]
    full = on(t_bar) and on(t_bar + BAR - .01)
    for st in range(16):
        t = t_bar + st * STEP
        if not on(t) or t > DUR: continue
        if st in KICK and (b % 2 == 0 or st != 6): drums.add(kick(), t, .55)
        if st in (4, 12) or (b % 2 == 1 and st == 15) or (b % 4 == 2 and st == 7): drums.add(clap(), t, .38 if st in (4, 12) else .2)
        roll = b % 2 == 1 and st >= 12
        if roll and st in (12, 14):                                   # triplet roll
            for k in range(3): drums.add(hat(), t + k * STEP * 2 / 3, .12, pan=.25)
        elif not roll or st in (13, 15):
            drums.add(hat(open_=(st == 10 and b % 4 == 3)), t, .16 if st % 2 == 0 else .09, pan=.25)
    # 808 phrase for the bar
    notes = [(k * STEP, root + SLIDE[k]) for k in KICK if on(t_bar + k * STEP)]
    if notes and on(t_bar):
        sig = eight08([(a - notes[0][0], m) for a, m in notes], BAR - notes[0][0])
        bass.add(sig, t_bar + notes[0][0], .42)
    # dark bell motif (every bar) + strings (always, so the twist keeps a bed)
    motif = [ch[2] + 12, ch[1] + 12, ch[0] + 12, ch[1] + 12] if b % 2 == 0 else [ch[2] + 12, ch[2] + 13, ch[2] + 12, ch[0] + 12]
    for k, m in enumerate(motif): keys.add(bell(m), t_bar + [0, 3, 6, 10][k] * STEP, .07 if on(t_bar) else .045, pan=-.3)
    keys.add(string(ch, BAR + .4), t_bar, .03)

# twist: everything filtered and low, then a riser into the drop
twist = (tt >= drop_out) & (tt < drop_in)
music.L += (drums.L + bass.L + keys.L); music.R += (drums.R + bass.R + keys.R)
for ch_ in (music.L, music.R):
    seg = ch_[twist]; ch_[twist] = band(seg, hi=900) * .8
n = int(SR * 2.4); r = band(rng.normal(0, 1, n), lo=1200, hi=9000) * (np.arange(n) / n) ** 2.5
sfx.add(r, drop_in - 2.4, .14)

# ---------- sound design ----------
def blip(f, d=.12):
    n = int(SR * d); t = np.arange(n) / SR
    return np.sin(2 * np.pi * f * t) * env(n, .002, .035)
def click():
    n = int(SR * .03); return band(rng.normal(0, 1, n), lo=3000, hi=9000) * env(n, .0003, .004)
def whoosh(d=.6):
    n = int(SR * d); t = np.arange(n) / SR
    return band(rng.normal(0, 1, n), lo=500, hi=5000) * np.sin(np.pi * t / d) ** 3
def boom():
    n = int(SR * 2.5); t = np.arange(n) / SR
    return np.tanh(2 * np.sin(2 * np.pi * (36 + 60 * np.exp(-t / .05)) * t) * env(n, .002, .8)) + band(rng.normal(0, 1, n), hi=700) * env(n, .002, .25) * .3

# a click for every airline checked (hook + site B)
for a, b, total in [(.1, S("liked") + .4, 48 * .55), (S("but") + .2, S("same") + .1, 48)]:
    for k in range(1, int(total)):
        sfx.add(click(), a + (b - a) * k / total, .1, pan=.3)
# results pop in (site A, then site B), stars land
for base in (S("instant") + .9, S("same") + .15):
    for k in range(4): sfx.add(blip(1320 + 120 * k), base + k * .06, .05)
for k in range(5): sfx.add(blip(880 * 2 ** (k / 12 * 3)), S("liked") + .1 + k * .15 * .8, .06)
sfx.add(blip(1760, .3), S("same") + .5, .06)                                # "="
for k in range(2): sfx.add(blip(600 + 300 * k, .25), S("rated") + .2 + k * .35, .05)
sfx.add(blip(1100, .25), S("blind") + .2, .06)                               # "!"
# whooshes into cuts
for c in ("harvard", "rated", "hate", "video", "cta"): sfx.add(whoosh(), S(c) - .4, .1)
# the twist hit + the drop
sfx.add(boom(), S("video") - .02, .3)
sfx.add(boom(), drop_in - .01, .45)
# step chimes in the app
for t0 in (S("rasolv") + .1, S("expert"), C["expert"][0] + .9, S("live")):
    sfx.add(bell(84, .8), t0, .05, pan=.2)
# the logo
c0 = S("cta") + .9
sfx.add(boom(), c0, .5)
for j, m in enumerate([65, 68, 72, 77]): sfx.add(bell(m, 2.4), c0 + j * .05, .06)

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
duck = 1 - .38 * np.clip(envv / (envv.max() * .25 + 1e-9), 0, 1)
duck = np.convolve(duck, np.ones(int(SR * .12)) / int(SR * .12), "same")

wetL, wetR = reverb(music.L + .5 * sfx.L), reverb(music.R + .5 * sfx.R)
L = (music.L + sfx.L + .35 * wetL) * duck * .5 + voice.L + .06 * reverb(voice.L, 1.2)
R = (music.R + sfx.R + .35 * wetR) * duck * .5 + voice.R + .06 * reverb(voice.R, 1.2)
fade = np.clip((DUR - tt) / 1.0, 0, 1) * np.clip(tt / .3, 0, 1)
mix = np.stack([L * fade, R * fade], 1)
mix /= np.abs(mix).max() / .89
out = wave.open(sys.argv[1] if len(sys.argv) > 1 else "out/mix.wav", "wb")
out.setnchannels(2); out.setsampwidth(2); out.setframerate(SR)
out.writeframes((mix * 32767).astype("<i2").tobytes()); out.close()
print("mix written", DUR, "s")
