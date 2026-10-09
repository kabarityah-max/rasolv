/* ===== F · 3D phone (18.75–22.5) ===== */
(() => {
  const s = $('#sF .in'); const t0 = T(40);
  h(`<div class="abs big center" id="f-bg3d" style="top:560px;font-size:720px;line-height:1;color:transparent;-webkit-text-stroke:4px rgba(255,110,5,.55);letter-spacing:-.04em">3D</div>`, s);
  const yp = h(`<div class="abs big" style="left:60px;top:170px;font-size:140px;line-height:.9" id="f-yp">YOUR<br><span class="or">PRODUCT</span></div>`, s);
  const stage = h(`<div class="abs" style="inset:0;perspective:1700px;perspective-origin:50% 50%"></div>`, s);
  const ph = h(`<div class="abs" id="f-phone" style="left:320px;top:520px;width:440px;height:900px;transform-style:preserve-3d"></div>`, stage);
  for (let i = 1; i <= 8; i++) h(`<div class="abs" style="inset:0;border-radius:78px;background:linear-gradient(160deg,#3a3a3d,#111);transform:translateZ(${-i * 4}px)"></div>`, ph);
  const front = h(`<div class="abs" style="inset:0;border-radius:78px;background:#0b0b0c;border:10px solid #2b2b2e;box-shadow:inset 0 0 0 2px #555, 0 0 120px rgba(255,110,5,.45);overflow:hidden;transform:translateZ(2px)"></div>`, ph);
  front.innerHTML = `<div class="abs" style="inset:0;background:radial-gradient(90% 55% at 15% 8%,#FF6E05,#a63d00 40%,#0b0b0c 75%)"></div>
   <div class="abs" style="left:150px;top:18px;width:120px;height:34px;border-radius:17px;background:#000"></div>
   <div class="abs mono" style="left:44px;top:24px;font-size:22px;font-weight:700">9:41</div>
   <div class="glass" style="left:22px;top:92px;width:376px;height:168px;border-radius:38px;box-shadow:inset 0 2px 0 rgba(255,255,255,.5),0 20px 40px rgba(0,0,0,.4)">
     <div class="abs" style="left:24px;top:16px;font-size:17px;letter-spacing:.14em;font-weight:800;display:flex;gap:8px;align-items:center"><span class="dot" style="width:12px;height:12px"></span>RASOLV <span style="margin-left:auto;color:#ffb27a">● LIVE</span></div>
     <div class="abs" style="left:24px;top:52px;font-size:34px;font-weight:800;line-height:1.05">An expert is on it</div>
     <div class="abs" style="left:24px;top:98px;font-size:18px;color:rgba(255,255,255,.75)">Ticket #4821 · reply in ~2 min</div>
     <div class="abs" style="left:24px;top:128px;display:flex">${['#FF6E05', '#5a6cff', '#e0457b'].map((c, i) => `<i style="width:30px;height:30px;border-radius:50%;background:${c};border:3px solid #222;margin-left:${i ? -8 : 0}px"></i>`).join('')}<span style="margin-left:10px;font-size:16px;color:rgba(255,255,255,.8);line-height:30px">3 experts reviewing</span></div>
   </div>
   <div class="abs" style="left:28px;top:300px;font-size:26px;font-weight:800">Active now</div>
   ${[['Maya Haddad', 'Billing expert', '#FF6E05'], ['Omar Khalil', 'Tech support', '#5a6cff'], ['Lina Saeed', 'Accounts', '#e0457b']].map((r, i) => `<div class="abs" style="left:22px;top:${346 + i * 96}px;width:376px;height:84px;border-radius:26px;background:rgba(255,255,255,.09);border:1px solid rgba(255,255,255,.14)"><i class="abs" style="left:16px;top:16px;width:52px;height:52px;border-radius:50%;background:${r[2]}"></i><div class="abs" style="left:84px;top:14px;font-size:22px;font-weight:700">${r[0]}</div><div class="abs" style="left:84px;top:44px;font-size:17px;color:rgba(255,255,255,.6)">${r[1]} · ★★★★★</div></div>`).join('')}
   <div class="abs" style="left:22px;right:22px;top:660px;height:84px;border-radius:42px;background:#FF6E05;color:#000;font-weight:800;font-size:26px;text-align:center;line-height:84px">Say thanks ↑</div>
   <div class="abs" style="left:140px;bottom:14px;width:140px;height:6px;border-radius:3px;background:rgba(255,255,255,.8)"></div>`;
  [['BILLING', -70, 300, 150], ['LIVE', 380, 180, 210], ['4 MIN', -40, 760, 180], ['SOLVED ✓', 390, 700, 120]].forEach(([l, x, y, z], i) => {
    const c = h(`<div class="chip glass" style="left:${x}px;top:${y}px;height:78px;font-size:30px;transform:translateZ(${z}px)"><span class="dot"></span>${l}</div>`, ph);
    tl.fromTo(c, { opacity: 0, scale: .3 }, { opacity: 1, scale: 1, duration: .4, ease: E.back }, t0 + .25 + i * .18);
    tl.to(c, { y: '+=' + (i % 2 ? 26 : -26), duration: 1.1, ease: 'sine.inOut', yoyo: true, repeat: 2 }, t0 + .2 + i * .1);
  });
  tl.fromTo('#f-yp', { x: -800, opacity: 0 }, { x: 0, opacity: 1, duration: .34, ease: E.snap }, t0 - .05);
  tl.fromTo('#f-bg3d', { scale: .6, opacity: 0 }, { scale: 1, opacity: 1, duration: .5, ease: E.out }, t0);
  tl.fromTo(ph, { rotationY: -75, rotationX: 14, y: 300, scale: .8, opacity: 0 }, { rotationY: -28, rotationX: 8, y: 0, scale: 1, opacity: 1, duration: .5, ease: E.out }, t0 - .2);
  [[28, .5, .5], [-26, .4, 1.2], [14, .35, 2.0], [-8, .6, 2.7]].forEach(([ry, rx, t]) => tl.to(ph, { rotationY: ry, rotationX: rx * 10, duration: .5, ease: 'power3.inOut' }, t0 + t));
  tl.to('#f-bg3d', { rotation: 6, x: 40, duration: 3.2, ease: 'none' }, t0);
})();

/* ===== G · live data / orbit (22.5–26.25) ===== */
(() => {
  const s = $('#sG .in'); const t0 = T(48); const cx = 540, cy = 860;
  const words = ['LIVE DATA', 'ORBITING', 'COUNTING', 'ALIVE.'];
  const hd = words.map((w, i) => h(`<div class="abs big center ${i % 2 ? 'or' : ''}" style="top:190px;font-size:${i == 0 ? 168 : 168}px;white-space:nowrap;opacity:0">${w}</div>`, s));
  [0.0, .76, 1.46, 2.34].forEach((o, i) => { const a = t0 + o; tl.set(hd[i], { opacity: 1 }, a); if (i < 3) tl.set(hd[i], { opacity: 0 }, t0 + [.76, 1.46, 2.34][i]); tl.fromTo(hd[i], { y: -120, scale: 1.5, filter: 'blur(14px)' }, { y: 0, scale: 1, filter: 'blur(0px)', duration: .26, ease: E.snap }, a - .04); });
  const svg = h(`<svg class="abs" style="left:0;top:0" width="1080" height="1920" viewBox="0 0 1080 1920"><g fill="none" stroke="rgba(255,255,255,.18)" stroke-width="2"><ellipse cx="${cx}" cy="${cy}" rx="400" ry="250"/><ellipse cx="${cx}" cy="${cy}" rx="300" ry="520" transform="rotate(30 ${cx} ${cy})"/><ellipse cx="${cx}" cy="${cy}" rx="300" ry="520" transform="rotate(-30 ${cx} ${cy})"/></g>
    <circle cx="${cx}" cy="${cy}" r="196" fill="rgba(255,255,255,.05)" stroke="rgba(255,255,255,.2)" stroke-width="18"/>
    <circle id="g-arc" cx="${cx}" cy="${cy}" r="196" fill="none" stroke="#FF6E05" stroke-width="18" stroke-linecap="round" transform="rotate(-90 ${cx} ${cy})" stroke-dasharray="1232" stroke-dashoffset="1232"/></svg>`, s);
  const num = h(`<div class="abs mono center" id="g-num" style="top:${cy - 76}px;font-size:150px;font-weight:700;letter-spacing:-.04em">0%</div>`, s);
  tl.fromTo(svg, { scale: .6, opacity: 0, transformOrigin: '540px 860px' }, { scale: 1, opacity: 1, duration: .45, ease: E.out }, t0 - .1);
  drive(t0 + .1, 1.7, p => { const k = gsap.parseEase('power2.out')(p); $('#g-arc').style.strokeDashoffset = 1232 * (1 - k); num.textContent = Math.round(k * 100) + '%'; });
  const chips = ['DATA', 'CHARTS', 'TICKERS', 'KPIs', 'LIVE'].map((l, i) => h(`<div class="chip glass" style="left:0;top:0;height:76px;font-size:30px;opacity:0"><span class="dot"></span>${l}</div>`, s));
  drive(t0, 3.75, p => chips.forEach((c, i) => { const a = i / chips.length * 6.283 + p * 5.2; const x = cx + 400 * Math.cos(a), y = cy + 250 * Math.sin(a); const z = Math.sin(a) * .5 + .5; c.style.transform = `translate(${x - 90}px,${y - 38}px) scale(${.75 + z * .45})`; c.style.zIndex = Math.round(z * 10); c.style.opacity = Math.min(1, p * 9 + 0); }));
  // bars + sparkline
  const bars = h(`<div class="abs" style="left:90px;top:1190px;width:900px;height:240px;display:flex;align-items:flex-end;gap:18px"></div>`, s);
  const hs = [.35, .55, .42, .7, .5, .85, .66, .95, .78];
  hs.forEach((v, i) => { const b = h(`<div class="glass" style="position:relative;flex:1;height:${v * 230}px;border-radius:18px;background:linear-gradient(180deg,rgba(255,110,5,.9),rgba(255,110,5,.25))"></div>`, bars); tl.fromTo(b, { scaleY: 0, transformOrigin: '50% 100%' }, { scaleY: 1, duration: .5, ease: E.back }, t0 + .5 + i * .08); });
  tl.fromTo(bars, { opacity: 0 }, { opacity: 1, duration: .2 }, t0 + .45);
})();

/* ===== H · use cases (26.25–30) ===== */
(() => {
  const s = $('#sH .in'); const t0 = T(56);
  h(`<div class="abs big center" style="top:190px;font-size:116px;white-space:nowrap">WHAT WE <span class="or">MAKE</span></div>`, s);
  const defs = [
    ['TRAINING', 'FILMS', 60, 570, -1400, 0, `<svg viewBox="0 0 200 200" width="200" height="200"><circle cx="100" cy="100" r="78" fill="none" stroke="rgba(255,255,255,.2)" stroke-width="16"/><circle class="hr" cx="100" cy="100" r="78" fill="none" stroke="#FF6E05" stroke-width="16" stroke-linecap="round" transform="rotate(-90 100 100)" stroke-dasharray="490" stroke-dashoffset="490"/><path class="hc" d="M62 104 L90 130 L142 76" fill="none" stroke="#fff" stroke-width="16" stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="130" stroke-dashoffset="130"/></svg>`],
    ['LAUNCH', 'FILMS', 390, 680, 0, 1500, `<svg viewBox="0 0 200 200" width="200" height="200"><path class="hl" d="M30 170 Q70 150 100 100 T170 30" fill="none" stroke="#FF6E05" stroke-width="12" stroke-linecap="round" stroke-dasharray="260" stroke-dashoffset="260"/><path class="hp" d="M170 30 l-34 6 l24 24z" fill="#fff" opacity="0"/><circle class="hd" cx="30" cy="170" r="12" fill="#fff"/></svg>`],
    ['BRAND', 'STORIES', 720, 570, 1400, 0, `<div class="hap" style="width:200px;height:200px"></div>`],
  ];
  const cards = defs.map(([a, b, x, y, fx, fy, art], i) => {
    const c = h(`<div class="glass" style="left:${x}px;top:${y}px;width:300px;height:640px;border-radius:56px"><div class="abs center" style="top:70px;display:flex;justify-content:center">${art}</div><div class="abs big center" style="top:340px;font-size:${a.length > 6 ? 52 : 60}px;line-height:.95">${a}<br><span class="or">${b}</span></div><div class="abs mono center" style="top:560px;font-size:22px;letter-spacing:.3em;color:rgba(255,255,255,.6)">0${i + 1} / 03</div></div>`, s);
    const t = t0 + i * 2 * BEAT - .05;
    tl.fromTo(c, { x: fx, y: fy, rotation: i == 1 ? 0 : (i ? 14 : -14), opacity: 0 }, { x: 0, y: 0, rotation: 0, opacity: 1, duration: .45, ease: E.snap }, t);
    tl.to(c, { y: -22, duration: .8, ease: 'sine.inOut', yoyo: true, repeat: 1 }, t + .5);
    return c;
  });
  const ring = $('.hr', cards[0]), chk = $('.hc', cards[0]), ln = $('.hl', cards[1]), tri = $('.hp', cards[1]), hap = $('.hap', cards[2]);
  tl.to(ring, { strokeDashoffset: 0, duration: .8, ease: 'power2.out' }, t0 + .2).to(chk, { strokeDashoffset: 0, duration: .35 }, t0 + .8);
  tl.to(ln, { strokeDashoffset: 0, duration: .7, ease: 'power2.out' }, t0 + 2 * BEAT + .2).to(tri, { opacity: 1, duration: .1 }, t0 + 2 * BEAT + .85);
  drive(t0 + 4 * BEAT, .8, p => ap(hap, { r: 37, grow: gsap.parseEase('power3.out')(p), bp: p, gap: '#1a0f08' }));
  ap(hap, { r: 37, grow: 0, bp: 0 });
  tl.fromTo(hap, { rotation: -90, scale: .4 }, { rotation: 0, scale: 1, duration: .8, ease: E.out }, t0 + 4 * BEAT);
  const st = h(`<div class="abs" style="left:150px;top:1330px;padding:22px 44px;border-radius:20px;background:#FF6E05;color:#060606;font-weight:900;font-size:60px;letter-spacing:.02em;transform:rotate(-4deg)">ANY BRAND. ANY STORY.</div>`, s);
  tl.fromTo(st, { scale: 3, opacity: 0, rotation: -14 }, { scale: 1, opacity: 1, rotation: -4, duration: .26, ease: E.snap }, t0 + 6 * BEAT + .1);
})();
