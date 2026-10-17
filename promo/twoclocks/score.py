"""Synthesises the "Two clocks" soundtrack — sound design synced to index.html — and mixes in the voiceover
(out/vo/*.wav, placed per out/vo/lines.json) with ducking. The stereo field follows the split screen:
the waiting side (tinny hold music, dull tick) sits left, the solved side (bright tick, update pops) sits right.
Usage: python3 score.py out/mix.wav"""
import sys, json, wave, subprocess
import numpy as np

SR = 48000
DUR = 30.0
N = int(SR * DUR)
rng = np.random.default_rng(22)
t_all = np.arange(N) / SR
# beats shared with index.html (T)
SEND, HI, MAYA, UPDATES, STOP, EXPAND, BLACK = 2.35, (3.95, 4.45), 6.0, (9.3, 11.3, 13.6), 14.9, 19.0, 22.9
STOP1, STOP2, END_IN, LOGO, PULSE = 23.25, 23.95, 25.75, 26.2, 28.75


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


def fft_filter(x, lo=None, hi=None):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR); g = np.ones_like(f)
    if hi: g *= 1 / (1 + (f / hi) ** 4)
    if lo: g *= 1 / (1 + (lo / np.maximum(f, 1e-3)) ** 4)
    return np.fft.irfft(X * g, len(x))


def reverb_ir(seconds=2.0, damp=5000):
    n = int(SR * seconds); t = np.arange(n) / SR
    ir = rng.normal(0, 1, n) * np.exp(-t / (seconds / 6.5))
    ir = fft_filter(ir, hi=damp); ir[: int(SR * 0.012)] = 0
    return ir / np.sqrt(np.sum(ir ** 2))


def convolve(x, ir):
    n = len(x) + len(ir); m = 1 << (n - 1).bit_length()
    return np.fft.irfft(np.fft.rfft(x, m) * np.fft.rfft(ir, m), m)[: len(x)]


def note(name):
    names = {'C': 0, 'C#': 1, 'D': 2, 'Eb': 3, 'E': 4, 'F': 5, 'F#': 6, 'G': 7, 'Ab': 8, 'A': 9, 'Bb': 10, 'B': 11}
    return 440 * 2 ** ((names[name[:-1]] + 12 * (int(name[-1]) + 1) - 69) / 12)


def tick(f, d=0.012, noise=0.5):
    n = int(SR * 0.08); t = np.arange(n) / SR
    return (np.sin(2 * np.pi * f * t) + noise * fft_filter(rng.normal(0, 1, n), lo=f * 0.7)) * env(n, 0.0003, d)


def pop(f, d=0.06):
    n = int(SR * 0.3); t = np.arange(n) / SR
    return np.sin(2 * np.pi * f * (1 + 0.6 * np.exp(-t / 0.01)) * t) * env(n, 0.001, d)


def chime(freqs, d=0.6):
    n = int(SR * d * 4); t = np.arange(n) / SR
    return sum(np.sin(2 * np.pi * f * t) * np.exp(-t / d) + 0.25 * np.sin(2 * np.pi * 2.01 * f * t) * np.exp(-t / (d * 0.4)) for f in freqs) / len(freqs) * env(n, 0.002, 9)


def whoosh(length, rev=False, band=(400, 6000)):
    n = int(SR * length); x = fft_filter(rng.normal(0, 1, n), lo=band[0], hi=band[1])
    e = np.sin(np.linspace(0, np.pi, n)) ** 2
    if rev: e = np.linspace(0, 1, n) ** 3
    return x * e * 0.5


def pad(freqs, length, a=1.5, r=1.5, bright=1800):
    n = int(SR * (length + r)); t = np.arange(n) / SR; s = np.zeros(n)
    for f in freqs:
        for det in (-0.3, 0.3):
            ph = rng.uniform(0, 6); s += np.sin(2 * np.pi * (f + det) * t + ph) + 0.25 * np.sin(2 * np.pi * 2 * (f + det) * t + ph)
    e = np.minimum(t / a, 1) * np.clip((length + r - t) / r, 0, 1) ** 2
    return fft_filter(s * e, hi=bright) / len(freqs)


def keyclick():
    n = int(SR * 0.04)
    return fft_filter(rng.normal(0, 1, n), lo=1500, hi=7000) * env(n, 0.0002, 0.006)


# story clocks, as on screen (same keys as index.html STORY_R / STORY_L)
def keys(t, K):
    if t <= K[0][0]: return K[0][1]
    for i in range(1, len(K)):
        if t <= K[i][0]:
            (a, va), (b, vb) = K[i - 1][:2], K[i][:2]
            k = (t - a) / (b - a)
            if len(K[i]) > 2: k = 4 * k ** 3 if k < .5 else 1 - (-2 * k + 2) ** 3 / 2
            return va + (vb - va) * k
    return K[-1][1]


STORY_R = [(0, 0), (8.2, 8.2), (9.3, 31), (11.3, 108), (13.6, 239), (14.9, 240)]
STORY_L = STORY_R + [(19.4, 252), (22.5, 2400, 'io'), (22.9, 2401)]

# ================= MUSIC =================
# low D-minor bed under the split; it simply stops at the hard cut
for chord, a, b in [(['D2', 'A2', 'F3'], 0.0, 8.0), (['Bb1', 'F2', 'D3'], 8.0, 15.0), (['G1', 'D2', 'Bb2'], 15.0, 19.0), (['A1', 'E2', 'C#3'], 19.0, BLACK)]:
    music.add(pad([note(c) for c in chord], b - a + 0.4, a=1.0 if a else 0.3, r=0.6), a, 0.32)
# warm release on the right when the case is done
music.add(pad([note(c) for c in ['D3', 'F#3', 'A3', 'E4']], 3.6, a=0.4, r=1.0, bright=3000), STOP + 0.05, 0.16, pan=0.5)
# hold music on the left phone's speaker: a cheerful little loop, band-limited to sound like a phone
mel = ['F5', 'A5', 'C6', 'A5', 'G5', 'E5', 'C5', 'E5', 'F5', 'A5', 'G5', 'F5', 'E5', 'G5', 'C5', 'C5']
hold = np.zeros(N)
for k in range(int(BLACK / 0.3)):
    f = note(mel[k % len(mel)]); n = int(SR * 0.28); tt = np.arange(n) / SR
    s = np.sign(np.sin(2 * np.pi * f * tt)) * 0.4 + np.sin(2 * np.pi * f * tt)
    i = int(k * 0.3 * SR); hold[i:i + n] += (s * env(n, 0.004, 0.16))[: N - i]
hold = np.tanh(fft_filter(hold, lo=500, hi=2800) * 1.5) * (t_all < BLACK)
hold *= 1 + 0.6 * np.clip((t_all - EXPAND) / 1.2, 0, 1)            # the left half takes the frame: louder
music.add(hold, 0, 0.09, pan=-0.75)

# ================= SFX =================
# clocks: a tick each time the shown second changes (capped while racing), left dull, right bright
for name, K, f, pan, g in [('L', STORY_L, 1100, -0.6, 0.22), ('R', STORY_R, 2600, 0.6, 0.2)]:
    last, lt = -1, -1.0
    for i in range(0, int(BLACK * 1000)):
        tt = i / 1000; s = int(keys(tt, K))
        if s != last and tt - lt > 0.045:
            sfx.add(tick(f * (1 + 0.04 * (s % 2)), 0.01 if name == 'R' else 0.02), tt, g * (0.7 if tt - lt < 0.3 else 1), pan)
            last, lt = s, tt
        elif s != last: last = s
# typing + send on the right
for i in range(18): sfx.add(keyclick(), 0.55 + i * (1.5 / 18) + rng.uniform(-.02, .02), 0.25, pan=0.5)
sfx.add(whoosh(0.35, False, (1500, 8000)), SEND, 0.35, pan=0.5)
# scan + highlights, Maya joins, updates land
sfx.add(whoosh(0.5, False, (3000, 10000)), 3.45, 0.12, pan=0.5)
for tt in HI: sfx.add(chime([note('A6'), note('E7')], 0.15), tt, 0.10, pan=0.55)
sfx.add(chime([note('D6'), note('A6')], 0.4), MAYA, 0.16, pan=0.5)
for i, tt in enumerate(UPDATES): sfx.add(pop(700 + 120 * i), tt, 0.35, pan=0.5)
sfx.add(chime([note('D6'), note('F#6'), note('A6')], 0.7), UPDATES[-1] + 0.02, 0.12, pan=0.5)
# 4:00 — the clock stops: a clack and a bright ring; then the exhale
sfx.add(tick(900, 0.05, 1.2), STOP, 0.6, pan=0.5)
sfx.add(chime([note('D6'), note('A6'), note('D7')], 1.2), STOP + 0.02, 0.2, pan=0.4)
sfx.add(fft_filter(rng.normal(0, 1, int(SR * 1.2)), lo=300, hi=2500) * np.sin(np.linspace(0, np.pi, int(SR * 1.2))) ** 2, STOP + 0.5, 0.04, pan=0.5)
# left takes the frame and races: riser into the cut
sfx.add(whoosh(1.2, False, (200, 4000)), EXPAND, 0.25, pan=-0.3)
rn = int(SR * (BLACK - EXPAND - 0.6)); rt = np.arange(rn) / SR
riser = fft_filter(rng.normal(0, 1, rn), lo=600, hi=9000) * (rt / rt[-1]) ** 2 + 0.4 * np.sin(2 * np.pi * np.cumsum(80 + 300 * (rt / rt[-1]) ** 2) / SR) * (rt / rt[-1]) ** 2
sfx.add(riser, EXPAND + 0.6, 0.2, pan=-0.3)
# black card: one beat of silence, then a key per typed letter
for k in range(len('Stop waiting.')): sfx.add(keyclick(), STOP1 + k * 0.55 / 13, 0.3)
for k in range(len('Someone real is already on it.')): sfx.add(keyclick(), STOP2 + k * 1.3 / 30, 0.3)
# end card: line slides in, folds into the aperture, reminder pulses once
sfx.add(whoosh(0.45, False, (500, 7000)), END_IN, 0.3)
n = int(SR * 1.5); tt = np.arange(n) / SR
boom = np.sin(2 * np.pi * np.cumsum(40 + 80 * np.exp(-tt / 0.05)) / SR) * env(n, 0.002, 0.5)
sfx.add(boom, LOGO + 0.2, 0.7)
music.add(pad([note(c) for c in ['D2', 'A2', 'D3', 'F#3', 'A3', 'E4']], 3.3, a=0.05, r=0.5, bright=3500), LOGO + 0.2, 0.36)
sfx.add(chime([note('D6'), note('A6'), note('F#7')], 1.0), LOGO + 0.25, 0.12)
sfx.add(pop(880, 0.08), PULSE - 0.05, 0.35); sfx.add(chime([note('A6'), note('D7')], 0.5), PULSE, 0.08)

# ================= VOICE =================
for ln in json.load(open('out/vo/lines.json'))['lines']:
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', f"out/vo/{ln['i']:02d}.wav", '-af', 'highpass=f=70,acompressor=threshold=-20dB:ratio=2.5:attack=5:release=80,equalizer=f=3500:t=q:w=1.2:g=2',
                          '-ar', str(SR), '-ac', '1', '-f', 'f32le', '-'], capture_output=True, check=True).stdout
    v = np.frombuffer(raw, np.float32).astype(float)
    voice.add(v / max(1e-6, np.abs(v).max()), ln['start'], 0.9)

# ================= MIX =================
blk = int(SR * 0.01); vo_env = np.abs(voice.L + voice.R)
ve = np.array([vo_env[i:i + blk].max() for i in range(0, N, blk)])
acc, dv = 0.0, np.empty(len(ve))
att, rel = np.exp(-1 / 2), np.exp(-1 / 30)
for j, v in enumerate(ve):
    tgt = 1.0 if v > 0.04 else 0.0
    acc = tgt + (acc - tgt) * (att if tgt > acc else rel); dv[j] = acc
duck = np.repeat(dv, blk)[:N]
ir = reverb_ir(1.8, 5500)
BED = 0.4   # music + sfx sit well under the voice
ML, MR = music.L * (1 - 0.55 * duck) * BED, music.R * (1 - 0.55 * duck) * BED
SL, SRr = sfx.L * (1 - 0.35 * duck) * BED, sfx.R * (1 - 0.35 * duck) * BED
wetL, wetR = convolve(ML * .6 + SL * .4, ir), convolve(MR * .6 + SRr * .4, np.roll(ir, 137))
# the hard cut to black kills the room too: true silence for one beat
gate = np.ones(N); gate[int(BLACK * SR):int(STOP1 * SR)] = 0
gate[int(STOP1 * SR):] = 1
bed_gate = gate.copy(); bed_gate[int(BLACK * SR):int(END_IN * SR)] = 0   # no tail of the split bleeds into the card
vwet = convolve(voice.L + voice.R, reverb_ir(0.5, 7000)) * 0.05
L = (ML + wetL * 0.25) * bed_gate + SL * gate + voice.L + vwet
R = (MR + wetR * 0.25) * bed_gate + SRr * gate + voice.R + vwet
fade = np.clip((DUR - t_all) / 0.3, 0, 1) * np.minimum(t_all / 0.01, 1)
L *= fade; R *= fade
peak = max(np.abs(L).max(), np.abs(R).max())
L, R = np.tanh(L / peak * 1.1) * 0.9, np.tanh(R / peak * 1.1) * 0.9
with wave.open(sys.argv[1], 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((np.stack([L, R], 1) * 32767).astype('<i2').tobytes())
print('wrote', sys.argv[1])
