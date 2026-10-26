// Lokaal bekijken met automatisch verversen: node dev.js (http://localhost:4330).
// Serveert de map zoals Vercel (cleanUrls) en herlaadt open pagina's zodra er
// een bestand verandert.
const http = require('http');
const fs = require('fs');
const path = require('path');

const PORT = process.env.PORT || 4330;
const ROOT = __dirname;
const TYPES = { '.html': 'text/html; charset=utf-8', '.js': 'text/javascript', '.css': 'text/css', '.svg': 'image/svg+xml', '.png': 'image/png', '.mp3': 'audio/mpeg', '.json': 'application/json' };
// Gaat onderaan elke pagina mee: bij een wijziging herlaadt de browser
const RELOAD = `<script>new EventSource('/__herlaad').onmessage = () => location.reload();</script>`;
const clients = new Set();

http.createServer((req, res) => {
  const url = new URL(req.url, 'http://x');
  if (url.pathname === '/__herlaad') {
    res.writeHead(200, { 'Content-Type': 'text/event-stream', 'Cache-Control': 'no-cache', Connection: 'keep-alive' });
    res.write(': verbonden\n\n');
    clients.add(res);
    req.on('close', () => clients.delete(res));
    return;
  }
  let name = decodeURIComponent(url.pathname);
  if (name.endsWith('/')) name += 'index.html';
  else if (!path.extname(name)) name += '.html';   // cleanUrls, zoals op Vercel
  const file = path.join(ROOT, path.normalize(name));
  // Alleen bestanden in deze map, en geen verborgen bestanden zoals .git
  if (!file.startsWith(ROOT + path.sep) || file.slice(ROOT.length).split(path.sep).some(p => p.startsWith('.'))) return res.writeHead(404).end('Niet gevonden');
  fs.readFile(file, (err, data) => {
    if (err) return res.writeHead(404).end('Niet gevonden');
    const type = TYPES[path.extname(file)] || 'application/octet-stream';
    if (type.startsWith('text/html')) data = data.toString().replace('</body>', RELOAD + '</body>');
    res.writeHead(200, { 'Content-Type': type, 'Cache-Control': 'no-store' }).end(data);
  });
}).listen(PORT, '127.0.0.1', () => console.log(`Botlu-website draait op http://localhost:${PORT} (ververst vanzelf)`));

// Bij een wijziging alle open pagina's herladen; even wachten, want editors
// schrijven een bestand soms in stappen
let timer;
fs.watch(ROOT, { recursive: true }, (event, f) => {
  if (!f || f.startsWith('.git') || f === 'dev.js') return;
  clearTimeout(timer);
  timer = setTimeout(() => { for (const c of clients) c.write('data: herlaad\n\n'); }, 150);
});
// Verbinding openhouden
setInterval(() => { for (const c of clients) c.write(': ping\n\n'); }, 30000);
