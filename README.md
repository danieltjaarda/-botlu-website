# Botlu.ai website

Marketingsite voor botlu.ai. Statisch: `index.html`, `branches/*.html` (21 pagina's per branche, gebouwd met `scripts/maak-branches.py`, dat ook het menu 'Branches' in index.html bijwerkt), `ontwikkelaars.html` (API, webhooks, no-code; gebouwd met `scripts/maak-ontwikkelaars.py`, basis uit index.html), de juridische pagina's, `linten.js` (gedeelde WebGL-linten), de stemfragmenten in `voices/` het lettertype in `fonts/` (Inter Variable 4.1, ingekort tot Latijns schrift, SIL OFL), de app-iconen in `apps/` (App Store), de bedrijfslogo's in `logos/` en de profielfoto's per branche in `avatars/` (gemaakt met Nano Banana 2).
Het dashboard is een apart project (~/fonia-dashboard) op app.botlu.ai.

Lokaal bekijken: `node dev.js` en open http://localhost:4330. De pagina ververst vanzelf zodra er een bestand verandert.

Na een wijziging in het menu of de footer van index.html: `python3 -I scripts/maak-branches.py && python3 -I scripts/maak-ontwikkelaars.py`, zodat alle pagina's dezelfde navigatie krijgen.
