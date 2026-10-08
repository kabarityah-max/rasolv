// Renders promo/cinema/index.html frame-by-frame (SCALE=2 → 3840x2160 4K, SCALE=1 → 1920x1080 Full HD) and pipes PNGs to ffmpeg.
// Usage: node render.js <out.mp4> [fps] [startFrame] [endFrame]
//        node render.js --stills <dir> <t1,t2,...>   (preview stills)
const path = require('path');
const { spawn } = require('child_process');
const { chromium } = require('playwright');

const HTML = 'file://' + path.join(__dirname, 'index.html');

async function open() {
  const browser = await chromium.launch({ args: ['--force-color-profile=srgb', '--disable-lcd-text', '--font-render-hinting=none'] });
  const page = await browser.newPage({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: Number(process.env.SCALE || 2) });
  await page.goto(HTML);
  await page.evaluate(() => window.ready);
  return { browser, page };
}

(async () => {
  const args = process.argv.slice(2);
  const { browser, page } = await open();

  if (args[0] === '--stills') {
    const dir = args[1];
    for (const t of args[2].split(',').map(Number)) {
      await page.evaluate(t => window.seek(t), t);
      await page.screenshot({ path: path.join(dir, `still_${t.toFixed(2)}.png`) });
    }
    await browser.close();
    return;
  }

  const out = args[0];
  const fps = Number(args[1] || 60);
  const duration = await page.evaluate(() => window.DURATION);
  const total = Math.round(duration * fps);
  const start = Number(args[2] || 0), end = Number(args[3] || total);

  const ff = spawn('ffmpeg', ['-y', '-v', 'error',
    '-f', 'image2pipe', '-framerate', String(fps), '-c:v', 'png', '-i', '-',
    '-c:v', 'libx264', '-preset', 'slow', '-crf', '12', '-profile:v', 'high', '-level:v', '5.2',
    '-pix_fmt', 'yuv420p', '-color_primaries', 'bt709', '-color_trc', 'bt709', '-colorspace', 'bt709',
    '-x264-params', 'keyint=60:min-keyint=60', out], { stdio: ['pipe', 'inherit', 'inherit'] });

  for (let f = start; f < end; f++) {
    await page.evaluate(t => window.seek(t), f / fps);
    const buf = await page.screenshot({ type: 'png' });
    if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
    if (f % 30 === 0) console.log(`[${path.basename(out)}] frame ${f}/${end}`);
  }
  ff.stdin.end();
  await new Promise(r => ff.on('close', r));
  await browser.close();
})();
