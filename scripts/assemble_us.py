"""Assemble the US-tier-1-in-Europe region entities from data/us/*.

Funds only (no angels in v1). Relevance uses the eu_deals_24m variant so
US giants are scored on their European early-stage activity, not their
(near-zero) European portfolio share.
"""
import math, os
from coverage_common import (relevance, bucket_pipeline, harmonic_cells, top_people,
                             points_from, load_json, clean_rels, dedup_key)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SLUG = {
    "Sequoia Capital": "sequoia", "Andreessen Horowitz": "a16z", "a16z": "a16z",
    "Lightspeed Venture Partners": "lightspeed", "General Catalyst": "general-catalyst",
    "Accel": "accel-us", "Bessemer Venture Partners": "bessemer",
    "Index Ventures": "index-us", "Coatue": "coatue", "Founders Fund": "founders-fund",
    "Khosla Ventures": "khosla", "Greenoaks": "greenoaks", "Thrive Capital": "thrive",
    "Kleiner Perkins": "kleiner-perkins", "Felicis": "felicis", "NEA": "nea",
    "Benchmark": "benchmark", "Greylock": "greylock", "First Round Capital": "first-round",
    "CRV": "crv", "Initialized": "initialized", "Craft Ventures": "craft",
    "Spark Capital": "spark", "Union Square Ventures": "usv",
    "Insight Partners": "insight", "IVP": "ivp", "Y Combinator": "ycombinator",
    "Base10": "base10", "Haun Ventures": "haun", "8VC": "8vc", "Redpoint": "redpoint",
}


def assemble(team):
    team_order = [m["name"] for m in team]
    investors = load_json(f"{ROOT}/data/us/investors.json")
    if not investors:
        return []
    connections = {int(k): v for k, v in (load_json(f"{ROOT}/data/us/connections.json") or {}).items()}
    coinvest = {c["name"]: c for c in (load_json(f"{ROOT}/data/us/coinvestments.json") or [])}
    affdir = f"{ROOT}/data/us/affinity"

    entities = []
    for inv in investors:
        name = inv["name"]
        slug = SLUG.get(name) or inv.get("slug")
        aff = load_json(f"{affdir}/{slug}.json", {"pipeline": [], "relationships": []})
        rels = clean_rels(aff.get("relationships"))
        aff_max = max((r.get("score") or 0 for r in rels), default=0)
        aff_strong = sum(1 for r in rels if (r.get("score") or 0) >= 0.5)

        conn = connections.get(inv.get("company_id"))
        cells, li = harmonic_cells(conn, team_order)
        max_cell = max(c["score"] for c in cells.values())
        total_w = sum(c["score"] for c in cells.values())
        harmonic_raw = 0.7 * math.sqrt(max_cell) + 0.3 * math.sqrt(total_w)
        rel = relevance(inv, eu_deals_24m=inv.get("eu_deals_24m"))

        tp = top_people(cells, rels)
        for p in tp:
            for k in p["contacts"]:
                if not k.get("linkedin"):
                    k["linkedin"] = li.get(dedup_key(k["person"]))
        pts = points_from(rels, cells, li)

        co = coinvest.get(name)
        entities.append({
            "name": name, "slug": slug, "kind": "fund",
            "category": inv.get("category") or ("growth" if inv.get("growth_shadow") else "vc"),
            "li": None,
            "city": (inv.get("city") or "") + (f" · {inv['cc']}" if inv.get("cc") else ""),
            "note": None,
            "num_investments": inv.get("num_investments"), "unicorns": inv.get("num_unicorns"),
            "last_investment": inv.get("last_investment"),
            "relevance": rel, "top_people": tp, "points": pts,
            "harmonic_raw": harmonic_raw, "aff_max": aff_max, "aff_strong": aff_strong,
            "buckets": bucket_pipeline(aff.get("pipeline")),
            "coinvest": (co or {}).get("company_names", []),
            "dormant": aff.get("dormant"),
        })
    return entities
