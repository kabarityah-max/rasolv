/* transitions, HUD frame, header/timecode, captions, background drift — then the single paused timeline is registered inline in index.html */
(() => {
  enter('sB', 'glass');
  enter('sC', 'zoom', { s: 1.8, flash: .9 });
  enter('sD1', 'shutter');
  enter('sD2', 'iris', { x: 540, y: 960 });
  enter('sE', 'glass');
  enter('sF', 'iris', { x: 540, y: 900, flash: .35 });
  enter('sG', 'zoom', { s: 1.15, flash: .25 });
  enter('sH', 'up', { flash: .25 });
  enter('sI', 'slice', { flash: .35 });
  enter('sJ', 'push', { flash: .25 });
  enter('sK', 'shutter');
  enter('sL', 'zoom', { s: 1.35, flash: .3 });
  enter('sM', 'slice', { flash: .35 });
  enter('sO', 'iris', { x: 540, y: 760, flash: .85 });
  /* production credit only where it belongs: the opening and the end card */
  tl.set('#foot', { opacity: 1 }, 0).to('#foot', { opacity: 0, duration: .4 }, 11.3).set('#foot', { opacity: 0 }, 11.7);
  /* background drift + progress */
  tl.to('.b1', { x: 500, y: -500, duration: 60, ease: 'sine.inOut' }, 0);
  tl.to('.b2', { x: -450, y: 900, duration: 60, ease: 'sine.inOut' }, 0);
  tl.to('.b3', { x: 400, y: 600, duration: 60, ease: 'sine.inOut' }, 0);
  tl.to('#prog i', { scaleX: 1, duration: 60, ease: 'none' }, 0);
  /* viewfinder frame */
  const hud = $('#hud');
  [['left:56px;top:56px;border-left-width:2px;border-top-width:2px'], ['right:56px;top:56px;border-right-width:2px;border-top-width:2px'], ['left:56px;bottom:56px;border-left-width:2px;border-bottom-width:2px'], ['right:56px;bottom:56px;border-right-width:2px;border-bottom-width:2px']].forEach(([st]) => h(`<div class="crop" style="${st}"></div>`, hud));
  /* header: mark + wordmark, record dot + frame timecode */
  const hd = $('#hdr');
  h(`<div class="abs" style="left:96px;top:96px;display:flex;align-items:center;gap:16px"><div id="hd-ap" style="width:46px;height:46px"></div><div style="font-weight:600;font-size:30px;letter-spacing:.32em">RASOLV</div></div>`, hd);
  ap($('#hd-ap'), { r: 37, grow: 1, bp: 0, gap: '#05060a', lines: false });
  h(`<div class="abs mono" style="right:96px;top:100px;font-size:26px;letter-spacing:.14em;color:rgba(244,239,233,.7);display:flex;gap:14px;align-items:center"><i id="hd-rec" style="width:12px;height:12px;border-radius:50%;background:#FF6E05;display:block"></i><span id="hd-t">00:00:00</span></div>`, hd);
  drive(0, 60, p => { const f = Math.floor(p * 1800); $('#hd-t').textContent = String(Math.floor(f / 1800)).padStart(2, '0') + ':' + String(Math.floor(f / 30) % 60).padStart(2, '0') + ':' + String(f % 30).padStart(2, '0'); $('#hd-rec').style.opacity = (Math.floor(p * 60 * 1.5) % 2) ? .25 : 1; });
  /* karaoke captions */
  const caps = $('#caps');
  window.CAPTIONS.forEach(c => {
    const ws = c.words, chunks = []; let cur = [];
    ws.forEach(w => { cur.push(w); if (cur.length >= 4 || (/[.?!,]$/.test(w[0]) && cur.length >= 2)) { chunks.push(cur); cur = []; } });
    if (cur.length) { if (chunks.length && cur.length === 1) chunks[chunks.length - 1].push(cur[0]); else chunks.push(cur); }
    chunks.forEach((ch, ci) => {
      const t0 = ch[0][1] - 0.04, nx = chunks[ci + 1]; const t1 = nx ? nx[0][1] - 0.04 : Math.min(c.end, ch[ch.length - 1][2] + 0.45);
      const d = h(`<div class="cap"><div class="cp">${ch.map(w => `<span>${w[0]}</span>`).join(' ')}</div></div>`, caps);
      tl.set(d, { opacity: 1 }, t0).set(d, { opacity: 0 }, t1);
      tl.fromTo(d, { y: 22, scale: .97 }, { y: 0, scale: 1, duration: .16, ease: 'power3.out' }, t0);
      $$('span', d).forEach((sp, k) => tl.set(sp, { color: '#FF8A33' }, ch[k][1]).set(sp, { color: '#F4EFE9' }, ch[k][2]));
    });
  });
})();
