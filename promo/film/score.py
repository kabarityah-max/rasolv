"""Synthesises the RASOLV film soundtrack — original score + UI sound design synced to index.html — and mixes
in the voiceover (out/vo/*.wav, placed per out/vo/lines.json) with sidechain ducking.
Usage: python3 score.py out/mix.wav"""
import sys, json, wave, subprocess
import numpy as np

SR = 48000
DUR = 38.0
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
BEAT = 0.6                      # 100 bpm
DROP = 10.65                    # downbeat when the dashboard lands
BAR = 4 * BEAT

# --- act 1 (0 – 8.3): tension. low drone, clock tick, uneasy cluster ---
drone = pad([note('D2'), note('A2'), note('D3'), note('E3'), note('F3')], 8.0, a=0.8, r=0.6, bright=900)
music.add(drone, 0.0, 0.55)
for k in range(int(8.0 / (BEAT / 2))):
    tt = k * BEAT / 2
    music.add(hat(0.018), tt, 0.10 if k % 2 else 0.16, pan=0.3 if k % 2 else -0.3)
    if k % 4 == 0: music.add(kick(0.35), tt + 0.0, 1.0)
music.add(pluck(note('A4'), 0.25, 0.4), 0.6, 0.18, -0.2); music.add(pluck(note('Bb4'), 0.25, 0.4), 1.8, 0.16, 0.2)
music.add(pluck(note('A4'), 0.25, 0.4), 3.0, 0.18, -0.2); music.add(pluck(note('E5'), 0.25, 0.4), 4.2, 0.14, 0.2)
music.add(pluck(note('F4'), 0.25, 0.4), 5.4, 0.18, -0.2); music.add(pluck(note('Bb4'), 0.25, 0.4), 6.6, 0.16, 0.2)
# rising tension under "scattered"
music.add(pad([note('D3'), note('Eb3'), note('A3')], 2.2, a=1.8, r=0.3, bright=1600), 5.5, 0.35)

# --- act 2 (8.3 – 10.65): it makes sense. silence after the click, warm chord blooms ---
music.add(pad([note('F2'), note('C3'), note('A3'), note('E4'), note('G4')], 2.3, a=0.9, r=0.4, bright=2600), 8.3, 0.55)
music.add(pluck(note('C5'), 0.4), 8.4, 0.16, -0.3); music.add(pluck(note('E5'), 0.4), 9.0, 0.14, 0.3)
music.add(pluck(note('G5'), 0.4), 9.6, 0.14, -0.3); music.add(pluck(note('A5'), 0.4), 9.85, 0.16, 0.3)

# --- act 3 (10.65 – 31.2): the groove. Fmaj7 – Dm9 – Bbmaj7 – C6, 100 bpm ---
CHORDS = [
    ('F2', ['F3', 'A3', 'C4', 'E4'], ['F4', 'A4', 'C5', 'E5', 'C5', 'A4', 'G4', 'A4']),
    ('D2', ['D3', 'F3', 'A3', 'E4'], ['D4', 'F4', 'A4', 'E5', 'A4', 'F4', 'E4', 'F4']),
    ('Bb1', ['Bb2', 'D3', 'F3', 'A3'], ['Bb3', 'D4', 'F4', 'A4', 'F4', 'D4', 'C4', 'D4']),
    ('C2', ['C3', 'E3', 'G3', 'A3'], ['C4', 'E4', 'G4', 'A4', 'C5', 'A4', 'G4', 'E4']),
]
END3 = 31.2
kicks = []
b = 0
while DROP + b * BAR < END3:
    bt = DROP + b * BAR
    root, ch, arp = CHORDS[b % 4]
    music.add(pad([note(n) for n in ch], BAR, a=0.25, r=0.5, bright=2200 + 400 * min(b, 4)), bt, 0.30)
    for k in range(4):
        tb = bt + k * BEAT
        if tb >= END3: break
        if not (27.6 < tb < 28.0): kicks.append(tb); music.add(kick(0.9), tb)
        if k in (1, 3) and b >= 1: music.add(clap(), tb, 0.22)
        music.add(hat(0.025), tb + BEAT / 2, 0.12, pan=0.25)
        if b >= 2: music.add(hat(0.012), tb + BEAT / 4, 0.05, pan=-0.35); music.add(hat(0.012), tb + 3 * BEAT / 4, 0.05, pan=-0.35)
        for e in (0, 1):  # offbeat-pumping bass (8ths)
            music.add(bass(note(root) * (2 if e and k == 3 else 1), BEAT * 0.42), tb + e * BEAT / 2, 0.20 if e else 0.12)
    for k, nm in enumerate(arp):
        tk = bt + k * BEAT / 2
        if tk < END3: music.add(pluck(note(nm), 0.28, 0.9), tk, 0.13, pan=(-0.35 if k % 2 else 0.35))
    b += 1
# riser into the drop + impact
music.add(whoosh(1.2, True, (300, 9000)), DROP - 1.2, 0.30)
music.add(impact(0.9), DROP)
music.add(chime([note('F5'), note('A5'), note('C6')], 0.05, 1.2), DROP, 0.10)
# break before the stats: suck back + impact at 27.95
music.add(whoosh(0.4, True, (500, 8000)), 27.55, 0.35)
music.add(impact(0.8), 27.95)

# --- act 4 (31.2 – 38): resolution. big Fadd9 bloom, then calm end card ---
music.add(pad([note('F2'), note('C3'), note('G3'), note('A3'), note('C4'), note('G4')], 3.8, a=0.4, r=1.6, bright=3200), 31.2, 0.50)
music.add(pad([note('Bb2'), note('F3'), note('A3'), note('D4'), note('F4')], 2.6, a=0.6, r=1.2, bright=2600), 35.2, 0.40)
for k, nm in enumerate(['C5', 'F5', 'G5', 'A5', 'C6', 'A5', 'G5', 'F5']):
    music.add(pluck(note(nm), 0.4), 32.45 + k * BEAT / 2, 0.11, pan=(-0.4 if k % 2 else 0.4))
for k, nm in enumerate(['F4', 'A4', 'C5', 'D5']):
    music.add(pluck(note(nm), 0.5), 35.3 + k * BEAT, 0.10, pan=(-0.3 if k % 2 else 0.3))

# kick sidechain pump on pads/bass
pump = np.ones(N)
for kt in kicks:
    i = int(kt * SR); n = int(SR * 0.3); x = np.arange(min(n, N - i)) / SR
    pump[i:i + len(x)] = np.minimum(pump[i:i + len(x)], 1 - 0.45 * np.exp(-x / 0.09))

# ================= SOUND DESIGN =================
# act 1
sfx.add(whoosh(0.35, True, (600, 7000)), -0.2, 0.25); sfx.add(pop(380, 0.08), 0.15, 0.45)
for i, d in enumerate([0.6, 0.2, 0.9, 0.4, 1.1, 0.7]):
    sfx.add(ding([1568, 1760, 1318.5, 1975.5, 1480, 1661][i], 0.25), 0.3 + d, 0.10, pan=[-.6, .6, .5, -.5, 0, .1][i])
for i in range(3): sfx.add(pop(520 + 90 * i, 0.05), 0.35 + i * 0.18, 0.25, pan=[-.5, .5, 0][i])
for k in range(10): sfx.add(tick(1500 + 300 * (k % 3), 0.01), 1.6 + k * 0.085, 0.10, pan=0.2)   # cursor rattle
sfx.add(whoosh(0.4, False, (500, 6000)), 2.75, 0.25)
# act 1b: emails / chats / tickets
for i, tt in enumerate([3.12, 3.95, 4.5]):
    sfx.add(pop(700 + 120 * i, 0.05), tt, 0.35); sfx.add(whoosh(0.25, False, (800, 7000)), tt + 0.03, 0.12, pan=[-.6, .6, .4][i])
sfx.add(whoosh(0.4, False, (500, 6000)), 5.4, 0.2)
# scattered tiles + badge chirps
for i in range(10): sfx.add(pop(420 + 60 * i, 0.05), 5.45 + i * 0.09, 0.22, pan=np.sin(i * 1.7) * 0.7)
for k in range(9): sfx.add(ding(2093 + 50 * k, 0.12), 5.9 + k * 0.17, 0.05, pan=np.cos(k) * 0.6)
sfx.add(pop(300, 0.09), 6.98, 0.35)
sfx.add(click(), 7.72, 0.7)
rev = whoosh(0.4, True, (300, 5000)); sfx.add(rev, 7.76, 0.35)
sfx.add(kick(0.5), 8.14)
# act 2
for i, tt in enumerate([8.35, 8.73, 9.12, 9.35, 9.59, 9.82]): sfx.add(tick(1200 + 80 * i, 0.02), tt, 0.10)
sfx.add(whoosh(0.3, False, (2000, 9000)), 9.98, 0.12); sfx.add(tick(3200, 0.03), 10.0, 0.18)
# act 3: dashboard
for i in range(6): sfx.add(whoosh(0.22, False, (1500, 8000)), 12.2 + i * 0.16, 0.07, pan=-0.3); sfx.add(tick(2200, 0.01), 12.2 + i * 0.16, 0.10)
sfx.add(shimmer(0.9, 2500), 14.1, 0.16); sfx.add(chime([note('C6'), note('E6'), note('G6')], 0.06, 0.4), 14.19, 0.07)
for i in range(6): sfx.add(pop(800 + 40 * i, 0.03), 14.95 + i * 0.05, 0.14)
sfx.add(whoosh(0.5, False, (600, 5000)), 15.1, 0.15)
for i in range(6): sfx.add(tick(1700 + 120 * i, 0.012), 16.35 + i * 0.1, 0.14, pan=0.4)
sfx.add(pop(500, 0.08), 17.8, 0.35); sfx.add(chime([note('A5'), note('C6'), note('F6')], 0.06, 0.6), 17.85, 0.12)
sfx.add(whoosh(0.45, False, (500, 6000)), 18.75, 0.2)
# act 3: full resolution
for i, tt in enumerate([19.7, 20.25, 20.8]): sfx.add(pop(600 + 150 * i, 0.04), tt, 0.25)
sfx.add(chime([note('F5'), note('A5'), note('C6'), note('F6')], 0.07, 1.0), 21.35, 0.20)
sfx.add(whoosh(0.4, False, (500, 6000)), 22.15, 0.2)
# act 3: AI
sfx.add(shimmer(1.4, 1800), 22.55, 0.20); sfx.add(whoosh(0.6, True, (400, 6000)), 22.0, 0.15)
for tt in [23.45, 24.9, 26.15]: sfx.add(whoosh(0.3, False, (900, 7000)), tt, 0.14, pan=0.5); sfx.add(pop(900, 0.04), tt + 0.05, 0.18, pan=0.5)
for k in range(44): sfx.add(key(), 23.75 + k * 1.1 / 44 + rng.uniform(-0.01, 0.01), 0.10, pan=0.5)
for i in range(7): sfx.add(tick(1400 + 110 * i, 0.012), 25.05 + i * 0.06, 0.10, pan=0.5)
# act 4: stats
for tt in [28.35, 29.5]: sfx.add(whoosh(0.35, False, (700, 7000)), tt, 0.16)
for k in range(14): sfx.add(tick(2600 - k * 60, 0.006), 28.55 + k * 0.07, 0.07, pan=-0.4)
for i in range(5): sfx.add(ding(1568 * 2 ** (i * 2 / 12), 0.3), 29.8 + i * 0.09, 0.08, pan=0.4)
sfx.add(whoosh(0.4, False, (500, 6000)), 30.85, 0.2)
# act 4: logo + outro
sfx.add(shimmer(1.1, 1600), 31.3, 0.22); sfx.add(whoosh(0.9, True, (300, 7000)), 30.6, 0.18)
sfx.add(impact(0.7), 32.45); sfx.add(whoosh(0.5, False, (600, 8000)), 32.45, 0.22)
sfx.add(whoosh(0.4, True, (500, 6000)), 33.7, 0.12); sfx.add(pop(420, 0.08), 34.45, 0.3)
sfx.add(whoosh(0.5, True, (300, 7000)), 34.3, 0.28); sfx.add(kick(0.6), 34.95)
sfx.add(pop(560, 0.06), 35.5, 0.25)
for k in range(6): sfx.add(key(), 35.95 + k * 0.65 / 6, 0.20)
sfx.add(click(), 36.95, 0.6); sfx.add(chime([note('F5'), note('C6'), note('F6'), note('A6')], 0.06, 1.4), 37.0, 0.18)

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
