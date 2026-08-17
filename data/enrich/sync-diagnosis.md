# Affinity sync diagnosis — 2026-08-17

Scope: why our per-fund pipelines (derived by matching fund names against the enriched
`affinity-data-investors` field on Highland Companies list 9387) diverge from what
Affinity shows. List size at time of check: **24,537 entries** (5,370 with funnel = Lead).

## 1. Acton Capital ("Affinity shows 22 Lead, we show 17")

Method: server-side keyword search of the term "acton" scoped to the
`affinity-data-investors` field on list 9387 (substring semantics — catches
"Acton Capital", "Acton Capital Partners", "Acton Capital Partners GmbH",
"Headline And Acton", etc.). This is strictly broader than any has-any-of
exact-value filter the Affinity UI applies.

Result: **34 entries** mention Acton in investors, of which **exactly 17 are funnel
= "Lead" today**:

JUPUS, Formalize, paretos, remberg, Jus Mundi, Hublo, Yoto, Plantura, 7Learnings,
Metalshub, Convelio, Laserhub, COMATCH, audibene, Tictail, Linas Matkasse, Windeln.de

Comparison with our stored `data/affinity/acton.json` (35 entries, 14 "Lead" +
3 "Qualified Lead" + 1 "Reach Out Now" + 1 "Pre-lead" + 5 Deprioritised + 11 Passed):

- **Our Lead bucket (Lead + Qualified Lead + Deal = 17) is exactly the same 17
  companies Affinity shows as Lead today.** No Lead-status entry present in Affinity
  is missing from our file. The count "we show 17" is correct and matches live
  Affinity's 17.
- **The "Qualified Lead" funnel option no longer exists** on list 9387 (current
  options: Pre-lead, Reach Out Now, Awaiting Reply, Hard to crack, Lead, Deal,
  Portfolio Company, Deprioritised (free for all), Passed). The three companies we
  stored as "Qualified Lead" (JUPUS, Hublo, Yoto) are now plain "Lead" — the option
  was merged/renamed after our pull. Our stored funnel labels are stale but bucket
  correctly.
- **iwoca** is in our file (Passed) but no longer matches "acton" in live investors —
  Affinity's enrichment dropped the Acton string since our pull. Enrichment data
  drifts over time; snapshots go stale.
- **The "22" cannot be reproduced from live data.** Even widening the keyword search
  to description fields, funnel = Lead + "acton" returns exactly 17. Candidate
  explanations, in order of likelihood:
  1. The Affinity view counted a broader status set — notably Lead (17) +
     Deprioritised (free for all) (5) = **22 exactly**. If the user's saved view
     groups or colour-codes statuses, Deprioritised rows may be being read as part
     of the Lead group.
  2. The count was taken at an earlier date, before recent funnel-status moves
     (statuses demonstrably changed recently: the Qualified Lead merge, iwoca's
     enrichment drift).
  3. A UI search box query (matches across more fields than investors) rather than
     an investors-column filter.

  → Recommend asking exactly which view/filter produced 22; live API data supports 17.

Root-cause takeaways for the app:
- Local substring matching against a stored snapshot was NOT the problem for Acton —
  the snapshot itself matched. The problems are (a) snapshot staleness (statuses and
  investor arrays change weekly), and (b) status-label drift ("Qualified Lead" no
  longer exists; keep bucketing by rank/dropdownOptionId, not by text).

## 2. Spot-checks: tracked companies our per-fund matching missed

All three ARE on the Highland Companies list; all three have sparse
`affinity-data-investors` values that omit the fund we filed them under. Investor
name matching can never find them — the enrichment field is incomplete, not our
matcher.

### CarOnSale (under Northzone)
- Affinity company id 289769140, list entry 107475084, domains caronsale.de / caronsale.com
- Funnel: **Deprioritised (free for all)** — owner: William De Quant — Berlin, Germany
- investors = **["Creandum"]** only.
- Why we missed it: **"Northzone" does not appear in the investors field at all**,
  even though Northzone is on the cap table (per Harmonic/press). Affinity's
  affinity-data enrichment lists only one investor for a company that has raised
  multiple rounds.

### Dalma (under Project A)
- Affinity company id 289770175, list entry 45102053, domain dalma.co
- Funnel: **Lead** — owner: William De Quant — Paris, France
- investors = **["Breega", "BPI France"]**
- Why we missed it: **"Project A" absent from investors** despite Project A having
  led/participated in Dalma's rounds. Same enrichment gap.

### Lyceum (under 10x Founders)
- Affinity company id 305791437, list entry 215621645, domain lyceum.technology
- Funnel: **Lead** — owner: William De Quant — Dresden, Germany
- investors = **["Redalpine"]**
- Why we missed it: **"10x Founders" absent from investors**. Same enrichment gap.

## 3. Systemic root causes (ranked)

1. **`affinity-data-investors` is incomplete and drifts.** It frequently lists a
   subset (sometimes one) of a company's actual investors, and values are added AND
   removed over time (iwoca). Any per-fund pipeline derived solely from this field
   under-counts, and any tracked/untracked judgement derived from "did the fund
   match" is wrong: a company can be tracked in Affinity while carrying none of the
   fund's name strings.
2. **Tracked-vs-untracked must be decided by list membership via domain/company id**
   against the full list dump (`data/affinity/_list-entries.json`), never by whether
   the investor match found the company.
3. **Fund attribution needs a second source** (e.g. Harmonic cap-table data) OR
   Affinity-side keyword search per fund (`search.fieldIds=[affinity-data-investors]`,
   substring semantics) instead of client-side matching on stale snapshots.
4. **Status text drift**: bucket funnel by dropdownOptionId/rank
   (61284=Lead r5, 61285=Deal r6, 2512885=Pre-lead r1, 5528570=Reach Out Now r2,
   2365120=Awaiting Reply r3, 108724=Hard to crack r4, 61289=Portfolio Company r7,
   4323670=Deprioritised r8, 61290=Passed r9), not by hard-coded text lists that
   include retired options like "Qualified Lead".

## 4. Full-dump verification (data/affinity/_list-entries.json)

The complete list was dumped on 2026-08-17 (24,537 entries — exact match with the
list's totalCount; 0 duplicates, 0 malformed rows). Funnel distribution:
Pre-lead 5,422 · Reach Out Now 152 · Awaiting Reply 1,379 · Hard to crack 328 ·
Lead 5,369 · Deal 37 · Portfolio Company 20 · Deprioritised 6,532 · Passed 5,282 ·
unset 16. Only 13,258 of 24,537 entries (54%) have ANY value in
affinity-data-investors — i.e. ~46% of tracked companies can never be surfaced by
investor-name matching regardless of matcher quality.

Local case-insensitive scan of the full dump confirms the Acton finding: exactly
34 entries mention "acton" in investors, of which exactly 17 are Lead — identical
to the server-side keyword search and to our stored file's Lead bucket. Nothing
was missed by keyword search; there is no hidden set of extra Acton Leads in the
data.

Transport note: the dump was produced via a temporary n8n workflow
"Affinity List 9387 Compact Dump B" (Hackathon project, workflow cEQdOXizG91eHbpR,
webhook-triggered, uses the "Affinity Bearer Token - Abhishek" credential against
the Affinity v2 API, 25 pages x 100 entries per run). It is left unpublished and
can be re-run for future refreshes or deleted.
