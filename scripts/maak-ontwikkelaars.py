# Bouwt ontwikkelaars.html (draai: python3 -I scripts/maak-ontwikkelaars.py): de basis (kleuren, navigatie, knoppen, footer, Terminal)
# komt uit index.html, zodat beide pagina's hetzelfde ogen. Opnieuw draaien overschrijft de pagina.
import html, pathlib, re

SITE = pathlib.Path.home() / 'botlu-website'
idx = (SITE / 'index.html').read_text()

def between(start, end, incl_end=False):
    a = idx.index(start); b = idx.index(end, a + len(start))
    return idx[a:b + (len(end) if incl_end else 0)]

head_links = between('<link rel="icon"', '\n<script>')
css_base = between('<style>\n', '  /* ---------- Hero met het lint ---------- */')[len('<style>\n'):]
css_h1 = re.search(r'\n(  h1 \{[^\n]*\})', idx).group(1) + '\n'
css_secties = between('  /* ---------- Secties ---------- */', '  /* Werkt met */')
# Opmaak van de donkere sectie en het Terminal-venster (staat sinds de expert-sectie niet meer in index.html)
css_devs = '''  /* ---------- Ontwikkelaars ---------- */
  .devs { background: var(--night); color: #fff; overflow: hidden; }
  /* Dezelfde chromen linten als in de hero, hier in de donkere studio, achter de inhoud */
  .sec-metal { position: absolute; inset: 0; z-index: 0; pointer-events: none; }
  .sec-metal canvas { position: absolute; inset: 0; width: 100%; height: 100%; display: block; }
  .devs > .wrap { position: relative; z-index: 1; }
  .devs .meer { margin-top: 30px; color: #fff; text-decoration-color: rgba(255,255,255,.4); }
  .devs .meer:hover { text-decoration-color: #fff; }
  .devs h2 .mute { color: rgba(255,255,255,.4); }
  .devs h2 { font-size: clamp(34px, 4vw, 50px); }
  .devs .sec-head p { color: rgba(255,255,255,.6); }
  .devs-grid { display: grid; grid-template-columns: .85fr 1.15fr; gap: 56px; align-items: start; }
  .dev-list { display: grid; gap: 26px; margin: 0; padding: 0; list-style: none; }
  .dev-list li { padding-left: 18px; border-left: 2px solid rgba(255,255,255,.12); }
  .dev-list b { display: block; margin-bottom: 4px; font-size: 17px; letter-spacing: -.015em; }
  .dev-list span { color: rgba(255,255,255,.58); font-size: 15px; }
  .dev-list code, .devs .sec-head code { padding: 1px 6px; border-radius: 6px; background: rgba(255,255,255,.08); font: 500 13.5px/1.4 ui-monospace, "SF Mono", Menlo, monospace; color: #d6d2ff; }
  /* Het codevoorbeeld als Terminal op de Mac: licht venster, profiel Basic (zwarte SF Mono op wit) */
  .term { overflow: hidden; border-radius: 12px; background: #fff; color: #000;
    box-shadow: 0 0 0 .5px rgba(0,0,0,.5), inset 0 0 0 .5px rgba(255,255,255,.35), 0 24px 70px 4px rgba(0,0,0,.55); }
  .term-bar { position: relative; display: flex; align-items: center; justify-content: center; height: 30px; background: #ececec; }
  .lights { position: absolute; left: 13px; top: 9px; display: flex; gap: 8px; }
  .lights i { width: 12px; height: 12px; border-radius: 50%; background: #ff5f57; box-shadow: inset 0 0 0 .5px #e0443e; }
  .lights i:nth-child(2) { background: #febc2e; box-shadow: inset 0 0 0 .5px #dea123; }
  .lights i:nth-child(3) { background: #28c840; box-shadow: inset 0 0 0 .5px #1aab29; }
  .term-title { max-width: 70%; overflow: hidden; color: #4d4d4d; font: 600 13px/1 -apple-system, BlinkMacSystemFont, "SF Pro Text", "Inter Variable", sans-serif; letter-spacing: -.01em; white-space: nowrap; text-overflow: ellipsis; }
  /* Tabbalk zoals in Terminal: tabs even breed, de actieve licht, de andere wat donkerder */
  .term-tabs { display: flex; background: #dadada; box-shadow: inset 0 1px 0 #cfcfcf, inset 0 -1px 0 #c8c8c8; }
  .term-tab { flex: 1; height: 26px; border: 0; border-left: 1px solid #c8c8c8; background: none; color: #6b6b6b; cursor: pointer;
    font: 500 12px/1 -apple-system, BlinkMacSystemFont, "SF Pro Text", "Inter Variable", sans-serif; transition: background .15s, color .15s; }
  .term-tab:first-child { border-left: 0; }
  .term-tab:hover { background: #d2d2d2; }
  .term-tab.on { background: #ececec; color: #262626; box-shadow: inset 0 -1px 0 #ececec; }
  .term pre { height: calc(22 * 1.45em + 20px); margin: 0; padding: 8px 10px 12px; overflow: auto; background: #fff; color: #000;
    font: 12.5px/1.45 "SF Mono", ui-monospace, Menlo, monospace; tab-size: 2; white-space: pre; }
  .term pre[hidden] { display: none; }
  .term .cur { display: inline-block; width: .6em; height: 1.15em; vertical-align: -.2em; background: rgba(0,0,0,.42); }

'''
css_cta = ''.join(l for l in between('  /* ---------- Afsluiter ---------- */', '  /* ---------- Kleinere schermen ---------- */').splitlines(True)
                  if '.visual' not in l and '.ring-stage' not in l)
css_stil = between('  @media (prefers-reduced-motion: reduce) {', '</style>')
nav = between('<header class="nav" id="nav">', '</header>', incl_end=True)
footer = between('<footer>', '</footer>', incl_end=True)

# Links van de homepage naar /, en Ontwikkelaars naar deze pagina
for sec in ['functies', 'stemmen', 'hoe', 'vragen', 'demo']:  # ook de knop Demo boeken
    nav = nav.replace(f'href="#{sec}"', f'href="/#{sec}"'); footer = footer.replace(f'href="#{sec}"', f'href="/#{sec}"')
nav = re.sub(r'href="[^"]*ontwikkelaars"', 'href="/ontwikkelaars" aria-current="page"', nav)
footer = re.sub(r'href="[^"]*ontwikkelaars"', 'href="/ontwikkelaars"', footer)

# ---------- Terminalvensters ----------
PROMPT = '\x00P'; CUR = '\x00C'
def sessie(tekst):
    """Platte terminaltekst naar HTML: prompt en cursor als spans, de rest ge-escaped."""
    t = html.escape(tekst, quote=False)
    return t.replace(PROMPT, '<span class="pr">jij@MacBook ~ %</span>').replace(CUR, '<span class="cur"></span>')

def terminal(tabs, title=None, cls=''):
    """tabs: lijst van (sleutel, label, venstertitel, tekst). Eén tab = geen tabbalk."""
    first = tabs[0]
    bar = (f'<div class="term-tabs" role="tablist">' + ''.join(
        f'<button class="term-tab{" on" if i == 0 else ""}" type="button" data-t="{k}" data-title="{html.escape(tt)}">{html.escape(lab)}</button>'
        for i, (k, lab, tt, _) in enumerate(tabs)) + '</div>') if len(tabs) > 1 else ''
    pres = ''.join(f'<pre data-p="{k}"{"" if i == 0 else " hidden"}>{sessie(txt)}</pre>' for i, (k, _, _, txt) in enumerate(tabs))
    return (f'<div class="term {cls}">\n  <div class="term-bar"><span class="lights" aria-hidden="true"><i></i><i></i><i></i></span>'
            f'<span class="term-title">{html.escape(title or first[2])}</span></div>\n  {bar}\n{pres}\n</div>')

LOGIN = 'Last login: Tue Oct 27 14:02:51 on ttys001\n'
CALL_ID = 'CA5d3f0e9b1c7a4e2f8d6b0a9c3e1f7d24'

HOOK = LOGIN + PROMPT + ''' node server.js
Botlu-webhooks: luistert op https://jouw-server.nl/botlu

POST /botlu  call.completed
{
  "id": "evt_6f1c0a9e2b7d4c3e8a51f0d2",
  "type": "call.completed",
  "created_at": "2026-10-27T14:03:18.000Z",
  "data": {
    "caller_name": "Sanne de Vries",
    "from": "+31612345678",
    "topic": "Lekke achterband",
    "summary": "Sanne komt morgen om 10:30 langs.",
    "outcome": "afspraak",
    "sentiment": 86,
    "duration_seconds": 74,
    "has_recording": true
  }
}
''' + CUR

LIJST = LOGIN + PROMPT + ''' curl "https://app.botlu.ai/api/v1/calls?limit=5" \\
>   -H "Authorization: Bearer $BOTLU_KEY"
{
  "data": [
    {
      "id": "''' + CALL_ID + '''",
      "started_at": "2026-10-27T14:01:58.000Z",
      "duration_seconds": 74,
      "agent": { "id": "k3f9x2a", "name": "Emma" },
      "caller_name": "Sanne de Vries",
      "topic": "Lekke achterband",
      "outcome": "afspraak",
      "has_recording": true
    }
  ],
  "has_more": true
}
''' + PROMPT + ' ' + CUR

GESPREK = PROMPT + ''' curl https://app.botlu.ai/api/v1/calls/''' + CALL_ID + ''' \\
>   -H "Authorization: Bearer $BOTLU_KEY"
{
  "id": "''' + CALL_ID + '''",
  "started_at": "2026-10-27T14:01:58.000Z",
  "duration_seconds": 74,
  "agent": { "id": "k3f9x2a", "name": "Emma" },
  "from": "+31612345678",
  "caller_name": "Sanne de Vries",
  "topic": "Lekke achterband",
  "summary": "Sanne komt morgen om 10:30 langs.",
  "outcome": "afspraak",
  "sentiment": 86,
  "has_recording": true,
  "transcript": [
    { "role": "assistant", "text": "Goedemiddag, je spreekt met Emma." },
    { "role": "caller", "text": "Hoi! Mijn achterband is lek." }
  ]
}
''' + PROMPT + ' ' + CUR

OPNAME = PROMPT + ''' curl -o gesprek.wav \\
>   https://app.botlu.ai/api/v1/calls/''' + CALL_ID + '''/recording \\
>   -H "Authorization: Bearer $BOTLU_KEY"
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100 1156k  100 1156k    0     0  2903k      0 --:--:-- --:--:-- --:--:-- 2905k
''' + PROMPT + ''' afplay gesprek.wav
''' + PROMPT + ' ' + CUR

AGENTS = PROMPT + ''' curl https://app.botlu.ai/api/v1/agents \\
>   -H "Authorization: Bearer $BOTLU_KEY"
{
  "data": [
    {
      "id": "k3f9x2a",
      "name": "Emma",
      "live": true,
      "voice": "emma",
      "language": "nl",
      "greeting": "Goedemiddag, je spreekt met Emma."
    }
  ]
}
''' + PROMPT + ' ' + CUR

CODE = LOGIN + PROMPT + ''' cat webhook.js
import crypto from 'node:crypto';

// Het geheim uit je dashboard (whsec_…), zonder het voorvoegsel
const key = Buffer.from(process.env.BOTLU_SECRET.slice(6), 'base64');

// body = de ruwe tekst van het verzoek, niet de geparste JSON
export function echtVanBotlu(headers, body) {
  const id = headers['webhook-id'], ts = headers['webhook-timestamp'];
  if (Math.abs(Date.now() / 1000 - ts) > 300) return false;
  const mac = crypto.createHmac('sha256', key)
    .update(`${id}.${ts}.${body}`).digest('base64');
  const verwacht = Buffer.from(`v1,${mac}`);
  return headers['webhook-signature'].split(' ').some(s => {
    const b = Buffer.from(s);
    return b.length === verwacht.length && crypto.timingSafeEqual(b, verwacht);
  });
}
''' + PROMPT + ' ' + CUR

hero_term = terminal([('hook', 'Webhook', 'jij — node server.js — 80×24', HOOK), ('api', 'API', 'jij — -zsh — 80×24', LIJST)])
api_term = terminal([('gesprek', 'Gesprek', 'jij — -zsh — 80×24', GESPREK), ('opname', 'Opname', 'jij — -zsh — 80×24', OPNAME),
                     ('agents', 'Assistenten', 'jij — -zsh — 80×24', AGENTS)], cls='op-wit')
code_term = terminal([('code', 'webhook.js', 'jij — -zsh — 80×24', CODE)], cls='op-wit')

ARROW = '<svg class="arrow" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 8h10M9 4l4 4-4 4"/></svg>'
def apps(*names): return ''.join(f'<img src="/apps/{n}.png" alt="" width="44" height="44" loading="lazy">' for n in names)
# Iconen: gewoon zwart, zonder vlak erachter (stijlregel van Daniel)
ICON = {
  'sleutel': '<path d="M15 7a4 4 0 1 1-3.9 4.9L4 19v-3h3v-3h3l.9-.9A4 4 0 0 1 15 7z"/><circle cx="15.5" cy="10.5" r="1"/>',
  'zegel': '<path d="M12 3l7 3v5c0 4.6-3 8.4-7 10-4-1.6-7-5.4-7-10V6l7-3z"/><path d="M8.5 12l2.5 2.5 4.5-5"/>',
  'slot': '<rect x="4.5" y="10.5" width="15" height="10" rx="2.5"/><path d="M8 10.5V7.5a4 4 0 0 1 8 0v3"/>',
  'klok': '<circle cx="12" cy="12" r="8.5"/><path d="M12 7.5V12l3 2"/>',
}
def icon(n): return f'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICON[n]}</svg>'
def velden(*v): return '<div class="velden">' + ''.join(f'<span>{x}</span>' for x in v) + '</div>'

page = f'''<!doctype html>
<html lang="nl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Ontwikkelaars · Botlu.ai</title>
<meta name="description" content="Koppel Botlu aan je eigen systemen: een REST-API voor gesprekken, transcripten en opnames, ondertekende webhooks bij elke gebeurtenis en een iCal-link voor je agenda.">
{head_links}
<script>document.documentElement.classList.add('js');</script>
<style>
{css_base}{css_h1}{css_secties}{css_devs}{css_cta}
  /* ---------- Pagina voor ontwikkelaars ---------- */
  /* Op de donkere hero: navigatie in wit tot je scrolt */
  .nav:not(.solid) {{ color: #fff; }}
  .nav:not(.solid) .nav-links a:hover {{ background: rgba(255,255,255,.1); }}
  .nav:not(.solid) .btn.sm {{ background: #fff; color: var(--ink); }}
  .nav:not(.solid) .btn.sm.demo {{ background: rgba(255,255,255,.08); border-color: rgba(255,255,255,.28); color: #fff; }}
  .nav:not(.solid) .btn.sm.demo:hover {{ background: rgba(255,255,255,.14); }}
  .nav-links a[aria-current] {{ opacity: 1; font-weight: 600; }}
  .dev-hero {{ padding: 150px 0 110px; }}
  .dev-hero h1 {{ font-size: clamp(38px, 4.4vw, 58px); line-height: 1.04; letter-spacing: -.04em; }}
  .dev-hero h1 .mute {{ color: rgba(255,255,255,.4); }}
  .dev-hero .devs-grid {{ align-items: center; }}
  /* Linten vervagen achter het menu, en een donkere waas achter de tekst links houdt wit leesbaar */
  .dev-hero .sec-metal {{ -webkit-mask-image: linear-gradient(rgba(0,0,0,.15), #000 160px); mask-image: linear-gradient(rgba(0,0,0,.15), #000 160px); }}
  .dev-hero .devs-grid > div:first-child {{ position: relative; }}
  .dev-hero .devs-grid > div:first-child::before {{ content: ""; position: absolute; inset: -14% -22% -14% -40%; z-index: -1; pointer-events: none;
    background: radial-gradient(closest-side, rgba(11,11,20,.9) 55%, rgba(11,11,20,0)); }}
  .dev-hero .dev-list {{ margin-top: 40px; }}
  .dev-hero .cta {{ display: flex; flex-wrap: wrap; gap: 12px; margin-top: 40px; }}
  .btn.wit {{ background: #fff; color: var(--ink); }}
  .btn.wit:hover {{ background: #e9e9f0; }}
  .btn.glas {{ background: rgba(255,255,255,.08); border-color: rgba(255,255,255,.2); color: #fff; }}
  .btn.glas:hover {{ background: rgba(255,255,255,.14); }}
  /* Terminal op een witte achtergrond: lichtere schaduw dan op de donkere hero */
  .term.op-wit {{ box-shadow: 0 0 0 .5px rgba(0,0,0,.28), 0 24px 56px -14px rgba(16,16,24,.38); }}
  .mono {{ font-family: "SF Mono", ui-monospace, Menlo, monospace; }}
  /* Stappen met grote lichte cijfers */
  .stappen {{ display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 18px; counter-reset: stap; }}
  .stap, .ev, .app {{ padding: 30px; border-radius: var(--r-2xl); background: var(--soft); }}
  .stap::before {{ content: counter(stap); counter-increment: stap; display: block; margin-bottom: 26px; color: var(--ink-4); font-size: 56px; line-height: 1; font-weight: 300; letter-spacing: -.04em; }}
  .stap p, .ev p, .app p {{ margin: 0; color: var(--ink-3); }}
  .chip {{ display: inline-block; margin-top: 20px; padding: 6px 10px; border-radius: 8px; background: #fff; box-shadow: 0 0 0 1px var(--line-2); color: var(--ink); font: 500 13px/1.3 "SF Mono", ui-monospace, Menlo, monospace; }}
  /* Gebeurtenissen */
  .events {{ display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 18px; }}
  .ev h3 {{ font: 600 17px/1.3 "SF Mono", ui-monospace, Menlo, monospace; letter-spacing: 0; }}
  .ev p {{ margin-bottom: 20px; }}
  .velden {{ display: flex; flex-wrap: wrap; gap: 6px; }}
  .velden span {{ padding: 4px 9px; border-radius: 7px; background: #fff; box-shadow: 0 0 0 1px var(--line-2); color: var(--ink-2); font: 12.5px/1.3 "SF Mono", ui-monospace, Menlo, monospace; }}
  .uitkomsten {{ margin: 26px 0 0; color: var(--ink-3); font-size: 15.5px; }}
  .uitkomsten code, .eplijst + p code, .headers code {{ padding: 2px 6px; border-radius: 6px; background: var(--soft); color: var(--ink); font: 500 13.5px/1.4 "SF Mono", ui-monospace, Menlo, monospace; }}
  /* API: endpoints links, Terminal rechts */
  .duo {{ display: grid; grid-template-columns: .9fr 1.1fr; gap: 56px; align-items: start; }}
  .basis {{ display: grid; gap: 14px; margin-bottom: 30px; }}
  .basis small {{ display: block; margin-bottom: 3px; color: var(--ink-4); font-size: 13px; font-weight: 500; }}
  .basis code {{ color: var(--ink); font: 500 15px/1.4 "SF Mono", ui-monospace, Menlo, monospace; }}
  .eplijst {{ margin: 0; padding: 0; list-style: none; border-top: 1px solid var(--line); }}
  .eplijst li {{ display: grid; grid-template-columns: 50px minmax(0, 1fr); gap: 4px 14px; padding: 16px 0; border-bottom: 1px solid var(--line); }}
  .eplijst .m {{ grid-row: span 2; align-self: start; padding: 3px 0; border-radius: 6px; background: var(--brand-soft); color: var(--brand); text-align: center; font: 600 12px/1.4 "SF Mono", ui-monospace, Menlo, monospace; }}
  .eplijst code {{ overflow-wrap: anywhere; color: var(--ink); font: 500 14.5px/1.4 "SF Mono", ui-monospace, Menlo, monospace; }}
  .eplijst span {{ color: var(--ink-3); font-size: 15px; }}
  .eplijst + p {{ margin: 22px 0 0; color: var(--ink-3); font-size: 15.5px; }}
  /* Handtekening: de drie headers */
  .headers {{ display: grid; gap: 22px; margin: 0; }}
  .headers div {{ padding-left: 18px; border-left: 2px solid var(--line-2); }}
  .headers dt {{ margin-bottom: 4px; color: var(--ink); font: 600 15px/1.4 "SF Mono", ui-monospace, Menlo, monospace; }}
  .headers dd {{ margin: 0; color: var(--ink-3); }}
  .headers + p {{ margin: 28px 0 0; color: var(--ink-3); }}
  .headers + p a {{ color: var(--brand); font-weight: 600; text-underline-offset: 4px; }}
  /* Zonder code: echte app-iconen */
  .apps {{ display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 18px; }}
  .app .ic {{ display: flex; gap: 8px; margin-bottom: 24px; }}
  .app .ic img {{ width: 44px; height: 44px; border-radius: 22.5%; box-shadow: 0 0 0 1px rgba(16,16,24,.06), 0 6px 14px -8px rgba(16,16,24,.35); }}
  .app .chip {{ display: block; width: fit-content; max-width: 100%; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }}
  /* Veilig: zwarte iconen zonder vlak */
  .veilig {{ display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 36px; }}
  .veilig svg {{ display: block; width: 28px; height: 28px; margin-bottom: 18px; color: var(--ink); }}
  .veilig p {{ margin: 0; color: var(--ink-3); font-size: 15.5px; }}
  .sec + .sec {{ padding-top: 0; }}

  footer {{ padding: 40px 0 56px; border-top: 1px solid var(--line); color: var(--ink-3); font-size: 14px; }}
  footer .wrap {{ display: flex; flex-wrap: wrap; align-items: center; gap: 20px 32px; }}
  footer nav {{ display: flex; flex-wrap: wrap; gap: 6px 22px; margin-left: auto; }}
  footer a {{ text-decoration: none; }}
  footer a:hover {{ color: var(--ink); }}
  .js .rv {{ opacity: 0; transform: translateY(26px); transition: opacity .9s var(--ease), transform .9s var(--ease); transition-delay: var(--d, 0s); }}
  .js .rv.in {{ opacity: 1; transform: none; }}

  @media (max-width: 1060px) {{
    .apps, .veilig {{ grid-template-columns: repeat(2, minmax(0, 1fr)); }}
  }}
  @media (max-width: 900px) {{
    .nav-links {{ display: none; }}
    .nav .wrap {{ gap: 12px; }}
    .nav .btn.sm {{ padding: 0 13px; }}
    .devs-grid, .duo {{ grid-template-columns: minmax(0, 1fr); gap: 40px; }}
    .stappen, .events {{ grid-template-columns: minmax(0, 1fr); }}
    .dev-hero {{ padding: 120px 0 84px; }}
    .sec-metal {{ opacity: .5; }}
  }}
  @media (max-width: 700px) {{
    .sec {{ padding: 84px 0; }}
    .apps, .veilig {{ grid-template-columns: minmax(0, 1fr); }}
    .stap, .ev, .app {{ padding: 24px; }}
    .cta-box {{ padding: 56px 24px; }}
    footer nav {{ margin-left: 0; }}
  }}
{css_stil}</style>
</head>
<body>

{nav}

<main>
  <!-- ========== Hero: koppel Botlu aan je eigen systemen ========== -->
  <section class="devs dev-hero">
    <div class="sec-metal" aria-hidden="true"><canvas></canvas></div>
    <div class="wrap">
      <div class="devs-grid">
        <div>
          <h1 class="rv">Koppel Botlu aan je eigen systemen. <span class="mute">Met een API en webhooks.</span></h1>
          <ul class="dev-list">
            <li class="rv" style="--d:.05s"><b>Webhooks bij elke gebeurtenis</b><span><code>call.completed</code>, <code>appointment.created</code>, <code>appointment.cancelled</code> en <code>callback.created</code>, ondertekend volgens Standard Webhooks.</span></li>
            <li class="rv" style="--d:.1s"><b>REST-API met sleutels</b><span>Haal gesprekken, transcripten, opnames, assistenten en nummers op met een <code>btl_</code>-sleutel.</span></li>
            <li class="rv" style="--d:.15s"><b>Agenda als iCal-link</b><span>Abonneer je op alle afspraken in je eigen agenda-app.</span></li>
          </ul>
          <div class="cta rv" style="--d:.2s">
            <a class="btn wit" href="https://app.botlu.ai/login#aanmaken">API-sleutel maken {ARROW}</a>
            <a class="btn glas" href="#api">Bekijk de endpoints</a>
          </div>
        </div>
        <div class="rv" style="--d:.1s">
{hero_term}
        </div>
      </div>
    </div>
  </section>

  <!-- ========== In drie stappen ========== -->
  <section class="sec" id="start">
    <div class="wrap">
      <div class="sec-head rv"><h2>In drie stappen gekoppeld. <span class="mute">Meestal binnen een kwartier.</span></h2></div>
      <div class="stappen">
        <div class="stap rv"><h3>Maak een API-sleutel</h3><p>In het dashboard onder API &amp; webhooks. Je ziet hem één keer; wij bewaren alleen een hash.</p><code class="chip">btl_…</code></div>
        <div class="stap rv" style="--d:.06s"><h3>Voeg je webhook toe</h3><p>Plak een https-adres en kies de gebeurtenissen. Je krijgt een geheim om elk bericht mee te controleren.</p><code class="chip">whsec_…</code></div>
        <div class="stap rv" style="--d:.12s"><h3>Controleer en bouw</h3><p>Check de handtekening, bewaar wat je nodig hebt en haal de rest op via de API.</p><code class="chip">webhook-signature: v1,…</code></div>
      </div>
    </div>
  </section>

  <!-- ========== Gebeurtenissen ========== -->
  <section class="sec" id="gebeurtenissen">
    <div class="wrap">
      <div class="sec-head rv"><h2>Vier gebeurtenissen. <span class="mute">Op het moment dat ze gebeuren.</span></h2></div>
      <div class="events">
        <div class="ev rv"><h3>call.completed</h3><p>Een gesprek is afgelopen en samengevat.</p>{velden('caller_name', 'from', 'topic', 'summary', 'outcome', 'sentiment', 'transcript', 'has_recording')}</div>
        <div class="ev rv" style="--d:.06s"><h3>appointment.created</h3><p>De assistent heeft een afspraak ingepland.</p>{velden('starts_at', 'ends_at', 'name', 'phone', 'email', 'reason', 'call_id')}</div>
        <div class="ev rv"><h3>appointment.cancelled</h3><p>Een afspraak is geannuleerd, door de beller of in het dashboard.</p>{velden('id', 'starts_at', 'name', 'status', 'call_id')}</div>
        <div class="ev rv" style="--d:.06s"><h3>callback.created</h3><p>Een beller wil teruggebeld worden.</p>{velden('name', 'phone', 'reason', 'call_id')}</div>
      </div>
      <p class="uitkomsten rv"><code>outcome</code> is altijd een van: <code>opgelost</code>, <code>afspraak</code>, <code>terugbellen</code>, <code>doorverbonden</code> of <code>opgehangen</code>.</p>
    </div>
  </section>

  <!-- ========== API ========== -->
  <section class="sec" id="api">
    <div class="wrap">
      <div class="sec-head rv"><h2>Eén API voor al je gesprekken. <span class="mute">Gewoon REST en JSON.</span></h2></div>
      <div class="duo">
        <div class="rv">
          <div class="basis">
            <div><small>Basis-URL</small><code>https://app.botlu.ai/api/v1</code></div>
            <div><small>Inloggen</small><code>Authorization: Bearer btl_…</code></div>
          </div>
          <ul class="eplijst">
            <li><span class="m">GET</span><code>/calls</code><span>Gesprekken, nieuwste eerst. Met <span class="mono">limit</span> (tot 100), <span class="mono">before</span> en <span class="mono">outcome</span>.</span></li>
            <li><span class="m">GET</span><code>/calls/{{id}}</code><span>Eén gesprek, met het hele transcript.</span></li>
            <li><span class="m">GET</span><code>/calls/{{id}}/recording</code><span>De opname als WAV-bestand.</span></li>
            <li><span class="m">GET</span><code>/agents</code><span>Je assistenten: naam, stem, taal en begroeting.</span></li>
            <li><span class="m">GET</span><code>/numbers</code><span>Je telefoonnummers en welke assistent opneemt.</span></li>
          </ul>
          <p>Gaat er iets mis, dan krijg je een gewone HTTP-status met <code>{{ "error": "…" }}</code> in gewone taal.</p>
        </div>
        <div class="rv" style="--d:.1s">
{api_term}
        </div>
      </div>
    </div>
  </section>

  <!-- ========== Handtekening ========== -->
  <section class="sec" id="handtekening">
    <div class="wrap">
      <div class="sec-head rv"><h2>Controleer elke webhook. <span class="mute">Dan weet je zeker dat hij van ons komt.</span></h2></div>
      <div class="duo">
        <div class="rv">
          <dl class="headers">
            <div><dt>webhook-id</dt><dd>Uniek per bericht. Heb je hem al gezien, sla hem dan over.</dd></div>
            <div><dt>webhook-timestamp</dt><dd>Wanneer we hem verstuurden, in Unix-tijd. Weiger berichten ouder dan vijf minuten.</dd></div>
            <div><dt>webhook-signature</dt><dd><code>v1,</code> met een HMAC-SHA256 over id, tijd en body, gemaakt met je <code>whsec_</code>-geheim.</dd></div>
          </dl>
          <p>Liever niets zelf schrijven? De bibliotheken van <a href="https://www.standardwebhooks.com" rel="noopener">Standard Webhooks</a> voor onder meer Node, Python, PHP en Go werken direct.</p>
        </div>
        <div class="rv" style="--d:.1s">
{code_term}
        </div>
      </div>
    </div>
  </section>

  <!-- ========== Zonder code ========== -->
  <section class="sec" id="zonder-code">
    <div class="wrap">
      <div class="sec-head rv"><h2>Liever zonder code? <span class="mute">Ook goed.</span></h2></div>
      <div class="apps">
        <div class="app rv"><div class="ic">{apps('make', 'n8n')}</div><h3>Make en n8n</h3><p>Plak de webhook-URL van je scenario in Botlu. Elk gesprek start dan je automatisering.</p></div>
        <div class="app rv" style="--d:.05s"><div class="ic">{apps('sheets')}</div><h3>Google Sheets</h3><p>Elk gesprek als nieuwe rij, met een klein script dat we voor je klaarzetten.</p></div>
        <div class="app rv" style="--d:.1s"><div class="ic">{apps('slack', 'teams', 'discord')}</div><h3>Slack, Teams en Discord</h3><p>Een bericht in je kanaal na elk gesprek, elke afspraak en elk terugbelverzoek.</p></div>
        <div class="app rv" style="--d:.15s"><div class="ic">{apps('google-agenda', 'outlook', 'apple-agenda')}</div><h3>Je eigen agenda</h3><p>Abonneer je op de geheime iCal-link; nieuwe afspraken verschijnen vanzelf.</p><code class="chip">…/api/agenda/••••.ics</code></div>
      </div>
    </div>
  </section>

  <!-- ========== Veilig ========== -->
  <section class="sec" id="veilig">
    <div class="wrap">
      <div class="sec-head rv"><h2>Veilig gebouwd. <span class="mute">Zonder dat jij er werk aan hebt.</span></h2></div>
      <div class="veilig">
        <div class="rv">{icon('sleutel')}<h3>Sleutels als hash</h3><p>We bewaren je API-sleutel niet zelf. Kwijt? Maak een nieuwe en trek de oude in.</p></div>
        <div class="rv" style="--d:.05s">{icon('zegel')}<h3>Elk bericht ondertekend</h3><p>HMAC-SHA256 volgens Standard Webhooks, met een eigen geheim per webhook.</p></div>
        <div class="rv" style="--d:.1s">{icon('slot')}<h3>Alleen https naar buiten</h3><p>Webhooks gaan alleen naar openbare https-adressen, nooit naar interne netwerken.</p></div>
        <div class="rv" style="--d:.15s">{icon('klok')}<h3>Snel of niet</h3><p>We wachten hooguit acht seconden op je server en volgen geen doorverwijzingen.</p></div>
      </div>
    </div>
  </section>

  <!-- ========== Afsluiter ========== -->
  <section class="cta-sec">
    <div class="wrap">
      <div class="cta-box rv">
        <div class="cta-copy">
          <h2>Klaar om te bouwen?</h2>
          <p>Maak een account, haal je sleutel op en ontvang vandaag nog je eerste webhook.</p>
          <div class="cta">
            <a class="btn dark" href="https://app.botlu.ai/login#aanmaken">Account aanmaken {ARROW}</a>
            <a class="btn line" href="https://app.botlu.ai/login">Inloggen</a>
          </div>
        </div>
      </div>
    </div>
  </section>
</main>

{footer}

<script src="/linten.js"></script>
<script>
const $ = s => document.querySelector(s);

// Navigatie krijgt een glazen achtergrond zodra je scrolt
const nav = $('#nav');
const solid = () => nav.classList.toggle('solid', scrollY > 40);
addEventListener('scroll', solid, {{ passive: true }});
solid();

// Tabs in de Terminal-vensters; de venstertitel volgt de tab
document.querySelectorAll('.term').forEach(term => {{
  const tabs = term.querySelector('.term-tabs');
  if (!tabs) return;
  tabs.addEventListener('click', e => {{
    const b = e.target.closest('.term-tab');
    if (!b) return;
    tabs.querySelectorAll('.term-tab').forEach(x => x.classList.toggle('on', x === b));
    term.querySelectorAll('pre[data-p]').forEach(p => p.hidden = p.dataset.p !== b.dataset.t);
    term.querySelector('.term-title').textContent = b.dataset.title;
  }});
}});

// Verschijnen bij scrollen
const io = new IntersectionObserver(es => es.forEach(e => {{ if (e.isIntersecting) {{ e.target.classList.add('in'); io.unobserve(e.target); }} }}), {{ rootMargin: '0px 0px -8% 0px' }});
document.querySelectorAll('.rv').forEach(el => io.observe(el));

$('#year').textContent = new Date().getFullYear();
// De chromen linten uit de hero van de homepage, in de donkere studio
metal($('.sec-metal canvas'), {{ dark: true }});
</script>
</body>
</html>
'''
(SITE / 'ontwikkelaars.html').write_text(page)
print('geschreven:', len(page), 'tekens')
