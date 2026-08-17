#!/usr/bin/env python3
"""Build the multi-region coverage map (Germany + Nordics) -> viz/index.html"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from coverage_common import (finalize, TODAY, AFFINITY_ORG, load_json, apply_enrich,
                             compute_bridges_and_synd, build_htc, angel_relevance)
import assemble_germany, assemble_nordics
import importlib.util as _ilu

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
team = load_json(f"{ROOT}/data/highland-team.json")
roster = [m["name"] for m in team] + ["Fergal Mullen", "Laurence Garrett", "Ronan Shally"]

empflags = load_json(f"{ROOT}/data/enrich/employment-flags.json", {})
htc_owners = load_json(f"{ROOT}/data/enrich/htc-owners.json", {})

REGION_CFG = {
    "germany": {"label": "Germany", "adj": "German", "assemble": assemble_germany.assemble},
    "nordics": {"label": "Nordics", "adj": "Nordic", "assemble": assemble_nordics.assemble},
}

regions = {}
for key, cfg in REGION_CFG.items():
    ents = cfg["assemble"](team)
    enrich = load_json(f"{ROOT}/data/enrich/{key}.json", {})
    recency = load_json(f"{ROOT}/data/enrich/recency-{key}.json", {})
    apply_enrich(ents, enrich, recency, empflags, key)
    finalize(ents)
    compute_bridges_and_synd(ents)
    # angel relevance + gap (needs syndication + pipeline counts)
    for e in ents:
        if e["kind"] == "angel":
            pipe_active = sum(len(e["buckets"][k]) for k in
                              ("prelead", "reachout", "awaiting", "lead", "hard"))
            synd = sum(1 for s in e.get("syndication", []) if s["tier"] == "strong")
            e["relevance"] = angel_relevance(e.get("num_investments"), e.get("unicorns"),
                                             synd, pipe_active)
            e["relevance"]["angel"] = True
            e["gap"] = round(e["relevance"]["total"] * (1 - e["connectivity"] / 100))
    regions[key] = {"label": cfg["label"], "adj": cfg["adj"], "entities": ents,
                    "htc": build_htc(ents, htc_owners)}

_spec = _ilu.spec_from_file_location("coverage_template",
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "coverage_template.py"))
_tpl = _ilu.module_from_spec(_spec); _spec.loader.exec_module(_tpl)

freshness = {
    "Harmonic universe & network": "12 Aug 2026",
    "Affinity relationships & pipeline": "17 Aug 2026",
    "Partner rosters, recent deals, recency": "17 Aug 2026",
}
payload = {"generated": TODAY.strftime("%d %b %Y"), "team": team, "roster": roster,
           "affinityOrg": AFFINITY_ORG, "regions": regions, "freshness": freshness}
html = (_tpl.TEMPLATE
        .replace("__DATA__", json.dumps(payload, ensure_ascii=False))
        .replace("__GENERATED__", payload["generated"]))
os.makedirs(f"{ROOT}/viz", exist_ok=True)
open(f"{ROOT}/viz/index.html", "w").write(html)
for k, r in regions.items():
    f = [e for e in r["entities"] if e["kind"] == "fund"]
    unt = sum(len(e.get("untracked") or []) for e in f)
    print(f"{k}: {len(f)} funds + {len(r['entities'])-len(f)} angels, "
          f"{len(r['htc'])} HTCs, {unt} untracked EU deals shown")
print(f"wrote viz/index.html ({len(html)//1024} KB)")
