"""Synthesises the RASOLV cinematic film soundtrack — dark original score + sound design synced to index.html — and mixes
in the voiceover (out/vo/*.wav, placed per out/vo/lines.json) with sidechain ducking.
Usage: python3 score.py out/mix.wav"""
import sys, json, wave, subprocess
import numpy as np

SR = 48000
DUR = 45.0
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



# ================= SCORE =================
BEAT = 60 / 112.5               # 0.5333 s — "See / Decide / Solve" sit 3 beats apart
BAR = 4 * BEAT
kicks = []


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


Dm9 = ['D3', 'F3', 'A3', 'C4', 'E4']; Bb = ['Bb2', 'D3', 'F3', 'A3', 'C4']; Gm9 = ['G2', 'Bb2', 'D3', 'F3', 'A3']; A7 = ['A2', 'E3', 'G3', 'C#4', 'D4']
PROG = [('D1', Dm9, ['D4', 'F4', 'A4', 'E5']), ('Bb0', Bb, ['Bb3', 'D4', 'F4', 'C5']), ('G1', Gm9, ['G3', 'Bb3', 'D4', 'A4']), ('A1', A7, ['A3', 'C#4', 'E4', 'G4'])]

# --- 0 – 7.4: dark ambience. sub drone, air pad, slow heartbeat ---
music.add(pad([note('D1'), note('A1'), note('D2')], 7.6, a=1.5, r=1.0, bright=500), 0.0, 0.9)
music.add(pad([note('A3'), note('D4'), note('E4'), note('F4')], 7.2, a=2.5, r=1.0, bright=1800), 0.3, 0.22)
for k in range(7): music.add(kick(0.35), 0.4 + k * 2 * BEAT * 1.0, 0.8); music.add(kick(0.2), 0.4 + k * 2 * BEAT + 0.18, 0.6)
music.add(shimmer(3.0, 3000), 1.5, 0.05); music.add(shimmer(3.0, 2600), 4.4, 0.05)
# --- 7.35 – 8.45 beams riser, 8.45 logo impact + bloom ---
music.add(whoosh(1.1, True, (200, 9000)), 7.35, 0.35)
music.add(impact(1.0), 8.45)
music.add(pad([note('D2'), note('A2'), note('F3'), note('C4'), note('E4'), note('A4')], 2.2, a=0.05, r=1.6, bright=3200), 8.45, 0.55)
music.add(chime([note('A5'), note('D6'), note('E6')], 0.06, 1.4), 8.5, 0.10)
# --- 10.5 – 14.4: sphere rises, filtered 16th arp creeps in ---
music.add(pad([note('D1'), note('A1'), note('D2'), note('A2')], 4.0, a=1.2, r=0.6, bright=700), 10.5, 0.8)
music.add(whoosh(2.2, True, (150, 2500)), 10.4, 0.25)
t0 = 11.2
for k in range(int((14.45 - t0) / (BEAT / 4))):
    nm = ['D4', 'F4', 'A4', 'E5'][k % 4]
    music.add(pluck(note(nm), 0.12, 0.3 + 0.7 * k / 24), t0 + k * BEAT / 4, 0.05 + 0.06 * k / 24, pan=0.3 if k % 2 else -0.3)
music.add(whoosh(0.9, True, (300, 8000)), 13.55, 0.3)
# --- 14.45 – 24.45: main groove (half-time), progression Dm9 – Bbmaj9 – Gm9 – A7sus ---
def groove(start, end, full=True, drums=True):
    b = 0
    while start + b * BAR < end - 0.01:
        bt = start + b * BAR
        root, ch, arp = PROG[b % 4]
        music.add(pad([note(n) for n in ch], BAR, a=0.3, r=0.6, bright=2000), bt, 0.26)
        for s16 in range(16):
            ts = bt + s16 * BEAT / 4
            if ts >= end: break
            music.add(pluck(note(arp[s16 % 4]) * (2 if s16 % 8 == 7 else 1), 0.12, 0.9), ts, 0.07 if s16 % 4 else 0.10, pan=0.35 if s16 % 2 else -0.35)
        for k in range(4):
            tb = bt + k * BEAT
            if tb >= end: break
            if drums:
                if k in (0, 2) or (full and k == 3 and b % 2): kicks.append(tb); music.add(kick(0.95), tb)
                if k == 2 and full: music.add(clap(), tb, 0.26)
                music.add(hat(0.02), tb + BEAT / 2, 0.10, pan=0.3)
            music.add(bass(note(root), BEAT * 0.9), tb, 0.22 if drums else 0.12)
        b += 1
groove(14.45, 24.45)
# --- 24.45 – 28.2: breakdown, no drums ---
music.add(impact(0.5), 24.45)
groove(24.45, 28.2, drums=False)
music.add(whoosh(1.0, True, (300, 7000)), 27.2, 0.22)
# --- 28.2 – 32.95: build — four-on-the-floor + snare roll + riser ---
groove(28.2, 32.95, full=True)
for k in range(int(4.0 / BEAT)): kicks.append(28.2 + k * BEAT + 0.0)
roll_t = 31.25
while roll_t < 32.9:
    gap = BEAT / 2 if roll_t < 31.9 else (BEAT / 4 if roll_t < 32.45 else BEAT / 8)
    music.add(clap(), roll_t, 0.12 + 0.18 * (roll_t - 31.25) / 1.65); roll_t += gap
music.add(whoosh(1.7, True, (200, 10000)), 31.25, 0.35)
# --- 32.95 / 34.55 / 36.2 word hits, 36.85 the big one ---
for tt, ch in [(32.95, ['D3', 'A3', 'D4', 'F4']), (34.55, ['Bb2', 'F3', 'Bb3', 'D4']), (36.15, ['G2', 'D3', 'G3', 'Bb3'])]:
    music.add(impact(0.45), tt); music.add(stab([note(n) for n in ch], 0.6), tt, 0.18)
    music.add(pad([note(n) for n in ch], 1.4, a=0.02, r=0.8, bright=2600), tt, 0.25)
music.add(whoosh(0.6, True, (300, 9000)), 36.25, 0.3)
music.add(impact(1.0), 36.85); music.add(stab([note('A2'), note('E3'), note('A3'), note('C#4'), note('E4')], 0.9), 36.85, 0.34)
groove(36.85, 39.45, full=True)
# --- 39.45 – 40.75 glitch: stutters + tape-stop; 40.75 clean logo hit ---
for k in range(6): music.add(glitch(0.12 + 0.05 * (k % 3)), 39.45 + k * 0.2, 0.18, pan=(-0.5 if k % 2 else 0.5))
music.add(whoosh(0.9, True, (400, 9000)), 39.85, 0.25)
music.add(impact(1.0), 40.75); music.add(chime([note('D6'), note('A6')], 0.04, 1.0), 40.78, 0.10)
# --- 41.55 – 45: wordmark — resolve to D major (it "solves") ---
music.add(pad([note('D2'), note('A2'), note('D3'), note('F#3'), note('A3'), note('E4'), note('A4')], 2.6, a=0.15, r=2.2, bright=3000), 41.55, 0.55)
for k, nm in enumerate(['A4', 'D5', 'E5', 'F#5', 'A5']): music.add(pluck(note(nm), 0.45), 41.6 + k * BEAT / 2, 0.09, pan=(-0.4 if k % 2 else 0.4))
music.add(pad([note('D1'), note('A1')], 3.0, a=0.1, r=1.4, bright=400), 41.55, 0.7)

pump = np.ones(N)
for kt in kicks:
    i = int(kt * SR); n = int(SR * 0.3); x = np.arange(min(n, N - i)) / SR
    pump[i:i + len(x)] = np.minimum(pump[i:i + len(x)], 1 - 0.4 * np.exp(-x / 0.09))

# ================= SOUND DESIGN =================
for tt in [0.5, 0.71, 0.93, 1.28, 1.49, 1.71, 1.92, 2.27, 4.4, 4.64, 4.88, 5.13]: sfx.add(tick(1400 + rng.uniform(-200, 200), 0.02), tt, 0.08)
sfx.add(whoosh(1.2, False, (300, 3000)), 0.3, 0.12, pan=0.6); sfx.add(whoosh(0.7, True, (300, 5000)), 3.4, 0.15)
sfx.add(whoosh(0.6, False, (400, 6000)), 4.0, 0.18, pan=-0.5)
for i, a in enumerate([7.35, 7.45, 7.6, 7.7]): sfx.add(whoosh(0.9, False, (600, 9000)), a, 0.14, pan=[-.7, .7, -.4, .4][i])
for i in range(7): sfx.add(pop(500 + 70 * i, 0.04), 11.2 + i * 0.07, 0.12, pan=np.cos(i) * 0.6)
sfx.add(whoosh(0.6, True, (500, 7000)), 12.75, 0.18); sfx.add(click(), 13.42, 0.5); sfx.add(ding(2637, 0.3), 13.45, 0.08)
sfx.add(whoosh(0.9, True, (200, 4000)), 13.6, 0.18)
for tt in [14.45, 14.6, 14.75, 14.9, 15.05, 15.2, 15.35, 15.5, 15.65, 15.8, 15.95, 16.1]: sfx.add(tick(2600 + rng.uniform(-300, 300), 0.01), tt, 0.07, pan=rng.uniform(-.6, .6))
for tt in [14.3, 14.75, 15.31, 15.89, 17.1]: sfx.add(ding(1760, 0.35), tt, 0.07); sfx.add(pop(900, 0.03), tt, 0.12)
sfx.add(click(), 4.88, 0.35); sfx.add(ding(2349, 0.3), 4.9, 0.06)
sfx.add(whoosh(0.5, False, (500, 6000)), 19.05, 0.16)
for tt in [19.5, 19.55, 19.7, 19.85, 19.95, 20.05, 20.15, 20.25, 22.55, 22.7]: sfx.add(tick(2200 + rng.uniform(-300, 300), 0.01), tt, 0.08, pan=rng.uniform(-.6, .6))
for k in range(22): sfx.add(tick(3200 - k * 50, 0.004), 19.7 + k * 0.075, 0.04)
sfx.add(click(), 20.02, 0.6); sfx.add(ding(2637, 0.3), 20.06, 0.06)
sfx.add(chime([note('D6'), note('F#6'), note('A6')], 0.06, 0.7), 22.58, 0.11)
sfx.add(whoosh(0.5, False, (400, 7000)), 24.15, 0.2)
for i in range(4): sfx.add(ding(2093 * 2 ** (i * 3 / 12), 0.25), 24.5 + i * 0.05, 0.06, pan=[-.5, .5, .5, -.5][i])
sfx.add(whoosh(0.7, True, (2000, 9000)), 25.25, 0.06)
sfx.add(whoosh(0.4, True, (500, 6000)), 25.85, 0.14); sfx.add(click(), 26.2, 0.35); sfx.add(shimmer(1.4, 2200), 26.25, 0.10)
sfx.add(whoosh(0.5, False, (500, 6000)), 27.8, 0.16)
for i in range(6): sfx.add(pop(380 + 40 * i, 0.04), 28.55 + i * 0.12, 0.10)
sfx.add(whoosh(0.4, False, (600, 6000)), 29.85, 0.12); sfx.add(click(), 31.03, 0.25)
sfx.add(whoosh(1.0, False, (300, 3000)), 32.2, 0.2)
for i in range(4): sfx.add(whoosh(0.4, False, (1500, 9000)), 34.5 + i * 0.22, 0.12, pan=np.cos(i * 1.3) * 0.7)
for i in range(6): sfx.add(tick(1800 + 150 * i, 0.012), 35.75 + i * 0.09, 0.12, pan=np.sin(i) * 0.6)
sfx.add(whoosh(0.8, False, (300, 9000)), 36.85, 0.3)
sfx.add(whoosh(0.5, False, (500, 6000)), 38.95, 0.18)
sfx.add(whoosh(0.4, True, (500, 8000)), 41.2, 0.15)
for i in range(6): sfx.add(tick(1500 + 90 * i, 0.012), 41.7 + i * 0.08, 0.06)

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
mgain = (1 - 0.6 * duck) * pump * 0.55
sgain = (1 - 0.4 * duck) * 0.75

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
