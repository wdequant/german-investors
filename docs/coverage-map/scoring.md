# Coverage Map scoring — self-assessment (Oct 9, 2026)

Will asked: *"Do a self assessment on the weights / scoring, are you happy, is there a
way to simplify."* This is the honest answer, written against the live build.

## The whole model on one page

Five numbers, each with one job:

| Score | Question it answers | Formula |
| --- | --- | --- |
| **R** (person edge, 0–100) | How real is this relationship? | `0.75·AffinityStrength + 25·e^(−days/180)`. Harmonic-only edges: flat 38 (email/calendar) or 28 (LinkedIn-only). |
| **cu / CT** (fund coverage) | Can you (or the team) get into this fund? | Noisy-OR over people-edges, seniority-weighted (Partner .95, Director .75, Associate .40, unknown .55). |
| **O** (fund opportunity) | Does this fund matter to Highland? | `0.5·relevance + 0.5·percentile(deal-flow weight)`. |
| **covu / covT** (area verdict) | Open ground / building / well covered | O-weighted average of cu over the shortlist. |
| **Doors rank** | Which contact is worth the most here? | `(R/100) · (0.45 + 0.55·O/100) · seniority`. |

Everything else (`Gu`, `M`, build/maintain states, warm/cold tags) is derived from those
five with a single threshold: **50**.

## What I'm happy with

- **R is honest and explainable.** Affinity's own composite plus recency decay; no magic.
  Every surfaced edge traces back to a logged interaction or a Harmonic-verified connection.
- **Noisy-OR for fund coverage** is the right shape: knowing two partners ≈ knowing the
  fund; knowing five associates ≠ knowing the fund. Seniority weights now rest on
  Harmonic-verified titles (the overnight sweep closes the remaining gaps).
- **Qualitative verdicts over percentages** — the tier words carry the product; the numbers
  stay one click down. The single 50-bar is easy to say out loud: *half the
  opportunity-weighted shortlist covered = well covered.*
- **Shortlist-weighted area rollups**: a long tail can't drag the verdict, and pins/removes
  give curation the last word.

## Known warts (documented, deliberately not papered over)

1. **Deal-flow percentile mixes measurement regimes.** Nordic deal counts come from
   Affinity-observed flow; UK/US counts from Harmonic 18-month pulls, which run richer.
   Percentiles are computed across all regions, so UK/US funds crowd the top of the
   deal-flow half of O. It cancels out *within* a region (verdicts are fine) but makes
   cross-region O comparisons ~10–15% generous to the newer regions. Fix when it matters:
   percentile within region, or re-pull Nordic deal flow from Harmonic the same way.
2. **Harmonic-layer edges are flat (38/28) regardless of activity.** A person you email
   monthly (below Affinity's radar) scores the same as one you met once in 2023. The data
   to fix it exists (Harmonic correspondence dates) — one enrichment pull away.
3. **Stage weighting of pipeline (prelead 1 / awaiting 2 / lead 3 / hard 2)** is spec-inherited
   and plausible but untested; it only shapes the Gu/doors ordering, not the verdicts.

## Simplifications made tonight

- **One threshold everywhere.** The team tiers used 55 where the personal tiers used 50;
  aligned both (and the intro-ready copy gates) at 50. One bar, one story.
- **Removed the `M` momentum score** from the docs narrative: it's `Gu` with a small warm-path
  boost and only orders the Build list. It stays in code (it does its one job) but is no
  longer presented as a separate concept.

## What I would *not* simplify

Collapsing R/cu/O into one "score" would read simpler but lie more — the three questions
(real relationship? reachable fund? fund worth reaching?) move independently, and the
product's best moments (Open ground + strong team = ask for the intro) come precisely from
keeping them apart.
