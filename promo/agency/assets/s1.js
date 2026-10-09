/* ===== A · hook (0–3.75 s) ===== */
(() => {
  const s = $('#sA .in');
  h(`<div class="abs mono" style="left:0;right:0;top:170px;text-align:center;font-size:700px;line-height:1;color:rgba(255,110,5,.10);font-weight:700" id="a-star">✻</div>`, s);
  tl.fromTo('#a-star', { rotation: -40, scale: .6 }, { rotation: 60, scale: 1.15, duration: 3.9, ease: 'none' }, 0);
  const w = ['THIS', 'ENTIRE', 'VIDEO<span class="or">?</span>'].map((t, i) => h(`<div class="abs big" style="left:64px;top:${330 + i * 255}px;font-size:${i == 1 ? 232 : 262}px;white-space:nowrap">${t}</div>`, s));
  [0.35, 0.6, 0.99].forEach((t, i) => tl.fromTo(w[i], { x: -1000, rotation: -7, opacity: 0 }, { x: 0, rotation: 0, opacity: 1, duration: .3, ease: E.snap }, t - .06));
  tl.to(w, { y: -900, opacity: 0, rotation: 4, stagger: .05, duration: .34, ease: E.in }, 1.42);
  // terminal
  const term = h(`<div class="glass" id="a-term" style="left:60px;top:250px;width:960px;height:520px;border-radius:44px"></div>`, s);
  term.innerHTML = `<div class="abs" style="left:34px;top:30px;display:flex;gap:14px"><i style="width:20px;height:20px;border-radius:50%;background:#ff5f57"></i><i style="width:20px;height:20px;border-radius:50%;background:#febc2e"></i><i style="width:20px;height:20px;border-radius:50%;background:#28c840"></i></div>
   <div class="abs mono" style="left:44px;top:96px;font-size:35px;line-height:1.55;color:#F4EFE9;width:880px"><div id="a-l1"></div><div id="a-l2" style="color:rgba(244,239,233,.65)"></div><div id="a-l3" style="color:rgba(244,239,233,.65)"></div><div id="a-l4" style="color:rgba(244,239,233,.65)"></div><div id="a-l5" style="color:var(--or)"></div></div>`;
  tl.fromTo(term, { y: 1500, rotation: 5, opacity: 0 }, { y: 0, rotation: 0, opacity: 1, duration: .55, ease: E.snap }, 1.38);
  const L = [['a-l1', '<b style="color:#FF6E05">❯</b> claude "build the rasolv film"', 1.7, .55], ['a-l2', '✓ storyboard · 16 scenes', 2.28, .3], ['a-l3', '✓ voiceover · music · captions', 2.5, .35], ['a-l4', '✓ motion graphics · maps · 3D', 2.75, .35], ['a-l5', '▸ rendering 1,800 frames…', 3.0, .4]];
  L.forEach(([id, txt, t, d]) => { const el = $('#' + id); const plain = txt.replace(/<[^>]+>/g, ''); drive(t, d, p => { const n = Math.floor(p * plain.length); el.innerHTML = p >= 1 ? txt : plain.slice(0, n) + '<span style="opacity:.8">▍</span>'; }); });
  // BUILT BY CLAUDE CODE
  const bb = h(`<div class="abs mono center" style="top:860px;font-size:42px;letter-spacing:.5em;color:rgba(244,239,233,.7);font-weight:700">BUILT BY</div>`, s);
  const c1 = h(`<div class="abs big center" style="top:935px;font-size:224px">CLAUDE</div>`, s);
  const c2 = h(`<div class="abs big center or" style="top:1150px;font-size:224px">CODE</div>`, s);
  tl.fromTo(bb, { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: .3 }, 1.62);
  tl.fromTo(c1, { scale: 2.4, opacity: 0, y: 80 }, { scale: 1, opacity: 1, y: 0, duration: .32, ease: E.snap }, 2.15);
  tl.fromTo(c2, { scale: 2.4, opacity: 0, y: 80 }, { scale: 1, opacity: 1, y: 0, duration: .32, ease: E.snap }, 2.45);
  tl.to(c2, { scale: 1.04, duration: .24, yoyo: true, repeat: 3, ease: 'sine.inOut' }, 2.9);
})();

/* ===== B · code → frame (3.75–7.5 s) ===== */
(() => {
  const s = $('#sB .in');
  const code = h(`<div class="glass" id="b-code" style="left:50px;top:210px;width:980px;height:640px;border-radius:44px"></div>`, s);
  const src = [
    ['<span class="k">&lt;div</span> <span class="a">class</span>=<span class="s">"clip"</span> <span class="a">data-start</span>=<span class="s">"7.5"</span><span class="k">&gt;</span>'],
    ['  <span class="k">&lt;h1</span> <span class="a">id</span>=<span class="s">"hero"</span><span class="k">&gt;</span>Rasolv<span class="k">&lt;/h1&gt;</span>'],
    ['<span class="k">&lt;/div&gt;</span>'],
    [''],
    ['<span class="d">const</span> tl = gsap.<span class="f">timeline</span>({ paused: <span class="d">true</span> });'],
    ['tl.<span class="f">fromTo</span>(<span class="s">"#hero"</span>,'],
    ['  { y: <span class="n">80</span>, opacity: <span class="n">0</span> },'],
    ['  { y: <span class="n">0</span>, opacity: <span class="n">1</span>, ease: <span class="s">"expo.out"</span> }, <span class="n">0.4</span>);'],
    ['tl.<span class="f">to</span>(<span class="s">"#hero"</span>, { scale: <span class="n">1.2</span> }, <span class="n">1.2</span>);'],
    ['window.__timelines[<span class="s">"main"</span>] = tl;'],
  ];
  code.innerHTML = `<style>#b-code .k{color:#FF9A3D}#b-code .a{color:#9fd3ff}#b-code .s{color:#ffd9a8}#b-code .d{color:#ff7aa8}#b-code .f{color:#9ef0b8}#b-code .n{color:#ffd166}</style>
   <div class="abs" style="left:34px;top:28px;display:flex;gap:14px"><i style="width:20px;height:20px;border-radius:50%;background:#ff5f57"></i><i style="width:20px;height:20px;border-radius:50%;background:#febc2e"></i><i style="width:20px;height:20px;border-radius:50%;background:#28c840"></i></div>
   <div class="abs mono" style="right:40px;top:26px;font-size:24px;color:rgba(244,239,233,.5)">index.html</div>
   <div class="abs mono" id="b-lines" style="left:40px;top:96px;width:900px;font-size:30px;line-height:1.62;color:#F4EFE9;white-space:pre">${src.map((l, i) => `<div class="bl" style="opacity:0">${l[0] || '&nbsp;'}</div>`).join('')}</div>`;
  tl.fromTo(code, { y: -700, rotation: -4, opacity: 0 }, { y: 0, rotation: 0, opacity: 1, duration: .5, ease: E.snap }, 3.62);
  $$('.bl', code).forEach((l, i) => tl.fromTo(l, { opacity: 0, x: -30 }, { opacity: 1, x: 0, duration: .18 }, 3.95 + i * .2));
  // timeline strip
  const strip = h(`<div class="abs" id="b-strip" style="left:50px;top:900px;width:980px;height:230px"></div>`, s);
  for (let i = 0; i < 8; i++) h(`<div class="glass" style="left:${i * 124}px;top:0;width:108px;height:192px;border-radius:22px;background:linear-gradient(${150 + i * 14}deg,rgba(255,110,5,${.25 + i * .07}),rgba(255,255,255,.05))"><div class="abs mono" style="left:12px;bottom:10px;font-size:22px;color:rgba(255,255,255,.8)">${String(i * 257).padStart(4, '0')}</div></div>`, strip);
  const ph = h(`<div class="abs" id="b-play" style="left:0;top:-14px;width:6px;height:230px;background:#fff;border-radius:3px;box-shadow:0 0 24px #fff"></div>`, strip);
  tl.fromTo(strip, { opacity: 0, y: 200 }, { opacity: 1, y: 0, duration: .45, ease: E.out }, 4.5);
  tl.fromTo(ph, { x: 0 }, { x: 970, duration: 2.5, ease: 'power1.inOut' }, 4.7);
  // frame counter
  const ctr = h(`<div class="abs mono center" id="b-ctr" style="top:1190px;font-size:150px;font-weight:700;line-height:1;letter-spacing:-.04em">0000</div>`, s);
  const sub = h(`<div class="abs mono center" id="b-sub" style="top:1370px;font-size:34px;letter-spacing:.34em;color:rgba(244,239,233,.6)">FRAME / 1800</div>`, s);
  tl.fromTo([ctr, sub], { opacity: 0, y: 60 }, { opacity: 1, y: 0, duration: .35, ease: E.out }, 4.6);
  drive(4.7, 1.9, p => { ctr.textContent = String(Math.round(gsap.parseEase('power2.inOut')(p) * 1800)).padStart(4, '0'); });
  // hyperframes slam
  const hf = h(`<div class="abs big center" id="b-hf" style="top:1160px;font-size:134px;white-space:nowrap;letter-spacing:-.03em">HYPER<span class="or">FRAMES</span></div>`, s);
  tl.to([ctr, sub], { opacity: 0, scale: .8, duration: .2 }, 6.2);
  tl.to(code, { y: -120, scale: .9, opacity: .25, filter: 'blur(6px)', duration: .4, ease: E.in }, 6.2);
  tl.fromTo(hf, { scale: 2.6, opacity: 0 }, { scale: 1, opacity: 1, duration: .34, ease: E.snap }, 6.3);
  const tag = h(`<div class="chip glass" style="left:250px;top:1330px;height:84px;font-size:34px"><span class="dot"></span>RENDERED FROM HTML</div>`, s);
  tl.fromTo(tag, { opacity: 0, y: 40, scale: .8 }, { opacity: 1, y: 0, scale: 1, duration: .35, ease: E.back }, 6.7);
})();

/* ===== C · aperture + RASOLV (7.5–11.25 s) ===== */
(() => {
  const s = $('#sC .in');
  const rings = [0, 1, 2].map(i => h(`<div class="abs" style="left:240px;top:520px;width:600px;height:600px;border-radius:50%;border:3px solid rgba(255,110,5,.7)"></div>`, s));
  const host = h(`<div class="abs" id="c-ap" style="left:190px;top:470px;width:700px;height:700px"></div>`, s);
  drive(7.55, 1.0, p => { const k = gsap.parseEase('power3.out')(p); ap(host, { r: 37 + 6 * Math.sin(p * 3.14), grow: k, bp: k, gap: '#060606' }); });
  tl.fromTo(host, { rotation: -120, scale: .3, opacity: 0 }, { rotation: 0, scale: 1, opacity: 1, duration: 1.0, ease: E.out }, 7.5);
  rings.forEach((r, i) => tl.fromTo(r, { scale: .4, opacity: .9 }, { scale: 2.6, opacity: 0, duration: 1.1, ease: 'power2.out' }, 7.52 + i * .2));
  const ag = h(`<div class="abs mono center" style="top:1190px;font-size:40px;letter-spacing:.5em;color:rgba(244,239,233,.75);font-weight:700">WITH OUR AGENCY</div>`, s);
  tl.fromTo(ag, { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: .3 }, 7.7);
  const word = h(`<div class="abs big center" style="top:1250px;font-size:208px;white-space:nowrap;letter-spacing:.0em">RASOLV</div>`, s);
  const cs = chars(word);
  tl.fromTo(cs, { y: 260, opacity: 0, rotation: 8 }, { y: 0, opacity: 1, rotation: 0, duration: .34, ease: E.snap, stagger: .05 }, 8.35);
  // second half: "we can do the same for you"
  const grp = h(`<div class="abs" style="left:0;top:0;width:1080px;height:1920px"></div>`, s);
  const l1 = h(`<div class="abs big center" style="top:830px;font-size:150px;white-space:nowrap">WE CAN DO</div>`, grp);
  const l2 = h(`<div class="abs big center or" style="top:1000px;font-size:178px;white-space:nowrap">THE SAME</div>`, grp);
  const l3 = h(`<div class="abs big center" style="top:1190px;font-size:178px;white-space:nowrap">FOR YOU.</div>`, grp);
  tl.to([host, word, ag, ...rings], { y: '-=560', scale: .7, opacity: 0, duration: .36, ease: E.in, stagger: .02 }, 9.45);
  tl.fromTo(l1, { x: -1100 }, { x: 0, duration: .34, ease: E.snap }, 9.55);
  tl.fromTo(l2, { x: 1100 }, { x: 0, duration: .34, ease: E.snap }, 9.9);
  tl.fromTo(l3, { scale: 3, opacity: 0 }, { scale: 1, opacity: 1, duration: .32, ease: E.snap }, 10.25);
  tl.to(l3, { scale: 1.05, duration: .22, yoyo: true, repeat: 3, ease: 'sine.inOut' }, 10.6);
  const mini = h(`<div class="abs" id="c-mini" style="left:440px;top:360px;width:200px;height:200px"></div>`, grp);
  drive(9.6, .5, p => ap(mini, { r: 37, grow: 1, bp: p, gap: '#060606' }));
  tl.fromTo(mini, { scale: 0, rotation: -90 }, { scale: 1, rotation: 0, duration: .5, ease: E.back }, 9.6);
})();
