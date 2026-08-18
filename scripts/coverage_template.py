# Multi-region coverage map template v5. Consumed by build_coverage.py.

TEMPLATE = r"""<title>Sonar</title>
<meta name="viewport" content="width=device-width,initial-scale=1">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@500;600&display=swap" rel="stylesheet">
<style>
:root{
  color-scheme:only light;
  --page:#f1eee6; --surface:#f7f5ee; --raise:#fcfbf6;
  --ink:#161619; --ink2:#54544f; --muted:#8f8c81;
  --hair:#dedacb; --hair2:#e9e5d9;
  --accent:#2733f0; --accent-ink:#1f28c4; --accent-soft:#e4e6fb;
  --covered:#1e6b47; --covered-ink:#155234;
  --thin:#b3801c; --thin-ink:#8a6100;
  --gap:#a8402f; --gap-ink:#933527;
  --c-prelead:#e9e5d9; --c-prelead-ink:#54544f;
  --c-reachout:#e4e6fb; --c-reachout-ink:#1f28c4;
  --c-awaiting:#f4ecd4; --c-awaiting-ink:#8a6100;
  --c-lead:#e2ede4; --c-lead-ink:#155234;
  --c-hard:#f6e3dd; --c-hard-ink:#933527;
  --shadow:0 1px 2px rgba(22,22,25,.05), 0 12px 32px rgba(22,22,25,.06);
  --display:"Poppins",system-ui,-apple-system,sans-serif;
}
*{box-sizing:border-box;margin:0}
html{scroll-behavior:smooth}
body{background:var(--page);color:var(--ink);
  font:14px/1.5 system-ui,-apple-system,"Segoe UI",sans-serif;padding-bottom:110px}
.appbar{position:sticky;top:0;z-index:20;background:var(--page);border-bottom:1px solid var(--hair)}
.appbar .in{max-width:1240px;margin:0 auto;display:flex;align-items:center;gap:14px;padding:12px 28px;flex-wrap:wrap}
.brand{font-weight:600;font-size:16px;letter-spacing:-.005em;white-space:nowrap;font-family:var(--display);
  display:flex;align-items:center;gap:8px}
.brand .mark{width:22px;height:22px;border-radius:4px;background:var(--accent);color:#fff;flex:none;
  display:inline-flex;align-items:center;justify-content:center;font-size:12.5px;font-weight:600}
.brand .by{font-family:system-ui,sans-serif;font-size:9.5px;color:var(--muted);letter-spacing:.14em;
  text-transform:uppercase;display:block;line-height:1;margin-top:1px}
.seg{display:flex;border:1px solid var(--hair);border-radius:8px;overflow:hidden}
.seg button{background:var(--surface);color:var(--ink2);border:0;padding:7px 14px;font-size:13px;cursor:pointer;font-weight:550}
.seg button.on{background:var(--ink);color:var(--surface)}
.appbar select{background:var(--surface);color:var(--ink);border:1px solid var(--hair);border-radius:8px;padding:7px 10px;font-size:13px;max-width:180px}
.appbar input[type=search]{flex:1 1 110px;min-width:100px;max-width:220px;margin-left:auto;
  background:var(--surface);color:var(--ink);
  border:1px solid var(--hair);border-radius:8px;padding:7px 12px;font-size:13px}
.btn{background:var(--ink);color:var(--page);border:0;border-radius:8px;padding:8px 14px;font-size:12.5px;
  font-weight:600;cursor:pointer;white-space:nowrap}
.btn:hover{opacity:.88}
.btn.ghost{background:var(--surface);color:var(--ink2);border:1px solid var(--hair)}
.btn.ghost:hover{border-color:var(--accent);color:var(--accent-ink);opacity:1}
#fbpop{position:fixed;top:64px;right:24px;z-index:70;max-width:320px;background:var(--raise);
  border:1px solid var(--hair);border-radius:12px;box-shadow:var(--shadow);padding:16px 18px;font-size:12.5px;
  color:var(--ink2);line-height:1.55}
#fbpop .th{font-size:9.5px;letter-spacing:.13em;text-transform:uppercase;color:var(--muted);font-weight:700;margin-bottom:7px}
#fbpop p{margin-bottom:9px}
#fbpop b{color:var(--ink)}
#fbpop a{color:var(--accent-ink)}
@media (max-width:700px){ #fbpop{left:14px;right:14px;max-width:none;top:110px} .btn.ghost{padding:5px 10px;font-size:11.5px} }
.wrap{max-width:1240px;margin:0 auto;padding:0 28px}
.hero{padding:38px 0 4px}
.kicker{font-size:10.5px;letter-spacing:.16em;text-transform:uppercase;color:var(--muted);margin-bottom:12px}
h1{font-size:33px;font-weight:600;letter-spacing:-.015em;text-wrap:balance;font-family:var(--display)}
.sub{color:var(--ink2);margin-top:10px;font-size:14px}
.score{display:flex;margin:28px 0 4px;border-top:1px solid var(--hair);border-bottom:1px solid var(--hair)}
.score .s{flex:1;padding:16px 20px 14px;border-left:1px solid var(--hair)}
.score .s:first-child{border-left:0;padding-left:2px}
.score b{display:block;font-size:28px;font-weight:650;font-variant-numeric:tabular-nums;letter-spacing:-.02em;line-height:1.1}
.score span{color:var(--muted);font-size:10.5px;text-transform:uppercase;letter-spacing:.1em}
.score .s.crit b{color:var(--gap-ink)} .score .s.warn b{color:var(--thin-ink)}
.filters{display:flex;gap:8px;align-items:center;flex-wrap:wrap;margin:14px 0 4px;font-size:12px}
.fchip{border:1px solid var(--hair);background:var(--surface);color:var(--ink2);border-radius:14px;
  padding:4px 12px;font-size:12px;cursor:pointer;font-weight:550}
.fchip.on{background:var(--accent-soft);border-color:var(--accent);color:var(--accent-ink)}
.filters .lbl{color:var(--muted);text-transform:uppercase;letter-spacing:.08em;font-size:10px;margin-left:6px}
.sechead{margin:40px 0 4px;display:flex;align-items:baseline;gap:14px}
.sechead h2{font-size:13px;font-weight:650;text-transform:uppercase;letter-spacing:.12em}
.sechead p{font-size:12.5px;color:var(--muted)}
table{border-collapse:collapse;width:100%}
thead th{position:sticky;top:53px;z-index:5;background:var(--page);text-align:left;
  font-size:10.5px;text-transform:uppercase;letter-spacing:.1em;color:var(--muted);font-weight:600;
  padding:14px 12px 10px;border-bottom:1px solid var(--ink);white-space:nowrap}
thead th.sortable{cursor:pointer;user-select:none}
thead th.sortable:hover{color:var(--ink)}
thead th.on{color:var(--ink)} thead th.on::after{content:" ↓";color:var(--accent-ink)}
tbody td{padding:13px 12px;border-bottom:1px solid var(--hair);vertical-align:middle}
tbody tr.mainrow{cursor:pointer}
tbody tr.mainrow:hover td{background:var(--hair2)}
tbody tr.mainrow:focus-visible{outline:2px solid var(--accent);outline-offset:-2px}
.fname{font-weight:620;font-size:14.5px;letter-spacing:-.005em;display:flex;align-items:center;gap:8px}
.fname .tdot{width:8px;height:8px;border-radius:50%;flex:none}
.fname a{color:inherit;text-decoration:none}
.fname a:hover{text-decoration:underline}
.fname.strong{color:var(--covered-ink)} .fname.strong .tdot{background:var(--covered)}
.fname.medium{color:var(--thin-ink)} .fname.medium .tdot{background:var(--thin)}
.fname.weak{color:var(--gap-ink)} .fname.weak .tdot{background:var(--gap)}
.fmeta{font-size:11.5px;color:var(--muted);margin-top:3px;padding-left:16px;display:flex;gap:8px;flex-wrap:wrap}
.badge{font-size:10px;border-radius:9px;padding:1px 7px;background:var(--hair2);color:var(--ink2);white-space:nowrap;letter-spacing:.03em}
.badge.co{color:var(--covered-ink);border:1px solid var(--covered);background:transparent}
.badge.unt{color:var(--accent-ink);border:1px solid var(--accent);background:transparent}
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
.chip .of{font-weight:400;opacity:.65;font-size:10.5px}
.chip.dim{opacity:.45}
.covcell .teamcov{color:var(--muted);font-size:10.5px;white-space:nowrap}
.pts{font-size:12.5px;color:var(--ink2);display:flex;flex-direction:column;gap:3px;min-width:220px}
.pts .pt b{color:var(--ink);font-weight:570}
.pts .via{color:var(--muted)}
.pts a{color:var(--accent-ink);text-decoration:none}
.pts a:hover{text-decoration:underline}
.pts .when{color:var(--muted);font-size:11px;font-variant-numeric:tabular-nums}
.pts .pt.stale{opacity:.55}
.pts .pt.stale .when{color:var(--thin-ink)}
.pts .dorm{color:var(--thin-ink)} .pts .dorm b{color:var(--thin-ink)}
.pts .askx{color:var(--muted);font-style:italic}
.pts .askx b{color:var(--ink2)}
.pts .pct{font-variant-numeric:tabular-nums;color:var(--covered-ink);font-weight:650;font-size:11.5px}
.flag{color:var(--gap-ink);font-size:10.5px;cursor:help}
.em{font-size:11px;opacity:.55;margin-left:2px;cursor:pointer;user-select:none}
.em:hover{opacity:1}
.em.guess{color:var(--thin-ink);position:relative}
.em.guess::after{content:'?';font-size:8px;vertical-align:super;margin-left:1px}
.pct{cursor:help}
#tip{position:fixed;z-index:99;max-width:290px;background:var(--raise);border:1px solid var(--hair);
  border-radius:10px;box-shadow:var(--shadow);padding:10px 13px;font-size:12px;line-height:1.5;color:var(--ink2);
  pointer-events:none;opacity:0;visibility:hidden;transition:opacity .12s}
#tip.show{opacity:1;visibility:visible}
#tip .th{font-size:9.5px;letter-spacing:.13em;text-transform:uppercase;color:var(--muted);font-weight:700;margin-bottom:5px}
#tip .th.warn{color:var(--gap-ink)}
#tip b{color:var(--ink);font-weight:620}
#tip .tf{margin-top:7px;padding-top:6px;border-top:1px solid var(--hair2);font-size:10.5px;color:var(--muted)}
tr.detailrow{display:none}
tr.detailrow.open{display:table-row}
tr.detailrow>td{background:var(--surface);padding:20px 22px 24px;border-bottom:2px solid var(--ink)}
.detail h5{font-size:10.5px;text-transform:uppercase;letter-spacing:.11em;color:var(--muted);margin:16px 0 8px}
.detail h5:first-child{margin-top:0}
.detail details.sec{border-top:1px solid var(--hair)}
.detail details.sec summary{cursor:pointer;list-style:none;display:flex;align-items:baseline;gap:8px;
  font-size:10.5px;font-weight:700;text-transform:uppercase;letter-spacing:.11em;color:var(--ink2);padding:9px 0}
.detail details.sec summary::-webkit-details-marker{display:none}
.detail details.sec summary::before{content:'▸';color:var(--muted);font-size:11px}
.detail details.sec[open] summary::before{content:'▾'}
.detail details.sec summary b{color:var(--ink);font-size:12px}
.detail details.sec summary .cnt{color:var(--muted);font-weight:400;text-transform:none;letter-spacing:0;font-size:11.5px}
.detail details.sec .plist{padding:2px 0 12px}
.detail details.dfsec{background:var(--accent-soft);border-top:0;border-radius:9px;padding:0 13px;margin:12px 0 6px}
.detail details.dfsec summary{color:var(--accent-ink)}
.detail details.dfsec summary::before{color:var(--accent-ink)}
.detail details.dfsec summary b{color:var(--accent-ink)}
.detail details.dfsec summary .cnt{color:var(--accent-ink);opacity:.7}
.detail details.dfsec + details.sec{border-top:0}
table.df thead th{border-bottom-color:rgba(31,40,196,.18)}
table.df td{border-bottom-color:rgba(31,40,196,.1)}
.dfwrap{overflow-x:auto;padding:2px 0 12px}
table.df{width:100%;border-collapse:collapse;font-size:12px}
table.df thead th{position:static;padding:5px 10px 5px 0;border-bottom:1px solid var(--hair);
  font-size:9.5px;letter-spacing:.1em;text-transform:uppercase;color:var(--muted);text-align:left;background:transparent}
table.df td{padding:5px 10px 5px 0;border-bottom:1px solid var(--hair2);white-space:nowrap}
table.df td a{color:var(--accent-ink);text-decoration:none;font-weight:550}
table.df td a:hover{text-decoration:underline}
table.df .num{font-variant-numeric:tabular-nums;color:var(--ink2)}
.dfst{font-size:10.5px;border-radius:8px;padding:2px 8px;white-space:nowrap;font-weight:550}
.dfst.in{background:var(--c-lead);color:var(--c-lead-ink) !important;text-decoration:none}
.dfst.out{background:var(--c-hard);color:var(--c-hard-ink)}
#filters select{background:var(--surface);color:var(--ink);border:1px solid var(--hair);border-radius:8px;
  padding:5px 8px;font-size:12.5px;color:var(--ink2)}
.meta-line{color:var(--muted);font-size:12.5px;margin-bottom:6px}
.plist{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:4px 26px}
.plist a{color:var(--accent-ink);text-decoration:none;font-weight:550}
.plist a:hover{text-decoration:underline}
.plist .st{display:inline-block;min-width:112px;margin-right:8px;font-size:11px;color:var(--muted)}
.plist .cc{color:var(--muted);font-size:10.5px}
.plist .offr{opacity:.5}
.pt.bridge{color:var(--ink2)}
.livebadge{color:var(--covered-ink);font-size:10px;font-weight:700;letter-spacing:.1em;text-transform:uppercase}
.fmeta .cc{color:var(--muted);font-size:11px}
.tmcols{display:flex;gap:28px;flex-wrap:wrap}
.tmcols .tm{min-width:200px}
.tmcols h6{font-size:12.5px;color:var(--accent-ink);margin-bottom:5px}
.tmcols div{font-size:12px;color:var(--ink2);padding:1.5px 0}
.tmcols .t{color:var(--muted)}
.tmcols a{color:var(--accent-ink);text-decoration:none}
.actionrow{margin-top:6px;display:flex;gap:10px}
.minibtn{border:1px solid var(--hair);background:var(--raise);color:var(--ink2);border-radius:7px;
  padding:4px 10px;font-size:11.5px;cursor:pointer;text-decoration:none;font-weight:550}
.minibtn:hover{border-color:var(--accent);color:var(--accent-ink)}
.note{font-size:12.5px;color:var(--muted);margin-top:48px;line-height:1.65;
  border-top:1px solid var(--hair);padding-top:18px}
.toast{position:fixed;bottom:24px;left:50%;transform:translateX(-50%);background:var(--ink);color:var(--page);
  border-radius:8px;padding:10px 18px;font-size:13px;display:none;z-index:40}
.htc-inv{display:flex;flex-direction:column;gap:2px;font-size:12px}
.htc-inv .nm{font-weight:570}
.htc-inv .nm.strong{color:var(--covered-ink)} .htc-inv .nm.medium{color:var(--thin-ink)} .htc-inv .nm.weak{color:var(--gap-ink)}
@media (max-width:900px){
  thead{display:none}
  tbody tr.mainrow{display:block;padding:12px 4px;border-bottom:1px solid var(--hair)}
  tbody tr.mainrow td{display:block;border:0;padding:4px 6px}
  tbody tr.mainrow td:nth-child(2){display:inline-block}
  tbody tr.mainrow td:nth-child(3){display:inline-block}
  .chips{max-width:none}
  .score{flex-wrap:wrap} .score .s{min-width:45%}
  .appbar input[type=search]{flex:1 1 100%;margin-left:0;order:9}
}
/* ---------- mobile experience (cards + dossier sheet) ---------- */
#mlist{display:none}
@media (max-width:700px){
  #fundsview table, #fundsview .sechead, #htcview table, #htcview .sechead{display:none}
  #mlist{display:block;padding-bottom:40px}
  .wrap{padding:0 14px}
  .hero{padding:20px 0 2px} h1{font-size:23px}
  .sub{font-size:13px}
  .appbar .in{padding:8px 14px 9px;gap:6px 8px}
  .brand{font-size:15px;margin-right:2px}
  .brand .by{display:none}
  .brand .mark{width:20px;height:20px;font-size:11.5px}
  .seg{border-radius:7px}
  .seg button{padding:5px 10px;font-size:12px}
  .appbar select{max-width:none;flex:1;padding:5px 8px;font-size:12px;color:var(--ink2)}
  #export{display:none}
  .appbar input[type=search]{flex:1 1 100%;margin-left:0;order:9;padding:6px 11px;font-size:12.5px;
    background:var(--hair2);border-color:transparent}
  .appbar input[type=search]:focus{background:var(--surface);border-color:var(--hair);outline:none}
  .kicker{font-size:9.5px;margin-bottom:8px}
  .score{display:flex;flex-wrap:nowrap;overflow-x:auto;gap:0;-webkit-overflow-scrolling:touch;scrollbar-width:none}
  .score::-webkit-scrollbar{display:none}
  .score .s{min-width:128px;flex:none;padding:12px 14px 10px}
  .score b{font-size:22px}
  .mhead{font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:.12em;color:var(--muted);margin:20px 0 8px}
  .mcard{background:var(--surface);border:1px solid var(--hair);border-radius:12px;padding:12px 14px;margin-bottom:10px;cursor:pointer}
  .mcard:active{background:var(--hair2)}
  .mtop{display:flex;align-items:center;gap:10px}
  .mtop .fname{flex:1;font-size:15px}
  .mcov{display:flex;align-items:center;gap:7px;font-variant-numeric:tabular-nums}
  .mcov b{font-size:15px;font-weight:650}
  .mcov .teamcov{color:var(--muted);font-size:10px}
  .mmeta{font-size:11px;color:var(--muted);margin:3px 0 7px;padding-left:18px;display:flex;gap:7px;flex-wrap:wrap}
  .mpath{font-size:12px;color:var(--ink2);padding-left:18px;margin-bottom:7px}
  .mpath b{color:var(--ink);font-weight:570}
  .mpath.dorm{color:var(--thin-ink)} .mpath.dorm b{color:var(--thin-ink)}
  .mchips{display:flex;gap:5px;flex-wrap:wrap;padding-left:18px}
  .mchips .chip{font-size:10.5px;padding:2px 7px;cursor:default}
  #sheet{position:fixed;inset:0;background:var(--page);z-index:60;overflow-y:auto;display:none;-webkit-overflow-scrolling:touch}
  #sheet.open{display:block}
  .sheethead{position:sticky;top:0;background:var(--page);border-bottom:1px solid var(--hair);
    display:flex;align-items:center;gap:10px;padding:13px 16px;z-index:5}
  .sheethead .fname{flex:1;font-size:16px;padding-right:52px} /* keep clear of the host viewer's floating button */
  .sheethead button{background:var(--surface);border:1px solid var(--hair);border-radius:8px;
    width:34px;height:34px;font-size:16px;color:var(--ink2);cursor:pointer;flex:none}
  .sheetstats{display:flex;gap:18px;padding:12px 16px;border-bottom:1px solid var(--hair);font-size:12px;color:var(--muted)}
  .sheetstats b{display:block;font-size:19px;color:var(--ink);font-variant-numeric:tabular-nums}
  .sheetbody{padding:14px 16px 60px}
  .sheetbody .plist{grid-template-columns:1fr}
  .sheetbody .tmcols{gap:16px}
  #tip{max-width:82vw}
}
</style>

<div class="appbar"><div class="in">
  <span class="brand"><span class="mark">S</span><span>Sonar<span class="by">Highland Europe</span></span></span>
  <div class="seg" id="regionseg"></div>
  <div class="seg" id="viewseg">
    <button data-v="funds" class="on">Investors</button><button data-v="htc">Hard to crack</button>
  </div>
  <select id="viewas" title="View coverage as"><option value="">Whole team</option></select>
  <input type="search" id="q" placeholder="Filter…">
  <button class="btn ghost" id="fb" title="Feedback & requests">💬 Feedback</button>
  <button class="btn" id="export" hidden>Export CSV</button>
  <div id="fbpop" hidden>
    <div class="th">Feedback &amp; requests</div>
    <p><b>Comment straight onto this page</b> — in the black claude.ai bar at the very top,
    tap the <b>speech-bubble icon</b> (next to your avatar), then tap or select anything on this
    page and write your note. Will &amp; Claude review every thread, and you'll get a reply on it
    when it ships.</p>
    <p>Prefer email? <a id="fbmail" href="mailto:william@highlandeurope.com?subject=Sonar%20feedback&body=What%20I%27d%20like%3A%0A%0AWhere%20(region%20%2F%20fund%20%2F%20view)%3A%0A">Send it to Will</a>.</p>
    <button class="minibtn" id="fbclose">Got it</button>
  </div>
</div></div>

<div class="wrap">
<div class="hero">
  <div class="kicker" id="kick">Highland Europe · relationship intelligence · __GENERATED__</div>
  <h1 id="pagetitle"></h1>
  <p class="sub"><span id="subcount"></span> Coverage blends the team's Harmonic network with Affinity
  relationships across the whole partnership, decayed by recency — a path untouched for over a year fades.
  Names are coloured by coverage: <b style="color:var(--covered-ink)">covered</b>,
  <b style="color:var(--thin-ink)">thin</b>, <b style="color:var(--gap-ink)">gap</b>.
  Click a fund row for the dossier; use <b>View as</b> to see it through one person's relationships.</p>
</div>

<div class="score" id="score"></div>

<div id="fundsview">
<div class="filters" id="filters"></div>
<div class="sechead"><h2>Funds</h2><p id="fundhint">sort via column headers · click a row for detail</p></div>
<table id="fundtable"></table>
<div class="sechead"><h2>Super-angels</h2><p>vital upstream nodes — ranked by their own relevance blend</p></div>
<table id="angeltable"></table>
</div>

<div id="htcview" style="display:none">
<div class="sechead"><h2>Hard to crack — reachable via mapped investors</h2><p id="htchint"></p></div>
<table id="htctable"></table>
</div>

<div id="mlist"></div>
<div id="sheet" role="dialog" aria-modal="true">
  <div class="sheethead"><button id="sheetclose" aria-label="Close">←</button><div class="fname" id="sheetname"></div></div>
  <div class="sheetstats" id="sheetstats"></div>
  <div class="sheetbody"><div class="detail" id="sheetdetail"></div></div>
</div>

<p class="note" id="method"><b>Method.</b> Relevance (funds) = stage fit 25 · sector fit 25 · Europe share 20 ·
activity 15 · graduation 15. Relevance (angels) = deal velocity + unicorns + syndication with covered funds +
presence on our pipeline cap tables. Coverage = 55% Harmonic team-network + 45% Affinity partnership
relationships (incl. Laurence, Fergal, Ronan), multiplied by a recency decay (≤6m ×1.0 · ≤1y ×0.9 · ≤2y ×0.5 ·
older ×0.3); dormant ties floor the score and show as ⏱ re-warmable paths. Pipeline chips = companies on the
Highland Companies list backed by the investor (Lead includes Qualified Lead and Deal; passed/deprioritised
excluded). “Untracked” = their post-Feb-2025 European deals absent from our pipeline list. ⚠ marks a contact
who appears to have left the fund. Percentages next to people are <b>Affinity relationship strength</b> (0–100%):
how warm that one-to-one connection is, driven by email &amp; meeting frequency and recency — 100% means an active
recent dialogue, 10% a thin or faded thread. It is not a probability or ownership figure. Hover any % for this
definition. For a full meeting brief, ask Claude: “prep my meeting with [fund]”.
<span id="fresh"></span></p>
</div>
<div class="toast" id="toast"></div>

<script>
const D = __DATA__;
const REGIONS = Object.keys(D.regions);
const BUCKETS = [["prelead","Pre-lead"],["reachout","Reach out"],["awaiting","Awaiting"],["lead","Lead"],["hard","Hard to crack"]];
const TIER = {strong:"var(--covered)", medium:"var(--thin)", weak:"var(--gap)"};
const state = {region: REGIONS[0], view:"funds", sort:"gap", q:"", person:"", cat:"", cc:""};
const E = () => D.regions[state.region].entities;
const affURL = id => `https://${D.affinityOrg}.affinity.co/companies/${id}`;
const isOwned = p => state.person && (p.own||[]).some(o=>o===state.person||o.startsWith(state.person.split(' ')[0]));
const bucketN = (e,k) => state.person ? e.buckets[k].filter(isOwned).length : e.buckets[k].length;
const pipeCount = e => BUCKETS.reduce((m,[k])=>m+bucketN(e,k),0);
const pipeCountTeam = e => BUCKETS.reduce((m,[k])=>m+e.buckets[k].length,0);
const fmtD = s => s ? new Date(s).toLocaleDateString('en-GB',{month:'short',year:'2-digit'}) : null;
const isStale = s => !s || (Date.now()-new Date(s).getTime()) > 365*864e5;

// ---------- personal mode ----------
function personSignal(e, name){
  const p = (e.top_people||[]).find(x=>x.name===name);
  const dorm = e.dormant && e.dormant.internal.includes(name) ? e.dormant : null;
  return {aff: p?p.aff:0, h: p?p.harmonic:0, contacts: p?p.contacts:[], dorm};
}
function personCov(e, name){
  const s = personSignal(e, name);
  let a = s.aff * (e.cov_parts ? e.cov_parts.decay : 1);
  if(s.dorm){ const age = 2026 - parseInt(s.dorm.last.slice(0,4));
    a = Math.max(a, age<=1?0.22:age<=3?0.15:age<=6?0.10:0.06); }
  const hn = Math.min(1, Math.sqrt(s.h)/Math.sqrt(30));
  return Math.round(100*(0.55*hn + 0.45*a));
}
function eff(e){
  if(!state.person) return {cov:e.connectivity, tier:e.tier, gap:e.gap, sig:null};
  const cov = personCov(e, state.person);
  const tier = cov>=50?'strong':cov>=22?'medium':'weak';
  const gap = Math.round((e.relevance?e.relevance.total:0)*(1-cov/100));
  return {cov, tier, gap, sig: personSignal(e, state.person)};
}

function ring(v, tier){
  const r=13, c=2*Math.PI*r, o=c*(1-v/100);
  return `<svg width="32" height="32" viewBox="0 0 32 32" role="img" aria-label="coverage ${v}">
    <circle cx="16" cy="16" r="${r}" fill="none" stroke="var(--hair)" stroke-width="4"/>
    <circle cx="16" cy="16" r="${r}" fill="none" stroke="${TIER[tier]}" stroke-width="4"
      stroke-dasharray="${c.toFixed(1)}" stroke-dashoffset="${o.toFixed(1)}"
      stroke-linecap="round" transform="rotate(-90 16 16)"/></svg>`;
}

function scoreboard(){
  const f = E().filter(e=>e.kind==='fund');
  const gaps = f.filter(e=>eff(e).tier==='weak' && e.relevance.total>=60);
  const live = E().reduce((n,e)=>n+pipeCount(e),0);
  const hard = D.regions[state.region].htc.length;
  const unt = f.reduce((n,e)=>n+((e.untracked||[]).length),0);
  document.getElementById('score').innerHTML = `
    <div class="s"><b>${f.length}+${E().length-f.length}</b><span>funds + angels</span></div>
    <div class="s"><b>${f.filter(e=>e.coinvest.length).length}</b><span>co-invested with</span></div>
    <div class="s"><b>${live}</b><span>${state.person?state.person.split(' ')[0]+"'s pipeline overlaps":'live pipeline overlaps'}</span></div>
    <div class="s warn"><b>${hard}</b><span>hard-to-cracks reachable</span></div>
    <div class="s warn"><b>${unt}</b><span>untracked recent EU deals</span></div>
    <div class="s crit"><b>${gaps.length}</b><span>${state.person?'uncovered by '+state.person.split(' ')[0]:'relevant funds uncovered'}</span></div>`;
}

// ---------- filters ----------
function filtersHTML(){
  const ccs = [...new Set(E().filter(e=>e.kind==='fund').map(e=>(e.city||'').split('·').pop().trim()).filter(Boolean))].sort();
  const cats = [...new Set(E().filter(e=>e.kind==='fund').map(e=>e.category))].sort();
  let h = `<span class="lbl">Type</span>`+cats.map(c=>`<button class="fchip${state.cat===c?' on':''}" data-cat="${c}">${c.toUpperCase()}</button>`).join('');
  if(ccs.length>1) h += `<span class="lbl">Country</span>`+ccs.map(c=>`<button class="fchip${state.cc===c?' on':''}" data-cc="${c}">${c}</button>`).join('');
  const SORTS=[["gap","Biggest gaps"],["connectivity","Coverage"],["relevance","Relevance"],["pipeline","Pipeline overlap"],["name","Name"]];
  h += `<span class="lbl">Sort</span><select id="sortsel">`+SORTS.map(([k,l])=>`<option value="${k}"${state.sort===k?' selected':''}>${l}</option>`).join('')+`</select>`;
  document.getElementById('filters').innerHTML = h;
  document.querySelectorAll('#filters .fchip').forEach(b=>b.addEventListener('click',()=>{
    if(b.dataset.cat!==undefined) state.cat = state.cat===b.dataset.cat?'':b.dataset.cat;
    if(b.dataset.cc!==undefined) state.cc = state.cc===b.dataset.cc?'':b.dataset.cc;
    render();
  }));
  document.getElementById('sortsel').addEventListener('change',ev=>{ state.sort=ev.target.value; render(); });
}

const COLS = [
  {k:"name", label:"Investor", sortable:true, sort:(a,b)=>a.name.localeCompare(b.name)},
  {k:"connectivity", label:"Coverage", sortable:true, sort:(a,b)=>eff(b).cov-eff(a).cov},
  {k:"relevance", label:"Relevance", sortable:true, sort:(a,b)=>(b.relevance?.total||0)-(a.relevance?.total||0)},
  {k:"pipeline", label:"Pipeline overlap", sortable:true, sort:(a,b)=>pipeCount(b)-pipeCount(a)},
  {k:"gap", label:"Strongest paths in", sortable:false, sort:(a,b)=>(eff(b).gap||0)-(eff(a).gap||0)||(b.relevance?.total||0)-(a.relevance?.total||0)},
];
function headHTML(){
  return `<thead><tr>`+COLS.map(c=>`<th data-k="${c.k}" class="${c.sortable?'sortable':''} ${state.sort===c.k?'on':''}">${c.label}</th>`).join('')+`</tr></thead>`;
}
function chipHTML(e){
  if(state.person){  // own count vs team count, side by side
    const chips = BUCKETS.map(([k,label])=>{
      const team = e.buckets[k].length; if(!team) return '';
      const own = e.buckets[k].filter(isOwned).length;
      return `<span class="chip ${k}${own?'':' dim'}" data-k="${k}"><b>${own}</b><span class="of">/${team}</span> ${label}</span>`;
    }).join('');
    return chips || `<span style="color:var(--muted);font-size:12px">no pipeline overlap</span>`;
  }
  return BUCKETS.map(([k,label])=>{
    const n = e.buckets[k].length;
    return n?`<span class="chip ${k}" data-k="${k}"><b>${n}</b> ${label}</span>`:'';
  }).join('') || `<span style="color:var(--muted);font-size:12px">no pipeline overlap</span>`;
}
const liSearch = (n,f) => `https://www.linkedin.com/search/results/people/?keywords=${encodeURIComponent(n+' '+(f||''))}`;
const emIcon = p => {
  const em = p.email || p.email_guess;
  if(!em) return '';
  return `<span class="em${p.email?'':' guess'}" data-em="${em}"${p.email?'':' data-guess="1"'}>✉</span>`;
};
function pathLine(p, ctx){
  const nm = `<a href="${p.linkedin||liSearch(p.external,ctx)}" target="_blank" rel="noopener"><b>${p.external}</b></a>`;
  const pct = (p.email?emIcon(p):'')+(p.pct!=null?` <span class="pct">${p.pct}%</span>`:'');
  const when = p.last?` <span class="when">· ${fmtD(p.last)}</span>`:'';
  const moved = p.moved?` <span class="flag" data-moved="${p.moved}">⚠</span>`:'';
  const stale = p.last && isStale(p.last) ? ' stale' : '';
  return `<span class="pt${stale}">${nm} <span class="via">↔ ${p.internal}</span>${pct}${when}${moved}</span>`;
}
function ptsHTML(e){
  const v = eff(e);
  if(state.person){
    const s = v.sig;
    const dormP = s.dorm ? `<span class="pt dorm" title="${s.dorm.context}">⏱ dormant · last touch ${s.dorm.last}</span>` : '';
    let mine = s.contacts.map(k=>{
      const nm = `<a href="${k.linkedin||liSearch(k.person,e.name)}" target="_blank" rel="noopener"><b>${k.person}</b></a>`;
      const extra = (k.email?emIcon(k):'')+(k.title?` <span class="via">· ${k.title}</span>`:'')+(k.pct!=null?` <span class="pct">${k.pct}%</span>`:'');
      const when = k.last?` <span class="when">· ${fmtD(k.last)}</span>`:'';
      return `<span class="pt${k.last&&isStale(k.last)?' stale':''}">${nm}${extra}${when}</span>`;
    }).join('')+dormP;
    if(!mine){
      const bits=[];
      const best = e.points && e.points[0];
      if(best) bits.push(`<span class="askx">ask <b>${best.internal}</b> (${best.external}${best.pct!=null?' · '+best.pct+'%':''})</span>`);
      if(!best && e.dormant) bits.push(`<span class="pt dorm" title="${e.dormant.context}">⏱ dormant — <b>${e.dormant.internal.join(' + ')}</b> <span class="via">· ${e.dormant.last}</span></span>`);
      if(!best) bits.push(...bridgeLines(e));
      mine = bits.join('') || `<span style="color:var(--muted)">no team path either</span>`;
    }
    return `<div class="pts">${mine}</div>`;
  }
  const dorm = e.dormant ? `<span class="pt dorm" title="${e.dormant.context}">⏱ <b>${e.dormant.internal.join(' + ')}</b> <span class="via">dormant · ${e.dormant.last}</span></span>` : '';
  const bridges = !e.points.length ? bridgeLines(e).join('') : '';
  if(!e.points.length && !dorm && !bridges) return `<div class="pts"><span style="color:var(--muted)">No mapped way in yet</span></div>`;
  return `<div class="pts">`+e.points.map(p=>pathLine(p,e.name)).join('')+dorm+bridges+`</div>`;
}
function bridgeLines(e){
  return (e.bridges||[]).slice(0,2).map(b=>
    `<span class="pt bridge">↪ via <b>${b.name}</b> <span class="via">(${b.internal}${b.pct!=null?' · '+b.pct+'%':''})</span></span>`);
}
function rowHTML(e){
  const v = eff(e);
  const rel = e.relevance? e.relevance.total : null;
  const co = e.coinvest.length?`<span class="badge co">✓ co-invested ×${e.coinvest.length}</span>`:'';
  const unt = (e.untracked||[]).length?`<span class="badge unt">${e.untracked.length} untracked EU deals</span>`:'';
  const lastT = e.fund_last?`<span>last touch ${fmtD(e.fund_last)}</span>`:'';
  const noCrm = e.no_crm?`<a class="badge" href="${e.harmonic_url}" target="_blank" rel="noopener">no CRM record · Harmonic ↗</a>`:'';
  const known = e.kind==='angel' && (e.notable||[]).length
    ? `<span class="cc">known for: ${e.notable.slice(0,3).map(n=>n.name).join(', ')}</span>` : '';
  const meta = e.kind==='fund'
    ? `<span class="badge">${e.category.toUpperCase()}</span><span>${e.city||''}</span>${lastT}${co}${unt}`
    : `<span>${e.note||''}</span>${known}${lastT}${noCrm}`;
  const nm = e.kind==='angel' && e.li ? `<a href="${e.li}" target="_blank" rel="noopener">${e.name}</a>`
    : e.website ? `<a href="https://${e.website}" target="_blank" rel="noopener">${e.name}</a>` : e.name;
  const relCell = `<b>${rel??'—'}</b><span class="rb"><i style="width:${rel||0}%"></i></span>`;
  return `<tr class="mainrow" data-slug="${e.slug}" tabindex="0">
    <td><div class="fname ${v.tier}"><span class="tdot"></span>${nm}</div><div class="fmeta">${meta}</div></td>
    <td class="covtd"><div class="covcell">${ring(v.cov, v.tier)}<b>${v.cov}</b>${state.person?`<span class="teamcov">team ${e.connectivity}</span>`:''}</div></td>
    <td class="relcell">${relCell}</td>
    <td><div class="chips">${chipHTML(e)}</div></td>
    <td>${ptsHTML(e)}</td>
  </tr>
  <tr class="detailrow" id="d-${e.slug}"><td colspan="5"><div class="detail"></div></td></tr>`;
}
function detailHTML(e){
  let h='';
  if(e.liveAt) h += `<div class="meta-line"><span class="livebadge">${liveLabel(e)}</span> <span class="cc">pipeline refreshed from your Affinity connector</span></div>`;
  if(e.kind==='fund'){
    const r=e.relevance;
    h += `<div class="meta-line">Relevance ${r.total} (stage ${r.stage} · sector ${r.sector} · Europe ${r.geo} at ${Math.round(r.europe)}% · activity ${r.activity} · graduation ${r.grad})
      · ${e.num_investments??'—'} investments · ${e.unicorns??0} unicorns · last investment ${e.last_investment||'—'}
      ${e.coinvest.length?` · <b style="color:var(--covered-ink)">co-invested:</b> ${e.coinvest.join(', ')}`:''}</div>`;
  } else if(e.relevance){
    const r=e.relevance;
    h += `<div class="meta-line">Angel relevance ${r.total} (deals ${r.deals} · outcomes ${r.uni} · syndication ${r.synd} · our-pipeline presence ${r.pipe}) · ${e.num_investments??'—'} tracked deals</div>`;
  }
  if(e.kind==='angel' && (e.notable||[]).length){
    h += `<h5>Why they're on the list — notable positions</h5><div class="plist">`+
      e.notable.map(n=>`<span>${n.harmonic_company_id?`<a href="https://console.harmonic.ai/dashboard/company/${n.harmonic_company_id}" target="_blank" rel="noopener">${n.name}</a>`:`<b>${n.name}</b>`} <span class="cc">${n.why||''}</span></span>`).join('')+`</div>`;
  }
  if((e.dealflow||[]).length){
    const money = v => v==null?'—':v>=995e6?('$'+(v/1e9).toFixed(1)+'B'):v>=1e6?('$'+Math.round(v/1e6)+'M'):('$'+Math.round(v/1e3)+'K');
    const unt = e.dealflow.filter(x=>!x.funnel).length;
    const eu = (e.untracked||[]).length;
    const untLbl = unt ? `${unt} not in our pipeline${eu&&eu!==unt?` (${eu} EU)`:''}` : '';
    h += `<details class="sec dfsec" id="sec-${e.slug}-df"><summary>Recent dealflow <b>${e.dealflow.length}</b>${untLbl?`<span class="cnt">${untLbl}</span>`:''}</summary>
      <div class="dfwrap"><table class="df"><thead><tr><th>Company</th><th>Round</th><th>Date</th><th>Size</th><th>Total raised</th><th>Valuation</th><th>Status</th></tr></thead><tbody>`+
      e.dealflow.map(x=>`<tr>
        <td><a href="https://console.harmonic.ai/dashboard/company/${x.harmonic_company_id}" target="_blank" rel="noopener">${x.name}</a> <span class="cc">${x.country||''}</span></td>
        <td><span class="st" style="min-width:0">${(x.round||'—').replaceAll('_',' ').toLowerCase()}</span></td>
        <td class="num">${(x.date||'').slice(0,7)}</td>
        <td class="num">${money(x.round_size_usd)}</td>
        <td class="num">${money(x.total_funding_usd)}</td>
        <td class="num">${money(x.valuation_usd)}${x.valuation_usd&&x.valuation_est?' <span class="cc">est.</span>':''}</td>
        <td>${x.funnel?`<a class="dfst in" href="${affURL(x.affinity_id)}" target="_blank" rel="noopener">${x.funnel.replace(' (free for all)','')}</a>`:`<span class="dfst out">not tracked</span>`}</td>
      </tr>`).join('')+`</tbody></table></div></details>`;
  } else if((e.untracked||[]).length){
    h += `<details class="sec"><summary>Recent EU deals we're not tracking <b>${e.untracked.length}</b>${e.recent_eu?`<span class="cnt">of ${e.recent_eu} recent EU deals</span>`:''}</summary><div class="plist">`+
      e.untracked.map(u=>`<span><span class="st">${(u.date||'').slice(0,7)} · ${(u.round||'').replaceAll('_',' ').toLowerCase()}</span><a href="https://console.harmonic.ai/dashboard/company/${u.harmonic_company_id}" target="_blank" rel="noopener">${u.name}</a> <span class="cc">${u.country||''}</span></span>`).join('')+`</div></details>`;
  }
  const secs = [...BUCKETS,["portfolio","Portfolio company"]];
  const isGlobal = (e.buckets.prelead.concat(e.buckets.lead)).some(p=>p.country!==undefined);
  const inRegion = p => !isGlobal || p.country===undefined || p.country===null || regionCountries().has(p.country);
  const pitem = (p,cls) => `<span${cls?` class="${cls}"`:''}><span class="st">${(p.funnel||'—').replace(' (free for all)','')}</span><a href="${affURL(p.id)}" target="_blank" rel="noopener">${p.name}</a>${(p.own||[]).length?` <span class="cc">${p.own.map(o=>o.split(' ')[0]).join(', ')}</span>`:''}</span>`;
  for(const [k,label] of secs){
    const list=e.buckets[k]; if(!list||!list.length) continue;
    if(state.person){
      const own = list.filter(isOwned), rest = list.filter(p=>!isOwned(p));
      h += `<details class="sec" id="sec-${e.slug}-${k}"><summary>${label} <b>${own.length}</b><span class="cnt">of ${list.length} team-wide owned by ${state.person.split(' ')[0]}</span></summary><div class="plist">`+
        own.map(p=>pitem(p,'')).join('')+rest.map(p=>pitem(p,'offr')).join('')+`</div></details>`;
      continue;
    }
    const inR = list.filter(inRegion), outR = list.filter(p=>!inRegion(p));
    h += `<details class="sec" id="sec-${e.slug}-${k}"><summary>${label} <b>${list.length}</b>${outR.length?`<span class="cnt">${inR.length} in region</span>`:''}</summary><div class="plist">`+
      inR.map(p=>pitem(p,'')).join('')+
      outR.map(p=>pitem(p,'offr')).join('')+`</div></details>`;
  }
  if(e.dormant){
    const mail = dormantMail(e);
    h += `<h5>Dormant tie</h5><div class="meta-line">⏱ ${e.dormant.internal.join(' + ')} — ${e.dormant.context} (last touch ${e.dormant.last}).</div>
      <div class="actionrow"><a class="minibtn" href="${mail}">✉ nudge ${e.dormant.internal[0].split(' ')[0]} to re-warm</a>
      <button class="minibtn" data-copy="${e.slug}">copy context</button></div>`;
  }
  if(e.bridges && e.bridges.length){
    h += `<h5>Routes in via covered co-investors</h5><div class="meta-line">`+
      e.bridges.map(b=>`via <b>${b.name}</b> (${b.internal}${b.pct!=null?' · '+b.pct+'%':''})`).join(' &nbsp;·&nbsp; ')+`</div>`;
  }
  if(e.syndication && e.syndication.length){
    h += `<h5>Syndicates most with</h5><div class="meta-line">`+
      e.syndication.map(s=>`<b>${s.name}</b>${s.tier==='strong'&&s.via?` (covered — ${s.via} can intro)`:''}`).join(' · ')+`</div>`;
  }
  if(e.top_people && e.top_people.length){
    const shown = state.person ? e.top_people.filter(p=>p.name===state.person).concat(e.top_people.filter(p=>p.name!==state.person).slice(0,3)) : e.top_people.slice(0,4);
    h += `<h5>Best Highland coverage${state.person?` — viewing as ${state.person}`:''}</h5><div class="tmcols">`+shown.map(p=>{
      const strength = p.aff>0 ? `${Math.round(p.aff*100)}%` : (p.harmonic>0 ? 'network only' : '');
      return `<div class="tm"><h6>${p.name} <span style="color:var(--muted)">${strength}</span></h6>`+
        p.contacts.map(k=>{
          const nm = `<a href="${k.linkedin||liSearch(k.person,e.name)}" target="_blank" rel="noopener">${k.person}</a>`;
          const bits = [k.title, k.pct!=null?`${k.pct}%`:null, k.last?fmtD(k.last):null].filter(Boolean).join(' · ');
          const moved = k.moved?` <span class="flag" data-moved="${k.moved}">⚠</span>`:'';
          return `<div>${nm}${k.email?emIcon(k):''}<span class="t">${bits?` · ${bits}`:''}</span>${moved}</div>`;
        }).join('')+`</div>`;
    }).join('')+`</div>`;
  }
  const liq = n => liSearch(n, e.name);
  if(e.partners_known && e.partners_known.length){
    h += `<h5>Their partners we already know</h5><div class="plist">`+
      e.partners_known.map(p=>`<span><a href="${p.linkedin||liq(p.name)}" target="_blank" rel="noopener">${p.name}</a>${emIcon(p)} <span class="via">↔ ${p.internal}</span>${p.score!=null?` <span class="pct">${Math.round(p.score*100)}%</span>`:''}${p.note?` <span class="cc">${p.note}</span>`:''}</span>`).join('')+`</div>`;
  }
  if(e.partners_unknown && e.partners_unknown.length){
    h += `<h5>Their partners we don't know${e.partners_total?` (${e.partners_unknown.length} of ${e.partners_total} on roster)`:''}</h5><div class="plist">`+
      e.partners_unknown.map(p=>`<span><a href="${p.linkedin||liq(p.name)}" target="_blank" rel="noopener">${p.name}</a>${emIcon(p)} <span class="cc">${p.title||''}</span></span>`).join('')+`</div>`;
  }
  h += `<div class="meta-line" style="margin-top:14px">Full brief: ask Claude — “prep my meeting with ${e.name}”.</div>`;
  return h;
}
function regionCountries(){
  if(state.region==='germany') return new Set(['Germany']);
  if(state.region==='france') return new Set(['France','Belgium','Luxembourg','Monaco']);
  return new Set(['Sweden','Denmark','Norway','Finland','Iceland']);
}
function dormantMail(e){
  const MAIL = {"Gaj Rajanathan":"gajan","Harry Williams":"harry","Sam Brooks":"sam","Ronan Shally":"ronan",
    "Fergal Mullen":"fergal","David Blyghton":"david","Helena Richardson":"helena","Laurence Garrett":"laurence",
    "Irena Goldenberg":"irena","Will de Quant":"william"};
  const d = e.dormant;
  const first = d.internal[0].split(' ')[0];
  const addr = (MAIL[d.internal[0]]||first.toLowerCase())+'@highlandeurope.com';
  const others = d.internal.slice(1).map(n=>n.split(' ')[0]);
  const yr = (d.last||'').slice(0,4);
  const who = others.length?`you and ${others.join(' and ')} were in touch with`:`you were in touch with`;
  const li = e.li?` (${e.li})`:'';
  const pipe = pipeCount(e);
  const fn = e.name.split(' ')[0];
  const kind = e.kind==='angel'?`${fn} is one of the more active angels on our ${D.regions[state.region].adj} coverage map`:`${e.name} is one of the more relevant funds on our ${D.regions[state.region].adj} coverage map`;
  const pipeBit = pipe?` — ${pipe} compan${pipe===1?'y':'ies'} on their cap tables overlap our pipeline —`:'';
  const sender = state.person?state.person.split(' ')[0]:'';
  const sub = encodeURIComponent(`${e.name} — worth re-warming?`);
  const body = encodeURIComponent(
`Hi ${first},

Quick one — ${who} ${e.name}${li} back in ${yr} as far as I can tell, but nothing since ${fmtD(d.last)||d.last}.

${kind}${pipeBit} and right now nobody at Highland has a live line in. Feels worth picking the thread back up — any appetite? Happy to run with it if you'd rather just make the intro.

${sender}`);
  return `mailto:${addr}?subject=${sub}&body=${body}`;
}

// ---------- HTC view ----------
function orderPaths(i){  // personal view: the viewer's own paths lead
  const ps = i.paths||[];
  return state.person ? [...ps].sort((a,b)=>(b.internal===state.person)-(a.internal===state.person)) : ps;
}
function htcHTML(){
  let rows = D.regions[state.region].htc;
  if(state.person) rows = rows.filter(c=>(c.owners||[]).some(o=>o===state.person || o.startsWith(state.person.split(' ')[0])));
  if(state.q) rows = rows.filter(c=>c.name.toLowerCase().includes(state.q));
  document.getElementById('htchint').textContent = state.person
    ? `companies owned by ${state.person} in Affinity, reachable via mapped investors`
    : `every hard-to-crack with a mapped investor on its cap table — sorted by reachability`;
  const body = rows.map(c=>`<tr>
    <td><div class="fname"><a href="${affURL(c.id)}" target="_blank" rel="noopener">${c.name}</a></div>
      <div class="fmeta"><span>${c.domain||''}</span><span>${c.country||''}</span></div></td>
    <td><div class="htc-inv">${c.investors.map(i=>`<span class="nm ${i.tier}">${i.name}</span>`).join('')}</div></td>
    <td><div class="htc-inv">${c.investors.map(i=>(i.paths&&i.paths.length)?`<span>${orderPaths(i).map(p=>`<b>${p.internal}</b>${p.external&&p.external!==i.name?` <span class="via">↔ ${p.external}</span>`:''}${p.email?emIcon(p):''}${p.pct!=null?` <span class="pct">${p.pct}%</span>`:''}${p.moved?` <span class="flag" data-moved="${p.moved}">⚠</span>`:''}`).join('<br>')}</span>`:`<span style="color:var(--muted)">—</span>`).join('')}</div></td>
    <td style="font-size:12px;color:var(--ink2)">${(c.owners||[]).join(', ')||'<span style="color:var(--muted)">unowned</span>'}</td>
  </tr>`).join('');
  document.getElementById('htctable').innerHTML =
    `<thead><tr><th>Company</th><th>On cap table</th><th>Our path via them</th><th>Affinity owner</th></tr></thead><tbody>${body||'<tr><td colspan="4" style="color:var(--muted)">Nothing matches.</td></tr>'}</tbody>`;
}

// ---------- mobile experience ----------
const isMobile = () => matchMedia('(max-width:700px)').matches;
function mPathLine(e){
  const v = eff(e);
  if(state.person){
    const k = v.sig.contacts[0];
    if(k) return `<div class="mpath"><b>${k.person}</b>${k.pct!=null?` <span class="pct">${k.pct}%</span>`:''}${k.last?` <span class="when">· ${fmtD(k.last)}</span>`:''}</div>`;
    const best = e.points && e.points[0];
    if(best) return `<div class="mpath askx">ask <b>${best.internal}</b> (${best.external})</div>`;
  }
  const p0 = e.points && e.points[0];
  if(p0) return `<div class="mpath"><b>${p0.external}</b>${p0.email?emIcon(p0):''} <span class="via">↔ ${p0.internal}</span>${p0.pct!=null?` <span class="pct">${p0.pct}%</span>`:''}${p0.moved?' <span class="flag">⚠</span>':''}</div>`;
  if(e.dormant) return `<div class="mpath dorm">⏱ <b>${e.dormant.internal.join(' + ')}</b> dormant · ${e.dormant.last}</div>`;
  if(e.bridges && e.bridges.length) return `<div class="mpath">↪ via <b>${e.bridges[0].name}</b> <span class="via">(${e.bridges[0].internal})</span></div>`;
  return `<div class="mpath" style="color:var(--muted)">No mapped way in yet</div>`;
}
function mCardHTML(e){
  const v = eff(e); const rel = e.relevance?e.relevance.total:null;
  const meta = e.kind==='fund'
    ? `<span class="badge">${e.category.toUpperCase()}</span><span>${(e.city||'').split('·')[0].trim()}</span>${rel!=null?`<span>rel ${rel}</span>`:''}${(e.untracked||[]).length?`<span class="badge unt">${e.untracked.length} untracked</span>`:''}`
    : `<span>${e.note||''}</span>${(e.notable||[]).length?`<span class="cc">known for: ${e.notable.slice(0,2).map(n=>n.name).join(', ')}</span>`:''}`;
  return `<div class="mcard" data-slug="${e.slug}" tabindex="0">
    <div class="mtop"><div class="fname ${v.tier}"><span class="tdot"></span>${e.name}</div>
      <div class="mcov">${ring(v.cov, v.tier)}<b>${v.cov}</b>${state.person?`<span class="teamcov">team ${e.connectivity}</span>`:''}</div></div>
    <div class="mmeta">${meta}</div>
    ${mPathLine(e)}
    <div class="mchips">${chipHTML(e)}</div>
  </div>`;
}
function mHtcCardHTML(c){
  const paths = c.investors.map(i=>(i.paths&&i.paths.length)
    ? orderPaths(i).slice(0,2).map(p=>`<div class="mpath"><b>${p.internal}</b>${p.external&&p.external!==i.name?` <span class="via">↔ ${p.external}</span>`:''}${p.email?emIcon(p):''}${p.pct!=null?` <span class="pct">${p.pct}%</span>`:''}</div>`).join('') : '').join('');
  return `<div class="mcard" onclick="window.open('${affURL(c.id)}','_blank')">
    <div class="mtop"><div class="fname">${c.name}</div><span class="cc">${c.country||''}</span></div>
    <div class="mmeta">on cap table: ${c.investors.map(i=>i.name).join(', ')}${(c.owners||[]).length?` · owner: ${c.owners.join(', ')}`:''}</div>
    ${paths||'<div class="mpath" style="color:var(--muted)">no mapped path yet</div>'}
  </div>`;
}
function renderMobile(){
  const el = document.getElementById('mlist');
  if(state.view==='htc'){
    let rows = D.regions[state.region].htc;
    if(state.person) rows = rows.filter(c=>(c.owners||[]).some(o=>o===state.person||o.startsWith(state.person.split(' ')[0])));
    if(state.q) rows = rows.filter(c=>c.name.toLowerCase().includes(state.q));
    el.innerHTML = `<div class="mhead">Hard to crack — tap for Affinity</div>`+
      (rows.map(mHtcCardHTML).join('')||'<div class="mpath" style="color:var(--muted)">Nothing matches.</div>');
    return;
  }
  const vis = visible();
  el.innerHTML = `<div class="mhead">Funds</div>`+srt(vis.filter(e=>e.kind==='fund')).map(mCardHTML).join('')+
    `<div class="mhead">Super-angels</div>`+srt(vis.filter(e=>e.kind==='angel')).map(mCardHTML).join('');
  el.querySelectorAll('.mcard[data-slug]').forEach(c=>{
    const open = ()=>openSheet(c.dataset.slug);
    c.addEventListener('click',ev=>{ if(!ev.target.closest('a')) open(); });
    c.addEventListener('keydown',ev=>{ if(ev.key==='Enter') open(); });
  });
}
function openSheet(slug){
  const e = E().find(x=>x.slug===slug); if(!e) return;
  const v = eff(e);
  document.getElementById('sheetname').innerHTML = `<span class="fname ${v.tier}"><span class="tdot"></span>${e.name}</span>`;
  document.getElementById('sheetstats').innerHTML = `
    <span><b>${v.cov}</b>coverage${state.person?` · team ${e.connectivity}`:''}</span>
    <span><b>${e.relevance?e.relevance.total:'—'}</b>relevance</span>
    <span><b>${pipeCount(e)}</b>${state.person?state.person.split(' ')[0]+"'s":'live'} pipeline</span>`;
  const det = document.getElementById('sheetdetail');
  det.innerHTML = detailHTML(e);
  det.querySelectorAll('[data-copy]').forEach(b=>b.addEventListener('click',()=>{
    navigator.clipboard?.writeText(`${e.name}: dormant tie via ${e.dormant.internal.join(' + ')} — ${e.dormant.context} (last ${e.dormant.last}).`); toast('Copied');}));
  document.getElementById('sheet').classList.add('open');
  document.getElementById('sheet').scrollTop = 0;
  state.open = slug; startLive(e); updateHash();
}
document.getElementById('fb').addEventListener('click',()=>{
  const p = document.getElementById('fbpop'); p.hidden = !p.hidden;
});
document.getElementById('fbclose').addEventListener('click',()=>{ document.getElementById('fbpop').hidden = true; });
document.getElementById('sheetclose').addEventListener('click',()=>{
  document.getElementById('sheet').classList.remove('open'); state.open=''; stopLive(); updateHash();
});
matchMedia('(max-width:700px)').addEventListener('change',()=>render());

// ---------- live sync (viewer's Affinity connector via window.claude.mcp) ----------
const LIVE_BUCKET = {'Pre-lead':'prelead','Reach Out Now':'reachout','Awaiting Reply':'awaiting',
  'Lead':'lead','Qualified Lead':'lead','Deal':'lead','Hard to crack':'hard','Portfolio Company':'portfolio'};
let liveSub = null;   // {slug, unsub}
const nrmInv = s => (s||'').toLowerCase().normalize('NFKD').replace(/[̀-ͯ]/g,'')
  .replace(/[^a-z0-9 ]+/g,' ').replace(/\s+/g,' ').trim();
function aliasHit(inv, aliases){
  const ni = nrmInv(inv);
  return aliases.some(a => ni===a || (ni.startsWith(a+' ') && a.split(' ').length>=2));
}
function stopLive(){ if(liveSub){ liveSub.unsub(); liveSub=null; } }
function startLive(e){
  stopLive();
  if(!window.claude || window.claude.mcp===undefined || e.kind!=='fund' || !e.liveTerm) return;
  if(!e._baked) e._baked = JSON.parse(JSON.stringify(e.buckets));
  const input = {list_id: 9387, limit: 100,
    field_ids: ["field-81237","field-81239","affinity-data-investors"],
    search_criteria: {search: {term: e.liveTerm, fieldIds: ["affinity-data-investors"]}}};
  const unsub = window.claude.mcp.watchTool('Affinity','search_list_entries', input, ev=>{
    if(liveSub && liveSub.slug!==e.slug) return;
    if(ev.type==='error'){
      const c = ev.error.code;
      if(['needs_reauth','server_not_connected','blocked_by_policy','approval_required',
          'not_granted','capability_disabled','capability_removed','not_in_manifest',
          'selection_required'].includes(c)){
        e.buckets = JSON.parse(JSON.stringify(e._baked)); e.liveAt = null; e.liveOff = true;
        rerenderOpen(e);
      } // transient errors: keep last-good data, no UI churn
      return;
    }
    const rows = (ev.result.payload && ev.result.payload.data) || [];
    const seenIds = new Set();
    let changed = false;
    const allItems = {};
    for(const k in e.buckets) for(const p of e.buckets[k]) allItems[p.id] = {k, p};
    for(const r of rows){
      const ent = r.entity || {}; const f = {};
      for(const fl of ent.fields||[]) f[fl.id] = fl.value && fl.value.data;
      const invs = f['affinity-data-investors'];
      if(!Array.isArray(invs) || !invs.some(x=>aliasHit(x, e.liveAliases))) continue;
      seenIds.add(ent.id);
      const funnel = f['field-81237'] && f['field-81237'].text;
      const bk = LIVE_BUCKET[funnel];
      const own = Array.isArray(f['field-81239']) ? f['field-81239'].map(o=>((o.firstName||'')+' '+(o.lastName||'')).trim()) : [];
      const cur = allItems[ent.id];
      if(cur){
        if(cur.p.funnel!==funnel){
          e.buckets[cur.k] = e.buckets[cur.k].filter(x=>x.id!==ent.id);
          if(bk){ cur.p.funnel = funnel; e.buckets[bk].push(cur.p); }
          changed = true;
        }
        if(own.length){ cur.p.own = own; }
      } else if(bk){
        e.buckets[bk].push({id: ent.id, name: ent.name, domain: ent.domain, funnel, country: null, own});
        changed = true;
      }
    }
    const at = (ev.result.cache && ev.result.cache.storedAt) || Date.now();
    if(changed || !e.liveAt){ e.liveAt = at; e.liveOff = false; rerenderOpen(e); }
    else { e.liveAt = at; const b = document.querySelector('.livebadge'); if(b) b.textContent = liveLabel(e); }
  }, {cache: {staleTime: 60000}, refetchInterval: 120000});
  liveSub = {slug: e.slug, unsub};
}
const liveLabel = e => `● live · Affinity · ${new Date(e.liveAt).toLocaleTimeString('en-GB',{hour:'2-digit',minute:'2-digit'})}`;
function rerenderOpen(e){
  if(isMobile()){
    const sheet = document.getElementById('sheet');
    if(sheet.classList.contains('open') && state.open===e.slug){
      document.getElementById('sheetdetail').innerHTML = detailHTML(e);
    }
    return;
  }
  const det = document.querySelector(`#d-${CSS.escape(e.slug)}.open .detail`);
  if(det) det.innerHTML = detailHTML(e);
  const row = document.querySelector(`tr.mainrow[data-slug="${e.slug}"]`);
  if(row && row.children[3]) row.children[3].innerHTML = `<div class="chips">${chipHTML(e)}</div>`;
}

// ---------- render ----------
function srt(list){ const col = COLS.find(c=>c.k===state.sort)||COLS[4]; return [...list].sort(col.sort); }
function visible(){
  return E().filter(e=>(!state.q||e.name.toLowerCase().includes(state.q))
    && (!state.cat || e.kind!=='fund' || e.category===state.cat)
    && (!state.cc || e.kind!=='fund' || (e.city||'').endsWith(state.cc)));
}
function render(){
  const mob = isMobile();
  if(!state.open) stopLive();
  document.getElementById('fundsview').style.display = state.view==='funds'?'':'none';
  document.getElementById('htcview').style.display = state.view==='htc'?'':'none';
  if(mob){
    if(state.view==='funds') filtersHTML();
    renderMobile(); updateHash(); return;
  }
  document.getElementById('sheet').classList.remove('open');
  if(state.view==='htc'){ htcHTML(); return; }
  filtersHTML();
  const vis = visible();
  const ft=document.getElementById('fundtable'), at=document.getElementById('angeltable');
  ft.innerHTML = headHTML()+`<tbody>`+srt(vis.filter(e=>e.kind==='fund')).map(rowHTML).join('')+`</tbody>`;
  at.innerHTML = headHTML()+`<tbody>`+srt(vis.filter(e=>e.kind==='angel')).map(rowHTML).join('')+`</tbody>`;
  [ft,at].forEach(bindTable);
  updateHash();
}
function bindTable(tbl){
  tbl.querySelectorAll('thead th.sortable').forEach(th=>th.addEventListener('click',()=>{state.sort=th.dataset.k;render();}));
  tbl.querySelectorAll('tr.mainrow').forEach(r=>{
    const open = ev=>{
      if(ev.target.closest('a')||ev.target.closest('button')) return;
      const slug=r.dataset.slug;
      toggleRow(slug, ev.target.closest('.chip'));
    };
    r.addEventListener('click', open);
    r.addEventListener('keydown', ev=>{ if(ev.key==='Enter') open(ev); });
  });
  tbl.querySelectorAll('[data-copy]').forEach(b=>b.addEventListener('click',()=>{
    const e=E().find(x=>x.slug===b.dataset.copy);
    navigator.clipboard?.writeText(`${e.name}: dormant tie via ${e.dormant.internal.join(' + ')} — ${e.dormant.context} (last ${e.dormant.last}). Coverage ${e.connectivity}, relevance ${e.relevance?e.relevance.total:'—'}.`);
    toast('Copied');
  }));
}
function toggleRow(slug, chip){
  if(isMobile()){ openSheet(slug); return; }
  const e=E().find(x=>x.slug===slug); if(!e) return;
  const det=document.getElementById('d-'+slug); if(!det) return;
  const wasOpen = det.classList.contains('open');
  document.querySelectorAll('tr.detailrow.open').forEach(x=>x.classList.remove('open'));
  if(!wasOpen){ det.querySelector('.detail').innerHTML=detailHTML(e); det.classList.add('open');
    det.querySelectorAll('[data-copy]').forEach(b=>b.addEventListener('click',()=>{
      navigator.clipboard?.writeText(`${e.name}: dormant tie via ${e.dormant.internal.join(' + ')} — ${e.dormant.context} (last ${e.dormant.last}).`); toast('Copied');}));
    state.open = slug;
    startLive(e);
    if(chip && !chip.classList.contains('empty')){
      const sec=document.getElementById(`sec-${slug}-${chip.dataset.k}`);
      if(sec){ sec.open=true; sec.scrollIntoView({behavior:'smooth', block:'center'}); }
    }
  } else { state.open = ''; stopLive(); }
  updateHash();
}
function labels(){
  const f=E().filter(e=>e.kind==='fund').length, a=E().length-f;
  document.getElementById('pagetitle').textContent = `Highland's ${D.regions[state.region].adj} VC Ecosystem Coverage`;
  document.getElementById('subcount').textContent = `The ${f} ${D.regions[state.region].label} funds that matter most plus ${a} super-angels.`;
  document.getElementById('fresh').innerHTML = ' Data as of: '+Object.entries(D.freshness).map(([k,v])=>`${k} — ${v}`).join(' · ')+'.';
}
// ---------- hash routing ----------
function updateHash(){
  let h = '#'+state.region;
  if(state.view==='htc') h+='/htc';
  else if(state.open) h+='/'+state.open;
  if(state.person) h+='?as='+encodeURIComponent(state.person);
  history.replaceState(null,'',h);
}
function readHash(){
  const m = location.hash.match(/^#([a-z]+)(?:\/([a-z0-9-]+))?(?:\?as=(.+))?$/i);
  if(!m) return;
  if(REGIONS.includes(m[1])) state.region=m[1];
  if(m[3]) state.person = decodeURIComponent(m[3]);
  if(m[2]==='htc') state.view='htc';
  else if(m[2]) state.pendingOpen = m[2];
}

addEventListener('hashchange',()=>{  // deep links work without a reload
  state.view = location.hash.includes('/htc') ? 'htc' : 'funds';
  if(!location.hash.includes('?as=')) state.person = '';
  state.open = '';
  readHash();
  document.querySelectorAll('#regionseg button').forEach(x=>x.classList.toggle('on', x.dataset.r===state.region));
  document.querySelectorAll('#viewseg button').forEach(x=>x.classList.toggle('on', x.dataset.v===state.view));
  const va2 = document.getElementById('viewas'); if(va2) va2.value = state.person||'';
  labels(); scoreboard(); render();
  if(state.pendingOpen){ const s=state.pendingOpen; state.pendingOpen='';
    toggleRow(s); const el=document.querySelector(`tr[data-slug="${s}"]`); el&&el.scrollIntoView({block:'center'}); }
});
// ---------- boot ----------
readHash();
const seg = document.getElementById('regionseg');
REGIONS.forEach(r=>{const b=document.createElement('button');b.textContent=D.regions[r].label;b.dataset.r=r;
  if(r===state.region)b.classList.add('on');
  b.addEventListener('click',()=>{state.region=r;state.open='';seg.querySelectorAll('button').forEach(x=>x.classList.remove('on'));b.classList.add('on');labels();scoreboard();render();});
  seg.appendChild(b);});
document.querySelectorAll('#viewseg button').forEach(b=>b.addEventListener('click',()=>{
  document.querySelectorAll('#viewseg button').forEach(x=>x.classList.remove('on'));
  b.classList.add('on'); state.view=b.dataset.v; render(); updateHash();
}));
const va = document.getElementById('viewas');
D.roster.forEach(n=>{const o=document.createElement('option');o.value=n;o.textContent=n;va.appendChild(o);});
if(state.person) va.value=state.person;
va.addEventListener('change',()=>{state.person=va.value; scoreboard(); render();});
const tip = document.createElement('div'); tip.id='tip'; document.body.appendChild(tip);
function showTip(target, html){
  tip.innerHTML = html; tip.classList.add('show');
  tip.style.left='0px'; tip.style.top='0px';
  const r = target.getBoundingClientRect(), tw = tip.offsetWidth, th = tip.offsetHeight;
  const x = Math.min(Math.max(8, r.left + r.width/2 - tw/2), innerWidth - tw - 8);
  let y = r.top - th - 9; if(y < 8) y = r.bottom + 9;
  tip.style.left = x+'px'; tip.style.top = y+'px';
}
const TIP_PCT = `<div class="th">Relationship strength</div>
  Affinity score for this one-to-one connection, from <b>email &amp; meeting frequency</b> and <b>recency</b>.
  <div class="tf"><b>100%</b> active recent dialogue &nbsp;·&nbsp; <b>10%</b> thin or faded thread</div>`;
const tipFlag = moved => `<div class="th warn">⚠ Stale affiliation</div>
  Harmonic now lists their primary role as <b>${moved||'another firm'}</b>. The tie is still warm,
  but may no longer open doors at this fund.
  <div class="tf">Automated check — can misread board seats as departures; flag it if wrong.</div>`;
function tipCov(e){
  const v = eff(e);
  if(state.person){
    const fn = state.person.split(' ')[0];
    return `<div class="th">Coverage ${v.cov}/100 — ${fn} only</div>
      Recomputed from <b>${fn}'s own</b> Affinity relationships and Harmonic network with ${e.name} — the whole-team blend is ignored in this view.`;
  }
  const cp = e.cov_parts||{};
  const dorm = cp.dorm?`<br>Dormant-tie floor <b>${Math.round(cp.dorm*100)}</b> <span style="color:var(--muted)">(an old thread keeps it above zero)</span>`:'';
  return `<div class="th">Coverage ${v.cov}/100</div>
    Harmonic team-network <b>${Math.round((cp.h||0)*100)}</b><br>
    Affinity partnership relationships <b>${Math.round((cp.a||0)*100)}</b><br>
    Recency decay <b>×${cp.decay??1}</b>${dorm}
    <div class="tf">Blend: 55% Harmonic + 45% Affinity, then × decay — a path untouched for over a year fades hard</div>`;
}
function tipRel(e){
  const r = e.relevance;
  if(!r) return `<div class="th">Relevance</div>No score — not enough Harmonic history for this profile.`;
  if(r.angel) return `<div class="th">Relevance ${r.total}/100 — angel blend</div>
    Deal velocity <b>${r.deals}</b><br>
    Unicorn outcomes <b>${r.uni}</b><br>
    Syndication with funds we cover <b>${r.synd}</b><br>
    Presence on our pipeline cap tables <b>${r.pipe}</b>
    <div class="tf">How upstream this angel is for Highland: how much they invest, how well it turns out, and how often it lands in front of us</div>`;
  return `<div class="th">Relevance ${r.total}/100</div>
    Stage fit <b>${r.stage}</b>/25 · Sector fit <b>${r.sector}</b>/25<br>
    Europe share <b>${r.geo}</b>/20 <span style="color:var(--muted)">(${Math.round(r.europe)}% of recent deals in Europe)</span><br>
    Activity <b>${r.activity}</b>/15 · Graduation to growth rounds <b>${r.grad}</b>/15
    <div class="tf">How much this fund's portfolio should feed Highland's pipeline — independent of how well we know them</div>`;
}
const tipEmail = el => `<div class="th${el.dataset.guess?' warn':''}">${el.dataset.guess?'Email — unverified guess':'Email'}</div>
  <b>${el.dataset.em}</b><br>${el.dataset.guess?`Inferred from this fund's email format — not confirmed, sanity-check before sending.`:'From Affinity.'}
  <div class="tf">Click to copy to clipboard</div>`;
document.addEventListener('click',ev=>{
  const el = ev.target.closest('.em');
  if(!el) return;
  ev.stopPropagation(); ev.preventDefault();
  navigator.clipboard?.writeText(el.dataset.em);
  toast(`Copied ${el.dataset.em}`);
}, true);
document.addEventListener('mouseover',ev=>{
  const em = ev.target.closest('.em');
  if(em){ showTip(em, tipEmail(em)); return; }
  const p = ev.target.closest('.pct'), f = ev.target.closest('.flag'),
        c = ev.target.closest('td.covtd'), rl = ev.target.closest('td.relcell');
  const ent = t => { const tr = t.closest('tr.mainrow'); return tr && E().find(x=>x.slug===tr.dataset.slug); };
  if(f) showTip(f, tipFlag(f.dataset.moved));
  else if(p) showTip(p, TIP_PCT);
  else if(c){ const e = ent(c); if(e) showTip(c.querySelector('.covcell')||c, tipCov(e)); }
  else if(rl){ const e = ent(rl); if(e) showTip(rl.querySelector('b')||rl, tipRel(e)); }
});
document.addEventListener('mouseout',ev=>{
  if(ev.target.closest && (ev.target.closest('.pct')||ev.target.closest('.flag')||ev.target.closest('td.covtd')||ev.target.closest('td.relcell')||ev.target.closest('.em'))) tip.classList.remove('show');
});
addEventListener('scroll',()=>tip.classList.remove('show'),true);
document.getElementById('q').addEventListener('input',e=>{state.q=e.target.value.toLowerCase();render()});

function toast(msg){const t=document.getElementById('toast');t.textContent=msg;t.style.display='block';setTimeout(()=>t.style.display='none',2400)}
function csv(){
  const rows=[["name","kind","category","city","relevance","coverage","tier","gap","last_touch","coinvested","untracked_eu",
    ...BUCKETS.map(([k])=>k),"top_path_external","top_path_internal","top_path_pct","top_path_last"]];
  for(const e of E()){
    const p=e.points[0]||{};
    rows.push([e.name,e.kind,e.category||'',e.city||'',e.relevance?e.relevance.total:'',eff(e).cov,eff(e).tier,eff(e).gap??'',
      e.fund_last||'',e.coinvest.join('; '),(e.untracked||[]).length,...BUCKETS.map(([k])=>e.buckets[k].length),
      p.external||'',p.internal||'',p.pct??'',p.last||'']);
  }
  return rows.map(r=>r.map(v=>`"${String(v).replaceAll('"','""')}"`).join(',')).join('\n');
}
if (window.claude && window.claude.downloads){
  const btn=document.getElementById('export'); btn.hidden=false;
  btn.addEventListener('click', async ()=>{
    const data=csv();
    try{ await window.claude.downloads.save({filename:`coverage-${state.region}.csv`, data}); toast("Saved"); }
    catch(err){
      if(err && err.code==='extension_not_enabled'){
        try{ await window.claude.downloads.save({filename:`coverage-${state.region}.txt`, data}); toast("Saved as .txt"); }
        catch(e2){ if(e2&&e2.code!=='declined') toast("Export unavailable"); }
      } else if(err && err.code==='rate_limited'){ toast("Try again in a moment");
      } else if(err && err.code!=='declined'){ toast("Export unavailable"); }
    }
  });
}
labels(); scoreboard(); render();
if(state.pendingOpen){ setTimeout(()=>{ toggleRow(state.pendingOpen); const el=document.querySelector(`tr[data-slug="${state.pendingOpen}"]`); el&&el.scrollIntoView({block:'center'}); }, 50); }
</script>
"""
