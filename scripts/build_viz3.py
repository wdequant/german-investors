#!/usr/bin/env python3
"""Germany Coverage Map v3 (app-frame design).

Condensed universe: top-30 VC/CVC/state funds (hybrid of investment activity +
unicorn production) + 9 German super-angels.

Blends three data layers per entity:
  - Harmonic team-network connections (per-teammate, per-contact, LinkedIn)
  - Affinity relationship intelligence (whole partnership incl. Laurence/Fergal)
  - Affinity pipeline overlap (which of the fund's companies sit in Highland
    Companies list 9387, by funnel stage, with Affinity links)

Output: viz/index.html
"""
import json, math, os, re, glob, unicodedata
from datetime import datetime, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TODAY = datetime(2026, 8, 12, tzinfo=timezone.utc)
AFFINITY_ORG = "highlandeurope"  # affinity web subdomain for entity links

investors = json.load(open(f"{ROOT}/data/germany-investors.json"))
connections = {int(k): v for k, v in json.load(open(f"{ROOT}/data/connections.json")).items()}
coinvest = {c["urn"]: c for c in json.load(open(f"{ROOT}/data/coinvestments.json"))}
team = json.load(open(f"{ROOT}/data/highland-team.json"))
TEAM_ORDER = [m["name"] for m in team]
TEAM_SET = set(TEAM_ORDER)

# ---------------- top-30 selection --------------------------------------------
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
    "Alstin Capital": "vc",  # added manually on request (outside the top-30 cut)
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

# ---------------- weights (same as v1) ----------------------------------------
def contact_weight(title, external=False):
    if external:
        return 0.25
    t = (title or "").lower()
    if any(k in t for k in ["venture partner", "expert partner", "operating partner",
                            "limited partner", "coaching partner", "venture scout"]):
        return 1.5
    if any(k in t for k in ["general partner", "founding partner", "managing partner",
                            "managing director", "founder", "co-founder", "ceo",
                            "chairman", "investment partner"]) or re.search(r"\bpartner\b", t):
        return 3.0
    if any(k in t for k in ["principal", "investment director", "head of venture", "director"]):
        return 2.0
    if any(k in t for k in ["investment manager", "investor", "vc", "member of the investment committee"]):
        return 1.5
    if any(k in t for k in ["associate", "analyst", "fellow"]):
        return 1.0
    return 0.5

def source_weight(sources):
    s = set(sources or [])
    if "CALENDAR" in s and "EMAIL" in s:
        return 3.5 if "LINKEDIN" in s else 3.0
    if "EMAIL" in s:
        return 2.0
    return 1.0

SECTOR_SOFTWARE = ("Communications & Information Technology", "Business Services")

def relevance(inv, name):
    stages = inv.get("entry_stage_focus") or ""
    if "SEED" in stages.replace("PRE_SEED", "") or "SERIES_A" in stages:
        stage_pts = 25
    elif "PRE_SEED" in stages:
        stage_pts = 15
    else:
        stage_pts = 7
    sf = inv.get("sector_focus") or ""
    if name in CRYPTO:
        sector_pts = 3
    elif any(s in sf for s in SECTOR_SOFTWARE):
        sector_pts = 25
    elif "Financial Services" in sf:
        sector_pts = 20
    elif "Consumer Products & Services" in sf or "Media & Entertainment" in sf:
        sector_pts = 17
    elif "Life Sciences" in sf:
        sector_pts = 7
    else:
        sector_pts = 12
    # geography: share of portfolio in Europe (80%+ = full marks)
    eu = inv.get("europe_share") or 0.0
    geo_pts = round(20 * min(1.0, eu / 80.0), 1)
    last = inv.get("last_investment")
    days = 9999
    if last and last != "null":
        days = (TODAY - datetime.fromisoformat(last.replace("Z", "+00:00"))).days
    activity_pts = 15 if days <= 60 else 12 if days <= 180 else 8 if days <= 365 else 3
    uni = inv.get("num_unicorns") or 0
    port = inv.get("num_portfolio_companies") or inv.get("num_investments") or 1
    fon = inv.get("follow_on_rate") or 0
    grad_pts = round(min(15, 15 * min(1.0, ((uni / max(port, 1)) * 10 + fon) / 1.4)), 1)
    return {"total": round(stage_pts + sector_pts + geo_pts + activity_pts + grad_pts),
            "stage": stage_pts, "sector": sector_pts, "geo": geo_pts,
            "activity": activity_pts, "grad": grad_pts, "europe": eu}

# ---------------- funnel buckets ----------------------------------------------
BUCKETS = [
    ("prelead", "Pre-lead", ["Pre-lead"]),
    ("reachout", "Reach out", ["Reach Out Now"]),
    ("awaiting", "Awaiting reply", ["Awaiting Reply"]),
    ("lead", "Lead", ["Lead", "Qualified Lead", "Deal"]),
    ("hard", "Hard to crack", ["Hard to crack"]),
]
CLOSED = ["Passed", "Deprioritised (free for all)", None, "Portfolio Company"]
TEXT2BUCKET = {t: key for key, _, texts in BUCKETS for t in texts}

def bucket_pipeline(pipeline):
    out = {k: [] for k, _, _ in BUCKETS}
    out["portfolio"] = []
    for p in pipeline:
        f = p.get("funnel")
        if f == "Portfolio Company":
            out["portfolio"].append(p)
        elif f in TEXT2BUCKET:
            out[TEXT2BUCKET[f]].append(p)
        # Passed / Deprioritised / no status: dropped entirely
    return out

def norm_name(s):
    return unicodedata.normalize("NFKD", s or "").encode("ascii", "ignore").decode().lower()

def load_affinity(slug, prefix=""):
    path = f"{ROOT}/data/affinity/{prefix}{slug}.json"
    if os.path.exists(path):
        return json.load(open(path))
    return {"pipeline": [], "relationships": [], "affinity_company_id": None}

# ---------------- assemble fund entities --------------------------------------
inv_by_name = {i["name"]: i for i in investors}
entities = []

for name, cat in CATEGORY.items():
    inv = inv_by_name[name]
    slug = FUND_SLUG[name]
    cid = int(inv["company_urn"].rsplit(":", 1)[1])
    rel = relevance(inv, name)
    aff = load_affinity(slug)

    # harmonic per-teammate cells
    cells = {u: {"score": 0.0, "contacts": []} for u in TEAM_ORDER}
    conn = connections.get(cid)
    li_by_person = {}
    if conn:
        for c in conn["connections"]:
            cw = contact_weight(c.get("title"), c.get("external", False))
            if c.get("linkedin") and c.get("person"):
                li_by_person[norm_name(c["person"])] = c["linkedin"]
            for via in c.get("via", []):
                u = via.get("user")
                if u not in TEAM_SET:
                    continue
                sw = source_weight(via.get("sources"))
                cells[u]["score"] += cw * sw
                cells[u]["contacts"].append({
                    "person": c.get("person") or "(unnamed)", "title": c.get("title") or "—",
                    "external": bool(c.get("external")), "linkedin": c.get("linkedin"),
                    "sources": via.get("sources") or [], "w": round(cw * sw, 1)})
    for u in cells:
        cells[u]["score"] = round(cells[u]["score"], 1)
        cells[u]["contacts"].sort(key=lambda x: -x["w"])
    max_cell = max(c["score"] for c in cells.values())
    total_w = sum(c["score"] for c in cells.values())
    harmonic_raw = 0.7 * math.sqrt(max_cell) + 0.3 * math.sqrt(total_w)

    # affinity relationships (whole partnership)
    rels = aff.get("relationships") or []
    aff_max = max((r.get("score") or 0 for r in rels), default=0)
    aff_strong = sum(1 for r in rels if (r.get("score") or 0) >= 0.5)
    dormant = aff.get("dormant")

    # top connection points: affinity interaction rels first, then harmonic
    points, seen = [], set()
    for r in sorted(rels, key=lambda r: -(r.get("score") or 0)):
        if (r.get("score") or 0) <= 0:
            continue
        key = norm_name(r.get("external", ""))
        if key in seen:
            continue
        seen.add(key)
        points.append({
            "external": r.get("external"), "internal": r.get("internal"),
            "pct": round((r.get("score") or 0) * 100),
            "linkedin": li_by_person.get(key), "src": "affinity"})
    hc = []
    for u in TEAM_ORDER:
        for k in cells[u]["contacts"]:
            if k["external"] or k["w"] < 3:
                continue
            hc.append((k["w"], k, u))
    for w, k, u in sorted(hc, key=lambda x: -x[0]):
        key = norm_name(k["person"])
        if key in seen:
            continue
        seen.add(key)
        points.append({"external": k["person"], "internal": u, "pct": None,
                       "title": k["title"], "linkedin": k.get("linkedin"), "src": "harmonic"})
    points = points[:3]

    buckets = bucket_pipeline(aff.get("pipeline") or [])
    co = coinvest.get(inv["urn"])
    entities.append({
        "name": name.replace(" | High-Tech Gründerfonds", ""), "slug": slug, "kind": "fund",
        "category": cat, "city": inv.get("city"), "stages": inv.get("entry_stage_focus"),
        "num_investments": inv.get("num_investments"), "unicorns": inv.get("num_unicorns"),
        "last_investment": (inv.get("last_investment") or "")[:10],
        "relevance": rel, "cells": cells, "harmonic_raw": harmonic_raw,
        "aff_max": aff_max, "aff_strong": aff_strong,
        "points": points, "buckets": buckets,
        "coinvest": (co or {}).get("company_names", []),
        "affinity_company_id": aff.get("affinity_company_id"),
        "dormant": dormant,
    })

# angels
for a in ANGELS:
    aff = load_affinity(a["slug"], prefix="angel-")
    rels = aff.get("relationships") or []
    aff_max = max((r.get("score") or 0 for r in rels), default=0)
    aff_strong = sum(1 for r in rels if (r.get("score") or 0) >= 0.5)
    dormant = aff.get("dormant")
    points = [{"external": a["name"], "internal": r.get("internal"),
               "pct": round((r.get("score") or 0) * 100), "linkedin": a["li"], "src": "affinity"}
              for r in sorted(rels, key=lambda r: -(r.get("score") or 0)) if (r.get("score") or 0) > 0][:3]
    buckets = bucket_pipeline(aff.get("pipeline") or [])
    entities.append({
        "name": a["name"], "slug": a["slug"], "kind": "angel", "category": "angel",
        "city": None, "note": a["note"], "li": a["li"], "num_investments": a["inv"],
        "relevance": None, "cells": None, "harmonic_raw": 0,
        "aff_max": aff_max, "aff_strong": aff_strong,
        "points": points, "buckets": buckets, "coinvest": [],
        "affinity_company_id": None, "dormant": dormant,
    })

# ---------------- top Highland people per entity -------------------------------
EX_STAFF = {"Emily Tan", "Anna Faulkner", "Zina Alfa", "Rachel Barbour-Fowles"}
NAME_MAP = {"Gajan Rajanathan": "Gaj Rajanathan", "William De Quant": "Will de Quant",
            "Stan Laurent": "Stan"}

def top_people(e, aff_rels):
    people = {}
    for r in aff_rels or []:
        nm = NAME_MAP.get(r.get("internal"), r.get("internal"))
        if not nm or nm in EX_STAFF:
            continue
        p = people.setdefault(nm, {"name": nm, "aff": 0.0, "harmonic": 0.0, "contacts": []})
        sc = r.get("score") or 0
        p["aff"] = max(p["aff"], sc)
        if r.get("external") and sc > 0:
            p["contacts"].append({"person": r["external"], "pct": round(sc * 100), "linkedin": None})
    if e.get("cells"):
        for u, c in e["cells"].items():
            if c["score"] <= 0 or u in EX_STAFF:
                continue
            p = people.setdefault(u, {"name": u, "aff": 0.0, "harmonic": 0.0, "contacts": []})
            p["harmonic"] = c["score"]
            for k in c["contacts"][:3]:
                if k["external"] or k["w"] < 2:
                    continue
                if not any(norm_name(x["person"]) == norm_name(k["person"]) for x in p["contacts"]):
                    p["contacts"].append({"person": k["person"], "pct": None,
                                          "title": k["title"], "linkedin": k.get("linkedin")})
    ranked = sorted(people.values(), key=lambda p: (-p["aff"], -p["harmonic"]))
    for p in ranked:
        p["contacts"] = p["contacts"][:3]
        p["harmonic"] = round(p["harmonic"], 1)
        p["aff"] = round(p["aff"], 2)
    return ranked[:4]

for e in entities:
    slug = e["slug"]
    prefix = "angel-" if e["kind"] == "angel" else ""
    aff = load_affinity(slug, prefix=prefix)
    e["top_people"] = top_people(e, aff.get("relationships"))
    # attach linkedin urls from harmonic contacts where names match
    li = {}
    if e.get("cells"):
        for u, c in e["cells"].items():
            for k in c["contacts"]:
                if k.get("linkedin"):
                    li[norm_name(k["person"])] = k["linkedin"]
    for p in e["top_people"]:
        for k in p["contacts"]:
            if not k.get("linkedin"):
                k["linkedin"] = li.get(norm_name(k["person"]))
    del e["cells"]  # full per-teammate dump no longer shipped

# ---------------- connectivity blend ------------------------------------------
funds = [e for e in entities if e["kind"] == "fund"]
hmax = max(e["harmonic_raw"] for e in funds) or 1
def dormant_weight(d):
    if not d:
        return 0.0
    yr = int(d["last"][:4])
    age = 2026 - yr
    return 0.22 if age <= 1 else 0.15 if age <= 3 else 0.10 if age <= 6 else 0.06

for e in entities:
    hn = e["harmonic_raw"] / hmax  # 0..1
    an = min(1.0, max(e["aff_max"] + 0.06 * e["aff_strong"], dormant_weight(e.get("dormant"))))
    e["connectivity"] = round(100 * (0.55 * hn + 0.45 * an))
    del e["harmonic_raw"]
for e in entities:
    r = (e["relevance"] or {}).get("total", 0)
    e["gap"] = round(r * (1 - e["connectivity"] / 100))
    c = e["connectivity"]
    e["tier"] = "strong" if c >= 50 else "medium" if c >= 22 else "weak"

# ---------------- page ---------------------------------------------------------
import importlib.util as _ilu
_spec = _ilu.spec_from_file_location("viz3_template", os.path.join(os.path.dirname(os.path.abspath(__file__)), "viz3_template.py"))
_tpl = _ilu.module_from_spec(_spec); _spec.loader.exec_module(_tpl)

payload = {"generated": TODAY.strftime("%d %b %Y"), "team": team,
           "affinityOrg": AFFINITY_ORG, "entities": entities}
DATA = json.dumps(payload, ensure_ascii=False)
html = _tpl.TEMPLATE.replace("__DATA__", DATA).replace("__GENERATED__", payload["generated"])
os.makedirs(f"{ROOT}/viz", exist_ok=True)
open(f"{ROOT}/viz/index.html", "w").write(html)
print(f"wrote viz/index.html ({len(html)//1024} KB), {len(funds)} funds + {len(entities)-len(funds)} angels")
