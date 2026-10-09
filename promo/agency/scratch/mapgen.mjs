// Pre-computes map geometry (deterministic, offline) -> assets/map.js
import fs from 'fs';
import { geoEqualEarth, geoPath, geoContains, geoGraticule10, geoCentroid } from 'd3-geo';
import { feature, mesh } from 'topojson-client';
const rd = f => JSON.parse(fs.readFileSync(new URL('../node_modules/world-atlas/' + f, import.meta.url)));
const W = 2400, H = 1200;
const proj = geoEqualEarth().fitSize([W, H], { type: 'Sphere' });
const land110 = feature(rd('land-110m.json'), rd('land-110m.json').objects.land);
// dot-matrix land
const dots = []; const step = 15;
for (let y = step / 2; y < H; y += step) for (let x = step / 2; x < W; x += step) {
  const ll = proj.invert([x, y]); if (!ll) continue;
  if (geoContains(land110, ll)) dots.push([Math.round(x), Math.round(y)]);
}
// vector coast+borders at 50m
const t50 = rd('countries-50m.json');
const p = geoPath(proj).digits(1);
const land50 = p(feature(t50, t50.objects.land));
const borders = p(mesh(t50, t50.objects.countries, (a, b) => a !== b));
const grat = p(geoGraticule10());
const cities = {
  tangier: [-5.8, 35.76], london: [-0.12, 51.5], newyork: [-74, 40.7], dubai: [55.3, 25.2], saopaulo: [-46.6, -23.55],
  singapore: [103.8, 1.35], lagos: [3.4, 6.5], sydney: [151.2, -33.9], mexico: [-99.1, 19.4], tokyo: [139.7, 35.7], toronto: [-79.4, 43.65], paris: [2.35, 48.85], cairo: [31.2, 30.0], mumbai: [72.9, 19.1], la: [-118.2, 34.05]
};
const pts = {}; for (const [k, v] of Object.entries(cities)) pts[k] = proj(v).map(n => Math.round(n * 10) / 10);
fs.writeFileSync(new URL('../assets/map.js', import.meta.url),
  'window.MAP=' + JSON.stringify({ W, H, dots, land50, borders, grat, pts }) + ';');
console.log('dots', dots.length, 'land50', land50.length, 'borders', borders.length, pts.tangier, pts.london);
