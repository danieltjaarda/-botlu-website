// Gedeeld door de homepage en /ontwikkelaars: de WebGL-hulpjes en de chromen linten.
// Gewoon script (geen module): stageGL, stageLoop en metal zijn daarna overal te gebruiken.
// Bij 'minder beweging' (stil) tekenen de lussen één stilstaand beeld.
const stil = matchMedia('(prefers-reduced-motion: reduce)').matches;

// Eén driehoek over het hele canvas met een fragment-shader erop; null als de
// browser het niet kan. Geeft de uniforms terug onder hun eigen naam.
function stageGL(canvas, fs, names) {
  const gl = canvas.getContext('webgl', { alpha: true, premultipliedAlpha: true, antialias: false, powerPreference: 'low-power' });
  if (!gl) return null;
  const compile = (type, src) => { const sh = gl.createShader(type); gl.shaderSource(sh, src); gl.compileShader(sh); return sh; };
  const prog = gl.createProgram();
  gl.attachShader(prog, compile(gl.VERTEX_SHADER, 'attribute vec2 p;void main(){gl_Position=vec4(p,0.,1.);}'));
  gl.attachShader(prog, compile(gl.FRAGMENT_SHADER, fs));
  gl.linkProgram(prog);
  if (!gl.getProgramParameter(prog, gl.LINK_STATUS)) return null;
  gl.useProgram(prog);
  gl.bindBuffer(gl.ARRAY_BUFFER, gl.createBuffer());
  gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([-1, -1, 3, -1, -1, 3]), gl.STATIC_DRAW);
  gl.enableVertexAttribArray(0);
  gl.vertexAttribPointer(0, 2, gl.FLOAT, false, 0, 0);
  return { gl, u: Object.fromEntries(names.map(n => [n, gl.getUniformLocation(prog, n)])) };
}

// Tekenlus die alleen loopt als het canvas te zien is. step(dt, now) tekent een
// beeld en zegt of er nog iets beweegt (bij 'minder beweging' stopt hij dan).
// Geeft kick() terug om hem weer te starten.
function stageLoop(canvas, step) {
  let visible = true, raf = 0, last = 0;
  const frame = now => {
    const dt = last ? Math.min(.05, (now - last) / 1000) : 0;
    last = now;
    const busy = step(dt, now);
    raf = visible && !document.hidden && (!stil || busy) ? requestAnimationFrame(frame) : 0;
    if (!raf) last = 0;
  };
  const kick = () => { if (!raf) raf = requestAnimationFrame(frame); };
  new IntersectionObserver(([e]) => { visible = e.isIntersecting; if (visible) kick(); }).observe(canvas);
  document.addEventListener('visibilitychange', () => { if (!document.hidden && visible) kick(); });
  addEventListener('resize', () => kick());
  kick();
  return kick;
}

// ---------- Chromen linten (hero en ontwikkelaars) ----------
// Shader overgenomen van de ShaderMetal-component (blauw getint chroom, 3 linten): geborstelde,
// gedraaide stroken die een fotostudio weerspiegelen, met zachte schaduwen op een
// doorzichtig canvas. Ze reageren hier niet op de muis.
// In plaats van de vaste kanteling van het origineel lopen ze hier langs de lijn
// van midden boven naar rechtsonder (u_center en u_tilt, uitgerekend bij elke maat),
// en op een smal scherm schalen ze met de breedte in plaats van de hoogte (u_scale).
const METAL_FS = `precision highp float;

uniform vec2 u_resolution;
uniform float u_time;
uniform float u_count;
uniform float u_iridescence;
uniform float u_pull;
uniform float u_dark;
uniform vec2 u_mouse;
uniform vec2 u_light;
uniform vec3 u_f0;
uniform vec2 u_center;
uniform float u_tilt;
uniform float u_scale;

const float TAU = 6.28318530718;

float hash(vec2 p) {
  vec3 p3 = fract(vec3(p.xyx) * 0.1031);
  p3 += dot(p3, p3.yzx + 33.33);
  return fract((p3.x + p3.y) * p3.z);
}

// Smooth 1D value noise, for the brushed grain that runs along each ribbon.
float lines(float x, float seed) {
  float i = floor(x);
  float f = fract(x);
  f = f * f * (3.0 - 2.0 * f);
  return mix(hash(vec2(i, seed)), hash(vec2(i + 1.0, seed)), f);
}

vec2 rotate(vec2 p, float a) {
  float c = cos(a);
  float s = sin(a);
  return vec2(c * p.x - s * p.y, s * p.x + c * p.y);
}

// The spine of ribbon k: three swells at different speeds, so it never
// settles into a loop. Near the pointer it leans toward it.
float spine(float x, float k, float lane, float t, vec2 m) {
  float y = lane;
  y += 0.13 * sin(1.15 * x + 0.55 * t + 2.1 * k);
  y += 0.06 * sin(2.6 * x - 0.8 * t + 1.3 * k + 0.7);
  y += 0.025 * sin(5.3 * x + 1.3 * t + 4.0 * k);
  float near = exp(-(x - m.x) * (x - m.x) * 5.0);
  y += (m.y - y) * 0.22 * u_pull * near;
  return y;
}

// A studio to reflect: sky and floor meet at a crisp horizon, a big
// softbox overhead, two strip lights and the key light. Linear light.
vec3 studio(vec3 r, float t) {
  float a = 0.28 * sin(t * 0.11);
  r.xz = rotate(r.xz, a);
  float y = r.y;

  vec3 top = mix(vec3(0.82, 0.83, 0.86), vec3(0.025, 0.025, 0.028), u_dark);
  vec3 horizon = mix(vec3(1.0), vec3(0.16, 0.16, 0.17), u_dark);
  vec3 ground = mix(vec3(0.05, 0.05, 0.055), vec3(0.004), u_dark);
  vec3 sky = mix(horizon, top, smoothstep(0.0, 0.85, y));
  vec3 floor_ = mix(ground * 2.4, ground, smoothstep(0.0, -0.5, y));
  vec3 c = mix(floor_, sky, smoothstep(-0.025, 0.025, y));

  // Overhead softbox, feathered.
  float box = smoothstep(0.6, 0.45, abs(r.x)) * smoothstep(0.42, 0.55, y) *
              smoothstep(1.0, 0.85, y);
  c += box * mix(1.6, 2.2, u_dark);

  // Tall strip lights left and right: warm and cool, faintly.
  float stripL = smoothstep(0.1, 0.03, abs(r.x + 0.78)) * smoothstep(-0.35, -0.1, y) * smoothstep(0.8, 0.5, y);
  float stripR = smoothstep(0.08, 0.02, abs(r.x - 0.72)) * smoothstep(-0.3, -0.05, y) * smoothstep(0.75, 0.45, y);
  c += stripL * vec3(1.25, 1.1, 0.95) * mix(1.0, 1.5, u_dark);
  c += stripR * vec3(0.9, 1.05, 1.3) * mix(0.8, 1.3, u_dark);

  // A low bounce card, so the undersides aren't dead.
  float card = smoothstep(0.7, 0.2, abs(r.x)) * smoothstep(-0.95, -0.7, y) * smoothstep(-0.4, -0.65, y);
  c += card * mix(0.35, 0.18, u_dark);
  return c;
}

vec3 tonemap(vec3 x) {
  x = max(x, 0.0);
  return clamp((x * (2.51 * x + 0.03)) / (x * (2.43 * x + 0.59) + 0.14), 0.0, 1.0);
}

vec3 linearToSrgb(vec3 c) {
  c = clamp(c, 0.0, 1.0);
  vec3 lo = c * 12.92;
  vec3 hi = 1.055 * pow(c, vec3(1.0 / 2.4)) - 0.055;
  return mix(lo, hi, step(vec3(0.0031308), c));
}

void main() {
  vec2 frag = gl_FragCoord.xy;
  float px = 1.0 / u_scale;
  vec2 p = rotate((frag - u_center) * px, u_tilt);
  vec2 m = rotate((u_mouse * u_resolution - u_center) * px, u_tilt);
  float t = u_time;

  vec3 L = normalize(vec3(u_light, 0.85));
  float count = u_count;
  float spread = mix(0.0, 0.3, clamp((count - 1.0) / 4.0, 0.0, 1.0)) + 0.08 * step(1.5, count);
  float baseWidth = mix(0.13, 0.075, clamp((count - 1.0) / 4.0, 0.0, 1.0));

  // Premultiplied, composited back to front.
  vec3 col = vec3(0.0);
  float alpha = 0.0;

  for (int i = 0; i < 5; i++) {
    float k = float(i);
    if (k >= count) break;
    float f = count > 1.0 ? k / (count - 1.0) : 0.5;
    float lane = (f - 0.5) * spread;
    // Farther ribbons drift a touch slower: a hint of depth.
    float tk = t * mix(0.82, 1.0, f);

    float x = p.x;
    float e = 0.004;
    float c = spine(x, k, lane, tk, m);
    float slope = (spine(x + e, k, lane, tk, m) - spine(x - e, k, lane, tk, m)) / (2.0 * e);
    float stretch = inversesqrt(1.0 + slope * slope);
    float d = (p.y - c) * stretch;

    // Twist along the length; width breathes.
    float theta = 1.5 * x + 0.45 * tk + 1.7 * k + 0.55 * sin(0.7 * x - 0.3 * tk + k);
    float ct = cos(theta);
    float st = sin(theta);
    float hw = baseWidth * (0.82 + 0.22 * sin(0.9 * x + 0.35 * tk + 2.3 * k));
    // Seen edge-on a ribbon still has a little thickness.
    float proj = hw * max(abs(ct), 0.035);

    // Soft contact shadow on whatever is behind, before the ribbon lands.
    float sd = d + 0.045;
    float shadowW = proj + 0.05;
    float shadow = (1.0 - smoothstep(0.35, 1.0, abs(sd) / shadowW)) * mix(0.2, 0.32, u_dark);
    col *= 1.0 - shadow;
    alpha = alpha + shadow * (1.0 - alpha);

    float v = d / (ct >= 0.0 ? proj : -proj);
    float aa = 1.2 * px / proj;
    float cover = 1.0 - smoothstep(1.0 - aa, 1.0 + aa, abs(v));
    if (cover <= 0.0) continue;

    // Ribbon frame: T along, N2 across in the screen plane, Z toward us.
    vec3 T = normalize(vec3(1.0, slope, 0.0));
    vec3 N2 = normalize(vec3(-slope, 1.0, 0.0));
    vec3 B = ct * N2 + st * vec3(0.0, 0.0, 1.0);
    vec3 n = -st * N2 + ct * vec3(0.0, 0.0, 1.0);

    // A shallow arc across the width, rolling over at the edges, plus
    // slow ripples running down the length and a brushed grain.
    float roll = v * 0.45 + v * v * v * 0.5;
    float ripple = sin(x * 13.0 - tk * 2.2 + k * 3.1) * 0.03 + sin(x * 31.0 + tk * 1.3 + k) * 0.0075;  // half zo diep als het origineel: rustiger glans
    float grain = lines(v * 34.0 + k * 17.0, k) - 0.5;
    n = normalize(n + B * (roll + grain * 0.015) + T * ripple);
    // Edge-on, what shows is the strip's polished edge. It faces us, tipped
    // up a little so it catches the sky rather than sitting on the horizon.
    float edge = smoothstep(0.14, 0.03, abs(ct));
    vec3 rim = B * (st >= 0.0 ? 1.0 : -1.0) + vec3(0.0, 0.2, 0.0);
    n = normalize(mix(n, normalize(rim), edge));
    float back = step(n.z, 0.0);
    n *= 1.0 - 2.0 * back;

    vec3 r = reflect(vec3(0.0, 0.0, -1.0), n);
    vec3 env = studio(r, t);

    float facing = clamp(n.z, 0.0, 1.0);
    vec3 F = u_f0 + (1.0 - u_f0) * pow(1.0 - facing, 5.0);

    // Thin film: thickness drifts along the ribbon, and the colour shifts
    // with the viewing angle, strongest on the turns.
    float film = 0.5 + 0.5 * sin(x * 1.6 + v * 0.9 + tk * 0.35 + k * 1.9);
    vec3 rainbow = 0.5 + 0.5 * cos(TAU * (film * 1.6 + facing * 1.1 + vec3(0.0, 0.33, 0.67)));
    // Keep the film's brightness level, so it tints the metal, never dims it.
    rainbow = 0.2 + 0.8 * rainbow;
    rainbow /= max(dot(rainbow, vec3(0.2126, 0.7152, 0.0722)), 0.2);
    float sheen = u_iridescence * (0.45 + 0.55 * (1.0 - facing));
    F *= mix(vec3(1.0), rainbow, sheen);

    float rl = max(dot(r, L), 0.0);
    float spec = pow(rl, 90.0) * 5.0 + pow(rl, 14.0) * 0.55;

    vec3 lit = env * F + spec * F;
    lit *= mix(1.0, 0.72, back) * (0.94 + grain * 0.12);
    lit *= mix(0.86, 1.0, f);
    vec3 rgb = linearToSrgb(tonemap(lit * 1.05));

    col = col * (1.0 - cover) + rgb * cover;
    alpha = alpha * (1.0 - cover) + cover;
  }

  // A hair of dither, so the long gradients never band. Faint shadows
  // need it on alpha too, or they step into contour lines.
  float dither = (hash(frag + fract(t) * 91.0) - 0.5) / 255.0;
  col += dither * alpha;
  alpha = clamp(alpha + dither * step(0.0005, alpha) * 1.5, 0.0, 1.0);
  gl_FragColor = vec4(clamp(col, 0.0, 1.0), alpha);
}`;

// tint: kleur van het metaal (hex), glans: hoeveel regenboog (0–1). Standaard het blauwe chroom.
function metal(canvas, { dark = false, tint = 'bce8f6', glans = .2 } = {}) {
  const G = stageGL(canvas, METAL_FS, ['u_resolution', 'u_time', 'u_count', 'u_iridescence', 'u_pull', 'u_dark', 'u_mouse', 'u_light', 'u_f0', 'u_center', 'u_tilt', 'u_scale']);
  if (!G) return;                                                    // zonder WebGL blijft alleen de zachte gloed
  const { gl, u } = G;
  // De tint als lineaire RGB, 3 linten, wat regenboogglans
  gl.uniform3fv(u.u_f0, [0, 2, 4].map(i => ((parseInt(tint.slice(i, i + 2), 16) / 255 + .055) / 1.055) ** 2.4));
  gl.uniform1f(u.u_dark, dark ? 1 : 0);                            // licht of donker studiolicht
  gl.uniform1f(u.u_count, 3);
  gl.uniform1f(u.u_iridescence, glans);
  // Scherp aan de randen, dus op schermresolutie (tot 2x), maar nooit meer dan 2,4 miljoen pixels
  const size = () => {
    const w = canvas.clientWidth, h = canvas.clientHeight;
    const r = Math.min(devicePixelRatio || 1, 2, Math.sqrt(2.4e6 / (w * h)));
    const W = Math.max(1, Math.floor(w * r)), H = Math.max(1, Math.floor(h * r));
    if (canvas.width === W && canvas.height === H) return;
    canvas.width = W; canvas.height = H;
    gl.viewport(0, 0, W, H);
    gl.uniform2f(u.u_resolution, W, H);
    // De lijn van midden boven (W/2, H) naar rechtsonder (W, 0); het midden ervan is het draaipunt
    gl.uniform2f(u.u_center, .75 * W, .5 * H);
    gl.uniform1f(u.u_tilt, Math.atan2(H, W / 2));
    // Maat van de linten: de hoogte, zoals het origineel, maar op een smal scherm de breedte
    gl.uniform1f(u.u_scale, Math.min(H, W * 1.1));
  };
  // Reageert niet op de muis (interactive: false): licht vast linksboven, linten buigen niet mee
  gl.uniform1f(u.u_pull, 0);
  gl.uniform2f(u.u_mouse, .5, .5);
  gl.uniform2f(u.u_light, -.45, .55);
  let clock = 0;
  stageLoop(canvas, dt => {
    size();
    if (!stil) clock += dt;
    gl.uniform1f(u.u_time, clock * .025 * 3 + 11);                // speed 0,025: 12x rustiger dan het origineel (0,3)
    gl.drawArrays(gl.TRIANGLES, 0, 3);
    return false;                                                  // bij 'minder beweging' blijft het één stilstaand beeld
  });
}

