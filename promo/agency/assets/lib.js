/* helpers shared by all scenes — everything here is a pure function of time (seek-safe) */
const BEAT = 60 / 128, T = b => b * BEAT;
const SCN = [0, 8, 16, 24, 28, 32, 44, 52, 60, 68, 76, 84, 92, 100, 112, 128];   // scene starts, in beats
const $ = (s, p = document) => p.querySelector(s);
const $$ = (s, p = document) => [...p.querySelectorAll(s)];
function h(html, parent) { const d = document.createElement('div'); d.innerHTML = html.trim(); const e = d.firstElementChild; if (parent) parent.appendChild(e); return e; }
const tl = gsap.timeline({ paused: true });
const E = { out: 'power3.out', in: 'power3.in', io: 'power3.inOut', back: 'back.out(1.5)', expo: 'expo.out', snap: 'power4.out' };
const ORANGE = '#FF6E05', ORANGE2 = '#FFA24A', WARM = '#F4EFE9';
const ease = (n, p) => gsap.parseEase(n)(Math.max(0, Math.min(1, p)));
/* per-frame function driven by a tween: fn(p) with p in 0..1 */
function drive(t, dur, fn, e = 'none') { const o = { p: 0 }; tl.to(o, { p: 1, duration: dur, ease: e, onUpdate: () => fn(o.p) }, t); }
function ap(host, opts) { host.innerHTML = `<svg viewBox="-100 -100 200 200" width="100%" height="100%" style="overflow:visible">${aperture(opts)}</svg>`; }
function chars(el, cls = 'ch') { const txt = el.textContent; el.textContent = ''; return [...txt].map(c => { const s = document.createElement('span'); s.className = cls; s.style.display = 'inline-block'; s.innerHTML = c === ' ' ? '&nbsp;' : c; el.appendChild(s); return s; }); }
/* premium text reveal: characters rise out of a blur */
function reveal(cs, t, o = {}) { tl.fromTo(cs, { y: o.y ?? 46, opacity: 0, filter: `blur(${o.blur ?? 16}px)`, scale: o.scale ?? 1.04 }, { y: 0, opacity: 1, filter: 'blur(0px)', scale: 1, duration: o.d ?? .5, ease: E.out, stagger: o.stagger ?? .028 }, t); }
/* svg tick ring: n ticks, every `major`-th longer */
function tickRing(r, n, len, major, col = 'rgba(244,239,233,.55)', w = 2) { let d = ''; for (let i = 0; i < n; i++) { const a = i / n * Math.PI * 2, L = i % major === 0 ? len * 2.2 : len; d += `M${(Math.cos(a) * r).toFixed(1)},${(Math.sin(a) * r).toFixed(1)}L${(Math.cos(a) * (r + L)).toFixed(1)},${(Math.sin(a) * (r + L)).toFixed(1)}`; } return `<path d="${d}" stroke="${col}" stroke-width="${w}" fill="none"/>`; }
/* scene transitions: scene `i` becomes visible at beat SCN[i]; the transition plays from cut-0.2s to cut+0.15s */
function enter(id, type, o = {}) {
  const sc = document.getElementById(id), i = +sc.dataset.i, t = T(SCN[i]) - 0.2, d = o.d || 0.36, inn = $('.in', sc);
  const x = o.x ?? 540, y = o.y ?? 960;
  if (type === 'zoom') tl.fromTo(inn, { scale: o.s || 1.5, opacity: 0, filter: 'blur(26px)' }, { scale: 1, opacity: 1, filter: 'blur(0px)', duration: d, ease: E.out }, t);
  else if (type === 'zoomout') tl.fromTo(inn, { scale: 0.55, opacity: 0, filter: 'blur(18px)' }, { scale: 1, opacity: 1, filter: 'blur(0px)', duration: d, ease: E.out }, t);
  else if (type === 'iris') tl.fromTo(inn, { clipPath: `circle(0px at ${x}px ${y}px)` }, { clipPath: `circle(1800px at ${x}px ${y}px)`, duration: d + 0.1, ease: 'power2.in' }, t);
  else if (type === 'slice') tl.fromTo(inn, { clipPath: 'polygon(0 0,0 0,-40% 100%,-40% 100%)' }, { clipPath: 'polygon(0 0,140% 0,100% 100%,-40% 100%)', duration: d, ease: E.io }, t);
  else if (type === 'up') tl.fromTo(inn, { clipPath: 'inset(100% 0 0 0)' }, { clipPath: 'inset(0% 0 0 0)', duration: d, ease: E.io }, t);
  else if (type === 'push') tl.fromTo(inn, { x: 1080 }, { x: 0, duration: d, ease: E.io }, t);
  else if (type === 'spin') tl.fromTo(inn, { rotation: -10, scale: 1.6, opacity: 0, filter: 'blur(20px)' }, { rotation: 0, scale: 1, opacity: 1, filter: 'blur(0px)', duration: d + 0.05, ease: E.out }, t);
  else if (type === 'glass') {      /* liquid-glass panel sweeps across, scene swaps underneath it */
    tl.set(inn, { opacity: 0 }, 0).set(inn, { opacity: 1 }, t + 0.22);
    tl.fromTo('#sweep', { x: -1500, opacity: 1, rotation: 0 }, { x: 1500, duration: 0.55, ease: 'power2.inOut', rotation: 4 }, t);
    tl.set('#sweep', { opacity: 0 }, t + 0.58);
  } else if (type === 'shutter') {  /* camera shutter: two plates close, swap, open */
    tl.set(inn, { opacity: 0 }, 0).set(inn, { opacity: 1 }, t + 0.2);
    tl.fromTo('#shT', { y: -960 }, { y: 0, duration: .2, ease: 'power3.in' }, t).fromTo('#shB', { y: 960 }, { y: 0, duration: .2, ease: 'power3.in' }, t);
    tl.to('#shT', { y: -960, duration: .26, ease: 'power3.out' }, t + .24).to('#shB', { y: 960, duration: .26, ease: 'power3.out' }, t + .24);
  }
  if (o.flash) { const f = o.flashColor || ORANGE; tl.set('#flash', { backgroundColor: f }, t + 0.12).fromTo('#flash', { opacity: o.flash }, { opacity: 0, duration: 0.24, ease: 'power2.out' }, t + 0.12); }
  if (i > 0 && type !== 'shutter' && type !== 'glass') { const prev = $('.in', document.querySelectorAll('.scene')[i - 1]); tl.to(prev, { scale: o.pscale || 0.94, filter: 'blur(8px)', duration: d + 0.1, ease: 'power2.in' }, t); }
}
