"""Shared scoring and assembly helpers for the multi-region coverage map."""
import json, math, os, re, unicodedata
from datetime import datetime, timezone

TODAY = datetime(2026, 8, 12, tzinfo=timezone.utc)
AFFINITY_ORG = "highland"  # tenant subdomain per Affinity get_current_user
EX_STAFF = {"Emily Tan", "Anna Faulkner", "Zina Alfa", "Rachel Barbour-Fowles",
            "Isabel Wright"}
NAME_MAP = {"Gajan Rajanathan": "Gaj Rajanathan", "William De Quant": "Will de Quant",
            "Stan Laurent": "Stan"}
# User-confirmed corrections to the automated employment check: these contacts
# are still at their fund (board seats / portfolio roles misread as departures).
EMP_OVERRIDES = {
    "Alexander Joel-Carbonell",   # led HV's investment in AMI, still at HV
    "Jean de La Rochebrochard",   # still at Kima; runs Cassius and New Wave alongside
    "Jean de la Rochebrochard",
}
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


def dedup_key(s):
    """Person-dedupe key that also collapses German transliterations, so
    'Julius Lühr' (Affinity) and 'Julius Luehr' (Harmonic) merge."""
    n = norm_name(s)
    for a, b in (("ue", "u"), ("oe", "o"), ("ae", "a"), ("ss", "s")):
        n = n.replace(a, b)
    return re.sub(r"[^a-z ]", "", n).strip()


def clean_rels(rels):
    """Drop Affinity relationships held only by ex-staff before any scoring."""
    return [r for r in (rels or [])
            if NAME_MAP.get(r.get("internal"), r.get("internal")) not in EX_STAFF]


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
            p["contacts"].append({"person": r["external"], "pct": round(sc * 100),
                                  "email": r.get("externalEmail") or None, "linkedin": None})
    if cells:
        for u, c in cells.items():
            if c["score"] <= 0 or u in EX_STAFF:
                continue
            p = people.setdefault(u, {"name": u, "aff": 0.0, "harmonic": 0.0, "contacts": []})
            p["harmonic"] = c["score"]
            for k in c["contacts"][:3]:
                if k["external"] or k["w"] < 2:
                    continue
                m = next((x for x in p["contacts"]
                          if dedup_key(x["person"]) == dedup_key(k["person"])), None)
                if m:  # same human from both sources: merge title/linkedin in
                    if not m.get("title"):
                        m["title"] = k["title"]
                    if not m.get("linkedin"):
                        m["linkedin"] = k.get("linkedin")
                else:
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
        key = dedup_key(r.get("external", ""))
        if key in seen:
            continue
        seen.add(key)
        points.append({"external": r.get("external"), "internal": nm,
                       "pct": round((r.get("score") or 0) * 100),
                       "email": r.get("externalEmail") or None,
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
    if not d or not d.get("last"):  # bare CRM record with no interaction history
        return 0.0
    yr = int(str(d["last"])[:4])
    age = 2026 - yr
    return 0.22 if age <= 1 else 0.15 if age <= 3 else 0.10 if age <= 6 else 0.06


def finalize(entities):
    """Blend connectivity (with recency decay), compute gap + tier."""
    funds = [e for e in entities if e["kind"] == "fund"]
    hmax = max((e["harmonic_raw"] for e in funds), default=1) or 1
    for e in entities:
        if e.get("dormant") and not e["dormant"].get("last"):
            e["dormant"] = None  # bare CRM record, no history: not a re-warmable path
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


def apply_enrich(entities, enrich, recency, empflags, region_key, pmeta=None):
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
                k["moved"] = (f.get("now") if f.get("status") == "moved"
                              and k["person"] not in EMP_OVERRIDES else None)
        for pt in e.get("points", []):
            info = cdates.get(pt["external"]) or {}
            pt["external"] = _strip_emoji(pt["external"])
            pt["last"] = info.get("last")
            f = flags.get(pt["external"]) or {}
            pt["moved"] = (f.get("now") if f.get("status") == "moved"
                           and pt["external"] not in EMP_OVERRIDES else None)
            known.add(norm_name(pt["external"]))
        # equal-strength paths: current-at-fund beats moved, then most recent
        # touch wins (a 100% from February shouldn't outrank one from July)
        e["points"] = sorted(e.get("points") or [], key=lambda pt: (
            -(pt.get("pct") or 0), bool(pt.get("moved")),
            -int((pt.get("last") or "0").replace("-", "")[:8] or 0)))
        if e["kind"] == "fund":
            ef = efunds.get(slug, {})
            e["website"] = ef.get("website")
            allp = []
            for p_ in (ef.get("partners") or []):
                n = _strip_emoji(p_.get("name") or "")
                if n:
                    allp.append({**p_, "name": n})
            e["partners_total"] = len(allp)
            meta = (pmeta or {}).get(slug, {})
            p_known, p_unknown = [], []
            for p_ in allp:
                if norm_name(p_.get("name")) in known:
                    continue
                m = meta.get(p_["name"]) or {}
                li = p_.get("linkedin") or m.get("linkedin")
                if (m.get("known_internal") and m["known_internal"] not in EX_STAFF
                        and ((m.get("known_score") or 0) >= 0.1 or m.get("note"))):
                    p_known.append({"name": p_["name"], "linkedin": li,
                                    "internal": m["known_internal"], "score": m.get("known_score"),
                                    "last": m.get("last"), "note": m.get("note")})
                else:
                    p_unknown.append({**p_, "linkedin": li})
            e["partners_known"] = p_known[:8]
            e["partners_unknown"] = p_unknown[:8]
            e["untracked"] = ef.get("recent_untracked_eu") or []
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


GENERIC_SUFFIX = {"capital", "partners", "ventures", "venture", "vc", "invest",
                  "management", "fund", "funds", "gmbh", "ab", "oy", "as", "aps", "ag"}
FUND_ALIASES = {
    "gfc": ["global founders capital", "gfc"],
    "htgf": ["htgf", "high tech grunderfonds", "high tech gruenderfonds"],
    "hv-capital": ["hv capital", "hv holtzbrinck ventures", "holtzbrinck ventures", "hv ventures", "hv"],
    "earlybird": ["earlybird", "earlybird venture capital", "earlybird vc"],
    "point-nine": ["point nine", "point nine capital", "point 9"],
    "cherry": ["cherry ventures", "cherry vc"],
    "project-a": ["project a", "project a ventures"],
    "ibb-ventures": ["ibb ventures", "ibb beteiligungsgesellschaft"],
    "bosch-ventures": ["bosch ventures", "robert bosch venture capital", "rbvc"],
    "uvc-partners": ["uvc partners", "unternehmertum venture capital"],
    "mig-capital": ["mig capital", "mig ag", "mig fonds", "mig verwaltungs"],
    "acton": ["acton capital", "acton capital partners", "acton"],
    "dvh-ventures": ["dieter von holtzbrinck ventures", "dvh ventures"],
    "vsquared": ["vsquared ventures", "vsquared", "v squared ventures"],
    "burda": ["burda principal investments"],
    "alstin": ["alstin capital", "alstin"],
    "redstone": ["redstone", "redstone digital", "redstone vc"],
    "10x-founders": ["10x founders", "10x group"],
    "northzone": ["northzone", "northzone ventures"],
    "lifeline": ["lifeline ventures"],
    "seed-capital": ["seed capital", "seedcapital"],
    "psv": ["psv", "psv tech", "psv ventures"],
    "eqt-ventures": ["eqt ventures"],
    "icebreaker": ["icebreaker vc", "icebreaker"],
    "alliance-vc": ["alliance vc", "alliance venture"],
    "norrsken": ["norrsken", "norrsken vc"],
    "maki": ["maki vc", "maki"],
    "first-fellow": ["first fellow partners", "first fellow"],
    "j12": ["j12", "j12 ventures"],
    "almi": ["almi"],
    "almi-invest": ["almi invest"],
    "heartcore": ["heartcore", "heartcore capital"],
    # france
    "kima": ["kima ventures", "kima"],
    "eurazeo": ["eurazeo", "idinvest partners", "idinvest", "eurazeo growth", "eurazeo venture"],
    "partech": ["partech", "partech partners", "partech ventures"],
    "aglae": ["aglae ventures", "aglae"],
    "elaia": ["elaia", "elaia partners"],
    "sofinnova": ["sofinnova partners", "sofinnova"],
    "xange": ["xange", "xange private equity"],
    "alven": ["alven", "alven capital"],
    "cathay": ["cathay innovation"],
    "newfund": ["newfund", "newfund capital"],
    "founders-future": ["founders future"],
    "motier": ["motier ventures", "motier"],
    "serena": ["serena", "serena capital", "serena ventures fr"],
    "seventure": ["seventure partners", "seventure"],
    "omnes": ["omnes capital", "omnes"],
    "demeter": ["demeter", "demeter partners", "demeter im"],
    "daphni": ["daphni"],
    "saint-james": ["financiere saint james", "saint james"],
    "50-partners": ["50 partners", "50partners"],
    "ventech": ["ventech"],
    "breega": ["breega", "breega capital"],
    "go-capital": ["go capital"],
    "evolem": ["evolem"],
    "bpifrance": ["bpifrance", "bpifrance large venture", "bpifrance digital venture",
                  "large venture", "bpi france"],
    "singular": ["singular", "singular capital partners"],
    "frst": ["frst", "frst capital"],
    "isai": ["isai", "isai gestion"],
    "otium": ["otium capital", "otium"],
    "hexa": ["hexa", "efounders", "e founders", "logic founders"],
}


def _nrm_inv(s):
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9 ]+", " ", norm_name(s))).strip()


def affinity_sync(entities, dump, region_key):
    """Reconcile fund pipelines against a full dump of the Affinity list:
    union in every entry whose investors field names the fund (alias-matched,
    longest alias wins so 'Almi Invest' never lands under 'Almi'), refresh
    funnel stages from the dump, and rescue 'untracked' deals that are in
    fact tracked in Affinity (moving them into the right funnel bucket)."""
    if not dump or not dump.get("entries"):
        return {}, {}
    entries = dump["entries"]
    by_domain, by_name = {}, {}
    for ent in entries:
        for d in (ent.get("domains") or []):
            if d:
                by_domain.setdefault(d.lower().removeprefix("www."), ent)
        by_name.setdefault(_nrm_inv(ent.get("name")), ent)

    funds = {e["slug"]: e for e in entities if e["kind"] == "fund"}
    alias2slug = {}
    for slug, e in funds.items():
        als = {_nrm_inv(e["name"])} | {_nrm_inv(a) for a in FUND_ALIASES.get(slug, [])}
        w = _nrm_inv(e["name"]).split()
        if len(w) > 1 and w[-1] in GENERIC_SUFFIX:
            als.add(" ".join(w[:-1]))
        for a in als:
            if a:
                alias2slug.setdefault(a, set()).add(slug)

    matched = {slug: {} for slug in funds}
    for ent in entries:
        for inv in (ent.get("investors") or []):
            ni = _nrm_inv(inv)
            if not ni:
                continue
            best = None
            for a, slugs in alias2slug.items():
                ok = ni == a or (ni.startswith(a + " ") and len(a.split()) >= 2)
                if ok and (best is None or len(a) > len(best[0])):
                    best = (a, slugs)
            if best:
                for slug in best[1]:
                    matched[slug][ent["id"]] = ent

    added_by = {}
    for slug, ents in matched.items():
        e = funds[slug]
        pipe = {p["id"]: p for k in e["buckets"] for p in e["buckets"][k]}
        added = 0
        for cid, ent in ents.items():
            f = ent.get("funnel")
            if cid in pipe:
                if f and pipe[cid].get("funnel") != f:
                    pipe[cid]["funnel"] = f  # dump is today's Affinity state
                continue
            if not f or f == "Passed" or f.startswith("Deprioritised"):
                continue
            pipe[cid] = {"id": cid, "name": ent.get("name"),
                         "domain": (ent.get("domains") or [None])[0],
                         "funnel": f, "country": ent.get("country")}
            added += 1
        e["buckets"] = bucket_pipeline(list(pipe.values()))
        if added:
            added_by[slug] = added

    rescued = {}
    for e in entities:
        keep = []
        for u in (e.get("untracked") or []):
            d = (u.get("domain") or "").lower().removeprefix("www.")
            ent = (by_domain.get(d) if d else None) or by_name.get(_nrm_inv(u.get("name")))
            if ent:  # in Affinity at all -> not 'untracked'
                b = ("portfolio" if ent.get("funnel") == "Portfolio Company"
                     else TEXT2BUCKET.get(ent.get("funnel")))
                if b:
                    pipe_ids = {p["id"] for k in e["buckets"] for p in e["buckets"][k]}
                    if ent["id"] not in pipe_ids:
                        e["buckets"][b].append({"id": ent["id"], "name": ent.get("name"),
                                                "domain": d or None, "funnel": ent.get("funnel"),
                                                "country": ent.get("country") or u.get("country")})
                rescued.setdefault(e["slug"], []).append(u["name"])
            else:
                keep.append(u)
        if e.get("untracked") is not None:
            e["untracked"] = keep

    # stamp Affinity owners onto every pipeline item (drives personal pipeline view)
    id2own = {ent["id"]: [NAME_MAP.get(o, o) for o in (ent.get("owners") or [])
                          if o not in EX_STAFF] for ent in entries}
    for e in entities:
        for lst in e["buckets"].values():
            for p in lst:
                p["own"] = id2own.get(p["id"], p.get("own") or [])
    return added_by, rescued


def inject_htc_captables(entities, captables, htc_owners=None):
    """Add missing investor <-> hard-to-crack links using Harmonic cap tables:
    Affinity's investor enrichment misses many real backers (e.g. Serena on
    Pelico), so a fund can be invested in one of our HTCs without its Affinity
    pipeline showing it. Harmonic's cap table is the source of truth here."""
    if not captables:
        return 0
    ho = htc_owners or {}
    ents = {e["slug"]: e for e in entities}
    alias2slug = {}
    for e in entities:
        als = {_nrm_inv(e["name"])}
        if e["kind"] == "fund":
            als |= {_nrm_inv(a) for a in FUND_ALIASES.get(e["slug"], [])}
            w = _nrm_inv(e["name"]).split()
            if len(w) > 1 and w[-1] in GENERIC_SUFFIX:
                als.add(" ".join(w[:-1]))
        for a in als:
            if a:
                alias2slug.setdefault(a, set()).add(e["slug"])
    added = 0
    for cid_s, c in captables.items():
        cid = int(cid_s) if str(cid_s).isdigit() else cid_s
        meta = ho.get(str(cid)) or {}
        for inv in c.get("investors") or []:
            ni = _nrm_inv(inv)
            if not ni:
                continue
            best = None
            for a, slugs in alias2slug.items():
                ok = ni == a or (ni.startswith(a + " ") and len(a.split()) >= 2)
                if ok and (best is None or len(a) > len(best[0])):
                    best = (a, slugs)
            if not best:
                continue
            for slug in best[1]:
                e = ents[slug]
                allids = {p["id"] for k in e["buckets"] for p in e["buckets"][k]}
                if cid in allids:
                    continue
                e["buckets"]["hard"].append({
                    "id": cid, "name": c.get("name"), "domain": c.get("domain"),
                    "funnel": "Hard to crack", "country": meta.get("country"),
                    "own": [NAME_MAP.get(o, o) for o in (meta.get("owners") or [])
                            if o not in EX_STAFF]})
                added += 1
    return added


def build_htc(entities, htc_owners):
    """Inverted hard-to-crack view: company -> investors on cap table -> best path."""
    ho = htc_owners or {}
    companies = {}
    for e in entities:
        for p in e["buckets"].get("hard", []):
            c = companies.setdefault(p["id"], {"id": p["id"], "name": p["name"],
                                               "domain": p.get("domain"), "investors": []})
            paths = [{"internal": pt["internal"], "external": pt.get("external"),
                      "pct": pt.get("pct"), "moved": pt.get("moved"),
                      "email": pt.get("email")}
                     for pt in (e.get("points") or [])[:3]]
            c["investors"].append({"name": e["name"], "slug": e["slug"], "kind": e["kind"],
                                   "tier": e["tier"], "best": paths[0] if paths else None,
                                   "paths": paths})
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
