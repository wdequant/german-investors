#!/usr/bin/env python3
"""Build the Highland x Germany connectivity matrix.

Inputs (data/):
  germany-investors.json   - 74 investors from the Harmonic saved search
  connections.json         - parsed get_company_connections output (70 companies)
  coinvestments.json       - German funds Highland has co-invested with + shared companies
  highland-team.json       - investment team roster mapped to Harmonic users

Output: viz/index.html (self-contained, no external requests)
"""
import json, math, os, re
from datetime import datetime, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TODAY = datetime(2026, 8, 12, tzinfo=timezone.utc)

investors = json.load(open(f"{ROOT}/data/germany-investors.json"))
connections = json.load(open(f"{ROOT}/data/connections.json"))
coinvest = json.load(open(f"{ROOT}/data/coinvestments.json"))
team = json.load(open(f"{ROOT}/data/highland-team.json"))

TEAM_ORDER = [m["name"] for m in team]
TEAM_SET = set(TEAM_ORDER)

# ---- categories -------------------------------------------------------------
CATEGORY = {
    "Global Founders Capital": "vc", "HTGF | High-Tech Gründerfonds": "state",
    "HV Capital": "vc", "Earlybird Venture Capital": "vc", "Point Nine": "vc",
    "468 Capital": "vc", "Picus Capital": "vc", "Cherry Ventures": "vc",
    "Bayern Kapital": "state", "Project A": "vc", "IBB Ventures": "state",
    "Atlantic Labs": "vc", "1kx": "vc", "TA Ventures": "vc",
    "Rocket Internet SE": "corporate", "Redstone": "vc", "Bosch Ventures": "cvc",
    "BlueYard Capital": "vc", "Possible Ventures": "vc", "Capnamic": "vc",
    "UVC Partners": "vc", "Angel Invest": "vc", "MIG Capital": "vc",
    "Acton Capital": "vc", "Foundamental": "vc", "NAP (New Amsterdam Partners)": "vc",
    "FoodLabs": "vc", "10x Founders": "vc", "Dieter von Holtzbrinck Ventures": "vc",
    "Vorwerk Ventures": "cvc", "Fly Ventures": "vc", "SquareOne Venture Capital": "vc",
    "Hitachi Ventures": "cvc", "CommerzVentures": "cvc", "Axel Springer": "corporate",
    "Cusp Capital": "vc", "Siemens": "corporate", "Senovo": "vc",
    "Porsche Ventures": "cvc", "Vsquared Ventures": "vc", "Moonrock Capital": "vc",
    "Matterwave Ventures": "vc", "STS Ventures": "vc", "Burda Principal Investments": "cvc",
    "Mario Götze": "angel", "10x Group": "vc", "Alstin Capital": "vc",
    "Discovery Ventures": "vc", "AENU": "vc", "Capmont Technology": "vc",
    "D11Z. Ventures": "vc", "Bertelsmann Investments": "cvc", "Lunar Ventures": "vc",
    "another.vc": "vc", "X Ventures": "vc", "Amino Collective": "vc",
    "Inflection.xyz": "vc", "SB21": "vc", "Simon Capital": "vc", "World Fund": "vc",
    "Bosch": "corporate", "Deutsche Börse": "corporate", "OCCIDENT": "vc",
    "kopa ventures": "vc", "Hanno Renner (Personio)": "angel", "DöhlerGroup": "corporate",
    "Merantix Capital": "vc", "Heliad": "cvc", "Reimann Investors": "cvc",
    "System.One": "vc", "FinLab AG": "cvc", "Julius Göllner (ARRtist)": "angel",
    "Matthias Hilpert (MH2 Capital)": "angel",
}
EXCLUDED = {"GV (data-quality flag: likely mis-mapped record)"}
CRYPTO = {"1kx", "Moonrock Capital", "Inflection.xyz", "X Ventures"}

# ---- weights ----------------------------------------------------------------
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
    if any(k in t for k in ["principal", "investment director", "senior investment director",
                            "head of venture", "director"]):
        return 2.0
    if any(k in t for k in ["investment manager", "investor", "vc", "member of the investment committee"]):
        return 1.5
    if any(k in t for k in ["associate", "analyst", "fellow"]):
        return 1.0
    return 0.5  # EA / events / comms / platform / IR / legal / unknown

def source_weight(sources):
    s = set(sources or [])
    if "CALENDAR" in s and "EMAIL" in s:
        return 3.5 if "LINKEDIN" in s else 3.0
    if "EMAIL" in s:
        return 2.0
    return 1.0  # LinkedIn only

# ---- per-fund assembly -------------------------------------------------------
coinvest_by_urn = {c["urn"]: c for c in coinvest}
conn_by_id = {int(k): v for k, v in connections.items()}

SECTOR_SOFTWARE = ("Communications & Information Technology", "Business Services")

def relevance(inv):
    name = inv["name"]
    # stage (30)
    stages = inv.get("entry_stage_focus") or ""
    if "SEED" in stages.replace("PRE_SEED", "") or "SERIES_A" in stages:
        stage_pts = 30
    elif "PRE_SEED" in stages:
        stage_pts = 18
    else:
        stage_pts = 8
    # sector (30)
    sf = inv.get("sector_focus") or ""
    if name in CRYPTO:
        sector_pts = 4
    elif any(s in sf for s in SECTOR_SOFTWARE):
        sector_pts = 30
    elif "Financial Services" in sf:
        sector_pts = 24
    elif "Consumer Products & Services" in sf or "Media & Entertainment" in sf:
        sector_pts = 20
    elif any(s in sf for s in ("Industrial", "Energy", "Materials", "Transportation", "Real Estate", "Agriculture", "Social Impact")):
        sector_pts = 14
    elif "Life Sciences" in sf:
        sector_pts = 8
    else:
        sector_pts = 14
    # activity (20)
    last = inv.get("last_investment")
    days = 9999
    if last and last != "null":
        days = (TODAY - datetime.fromisoformat(last.replace("Z", "+00:00"))).days
    activity_pts = 20 if days <= 60 else 16 if days <= 180 else 10 if days <= 365 else 4
    # graduation quality (20)
    uni = inv.get("num_unicorns") or 0
    port = inv.get("num_portfolio_companies") or inv.get("num_investments") or 1
    for_ = inv.get("follow_on_rate") or 0
    grad_pts = round(min(20, 20 * min(1.0, ((uni / max(port, 1)) * 10 + for_) / 1.4)), 1)
    return {
        "total": round(stage_pts + sector_pts + activity_pts + grad_pts),
        "stage": stage_pts, "sector": sector_pts, "activity": activity_pts, "grad": grad_pts,
        "days_since": days,
    }

funds = []
for inv in investors:
    name = inv["name"]
    cid = None
    if ":company:" in (inv.get("company_urn") or ""):
        cid = int(inv["company_urn"].rsplit(":", 1)[1])
    cat = "excluded" if name in EXCLUDED else CATEGORY.get(name, "vc")
    rel = relevance(inv)

    cells = {u: {"score": 0.0, "contacts": []} for u in TEAM_ORDER}
    conn = conn_by_id.get(cid) if cid else None
    if conn:
        for c in conn["connections"]:
            cw = contact_weight(c.get("title"), c.get("external", False))
            for via in c.get("via", []):
                u = via.get("user")
                if u not in TEAM_SET:
                    continue
                sw = source_weight(via.get("sources"))
                cells[u]["score"] += cw * sw
                cells[u]["contacts"].append({
                    "person": c.get("person") or "(unnamed)",
                    "title": c.get("title") or "—",
                    "external": bool(c.get("external")),
                    "sources": via.get("sources") or [],
                    "w": round(cw * sw, 1),
                })
    for u in cells:
        cells[u]["score"] = round(cells[u]["score"], 1)
        cells[u]["contacts"].sort(key=lambda x: -x["w"])

    max_cell = max(c["score"] for c in cells.values())
    breadth = sum(1 for c in cells.values() if c["score"] > 0)
    total_w = sum(c["score"] for c in cells.values())
    conn_score = 0.7 * math.sqrt(max_cell) + 0.3 * math.sqrt(total_w)

    co = coinvest_by_urn.get(inv["urn"])
    funds.append({
        "name": name, "city": inv.get("city"), "category": cat,
        "stages": inv.get("entry_stage_focus"), "sector": inv.get("sector_focus"),
        "num_investments": inv.get("num_investments"),
        "unicorns": inv.get("num_unicorns"),
        "last_investment": (inv.get("last_investment") or "")[:10],
        "relevance": rel, "cells": cells,
        "max_cell": max_cell, "breadth": breadth, "total_w": round(total_w, 1),
        "conn_raw": conn_score,
        "coinvest": co["company_names"] if co else [],
        "urn": inv["urn"],
    })

# normalise connectivity 0-100 within included funds
included = [f for f in funds if f["category"] not in ("excluded", "angel")]
cmax = max(f["conn_raw"] for f in included) or 1
for f in funds:
    f["connectivity"] = round(100 * f["conn_raw"] / cmax)
    f["gap"] = round(f["relevance"]["total"] * (1 - f["connectivity"] / 100))
    del f["conn_raw"]

payload = {
    "generated": TODAY.strftime("%d %b %Y"),
    "team": team,
    "funds": funds,
}

# ---- HTML -------------------------------------------------------------------
DATA = json.dumps(payload, ensure_ascii=False)

html = """<title>Germany Coverage Map</title>
<style>
:root{
  color-scheme:light;
  --page:#f9f9f7; --surface:#fcfcfb; --ink:#0b0b0b; --ink2:#52514e; --muted:#898781;
  --grid:#e1e0d9; --baseline:#c3c2b7; --ring:rgba(11,11,11,.10);
  --accent:#2a78d6; --accent-deep:#1c5cab;
  --seq0:transparent; --seq1:#cde2fb; --seq2:#9ec5f4; --seq3:#6da7ec;
  --seq4:#3987e5; --seq5:#256abf; --seq6:#184f95; --seq7:#0d366b;
  --good:#0ca30c; --good-text:#006300; --critical:#d03b3b;
  --chip:#f0efec; --rowhover:#f3f2ee;
}
@media (prefers-color-scheme: dark){
  :root:where(:not([data-theme="light"])){
    color-scheme:dark;
    --page:#0d0d0d; --surface:#1a1a19; --ink:#ffffff; --ink2:#c3c2b7; --muted:#898781;
    --grid:#2c2c2a; --baseline:#383835; --ring:rgba(255,255,255,.10);
    --accent:#3987e5; --accent-deep:#86b6ef;
    --seq1:#0d366b; --seq2:#104281; --seq3:#184f95; --seq4:#1c5cab;
    --seq5:#256abf; --seq6:#3987e5; --seq7:#86b6ef;
    --good:#0ca30c; --good-text:#0ca30c; --critical:#e66767;
    --chip:#242423; --rowhover:#222221;
  }
}
:root[data-theme="dark"]{
  color-scheme:dark;
  --page:#0d0d0d; --surface:#1a1a19; --ink:#ffffff; --ink2:#c3c2b7; --muted:#898781;
  --grid:#2c2c2a; --baseline:#383835; --ring:rgba(255,255,255,.10);
  --accent:#3987e5; --accent-deep:#86b6ef;
  --seq1:#0d366b; --seq2:#104281; --seq3:#184f95; --seq4:#1c5cab;
  --seq5:#256abf; --seq6:#3987e5; --seq7:#86b6ef;
  --good:#0ca30c; --good-text:#0ca30c; --critical:#e66767;
  --chip:#242423; --rowhover:#222221;
}
*{box-sizing:border-box;margin:0}
body{background:var(--page);color:var(--ink);
  font:14px/1.45 system-ui,-apple-system,"Segoe UI",sans-serif;padding:28px 24px 80px}
h1{font-size:22px;font-weight:650;letter-spacing:-.01em}
.sub{color:var(--ink2);margin-top:4px;max-width:72ch}
.kicker{font-size:11px;letter-spacing:.08em;text-transform:uppercase;color:var(--muted);margin-bottom:6px}
.tiles{display:flex;gap:12px;flex-wrap:wrap;margin:20px 0}
.tile{background:var(--surface);border:1px solid var(--ring);border-radius:8px;padding:12px 16px;min-width:130px}
.tile b{display:block;font-size:24px;font-weight:650;font-variant-numeric:tabular-nums}
.tile span{color:var(--ink2);font-size:12px}
.tile.crit b{color:var(--critical)}
.controls{display:flex;gap:10px;align-items:center;flex-wrap:wrap;margin:14px 0 10px}
.controls label{font-size:12px;color:var(--ink2)}
.chipbtn{border:1px solid var(--ring);background:var(--chip);color:var(--ink2);
  border-radius:14px;padding:4px 12px;font-size:12px;cursor:pointer}
.chipbtn.on{background:var(--accent);border-color:var(--accent);color:#fff}
select,input[type=search]{background:var(--surface);color:var(--ink);border:1px solid var(--grid);
  border-radius:6px;padding:5px 8px;font-size:13px}
input[type=search]{width:180px}
.legend{display:flex;align-items:center;gap:6px;font-size:12px;color:var(--ink2);margin-left:auto}
.legend .sw{width:16px;height:12px;border-radius:2px;border:1px solid var(--ring)}
.matrix-wrap{overflow-x:auto;background:var(--surface);border:1px solid var(--ring);border-radius:10px}
table{border-collapse:separate;border-spacing:0;width:100%;font-variant-numeric:tabular-nums}
th,td{padding:0;border-bottom:1px solid var(--grid)}
thead th{position:sticky;top:0;background:var(--surface);z-index:3;
  font-size:11px;font-weight:600;color:var(--ink2);vertical-align:bottom;padding:8px 3px;text-align:center}
thead th.colname span{writing-mode:vertical-rl;transform:rotate(190deg);transform:rotate(180deg);
  display:inline-block;max-height:110px;overflow:hidden;letter-spacing:.02em}
thead th.grp{border-left:1px solid var(--grid)}
td.fund,th.fund{position:sticky;left:0;background:var(--surface);z-index:2;text-align:left;
  padding:7px 12px;min-width:230px;max-width:280px;border-right:1px solid var(--grid)}
tr:hover td{background:var(--rowhover)}
tr:hover td.fund{background:var(--rowhover)}
.fname{font-weight:600;font-size:13px;cursor:pointer}
.fmeta{font-size:11px;color:var(--muted);margin-top:1px;display:flex;gap:6px;flex-wrap:wrap;align-items:center}
.badge{font-size:10px;border-radius:9px;padding:1px 7px;background:var(--chip);color:var(--ink2);white-space:nowrap}
.badge.co{color:var(--good-text);border:1px solid var(--good);background:transparent}
.badge.gapb{color:var(--critical);border:1px solid var(--critical);background:transparent;font-weight:600}
.badge.cat{text-transform:uppercase;letter-spacing:.05em}
td.num{padding:6px 8px;text-align:right;font-size:12px;color:var(--ink2);white-space:nowrap}
td.num b{color:var(--ink);font-weight:600}
td.cell{width:34px;height:30px;text-align:center;border-left:1px solid var(--grid);position:relative;cursor:default}
td.cell .fill{position:absolute;inset:2px;border-radius:3px}
td.cell.grp{border-left:1px solid var(--baseline)}
.relbar{display:inline-block;vertical-align:middle;width:56px;height:6px;background:var(--chip);
  border-radius:3px;overflow:hidden;margin-left:6px}
.relbar i{display:block;height:100%;background:var(--accent);border-radius:3px}
.gaprow td.fund{box-shadow:inset 3px 0 0 var(--critical)}
#tip{position:fixed;z-index:50;background:var(--surface);border:1px solid var(--ring);border-radius:8px;
  box-shadow:0 6px 24px rgba(0,0,0,.18);padding:10px 12px;font-size:12px;max-width:340px;display:none;pointer-events:none}
#tip h4{font-size:12px;margin-bottom:6px}
#tip .c{display:flex;justify-content:space-between;gap:12px;padding:2px 0;border-top:1px dashed var(--grid)}
#tip .c:first-of-type{border-top:0}
#tip .src{color:var(--muted);font-size:10px;letter-spacing:.04em}
#tip .ext{color:var(--muted);font-style:italic}
.detail{display:none}
.detail.open{display:table-row}
.detail>td{background:var(--page);padding:12px 16px 16px;border-bottom:2px solid var(--baseline)}
.detail .cols{display:flex;gap:22px;flex-wrap:wrap}
.detail .tm{min-width:200px}
.detail .tm h5{font-size:12px;margin-bottom:4px;color:var(--accent-deep)}
.detail .tm div{font-size:12px;padding:2px 0;color:var(--ink2)}
.detail .tm .t{color:var(--muted)}
.detail .scorebits{font-size:11px;color:var(--muted);margin-bottom:8px}
.note{font-size:12px;color:var(--muted);margin-top:14px;max-width:90ch}
@media (max-width:700px){ td.fund,th.fund{min-width:170px} }
</style>

<div class="kicker">Highland Europe · VC ecosystem connectivity · Germany</div>
<h1>Germany Coverage Map</h1>
<p class="sub">Who at Highland is best connected into each active German early-stage fund, where we have
co-invested before, and which relevant funds we barely know. Cell colour = strength of that person's
relationships into the fund (contact seniority × email/calendar/LinkedIn evidence, from the Harmonic
team-network sync). Rows flagged <b style="color:var(--critical)">⚑ gap</b> are relevant funds with weak coverage.</p>

<div class="tiles" id="tiles"></div>

<div class="controls">
  <label>Show:</label>
  <button class="chipbtn on" data-cat="vc">VC</button>
  <button class="chipbtn on" data-cat="state">State</button>
  <button class="chipbtn" data-cat="cvc">CVC</button>
  <button class="chipbtn" data-cat="corporate">Corporate</button>
  <button class="chipbtn" data-cat="angel">Angels</button>
  <label style="margin-left:10px">Sort:</label>
  <select id="sort">
    <option value="gap">Coverage gap</option>
    <option value="relevance">Relevance</option>
    <option value="connectivity">Connectivity</option>
    <option value="name">Name</option>
  </select>
  <input type="search" id="q" placeholder="Filter funds…">
  <div class="legend">weak <span class="sw" style="background:var(--seq1)"></span><span class="sw" style="background:var(--seq3)"></span><span class="sw" style="background:var(--seq5)"></span><span class="sw" style="background:var(--seq7)"></span> strong</div>
</div>

<div class="matrix-wrap"><table id="mx"></table></div>
<div id="tip"></div>

<p class="note"><b>Method.</b> Universe: “Germany Investors” Harmonic saved search (74 investors).
Relevance (0–100) = stage fit (Seed/A entry, 30) + sector fit vs Highland's software/internet thesis (30)
+ activity recency (20) + graduation quality (unicorn rate &amp; follow-on, 20). Connectivity (0–100) is
normalised across funds: strongest single teammate link (70%) + team breadth (30%).
Gap = relevance × (1 − connectivity). Co-invest badges from Highland's Harmonic co-investor record.
Caveats: Fergal &amp; Laurence have no active Harmonic network sync, so their relationships are invisible here;
LinkedIn-only links are weighted well below email/calendar relationships; angels have no network pull yet.</p>

<script>
const D = __DATA__;
const seqVars = ['--seq1','--seq2','--seq3','--seq4','--seq5','--seq6','--seq7'];
const state = {cats:new Set(['vc','state']), sort:'gap', q:''};
const SRC = {LINKEDIN:'LI', EMAIL:'Email', CALENDAR:'Cal'};

function fmt(n){return n==null?'—':n.toLocaleString('en-GB')}
function cellStep(s){ if(s<=0)return -1; const t=Math.min(1,Math.sqrt(s)/Math.sqrt(30)); return Math.min(6,Math.floor(t*7)); }

function visibleFunds(){
  let fs = D.funds.filter(f=>state.cats.has(f.category));
  if(state.q) fs = fs.filter(f=>f.name.toLowerCase().includes(state.q));
  const key = state.sort;
  fs.sort((a,b)=> key==='name' ? a.name.localeCompare(b.name)
    : key==='relevance' ? b.relevance.total-a.relevance.total
    : key==='connectivity' ? b.connectivity-a.connectivity
    : b.gap-a.gap);
  return fs;
}

function tiles(){
  const inc = D.funds.filter(f=>!['excluded','angel'].includes(f.category));
  const gaps = inc.filter(f=>['vc','state'].includes(f.category) && f.relevance.total>=60 && f.connectivity<25);
  const cos  = inc.filter(f=>f.coinvest.length);
  const covered = inc.filter(f=>f.connectivity>=40);
  document.getElementById('tiles').innerHTML = `
    <div class="tile"><b>${D.funds.length}</b><span>funds tracked</span></div>
    <div class="tile"><b>${cos.length}</b><span>co-invested with</span></div>
    <div class="tile"><b>${covered.length}</b><span>well covered (conn ≥ 40)</span></div>
    <div class="tile crit"><b>${gaps.length}</b><span>⚑ coverage gaps (rel ≥ 60, conn &lt; 25)</span></div>`;
}

function render(){
  const fs = visibleFunds();
  const groups = {partner:'Partners', senior:'Senior', associate:'Associates', analyst:''};
  let prevRole=null;
  let head = '<thead><tr><th class="fund">Fund</th><th style="min-width:74px">Rel · Conn</th>';
  D.team.forEach(m=>{ const g=m.role!==prevRole; prevRole=m.role;
    head += `<th class="colname${g?' grp':''}"><span>${m.name}</span></th>`; });
  head += '</tr></thead>';
  let body='<tbody>';
  fs.forEach((f,idx)=>{
    const isGap = f.relevance.total>=60 && f.connectivity<25 && ['vc','state'].includes(f.category);
    const co = f.coinvest.length?`<span class="badge co">✓ co-invested ×${f.coinvest.length}</span>`:'';
    const gapb = isGap?'<span class="badge gapb">⚑ gap</span>':'';
    body += `<tr class="frow${isGap?' gaprow':''}" data-i="${idx}">
      <td class="fund"><div class="fname" data-i="${idx}">${f.name}</div>
        <div class="fmeta"><span class="badge cat">${f.category}</span><span>${f.city||''}</span>${co}${gapb}</div></td>
      <td class="num"><b>${f.relevance.total}</b><span class="relbar"><i style="width:${f.relevance.total}%"></i></span><br>
        <b>${f.connectivity}</b><span class="relbar"><i style="width:${f.connectivity}%;background:var(--seq5)"></i></span></td>`;
    prevRole=null;
    D.team.forEach(m=>{ const g=m.role!==prevRole; prevRole=m.role;
      const c=f.cells[m.name]; const step=cellStep(c.score);
      const fill = step<0?'':`<span class="fill" style="background:var(${seqVars[step]})"></span>`;
      body += `<td class="cell${g?' grp':''}" data-i="${idx}" data-u="${m.name}">${fill}</td>`; });
    body += '</tr>';
    body += `<tr class="detail" id="d${idx}"><td colspan="${D.team.length+2}"></td></tr>`;
  });
  body+='</tbody>';
  document.getElementById('mx').innerHTML = head+body;
  bind(fs);
}

function bind(fs){
  const tip=document.getElementById('tip');
  document.querySelectorAll('td.cell').forEach(td=>{
    td.addEventListener('mousemove',e=>{
      const f=fs[+td.dataset.i], u=td.dataset.u, c=f.cells[u];
      if(!c.contacts.length){tip.style.display='none';return}
      tip.innerHTML = `<h4>${u} → ${f.name} <span style="color:var(--muted)">(${c.score})</span></h4>`+
        c.contacts.slice(0,8).map(k=>`<div class="c"><span class="${k.external?'ext':''}">${k.person}
          <span class="t" style="color:var(--muted)">· ${k.title}${k.external?' (adjacent)':''}</span></span>
          <span class="src">${k.sources.map(s=>SRC[s]||s).join(' · ')}</span></div>`).join('')+
        (c.contacts.length>8?`<div class="src">+${c.contacts.length-8} more…</div>`:'');
      tip.style.display='block';
      const w=tip.offsetWidth,h=tip.offsetHeight;
      tip.style.left=Math.min(innerWidth-w-12,e.clientX+14)+'px';
      tip.style.top=(e.clientY+16+h>innerHeight?e.clientY-h-10:e.clientY+16)+'px';
    });
    td.addEventListener('mouseleave',()=>tip.style.display='none');
  });
  document.querySelectorAll('.fname').forEach(el=>{
    el.addEventListener('click',()=>{
      const i=+el.dataset.i, f=fs[i], row=document.getElementById('d'+i);
      if(row.classList.contains('open')){row.classList.remove('open');return}
      document.querySelectorAll('.detail.open').forEach(r=>r.classList.remove('open'));
      const best = D.team.map(m=>({m,s:f.cells[m.name].score})).filter(x=>x.s>0).sort((a,b)=>b.s-a.s);
      let html = `<div class="scorebits">Relevance ${f.relevance.total}
        (stage ${f.relevance.stage} · sector ${f.relevance.sector} · activity ${f.relevance.activity} · graduation ${f.relevance.grad})
        &nbsp;·&nbsp; last investment ${f.last_investment||'—'} &nbsp;·&nbsp; ${fmt(f.num_investments)} investments · ${fmt(f.unicorns)} unicorns
        ${f.coinvest.length?` &nbsp;·&nbsp; <b style="color:var(--good-text)">co-invested:</b> ${f.coinvest.join(', ')}`:''}
        ${best.length?` &nbsp;·&nbsp; <b>door-opener: ${best[0].m.name}</b>`:''}</div>`;
      if(!best.length) html += '<div class="tm">No mapped relationships on the investment team.</div>';
      html += '<div class="cols">'+best.map(({m})=>{
        const c=f.cells[m.name];
        return `<div class="tm"><h5>${m.name} <span style="color:var(--muted)">(${c.score})</span></h5>`+
          c.contacts.map(k=>`<div>${k.person} <span class="t">· ${k.title}${k.external?' (adjacent)':''} · ${k.sources.map(s=>SRC[s]||s).join(' · ')}</span></div>`).join('')+`</div>`;
      }).join('')+'</div>';
      row.firstElementChild.innerHTML=html;
      row.classList.add('open');
    });
  });
}

document.querySelectorAll('.chipbtn').forEach(b=>b.addEventListener('click',()=>{
  b.classList.toggle('on');
  b.classList.contains('on')?state.cats.add(b.dataset.cat):state.cats.delete(b.dataset.cat);
  render();
}));
document.getElementById('sort').addEventListener('change',e=>{state.sort=e.target.value;render()});
document.getElementById('q').addEventListener('input',e=>{state.q=e.target.value.toLowerCase();render()});
tiles(); render();
</script>
"""

html = html.replace("__DATA__", DATA)
os.makedirs(f"{ROOT}/viz", exist_ok=True)
open(f"{ROOT}/viz/index.html", "w").write(html)
print(f"wrote viz/index.html ({len(html)//1024} KB), {len(funds)} funds, {len(TEAM_ORDER)} team columns")
gaps = [f["name"] for f in funds if f["relevance"]["total"] >= 60 and f["connectivity"] < 25 and f["category"] not in ("excluded", "angel")]
print("gap flags:", gaps)
top = sorted(included, key=lambda f: -f["connectivity"])[:8]
print("best covered:", [(f["name"], f["connectivity"]) for f in top])
