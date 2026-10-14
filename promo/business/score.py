"""Original 128 BPM score + sound design for the RASOLV for Business ad, synced to index.html, with the two-voice
dialogue (out/vo/*.wav placed per out/vo/lines.json) mixed on top with sidechain ducking.
Instruments and DSP helpers are shared with ../cinema/score.py.
Usage: python3 score.py out/mix.wav"""
import sys, os, json, wave, subprocess
import numpy as np

# ---- pull in the shared instruments (everything above the SCORE section of ../cinema/score.py) ----
_src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'cinema', 'score.py')).read()
_src = _src[:_src.index('# ================= SCORE')].replace('DUR = 45.0', 'DUR = 30.0')
exec(_src)
assert DUR == 30.0

BEAT = 60 / 128; BAR = 4 * BEAT; DROP = 7 * BAR          # 13.125
kicks = []


def glitch(length=0.4):
    n = int(SR * length); x = rng.normal(0, 1, n)
    hold = int(SR / 900); x = np.repeat(x[::hold], hold)[:n]
    gate = (np.floor(np.arange(n) / (SR * 0.03)) % 2 == 0).astype(float)
    return fft_filter(x, lo=300, hi=7000) * gate * np.linspace(1, 0.2, n)


def stab(freqs, d=0.5):
    n = int(SR * 2.5); t = np.arange(n) / SR; s = np.zeros(n)
    for f in freqs: s += sum((1 / h) * np.sin(2 * np.pi * f * h * t) for h in range(1, 6))
    return np.tanh(fft_filter(s / len(freqs), hi=3500)) * env(n, 0.003, d)


def buzz(length=0.35):
    n = int(SR * length); t = np.arange(n) / SR
    return np.sign(np.sin(2 * np.pi * 110 * t)) * 0.5 * np.minimum(t / 0.005, 1) * np.clip((length - t) / 0.05, 0, 1)


def metal(gain=1.0):
    n = int(SR * 1.2); t = np.arange(n) / SR
    s = sum(np.sin(2 * np.pi * f * t) * np.exp(-t / d) for f, d in [(523, .5), (1187, .25), (1873, .18), (2963, .1)])
    return (s / 3 + fft_filter(rng.normal(0, 1, n), lo=1500) * env(n, 0.0005, 0.02)) * gain


Am = ['A2', 'E3', 'A3', 'C4', 'E4']; F = ['F2', 'C3', 'F3', 'A3', 'C4']; C = ['C3', 'G3', 'C4', 'E4', 'G4']; G = ['G2', 'D3', 'G3', 'B3', 'D4']
PROG = [('A1', Am, ['A4', 'C5', 'E5', 'B4']), ('F1', F, ['F4', 'A4', 'C5', 'E5']), ('C2', C, ['C5', 'E5', 'G5', 'D5']), ('G1', G, ['G4', 'B4', 'D5', 'A4'])]


def groove(start, end, drums=True, full=True, arp=True, bars0=0):
    b = 0
    while start + b * BAR < end - 0.01:
        bt = start + b * BAR; root, ch, ar = PROG[(b + bars0) % 4]
        music.add(pad([note(n) for n in ch], BAR, a=0.2, r=0.5, bright=2200), bt, 0.22)
        for s16 in range(16):
            ts = bt + s16 * BEAT / 4
            if ts >= end: break
            if arp: music.add(pluck(note(ar[s16 % 4]) * (2 if s16 % 8 == 7 else 1), 0.1, 0.9), ts, 0.07 if s16 % 4 else 0.1, pan=0.35 if s16 % 2 else -0.35)
            if s16 % 2 == 0: music.add(bass(note(root) * (2 if s16 % 8 == 6 else 1), BEAT * 0.42), ts, 0.2 if drums else 0.1)
        for k in range(4):
            tb = bt + k * BEAT
            if tb >= end: break
            if drums:
                kicks.append(tb); music.add(kick(1.0), tb)
                if k in (1, 3) and full: music.add(clap(), tb, 0.3)
                music.add(hat(0.02), tb + BEAT / 2, 0.12, pan=0.3)
                if full: music.add(hat(0.012), tb + BEAT / 4, 0.05, pan=-0.3); music.add(hat(0.012), tb + 3 * BEAT / 4, 0.05, pan=-0.3)
        b += 1


# ================= ACT 1: the cost (0 – 7.5) =================
music.add(pad([note('A0'), note('E1'), note('A1')], 5.8, a=0.4, r=0.4, bright=400), 0.0, 0.9)
for k in range(8): sfx.add(tick(1500, 0.03) + tick(3200, 0.006) * 0.5, k * BEAT, 0.5)            # clock tick on every beat
for i, tt in enumerate([0.94, 0.94 + BEAT / 2, 0.94 + BEAT, 0.94 + 1.5 * BEAT]):                    # loss flashes
    sfx.add(glitch(0.12), tt, 0.25, pan=(-.4 if i % 2 else .4)); sfx.add(pop(300 + 80 * i, 0.05), tt, 0.25)
music.add(impact(0.5), 1.875)
sfx.add(whoosh(0.25, True, (800, 9000)), 1.85, 0.2); sfx.add(impact(0.35), 2.06); sfx.add(shimmer(1.0, 2600), 2.07, 0.08)  # light snaps on
sfx.add(ding(1760, 0.5), 3.45, 0.18); sfx.add(ding(1661, 0.5), 3.47, 0.15)                          # timer hits 1:00:00
# heartbeat riser on the phone
for k in range(8):
    tb = 3.75 + k * BEAT / (1 + k * 0.12)
    music.add(kick(0.55), tb); music.add(kick(0.35), tb + 0.16)
music.add(whoosh(1.8, True, (150, 4000)), 3.75, 0.25)
for tt in [3.85, 4.22, 4.45, 4.69, 5.15]:
    for j in range(5): sfx.add(key(), tt - 0.12 + j * 0.025, 0.25)
    sfx.add(pop(900, 0.03), tt, 0.25)
for tt in [4.22, 4.45, 4.69]: sfx.add(glitch(0.15), tt, 0.3)
sfx.add(whoosh(0.35, False, (600, 7000)), 5.15, 0.3); sfx.add(buzz(0.4), 5.36, 0.12)
# 5.625 – 7.5 hard silence: only a low air bed
music.add(pad([note('A1')], 1.9, a=0.3, r=0.3, bright=250), 5.625, 0.35)

# ================= ACT 2: the edge (7.5 – 13.125) =================
music.add(pad([note('A0'), note('A1')], 5.6, a=0.2, r=0.2, bright=350), 7.5, 0.8)
t0 = 7.5
for k in range(int((12.95 - t0) / (BEAT / 4))):
    ts = t0 + k * BEAT / 4
    if ts >= 12.95: break
    nm = ['A4', 'C5', 'E5', 'B4'][k % 4]
    music.add(pluck(note(nm), 0.09, 0.3 + 0.7 * k / 47), ts, 0.03 + 0.07 * k / 47, pan=0.3 if k % 2 else -0.3)
    if k % 4 == 0: music.add(bass(note('A1'), BEAT * 0.5), ts, 0.08 + 0.1 * k / 47)
for k in range(int((12.95 - 9.375) / BEAT)): kicks.append(9.375 + k * BEAT); music.add(kick(0.6), 9.375 + k * BEAT)
for w in [7.5, 9.375, 11.25]: sfx.add(whoosh(0.3, True, (500, 9000)), w - 0.2, 0.35, pan=0.6); sfx.add(whoosh(0.3, False, (500, 9000)), w, 0.25, pan=-0.6)
sfx.add(pop(700, 0.05), 9.4, 0.3); sfx.add(chime([note('E6'), note('A6')], 0.05, 0.6), 9.52, 0.12)       # terminal snaps open, Claude pops
for k in range(30): sfx.add(key(), 9.55 + k * 0.045, 0.12)
sfx.add(whoosh(0.9, True, (300, 6000)), 11.65, 0.25)                                                     # flare
music.add(whoosh(1.7, True, (200, 12000)), 11.25, 0.45)
roll = 11.25
while roll < 12.93:
    gap = BEAT / 2 if roll < 12.0 else (BEAT / 4 if roll < 12.55 else BEAT / 8)
    music.add(clap(), roll, 0.1 + 0.2 * (roll - 11.25) / 1.7); roll += gap
# 12.95 – 13.125: dead silence (the black)

# ================= DROP + ACT 3 (13.125 – 24.375) =================
music.add(impact(1.2), DROP); music.add(stab([note(n) for n in Am], 0.8), DROP, 0.4)
music.add(impact(0.7), DROP + BEAT / 2); music.add(stab([note(n) for n in Am], 0.5), DROP + BEAT / 2, 0.25)
groove(14.06, 24.375)
for i, tt in enumerate([14.53, 15.0, 15.47, 15.94]):
    sfx.add(impact(0.35), tt); sfx.add(stab([note(['A3', 'C4', 'E4', 'G4'][i]), note(['E4', 'G4', 'B4', 'D5'][i])], 0.25), tt, 0.15)
for i in range(12): sfx.add(whoosh(0.25, False, (1500, 9000)), 14.06 + i * 0.04, 0.05, pan=np.sin(i) * 0.7)
sfx.add(whoosh(0.5, True, (400, 8000)), 14.8, 0.2)
for tt in [16.95, 17.15, 17.3]: sfx.add(whoosh(0.35, True, (800, 9000)), tt, 0.18, pan=0.4)
for tt in [17.2, 17.4]: sfx.add(pop(600, 0.05), tt, 0.25)
for k in range(26): sfx.add(key(), 17.5 + k * 0.034, 0.12)
sfx.add(click(), 18.15, 0.4); sfx.add(ding(2637, 0.3), 18.17, 0.08)
sfx.add(glitch(0.25), 19.3, 0.35); sfx.add(whoosh(0.2, True, (1000, 9000)), 19.28, 0.3)                # strike-through
sfx.add(impact(0.9), 19.72); sfx.add(chime([note('A5'), note('E6')], 0.04, 0.6), 19.75, 0.1)          # 4 MIN
for i in range(5): sfx.add(ding(1318.5 * 2 ** (i * 2 / 12), 0.25), 20.12 + i * 0.075, 0.09, pan=(i - 2) * 0.25)
sfx.add(whoosh(0.4, False, (300, 5000)), 20.6, 0.2); sfx.add(shimmer(0.8, 2400), 21.4, 0.12)
sfx.add(whoosh(0.4, True, (300, 6000)), 22.6, 0.2); sfx.add(metal(0.6), 22.97); sfx.add(impact(0.6), 22.97)

# ================= ACT 4: hero (24.375 – 28.125) — half-time, big and slow =================
music.add(impact(0.6), 24.375)
for b in range(2):
    bt = 24.375 + b * BAR; root, ch, ar = PROG[b % 4]
    music.add(pad([note(n) for n in ch] + [note(ch[-1]) * 2], BAR, a=0.5, r=0.9, bright=2600), bt, 0.32)
    music.add(bass(note(root), BAR * 0.95), bt, 0.12)
    kicks.append(bt); music.add(kick(0.8), bt); music.add(clap(), bt + 2 * BEAT, 0.18)
    for k in range(8): music.add(pluck(note(ar[k % 4]) * 2, 0.3, 0.5), bt + k * BEAT / 2, 0.035, pan=(-.5 if k % 2 else .5))
music.add(shimmer(3.5, 2200), 24.4, 0.06)
music.add(whoosh(0.9, True, (200, 10000)), 27.2, 0.35)

# ================= logo (28.125 – 30) =================
music.add(impact(1.3), 28.125)
music.add(pad([note('A1'), note('E2'), note('A2'), note('C#3'), note('E3'), note('A3'), note('B3')], 1.0, a=0.05, r=1.0, bright=3000), 28.125, 0.5)
music.add(chime([note('A5'), note('E6'), note('A6')], 0.05, 1.2), 28.15, 0.12)
sfx.add(whoosh(0.4, True, (500, 8000)), 28.4, 0.12)
for i in range(4): sfx.add(tick(1500 + 120 * i, 0.012), 28.8 + i * 0.07, 0.07)

pump = np.ones(N)
for kt in kicks:
    i = int(kt * SR); n = int(SR * 0.3); x = np.arange(min(n, N - i)) / SR
    pump[i:i + len(x)] = np.minimum(pump[i:i + len(x)], 1 - 0.4 * np.exp(-x / 0.09))

# ================= VOICE =================
for ln in json.load(open('out/vo/lines.json'))['lines']:
    eq = 'equalizer=f=3500:t=q:w=1.2:g=2' if ln['who'] == 'F' else 'equalizer=f=4500:t=q:w=1.2:g=2.5'
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', f"out/vo/{ln['i']:02d}.wav", '-af', f'highpass=f=70,acompressor=threshold=-20dB:ratio=2.5:attack=5:release=80,{eq}',
                          '-ar', str(SR), '-ac', '1', '-f', 'f32le', '-'], capture_output=True, check=True).stdout
    v = np.frombuffer(raw, np.float32).astype(float); v /= max(1e-6, np.abs(v).max())
    voice.add(v, ln['start'], 0.9, pan=0.0 if ln['who'] == 'F' else 0.08)

# ================= MIX (same staging as ../cinema/score.py) =================
blk = int(SR * 0.01)
vo_env = np.abs(voice.L + voice.R)
ve = np.repeat([vo_env[i:i + blk].max() for i in range(0, N, blk)], blk)[:N]
acc = 0.0; att, rel = np.exp(-1 / (0.02 * 100)), np.exp(-1 / (0.3 * 100)); dv = []
for i in range(0, N, blk):
    tg = 1.0 if ve[i] > 0.04 else 0.0; acc = tg + (acc - tg) * (att if tg > acc else rel); dv.append(acc)
duck = np.repeat(dv, blk)[:N]
mgain = (1 - 0.55 * duck) * pump * 0.55
sgain = (1 - 0.35 * duck) * 0.8
ir = reverb_ir(2.0, 6000)
ML, MR = music.L * mgain, music.R * mgain
SL, SRr = sfx.L * sgain, sfx.R * sgain
wetL = convolve(ML * 0.6 + SL * 0.5, ir); wetR = convolve(MR * 0.6 + SRr * 0.5, np.roll(ir, 137))
vwet = convolve(voice.L + voice.R, reverb_ir(0.5, 7000)) * 0.05
L = ML + SL + wetL * 0.2 + voice.L + vwet
R = MR + SRr + wetR * 0.2 + voice.R + vwet
gate = np.ones(N); a, b = int(12.95 * SR), int(DROP * SR); gate[a:b] = 0.0                            # the dead-silence black before the drop
gate[a - 480:a] = np.linspace(1, 0, 480)
fade = np.clip((DUR - t_all) / 0.6, 0, 1) * np.minimum(t_all / 0.02, 1)
L *= fade * gate; R *= fade * gate
peak = max(np.abs(L).max(), np.abs(R).max())
L, R = np.tanh(L / peak * 1.1) * 0.9, np.tanh(R / peak * 1.1) * 0.9
with wave.open(sys.argv[1], 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((np.stack([L, R], 1) * 32767).astype('<i2').tobytes())
print('wrote', sys.argv[1])
