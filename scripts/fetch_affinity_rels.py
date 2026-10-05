#!/usr/bin/env python3
"""Refresh per-fund Affinity relationship edges from the live API (v1).

Replaces the frozen August top-10 snapshots. For every tracked fund file that
carries an affinity_domain (angels keep their curated edges):
  1. GET /persons?term=<domain>&with_interaction_dates=true   (paged)
  2. keep real people whose email is at the fund's domain
  3. GET /relationships-strengths?external_id=<id> -> who at Highland holds it
  4. rewrite the file's "relationships" as
     {internal, external, externalEmail, score, last, meet}
     where last = last interaction of any kind, meet = last calendar event.

Reads AFFINITY_API_KEY. Exits 0 untouched when the key is absent so callers
can run it unconditionally. A fund whose fetch fails keeps its old edges.
"""
import base64
import datetime
import glob
import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TODAY = datetime.date.today()

key = os.environ.get("AFFINITY_API_KEY")
if not key:
    print("AFFINITY_API_KEY not set — keeping committed relationship snapshots")
    sys.exit(0)

AUTH = "Basic " + base64.b64encode(f":{key}".encode()).decode()

# role/system mailboxes and event records that are not people
JUNK_LOCAL = {"events", "event", "info", "hello", "team", "office", "press",
              "contact", "noreply", "no-reply", "invites", "news", "careers",
              "jobs", "hi", "mail", "admin", "ir", "lp", "legal", "invest"}
JUNK_NAME = re.compile(r"drinks|dinner|event|day zero|summit|team|newsletter", re.I)


def get(path, tries=4):
    req = urllib.request.Request("https://api.affinity.co" + path,
                                 headers={"Authorization": AUTH})
    for attempt in range(tries):
        try:
            with urllib.request.urlopen(req, timeout=45) as r:
                return json.load(r)
        except Exception as e:  # noqa: BLE001 — retry 429/5xx/network
            if attempt == tries - 1:
                raise
            time.sleep(2 ** (attempt + 1))
            print(f"  retry {path.split('?')[0]}: {e}")


def persons_at(domain):
    """All Affinity persons with an email at this domain, with interaction dates."""
    out, token = [], None
    while True:
        q = {"term": domain, "with_interaction_dates": "true", "page_size": 500}
        if token:
            q["page_token"] = token
        page = get("/persons?" + urllib.parse.urlencode(q))
        for p in page.get("persons", []):
            emails = [e.lower() for e in (p.get("emails") or []) if e]
            if not any(e.endswith("@" + domain) or e.endswith("." + domain)
                       for e in emails):
                continue
            local = next((e.split("@")[0] for e in emails
                          if e.endswith("@" + domain)), "")
            name = " ".join(filter(None, [p.get("first_name"), p.get("last_name")]))
            if (local in JUNK_LOCAL or JUNK_NAME.search(name)
                    or len(name.split()) > 4 or not name.strip()):
                continue
            out.append(p)
        token = page.get("next_page_token")
        if not token:
            return out


_internal_names = {}


def internal_name(pid):
    if pid not in _internal_names:
        p = get(f"/persons/{pid}")
        _internal_names[pid] = " ".join(
            filter(None, [p.get("first_name"), p.get("last_name")]))
        time.sleep(0.05)
    return _internal_names[pid]


def _decay(last):
    if not last:
        return 0.85
    days = (TODAY - datetime.date.fromisoformat(str(last)[:10])).days
    return 1.0 if days <= 180 else 0.9 if days <= 365 else 0.5 if days <= 730 else 0.3


def refresh(path):
    data = json.load(open(path))
    domain = data.get("affinity_domain")
    if not domain:
        return None
    people = persons_at(domain)
    time.sleep(0.07)
    rels = []
    for p in people:
        ia = p.get("interaction_dates") or {}
        last = (ia.get("last_interaction_date") or "")[:10] or None
        meet = (ia.get("last_event_date") or "")[:10] or None
        if not last:          # no interaction ever -> no edge to rank
            continue
        strengths = get(f"/relationships-strengths?external_id={p['id']}")
        time.sleep(0.07)
        name = " ".join(filter(None, [p.get("first_name"), p.get("last_name")]))
        email = next((e for e in (p.get("emails") or [])
                      if e.lower().endswith("@" + domain)), p.get("primary_email"))
        for s in strengths or []:
            sc = s.get("strength") or 0
            if sc < 0.05:
                continue
            rels.append({"internal": internal_name(s["internal_id"]),
                         "external": name, "externalEmail": email,
                         "score": round(sc, 2), "last": last, "meet": meet})
    rels.sort(key=lambda r: -(r["score"] * _decay(r["last"])
                              * (1.0 if r["meet"] else 0.75)))
    data["relationships"] = rels[:40]
    data["rels_fetched"] = TODAY.isoformat()
    json.dump(data, open(path, "w"), ensure_ascii=False, indent=1)
    return len(people), len(data["relationships"])


paths = sorted(glob.glob(f"{ROOT}/data/affinity/*.json")
               + glob.glob(f"{ROOT}/data/*/affinity/*.json"))
if sys.argv[1:]:  # optional prefix filter, e.g. `fetch_affinity_rels.py data/us`
    paths = [p for p in paths
             if any(p.removeprefix(ROOT + "/").startswith(a) for a in sys.argv[1:])]
done = failed = 0
for path in paths:
    base = os.path.basename(path)
    if base.startswith(("_", "angel-", "50-partners", "partners-meta")):
        continue
    try:
        res = refresh(path)
        if res:
            done += 1
            print(f"{path.removeprefix(ROOT + '/')}: {res[0]} people -> {res[1]} edges")
    except Exception as e:  # noqa: BLE001 — keep the old snapshot for this fund
        failed += 1
        print(f"FAILED {path.removeprefix(ROOT + '/')}: {e} — old edges kept")
print(f"refreshed {done} funds, {failed} failed")
sys.exit(1 if (failed and not done) else 0)
