// Starts the Microsoft Entra ID sign-in flow (authorization code, confidential client).
function randomHex(n) {
  const b = new Uint8Array(n);
  crypto.getRandomValues(b);
  return [...b].map(x => x.toString(16).padStart(2, '0')).join('');
}

export default function handler(req, res) {
  const { AZURE_TENANT_ID, AZURE_CLIENT_ID } = process.env;
  if (!AZURE_TENANT_ID || !AZURE_CLIENT_ID) {
    res.status(503).send('Sonar login is not configured: set AZURE_TENANT_ID and AZURE_CLIENT_ID in Vercel.');
    return;
  }
  const state = randomHex(16);
  res.setHeader('Set-Cookie',
    `sonar_state=${state}; HttpOnly; Secure; Path=/; Max-Age=600; SameSite=Lax`);
  const u = new URL(`https://login.microsoftonline.com/${AZURE_TENANT_ID}/oauth2/v2.0/authorize`);
  u.searchParams.set('client_id', AZURE_CLIENT_ID);
  u.searchParams.set('response_type', 'code');
  u.searchParams.set('response_mode', 'query');
  u.searchParams.set('redirect_uri', `https://${req.headers.host}/api/callback`);
  u.searchParams.set('scope', 'openid profile email');
  u.searchParams.set('state', state);
  res.redirect(302, u.toString());
}
