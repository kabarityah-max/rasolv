"""Synthesises the RASOLV prompt-reel soundtrack — original 120 BPM score + sound design synced to index.html — and mixes
in the voiceover (out/vo/*.wav, placed per out/vo/lines.json) with sidechain ducking. Instruments and mix bus are the
same as ../bilingual/score.py. Cue times come from the voiceover word timings in captions.js, like the picture.
Usage: python3 score.py out/mix.wav [stem_prefix]"""
import sys, json, wave, subprocess
import numpy as np

SR = 48000
DUR = 31.5
N = int(SR * DUR)
rng = np.random.default_rng(23)
t_all = np.arange(N) / SR
CAP = json.loads(open('captions.js').read().split('window.CAPTIONS = ', 1)[1].split(';\n', 1)[0])
W = lambda li, wi: CAP[li]['words'][wi][1]


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



def glitch(length=0.4):
    n = int(SR * length); x = rng.normal(0, 1, n)
    hold = int(SR / 900); x = np.repeat(x[::hold], hold)[:n]           # sample-and-hold crunch
    gate = (np.floor(np.arange(n) / (SR * 0.03)) % 2 == 0).astype(float)
    return fft_filter(x, lo=300, hi=7000) * gate * np.linspace(1, 0.2, n)


def stab(freqs, d=0.5):
    n = int(SR * 2.5); t = np.arange(n) / SR; s = np.zeros(n)
    for f in freqs:
        s += sum((1 / h) * np.sin(2 * np.pi * f * h * t) for h in range(1, 6))
    return np.tanh(fft_filter(s / len(freqs), hi=3500)) * env(n, 0.003, d)



# ================= SCORE =================
BEAT = 0.5                      # 120 BPM; montage cuts land every 2 beats
BAR = 4 * BEAT
kicks = []
Dm = ['D3', 'F3', 'A3', 'C4', 'E4']; Bb = ['Bb2', 'D3', 'F3', 'A3', 'C4']; Gm = ['G2', 'Bb2', 'D3', 'F3', 'A3']; A7 = ['A2', 'E3', 'G3', 'C#4', 'D4']
PROG = [('D1', Dm, ['D4', 'F4', 'A4', 'E5']), ('Bb0', Bb, ['Bb3', 'D4', 'F4', 'C5']), ('G1', Gm, ['G3', 'Bb3', 'D4', 'A4']), ('A1', A7, ['A3', 'C#4', 'E4', 'G4'])]


def groove(start, end, full=True, drums=True, arp=True, lvl=1.0):
    b = 0
    while start + b * BAR < end - 0.01:
        bt = start + b * BAR
        root, ch, ar = PROG[b % 4]
        music.add(pad([note(n) for n in ch], min(BAR, end - bt), a=0.2, r=0.5, bright=2200), bt, 0.22 * lvl)
        if arp:
            for s16 in range(16):
                ts = bt + s16 * BEAT / 4
                if ts >= end: break
                music.add(pluck(note(ar[s16 % 4]) * (2 if s16 % 8 == 7 else 1), 0.11, 0.9), ts, (0.06 if s16 % 4 else 0.09) * lvl, pan=0.35 if s16 % 2 else -0.35)
        for k in range(4):
            tb = bt + k * BEAT
            if tb >= end: break
            if drums:
                if full or k in (0, 2): kicks.append(tb); music.add(kick(0.95), tb, lvl)
                if k in (1, 3) and full: music.add(clap(), tb, 0.24 * lvl)
                music.add(hat(0.02), tb + BEAT / 2, 0.11 * lvl, pan=0.3)
                if full: music.add(hat(0.012), tb + BEAT / 4, 0.05 * lvl, pan=-0.3); music.add(hat(0.012), tb + 3 * BEAT / 4, 0.05 * lvl, pan=-0.3)
            music.add(bass(note(root), BEAT * 0.85), tb, (0.24 if drums else 0.14) * lvl)
        b += 1


def tape_stop(sig, length):
    """Slows a signal to a halt (vinyl/tape stop)."""
    n = int(SR * length); rate = np.linspace(1, 0, n) ** 1.3
    pos = np.cumsum(rate); pos = pos[pos < len(sig) - 1]
    i = pos.astype(int); f = pos - i
    return (sig[i] * (1 - f) + sig[i + 1] * f) * np.linspace(1, 0.3, len(pos))


# --- 0 – 1.72 hook: one slam per word ---
music.add(pad([note('D1'), note('A1'), note('D2')], 1.9, a=0.01, r=0.4, bright=600), 0.0, 0.8)
for i in range(4):
    h = max(0.0, W(0, i) - 0.04)
    music.add(impact(0.8 if i < 3 else 1.0), h); music.add(stab([note(n) for n in (['D3', 'A3', 'D4'] if i < 3 else ['D3', 'A3', 'D4', 'F4', 'A4'])], 0.35), h, 0.16 + 0.05 * i)
    kicks.append(h)
music.add(whoosh(0.35, True, (500, 9000)), 1.3, 0.25)
# --- 1.72 – 5.5: half-time groove under "No After Effects…", riser into the drop ---
groove(1.72, 5.5 - 0.02, full=False, arp=False, lvl=0.85)
music.add(whoosh(1.4, True, (200, 12000)), 4.1, 0.4)
roll = 4.5
while roll < 5.48:
    gap = BEAT / 2 if roll < 4.9 else (BEAT / 4 if roll < 5.25 else BEAT / 8)
    music.add(clap(), roll, 0.1 + 0.18 * (roll - 4.5)); roll += gap
# --- 5.5 – 11.5: the drop — full groove under the montage ---
music.add(impact(1.0), 5.5)
groove(5.5, 11.5, full=True)
# --- 11.5: freeze — tape stop, then silence + heartbeat ---
ts_src = np.zeros(int(SR * 1.2)); ts_src += stab([note('D3'), note('A3'), note('D4'), note('F4')], 0.8)[:len(ts_src)] * 0.5
ts_src[: int(SR * 0.5)] += bass(note('D2'), 0.5) * 0.4
music.add(tape_stop(ts_src, 0.75), 11.5, 0.5)
for hb in (12.35, 12.62, 13.15, 13.42): music.add(kick(0.55), hb, 0.7)
music.add(pad([note('D1'), note('A1')], 1.9, a=0.6, r=0.4, bright=300), 11.7, 0.5)
# --- 13.3 – 17.0: terminal — soft pulse, then build ---
music.add(pad([note('D2'), note('A2'), note('F3'), note('C4')], 3.7, a=0.4, r=0.4, bright=1400), 13.3, 0.22)
for k in range(int((17.0 - 14.0) / (BEAT / 2))):
    tt = 14.0 + k * BEAT / 2
    music.add(pluck(note(['D4', 'A4', 'F4', 'C5'][k % 4]), 0.1, 0.4 + 0.6 * k / 12), tt, 0.03 + 0.05 * k / 12, pan=0.3 if k % 2 else -0.3)
for k in range(8): kicks.append(15.0 + k * BEAT / 2); music.add(kick(0.5), 15.0 + k * BEAT / 4 * (2 if k < 4 else 1) + (0 if k < 4 else 1.0), 0.5)
music.add(whoosh(1.2, True, (200, 12000)), 15.8, 0.42)
# --- 17.0: ONE PROMPT. — main drop ---
music.add(impact(1.0), 17.0); music.add(stab([note('D3'), note('A3'), note('D4'), note('F4'), note('A4')], 0.8), 17.0, 0.3)
music.add(impact(0.5), W(9, 3))
groove(17.0, 22.9, full=True)
music.add(whoosh(0.8, True, (300, 9000)), 22.1, 0.3)
# --- 22.9 – 25.35: lighter (no claps) under "motion graphics … now" ---
music.add(impact(0.7), 22.9)
groove(22.9, 25.35, full=False, lvl=0.9)
music.add(impact(0.7), W(11, 7) + 0.15); music.add(stab([note('D3'), note('F#3'), note('A3'), note('D4')], 0.6), W(11, 7) + 0.15, 0.22)
# --- 25.35 – 29.2: CTA groove ---
groove(25.35, 29.2, full=True, lvl=0.9)
music.add(whoosh(0.9, True, (300, 9000)), 28.3, 0.3)
# --- 29.2 – 31.5: logo — resolve to D major ---
L0 = W(13, 0)
music.add(impact(1.0), L0); kicks.append(L0)
music.add(pad([note('D2'), note('A2'), note('D3'), note('F#3'), note('A3'), note('E4'), note('A4')], 1.8, a=0.1, r=1.4, bright=3000), L0, 0.5)
music.add(pad([note('D1'), note('A1')], 2.0, a=0.1, r=1.0, bright=400), L0, 0.6)
music.add(chime([note('D6'), note('F#6'), note('A6')], 0.05, 1.2), L0 + 0.03, 0.1)
for k, nm in enumerate(['A4', 'D5', 'E5', 'F#5', 'A5']): music.add(pluck(note(nm), 0.45), L0 + 0.1 + k * BEAT / 2, 0.08, pan=(-0.4 if k % 2 else 0.4))

pump = np.ones(N)
for kt in kicks:
    i = int(kt * SR); n = int(SR * 0.3); x = np.arange(min(n, N - i)) / SR
    pump[i:i + len(x)] = np.minimum(pump[i:i + len(x)], 1 - 0.4 * np.exp(-x / 0.09))

# ================= SOUND DESIGN =================
for i in range(4): sfx.add(whoosh(0.3, False, (600, 8000)), max(0, W(0, i) - 0.08), 0.14, pan=(-.5 if i % 2 else .5))
sfx.add(whoosh(0.4, True, (800, 10000)), 1.5, 0.2)
for i, (wn, wo) in enumerate([(0, 1), (3, 4), (5, 6)]):
    sfx.add(whoosh(0.35, False, (500, 7000)), W(1, wn) - 0.15, 0.2, pan=0.6)
    sfx.add(whoosh(0.18, True, (2000, 10000)), W(1, wo) + 0.2, 0.18, pan=-0.3)     # strike swipe
    sfx.add(pop(700, 0.05), W(1, wo) + 0.36, 0.2)
for i in range(1, 6): sfx.add(whoosh(0.3, True, (800, 10000)), 5.5 + i - 0.25, 0.22, pan=(-.5 if i % 2 else .5)); sfx.add(click(), 5.5 + i, 0.3)
for k in range(10): sfx.add(tick(1800 + 120 * k, 0.01), 5.55 + k * 0.08, 0.07, pan=np.sin(k) * 0.6)                 # kinetic type
sfx.add(whoosh(0.9, False, (300, 5000)), 6.5, 0.22, pan=-0.6); sfx.add(whoosh(0.6, True, (400, 6000)), 6.75, 0.12, pan=0.6)  # 3D
for k in range(3): sfx.add(pop(500 + 120 * k, 0.04), 6.62 + k * 0.1, 0.14)
sfx.add(shimmer(1.0, 2500), 7.5, 0.16); sfx.add(whoosh(0.7, True, (500, 9000)), 7.6, 0.15); sfx.add(chime([note('A5'), note('D6')], 0.05, 0.6), 8.15, 0.07)  # particles
for k, a in enumerate([0.2, 0.42, 0.64, 0.84]): sfx.add(pop(380 + 90 * k, 0.07), 8.5 + a, 0.2)                     # morphs
for k in range(7): sfx.add(tick(1200 + 180 * k, 0.015), 9.54 + k * 0.05, 0.12)                                   # data
for k in range(22): sfx.add(tick(3000 + k * 40, 0.004), 9.6 + k * 0.03, 0.04)
for k in range(6): sfx.add(glitch(0.1 + 0.05 * (k % 3)), 10.5 + k * 0.16, 0.2, pan=(-0.5 if k % 2 else 0.5))       # glitch
sfx.add(whoosh(0.6, False, (300, 4000)), 11.5, 0.15)
sfx.add(whoosh(0.5, True, (300, 6000)), 13.15, 0.12)
t = 13.72; k = 0
while t < 15.7:
    sfx.add(key(), t, 0.22, pan=rng.uniform(-.3, .3)); t += 0.045 + 0.025 * rng.random(); k += 1
sfx.add(click(), 15.82, 0.55); sfx.add(tick(900, 0.03), 15.82, 0.2)
for tt in (16.25, 16.42, 16.59, 16.76): sfx.add(tick(2400, 0.012), tt, 0.1); sfx.add(pop(900, 0.03), tt, 0.08)
for tt in (W(10, 3), W(10, 5), W(10, 6)): sfx.add(ding(1760, 0.3), tt + 0.15, 0.07); sfx.add(pop(900, 0.03), tt + 0.15, 0.12)
for k in range(30): sfx.add(tick(2000 + k * 50, 0.004), W(10, 9) + k * 0.033, 0.035)
sfx.add(chime([note('D6'), note('F#6'), note('A6')], 0.06, 0.7), 22.7, 0.1)
sfx.add(whoosh(0.4, True, (800, 9000)), 22.75, 0.2)
for k in range(14): sfx.add(tick(1500 + 60 * k, 0.008), W(11, 5) + k * 0.06, 0.08)                                # year slot
sfx.add(whoosh(0.4, False, (500, 6000)), 25.1, 0.18)
for i in range(4): sfx.add(pop(450 + 60 * i, 0.04), W(12, i), 0.12)
for k in range(6): sfx.add(key(), W(12, 4) + k * 0.05, 0.3)
send = W(12, 6) - 0.05
sfx.add(click(), send, 0.5); sfx.add(pop(800, 0.05), send + 0.02, 0.2); sfx.add(pop(1300, 0.04), send + 0.4, 0.16)
sfx.add(whoosh(0.6, True, (600, 9000)), send + 0.1, 0.2, pan=-0.4)
sfx.add(ding(1568, 0.4), W(12, 8), 0.12); sfx.add(ding(2093, 0.4), W(12, 8) + 0.09, 0.1)
sfx.add(whoosh(0.5, True, (400, 9000)), L0 - 0.4, 0.18)
for i in range(6): sfx.add(tick(1500 + 90 * i, 0.012), L0 + 0.35 + i * 0.08, 0.06)
sfx.add(pop(600, 0.05), L0 + 0.3, 0.15)

# ================= VOICE =================
lines = json.load(open('out/vo/lines.json'))['lines']
for ln in lines:
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', f"out/vo/{ln['i']:02d}.wav", '-af', 'highpass=f=70,acompressor=threshold=-20dB:ratio=2.5:attack=5:release=80,equalizer=f=3500:t=q:w=1.2:g=2',
                          '-ar', str(SR), '-ac', '1', '-f', 'f32le', '-'], capture_output=True, check=True).stdout
    v = np.frombuffer(raw, np.float32).astype(float)
    v /= max(1e-6, np.abs(v).max())
    voice.add(v, ln['start'], 0.9)

# ================= MIX =================
vo_env = np.abs(voice.L + voice.R)
blk = int(SR * 0.01); ve = np.repeat([vo_env[i:i + blk].max() for i in range(0, N, blk)], blk)[:N]
duck = np.zeros(N); acc = 0.0
att, rel = np.exp(-1 / (0.02 * 100)), np.exp(-1 / (0.35 * 100))
dvals = np.empty(len(range(0, N, blk)))
for j, i in enumerate(range(0, N, blk)):
    target = 1.0 if ve[i] > 0.04 else 0.0
    acc = target + (acc - target) * (att if target > acc else rel); dvals[j] = acc
duck = np.repeat(dvals, blk)[:N]
mgain = (1 - 0.72 * duck) * pump * 0.42
sgain = (1 - 0.5 * duck) * 0.6

ir = reverb_ir(2.4, 6000)
ML = music.L * mgain; MR = music.R * mgain
SL, SRr = sfx.L * sgain, sfx.R * sgain
wetL = convolve(ML * 0.6 + SL * 0.5, ir); wetR = convolve(MR * 0.6 + SRr * 0.5, np.roll(ir, 137))
vwet = convolve(voice.L + voice.R, reverb_ir(0.6, 7000)) * 0.05
L = ML + SL + wetL * 0.22 + voice.L + vwet
R = MR + SRr + wetR * 0.22 + voice.R + vwet
fade = np.clip((DUR - t_all) / 0.5, 0, 1) * np.minimum(t_all / 0.02, 1)
L *= fade; R *= fade
peak = max(np.abs(L).max(), np.abs(R).max())
L, R = np.tanh(L / peak * 1.1) * 0.9, np.tanh(R / peak * 1.1) * 0.9
out = np.stack([L, R], 1)
with wave.open(sys.argv[1], 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((out * 32767).astype('<i2').tobytes())
print('wrote', sys.argv[1])

if len(sys.argv) > 2:  # optional: write voice / bed stems (same gain staging) for balance checks
    for name, (a, b) in {'voice': (voice.L + vwet, voice.R + vwet), 'bed': (ML + SL + wetL * 0.22, MR + SRr + wetR * 0.22)}.items():
        st = np.stack([a * fade / peak, b * fade / peak], 1)
        with wave.open(f"{sys.argv[2]}_{name}.wav", 'wb') as w:
            w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.clip(st, -1, 1) * 32767).astype('<i2').tobytes())
