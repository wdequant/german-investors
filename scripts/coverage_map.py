"""Coverage Map (spec: docs/coverage-map/discovery.md).

Everything heavy happens here at build time: Natural Earth geometry is decoded,
projected (Lambert azimuthal equal-area, centre 10E 52N) and emitted as SVG path
strings; all five scores from spec section 6 are computed per user; bubbles are
packed per city. The client only draws. M1 scope: Nordics active, rest greyed.
"""
import json, math, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOPO = f"{ROOT}/data/geo/countries-50m.json"
TOPO_FALLBACK = TOPO

# ---- config (spec: config/regions.ts + config/scoring.ts) ----
NORDIC_CC = ["SE", "DK", "NO", "FI", "IS"]
CC_NAME = {"SE": "Sweden", "DK": "Denmark", "NO": "Norway", "FI": "Finland", "IS": "Iceland"}
COUNTRY_CC = {v: k for k, v in CC_NAME.items()}
EURO_BG = ["Germany", "Austria", "Switzerland", "France", "Netherlands", "Belgium",
           "Luxembourg", "United Kingdom", "Ireland", "Spain", "Portugal", "Italy",
           "Greece", "Poland", "Czechia", "Estonia", "Latvia", "Lithuania", "Romania",
           "Hungary", "Slovakia", "Slovenia", "Croatia", "Bulgaria", "Serbia",
           "Bosnia and Herz.", "Albania", "North Macedonia", "Ukraine", "Belarus",
           "Moldova", "Montenegro", "Kosovo"]
EXTRA_BG = ["Greenland", "Turkey", "Morocco", "Algeria", "Tunisia", "Libya", "Egypt",
            "Israel", "Lebanon", "Jordan", "Syria", "Cyprus", "Georgia", "Armenia", "Azerbaijan", "Iraq"]
REGIONS = [  # L0 bubbles; only nordics is live in M1
    {"id": "nordics", "name": "Nordics", "ll": (16.0, 62.5), "active": True},
    {"id": "dach", "name": "DACH", "ll": (10.8, 48.8)},
    {"id": "france", "name": "France", "ll": (2.5, 46.8)},
    {"id": "benelux", "name": "Benelux", "ll": (5.0, 52.0)},
    {"id": "ukie", "name": "UK & Ireland", "ll": (-2.5, 53.5)},
    {"id": "south", "name": "Southern Europe", "ll": (3.0, 40.5)},
    {"id": "cee", "name": "CEE & Baltics", "ll": (21.0, 51.5)},
]
CITY_LL = {  # map anchor per city; suburbs fold into the metro
    "Stockholm": ("SE", 18.07, 59.33), "Norrmalm": ("SE", 18.07, 59.33),
    "Gothenburg": ("SE", 11.97, 57.71), "Malmo": ("SE", 13.00, 55.60), "Malmö": ("SE", 13.00, 55.60),
    "Copenhagen": ("DK", 12.57, 55.68), "Kongens Lyngby": ("DK", 12.57, 55.68),
    "Aarhus": ("DK", 10.20, 56.16),
    "Oslo": ("NO", 10.75, 59.91), "Trondheim": ("NO", 10.40, 63.43), "Bergen": ("NO", 5.32, 60.39),
    "Helsinki": ("FI", 24.94, 60.17), "Espoo": ("FI", 24.94, 60.17), "Oulu": ("FI", 25.47, 65.01),
    "Reykjavik": ("IS", -21.94, 64.15), "Reykjavík": ("IS", -21.94, 64.15),
}
CITY2CC = {"copenhagen": "DK", "aarhus": "DK", "odense": "DK", "aalborg": "DK",
           "kongens lyngby": "DK", "hellerup": "DK", "frederiksberg": "DK",
           "stockholm": "SE", "gothenburg": "SE", "malmo": "SE", "malm\u00f6": "SE", "uppsala": "SE", "lund": "SE",
           "oslo": "NO", "bergen": "NO", "trondheim": "NO",
           "helsinki": "FI", "espoo": "FI", "tampere": "FI", "oulu": "FI",
           "reykjavik": "IS", "reykjav\u00edk": "IS"}
SCORING = {
    "sr_w": {"Partner": 0.95, "Director": 0.75, "Associate": 0.40, None: 0.55},
    "stage_w": {"prelead": 1, "reachout": 1, "awaiting": 2, "lead": 3, "hard": 2, "portfolio": 0},
    "df_funnel_hot": {"Lead", "Qualified Lead", "Deal", "Hard to crack"},
    "o_thresh": 50, "c_thresh": 50,
}
W, H = 1000.0, 1120.0
_L0, _P1 = math.radians(10.0), math.radians(52.0)


def _laea(lon, lat):
    lam, phi = math.radians(lon), math.radians(lat)
    d = 1 + math.sin(_P1) * math.sin(phi) + math.cos(_P1) * math.cos(phi) * math.cos(lam - _L0)
    if d <= 1e-9:
        d = 1e-9
    k = math.sqrt(2.0 / d)
    return (k * math.cos(phi) * math.sin(lam - _L0),
            k * (math.cos(_P1) * math.sin(phi) - math.sin(_P1) * math.cos(phi) * math.cos(lam - _L0)))


class _Proj:
    def __init__(self, scale, cx, cy):
        self.s, self.cx, self.cy = scale, cx, cy

    def px(self, lon, lat):
        x, y = _laea(lon, lat)
        return (round(self.cx + self.s * x, 1), round(self.cy - self.s * y, 1))


def _decode_topo(topo, names):
    """Minimal TopoJSON arc decoder -> {name: [rings as [(lon,lat)...]]}"""
    tr = topo.get("transform") or {}
    sx, sy = (tr.get("scale") or [1, 1])
    tx, ty = (tr.get("translate") or [0, 0])
    arcs = []
    for arc in topo["arcs"]:
        pts, x, y = [], 0, 0
        for dx, dy in arc:
            x += dx; y += dy
            pts.append((x * sx + tx, y * sy + ty))
        arcs.append(pts)

    def ring(arc_ids):
        out = []
        for i in arc_ids:
            pts = arcs[i] if i >= 0 else list(reversed(arcs[~i]))
            out.extend(pts if not out else pts[1:])
        return out

    res = {}
    for g in topo["objects"]["countries"]["geometries"]:
        nm = (g.get("properties") or {}).get("name")
        if nm not in names:
            continue
        polys = g["arcs"] if g["type"] == "MultiPolygon" else [g["arcs"]]
        rings = []
        for poly in polys:
            for rg in poly:
                rings.append(ring(rg))
        res[nm] = rings
    return res


def _keep_ring(r, loose=False):
    """Drop overseas territories and Svalbard so Europe fills the frame."""
    lon = sum(p[0] for p in r) / len(r)
    lat = sum(p[1] for p in r) / len(r)
    if loose:
        return -75 <= lon <= 55 and 18 <= lat <= 85
    return -26 <= lon <= 45 and 34 <= lat <= 71.5


def _path(rings, proj, loose=False):
    out = []
    for r in rings:
        if len(r) < 4 or not _keep_ring(r, loose):
            continue
        pts = [proj.px(lon, lat) for lon, lat in r]
        # light simplification: skip points closer than 0.7px to the last kept one
        kept = [pts[0]]
        for p in pts[1:]:
            if abs(p[0] - kept[-1][0]) + abs(p[1] - kept[-1][1]) >= 0.7:
                kept.append(p)
        if len(kept) < 3:
            continue
        out.append("M" + "L".join(f"{x:g} {y:g}" for x, y in kept) + "Z")
    return "".join(out)


def _bounds_of(rings_list, proj):
    xs, ys = [], []
    for rings in rings_list:
        for r in rings:
            if not _keep_ring(r):
                continue
            for lon, lat in r:
                x, y = proj.px(lon, lat)
                xs.append(x); ys.append(y)
    return min(xs), min(ys), max(xs), max(ys)


def _rec(last):
    if not last:
        return 0.0
    try:
        import datetime
        days = (datetime.date.today() - datetime.date.fromisoformat(str(last)[:10])).days
        return math.exp(-max(days, 0) / 180.0)
    except Exception:
        return 0.0


def _noisy_or(items):  # items: [(R 0-100, s 0-1)]
    prod = 1.0
    for r, s in items:
        prod *= (1 - min(r, 100) / 100.0 * s)
    return round(100 * (1 - prod), 1)


def _pctile(vals):
    """value -> percentile rank 0-100 within vals"""
    sv = sorted(vals)
    n = len(sv)

    def pr(v):
        if n <= 1:
            return 50.0
        below = sum(1 for x in sv if x < v)
        return round(100.0 * below / (n - 1), 1)
    return pr


def build_covmap(regions, mynet, roster, load_json):
    pm = load_json(f"{ROOT}/data/enrich/person-meta.json", {}) or {}
    topo_path = TOPO if os.path.exists(TOPO) else TOPO_FALLBACK
    topo = json.load(open(topo_path))
    names = set(CC_NAME.values()) | set(EURO_BG)
    shapes = _decode_topo(topo, names)
    extra_shapes = _decode_topo(topo, set(EXTRA_BG))

    # fit projection to the shapes we keep, centred in the frame
    p0 = _Proj(1.0, 0.0, 0.0)
    x0, y0, x1, y1 = _bounds_of(shapes.values(), p0)
    s = min((W - 30) / (x1 - x0), (H - 30) / (y1 - y0))
    proj = _Proj(s, 0.0, 0.0)
    bx0, by0, bx1, by1 = _bounds_of(shapes.values(), proj)
    proj = _Proj(s, (W - (bx1 - bx0)) / 2 - bx0, (H - (by1 - by0)) / 2 - by0)

    countries = []
    cbounds = {}
    for nm, rings in shapes.items():
        cc = COUNTRY_CC.get(nm)
        d = _path(rings, proj)
        if not d:
            continue
        ent = {"d": d}
        if cc:
            ent["id"] = cc
            ent["name"] = nm
            xs0, ys0, xs1, ys1 = _bounds_of([rings], proj)
            cbounds[cc] = (xs0, ys0, xs1, ys1)
        else:
            ent["bg"] = 1
        countries.append(ent)
    for nm, rings in extra_shapes.items():   # world context beyond the frame; visible when zooming out/panning
        d = _path(rings, proj, loose=True)
        if d:
            countries.append({"d": d, "bg": 1})

    # viewboxes per level, padded
    def vb(x0, y0, x1, y1, pad):
        w, h = x1 - x0, y1 - y0
        return [round(x0 - w * pad, 1), round(y0 - h * pad, 1),
                round(w * (1 + 2 * pad), 1), round(h * (1 + 2 * pad), 1)]
    nx0 = min(cbounds[c][0] for c in NORDIC_CC if c in cbounds)
    ny0 = min(cbounds[c][1] for c in NORDIC_CC if c in cbounds)
    nx1 = max(cbounds[c][2] for c in NORDIC_CC if c in cbounds)
    ny1 = max(cbounds[c][3] for c in NORDIC_CC if c in cbounds)
    vbs = {"l0": [0, 0, W, H], "nordics": vb(nx0, ny0, nx1, ny1, 0.06)}
    for cc in NORDIC_CC:
        if cc in cbounds:
            vbs[cc] = vb(*cbounds[cc], 0.12)

    region_pts = [{"id": r["id"], "name": r["name"], "active": bool(r.get("active")),
                   "x": proj.px(*r["ll"])[0], "y": proj.px(*r["ll"])[1]} for r in REGIONS]
    city_px = {c: proj.px(lon, lat) for c, (cc, lon, lat) in CITY_LL.items()}

    # ---- entities: nordic funds + angels ----
    _mnidx = {}   # user -> contact name lower -> mynet edge (person-level Affinity/calendar score)
    for _u0, _lst0 in (mynet or {}).items():
        _mnidx[_u0] = {x["n"].lower(): x for x in _lst0}
    nreg = regions.get("nordics") or {"entities": []}
    ents, df_raws, pu_raws = [], [], {u: [] for u in roster}
    import datetime
    cutoff = (datetime.date.today() - datetime.timedelta(days=365)).isoformat()
    for e in nreg["entities"]:
        city_raw = (e.get("city") or "").split("·")[0].strip()
        anchor = CITY_LL.get(city_raw)
        cc = anchor[0] if anchor else None
        tray = cc is None
        # people + R per user
        people, rmax = {}, {}
        for tp in (e.get("top_people") or []):
            u = tp.get("name")
            if u not in roster:
                continue
            for c in (tp.get("contacts") or []):
                nm = c.get("person")
                if not nm or (pm.get(nm.lower()) or {}).get("inv") is False:
                    continue   # assistants/ops never count toward coverage
                R = round(0.75 * (c.get("pct") or 0) + 25 * _rec(c.get("last")), 1)
                p = people.setdefault(nm, {"n": nm, "r": {}, "last": None})
                p["r"][u] = max(p["r"].get(u, 0), R)
                if c.get("last") and (not p["last"] or c["last"] > p["last"]):
                    p["last"] = c["last"]
                rmax[nm] = max(rmax.get(nm, 0), R)
        # person-level scores beat entity-level ones, and mynet adds contacts top_people missed
        _enl = e["name"].lower()
        for _u1, _byn in _mnidx.items():
            for _k1, _mx in _byn.items():
                if (_mx.get("f") or "").lower() != _enl and _k1 != _enl:
                    continue
                nm1 = _mx["n"]
                R2 = round(0.75 * (_mx.get("p") or 0) + 25 * _rec(_mx.get("l")), 1)
                p1 = people.setdefault(nm1, {"n": nm1, "r": {}, "last": None})
                if R2 > p1["r"].get(_u1, 0):
                    p1["r"][_u1] = R2
                if _mx.get("l") and (not p1["last"] or _mx["l"] > p1["last"]):
                    p1["last"] = _mx["l"]
        for p in people.values():
            meta = pm.get(p["n"].lower()) or {}
            p["sr"] = "Partner" if e["kind"] == "angel" else _sr_from_title(meta.get("title"))
            if meta.get("title"):
                p["t"] = meta["title"]
        # seniority weights
        def sw(p):
            return 1.0 if e["kind"] == "angel" else SCORING["sr_w"].get(p.get("sr"), SCORING["sr_w"][None])
        CT = _noisy_or([(max(p["r"].values(), default=0), sw(p)) for p in people.values()])
        cu = {}
        for u in roster:
            items = [(p["r"].get(u, 0), sw(p)) for p in people.values() if p["r"].get(u)]
            if items:
                cu[u] = _noisy_or(items)
        # deal flow 12m
        df12, dfw = 0, 0.0
        for d in (e.get("dealflow") or []):
            if (d.get("date") or "") < cutoff:
                continue
            df12 += 1
            fn = d.get("funnel")
            dfw += 2 if fn in SCORING["df_funnel_hot"] else (1 if fn else 0.25)
        dfw += 2 * len(e.get("coinvest") or [])
        df_raws.append(dfw)
        # my pipeline weight per user
        pu = {}
        for bk, wgt in SCORING["stage_w"].items():
            for co in (e.get("buckets") or {}).get(bk) or []:
                for u in (co.get("own") or []):
                    if u in roster and wgt:
                        pu[u] = pu.get(u, 0) + wgt
        for u, v in pu.items():
            pu_raws[u].append(v)
        _dfl = [{"n": _d7.get("name"), "r": (_d7.get("round") or "").replace("_", " ").title(),
                 "d": _d7.get("date"), "fu": _d7.get("funnel")} for _d7 in (e.get("dealflow") or [])[:6]]
        _pipe = {bk: [{"n": co.get("name"), "o": [u for u in (co.get("own") or []) if u in roster]}
                      for co in v[:8]]
                 for bk, v in (e.get("buckets") or {}).items() if v}
        ents.append({
            "dfl": _dfl, "pipe": _pipe,
            "slug": e["slug"], "name": e["name"], "kind": e["kind"],
            "cat": e.get("category"), "tier": e.get("tier"),
            "city": city_raw or None, "cc": cc, "tray": tray or None,
            "rel": (e.get("relevance") or {}).get("total") or 0,
            "df12": df12, "dfw": round(dfw, 2), "coinv": len(e.get("coinvest") or []),
            "CT": CT, "cu": cu, "pu": pu,
            "people": sorted(people.values(), key=lambda p: -max(p["r"].values(), default=0))[:10],
        })

    # ---- O, O_u, G, M, states ----
    dfp = _pctile(df_raws)
    pup = {u: _pctile(v or [0]) for u, v in pu_raws.items()}
    for i, e in enumerate(ents):
        e["O"] = round(0.5 * e["rel"] + 0.5 * dfp(e["dfw"]), 1)
        U = {}
        for u in roster:
            Cu = e["cu"].get(u, 0)
            Pu = e["pu"].get(u, 0)
            Ou = round(0.5 * e["O"] + 0.5 * (pup[u](Pu) if Pu else 0), 1)
            Gu = round(Ou * (1 - Cu / 100.0), 1)
            G = round(e["O"] * (1 - Cu / 100.0), 1)
            M = round(Gu * (1 + 0.5 * e["CT"] / 100.0), 1)
            hiO = e["O"] >= SCORING["o_thresh"] or Ou >= SCORING["o_thresh"]
            st = ("build" if hiO and Cu < SCORING["c_thresh"] else
                  "maintain" if hiO else
                  "over" if Cu >= SCORING["c_thresh"] else "ignore")
            tag = ("warm" if st == "build" and e["CT"] >= 60 else
                   "cold" if st == "build" and e["CT"] < 30 else None)
            rec = {"cu": Cu, "ou": Ou, "gu": Gu, "g": G, "m": M, "st": st}
            if Pu:
                rec["pu"] = Pu
            if tag:
                rec["tag"] = tag
            if Cu or Pu or st == "build":
                U[u] = rec
        e["u"] = U

    # ---- bubble layout per level (map units; r chosen for that level's zoom) ----
    def rad(O, lvl_zoom, lo=7, hi=26):
        return round((lo + (hi - lo) * math.sqrt(max(O, 1) / 100.0)) / lvl_zoom, 2)
    zoom_l2 = {cc: W / vbs[cc][2] for cc in NORDIC_CC if cc in vbs}
    bycity = {}
    for e in ents:
        if e["tray"]:
            continue
        bycity.setdefault(e["city"], []).append(e)
    for city, group in bycity.items():
        ax, ay = city_px[city]
        cc = CITY_LL[city][0]
        z = zoom_l2.get(cc, 5)
        group.sort(key=lambda e: -e["O"])
        placed = []
        for e in group:
            r = rad(e["O"], z)
            # sunflower placement around the anchor until no collision
            k, x, y = 0, ax, ay
            while any((x - q[0]) ** 2 + (y - q[1]) ** 2 < (r + q[2] + 1.5 / z) ** 2 for q in placed):
                k += 1
                th = k * 2.39996
                rr = (2.2 / z) * math.sqrt(k) * (r * z / 9 + 2)
                x, y = ax + rr * math.cos(th), ay + rr * math.sin(th)
            placed.append((x, y, r))
            e["x"], e["y"], e["r2"] = round(x, 1), round(y, 1), r
    # country bubble geometry at L1
    zoom_l1 = W / vbs["nordics"][2]
    ccent = {cc: ((cbounds[cc][0] + cbounds[cc][2]) / 2, (cbounds[cc][1] + cbounds[cc][3]) / 2)
             for cc in NORDIC_CC if cc in cbounds}
    ccent["DK"] = (ccent["DK"][0] - 6, ccent["DK"][1])  # nudge off Sweden's coast

    # ---- area roll-ups per user + team ----
    def rollup(sel):
        o_sum = sum(x["O"] for x in sel) or 1e-9
        covT = round(sum(x["O"] * x["CT"] for x in sel) / o_sum, 1)
        out = {"covT": covT, "opp": round(o_sum, 1), "n": len(sel)}
        pu_users = {}
        for u in roster:
            covu = round(sum(x["O"] * x["cu"].get(u, 0) for x in sel) / o_sum, 1)
            gap = round(sum(x["u"][u]["gu"] for x in sel if u in x["u"]), 1)
            if covu or gap:
                pu_users[u] = {"covu": covu, "gap": gap}
        out["u"] = pu_users
        return out
    areas = {"nordics": rollup([e for e in ents if not e["tray"]])}
    for cc in NORDIC_CC:
        sel = [e for e in ents if e["cc"] == cc]
        if sel:
            areas[cc] = rollup(sel)
    # pipeline exposure per user per country (share of stage-weighted nordic pipeline)
    for u in roster:
        tot = sum(e["pu"].get(u, 0) for e in ents) or 0
        if not tot:
            continue
        for cc in NORDIC_CC:
            if cc in areas:
                share = round(100 * sum(e["pu"].get(u, 0) for e in ents if e["cc"] == cc) / tot, 1)
                if share and u in areas[cc]["u"]:
                    areas[cc]["u"][u]["exp"] = share

    # ---- Affinity completeness layer: every investor-kind company in the Nordics (Compass sweep) ----
    import re as _re
    _nrm = lambda x: _re.sub(r"[^a-z0-9]", "", (x or "").lower())
    CNTRY_CC = {"Sweden": "SE", "Denmark": "DK", "Norway": "NO", "Finland": "FI", "Iceland": "IS"}
    _curn, _curd = set(), set()
    for _rk4, _reg4 in regions.items():
        for _e6 in _reg4["entities"]:
            _curn.add(_nrm(_e6["name"]))
            _w6 = (_e6.get("website") or "").lower().replace("https://", "").replace("http://", "").replace("www.", "").split("/")[0]
            if _w6:
                _curd.add(_w6)
    _mnd, _mnn = {}, {}
    for _u5, _lst5 in (mynet or {}).items():
        for _mx5 in _lst5:
            R5 = round(0.75 * (_mx5.get("p") or 0) + 25 * _rec(_mx5.get("l")), 1)
            if _mx5.get("d"):
                _mnd.setdefault(_mx5["d"].lower(), []).append((_u5, _mx5["n"], R5, _mx5.get("l")))
            if _mx5.get("f"):
                _mnn.setdefault(_nrm(_mx5["f"]), []).append((_u5, _mx5["n"], R5, _mx5.get("l")))
    aff_ents = []
    for _row in (load_json(f"{ROOT}/data/enrich/nordic-investors-affinity.json", []) or []):
        if _nrm(_row["name"]) in _curn or (_row.get("domain") or "") in _curd:
            continue
        _cc5 = CNTRY_CC.get(_row.get("country"))
        if not _cc5:
            continue
        _hits = (_mnd.get((_row.get("domain") or "").lower(), []) + _mnn.get(_nrm(_row["name"]), []))
        _pp5, _cu5 = {}, {}
        for _u6, _nm6, _r6, _l6 in _hits:
            _p6 = _pp5.setdefault(_nm6, {"n": _nm6, "r": {}, "last": None})
            _p6["r"][_u6] = max(_p6["r"].get(_u6, 0), _r6)
            if _l6 and (not _p6["last"] or _l6 > _p6["last"]):
                _p6["last"] = _l6
        for _u6 in roster:
            _it6 = [(_p6["r"].get(_u6, 0), 0.75) for _p6 in _pp5.values() if _p6["r"].get(_u6)]
            if _it6:
                _cu5[_u6] = _noisy_or(_it6)
        _ct5 = _noisy_or([(max(_p6["r"].values(), default=0), 0.75) for _p6 in _pp5.values()])
        aff_ents.append({"slug": "aff-" + _nrm(_row["name"])[:30], "name": _row["name"], "kind": "aff",
                         "city": _row.get("city"), "cc": _cc5, "lc": _row.get("last_call"),
                         "CT": _ct5, "cu": _cu5,
                         "people": sorted(_pp5.values(), key=lambda p: -max(p["r"].values(), default=0))[:6]})

    _entnames = {e["name"].lower() for e in ents}
    _entppl = {p["n"].lower() for e in ents for p in e["people"]}
    people_in = {}
    for _u2, _lst2 in (mynet or {}).items():
        for _mx in _lst2:
            _cc2 = CITY2CC.get((_mx.get("c") or "").lower())
            if not _cc2 or (_mx.get("p") or 0) < 30:
                continue
            if (_mx.get("f") or "").lower() in _entnames or _mx["n"].lower() in _entppl:
                continue   # already counted on the map
            people_in.setdefault(_cc2, {}).setdefault(_u2, []).append(
                {"n": _mx["n"], "f": _mx.get("f"), "p": _mx["p"], "c": _mx.get("c")})
    for _cc3 in people_in:
        for _u3 in people_in[_cc3]:
            people_in[_cc3][_u3] = sorted(people_in[_cc3][_u3], key=lambda x: -x["p"])[:30]

    return {
        "vb": vbs, "peopleIn": people_in, "aff": aff_ents, "countries": countries, "regions": region_pts,
        "ccent": {k: [round(v[0], 1), round(v[1], 1)] for k, v in ccent.items()},
        "cities": {c: [city_px[c][0], city_px[c][1]] for c in city_px},
        "zoomL1": round(zoom_l1, 2), "zoomL2": {k: round(v, 2) for k, v in zoom_l2.items()},
        "ents": ents, "areas": areas, "ccName": CC_NAME, "nordics": NORDIC_CC,
    }


def _sr_from_title(title):
    t = (title or "").lower()
    if not t:
        return None
    if any(k in t for k in ("partner", "managing director", "head of", "chief", "founder", "cio", "ceo")):
        return "Partner"
    if any(k in t for k in ("principal", "director", "vice president", " vp", "vp ", "investment manager", "lead")):
        return "Director"
    if any(k in t for k in ("associate", "analyst")):
        return "Associate"
    return None
