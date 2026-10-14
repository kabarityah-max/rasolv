"""Synthesises the RASOLV "support receipt" short's soundtrack: a tense A-minor groove while the bill adds up,
a stop on "So here's the fix", then a brighter C-major groove for the RASOLV half; plus sound design locked to
index.html (receipt printer, notification pops, stamps, typing, live-update dings) and the voiceover with ducking.
Instruments and mix chain come from ../aw2candine/score.py.
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
caps = json.loads(open('captions.js').read().split('window.CAPTIONS = ')[1].split(';\n')[0])
WT = {c['scene']: [w[1] for w in c['words']] for c in caps}
S = {l['scene']: l['start'] - 0.25 for l in lines}
CUTS = [S[k] for k in ('hold', 'bot', 'transfer', 'ticket', 'refund', 'per', 'year', 'rasolv', 'solve', 'clear', 'outro')]
FIX = WT['fix'][3]
BREAK = (S['fix'] + 0.25, S['rasolv'])          # music stops for "So here's the fix."
LOCK = WT['outro'][0] - 0.05
BEAT = 0.5; BAR = 4 * BEAT; T0 = 0.5

MINOR = [('A1', ['A3', 'C4', 'E4']), ('F1', ['F3', 'A3', 'C4']), ('D2', ['D3', 'F3', 'A3']), ('E1', ['E3', 'Ab3', 'B3'])]
MAJOR = [('C2', ['C4', 'E4', 'G4']), ('G1', ['B3', 'D4', 'G4']), ('A1', ['A3', 'C4', 'E4']), ('F1', ['A3', 'C4', 'F4'])]
kicks = []


def muted(t):
    return any(c - 0.5 <= t < c - 0.01 for c in CUTS) or BREAK[0] <= t < BREAK[1] or t >= LOCK


def groove(t_start, t_end, CH, bright):
    b = 0
    while t_start + b * BAR < t_end - 0.01:
        bt = t_start + b * BAR
        root, ch = CH[b % 4]; fr = [note(n) for n in ch]
        music.add(pad(fr, min(BAR, t_end - bt), a=0.05, r=0.3, bright=2000 + 1200 * bright), bt, 0.10)
        for k in range(8):
            te = bt + k * BEAT / 2
            if te >= t_end: break
            if not muted(te):
                if k % 2 == 0: kicks.append(te); music.add(kick(1.0), te)
                if k in (2, 6): music.add(clap(), te, 0.3)
                for s16 in range(2): music.add(hat(0.015), te + s16 * BEAT / 4, 0.04 + 0.015 * bright, pan=-0.3)
                if bright and k % 2: music.add(ohat(), te, 0.08, pan=0.25)
                bn = note(root) * (2 if k in (3, 7) else 1)
                if k in (0, 3, 4, 6, 7): music.add(bass(bn, BEAT * 0.4), te, 0.2)
            if bright and k in (1, 3, 6) and not muted(te): music.add(stab(fr, 0.16), te, 0.1, pan=(-0.3 if k == 3 else 0.3))
        for s16 in range(16):                           # plucked arp: sparse + dark first, busy + bright after the fix
            ts = bt + s16 * BEAT / 4
            if ts >= t_end or muted(ts) or (not bright and s16 % 4 == 3) or (bright and s16 % 3 == 2): continue
            music.add(pluck(note(ch[s16 % 3]) * 2, 0.09, 0.5 + 0.5 * bright), ts, 0.03, pan=(0.4 if s16 % 2 else -0.4))
        b += 1


# ================= SCORE =================
music.add(impact(0.9), T0)
groove(T0, BREAK[0], MINOR, 0)
groove(BREAK[1], LOCK, MAJOR, 1)
for c in CUTS:
    music.add(whoosh(0.45, True, (300, 8000)), c - 0.45, 0.22)
    music.add(impact(0.35), c)
# the fix: countdown ticks into a stop, riser into the RASOLV drop
for k in range(4): music.add(tick(2200, 0.012), FIX - 1.5 + k * 0.5, 0.25)
music.add(chime([note('E5'), note('A5'), note('Db6')], 0.05, 0.6), FIX, 0.14)
music.add(whoosh(1.0, True, (200, 10000)), BREAK[1] - 1.0, 0.4)
music.add(impact(1.0), BREAK[1])
# outro resolve
music.add(whoosh(0.8, True, (300, 10000)), LOCK - 0.8, 0.35)
music.add(impact(1.0), LOCK)
music.add(pad([note('C2'), note('G2'), note('C3'), note('E3'), note('G3'), note('B3'), note('D4')], DUR - LOCK - 0.4, a=0.02, r=1.2, bright=3200), LOCK, 0.4)
music.add(chime([note('G5'), note('C6'), note('E6'), note('G6')], 0.06, 1.2), LOCK + 0.02, 0.12)

pump = np.ones(N)
for kt in kicks:
    i = int(kt * SR); n = int(SR * 0.25); x = np.arange(min(n, N - i)) / SR
    pump[i:i + len(x)] = np.minimum(pump[i:i + len(x)], 1 - 0.35 * np.exp(-x / 0.08))

# ================= SOUND DESIGN =================
def printer(t, n=10):                                  # thermal receipt printer: fast dotted ticks
    for k in range(n): sfx.add(tick(rng.uniform(3200, 4200), 0.004), t + k * 0.028, 0.12, pan=0.2)

w = WT['hook']
printer(w[3] - 0.2, 16)
for wi in (1, 3, 5, 6): sfx.add(pop(700, 0.05), w[wi] - 0.1, 0.16, pan=-0.3)          # notifications
w = WT['intro']; sfx.add(pop(900, 0.05), w[4], 0.18)                                      # countdown pill
for scene, wi in (('hold', 4), ('bot', 3), ('transfer', 0), ('ticket', 6), ('refund', 2), ('year', 1)):
    printer(WT[scene][wi]); sfx.add(ding(1760, 0.15), WT[scene][wi] + 0.3, 0.05)
for wi in (2, 4, 5, 6): sfx.add(pop(560, 0.05), WT['bot'][wi], 0.15, pan=(0.3 if wi in (5,) else -0.3))
sfx.add(whoosh(0.4, False, (600, 7000)), WT['bot'][7], 0.12)
for wi in (1, 5): sfx.add(whoosh(0.35, False, (500, 7000)), WT['transfer'][wi], 0.16, pan=0.5)
sfx.add(impact(0.4), WT['transfer'][6]); sfx.add(clap(), WT['transfer'][6], 0.2)
for i in range(5): sfx.add(tick(1500, 0.02), WT['ticket'][6] + .1 + i * .18, 0.18)
sfx.add(impact(0.7), WT['per'][6] - 0.05); sfx.add(clap(), WT['per'][6] - 0.05, 0.35)     # PER PROBLEM stamp
for i in range(12): sfx.add(tick(2000 + 60 * i, 0.01), S['year'] + 0.1 + i * 0.11, 0.07)
w = WT['rasolv']
t0, t1 = w[1], w[4] + 0.2
for k in range(21): sfx.add(key(), t0 + (t1 - t0) * k / 21, 0.22)                        # typing
for i in range(5): sfx.add(pop(800 + 60 * i, 0.04), w[5] + i * 0.16, 0.12)                # AI signals
w = WT['match']; sfx.add(chime([note('C6'), note('E6'), note('G6')], 0.05, 0.6), w[3], 0.13); sfx.add(pop(900, 0.05), w[5], 0.18)
w = WT['solve']
for wi in (1, 3): sfx.add(ding(1568, 0.3), w[wi], 0.08)
sfx.add(chime([note('C6'), note('E6'), note('G6'), note('C7')], 0.05, 0.8), w[4], 0.14)
w = WT['clear']
for i in range(6): sfx.add(whoosh(0.15, False, (1500, 9000)), w[0] + i * 0.14, 0.08)       # strike-throughs
sfx.add(impact(0.7), w[5] + 0.05); sfx.add(clap(), w[5] + 0.05, 0.3); sfx.add(shimmer(0.9, 2400), w[5] + 0.1, 0.1)

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
