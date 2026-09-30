#!/usr/bin/env python3
"""Refresh data/affinity/_list-entries.json from the Affinity API (v2).

Produces the same compact shape the n8n dump workflow wrote:
{count, fetched: YYYY-MM-DD, entries: [{id, entry_id, name, domains, funnel,
owners, investors, country}]}

Reads AFFINITY_API_KEY from the environment. Exits 0 with a message (no file
change) when the key is absent, so callers can run it unconditionally.
"""
import json, os, sys, time, datetime, urllib.request, urllib.parse

LIST_ID = 9387
FIELDS = ["field-81237", "field-81239", "affinity-data-investors", "affinity-data-location"]
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = f"{ROOT}/data/affinity/_list-entries.json"

key = os.environ.get("AFFINITY_API_KEY")
if not key:
    print("AFFINITY_API_KEY not set — keeping committed dump")
    sys.exit(0)


def get(url):
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {key}"})
    for attempt in range(4):
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                return json.load(r)
        except Exception as e:  # noqa: BLE001 — retry transient API/network errors
            if attempt == 3:
                raise
            print(f"retry after error: {e}")
            time.sleep(2 ** (attempt + 1))


def names(v):
    """Extract a list of display names/texts from any v2 field value shape."""
    out = []
    def walk(x):
        if isinstance(x, list):
            for i in x:
                walk(i)
        elif isinstance(x, dict):
            if x.get("text"):
                out.append(x["text"])
            elif x.get("name"):
                out.append(x["name"])
            elif x.get("firstName") or x.get("lastName"):
                out.append(" ".join(filter(None, [x.get("firstName"), x.get("lastName")])))
            else:
                for k in ("data", "value", "values"):
                    if k in x:
                        walk(x[k])
        elif isinstance(x, str) and x:
            out.append(x)
    walk(v)
    return out


def country(v):
    def find(x):
        if isinstance(x, dict):
            if x.get("country"):
                return x["country"]
            for k in ("data", "value"):
                if k in x:
                    got = find(x[k])
                    if got:
                        return got
        if isinstance(x, list):
            for i in x:
                got = find(i)
                if got:
                    return got
        return None
    return find(v)


entries, unknown = [], set()
url = (f"https://api.affinity.co/v2/lists/{LIST_ID}/list-entries?limit=100&"
       + urllib.parse.urlencode([("fieldIds", f) for f in FIELDS]))
pages = 0
while url:
    page = get(url)
    pages += 1
    for row in page.get("data", []):
        ent = row.get("entity") or {}
        fields = {f.get("id"): f.get("value") for f in (row.get("fields") or [])}
        funnel_names = names(fields.get("field-81237"))
        entries.append({
            "id": ent.get("id"),
            "entry_id": row.get("id"),
            "name": ent.get("name"),
            "domains": ent.get("domains") or ([ent.get("domain")] if ent.get("domain") else []),
            "funnel": funnel_names[0] if funnel_names else None,
            "owners": names(fields.get("field-81239")),
            "investors": names(fields.get("affinity-data-investors")),
            "country": country(fields.get("affinity-data-location")),
        })
        for fid in fields:
            if fid not in FIELDS:
                unknown.add(fid)
    nxt = (page.get("pagination") or {}).get("nextUrl")
    url = nxt
    if pages % 25 == 0:
        print(f"  …{len(entries)} entries after {pages} pages")

if len(entries) < 1000:
    print(f"SAFEGUARD: only {len(entries)} entries fetched (expected ~24k+) — "
          "refusing to overwrite the committed dump")
    sys.exit(1)

out = {"count": len(entries),
       "fetched": datetime.date.today().isoformat(),
       "entries": entries}
json.dump(out, open(OUT, "w"), ensure_ascii=False)
print(f"wrote {OUT}: {len(entries)} entries over {pages} pages"
      + (f" (unexpected field ids seen: {sorted(unknown)[:5]})" if unknown else ""))
