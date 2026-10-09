const clamp = (x, a = 0, b = 1) => Math.min(b, Math.max(a, x));
function aperture({ r = 37, rot = 0, bp = 1, grow = 1, color = '#FF6E05', gap = '#000', R = 80, lines = true } = {}) {
  const P = (a, rad) => [rad * Math.cos(a * Math.PI / 180), rad * Math.sin(a * Math.PI / 180)];
  const O = [...Array(6)].map((_, i) => P(-90 + 60 * i, R));
  const I = [...Array(6)].map((_, i) => P(-60 + 60 * i + rot, Math.max(r, 0.01)));
  const ang = q => (Math.atan2(q[1], q[0]) * 180 / Math.PI + 360) % 360;
  const hit = (p, d) => {
    let best = null;
    for (let k = 0; k < 6; k++) {
      const a = O[k], b = O[(k + 1) % 6], e = [b[0] - a[0], b[1] - a[1]];
      const den = d[0] * e[1] - d[1] * e[0]; if (Math.abs(den) < 1e-9) continue;
      const t = ((a[0] - p[0]) * e[1] - (a[1] - p[1]) * e[0]) / den;
      const u = ((a[0] - p[0]) * d[1] - (a[1] - p[1]) * d[0]) / den;
      if (t > 1e-6 && u >= -1e-6 && u <= 1 + 1e-6 && (!best || t < best.t)) best = { t, q: [p[0] + t * d[0], p[1] + t * d[1]] };
    }
    return best.q;
  };
  const Pt = I.map((q, i) => { const pr = I[(i + 5) % 6]; return hit(q, [q[0] - pr[0], q[1] - pr[1]]); });
  const f = q => q[0].toFixed(2) + ',' + q[1].toFixed(2);
  let blades = '', seps = '';
  for (let i = 0; i < 6; i++) {
    const j = (i + 1) % 6, a0 = ang(Pt[i]), span = (ang(Pt[j]) - a0 + 360) % 360;
    const mids = O.filter(v => { const d = (ang(v) - a0 + 360) % 360; return d > 1e-3 && d < span - 1e-3; })
                  .sort((u, v) => ((ang(v) - a0 + 360) % 360) - ((ang(u) - a0 + 360) % 360));
    const poly = [I[i], I[j], Pt[j], ...mids, Pt[i]];
    const c = poly.reduce((m, q) => [m[0] + q[0] / poly.length, m[1] + q[1] / poly.length], [0, 0]);
    const g = 0.6 + 0.4 * clamp(grow * 1.6 - i * 0.12);
    const o = clamp(grow * 2 - i * 0.18);
    blades += `<polygon points="${poly.map(f).join(' ')}" fill="${color}" opacity="${o}" transform="translate(${f(c)}) scale(${g}) translate(${f([-c[0], -c[1]])})"/>`;
    seps += `<line x1="${f(I[i]).replace(',', '" y1="')}" x2="${f(Pt[i]).replace(',', '" y2="')}" stroke="${gap}" stroke-width="4.2" stroke-linecap="square"/>`;
    if (lines && (i === 0 || i === 3)) {
      const s0 = [I[i][0] + (I[j][0] - I[i][0]) * 0.55, I[i][1] + (I[j][1] - I[i][1]) * 0.55];
      const d = [Pt[i][0] - I[i][0], Pt[i][1] - I[i][1]];
      seps += `<line x1="${s0[0] + d[0] * 0.08}" y1="${s0[1] + d[1] * 0.08}" x2="${s0[0] + d[0] * 0.62}" y2="${s0[1] + d[1] * 0.62}" stroke="${gap}" stroke-width="3.6"/>`;
    }
    if (lines && (i === 1 || i === 4))
      seps += `<line x1="${f(I[j]).replace(',', '" y1="')}" x2="${f(O[(i + 2) % 6]).replace(',', '" y2="')}" stroke="${gap}" stroke-width="0.9"/>`;
  }
  let bpS = '';
  if (bp > 0) {
    for (let k = 0; k < 6; k++) {
      const a = O[k], b = O[(k + 1) % 6], e = [b[0] - a[0], b[1] - a[1]], L = Math.hypot(...e);
      const n = [e[1] / L, -e[0] / L]; const off = 13; const kk = clamp(bp * 1.4 - k * 0.07);
      const a1 = [a[0] + n[0] * off + e[0] * 0.08, a[1] + n[1] * off + e[1] * 0.08];
      const b1 = [a1[0] + e[0] * 0.84 * kk, a1[1] + e[1] * 0.84 * kk];
      const tick = (q, s) => `<line x1="${q[0] - n[0] * 4 * s}" y1="${q[1] - n[1] * 4 * s}" x2="${q[0] + n[0] * 4 * s}" y2="${q[1] + n[1] * 4 * s}"/>`;
      bpS += `<line x1="${f(a1).replace(',', '" y1="')}" x2="${f(b1).replace(',', '" y2="')}"/>` + tick(a1, kk) + tick(b1, kk);
      const ra = P(-90 + 60 * k, R + 6), rb = P(-90 + 60 * k, R + 6 + 12 * kk);
      bpS += `<line x1="${f(ra).replace(',', '" y1="')}" x2="${f(rb).replace(',', '" y2="')}"/>`;
    }
    bpS = `<g stroke="${color}" stroke-width="1.3" fill="none" opacity="${clamp(bp * 3)}">${bpS}</g>`;
  }
  return bpS + `<g>${blades}${seps}</g>`;
}
