// Edge middleware: every page request must carry a valid signed session cookie.
// Fails closed — with no SESSION_SECRET configured, the site serves a setup
// notice rather than the (sensitive) page.
export const config = { matcher: ['/((?!api/|_vercel).*)'] };

const enc = new TextEncoder();

async function hmac(secret, msg) {
  const key = await crypto.subtle.importKey(
    'raw', enc.encode(secret), { name: 'HMAC', hash: 'SHA-256' }, false, ['sign']);
  const sig = await crypto.subtle.sign('HMAC', key, enc.encode(msg));
  return [...new Uint8Array(sig)].map(b => b.toString(16).padStart(2, '0')).join('');
}

function getCookie(req, name) {
  const m = (req.headers.get('cookie') || '').match(new RegExp('(?:^|;\\s*)' + name + '=([^;]+)'));
  return m ? m[1] : null;
}

export default async function middleware(req) {
  const secret = process.env.SESSION_SECRET;
  if (!secret) {
    return new Response(
      'Sonar is deployed but not yet configured: set SESSION_SECRET (and the AZURE_* variables) '
      + 'in Vercel project settings, then redeploy. See deploy/README.md in the repo.',
      { status: 503, headers: { 'content-type': 'text/plain' } });
  }
  const cookie = getCookie(req, 'sonar_session');
  if (cookie) {
    const [exp, who, sig] = cookie.split('.');
    if (exp && who && sig && Number(exp) > Date.now() / 1000
        && sig === await hmac(secret, `${exp}.${who}`)) {
      return; // valid session — serve the page
    }
  }
  return Response.redirect(new URL('/api/login', req.url), 302);
}
