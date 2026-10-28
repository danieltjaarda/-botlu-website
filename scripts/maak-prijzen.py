# Bouwt prijzen.html (draai: python3 -I scripts/maak-prijzen.py): de basis (kleuren, navigatie, knoppen, footer)
# komt uit index.html, zodat alle pagina's hetzelfde ogen. Opnieuw draaien overschrijft de pagina.
# Achter de plannen dezelfde chromen linten als in de hero, hier in parelmoer.
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
css_cta = ''.join(l for l in between('  /* ---------- Afsluiter ---------- */', '  /* ---------- Kleinere schermen ---------- */').splitlines(True)
                  if '.visual' not in l and '.ring-stage' not in l)
css_stil = between('  @media (prefers-reduced-motion: reduce) {', '</style>')
nav = between('<header class="nav" id="nav">', '</header>', incl_end=True)
footer = between('<footer>', '</footer>', incl_end=True)

# Links van de homepage naar /, en Prijzen naar deze pagina
nav = re.sub(r'href="#([\w-]+)"', r'href="/#\1"', nav); footer = re.sub(r'href="#([\w-]+)"', r'href="/#\1"', footer)
nav = nav.replace('href="/prijzen"', 'href="/prijzen" aria-current="page"')

ARROW = '<svg class="arrow" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 8h10M9 4l4 4-4 4"/></svg>'
VINK = '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M3 8.5l3.2 3.2L13 5"/></svg>'
KRUIS = '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" aria-hidden="true"><path d="M4.5 4.5l7 7M11.5 4.5l-7 7"/></svg>'
INFO = '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.3" stroke-linecap="round" aria-hidden="true"><circle cx="8" cy="8" r="6.2"/><path d="M8 7.3v3.6M8 5.1v.01"/></svg>'
# Iconen in de tabs: gewoon zwart, zonder vlak (stijlregel van Daniel)
TAB = {
  'bel': '<path d="M6.6 3.5h2.6l1.6 4-2 1.3a11 11 0 0 0 5.4 5.4l1.3-2 4 1.6v2.6a2 2 0 0 1-2.2 2A16.5 16.5 0 0 1 4.6 5.7a2 2 0 0 1 2-2.2z"/>',
  'whatsapp': '<path d="M20 11.5a7.5 7.5 0 0 1-11 6.6L4.5 19.5l1.4-4.3A7.5 7.5 0 1 1 20 11.5z"/>',
  'mail': '<rect x="3.5" y="5.5" width="17" height="13" rx="2.5"/><path d="M4 7l8 6 8-6"/>',
}
def tab_icon(n): return f'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{TAB[n]}</svg>'

def wissel(jaar, maand):
    """Tekst die meeverandert met maandelijks/jaarlijks; jaarlijks staat standaard aan."""
    return f'<span data-jaar="{html.escape(jaar)}" data-maand="{html.escape(maand)}">{html.escape(jaar)}</span>'

def info(tip): return f'<span class="info" tabindex="0" role="note" aria-label="{html.escape(tip)}" data-tip="{html.escape(tip)}">{INFO}</span>'

def punt(tekst, klein='', tip='', nee=False):
    return (f'<li{" class=nee" if nee else ""}>{KRUIS if nee else VINK}<span>{tekst}'
            f'{f" <small>{klein}</small>" if klein else ""}{info(tip) if tip else ""}</span></li>')

# Plannen: naam, voor wie, prijs per maand (jaarlijks, maandelijks), badge, knop, inbegrepen, functies
PLANNEN = [
  dict(naam='Solo', voor='Voor 1 tot 20 gesprekken per dag', jaar=99, maand=119, knop=('Nu starten', 'https://app.botlu.ai/login#aanmaken', 'zwart'),
       inbegrepen=[punt('1.000 minuten', wissel('€0,10 per minuut', '€0,12 per minuut'), 'Alle gesprekstijd van je assistenten samen, per maand.'),
                   punt('Geen gesprekken tegelijk', nee=True),
                   punt('1 telefoonnummer', '€9 per extra nummer'),
                   punt('<b class="oneindig">∞</b> assistenten')],
       functies=[punt('12 Nederlandse stemmen'),
                 punt('5 talen', tip='Nederlands, Engels, Duits, Frans en Spaans.'),
                 punt('Agenda en afspraken', tip='Je assistent plant afspraken in en verzet ze. Ze verschijnen vanzelf in Google Agenda, Outlook of Apple Agenda.'),
                 punt('Opnames en samenvattingen')]),
  dict(naam='Team', voor='Voor 20 tot 100 gesprekken per dag', jaar=299, maand=359, pop=True, knop=('Nu starten', 'https://app.botlu.ai/login#aanmaken', 'brand'),
       inbegrepen=[punt('3.600 minuten', wissel('€0,08 per minuut', '€0,10 per minuut'), 'Alle gesprekstijd van je assistenten samen, per maand.'),
                   punt('3 gesprekken tegelijk', tip='Zoveel bellers kan je assistent tegelijk te woord staan.'),
                   punt('3 telefoonnummers', '€9 per extra nummer'),
                   punt('<b class="oneindig">∞</b> assistenten')],
       functies=[punt('Alles in <span class="plan-chip">Solo</span>'),
                 punt('Koppelingen', tip='Shopify, WooCommerce, Slack, Discord, Notion, Airtable, Make, n8n en meer.'),
                 punt('API en webhooks', tip='Haal gesprekken op via de API en krijg een bericht bij elk gesprek, elke afspraak en elk terugbelverzoek.')]),
  dict(naam='Scale', voor='Vanaf 100 gesprekken per dag', jaar=539, maand=599, vanaf=True, badge='Prijs op maat', knop=('Plan maken', '/#demo', 'zwart'),
       inbegrepen=[punt('Vanaf 6.000 minuten', tip='We stemmen het aantal minuten af op hoeveel er bij jou gebeld wordt.'),
                   punt('Gesprekken tegelijk op maat'),
                   punt('Telefoonnummers op maat'),
                   punt('<b class="oneindig">∞</b> assistenten')],
       functies=[punt('Alles in <span class="plan-chip">Team</span>'),
                 punt('Eigen stem', tip='Een stem die klinkt als jij of als je merk.'),
                 punt('Eigen bewaartermijn', tip='Jij bepaalt hoe lang we opnames en transcripten bewaren.'),
                 punt('Vaste contactpersoon')]),
]

def plan(p, i):
    tekst, href, kleur = p['knop']
    badge = (f'<span class="badge">{p["badge"]}</span>' if p.get('badge')
             else f'<span class="badge alleen-jaar">Bespaar €{p["maand"] - p["jaar"]}</span>')
    return f'''        <article class="plan rv{" pop" if p.get("pop") else ""}" style="--d:{i * .06:.2f}s">
          {'<span class="pop-label">Populair</span>' if p.get('pop') else ''}
          <h3>{p['naam']}</h3>
          <p class="voor">{p['voor']}</p>
          <div class="prijs">{'<span class="vanaf">Vanaf</span>' if p.get('vanaf') else ''}<b>{wissel(f"€{p['jaar']}", f"€{p['maand']}")}</b>{badge}</div>
          <p class="per">Per maand, {wissel('jaarlijks gefactureerd', 'maandelijks gefactureerd')}</p>
          <a class="btn {kleur}" href="{href}">{tekst}</a>
          <h4>Inbegrepen</h4>
          <ul>{''.join(p['inbegrepen'])}</ul>
          <h4>Functies</h4>
          <ul>{''.join(p['functies'])}</ul>
        </article>'''

plannen = '\n'.join(plan(p, i) for i, p in enumerate(PLANNEN))

page = f'''<!doctype html>
<html lang="nl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Prijzen · Botlu.ai</title>
<meta name="description" content="De prijzen van Botlu: een AI-assistent die je telefoon opneemt, vanaf €99 per maand. Solo, Team of Scale, maandelijks of jaarlijks.">
{head_links}
<script>document.documentElement.classList.add('js');</script>
<style>
{css_base}{css_h1}{css_secties}{css_cta}
  /* ---------- Prijzen ---------- */
  .nav-links a[aria-current] {{ opacity: 1; font-weight: 600; }}
  .prijzen {{ position: relative; isolation: isolate; padding: 150px 0 70px; overflow-x: clip; }}
  /* Parelmoer gloed en linten achter de kop en de bovenkant van de plannen */
  .prijs-gloed {{ position: absolute; inset: 0 0 auto; height: 900px; z-index: -3; overflow: hidden; pointer-events: none;
    -webkit-mask-image: linear-gradient(#000 55%, transparent); mask-image: linear-gradient(#000 55%, transparent); }}
  .prijs-gloed::before {{ content: ""; position: absolute; inset: -20%;
    background: radial-gradient(36% 40% at 16% 14%, rgba(222,210,250,.7), transparent 70%),
                radial-gradient(32% 38% at 84% 10%, rgba(255,214,234,.5), transparent 70%),
                radial-gradient(40% 42% at 78% 70%, rgba(204,226,252,.6), transparent 70%),
                radial-gradient(34% 40% at 28% 72%, rgba(236,226,252,.6), transparent 70%);
    animation: glow 22s ease-in-out infinite alternate; }}
  @keyframes glow {{ to {{ transform: translate3d(4%, -3%, 0) rotate(6deg) scale(1.06); }} }}
  .prijs-metal {{ position: absolute; inset: 0 0 auto; height: 900px; z-index: -1; overflow: hidden; pointer-events: none;
    -webkit-mask-image: linear-gradient(rgba(0,0,0,.18), #000 130px, #000 60%, transparent); mask-image: linear-gradient(rgba(0,0,0,.18), #000 130px, #000 60%, transparent); }}
  .prijs-metal canvas {{ position: absolute; inset: 0; width: 100%; height: 100%; display: block; }}
  .prijs-kop {{ position: relative; max-width: 760px; margin: 0 auto 48px; text-align: center; }}
  /* Zachte witte waas achter de kop: de linten vervagen onder de tekst */
  .prijs-kop::before {{ content: ""; position: absolute; inset: -55% -22%; z-index: -1; pointer-events: none;
    background: radial-gradient(closest-side, rgba(255,255,255,.96) 58%, rgba(255,255,255,0)); }}
  .prijs-kop h1 {{ font-size: clamp(40px, 5.4vw, 68px); }}
  .prijs-kop h1 .mute {{ display: block; color: var(--ink-4); }}

  /* Product en facturering */
  .keuzes {{ display: flex; align-items: center; justify-content: space-between; gap: 16px; margin-bottom: 20px; }}
  .schakel {{ display: flex; gap: 4px; padding: 5px; border-radius: var(--r-md); background: rgba(244,244,246,.82);
    backdrop-filter: blur(16px) saturate(1.4); -webkit-backdrop-filter: blur(16px) saturate(1.4); box-shadow: 0 0 0 1px rgba(16,16,24,.05); }}
  .schakel button {{ display: inline-flex; align-items: center; gap: 8px; height: 40px; padding: 0 16px; border: 0; border-radius: 9px; background: none;
    color: var(--ink-3); font-size: 15px; font-weight: 500; white-space: nowrap; cursor: pointer; transition: background .2s, color .2s, box-shadow .2s; }}
  .schakel button:hover:not(:disabled) {{ color: var(--ink); }}
  .schakel button.on {{ background: #fff; color: var(--ink); box-shadow: 0 1px 2px rgba(16,16,24,.08), 0 0 0 1px rgba(16,16,24,.04); }}
  .schakel button:disabled {{ cursor: default; }}
  .schakel svg {{ width: 19px; height: 19px; color: currentColor; }}
  .schakel em {{ padding: 2px 8px; border-radius: 99px; background: var(--brand-soft); color: var(--brand-ink); font-size: 11.5px; font-style: normal; font-weight: 600; }}
  .periode em {{ padding: 0; background: none; font-size: 15px; font-weight: 500; }}

  /* De plannen */
  .plannen {{ display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 20px; align-items: stretch; }}
  .plan {{ position: relative; display: flex; flex-direction: column; padding: 34px 32px 36px; border-radius: var(--r-xl); background: rgba(255,255,255,.9);
    backdrop-filter: blur(18px) saturate(1.3); -webkit-backdrop-filter: blur(18px) saturate(1.3); box-shadow: 0 0 0 1px var(--line-2), 0 20px 50px -30px rgba(16,16,24,.25); }}
  .plan.pop {{ box-shadow: 0 0 0 1.5px var(--brand), 0 28px 60px -26px rgba(33,179,224,.55); }}
  .pop-label {{ position: absolute; top: 22px; right: 22px; padding: 5px 11px; border-radius: 8px; background: var(--brand); color: #fff; font-size: 11.5px; font-weight: 700; letter-spacing: .08em; text-transform: uppercase; }}
  .plan h3 {{ margin: 0; font-size: 26px; font-weight: 560; letter-spacing: -.02em; }}
  .voor {{ margin: 6px 0 0; color: var(--ink-3); font-size: 16.5px; }}
  .prijs {{ display: flex; flex-wrap: wrap; align-items: center; gap: 4px 12px; margin-top: 44px; }}
  .prijs b {{ font-size: 46px; line-height: 1; font-weight: 560; letter-spacing: -.04em; font-variant-numeric: tabular-nums; }}
  .vanaf {{ align-self: flex-end; margin-right: -4px; color: var(--ink-3); font-size: 16px; }}
  .badge {{ padding: 4px 10px; border-radius: 8px; box-shadow: inset 0 0 0 1px rgba(33,179,224,.4); color: var(--brand-ink); font-size: 13.5px; font-weight: 500; }}
  .maandelijks .alleen-jaar {{ display: none; }}
  .per {{ margin: 12px 0 0; color: var(--ink-3); font-size: 15.5px; }}
  .plan .btn {{ width: 100%; height: 54px; margin: 32px 0 30px; font-size: 16px; }}
  .btn.zwart {{ background: var(--ink); color: #fff; box-shadow: inset 0 1px 0 rgba(255,255,255,.14), 0 8px 20px -10px rgba(16,16,24,.6); }}
  .btn.zwart:hover {{ background: #26262c; }}
  .plan h4 {{ margin: 0 0 14px; padding-top: 0; font-size: 17px; font-weight: 600; letter-spacing: -.01em; }}
  .plan .btn + h4 {{ padding-top: 30px; border-top: 1px solid var(--line); }}
  .plan ul {{ display: grid; gap: 12px; margin: 0 0 30px; padding: 0; list-style: none; }}
  .plan ul:last-child {{ margin-bottom: 0; }}
  .plan li {{ display: flex; align-items: flex-start; gap: 11px; font-size: 16px; line-height: 1.4; }}
  .plan li > svg {{ width: 17px; height: 17px; flex: none; margin-top: 2px; color: var(--brand); }}
  .plan li small {{ color: var(--ink-3); font-size: 14px; white-space: nowrap; }}
  .plan li.nee {{ color: var(--ink-4); }}
  .plan li.nee > svg {{ color: var(--ink-4); }}
  .oneindig {{ font-weight: 600; }}
  .plan-chip {{ margin-left: 2px; padding: 2px 8px; border-radius: 7px; background: var(--soft); font-weight: 600; }}
  /* Uitleg bij een rondje met een i: verschijnt bij hover of focus */
  .info {{ position: relative; display: inline-flex; vertical-align: -2px; margin-left: 6px; color: var(--ink-4); cursor: help; }}
  .info svg {{ width: 15px; height: 15px; }}
  .info:hover, .info:focus-visible {{ color: var(--ink-2); }}
  .info::after {{ content: attr(data-tip); position: absolute; bottom: calc(100% + 10px); left: 50%; z-index: 5; width: max-content; max-width: 240px; padding: 10px 12px;
    border-radius: 10px; background: var(--ink); color: #fff; font-size: 13.5px; font-weight: 400; line-height: 1.45; text-align: left;
    opacity: 0; visibility: hidden; transform: translate(-50%, 4px); transition: opacity .2s var(--ease), transform .25s var(--ease), visibility 0s .25s; pointer-events: none; }}
  .info:hover::after, .info:focus-visible::after {{ opacity: 1; visibility: visible; transform: translate(-50%, 0); transition-delay: 0s; }}
  /* Afsluiter met een foto van iemand die je spreekt, rechts tot aan de rand */
  .cta-box {{ display: grid; grid-template-columns: minmax(0, 1fr) minmax(0, .8fr); gap: 40px; align-items: center; min-height: 460px; padding-right: 0; padding-block: 0; }}
  .cta-box .cta-copy {{ padding: 80px 0; }}
  .cta-foto {{ position: relative; align-self: stretch; margin: 0; }}
  .cta-foto img {{ position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; object-position: 50% 18%;
    -webkit-mask-image: linear-gradient(90deg, transparent, #000 22%); mask-image: linear-gradient(90deg, transparent, #000 22%); }}
  .cta-foto figcaption {{ position: absolute; left: 18%; bottom: 28px; display: flex; align-items: center; gap: 9px; padding: 10px 16px; border-radius: 99px;
    background: rgba(255,255,255,.82); backdrop-filter: blur(14px) saturate(1.4); -webkit-backdrop-filter: blur(14px) saturate(1.4);
    box-shadow: 0 10px 30px -12px rgba(16,16,24,.35), 0 0 0 1px rgba(16,16,24,.05); font-size: 14.5px; font-weight: 600; white-space: nowrap; }}
  .cta-foto i {{ width: 8px; height: 8px; border-radius: 50%; background: var(--good); box-shadow: 0 0 0 4px var(--good-soft); }}
  .btw {{ margin: 28px 0 0; color: var(--ink-3); font-size: 15px; text-align: center; }}

  footer {{ padding: 40px 0 56px; border-top: 1px solid var(--line); color: var(--ink-3); font-size: 14px; }}
  footer .wrap {{ display: flex; flex-wrap: wrap; align-items: center; gap: 20px 32px; }}
  footer nav {{ display: flex; flex-wrap: wrap; gap: 6px 22px; margin-left: auto; }}
  footer a {{ text-decoration: none; }}
  footer a:hover {{ color: var(--ink); }}
  .js .rv {{ opacity: 0; transform: translateY(26px); transition: opacity .9s var(--ease), transform .9s var(--ease); transition-delay: var(--d, 0s); }}
  .js .rv.in {{ opacity: 1; transform: none; }}

  @media (max-width: 1060px) {{
    .plannen {{ grid-template-columns: minmax(0, 1fr); max-width: 560px; margin: 0 auto; }}
    .keuzes {{ flex-direction: column; }}
  }}
  @media (max-width: 900px) {{
    .nav-links {{ display: none; }}
    .nav .wrap {{ gap: 12px; }}
    .nav .btn.sm {{ padding: 0 13px; }}
    .prijzen {{ padding-top: 120px; }}
    .prijs-metal {{ opacity: .5; }}
  }}
  @media (max-width: 700px) {{
    .producten button:disabled {{ display: none; }}                 /* op mobiel alleen wat er nu is */
    .plan {{ padding: 28px 22px 30px; }}
    .prijs b {{ font-size: 42px; }}
    .info::after {{ left: auto; right: -8px; transform: translateY(4px); }}
    .info:hover::after, .info:focus-visible::after {{ transform: none; }}
    .cta-box {{ grid-template-columns: minmax(0, 1fr); gap: 0; padding: 0; }}
    .cta-box .cta-copy {{ padding: 8px 24px 48px; }}
    .cta-foto {{ order: -1; height: 320px; }}
    .cta-foto img {{ -webkit-mask-image: linear-gradient(#000 70%, transparent); mask-image: linear-gradient(#000 70%, transparent); }}
    .cta-foto figcaption {{ left: 24px; bottom: 36px; }}
    footer nav {{ margin-left: 0; }}
  }}
{css_stil}</style>
</head>
<body>

{nav}

<main>
  <!-- ========== Prijzen ========== -->
  <section class="prijzen">
    <div class="prijs-gloed" aria-hidden="true"></div>
    <div class="prijs-metal" aria-hidden="true"><canvas></canvas></div>
    <div class="wrap">
      <div class="prijs-kop">
        <h1 class="rv">Eenvoudige prijzen. <span class="mute">Geen verrassingen.</span></h1>
      </div>
      <div class="keuzes rv" style="--d:.1s">
        <div class="schakel producten" role="group" aria-label="Product">
          <button class="on" type="button" aria-pressed="true">{tab_icon('bel')}AI bel-assistent</button>
          <button type="button" disabled>{tab_icon('whatsapp')}AI WhatsApp-assistent <em>Binnenkort</em></button>
          <button type="button" disabled>{tab_icon('mail')}AI mail-assistent <em>Binnenkort</em></button>
        </div>
        <div class="schakel periode" role="group" aria-label="Facturering">
          <button type="button" data-p="maand" aria-pressed="false">Maandelijks</button>
          <button class="on" type="button" data-p="jaar" aria-pressed="true">Jaarlijks <em>−17%</em></button>
        </div>
      </div>
      <div class="plannen">
{plannen}
      </div>
      <p class="btw rv">Alle prijzen zijn per maand en exclusief btw. Minuten op? Dan komen er automatisch 100 minuten bij voor €15.</p>
    </div>
  </section>

  <!-- ========== Afsluiter ========== -->
  <section class="cta-sec">
    <div class="wrap">
      <div class="cta-box rv">
        <div class="cta-copy">
          <h2>Twijfel je welk plan past?</h2>
          <p>Boek een demo. We kijken samen hoeveel er bij je gebeld wordt en wat je assistent moet kunnen.</p>
          <div class="cta">
            <a class="btn dark" href="/#demo">Demo boeken {ARROW}</a>
            <a class="btn line" href="https://app.botlu.ai/login#aanmaken">Account aanmaken</a>
          </div>
        </div>
        <figure class="cta-foto">
          <img src="/media/medewerker.jpg" alt="Een medewerker van Botlu met een headset, in gesprek" width="820" height="1230" loading="lazy" decoding="async">
          <figcaption><i aria-hidden="true"></i>Gratis en vrijblijvend</figcaption>
        </figure>
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

// Maandelijks of jaarlijks: prijzen en teksten wisselen mee
document.querySelectorAll('.periode button').forEach(b => b.addEventListener('click', () => {{
  const p = b.dataset.p;
  document.querySelectorAll('.periode button').forEach(x => {{ x.classList.toggle('on', x === b); x.setAttribute('aria-pressed', x === b); }});
  document.querySelectorAll('[data-jaar]').forEach(el => el.textContent = el.dataset[p]);
  document.documentElement.classList.toggle('maandelijks', p === 'maand');
}}));

// Verschijnen bij scrollen
const io = new IntersectionObserver(es => es.forEach(e => {{ if (e.isIntersecting) {{ e.target.classList.add('in'); io.unobserve(e.target); }} }}), {{ rootMargin: '0px 0px -8% 0px' }});
document.querySelectorAll('.rv').forEach(el => io.observe(el));

$('#year').textContent = new Date().getFullYear();
// De chromen linten uit de hero van de homepage, hier in parelmoer
metal($('.prijs-metal canvas'), {{ tint: 'ddd2f8', glans: .55 }});
</script>
</body>
</html>
'''
(SITE / 'prijzen.html').write_text(page)
print('geschreven:', len(page), 'tekens')
