"""Synthesises the RASOLV film soundtrack — original score + UI sound design synced to index.html — and mixes
in the voiceover (out/vo/*.wav, placed per out/vo/lines.json) with sidechain ducking.
Usage: python3 score.py out/mix.wav"""
import sys, json, wave, subprocess
import numpy as np

SR = 48000
DUR = 60.0
N = int(SR * DUR)
rng = np.random.default_rng(11)
t_all = np.arange(N) / SR


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


# ---------------- dsp helpers ----------------
def env(n, a, d):
    t = np.arange(n) / SR
    return np.minimum(t / max(a, 1e-4), 1) * np.exp(-t / d)


def fft_filter(x, lo=None, hi=None):
    """Zero-phase brickwall-ish band filter with soft edges (fast for static cutoffs)."""
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR); g = np.ones_like(f)
    if hi: g *= 1 / (1 + (f / hi) ** 4)
    if lo: g *= 1 / (1 + (lo / np.maximum(f, 1e-3)) ** 4)
    return np.fft.irfft(X * g, len(x))


def sweep_lp(x, c0, c1):
    """Lowpass whose cutoff glides c0→c1 (processed in 20 ms blocks)."""
    out = np.zeros_like(x); blk = int(SR * 0.02); pad = blk
    for s in range(0, len(x), blk):
        c = c0 + (c1 - c0) * (s / max(1, len(x) - 1))
        a, b = max(0, s - pad), min(len(x), s + blk + pad)
        out[s:s + blk] = fft_filter(x[a:b], hi=c)[s - a: s - a + blk]
    return out


def reverb_ir(seconds=2.2, damp=5000):
    n = int(SR * seconds); t = np.arange(n) / SR
    ir = rng.normal(0, 1, n) * np.exp(-t / (seconds / 6.5))
    ir = fft_filter(ir, hi=damp); ir[: int(SR * 0.012)] = 0
    return ir / np.sqrt(np.sum(ir ** 2))


def convolve(x, ir):
    n = len(x) + len(ir); m = 1 << (n - 1).bit_length()
    return np.fft.irfft(np.fft.rfft(x, m) * np.fft.rfft(ir, m), m)[: len(x)]


def note(name):
    names = {'C': 0, 'C#': 1, 'Db': 1, 'D': 2, 'Eb': 3, 'E': 4, 'F': 5, 'F#': 6, 'G': 7, 'Ab': 8, 'A': 9, 'Bb': 10, 'B': 11}
    return 440 * 2 ** ((names[name[:-1]] + 12 * (int(name[-1]) + 1) - 69) / 12)


# ---------------- instruments ----------------
def kick(gain=1.0):
    n = int(SR * 0.5); t = np.arange(n) / SR
    f = 45 + 95 * np.exp(-t / 0.035)
    body = np.sin(2 * np.pi * np.cumsum(f) / SR) * env(n, 0.001, 0.22)
    click = rng.normal(0, 1, n) * env(n, 0.0002, 0.003) * 0.25
    return np.tanh(1.8 * (body + click)) * gain


def hat(d=0.03):
    n = int(SR * 0.12)
    return fft_filter(rng.normal(0, 1, n), lo=7000) * env(n, 0.0005, d)


def clap():
    n = int(SR * 0.4); x = fft_filter(rng.normal(0, 1, n), lo=900, hi=6000)
    e = sum(env(n, 0.0005, 0.008) * (np.arange(n) >= int(SR * k * 0.011)) for k in range(3)) + env(n, 0.002, 0.09) * 0.6
    return x * e


def pluck(f, d=0.35, bright=1.0):
    n = int(SR * (d * 4)); t = np.arange(n) / SR
    s = np.zeros(n)
    for h, a in [(1, 1), (2, .45 * bright), (3, .22 * bright), (4, .12 * bright), (5, .06 * bright)]:
        s += a * np.sin(2 * np.pi * f * h * t) * np.exp(-t * h / d * 0.9)
    return s * env(n, 0.002, d * 1.6) * 0.5


def bass(f, length):
    n = int(SR * length); t = np.arange(n) / SR
    s = sum((1 / h) * np.sin(2 * np.pi * f * h * t) for h in range(1, 7))
    return np.tanh(1.2 * s) * np.minimum(t / 0.01, 1) * np.clip((length - t) / 0.05, 0, 1)


def pad(freqs, length, a=1.2, r=1.2, bright=2400):
    n = int(SR * (length + r)); t = np.arange(n) / SR; s = np.zeros(n)
    for f in freqs:
        for det in (-0.35, 0.35):
            ph = rng.uniform(0, 6)
            s += np.sin(2 * np.pi * (f + det) * t + ph) + 0.3 * np.sin(2 * np.pi * 2 * (f + det) * t + ph)
    e = np.minimum(t / a, 1) * np.clip((length + r - t) / r, 0, 1) ** 2
    return fft_filter(s / (len(freqs) * 2), hi=bright) * e


def whoosh(length=0.5, rise=True, c=(400, 6000)):
    n = int(SR * length); x = np.linspace(0, 1, n)
    shape = x ** 2.4 if rise else (1 - x) ** 1.6 * np.minimum(x / 0.02, 1)
    w = sweep_lp(rng.normal(0, 1, n), *(c if rise else c[::-1]))
    return w * shape * 1.4


def impact(gain=1.0):
    n = int(SR * 2.4); t = np.arange(n) / SR
    f = 38 + 70 * np.exp(-t / 0.05)
    sub = np.sin(2 * np.pi * np.cumsum(f) / SR) * env(n, 0.002, 0.7)
    air = fft_filter(rng.normal(0, 1, n), lo=200, hi=5000) * env(n, 0.001, 0.25) * 0.35
    return np.tanh(1.5 * (sub + air)) * gain


def pop(f0=600, d=0.06):
    n = int(SR * 0.25); t = np.arange(n) / SR
    f = f0 * (1 + 1.2 * np.exp(-t / 0.012))
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * env(n, 0.001, d)


def tick(f=2600, d=0.012):
    n = int(SR * 0.08); t = np.arange(n) / SR
    return np.sin(2 * np.pi * f * t) * env(n, 0.0005, d) + fft_filter(rng.normal(0, 1, n), lo=3000) * env(n, 0.0002, 0.003) * 0.4


def click():
    return tick(1900, 0.014) * 0.9 + tick(5200, 0.005) * 0.5


def key():
    return tick(rng.uniform(1600, 2400), 0.008) * 0.6 + fft_filter(rng.normal(0, 1, int(SR * 0.08)), lo=2000, hi=8000) * env(int(SR * 0.08), 0.0003, 0.006) * 0.5


def ding(f=1318.5, d=0.6):
    n = int(SR * 2.0); t = np.arange(n) / SR
    return (np.sin(2 * np.pi * f * t) + 0.35 * np.sin(2 * np.pi * f * 2.76 * t) * np.exp(-t / 0.08)) * env(n, 0.002, d) * 0.5


def chime(freqs, gap=0.07, d=0.9):
    n = int(SR * 3.0); out = np.zeros(n)
    for k, f in enumerate(freqs):
        s = int(k * gap * SR); dg = ding(f, d)[: n - s]; out[s:s + len(dg)] += dg
    return out / np.sqrt(len(freqs))


def shimmer(length=1.2, f0=2000):
    n = int(SR * length); t = np.arange(n) / SR; s = np.zeros(n)
    for k in range(10):
        f = f0 * 2 ** (rng.uniform(0, 1.5)); s += np.sin(2 * np.pi * f * t + rng.uniform(0, 6)) * (0.5 + 0.5 * np.sin(2 * np.pi * rng.uniform(4, 9) * t))
    return s / 10 * np.sin(np.pi * t / length) ** 2


