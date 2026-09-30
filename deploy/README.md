# Sonar on Vercel — deploy & setup runbook

The app is a static build (`public/index.html`, produced by `scripts/build_coverage.py`)
behind a login gate implemented in this directory:

- `middleware.js` — refuses to serve any page without a valid signed session cookie.
  **Fails closed**: with no `SESSION_SECRET` configured it serves a setup notice, never the data.
- `api/login.js` — the team-password sign-in form; a correct password issues a 7-day
  signed cookie. (The original Microsoft Entra SSO flow is in git history at commit
  `eec9b62` — swap back when Highland wants per-person SSO.)
- `api/logout.js` — clears the session.

Deploys are driven by `.github/workflows/deploy.yml`: every push (and a nightly
05:30 UTC rebuild) reruns the Python build and ships `deploy/` to Vercel
(project `sonar`, team `highland-europe`).

## Setup (Will — ~5 minutes)

1. Vercel dashboard → `sonar` project → **Settings → Environment Variables** (Production):
   - `SONAR_PASSWORD` — the team password you'll share with colleagues
   - `SESSION_SECRET` — any long random string (e.g. `openssl rand -hex 32`)
2. **Settings → Deployment Protection → turn OFF Vercel Authentication** — otherwise
   colleagues without Vercel accounts never reach the password page. The password
   gate is then the site's lock.
3. Redeploy (re-run the GitHub Action or push any commit) so the env vars take effect.
4. Optional domain: **Settings → Domains** → add `sonar.highlandeurope.com`, create
   the CNAME Vercel shows in the highlandeurope.com DNS.

## Day-2 notes
- Every push redeploys automatically; the nightly cron rebuilds with committed data.
- Sessions last 7 days; `/api/logout` signs out.
- To lock everyone out at once (or after sharing the password too widely):
  change `SONAR_PASSWORD` *and* rotate `SESSION_SECRET`, then redeploy.
- A shared password is an interim lock: anyone who has it (including a leaver) gets in
  until it's rotated. The Entra SSO flow in git history removes that class of risk —
  revisit once the app has proven itself.

## Appendix: the Microsoft Entra SSO upgrade (when ready)

Restore `api/callback.js` and the SSO `api/login.js` from commit `eec9b62`, then:

1. portal.azure.com → **Microsoft Entra ID → App registrations → New registration**.
   - Name: `Sonar` · this-directory-only · Redirect URI (**Web**):
     `https://sonar.highlandeurope.com/api/callback` (plus the `*.vercel.app` one for testing)
2. Copy **Application (client) ID** and **Directory (tenant) ID**; create a client secret.
3. Vercel env vars: `AZURE_TENANT_ID`, `AZURE_CLIENT_ID`, `AZURE_CLIENT_SECRET`
   (keep `SESSION_SECRET`; `ALLOWED_EMAIL_DOMAIN` defaults to `highlandeurope.com`).
4. Redeploy. Leavers then lose access when IT disables their Microsoft account.
