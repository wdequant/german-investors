#!/usr/bin/env python3
"""Build the multi-region coverage map (Germany + Nordics) -> viz/index.html"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import glob as _glob
from coverage_common import (finalize, TODAY, AFFINITY_ORG, load_json, apply_enrich,
                             compute_bridges_and_synd, build_htc, angel_relevance,
                             affinity_sync, inject_htc_captables,
                             collect_linkedin, backfill_linkedin, attach_dealflow)
import assemble_germany, assemble_nordics, assemble_france, assemble_us
import importlib.util as _ilu

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
team = load_json(f"{ROOT}/data/highland-team.json")
roster = [m["name"] for m in team] + ["Fergal Mullen", "Laurence Garrett", "Ronan Shally"]

empflags = load_json(f"{ROOT}/data/enrich/employment-flags.json", {})
htc_owners = load_json(f"{ROOT}/data/enrich/htc-owners.json", {})
aff_dump = load_json(f"{ROOT}/data/affinity/_list-entries.json", {})
angel_deals = load_json(f"{ROOT}/data/enrich/angel-deals.json", {})

# global cross-source LinkedIn index: harvest every name->URL pair we hold
LI_INDEX = {}
for _f in (["data/connections.json", "data/nordics/connections.json",
            "data/france/connections.json", "data/nordics/investors.json",
            "data/france/investors.json"]
           + [p.removeprefix(f"{ROOT}/") for p in
              _glob.glob(f"{ROOT}/data/enrich/partners-meta-*.json")
              + _glob.glob(f"{ROOT}/data/enrich/*-funds.json")
              + [f"{ROOT}/data/enrich/germany.json", f"{ROOT}/data/enrich/nordics.json"]]):
    collect_linkedin(load_json(f"{ROOT}/{_f}", {}), LI_INDEX)
print(f"linkedin index: {len(LI_INDEX)} names")

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
         "france": pmeta_france,
         "us": load_json(f"{ROOT}/data/enrich/partners-meta-us.json", {}) or {}}


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
    "us": {"label": "US → EU", "adj": "US tier-1", "assemble": assemble_us.assemble},
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
    li_filled = backfill_linkedin(ents, LI_INDEX)
    if li_filled:
        print(f"  [{key}] linkedin backfill: +{li_filled} URLs from cross-source index")
    added_by, rescued = affinity_sync(ents, aff_dump, key)
    from coverage_common import FUND_ALIASES, _nrm_inv
    for e in ents:  # live-sync metadata: query term + aliases for client-side matching
        if e["kind"] == "fund":
            als = sorted({_nrm_inv(a) for a in [e["name"]] + FUND_ALIASES.get(e["slug"], []) if _nrm_inv(a)})
            e["liveAliases"] = als
            e["liveTerm"] = min((a for a in als if len(a) >= 4), key=len, default=e["name"])
    # dealflow blocklist: Harmonic occasionally mis-merges a startup's round onto
    # an unrelated corporate record (e.g. E.ON SE carrying an Aug-26 "seed");
    # verified bad ids are filtered everywhere a deal row can surface.
    _df_block = {b.get("harmonic_company_id")
                 for b in load_json(f"{ROOT}/data/enrich/dealflow-blocklist.json", []) or []}
    _df = load_json(f"{ROOT}/data/enrich/dealflow-{key}.json", {}) or {}
    if _df_block:
        _df = {s: ([x for x in rows if isinstance(x, dict)
                    and x.get("harmonic_company_id") not in _df_block]
                   if isinstance(rows, list) else rows)
               for s, rows in _df.items()}
        for e in ents:
            if e.get("untracked"):
                e["untracked"] = [u for u in e["untracked"]
                                  if u.get("harmonic_company_id") not in _df_block]
    attach_dealflow(ents, _df, aff_dump)
    htc_added = inject_htc_captables(ents, load_json(f"{ROOT}/data/enrich/htc-captables.json", {}),
                                     htc_owners)
    # Unframe combined priority: brain score blended equally with note priority and
    # note sentiment (Unframe's documented combined_priority definition); companies
    # without notes rank on brain score alone. Drives relevance + per-company badges.
    def _combined(c):
        parts = [min(1.0, (c.get("score") or 0) / 100.0)]
        if c.get("notesPriority") is not None:
            parts.append(min(1.0, c["notesPriority"] / 5.0))
        v = (c.get("verdict") or "").lower()
        if v in ("positive", "negative", "neutral"):
            parts.append(1.0 if v == "positive" else 0.5 if v == "neutral" else 0.0)
        return round(100.0 * sum(parts) / len(parts), 1)

    uf_data = load_json(f"{ROOT}/data/enrich/unframe-{key}.json", {}) or {}
    uf_hit = 0
    uf_high_set = set()
    for e in ents:
        if e["kind"] != "fund":
            continue
        d = uf_data.get(e["slug"]) or {}
        comps = [c for c in (d.get("companies") or []) if c.get("score")]
        for c in comps:
            c["combined"] = _combined(c)
        scores = sorted((c["combined"] for c in comps), reverse=True)
        high = sum(1 for s in scores if s >= 85)
        avg10 = sum(scores[:10]) / min(10, len(scores)) if scores else 0.0
        pts = min(25.0, high * 2.5) + 15.0 * avg10 / 100.0
        e["uf"] = {"high": high, "avg10": round(avg10, 1),
                   "total": d.get("total") or 0, "pts": round(pts, 1),
                   "top": [{"name": c.get("name"), "domain": c.get("domain"),
                            "score": c["combined"], "tracking": c.get("tracking")}
                           for c in sorted(comps, key=lambda c: -c["combined"])[:3]]}
        for c in comps:
            if c["combined"] >= 85:
                uf_high_set.add((c.get("domain") or c.get("name") or "").lower())
        if e.get("relevance") and scores:
            r = e["relevance"]
            r["thesis"] = r["total"]
            r["unframe"] = round(pts, 1)
            r["total"] = round(0.6 * r["total"] + pts)
        bydom = {(c.get("domain") or "").lower(): c["combined"] for c in comps if c.get("domain")}
        byname = {(c.get("name") or "").lower(): c["combined"] for c in comps if c.get("name")}
        stamp = lambda o: bydom.get((o.get("domain") or "").lower()) or byname.get((o.get("name") or "").lower())
        for lst in e["buckets"].values():
            for p in lst:
                sc = stamp(p)
                if sc:
                    p["uf"] = sc
                    uf_hit += 1
        for u in e.get("untracked") or []:
            sc = stamp(u)
            if sc:
                u["uf"] = sc
                uf_hit += 1
    if uf_hit:
        print(f"  [{key}] unframe: {uf_hit} companies stamped with brain scores")
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
                    "ufHigh": len(uf_high_set),
                    "htc": build_htc(ents, htc_owners)}

# ---------- global post-pass: cross-region H2C paths, global Unframe index, cities ----------
from coverage_common import FUND_ALIASES as _FA, _nrm_inv as _ni, GENERIC_SUFFIX as _GS


def _combined_g(c):
    parts = [min(1.0, (c.get("score") or 0) / 100.0)]
    if c.get("notesPriority") is not None:
        parts.append(min(1.0, c["notesPriority"] / 5.0))
    v = (c.get("verdict") or "").lower()
    if v in ("positive", "negative", "neutral"):
        parts.append(1.0 if v == "positive" else 0.5 if v == "neutral" else 0.0)
    return round(100.0 * sum(parts) / len(parts), 1)


# global Unframe combined-priority index (domain + name), across every region's sweep
_uf_dom, _uf_name = {}, {}
for _k in REGION_CFG:
    for _slug, _d in (load_json(f"{ROOT}/data/enrich/unframe-{_k}.json", {}) or {}).items():
        for _c in (_d.get("companies") or []) if isinstance(_d, dict) else []:
            if not _c.get("score"):
                continue
            _sc = _combined_g(_c)
            if _c.get("domain"):
                _uf_dom[_c["domain"].lower()] = max(_sc, _uf_dom.get(_c["domain"].lower(), 0))
            if _c.get("name"):
                _uf_name[_c["name"].lower()] = max(_sc, _uf_name.get(_c["name"].lower(), 0))
for _d, _sc in (load_json(f"{ROOT}/data/enrich/unframe-fill.json", {}) or {}).items():
    if isinstance(_sc, (int, float)) and _sc > 0:
        _k = _d.lower().removeprefix("www.")
        _uf_dom[_k] = max(_sc, _uf_dom.get(_k, 0))
_uf_of = lambda o: (_uf_dom.get((o.get("domain") or "").lower().removeprefix("www."))
                    or _uf_name.get((o.get("name") or "").lower()))

# city stamp for pipeline + H2C companies (data/enrich/company-cities.json, Harmonic backfill)
_cities = load_json(f"{ROOT}/data/enrich/company-cities.json", {}) or {}
_city_of = lambda o: (_cities.get((o.get("domain") or "").lower().removeprefix("www.")) or {}).get("city")

# alias index over every entity in every region, for global cap-table matching
_alias2ent = {}
for _k, _reg in regions.items():
    for _e in _reg["entities"]:
        _als = {_ni(_e["name"])}
        if _e["kind"] == "fund":
            _als |= {_ni(a) for a in _FA.get(_e["slug"], [])}
            _w = _ni(_e["name"]).split()
            if len(_w) > 1 and _w[-1] in _GS:
                _als.add(" ".join(_w[:-1]))
        for _a in _als:
            if _a:
                _alias2ent.setdefault(_a, []).append((_k, _e))

_captables = load_json(f"{ROOT}/data/enrich/htc-captables.json", {}) or {}
_xreg = 0
_xun = 0

# untracked backers: backer name -> domain -> Highland's live Affinity edges
from coverage_common import NAME_MAP as _NM0, EX_STAFF as _EX0
_bdom = {}
for _n, _m in (load_json(f"{ROOT}/data/enrich/backer-domains.json", {}) or {}).items():
    _d = (_m.get("domain") or "").lower().removeprefix("www.")
    if _d and _m.get("kind") != "person":
        _bdom[_ni(_n)] = _d
_brels = load_json(f"{ROOT}/data/enrich/backer-rels.json", {}) or {}
_hmeta = load_json(f"{ROOT}/data/enrich/htc-meta.json", {}) or {}
_profiles_raw = load_json(f"{ROOT}/data/enrich/company-profiles.json", {}) or {}
_profiles = {}
for _d, _p in _profiles_raw.items():
    if not _p or not _p.get("name"):
        continue
    _desc = (_p.get("desc") or "").strip()
    if len(_desc) > 300:
        _desc = _desc[:300].rsplit(" ", 1)[0].rstrip(" ,;:") + "…"
    elif len(_desc) >= 165 and _desc[-1] not in ".!?":   # fetch-side mid-word cut
        _desc = _desc.rsplit(" ", 1)[0].rstrip(" ,;:") + "…"
    _profiles[_d] = {k: v for k, v in {
        "d": _desc or None, "hc": _p.get("hc"), "hg": _p.get("hc_yoy"),
        "f": _p.get("founded"), "fu": _p.get("funding_usd"),
        "st": _p.get("stage")}.items() if v is not None}


def _bdecay(last):
    if not last:
        return 0.85
    days = (TODAY.date() - __import__("datetime").date.fromisoformat(str(last)[:10])).days
    return 1.0 if days <= 180 else 0.9 if days <= 365 else 0.5 if days <= 730 else 0.3


_bflags = load_json(f"{ROOT}/data/enrich/employment-flags-backers.json", {}) or {}


def _backer_paths(dom):
    """Top Highland paths into an untracked backer, scored like fund paths."""
    best = {}
    _bf = _bflags.get(dom) or {}
    for r in (_brels.get(dom) or {}).get("rels") or []:
        nm = _NM0.get(r["internal"], r["internal"])
        if nm in _EX0:
            continue
        _st = (_bf.get(r.get("external") or "") or {}).get("status")
        if _st == "moved":          # left the backer — not a door into it anymore
            continue
        pct = round(100 * (r.get("score") or 0) * _bdecay(r.get("last"))
                    * (1.0 if r.get("meet") else 0.75))
        if pct <= 0:
            continue
        p = {"internal": nm, "external": r["external"], "pct": pct, "moved": None,
             "unverified": not r.get("meet"), "email": r.get("externalEmail"),
             "ever": _st == "current"}
        # keyed per (holder, contact): a viewer's own weaker edge must survive
        # the team's stronger one, so the UI can prefer doors the viewer holds
        k = (nm, r["external"])
        if k not in best or pct > best[k]["pct"]:
            best[k] = p
    return sorted(best.values(), key=lambda p: -p["pct"])[:8]


def _resolve_backers(_c, _backers):
    """Match a company's backer names against every tracked entity; give
    untracked backers paths from their own Affinity edges where we hold any;
    keep the rest as 'others'."""
    global _xreg, _xun
    _have = {_i["slug"] for _i in _c["investors"]}
    _others = []
    for _inv in _backers:
        _niv = _ni(_inv)
        if not _niv:
            continue
        _best = None
        for _a, _ents in _alias2ent.items():
            if (_niv == _a or (_niv.startswith(_a + " ") and len(_a.split()) >= 2)) \
                    and (_best is None or len(_a) > len(_best[0])):
                _best = (_a, _ents)
        if not _best:
            _bp = _backer_paths(_bdom[_niv]) if _niv in _bdom else []
            if _bp:
                _c["investors"].append({"name": _inv.strip(), "slug": None,
                                        "kind": "fund", "tier": "x", "region": None,
                                        "untracked": True,
                                        "best": _bp[0], "paths": _bp})
                _xun += 1
            else:
                _others.append(_inv)
            continue
        for _rk, _e in _best[1]:
            if _e["slug"] in _have:
                continue
            _have.add(_e["slug"])
            _paths = [{"internal": pt["internal"], "external": pt.get("external"),
                       "pct": pt.get("pct"), "moved": pt.get("moved"),
                       "unverified": pt.get("unverified"), "email": pt.get("email"),
                       "linkedin": pt.get("linkedin")}
                      for pt in (_e.get("points") or [])[:3]]
            _c["investors"].append({"name": _e["name"], "slug": _e["slug"],
                                    "kind": _e["kind"], "tier": _e["tier"],
                                    "region": _rk, "best": _paths[0] if _paths else None,
                                    "paths": _paths})
            _xreg += 1
    # drop 'others' that are really a matched investor under another spelling,
    # then dedupe near-identical backer names (Sequoia vs Sequoia Capital)
    _mn = {_ni(i["name"]) for i in _c["investors"]}
    _others = [o.strip() for o in _others
               if not any(_ni(o) == m or _ni(o).startswith(m + " ") or m.startswith(_ni(o) + " ")
                          for m in _mn)]
    _c["others"] = sorted({o for o in _others
                           if not any(_ni(o) != _ni(p) and _ni(o) in _ni(p) for p in _others)})[:8]
    _c["investors"].sort(key=lambda i: -(((i.get("best") or {}).get("pct")) or 0))
    _c["reachable"] = any(i.get("best") for i in _c["investors"])


for _k, _reg in regions.items():
    for _c in _reg["htc"]:
        _c["uf"] = _uf_of(_c)
        _c["city"] = _city_of(_c)
        for _i in _c["investors"]:
            _i["region"] = _k
        _cap = _captables.get(str(_c["id"])) or {}
        _c["meta"] = _hmeta.get(str(_c["id"]))
        _resolve_backers(_c, _cap.get("investors") or [])
    _reg["htc"].sort(key=lambda c: (-(c.get("uf") or 0), -c["reachable"], -len(c["investors"])))

# every remaining Affinity hard-to-crack (any owner), even when no tracked fund
# backs it — the H2C workflow covers the whole book, not just tracked-fund overlap
from coverage_common import NAME_MAP as _NM, EX_STAFF as _EX, owners_departed as _odep
_seen_h = {c["id"] for r in regions.values() for c in r["htc"]}
_xtra = []
for _ent in (aff_dump or {}).get("entries") or []:
    if _ent.get("funnel") != "Hard to crack" or _ent["id"] in _seen_h or _odep(_ent):
        continue
    _c = {"id": _ent["id"], "name": _ent.get("name"),
          "domain": (_ent.get("domains") or [None])[0],
          "owners": [_NM.get(o, o) for o in (_ent.get("owners") or []) if o not in _EX],
          "country": _ent.get("country"), "investors": []}
    _c["uf"] = _uf_of(_c)
    _c["city"] = _city_of(_c)
    _c["meta"] = _hmeta.get(str(_ent["id"]))
    _cap = _captables.get(str(_ent["id"])) or {}
    _resolve_backers(_c, _cap.get("investors") or _ent.get("investors") or [])
    _xtra.append(_c)
_xtra.sort(key=lambda c: (-(c.get("uf") or 0), -c["reachable"], -len(c["investors"])))

# global fallback stamping: score + city on every pipeline entry
_gstamp = _cstamp = 0
for _k, _reg in regions.items():
    for _e in _reg["entities"]:
        for _lst in _e["buckets"].values():
            for _p in _lst:
                if _p.get("uf") is None:
                    _sc = _uf_of(_p)
                    if _sc:
                        _p["uf"] = _sc
                        _gstamp += 1
                if _p.get("city") is None:
                    _ct = _city_of(_p)
                    if _ct:
                        _p["city"] = _ct
                        _cstamp += 1
print(f"global pass: +{_xreg} cross-region H2C links, +{_gstamp} unframe stamps, "
      f"+{_cstamp} city stamps ({len(_cities)} cities known), "
      f"+{len(_xtra)} Affinity H2Cs beyond tracked funds, +{_xun} untracked-backer paths")

_spec = _ilu.spec_from_file_location("coverage_template",
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "coverage_template.py"))
_tpl = _ilu.module_from_spec(_spec); _spec.loader.exec_module(_tpl)

_dump_date = (aff_dump or {}).get("fetched") or "17 Aug 2026"
try:
    from datetime import date as _date
    _dump_date = _date.fromisoformat(_dump_date).strftime("%d %b %Y")
except ValueError:
    pass
_uf_any = any(r.get("ufHigh") for r in regions.values())
import glob as _glob
_rels_date = max((d.get("rels_fetched") or ""
                  for p in _glob.glob(f"{ROOT}/data/affinity/*.json")
                  + _glob.glob(f"{ROOT}/data/*/affinity/*.json")
                  for d in [load_json(p, {})] if isinstance(d, dict)),
                 default="") or None
try:
    from datetime import date as _date2
    _rels_date = _date2.fromisoformat(_rels_date).strftime("%d %b %Y") if _rels_date else None
except ValueError:
    _rels_date = None
freshness = {
    "Harmonic universe & network": "12 Aug 2026",
    "Affinity pipeline": _dump_date,
    "Affinity relationships (paths in)": _rels_date or "17 Aug 2026",
    "Partner rosters, recent deals, recency": "17 Aug 2026",
}
if _uf_any:
    freshness["Unframe priority scores"] = TODAY.strftime("%d %b %Y")
# what's-changed: diff current dump vs weekly baseline, scoped to tracked investors
_base = load_json(f"{ROOT}/data/affinity/_baseline.json", {}) or {}
changes = {}
if _base.get("entries") and (aff_dump or {}).get("entries"):
    _prevby = {e["entry_id"]: e for e in _base["entries"]}
    _RANK = {"Pre-lead": 1, "Hard to crack": 2, "Awaiting Reply": 3, "Reach Out Now": 4,
             "Lead": 5, "Qualified Lead": 6, "Deal": 7, "Term Sheet Presented": 8,
             "Portfolio Company": 9}
    for rk, r in regions.items():
        comp2funds = {}
        for e in r["entities"]:
            if e["kind"] != "fund":
                continue
            for lst in e["buckets"].values():
                for pp in lst:
                    if pp.get("id"):
                        comp2funds.setdefault(pp["id"], set()).add(e["name"])
        moves, added, seen = [], [], set()
        for ce in aff_dump["entries"]:
            funds = comp2funds.get(ce.get("id"))
            if not funds:
                continue
            pe = _prevby.get(ce.get("entry_id"))
            fund = sorted(funds)[0]
            key = (ce.get("id"), fund)
            if key in seen:
                continue
            if pe is None:
                seen.add(key)
                added.append({"name": ce.get("name"), "id": ce.get("id"),
                              "funnel": ce.get("funnel"), "fund": fund})
            elif (pe.get("funnel") or "") != (ce.get("funnel") or "") and ce.get("funnel"):
                seen.add(key)
                moves.append({"name": ce.get("name"), "id": ce.get("id"),
                              "from": pe.get("funnel"), "to": ce.get("funnel"), "fund": fund,
                              "up": _RANK.get(ce.get("funnel"), 0) >= _RANK.get(pe.get("funnel") or "", 0)})
        moves.sort(key=lambda m: -_RANK.get(m["to"], 0))
        changes[rk] = {"since": _base.get("fetched"), "moves": moves[:15], "added": added[:15]}
        if moves or added:
            print(f"  [{rk}] what's-changed: {len(moves)} funnel moves, {len(added)} new entries since {_base.get('fetched')}")

# ---- per-person investor network (My People page) + recent movers feed ----
import glob as _glob
from coverage_common import _strip_emoji
_slug2 = {}
for _rk0, _reg0 in regions.items():
    for _e0 in _reg0["entities"]:
        if _e0["kind"] == "fund":
            _slug2[_e0["slug"]] = (_e0["name"], _rk0)
_bflags2 = load_json(f"{ROOT}/data/enrich/employment-flags-backers.json", {}) or {}
_mvdates = load_json(f"{ROOT}/data/enrich/mover-dates.json", {}) or {}
_bd2 = {}
for _bn, _bm in (load_json(f"{ROOT}/data/enrich/backer-domains.json", {}) or {}).items():
    _d0 = (_bm.get("domain") or "").lower().removeprefix("www.")
    if _d0 and _d0 not in _bd2:
        _bd2[_d0] = _bn
_mynet, _knew = {}, {}
def _net_add(intern, entry):
    _mynet.setdefault(intern, []).append(entry)
for _f0 in _glob.glob(f"{ROOT}/data/*/affinity/*.json"):
    try:
        _d1 = json.load(open(_f0))
    except Exception:
        continue
    _sl = _d1.get("slug") or os.path.basename(_f0)[:-5]
    if _sl not in _slug2:
        continue
    _fund, _rk1 = _slug2[_sl]
    _fl1 = ((empflags or {}).get(_rk1, {}) or {}).get(_sl, {}) or {}
    for _r1 in _d1.get("relationships") or []:
        _in = _NM.get(_r1.get("internal"), _r1.get("internal"))
        _ex = _strip_emoji(_r1.get("external") or "")
        if not _ex or _in in _EX:
            continue
        _pc = round((_r1.get("score") or 0) * 100)
        if _pc >= 40:
            _knew.setdefault(_ex, set()).add(_in)
        _st1 = (_fl1.get(_ex) or {}).get("status")
        if _st1 == "moved" or _pc < 15:
            continue
        _net_add(_in, {"n": _ex, "f": _fund, "s": _sl, "g": _rk1, "p": _pc,
                       "l": _r1.get("last"), "m": _r1.get("meet"),
                       "e": _r1.get("externalEmail"), "v": _st1 == "current"})
for _dm, _bv in (_brels or {}).items():
    _bnm = _bd2.get(_dm, _dm)
    _fl2 = (_bflags2.get(_dm) or {})
    for _r2 in _bv.get("rels") or []:
        _in = _NM.get(_r2.get("internal"), _r2.get("internal"))
        _ex = _strip_emoji(_r2.get("external") or "")
        if not _ex or _in in _EX:
            continue
        _pc = round((_r2.get("score") or 0) * 100)
        if _pc >= 40:
            _knew.setdefault(_ex, set()).add(_in)
        _st2 = (_fl2.get(_ex) or {}).get("status")
        if _st2 == "moved" or _pc < 15:
            continue
        _net_add(_in, {"n": _ex, "f": _bnm, "d": _dm, "p": _pc,
                       "l": _r2.get("last"), "m": _r2.get("meet"),
                       "e": _r2.get("externalEmail"), "v": _st2 == "current"})
for _k2 in _mynet:   # dedupe same contact tracked under two region entries, strongest first, cap
    _best = {}
    for _e3 in _mynet[_k2]:
        _old = _best.get(_e3["n"])
        if _old is None or (_e3["v"], _e3["p"], _e3.get("l") or "") > (_old["v"], _old["p"], _old.get("l") or ""):
            _best[_e3["n"]] = _e3
    _mynet[_k2] = sorted(_best.values(), key=lambda x: -x["p"])[:400]
_movers, _mvseen = [], set()
def _mv_add(name, from_name, info):
    _nk = name.lower()   # "Omri BENAYOUN" and "Omri Benayoun" are one person
    if _nk in _mvseen:
        return
    _mvseen.add(_nk)
    _md = _mvdates.get(name) or {}
    _movers.append({"n": name, "fr": from_name, "now": info.get("now"),
                    "since": _md.get("since"), "co": _md.get("company"),
                    "ti": _md.get("title"),
                    "k": sorted(_knew.get(name, []))})
for _rk2, _sm in (empflags or {}).items():
    for _sl2, _pp in (_sm or {}).items():
        for _nm2, _vv in (_pp or {}).items():
            if _vv.get("status") == "moved" and _sl2 in _slug2:
                _mv_add(_nm2, _slug2[_sl2][0], _vv)
for _dm2, _pp2 in _bflags2.items():
    for _nm3, _vv2 in (_pp2 or {}).items():
        if _vv2.get("status") == "moved":
            _mv_add(_nm3, _bd2.get(_dm2, _dm2), _vv2)
print(f"mynet: {sum(len(v) for v in _mynet.values())} edges across {len(_mynet)} people; "
      f"movers: {len(_movers)} ({sum(1 for m in _movers if m['since'])} dated)")

payload = {"generated": TODAY.strftime("%d %b %Y"), "team": team, "roster": roster,
           "affinityOrg": AFFINITY_ORG, "regions": regions, "xhtc": _xtra,
           "profiles": _profiles, "freshness": freshness,
           "changes": changes,
           "untProfiles": load_json(f"{ROOT}/data/enrich/untracked-profiles.json", {}) or {},
           "mynet": _mynet, "movers": _movers}
from coverage_common import _strip_emoji
_aff_ids = load_json(f"{ROOT}/data/enrich/untracked-affinity-ids.json", {}) or {}
for _cid, _v in payload["untProfiles"].items():  # sanitize + join Affinity ids
    for _f in _v.get("founders") or []:
        if _f.get("name"):
            _f["name"] = _strip_emoji(_f["name"].replace("�", ""))
    if _v.get("desc"):
        _v["desc"] = _strip_emoji(_v["desc"].replace("�", ""))
    _v["affinity_id"] = _aff_ids.get(str(_cid)) or _aff_ids.get(_cid)
html = (_tpl.TEMPLATE
        .replace("__DATA__", json.dumps(payload, ensure_ascii=False).replace("\ufffd", ""))
        .replace("__GENERATED__", payload["generated"]))
os.makedirs(f"{ROOT}/viz", exist_ok=True)
open(f"{ROOT}/viz/index.html", "w").write(html)
# same payload for the /api/ask serverless chat (gitignored; bundled at deploy time)
open(f"{ROOT}/deploy/api/_data.json", "w").write(json.dumps(payload, ensure_ascii=False).replace("\ufffd", ""))
for k, r in regions.items():
    f = [e for e in r["entities"] if e["kind"] == "fund"]
    unt = sum(len(e.get("untracked") or []) for e in f)
    print(f"{k}: {len(f)} funds + {len(r['entities'])-len(f)} angels, "
          f"{len(r['htc'])} HTCs, {unt} untracked EU deals shown")
print(f"wrote viz/index.html ({len(html)//1024} KB)")
