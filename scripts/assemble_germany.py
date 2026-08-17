"""Assemble the Germany region entities from data/* (top-31 funds + 9 angels)."""
import math, os
from coverage_common import (relevance, bucket_pipeline, harmonic_cells, top_people,
                             points_from, load_json, norm_name, clean_rels)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CATEGORY = {
    "Global Founders Capital": "vc", "HTGF | High-Tech Gründerfonds": "state",
    "HV Capital": "vc", "Earlybird Venture Capital": "vc", "Point Nine": "vc",
    "468 Capital": "vc", "Picus Capital": "vc", "Cherry Ventures": "vc",
    "Bayern Kapital": "state", "Project A": "vc", "IBB Ventures": "state",
    "Atlantic Labs": "vc", "1kx": "vc", "TA Ventures": "vc", "Redstone": "vc",
    "Bosch Ventures": "cvc", "BlueYard Capital": "vc", "Possible Ventures": "vc",
    "Capnamic": "vc", "UVC Partners": "vc", "MIG Capital": "vc",
    "Acton Capital": "vc", "NAP (New Amsterdam Partners)": "vc",
    "10x Founders": "vc", "Dieter von Holtzbrinck Ventures": "vc",
    "Vsquared Ventures": "vc", "Discovery Ventures": "vc", "10x Group": "vc",
    "Burda Principal Investments": "cvc", "CommerzVentures": "cvc",
    "Alstin Capital": "vc",
}
FUND_SLUG = {
    "Global Founders Capital": "gfc", "HTGF | High-Tech Gründerfonds": "htgf",
    "HV Capital": "hv-capital", "Point Nine": "point-nine",
    "Earlybird Venture Capital": "earlybird", "Cherry Ventures": "cherry",
    "468 Capital": "468-capital", "Picus Capital": "picus", "Project A": "project-a",
    "Bayern Kapital": "bayern-kapital", "BlueYard Capital": "blueyard",
    "Atlantic Labs": "atlantic-labs", "Redstone": "redstone",
    "UVC Partners": "uvc-partners", "TA Ventures": "ta-ventures",
    "Bosch Ventures": "bosch-ventures", "IBB Ventures": "ibb-ventures",
    "1kx": "1kx", "10x Group": "10x-group", "Possible Ventures": "possible-ventures",
    "Dieter von Holtzbrinck Ventures": "dvh-ventures",
    "Discovery Ventures": "discovery-ventures", "Vsquared Ventures": "vsquared",
    "Capnamic": "capnamic", "Burda Principal Investments": "burda",
    "NAP (New Amsterdam Partners)": "nap", "CommerzVentures": "commerzventures",
    "MIG Capital": "mig-capital", "10x Founders": "10x-founders",
    "Acton Capital": "acton", "Alstin Capital": "alstin",
}
CRYPTO = {"1kx"}
ANGELS = [
    {"name": "Mario Götze", "slug": "mario-goetze", "note": "Footballer-investor (Companion-M)", "li": "https://linkedin.com/in/mario-goetze", "inv": 56},
    {"name": "Hanno Renner", "slug": "hanno-renner", "note": "Founder/CEO Personio", "li": "https://linkedin.com/in/hanno-renner", "inv": 32},
    {"name": "Julius Göllner", "slug": "julius-goellner", "note": "ARRtist, SaaS angel", "li": "https://linkedin.com/in/julius-goellner", "inv": 26},
    {"name": "Matthias Hilpert", "slug": "matthias-hilpert", "note": "MH2 Capital", "li": "https://linkedin.com/in/matthiashilpert", "inv": 25},
    {"name": "Philipp Klöckner", "slug": "philipp-kloeckner", "note": "'Pip', Doppelgänger pod, SEO/marketplaces", "li": "https://linkedin.com/in/kloeckner", "inv": None},
    {"name": "Christian Vollmann", "slug": "christian-vollmann", "note": "nebenan.de / C1, prolific pre-seed", "li": "https://linkedin.com/in/christianvollmann", "inv": 26},
    {"name": "Verena Pausder", "slug": "verena-pausder", "note": "Startup-Verband chair", "li": "https://linkedin.com/in/verenapausder", "inv": None},
    {"name": "Hakan Koç", "slug": "hakan-koc", "note": "Co-founder AUTO1", "li": "https://linkedin.com/in/hakan-koc", "inv": None},
    {"name": "Christian Reber", "slug": "christian-reber", "note": "Pitch / Wunderlist, Interface Capital", "li": "https://linkedin.com/in/christianreber", "inv": None},
]


def assemble(team):
    team_order = [m["name"] for m in team]
    investors = load_json(f"{ROOT}/data/germany-investors.json")
    connections = {int(k): v for k, v in load_json(f"{ROOT}/data/connections.json").items()}
    coinvest = {c["urn"]: c for c in load_json(f"{ROOT}/data/coinvestments.json")}
    inv_by_name = {i["name"]: i for i in investors}
    affdir = f"{ROOT}/data/affinity"

    entities = []
    for name, cat in CATEGORY.items():
        inv = inv_by_name[name]
        slug = FUND_SLUG[name]
        cid = int(inv["company_urn"].rsplit(":", 1)[1])
        aff = load_json(f"{affdir}/{slug}.json", {"pipeline": [], "relationships": []})
        rels = clean_rels(aff.get("relationships"))
        aff_max = max((r.get("score") or 0 for r in rels), default=0)
        aff_strong = sum(1 for r in rels if (r.get("score") or 0) >= 0.5)

        cells, li = harmonic_cells(connections.get(cid), team_order)
        max_cell = max(c["score"] for c in cells.values())
        total_w = sum(c["score"] for c in cells.values())
        harmonic_raw = 0.7 * math.sqrt(max_cell) + 0.3 * math.sqrt(total_w)

        tp = top_people(cells, rels)
        for p in tp:
            for k in p["contacts"]:
                if not k.get("linkedin"):
                    k["linkedin"] = li.get(norm_name(k["person"]))
        co = coinvest.get(inv["urn"])
        entities.append({
            "name": name.replace(" | High-Tech Gründerfonds", ""), "slug": slug, "kind": "fund",
            "category": cat, "city": (inv.get("city") or "") + " · DE",
            "num_investments": inv.get("num_investments"), "unicorns": inv.get("num_unicorns"),
            "last_investment": (inv.get("last_investment") or "")[:10],
            "relevance": relevance(inv, CRYPTO), "top_people": tp,
            "points": points_from(rels, cells, li),
            "harmonic_raw": harmonic_raw, "aff_max": aff_max, "aff_strong": aff_strong,
            "buckets": bucket_pipeline(aff.get("pipeline")),
            "coinvest": (co or {}).get("company_names", []),
            "dormant": aff.get("dormant"),
        })

    for a in ANGELS:
        aff = load_json(f"{affdir}/angel-{a['slug']}.json", {"pipeline": [], "relationships": []})
        rels = clean_rels(aff.get("relationships"))
        aff_max = max((r.get("score") or 0 for r in rels), default=0)
        aff_strong = sum(1 for r in rels if (r.get("score") or 0) >= 0.5)
        tp = top_people(None, rels)
        pts = [{"external": a["name"], "internal": p["name"], "pct": round(p["aff"] * 100),
                "linkedin": a["li"], "src": "affinity"} for p in tp if p["aff"] > 0][:3]
        entities.append({
            "name": a["name"], "slug": a["slug"], "kind": "angel", "category": "angel",
            "li": a["li"],
            "city": None, "note": a["note"], "num_investments": a["inv"],
            "unicorns": None, "last_investment": None,
            "relevance": None, "top_people": tp, "points": pts,
            "harmonic_raw": 0, "aff_max": aff_max, "aff_strong": aff_strong,
            "buckets": bucket_pipeline(aff.get("pipeline")),
            "coinvest": [], "dormant": aff.get("dormant"),
        })
    return entities
