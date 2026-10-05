#!/usr/bin/env python3
"""Fetch Highland's Affinity relationship edges for UNTRACKED H2C backers.

Driven by data/enrich/backer-domains.json (backer name -> {domain, kind, ...}).
For every fund-kind backer with a domain not yet in data/enrich/backer-rels.json:
  1. GET /persons?term=<domain>&with_interaction_dates=true
  2. keep real people whose email is at that domain
  3. GET /relationships-strengths?external_id=<id>
  4. store {internal, external, externalEmail, score, last, meet} per domain

Merge-writes backer-rels.json (existing domains kept; pass --refresh to refetch
all). Reads AFFINITY_API_KEY; exits 0 untouched without it.
"""
import datetime
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fetch_affinity_rels import get, persons_at, internal_name, _decay  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TODAY = datetime.date.today()

if not os.environ.get("AFFINITY_API_KEY"):
    print("AFFINITY_API_KEY not set — keeping committed backer edges")
    sys.exit(0)

import time  # noqa: E402

DOMS = os.path.join(ROOT, "data/enrich/backer-domains.json")
OUT = os.path.join(ROOT, "data/enrich/backer-rels.json")

domains = {}
try:
    for name, meta in json.load(open(DOMS)).items():
        d = (meta.get("domain") or "").lower().removeprefix("www.")
        if d and meta.get("kind") != "person":
            domains[d] = name
except FileNotFoundError:
    pass
for d in sys.argv[1:]:
    if d != "--refresh":
        domains[d.lower()] = d

out = {}
if "--refresh" not in sys.argv:
    try:
        out = json.load(open(OUT))
    except FileNotFoundError:
        pass

todo = [d for d in sorted(domains) if d not in out]
print(f"{len(domains)} backer domains, {len(todo)} to fetch")
done = failed = 0
for dom in todo:
    try:
        rels = []
        for p in persons_at(dom):
            ia = p.get("interaction_dates") or {}
            last = (ia.get("last_interaction_date") or "")[:10] or None
            meet = (ia.get("last_event_date") or "")[:10] or None
            if not last:
                continue
            strengths = get(f"/relationships-strengths?external_id={p['id']}")
            time.sleep(0.07)
            name = " ".join(filter(None, [p.get("first_name"), p.get("last_name")]))
            email = next((e for e in (p.get("emails") or [])
                          if e.lower().endswith("@" + dom)), p.get("primary_email"))
            for s in strengths or []:
                sc = s.get("strength") or 0
                if sc < 0.05:
                    continue
                rels.append({"internal": internal_name(s["internal_id"]),
                             "external": name, "externalEmail": email,
                             "score": round(sc, 2), "last": last, "meet": meet})
        rels.sort(key=lambda r: -(r["score"] * _decay(r["last"])
                                  * (1.0 if r["meet"] else 0.75)))
        out[dom] = {"fetched": TODAY.isoformat(), "rels": rels[:20]}
        done += 1
        print(f"{dom}: {len(rels)} edges")
        if done % 10 == 0:
            json.dump(out, open(OUT, "w"), ensure_ascii=False, indent=1)
    except Exception as e:  # noqa: BLE001
        failed += 1
        print(f"FAILED {dom}: {e}")
json.dump(out, open(OUT, "w"), ensure_ascii=False, indent=1)
print(f"fetched {done} domains, {failed} failed -> {OUT}")
sys.exit(1 if (failed and not done) else 0)
