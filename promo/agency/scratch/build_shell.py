"""Builds index.html: static shell + 16 timed scene sections (times come from the beat grid) + script includes."""
BEAT = 60 / 128
SC = [0, 8, 16, 24, 28, 32, 44, 52, 60, 68, 76, 84, 92, 100, 112, 128]
IDS = list('ABCDEFGHIJKLMNO') + ['P']
IDS = ['sA','sB','sC','sD1','sD2','sE','sF','sG','sH','sI','sJ','sK','sL','sM','sO']
secs = ''
for i, id_ in enumerate(IDS):
    st = max(0, SC[i] * BEAT - 0.2); en = SC[i + 1] * BEAT + (0.3 if i < len(IDS) - 1 else 0)
    secs += f'    <section class="scene clip" id="{id_}" data-i="{i}" data-start="{st:.3f}" data-duration="{en - st:.3f}" data-track-index="{i % 3 + 1}"><div class="in"></div></section>\n'
css = open('scratch/style.css').read()
html = f'''<!doctype html>
<html lang="en" data-resolution="portrait">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=1080, height=1920" />
<script src="assets/gsap.min.js"></script>
<style>
{css}
</style>
</head>
<body>
<svg width="0" height="0" style="position:absolute">
  <defs>
    <filter id="refract" x="-10%" y="-10%" width="120%" height="120%">
      <feTurbulence type="fractalNoise" baseFrequency="0.012 0.018" numOctaves="2" seed="4" result="n"/>
      <feDisplacementMap in="SourceGraphic" in2="n" scale="38" xChannelSelector="R" yChannelSelector="G"/>
    </filter>
    <filter id="grainf"><feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="2" seed="3"/><feColorMatrix type="saturate" values="0"/></filter>
  </defs>
</svg>
<div id="root" data-composition-id="main" data-start="0" data-duration="60" data-width="1080" data-height="1920">
  <div id="bg" class="clip" data-start="0" data-duration="60" data-track-index="0">
    <div class="blob b1"></div><div class="blob b2"></div><div class="blob b3"></div>
  </div>
{secs}  <div id="grid" class="clip" data-start="0" data-duration="60" data-track-index="0"></div>
  <div id="grain" class="clip" data-start="0" data-duration="60" data-track-index="5"><svg width="1080" height="1920"><rect width="1080" height="1920" filter="url(#grainf)"/></svg></div>
  <div id="sweepw" class="clip" data-start="0" data-duration="60" data-track-index="6"><div id="sweep" class="glass"></div></div>
  <div id="shw" class="clip" data-start="0" data-duration="60" data-track-index="6" style="position:absolute;inset:0;z-index:36;pointer-events:none"><div id="shT"></div><div id="shB"></div></div>
  <div id="flash" class="clip" data-start="0" data-duration="60" data-track-index="7"></div>
  <div id="hud" class="clip" data-start="0" data-duration="60" data-track-index="8"></div>
  <div id="hdr" class="clip" data-start="0" data-duration="60" data-track-index="8"></div>
  <div id="caps" class="clip" data-start="0" data-duration="60" data-track-index="9"></div>
  <div id="foot" class="clip" data-start="0" data-duration="60" data-track-index="8">CREATED BY CLAUDE CODE  ·  RENDERED WITH HYPERFRAMES</div>
  <div id="prog" class="clip" data-start="0" data-duration="60" data-track-index="8"><i></i></div>
  <audio id="mix" src="assets/mix.wav" data-start="0" data-duration="60" data-track-index="10" data-volume="1"></audio>
</div>
<script src="assets/map.js"></script>
<script src="assets/captions.js"></script>
<script src="assets/aperture.js"></script>
<script src="assets/lib.js"></script>
<script src="assets/s1.js"></script>
<script src="assets/s2.js"></script>
<script src="assets/s3.js"></script>
<script src="assets/s4.js"></script>
<script src="assets/s5.js"></script>
<script src="assets/main.js"></script>
<script>window.__timelines = window.__timelines || {{}}; window.__timelines["main"] = tl;</script>
</body>
</html>
'''
open('index.html', 'w').write(html)
print('index.html written')
