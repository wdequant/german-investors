"""Shared scoring and assembly helpers for the multi-region coverage map."""
import json, math, os, re, unicodedata
from datetime import datetime, timezone

TODAY = datetime(2026, 8, 12, tzinfo=timezone.utc)
AFFINITY_ORG = "highland"  # tenant subdomain per Affinity get_current_user
EX_STAFF = {"Emily Tan", "Anna Faulkner", "Zina Alfa", "Rachel Barbour-Fowles"}
NAME_MAP = {"Gajan Rajanathan": "Gaj Rajanathan", "William De Quant": "Will de Quant",
            "Stan Laurent": "Stan"}
SECTOR_SOFTWARE = ("Communications & Information Technology", "Business Services")

BUCKETS = [
    ("prelead", "Pre-lead", ["Pre-lead"]),
    ("reachout", "Reach out", ["Reach Out Now"]),
    ("awaiting", "Awaiting reply", ["Awaiting Reply"]),
    ("lead", "Lead", ["Lead", "Qualified Lead", "Deal"]),
    ("hard", "Hard to crack", ["Hard to crack"]),
]
TEXT2BUCKET = {t: key for key, _, texts in BUCKETS for t in texts}


def norm_name(s):
    return unicodedata.normalize("NFKD", s or "").encode("ascii", "ignore").decode().lower()


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


def relevance(inv, crypto_names=()):
    """inv needs: name, entry_stage_focus, sector_focus, europe_share,
    last_investment, num_unicorns, num_portfolio (opt), num_investments, follow_on_rate."""
    stages = inv.get("entry_stage_focus") or ""
    if "SEED" in stages.replace("PRE_SEED", "") or "SERIES_A" in stages:
        stage_pts = 25
    elif "PRE_SEED" in stages or "ACCELERATOR" in stages:
        stage_pts = 15
    else:
        stage_pts = 12  # unknown/multi-stage: neutral-low rather than punitive
    sf = inv.get("sector_focus") or ""
    if inv["name"] in crypto_names:
        sector_pts = 3
    elif any(s in sf for s in SECTOR_SOFTWARE):
        sector_pts = 25
    elif "Financial Services" in sf:
        sector_pts = 20
    elif "Consumer Products & Services" in sf or "Media & Entertainment" in sf or "Education" in sf:
        sector_pts = 17
    elif "Life Sciences" in sf:
        sector_pts = 7
    else:
        sector_pts = 12
    eu = inv.get("europe_share") or 0.0
    geo_pts = round(20 * min(1.0, eu / 80.0), 1)
    last = inv.get("last_investment")
    days = 9999
    if last and last != "null":
        days = (TODAY - datetime.fromisoformat(last[:10] + "T00:00:00+00:00")).days
    activity_pts = 15 if days <= 60 else 12 if days <= 180 else 8 if days <= 365 else 3
    uni = inv.get("num_unicorns") or 0
    port = inv.get("num_portfolio_companies") or inv.get("num_investments") or 1
    fon = inv.get("follow_on_rate") or 0
    grad_pts = round(min(15, 15 * min(1.0, ((uni / max(port, 1)) * 10 + fon) / 1.4)), 1)
    return {"total": round(stage_pts + sector_pts + geo_pts + activity_pts + grad_pts),
            "stage": stage_pts, "sector": sector_pts, "geo": geo_pts,
            "activity": activity_pts, "grad": grad_pts, "europe": eu}


def bucket_pipeline(pipeline):
    out = {k: [] for k, _, _ in BUCKETS}
    out["portfolio"] = []
    for p in pipeline or []:
        f = p.get("funnel")
        if f == "Portfolio Company":
            out["portfolio"].append(p)
        elif f in TEXT2BUCKET:
            out[TEXT2BUCKET[f]].append(p)
    return out


def harmonic_cells(conn, team_order):
    """conn = parsed get_company_connections record -> per-team-member cells."""
    cells = {u: {"score": 0.0, "contacts": []} for u in team_order}
    li_by_person = {}
    if conn:
        for c in conn["connections"]:
            cw = contact_weight(c.get("title"), c.get("external", False))
            if c.get("linkedin") and c.get("person"):
                li_by_person[norm_name(c["person"])] = c["linkedin"]
            for via in c.get("via", []):
                u = via.get("user")
                if u not in cells:
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
    return cells, li_by_person


def top_people(cells, aff_rels):
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
    if cells:
        for u, c in cells.items():
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
    return ranked


def points_from(rels, cells, li_by_person):
    """Top-3 'strongest paths in' for the team view."""
    points, seen = [], set()
    for r in sorted(rels or [], key=lambda r: -(r.get("score") or 0)):
        if (r.get("score") or 0) <= 0:
            continue
        nm = NAME_MAP.get(r.get("internal"), r.get("internal"))
        if nm in EX_STAFF:
            continue
        key = norm_name(r.get("external", ""))
        if key in seen:
            continue
        seen.add(key)
        points.append({"external": r.get("external"), "internal": nm,
                       "pct": round((r.get("score") or 0) * 100),
                       "linkedin": li_by_person.get(key), "src": "affinity"})
    hc = []
    if cells:
        for u, c in cells.items():
            for k in c["contacts"]:
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
    return points[:3]


def recency_decay(last):
    """Decay factor for affinity strength by time since last touch.
    None (unknown) is treated gently; >1y decays considerably per spec."""
    if not last:
        return 0.85
    try:
        d = datetime.fromisoformat(str(last)[:10] + "T00:00:00+00:00")
    except ValueError:
        return 0.85
    days = (TODAY - d).days
    if days <= 180:
        return 1.0
    if days <= 365:
        return 0.9
    if days <= 730:
        return 0.5
    return 0.3


def angel_relevance(deals, unicorns, synd_overlap, pipeline_active):
    """0-100 relevance for angels: deal velocity, outcomes, syndication with
    our mapped funds, and presence on our pipeline cap tables."""
    d = min(25, (deals or 0) * 0.5)
    u = min(15, (unicorns or 0) * 4)
    sy = min(30, synd_overlap * 7)
    pl = min(30, pipeline_active * 1.5)
    return {"total": round(d + u + sy + pl), "deals": round(d, 1), "uni": round(u, 1),
            "synd": round(sy, 1), "pipe": round(pl, 1)}


def dormant_weight(d):
    if not d:
        return 0.0
    yr = int(str(d["last"])[:4])
    age = 2026 - yr
    return 0.22 if age <= 1 else 0.15 if age <= 3 else 0.10 if age <= 6 else 0.06


def finalize(entities):
    """Blend connectivity (with recency decay), compute gap + tier."""
    funds = [e for e in entities if e["kind"] == "fund"]
    hmax = max((e["harmonic_raw"] for e in funds), default=1) or 1
    for e in entities:
        hn = e["harmonic_raw"] / hmax
        decay = recency_decay(e.get("fund_last"))
        a_raw = min(1.0, e["aff_max"] + 0.06 * e["aff_strong"])
        an = max(a_raw * decay, dormant_weight(e.get("dormant")))
        e["connectivity"] = round(100 * (0.55 * hn + 0.45 * an))
        e["cov_parts"] = {"h": round(hn, 2), "a": round(a_raw, 2), "decay": decay,
                          "dorm": dormant_weight(e.get("dormant"))}
        del e["harmonic_raw"]
    for e in entities:
        r = (e["relevance"] or {}).get("total", 0)
        e["gap"] = round(r * (1 - e["connectivity"] / 100))
        c = e["connectivity"]
        e["tier"] = "strong" if c >= 50 else "medium" if c >= 22 else "weak"
    return entities


def load_json(path, default=None):
    if os.path.exists(path):
        return json.load(open(path))
    return default


def _strip_emoji(s):
    """Drop non-BMP symbols/emoji (Harmonic names sometimes carry them)."""
    return "".join(ch for ch in (s or "") if ord(ch) < 0x2600).strip(" -·|")


def apply_enrich(entities, enrich, recency, empflags, region_key):
    """Merge agent-collected enrichment into assembled entities (all optional)."""
    efunds = (enrich or {}).get("funds", {})
    eangels = (enrich or {}).get("angels", {})
    rec = recency or {}
    emp = (empflags or {}).get(region_key, {})
    for e in entities:
        slug = e["slug"]
        rkey = slug if e["kind"] == "fund" else f"angel-{slug}"
        r = rec.get(rkey, {})
        e["fund_last"] = r.get("fund_last")
        cdates = r.get("contacts", {})
        flags = emp.get(slug, {})
        known = set()
        for p_ in e.get("top_people", []):
            for k in p_["contacts"]:
                orig = k["person"]
                k["person"] = _strip_emoji(orig)
                known.add(norm_name(k["person"]))
                info = cdates.get(orig) or cdates.get(k["person"]) or {}
                k["last"] = info.get("last")
                k["mismatch"] = bool(info.get("mismatch"))
                f = flags.get(k["person"]) or {}
                k["moved"] = f.get("now") if f.get("status") == "moved" else None
        for pt in e.get("points", []):
            info = cdates.get(pt["external"]) or {}
            pt["external"] = _strip_emoji(pt["external"])
            pt["last"] = info.get("last")
            f = flags.get(pt["external"]) or {}
            pt["moved"] = f.get("now") if f.get("status") == "moved" else None
            known.add(norm_name(pt["external"]))
        if e["kind"] == "fund":
            ef = efunds.get(slug, {})
            e["website"] = ef.get("website")
            allp = []
            for p_ in (ef.get("partners") or []):
                n = _strip_emoji(p_.get("name") or "")
                if n:
                    allp.append({**p_, "name": n})
            e["partners_total"] = len(allp)
            e["partners_unknown"] = [p_ for p_ in allp if norm_name(p_.get("name")) not in known][:8]
            e["untracked"] = (ef.get("recent_untracked_eu") or [])[:12]
            e["recent_total"] = ef.get("recent_total")
            e["recent_eu"] = ef.get("recent_eu")
            e["co_investor_names"] = ef.get("co_investors") or []
        else:
            ea = eangels.get(slug, {})
            e["co_investor_names"] = ea.get("co_investors") or []
    return entities


def compute_bridges_and_synd(entities):
    """After finalize: for weak/medium entities, suggest routes via covered
    entities that co-invest with them; for angels, record syndication overlap."""
    by_norm = {norm_name(e["name"]): e for e in entities}
    # crude alias: also index without legal suffixes
    for e in entities:
        for e2name in list(by_norm):
            pass
    for e in entities:
        overlaps = []
        for cn in e.get("co_investor_names", []):
            t = by_norm.get(norm_name(cn))
            if t and t["slug"] != e["slug"]:
                overlaps.append(t)
        if e["kind"] == "angel":
            e["syndication"] = [{"name": t["name"], "slug": t["slug"], "tier": t["tier"],
                                 "via": (t["points"][0]["internal"] if t["points"] else None)}
                                for t in overlaps][:5]
        if e["tier"] in ("weak", "medium"):
            bridges = [t for t in overlaps if t["tier"] == "strong" and t["points"]]
            bridges.sort(key=lambda t: -t["connectivity"])
            e["bridges"] = [{"name": t["name"], "slug": t["slug"],
                             "internal": t["points"][0]["internal"],
                             "pct": t["points"][0]["pct"]} for t in bridges[:3]]
        else:
            e["bridges"] = []
        e.pop("co_investor_names", None)
    return entities


def build_htc(entities, htc_owners):
    """Inverted hard-to-crack view: company -> investors on cap table -> best path."""
    ho = htc_owners or {}
    companies = {}
    for e in entities:
        for p in e["buckets"].get("hard", []):
            c = companies.setdefault(p["id"], {"id": p["id"], "name": p["name"],
                                               "domain": p.get("domain"), "investors": []})
            best = e["points"][0] if e.get("points") else None
            c["investors"].append({"name": e["name"], "slug": e["slug"], "kind": e["kind"],
                                   "tier": e["tier"],
                                   "best": ({"internal": best["internal"], "pct": best.get("pct")}
                                            if best else None)})
    out = []
    for cid, c in companies.items():
        meta = ho.get(str(cid)) or ho.get(cid) or {}
        c["owners"] = [NAME_MAP.get(o, o) for o in (meta.get("owners") or [])
                       if o not in EX_STAFF]
        c["country"] = meta.get("country")
        c["reachable"] = any(i["best"] for i in c["investors"])
        out.append(c)
    out.sort(key=lambda c: (-c["reachable"], -len(c["investors"])))
    return out
