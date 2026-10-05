#!/usr/bin/env python3
"""Per-H2C Affinity communication history + time-in-status.

For every Hard-to-crack entry in the pipeline dump:
  - GET /organizations/{id}?with_interaction_dates=true  (v1)
      -> first/last email, last meeting, last touch of any kind
  - GET /field-value-changes?field_id=81237&list_entry_id={entry_id}  (v1)
      -> when the entry last moved into its current status

Writes data/enrich/htc-meta.json keyed by the Affinity org id (string).
Merge-writes: existing ids are kept unless --refresh. Reads AFFINITY_API_KEY;
exits 0 untouched without it.
"""
import base64
import datetime
import json
import os
import sys
import time
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = f"{ROOT}/data/enrich/htc-meta.json"
STATUS_FIELD = 81237

key = os.environ.get("AFFINITY_API_KEY")
if not key:
    print("AFFINITY_API_KEY not set — keeping committed H2C meta")
    sys.exit(0)
AUTH = "Basic " + base64.b64encode(f":{key}".encode()).decode()


def get(path, tries=4):
    req = urllib.request.Request("https://api.affinity.co" + path,
                                 headers={"Authorization": AUTH})
    for attempt in range(tries):
        try:
            with urllib.request.urlopen(req, timeout=45) as r:
                return json.load(r)
        except Exception as e:  # noqa: BLE001
            if attempt == tries - 1:
                raise
            time.sleep(2 ** (attempt + 1))
            print(f"  retry {path.split('?')[0]}: {e}")


dump = json.load(open(f"{ROOT}/data/affinity/_list-entries.json"))
htcs = [e for e in dump["entries"] if e.get("funnel") == "Hard to crack"]

out = {}
if "--refresh" not in sys.argv:
    try:
        out = json.load(open(OUT))
    except FileNotFoundError:
        pass

todo = [e for e in htcs if str(e["id"]) not in out]
print(f"{len(htcs)} H2C entries, {len(todo)} to fetch")
done = failed = 0
for e in todo:
    try:
        org = get(f"/organizations/{e['id']}?with_interaction_dates=true") or {}
        ia = org.get("interaction_dates") or {}
        rec = {"first_email": (ia.get("first_email_date") or "")[:10] or None,
               "last_email": (ia.get("last_email_date") or "")[:10] or None,
               "last_meet": (ia.get("last_event_date") or "")[:10] or None,
               "last_touch": (ia.get("last_interaction_date") or "")[:10] or None,
               "status_since": None}
        time.sleep(0.06)
        if e.get("entry_id"):
            try:
                ch = get(f"/field-value-changes?field_id={STATUS_FIELD}"
                         f"&list_entry_id={e['entry_id']}") or []
                dates = [c.get("changed_at", "")[:10] for c in ch
                         if c.get("changed_at")]
                if dates:
                    rec["status_since"] = max(dates)
            except Exception:  # noqa: BLE001 — history is best-effort
                pass
            time.sleep(0.06)
        out[str(e["id"])] = rec
        done += 1
        if done % 25 == 0:
            json.dump(out, open(OUT, "w"), ensure_ascii=False, indent=1)
            print(f"  {done}/{len(todo)}")
    except Exception as err:  # noqa: BLE001
        failed += 1
        print(f"FAILED {e.get('name')}: {err}")
json.dump(out, open(OUT, "w"), ensure_ascii=False, indent=1)
print(f"fetched {done}, failed {failed} -> {OUT} "
      f"(as of {datetime.date.today().isoformat()})")
sys.exit(1 if (failed and not done) else 0)
