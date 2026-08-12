# Template for Germany Coverage Map v3 — Nordic app-frame design.
# Consumed by build_viz3.py; placeholder __DATA__ / __GENERATED__ substituted at build time.

TEMPLATE = r"""<title>Germany Coverage Map</title>
<style>
:root{
  color-scheme:light;
  --page:#f2f3f1; --surface:#fbfbfa; --raise:#ffffff;
  --ink:#17191a; --ink2:#55595c; --muted:#8b8f8a;
  --hair:#e2e4df; --hair2:#ecede9;
  --accent:#2a5fd0; --accent-ink:#1e4aa8; --accent-soft:#e8eefb;
  --covered:#1d7a38; --covered-ink:#135f2a;
  --thin:#c98a00; --thin-ink:#8a6100;
  --gap:#c03434; --gap-ink:#a92c2c;
  --c-prelead:#ecede9; --c-prelead-ink:#55595c;
  --c-reachout:#e3ebf7; --c-reachout-ink:#1e4aa8;
  --c-awaiting:#f6ecd2; --c-awaiting-ink:#8a6100;
  --c-lead:#e1efe3; --c-lead-ink:#135f2a;
  --c-hard:#f8e2df; --c-hard-ink:#a92c2c;
  --shadow:0 1px 2px rgba(18,20,22,.05), 0 12px 32px rgba(18,20,22,.06);
}
@media (prefers-color-scheme: dark){
  :root:where(:not([data-theme="light"])){
    color-scheme:dark;
    --page:#0f1110; --surface:#181a19; --raise:#1e201f;
    --ink:#f0f1ef; --ink2:#b3b6b1; --muted:#7f827d;
    --hair:#292b29; --hair2:#222423;
    --accent:#5b8ae6; --accent-ink:#8fb2f0; --accent-soft:#1b2options0;
    --accent-soft:#1c2740;
    --covered:#2f9a4d; --covered-ink:#54c274;
    --thin:#d9a13b; --thin-ink:#dfae57;
    --gap:#e05c5c; --gap-ink:#e87a7a;
    --c-prelead:#222423; --c-prelead-ink:#b3b6b1;
    --c-reachout:#1b2536; --c-reachout-ink:#8fb2f0;
    --c-awaiting:#2d2515; --c-awaiting-ink:#dfae57;
    --c-lead:#1a2a1d; --c-lead-ink:#54c274;
    --c-hard:#301c1a; --c-hard-ink:#e87a7a;
    --shadow:none;
  }
}
:root[data-theme="dark"]{
  color-scheme:dark;
  --page:#0f1110; --surface:#181a19; --raise:#1e201f;
  --ink:#f0f1ef; --ink2:#b3b6b1; --muted:#7f827d;
  --hair:#292b29; --hair2:#222423;
  --accent:#5b8ae6; --accent-ink:#8fb2f0; --accent-soft:#1c2740;
  --covered:#2f9a4d; --covered-ink:#54c274;
  --thin:#d9a13b; --thin-ink:#dfae57;
  --gap:#e05c5c; --gap-ink:#e87a7a;
  --c-prelead:#222423; --c-prelead-ink:#b3b6b1;
  --c-reachout:#1b2536; --c-reachout-ink:#8fb2f0;
  --c-awaiting:#2d2515; --c-awaiting-ink:#dfae57;
  --c-lead:#1a2a1d; --c-lead-ink:#54c274;
  --c-hard:#301c1a; --c-hard-ink:#e87a7a;
  --shadow:none;
}
*{box-sizing:border-box;margin:0}
html{scroll-behavior:smooth}
body{background:var(--page);color:var(--ink);
  font:14px/1.5 system-ui,-apple-system,"Segoe UI",sans-serif;padding-bottom:110px}
.appbar{position:sticky;top:0;z-index:20;background:var(--page);border-bottom:1px solid var(--hair)}
.appbar .in{max-width:1240px;margin:0 auto;display:flex;align-items:center;gap:16px;padding:14px 28px}
.brand{font-weight:650;font-size:15px;letter-spacing:-.01em;white-space:nowrap}
.brand small{color:var(--muted);font-weight:500;margin-left:8px;letter-spacing:.1em;text-transform:uppercase;font-size:10px}
.appbar input[type=search]{flex:0 1 260px;margin-left:auto;background:var(--surface);color:var(--ink);
  border:1px solid var(--hair);border-radius:8px;padding:7px 12px;font-size:13px}
.btn{background:var(--ink);color:var(--page);border:0;border-radius:8px;padding:8px 14px;font-size:12.5px;
  font-weight:600;cursor:pointer;white-space:nowrap}
.btn:hover{opacity:.88}
.wrap{max-width:1240px;margin:0 auto;padding:0 28px}
.hero{padding:44px 0 6px}
.kicker{font-size:10.5px;letter-spacing:.16em;text-transform:uppercase;color:var(--muted);margin-bottom:12px}
h1{font-size:34px;font-weight:650;letter-spacing:-.022em;text-wrap:balance}
.sub{color:var(--ink2);margin-top:12px;max-width:70ch;font-size:14.5px}
.score{display:flex;margin:34px 0 4px;border-top:1px solid var(--hair);border-bottom:1px solid var(--hair)}
.score .s{flex:1;padding:18px 22px 16px;border-left:1px solid var(--hair)}
.score .s:first-child{border-left:0;padding-left:2px}
.score b{display:block;font-size:30px;font-weight:650;font-variant-numeric:tabular-nums;letter-spacing:-.02em;line-height:1.1}
.score span{color:var(--muted);font-size:11px;text-transform:uppercase;letter-spacing:.1em}
.score .s.crit b{color:var(--gap-ink)} .score .s.warn b{color:var(--thin-ink)}
.sechead{margin:44px 0 4px;display:flex;align-items:baseline;gap:14px}
.sechead h2{font-size:13px;font-weight:650;text-transform:uppercase;letter-spacing:.12em}
.sechead p{font-size:12.5px;color:var(--muted)}
table{border-collapse:collapse;width:100%}
thead th{position:sticky;top:57px;z-index:5;background:var(--page);text-align:left;
  font-size:10.5px;text-transform:uppercase;letter-spacing:.1em;color:var(--muted);font-weight:600;
  padding:14px 12px 10px;border-bottom:1px solid var(--ink);cursor:pointer;user-select:none;white-space:nowrap}
thead th:hover{color:var(--ink)}
thead th.on{color:var(--ink)}
thead th.on::after{content:" ↓";color:var(--accent-ink)}
tbody td{padding:14px 12px;border-bottom:1px solid var(--hair);vertical-align:middle}
tbody tr.mainrow{cursor:pointer}
tbody tr.mainrow:hover td{background:var(--hair2)}
.fname{font-weight:620;font-size:14.5px;letter-spacing:-.005em;display:flex;align-items:center;gap:8px}
.fname .tdot{width:8px;height:8px;border-radius:50%;flex:none}
.fname.strong{color:var(--covered-ink)} .fname.strong .tdot{background:var(--covered)}
.fname.medium{color:var(--thin-ink)} .fname.medium .tdot{background:var(--thin)}
.fname.weak{color:var(--gap-ink)} .fname.weak .tdot{background:var(--gap)}
.fmeta{font-size:11.5px;color:var(--muted);margin-top:3px;padding-left:16px;display:flex;gap:8px;flex-wrap:wrap}
.badge{font-size:10px;border-radius:9px;padding:1px 7px;background:var(--hair2);color:var(--ink2);white-space:nowrap;letter-spacing:.03em}
.badge.co{color:var(--covered-ink);border:1px solid var(--covered);background:transparent}
.covcell{display:flex;align-items:center;gap:10px;font-variant-numeric:tabular-nums}
.covcell svg{flex:none}
.covcell b{font-size:16px;font-weight:650}
.relcell{font-variant-numeric:tabular-nums}
.relcell b{font-size:14.5px;font-weight:620}
.relcell .rb{display:block;width:64px;height:3px;background:var(--hair);border-radius:2px;margin-top:5px;overflow:hidden}
.relcell .rb i{display:block;height:100%;background:var(--ink2);border-radius:2px}
.chips{display:flex;gap:6px;flex-wrap:wrap;max-width:430px}
.chip{font-size:11.5px;border-radius:8px;padding:3px 9px;cursor:pointer;border:1px solid transparent;
  font-variant-numeric:tabular-nums;white-space:nowrap;font-weight:550}
.chip b{font-weight:650}
.chip.prelead{background:var(--c-prelead);color:var(--c-prelead-ink)}
.chip.reachout{background:var(--c-reachout);color:var(--c-reachout-ink)}
.chip.awaiting{background:var(--c-awaiting);color:var(--c-awaiting-ink)}
.chip.lead{background:var(--c-lead);color:var(--c-lead-ink)}
.chip.hard{background:var(--c-hard);color:var(--c-hard-ink)}
.chip:hover{border-color:currentColor}
.chip.empty{opacity:.32;cursor:default}
.chip.empty:hover{border-color:transparent}
.pts{font-size:12.5px;color:var(--ink2);display:flex;flex-direction:column;gap:3px;min-width:220px}
.pts .pt b{color:var(--ink);font-weight:570}
.pts .via{color:var(--muted)}
.pts a{color:var(--accent-ink);text-decoration:none}
.pts a:hover{text-decoration:underline}
.pts .pct{font-variant-numeric:tabular-nums;color:var(--covered-ink);font-weight:650;font-size:11.5px}
tr.detailrow{display:none}
tr.detailrow.open{display:table-row}
tr.detailrow>td{background:var(--surface);padding:20px 22px 24px;border-bottom:2px solid var(--ink)}
.detail h5{font-size:10.5px;text-transform:uppercase;letter-spacing:.11em;color:var(--muted);margin:16px 0 8px}
.detail h5:first-child{margin-top:0}
.meta-line{color:var(--muted);font-size:12.5px;margin-bottom:6px}
.plist{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:4px 26px}
.plist a{color:var(--accent-ink);text-decoration:none;font-weight:550}
.plist a:hover{text-decoration:underline}
.plist .st{display:inline-block;min-width:112px;margin-right:8px;font-size:11px;color:var(--muted)}
.tmcols{display:flex;gap:28px;flex-wrap:wrap}
.tmcols .tm{min-width:200px}
.tmcols h6{font-size:12.5px;color:var(--accent-ink);margin-bottom:5px}
.tmcols div{font-size:12px;color:var(--ink2);padding:1.5px 0}
.tmcols .t{color:var(--muted)}
.tmcols a{color:var(--accent-ink);text-decoration:none}
.note{font-size:12.5px;color:var(--muted);margin-top:48px;max-width:88ch;line-height:1.65;
  border-top:1px solid var(--hair);padding-top:18px}
.toast{position:fixed;bottom:24px;left:50%;transform:translateX(-50%);background:var(--ink);color:var(--page);
  border-radius:8px;padding:10px 18px;font-size:13px;display:none;z-index:40}
@media (max-width:900px){ .chips{max-width:none} thead{display:none}
  tbody tr.mainrow{display:grid;grid-template-columns:1fr auto;padding:10px 0}
  tbody td{border:0;padding:6px 10px} tbody tr.mainrow{border-bottom:1px solid var(--hair)} }
</style>

<div class="appbar"><div class="in">
  <span class="brand">Coverage<small>Germany</small></span>
  <input type="search" id="q" placeholder="Filter funds & angels…">
  <button class="btn" id="export" hidden>Export CSV</button>
</div></div>

<div class="wrap">
<div class="hero">
  <div class="kicker">Highland Europe · relationship intelligence · __GENERATED__</div>
  <h1>Who covers the German ecosystem — and&nbsp;who&nbsp;doesn't</h1>
  <p class="sub">The 31 funds that matter most plus nine super-angels. Coverage blends the team's Harmonic
  network with Affinity relationships across the whole partnership. Names are coloured by coverage —
  <b style="color:var(--covered-ink)">covered</b>, <b style="color:var(--thin-ink)">thin</b>,
  <b style="color:var(--gap-ink)">gap</b>. Funnel chips show where each investor's portfolio sits in our
  pipeline; click a row for the full dossier.</p>
</div>

<div class="score" id="score"></div>

<div class="sechead"><h2>Funds</h2><p>click column headers to sort · click a row for detail</p></div>
<table id="fundtable"></table>

<div class="sechead"><h2>Super-angels</h2><p>coverage is Affinity-led — Harmonic barely sees angels</p></div>
<table id="angeltable"></table>

<p class="note"><b>Method.</b> Universe: top 30 of the 74-investor Harmonic saved search by
½·investments + ½·unicorns (normalised), plus Alstin (added manually) and nine angels resolved in
Harmonic. Relevance = stage fit 30 · sector fit 30 · activity 20 · graduation 20. Coverage = 55%
Harmonic team-network (contact seniority × email/calendar evidence) + 45% Affinity partnership
relationships (incl. Laurence, Fergal, Ronan). Pipeline chips = companies in the Highland Companies
list whose investor set includes the fund or its vehicles; Lead includes Qualified Lead and Deal;
passed/deprioritised sit in the drill-down only. Percentages are Affinity interaction scores; names
link to LinkedIn, companies to Affinity. Angel pipeline matching includes known vehicles
(Companion-M, Interface Capital, MH2) — Affinity's investor enrichment still under-captures angel
tickets, so treat angel overlap as a floor.</p>
</div>
<div class="toast" id="toast"></div>

<script>
const D = __DATA__;
const BUCKETS = [["prelead","Pre-lead"],["reachout","Reach out"],["awaiting","Awaiting"],["lead","Lead"],["hard","Hard to crack"]];
const state = {sort:"gap", q:""};
const affURL = id => `https://${D.affinityOrg}.affinity.co/companies/${id}`;
const pipeCount = e => BUCKETS.reduce((m,[k])=>m+e.buckets[k].length,0);
const TIER = {strong:"var(--covered)", medium:"var(--thin)", weak:"var(--gap)"};

function ring(v, tier){
  const r=13, c=2*Math.PI*r, o=c*(1-v/100);
  return `<svg width="32" height="32" viewBox="0 0 32 32" role="img" aria-label="coverage ${v}">
    <circle cx="16" cy="16" r="${r}" fill="none" stroke="var(--hair)" stroke-width="4"/>
    <circle cx="16" cy="16" r="${r}" fill="none" stroke="${TIER[tier]}" stroke-width="4"
      stroke-dasharray="${c.toFixed(1)}" stroke-dashoffset="${o.toFixed(1)}"
      stroke-linecap="round" transform="rotate(-90 16 16)"/></svg>`;
}

function scoreboard(){
  const f = D.entities.filter(e=>e.kind==='fund');
  const gaps = f.filter(e=>e.tier==='weak' && e.relevance.total>=60);
  const live = D.entities.reduce((n,e)=>n+pipeCount(e),0);
  const hard = D.entities.reduce((n,e)=>n+e.buckets.hard.length,0);
  const co = f.filter(e=>e.coinvest.length).length;
  document.getElementById('score').innerHTML = `
    <div class="s"><b>${f.length}+${D.entities.length-f.length}</b><span>funds + angels</span></div>
    <div class="s"><b>${co}</b><span>co-invested with</span></div>
    <div class="s"><b>${live}</b><span>live pipeline overlaps</span></div>
    <div class="s warn"><b>${hard}</b><span>hard-to-cracks reachable</span></div>
    <div class="s crit"><b>${gaps.length}</b><span>relevant funds uncovered</span></div>`;
}

const COLS = [
  {k:"name", label:"Investor", sort:(a,b)=>a.name.localeCompare(b.name)},
  {k:"connectivity", label:"Coverage", sort:(a,b)=>b.connectivity-a.connectivity},
  {k:"relevance", label:"Relevance", sort:(a,b)=>(b.relevance?.total||0)-(a.relevance?.total||0)},
  {k:"pipeline", label:"Pipeline overlap", sort:(a,b)=>pipeCount(b)-pipeCount(a)},
  {k:"gap", label:"Strongest paths in", sort:(a,b)=>(b.gap||0)-(a.gap||0)||(b.relevance?.total||0)-(a.relevance?.total||0)},
];
function headHTML(){
  return `<thead><tr>`+COLS.map(c=>`<th data-k="${c.k}" class="${state.sort===c.k?'on':''}">${c.label}</th>`).join('')+`</tr></thead>`;
}
function chipHTML(e){
  return BUCKETS.map(([k,label])=>{
    const n = e.buckets[k].length;
    return `<span class="chip ${k}${n?'':' empty'}" data-k="${k}"><b>${n}</b> ${label}</span>`;
  }).join('');
}
function ptsHTML(e){
  if(!e.points.length) return `<div class="pts"><span style="color:var(--muted)">No mapped way in yet</span></div>`;
  return `<div class="pts">`+e.points.map(p=>{
    const nm = p.linkedin?`<a href="${p.linkedin}" target="_blank" rel="noopener"><b>${p.external}</b></a>`:`<b>${p.external}</b>`;
    const pct = p.pct!=null?` <span class="pct">${p.pct}%</span>`:'';
    return `<span class="pt">${nm} <span class="via">↔ ${p.internal}</span>${pct}</span>`;
  }).join('')+`</div>`;
}
function rowHTML(e){
  const rel = e.relevance? e.relevance.total : null;
  const co = e.coinvest.length?`<span class="badge co">✓ co-invested ×${e.coinvest.length}</span>`:'';
  const meta = e.kind==='fund'
    ? `<span class="badge">${e.category.toUpperCase()}</span><span>${e.city||''}</span>${co}`
    : `<span>${e.note||''}</span>`;
  const relCell = e.kind==='fund'
    ? `<b>${rel}</b><span class="rb"><i style="width:${rel}%"></i></span>`
    : `<span style="color:var(--muted);font-size:12px">${e.num_investments!=null? e.num_investments+' tracked deals':'—'}</span>`;
  return `<tr class="mainrow" data-slug="${e.slug}">
    <td><div class="fname ${e.tier}"><span class="tdot"></span>${e.name}</div><div class="fmeta">${meta}</div></td>
    <td><div class="covcell">${ring(e.connectivity, e.tier)}<b>${e.connectivity}</b></div></td>
    <td class="relcell">${relCell}</td>
    <td><div class="chips">${chipHTML(e)}</div></td>
    <td>${ptsHTML(e)}</td>
  </tr>
  <tr class="detailrow" id="d-${e.slug}"><td colspan="5"><div class="detail"></div></td></tr>`;
}
function detailHTML(e){
  let h='';
  if(e.kind==='fund'){
    const r=e.relevance;
    h += `<div class="meta-line">Relevance ${r.total} (stage ${r.stage} · sector ${r.sector} · activity ${r.activity} · graduation ${r.grad})
      · ${e.num_investments??'—'} investments · ${e.unicorns??0} unicorns · last investment ${e.last_investment||'—'}
      ${e.coinvest.length?` · <b style="color:var(--covered-ink)">co-invested:</b> ${e.coinvest.join(', ')}`:''}</div>`;
  }
  const secs = [...BUCKETS,["portfolio","Portfolio company"],["closed","Passed / deprioritised"]];
  let any=false;
  for(const [k,label] of secs){
    const list=e.buckets[k]; if(!list||!list.length) continue; any=true;
    h += `<h5 id="sec-${e.slug}-${k}">${label} (${list.length})</h5><div class="plist">`+
      list.map(p=>`<span><span class="st">${(p.funnel||'—').replace(' (free for all)','')}</span><a href="${affURL(p.id)}" target="_blank" rel="noopener">${p.name}</a> <span style="color:var(--muted)">${p.domain||''}</span></span>`).join('')+`</div>`;
  }
  if(!any) h += `<h5>Pipeline overlap</h5><div class="meta-line">None of their portfolio is in our pipeline list.</div>`;
  if(e.cells){
    const best = D.team.map(m=>({m,c:e.cells[m.name]})).filter(x=>x.c.score>0).sort((a,b)=>b.c.score-a.c.score);
    if(best.length){
      h += `<h5>Harmonic network, by team member</h5><div class="tmcols">`+best.map(({m,c})=>
        `<div class="tm"><h6>${m.name} <span style="color:var(--muted)">(${c.score})</span></h6>`+
        c.contacts.map(k=>{
          const nm = k.linkedin?`<a href="${k.linkedin}" target="_blank" rel="noopener">${k.person}</a>`:k.person;
          return `<div>${nm} <span class="t">· ${k.title}${k.external?' (adjacent)':''} · ${(k.sources||[]).map(s=>({LINKEDIN:'LI',EMAIL:'Email',CALENDAR:'Cal'})[s]||s).join(' · ')}</span></div>`;
        }).join('')+`</div>`).join('')+`</div>`;
    }
  }
  return h;
}
function bindTable(tbl){
  tbl.querySelectorAll('thead th').forEach(th=>th.addEventListener('click',()=>{
    state.sort = th.dataset.k; render();
  }));
  tbl.querySelectorAll('tr.mainrow').forEach(r=>r.addEventListener('click',ev=>{
    if(ev.target.closest('a')) return;
    const slug=r.dataset.slug, e=D.entities.find(x=>x.slug===slug);
    const det=document.getElementById('d-'+slug);
    const chip=ev.target.closest('.chip');
    if(!det.classList.contains('open')){ det.querySelector('.detail').innerHTML=detailHTML(e); det.classList.add('open'); }
    else if(!chip){ det.classList.remove('open'); return; }
    if(chip && !chip.classList.contains('empty')){
      const sec=document.getElementById(`sec-${slug}-${chip.dataset.k}`);
      if(sec) sec.scrollIntoView({behavior:'smooth', block:'center'});
    }
  }));
}
function render(){
  const q=state.q;
  const col = COLS.find(c=>c.k===state.sort)||COLS[4];
  const vis = D.entities.filter(e=>!q||e.name.toLowerCase().includes(q));
  const ft=document.getElementById('fundtable'), at=document.getElementById('angeltable');
  ft.innerHTML = headHTML()+`<tbody>`+vis.filter(e=>e.kind==='fund').sort(col.sort).map(rowHTML).join('')+`</tbody>`;
  at.innerHTML = headHTML()+`<tbody>`+vis.filter(e=>e.kind==='angel').sort(col.sort).map(rowHTML).join('')+`</tbody>`;
  bindTable(ft); bindTable(at);
}
document.getElementById('q').addEventListener('input',e=>{state.q=e.target.value.toLowerCase();render()});

// CSV export via downloads capability
function csv(){
  const rows=[["name","kind","category","city","relevance","coverage","tier","gap","coinvested",
    ...BUCKETS.map(([k])=>k),"top_path_external","top_path_internal","top_path_pct"]];
  for(const e of D.entities){
    const p=e.points[0]||{};
    rows.push([e.name,e.kind,e.category||'',e.city||'',e.relevance?e.relevance.total:'',e.connectivity,e.tier,e.gap??'',
      e.coinvest.join('; '),...BUCKETS.map(([k])=>e.buckets[k].length),p.external||'',p.internal||'',p.pct??'']);
  }
  return rows.map(r=>r.map(v=>`"${String(v).replaceAll('"','""')}"`).join(',')).join('\n');
}
function toast(msg){const t=document.getElementById('toast');t.textContent=msg;t.style.display='block';setTimeout(()=>t.style.display='none',2600)}
if (window.claude && window.claude.downloads){
  const btn=document.getElementById('export'); btn.hidden=false;
  btn.addEventListener('click', async ()=>{
    const data=csv();
    try{ await window.claude.downloads.save({filename:"germany-coverage.csv", data}); toast("Saved"); }
    catch(err){
      if(err && err.code==='extension_not_enabled'){
        try{ await window.claude.downloads.save({filename:"germany-coverage.txt", data}); toast("Saved as .txt"); }
        catch(e2){ if(e2&&e2.code!=='declined') toast("Export unavailable"); }
      } else if(err && err.code==='rate_limited'){ toast("Try again in a moment");
      } else if(err && err.code!=='declined'){ toast("Export unavailable"); }
    }
  });
}
scoreboard(); render();
</script>
"""
