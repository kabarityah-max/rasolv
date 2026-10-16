"""Soundtrack for the RASOLV "on hold" story. Three layers, all synthesised (royalty-free):
  * HOLD MUSIC  — a cheesy bossa "muzak" loop squeezed through a telephone band-pass. Full level for the four wordless
                  opening seconds, ducked under the story, muffled in the dark hall, back for the recap, and cut dead by
                  a hang-up click on "exit".
  * UNDERSCORE  — sparse felt-piano + warm pad in F (D minor in the dark hall) under the narration.
  * RASOLV BED  — after the click: warm Bb–F–C–F pad, plucked arps, chime on the logo.
Plus sound design (headline thuds, wire spark, radio static, sign ding, hang-up) and the voiceover with ducking.
DSP helpers and instruments are the ones from ../aw2candine/score.py.
Usage: python3 score.py out/mix.wav [stem-prefix]"""
import sys, json, wave, subprocess
import numpy as np

SR = 48000
META = json.load(open("out/vo/lines.json"))
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
X = 0.35
CUT = {'dark': S['then'] - X, 'pair': S['pair'] - X, 'same': S['same'] - X, 'end': S['exit'] - X}
MEANS = S['means'] - X
CLICK = WT['exit'][3] - 0.05           # "exit" — hang-up
HL_AT = [S[k] - X for k in ('tune', 'year', 'wire', 'ant', 'hear', 'stop', 'less', 'pat', 'now', 'what', 'noth', 'trick', 'then', 'means', 'same', 'stay', 'exit', 'which')]


def ramp(points):
    """Piecewise-linear gain envelope over the whole timeline from [(t, g), ...]."""
    ts, gs = zip(*points)
    return np.interp(t_all, ts, gs)


# ================= instruments for this piece =================
def epiano(f, d=0.9):
    n = int(SR * (d + 0.4)); t = np.arange(n) / SR
    s = np.sin(2 * np.pi * f * t) + 0.35 * np.sin(2 * np.pi * 2 * f * t + 0.3) * np.exp(-t * 4) + 0.12 * np.sin(2 * np.pi * 3 * f * t) * np.exp(-t * 7)
    trem = 1 + 0.12 * np.sin(2 * np.pi * 5.3 * t)
    return s * trem * env(n, 0.004, d * 0.45) * 0.5


def flute(f, d=0.5):
    n = int(SR * (d + 0.25)); t = np.arange(n) / SR
    vib = 1 + 0.006 * np.sin(2 * np.pi * 5.5 * t) * np.minimum(t / 0.15, 1)
    ph = 2 * np.pi * np.cumsum(f * vib) / SR
    s = np.sin(ph) + 0.25 * np.sin(2 * ph) + 0.08 * np.sin(3 * ph)
    breath = fft_filter(rng.normal(0, 1, n), lo=1500, hi=6000) * 0.03
    e = np.minimum(t / 0.06, 1) * np.clip((d + 0.25 - t) / 0.22, 0, 1)
    return (s * 0.5 + breath) * e * 0.5


def rim():
    n = int(SR * 0.08); t = np.arange(n) / SR
    return (np.sin(2 * np.pi * 900 * t) * env(n, 0.0005, 0.012) + fft_filter(rng.normal(0, 1, n), lo=2500, hi=7000) * env(n, 0.0003, 0.006)) * 0.6


def shaker():
    n = int(SR * 0.09)
    return fft_filter(rng.normal(0, 1, n), lo=5000) * env(n, 0.003, 0.02) * 0.35


def felt(f, d=1.6):
    n = int(SR * (d + 0.5)); t = np.arange(n) / SR
    s = np.sin(2 * np.pi * f * t) + 0.22 * np.sin(2 * np.pi * 2 * f * t) * np.exp(-t * 3) + 0.05 * np.sin(2 * np.pi * 3 * f * t) * np.exp(-t * 6)
    thump = fft_filter(rng.normal(0, 1, n), hi=400) * env(n, 0.001, 0.015) * 0.5
    return (s * env(n, 0.006, d * 0.5) + thump) * 0.5


def drone(f, length):
    n = int(SR * length); t = np.arange(n) / SR
    s = np.sin(2 * np.pi * f * t) + 0.5 * np.sin(2 * np.pi * f * 1.005 * t) + 0.25 * np.sin(2 * np.pi * 2 * f * t)
    return s / 1.75 * np.minimum(t / 2.0, 1) * np.clip((length - t) / 1.5, 0, 1)


def static(length=1.0):
    n = int(SR * length); t = np.arange(n) / SR
    s = fft_filter(rng.normal(0, 1, n), lo=800, hi=5000) * (0.6 + 0.4 * np.sin(2 * np.pi * 7 * t) * np.sin(2 * np.pi * 1.3 * t))
    return s * np.sin(np.pi * t / length) ** 1.2 * 0.5


def crackle(length=0.6):
    n = int(SR * length); x = np.zeros(n)
    for _ in range(26):
        i = int(rng.uniform(0, n - 400)); x[i:i + 400] += fft_filter(rng.normal(0, 1, 400), lo=1200) * env(400, 0.0002, 0.004) * rng.uniform(0.3, 1)
    return x


def hangup():
    n = int(SR * 0.3); t = np.arange(n) / SR
    c = fft_filter(rng.normal(0, 1, n), lo=400, hi=5000) * env(n, 0.0003, 0.012) + np.sin(2 * np.pi * 220 * t) * env(n, 0.001, 0.03) * 0.6
    return c


def phone_fx(x, lo=300, hi=3400, drive=1.6):
    """Telephone band-pass + a little saturation + hiss."""
    y = fft_filter(x, lo=lo, hi=hi)
    y = np.tanh(y * drive) / drive
    return y + fft_filter(rng.normal(0, 1, len(x)), lo=1000, hi=3400) * 0.004


# ================= HOLD MUSIC (bossa muzak, 100 bpm, F major) =================
hold = Bus()
BPM = 100; B = 60 / BPM; BAR = 4 * B
CHORDS = [('F2', ['F3', 'A3', 'C4', 'E4']), ('G2', ['G3', 'Bb3', 'D4', 'F4']), ('C2', ['C3', 'E3', 'G3', 'Bb3']), ('F2', ['F3', 'A3', 'C4', 'E4']),
          ('D2', ['D3', 'F3', 'A3', 'C4']), ('G2', ['G3', 'Bb3', 'D4', 'F4']), ('C2', ['C3', 'E3', 'G3', 'Bb3']), ('F2', ['F3', 'A3', 'C4', 'D4'])]
# melody: (beat offset within the 8-bar phrase, note, length in beats)
MEL = [(0, 'A4', 1.5), (1.5, 'G4', 0.5), (2, 'F4', 1.5), (4, 'D4', 1), (5, 'E4', 1), (6, 'F4', 2),
       (8, 'G4', 1.5), (9.5, 'A4', 0.5), (10, 'Bb4', 1.5), (12, 'A4', 1), (13, 'G4', 1), (14, 'E4', 2),
       (16, 'F4', 1.5), (17.5, 'E4', 0.5), (18, 'D4', 1.5), (20, 'C4', 1), (21, 'D4', 1), (22, 'A4', 2),
       (24, 'G4', 1.5), (25.5, 'F4', 0.5), (26, 'E4', 1.5), (28, 'G4', 1), (29, 'F4', 3)]
bar = 0
while bar * BAR < DUR:
    bt = bar * BAR; root, ch = CHORDS[bar % 8]; fr = [note(n) for n in ch]
    for off in (0, 1.5, 3, 3.5):                     # bossa comping
        for f in fr: hold.add(epiano(f, 0.7 if off != 3.5 else 0.35), bt + off * B, 0.09, pan=rng.uniform(-0.3, 0.3))
    for off, mult in ((0, 1), (1.5, 1.5), (2, 1), (3.5, 1.5)):
        hold.add(bass(note(root) * mult, B * 0.55), bt + off * B, 0.28)
    for k in range(8):
        hold.add(shaker(), bt + k * B / 2, 0.08 if k % 2 else 0.14, pan=0.35)
    for off in (1, 3): hold.add(rim(), bt + off * B, 0.25, pan=-0.3)
    bar += 1
ph = 0
while ph * 8 * BAR < DUR:
    for off, nm, ln in MEL: hold.add(flute(note(nm), ln * B * 0.9), ph * 8 * BAR + off * B, 0.5)
    ph += 1
hold_dry = (hold.L + hold.R) * 0.5
hold_phone = phone_fx(hold_dry)                              # tinny: the handset
hold_muffled = fft_filter(hold_dry, lo=150, hi=900) * 0.35    # behind a door
g_phone = ramp([(0, 1.0), (3.9, 1.0), (5.2, 0.5), (S['year'] - 0.3, 0.5), (S['year'], 0.32), (S['hear'] - 0.3, 0.32), (S['hear'], 0.5),
                (S['pat'], 0.5), (S['now'], 0.38), (CUT['dark'] - 0.6, 0.34), (CUT['dark'], 0.0),
                (CUT['same'] - 0.01, 0.0), (CUT['same'] + 0.3, 0.75), (CLICK - 0.001, 0.75), (CLICK, 0.0), (DUR, 0.0)])
g_muff = ramp([(0, 0), (CUT['dark'] - 0.01, 0), (CUT['dark'] + 0.4, 1.0), (MEANS - 0.3, 1.0), (MEANS + 0.5, 0.0), (DUR, 0)])
holdL = hold_phone * g_phone + hold_muffled * g_muff
holdR = holdL.copy()

# ================= UNDERSCORE (felt piano + pad) =================
FELT = ['F3', 'C4', 'A4', 'E4', 'C4', 'A3', 'G4', 'C4', 'F3', 'E4', 'A4', 'C5', 'G4', 'E4', 'C4', 'A3']
DARK = ['D3', 'A3', 'F4', 'E4', 'D4', 'A3', 'C4', 'F3']
PADS = [('F', ['F2', 'C3', 'A3', 'E4']), ('Dm', ['D2', 'A2', 'F3', 'C4']), ('Bb', ['Bb1', 'F3', 'D4', 'A3']), ('C', ['C2', 'G2', 'E3', 'Bb3'])]
U0 = S['year'] - 0.6
k = 0; tt = U0
while tt < CUT['end'] - 0.3:
    dark = CUT['dark'] - 0.3 <= tt < MEANS
    if tt < CUT['dark'] - 0.3 or tt >= MEANS:
        nm = FELT[k % len(FELT)]; gap = 1.2 if k % 4 != 3 else 1.8
    else:
        nm = DARK[k % len(DARK)]; gap = 1.8
    if not (S['what'] - 0.3 <= tt < S['trick'] - 0.3):        # drop out under "What did it fix? Nothing."
        music.add(felt(note(nm), 1.8), tt, 0.24, pan=rng.uniform(-0.45, 0.45))
    tt += gap; k += 1
pt = U0; pi = 0
while pt < CUT['dark'] - 0.3:
    ln = min(4.8, CUT['dark'] - 0.3 - pt)
    music.add(pad([note(n) for n in PADS[pi % 4][1]], ln, a=1.5, r=1.5, bright=1600), pt, 0.11); pt += ln; pi += 1
music.add(drone(note('D1'), MEANS - CUT['dark'] + 1.0), CUT['dark'] - 0.5, 0.22)
music.add(pad([note(n) for n in ['D2', 'A2', 'F3', 'A3']], MEANS - CUT['dark'] + 0.5, a=2.0, r=1.5, bright=1200), CUT['dark'], 0.10)
pt = MEANS; pi = 0
while pt < CUT['end'] - 0.3:
    ln = min(4.8, CUT['end'] - 0.3 - pt)
    music.add(pad([note(n) for n in PADS[pi % 4][1]], ln, a=1.5, r=1.2, bright=1500), pt, 0.09); pt += ln; pi += 1
music.add(whoosh(1.4, True, (200, 7000)), CLICK - 1.4, 0.16)                  # riser into the hang-up

# ================= RASOLV BED (after the click) =================
R0 = CLICK + 0.25
RB = [('Bb', ['Bb1', 'F3', 'D4', 'A4']), ('F', ['F2', 'C3', 'A3', 'E4']), ('C', ['C2', 'G2', 'E3', 'G3']), ('F', ['F2', 'C3', 'A3', 'C4'])]
pt = R0; pi = 0
while pt < DUR - 0.5:
    ln = min(3.6, DUR - 0.5 - pt)
    music.add(pad([note(n) for n in RB[pi % 4][1]], ln, a=1.0, r=1.6, bright=3000), pt, 0.30); pt += ln; pi += 1
ARP = ['F4', 'A4', 'C5', 'E5', 'C5', 'A4']
ta = R0 + 0.4; ai = 0
while ta < DUR - 1.0:
    music.add(pluck(note(ARP[ai % 6]), 0.5, 0.7), ta, 0.11, pan=(0.4 if ai % 2 else -0.4)); ta += 0.3; ai += 1
music.add(impact(0.35), WT['ras'][0] - 0.02)
music.add(chime([note('F5'), note('A5'), note('C6'), note('F6')], 0.07, 1.4), WT['logo'][0], 0.14)
music.add(impact(0.5), WT['logo'][0])
music.add(pad([note(n) for n in ['F1', 'C2', 'F2', 'A2', 'C3', 'E3', 'A3']], DUR - WT['logo'][0] - 0.3, a=0.05, r=1.5, bright=2600), WT['logo'][0], 0.22)

# ================= SOUND DESIGN =================
sfx.add(click(), 0.15, 0.5)                                                  # handset lifted
for h in HL_AT:                                                              # soft thud on every headline
    sfx.add(fft_filter(impact(0.5), hi=220), h, 0.22)
sfx.add(crackle(0.7), WT['wire'][4] - 0.05, 0.6)                             # the spark
sfx.add(static(1.6), S['ant'] - X, 0.28)                                     # radio tuning as the antenna lights up
for k in range(3): sfx.add(crackle(0.4), S['hear'] - X + k * 0.9 + 0.2, 0.18)
sfx.add(pop(520, 0.06), S['stop'] - X, 0.25)                                 # first callers
sfx.add(whoosh(1.2, True, (300, 6000)), S['now'] - X - 0.2, 0.22)            # crowd pours in
sfx.add(ding(1760, 0.5), S['imp'] - 0.1, 0.09)                               # announcement chime before the recording
sfx.add(ding(1320, 0.5), S['imp'] + 0.08, 0.07)
sfx.add(whoosh(0.6, False, (300, 6000)), CUT['same'], 0.14)                  # recap frame rises
sfx.add(hangup(), CLICK, 0.9)                                                # hang up
sfx.add(whoosh(0.9, True, (300, 9000)), WT['exit'][3] - 0.2, 0.18)           # aperture opens
for i, wi in enumerate((0, 7, 9)): sfx.add(pop(600 + 120 * i, 0.05), WT['exp'][wi] - 0.1, 0.2)
sfx.add(pop(500, 0.06), WT['which'][4] - 0.1, 0.2); sfx.add(pop(760, 0.06), WT['which'][7] - 0.1, 0.2)
sfx.add(pop(820, 0.06), WT['logo'][3] + 0.1, 0.18)                           # CTA

# ================= VOICE =================
for ln in lines:
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', f"out/vo/{ln['i']:02d}.wav", '-af', 'highpass=f=80,acompressor=threshold=-20dB:ratio=3:attack=4:release=60,equalizer=f=3000:t=q:w=1.2:g=2',
                          '-ar', str(SR), '-ac', '1', '-f', 'f32le', '-'], capture_output=True, check=True).stdout
    v = np.frombuffer(raw, np.float32).astype(float)
    act = v[np.abs(v) > 0.02 * np.abs(v).max()]
    v *= 0.16 / max(1e-6, np.sqrt(np.mean(act ** 2)))
    voice.add(v, ln['start'], 1.0)

# ================= MIX =================
vo_env = np.abs(voice.L + voice.R)
blk = int(SR * 0.01); ve = np.repeat([vo_env[i:i + blk].max() for i in range(0, N, blk)], blk)[:N]
acc = 0.0; att, rel = np.exp(-1 / (0.02 * 100)), np.exp(-1 / (0.35 * 100))
dvals = np.empty(len(range(0, N, blk)))
for j, i in enumerate(range(0, N, blk)):
    target = 1.0 if ve[i] > 0.04 else 0.0
    acc = target + (acc - target) * (att if target > acc else rel); dvals[j] = acc
duck = np.repeat(dvals, blk)[:N]
mgain = (1 - 0.5 * duck) * 0.42
hgain = (1 - 0.55 * duck) * 1.35
sgain = (1 - 0.45 * duck) * 0.6

ir = reverb_ir(1.8, 5000)
ML = music.L * mgain; MR = music.R * mgain
HL_ = holdL * hgain; HR_ = holdR * hgain
SL, SRr = sfx.L * sgain, sfx.R * sgain
wetL = convolve(ML * 0.6 + SL * 0.4, ir); wetR = convolve(MR * 0.6 + SRr * 0.4, np.roll(ir, 137))
vwet = convolve(voice.L + voice.R, reverb_ir(0.4, 6000)) * 0.03
L = ML + HL_ + SL + wetL * 0.2 + voice.L + vwet
R = MR + HR_ + SRr + wetR * 0.2 + voice.R + vwet
fade = np.clip((DUR - t_all) / 0.6, 0, 1) * np.minimum(t_all / 0.01, 1)
L *= fade; R *= fade
peak = max(np.abs(L).max(), np.abs(R).max())
L, R = np.tanh(L / peak * 1.1) * 0.9, np.tanh(R / peak * 1.1) * 0.9
with wave.open(sys.argv[1], 'wb') as wf:
    wf.setnchannels(2); wf.setsampwidth(2); wf.setframerate(SR)
    wf.writeframes((np.stack([L, R], 1) * 32767).astype('<i2').tobytes())
print('wrote', sys.argv[1], f'{DUR}s')

if len(sys.argv) > 2:
    for name, (a, b) in {'voice': (voice.L + vwet, voice.R + vwet), 'hold': (HL_, HR_), 'bed': (ML + SL + wetL * 0.2, MR + SRr + wetR * 0.2)}.items():
        st = np.stack([a * fade / peak, b * fade / peak], 1)
        with wave.open(f"{sys.argv[2]}_{name}.wav", 'wb') as wf:
            wf.setnchannels(2); wf.setsampwidth(2); wf.setframerate(SR); wf.writeframes((np.clip(st, -1, 1) * 32767).astype('<i2').tobytes())
