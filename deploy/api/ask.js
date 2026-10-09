// Ask Sonar — chat over the live relationship data, answered by Claude.
// POST {messages:[{role,content}...], who} -> {answer, used:[tool names]}.
// Auth: the same signed sonar_session cookie the middleware checks (the
// middleware matcher excludes /api/, so this route verifies it itself).
// Claude gets a small set of tools over the build's data payload and must
// ground every answer in what they return.
import { createHmac, timingSafeEqual } from 'node:crypto';
import { readFileSync } from 'node:fs';
import Anthropic from '@anthropic-ai/sdk';

export const config = { maxDuration: 60 };

const D = JSON.parse(readFileSync(new URL('./_data.json', import.meta.url), 'utf8'));
const REGIONS = Object.keys(D.regions);
const ACCELCAT = { accelerator: 1, accel: 1, studio: 1 };
const PROF = D.profiles || {};
const ALLE = REGIONS.flatMap(r => D.regions[r].entities.map(e => ({ r, e })));

// ---- scoring, ported from the viz (keep in sync with coverage_template.py) ----
function personSignal(e, name) {
  const p = (e.top_people || []).find(x => x.name === name);
  const dorm = e.dormant && e.dormant.internal.includes(name) ? e.dormant : null;
  return { aff: p ? p.aff : 0, h: p ? p.harmonic : 0, dorm };
}
function personCov(e, name) {
  const s = personSignal(e, name);
  let a = s.aff * (e.cov_parts ? e.cov_parts.decay : 1);
  if (s.dorm) {
    const age = 2026 - parseInt(s.dorm.last.slice(0, 4));
    a = Math.max(a, age <= 1 ? 0.22 : age <= 3 ? 0.15 : age <= 6 ? 0.10 : 0.06);
  }
  const hn = Math.min(1, Math.sqrt(s.h) / Math.sqrt(30));
  return Math.round(100 * (0.55 * hn + 0.45 * a));
}
const norm = s => (s || '').toLowerCase().replace(/[^a-z0-9]+/g, ' ').trim();

function htcBook() {
  const seen = new Set(), out = [];
  REGIONS.forEach(r => (D.regions[r].htc || []).forEach(c => {
    if (!seen.has(c.id)) { seen.add(c.id); out.push({ ...c, region: r }); }
  }));
  (D.xhtc || []).forEach(c => { if (!seen.has(c.id)) { seen.add(c.id); out.push({ ...c, region: null }); } });
  return out;
}
const HTC = htcBook();

function pipelineCos() {
  const seen = new Set(), out = [];
  ALLE.forEach(({ e }) => Object.entries(e.buckets || {}).forEach(([stage, l]) => l.forEach(p => {
    if (!seen.has(p.id)) { seen.add(p.id); out.push({ ...p, stage, via: e.name }); }
  })));
  return out;
}
const PIPE = pipelineCos();

const profOf = o => PROF[((o && o.domain) || '').toLowerCase().replace(/^www\./, '')] || {};
const bizBits = pr => ({
  description: pr.d || null, headcount: pr.hc ?? null, headcount_growth_yoy_pct: pr.hg ?? null,
  funding_usd: pr.fu ?? null, stage: pr.st || null, founded: pr.f ?? null,
});
const pathOut = p => ({
  highland_contact: p.internal, external_contact: p.external || null, via_fund: p.fund || null,
  strength_pct: p.pct ?? null, last_touch: p.last || null, last_meeting: p.meet || null,
  contact_moved_on: !!p.moved, untracked_backer: !!p.untracked || !!p.unt,
  employment_verified: p.ever === false ? 'unverified — no current Harmonic match, from Affinity history alone' : 'verified current',
});
const BYSLUG = {}; ALLE.forEach(({ e }) => { if (e.slug) BYSLUG[e.slug] = e; });
// the asking user's own best contact at a tracked fund (team paths dedupe these away)
function ownDoor(slug, who) {
  const e = who && slug ? BYSLUG[slug] : null; if (!e) return null;
  const tp = (e.top_people || []).find(x => x.name === who);
  const k = ((tp && tp.contacts) || []).filter(c => !c.moved && (c.pct || 0) > 0)
    .sort((a, b) => (b.pct || 0) - (a.pct || 0))[0];
  return k ? { internal: who, external: k.person, pct: k.pct } : null;
}
function companyOut(c, who) {
  const all = (c.investors || []).flatMap(i => {
    const ps = (i.paths && i.paths.length ? i.paths : (i.best ? [i.best] : [])).slice();
    const o = ownDoor(i.slug, who);
    if (o && !ps.some(p => p && p.internal === who && p.external === o.external)) ps.push(o);
    return ps.filter(p => p && p.internal && !p.moved)
      .map(p => ({ ...p, fund: i.name, untracked: i.untracked }));
  }).sort((a, b) => (b.pct || 0) - (a.pct || 0));
  const byX = {}; all.forEach(p => { const k = p.external || p.fund; (byX[k] = byX[k] || []).push(p); });
  const team = Object.values(byX).map(l => l[0])
    .sort((a, b) => (b.pct || 0) - (a.pct || 0)).slice(0, 6);
  const own = who ? all.filter(p => p.internal === who).slice(0, 4) : [];
  const m = c.meta || {};
  return {
    name: c.name, city: c.city || c.country || null, owners: c.owners || [],
    unframe_score: c.uf != null ? Math.round(c.uf) : null,
    ...bizBits(profOf(c)),
    your_own_relationships: own.map(pathOut),
    strongest_team_paths_in: team.map(pathOut),
    other_backers_untracked: (c.others || []).slice(0, 6),
    comms: { last_email: m.last_email || null, last_meeting: m.last_meet || null, hard_to_crack_since: m.status_since || null },
  };
}
function fundOut(x, who) {
  const { r, e } = x;
  const points = (e.points || []).slice(0, 3).map(pathOut);
  const pipe = {};
  Object.entries(e.buckets || {}).forEach(([k, l]) => { if (l.length) pipe[k] = l.length; });
  return {
    name: e.name, region: D.regions[r].label, city: (e.city || '').split('·')[0].trim() || null,
    category: e.category || 'fund',
    relevance_0_100: e.relevance?.total ?? null,
    team_coverage_0_100: e.connectivity, your_coverage_0_100: who ? personCov(e, who) : null,
    strongest_team_relationships: points,
    pipeline_companies_sourced_via_them: pipe,
    backs_high_priority_cos: e.uf?.high || 0,
    top_portfolio_by_unframe: (e.uf?.top || []).slice(0, 3).map(t => ({ name: t.name, unframe: t.score ? Math.round(t.score) : null })),
    co_invested_with_highland: (e.coinvest || []).length || 0,
  };
}

// ---- tools ----
const TOOLS = {
  search_entities: {
    description: 'Fuzzy name search across everything Sonar tracks: funds/investors, hard-to-crack companies, and pipeline companies. Use first when the user names something, to resolve the exact entity.',
    schema: { query: { type: 'string', description: 'Name or part of a name' } },
    required: ['query'],
    run({ query }) {
      const q = norm(query);
      if (!q) return { matches: [] };
      const score = n => { const nn = norm(n); return nn === q ? 3 : nn.startsWith(q) ? 2 : nn.includes(q) ? 1 : 0; };
      const out = [];
      ALLE.forEach(({ r, e }) => { const s = score(e.name); if (s) out.push({ s, name: e.name, type: e.kind === 'fund' ? 'fund' : 'angel', region: D.regions[r].label }); });
      HTC.forEach(c => { const s = score(c.name); if (s) out.push({ s, name: c.name, type: 'hard_to_crack_company', city: c.city || null, owners: c.owners || [] }); });
      PIPE.forEach(p => { const s = score(p.name); if (s) out.push({ s, name: p.name, type: 'pipeline_company', stage: p.stage, city: p.city || null, owners: p.own || [] }); });
      out.sort((a, b) => b.s - a.s);
      return { matches: out.slice(0, 12).map(({ s, ...rest }) => rest) };
    },
  },
  fund_profile: {
    description: 'Full profile of one fund/investor: relevance, team vs your coverage, who at Highland holds the strongest relationships there, pipeline sourced via them, Unframe portfolio signal.',
    schema: { name: { type: 'string', description: 'Fund name, as returned by search_entities' } },
    required: ['name'],
    run({ name }, who) {
      const q = norm(name);
      const x = ALLE.find(a => norm(a.e.name) === q) || ALLE.find(a => norm(a.e.name).includes(q));
      if (!x) return { error: `No tracked fund matching "${name}". Try search_entities.` };
      return fundOut(x, who);
    },
  },
  company_paths: {
    description: 'How to get into a specific company: owners, Unframe priority, company profile, and the warmest Highland paths in via its backers (including backers outside the tracked fund lists).',
    schema: { name: { type: 'string', description: 'Company name, as returned by search_entities' } },
    required: ['name'],
    run({ name }, who) {
      const q = norm(name);
      let c = HTC.find(c => norm(c.name) === q) || HTC.find(c => norm(c.name).includes(q));
      if (c) return { status: 'hard_to_crack', ...companyOut(c, who) };
      const p = PIPE.find(p => norm(p.name) === q) || PIPE.find(p => norm(p.name).includes(q));
      if (p) return {
        status: `in pipeline (${p.stage})`, name: p.name, city: p.city || null, owners: p.own || [],
        unframe_score: p.uf != null ? Math.round(p.uf) : null, sourced_via_fund: p.via, ...bizBits(profOf(p)),
        note: 'Already in the Affinity pipeline — the owner holds the relationship; coordinate with them rather than opening a new door.',
      };
      return { error: `No company matching "${name}" in the H2C book or pipeline. Try search_entities.` };
    },
  },
  my_coverage: {
    description: "The asking user's coverage quality vs the team's, per region, over relevant funds (relevance >= 55), with their biggest gaps and strengths. Requires a selected identity.",
    schema: { region: { type: 'string', description: 'Optional: germany | nordics | france | us. Omit for all regions.' } },
    required: [],
    run({ region }, who) {
      if (!who) return { error: 'No identity selected in Sonar — ask the user to pick who they are (top right).' };
      const regs = region && D.regions[region] ? [region] : REGIONS;
      const avg = a => a.length ? Math.round(a.reduce((x, y) => x + y, 0) / a.length) : 0;
      return {
        person: who,
        regions: regs.map(r => {
          const rel = D.regions[r].entities.filter(e => e.kind === 'fund' && !ACCELCAT[e.category] && (e.relevance?.total || 0) >= 55);
          const rows = rel.map(e => ({ name: e.name, relevance: e.relevance.total, you: personCov(e, who), team: e.connectivity }))
            .sort((a, b) => b.relevance - a.relevance);
          return {
            region: D.regions[r].label,
            your_avg_coverage: avg(rows.map(x => x.you)), team_avg_coverage: avg(rows.map(x => x.team)),
            biggest_gaps: rows.filter(x => x.you < 22).slice(0, 5),
            strongest: rows.filter(x => x.you >= 50).sort((a, b) => b.you - a.you).slice(0, 3),
          };
        }),
      };
    },
  },
  next_intros: {
    description: 'Who the asking user should build a relationship with next: the highest-relevance funds where their own coverage is weak but a teammate holds a strong door and can intro them. Requires a selected identity.',
    schema: { limit: { type: 'integer', description: 'Max suggestions (default 6)' } },
    required: [],
    run({ limit }, who) {
      if (!who) return { error: 'No identity selected in Sonar — ask the user to pick who they are (top right).' };
      const borrow = ALLE.filter(x => x.e.kind === 'fund' && !ACCELCAT[x.e.category]
          && personCov(x.e, who) < 30 && x.e.connectivity >= 50 && (x.e.points || []).length)
        .sort((a, b) => (b.e.relevance?.total || 0) - (a.e.relevance?.total || 0))
        .slice(0, Math.min(limit || 6, 12));
      return {
        person: who,
        suggestions: borrow.map(x => {
          const p = x.e.points[0];
          return {
            fund: x.e.name, region: D.regions[x.r].label, relevance: x.e.relevance?.total ?? null,
            your_coverage: personCov(x.e, who), team_coverage: x.e.connectivity,
            ask: { teammate: p.internal, their_contact: p.external || null, strength_pct: p.pct ?? null },
            why: { backs_high_priority_cos: x.e.uf?.high || 0, co_invested_with_highland: (x.e.coinvest || []).length || 0 },
          };
        }),
      };
    },
  },
  earmark_for_trip: {
    description: "Offer one-tap earmarking into the user's Plan-a-City-Trip shortlist. Call this AFTER answering any 'who should I meet / visit in <city>' style question, passing the city and the concrete companies/funds you named. The UI then shows an earmark button under your answer.",
    schema: {
      city: { type: 'string', description: 'City the trip is about' },
      items: { type: 'array', items: { type: 'object', properties: {
        type: { type: 'string', enum: ['co', 'fund'] },
        name: { type: 'string' },
        note: { type: 'string', description: 'Short context shown next to the name, e.g. "Unframe 83" or "rel 71"' },
      }, required: ['type', 'name'], additionalProperties: false } },
    },
    required: ['city', 'items'],
    run({ city, items }, who, actions) {
      const its = (items || []).slice(0, 15);
      if (!its.length) return { error: 'no items passed' };
      actions.push({ kind: 'earmark', city, items: its });
      return { ok: true, note: 'Earmark button added under your answer — tell the user it is there.' };
    },
  },
  city_plan: {
    description: "Plan a visit to a city: the asking user's open pipeline companies there (with Unframe priority) and the relevant funds based there with team/your coverage.",
    schema: { city: { type: 'string', description: 'City name, e.g. Berlin, Paris, Stockholm' } },
    required: ['city'],
    run({ city }, who) {
      const q = norm(city);
      const cos = [], funds = [];
      ALLE.forEach(({ r, e }) => {
        const fc = norm((e.city || '').split('·')[0]);
        if (e.kind === 'fund' && fc.includes(q) && !ACCELCAT[e.category])
          funds.push({ name: e.name, relevance: e.relevance?.total ?? null, team_coverage: e.connectivity, your_coverage: who ? personCov(e, who) : null });
        Object.values(e.buckets || {}).forEach(l => l.forEach(p => {
          if (!norm(p.city || '').includes(q)) return;
          if (who && !(p.own || []).includes(who)) return;
          if (!cos.some(c => c.id === p.id)) cos.push({ id: p.id, name: p.name, unframe: p.uf != null ? Math.round(p.uf) : null, owners: p.own || [] });
        }));
      });
      cos.sort((a, b) => (b.unframe ?? -1) - (a.unframe ?? -1));
      funds.sort((a, b) => (b.relevance ?? -1) - (a.relevance ?? -1));
      return { city, pipeline_companies: cos.slice(0, 10).map(({ id, ...c }) => c), funds_based_there: funds.slice(0, 10) };
    },
  },
};

export const _tools = TOOLS; // for tests

const toolDefs = Object.entries(TOOLS).map(([name, t]) => ({
  name, description: t.description, strict: true,
  input_schema: { type: 'object', properties: t.schema, required: t.required, additionalProperties: false },
}));

const roleOf = n => {
  const t = (D.team || []).find(t => (t.full || t.name) === n);
  return (t && t.role) || { 'Fergal Mullen': 'partner', 'Laurence Garrett': 'partner' }[n] || null;
};
const systemPrompt = who => `You are Sonar, Highland Europe's relationship-intelligence assistant, answering ${who ? `${who}${roleOf(who) ? ` (${roleOf(who)})` : ''}` : 'a Highland investor (no identity selected)'} on ${D.generated}.

Sonar tracks ~111 venture funds across Germany, the Nordics, France and US funds active in Europe, plus Highland's full Affinity pipeline and every "hard to crack" company, enriched with Unframe scores and Harmonic data.

Score semantics:
- Coverage (0-100): strength of a relationship with a fund. >=50 strong, 22-49 workable, <22 effectively unreachable.
- Relevance (0-100): how much a fund matters for Highland's dealflow. >=55 counts as relevant.
- Unframe combined score (0-100): Highland's key pipeline-prioritisation measure. >=85 top priority, 70-84 solid, below that lower priority.
- Path strength % : how live a Highland person's relationship with an external contact is (meeting recency and interaction strength).

Rules:
- Always resolve names with search_entities first if unsure, then use the specific tool. Base every claim on tool output; if the data does not contain something, say so plainly — never invent names, scores or relationships.
- For trip or city questions ("who should I meet in Stockholm"), use city_plan and give a complete answer first: every pick on its own "-" line with the **name**, the one number that matters and a short why (the door, the score, the pipeline tie). Then call earmark_for_trip with those picks. Close with one short line like "tap below to earmark these for the trip" — the buttons are a convenience under your answer, never the substance of it.
- Contacts marked employment_verified "unverified" could not be matched to a current Harmonic role: the relationship comes from Affinity history alone, so mention the caveat (they may have changed roles) when recommending such a door.
- When the asking user already holds a live relationship themselves (your_own_relationships, or a path whose highland_contact is them), recommend going direct through it and mention the teammate's stronger door only as a complement — never tell them to ask a colleague for an intro to someone they already know. Note that path strength only counts interactions logged in Affinity, so their real relationship may be stronger than the number.
- Tailor network-building advice to the asker's seniority (given above). A PARTNER is not trying to replicate relationships the firm already has: when they ask who to build with or where to focus, lead with funds where Highland's TEAM coverage is low — the firm's collective white space — and never suggest they get introduced to a contact a teammate already holds strongly; if a fund is well covered, say who covers it and move on. An ASSOCIATE, ANALYST or SENIOR is building their own book: personal coverage gaps are the point, and borrowing a teammate's door with an intro ask is exactly right.
- Be concise and actionable: name the exact person to ask and the door they hold. Lead with the recommendation, then the one or two numbers that justify it.
- Plain text only: short paragraphs and "-" bullets. Bold key names with **. No tables, no headers.
- Keep answers under ~180 words unless the user asks for depth; city/trip answers may run longer when listing picks.`;

// ---- auth ----
function authed(req) {
  const secret = process.env.SESSION_SECRET;
  if (!secret) return false;
  const m = (req.headers.cookie || '').match(/(?:^|;\s*)sonar_session=([^;]+)/);
  if (!m) return false;
  const [exp, whoTok, sig] = m[1].split('.');
  if (!exp || !whoTok || !sig || Number(exp) <= Date.now() / 1000) return false;
  const want = createHmac('sha256', secret).update(`${exp}.${whoTok}`).digest('hex');
  const a = Buffer.from(sig), b = Buffer.from(want);
  return a.length === b.length && timingSafeEqual(a, b);
}

export default async function handler(req, res) {
  if (req.method !== 'POST') { res.status(405).json({ error: 'POST only' }); return; }
  if (!authed(req)) { res.status(401).json({ error: 'not signed in' }); return; }
  if (!process.env.ANTHROPIC_API_KEY) { res.status(503).json({ error: 'not_configured' }); return; }

  const body = typeof req.body === 'object' && req.body ? req.body : {};
  const who = typeof body.who === 'string' ? body.who.slice(0, 60) : '';
  const history = Array.isArray(body.messages) ? body.messages.slice(-12) : [];
  const messages = history
    .filter(m => m && (m.role === 'user' || m.role === 'assistant') && typeof m.content === 'string' && m.content.trim())
    .map(m => ({ role: m.role, content: m.content.slice(0, 4000) }));
  if (!messages.length || messages[messages.length - 1].role !== 'user') {
    res.status(400).json({ error: 'last message must be from the user' }); return;
  }

  const client = new Anthropic();
  const used = [];
  const actions = [];
  try {
    for (let i = 0; i < 6; i++) {
      const response = await client.beta.messages.create({
        model: process.env.SONAR_CHAT_MODEL || 'claude-opus-5-5',
        max_tokens: 1600,
        output_config: { effort: 'medium' },
        betas: ['server-side-fallback-2026-07-01'],
        fallbacks: 'default',
        system: systemPrompt(who),
        tools: toolDefs,
        messages,
      });
      const toolUses = response.content.filter(b => b.type === 'tool_use');
      if (response.stop_reason !== 'tool_use' || !toolUses.length) {
        const answer = response.content.filter(b => b.type === 'text').map(b => b.text).join('\n').trim();
        res.status(200).json({ answer: answer || 'I could not produce an answer — try rephrasing.', used, actions });
        return;
      }
      messages.push({ role: 'assistant', content: response.content });
      messages.push({
        role: 'user',
        content: toolUses.map(tu => {
          used.push(tu.name);
          let result;
          try { result = TOOLS[tu.name] ? TOOLS[tu.name].run(tu.input || {}, who, actions) : { error: 'unknown tool' }; }
          catch (e) { result = { error: String(e && e.message || e) }; }
          return { type: 'tool_result', tool_use_id: tu.id, content: JSON.stringify(result) };
        }),
      });
    }
    res.status(200).json({ answer: 'That took too many steps to resolve — try a more specific question.', used });
  } catch (err) {
    const status = err && err.status;
    if (status === 401) { res.status(502).json({ error: 'bad_key' }); return; }
    if (status === 429) { res.status(429).json({ error: 'rate_limited' }); return; }
    console.error('ask error', err);
    res.status(502).json({ error: 'upstream', detail: String(err && err.message || err).slice(0, 300) });
  }
}
