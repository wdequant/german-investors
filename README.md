# Highland VC Connectivity Map — Germany

A tool that visualises Highland Europe's connectivity into a country's early-stage VC
ecosystem, starting with Germany. For every relevant early-stage fund it answers:

1. **Who is the best-connected Highland investor into this fund?**
2. **Have we co-invested with this fund before?**
3. **Where are our coverage gaps?** (relevant fund × weak relationships → highlighted)

## Data sources (validated)

| Question | Source | Status |
|---|---|---|
| Universe of German funds | Harmonic saved search `urn:harmonic:saved_search:245331` (74 investors) | ✅ pulled → `data/germany-investors.json` |
| Who knows whom at each fund | Harmonic `get_company_connections` — per-teammate connections into fund personnel, with sources (EMAIL / CALENDAR / LINKEDIN) and the contact's role at the fund | ✅ validated (Cherry Ventures: 25 connected people across 7+ Highland team members) |
| Co-investment history | Harmonic `get_investors` on Highland Europe (`urn:harmonic:investor:198178`) with `co_investors` field group — 331 co-investors incl. HV (4 shared companies), HTGF (3), Atlantic Labs (2), DvH (2) | ✅ validated |
| Relationship recency/strength (optional enrichment) | Harmonic `connection_fields: correspondence` (latest email + meeting per teammate) and/or Affinity relationship data | ⬜ decide |

## Methodology

### 1. Relevance score — "is this a fund we should have covered?"

Filters first (drop or tag):
- **Bad records** — e.g. `GV` (urn 131890…142901) is a mis-mapped record (Google Ventures
  stats attached to a Ludwigsburg company). Manual exclude list.
- **Entity type** — tag angels (Götze, Renner, Göllner, Hilpert), corporate balance-sheet
  investors (Siemens, Bosch, Axel Springer, Deutsche Börse, Döhler), and state/public funds
  (HTGF, Bayern Kapital, IBB) separately from institutional VCs. Default view = institutional
  VC + dedicated CVC funds; toggles for the rest.

Then score each remaining fund 0–100 on "produces companies Highland would fund later":
- **Stage fit (30%)** — entry stage focus is Seed / Series A (the sweet spot: their winners
  raise the Series B/C growth rounds Highland leads).
- **Sector fit (30%)** — share of portfolio in software / internet / tech sectors Highland
  invests in (Communications & IT, Business Services, FinServ software, …). Penalise pure
  crypto (1kx, Moonrock, Inflection.xyz) and pure biotech (OCCIDENT, Amino, MIG) portfolios.
- **Activity (20%)** — new investments in the last 12 months; most recent investment date.
- **Graduation quality (20%)** — how often their portfolio raises downstream growth rounds
  (unicorn count, follow-on/graduation signals; can be computed precisely from portfolio
  funding data later).

### 2. Connectivity score — per (fund × Highland investor)

From `get_company_connections` on each fund's company URN:
- Count distinct people known at the fund, weighted by **contact seniority** (Partner/GP > Principal > Associate > non-investment staff)
- Weight by **connection source** (CALENDAR+EMAIL ≫ LINKEDIN-only)
- Optional: recency of last interaction via `correspondence` fields

Fund-level connectivity = max over Highland investors (who's the door-opener), plus breadth
(how many of us know them).

### 3. Co-investment flag

From Highland's co-investor list: shared portfolio companies per fund → strongest possible
relationship signal, displayed as a badge with the shared company names.

### 4. Gap highlighting

`gap = relevance × (1 − normalised connectivity)`. High-relevance, low-connectivity funds
get the red treatment.

## Repo layout

- `docs/harmonic-api-reference.md` — Harmonic API reference (uploaded)
- `data/germany-investors.json` — the 74 funds from the saved search, with stage/sector/
  activity stats (names resolved via `get_investors`)
- Next: `data/connections/` (per-fund network pulls), scoring script, visualisation

## Open questions

See the discussion in the working session — key decisions: exact relevance weights,
Harmonic-vs-Affinity as the relationship source of truth, and visual design (matrix/heatmap
vs. network graph).
