// Password gate: GET shows the sign-in form, POST checks the password against
// SONAR_PASSWORD and issues the signed 7-day session cookie the middleware checks.
// (The earlier Microsoft Entra SSO flow lives in git history — swap back when ready.)
import { createHmac, createHash, timingSafeEqual } from 'node:crypto';

const WEEK = 7 * 24 * 3600;

const FORM = (err) => `<!doctype html><html><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Sonar — sign in</title>
<style>
body{margin:0;min-height:100vh;display:flex;align-items:center;justify-content:center;
  background:#f1eee6;font-family:-apple-system,'Segoe UI',Roboto,sans-serif;color:#1a1a1a}
.card{background:#fcfbf6;border:1px solid #e2ddd0;border-radius:14px;padding:36px 40px;
  max-width:340px;width:88%;box-shadow:0 1px 4px rgba(0,0,0,.04)}
.mark{display:inline-flex;width:34px;height:34px;border-radius:9px;background:#2733f0;color:#fff;
  align-items:center;justify-content:center;font-weight:700;font-size:18px;margin-bottom:14px}
h1{font-size:19px;margin:0 0 4px}
p{font-size:13px;color:#6b675e;margin:0 0 20px}
input{width:100%;box-sizing:border-box;padding:10px 12px;font-size:15px;border:1px solid #d8d2c2;
  border-radius:9px;background:#fff;margin-bottom:12px}
input:focus{outline:none;border-color:#2733f0}
button{width:100%;padding:10px;font-size:14px;font-weight:600;color:#fff;background:#2733f0;
  border:0;border-radius:9px;cursor:pointer}
.err{color:#a33;font-size:12.5px;margin:-4px 0 12px}
</style></head><body><form class="card" method="POST" action="/api/login">
<span class="mark">S</span>
<h1>Sonar</h1><p>Highland Europe · relationship intelligence</p>
${err ? '<div class="err">Wrong password — try again.</div>' : ''}
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
