"""Assemble the France region entities from data/france/*."""
import math, os
from coverage_common import (relevance, bucket_pipeline, harmonic_cells, top_people,
                             points_from, load_json, norm_name, clean_rels)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SLUG = {
    "Kima Ventures": "kima", "Eurazeo": "eurazeo", "Partech": "partech",
    "Aglaé Ventures": "aglae", "Elaia": "elaia", "Sofinnova Partners": "sofinnova",
    "XAnge": "xange", "Alven": "alven", "Cathay Innovation": "cathay",
    "Newfund": "newfund", "Founders Future": "founders-future",
    "Motier Ventures": "motier", "Serena": "serena", "Seventure Partners": "seventure",
    "Omnes": "omnes", "Omnes Capital": "omnes", "Demeter": "demeter", "Daphni": "daphni",
    "Financière Saint James": "saint-james", "50 Partners": "50-partners",
    "Ventech": "ventech", "BREEGA": "breega", "Breega": "breega",
    "GO Capital": "go-capital", "Evolem": "evolem", "Bpifrance": "bpifrance",
    "Singular": "singular", "Frst": "frst", "ISAI": "isai",
    "Otium Capital": "otium", "Hexa": "hexa",
    "Xavier Niel": "xavier-niel", "Thibaud Elziere": "thibaud-elziere",
    "Fabrice Grinda": "fabrice-grinda", "Edward Lando": "edward-lando",
    "Eduardo Ronzano": "eduardo-ronzano",
    "Pierre Kosciusko-Morizet": "pkm", "Olivier Pomel": "olivier-pomel",
    "Thierry Petit": "thierry-petit", "Didier Valet": "didier-valet",
    "Marc Simoncini": "marc-simoncini",
    "Jean de La Rochebrochard": "jdlr", "Jean de la Rochebrochard": "jdlr",
    "Antoine Martin": "antoine-martin", "Oleg Tscheltzoff": "oleg-tscheltzoff",
    "Florian Douetteau": "florian-douetteau", "Clément Delangue": "clement-delangue",
}
ANGEL_NOTE = {
    "Xavier Niel": "Iliad/Free founder; Kima, Station F",
    "Thibaud Elziere": "Fotolia; founder of Hexa (eFounders)",
    "Fabrice Grinda": "OLX; FJ Labs — most prolific angel globally",
    "Edward Lando": "Pareto Holdings; prolific pre-seed",
    "Eduardo Ronzano": "KelDoc founder; 200+ French seed cheques",
    "Pierre Kosciusko-Morizet": "PriceMinister founder; Kernel",
    "Olivier Pomel": "Datadog CEO",
    "Thierry Petit": "Showroomprivé co-founder",
    "Didier Valet": "ex-SocGen deputy CEO",
    "Marc Simoncini": "Meetic founder; Jaïna Capital",
    "Jean de La Rochebrochard": "ex-Kima lead, now GP at Cassius; NJF",
    "Jean de la Rochebrochard": "ex-Kima lead, now GP at Cassius; NJF",
    "Antoine Martin": "Zenly co-founder, now Amo",
    "Oleg Tscheltzoff": "Fotolia co-founder; prolific Paris angel",
    "Florian Douetteau": "Dataiku CEO",
    "Clément Delangue": "Hugging Face CEO",
}


def assemble(team):
    team_order = [m["name"] for m in team]
    investors = load_json(f"{ROOT}/data/france/investors.json") or []
    connections = {int(k): v for k, v in (load_json(f"{ROOT}/data/france/connections.json") or {}).items()}
    angel_conn = load_json(f"{ROOT}/data/france/angel_connections.json") or {}
    coinvest = {c["name"]: c for c in (load_json(f"{ROOT}/data/france/coinvestments.json") or [])}
    affdir = f"{ROOT}/data/france/affinity"

    entities = []
    for inv in investors:
        name = inv["name"]
        slug = SLUG[name]
        kind = inv["kind"]
        prefix = "angel-" if kind == "angel" else ""
        aff = load_json(f"{affdir}/{prefix}{slug}.json", {"pipeline": [], "relationships": []})
        rels = clean_rels(aff.get("relationships"))
        if kind == "angel":  # person-level rels may omit external: it is the angel
            for r in rels:
                if not r.get("external"):
                    r["external"] = name
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
            "li": inv.get("linkedin") if kind == "angel" else None,
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
