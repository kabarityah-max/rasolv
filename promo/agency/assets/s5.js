/* ===== M · "We see the whole picture. Then we solve it." (46.875–52.5 s) ===== */
(() => {
  const s = $('#sM .in'); const t0 = T(100), cx = 540, cy = 760;
  const beams = h(`<svg class="abs" style="left:0;top:0" width="1080" height="1920" viewBox="0 0 1080 1920"><defs><linearGradient id="bg2" x1="0" x2="1"><stop offset="0" stop-color="#FF6E05" stop-opacity="0"/><stop offset="1" stop-color="#FFC59A" stop-opacity=".95"/></linearGradient></defs>${[0, 1, 2, 3, 4, 5].map(i => { const a = (-90 + i * 60 + 30) * Math.PI / 180; return `<line x1="${cx + Math.cos(a) * 1400}" y1="${cy + Math.sin(a) * 1400}" x2="${cx}" y2="${cy}" stroke="url(#bg2)" stroke-width="5" style="stroke-dasharray:1500;stroke-dashoffset:1500"/>`; }).join('')}</svg>`, s);
  $$('line', beams).forEach((l, i) => { tl.to(l, { strokeDashoffset: 0, duration: .45, ease: 'power2.in' }, t0 - .1 + i * .04); tl.to(l, { opacity: 0, duration: .3 }, t0 + .6); });
  const ringsvg = h(`<svg class="abs" style="left:0;top:0" width="1080" height="1920" viewBox="0 0 1080 1920"><g transform="translate(${cx} ${cy})" id="m-r">${tickRing(330, 90, 8, 5, 'rgba(244,239,233,.5)', 2)}<circle r="300" fill="none" stroke="rgba(255,110,5,.45)" stroke-width="2" stroke-dasharray="3 12"/></g></svg>`, s);
  tl.fromTo('#m-r', { opacity: 0, scale: .6, svgOrigin: `${cx} ${cy}` }, { opacity: 1, scale: 1.25, duration: .8, ease: E.out, svgOrigin: `${cx} ${cy}` }, t0 + .2);
  tl.to('#m-r', { rotation: 70, duration: 5.6, ease: 'none', svgOrigin: `${cx} ${cy}` }, t0);
  const orb = h(`<div class="abs" id="m-orb" style="left:${cx - 215}px;top:${cy - 215}px;width:430px;height:430px;border-radius:50%;overflow:hidden;z-index:5;background:radial-gradient(circle at 32% 24%,rgba(255,255,255,.44),rgba(255,255,255,.07) 38%,rgba(255,110,5,.2) 70%,rgba(0,0,0,.45));border:1.5px solid rgba(255,255,255,.4);box-shadow:inset 0 0 60px rgba(255,255,255,.14),inset -22px -34px 70px rgba(255,110,5,.4),0 34px 90px rgba(0,0,0,.65),0 0 120px rgba(255,110,5,.36)"></div>`, s);
  const ah = h(`<div class="abs" style="left:75px;top:75px;width:280px;height:280px"></div>`, orb);
  h(`<div class="abs" style="left:64px;top:34px;width:170px;height:76px;border-radius:50%;background:radial-gradient(ellipse,rgba(255,255,255,.7),rgba(255,255,255,0) 70%);transform:rotate(-28deg)"></div>`, orb);
  tl.fromTo(orb, { scale: .2, opacity: 0 }, { scale: 1, opacity: 1, duration: .7, ease: E.back }, t0 + .25);
  const names = ['Brand', 'Product', 'Story', 'Data', 'Audience', 'Launch'];
  const chips = names.map(l => h(`<div class="chip glass" style="left:0;top:0;height:64px;font-size:27px;opacity:0"><span class="dot"></span>${l}</div>`, s));
  drive(t0, 5.6, p => { const t = p * 5.6;
    const open = ease('power3.out', (t - .5) / 1.6) * (1 - ease('power2.in', (t - 3.6) / .9) * .85); ap(ah, { r: 8 + 46 * open, grow: 1, bp: 0, gap: '#0a0a0f', lines: false }); ah.style.transform = `rotate(${t * 20}deg)`;
    const col = ease('power3.in', (t - 2.0) / .7);   // chips collapse into the sphere on "solve"
    chips.forEach((c, i) => { const a = i / 6 * 6.283 + t * 1.2 + .5; const R = 470 * (1 - col), z = Math.sin(a) * .5 + .5; const x = cx + R * Math.cos(a), y = cy + (R * .26) * Math.sin(a) + 20 * (1 - col); c.style.transform = `translate(${x - 90}px,${y - 32}px) scale(${(.7 + z * .5) * (1 - col * .6)})`; c.style.zIndex = z > .5 ? 8 : 3; c.style.opacity = Math.min(1, Math.max(0, (t - .5 - i * .08) * 5)) * (1 - col); });
    $('#m-orb').style.transform = `scale(${1.28 + .07 * Math.sin(Math.max(0, t - 2.0) * 7) * Math.max(0, 1 - (t - 2.0) / 1.2) + ease('power2.in', (t - 4.6) / 1.0) * .5})`;
  });
  tl.set('#flash', { backgroundColor: '#FFD0A8' }, t0 + 2.0).fromTo('#flash', { opacity: .4 }, { opacity: 0, duration: .3 }, t0 + 2.0);
  // text
  const a = h(`<div class="abs disp" style="left:70px;top:1130px;font-size:94px;white-space:nowrap">We see the</div>`, s), b = h(`<div class="abs disp" style="left:70px;top:1236px;font-size:116px;font-weight:600;white-space:nowrap">whole picture.</div>`, s);
  reveal(chars(a), t0 + .25, { stagger: .03, d: .5 }); reveal(chars(b, 'ch gt'), t0 + .45, { stagger: .03, d: .55 });
  tl.to([a, b], { opacity: 0, y: -50, filter: 'blur(10px)', duration: .3, ease: E.in }, t0 + 1.95);
  const c = h(`<div class="abs disp" style="left:70px;top:1130px;font-size:94px;white-space:nowrap">Then we</div>`, s), d = h(`<div class="abs disp" style="left:70px;top:1236px;font-size:156px;font-weight:600;white-space:nowrap">solve it.</div>`, s);
  reveal(chars(c), t0 + 2.1, { stagger: .03, d: .45 }); reveal(chars(d, 'ch gt'), t0 + 2.3, { stagger: .04, d: .6, y: 80 });
  // see · decide · solve tracker
  const lab = [['SEE', .4], ['SOLVE', 2.3]].map(([l, t], i) => { const e = h(`<div class="abs mono" style="left:${70 + i * 760}px;top:1040px;font-size:30px;letter-spacing:.34em;color:rgba(244,239,233,.5);font-weight:700;${i ? 'text-align:right;width:0;white-space:nowrap;direction:rtl;left:1010px' : ''}">${l}</div>`, s); tl.set(e, { color: '#FF8A33' }, t0 + t); return e; });
  h(`<div class="abs" style="left:70px;top:1090px;width:900px;height:2px;background:rgba(255,255,255,.2)"><i id="m-tr" style="display:block;height:100%;width:100%;background:#FF6E05;transform-origin:0 50%;transform:scaleX(0)"></i></div>`, s);
  tl.to('#m-tr', { scaleX: 1, duration: 2.7, ease: 'none' }, t0 + .3);
})();

/* ===== O · end card (52.5–60 s)  "RASOLV. Vision that solves. Let's build yours." ===== */
(() => {
  const s = $('#sO .in'); const t0 = T(112);
  const cx = 540, cy = 590;
  const tr = h(`<svg class="abs" style="left:0;top:0" width="1080" height="1920" viewBox="0 0 1080 1920"><g id="o-tick" transform="translate(${cx} ${cy})">${tickRing(372, 120, 8, 5, 'rgba(244,239,233,.5)', 2)}<circle r="350" fill="none" stroke="rgba(255,110,5,.4)" stroke-width="2" stroke-dasharray="3 12"/></g></svg>`, s);
  tl.fromTo('#o-tick', { opacity: 0, scale: .5, rotation: -60, svgOrigin: `${cx} ${cy}` }, { opacity: 1, scale: 1, rotation: 0, duration: 1.2, ease: E.out, svgOrigin: `${cx} ${cy}` }, t0 - .05);
  tl.to('#o-tick', { rotation: 40, duration: 6.5, ease: 'none', svgOrigin: `${cx} ${cy}` }, t0 + 1.2);
  const rings = [0, 1].map(i => h(`<div class="abs" style="left:${cx - 300}px;top:${cy - 300}px;width:600px;height:600px;border-radius:50%;border:2px solid rgba(255,110,5,.7)"></div>`, s));
  const host = h(`<div class="abs" id="o-ap" style="left:${cx - 300}px;top:${cy - 300}px;width:600px;height:600px"></div>`, s);
  drive(t0 - .05, .9, p => { const k = ease('power3.out', p); ap(host, { r: 37 + 5 * Math.sin(p * 3.14), grow: k, bp: k, gap: '#05060a' }); });
  tl.fromTo(host, { rotation: -140, scale: .3, opacity: 0 }, { rotation: 0, scale: 1, opacity: 1, duration: .95, ease: E.out }, t0 - .05);
  tl.to(host, { rotation: 18, duration: 6.5, ease: 'none' }, t0 + 1);
  rings.forEach((r, i) => tl.fromTo(r, { scale: .5, opacity: .9 }, { scale: 2.3, opacity: 0, duration: 1.3, ease: 'power2.out', repeat: 2, repeatDelay: .5 }, t0 + i * .3));
  const word = h(`<div class="abs disp center" style="top:960px;font-size:190px;font-weight:600;white-space:nowrap;letter-spacing:.06em">RASOLV</div>`, s);
  reveal(chars(word), t0 + .25, { stagger: .06, d: .6, y: 120 });
  const vs = h(`<div class="abs mono center" style="top:1210px;font-size:40px;letter-spacing:.3em;white-space:nowrap;color:#FF9A3D">VISION THAT SOLVES.</div>`, s);
  tl.fromTo(vs, { opacity: 0, y: 30, filter: 'blur(10px)' }, { opacity: 1, y: 0, filter: 'blur(0px)', duration: .6, ease: E.out }, t0 + 1.1);
  const cta = h(`<div class="chip" style="left:150px;top:1350px;width:780px;height:116px;border-radius:58px;justify-content:center;font-size:44px;font-weight:600;background:#FF6E05;color:#05060a;box-shadow:0 20px 70px rgba(255,110,5,.55), inset 0 2px 0 rgba(255,255,255,.55), inset 0 0 0 1.5px rgba(255,255,255,.35);overflow:hidden">Let's build yours.<i id="o-sh" style="position:absolute;top:-10%;left:-30%;width:22%;height:120%;background:linear-gradient(100deg,rgba(255,255,255,0),rgba(255,255,255,.55),rgba(255,255,255,0));transform:skewX(-18deg)"></i></div>`, s);
  tl.fromTo('#o-sh', { x: 0 }, { x: 1100, duration: .9, ease: 'power2.inOut', repeat: 3, repeatDelay: .8 }, t0 + 2.4);
  tl.fromTo(cta, { scale: .3, opacity: 0, y: 90 }, { scale: 1, opacity: 1, y: 0, duration: .5, ease: E.back }, t0 + 1.75);
  tl.to(cta, { scale: 1.035, duration: .234, yoyo: true, repeat: 14, ease: 'sine.inOut' }, t0 + 2.3);
  tl.set('#caps', { opacity: 0 }, t0 + 1.7);
  tl.to('#sO .in', { opacity: 0, duration: .55, ease: 'power1.in' }, 59.45);
})();
