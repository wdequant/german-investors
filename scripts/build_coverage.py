#!/usr/bin/env python3
"""Build the multi-region coverage map (Germany + Nordics) -> viz/index.html"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from coverage_common import (finalize, TODAY, AFFINITY_ORG, load_json, apply_enrich,
                             compute_bridges_and_synd, build_htc, angel_relevance,
                             affinity_sync, inject_htc_captables)
import assemble_germany, assemble_nordics, assemble_france
import importlib.util as _ilu

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
team = load_json(f"{ROOT}/data/highland-team.json")
roster = [m["name"] for m in team] + ["Fergal Mullen", "Laurence Garrett", "Ronan Shally"]

empflags = load_json(f"{ROOT}/data/enrich/employment-flags.json", {})
htc_owners = load_json(f"{ROOT}/data/enrich/htc-owners.json", {})
aff_dump = load_json(f"{ROOT}/data/affinity/_list-entries.json", {})
angel_deals = load_json(f"{ROOT}/data/enrich/angel-deals.json", {})

pmeta_germany = {}
for part in ("a", "b"):
    for slug, d in (load_json(f"{ROOT}/data/enrich/partners-meta-germany-{part}.json", {}) or {}).items():
        pmeta_germany.setdefault(slug, {}).update(d)
pmeta_france = {}
for part in ("a", "b"):
    for slug, d in (load_json(f"{ROOT}/data/enrich/partners-meta-france-{part}.json", {}) or {}).items():
        pmeta_france.setdefault(slug, {}).update(d)
PMETA = {"germany": pmeta_germany,
         "nordics": load_json(f"{ROOT}/data/enrich/partners-meta-nordics.json", {}) or {},
         "france": pmeta_france}


def merge_10x(ents):
    """10x Group is the predecessor angel vehicle of 10x Founders (same GPs) —
    fold its Affinity pipeline into 10x Founders and drop the duplicate row."""
    g = next((e for e in ents if e["slug"] == "10x-group"), None)
    f = next((e for e in ents if e["slug"] == "10x-founders"), None)
    if g and f:
        seen = {p["id"] for k in f["buckets"] for p in f["buckets"][k]}
        for k, lst in g["buckets"].items():
            f["buckets"].setdefault(k, []).extend(p for p in lst if p["id"] not in seen)
        f["coinvest"] = sorted(set(f["coinvest"]) | set(g["coinvest"]))
        f["aff_max"] = max(f["aff_max"], g["aff_max"])
        f["aff_strong"] = max(f["aff_strong"], g["aff_strong"])
        f["harmonic_raw"] = max(f["harmonic_raw"], g["harmonic_raw"])
        if not f.get("dormant"):
            f["dormant"] = g.get("dormant")
        ents.remove(g)
    return ents

REGION_CFG = {
    "germany": {"label": "Germany", "adj": "German", "assemble": assemble_germany.assemble},
    "nordics": {"label": "Nordics", "adj": "Nordic", "assemble": assemble_nordics.assemble},
    "france": {"label": "France", "adj": "French", "assemble": assemble_france.assemble},
}

regions = {}
for key, cfg in REGION_CFG.items():
    ents = cfg["assemble"](team)
    if not ents:
        continue  # region data not yet collected
    if key == "germany":
        ents = merge_10x(ents)
    if key == "france":  # france agents write split fragments to avoid collisions
        enrich = {"funds": load_json(f"{ROOT}/data/enrich/france-funds.json", {}) or {},
                  "angels": load_json(f"{ROOT}/data/enrich/france-angels.json", {}) or {}}
        recency = {**(load_json(f"{ROOT}/data/enrich/recency-france-a.json", {}) or {}),
                   **(load_json(f"{ROOT}/data/enrich/recency-france-b.json", {}) or {})}
    else:
        enrich = load_json(f"{ROOT}/data/enrich/{key}.json", {})
        recency = load_json(f"{ROOT}/data/enrich/recency-{key}.json", {})
    apply_enrich(ents, enrich, recency, empflags, key, PMETA.get(key))
    added_by, rescued = affinity_sync(ents, aff_dump, key)
    htc_added = inject_htc_captables(ents, load_json(f"{ROOT}/data/enrich/htc-captables.json", {}),
                                     htc_owners)
    if htc_added:
        print(f"  [{key}] harmonic cap tables: +{htc_added} hard-to-crack links")
    if added_by or rescued:
        print(f"  [{key}] affinity sync: +{sum(added_by.values())} pipeline entries "
              f"across {len(added_by)} funds; rescued from 'untracked': "
              f"{sum(len(v) for v in rescued.values())} ({', '.join(n for v in rescued.values() for n in v[:2])[:120]})")
    finalize(ents)
    compute_bridges_and_synd(ents)
    # angel relevance + gap (needs syndication + pipeline counts)
    for e in ents:
        if e["kind"] == "angel":
            e["notable"] = (angel_deals.get(key) or {}).get(e["slug"]) or []
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
