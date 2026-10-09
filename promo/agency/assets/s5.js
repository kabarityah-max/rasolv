/* ===== N · customers everywhere → dive into Tangier (48.75–54.375) ===== */
(() => {
  const s = $('#sN .in'); const t0 = T(104), M = window.MAP, P = M.pts, NS = 'http://www.w3.org/2000/svg';
  const world = h(`<div class="abs" id="n-world" style="left:0;top:0;width:2400px;height:1200px;transform-origin:0 0"></div>`, s);
  world.innerHTML = `<svg width="2400" height="1200" viewBox="0 0 2400 1200" style="overflow:visible"><path d="${M.grat}" fill="none" stroke="rgba(255,255,255,.08)" stroke-width="1.5"/>
    <g id="n-dots" fill="rgba(244,239,233,.5)">${M.dots.map(d => `<circle cx="${d[0]}" cy="${d[1]}" r="4.4"/>`).join('')}</g>
    <g id="n-vec" opacity="0"><path d="${M.land50}" fill="rgba(255,150,60,.10)" stroke="#FF9A3D" stroke-width="2.2" stroke-linejoin="round"/><path d="${M.borders}" fill="none" stroke="rgba(255,255,255,.35)" stroke-width="1.2"/></g></svg>`;
  const over = h(`<svg class="abs" style="left:0;top:0" width="1080" height="1920" viewBox="0 0 1080 1920"><g id="n-arcs"></g><g id="n-pins"></g></svg>`, s);
  const vecPaths = [[$('#n-world svg > path'), 1.5], [$('#n-vec path:nth-child(1)'), 2.4], [$('#n-vec path:nth-child(2)'), 1.2]];
  const arcsG = $('#n-arcs'), pinsG = $('#n-pins');
  const keys = ['london', 'newyork', 'dubai', 'saopaulo', 'singapore', 'lagos', 'sydney', 'mexico', 'tokyo', 'toronto', 'mumbai', 'la', 'cairo', 'paris'];
  const hub = P.tangier;
  const pinEls = keys.map(k => { const g = document.createElementNS(NS, 'g'); g.innerHTML = `<circle class="r" r="30" fill="rgba(255,110,5,.28)"/><circle r="11" fill="#FF6E05" stroke="#fff" stroke-width="4"/>`; pinsG.appendChild(g); g.setAttribute('opacity', 0); return g; });
  const arcEls = keys.map(k => { const p = document.createElementNS(NS, 'path'); p.setAttribute('fill', 'none'); p.setAttribute('stroke', '#FF6E05'); p.setAttribute('stroke-width', 4); p.setAttribute('stroke-linecap', 'round'); arcsG.appendChild(p); return p; });
  const dotEls = keys.map(k => { const c = document.createElementNS(NS, 'circle'); c.setAttribute('r', 9); c.setAttribute('fill', '#fff'); c.setAttribute('opacity', 0); arcsG.appendChild(c); return c; });
  const hubG = document.createElementNS(NS, 'g'); hubG.innerHTML = `<circle class="hr1" r="40" fill="none" stroke="#FF6E05" stroke-width="5"/><circle class="hr2" r="40" fill="none" stroke="#fff" stroke-width="3"/><circle r="16" fill="#FF6E05" stroke="#fff" stroke-width="5"/>`; pinsG.appendChild(hubG);
  const chip = h(`<div class="chip glass" id="n-chip" style="left:0;top:0;height:96px;font-size:40px;opacity:0;border-radius:48px"><span class="dot"></span>RASOLV · ON IT ✓</div>`, s);
  const C0 = [1200, 600], s0 = 0.56, s1 = 26;
  const ez = gsap.parseEase('power3.inOut');
  const cam = pr => { const p = Math.max(0, Math.min(1, pr)); const k = ez(p); const sc = Math.exp(Math.log(s0) + (Math.log(s1) - Math.log(s0)) * k); const cx = C0[0] + (hub[0] - C0[0]) * k, cy = C0[1] + (hub[1] - C0[1]) * k; return { sc, x: 540 - sc * cx, y: 930 - sc * cy }; };
  const scr = (pt, c) => [c.x + c.sc * pt[0], c.y + c.sc * pt[1]];
  const TD0 = 3.3, TD1 = 5.5, tot = 5.625;   // dive starts 3.3 s into the scene
  const arcPts = (A, B, n, upk) => { const mx = (A[0] + B[0]) / 2, my = (A[1] + B[1]) / 2 - upk * Math.hypot(B[0] - A[0], B[1] - A[1]); return Array.from({ length: n + 1 }, (_, i) => { const t = i / n; return [(1 - t) * (1 - t) * A[0] + 2 * (1 - t) * t * mx + t * t * B[0], (1 - t) * (1 - t) * A[1] + 2 * (1 - t) * t * my + t * t * B[1]]; }); };
  const arcs = keys.map(k => arcPts(P[k], hub, 36, .22));
  drive(t0 - .2, tot + .2, pr => {
    const t = pr * (tot + .2) - .2;
    const c = cam((t - TD0) / (TD1 - TD0));
    world.style.transform = `translate(${c.x}px,${c.y}px) scale(${c.sc})`;
    const vecO = Math.max(0, Math.min(1, (c.sc - 3) / 5)); $('#n-vec').setAttribute('opacity', vecO); $('#n-dots').setAttribute('opacity', 1 - vecO); vecPaths.forEach(([e, w]) => e.setAttribute('stroke-width', (w / c.sc).toFixed(3)));
    keys.forEach((k, i) => {
      const appear = .15 + i * .09, pa = Math.max(0, Math.min(1, (t - appear) / .3)); const [px, py] = scr(P[k], c);
      pinEls[i].setAttribute('transform', `translate(${px},${py}) scale(${pa * (c.sc > 3 ? Math.max(0, 1 - (c.sc - 3) / 4) : 1)})`); pinEls[i].setAttribute('opacity', pa);
      const rr = $('.r', pinEls[i]); const ph = ((t - appear) * 1.1) % 1; rr.setAttribute('r', 14 + 40 * Math.max(0, ph)); rr.setAttribute('opacity', pa * (1 - Math.max(0, ph)));
      const ap = Math.max(0, Math.min(1, (t - (1.5 + i * .09)) / .9)); const pts = arcs[i]; const m = Math.max(1, Math.floor(ap * 36));
      const fade = c.sc > 3 ? Math.max(0, 1 - (c.sc - 3) / 3) : 1;
      arcEls[i].setAttribute('d', ap > 0 ? 'M' + pts.slice(0, m + 1).map(q => scr(q, c).map(v => v.toFixed(1)).join(',')).join(' L') : ''); arcEls[i].setAttribute('opacity', fade);
      const travel = ((t - 1.5 - i * .09 - .6) * .8); const tq = travel > 0 ? pts[Math.min(36, Math.floor((travel % 1) * 36))] : pts[0]; const [dx, dy] = scr(tq, c);
      dotEls[i].setAttribute('cx', dx); dotEls[i].setAttribute('cy', dy); dotEls[i].setAttribute('opacity', travel > 0 ? fade : 0);
    });
    const [hx, hy] = scr(hub, c); const hs = Math.max(0, Math.min(1, t / .3)); hubG.setAttribute('transform', `translate(${hx},${hy}) scale(${Math.min(hs, 1) * (1 + .25 * Math.sin(t * 5))})`);
    $('.hr1', hubG).setAttribute('r', 40 + 60 * ((t * 1.3) % 1)); $('.hr1', hubG).setAttribute('opacity', 1 - ((t * 1.3) % 1));
    $('.hr2', hubG).setAttribute('r', 20 + 120 * (Math.max(0, t - 4.4) * .8 % 1)); $('.hr2', hubG).setAttribute('opacity', t > 4.4 ? 1 - (Math.max(0, t - 4.4) * .8 % 1) : 0);
    const co = Math.max(0, Math.min(1, (t - 4.5) / .25)); chip.style.opacity = co; chip.style.transform = `translate(${hx - 230}px,${hy - 190 - 20 * (1 - co)}px) scale(${.8 + .2 * co})`;
  });
  // headline swaps
  const l1 = h(`<div class="abs big" style="left:60px;top:170px;font-size:158px;line-height:.9;text-shadow:0 10px 50px rgba(0,0,0,.8)">WHEREVER<br><span class="or">YOU ARE</span></div>`, s);
  const l2 = h(`<div class="abs big" style="left:60px;top:170px;font-size:236px;line-height:.86;text-shadow:0 10px 50px rgba(0,0,0,.8);opacity:0">ONE <span class="or">TAP</span><br>AWAY.</div>`, s);
  tl.fromTo(l1, { x: -900, opacity: 0 }, { x: 0, opacity: 1, duration: .34, ease: E.snap }, t0 - .05);
  tl.to(l1, { x: 900, opacity: 0, duration: .25, ease: E.in }, t0 + 3.05);
  tl.set(l2, { opacity: 1 }, t0 + 3.3).fromTo(l2, { scale: 1.6, y: -80, filter: 'blur(14px)' }, { scale: 1, y: 0, filter: 'blur(0px)', duration: .3, ease: E.snap }, t0 + 3.28);
})();

/* ===== O · end card (54.375–60) ===== */
(() => {
  const s = $('#sO .in'); const t0 = T(116);
  const rings = [0, 1, 2].map(i => h(`<div class="abs" style="left:190px;top:330px;width:700px;height:700px;border-radius:50%;border:3px solid rgba(255,110,5,.75)"></div>`, s));
  const host = h(`<div class="abs" id="o-ap" style="left:190px;top:330px;width:700px;height:700px"></div>`, s);
  drive(t0 - .1, 1.0, p => { const k = gsap.parseEase('power3.out')(p); ap(host, { r: 37 + 5 * Math.sin(p * 3.14), grow: k, bp: k, gap: '#060606' }); });
  tl.fromTo(host, { rotation: -150, scale: .2, opacity: 0 }, { rotation: 0, scale: 1, opacity: 1, duration: .95, ease: E.out }, t0 - .1);
  tl.to(host, { rotation: 30, duration: 5.2, ease: 'sine.inOut' }, t0 + .9);
  rings.forEach((r, i) => tl.fromTo(r, { scale: .4, opacity: .9 }, { scale: 2.7, opacity: 0, duration: 1.2, ease: 'power2.out', repeat: 2, repeatDelay: .2 }, t0 + i * .25));
  const word = h(`<div class="abs big center" style="top:1060px;font-size:214px;white-space:nowrap">RASOLV</div>`, s);
  const cs = chars(word);
  tl.fromTo(cs, { y: 300, opacity: 0, rotation: 10 }, { y: 0, opacity: 1, rotation: 0, duration: .36, ease: E.snap, stagger: .055 }, t0 + .15);
  const vs = h(`<div class="abs mono center" style="top:1300px;font-size:40px;letter-spacing:.42em;color:#FF9A3D;font-weight:700">VISION THAT SOLVES.</div>`, s);
  tl.fromTo(vs, { opacity: 0, y: 30, letterSpacing: '1em' }, { opacity: 1, y: 0, letterSpacing: '.42em', duration: .5, ease: E.out }, t0 + 1.3);
  const cta = h(`<div class="chip" style="left:140px;top:1400px;width:800px;height:120px;border-radius:60px;justify-content:center;font-size:48px;font-weight:900;background:#FF6E05;color:#060606;box-shadow:0 20px 70px rgba(255,110,5,.55), inset 0 3px 0 rgba(255,255,255,.55)">LET'S BUILD YOURS →</div>`, s);
  tl.fromTo(cta, { scale: .2, opacity: 0, y: 100 }, { scale: 1, opacity: 1, y: 0, duration: .45, ease: E.back }, t0 + 2.6);
  tl.to(cta, { scale: 1.04, duration: .23, yoyo: true, repeat: 7, ease: 'sine.inOut' }, t0 + 3.1);
  tl.to('#sO .in', { opacity: 0, duration: .5, ease: 'power1.in' }, 59.5);
})();
