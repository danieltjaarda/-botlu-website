# Bouwt sitemap.xml voor zoekmachines (draai: python3 -I scripts/maak-sitemap.py, na de andere scripts).
# Elke .html-pagina komt erin; de datum is die van de laatste commit van dat bestand, of vandaag bij wijzigingen.
import datetime, pathlib, subprocess

SITE = pathlib.Path(__file__).resolve().parent.parent
URL = 'https://botlu.ai'

def datum(f):
    rel = str(f.relative_to(SITE))
    gewijzigd = subprocess.run(['git', 'status', '--porcelain', '--', rel], cwd=SITE, capture_output=True, text=True).stdout.strip()
    laatst = subprocess.run(['git', 'log', '-1', '--format=%cs', '--', rel], cwd=SITE, capture_output=True, text=True).stdout.strip()
    return laatst if laatst and not gewijzigd else datetime.date.today().isoformat()

paginas = [SITE / 'index.html'] + sorted(f for f in SITE.glob('*.html') if f.name != 'index.html') + sorted((SITE / 'branches').glob('*.html'))
regels = []
for f in paginas:
    pad = '/' if f.name == 'index.html' else '/' + str(f.relative_to(SITE))[:-5]
    regels.append(f'  <url><loc>{URL}{pad}</loc><lastmod>{datum(f)}</lastmod></url>')
(SITE / 'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + '\n'.join(regels) + '\n</urlset>\n')
print(f'sitemap.xml: {len(regels)} pagina’s')
