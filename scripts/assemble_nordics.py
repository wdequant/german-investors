"""Assemble the Nordics region entities from data/nordics/*."""
import math, os
from coverage_common import (relevance, bucket_pipeline, harmonic_cells, top_people,
                             points_from, load_json, norm_name)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SLUG = {
    "Almi": "almi", "Antler": "antler", "Northzone": "northzone", "Creandum": "creandum",
    "Lifeline Ventures": "lifeline", "Industrifonden": "industrifonden",
    "Seed Capital": "seed-capital", "PSV": "psv", "Inventure": "inventure",
    "EQT Ventures": "eqt-ventures", "Sting": "sting", "Investinor": "investinor",
    "Icebreaker.vc": "icebreaker", "Startuplab": "startuplab", "Innovestor": "innovestor",
    "Alliance VC": "alliance-vc", "Norrsken": "norrsken", "byFounders": "byfounders",
    "Almi Invest": "almi-invest", "Accelerace": "accelerace", "Maki.vc": "maki",
    "Spintop Ventures": "spintop", "Luminar Ventures": "luminar",
    "Gorilla Capital": "gorilla", "First Fellow Partners": "first-fellow",
    "Voima Ventures": "voima", "Superhero Capital": "superhero",
    "Skyfall Ventures": "skyfall", "J12": "j12",
    "Ilkka Paananen": "ilkka-paananen", "Cristina Stenbeck": "cristina-stenbeck",
    "Ali Omar": "ali-omar", "Charlie Songhurst": "charlie-songhurst",
    "Sophia Bendz": "sophia-bendz", "Mattias Miksche": "mattias-miksche",
    "David Helgason": "david-helgason", "Hampus Jakobsson": "hampus-jakobsson",
    "Risto Siilasmaa": "risto-siilasmaa", "Sebastian Knutsson": "sebastian-knutsson",
}
ANGEL_NOTE = {
    "Ilkka Paananen": "CEO/co-founder Supercell, Illusian family office",
    "Cristina Stenbeck": "Kinnevik",
    "Ali Omar": "Med Group founder, 45+ startups",
    "Charlie Songhurst": "ex-Microsoft strategy, Katana; prolific Nordic-heavy angel",
    "Sophia Bendz": "ex-Spotify CMO, GP Cherry Ventures",
    "Mattias Miksche": "Stardoll founder, first-cheque angel",
    "David Helgason": "Unity founder, Transition climate VC",
    "Hampus Jakobsson": "TAT founder, GP Pale Blue Dot",
    "Risto Siilasmaa": "F-Secure founder, ex-Nokia chair, First Fellow",
    "Sebastian Knutsson": "King co-founder, Sweet Capital",
}


def assemble(team):
    team_order = [m["name"] for m in team]
    investors = load_json(f"{ROOT}/data/nordics/investors.json")
    connections = {int(k): v for k, v in (load_json(f"{ROOT}/data/nordics/connections.json") or {}).items()}
    angel_conn = load_json(f"{ROOT}/data/nordics/angel_connections.json") or {}
    coinvest = {c["name"]: c for c in (load_json(f"{ROOT}/data/nordics/coinvestments.json") or [])}
    affdir = f"{ROOT}/data/nordics/affinity"

    entities = []
    for inv in investors:
        name = inv["name"]
        slug = SLUG[name]
        kind = inv["kind"]
        prefix = "angel-" if kind == "angel" else ""
        aff = load_json(f"{affdir}/{prefix}{slug}.json", {"pipeline": [], "relationships": []})
        rels = [r for r in (aff.get("relationships") or [])]
        aff_max = max((r.get("score") or 0 for r in rels), default=0)
        aff_strong = sum(1 for r in rels if (r.get("score") or 0) >= 0.5)
        dormant = aff.get("dormant")

        if kind == "fund":
            conn = connections.get(inv["company_id"])
            cells, li = harmonic_cells(conn, team_order)
            max_cell = max(c["score"] for c in cells.values())
            total_w = sum(c["score"] for c in cells.values())
            harmonic_raw = 0.7 * math.sqrt(max_cell) + 0.3 * math.sqrt(total_w)
            rel = relevance(inv)
        else:
            # angels: harmonic person connections -> pseudo-cells (person-level, seniority=3)
            cells = {u: {"score": 0.0, "contacts": []} for u in team_order}
            ac = angel_conn.get(str(inv["person_id"])) or angel_conn.get(inv["person_id"])
            li = {norm_name(name): inv.get("linkedin")} if inv.get("linkedin") else {}
            if ac:
                from coverage_common import source_weight
                for v in ac.get("via", []):
                    u = v.get("user")
                    if u in cells:
                        w = 3.0 * source_weight(v.get("sources"))
                        cells[u]["score"] += w
                        cells[u]["contacts"].append({"person": name, "title": "angel",
                                                     "external": False, "linkedin": inv.get("linkedin"),
                                                     "sources": v.get("sources") or [], "w": round(w, 1)})
            max_cell = max(c["score"] for c in cells.values())
            total_w = sum(c["score"] for c in cells.values())
            harmonic_raw = 0.7 * math.sqrt(max_cell) + 0.3 * math.sqrt(total_w)
            rel = None

        tp = top_people(cells, rels)
        # attach linkedin from harmonic contacts where names match
        for p in tp:
            for k in p["contacts"]:
                if not k.get("linkedin"):
                    k["linkedin"] = li.get(norm_name(k["person"]))
        pts = points_from(rels, cells, li)
        if kind == "angel" and not pts and any(c["score"] > 0 for c in cells.values()):
            best = sorted(((c["score"], u) for u, c in cells.items()), reverse=True)[:3]
            pts = [{"external": name, "internal": u, "pct": None, "linkedin": inv.get("linkedin"), "src": "harmonic"}
                   for _, u in best if _ > 0]

        co = coinvest.get(name)
        entities.append({
            "name": name, "slug": slug, "kind": kind, "category": inv["category"],
            "city": (inv.get("city") or "") + (f" · {inv['cc']}" if inv.get("cc") else ""),
            "note": ANGEL_NOTE.get(name),
            "num_investments": inv.get("num_investments"), "unicorns": inv.get("num_unicorns"),
            "last_investment": inv.get("last_investment"),
            "relevance": rel, "top_people": tp, "points": pts,
            "harmonic_raw": harmonic_raw, "aff_max": aff_max, "aff_strong": aff_strong,
            "buckets": bucket_pipeline(aff.get("pipeline")),
            "coinvest": (co or {}).get("company_names", []),
            "dormant": dormant,
        })
    return entities
