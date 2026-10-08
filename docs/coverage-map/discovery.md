# Coverage Map — discovery: spec → real Sonar schema

Oct 8, 2026. Maps every entity in spec §5 to what Sonar actually holds, lists gaps, and records
the architectural adaptations §0/§10 permit ("match Sonar's existing stack").

## How Sonar is actually built (vs the spec's assumptions)

Sonar is **not** a React app with an API and a database. It is:

- `scripts/build_coverage.py` + `scripts/coverage_common.py` → compute everything offline
  (nightly CI at 05:30 UTC + on demand) and emit **one static payload** (`const D = {...}`)
  baked into a single-file SPA (`viz/index.html`, template in `scripts/coverage_template.py`).
- The only server code is `deploy/api/ask.js` (chat) + `login.js` (password gate) on Vercel.
- No client framework, no external JS deps, no tile servers. All heavy computation happens
  at build time in Python; the client renders prebuilt JSON.

**Adaptation (spec §10):** the "nightly scoring job" is a new build-time module
(`scripts/coverage_map.py`) called from `build_coverage.py`; the "Coverage API" is a
precomputed `D.covmap` payload section; the "scores store" is the payload plus monthly
snapshot JSONs under `data/enrich/covmap-snapshots/`. Map rendering is hand-rolled SVG with
**all geometry projected and all bubble layouts packed at build time in Python** — the client
only draws, animates the viewBox between zoom levels, and swaps lenses. No d3 needed, no CDN,
single-file constraint preserved. `config/regions.ts` / `config/scoring.ts` become
`REGION_DEF` / `SCORING` dicts at the top of `scripts/coverage_map.py`.

## Entity mapping (spec §5 → real schema)

| Spec entity | Real location | Notes |
| --- | --- | --- |
| User | `D.roster` (21 names); viewer chosen via who-chip / `ap.who` | No auth identities; `?as=` equivalent is the existing "Acting as" select |
| Fund | `D.regions[rk].entities` (kind `fund`, 111) + angels (kind `angel`, 38) | `category` (vc/cvc/pe/fo/state/accelerator/angel), `tier`, `relevance.{total,stage,sector,geo,activity,europe,thesis,unframe}`, curated by construction |
| Fund type/stage (untracked firms) | `data/enrich/fund-meta.json` (618 firms, type + stage focus) | Built Oct 8 |
| Office | **Does not exist.** Fund has one `city` ("Stockholm · SE" — country code embedded) | v1 places each fund at its single curated city; multi-office split (§6.6) deferred, flagged below |
| Contact | `top_people[].contacts[]` per fund (`person`, `pct`, `last`, `meet`, `email`, `linkedin`, `ever`) + `D.mynet[user][]` (`n,f,s,g,p,l,m,e,v,t,sr,c,ft,fs`) | `sr` (Partner/Director/Associate) + `t` (title) + `c` (city) from `data/enrich/person-meta.json` (1,868 Harmonic-classified people) |
| Relationship edge | Affinity composite `pct` (0–100) + `last`/`meet` dates; Compass calendar edges (meetings count → `p`, `src:'cal'`) | **Gap:** no per-edge emails-12m / reciprocity / interaction-type history → spec §6.1 components Freq/Depth/Recip are not computable. See scoring adaptation |
| Deal flow link | `fund.dealflow[]` (name, country, date, round, `funnel` = Affinity status of the invested company) + `fund.coinvest[]` + `fund.uf.high` (backs high-priority pipeline cos) | Dates present → 12m windows work |
| Pipeline company | `fund.buckets.{prelead,reachout,awaiting,lead,hard,portfolio}[]` each with `own:[users]`, country, city | Powers P_u directly |
| Region prefs | **New**: `localStorage sonar_mapprefs` (client-side), M1 hard-codes Nordics = 1.0 | No server-side user store exists; acceptable for a personal tool |
| Snapshots | **New**: monthly JSON written by build when month changes | **Gap:** cannot back-fill 12 months (interaction history is not retained), trend starts accruing now. Flagged |

## Scoring adaptations (spec §6 → computable form)

- **R(user, contact)** — spec wants 0.4·Rec + 0.3·Freq + 0.2·Depth + 0.1·Recip blended 50/50
  with Affinity strength. Freq/Depth/Recip don't exist. Affinity's `pct` already *is* a
  composite interaction-strength score, so: **R = 0.75·pct + 25·exp(−days since last touch /180)**
  (missing date → recency 0). Same tiers (Strong 70+ / Warm 40–69 / Weak 15–39 / Cold <15).
- **C_u / C_T (noisy-OR, §6.2)** — as specced, over `top_people` contacts. Seniority weight
  from person-meta `sr`: Partner 0.95, Director 0.75, Associate 0.40, unknown 0.55
  (spec's finer 7-level ladder needs titles we only partially hold; the 4 buckets we have are
  Harmonic-verified). Importance ×1.5 (§6.8) when the contact's fund backs one of my pipeline
  companies at lead stage or better.
- **O (§6.3)** — 0.5·`relevance.total` + 0.5·percentile(deal-flow score) where deal-flow score
  = Σ over `dealflow[]` in window: funnel ∈ {Lead, Qualified Lead, Deal, Hard to crack} → 2,
  other funnel → 1, no funnel → 0.25; plus 2 per co-investment. Spec §13's double-count
  question: `relevance.total` already contains an `activity` component (max 8 pts of 100) —
  small, so deal-flow half stays at 0.5, noted for tuning.
- **P_u / O_u / G_u (§6.8)** — stage weights on buckets: prelead/reachout 1, awaiting 2,
  lead 3, hard 2 (a hard-to-crack is active intent), portfolio 0.
- **States (§6.5/6.9), G, M (§6.4), area roll-ups (§6.6)** — exactly as specced.
- **Explainability (§6.7)** — each fund carries a `why` string + component list, built in Python.

## Geometry

Natural Earth 1:50m via `world-atlas` npm asset, subset to Europe, projected at build time
(Lambert azimuthal equal-area, centre 10°E 52°N) to a 1000×1150 px space; countries emitted as
SVG path strings (~1-decimal precision), cities from a hand-curated `CITY_LL` table in
`coverage_map.py`. No runtime projection, no tiles, asset cost ≈ 200KB inside the payload.

## Flagged for Will (spec §13 defaults in force)

1. **R formula simplified** as above — Affinity pct + recency only. Honest, explainable,
   but Freq/Depth/Recip need interaction-level ingestion we don't have (possible via Compass
   per-call counts later).
2. **No multi-office split** in v1: each fund sits at its curated city. London fund with a
   Stockholm partner stays in London until we hold per-person offices (person-meta `c` could
   drive this in v2).
3. **Trend back-fill impossible** — snapshots start accruing from first build.
4. **Bubble size = opportunity** (spec default) with no toggle in M1.
5. **Angels share the layer** as diamonds (spec default).
6. **Team view** = the existing team lens; no per-colleague share breakdown in M1.
7. Relevance already includes a small activity term (8/100) — deal-flow weight kept at 0.5.
8. Owen's Compass network map not reviewed (no access from this session); L3 built standalone
   as a two-column ego graph.
