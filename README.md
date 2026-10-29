# Botlu.ai website

Marketingsite voor botlu.ai. Statisch: `index.html`, `branches/*.html` (21 pagina's per branche, gebouwd met `scripts/maak-branches.py`, dat ook het menu 'Branches' in index.html bijwerkt), `ontwikkelaars.html` (API, webhooks, no-code; gebouwd met `scripts/maak-ontwikkelaars.py`, basis uit index.html), de juridische pagina's, `linten.js` (gedeelde WebGL-linten), de stemfragmenten in `voices/` het lettertype in `fonts/` (Inter Variable 4.1, ingekort tot Latijns schrift, SIL OFL), de app-iconen in `apps/` (App Store, als WebP), de bedrijfslogo's in `logos/` en de profielfoto's per branche in `avatars/` (gemaakt met Nano Banana 2).
Het dashboard is een apart project (~/fonia-dashboard) op app.botlu.ai.

Lokaal bekijken: `node dev.js` en open http://localhost:4330. De pagina ververst vanzelf zodra er een bestand verandert.

Na een wijziging in het menu of de footer van index.html: `python3 -I scripts/maak-branches.py && python3 -I scripts/maak-ontwikkelaars.py && python3 -I scripts/maak-prijzen.py && python3 -I scripts/maak-sitemap.py`, zodat alle pagina's dezelfde navigatie krijgen en de sitemap klopt.

SEO: titel, omschrijving, canonical en Open Graph per pagina komen uit `scripts/kop.py` (deelafbeelding `media/og-botlu.jpg`, 1200×630). Bij een nieuwe pagina ook `scripts/maak-sitemap.py` draaien. App-iconen en logo's staan als WebP; het woordmerk (Poppins 500, alleen de letters van "Botlu.ai") zit ingebakken in de CSS, er wordt niets bij Google Fonts opgehaald.
