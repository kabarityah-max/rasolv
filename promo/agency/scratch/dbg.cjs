const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
  p.on('console', m => console.log('console:', m.type(), m.text().slice(0, 300)));
  p.on('pageerror', e => console.log('PAGEERROR:', e.message.slice(0, 400), (e.stack||'').split('\n').slice(0,3).join(' | ')));
  await p.goto('file:///home/user/rasolv/promo/agency/index.html'); await p.waitForTimeout(1500);
  console.log(await p.evaluate(() => typeof gsap + ' ' + typeof window.__timelines + ' ' + (window.__timelines && Object.keys(window.__timelines))));
  await b.close();
})();
