"""Synthesises the A&W "2 Can Dine" staff video soundtrack — upbeat 120 bpm groove (Bb–F–Gm–Eb) + sound design locked
to the scene cuts in index.html — and mixes in the voiceover (out/vo/*.wav, placed per out/vo/lines.json) with ducking.
Instruments and mix chain come from ../cinema/score.py.
Usage: python3 score.py out/mix.wav"""
import sys, json, wave, subprocess
import numpy as np

SR = 48000
META = json.load(open('out/vo/lines.json'))
DUR = META['duration']
N = int(SR * DUR)
rng = np.random.default_rng(23)
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





def stab(freqs, d=0.25):
    n = int(SR * 1.2); t = np.arange(n) / SR; s = np.zeros(n)
    for f in freqs:
        for det in (-1.5, 1.5):
            s += sum((1 / h) * np.sin(2 * np.pi * (f + det) * h * t) for h in range(1, 7))
    return np.tanh(1.4 * fft_filter(s / (2 * len(freqs)), hi=4200)) * env(n, 0.002, d)


def ohat():
    n = int(SR * 0.25)
    return fft_filter(rng.normal(0, 1, n), lo=6000) * env(n, 0.001, 0.07)


# ================= TIMELINE (from vo.py / captions.js) =================
lines = META['lines']
S = {l['scene']: l['start'] for l in lines}
caps = json.loads(open('captions.js').read().split('window.CAPTIONS = ')[1].split(';\n')[0])
WT = {c['scene']: [w[1] for w in c['words']] for c in caps}
CUTS = [S[k] - 0.25 for k in ('ask', 'one', 'same', 'addons', 'outro')]
LOCK = WT['outro'][7] + 1.15
BEAT = 0.5; BAR = 4 * BEAT; T0 = 0.5

CH = [('Bb1', ['Bb3', 'D4', 'F4']), ('F1', ['A3', 'C4', 'F4']), ('G1', ['G3', 'Bb3', 'D4']), ('Eb1', ['G3', 'Bb3', 'Eb4'])]
kicks = []


def muted(t):  # drums drop out for the half beat before each cut (the riser takes the space)
    return any(c - 0.5 <= t < c - 0.01 for c in CUTS) or t >= LOCK


# ================= SCORE =================
music.add(whoosh(0.5, True, (200, 9000)), 0.0, 0.35)
music.add(impact(1.0), T0)
b = 0
while T0 + b * BAR < LOCK - 0.01:
    bt = T0 + b * BAR
    root, ch = CH[b % 4]
    fr = [note(n) for n in ch]
    music.add(pad(fr, BAR, a=0.05, r=0.3, bright=2600), bt, 0.10)
    for k in range(8):                       # 8th-note grid
        te = bt + k * BEAT / 2
        if te >= LOCK: break
        on = k % 2 == 0
        if not muted(te):
            if on: kicks.append(te); music.add(kick(1.0), te)
            if k in (2, 6): music.add(clap(), te, 0.34)
            if not on: music.add(ohat(), te, 0.09, pan=0.25)
            for s16 in range(2): music.add(hat(0.015), te + s16 * BEAT / 4, 0.045, pan=-0.3)
        # bouncy bass: root on beats, octave on the "and" of 2 and 4
        bn = note(root) * (2 if k in (3, 7) else 1)
        if k in (0, 1, 3, 4, 6, 7): music.add(bass(bn, BEAT * 0.42), te, 0.2)
        if k in (1, 3, 6): music.add(stab(fr, 0.16), te, 0.11, pan=(-0.3 if k == 3 else 0.3))
    if b >= 2:                               # pluck hook rides on top after the first two bars
        for s16 in range(16):
            ts = bt + s16 * BEAT / 4
            if ts >= LOCK or s16 % 3 == 2: continue
            nm = ch[s16 % 3]; f = note(nm) * 2
            music.add(pluck(f, 0.09, 0.8), ts, 0.035, pan=(0.4 if s16 % 2 else -0.4))
    b += 1

for c in CUTS:                                # riser into every cut, impact on it
    music.add(whoosh(0.5, True, (300, 9000)), c - 0.5, 0.3)
    music.add(impact(0.55), c)

# outro word hits + final lockup resolve
for wi in (0, 2, 4):
    music.add(stab([note('Bb3'), note('D4'), note('F4'), note('Bb4')], 0.35), WT['outro'][wi], 0.14)
music.add(whoosh(0.8, True, (300, 10000)), LOCK - 0.8, 0.35)
music.add(impact(1.0), LOCK)
music.add(pad([note('Bb1'), note('F2'), note('Bb2'), note('D3'), note('F3'), note('A3'), note('C4')], DUR - LOCK - 0.4, a=0.02, r=1.2, bright=3200), LOCK, 0.4)
music.add(chime([note('F5'), note('Bb5'), note('D6'), note('F6')], 0.06, 1.2), LOCK + 0.02, 0.12)
for k, nm in enumerate(['F4', 'Bb4', 'D5', 'F5', 'Bb5']):
    music.add(pluck(note(nm), 0.4), LOCK + 0.25 + k * BEAT / 2, 0.08, pan=(-0.4 if k % 2 else 0.4))

pump = np.ones(N)
for kt in kicks:
    i = int(kt * SR); n = int(SR * 0.25); x = np.arange(min(n, N - i)) / SR
    pump[i:i + len(x)] = np.minimum(pump[i:i + len(x)], 1 - 0.35 * np.exp(-x / 0.08))

# ================= SOUND DESIGN =================
w = WT['hook']
sfx.add(whoosh(0.3, False, (400, 7000)), w[1], 0.2)                       # CAN DINE bar
sfx.add(pop(700, 0.05), w[3], 0.18)                                        # combos chip
sfx.add(impact(0.4), w[5] + 0.05); sfx.add(chime([note('C6'), note('E6'), note('G6')], 0.05, 0.6), w[5] + 0.08, 0.16)  # price
w = WT['ask']
sfx.add(pop(520, 0.06), w[5] - 0.2, 0.2)                                   # bubble
for k in range(5): sfx.add(tick(2400 + 120 * k, 0.01), w[5 + k], 0.08, pan=0.3)
w = WT['one']
sfx.add(whoosh(0.4, False, (500, 7000)), w[3], 0.22, pan=0.6)             # second tray slides in
sfx.add(pop(900, 0.05), w[5], 0.2); sfx.add(ding(2093, 0.3), w[5], 0.07)   # x2
w = WT['same']
sfx.add(whoosh(0.35, False, (500, 6000)), w[3], 0.16)
sfx.add(click(), w[7], 0.5); sfx.add(ding(2637, 0.25), w[7] + 0.02, 0.07)  # COUPON
w = WT['mixed']
sfx.add(whoosh(0.35, False, (500, 6000)), w[0], 0.16)
sfx.add(click(), w[4], 0.5); sfx.add(ding(2349, 0.25), w[4] + 0.02, 0.07)  # MANUAL OVERRIDE
sfx.add(impact(0.5), w[6]); sfx.add(clap(), w[6], 0.25)                    # IN-STORE stamp
w = WT['addons']
for k, wi in enumerate((4, 6, 8, 11)):
    sfx.add(pop(480 + 90 * k, 0.05), w[wi] - 0.08, 0.22, pan=(-0.4 if k % 2 == 0 else 0.4))
    sfx.add(whoosh(0.25, False, (800, 8000)), w[wi] - 0.08, 0.1)
w = WT['outro']
sfx.add(pop(800, 0.06), w[7], 0.2); sfx.add(shimmer(0.8, 2400), w[7], 0.1)

# ================= VOICE =================
for ln in lines:
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', f"out/vo/{ln['i']:02d}.wav", '-af', 'highpass=f=80,acompressor=threshold=-20dB:ratio=3:attack=4:release=60,equalizer=f=3200:t=q:w=1.2:g=2.5',
                          '-ar', str(SR), '-ac', '1', '-f', 'f32le', '-'], capture_output=True, check=True).stdout
    v = np.frombuffer(raw, np.float32).astype(float)
    act = v[np.abs(v) > 0.02 * np.abs(v).max()]          # level-match lines by speech RMS, not peak
    v *= 0.16 / max(1e-6, np.sqrt(np.mean(act ** 2)))
    voice.add(v, ln['start'], 1.0)

# ================= MIX =================
vo_env = np.abs(voice.L + voice.R)
blk = int(SR * 0.01); ve = np.repeat([vo_env[i:i + blk].max() for i in range(0, N, blk)], blk)[:N]
acc = 0.0; att, rel = np.exp(-1 / (0.02 * 100)), np.exp(-1 / (0.3 * 100))
dvals = np.empty(len(range(0, N, blk)))
for j, i in enumerate(range(0, N, blk)):
    target = 1.0 if ve[i] > 0.04 else 0.0
    acc = target + (acc - target) * (att if target > acc else rel); dvals[j] = acc
duck = np.repeat(dvals, blk)[:N]
mgain = (1 - 0.65 * duck) * pump * 0.3
sgain = (1 - 0.5 * duck) * 0.6

ir = reverb_ir(1.6, 6000)
ML = music.L * mgain; MR = music.R * mgain
SL, SRr = sfx.L * sgain, sfx.R * sgain
wetL = convolve(ML * 0.5 + SL * 0.5, ir); wetR = convolve(MR * 0.5 + SRr * 0.5, np.roll(ir, 137))
vwet = convolve(voice.L + voice.R, reverb_ir(0.5, 7000)) * 0.04
L = ML + SL + wetL * 0.18 + voice.L + vwet
R = MR + SRr + wetR * 0.18 + voice.R + vwet
fade = np.clip((DUR - t_all) / 0.4, 0, 1) * np.minimum(t_all / 0.01, 1)
L *= fade; R *= fade
peak = max(np.abs(L).max(), np.abs(R).max())
L, R = np.tanh(L / peak * 1.15) * 0.9, np.tanh(R / peak * 1.15) * 0.9
with wave.open(sys.argv[1], 'wb') as wf:
    wf.setnchannels(2); wf.setsampwidth(2); wf.setframerate(SR)
    wf.writeframes((np.stack([L, R], 1) * 32767).astype('<i2').tobytes())
print('wrote', sys.argv[1], f'{DUR}s')

if len(sys.argv) > 2:  # optional: write voice / bed stems (same gain staging) for balance checks
    for name, (a, b) in {'voice': (voice.L + vwet, voice.R + vwet), 'bed': (ML + SL + wetL * 0.18, MR + SRr + wetR * 0.18)}.items():
        st = np.stack([a * fade / peak, b * fade / peak], 1)
        with wave.open(f"{sys.argv[2]}_{name}.wav", 'wb') as wf:
            wf.setnchannels(2); wf.setsampwidth(2); wf.setframerate(SR); wf.writeframes((np.clip(st, -1, 1) * 32767).astype('<i2').tobytes())
