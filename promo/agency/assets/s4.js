/* ===== I · voice / music / captions (30–33.75) ===== */
(() => {
  const s = $('#sI .in'); const t0 = T(64);
  h(`<div class="abs mono" style="left:64px;top:190px;font-size:34px;letter-spacing:.36em;color:#FF9A3D;font-weight:700">AND THE SOUND?</div>`, s);
  const mkRow = (y, label, sub, inner, fx) => { const r = h(`<div class="glass" style="left:60px;top:${y}px;width:960px;height:290px;border-radius:50px"><div class="abs" style="left:44px;top:34px;display:flex;align-items:center;gap:16px;font-weight:900;font-size:48px;letter-spacing:.02em"><span class="dot"></span>${label}<span class="mono" style="font-size:24px;font-weight:700;color:rgba(255,255,255,.55);margin-left:12px;letter-spacing:.2em">${sub}</span></div>${inner}</div>`, s); return r; };
  const bars = n => `<div class="abs" style="left:44px;right:44px;top:120px;height:130px;display:flex;align-items:center;gap:8px">${'<i style="flex:1;border-radius:6px;background:#FF6E05;height:20px"></i>'.repeat(n)}</div>`;
  const r1 = mkRow(280, 'VOICEOVER', 'KOKORO · AI VOICE', bars(48));
  const r2 = mkRow(600, 'MUSIC', 'ORIGINAL · 128 BPM', bars(32).replace(/#FF6E05/g, '#FFA24A'));
  const r3 = mkRow(920, 'CAPTIONS', 'WORD-TIMED', `<div class="abs big" id="i-cap" style="left:44px;right:44px;top:130px;font-size:84px;line-height:1;white-space:nowrap;letter-spacing:-.01em"><span style="color:rgba(255,255,255,.4)">ALL</span> <span style="color:rgba(255,255,255,.4)">GENERATED</span></div>`);
  [[r1, -1300], [r2, 1300], [r3, -1300]].forEach(([r, x], i) => tl.fromTo(r, { x, opacity: 0, rotation: i == 1 ? 4 : -4 }, { x: 0, opacity: 1, rotation: 0, duration: .45, ease: E.snap }, t0 + .15 + i * .5));
  const A = $$('i', r1), B = $$('i', r2);
  drive(t0, 3.75, p => { const t = p * 3.75; A.forEach((e, i) => e.style.height = (14 + 105 * Math.abs(Math.sin(t * 7.1 + i * .55)) * (.35 + .65 * Math.abs(Math.sin(i * 1.7 + t * 2.3)))) + 'px');
    B.forEach((e, i) => e.style.height = (16 + 108 * Math.abs(Math.sin(t * 8 + i * .9 + Math.sin(t * 3)))) * (1 - i / 60) + 'px'); });
  const cw = $$('span', $('#i-cap'));
  tl.set(cw[0], { color: '#FF6E05' }, t0 + 2.25).set(cw[1], { color: '#FF6E05' }, t0 + 2.55);
  const big = h(`<div class="abs big center" style="top:1250px;font-size:108px;white-space:nowrap">ALL <span class="or">GENERATED.</span></div>`, s);
  tl.fromTo(big, { scale: 2.6, opacity: 0 }, { scale: 1, opacity: 1, duration: .3, ease: E.snap }, t0 + 2.2);
})();

/* ===== J · every cut on the beat: 8 micro-cuts (33.75–37.5) ===== */
(() => {
  const s = $('#sJ .in'); const t0 = T(72);
  const defs = [
    ['#FF6E05', '#060606', '1', `<div class="jr" style="left:240px;top:520px;width:600px;height:600px;border-radius:50%;border:8px solid #060606"></div><div class="jr" style="left:240px;top:520px;width:600px;height:600px;border-radius:50%;border:8px solid #060606"></div>`],
    ['#060606', '#FF6E05', '2', `<div class="jr" style="left:200px;top:480px;width:680px;height:680px;border:10px solid #F4EFE9;transform:rotate(20deg)"></div>`],
    ['#F4EFE9', '#060606', '3', [0, 1, 2].map(i => `<div class="jb" style="left:${90 + i * 320}px;top:300px;width:240px;height:1200px;background:#FF6E05"></div>`).join('')],
    ['#FF6E05', '#F4EFE9', '4', [0, 1, 2, 3, 4].map(i => `<div class="jd" style="left:-400px;top:${200 + i * 300}px;width:1900px;height:80px;background:#060606;transform:rotate(-14deg)"></div>`).join('')],
    ['#060606', 'transparent', '5', `<div class="abs jap" style="left:-60px;top:380px;width:1200px;height:1200px;opacity:.9"></div>`],
    ['#F4EFE9', '#FF6E05', '6', Array.from({ length: 24 }, (_, i) => `<i class="jq" style="left:${60 + (i % 4) * 250}px;top:${240 + Math.floor(i / 4) * 250}px;width:150px;height:150px;border-radius:30px;background:#060606"></i>`).join('')],
    ['#060606', '#F4EFE9', '7', [0, 1, 2, 3].map(i => `<div class="jr" style="left:${540 - 150 - i * 120}px;top:${820 - 150 - i * 120}px;width:${300 + i * 240}px;height:${300 + i * 240}px;border-radius:50%;border:6px solid rgba(255,110,5,${.9 - i * .15})"></div>`).join('')],
    ['#FF6E05', '#060606', '8', `<div class="abs big center" style="top:1330px;font-size:84px;color:#060606;white-space:nowrap;letter-spacing:.02em">ON THE BEAT.</div>`],
  ];
  const panels = []; defs.forEach(([bg, fg, n, shapes], i) => {
    const p = h(`<div class="abs" style="inset:0;background:${bg};opacity:0;overflow:hidden"><style>.jr,.jb,.jd,.jq{position:absolute}</style>${shapes}<div class="abs big center" style="top:200px;font-size:1000px;line-height:1;color:${n == '5' ? 'transparent' : fg};${n == '5' ? '-webkit-text-stroke:10px #F4EFE9;' : ''}letter-spacing:-.04em">${n}</div></div>`, s);
    const a = t0 + i * BEAT; tl.set(p, { opacity: 1 }, a - (i ? 0 : .2)); if (i) tl.set(panels[i - 1], { opacity: 0 }, a);
    tl.fromTo($('.big', p), { scale: 1.5, opacity: 0 }, { scale: 1, opacity: 1, duration: .2, ease: E.snap }, a - (i ? 0 : .05));
    $$('.jr', p).forEach((e, k) => tl.fromTo(e, { scale: .3, opacity: 1 }, { scale: 1.6, opacity: 0, duration: .5, ease: 'power2.out', delay: k * .1 }, a));
    $$('.jb', p).forEach((e, k) => tl.fromTo(e, { y: 1600 }, { y: 0, duration: .3, ease: E.snap }, a + k * .06));
    $$('.jd', p).forEach((e, k) => tl.fromTo(e, { x: k % 2 ? 900 : -900 }, { x: 0, duration: .3, ease: E.snap }, a + k * .04));
    $$('.jq', p).forEach((e, k) => tl.fromTo(e, { scale: 0 }, { scale: 1, duration: .25, ease: E.back }, a + k * .012));
    panels.push(p);
  });
  ap($('.jap', panels[4]), { r: 37, grow: 1, bp: 1, color: '#FF6E05', gap: '#060606' });
  tl.fromTo($('.jap', panels[4]), { rotation: -90, scale: .4 }, { rotation: 0, scale: 1, duration: .4, ease: E.snap }, t0 + 4 * BEAT);
  // beat tracker
  const tr = h(`<div class="abs" style="left:60px;right:60px;top:1700px;display:flex;gap:10px"></div>`, s);
  for (let i = 0; i < 8; i++) { const c = h(`<i style="flex:1;height:22px;border-radius:11px;background:rgba(128,128,128,.55);display:block"></i>`, tr); tl.set(c, { backgroundColor: '#FF6E05', scaleY: 1.8 }, t0 + i * BEAT).to(c, { scaleY: 1, duration: .3 }, t0 + i * BEAT); }
})();

/* ===== K · five critics (37.5–41.25) ===== */
(() => {
  const s = $('#sK .in'); const t0 = T(80);
  h(`<div class="abs big" style="left:60px;top:170px;font-size:150px;line-height:.88" id="k-t">FIVE<br><span class="or">CRITICS</span></div>`, s);
  tl.fromTo('#k-t', { x: -800, opacity: 0 }, { x: 0, opacity: 1, duration: .34, ease: E.snap }, t0 - .05);
  const X0 = 250, W = 700, passX = X0 + W * .75;
  const lvl = [.52, .6, .68, .82, .93];
  const rows = lvl.map((v, i) => {
    const y = 600 + i * 176;
    const r = h(`<div class="glass" style="left:60px;top:${y}px;width:960px;height:150px;border-radius:44px"><div class="abs mono" style="left:34px;top:48px;font-size:30px;font-weight:700;letter-spacing:.12em">R${i + 1}</div><div class="abs" style="left:${X0 - 60}px;top:60px;width:${W}px;height:30px;border-radius:15px;background:rgba(255,255,255,.12)"><div class="kf" style="width:${v * 100}%;height:100%;border-radius:15px;background:${v >= .75 ? '#FF6E05' : '#d9d2c9'};transform-origin:0 50%"></div></div><div class="abs mono kv" style="right:30px;top:52px;font-size:28px;font-weight:700;color:${v >= .75 ? '#FF6E05' : 'rgba(255,255,255,.6)'}">${v >= .75 ? 'PASS' : 'REDO'}</div></div>`, s);
    const t = t0 + .1 + i * 1.5 * BEAT * .6;
    tl.fromTo(r, { x: i % 2 ? 1200 : -1200, opacity: 0 }, { x: 0, opacity: 1, duration: .4, ease: E.snap }, t);
    tl.fromTo($('.kf', r), { scaleX: 0 }, { scaleX: 1, duration: .6, ease: 'power3.out' }, t + .15);
    tl.fromTo($('.kv', r), { opacity: 0 }, { opacity: 1, duration: .15 }, t + .6);
    return r;
  });
  const line = h(`<div class="abs" style="left:${passX - 6 + 0}px;top:560px;width:0;height:900px;border-left:5px dashed #fff;opacity:0"></div>`, s);
  const lab = h(`<div class="chip glass" style="left:${passX - 150}px;top:488px;height:60px;font-size:26px;padding:0 24px;border-radius:30px"><span class="dot"></span>PASS BAR 75</div>`, s);
  tl.fromTo(line, { opacity: 0, scaleY: 0, transformOrigin: '50% 0' }, { opacity: 1, scaleY: 1, duration: .4, ease: E.out }, t0 + .2);
  tl.fromTo(lab, { opacity: 0, y: -30, scale: .8 }, { opacity: 1, y: 0, scale: 1, duration: .35, ease: E.back }, t0 + .45);
})();

/* ===== L · rejected (41.25–45) ===== */
(() => {
  const s = $('#sL .in'); const t0 = T(88);
  const cardA = h(`<div class="glass" id="l-a" style="left:110px;top:360px;width:860px;height:900px;border-radius:70px"><div class="abs mono center" style="top:70px;font-size:44px;letter-spacing:.4em;color:rgba(255,255,255,.7);font-weight:700">ANYTHING UNDER</div><div class="abs big center or" style="top:150px;font-size:520px;line-height:1;letter-spacing:-.04em">75</div></div>`, s);
  tl.fromTo(cardA, { y: -1400, rotation: -8, opacity: 0 }, { y: 0, rotation: 0, opacity: 1, duration: .45, ease: E.snap }, t0 - .15);
  const stamp = h(`<div class="abs" id="l-stamp" style="left:130px;top:820px;width:820px;padding:20px 0;text-align:center;border:16px solid #ff3b30;border-radius:28px;color:#ff3b30;font-weight:900;font-size:148px;letter-spacing:.02em;line-height:1;transform:rotate(-12deg);background:rgba(20,0,0,.35);opacity:0">REJECTED</div>`, s);
  tl.fromTo(stamp, { scale: 3.2, opacity: 0, rotation: -26 }, { scale: 1, opacity: 1, rotation: -12, duration: .22, ease: 'power4.in' }, t0 + 1.05);
  [[8, -6], [-8, 6], [5, -4], [0, 0]].forEach(([x, y], i) => tl.to('#sL .in', { x, y, duration: .035 }, t0 + 1.27 + i * .04));
  tl.set('#flash', { backgroundColor: '#ff3b30' }, t0 + 1.27).fromTo('#flash', { opacity: .55 }, { opacity: 0, duration: .25 }, t0 + 1.27);
  // pass card
  const cardB = h(`<div class="glass" id="l-b" style="left:110px;top:360px;width:860px;height:900px;border-radius:70px;background:linear-gradient(150deg,rgba(255,110,5,.7),rgba(255,110,5,.2))"><div class="abs mono center" style="top:70px;font-size:44px;letter-spacing:.4em;font-weight:700">SCORE</div><div class="abs big center" style="top:150px;font-size:430px;line-height:1;letter-spacing:-.04em">75+</div><div class="abs center" style="top:700px;display:flex;justify-content:center"><svg width="120" height="120" viewBox="0 0 120 120"><circle cx="60" cy="60" r="52" fill="#fff"/><path id="l-ck" d="M34 62 L54 82 L88 40" fill="none" stroke="#FF6E05" stroke-width="12" stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="100" stroke-dashoffset="100"/></svg></div></div>`, s);
  const tb = t0 + 4 * BEAT - .05;
  tl.to([cardA, stamp], { x: -1300, rotation: -12, opacity: 0, duration: .35, ease: E.in }, tb);
  tl.fromTo(cardB, { x: 1300, rotation: 10, opacity: 0 }, { x: 0, rotation: 0, opacity: 1, duration: .4, ease: E.snap }, tb + .06);
  tl.to('#l-ck', { strokeDashoffset: 0, duration: .35, ease: 'power2.out' }, tb + .45);
  const nx = h(`<div class="abs big center" style="top:1330px;font-size:112px;white-space:nowrap">NO <span class="or">EXCEPTIONS.</span></div>`, s);
  tl.fromTo(nx, { scale: 2.6, opacity: 0 }, { scale: 1, opacity: 1, duration: .28, ease: E.snap }, tb + .3);
})();

/* ===== M · brief in → video out (45–48.75) ===== */
(() => {
  const s = $('#sM .in'); const t0 = T(96);
  const items = [['BRIEF', '✎', 'WHAT YOU WANT'], ['CODE', '</>', 'CLAUDE WRITES IT'], ['RENDER', '▶▶', 'EVERY FRAME'], ['VIDEO', '●', 'READY TO POST']];
  const ts = [.1, .55, 1.0, 1.4];
  items.forEach(([a, ic, sub], i) => {
    const y = 240 + i * 215;
    const c = h(`<div class="glass" style="left:110px;top:${y}px;width:860px;height:170px;border-radius:56px"><div class="abs mono" style="left:44px;top:42px;font-size:62px;font-weight:700;color:#FF6E05">${ic}</div><div class="abs big" style="left:240px;top:34px;font-size:78px;line-height:1">${a}</div><div class="abs mono" style="left:242px;top:118px;font-size:24px;letter-spacing:.22em;color:rgba(255,255,255,.65)">${sub}</div><div class="abs" style="right:44px;top:60px;width:50px;height:50px;border-radius:50%;background:#FF6E05;display:flex;align-items:center;justify-content:center;color:#000;font-weight:900;font-size:28px;opacity:0" class="ok">✓</div></div>`, s);
    tl.fromTo(c, { x: 1200, opacity: 0, scale: .9 }, { x: 0, opacity: 1, scale: 1, duration: .38, ease: E.snap }, t0 + ts[i] - .1);
    if (i < 3) { const cn = h(`<div class="abs" style="left:${540 - 3}px;top:${y + 170}px;width:6px;height:45px;background:#FF6E05;border-radius:3px;transform-origin:50% 0"></div>`, s); tl.fromTo(cn, { scaleY: 0 }, { scaleY: 1, duration: .2, ease: 'power2.out' }, t0 + ts[i] + .3); }
  });
  const hrs = h(`<div class="abs big center or" style="top:1110px;font-size:230px;line-height:1;white-space:nowrap">HOURS,</div>`, s);
  const nw = h(`<div class="abs big center" style="top:1330px;font-size:150px;line-height:1;white-space:nowrap;position:absolute">NOT <span id="m-weeks" style="position:relative;display:inline-block">WEEKS<i id="m-strike" style="position:absolute;left:-10px;right:-10px;top:50%;height:16px;background:#ff3b30;border-radius:8px;transform-origin:0 50%;transform:scaleX(0)"></i></span></div>`, s);
  tl.fromTo(hrs, { scale: 2.8, opacity: 0, y: 60 }, { scale: 1, opacity: 1, y: 0, duration: .3, ease: E.snap }, t0 + 2.0);
  tl.fromTo(nw, { x: 1100, opacity: 0 }, { x: 0, opacity: 1, duration: .32, ease: E.snap }, t0 + 2.4);
  tl.to('#m-strike', { scaleX: 1, duration: .2, ease: 'power3.out' }, t0 + 2.95);
  tl.to('#m-weeks', { opacity: .45, duration: .2 }, t0 + 2.95);
})();
