# Gedeelde regels voor de <head> van elke pagina: vaste link (canonical), Open Graph en
# Twitter-kaart, zodat zoekmachines en gedeelde links overal hetzelfde beeld krijgen.
# Laden vanuit een ander script: runpy.run_path(.../kop.py)['seo'] (python -I kent geen import uit deze map).
import html, json

SITE_URL = 'https://botlu.ai'
OG_IMAGE = SITE_URL + '/media/og-botlu.jpg'


def seo(pad, titel, omschrijving, ld=None):
    """pad = '/' of '/prijzen'; ld = optionele structured data (dict of lijst) als JSON-LD."""
    e = lambda s: html.escape(s, quote=True)
    url = SITE_URL + pad
    regels = [
        f'<link rel="canonical" href="{url}">',
        f'<meta property="og:type" content="website">',
        f'<meta property="og:site_name" content="Botlu.ai">',
        f'<meta property="og:locale" content="nl_NL">',
        f'<meta property="og:url" content="{url}">',
        f'<meta property="og:title" content="{e(titel)}">',
        f'<meta property="og:description" content="{e(omschrijving)}">',
        f'<meta property="og:image" content="{OG_IMAGE}">',
        '<meta property="og:image:width" content="1200">',
        '<meta property="og:image:height" content="630">',
        '<meta name="twitter:card" content="summary_large_image">',
        '<meta name="theme-color" content="#ffffff">',
        '<link rel="apple-touch-icon" href="/media/icoon-180.png">',
    ]
    if ld:
        regels.append('<script type="application/ld+json">' + json.dumps(ld, ensure_ascii=False).replace('</', '<\\/') + '</script>')
    return '\n'.join(regels)
