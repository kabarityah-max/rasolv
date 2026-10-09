/* captions, header, progress bar, background drift — then register the single paused timeline */
(() => {
  /* ---- scene transitions (each scene's entrance; previous scene is pushed away underneath) ---- */
  enter('sB', 'glass', { flash: false });
  enter('sC', 'zoom', { s: 1.9, flashColor: ORANGE, fa: 1 });
  enter('sD1', 'slice', { flashColor: ORANGE, fa: .5 });
  enter('sD2', 'iris', { x: 540, y: 960 });
  enter('sE', 'glass', { flash: false });
  enter('sF', 'zoom', { s: 1.4, flashColor: ORANGE, fa: .35 });
  enter('sG', 'spin', { flashColor: ORANGE, fa: .3 });
  enter('sH', 'up', { flashColor: ORANGE, fa: .3 });
  enter('sI', 'slice', { flashColor: ORANGE, fa: .6 });
  enter('sJ', 'none', { flashColor: ORANGE, fa: .9 });
  enter('sK', 'zoomout', { flashColor: ORANGE, fa: .3 });
  enter('sL', 'drop', { flashColor: ORANGE, fa: .35 });
  enter('sM', 'push', { flashColor: ORANGE, fa: .3 });
  enter('sN', 'iris', { x: 540, y: 1250, flashColor: ORANGE, fa: .5 });
  enter('sO', 'zoom', { s: 2.2, flashColor: ORANGE, fa: 1 });
  /* background blobs drift */
  tl.to('.b1', { x: 500, y: -500, duration: 60, ease: 'sine.inOut' }, 0);
  tl.to('.b2', { x: -450, y: 900, duration: 60, ease: 'sine.inOut' }, 0);
  tl.to('.b3', { x: 400, y: 600, duration: 60, ease: 'sine.inOut' }, 0);
  /* progress bar */
  tl.to('#prog i', { scaleX: 1, duration: 60, ease: 'none' }, 0);
  /* header */
  const hd = $('#hdr');
  h(`<div class="abs" style="left:56px;top:92px;display:flex;align-items:center;gap:18px"><div id="hd-ap" style="width:54px;height:54px"></div><div style="font-weight:800;font-size:34px;letter-spacing:.22em">RASOLV</div></div>`, hd);
  ap($('#hd-ap'), { r: 37, grow: 1, bp: 0, gap: '#060606', lines: false });
  h(`<div class="abs mono" style="right:56px;top:104px;font-size:24px;letter-spacing:.2em;color:rgba(244,239,233,.55)" id="hd-t">00:00</div>`, hd);
  drive(0, 60, p => { const t = Math.floor(p * 60); $('#hd-t').textContent = '00:' + String(t).padStart(2, '0'); });
  /* karaoke captions: chunks of <=4 words, highlight on the spoken word */
  const caps = $('#caps');
  window.CAPTIONS.forEach(c => {
    const ws = c.words, chunks = []; let cur = [];
    ws.forEach((w, i) => { cur.push(w); if (cur.length >= 4 || /[.?!,]$/.test(w[0]) && cur.length >= 2) { chunks.push(cur); cur = []; } });
    if (cur.length) { if (chunks.length && cur.length === 1) chunks[chunks.length - 1].push(cur[0]); else chunks.push(cur); }
    chunks.forEach((ch, ci) => {
      const t0 = ch[0][1] - 0.04, nx = chunks[ci + 1]; const t1 = nx ? nx[0][1] - 0.04 : Math.min(c.end, ch[ch.length - 1][2] + 0.45);
      const d = h(`<div class="cap"><div class="cp">${ch.map(w => `<span>${w[0]}</span>`).join(' ')}</div></div>`, caps);
      tl.set(d, { opacity: 1 }, t0).set(d, { opacity: 0 }, t1);
      tl.fromTo(d, { y: 26, scale: .96 }, { y: 0, scale: 1, duration: .16, ease: 'power3.out' }, t0);
      $$('span', d).forEach((sp, k) => tl.set(sp, { color: '#FF6E05', scale: 1.0 }, ch[k][1]).set(sp, { color: '#F4EFE9' }, ch[k][2] + 0.0));
    });
  });
})();
