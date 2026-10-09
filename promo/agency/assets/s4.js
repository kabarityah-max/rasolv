/* ===== I · sound (31.875–35.625 s)  "Voice, music and captions, composed around you." ===== */
(() => {
  const s = $('#sI .in'); const t0 = T(68);
  const a = h(`<div class="abs disp" style="left:70px;top:190px;font-size:104px;white-space:nowrap">Composed</div>`, s), b = h(`<div class="abs disp" style="left:70px;top:304px;font-size:140px;font-weight:600;white-space:nowrap">around you.</div>`, s);
  reveal(chars(a), t0 - .05, { stagger: .03, d: .5 }); reveal(chars(b, 'ch gt'), t0 + .1, { stagger: .03, d: .55 });
  const bars = n => `<div class="abs" style="left:44px;right:44px;top:108px;height:110px;display:flex;align-items:center;gap:4px">${'<i style="flex:1;border-radius:3px;background:linear-gradient(180deg,#FFC59A,#FF6E05);height:12px;display:block"></i>'.repeat(n)}</div>`;
  const row = (y, label, sub, inner) => h(`<div class="glass" style="left:60px;top:${y}px;width:960px;height:250px;border-radius:44px"><div class="abs disp" style="left:44px;top:28px;font-size:48px;font-weight:500">${label}</div><div class="abs mono" style="right:44px;top:42px;font-size:22px;letter-spacing:.28em;color:rgba(244,239,233,.7)">${sub}</div>${inner}</div>`, s);
  const r1 = row(520, 'Voice', 'NATURAL · ON BRAND', bars(100));
  const r2 = row(800, 'Music', 'ORIGINAL SCORE', bars(100));
  const r3 = row(1080, 'Captions', 'SYNCED TO EVERY WORD', `<div class="abs disp" id="i-cap" style="left:44px;top:112px;font-size:76px;white-space:nowrap;font-weight:500"><span>Voice,</span> <span>music</span> <span>and</span> <span>captions</span></div>`);
  [[r1, -1100], [r2, 1100], [r3, -1100]].forEach(([r, x], i) => tl.fromTo(r, { x, opacity: 0 }, { x: 0, opacity: 1, duration: .5, ease: E.snap }, t0 + .1 + i * .35));
  const A = $$('i', r1), B = $$('i', r2);
  drive(t0, 3.75, p => { const t = p * 3.75;
    A.forEach((e, i) => e.style.height = (10 + 98 * Math.abs(Math.sin(t * 6.3 + i * .37)) * (.3 + .7 * Math.abs(Math.sin(i * .21 + t * 2.1))) * (1 - Math.abs(i - 50) / 120)) + 'px');
    B.forEach((e, i) => e.style.height = (10 + 98 * Math.abs(Math.sin(t * 7.5 + i * .55 + Math.sin(t * 3 + i * .1))) * (.5 + .5 * Math.sin(i * .09 + t))) + 'px'); });
  const cw = $$('span', $('#i-cap'));
  cw.forEach(w => w.style.color = 'rgba(244,239,233,.45)');
  [.15, .45, .8, 1.05].forEach((o, k) => tl.set(cw[k], { color: '#FF8A33' }, t0 + 1.2 + o));
})();

/* ===== J · one line of code, whole film follows (35.625–39.375 s) ===== */
(() => {
  const s = $('#sJ .in'); const t0 = T(76);
  const code = h(`<div class="glass" style="left:60px;top:200px;width:960px;height:520px;border-radius:36px"></div>`, s);
  code.innerHTML = `<div class="abs mono" style="left:36px;top:26px;font-size:22px;letter-spacing:.18em;color:rgba(244,239,233,.55)">FILM.CONFIG.JS</div><div class="abs" style="left:36px;right:36px;top:72px;height:1px;background:rgba(255,255,255,.15)"></div>
   <div class="abs mono" style="left:36px;top:96px;font-size:32px;line-height:1.62;white-space:pre;color:rgba(244,239,233,.28)">1\n2\n3\n4\n5\n6</div>
   <div class="abs mono" style="left:90px;top:96px;font-size:32px;line-height:1.62;white-space:pre;color:#F4EFE9"><div><span style="color:#ff7aa8">const</span> film = {</div><div id="j-l2">  title:  <span id="j-t" style="color:#ffd9a8"></span>,</div><div id="j-l3">  accent: <span id="j-c" style="color:#ffd9a8"></span>,</div><div>  format: <span style="color:#ffd9a8">"9:16"</span>,</div><div>  voice:  <span style="color:#ffd9a8">"af_heart"</span>,</div><div>};</div></div>
   <div class="abs" id="j-hl" style="left:0;top:140px;width:100%;height:52px;background:linear-gradient(90deg,rgba(255,110,5,.28),rgba(255,110,5,0));border-left:5px solid #FF6E05;opacity:0"></div>`;
  tl.fromTo(code, { y: -700, opacity: 0, rotationX: 20 }, { y: 0, opacity: 1, rotationX: 0, duration: .5, ease: E.snap }, t0 - .1);
  // preview
  const pv = h(`<div class="glass" style="left:375px;top:800px;width:330px;height:590px;border-radius:44px"></div>`, s);
  pv.innerHTML = `<div class="abs" id="j-pbg" style="inset:0;opacity:.55"></div><div class="abs" id="j-pap" style="left:95px;top:90px;width:140px;height:140px"></div><div class="abs disp" id="j-pt" style="left:0;right:0;text-align:center;top:290px;font-size:50px;font-weight:600;line-height:1"></div><div class="abs mono" style="left:0;right:0;text-align:center;top:360px;font-size:18px;letter-spacing:.3em;color:rgba(255,255,255,.7)">YOUR BRAND</div><div class="abs" style="left:34px;right:34px;bottom:44px;height:6px;border-radius:3px;background:rgba(255,255,255,.2)"><i id="j-pg" style="display:block;height:100%;width:60%;border-radius:3px"></i></div>`;
  tl.fromTo(pv, { y: 900, opacity: 0, scale: .9 }, { y: 0, opacity: 1, scale: 1, duration: .55, ease: E.snap }, t0 + .15);
  const lab1 = h(`<div class="abs mono" id="j-v" style="left:60px;top:1060px;font-size:26px;letter-spacing:.3em;color:rgba(244,239,233,.7)">VERSION 01</div>`, s);
  const lab2 = h(`<div class="abs mono" id="j-x" style="right:60px;top:1060px;font-size:26px;letter-spacing:.2em;text-align:right;color:rgba(244,239,233,.7)">#FF6E05</div>`, s);
  const V = [['Spring Launch', '#FF6E05'], ['Autumn Offer', '#4F8CFF'], ['Summer Drop', '#2DD4A7']], sw = [.75, 2.0];
  const hex2 = c => [1, 3, 5].map(i => parseInt(c.slice(i, i + 2), 16));
  const mix = (a, b, k) => { const A = hex2(a), B = hex2(b); return `rgb(${A.map((v, i) => Math.round(v + (B[i] - v) * k)).join(',')})`; };
  const typed = (o, n, u) => u < 0 ? o : u < .15 ? o.slice(0, Math.round(o.length * (1 - u / .15))) : n.slice(0, Math.round(n.length * Math.min(1, (u - .15) / .4)));
  drive(t0 - .1, 3.75, p => {
    const t = p * 3.75 - .1; let vi = 0; sw.forEach((x, k) => { if (t >= x) vi = k + 1; });
    const o = V[Math.max(0, vi - 1)], n = V[vi], u = vi ? t - sw[vi - 1] : -1;
    const ts = vi ? typed(o[0], n[0], u) : V[0][0], cs = vi ? typed(o[1], n[1], u) : V[0][1];
    $('#j-t').textContent = `"${ts}"`; $('#j-c').textContent = `"${cs}"`;
    const k = vi ? Math.max(0, Math.min(1, (u - .35) / .25)) : 1, col = mix(vi ? o[1] : V[0][1], n[1], k);
    $('#j-hl').style.opacity = t > .15 && vi ? (u < .75 ? 1 : 0) : (t > .5 && t < .75 ? 1 : 0); $('#j-hl').style.top = (u < .3 && vi ? 140 : 188) + 'px';
    $('#j-pbg').style.background = `linear-gradient(160deg, ${col}, #0a0a10 80%)`; $('#j-pg').style.background = col;
    ap($('#j-pap'), { r: 37, grow: 1, bp: 0, color: col, gap: '#0a0a10', lines: false });
    $('#j-pt').textContent = vi ? (u < .35 ? o[0] : n[0]) : V[0][0]; $('#j-x').textContent = cs; $('#j-x').style.color = col; $('#j-v').textContent = 'VERSION 0' + (vi + 1);
  });
  [sw[0], sw[1]].forEach(x => tl.fromTo('#j-pt', { y: 0 }, { y: -6, duration: .12, yoyo: true, repeat: 1 }, t0 + x + .35));
})();

/* ===== K · one source, every format (39.375–43.125 s) ===== */
(() => {
  const s = $('#sK .in'); const t0 = T(84);
  const a = h(`<div class="abs disp" style="left:70px;top:190px;font-size:104px;white-space:nowrap">One source.</div>`, s), b = h(`<div class="abs disp" style="left:70px;top:304px;font-size:128px;font-weight:600;white-space:nowrap">Every format.</div>`, s);
  reveal(chars(a), t0 - .05, { stagger: .03, d: .5 }); reveal(chars(b, 'ch gt'), t0 + .12, { stagger: .03, d: .55 });
  const body = (w, hh) => { const m = Math.min(w, hh); return `<div class="abs" style="inset:0;background:linear-gradient(160deg,#5a2308,#0a0b11 72%)"></div><div class="abs" style="left:${w / 2 - m * .17}px;top:${hh * .16}px;width:${m * .34}px;height:${m * .34}px" data-ap></div><div class="abs disp" style="left:0;right:0;text-align:center;top:${hh * .58}px;font-size:${m * .13}px;font-weight:600;line-height:1">Your brand.</div><div class="abs" style="left:${w * .18}px;right:${w * .18}px;bottom:${hh * .1}px;height:${Math.max(3, m * .014)}px;background:#FF6E05"></div>`; };
  const frame = (x, y, w, hh, label) => { const f = h(`<div class="glass" style="left:${x}px;top:${y}px;width:${w}px;height:${hh}px;border-radius:${Math.min(w, hh) * .07}px">${body(w, hh)}</div>`, s); ap($('[data-ap]', f), { r: 37, grow: 1, bp: 0, gap: '#07080c', lines: false }); const l = h(`<div class="abs mono" style="left:${x}px;top:${y + hh + 14}px;font-size:30px;letter-spacing:.3em;color:#FF9A3D">${label}</div>`, s); return [f, l]; };
  // morphing source frame
  const mw = { w: 300, h: 533 };
  const src = h(`<div class="glass" id="k-src" style="left:390px;top:640px;width:300px;height:533px;border-radius:24px"></div>`, s);
  const lab = h(`<div class="abs mono center" id="k-lab" style="top:1230px;font-size:40px;letter-spacing:.4em;color:#FF9A3D;font-weight:700">9:16</div>`, s);
  const shapes = [[300, 533, '9:16'], [480, 480, '1:1'], [760, 428, '16:9']];
  const draw = (w, hh) => { src.innerHTML = body(w, hh); ap($('[data-ap]', src), { r: 37, grow: 1, bp: 0, gap: '#07080c', lines: false }); };
  draw(300, 533);
  tl.fromTo(src, { scale: .5, opacity: 0, rotationY: 80 }, { scale: 1, opacity: 1, rotationY: 0, duration: .45, ease: E.out }, t0 - .05);
  drive(t0 + .35, 1.2, p => { const seg = Math.min(1.999, p * 2), i = Math.floor(seg), k = ease('power3.inOut', seg - i); const A = shapes[i], B = shapes[i + 1]; const w = A[0] + (B[0] - A[0]) * k, hh = A[1] + (B[1] - A[1]) * k;
    src.style.width = w + 'px'; src.style.height = hh + 'px'; src.style.left = (540 - w / 2) + 'px'; src.style.top = (900 - hh / 2) + 'px'; draw(w, hh); lab.textContent = k > .5 ? B[2] : A[2]; });
  tl.to(src, { opacity: 0, scale: .9, duration: .25 }, t0 + 1.62); tl.to(lab, { opacity: 0, duration: .2 }, t0 + 1.6);
  const F = [frame(160, 500, 760, 428, '16:9'), frame(160, 1000, 340, 340, '1:1'), frame(580, 980, 240, 427, '9:16')];
  F.forEach(([f, l], i) => { tl.fromTo(f, { scale: .2, opacity: 0, y: 150 - i * 30 }, { scale: 1, opacity: 1, y: 0, duration: .5, ease: E.back }, t0 + 1.72 + i * .14); tl.fromTo(l, { opacity: 0 }, { opacity: 1, duration: .3 }, t0 + 2.0 + i * .14); });
})();

/* ===== L · precision of code, feel of cinema (43.125–46.875 s) ===== */
(() => {
  const s = $('#sL .in'); const t0 = T(92);
  // ruler / grid ("precision")
  const rl = h(`<svg class="abs" style="left:0;top:0" width="1080" height="1920" viewBox="0 0 1080 1920"><g stroke="rgba(244,239,233,.45)" stroke-width="2">${[...Array(55)].map((_, i) => `<line x1="${60 + i * 18}" y1="${i % 5 ? 520 : 500}" x2="${60 + i * 18}" y2="540" />`).join('')}</g><line x1="60" y1="540" x2="1020" y2="540" stroke="rgba(244,239,233,.6)" stroke-width="2"/></svg>`, s);
  tl.fromTo(rl, { opacity: 0, clipPath: 'inset(0 100% 0 0)' }, { opacity: 1, clipPath: 'inset(0 0% 0 0)', duration: .6, ease: E.out }, t0 - .05);
  const pr = h(`<div class="abs mono" id="l-pr" style="left:60px;top:300px;font-size:70px;font-weight:700;letter-spacing:-.02em;white-space:nowrap"></div>`, s);
  h(`<div class="abs mono" style="left:62px;top:220px;font-size:28px;letter-spacing:.34em;color:#FF9A3D">// 01 · PRECISION</div>`, s);
  const full = 'Precision of code.'; drive(t0 + .05, .8, p => { const n = Math.floor(p * full.length); pr.innerHTML = p >= 1 ? full : full.slice(0, n) + '<span style="color:#FF6E05">▍</span>'; });
  // cinema strip
  const strip = h(`<div class="abs" id="l-strip" style="left:0;top:590px;width:1080px;height:520px;overflow:hidden;background:radial-gradient(60% 90% at 50% 50%,#2a1305,#07080c)"></div>`, s);
  const sk = h(`<div class="abs" style="left:0;top:0;width:1080px;height:520px"></div>`, strip);
  for (let i = 0; i < 9; i++) h(`<div class="abs" style="left:${60 + i * 120}px;top:${60 + (i * 83) % 280}px;width:${50 + (i * 37) % 70}px;height:${50 + (i * 37) % 70}px;border-radius:50%;background:radial-gradient(circle,rgba(255,170,90,.55),rgba(255,110,5,0) 70%);filter:blur(4px)" class="bk"></div>`, sk);
  const host = h(`<div class="abs" id="l-ap" style="left:410px;top:100px;width:260px;height:260px"></div>`, strip); ap(host, { r: 37, grow: 1, bp: 1, gap: '#07080c' });
  const streak = h(`<div class="abs" id="l-streak" style="left:-100px;top:252px;width:1280px;height:6px;background:linear-gradient(90deg,transparent,rgba(255,200,150,.95) 30%,#fff 50%,rgba(255,200,150,.95) 70%,transparent);filter:blur(1.5px);box-shadow:0 0 36px 6px rgba(255,140,50,.7)"></div>`, strip);
  h(`<div class="abs mono" style="left:30px;top:18px;font-size:20px;letter-spacing:.3em;color:rgba(244,239,233,.7)">2.39:1 · 24P</div><div class="abs mono" style="right:30px;top:18px;font-size:20px;letter-spacing:.3em;color:rgba(244,239,233,.7)">● REC</div>`, strip);
  tl.fromTo(strip, { clipPath: 'inset(50% 0 50% 0)' }, { clipPath: 'inset(0% 0 0% 0)', duration: .55, ease: E.io }, t0 + 1.0);
  tl.fromTo(host, { scale: .5, rotation: -80, opacity: 0 }, { scale: 1, rotation: 0, opacity: 1, duration: .8, ease: E.out }, t0 + 1.2);
  tl.fromTo(streak, { scaleX: 0, opacity: 0 }, { scaleX: 1, opacity: 1, duration: .5, ease: E.out }, t0 + 1.35);
  $$('.bk', sk).forEach((b, i) => tl.fromTo(b, { x: 0, opacity: 0 }, { x: -80 - i * 14, opacity: 1, duration: 2, ease: 'none' }, t0 + 1.0));
  tl.to(sk, { scale: 1.08, duration: 2.5, ease: 'none' }, t0 + 1.0);
  h(`<div class="abs mono" style="left:62px;top:1150px;font-size:28px;letter-spacing:.34em;color:#FF9A3D">// 02 · CINEMA</div>`, s);
  const fc = h(`<div class="abs disp" style="left:60px;top:1205px;font-size:128px;white-space:nowrap"><span>Feel of </span><b class="gt">cinema.</b></div>`, s);
  const cs = chars(fc.firstElementChild).concat(chars(fc.lastElementChild, 'ch gt')); reveal(cs, t0 + 1.25, { stagger: .035, d: .55, y: 70 });
})();
