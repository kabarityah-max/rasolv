/* helpers shared by all scenes — everything here is a pure function of time (seek-safe) */
const BEAT = 60 / 128, T = b => b * BEAT;
const SCN = [0, 8, 16, 24, 28, 32, 40, 48, 56, 64, 72, 80, 88, 96, 104, 116, 128];   // scene starts, in beats
const $ = (s, p = document) => p.querySelector(s);
const $$ = (s, p = document) => [...p.querySelectorAll(s)];
function h(html, parent) { const d = document.createElement('div'); d.innerHTML = html.trim(); const e = d.firstElementChild; if (parent) parent.appendChild(e); return e; }
function mulberry(a) { return () => { a |= 0; a = a + 0x6D2B79F5 | 0; let t = Math.imul(a ^ a >>> 15, 1 | a); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; }; }
const R = mulberry(7);
const tl = gsap.timeline({ paused: true });
const E = { out: 'power3.out', in: 'power3.in', io: 'power3.inOut', back: 'back.out(1.7)', expo: 'expo.out', snap: 'power4.out' };
/* per-frame function driven by a tween: fn(p) with p in 0..1 */
function drive(t, dur, fn, ease = 'none') { const o = { p: 0 }; tl.to(o, { p: 1, duration: dur, ease, onUpdate: () => fn(o.p) }, t); }
function ap(host, opts) { host.innerHTML = `<svg viewBox="-100 -100 200 200" width="100%" height="100%" style="overflow:visible">${aperture(opts)}</svg>`; }
function chars(el, cls = 'ch') { const txt = el.textContent; el.textContent = ''; return [...txt].map(c => { const s = document.createElement('span'); s.className = cls; s.style.display = 'inline-block'; s.innerHTML = c === ' ' ? '&nbsp;' : c; el.appendChild(s); return s; }); }
/* scene transitions: scene `i` becomes visible at beat SCN[i]; the transition plays from cut-0.2s to cut+0.15s */
function enter(id, type, o = {}) {
  const i = +document.getElementById(id).dataset.i, t = T(SCN[i]) - 0.2, d = o.d || 0.36, inn = $('#' + id + ' .in');
  const x = o.x ?? 540, y = o.y ?? 960;
  if (type === 'zoom') tl.fromTo(inn, { scale: o.s || 1.5, opacity: 0, filter: 'blur(26px)' }, { scale: 1, opacity: 1, filter: 'blur(0px)', duration: d, ease: E.out }, t);
  else if (type === 'zoomout') tl.fromTo(inn, { scale: 0.55, opacity: 0, filter: 'blur(18px)' }, { scale: 1, opacity: 1, filter: 'blur(0px)', duration: d, ease: E.out }, t);
  else if (type === 'iris') tl.fromTo(inn, { clipPath: `circle(0px at ${x}px ${y}px)` }, { clipPath: `circle(1800px at ${x}px ${y}px)`, duration: d + 0.1, ease: 'power2.in' }, t);
  else if (type === 'slice') tl.fromTo(inn, { clipPath: 'polygon(0 0,0 0,-40% 100%,-40% 100%)' }, { clipPath: 'polygon(0 0,140% 0,100% 100%,-40% 100%)', duration: d, ease: E.io }, t);
  else if (type === 'up') tl.fromTo(inn, { clipPath: 'inset(100% 0 0 0)' }, { clipPath: 'inset(0% 0 0 0)', duration: d, ease: E.io }, t);
  else if (type === 'down') tl.fromTo(inn, { clipPath: 'inset(0 0 100% 0)' }, { clipPath: 'inset(0 0 0% 0)', duration: d, ease: E.io }, t);
  else if (type === 'drop') tl.fromTo(inn, { y: -1920 }, { y: 0, duration: d + 0.1, ease: 'power4.out' }, t);
  else if (type === 'push') tl.fromTo(inn, { x: 1080 }, { x: 0, duration: d, ease: E.io }, t);
  else if (type === 'spin') tl.fromTo(inn, { rotation: -14, scale: 1.7, opacity: 0, filter: 'blur(20px)' }, { rotation: 0, scale: 1, opacity: 1, filter: 'blur(0px)', duration: d + 0.05, ease: E.out }, t);
  else if (type === 'glass') {      /* liquid-glass panel sweeps across, scene swaps underneath it */
    tl.set(inn, { opacity: 0 }, 0).set(inn, { opacity: 1 }, t + 0.22);
    tl.fromTo('#sweep', { x: -1500, opacity: 1, rotation: 0 }, { x: 1500, duration: 0.55, ease: 'power2.inOut', rotation: 4 }, t);
    tl.set('#sweep', { opacity: 0 }, t + 0.58);
  }
  if (o.flash !== false) { const f = o.flashColor || '#fff'; tl.set('#flash', { backgroundColor: f }, t + 0.1).fromTo('#flash', { opacity: o.fa ?? 0.85 }, { opacity: 0, duration: 0.22, ease: 'power2.out' }, t + 0.1); }
  /* outgoing scene: push away */
  if (i > 0) { const prev = $('#' + document.querySelectorAll('.scene')[i - 1].id + ' .in'); tl.to(prev, { scale: o.pscale || 0.92, filter: 'blur(8px)', duration: d + 0.1, ease: 'power2.in' }, t); }
}
function glass(cls = '') { return `class="glass ${cls}"`; }
const ORANGE = '#FF6E05', ORANGE2 = '#FFA24A', WARM = '#F4EFE9';
