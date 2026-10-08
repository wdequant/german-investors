"""Assemble the UK region entities from data/uk/* + data/enrich/uk-funds.json.

The UK universe was curated top-down (66 funds ranked in uk-funds.json, keyed by
domain) with Harmonic profiles in data/uk/investors.json (keyed by name). Coverage
blends the live Affinity relationship edges in data/uk/affinity/<slug>.json with
the Harmonic team-network dump in data/uk/connections.json (email, calendar and
LinkedIn connections per fund, same shape as the other regions).
"""
import math
import os
import re
from coverage_common import (relevance, bucket_pipeline, harmonic_cells, top_people,
                             points_from, load_json, clean_rels, dedup_key, net_from_cells)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

TYPE_CAT = {"VC": "vc", "CVC": "cvc", "PE": "pe", "State": "state",
            "Accelerator": "accelerator", "FO": "fo"}
SUB_CITY = {"LON": "London", "CAM": "Cambridge", "OXF": "Oxford",
            "EDI": "Edinburgh", "MAN": "Manchester"}

_nrm = lambda s: re.sub(r"[^a-z0-9]", "", (s or "").lower())


def assemble(team):
    team_order = [m["name"] for m in team]
    investors = load_json(f"{ROOT}/data/uk/investors.json") or []
    funds = load_json(f"{ROOT}/data/enrich/uk-funds.json") or {}
    slugmap = load_json(f"{ROOT}/data/uk/slug-map.json") or {}
    if not investors or not funds:
        return []
    connections = {int(k): v for k, v in (load_json(f"{ROOT}/data/uk/connections.json") or {}).items()}
    byname = {_nrm(v["name"]): d for d, v in funds.items()}

    def domain_of(name):
        k = _nrm(name)
        if k in byname:
            return byname[k]
        hits = [d for nk, d in byname.items() if k in nk or nk in k]
        return hits[0] if len(hits) == 1 else None

    affdir = f"{ROOT}/data/uk/affinity"
    entities = []
    for inv in investors:
        dom = domain_of(inv["name"])
        if not dom:
            continue
        meta = funds[dom]
        slug = slugmap.get(dom) or _nrm(meta["name"])[:30]
        aff = load_json(f"{affdir}/{slug}.json", {"pipeline": [], "relationships": []})
        rels = clean_rels(aff.get("relationships"))
        aff_max = max((r.get("score") or 0 for r in rels), default=0)
        aff_strong = sum(1 for r in rels if (r.get("score") or 0) >= 0.5)
        cid = int(inv["company_urn"].rsplit(":", 1)[1])
        cells, li = harmonic_cells(connections.get(cid), team_order)
        max_cell = max(c["score"] for c in cells.values())
        total_w = sum(c["score"] for c in cells.values())
        harmonic_raw = 0.7 * math.sqrt(max_cell) + 0.3 * math.sqrt(total_w)
        tp = top_people(cells, rels)
        for p in tp:
            for k in p["contacts"]:
                if not k.get("linkedin"):
                    k["linkedin"] = li.get(dedup_key(k["person"]))
        entities.append({
            "name": meta["name"], "slug": slug, "kind": "fund",
            "category": TYPE_CAT.get(meta.get("type"), "vc"),
            # the curated sub decides placement: Accel's Harmonic HQ is Palo Alto,
            # but its UK seat is London and that is what this map covers
            "city": SUB_CITY.get(meta.get("sub"), "London") + " · GB",
            "uk_sub": meta.get("sub") or "LON",
            "note": meta.get("note"),
            "num_investments": inv.get("num_investments"), "unicorns": inv.get("num_unicorns"),
            "last_investment": (inv.get("last_investment") or "")[:10] or None,
            "relevance": relevance(inv), "top_people": tp,
            "points": points_from(rels, cells, li),
            "harmonic_raw": harmonic_raw, "aff_max": aff_max, "aff_strong": aff_strong,
            "buckets": bucket_pipeline(aff.get("pipeline")),
            "coinvest": [], "dormant": aff.get("dormant"),
            "net": net_from_cells(cells),
        })
    return entities
