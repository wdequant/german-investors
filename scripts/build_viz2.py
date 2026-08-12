#!/usr/bin/env python3
"""Germany Coverage Map v2.

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
        stage_pts = 30
    elif "PRE_SEED" in stages:
        stage_pts = 18
    else:
        stage_pts = 8
    sf = inv.get("sector_focus") or ""
    if name in CRYPTO:
        sector_pts = 4
    elif any(s in sf for s in SECTOR_SOFTWARE):
        sector_pts = 30
    elif "Financial Services" in sf:
        sector_pts = 24
    elif "Consumer Products & Services" in sf or "Media & Entertainment" in sf:
        sector_pts = 20
    elif "Life Sciences" in sf:
        sector_pts = 8
    else:
        sector_pts = 14
    last = inv.get("last_investment")
    days = 9999
    if last and last != "null":
        days = (TODAY - datetime.fromisoformat(last.replace("Z", "+00:00"))).days
    activity_pts = 20 if days <= 60 else 16 if days <= 180 else 10 if days <= 365 else 4
    uni = inv.get("num_unicorns") or 0
    port = inv.get("num_portfolio_companies") or inv.get("num_investments") or 1
    fon = inv.get("follow_on_rate") or 0
    grad_pts = round(min(20, 20 * min(1.0, ((uni / max(port, 1)) * 10 + fon) / 1.4)), 1)
    return {"total": round(stage_pts + sector_pts + activity_pts + grad_pts),
            "stage": stage_pts, "sector": sector_pts, "activity": activity_pts, "grad": grad_pts}

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
    out["closed"] = []
    out["portfolio"] = []
    for p in pipeline:
        f = p.get("funnel")
        if f == "Portfolio Company":
            out["portfolio"].append(p)
        elif f in TEXT2BUCKET:
            out[TEXT2BUCKET[f]].append(p)
        else:
            out["closed"].append(p)
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
    })

# angels
for a in ANGELS:
    aff = load_affinity(a["slug"], prefix="angel-")
    rels = aff.get("relationships") or []
    aff_max = max((r.get("score") or 0 for r in rels), default=0)
    aff_strong = sum(1 for r in rels if (r.get("score") or 0) >= 0.5)
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
        "affinity_company_id": None,
    })

# ---------------- connectivity blend ------------------------------------------
funds = [e for e in entities if e["kind"] == "fund"]
hmax = max(e["harmonic_raw"] for e in funds) or 1
for e in entities:
    hn = e["harmonic_raw"] / hmax  # 0..1
    an = min(1.0, e["aff_max"] + 0.06 * e["aff_strong"])
    e["connectivity"] = round(100 * (0.55 * hn + 0.45 * an))
    del e["harmonic_raw"]
for e in entities:
    r = (e["relevance"] or {}).get("total", 0)
    e["gap"] = round(r * (1 - e["connectivity"] / 100))
    c = e["connectivity"]
    e["tier"] = "strong" if c >= 50 else "medium" if c >= 22 else "weak"

payload = {"generated": TODAY.strftime("%d %b %Y"), "team": team,
           "affinityOrg": AFFINITY_ORG, "entities": entities}
DATA = json.dumps(payload, ensure_ascii=False)

# ---------------- page ---------------------------------------------------------
html = """<title>Germany Coverage Map</title>
<style>
:root{
  color-scheme:light;
  --page:#f6f6f3; --surface:#ffffff; --ink:#191b1d; --ink2:#5b5f63; --muted:#96988f;
  --hair:#e8e8e2; --hair2:#f0f0eb;
  --accent:#2a78d6; --accent-ink:#1c5cab;
  --seq1:#cde2fb; --seq3:#6da7ec; --seq5:#256abf; --seq7:#0d366b;
  --good:#0ca30c; --good-ink:#006300; --warn-ink:#8a6100; --crit:#d03b3b; --crit-ink:#b32d2d;
  --chip:#f1f1ec; --rowhover:#fafaf7;
  --c-prelead:#f1f1ec; --c-prelead-ink:#5b5f63;
  --c-reachout:#e4ecf6; --c-reachout-ink:#1c5cab;
  --c-awaiting:#f7ecd4; --c-awaiting-ink:#8a6100;
  --c-lead:#e2f0e4; --c-lead-ink:#1e6b32;
  --c-hard:#f9e3e0; --c-hard-ink:#b32d2d;
  --shadow:0 1px 2px rgba(20,22,24,.04), 0 8px 24px rgba(20,22,24,.05);
}
@media (prefers-color-scheme: dark){
  :root:where(:not([data-theme="light"])){
    color-scheme:dark;
    --page:#111211; --surface:#1a1b1a; --ink:#f4f4f1; --ink2:#b7bab4; --muted:#84867f;
    --hair:#2b2c2a; --hair2:#242523;
    --accent:#3987e5; --accent-ink:#86b6ef;
    --seq1:#0d366b; --seq3:#1c5cab; --seq5:#3987e5; --seq7:#86b6ef;
    --good:#0ca30c; --good-ink:#3fbf3f; --warn-ink:#d9a13b; --crit:#e66767; --crit-ink:#e66767;
    --chip:#242523; --rowhover:#202120;
    --c-prelead:#242523; --c-prelead-ink:#b7bab4;
    --c-reachout:#1b2836; --c-reachout-ink:#86b6ef;
    --c-awaiting:#2e2618; --c-awaiting-ink:#d9a13b;
    --c-lead:#1c2a1e; --c-lead-ink:#5fce74;
    --c-hard:#301d1b; --c-hard-ink:#e66767;
    --shadow:none;
  }
}
:root[data-theme="dark"]{
  color-scheme:dark;
  --page:#111211; --surface:#1a1b1a; --ink:#f4f4f1; --ink2:#b7bab4; --muted:#84867f;
  --hair:#2b2c2a; --hair2:#242523;
  --accent:#3987e5; --accent-ink:#86b6ef;
  --seq1:#0d366b; --seq3:#1c5cab; --seq5:#3987e5; --seq7:#86b6ef;
  --good:#0ca30c; --good-ink:#3fbf3f; --warn-ink:#d9a13b; --crit:#e66767; --crit-ink:#e66767;
  --chip:#242523; --rowhover:#202120;
  --c-prelead:#242523; --c-prelead-ink:#b7bab4;
  --c-reachout:#1b2836; --c-reachout-ink:#86b6ef;
  --c-awaiting:#2e2618; --c-awaiting-ink:#d9a13b;
  --c-lead:#1c2a1e; --c-lead-ink:#5fce74;
  --c-hard:#301d1b; --c-hard-ink:#e66767;
  --shadow:none;
}
*{box-sizing:border-box;margin:0}
body{background:var(--page);color:var(--ink);
  font:14px/1.5 system-ui,-apple-system,"Segoe UI",sans-serif;
  padding:44px 28px 96px}
.wrap{max-width:1180px;margin:0 auto}
.kicker{font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:var(--muted);margin-bottom:10px}
h1{font-size:30px;font-weight:600;letter-spacing:-.015em;text-wrap:balance}
.sub{color:var(--ink2);margin-top:10px;max-width:68ch}
.tiles{display:flex;gap:14px;flex-wrap:wrap;margin:30px 0 8px}
.tile{background:var(--surface);border:1px solid var(--hair);border-radius:12px;
  padding:16px 20px;min-width:150px;box-shadow:var(--shadow)}
.tile b{display:block;font-size:26px;font-weight:600;font-variant-numeric:tabular-nums;letter-spacing:-.01em}
.tile span{color:var(--ink2);font-size:12px}
.legend-row{display:flex;gap:18px;align-items:center;flex-wrap:wrap;margin:18px 0 12px;font-size:12px;color:var(--ink2)}
.dot{display:inline-block;width:8px;height:8px;border-radius:50%;margin-right:5px;vertical-align:1px}
.controls{display:flex;gap:10px;align-items:center;flex-wrap:wrap;margin:6px 0 16px}
select,input[type=search]{background:var(--surface);color:var(--ink);border:1px solid var(--hair);
  border-radius:8px;padding:7px 10px;font-size:13px}
input[type=search]{width:200px}
.seg{display:flex;border:1px solid var(--hair);border-radius:8px;overflow:hidden}
.seg button{background:var(--surface);color:var(--ink2);border:0;padding:7px 14px;font-size:13px;cursor:pointer}
.seg button.on{background:var(--ink);color:var(--surface)}
.board{display:flex;flex-direction:column;gap:10px}
.card{background:var(--surface);border:1px solid var(--hair);border-radius:12px;box-shadow:var(--shadow)}
.rowmain{display:grid;grid-template-columns:250px 128px 1fr 260px;gap:18px;align-items:center;
  padding:15px 20px;cursor:pointer}
.rowmain:hover{background:var(--rowhover);border-radius:12px}
.fname{font-weight:600;font-size:15px;letter-spacing:-.005em}
.fname.strong{color:var(--good-ink)} .fname.medium{color:var(--warn-ink)} .fname.weak{color:var(--crit-ink)}
.fmeta{font-size:12px;color:var(--muted);margin-top:3px;display:flex;gap:8px;flex-wrap:wrap;align-items:center}
.badge{font-size:10.5px;border-radius:10px;padding:1.5px 8px;background:var(--chip);color:var(--ink2);white-space:nowrap}
.badge.co{color:var(--good-ink);border:1px solid var(--good);background:transparent}
.scores{font-variant-numeric:tabular-nums;font-size:12px;color:var(--ink2);display:flex;flex-direction:column;gap:5px}
.scores .lbl{display:inline-block;width:34px;color:var(--muted);font-size:10.5px;text-transform:uppercase;letter-spacing:.06em}
.bar{display:inline-block;vertical-align:middle;width:58px;height:5px;background:var(--hair2);border-radius:3px;overflow:hidden;margin:0 7px 0 2px}
.bar i{display:block;height:100%;border-radius:3px;background:var(--accent)}
.bar i.rel{background:var(--muted)}
.chips{display:flex;gap:7px;flex-wrap:wrap}
.chip{font-size:12px;border-radius:9px;padding:3.5px 10px;cursor:pointer;border:1px solid transparent;
  font-variant-numeric:tabular-nums;white-space:nowrap}
.chip b{font-weight:600}
.chip.prelead{background:var(--c-prelead);color:var(--c-prelead-ink)}
.chip.reachout{background:var(--c-reachout);color:var(--c-reachout-ink)}
.chip.awaiting{background:var(--c-awaiting);color:var(--c-awaiting-ink)}
.chip.lead{background:var(--c-lead);color:var(--c-lead-ink)}
.chip.hard{background:var(--c-hard);color:var(--c-hard-ink)}
.chip:hover{border-color:currentColor}
.chip.empty{opacity:.38;cursor:default}
.chip.empty:hover{border-color:transparent}
.pts{font-size:12.5px;color:var(--ink2);display:flex;flex-direction:column;gap:3px}
.pts .pt b{color:var(--ink);font-weight:570}
.pts .via{color:var(--muted)}
.pts a{color:var(--accent-ink);text-decoration:none}
.pts a:hover{text-decoration:underline}
.pts .pct{font-variant-numeric:tabular-nums;color:var(--good-ink);font-weight:600}
.detail{display:none;border-top:1px solid var(--hair);padding:16px 20px 20px;font-size:13px}
.card.open .detail{display:block}
.detail h5{font-size:11px;text-transform:uppercase;letter-spacing:.09em;color:var(--muted);margin:14px 0 7px}
.detail h5:first-child{margin-top:0}
.plist{display:flex;flex-direction:column;gap:4px}
.plist a{color:var(--accent-ink);text-decoration:none}
.plist a:hover{text-decoration:underline}
.plist .st{display:inline-block;min-width:120px;margin-right:8px;font-size:11px;color:var(--muted)}
.tmcols{display:flex;gap:26px;flex-wrap:wrap}
.tmcols .tm{min-width:190px}
.tmcols h6{font-size:12.5px;color:var(--accent-ink);margin-bottom:4px}
.tmcols div{font-size:12px;color:var(--ink2);padding:1.5px 0}
.tmcols .t{color:var(--muted)}
.meta-line{color:var(--muted);font-size:12px;margin-bottom:4px}
.sechead{margin:34px 0 12px}
.sechead h2{font-size:15px;font-weight:600;letter-spacing:-.005em}
.sechead p{font-size:12.5px;color:var(--muted);margin-top:2px}
.note{font-size:12.5px;color:var(--muted);margin-top:40px;max-width:88ch;line-height:1.6}
a.ext{color:var(--accent-ink);text-decoration:none}
@media (max-width:960px){ .rowmain{grid-template-columns:1fr 120px;grid-auto-rows:auto;row-gap:10px} }
</style>

<div class="wrap">
<div class="kicker">Highland Europe · Germany · __GENERATED__</div>
<h1>Germany Coverage Map</h1>
<p class="sub">The 30 German funds that matter most — most active, most unicorn-productive — plus nine
super-angels. Each row: how relevant they are to our thesis, how well we cover them (Harmonic network
+ full-partnership Affinity relationships), our strongest ways in, and where their portfolio already
sits in our pipeline. Fund names are coloured by coverage:
<span class="dot" style="background:var(--good)"></span><b style="color:var(--good-ink)">covered</b> ·
<span class="dot" style="background:#eda100"></span><b style="color:var(--warn-ink)">thin</b> ·
<span class="dot" style="background:var(--crit)"></span><b style="color:var(--crit-ink)">gap</b>.</p>

<div class="tiles" id="tiles"></div>

<div class="controls">
  <div class="seg" id="sortseg">
    <button data-s="gap" class="on">Biggest gaps</button><button data-s="relevance">Relevance</button><button data-s="connectivity">Coverage</button><button data-s="pipeline">Pipeline overlap</button>
  </div>
  <input type="search" id="q" placeholder="Filter…">
</div>

<div class="sechead"><h2>Funds</h2><p>Top 30 by blended activity × unicorn production. Click a row for the full relationship map; click a funnel chip for the companies behind it.</p></div>
<div class="board" id="funds"></div>

<div class="sechead"><h2>Super-angels</h2><p>Nine prolific German angels. Coverage here is Affinity-led — most have no Harmonic network trace.</p></div>
<div class="board" id="angels"></div>

<p class="note"><b>Method.</b> Universe condensed from the 74-investor Harmonic saved search: rank = ½·investment
count + ½·unicorn count (normalised), top 30 across VC/CVC/state. Relevance (0–100): stage fit 30 · sector fit
vs our software/internet thesis 30 · activity recency 20 · graduation quality 20. Coverage (0–100) blends the
Harmonic team-network (contact seniority × email/calendar evidence, 55%) with Affinity relationship intelligence
across the whole partnership including Laurence, Fergal and Ronan (45%). Pipeline chips = companies in the
Highland Companies list whose investor set includes the fund (Affinity enriched data; Lead includes Qualified
Lead and Deal; passed/deprioritised shown only in the drill-down). Names link to LinkedIn; pipeline companies
link to Affinity. Percentages on connection points are Affinity interaction scores.</p>
</div>

<script>
const D = __DATA__;
const BUCKETS = [["prelead","Pre-lead"],["reachout","Reach out"],["awaiting","Awaiting"],["lead","Lead"],["hard","Hard to crack"]];
const state = {sort:"gap", q:""};
const affURL = id => `https://${D.affinityOrg}.affinity.co/companies/${id}`;

function tiles(){
  const f = D.entities.filter(e=>e.kind==='fund');
  const gaps = f.filter(e=>e.tier==='weak' && e.relevance.total>=60);
  const pipeTotal = D.entities.reduce((n,e)=>n+BUCKETS.reduce((m,[k])=>m+e.buckets[k].length,0),0);
  const hard = D.entities.reduce((n,e)=>n+e.buckets.hard.length,0);
  document.getElementById('tiles').innerHTML = `
    <div class="tile"><b>${f.length}+${D.entities.length-f.length}</b><span>funds + angels mapped</span></div>
    <div class="tile"><b>${f.filter(e=>e.coinvest.length).length}</b><span>co-invested with</span></div>
    <div class="tile"><b>${pipeTotal}</b><span>live pipeline overlaps</span></div>
    <div class="tile"><b style="color:var(--crit-ink)">${gaps.length}</b><span>relevant funds with gap coverage</span></div>
    <div class="tile"><b style="color:var(--warn-ink)">${hard}</b><span>hard-to-cracks via these investors</span></div>`;
}

function srt(list){
  const k = state.sort;
  return [...list].sort((a,b)=>{
    if(k==='relevance') return (b.relevance?.total||0)-(a.relevance?.total||0);
    if(k==='connectivity') return b.connectivity-a.connectivity;
    if(k==='pipeline'){
      const p = e=>BUCKETS.reduce((m,[x])=>m+e.buckets[x].length,0);
      return p(b)-p(a);
    }
    return (b.gap||0)-(a.gap||0) || (b.relevance?.total||0)-(a.relevance?.total||0);
  });
}

function chipHTML(e){
  return BUCKETS.map(([k,label])=>{
    const n = e.buckets[k].length;
    return `<span class="chip ${k}${n?'':' empty'}" data-k="${k}" data-slug="${e.slug}"><b>${n}</b> ${label}</span>`;
  }).join('');
}

function ptsHTML(e){
  if(!e.points.length) return `<div class="pts"><span style="color:var(--muted)">No mapped way in yet</span></div>`;
  return `<div class="pts">`+e.points.map(p=>{
    const nm = p.linkedin?`<a href="${p.linkedin}" target="_blank" rel="noopener"><b>${p.external}</b></a>`:`<b>${p.external}</b>`;
    const pct = p.pct!=null?` <span class="pct">${p.pct}%</span>`:'';
    return `<span class="pt">${nm} <span class="via">↔ ${p.internal}</span>${pct}</span>`;
  }).join('')+`</div>`;
}

function rowHTML(e){
  const rel = e.relevance? e.relevance.total : null;
  const co = e.coinvest.length?`<span class="badge co">✓ co-invested ×${e.coinvest.length}</span>`:'';
  const meta = e.kind==='fund'
    ? `<span class="badge">${e.category.toUpperCase()}</span><span>${e.city||''}</span>${co}`
    : `<span>${e.note||''}</span>`;
  const scores = e.kind==='fund'
    ? `<div class="scores">
        <span><span class="lbl">Rel</span><span class="bar"><i class="rel" style="width:${rel}%"></i></span><b>${rel}</b></span>
        <span><span class="lbl">Cov</span><span class="bar"><i style="width:${e.connectivity}%"></i></span><b>${e.connectivity}</b></span></div>`
    : `<div class="scores">
        <span><span class="lbl">Inv</span><b>${e.num_investments??'—'}</b></span>
        <span><span class="lbl">Cov</span><span class="bar"><i style="width:${e.connectivity}%"></i></span><b>${e.connectivity}</b></span></div>`;
  return `<div class="card" id="card-${e.slug}">
    <div class="rowmain" data-slug="${e.slug}">
      <div><div class="fname ${e.tier}">${e.name}</div><div class="fmeta">${meta}</div></div>
      ${scores}
      <div class="chips">${chipHTML(e)}</div>
      ${ptsHTML(e)}
    </div>
    <div class="detail" id="detail-${e.slug}"></div>
  </div>`;
}

function detailHTML(e){
  let h = '';
  if(e.kind==='fund'){
    const r=e.relevance;
    h += `<div class="meta-line">Relevance ${r.total} (stage ${r.stage} · sector ${r.sector} · activity ${r.activity} · graduation ${r.grad})
      · ${e.num_investments??'—'} investments · ${e.unicorns??0} unicorns · last investment ${e.last_investment||'—'}
      ${e.coinvest.length?` · <b style="color:var(--good-ink)">co-invested:</b> ${e.coinvest.join(', ')}`:''}</div>`;
  }
  const anyPipe = BUCKETS.some(([k])=>e.buckets[k].length) || e.buckets.portfolio.length || e.buckets.closed.length;
  if(anyPipe){
    for(const [k,label] of [...BUCKETS,["portfolio","Portfolio company"],["closed","Passed / deprioritised"]]){
      const list = e.buckets[k]; if(!list||!list.length) continue;
      h += `<h5 id="sec-${e.slug}-${k}">${label} (${list.length})</h5><div class="plist">`+
        list.map(p=>`<span><span class="st">${(p.funnel||'—').replace(' (free for all)','')}</span><a href="${affURL(p.id)}" target="_blank" rel="noopener">${p.name}</a> <span style="color:var(--muted)">${p.domain||''}</span></span>`).join('')+`</div>`;
    }
  } else { h += `<h5>Pipeline overlap</h5><div class="meta-line">None of their portfolio is in our pipeline list.</div>`; }
  if(e.cells){
    const best = D.team.map(m=>({m,c:e.cells[m.name]})).filter(x=>x.c.score>0).sort((a,b)=>b.c.score-a.c.score);
    if(best.length){
      h += `<h5>Harmonic network, by team member</h5><div class="tmcols">`+best.map(({m,c})=>
        `<div class="tm"><h6>${m.name} <span style="color:var(--muted)">(${c.score})</span></h6>`+
        c.contacts.map(k=>{
          const nm = k.linkedin?`<a class="ext" href="${k.linkedin}" target="_blank" rel="noopener">${k.person}</a>`:k.person;
          return `<div>${nm} <span class="t">· ${k.title}${k.external?' (adjacent)':''} · ${(k.sources||[]).map(s=>({LINKEDIN:'LI',EMAIL:'Email',CALENDAR:'Cal'})[s]||s).join(' · ')}</span></div>`;
        }).join('')+`</div>`).join('')+`</div>`;
    }
  }
  return h;
}

function render(){
  const q = state.q;
  const vis = D.entities.filter(e=>!q || e.name.toLowerCase().includes(q));
  document.getElementById('funds').innerHTML = srt(vis.filter(e=>e.kind==='fund')).map(rowHTML).join('');
  document.getElementById('angels').innerHTML = srt(vis.filter(e=>e.kind==='angel')).map(rowHTML).join('');
  document.querySelectorAll('.rowmain').forEach(r=>{
    r.addEventListener('click',ev=>{
      if(ev.target.closest('a')) return;
      const slug = r.dataset.slug, card = document.getElementById('card-'+slug);
      const e = D.entities.find(x=>x.slug===slug);
      const chip = ev.target.closest('.chip');
      const det = document.getElementById('detail-'+slug);
      if(!card.classList.contains('open')){ det.innerHTML = detailHTML(e); card.classList.add('open'); }
      else if(!chip){ card.classList.remove('open'); return; }
      if(chip && !chip.classList.contains('empty')){
        const sec = document.getElementById(`sec-${slug}-${chip.dataset.k}`);
        if(sec) sec.scrollIntoView({behavior:'smooth', block:'center'});
      }
    });
  });
}
document.querySelectorAll('#sortseg button').forEach(b=>b.addEventListener('click',()=>{
  document.querySelectorAll('#sortseg button').forEach(x=>x.classList.remove('on'));
  b.classList.add('on'); state.sort=b.dataset.s; render();
}));
document.getElementById('q').addEventListener('input',e=>{state.q=e.target.value.toLowerCase();render()});
tiles(); render();
</script>
"""

html = html.replace("__DATA__", DATA).replace("__GENERATED__", payload["generated"])
os.makedirs(f"{ROOT}/viz", exist_ok=True)
open(f"{ROOT}/viz/index.html", "w").write(html)
print(f"wrote viz/index.html ({len(html)//1024} KB), {len(funds)} funds + {len(entities)-len(funds)} angels")
for e in sorted(funds, key=lambda x: -x["gap"])[:10]:
    pipe = sum(len(e["buckets"][k]) for k, _, _ in BUCKETS)
    print(f"  gap {e['gap']:3} {e['name'][:32]:34} rel={e['relevance']['total']:3} cov={e['connectivity']:3} pipe={pipe} tier={e['tier']}")
