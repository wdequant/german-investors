// Live check: verifies the open dossier against Affinity (funnel + owners per
// company) and Harmonic (headcount + latest funding per domain), in real time.
// Session-gated with the same signed cookie the middleware checks.
import { createHmac } from 'node:crypto';

const LIST_ID = 9387;

function authed(req, secret) {
  const m = (req.headers.cookie || '').match(/(?:^|;\s*)sonar_session=([^;]+)/);
  if (!m) return false;
  const [exp, who, sig] = m[1].split('.');
  return !!(exp && who && sig && Number(exp) > Date.now() / 1000
    && sig === createHmac('sha256', secret).update(`${exp}.${who}`).digest('hex'));
}

export default async function handler(req, res) {
  const { SESSION_SECRET, AFFINITY_API_KEY, HARMONIC_API_KEY } = process.env;
  if (!SESSION_SECRET) { res.status(503).json({ error: 'not configured' }); return; }
  if (!authed(req, SESSION_SECRET)) { res.status(401).json({ error: 'sign in' }); return; }

  const ids = String(req.query.ids || '').split(',').filter(s => /^\d+$/.test(s)).slice(0, 60);
  const domains = String(req.query.domains || '').split(',')
    .map(s => s.trim().toLowerCase()).filter(s => /^[a-z0-9.-]+\.[a-z]{2,}$/.test(s)).slice(0, 25);

  const out = { checkedAt: new Date().toISOString(), affinity: {}, harmonic: {},
                sources: { affinity: !!AFFINITY_API_KEY, harmonic: !!HARMONIC_API_KEY } };

  const jobs = [];
  if (AFFINITY_API_KEY) {
    for (const id of ids) {
      jobs.push((async () => {
        const r = await fetch(`https://api.affinity.co/v2/companies/${id}/list-entries`,
          { headers: { authorization: `Bearer ${AFFINITY_API_KEY}` } });
        if (!r.ok) return;
        const entry = ((await r.json()).data || []).find(x => x.listId === LIST_ID);
        if (!entry) { out.affinity[id] = { tracked: false }; return; }
        let funnel = null, owners = [];
        for (const f of entry.fields || []) {
          if (f.id === 'field-81237') funnel = f.value?.data?.text || null;
          if (f.id === 'field-81239') owners = (f.value?.data || [])
            .map(p => `${p.firstName || ''} ${p.lastName || ''}`.trim()).filter(Boolean);
        }
        out.affinity[id] = { tracked: true, funnel, owners };
      })());
    }
  }
  if (HARMONIC_API_KEY) {
    for (const dom of domains) {
      jobs.push((async () => {
        const r = await fetch(
          `https://api.harmonic.ai/companies?website_domain=${encodeURIComponent(dom)}`,
          { method: 'POST', headers: { apikey: HARMONIC_API_KEY } });
        if (!r.ok) return;
        const d = await r.json();
        out.harmonic[dom] = {
          headcount: d.headcount ?? null,
          last_funding_at: d.funding?.last_funding_at || null,
          last_funding_type: d.funding?.last_funding_type || null,
          last_funding_total: d.funding?.last_funding_total ?? null,
          funding_total: d.funding?.funding_total ?? null,
        };
      })());
    }
  }
  await Promise.allSettled(jobs);
  res.setHeader('cache-control', 'no-store');
  res.status(200).json(out);
}
