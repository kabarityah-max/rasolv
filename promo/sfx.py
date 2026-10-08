"""Synthesises the RASOLV soundtrack (ambient pad + UI sound design) synced to index.html's timeline.
Usage: python3 sfx.py out.wav"""
import sys, wave
import numpy as np

SR = 48000
DUR = 14.0
N = int(SR * DUR)
rng = np.random.default_rng(7)
L = np.zeros(N); R = np.zeros(N)


def add(sig, t, gain=1.0, pan=0.0):
    i = int(t * SR)
    sig = sig[: max(0, N - i)]
    L[i:i + len(sig)] += sig * gain * (1 - max(0, pan))
    R[i:i + len(sig)] += sig * gain * (1 + min(0, pan))


def env(n, a, d):
    t = np.arange(n) / SR
    return np.minimum(t / max(a, 1e-4), 1) * np.exp(-t / d)


def lowpass(x, cutoff):
    # simple one-pole, cutoff may be an array
    c = np.broadcast_to(np.asarray(cutoff, float), x.shape)
    k = 1 - np.exp(-2 * np.pi * c / SR)
    y = np.empty_like(x); acc = 0.0
    for i in range(len(x)):
        acc += k[i] * (x[i] - acc); y[i] = acc
    return y


def tick(freq=2400, d=0.025):
    n = int(SR * 0.12); t = np.arange(n) / SR
    return np.sin(2 * np.pi * freq * t) * env(n, 0.0008, d) + rng.normal(0, 1, n) * env(n, 0.0003, 0.004) * 0.3


def click():
    return tick(1800, 0.018) * 0.8 + tick(5200, 0.006) * 0.4


def pop(f0=420):
    n = int(SR * 0.25); t = np.arange(n) / SR
    f = f0 * (1 + 1.5 * np.exp(-t / 0.02))
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * env(n, 0.002, 0.06)


def whoosh(length=0.45, rise=True, bright=4000):
    n = int(SR * length); x = np.linspace(0, 1, n)
    shape = (x ** 2 if rise else (1 - x) ** 2) if False else np.sin(np.pi * x) ** 2
    if rise: shape = x ** 2.2 * np.exp(-((x - 1) ** 2) * 0)  # swells into the hit
    cut = 300 + bright * shape
    return lowpass(rng.normal(0, 1, n), cut) * shape * 1.8


def boom(f0=55, d=0.9):
    n = int(SR * 2.0); t = np.arange(n) / SR
    f = f0 * (1 + 2.5 * np.exp(-t / 0.03))
    return np.tanh(1.6 * np.sin(2 * np.pi * np.cumsum(f) / SR) * env(n, 0.002, d))


def chime(freqs, d=0.9):
    n = int(SR * 2.5); t = np.arange(n) / SR; out = np.zeros(n)
    for k, f in enumerate(freqs):
        s = int(k * 0.07 * SR)
        tt = t[: n - s]
        out[s:] += (np.sin(2 * np.pi * f * tt) + 0.25 * np.sin(2 * np.pi * 2 * f * tt)) * env(n - s, 0.003, d)
    return out / len(freqs)


# ---- ambient pad bed (A maj9-ish), slow filter swell ----
t = np.arange(N) / SR
pad = np.zeros(N)
for f in [110, 164.81, 220, 277.18, 329.63, 493.88]:
    for det in (-0.6, 0.6):
        pad += np.sin(2 * np.pi * (f + det) * t + rng.uniform(0, 6))
pad /= 12
fade = np.minimum(t / 1.5, 1) * np.clip((DUR - t) / 0.8, 0, 1)
pad *= fade * (0.55 + 0.45 * np.sin(2 * np.pi * t / 7) ** 2)
add(pad, 0, 0.12)

# soft pulse kick each 0.72s through the UI section
for k in np.arange(0, 11.6, 0.72):
    add(boom(48, 0.12), k, 0.35)

# ---- keyword flashes ----
for k, tt in enumerate([0.0, 0.72, 1.44]):
    add(pop(520 + 80 * k), tt + 0.02, 0.5)
    add(whoosh(0.5, False, 3000), tt + 0.05, 0.25, pan=(0.5 if k != 1 else -0.5))
# circle wipe into impact
add(whoosh(0.5, True, 6000), 2.05, 0.5)
add(boom(50, 0.5), 2.55, 0.7)
# letters
for i in range(7):
    add(tick(2600 + i * 180, 0.02), 2.62 + i * 0.065, 0.35, pan=(i - 3) * 0.1)
# morph to icon
add(whoosh(0.6, True, 3500), 3.35, 0.35)
add(pop(260), 3.95, 0.7)
# icon -> chips
add(whoosh(0.3, False, 5000), 4.3, 0.25)
add(pop(600), 4.47, 0.5)
for tt in (4.95, 5.45):
    add(tick(3000, 0.03), tt, 0.4); add(whoosh(0.25, False, 4000), tt, 0.15)
add(whoosh(0.3, True, 4000), 5.82, 0.25)
# issue entries
for i, tt in enumerate([6.05, 6.32, 6.56, 6.80]):
    add(tick(2200 + 200 * i, 0.025), tt, 0.4)
add(click(), 6.98, 0.7)
add(whoosh(0.3, True, 4000), 7.05, 0.25)
# ticket card
add(pop(380), 7.3, 0.5)
add(click(), 8.04, 0.7)
add(whoosh(0.45, True, 5000), 8.45, 0.4)   # 3D flip
add(pop(300), 8.95, 0.45)
add(chime([880, 1318.5], 0.35), 9.58, 0.35)
# resolved
add(whoosh(0.3, True, 4000), 9.85, 0.25)
add(chime([659.25, 880, 1108.7, 1318.5], 0.8), 10.55, 0.5)
# rating
add(whoosh(0.35, False, 3000), 10.92, 0.25)
for i in range(5):
    add(tick(1760 * 2 ** (i / 12 * 2), 0.04), 11.14 + i * 0.06, 0.3, pan=(i - 2) * 0.2)
# outro
add(whoosh(1.0, True, 2500), 11.6, 0.35)
add(boom(42, 1.2), 12.62, 0.9)
add(chime([440, 659.25, 880, 1318.5], 1.4), 12.64, 0.35)

# ---- master ----
mix = np.stack([L, R], 1)
mix = np.tanh(mix * 1.2) / np.tanh(1.2)
mix *= 0.89 / np.max(np.abs(mix))
pcm = (mix * 32767).astype('<i2')
with wave.open(sys.argv[1], 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
print('wrote', sys.argv[1])
