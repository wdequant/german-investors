// Password gate: GET shows the sign-in form, POST checks the password against
// SONAR_PASSWORD and issues the signed 7-day session cookie the middleware checks.
// (The earlier Microsoft Entra SSO flow lives in git history — swap back when ready.)
import { createHmac, createHash, timingSafeEqual } from 'node:crypto';

const WEEK = 7 * 24 * 3600;

const FORM = (err) => `<!doctype html><html><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Sonar — sign in</title>
<link rel="icon" type="image/svg+xml" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Crect width='24' height='24' rx='5.5' fill='%232733f0'/%3E%3Cg fill='none' stroke='%23fff' stroke-linecap='round' stroke-width='1.7'%3E%3Cpath d='M7 12.8 A4.2 4.2 0 0 1 11.2 17'/%3E%3Cpath d='M7 9.3 A7.7 7.7 0 0 1 14.7 17' opacity='.72'/%3E%3Cpath d='M7 5.8 A11.2 11.2 0 0 1 18.2 17' opacity='.45'/%3E%3C/g%3E%3Ccircle cx='7' cy='17' r='1.8' fill='%23fff'/%3E%3Ccircle cx='15.2' cy='8.8' r='1.5' fill='%23fff'/%3E%3C/svg%3E">
<style>
body{margin:0;min-height:100vh;display:flex;align-items:center;justify-content:center;
  background:#f1eee6;font-family:-apple-system,'Segoe UI',Roboto,sans-serif;color:#1a1a1a}
.card{background:#fcfbf6;border:1px solid #e2ddd0;border-radius:14px;padding:36px 40px;
  max-width:340px;width:88%;box-shadow:0 1px 4px rgba(0,0,0,.04)}
.mark{display:inline-flex;width:34px;height:34px;margin-bottom:14px}
.mark svg{width:100%;height:100%;display:block}
h1{font-size:19px;margin:0 0 4px}
p{font-size:13px;color:#6b675e;margin:0 0 20px}
input{width:100%;box-sizing:border-box;padding:10px 12px;font-size:15px;border:1px solid #d8d2c2;
  border-radius:9px;background:#fff;margin-bottom:12px}
input:focus{outline:none;border-color:#2733f0}
button{width:100%;padding:10px;font-size:14px;font-weight:600;color:#fff;background:#2733f0;
  border:0;border-radius:9px;cursor:pointer}
.err{background:#fbeaea;border:1px solid #e3b8b8;color:#8c2f2f;font-size:13px;
  padding:9px 12px;border-radius:8px;margin:0 0 14px}
</style></head><body><form class="card" method="POST" action="/api/login"
  onsubmit="var b=this.querySelector('button');b.disabled=true;b.textContent='Checking…'">
<span class="mark"><svg viewBox="0 0 24 24"><rect width="24" height="24" rx="5.5" fill="#2733f0"/><g fill="none" stroke="#fff" stroke-linecap="round" stroke-width="1.7"><path d="M7 12.8 A4.2 4.2 0 0 1 11.2 17"/><path d="M7 9.3 A7.7 7.7 0 0 1 14.7 17" opacity=".72"/><path d="M7 5.8 A11.2 11.2 0 0 1 18.2 17" opacity=".45"/></g><circle cx="7" cy="17" r="1.8" fill="#fff"/><circle cx="15.2" cy="8.8" r="1.5" fill="#fff"/></svg></span>
<h1>Sonar</h1><p>Highland Europe · relationship intelligence</p>
${err ? '<div class="err">Wrong password — check for autofill of an old one, then try again.</div>' : ''}
<input type="password" name="password" placeholder="Team password" autofocus autocomplete="current-password">
<button type="submit">Enter</button>
</form></body></html>`;

const sha = (s) => createHash('sha256').update(s, 'utf8').digest();

export default async function handler(req, res) {
  const { SONAR_PASSWORD, SESSION_SECRET } = process.env;
  if (!SONAR_PASSWORD || !SESSION_SECRET) {
    res.status(503).send('Sonar login is not configured: set SONAR_PASSWORD and SESSION_SECRET in Vercel.');
    return;
  }
  if (req.method !== 'POST') {
    res.status(200).setHeader('content-type', 'text/html; charset=utf-8');
    res.send(FORM('e' in (req.query || {})));
    return;
  }
  const body = typeof req.body === 'string'
    ? Object.fromEntries(new URLSearchParams(req.body)) : (req.body || {});
  const given = String(body.password || '');
  if (!given || !timingSafeEqual(sha(given), sha(SONAR_PASSWORD))) {
    await new Promise(r => setTimeout(r, 800)); // slow down guessing
    res.redirect(302, '/api/login?e');
    return;
  }
  const exp = Math.floor(Date.now() / 1000) + WEEK;
  const who = Buffer.from('team').toString('base64url');
  const sig = createHmac('sha256', SESSION_SECRET).update(`${exp}.${who}`).digest('hex');
  res.setHeader('Set-Cookie',
    `sonar_session=${exp}.${who}.${sig}; HttpOnly; Secure; Path=/; Max-Age=${WEEK}; SameSite=Lax`);
  res.redirect(302, '/');
}
