"""Usage: python3 scratch/frames.py <round>  — snapshots 48 frames (3 per scene), JPEG contact sheets (4x2) + INDEX.txt in review/rN/"""
import sys, subprocess, os, glob, json
from PIL import Image, ImageDraw
r = sys.argv[1]; out = f'review/r{r}'; os.makedirs(out, exist_ok=True)
B = 60 / 128; SC = [0, 8, 16, 24, 28, 32, 40, 48, 56, 64, 72, 80, 88, 96, 104, 116, 128]
names = ['A hook', 'B code->frame', 'C logo', 'D1 kinetic', 'D2 liquid glass', 'E maps', 'F 3D phone', 'G live data', 'H what we make', 'I sound', 'J beat cuts', 'K five critics', 'L rejected', 'M brief->video', 'N map dive', 'O end card']
ts = []
for i, n in enumerate(names):
    a, b = SC[i] * B, SC[i + 1] * B
    for f in (0.3, (b - a) / 2, (b - a) - 0.35): ts.append((round(a + f, 2), n))
ts = [(min(t, 59.7), n) for t, n in ts]
subprocess.run(['npx', 'hyperframes', 'snapshot', '--no-end', '--at', ','.join(str(t) for t, _ in ts), '-o', f'{out}/raw'], check=True, capture_output=True)
files = sorted(glob.glob(f'{out}/raw/frame-*.png'))
assert len(files) == len(ts), (len(files), len(ts))
tiles = []
for f, (t, n) in zip(files, ts):
    im = Image.open(f).convert('RGB').resize((360, 640), Image.LANCZOS); d = ImageDraw.Draw(im); d.rectangle([0, 0, 150, 22], fill=(0, 0, 0)); d.text((4, 4), f'{t:05.2f}s', fill=(255, 255, 255)); tiles.append(im)
idx = []
for s in range(6):
    sheet = Image.new('RGB', (4 * 360, 2 * 640))
    for k in range(8):
        j = s * 8 + k; sheet.paste(tiles[j], ((k % 4) * 360, (k // 4) * 640)); idx.append(f'sheet{s + 1}.jpg tile{k + 1} = {ts[j][0]:05.2f}s  scene {ts[j][1]}')
    sheet.save(f'{out}/sheet{s + 1}.jpg', quality=90)
open(f'{out}/INDEX.txt', 'w').write('\n'.join(idx) + '\n')
print('\n'.join(idx))
