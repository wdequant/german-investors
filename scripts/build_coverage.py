#!/usr/bin/env python3
"""Build the multi-region coverage map (Germany + Nordics) -> viz/index.html"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from coverage_common import finalize, TODAY, AFFINITY_ORG, load_json
import assemble_germany, assemble_nordics
import importlib.util as _ilu

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
team = load_json(f"{ROOT}/data/highland-team.json")
roster = [m["name"] for m in team] + ["Fergal Mullen", "Laurence Garrett", "Ronan Shally"]

regions = {
    "germany": {"label": "Germany", "adj": "German", "entities": finalize(assemble_germany.assemble(team))},
    "nordics": {"label": "Nordics", "adj": "Nordic", "entities": finalize(assemble_nordics.assemble(team))},
}

_spec = _ilu.spec_from_file_location("coverage_template", os.path.join(os.path.dirname(os.path.abspath(__file__)), "coverage_template.py"))
_tpl = _ilu.module_from_spec(_spec); _spec.loader.exec_module(_tpl)

payload = {"generated": TODAY.strftime("%d %b %Y"), "team": team, "roster": roster,
           "affinityOrg": AFFINITY_ORG, "regions": regions}
html = _tpl.TEMPLATE.replace("__DATA__", json.dumps(payload, ensure_ascii=False)).replace("__GENERATED__", payload["generated"])
os.makedirs(f"{ROOT}/viz", exist_ok=True)
open(f"{ROOT}/viz/index.html", "w").write(html)
for k, r in regions.items():
    f = [e for e in r["entities"] if e["kind"] == "fund"]
    print(f"{k}: {len(f)} funds + {len(r['entities'])-len(f)} angels, top gap: {max(f, key=lambda x: x['gap'])['name']}")
print(f"wrote viz/index.html ({len(html)//1024} KB)")
