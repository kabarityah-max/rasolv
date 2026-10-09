/* ===== D1 · kinetic type, 4 sub-cuts (11.25–13.125) ===== */
(() => {
  const s = $('#sD1 .in'); const t0 = T(24);
  const mk = (bg, html) => h(`<div class="abs" style="inset:0;background:${bg};opacity:0;overflow:hidden">${html}</div>`, s);
  const ticker = (txt, top, col, dir) => `<div class="abs mono" style="left:0;top:${top}px;white-space:nowrap;font-size:96px;font-weight:700;color:${col};letter-spacing:.04em" data-dir="${dir}">${(txt + ' ✻ ').repeat(8)}</div>`;
  const p1 = mk('#FF6E05', `<div class="abs" id="d1-ring" style="left:-180px;top:380px;width:1440px;height:1440px;opacity:.22"></div>${ticker('MOTION', 200, '#060606', -1)}${ticker('MOTION', 1560, '#060606', 1)}<div class="abs big center" id="d1-w1" style="top:700px;font-size:240px;color:#060606;white-space:nowrap">MOTION</div>`);
  const p2 = mk('#060606', `${ticker('GRAPHICS', 200, 'rgba(255,110,5,.5)', 1)}${ticker('GRAPHICS', 1560, 'rgba(255,110,5,.5)', -1)}<div class="abs big center" id="d1-w2" style="top:760px;font-size:176px;color:transparent;-webkit-text-stroke:5px #F4EFE9;white-space:nowrap">GRAPHICS</div>` + [0, 1, 2].map(i => `<div class="glass d1g" style="left:${120 + i * 330}px;top:${430 + (i % 2) * 740}px;width:260px;height:260px;border-radius:60px"></div>`).join(''));
  const p3 = mk('#F4EFE9', `<div class="abs big" id="d1-w3a" style="left:60px;top:430px;font-size:250px;color:#060606">THAT</div><div class="abs big" id="d1-w3b" style="left:60px;top:690px;font-size:250px;color:#FF6E05">NEVER</div><div class="abs mono" style="left:64px;top:1080px;font-size:44px;letter-spacing:.3em;color:#060606;font-weight:700">NOT FOR A SECOND</div>`);
  const p4 = mk('#060606', `<div class="abs big" id="d1-w4" style="left:0;right:0;top:430px;text-align:center;font-size:330px;line-height:.9"><div>SIT</div><div class="or">STILL</div></div>`);
  ap($('#d1-ring'), { r: 37, grow: 1, bp: 0, color: '#060606', gap: '#FF6E05', lines: false });
  tl.to('#d1-ring', { rotation: 180, duration: 1.9, ease: 'none' }, t0 - 0.2);
  const subs = [p1, p2, p3, p4];
  subs.forEach((p, i) => { const a = t0 + i * BEAT; tl.set(p, { opacity: 1 }, a - (i ? 0 : 0.2)); if (i) tl.set(subs[i - 1], { opacity: 0 }, a); });
  // each sub-cut gets a punchy entrance
  tl.fromTo('#d1-w1', { x: -1200, rotation: -9, scale: 1.2 }, { x: 0, rotation: 0, scale: 1, duration: .26, ease: E.snap }, t0 - .05);
  tl.fromTo('#d1-w2', { x: 1200, skewX: -20 }, { x: 0, skewX: 0, duration: .26, ease: E.snap }, t0 + BEAT);
  $$('.d1g').forEach((g, i) => { tl.fromTo(g, { scale: 0, rotation: -90 }, { scale: 1, rotation: 0, duration: .35, ease: E.back }, t0 + BEAT + .06 * i); tl.to(g, { rotation: 360, y: '+=60', duration: .5, ease: 'sine.inOut' }, t0 + BEAT + .1); });
  tl.fromTo('#d1-w3a', { y: -500, opacity: 0 }, { y: 0, opacity: 1, duration: .24, ease: E.snap }, t0 + 2 * BEAT);
  tl.fromTo('#d1-w3b', { y: 500, opacity: 0 }, { y: 0, opacity: 1, duration: .24, ease: E.snap }, t0 + 2 * BEAT + .08);
  tl.fromTo('#d1-w4 div', { scale: 3, opacity: 0, rotation: (i) => i ? 12 : -12 }, { scale: 1, opacity: 1, rotation: 0, duration: .26, ease: E.snap, stagger: .1 }, t0 + 3 * BEAT);
  tl.to('#d1-w4 div', { y: -26, duration: .2, yoyo: true, repeat: 3, ease: 'sine.inOut', stagger: .1 }, t0 + 3 * BEAT + .35);
  // tickers drift
  $$('.mono[data-dir]', s).forEach(e => { const d = +e.dataset.dir; tl.fromTo(e, { x: d > 0 ? -1800 : 0 }, { x: d > 0 ? 0 : -1800, duration: 1.9, ease: 'none' }, t0 - .2); });
})();

/* ===== D2 · liquid glass lens (13.125–15.0) ===== */
(() => {
  const s = $('#sD2 .in'); const t0 = T(28);
  const lines = ['LIQUID', 'GLASS', 'LIQUID', 'GLASS', 'LIQUID'];
  const layer = (cls, style = '') => `<div class="abs ${cls}" style="inset:0;${style}">${lines.map((l, i) => `<div class="abs big" style="left:40px;top:${230 + i * 250}px;font-size:${l == 'LIQUID' ? 230 : 280}px;white-space:nowrap;color:${i % 2 ? '#FF6E05' : 'rgba(244,239,233,.22)'};${i % 2 ? '' : '-webkit-text-stroke:3px rgba(244,239,233,.5);color:transparent'}">${l}</div>`).join('')}</div>`;
  const base = h(layer('d2base'), s);
  const mag = h(layer('d2mag', 'background:#0b0603;clip-path:circle(0px at 540px 960px);'), s);
  const lens = h(`<div class="abs" id="d2-lens" style="left:0;top:0;width:560px;height:560px;border-radius:50%;box-shadow:inset 0 0 0 3px rgba(255,255,255,.7), inset 10px 14px 40px rgba(255,255,255,.4), inset -14px -16px 40px rgba(255,110,5,.45), 0 40px 100px rgba(0,0,0,.6), 0 0 0 10px rgba(255,255,255,.08);background:radial-gradient(120% 90% at 30% 15%, rgba(255,255,255,.28), rgba(255,255,255,0) 52%)"></div>`, s);
  const spec = h(`<div class="abs" id="d2-spec" style="left:0;top:0;width:150px;height:60px;border-radius:50%;background:rgba(255,255,255,.7);filter:blur(8px)"></div>`, s);
  const fps = h(`<div class="abs mono" style="right:60px;top:1420px;font-size:40px;color:rgba(244,239,233,.85);font-weight:700;letter-spacing:.2em">REAL TIME · <span id="d2-fps">30</span> FPS</div>`, s);
  const path = p => [540 + Math.cos(p * 6.2 - 1.2) * 380, 880 + Math.sin(p * 9.4) * 420];
  drive(t0 - .2, 2.0, p => {
    const [x, y] = path(p), r = 280 * Math.min(1, p * 8);
    mag.style.clipPath = `circle(${r}px at ${x}px ${y}px)`; mag.style.transformOrigin = `${x}px ${y}px`; mag.style.transform = `scale(1.45)`;
    lens.style.transform = `translate(${x - 280}px,${y - 280}px) scale(${Math.min(1, p * 8)})`;
    spec.style.transform = `translate(${x - 150}px,${y - 200}px) rotate(-24deg)`; spec.style.opacity = Math.min(1, p * 8);
  });
  tl.fromTo([base], { x: 40, filter: 'blur(0px)' }, { x: -40, duration: 2, ease: 'none' }, t0 - .2);
  [0, 1, 2].forEach(i => { const c = h(`<div class="glass" style="left:${100 + i * 340}px;top:${1330 + (i % 2) * 40}px;width:220px;height:110px;border-radius:55px"></div>`, s); tl.fromTo(c, { y: 300, opacity: 0 }, { y: 0, opacity: 1, duration: .4, ease: E.back }, t0 + .1 * i); });
})();

/* ===== E · maps (15–18.75) ===== */
(() => {
  const s = $('#sE .in'); const t0 = T(32), M = window.MAP, P = M.pts;
  const stage = h(`<div class="abs" style="inset:0;perspective:1500px;perspective-origin:50% 45%"></div>`, s);
  const cam = h(`<div class="abs" id="e-cam" style="left:0;top:0;width:1080px;height:1920px;transform-style:preserve-3d;transform-origin:540px 860px"></div>`, stage);
  const world = h(`<div class="abs" id="e-world" style="left:0;top:0;width:2400px;height:1200px;transform-origin:0 0"></div>`, cam);
  const svg = `<svg width="2400" height="1200" viewBox="0 0 2400 1200"><path d="${M.grat}" fill="none" stroke="rgba(255,255,255,.07)" stroke-width="1.4"/>
    <g fill="rgba(244,239,233,.42)">${M.dots.map(d => `<circle cx="${d[0]}" cy="${d[1]}" r="3.6"/>`).join('')}</g><g id="e-arcs"></g><g id="e-pins"></g></svg>`;
  world.innerHTML = svg;
  const mid = ks => ks.reduce((a, k) => [a[0] + P[k][0] / ks.length, a[1] + P[k][1] / ks.length], [0, 0]);
  const shot = (ks, sc) => { const c = mid(ks); return { x: 540 - sc * c[0], y: 900 - sc * c[1], s: sc }; };
  const arcs = $('#e-arcs'), pins = $('#e-pins'), NS = 'http://www.w3.org/2000/svg';
  const addArc = (a, b, up) => { const A = P[a], B = P[b], mx = (A[0] + B[0]) / 2, my = (A[1] + B[1]) / 2 - up; const d = `M${A[0]},${A[1]} Q${mx},${my} ${B[0]},${B[1]}`;
    const pth = document.createElementNS(NS, 'path'); pth.setAttribute('d', d); pth.setAttribute('fill', 'none'); pth.setAttribute('stroke', '#FF6E05'); pth.setAttribute('stroke-width', 5); pth.setAttribute('stroke-linecap', 'round'); arcs.appendChild(pth);
    const L = Math.hypot(B[0] - A[0], B[1] - A[1]) * 1.15; pth.style.strokeDasharray = L; pth.style.strokeDashoffset = L; return [pth, L]; };
  const addPin = (k, label, u) => { const g = document.createElementNS(NS, 'g'); g.setAttribute('transform', `translate(${P[k][0]},${P[k][1]})`);
    g.innerHTML = `<circle r="${26 * u}" fill="rgba(255,110,5,.25)" class="ring"/><circle r="${9 * u}" fill="#FF6E05" stroke="#fff" stroke-width="${3 * u}"/><g transform="translate(${16 * u},${-34 * u})"><rect rx="${22 * u}" height="${44 * u}" width="${(label.length * 17 + 40) * u}" fill="rgba(20,20,20,.7)" stroke="rgba(255,255,255,.5)" stroke-width="${2 * u}"/><text x="${20 * u}" y="${30 * u}" font-family="Rubik" font-weight="800" font-size="${24 * u}" fill="#F4EFE9" letter-spacing="${1.5 * u}">${label}</text></g>`;
    pins.appendChild(g); g.style.opacity = 0; return g; };
  // shot 1 (Atlantic) then shot 2 (Asia)
  const s1 = shot(['newyork', 'london', 'tangier', 'saopaulo', 'dubai'], 1.5), s2 = shot(['dubai', 'mumbai', 'singapore', 'tokyo', 'sydney'], 1.75);
  const u1 = 1 / s1.s, u2 = 1 / s2.s;
  const A1 = [['tangier', 'london'], ['tangier', 'newyork'], ['tangier', 'saopaulo'], ['tangier', 'dubai'], ['tangier', 'lagos']].map(([a, b]) => addArc(a, b, 90));
  const pin1 = [['tangier', 'TANGIER'], ['london', 'LONDON'], ['newyork', 'NEW YORK'], ['saopaulo', 'SÃO PAULO'], ['dubai', 'DUBAI']].map(([k, l]) => addPin(k, l, u1 * 1.7));
  const A2 = [['dubai', 'mumbai'], ['dubai', 'singapore'], ['singapore', 'tokyo'], ['singapore', 'sydney']].map(([a, b]) => addArc(a, b, 70));
  const pin2 = [['mumbai', 'MUMBAI'], ['singapore', 'SINGAPORE'], ['tokyo', 'TOKYO'], ['sydney', 'SYDNEY']].map(([k, l]) => addPin(k, l, u2 * 1.7));
  tl.set(cam, { rotationX: 52 }, 0);
  tl.fromTo(world, { x: s1.x + 120, y: s1.y + 60, scale: s1.s * 1.12 }, { x: s1.x - 60, y: s1.y - 20, scale: s1.s, duration: 2 * 4 * BEAT / 2 + .2, ease: 'power1.out' }, t0 - .2);
  pin1.forEach((g, i) => tl.fromTo(g, { opacity: 0, scale: .2, transformOrigin: '0 0' }, { opacity: 1, scale: 1, duration: .3, ease: E.back }, t0 + .12 + i * .17));
  A1.forEach(([p, L], i) => tl.to(p, { strokeDashoffset: 0, duration: .6, ease: 'power2.out' }, t0 + .25 + i * .17));
  // sub-cut at beat 36: swing to Asia
  const t1 = t0 + 4 * BEAT;
  tl.set(world, { x: s2.x + 80, y: s2.y + 40, scale: s2.s * 1.1 }, t1);
  tl.set([...pin1, ...A1.map(a => a[0])], { opacity: 0 }, t1);
  tl.to(world, { x: s2.x - 40, y: s2.y - 10, scale: s2.s, duration: 1.9, ease: 'power1.out' }, t1);
  tl.fromTo('#e-cam', { rotationZ: 0 }, { rotationZ: -6, duration: 1.9, ease: 'sine.inOut' }, t1);
  tl.set('#flash', { backgroundColor: '#FF6E05' }, t1).fromTo('#flash', { opacity: .55 }, { opacity: 0, duration: .2 }, t1);
  [...A2.map(a => a[0])].forEach(p => tl.set(p, { opacity: 1 }, t1 - .01));
  pin2.forEach((g, i) => tl.fromTo(g, { opacity: 0, scale: .2, transformOrigin: '0 0' }, { opacity: 1, scale: 1, duration: .3, ease: E.back }, t1 + .1 + i * .2));
  A2.forEach(([p, L], i) => tl.to(p, { strokeDashoffset: 0, duration: .6, ease: 'power2.out' }, t1 + .2 + i * .2));
  // pulse rings
  $$('.ring', svg === '' ? s : world).forEach((r, i) => tl.to(r, { scale: 2.4, opacity: 0, transformOrigin: 'center', duration: .9, ease: 'power2.out', repeat: 1 }, t0 + .4 + (i % 5) * .1));
  // title
  const ttl = h(`<div class="abs big" style="left:60px;top:170px;font-size:230px;text-shadow:0 10px 50px rgba(0,0,0,.7)">MAPS</div>`, s);
  const sub = h(`<div class="abs mono" style="left:66px;top:386px;font-size:34px;letter-spacing:.34em;color:#FF9A3D;font-weight:700;text-shadow:0 4px 20px #000">THAT FLY TO YOUR CUSTOMERS</div>`, s);
  tl.fromTo(ttl, { x: -700, opacity: 0 }, { x: 0, opacity: 1, duration: .32, ease: E.snap }, t0 - .05);
  tl.fromTo(sub, { opacity: 0, y: 24 }, { opacity: 1, y: 0, duration: .3 }, t0 + .2);
})();
