"""Coverage Map (spec: docs/coverage-map/discovery.md).

Everything heavy happens here at build time: Natural Earth geometry is decoded,
projected (Lambert azimuthal equal-area, centre 10E 52N) and emitted as SVG path
strings; all five scores from spec section 6 are computed per user; bubbles are
packed per city. The client only draws. M1 scope: Nordics active, rest greyed.
"""
import json, math, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOPO = f"{ROOT}/data/geo/countries-50m.json"
TOPO_FALLBACK = TOPO

# ---- config (spec: config/regions.ts + config/scoring.ts) ----
NORDIC_CC = ["SE", "DK", "NO", "FI"]
CC_NAME = {"SE": "Sweden", "DK": "Denmark", "NO": "Norway", "FI": "Finland"}
COUNTRY_CC = {v: k for k, v in CC_NAME.items()}
EURO_BG = ["Germany", "Austria", "Switzerland", "France", "Netherlands", "Belgium",
           "Luxembourg", "United Kingdom", "Ireland", "Spain", "Portugal", "Italy",
           "Greece", "Poland", "Czechia", "Estonia", "Latvia", "Lithuania", "Romania",
           "Hungary", "Slovakia", "Slovenia", "Croatia", "Bulgaria", "Serbia",
           "Bosnia and Herz.", "Albania", "North Macedonia", "Ukraine", "Belarus",
           "Moldova", "Montenegro", "Kosovo"]
EXTRA_BG = ["Greenland", "Turkey", "Morocco", "Algeria", "Tunisia", "Libya", "Egypt",
            "Israel", "Lebanon", "Jordan", "Syria", "Cyprus", "Georgia", "Armenia", "Azerbaijan", "Iraq"]
G_SUB = {"Berlin": "BER", "Potsdam": "BER", "Leipzig": "BER", "Erfurt": "BER", "Dresden": "BER",
         "Munich": "MUC", "Landshut": "MUC", "Pullach": "MUC", "Nuremberg": "MUC", "Wessling": "MUC",
         "Stuttgart": "MUC", "Heilbronn": "MUC", "Gerlingen": "MUC",
         "Frankfurt": "FRA", "Eschborn": "FRA", "Wiesbaden": "FRA", "Darmstadt": "FRA", "Mainz": "FRA",
         "Heidelberg": "FRA", "Karlsruhe": "FRA", "Ludwigshafen": "FRA", "Freiburg im Breisgau": "FRA",
         "Cologne": "CGN", "Bonn": "CGN", "Dusseldorf": "CGN", "D\u00fcsseldorf": "CGN", "Essen": "CGN",
         "Munster": "CGN", "M\u00fcnster": "CGN", "Greven": "CGN", "Gutersloh": "CGN", "Mulheim": "CGN",
         "Bielefeld": "CGN", "Dortmund": "CGN", "Aachen": "CGN",
         "Hamburg": "HAM", "Bremen": "HAM", "Hannover": "HAM"}
G_ANCHOR = {"BER": (13.40, 52.52), "MUC": (11.58, 48.25), "FRA": (8.95, 49.95),
            "CGN": (6.55, 51.15), "HAM": (9.99, 53.55)}
UK_ANCHOR = {"LON": (-0.13, 51.51), "CAM": (0.12, 52.21), "OXF": (-1.26, 51.75),
             "EDI": (-3.19, 55.95), "MAN": (-2.24, 53.48)}
US_METRO = {"SF": (-122.42, 37.77), "NYC": (-74.00, 40.71), "BOS": (-71.06, 42.36)}
G_CITY_LL = {"Berlin": (13.40, 52.52), "Potsdam": (13.06, 52.39), "Leipzig": (12.37, 51.34),
             "Munich": (11.58, 48.14), "Landshut": (12.15, 48.54), "Pullach": (11.52, 48.06),
             "Nuremberg": (11.08, 49.45), "Stuttgart": (9.18, 48.78),
             "Frankfurt": (8.68, 50.11), "Wiesbaden": (8.24, 50.08), "Heidelberg": (8.69, 49.40),
             "Karlsruhe": (8.40, 49.01), "Cologne": (6.96, 50.94), "Bonn": (7.10, 50.73),
             "Dusseldorf": (6.78, 51.23), "Essen": (7.01, 51.46), "Hamburg": (9.99, 53.55)}
REGION_SUBS = {"nordics": ["SE", "DK", "NO", "FI"], "germany": ["BER", "MUC", "CGN", "FRA", "HAM"],
               "france": ["FR"], "uk": ["LON", "CAM", "OXF", "EDI", "MAN"], "us": ["SF", "NYC", "BOS"]}
SUB_NAME = {"SE": "Sweden", "DK": "Denmark", "NO": "Norway", "FI": "Finland", "FR": "France",
            "BER": "Berlin", "MUC": "Munich", "FRA": "Frankfurt", "CGN": "Cologne/Bonn", "HAM": "Hamburg",
            "LON": "London", "CAM": "Cambridge", "OXF": "Oxford", "EDI": "Edinburgh", "MAN": "Manchester",
            "US": "US tier-1", "SF": "SF Bay Area", "NYC": "New York", "BOS": "Boston"}
REGIONS = [  # L0 bubbles; only nordics is live in M1
    {"id": "nordics", "name": "Nordics", "ll": (16.0, 62.5), "active": True},
    {"id": "germany", "name": "Germany", "ll": (10.3, 51.2), "active": True},
    {"id": "france", "name": "France", "ll": (2.5, 46.8), "active": True, "solo": "FR"},
    {"id": "uk", "name": "UK", "ll": (-1.5, 52.8), "active": True},
    {"id": "us", "name": "US tier-1", "ll": (-91.0, 40.0), "active": True},
    {"id": "benelux", "name": "Benelux", "ll": (5.0, 52.0)},
    {"id": "iberia", "name": "Iberia", "ll": (-4.5, 40.3)},
    {"id": "israel", "name": "Israel", "ll": (34.8, 32.0)},
    {"id": "baltics", "name": "Baltics", "ll": (24.7, 57.3)},
]
CITY_LL = {  # map anchor per city; suburbs fold into the metro
    "Stockholm": ("SE", 18.07, 59.33), "Norrmalm": ("SE", 18.07, 59.33),
    "Gothenburg": ("SE", 11.97, 57.71), "Malmo": ("SE", 13.00, 55.60), "Malmö": ("SE", 13.00, 55.60),
    "Copenhagen": ("DK", 12.57, 55.68), "Kongens Lyngby": ("DK", 12.57, 55.68),
    "Aarhus": ("DK", 10.20, 56.16),
    "Oslo": ("NO", 10.75, 59.91), "Trondheim": ("NO", 10.40, 63.43), "Bergen": ("NO", 5.32, 60.39),
    "Helsinki": ("FI", 24.94, 60.17), "Espoo": ("FI", 24.94, 60.17), "Oulu": ("FI", 25.47, 65.01),
    "Reykjavik": ("IS", -21.94, 64.15), "Reykjavík": ("IS", -21.94, 64.15),
    "Lund": ("SE", 13.19, 55.70), "Uppsala": ("SE", 17.64, 59.86), "Are": ("SE", 13.08, 63.40),
    "Vaxjo": ("SE", 14.81, 56.88), "Sodertalje": ("SE", 18.07, 59.33), "Solna": ("SE", 18.07, 59.33),
    "Kista": ("SE", 18.07, 59.33), "Limhamn": ("SE", 13.00, 55.60), "Eskilstuna": ("SE", 16.51, 59.37),
    "Hellerup": ("DK", 12.57, 55.68), "Frederiksberg": ("DK", 12.57, 55.68),
    "Humlebaek": ("DK", 12.57, 55.68), "Vedbaek": ("DK", 12.57, 55.68),
    "Odense": ("DK", 10.39, 55.40), "Aalborg": ("DK", 9.92, 57.05),
    "Fornebu": ("NO", 10.75, 59.91), "Stavanger": ("NO", 5.73, 58.97),
    "Tampere": ("FI", 23.76, 61.50),
    "London": ("LON", -0.13, 51.51), "Cambridge": ("CAM", 0.12, 52.21),
    "Oxford": ("OXF", -1.26, 51.75), "Edinburgh": ("EDI", -3.19, 55.95),
    "Manchester": ("MAN", -2.24, 53.48), "Glasgow": ("EDI", -4.25, 55.86),
    "San Francisco": ("SF", -122.42, 37.77), "Menlo Park": ("SF", -122.18, 37.45),
    "Palo Alto": ("SF", -122.14, 37.44), "Mountain View": ("SF", -122.08, 37.39),
    "Woodside": ("SF", -122.25, 37.43), "New York": ("NYC", -74.00, 40.71),
    "Boston": ("BOS", -71.06, 42.36), "Austin": ("SF", -97.74, 30.27),
}
CITY2CC = {"paris": "FR", "lyon": "FR", "berlin": "BER", "potsdam": "BER", "munich": "MUC", "m\u00fcnchen": "MUC",
           "frankfurt": "FRA", "hamburg": "HAM", "cologne": "CGN", "k\u00f6ln": "CGN",
           "bonn": "CGN", "dusseldorf": "CGN", "d\u00fcsseldorf": "CGN",
           "copenhagen": "DK", "aarhus": "DK", "odense": "DK", "aalborg": "DK",
           "kongens lyngby": "DK", "hellerup": "DK", "frederiksberg": "DK",
           "stockholm": "SE", "gothenburg": "SE", "malmo": "SE", "malm\u00f6": "SE", "uppsala": "SE", "lund": "SE",
           "oslo": "NO", "bergen": "NO", "trondheim": "NO",
           "helsinki": "FI", "espoo": "FI", "tampere": "FI", "oulu": "FI",
           "reykjavik": "IS", "reykjav\u00edk": "IS",
           "london": "LON", "cambridge": "CAM", "oxford": "OXF",
           "edinburgh": "EDI", "glasgow": "EDI", "manchester": "MAN",
           "san francisco": "SF", "menlo park": "SF", "palo alto": "SF",
           "mountain view": "SF", "new york": "NYC", "boston": "BOS",
           "marseille": "FR", "toulouse": "FR", "bordeaux": "FR", "nantes": "FR", "lille": "FR",
           "stuttgart": "FRA", "leipzig": "BER", "nuremberg": "MUC", "dresden": "BER",
           "brooklyn": "NYC", "oakland": "SF", "san mateo": "SF", "redwood city": "SF",
           "cambridge, ma": "BOS", "somerville": "BOS"}
SCORING = {
    "sr_w": {"Partner": 0.95, "Director": 0.75, "Associate": 0.40, None: 0.55},
    "stage_w": {"prelead": 1, "reachout": 1, "awaiting": 2, "lead": 3, "hard": 2, "portfolio": 0},
    "df_funnel_hot": {"Lead", "Qualified Lead", "Deal", "Hard to crack"},
    "o_thresh": 50, "c_thresh": 50,
}
W = 1440.0   # world width in map units; Web Mercator, the map everyone knows


class _Proj:
    """Web Mercator at fixed world scale: the flat world map, zoomable to street level."""
    def px(self, lon, lat, nd=1):
        lat = max(min(lat, 84.0), -84.0)
        x = (lon + 180.0) / 360.0 * W
        y = (1 - math.log(math.tan(math.pi / 4 + math.radians(lat) / 2)) / math.pi) / 2 * W
        return (round(x, nd), round(y, nd))


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
        if (names is not None and nm not in names) or nm == "Antarctica":
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


def _unwrap(r):
    """Rings crossing the antimeridian smear across the map; shift them to one side."""
    lons = [p[0] for p in r]
    if max(lons) - min(lons) <= 180:
        return r
    east = sum(1 for l in lons if l > 90)
    west = sum(1 for l in lons if l < -90)
    if east >= west:
        return [(lon + 360 if lon < 0 else lon, lat) for lon, lat in r]
    return [(lon - 360 if lon > 0 else lon, lat) for lon, lat in r]


def _path(rings, proj, tol=0.9, nd=1):
    out = []
    for r in rings:
        if len(r) < 4:
            continue
        r = _unwrap(r)
        pts = [proj.px(lon, lat, nd) for lon, lat in r]
        xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
        if max(xs) - min(xs) < tol * 2 and max(ys) - min(ys) < tol * 2:
            continue   # ring smaller than the pen
        kept = [pts[0]]
        for p in pts[1:]:
            if abs(p[0] - kept[-1][0]) + abs(p[1] - kept[-1][1]) >= tol:
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
    _EMPF = load_json(f"{ROOT}/data/enrich/employment-flags.json", {}) or {}
    _COVR = load_json(f"{ROOT}/data/enrich/contact-overrides.json", {}) or {}
    # stage focus per curated fund (uk-funds for the UK; fund-meta for firms it knows)
    _FS_BY_SLUG = {}
    _ukf = load_json(f"{ROOT}/data/enrich/uk-funds.json", {}) or {}
    _uksm = load_json(f"{ROOT}/data/uk/slug-map.json", {}) or {}
    for _d12, _m12 in _ukf.items():
        if _uksm.get(_d12) and _m12.get("stage"):
            _FS_BY_SLUG[_uksm[_d12]] = _m12["stage"]
    topo_path = TOPO if os.path.exists(TOPO) else TOPO_FALLBACK
    topo = json.load(open(topo_path))
    shapes = _decode_topo(topo, None)   # the whole world
    proj = _Proj()
    fine = set(CC_NAME.values()) | set(EURO_BG)

    countries, cbounds = [], {}
    for nm, rings in shapes.items():
        cc = COUNTRY_CC.get(nm) or {"Germany": "DE", "France": "FR", "United Kingdom": "GB",
                                    "United States of America": "US"}.get(nm)
        d = _path(rings, proj, tol=0.12 if nm in fine else 0.9, nd=2 if nm in fine else 1)
        if not d:
            continue
        ent = {"d": d}
        if cc:
            ent["id"] = cc
            ent["name"] = nm
            # vb bounds from the European mainland only (no Svalbard stretch)
            core = [r for r in rings if _keep_ring(r)]
            xs, ys = [], []
            for r in core:
                for lon, lat in r:
                    x, y = proj.px(lon, lat)
                    xs.append(x); ys.append(y)
            if xs:
                cbounds[cc] = (min(xs), min(ys), max(xs), max(ys))
        else:
            ent["bg"] = 1
        countries.append(ent)

    # viewboxes per level, padded
    def vb(x0, y0, x1, y1, pad):
        w, h = x1 - x0, y1 - y0
        return [round(x0 - w * pad, 1), round(y0 - h * pad, 1),
                round(w * (1 + 2 * pad), 1), round(h * (1 + 2 * pad), 1)]
    wx0, wy0 = proj.px(-141, 74.5)   # L0 frame: North America + Europe
    wx1, wy1 = proj.px(55, 21.5)
    nx0 = min(cbounds[c][0] for c in NORDIC_CC if c in cbounds)
    ny0 = min(cbounds[c][1] for c in NORDIC_CC if c in cbounds)
    nx1 = max(cbounds[c][2] for c in NORDIC_CC if c in cbounds)
    ny1 = max(cbounds[c][3] for c in NORDIC_CC if c in cbounds)
    vbs = {"l0": vb(wx0, wy0, wx1, wy1, 0.0), "nordics": vb(nx0, ny0, nx1, ny1, 0.06)}
    for cc in NORDIC_CC:
        if cc in cbounds:
            vbs[cc] = vb(*cbounds[cc], 0.12)
    vbs["nordics"] = vb(nx0, ny0, nx1, ny1, 0.14)
    if "DE" in cbounds:
        vbs["germany"] = vb(*cbounds["DE"], 0.16)
    if "FR" in cbounds:
        vbs["france"] = vb(*cbounds["FR"], 0.14)
        vbs["FR"] = vbs["france"]
    if "GB" in cbounds:
        vbs["uk"] = vb(*cbounds["GB"], 0.14)
    _usx0, _usy0 = proj.px(-130, 52)   # continental US frame (coast to coast)
    _usx1, _usy1 = proj.px(-62, 23)
    vbs["us"] = vb(_usx0, _usy0, _usx1, _usy1, 0.04)
    for _gk, (_glon, _glat) in {**G_ANCHOR, **UK_ANCHOR, **US_METRO}.items():
        _gx0, _gy0 = proj.px(_glon - 0.95, _glat + 0.55)
        _gx1, _gy1 = proj.px(_glon + 0.95, _glat - 0.55)
        vbs[_gk] = vb(_gx0, _gy0, _gx1, _gy1, 0.0)

    region_pts = [{"id": r["id"], "name": r["name"], "active": bool(r.get("active")),
                   "solo": r.get("solo"),
                   "x": proj.px(*r["ll"])[0], "y": proj.px(*r["ll"])[1]} for r in REGIONS]
    city_px = {c: proj.px(lon, lat) for c, (cc, lon, lat) in CITY_LL.items()}

    # ---- entities: nordic funds + angels ----
    _mnidx = {}   # user -> contact name lower -> mynet edge (person-level Affinity/calendar score)
    for _u0, _lst0 in (mynet or {}).items():
        _mnidx[_u0] = {x["n"].lower(): x for x in _lst0}
    ents, df_raws, pu_raws = [], [], {u: [] for u in roster}
    import datetime
    cutoff = (datetime.date.today() - datetime.timedelta(days=365)).isoformat()
    FUND_CITY_OVERRIDE = {"northzone": "Stockholm"}   # London-HQ but a Nordic fund; belongs on this map
    _region_ents = [(rg, e) for rg in ("nordics", "germany", "france", "uk", "us")
                    for e in (regions.get(rg) or {"entities": []})["entities"]]
    _nrm0 = lambda x: re.sub(r"[^a-z0-9]", "", (x or "").lower())
    _euro_names = set()   # a US fund whose London/EU seat is already curated keeps that card only
    for _rgid, e in _region_ents:
        city_raw = FUND_CITY_OVERRIDE.get(e["slug"]) or (e.get("city") or "").split("·")[0].strip()
        ANGEL_CITY = {"verena pausder": "Berlin", "christian reber": "Berlin", "hakan ko\u00e7": "Berlin",
                      "philipp kl\u00f6ckner": "Berlin", "christian vollmann": "Berlin",
                      "julius g\u00f6llner": "Berlin", "matthias hilpert": "Berlin",
                      "hanno renner": "Munich", "mario g\u00f6tze": "Munich"}
        if not city_raw and e["kind"] == "angel":
            city_raw = (((pm.get(e["name"].lower()) or {}).get("city") or "") or
                        ANGEL_CITY.get(e["name"].lower(), "")).strip()
        if _rgid == "nordics":
            anchor = CITY_LL.get(city_raw)
            cc = anchor[0] if anchor else None
        elif _rgid == "germany":
            cc = G_SUB.get(city_raw)
        elif _rgid == "uk":
            cc = e.get("uk_sub")   # curated sub decides placement, not the Harmonic HQ
        elif _rgid == "us":
            if _nrm0(e["name"]) in _euro_names:
                continue   # its European seat is a curated entity elsewhere on the map
            cc = e.get("us_sub") or "SF"
        else:   # france: one node, Paris in all but name
            cc = "FR" if (e.get("city") or "").endswith("FR") or city_raw in ("Paris", "Lyon") or e["kind"] == "angel" and city_raw == "Paris" else ("FR" if city_raw in ("Saint-Jacques-de-la-Lande",) else None)
        if _rgid != "us":
            _euro_names.add(_nrm0(e["name"]))
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
                p = people.setdefault(nm.lower(), {"n": nm, "r": {}, "last": None})
                p["r"][u] = max(p["r"].get(u, 0), R)
                if c.get("linkedin") and not p.get("li"):
                    p["li"] = c["linkedin"]
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
                p1 = people.setdefault(nm1.lower(), {"n": nm1, "r": {}, "last": None})
                if R2 > p1["r"].get(_u1, 0):
                    p1["r"][_u1] = R2
                if _mx.get("l") and (not p1["last"] or _mx["l"] > p1["last"]):
                    p1["last"] = _mx["l"]
        # Harmonic team-network layer: LinkedIn/email/calendar connections that never
        # made it into Affinity still count as (weak) coverage — they are real paths in
        _NETJUNK = re.compile(r"assistant|office manager|recruiter|reception|counsel|legal"
                              r"|head of finance|chief financial|people|talent|marketing"
                              r"|platform|community|comms|press", re.I)
        _empf7 = ((_EMPF.get(_rgid) or {}).get(e["slug"]) or {})
        for _nr in (e.get("net") or []):
            _nm7 = _nr.get("n")
            if not _nm7 or (pm.get(_nm7.lower()) or {}).get("inv") is False:
                continue
            if (_empf7.get(_nm7) or {}).get("status") == "moved":
                continue   # left this fund (Harmonic-verified): not a door into it
            if _nr.get("t") and _NETJUNK.search(_nr["t"]):
                continue
            for _u7, _vi7 in (_nr.get("via") or {}).items():
                if _u7 not in roster:
                    continue
                _srcs7 = _vi7.get("s") if isinstance(_vi7, dict) else _vi7
                _last7 = _vi7.get("l") if isinstance(_vi7, dict) else None
                _li7 = "LINKEDIN" in set(_srcs7 or [])
                if _last7:   # dated edge: strength follows actual activity (22..50);
                    # a standing LinkedIn connection floors it at the LinkedIn-only 28
                    R7 = max(28.0 if _li7 else 20.0, min(50.0, round(22 + 28 * _rec(_last7), 1)))
                elif {"EMAIL", "CALENDAR"} & set(_srcs7 or []):
                    R7 = 38.0
                else:
                    R7 = 28.0
                _p7 = people.setdefault(_nm7.lower(), {"n": _nm7, "r": {}, "last": None})
                if R7 > _p7["r"].get(_u7, 0):
                    _p7["r"][_u7] = R7
                if _last7 and (not _p7["last"] or _last7 > _p7["last"]):
                    _p7["last"] = _last7
                if _nr.get("li") and not _p7.get("li"):
                    _p7["li"] = _nr["li"]
                if _nr.get("t") and not _p7.get("t"):
                    _p7["t"] = _nr["t"]
        # user-attested contact overrides (WhatsApp/Signal threads no connector sees):
        # the attested date feeds the same dated-edge formula, never a free-form score
        for _u8, _m8 in _COVR.items():
            if _u8 not in roster:
                continue
            for _nm8, _o8 in _m8.items():
                if _o8.get("firm") and _o8["firm"].lower() not in e["name"].lower():
                    continue   # same name at another firm is a different relationship (or person)
                _p8 = next((p for p in people.values() if p["n"].lower() == _nm8.lower()), None)
                if not _p8 or not _o8.get("last"):
                    continue
                R8 = round(22 + 28 * _rec(_o8["last"]), 1)
                if R8 > _p8["r"].get(_u8, 0):
                    _p8["r"][_u8] = R8
                if not _p8["last"] or _o8["last"] > _p8["last"]:
                    _p8["last"] = _o8["last"]
        for p in people.values():
            meta = pm.get(p["n"].lower()) or {}
            p["sr"] = ("Partner" if e["kind"] == "angel"
                       else _sr_from_title(meta.get("title") or p.get("t")))
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
                 "d": _d7.get("date"), "fu": _d7.get("funnel"), "do": _d7.get("domain"),
                 "aid": _d7.get("affinity_id")} for _d7 in (e.get("dealflow") or [])[:12]]
        _pipe = {bk: [{"n": co.get("name"), "aid": co.get("id"),
                       "o": [u for u in (co.get("own") or []) if u in roster]}
                      for co in v[:8]]
                 for bk, v in (e.get("buckets") or {}).items() if v}
        _dom = (e.get("website") or "").lower().replace("https://", "").replace("http://", "").replace("www.", "").split("/")[0]
        ents.append({
            "dfl": _dfl, "pipe": _pipe, "dom": _dom or None,
            "slug": e["slug"], "name": e["name"], "kind": e["kind"],
            "fs": _FS_BY_SLUG.get(e["slug"]),
            "cat": e.get("category"), "tier": e.get("tier"),
            "city": city_raw or None, "cc": cc, "rg": _rgid, "tray": tray or None,
            "rel": (e.get("relevance") or {}).get("total") or 0,
            "df12": df12, "dfw": round(dfw, 2), "coinv": len(e.get("coinvest") or []),
            "CT": CT, "cu": cu, "pu": pu,
            "people": sorted(people.values(), key=lambda p: -max(p["r"].values(), default=0))[:25],
        })

    # ---- O, O_u, G, M, states ----
    # deal-flow percentile WITHIN each region: the regions' deal counts come from
    # different measurement regimes (Affinity-observed vs Harmonic pulls), so a
    # global percentile would flatter whichever regime runs richer (scoring.md wart #1)
    _dfw_by_rg = {}
    for e in ents:
        _dfw_by_rg.setdefault(e.get("rg"), []).append(e["dfw"])
    dfp_rg = {rg: _pctile(v) for rg, v in _dfw_by_rg.items()}
    pup = {u: _pctile(v or [0]) for u, v in pu_raws.items()}
    for i, e in enumerate(ents):
        e["O"] = round(0.5 * e["rel"] + 0.5 * dfp_rg[e.get("rg")](e["dfw"]), 1)
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
    zoom_l2 = {k: W / vbs[k][2] for subs in REGION_SUBS.values() for k in subs if k in vbs}
    CITY_PT = dict(city_px)
    for _gc, (_glon2, _glat2) in G_CITY_LL.items():
        CITY_PT[_gc] = proj.px(_glon2, _glat2)
    CITY_PT["Paris"] = proj.px(2.35, 48.86)
    CITY_PT["Lyon"] = proj.px(4.84, 45.76)
    CITY_PT["Saint-Jacques-de-la-Lande"] = proj.px(-1.72, 48.07)
    bycity = {}
    for e in ents:
        if e["tray"] or e["city"] not in CITY_PT:
            continue
        bycity.setdefault(e["city"], []).append(e)
    for city, group in bycity.items():
        ax, ay = CITY_PT[city]
        cc = group[0]["cc"]
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
    # L1 bubble anchors: countries for the Nordics, cities for Germany
    zoom_l1 = W / vbs["nordics"][2]
    _ANCHOR = {"SE": (15.3, 61.6), "DK": (9.3, 55.9), "NO": (8.2, 60.9), "FI": (26.0, 63.3)}
    _ANCHOR.update(G_ANCHOR)
    _ANCHOR.update(UK_ANCHOR)
    _ANCHOR["FR"] = (2.35, 47.5)
    _ANCHOR.update(US_METRO)
    ccent = {k: proj.px(*_ANCHOR[k]) for k in _ANCHOR}
    subs_of = {rg: [{"id": k, "name": SUB_NAME[k], "x": ccent[k][0], "y": ccent[k][1]}
                    for k in subs] for rg, subs in REGION_SUBS.items()}
    reg_of = {k: rg for rg, subs in REGION_SUBS.items() for k in subs}
    zoom_reg = {rg: round(W / vbs[rg][2], 2) for rg in REGION_SUBS if rg in vbs}

    # ---- area roll-ups per user + team ----
    def rollup(sel):
        o_sum = sum(x["O"] for x in sel) or 1e-9
        covT = round(sum(x["O"] * x["CT"] for x in sel) / o_sum, 1)
        out = {"covT": covT, "opp": round(o_sum, 1), "n": len(sel),
               "pw": round(sum(sum((x.get("pu") or {}).values()) for x in sel), 1)}
        pu_users = {}
        for u in roster:
            covu = round(sum(x["O"] * x["cu"].get(u, 0) for x in sel) / o_sum, 1)
            gap = round(sum(x["u"][u]["gu"] for x in sel if u in x["u"]), 1)
            if covu or gap:
                pu_users[u] = {"covu": covu, "gap": gap}
        out["u"] = pu_users
        return out
    areas = {}
    for _rg, _subs in REGION_SUBS.items():
        areas[_rg] = rollup([e for e in ents if e.get("rg") == _rg and not e["tray"]])
        for cc in _subs:
            # every registered sub gets an area, even with no curated funds yet
            # (Hamburg holds only Affinity-layer investors) — the node must still render
            areas[cc] = rollup([e for e in ents if e["cc"] == cc])
        for u in roster:   # pipeline exposure: share of the user's stage-weighted regional pipeline
            tot = sum(e["pu"].get(u, 0) for e in ents if e.get("rg") == _rg) or 0
            totg = sum(e["pu"].get(u, 0) for e in ents if not e["tray"]) or 0
            if not tot:
                continue
            for cc in _subs:
                if cc in areas:
                    here = sum(e["pu"].get(u, 0) for e in ents if e["cc"] == cc)
                    share = round(100 * here / tot, 1)
                    if share and u in areas[cc]["u"]:
                        areas[cc]["u"][u]["exp"] = share
                        if totg:   # and the same slice of the user's GLOBAL open pipeline
                            areas[cc]["u"][u]["expg"] = round(100 * here / totg, 1)

    # ---- Affinity completeness layer: every investor-kind company in the Nordics (Compass sweep) ----
    import re as _re
    _nrm = lambda x: _re.sub(r"[^a-z0-9]", "", (x or "").lower())
    CNTRY_CC = {"Sweden": "SE", "Denmark": "DK", "Norway": "NO", "Finland": "FI"}
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
    aff_ents, _alias_rows = [], {}
    _nim = load_json(f"{ROOT}/data/enrich/nordic-investors-meta.json", {}) or {}
    _nim.update(load_json(f"{ROOT}/data/enrich/germany-investors-meta.json", {}) or {})
    _nim.update(load_json(f"{ROOT}/data/enrich/uk-investors-meta.json", {}) or {})
    _cards = load_json(f"{ROOT}/data/enrich/nordic-fund-cards.json", {}) or {}
    _cur = load_json(f"{ROOT}/data/enrich/curation.json", {}) or {}
    _pins = set(_cur.get("pins") or [])
    _removes = set(_cur.get("removes") or [])
    for _row in ((load_json(f"{ROOT}/data/enrich/nordic-investors-affinity.json", []) or []) +
                 (load_json(f"{ROOT}/data/enrich/germany-investors-affinity.json", []) or []) +
                 (load_json(f"{ROOT}/data/enrich/uk-investors-affinity.json", []) or [])):
        if _nrm(_row["name"]) in _curn or (_row.get("domain") or "") in _curd:
            continue
        _m9 = _nim.get(_row.get("domain") or "") or _nim.get(_nrm(_row["name"])) or {}
        if _m9.get("verdict") == "drop":
            continue   # operating parent, bank, science park, grant agency
        if _m9.get("verdict") == "alias":
            if _m9.get("alias_of"):
                _alias_rows.setdefault(_m9["alias_of"], []).append(_row)
            continue
        if _m9.get("name"):
            _row = dict(_row, name=_m9["name"])   # e.g. Statkraft -> Statkraft Ventures
        if _row.get("country") == "Germany":
            _cc5 = _row.get("sub") or G_SUB.get(_row.get("city") or "")
        else:   # UK sweep rows carry their sub directly; Nordics map by country
            _cc5 = _row.get("sub") or CNTRY_CC.get(_row.get("country"))
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
        _ae = {"slug": "aff-" + _nrm(_row["name"])[:30], "name": _row["name"], "kind": "aff",
               "city": _row.get("city"), "cc": _cc5, "lc": _row.get("last_call"),
               "CT": _ct5, "cu": _cu5,
               "people": sorted(_pp5.values(), key=lambda p: -max(p["r"].values(), default=0))[:6]}
        if _m9.get("type"):
            _ae["ft"] = _m9["type"]
        if _m9.get("stage"):
            _ae["fs"] = _m9["stage"]
        _card = _cards.get(_row.get("domain") or "") or _cards.get(_nrm(_row["name"])) or {}
        if _card.get("team"):
            _ae["team"] = _card["team"][:10]
        if _card.get("desc"):
            _ae["desc"] = _card["desc"]
        _anchor5 = CITY_LL.get(_row.get("city") or "")
        if _anchor5:
            _ae["x"], _ae["y"] = proj.px(_anchor5[1], _anchor5[2])
        _ae["dom"] = _row.get("domain")
        aff_ents.append(_ae)

    # ---- alias merge: fold duplicate records' relationships into the canonical card ----
    _bydom = {}
    for _e8 in ents + aff_ents:
        if _e8.get("dom"):
            _bydom[_e8["dom"]] = _e8
        _bydom.setdefault(_nrm(_e8["name"]), _e8)
    for _canon_key, _rows8 in _alias_rows.items():
        _tgt = _bydom.get(_canon_key)
        if not _tgt:
            continue
        for _row8 in _rows8:
            _hits8 = (_mnd.get((_row8.get("domain") or "").lower(), []) + _mnn.get(_nrm(_row8["name"]), []))
            _ppl8 = {p["n"]: p for p in _tgt.get("people") or []}
            for _u8, _nm8, _r8, _l8 in _hits8:
                _p8 = _ppl8.setdefault(_nm8, {"n": _nm8, "r": {}, "last": None})
                if _r8 > _p8["r"].get(_u8, 0):
                    _p8["r"][_u8] = _r8
                if _l8 and (not _p8["last"] or _l8 > _p8["last"]):
                    _p8["last"] = _l8
            _tgt["people"] = sorted(_ppl8.values(), key=lambda p: -max(p["r"].values(), default=0))[:10]
        # recompute coverage on the merged people (seniority defaults where unknown)
        def _sw8(p):
            return SCORING["sr_w"].get(p.get("sr"), 0.75)
        _tgt["CT"] = max(_tgt.get("CT") or 0, _noisy_or([(max(p["r"].values(), default=0), _sw8(p)) for p in _tgt["people"]]))
        for _u8 in roster:
            _it8 = [(p["r"].get(_u8, 0), _sw8(p)) for p in _tgt["people"] if p["r"].get(_u8)]
            if _it8:
                _tgt.setdefault("cu", {})[_u8] = max((_tgt.get("cu") or {}).get(_u8, 0), _noisy_or(_it8))

    # ---- arm merge: "Almi"+"Almi Invest", "Norrsken"+"Norrsken VC" are one investor ----
    _ARM_SUFFIX = {"vc", "ventures", "venture", "capital", "invest", "ventureCapital".lower(), "venturecapital", "growth"}
    _all9 = ents + aff_ents
    _dead = set()
    for _a9 in _all9:
        for _b9 in _all9:
            if _a9 is _b9 or id(_a9) in _dead or id(_b9) in _dead:
                continue
            na, nb = _nrm(_a9["name"]), _nrm(_b9["name"])
            if _a9.get("cc") != _b9.get("cc") or not nb.startswith(na) or na == nb:
                continue
            if nb[len(na):] not in _ARM_SUFFIX:
                continue
            # canonical keeps the scored record: if the SHORT-named side is curated and the
            # arm-named side is a bare Affinity row, keep the curated one and give it the arm's name
            if _a9.get("kind") != "aff" and _b9.get("kind") == "aff":
                _a9["name"] = _b9["name"]
                _a9, _b9 = _b9, _a9   # fold the bare row into the curated one
            # _b9 is canonical; fold _a9 into it
            _pplB = {p["n"]: p for p in _b9.get("people") or []}
            for _pA in _a9.get("people") or []:
                _pB = _pplB.setdefault(_pA["n"], _pA)
                if _pB is not _pA:
                    for _uA, _rA in _pA["r"].items():
                        _pB["r"][_uA] = max(_pB["r"].get(_uA, 0), _rA)
            _b9["people"] = sorted(_pplB.values(), key=lambda p: -max(p["r"].values(), default=0))[:10]
            _b9["CT"] = max(_b9.get("CT") or 0, _a9.get("CT") or 0)
            for _uA, _vA in (_a9.get("cu") or {}).items():
                _b9.setdefault("cu", {})[_uA] = max((_b9.get("cu") or {}).get(_uA, 0), _vA)
            if _a9.get("dfw", 0) > _b9.get("dfw", 0):
                _b9["dfw"], _b9["df12"], _b9["dfl"] = _a9["dfw"], _a9.get("df12", 0), _a9.get("dfl", [])
            if _a9.get("O", 0) > _b9.get("O", 0):
                _b9["O"] = _a9["O"]
            if _a9.get("pin"):
                _b9["pin"] = 1
            _dead.add(id(_a9))
    ents[:] = [e for e in ents if id(e) not in _dead]
    aff_ents[:] = [e for e in aff_ents if id(e) not in _dead]

    # ---- shortlist (v2 spec section 5): 20-30 per country, deal-flow ranked ----
    for _e9 in ents + aff_ents:
        _key9 = _e9.get("dom") or _nrm(_e9["name"])
        _e9["pin"] = 1 if (_key9 in _pins or _nrm(_e9["name"]) in _pins) else 0
        _e9["rm"] = 1 if (_e9["name"].lower() in _removes or _key9 in _removes) else 0
    for _cc9 in [k for subs in REGION_SUBS.values() for k in subs]:
        _pool = [e for e in ents if e.get("cc") == _cc9 and not e.get("rm")]
        _poolA = [e for e in aff_ents if e.get("cc") == _cc9 and not e.get("rm")]
        _ranked = sorted(_pool, key=lambda e: (-e.get("dfw", 0), -e.get("rel", 0)))[:25]
        _sl = {id(e) for e in _ranked}
        for e in _pool + _poolA:
            if e.get("pin") or (e in _poolA and (e.get("CT") or 0) >= 30):
                _sl.add(id(e))
        for e in _pool + _poolA:
            e["sl"] = 1 if id(e) in _sl else 0

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

    # ---- "Who do you know in <country>": every edge with a person there ----
    _pcs = load_json(f"{ROOT}/data/us/people-cities.json", {}) or {}
    _METRO_CC = {"SF": "SF", "NYC": "NYC", "BOS": "BOS", "LON": "LON"}
    def _person_cc(e, nm):
        """People file under the sub-area where they actually sit (Harmonic-verified
        city), for every region: a London-based Sequoia partner belongs to London,
        a Stockholm-based Northzone partner to Stockholm. Unknown city -> the
        fund's own area; a known city outside the map keeps them off city lists."""
        _k = (nm or "").lower()
        _city = ((pm.get(_k) or {}).get("city") or "")
        _cc = CITY2CC.get(_city.lower())
        if _cc:
            return _cc
        _m = ((_pcs.get(_k) or {}).get("metro") or "")
        _cc = _METRO_CC.get(_m) or CITY2CC.get(_m.lower())
        if _cc:
            return _cc
        if _city and e.get("rg") == "us":
            return None   # verified city off the map: not a door in any mapped metro
        return e["cc"]
    who_in = {}
    for _e10 in ents + aff_ents:
        if not _e10.get("cc"):
            continue
        for _p10 in _e10.get("people") or []:
            _r10 = {u: r for u, r in _p10["r"].items() if r >= 15}
            _cc10x = _person_cc(_e10, _p10["n"]) if _r10 else None
            if _r10 and _cc10x:
                _w10 = who_in.setdefault(_cc10x, {}).setdefault(_p10["n"], {
                    "n": _p10["n"], "org": _e10["name"], "last": _p10.get("last"), "r": {}})
                _w10["r"].update(_r10)
                for _k10 in ("sr", "t", "li"):
                    if _p10.get(_k10) and not _w10.get(_k10):
                        _w10[_k10] = _p10[_k10]
                if (_e10.get("O") or 0) >= (_w10.get("o") or 0):
                    _w10["o"] = _e10.get("O") or 0
                    _w10["df"] = _e10.get("df12") or 0
                    _w10["slug"] = _e10["slug"]
    for _cc10, _by10 in (people_in or {}).items():
        for _u10, _lst10 in _by10.items():
            for _px10 in _lst10:
                _rec10 = who_in.setdefault(_cc10, {}).setdefault(_px10["n"], {
                    "n": _px10["n"], "org": _px10.get("f"), "last": None, "r": {}})
                _rec10["r"][_u10] = max(_rec10["r"].get(_u10, 0), _px10["p"])
    # cap per geo, but never let the team's strongest edges crowd out a member's own
    # network: keep the global top 80 plus every member's personal top 40
    def _who_cap(rows):
        ranked = sorted(rows, key=lambda x: -max(x["r"].values(), default=0))
        keep = {id(x) for x in ranked[:80]}
        for u in roster:
            mine = sorted((x for x in rows if x["r"].get(u)), key=lambda x: -x["r"][u])[:40]
            keep.update(id(x) for x in mine)
        return [x for x in ranked if id(x) in keep]
    who_in = {cc: _who_cap(list(v.values())) for cc, v in who_in.items()}

    # ---- multi-pin: a fund also appears wherever its current team verifiably sits ----
    pins_in = {}
    for _e12 in ents:
        if not _e12.get("cc") or _e12.get("kind") == "angel":
            continue
        _locs12 = {}
        for _p12 in _e12.get("people") or []:
            _c12 = _person_cc(_e12, _p12["n"])
            if _c12 and _c12 != _e12["cc"] and _c12 in SUB_NAME:
                _locs12.setdefault(_c12, []).append(_p12["n"])
        for _c12, _nms12 in _locs12.items():
            # same human under two spellings (token-subset match): keep the fuller name
            import unicodedata as _ud12
            _tok12 = lambda n: {t for t in _ud12.normalize("NFKD", n.lower()).encode("ascii", "ignore").decode().split() if len(t) > 1}
            _kept12 = []
            for _n12 in sorted(set(_nms12), key=len, reverse=True):
                _t12 = _tok12(_n12)
                if not any(_t12 <= _tok12(k) or _tok12(k) <= _t12 for k in _kept12):
                    _kept12.append(_n12)
            pins_in.setdefault(_c12, []).append({"slug": _e12["slug"], "name": _e12["name"],
                                                 "cc": _e12["cc"], "ppl": _kept12[:4]})
    for _c12 in pins_in:
        pins_in[_c12].sort(key=lambda x: -len(x["ppl"]))

    # shortlist-based roll-ups replace the raw ones (a long tail cannot drag the number)
    for _cc11 in list(areas.keys()):
        if _cc11 in REGION_SUBS:
            _sel11 = [e for e in ents if e.get("rg") == _cc11 and e.get("sl")]
        else:
            _sel11 = [e for e in ents if e.get("cc") == _cc11 and e.get("sl")]
        # with no curated shortlist (Hamburg) keep the raw rollup, but still count the aff layer
        _ru = rollup(_sel11) if _sel11 else dict(areas[_cc11])
        _subs11 = REGION_SUBS.get(_cc11)
        _ru["sln"] = len(_sel11) + sum(1 for a in aff_ents if a.get("sl") and (
            (a.get("cc") in _subs11) if _subs11 else a.get("cc") == _cc11))
        _ru["known"] = ({u: len({p["n"] for cc2 in _subs11 for p in who_in.get(cc2, []) if p["r"].get(u)}) for u in roster}
                        if _subs11 else
                        {u: len([1 for p in who_in.get(_cc11, []) if p["r"].get(u)]) for u in roster})
        for _u11 in list(areas[_cc11].get("u") or {}):
            for _k11 in ("exp", "expg"):
                if _u11 in _ru["u"] and _k11 in areas[_cc11]["u"][_u11]:
                    _ru["u"][_u11][_k11] = areas[_cc11]["u"][_u11][_k11]
        areas[_cc11] = _ru

    # the full network rows were only needed for scoring — keep them out of the payload
    for _reg9 in regions.values():
        for _e9 in _reg9.get("entities") or []:
            _e9.pop("net", None)

    return {
        "vb": vbs, "peopleIn": people_in, "aff": aff_ents, "who": who_in,
        "subsOf": subs_of, "regOf": reg_of, "zoomReg": zoom_reg, "pinsIn": pins_in,
        "hl": {"nordics": REGION_SUBS["nordics"], "germany": ["DE"], "france": ["FR"], "uk": ["GB"], "us": ["US"]}, "countries": countries, "regions": region_pts,
        "ccent": {k: [round(v[0], 1), round(v[1], 1)] for k, v in ccent.items()},
        "cities": {c: [city_px[c][0], city_px[c][1]] for c in city_px},
        "zoomL1": round(zoom_l1, 2), "zoomL2": {k: round(v, 2) for k, v in zoom_l2.items()},
        "ents": ents, "areas": areas, "ccName": SUB_NAME, "nordics": NORDIC_CC,
    }


def _sr_from_title(title):
    t = (title or "").lower()
    if not t:
        return None
    if re.search(r"\blimited partner\b|investor\s*/\s*lp|\blp\b", t):
        return None   # an LP backs the fund but is not investment staff
    if (any(k in t for k in ("partner", "managing director", "head of", "chief", "founder", "cio", "ceo"))
            or re.search(r"\bgp\b", t)):
        return "Partner"
    if any(k in t for k in ("principal", "director", "vice president", " vp", "vp ", "investment manager", "lead")):
        return "Director"
    if any(k in t for k in ("associate", "analyst")):
        return "Associate"
    return None
