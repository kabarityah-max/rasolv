/* ===== F · 3D product (20.625–24.375 s)  "Your product, in three dimensions." ===== */
(() => {
  const s = $('#sF .in'); const t0 = T(44);
  h(`<div class="abs disp center" id="f-bg3d" style="top:560px;font-size:700px;line-height:1;color:transparent;-webkit-text-stroke:3px rgba(255,110,5,.65);letter-spacing:-.05em;font-weight:600">3D</div>`, s);
  const rings = h(`<svg class="abs" style="left:0;top:0" width="1080" height="1920" viewBox="0 0 1080 1920"><g fill="none" stroke="rgba(244,239,233,.22)" stroke-width="1.5"><ellipse cx="540" cy="980" rx="500" ry="170" transform="rotate(-18 540 980)"/><ellipse cx="540" cy="980" rx="430" ry="130" transform="rotate(22 540 980)"/></g><circle id="f-c1" r="9" fill="#FF6E05"/><circle id="f-c2" r="7" fill="#fff"/></svg>`, s);
  drive(t0 - .2, 4, p => { const a = p * 8; const e1 = (r1x, r1y, rot, ang) => { const x = r1x * Math.cos(ang), y = r1y * Math.sin(ang), r = rot * Math.PI / 180; return [540 + x * Math.cos(r) - y * Math.sin(r), 980 + x * Math.sin(r) + y * Math.cos(r)]; };
    const [x1, y1] = e1(500, 170, -18, a), [x2, y2] = e1(430, 130, 22, -a * 1.3 + 1); $('#f-c1').setAttribute('cx', x1); $('#f-c1').setAttribute('cy', y1); $('#f-c2').setAttribute('cx', x2); $('#f-c2').setAttribute('cy', y2); });
  const hd = h(`<div class="abs disp" style="left:70px;top:210px;font-size:104px;white-space:nowrap" id="f-yp">Your product</div>`, s);
  const hd2 = h(`<div class="abs disp" style="left:74px;top:332px;font-size:60px;white-space:nowrap;font-weight:500"><span class="or">in three dimensions.</span></div>`, s);
  reveal(chars(hd), t0 - .05, { stagger: .03, d: .5 }); tl.fromTo(hd2, { opacity: 0, x: -40 }, { opacity: 1, x: 0, duration: .45, ease: E.out }, t0 + .3);
  const stage = h(`<div class="abs" style="inset:0;perspective:1700px;perspective-origin:50% 50%"></div>`, s);
  const ph = h(`<div class="abs" id="f-phone" style="left:320px;top:520px;width:440px;height:900px;transform-style:preserve-3d"></div>`, stage);
  for (let i = 1; i <= 8; i++) h(`<div class="abs" style="inset:0;border-radius:78px;background:linear-gradient(160deg,#3a3a3d,#111);transform:translateZ(${-i * 4}px)"></div>`, ph);
  const front = h(`<div class="abs" style="inset:0;border-radius:78px;background:#0b0b0c;border:10px solid #2b2b2e;box-shadow:inset 0 0 0 2px #555, 0 0 120px rgba(255,110,5,.45);overflow:hidden;transform:translateZ(2px)"></div>`, ph);
  front.innerHTML = `<div class="abs" style="inset:0;background:radial-gradient(90% 55% at 15% 8%,#FF6E05,#a63d00 40%,#0b0b0c 75%)"></div>
   <div class="abs" style="left:150px;top:18px;width:120px;height:34px;border-radius:17px;background:#000"></div>
   <div class="abs mono" style="left:44px;top:24px;font-size:22px;font-weight:700">9:41</div>
   <div class="abs mono" style="left:30px;top:96px;font-size:18px;letter-spacing:.3em;font-weight:700;color:rgba(255,255,255,.85)">YOUR BRAND</div>
   <div class="abs disp" style="left:28px;top:140px;font-size:88px;line-height:.92">Your<br>next<br><b style="color:#fff">launch</b></div>
   <div class="glass" style="left:22px;top:470px;width:376px;height:250px;border-radius:38px;box-shadow:inset 0 2px 0 rgba(255,255,255,.5),0 20px 40px rgba(0,0,0,.4)">
     <div class="abs" style="left:0;top:0;width:100%;height:150px;background:linear-gradient(135deg,rgba(255,110,5,.55),rgba(255,255,255,.08))"></div>
     <div class="abs" style="left:150px;top:36px;width:76px;height:76px;border-radius:50%;background:#fff;display:flex;align-items:center;justify-content:center"><div style="width:0;height:0;border-left:26px solid #FF6E05;border-top:16px solid transparent;border-bottom:16px solid transparent;margin-left:8px"></div></div>
     <div class="abs" style="left:24px;top:170px;width:328px;height:8px;border-radius:4px;background:rgba(255,255,255,.25)"><div style="width:62%;height:100%;border-radius:4px;background:#FF6E05"></div></div>
     <div class="abs mono" style="left:24px;top:196px;font-size:20px;color:rgba(255,255,255,.8);letter-spacing:.12em">0:24 / 0:60 · 9:16</div>
   </div>
   <div class="abs" style="left:22px;right:22px;top:760px;height:84px;border-radius:42px;background:#FF6E05;color:#000;font-weight:600;font-size:26px;text-align:center;line-height:84px">Watch the film ▸</div>
   <div class="abs" style="left:140px;bottom:14px;width:140px;height:6px;border-radius:3px;background:rgba(255,255,255,.8)"></div>`;
  const sheen = h(`<div class="abs" style="inset:0;border-radius:78px;overflow:hidden;transform:translateZ(3px);pointer-events:none"><div id="f-sheen" style="position:absolute;top:-20%;left:-60%;width:40%;height:140%;background:linear-gradient(100deg,rgba(255,255,255,0),rgba(255,255,255,.35),rgba(255,255,255,0));transform:skewX(-16deg)"></div></div>`, ph);
  tl.fromTo('#f-sheen', { x: 0 }, { x: 1400, duration: 1.1, ease: 'power2.inOut', repeat: 2, repeatDelay: .5 }, t0 + .5);
  [['Light', -190, 250, 150], ['Depth', 440, 120, 210], ['Motion', -180, 760, 170], ['Detail', 450, 700, 120]].forEach(([l, x, y, z], i) => {
    const c = h(`<div class="chip glass" style="left:${x}px;top:${y}px;height:80px;font-size:34px;transform:translateZ(${z}px)"><span class="dot"></span>${l}</div>`, ph);
    tl.fromTo(c, { opacity: 0, scale: .3 }, { opacity: 1, scale: 1, duration: .4, ease: E.back }, t0 + .25 + i * .16);
    tl.to(c, { y: '+=' + (i % 2 ? 24 : -24), duration: 1.1, ease: 'sine.inOut', yoyo: true, repeat: 2 }, t0 + .2 + i * .1);
  });
  tl.fromTo('#f-bg3d', { scale: .6, opacity: 0 }, { scale: 1, opacity: 1, duration: .5, ease: E.out }, t0);
  tl.fromTo(ph, { rotationY: -75, rotationX: 14, y: 300, scale: .8, opacity: 0 }, { rotationY: -28, rotationX: 8, y: 0, scale: 1, opacity: 1, duration: .5, ease: E.out }, t0 - .2);
  [[28, .5, .5], [-26, .4, 1.2], [14, .35, 2.0], [-8, .6, 2.7]].forEach(([ry, rx, t]) => tl.to(ph, { rotationY: ry, rotationX: rx * 10, duration: .5, ease: 'power3.inOut' }, t0 + t));
  tl.to('#f-bg3d', { rotation: 5, x: 40, duration: 3.2, ease: 'none' }, t0);
})();

/* ===== G · lens-focus HUD (24.375–28.125 s)  "Every detail, in focus." ===== */
(() => {
  const s = $('#sG .in'); const t0 = T(52), cx = 540, cy = 905;
  const hud = h(`<div class="abs" id="g-hud" style="inset:0"></div>`, s);
  const inner = h(`<div class="abs" style="inset:0;transform:scale(.94);transform-origin:540px ${cy}px"></div>`, hud);
  const arc = (r, a0, a1) => { const p = a => [(Math.cos(a) * r).toFixed(1), (Math.sin(a) * r).toFixed(1)]; const A = p(a0), B = p(a1); return `M${A[0]},${A[1]}A${r},${r} 0 0 1 ${B[0]},${B[1]}`; };
  const deg = [...Array(12)].map((_, i) => `<text transform="rotate(${i * 30}) translate(0,-492)" text-anchor="middle" font-family="JetBrains Mono" font-size="19" fill="rgba(244,239,233,.55)" letter-spacing="2">${String(i * 30).padStart(3, '0')}</text>`).join('');
  const segs = [...Array(36)].map((_, i) => `<path class="gs" d="${arc(352, (i * 10 + 1.5) * Math.PI / 180, (i * 10 + 8.5) * Math.PI / 180)}" stroke="#FF6E05" stroke-width="16" fill="none" opacity=".12"/>`).join('');
  const trail = [...Array(26)].map(() => `<path class="gt2" stroke="#fff" fill="none" stroke-linecap="round"/>`).join('');
  inner.innerHTML = `<svg class="abs" style="left:0;top:0" width="1080" height="1920" viewBox="0 0 1080 1920"><g transform="translate(${cx} ${cy})">
      <g id="g-r1">${tickRing(436, 120, 9, 5, 'rgba(244,239,233,.55)', 2)}${deg}</g>
      <g id="g-r2">${segs}</g>
      <circle r="296" fill="none" stroke="rgba(244,239,233,.22)" stroke-width="1.5"/>
      <circle r="262" fill="none" stroke="rgba(255,110,5,.4)" stroke-width="1.5" stroke-dasharray="2 10"/>
      <g id="g-tr">${trail}</g><circle id="g-cm" r="9" fill="#fff" style="filter:drop-shadow(0 0 10px #fff)"/>
    </g></svg>`;
  const orb = h(`<div class="abs" id="g-orb" style="left:${cx - 190}px;top:${cy - 190}px;width:380px;height:380px;border-radius:50%;overflow:hidden;z-index:5;background:radial-gradient(circle at 32% 24%,rgba(255,255,255,.44),rgba(255,255,255,.07) 38%,rgba(255,110,5,.18) 70%,rgba(0,0,0,.45));border:1.5px solid rgba(255,255,255,.4);box-shadow:inset 0 0 60px rgba(255,255,255,.14),inset -22px -34px 70px rgba(255,110,5,.38),0 34px 90px rgba(0,0,0,.65),0 0 110px rgba(255,110,5,.32)"></div>`, inner);
  const ahost = h(`<div class="abs" style="left:65px;top:65px;width:250px;height:250px"></div>`, orb);
  h(`<div class="abs" style="left:58px;top:30px;width:150px;height:70px;border-radius:50%;background:radial-gradient(ellipse,rgba(255,255,255,.7),rgba(255,255,255,0) 70%);transform:rotate(-28deg)"></div>`, orb);
  const ret = h(`<svg class="abs" style="left:0;top:0;z-index:6" width="1080" height="1920" viewBox="0 0 1080 1920"><g transform="translate(${cx} ${cy})" id="g-ret" stroke="#fff" stroke-width="5" fill="none" stroke-linecap="square"><path d="M-1 -1" /><g class="rb"><path d="M-60 0H0V-60" transform="translate(0 0)"/></g></g></svg>`, inner);
  const g = $('#g-ret'); g.innerHTML = [[-1, -1], [1, -1], [1, 1], [-1, 1]].map(([sx, sy]) => `<path class="rb" d="M${sx * -70} ${sy * 0}H0V${sy * -70}" transform="scale(${sx} ${sy})"/>`).join('') + `<path d="M-14 0H14M0 -14V14" stroke-width="3"/>`;
  const chips = ['Type', 'Light', 'Motion', 'Depth', 'Sound'].map(l => h(`<div class="chip glass" style="left:0;top:0;height:68px;font-size:30px;opacity:0"><span class="dot"></span>${l}</div>`, inner));
  const segEls = $$('.gs', inner), trEls = $$('.gt2', inner);
  const cm = $('#g-cm');
  drive(t0 - .1, 3.9, p => {
    const t = p * 3.9 - .1;
    $('#g-r1').setAttribute('transform', `rotate(${t * 9})`); $('#g-r2').setAttribute('transform', `rotate(${-t * 4})`);
    const head = Math.max(0, (t - .1) / 1.3) * 360;           // focus-lock sweep
    segEls.forEach((e, i) => { const a = i * 10; const lit = a < head; const near = Math.max(0, 1 - Math.abs(head - a) / 60); e.setAttribute('opacity', lit ? (head >= 360 ? .95 : .55 + .45 * near) : .12); e.setAttribute('stroke', lit && head < 360 && near > .8 ? '#FFD0A8' : '#FF6E05'); });
    const ang = t * 3.2;
    trEls.forEach((e, i) => { const a1 = ang - i * .045, a0 = a1 - .05; e.setAttribute('d', arc(296, a0, a1)); e.setAttribute('opacity', (1 - i / 26) * .9); e.setAttribute('stroke-width', 7 * (1 - i / 26) + .5); });
    cm.setAttribute('cx', Math.cos(ang) * 296); cm.setAttribute('cy', Math.sin(ang) * 296);
    // iris opens as focus locks
    const open = ease('power3.out', (t - .2) / 1.5); ap(ahost, { r: 8 + 46 * open, grow: 1, bp: 0, gap: '#0a0a0f', lines: false });
    ahost.style.transform = `rotate(${t * -14}deg)`;
    const k = ease('power3.out', (t - .1) / 1.5), d = 330 - 110 * k; $$('.rb', g).forEach(e => e.setAttribute('transform', e.getAttribute('transform').replace(/translate\([^)]*\)/, '') + ''));
    $$('.rb', g).forEach((e, i) => { const sx = [-1, 1, 1, -1][i], sy = [-1, -1, 1, 1][i]; e.setAttribute('transform', `translate(${sx * d} ${sy * d}) scale(${sx} ${sy})`); });
    chips.forEach((c, i) => { const a = i / chips.length * 6.283 + t * 1.5 + .6; const x = cx + 450 * Math.cos(a), y = cy + 120 * Math.sin(a) + 40, z = Math.sin(a) * .5 + .5; c.style.transform = `translate(${x - 80}px,${y - 33}px) scale(${.72 + z * .5})`; c.style.zIndex = z > .5 ? 8 : 3; c.style.opacity = Math.min(1, Math.max(0, (t - .35 - i * .08) * 5)); });
  });
  // focus pull + headline
  tl.fromTo(hud, { filter: 'blur(30px)', scale: 1.08, transformOrigin: '540px 905px' }, { filter: 'blur(0px)', scale: 1, duration: 1.5, ease: 'power3.out' }, t0 + .05);
  const a = h(`<div class="abs disp" style="left:70px;top:190px;font-size:92px;white-space:nowrap">Every detail,</div>`, s), b = h(`<div class="abs disp" style="left:70px;top:288px;font-size:124px;font-weight:600;white-space:nowrap">in focus.</div>`, s);
  tl.fromTo([a, b], { filter: 'blur(26px)', opacity: .0, y: 30 }, { filter: 'blur(0px)', opacity: 1, y: 0, duration: 1.3, ease: 'power3.out', stagger: .25 }, t0 + .02);
  b.classList.add('gt'); 
  const lock = h(`<div class="chip glass" style="left:290px;top:1262px;height:70px;font-size:24px;letter-spacing:.24em;font-family:JBM,monospace;font-weight:700"><span class="dot"></span>IN FOCUS · LOCKED</div>`, s);
  tl.fromTo(lock, { opacity: 0, y: 30, scale: .85 }, { opacity: 1, y: 0, scale: 1, duration: .4, ease: E.back }, t0 + 1.45);
  [['f/1.4', 'APERTURE'], ['1/60', 'SHUTTER'], ['100', 'ISO']].forEach(([v, l], i) => {
    const c = h(`<div class="glass" style="left:${60 + i * 322}px;top:1350px;width:300px;height:118px;border-radius:30px"><div class="abs mono" style="left:26px;top:16px;font-size:48px;font-weight:700">${v}</div><div class="abs mono" style="left:28px;top:82px;font-size:19px;letter-spacing:.3em;color:rgba(244,239,233,.7)">${l}</div></div>`, s);
    tl.fromTo(c, { opacity: 0, y: 70 }, { opacity: 1, y: 0, duration: .45, ease: E.out }, t0 + 1.2 + i * .12);
  });
})();

/* ===== H · what we make (28.125–31.875 s)  "Launch films. Product films. Training films." ===== */
(() => {
  const s = $('#sH .in'); const t0 = T(60);
  const a = h(`<div class="abs disp" style="left:70px;top:200px;font-size:100px;white-space:nowrap">Films for</div>`, s), b = h(`<div class="abs disp" style="left:70px;top:312px;font-size:128px;font-weight:600;white-space:nowrap">every moment.</div>`, s);
  reveal(chars(a), t0 - .05, { stagger: .03, d: .5 }); reveal(chars(b, 'ch gt'), t0 + .12, { stagger: .03, d: .55 });
  const cube = `<div class="abs" style="left:95px;top:60px;width:110px;height:110px;perspective:600px"><div class="cb" style="position:absolute;inset:0;transform-style:preserve-3d">${[['rotateY(0deg)'], ['rotateY(90deg)'], ['rotateY(180deg)'], ['rotateY(-90deg)'], ['rotateX(90deg)'], ['rotateX(-90deg)']].map(([tf], i) => `<div style="position:absolute;inset:0;transform:${tf} translateZ(55px);background:linear-gradient(135deg,rgba(255,110,5,${.25 + (i % 3) * .12}),rgba(255,255,255,.1));border:1.5px solid rgba(255,255,255,.7)"></div>`).join('')}</div></div>`;
  const launch = `<svg viewBox="0 0 300 200" width="300" height="200" class="abs" style="left:0;top:20px"><path class="la" d="M40 170 Q110 160 150 100 T250 24" fill="none" stroke="#FF6E05" stroke-width="5" stroke-linecap="round" stroke-dasharray="320" stroke-dashoffset="320"/><circle class="lc" r="9" fill="#fff" cx="40" cy="170"/><g fill="rgba(255,255,255,.7)"><circle cx="70" cy="60" r="2.5"/><circle cx="210" cy="150" r="2.5"/><circle cx="250" cy="90" r="2"/><circle cx="120" cy="30" r="2"/></g></svg>`;
  const train = `<svg viewBox="0 0 300 200" width="300" height="200" class="abs" style="left:0;top:20px"><line x1="150" y1="30" x2="150" y2="170" stroke="rgba(255,255,255,.25)" stroke-width="3"/><line class="tp" x1="150" y1="30" x2="150" y2="170" stroke="#FF6E05" stroke-width="3" stroke-dasharray="140" stroke-dashoffset="140"/>${[30, 80, 125, 170].map((y, i) => `<circle class="tn" cx="150" cy="${y}" r="13" fill="#05060a" stroke="rgba(255,255,255,.5)" stroke-width="3"/>`).join('')}</svg>`;
  const defs = [['01', 'Launch', launch, 60, 600, -1400, 0], ['02', 'Product', cube, 390, 700, 0, 1500], ['03', 'Training', train, 720, 600, 1400, 0]];
  const cards = defs.map(([n, name, art, x, y, fx, fy], i) => {
    const c = h(`<div class="glass" style="left:${x}px;top:${y}px;width:300px;height:700px;border-radius:48px"><div class="abs mono" style="left:30px;top:30px;font-size:22px;letter-spacing:.3em;color:rgba(255,255,255,.6)">${n}</div><div class="abs" style="left:0;top:100px;width:300px;height:230px;transform:scale(1.25);transform-origin:50% 40%">${art}</div><div class="abs disp" style="left:30px;top:470px;font-size:58px;font-weight:500">${name}</div><div class="abs mono" style="left:32px;top:548px;font-size:24px;letter-spacing:.3em;color:#FF9A3D">FILMS</div><div class="abs" style="left:30px;right:30px;bottom:34px;height:3px;background:rgba(255,255,255,.15)"><i class="pg" style="display:block;height:100%;width:100%;background:#FF6E05;transform-origin:0 50%;transform:scaleX(0)"></i></div></div>`, s);
    const t = t0 + i * 2 * BEAT * .55 + .1;
    tl.fromTo(c, { x: fx, y: fy, rotation: i == 1 ? 0 : (i ? 14 : -14), opacity: 0 }, { x: 0, y: 0, rotation: 0, opacity: 1, duration: .5, ease: E.snap }, t);
    tl.to($('.pg', c), { scaleX: 1, duration: 1.4, ease: 'power1.inOut' }, t + .3);
    tl.to(c, { y: -18, duration: .9, ease: 'sine.inOut', yoyo: true, repeat: 1 }, t + .5);
    return c;
  });
  tl.to($('.la', cards[0]), { strokeDashoffset: 0, duration: .9, ease: 'power2.out' }, t0 + .3);
  drive(t0 + .3, .9, p => { const pa = $('.la', cards[0]); const L = pa.getTotalLength(); const pt = pa.getPointAtLength(ease('power2.out', p) * L); const c = $('.lc', cards[0]); c.setAttribute('cx', pt.x); c.setAttribute('cy', pt.y); });
  tl.to($('.cb', cards[1]), { rotationY: 360, rotationX: 40, duration: 3, ease: 'none' }, t0 + .8);
  tl.to($('.tp', cards[2]), { strokeDashoffset: 0, duration: 1.2, ease: 'none' }, t0 + 1.3);
  $$('.tn', cards[2]).forEach((n, i) => tl.to(n, { fill: '#FF6E05', stroke: '#fff', duration: .15 }, t0 + 1.3 + i * .4));
  tl.to(cards, { rotationY: (i) => [10, 0, -10][i], duration: 1.2, ease: 'sine.inOut' }, t0 + 2.2);
})();
