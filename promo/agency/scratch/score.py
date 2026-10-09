"""Original 128 BPM score + beat-synced sound design for the RASOLV agency film, mixed with the voiceover.
All cuts sit on the beat grid (BEAT = 60/128 s); see SCENES in ../index.html (same beat numbers).
Usage: python3 score.py ../assets/mix.wav"""
import sys, json, wave, subprocess
sys.argv = sys.argv[:]
from dsp import *   # noqa  (helpers, Bus, instruments; SR, N, DUR, rng)

BEAT = 60 / 128
BAR = 4 * BEAT
def tb(b): return b * BEAT
# scene starts in beats (must match index.html)
SC = [0, 8, 16, 24, 28, 32, 40, 48, 56, 64, 72, 80, 88, 96, 104, 116, 128]

CH = [('A1', ['A3', 'C4', 'E4'], ['A4', 'C5', 'E5', 'A5', 'E5', 'C5', 'E5', 'C5']),
      ('F1', ['F3', 'A3', 'C4'], ['F4', 'A4', 'C5', 'F5', 'C5', 'A4', 'C5', 'A4']),
      ('C2', ['E3', 'G3', 'C4'], ['G4', 'C5', 'E5', 'G5', 'E5', 'C5', 'E5', 'C5']),
      ('G1', ['D3', 'G3', 'B3'], ['G4', 'B4', 'D5', 'G5', 'D5', 'B4', 'D5', 'B4'])]
kicks = []
for bar in range(32):
    b0 = bar * 4; t0 = tb(b0); root, ch, arp = CH[bar % 4]
    intro = b0 < 16
    brk = 80 <= b0 < 88          # tension break under "critics"
    calm = 104 <= b0 < 116       # map scene: lighter
    fin = b0 >= 116
    music.add(pad([note(n) for n in ch], BAR, a=0.2, r=0.5, bright=(1200 if intro or brk else 2600)), t0, 0.30 if not fin else 0.4)
    for k in range(4):
        t = t0 + k * BEAT; bb = b0 + k
        drums = (not intro or bb >= 8) and not brk and not (calm and bb < 112) and not (fin and bb > 119)
        if drums:
            kicks.append(t); music.add(kick(0.85 if not intro else 0.5), t)
            if k in (1, 3) and not intro: music.add(clap(), t, 0.22)
            music.add(hat(0.025), t + BEAT / 2, 0.11, pan=0.25)
            if b0 >= 32 and not intro: music.add(hat(0.012), t + BEAT / 4, 0.05, pan=-0.3); music.add(hat(0.012), t + 3 * BEAT / 4, 0.05, pan=-0.3)
        if brk:   # ticking clock + sub heartbeat
            music.add(tick(1800 + 200 * (k % 2), 0.01), t, 0.18); music.add(tick(2400, 0.008), t + BEAT / 2, 0.10)
            if k == 0: music.add(kick(0.5), t)
        if not intro and not brk and not calm:
            for e in (0, 1):
                music.add(bass(note(root) * (2 if e and k == 3 else 1), BEAT * 0.42), t + e * BEAT / 2, 0.20 if e else 0.12)
    if not brk:
        for k, nm in enumerate(arp):
            if intro and b0 < 8 and k % 2: continue
            music.add(pluck(note(nm), 0.28, 0.9), t0 + k * BEAT / 2, 0.12 if not calm else 0.09, pan=(-0.35 if k % 2 else 0.35))
# opening: filtered swell into beat 8, big riser into the drop at beat 16
music.add(pad([note('A2'), note('E3'), note('A3')], tb(8), a=3, r=0.2, bright=700), 0.0, 0.5)
music.add(whoosh(tb(8) - 0.0, True, (200, 9000)), tb(8) - tb(8) + 0.0, 0.0)
music.add(whoosh(tb(4), True, (300, 9000)), tb(12), 0.32)
music.add(impact(1.0), tb(16)); music.add(chime([note('A5'), note('C6'), note('E6')], 0.05, 1.2), tb(16), 0.10)
# break riser + REJECTED hit
music.add(whoosh(tb(8), True, (200, 8000)), tb(80), 0.25); music.add(impact(1.0), tb(88))
# final resolve
music.add(pad([note('A2'), note('E3'), note('A3'), note('C4'), note('E4'), note('B4')], 6.0, a=0.3, r=2.0, bright=3400), tb(116), 0.5)
music.add(impact(1.1), tb(116))
for k, nm in enumerate(['A5', 'C6', 'E6', 'A6']): music.add(pluck(note(nm), 0.5), tb(120) + k * BEAT / 2, 0.10, pan=0.3 * (-1) ** k)
music.add(chime([note('A5'), note('E6'), note('A6'), note('C7')], 0.07, 1.6), tb(124), 0.16)

pump = np.ones(N)
for kt in kicks:
    i = int(kt * SR); n = int(SR * 0.28); x = np.arange(min(n, N - i)) / SR
    pump[i:i + len(x)] = np.minimum(pump[i:i + len(x)], 1 - 0.45 * np.exp(-x / 0.09))

# ---------------- sound design ----------------
for i, b in enumerate(SC[1:-1], 1):         # every cut: riser into it, hit on it
    t = tb(b)
    sfx.add(whoosh(0.35, True, (500, 8000)), t - 0.33, 0.20, pan=0.3 * (-1) ** i)
    sfx.add(pop(420 + 30 * (i % 5), 0.06), t, 0.30)
    sfx.add(tick(3000, 0.02), t, 0.12)
# A: terminal typing
for k in range(24): sfx.add(key(), 1.7 + k * 0.05 + rng.uniform(-0.01, 0.01), 0.14, pan=0.2)
sfx.add(click(), 3.0, 0.4)
# B: frame counter ticks
for k in range(18): sfx.add(tick(1800 + 60 * k, 0.008), tb(8) + 0.4 + k * 0.1, 0.09, pan=-0.3)
# C: aperture assembly
sfx.add(shimmer(1.2, 1800), tb(16) + 0.1, 0.16); sfx.add(impact(0.6), tb(20))
# D: kinetic words slam each 2 beats
for k in range(4): sfx.add(pop(300 + 60 * k, 0.07), tb(24) + k * BEAT, 0.25)
for k in range(4): sfx.add(shimmer(0.5, 2600 + 300 * k), tb(28) + k * BEAT, 0.08)
# E: map pings
for k in range(8): sfx.add(ding(1568 * 2 ** ([0, 4, 7, 12, 7, 4, 0, 9][k] / 12), 0.25), tb(32) + 0.5 + k * 0.25, 0.08, pan=np.sin(k) * 0.6)
# F: phone spin whooshes
for k in range(4): sfx.add(whoosh(0.4, False, (700, 7000)), tb(40) + k * 2 * BEAT, 0.14, pan=0.5 * (-1) ** k)
# G: counters
for k in range(24): sfx.add(tick(2600 - k * 40, 0.006), tb(48) + 0.5 + k * 0.07, 0.07, pan=-0.4)
sfx.add(chime([note('E6'), note('A6')], 0.06, 0.6), tb(54), 0.12)
# H: three stickers
for k in range(3): sfx.add(pop(520 + 110 * k, 0.05), tb(56) + k * 2 * BEAT, 0.30); sfx.add(clap(), tb(56) + k * 2 * BEAT, 0.10)
# I: waveform
for k in range(16): sfx.add(tick(1500 + 150 * (k % 4), 0.01), tb(64) + 0.5 + k * 0.12, 0.08)
# J: metronome flash cuts every beat
for k in range(8): sfx.add(click(), tb(72) + k * BEAT, 0.35 if k % 2 == 0 else 0.22)
# K: five rounds stamped
for k in range(5): sfx.add(pop(380 + 70 * k, 0.07), tb(80) + k * 1.5 * BEAT + 0.25, 0.30); sfx.add(tick(900, 0.03), tb(80) + k * 1.5 * BEAT + 0.25, 0.2)
# L: REJECTED stamp
sfx.add(impact(0.9), tb(88) + 0.02); sfx.add(clap(), tb(88), 0.4); sfx.add(chime([note('E6'), note('A6')], 0.08, 0.8), tb(92), 0.14)
# M: pipeline
for k in range(4): sfx.add(pop(480 + 90 * k, 0.05), tb(96) + k * 1.5 * BEAT + 0.3, 0.28)
# N: map zoom
sfx.add(whoosh(1.6, True, (300, 9000)), tb(104) + 0.1, 0.22); sfx.add(ding(1975, 0.5), tb(109), 0.14); sfx.add(chime([note('A5'), note('E6')], 0.08, 0.9), tb(111), 0.12)
# O: logo
sfx.add(shimmer(1.4, 1700), tb(116) + 0.05, 0.22); sfx.add(whoosh(0.9, False, (600, 8000)), tb(116), 0.25)
sfx.add(click(), tb(126), 0.5)

# ---------------- voice ----------------
lines = json.load(open('lines.json'))['lines']
for ln in lines:
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', f"../vo/{ln['i']:02d}.wav", '-af', 'highpass=f=70,acompressor=threshold=-20dB:ratio=2.5:attack=5:release=80,equalizer=f=3500:t=q:w=1.2:g=2',
                          '-ar', str(SR), '-ac', '1', '-f', 'f32le', '-'], capture_output=True, check=True).stdout
    v = np.frombuffer(raw, np.float32).astype(float); v /= max(1e-6, np.abs(v).max())
    voice.add(v, ln['start'], 0.9)

# ---------------- mix ----------------
vo_env = np.abs(voice.L + voice.R); blk = int(SR * 0.01)
ve = np.repeat([vo_env[i:i + blk].max() for i in range(0, N, blk)], blk)[:N]
acc = 0.0; att, rel = np.exp(-1 / (0.02 * 100)), np.exp(-1 / (0.3 * 100)); dvals = np.empty(len(range(0, N, blk)))
for j, i in enumerate(range(0, N, blk)):
    target = 1.0 if ve[i] > 0.04 else 0.0
    acc = target + (acc - target) * (att if target > acc else rel); dvals[j] = acc
duck = np.repeat(dvals, blk)[:N]
mgain = (1 - 0.5 * duck) * pump * 0.55; sgain = (1 - 0.35 * duck) * 0.8
ir = reverb_ir(2.2, 6000)
ML, MR = music.L * mgain, music.R * mgain; SL, SRr = sfx.L * sgain, sfx.R * sgain
wetL = convolve(ML * 0.6 + SL * 0.5, ir); wetR = convolve(MR * 0.6 + SRr * 0.5, np.roll(ir, 137))
vwet = convolve(voice.L + voice.R, reverb_ir(0.5, 7000)) * 0.04
L = ML + SL + wetL * 0.2 + voice.L + vwet; R = MR + SRr + wetR * 0.2 + voice.R + vwet
fade = np.clip((DUR - t_all) / 0.6, 0, 1) * np.minimum(t_all / 0.02, 1)
L *= fade; R *= fade
peak = max(np.abs(L).max(), np.abs(R).max())
L, R = np.tanh(L / peak * 1.1) * 0.9, np.tanh(R / peak * 1.1) * 0.9
out = np.stack([L, R], 1)
tmp = sys.argv[1] + '.raw.wav'
with wave.open(tmp, 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((out * 32767).astype('<i2').tobytes())
subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', tmp, '-af', 'loudnorm=I=-14:TP=-1.0:LRA=7', '-ar', '48000', sys.argv[1]], check=True)
import os; os.remove(tmp)
print('wrote', sys.argv[1])
