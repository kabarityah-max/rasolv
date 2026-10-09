/* ===== A · hook (0–3.75 s)  "This entire film was created by Claude Code." ===== */
(() => {
  const s = $('#sA .in');
  // viewfinder (brand mark present from the first frame)
  const ghost = h(`<div class="abs" id="a-ghost" style="left:290px;top:510px;width:500px;height:500px;opacity:.16"></div>`, s); ap(ghost, { r: 37, grow: 1, bp: 1, gap: '#05060a' }); tl.to(ghost, { rotation: 60, duration: 3.8, ease: 'none' }, 0);
  const vf = h(`<svg class="abs" style="left:0;top:0" width="1080" height="1920" viewBox="0 0 1080 1920"><g transform="translate(540 760)" id="a-vf">${tickRing(420, 120, 8, 5, 'rgba(244,239,233,.5)', 2)}<circle r="400" fill="none" stroke="rgba(244,239,233,.18)" stroke-width="1.5"/><circle r="330" fill="none" stroke="rgba(255,110,5,.5)" stroke-width="2" stroke-dasharray="3 14"/><path d="M-470 0H-300M300 0H470M0 -470V-300M0 300V470" stroke="rgba(244,239,233,.35)" stroke-width="2"/></g></svg>`, s);
  tl.fromTo('#a-vf', { rotation: -30, scale: 1.25, opacity: 0, svgOrigin: '540 760' }, { rotation: 20, scale: 1, opacity: 1, duration: 3.8, ease: 'power1.out', svgOrigin: '540 760' }, 0);
  // title
  const l1 = h(`<div class="abs disp" style="left:70px;top:610px;font-size:124px;white-space:nowrap">This entire film</div>`, s);
  const c1 = chars(l1);
  c1.forEach((c, i) => { if (i > 11) c.classList.add('gt'); });
  reveal(c1, 0.0, { stagger: .03, d: .55 });
  tl.to(c1, { y: -520, opacity: 0, filter: 'blur(14px)', duration: .4, ease: E.in, stagger: .012 }, 1.45);
  // terminal
  const term = h(`<div class="glass" id="a-term" style="left:64px;top:200px;width:952px;height:470px;border-radius:36px"></div>`, s);
  term.innerHTML = `<div class="abs mono" style="left:36px;top:26px;font-size:22px;letter-spacing:.18em;color:rgba(244,239,233,.55)">CLAUDE CODE · RASOLV-FILM</div><div class="abs" style="left:36px;right:36px;top:72px;height:1px;background:rgba(255,255,255,.15)"></div>
   <div class="abs mono" style="left:40px;top:100px;font-size:33px;line-height:1.55;width:880px"><div id="a-l1"></div><div id="a-l2" style="color:rgba(244,239,233,.62)"></div><div id="a-l3" style="color:rgba(244,239,233,.62)"></div><div id="a-l4" style="color:rgba(244,239,233,.62)"></div><div id="a-l5" style="color:var(--or)"></div></div>
   <div class="abs" style="left:40px;right:40px;bottom:40px;height:8px;border-radius:4px;background:rgba(255,255,255,.12)"><div id="a-bar" style="height:100%;width:100%;border-radius:4px;background:linear-gradient(90deg,#FF6E05,#FFC59A);transform-origin:0 50%;transform:scaleX(0)"></div></div>`;
  tl.fromTo(term, { y: 1500, rotation: 4, opacity: 0 }, { y: 0, rotation: 0, opacity: 1, duration: .6, ease: E.snap }, 1.35);
  const L = [['a-l1', '<b style="color:#FF6E05">›</b> make the RASOLV film', 1.7, .55], ['a-l5', '▸ rendering 1,800 frames', 2.5, .5]];
  L.forEach(([id, txt, t, d]) => { const el = $('#' + id); const plain = txt.replace(/<[^>]+>/g, ''); drive(t, d, p => { const n = Math.floor(p * plain.length); el.innerHTML = p >= 1 ? txt : plain.slice(0, n) + '<span style="opacity:.8">▍</span>'; }); });
  tl.to('#a-bar', { scaleX: 1, duration: 1.7, ease: 'power1.inOut' }, 2.0);
  // was created by / Claude Code
  const cb = h(`<div class="abs mono" style="left:72px;top:760px;font-size:36px;letter-spacing:.42em;color:rgba(244,239,233,.95)">WAS CREATED BY</div>`, s);
  const n1 = h(`<div class="abs disp" style="left:64px;top:840px;font-size:176px;font-weight:400">Claude</div>`, s), n2 = h(`<div class="abs disp" style="left:64px;top:1020px;font-size:176px;font-weight:500">Code</div>`, s);
  const ch1 = chars(n1), ch2 = chars(n2, 'ch gt');
  tl.fromTo(cb, { opacity: 0, x: -30 }, { opacity: 1, x: 0, duration: .35 }, 1.7);
  reveal(ch1, 2.1, { stagger: .04, d: .55, y: 80 }); reveal(ch2, 2.5, { stagger: .05, d: .6, y: 80 });
  tl.fromTo(h(`<div class="abs" style="left:64px;top:1230px;width:0;height:3px;background:linear-gradient(90deg,#FF6E05,transparent)"></div>`, s), { width: 0 }, { width: 560, duration: .7, ease: E.out }, 2.9);
})();

/* ===== B · code → frames (3.75–7.5 s)  "Written in code. Rendered with HyperFrames." ===== */
(() => {
  const s = $('#sB .in');
  const stage = h(`<div class="abs" style="inset:0;perspective:1600px"></div>`, s);
  const code = h(`<div class="glass" id="b-code" style="left:56px;top:200px;width:968px;height:700px;border-radius:36px;transform-origin:50% 50%"></div>`, stage);
  const src = [
    '<span class="k">&lt;div</span> <span class="a">class</span>=<span class="s">"clip"</span> <span class="a">data-start</span>=<span class="s">"7.5"</span><span class="k">&gt;</span>',
    '  <span class="k">&lt;h1</span> <span class="a">id</span>=<span class="s">"hero"</span><span class="k">&gt;</span>Rasolv<span class="k">&lt;/h1&gt;</span>',
    '<span class="k">&lt;/div&gt;</span>', '',
    '<span class="d">const</span> tl = gsap.<span class="f">timeline</span>({ paused: <span class="d">true</span> });',
    'tl.<span class="f">fromTo</span>(<span class="s">"#hero"</span>,',
    '  { y: <span class="n">80</span>, opacity: <span class="n">0</span> },',
    '  { y: <span class="n">0</span>, opacity: <span class="n">1</span>, ease: <span class="s">"expo.out"</span> }, <span class="n">0.4</span>);',
    'tl.<span class="f">to</span>(<span class="s">"#hero"</span>, { scale: <span class="n">1.2</span> }, <span class="n">1.2</span>);',
    'window.__timelines[<span class="s">"main"</span>] = tl;'];
  code.innerHTML = `<style>#b-code .k{color:#FF9A3D}#b-code .a{color:#9fd3ff}#b-code .s{color:#ffd9a8}#b-code .d{color:#ff7aa8}#b-code .f{color:#9ef0b8}#b-code .n{color:#ffd166}</style>
   <div class="abs mono" style="left:36px;top:26px;font-size:22px;letter-spacing:.18em;color:rgba(244,239,233,.55)">INDEX.HTML</div><div class="abs" style="left:36px;right:36px;top:72px;height:1px;background:rgba(255,255,255,.15)"></div>
   <div class="abs mono" style="left:36px;top:96px;width:60px;font-size:28px;line-height:1.62;color:rgba(244,239,233,.28);white-space:pre">${src.map((_, i) => i + 1).join('\n')}</div>
   <div class="abs mono" style="left:100px;top:96px;width:850px;font-size:28px;line-height:1.62;color:#F4EFE9;white-space:pre">${src.map(l => `<div class="bl" style="opacity:0">${l || '&nbsp;'}</div>`).join('')}</div>`;
  tl.fromTo(code, { y: -800, rotationX: 30, opacity: 0 }, { y: 0, rotationX: 0, opacity: 1, duration: .55, ease: E.snap }, 3.62);
  $$('.bl', code).forEach((l, i) => tl.fromTo(l, { opacity: 0, x: -30 }, { opacity: 1, x: 0, duration: .16 }, 3.95 + i * .17));
  // render stage: filmstrip + counter
  const strip = h(`<div class="abs" id="b-strip" style="left:56px;top:960px;width:968px;height:240px"></div>`, s);
  for (let i = 0; i < 8; i++) h(`<div class="glass" style="left:${i * 122}px;top:0;width:106px;height:188px;border-radius:20px;background:linear-gradient(${150 + i * 12}deg,rgba(255,110,5,${.2 + i * .07}),rgba(255,255,255,.04))"><div class="abs mono" style="left:12px;bottom:10px;font-size:20px;color:rgba(255,255,255,.8)">${String(i * 257).padStart(4, '0')}</div></div>`, strip);
  const ph = h(`<div class="abs" style="left:0;top:-12px;width:4px;height:212px;background:#fff;border-radius:2px;box-shadow:0 0 22px #fff"></div>`, strip);
  tl.fromTo(strip, { opacity: 0, y: 200 }, { opacity: 1, y: 0, duration: .45, ease: E.out }, 4.7);
  tl.fromTo(ph, { x: 0 }, { x: 962, duration: 2.0, ease: 'power1.inOut' }, 4.9);
  const ctr = h(`<div class="abs mono center" id="b-ctr" style="top:1240px;font-size:128px;font-weight:700;line-height:1;letter-spacing:-.04em">0000</div>`, s);
  const sub = h(`<div class="abs mono center" style="top:1388px;font-size:28px;letter-spacing:.4em;color:rgba(244,239,233,.55)">FRAME / 1800</div>`, s);
  tl.fromTo([ctr, sub], { opacity: 0, y: 50 }, { opacity: 1, y: 0, duration: .35, ease: E.out }, 4.8);
  drive(4.9, 1.7, p => { ctr.textContent = String(Math.round(ease('power2.inOut', p) * 1800)).padStart(4, '0'); });
  // HyperFrames lockup
  const hf = h(`<div class="abs disp center" id="b-hf" style="top:1190px;font-size:128px;white-space:nowrap;font-weight:400">Hyper<b class="or">Frames</b></div>`, s);
  tl.to([ctr, sub], { opacity: 0, scale: .85, duration: .2 }, 6.3);
  tl.to(code, { y: -90, scale: .92, opacity: .22, filter: 'blur(6px)', duration: .4, ease: E.in }, 6.3);
  tl.fromTo(hf, { scale: 1.8, opacity: 0, filter: 'blur(16px)' }, { scale: 1, opacity: 1, filter: 'blur(0px)', duration: .45, ease: E.out }, 6.4);
  const tag = h(`<div class="chip glass" style="left:300px;top:1340px;height:76px;font-size:28px;letter-spacing:.2em;font-family:JBM,monospace;font-weight:700"><span class="dot"></span>HTML → MP4</div>`, s);
  tl.fromTo(tag, { opacity: 0, y: 40, scale: .85 }, { opacity: 1, y: 0, scale: 1, duration: .35, ease: E.back }, 6.8);
})();

/* ===== C · aperture + RASOLV (7.5–11.25 s)  "With our agency, RASOLV, we can do the same for you." ===== */
(() => {
  const s = $('#sC .in');
  // light beams converge to build the mark
  const beams = h(`<svg class="abs" style="left:0;top:0" width="1080" height="1920" viewBox="0 0 1080 1920"><defs><linearGradient id="bg1" x1="0" x2="1"><stop offset="0" stop-color="#FF6E05" stop-opacity="0"/><stop offset="1" stop-color="#FFC59A" stop-opacity=".95"/></linearGradient></defs>${[0, 1, 2, 3, 4, 5].map(i => { const a = (-90 + i * 60) * Math.PI / 180; const x0 = 540 + Math.cos(a) * 1300, y0 = 680 + Math.sin(a) * 1300; return `<g class="bm"><line x1="${x0}" y1="${y0}" x2="540" y2="680" stroke="url(#bg1)" stroke-width="5" style="stroke-dasharray:1400;stroke-dashoffset:1400"/></g>`; }).join('')}</svg>`, s);
  $$('.bm line', beams).forEach((l, i) => { tl.to(l, { strokeDashoffset: 0, duration: .4, ease: 'power2.in' }, 7.3 + i * .03); tl.to(l, { opacity: 0, duration: .25 }, 7.78); });
  const rings = [0, 1].map(i => h(`<div class="abs" style="z-index:0;left:215px;top:355px;width:650px;height:650px;border-radius:50%;border:2px solid rgba(255,110,5,.7)"></div>`, s));
  const host = h(`<div class="abs" id="c-ap" style="z-index:1;left:190px;top:330px;width:700px;height:700px"></div>`, s);
  drive(7.55, .9, p => { const k = ease('power3.out', p); ap(host, { r: 37 + 5 * Math.sin(p * 3.14), grow: k, bp: k, gap: '#05060a' }); });
  tl.fromTo(host, { rotation: -100, scale: .4, opacity: 0 }, { rotation: 0, scale: 1, opacity: 1, duration: .9, ease: E.out }, 7.6);
  rings.forEach((r, i) => tl.fromTo(r, { scale: .5, opacity: .9 }, { scale: 2.6, opacity: 0, duration: 1.2, ease: 'power2.out' }, 7.62 + i * .25));
  const ag = h(`<div class="abs mono center" style="top:1090px;font-size:34px;letter-spacing:.46em;color:#fff;text-shadow:0 0 24px rgba(0,0,0,.9)">WITH OUR AGENCY</div>`, s);
  tl.fromTo(ag, { opacity: 0, y: 24 }, { opacity: 1, y: 0, duration: .35 }, 7.75);
  const word = h(`<div class="abs disp center" style="top:1150px;font-size:178px;font-weight:600;white-space:nowrap;letter-spacing:.06em">RASOLV</div>`, s);
  const cs = chars(word);
  reveal(cs, 8.55, { stagger: .06, d: .6, y: 110 });
  // "we can do the same for you"
  const grp = h(`<div class="abs" style="left:0;top:0;width:1080px;height:1920px"></div>`, s);
  const l1 = h(`<div class="abs disp" style="left:70px;top:760px;font-size:118px;white-space:nowrap">We can do</div>`, grp);
  const l2 = h(`<div class="abs disp" style="left:70px;top:890px;font-size:170px;font-weight:500;white-space:nowrap">the same</div>`, grp);
  const l3 = h(`<div class="abs disp" style="left:70px;top:1075px;font-size:226px;font-weight:600;white-space:nowrap">for you.</div>`, grp);
  tl.to([host, word, ag, ...rings], { y: '-=640', scale: .6, opacity: 0, filter: 'blur(10px)', duration: .4, ease: E.in, stagger: .02 }, 9.45);
  reveal(chars(l1), 9.65, { stagger: .02, d: .45 }); reveal(chars(l2), 9.95, { stagger: .03, d: .5 });
  const c3 = chars(l3, 'ch gt'); reveal(c3, 10.3, { stagger: .05, d: .6, y: 90 });
  tl.fromTo(h(`<div class="abs" style="left:70px;top:1360px;width:0;height:3px;background:linear-gradient(90deg,#FF6E05,transparent)"></div>`, grp), { width: 0 }, { width: 760, duration: .8, ease: E.out }, 10.55);
  const mini = h(`<div class="abs" id="c-mini" style="left:70px;top:330px;width:150px;height:150px"></div>`, grp);
  drive(9.6, .5, p => ap(mini, { r: 37, grow: 1, bp: p, gap: '#05060a' }));
  tl.fromTo(mini, { scale: 0, rotation: -90 }, { scale: 1, rotation: 0, duration: .5, ease: E.back }, 9.6);

})();
