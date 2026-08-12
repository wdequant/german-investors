# Highland VC Connectivity Map — Germany

A tool that visualises Highland Europe's connectivity into a country's early-stage VC
ecosystem, starting with Germany. For every fund/angel that matters it answers:

1. **How relevant are they** to businesses Highland may eventually invest in?
2. **How well do we cover them** — and who is the best-connected Highland person?
3. **Have we co-invested** with them before?
4. **Where does their portfolio sit in our pipeline** (pre-lead → reach out → awaiting
   reply → lead → hard to crack), with Affinity links per company?

Live map: `viz/index.html` (published as a Claude artifact; same URL redeployed on rebuild).

## Universe (v2)

- Source: Harmonic saved search `urn:harmonic:saved_search:245331` (74 German investors),
  full pull in `data/germany-investors.json`.
- Condensed to the **top 30 VC/CVC/state funds** by a hybrid score:
  `½ · normalised(investment count) + ½ · normalised(unicorn count)`.
- Plus **9 super-angels**: Götze, Renner, Göllner, Hilpert (from the saved search) +
  Klöckner, Vollmann, Pausder, Koç, Reber (resolved directly in Harmonic).
- Excluded: corporates investing off balance sheet (Siemens, Bosch, Axel Springer, …),
  the mis-mapped "GV" record, and everything outside the top-30 cut.

## Data layers

| Layer | Source | Files |
|---|---|---|
| Fund stats (stage/sector/activity/unicorns) | Harmonic saved search | `data/germany-investors.json` |
| Team network (who knows whom, per teammate, with LinkedIn) | Harmonic `get_company_connections` / `get_person_connections`, 18 investment-team users | `data/connections.json`, `data/highland-team.json` |
| Co-investment history | Harmonic co-investor record for Highland Europe | `data/coinvestments.json` |
| Partnership relationships (incl. Laurence, Fergal, Ronan — no Harmonic sync needed) | Affinity `get_company_relationships` / `get_person_relationships` | `data/affinity/<slug>.json` |
| Pipeline overlap by funnel stage | Affinity list 9387 ("Highland Companies"), `Funnel` field `field-81237`, filtered on the enriched `Investors` field | `data/affinity/<slug>.json` |

## Scores

- **Relevance (0–100)** — funds only: stage fit (Seed/A entry, 30) + sector fit vs the
  software/internet thesis (30) + activity recency (20) + graduation quality (20).
- **Coverage (0–100)**: `0.55 · harmonic + 0.45 · affinity`, where harmonic = normalised
  (0.7·√best-teammate-cell + 0.3·√team-total; cell = Σ contact-seniority × source-weight)
  and affinity = max partnership interaction score + 0.06 per strong (≥0.5) relationship.
- **Colour coding** replaces the old gap flag: fund names render green (≥50), amber
  (22–49) or red (<22) by coverage.
- Funnel buckets: Lead includes Qualified Lead and Deal; Passed/Deprioritised only in
  the drill-down.

## Rebuild

```
python3 scripts/build_viz3.py   # regenerates viz/index.html from data/ (v3 app-frame design)
```

`scripts/build_viz.py` (v1 heatmap) and `scripts/build_viz2.py` (v2 cards) are kept for reference; the v3 template lives in `scripts/viz3_template.py`.

## Caveats

- Harmonic network only sees synced users; Fergal/Laurence appear via Affinity only.
- Pipeline matching relies on Affinity's enriched Investors text (alias lists per fund);
  a fund written differently in Affinity than our aliases will be missed.
- Affinity person records don't exist for most of the super-angels — their coverage
  score is genuinely near-zero, which is itself the finding.
- Affinity company links assume the `highlandeurope.affinity.co` workspace URL.
