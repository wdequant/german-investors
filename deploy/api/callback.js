// Completes the Microsoft sign-in: exchanges the code, checks the user is in the
// Highland tenant and on the allowed email domain, then issues the signed session cookie.
import { createHmac } from 'node:crypto';

const WEEK = 7 * 24 * 3600;

function getCookie(req, name) {
  const m = (req.headers.cookie || '').match(new RegExp('(?:^|;\\s*)' + name + '=([^;]+)'));
  return m ? m[1] : null;
}

function b64urlJSON(part) {
  return JSON.parse(Buffer.from(part.replace(/-/g, '+').replace(/_/g, '/'), 'base64').toString('utf8'));
}

export default async function handler(req, res) {
  const { AZURE_TENANT_ID, AZURE_CLIENT_ID, AZURE_CLIENT_SECRET, SESSION_SECRET } = process.env;
  const allowedDomain = (process.env.ALLOWED_EMAIL_DOMAIN || 'highlandeurope.com').toLowerCase();
  if (!AZURE_TENANT_ID || !AZURE_CLIENT_ID || !AZURE_CLIENT_SECRET || !SESSION_SECRET) {
    res.status(503).send('Sonar login is not configured: set the AZURE_* variables and SESSION_SECRET in Vercel.');
    return;
  }
  const { code, state, error, error_description } = req.query;
  if (error) { res.status(401).send(`Microsoft sign-in failed: ${error_description || error}`); return; }
  if (!code || !state || state !== getCookie(req, 'sonar_state')) {
    res.status(401).send('Sign-in state mismatch — please go back and try again.');
    return;
  }

  const tokenResp = await fetch(
    `https://login.microsoftonline.com/${AZURE_TENANT_ID}/oauth2/v2.0/token`, {
      method: 'POST',
      headers: { 'content-type': 'application/x-www-form-urlencoded' },
      body: new URLSearchParams({
        client_id: AZURE_CLIENT_ID,
        client_secret: AZURE_CLIENT_SECRET,
        grant_type: 'authorization_code',
        code,
        redirect_uri: `https://${req.headers.host}/api/callback`,
      }),
    });
  if (!tokenResp.ok) {
    res.status(401).send('Token exchange with Microsoft failed — check the app registration and client secret.');
    return;
  }
  const { id_token } = await tokenResp.json();
  // The id_token comes straight from Microsoft's token endpoint over TLS in a
  // confidential-client exchange, so we read its claims without a local JWKS check.
  const claims = b64urlJSON(id_token.split('.')[1]);
  const email = (claims.email || claims.preferred_username || '').toLowerCase();
  if (claims.tid !== AZURE_TENANT_ID || !email.endsWith('@' + allowedDomain)) {
    res.status(403).send(`Access is limited to @${allowedDomain} accounts.`);
    return;
  }

  const exp = Math.floor(Date.now() / 1000) + WEEK;
  const who = Buffer.from(email).toString('base64url');
  const sig = createHmac('sha256', SESSION_SECRET).update(`${exp}.${who}`).digest('hex');
  res.setHeader('Set-Cookie', [
    `sonar_session=${exp}.${who}.${sig}; HttpOnly; Secure; Path=/; Max-Age=${WEEK}; SameSite=Lax`,
    'sonar_state=; HttpOnly; Secure; Path=/; Max-Age=0; SameSite=Lax',
  ]);
  res.redirect(302, '/');
}
