"""RASOLV promo soundtrack: original 125 BPM electronic track + sound design + voiceover mix.
Everything is synthesised here (no samples), so the music is royalty-free.
Usage: python3 music.py out/mix.wav [--no-vo]"""
import sys, json, os, wave
import numpy as np
from scipy import signal
import soundfile as sf

SR = 48000
DUR = 19.6
N = int(SR * DUR)
BPM = 125
BEAT = 60 / BPM            # 0.48 s
BAR = 4 * BEAT             # 1.92 s
DROP = 5 * BAR             # 9.6 s
LOGO = 8 * BAR             # 15.36 s
HERE = os.path.dirname(os.path.abspath(__file__))
rng = np.random.default_rng(11)

# voiceover placement (seconds) — matches the visual timeline in index.html
VO_AT = [0.45, 3.62, 6.38, 9.70, 11.85, 13.75, 16.05]


def buf():
    return np.zeros((N, 2))


def place(dst, sig, t, gain=1.0, pan=0.0):
    if sig.ndim == 1:
        sig = np.stack([sig * (1 - max(0, pan)), sig * (1 + min(0, pan))], 1)
    i = int(round(t * SR))
    if i >= N:
        return
    n = min(len(sig), N - i)
    dst[i:i + n] += sig[:n] * gain


def env(n, a, d, sustain=0.0):
    t = np.arange(n) / SR
    return np.minimum(t / max(a, 1e-4), 1) * (sustain + (1 - sustain) * np.exp(-t / d))


def lp(x, fc, q=0.707):
    b, a = signal.butter(2, min(fc, SR * 0.45) / (SR / 2), 'low')
    return signal.lfilter(b, a, x, axis=0)


def hp(x, fc):
    b, a = signal.butter(2, fc / (SR / 2), 'high')
    return signal.lfilter(b, a, x, axis=0)


def bp(x, lo, hi):
    b, a = signal.butter(2, [lo / (SR / 2), hi / (SR / 2)], 'band')
    return signal.lfilter(b, a, x, axis=0)


def sweep_lp(x, f0, f1, curve=2.0):
    """time-varying low-pass via block processing (state carried across blocks)."""
    out = np.zeros_like(x)
    blk = 512
    zi = None
    for s in range(0, len(x), blk):
        k = (s / max(1, len(x) - 1)) ** curve
        fc = f0 * (f1 / f0) ** k
        b, a = signal.butter(2, min(fc, SR * 0.45) / (SR / 2), 'low')
        if zi is None:
            zi = np.zeros((2, x.shape[1])) if x.ndim == 2 else np.zeros(2)
        out[s:s + blk], zi = signal.lfilter(b, a, x[s:s + blk], axis=0, zi=zi)
    return out


def saw(f, n, phase=0.0):
    t = np.arange(n) / SR
    return signal.sawtooth(2 * np.pi * f * t + phase)


def supersaw(f, n, voices=7, detune=0.012):
    out = np.zeros((n, 2))
    for v in range(voices):
        d = (v - (voices - 1) / 2) / ((voices - 1) / 2) * detune
        s = saw(f * (1 + d), n, rng.uniform(0, 6.28))
        pan = (v - (voices - 1) / 2) / ((voices - 1) / 2) * 0.8
        out[:, 0] += s * (1 - max(0, pan)); out[:, 1] += s * (1 + min(0, pan))
    return out / voices


def reverb(x, secs=2.2, mix=0.25, pre=0.02):
    n = int(SR * secs)
    t = np.arange(n) / SR
    irs = []
    for ch in range(2):
        ir = rng.normal(0, 1, n) * np.exp(-t / (secs / 6.5))
        ir = lp(ir, 6000)
        ir[: int(pre * SR)] = 0
        irs.append(ir / np.sqrt(np.sum(ir ** 2)))
    wet = np.stack([signal.fftconvolve(x[:, c], irs[c])[: len(x)] for c in range(2)], 1)
    return x * (1 - mix) + wet * mix * 1.6


def midi(m):
    return 440 * 2 ** ((m - 69) / 12)


# ---------- harmony: F minor  i – VI – III – VII (Fm Db Ab Eb) ----------
CHORDS = [[53, 56, 60, 65], [49, 53, 56, 61], [56, 60, 63, 68], [51, 55, 58, 63]]
ROOTS = [41, 37, 44, 39]
def chord_at(t):  # one chord per bar
    return int(t // BAR) % 4


# ---------- drums ----------
def kick(n=int(SR * .45), punch=1.0):
    t = np.arange(n) / SR
    f = 46 + 140 * np.exp(-t / 0.035)
    body = np.sin(2 * np.pi * np.cumsum(f) / SR) * env(n, .001, .16)
    click = hp(rng.normal(0, 1, n), 3000) * env(n, .0005, .004) * .5
    return np.tanh(1.8 * (body + click) * punch)


def clap(n=int(SR * .35)):
    x = bp(rng.normal(0, 1, n), 900, 5000)
    e = np.zeros(n)
    for o in (0, .009, .018, .027):
        i = int(o * SR); e[i:] += env(n - i, .0005, .006 if o < .027 else .09)
    return x * e * .8


def hat(open_=False):
    n = int(SR * (.25 if open_ else .06))
    x = hp(rng.normal(0, 1, n), 7500)
    return x * env(n, .0005, .07 if open_ else .012)


def snare(n=int(SR * .25)):
    t = np.arange(n) / SR
    tone = np.sin(2 * np.pi * 190 * t) * env(n, .001, .05)
    return (tone * .6 + bp(rng.normal(0, 1, n), 1500, 8000) * env(n, .001, .07)) * .7


# ---------- sound design ----------
def whoosh(length, f0=300, f1=8000, rise=True):
    n = int(SR * length)
    x = rng.normal(0, 1, (n, 2))
    e = np.linspace(0, 1, n)
    shape = (e ** 2.5) if rise else ((1 - e) ** 1.6) * np.minimum(e * 12, 1)
    y = sweep_lp(x, f0 if rise else f1, f1 if rise else f0, 1.0)
    return y * shape[:, None]


def impact():
    n = int(SR * 3.0)
    t = np.arange(n) / SR
    f = 38 + 90 * np.exp(-t / .05)
    sub = np.tanh(2.2 * np.sin(2 * np.pi * np.cumsum(f) / SR) * env(n, .001, .7))
    crash = hp(rng.normal(0, 1, n), 4000) * env(n, .001, .9) * .35
    return np.stack([sub + crash, sub + crash * .9], 1)


def reverse_cymbal(length):
    n = int(SR * length)
    x = hp(rng.normal(0, 1, (n, 2)), 3000)
    return x * (np.linspace(0, 1, n) ** 3)[:, None] * .6


def ui_click(f=2400):
    n = int(SR * .08)
    t = np.arange(n) / SR
    return np.sin(2 * np.pi * f * t) * env(n, .0005, .012) + hp(rng.normal(0, 1, n), 4000) * env(n, .0003, .003) * .4


def notif():
    n = int(SR * 1.2)
    t = np.arange(n) / SR
    out = np.zeros(n)
    for k, m in enumerate([84, 91]):
        s = int(k * .09 * SR)
        out[s:] += np.sin(2 * np.pi * midi(m) * t[: n - s]) * env(n - s, .002, .35)
    return out * .5


# ================= build stems =================
music, drums, fx = buf(), buf(), buf()

# --- pads (whole song), filter opens through the intro, sidechained after the drop ---
pad = buf()
for b in range(int(np.ceil(DUR / BAR))):
    t0 = b * BAR
    n = int(BAR * SR) + int(.3 * SR)
    ch = CHORDS[b % 4]
    s = sum(supersaw(midi(m), n) for m in ch) / len(ch)
    e = env(n, .08, 3.0, .7)
    e[-int(.3 * SR):] *= np.linspace(1, 0, int(.3 * SR))
    place(pad, s * e[:, None], t0)
cut = np.interp(np.arange(N) / SR, [0, DROP - .3, DROP, LOGO, DUR], [350, 2600, 4200, 5200, 1200])
padf = np.zeros_like(pad)
blk = 1024
zi = np.zeros((2, 2))
for s in range(0, N, blk):
    b_, a_ = signal.butter(2, cut[s] / (SR / 2), 'low')
    padf[s:s + blk], zi = signal.lfilter(b_, a_, pad[s:s + blk], axis=0, zi=zi)
pad = padf
pad *= np.interp(np.arange(N) / SR, [0, 1.5, DROP - .15, DROP - .14, DROP, DUR - 1.5, DUR], [0, .8, 1, 0, 1, .9, 0])[:, None]

# --- pluck arp (16ths) from bar 2 ---
arp = buf()
pattern = [0, 2, 1, 3, 2, 1, 3, 2]
step = BEAT / 4
t = BAR
i = 0
while t < DUR - 1.2:
    if DROP - .15 <= t < DROP:
        t += step; i += 1; continue
    ch = CHORDS[chord_at(t) % 4]
    m = ch[pattern[i % 8] % 4] + 12 + (12 if (i // 8) % 2 and t >= DROP else 0)
    n = int(.25 * SR)
    tt = np.arange(n) / SR
    x = (signal.square(2 * np.pi * midi(m) * tt, .3) * .5 + saw(midi(m), n) * .5)
    x = lp(x, 1200 + 2500 * min(1, t / DROP) + (2500 if t >= DROP else 0)) * env(n, .001, .07)
    place(arp, x, t, .32, pan=.35 * np.sin(i * 1.3))
    t += step; i += 1
arp *= np.interp(np.arange(N) / SR, [0, BAR, 2 * BAR, DUR - 2, DUR], [0, 0, 1, .8, 0])[:, None]

# --- bass: offbeat pumping in the drop, long sub under the logo ---
bass = buf()
for b in range(5, 8):
    for q in range(8):
        tb = b * BAR + q * BEAT / 2
        if q % 2 == 0:
            continue
        r = ROOTS[b % 4]
        n = int(BEAT / 2 * .95 * SR)
        x = np.sin(2 * np.pi * midi(r) * np.arange(n) / SR) * .8 + lp(saw(midi(r + 12), n), 900) * .5
        place(bass, np.tanh(1.5 * x) * env(n, .003, .2, .6), tb, .6)
n = int(3.5 * SR)
place(bass, np.sin(2 * np.pi * midi(29) * np.arange(n) / SR) * env(n, .01, 1.6), LOGO, .5)

# --- drums ---
for b in range(2, 5):           # soft heartbeat kick in the build
    for q in range(4):
        tb = b * BAR + q * BEAT
        if tb < DROP - BAR:
            place(drums, lp(kick(punch=.7), 900), tb, .35 if q % 2 == 0 else .15)
# snare roll into the drop
t = DROP - BAR
k = 0
while t < DROP - .16:
    frac = (t - (DROP - BAR)) / BAR
    place(drums, snare(), t, .15 + .4 * frac, pan=.15 * np.sin(k))
    t += BEAT / (2 if frac < .5 else 4 if frac < .75 else 8); k += 1
# the drop
for b in range(5, 8):
    for q in range(4):
        tb = b * BAR + q * BEAT
        place(drums, kick(), tb, .95)
        if q in (1, 3):
            place(drums, clap(), tb, .55)
            place(drums, reverb(np.stack([clap(), clap()], 1), 1.2, .5), tb, .15)
        place(drums, hat(True), tb + BEAT / 2, .22, pan=.2)
        for s16 in range(4):
            place(drums, hat(), tb + s16 * BEAT / 4, .12 if s16 % 2 else .07, pan=-.25)

# --- sidechain (duck pads/arp/bass by the kick in the drop) ---
sc = np.ones(N)
for b in range(5, 8):
    for q in range(4):
        i0 = int((b * BAR + q * BEAT) * SR)
        n = int(BEAT * SR)
        tt = np.arange(n) / SR
        sc[i0:i0 + n] = np.minimum(sc[i0:i0 + n], 1 - .75 * np.exp(-tt / .09))
for stem in (pad, arp, bass):
    stem *= sc[:, None]

music = reverb(pad, 3.2, .35) * .55 + reverb(arp, 2.0, .3) * .7 + bass
# lift the intro so the build is present under the voice (drop stays the loudest part)
music *= np.interp(np.arange(N) / SR, [0, .4, DROP - .2, DROP], [1.2, 1.9, 1.6, 1.0])[:, None]

# --- sound design synced to visuals ---
place(fx, whoosh(1.2, 200, 3000), 0.0, .25)                 # phone rises
place(fx, ui_click(2000), 1.55, .35)                          # tap the Rasolv icon
place(fx, notif(), 1.86, .5)                                  # live activity
place(fx, whoosh(.5, 400, 9000), 3.3, .5)                     # push into widget
place(fx, ui_click(2800), 4.6, .3)                            # pill switch
place(fx, whoosh(.3, 500, 8000), 5.9, .45)                    # whip pan
place(fx, ui_click(2200), 7.08, .3)                           # expand row
place(fx, whoosh(DROP - 7.8, 150, 12000), 7.8, .55)           # riser into the drop
place(fx, reverse_cymbal(.5), DROP - .5, .4)
place(fx, impact() * .6, DROP, .9)                            # drop hit
place(fx, reverse_cymbal(.6), LOGO - .6, .5)
place(fx, impact(), LOGO, 1.0)                                # logo hit
for k, t in enumerate([9.70, 11.85, 13.75]):                  # type swooshes
    place(fx, whoosh(.35, 3000, 600, rise=False), t, .18, pan=(-.3, .3, 0)[k])
fx = reverb(fx, 1.6, .2)

# ================= voiceover =================
vo = buf()
if '--no-vo' not in sys.argv:
    vdir = os.path.join(HERE, 'vo')
    for i, at in enumerate(VO_AT):
        x, sr = sf.read(os.path.join(vdir, f'line{i}.wav'))
        if x.ndim > 1:
            x = x.mean(1)
        x = signal.resample_poly(x, SR, sr)
        x = hp(x, 90)
        # presence + gentle compression
        x = x + .35 * bp(x, 2500, 6000)
        x = np.tanh(2.2 * x / (np.max(np.abs(x)) + 1e-9)) / np.tanh(2.2)
        place(vo, x, at, 1.0)
    vo = reverb(vo, .9, .08)

# duck music under the voice
venv = np.abs(vo).max(1)
venv = signal.lfilter([1 - np.exp(-1 / (SR * .03))], [1, -np.exp(-1 / (SR * .03))], venv)
venv = np.maximum.accumulate(venv[::-1])[::-1] * 0 + venv  # (kept simple)
duck = 1 - .5 * np.clip(venv / (venv.max() + 1e-9) * 3, 0, 1)
duck = signal.lfilter([1 - np.exp(-1 / (SR * .12))], [1, -np.exp(-1 / (SR * .12))], duck)

mix = (music * .9 + drums * .8) * duck[:, None] + fx * .7 * (.6 + .4 * duck[:, None]) + vo * .95

# master: glue + soft limit, normalise to ~-14 LUFS-ish (RMS proxy)
mix = hp(mix, 25)
rms = np.sqrt(np.mean(mix ** 2))
mix *= 0.2 / (rms + 1e-9)
mix = np.tanh(mix * 1.1) / np.tanh(1.1)
mix *= 0.95 / np.max(np.abs(mix))
fade = np.ones(N); fade[-int(.25 * SR):] = np.linspace(1, 0, int(.25 * SR))
mix *= fade[:, None]
sf.write(sys.argv[1], mix.astype(np.float32), SR, subtype='PCM_24')
print('wrote', sys.argv[1], f'{DUR}s')
