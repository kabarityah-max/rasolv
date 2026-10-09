/* ===== D1 · "Your brand." (11.25–13.125) ===== */
(() => {
  const s = $('#sD1 .in'); const t0 = T(24);
  const wall = h(`<div class="abs" style="inset:0;perspective:1400px"></div>`, s);
  const COL = ['#FF6E05', '#F4EFE9', '#FFA24A', '#FF6E05', '#F4EFE9', '#FF8A33', '#FFC59A', '#F4EFE9'];
  const tiles = [];
  for (let r = 0; r < 5; r++) for (let c = 0; c < 4; c++) {
    if (r === 2 || r === 3) continue;
    const i = r * 4 + c;
    const t = h(`<div class="glass" style="left:${52 + c * 246}px;top:${200 + r * 246}px;width:226px;height:226px;border-radius:40px;opacity:0"><div class="abs" style="left:43px;top:43px;width:140px;height:140px" data-tile></div></div>`, wall);
    ap($('[data-tile]', t), { r: 37, grow: 1, bp: 0, color: COL[(i * 3 + r) % 8], gap: (i + r) % 3 === 0 ? '#F4EFE9' : '#05060a', lines: false });
    if ((i + r) % 3 === 0) t.style.background = 'linear-gradient(155deg,rgba(255,110,5,.5),rgba(255,110,5,.12))';
    tiles.push(t);
  }
  tl.fromTo(tiles, { rotationY: 100, opacity: 0, scale: .8 }, { rotationY: 0, opacity: .38, scale: 1, duration: .42, ease: E.out, stagger: .03 }, t0 - .15);
  tl.to(tiles, { rotationX: 360, backgroundColor: 'rgba(255,110,5,.2)', duration: .5, ease: 'power3.inOut', stagger: .02 }, t0 + .85);
  h(`<div class="abs" style="inset:0;background:radial-gradient(70% 26% at 42% 52%,rgba(5,6,10,.88),rgba(5,6,10,0))"></div>`, s);
  const a = h(`<div class="abs disp" style="left:70px;top:620px;font-size:240px;white-space:nowrap">Your</div>`, s), b = h(`<div class="abs disp" style="left:70px;top:850px;font-size:250px;font-weight:500;white-space:nowrap">brand.</div>`, s);
  reveal(chars(a), t0 + .02, { stagger: .05, d: .5, y: 90 }); reveal(chars(b, 'ch gt'), t0 + .2, { stagger: .05, d: .55, y: 90 });
  tl.to([a, b], { scale: 1.06, duration: .5, ease: 'sine.inOut' }, t0 + .6);
})();

/* ===== D2 · "In motion." with a refracting glass lens (13.125–15.0) ===== */
(() => {
  const s = $('#sD2 .in'); const t0 = T(28);
  const lines = [...Array(14)].map((_, i) => h(`<div class="abs" style="left:-200px;top:${200 + i * 98}px;width:${300 + (i * 97) % 500}px;height:2px;background:linear-gradient(90deg,transparent,rgba(244,239,233,${.18 + (i % 3) * .1}),transparent)"></div>`, s));
  lines.forEach((l, i) => tl.fromTo(l, { x: -400 }, { x: 1700, duration: .8 + (i % 4) * .15, ease: 'power2.in' }, t0 - .2 + (i % 5) * .08));
  const mk = cls => `<div class="abs ${cls}" style="inset:0"><div class="abs disp" style="left:70px;top:630px;font-size:230px;white-space:nowrap">In</div><div class="abs disp" style="left:70px;top:850px;font-size:236px;font-weight:500;white-space:nowrap;color:#FF8A33">motion.</div></div>`;
  const base = h(mk('d2b'), s);
  // ghost trail
  const ghosts = [1, 2, 3, 4].map(k => { const g = h(mk('d2g'), s); g.style.opacity = 0; return g; });
  tl.fromTo(base, { x: -900, opacity: 0, filter: 'blur(24px)' }, { x: 0, opacity: 1, filter: 'blur(0px)', duration: .5, ease: E.snap }, t0 - .05);
  ghosts.forEach((g, k) => tl.fromTo(g, { x: -900, opacity: .0 }, { x: -60 * (k + 1) + 60 * (k + 1) * 0, opacity: .22 - k * .04, duration: .5, ease: E.snap, filter: 'blur(' + (6 + k * 4) + 'px)' }, t0 - .05 + k * .03));
  tl.to(ghosts, { opacity: 0, x: 0, duration: .3 }, t0 + .6);
  const band = h(`<div class="abs" id="d2-band" style="left:-420px;top:560px;width:300px;height:640px;transform:skewX(-14deg);background:linear-gradient(90deg,rgba(255,255,255,.07),rgba(255,235,215,.3) 50%,rgba(255,255,255,.07));backdrop-filter:brightness(1.7) saturate(1.5);-webkit-backdrop-filter:brightness(1.7) saturate(1.5);border-left:2px solid rgba(255,255,255,.55);border-right:2px solid rgba(255,200,150,.5);box-shadow:0 0 60px rgba(255,160,70,.35)"></div>`, s);
  tl.fromTo(band, { x: 0 }, { x: 1750, duration: 1.2, ease: 'power2.inOut' }, t0 + .3);
  const lbl = h(`<div class="abs mono center" style="top:1250px;font-size:30px;letter-spacing:.5em;color:rgba(244,239,233,.7)">— MOTION · LIGHT · DEPTH —</div>`, s);
  tl.fromTo(lbl, { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: .4 }, t0 + .45);
})();

/* ===== E · maps: customers everywhere → dive (15–20.6 s) ===== */
(() => {
  const s = $('#sE .in'); const t0 = T(32), M = window.MAP, P = M.pts, NS = 'http://www.w3.org/2000/svg';
  const stage = h(`<div class="abs" style="inset:0;perspective:1500px;perspective-origin:50% 45%;-webkit-mask-image:linear-gradient(180deg,#000 0%,#000 60%,transparent 84%);mask-image:linear-gradient(180deg,#000 0%,#000 60%,transparent 84%)"></div>`, s);
  const cam = h(`<div class="abs" id="e-cam" style="left:0;top:0;width:1080px;height:1920px;transform-style:preserve-3d;transform-origin:540px 900px"></div>`, stage);
  const world = h(`<div class="abs" id="e-world" style="left:0;top:0;width:2400px;height:1200px;transform-origin:0 0"></div>`, cam);
  world.innerHTML = `<svg width="2400" height="1200" viewBox="0 0 2400 1200"><path id="e-grat" d="${M.grat}" fill="none" stroke="rgba(255,255,255,.08)" stroke-width="1.4"/>
    <g id="e-dots" fill="rgba(244,239,233,.74)">${M.dots.map(d => `<circle cx="${d[0]}" cy="${d[1]}" r="3.6"/>`).join('')}</g>
    <g id="e-arcs"></g><g id="e-pins"></g></svg>`;
  const mid = ks => ks.reduce((a, k) => [a[0] + P[k][0] / ks.length, a[1] + P[k][1] / ks.length], [0, 0]);
  const shot = (ks, sc) => { const c = mid(ks); return { x: 540 - sc * c[0], y: 900 - sc * c[1], s: sc, c }; };
  const arcs = $('#e-arcs'), pins = $('#e-pins');
  const addArc = (a, b, up) => { const A = P[a], B = P[b], mx = (A[0] + B[0]) / 2, my = (A[1] + B[1]) / 2 - up; const pth = document.createElementNS(NS, 'path'); pth.setAttribute('d', `M${A[0]},${A[1]} Q${mx},${my} ${B[0]},${B[1]}`); pth.setAttribute('fill', 'none'); pth.setAttribute('stroke', '#FF6E05'); pth.setAttribute('stroke-width', 5); pth.setAttribute('stroke-linecap', 'round'); arcs.appendChild(pth); const L = Math.hypot(B[0] - A[0], B[1] - A[1]) * 1.15; pth.style.strokeDasharray = L; pth.style.strokeDashoffset = L; return pth; };
  const addPin = (k, label, u) => { const g = document.createElementNS(NS, 'g'); g.setAttribute('transform', `translate(${P[k][0]},${P[k][1]})`);
    g.innerHTML = `<circle r="${26 * u}" fill="rgba(255,110,5,.25)"/><circle r="${9 * u}" fill="#FF6E05" stroke="#fff" stroke-width="${3 * u}"/><g transform="translate(${16 * u},${-34 * u})"><rect rx="${22 * u}" height="${44 * u}" width="${(label.length * 17 + 40) * u}" fill="rgba(14,14,16,.72)" stroke="rgba(255,255,255,.5)" stroke-width="${2 * u}"/><text x="${20 * u}" y="${30 * u}" font-family="Rubik" font-weight="600" font-size="${24 * u}" fill="#F4EFE9" letter-spacing="${1.5 * u}">${label}</text></g>`; pins.appendChild(g); g.style.opacity = 0; return g; };
  const s1 = shot(['newyork', 'london', 'tangier', 'saopaulo', 'dubai'], 1.7), s2 = shot(['dubai', 'mumbai', 'singapore', 'tokyo', 'sydney'], 1.5);
  const u1 = 1.7 / s1.s, u2 = 1.7 / s2.s;
  const A1 = [['tangier', 'london'], ['tangier', 'newyork'], ['tangier', 'saopaulo'], ['tangier', 'dubai'], ['tangier', 'lagos']].map(([a, b]) => addArc(a, b, 90));
  const pin1 = [['tangier', 'TANGIER'], ['london', 'LONDON'], ['newyork', 'NEW YORK'], ['saopaulo', 'SÃO PAULO'], ['dubai', 'DUBAI']].map(([k, l]) => addPin(k, l, u1));
  const A2 = [['dubai', 'mumbai'], ['dubai', 'singapore'], ['singapore', 'tokyo'], ['singapore', 'sydney']].map(([a, b]) => addArc(a, b, 70));
  const pin2 = [['mumbai', 'MUMBAI'], ['singapore', 'SINGAPORE'], ['tokyo', 'TOKYO'], ['sydney', 'SYDNEY']].map(([k, l]) => addPin(k, l, u2));
  tl.set(cam, { rotationX: 46 }, 0);
  tl.fromTo(world, { x: s1.x + 120, y: s1.y + 60, scale: s1.s * 1.12 }, { x: s1.x - 60, y: s1.y - 20, scale: s1.s, duration: 2.2, ease: 'power1.out' }, t0 - .2);
  pin1.forEach((g, i) => tl.fromTo(g, { opacity: 0, scale: .2, transformOrigin: '0 0' }, { opacity: 1, scale: 1, duration: .3, ease: E.back }, t0 + .02 + i * .12));
  A1.forEach((p, i) => tl.to(p, { strokeDashoffset: 0, duration: .6, ease: 'power2.out' }, t0 + .12 + i * .12));
  const t1 = t0 + 4 * BEAT;
  tl.set(world, { x: s2.x + 80, y: s2.y + 40, scale: s2.s * 1.1 }, t1);
  tl.set([...pin1, ...A1], { opacity: 0 }, t1);
  tl.to(world, { x: s2.x - 40, y: s2.y - 10, scale: s2.s, duration: 1.8, ease: 'power1.out' }, t1);
  tl.fromTo('#e-cam', { rotationZ: 0 }, { rotationZ: -6, duration: 1.8, ease: 'sine.inOut' }, t1);
  tl.set('#flash', { backgroundColor: ORANGE }, t1).fromTo('#flash', { opacity: .4 }, { opacity: 0, duration: .2 }, t1);
  A2.forEach(p => tl.set(p, { opacity: 1 }, t1 - .01));
  pin2.forEach((g, i) => tl.fromTo(g, { opacity: 0, scale: .2, transformOrigin: '0 0' }, { opacity: 1, scale: 1, duration: .3, ease: E.back }, t1 + .1 + i * .2));
  A2.forEach((p, i) => tl.to(p, { strokeDashoffset: 0, duration: .6, ease: 'power2.out' }, t1 + .2 + i * .2));
  // dive into Tangier
  const t2 = T(40), hub = P.tangier, dur = 1.8;
  const dive = h(`<svg class="abs" id="e-dive" style="left:0;top:0;opacity:0" width="1080" height="1920" viewBox="0 0 1080 1920"><path d="${M.grat}" fill="none" stroke="rgba(255,255,255,.14)" stroke-width="1.4" vector-effect="non-scaling-stroke"/><path d="${M.land50}" fill="rgba(255,150,60,.2)" stroke="#FFB070" stroke-width="2.6" vector-effect="non-scaling-stroke" stroke-linejoin="round"/><path d="${M.borders}" fill="none" stroke="rgba(255,255,255,.6)" stroke-width="1.4" vector-effect="non-scaling-stroke"/></svg>`, s);
  const ring = h(`<div class="abs" id="e-hub" style="left:420px;top:780px;width:240px;height:240px;border-radius:50%;border:3px solid #FF6E05;opacity:0;box-shadow:0 0 40px rgba(255,110,5,.6)"></div>`, s);
  drive(t2, dur, p => {
    const k = ease('power3.inOut', p), sc = Math.exp(Math.log(s2.s) + (Math.log(14) - Math.log(s2.s)) * k);
    const cx = s2.c[0] + (hub[0] - s2.c[0]) * k, cy = s2.c[1] + (hub[1] - s2.c[1]) * k;
    gsap.set(world, { x: 540 - sc * cx, y: 900 - sc * cy, scale: sc });
    gsap.set(cam, { rotationX: 46 * (1 - k), rotationZ: -6 * (1 - k) });
    const vo = Math.max(0, Math.min(1, (sc - 2.4) / 3)); dive.style.opacity = vo; $('#e-dots').setAttribute('opacity', 1 - vo * .95); $('#e-grat').setAttribute('opacity', 1 - vo);
    dive.setAttribute('viewBox', `${cx - 540 / sc} ${cy - 900 / sc} ${1080 / sc} ${1920 / sc}`);
    $('#e-arcs').setAttribute('opacity', Math.max(0, 1 - p * 5)); $('#e-pins').setAttribute('opacity', Math.max(0, 1 - p * 5));
    ring.style.opacity = Math.max(0, (p - .55) / .3); ring.style.transform = `scale(${.4 + (p - .55) * 1.5 + .08 * Math.sin(p * 40)})`;
  });
  h(`<div class="abs" style="left:0;top:0;width:1080px;height:560px;background:linear-gradient(180deg,rgba(5,6,10,.92),rgba(5,6,10,0))"></div>`, s);
  const ro = h(`<div class="abs mono center" style="top:1040px;font-size:30px;letter-spacing:.3em;color:#FFC59A;opacity:0">35.76° N · 5.80° W</div>`, s);
  tl.fromTo(ro, { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: .4 }, t2 + 1.2);
  // headline
  const a = h(`<div class="abs disp" style="left:70px;top:200px;font-size:118px;white-space:nowrap">Your story,</div>`, s);
  const a2 = h(`<div class="abs mono" style="left:76px;top:340px;font-size:30px;letter-spacing:.36em;color:#FF9A3D;text-shadow:0 4px 20px #000">IN FRONT OF CUSTOMERS</div>`, s);
  const b = h(`<div class="abs disp" style="left:70px;top:200px;font-size:128px;opacity:0;white-space:nowrap">Wherever<br><b class="or">they are.</b></div>`, s);
  reveal(chars(a), t0 - .05, { stagger: .03, d: .5 }); tl.fromTo(a2, { opacity: 0, x: -30 }, { opacity: 1, x: 0, duration: .4 }, t0 + .25);
  tl.to([a, a2], { opacity: 0, y: -60, filter: 'blur(10px)', duration: .3, ease: E.in }, t2 - .4);
  tl.set(b, { opacity: 1 }, t2 - .1).fromTo(b, { y: 50, filter: 'blur(14px)' }, { y: 0, filter: 'blur(0px)', duration: .5, ease: E.out }, t2 - .1);
})();
