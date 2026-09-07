# Sonar on Vercel — deploy & setup runbook

The app is a static build (`public/index.html`, produced by `scripts/build_coverage.py`)
behind a Microsoft-SSO gate implemented in this directory:

- `middleware.js` — refuses to serve any page without a valid signed session cookie.
  **Fails closed**: with no `SESSION_SECRET` configured it serves a setup notice, never the data.
- `api/login.js` → redirects to Microsoft Entra sign-in.
- `api/callback.js` → completes sign-in; only accepts accounts in the Highland tenant
  with an `@highlandeurope.com` address, then sets a 7-day signed cookie.
- `api/logout.js` → clears the session.

Deploys are driven by `.github/workflows/deploy.yml`: every push (and a nightly
05:30 UTC rebuild) reruns the Python build and ships `deploy/` to Vercel.

## One-time setup (Will / IT — ~30 minutes total)

### 1. Vercel (5 min)
1. Create/sign in at vercel.com (a Hobby account works; Pro if you want it on the company org).
2. Account → **Settings → Tokens** → create a token named `sonar-ci` (no expiry or 1 year).
3. In GitHub, repo **Settings → Secrets and variables → Actions → New repository secret**:
   name `VERCEL_TOKEN`, value = the token.
4. Run the **Build & deploy Sonar** workflow once (repo → Actions → select it → Run workflow).
   It creates the `sonar` project on Vercel and deploys. The site will show the
   "not yet configured" notice — that's the fail-closed gate working.

### 2. Microsoft Entra app registration (10 min, needs an Entra admin)
1. portal.azure.com → **Microsoft Entra ID → App registrations → New registration**.
   - Name: `Sonar`
   - Supported account types: **Accounts in this organizational directory only**
   - Redirect URI (type **Web**): `https://sonar.highlandeurope.com/api/callback`
   - Also add the temporary one so you can test before DNS:
     `https://<your-project>.vercel.app/api/callback` (exact URL shown after the first deploy)
2. On the app's Overview page, copy **Application (client) ID** and **Directory (tenant) ID**.
3. **Certificates & secrets → New client secret** (24 months) — copy the secret **value** immediately.

### 3. Vercel environment variables (5 min)
Vercel dashboard → `sonar` project → **Settings → Environment Variables** (Production):

| Name | Value |
|---|---|
| `AZURE_TENANT_ID` | Directory (tenant) ID from step 2 |
| `AZURE_CLIENT_ID` | Application (client) ID from step 2 |
| `AZURE_CLIENT_SECRET` | client secret value from step 2 |
| `SESSION_SECRET` | random string, e.g. output of `openssl rand -hex 32` |
| `ALLOWED_EMAIL_DOMAIN` | `highlandeurope.com` (optional — this is the default) |

Then redeploy (re-run the GitHub Action, or Vercel → Deployments → Redeploy).
Visiting the site should now bounce you to the Microsoft login and back in.

### 4. Domain (5 min + DNS propagation)
1. Vercel → `sonar` project → **Settings → Domains** → add `sonar.highlandeurope.com`.
2. In the highlandeurope.com DNS, add the CNAME record Vercel shows
   (typically `sonar → cname.vercel-dns.com`).
3. Once it's live, keep only the production redirect URI in the Entra app
   (remove the `*.vercel.app` one) so logins only flow through the real domain.

## Day-2 notes
- **Every push to the repo redeploys automatically**; the nightly cron redeploys with
  whatever data is committed. Refreshing the Affinity dump nightly (n8n → repo commit)
  is the follow-up that makes the cron meaningful.
- Sessions last 7 days; `https://sonar.highlandeurope.com/api/logout` signs out.
- To revoke a leaver's access: they lose it when IT disables their Microsoft account
  (an existing cookie dies within its 7-day window; rotate `SESSION_SECRET` to kill
  all sessions immediately).
- The `*.vercel.app` URL stays reachable but sits behind the same login gate.
