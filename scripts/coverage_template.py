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
.appbar .in{max-width:1760px;margin:0 auto;display:flex;align-items:center;gap:14px;padding:12px 28px;flex-wrap:wrap}
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
.wrap{max-width:1760px;margin:0 auto;padding:0 28px}
.hero{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:8px 56px;align-items:end;
  padding:32px 0 20px;border-bottom:1px solid var(--hair)}
.heroL{min-width:0}
.kicker{font-size:10.5px;letter-spacing:.16em;text-transform:uppercase;color:var(--muted);margin-bottom:10px}
h1{font-size:30px;font-weight:600;letter-spacing:-.015em;text-wrap:balance;font-family:var(--display);margin:0}
.sub{color:var(--ink2);margin-top:8px;font-size:14px;max-width:980px}
.regionnav{display:inline-flex;border:1px solid var(--hair);border-radius:11px;overflow:hidden;
  background:var(--surface);flex-wrap:nowrap}
.regionnav button{background:transparent;color:var(--ink2);border:0;border-left:1px solid var(--hair);
  border-radius:0;padding:9px 22px;font-size:14px;font-weight:650;cursor:pointer;letter-spacing:-.01em}
.regionnav button:first-child{border-left:0}
.regionnav button:hover{color:var(--ink)}
.regionnav button.on{background:var(--ink);color:var(--surface)}
.shrow.trip .shcard{min-width:0}
.tripdoors{font-size:11.5px;margin-top:3px;color:var(--ink2)}
.tripdoors a{font-weight:600}
.toolbar{display:flex;align-items:center;justify-content:space-between;gap:14px;flex-wrap:wrap;padding:14px 0 2px}
.actionrow{display:flex;gap:8px;align-items:center;flex-wrap:wrap}
.actlabel{font-size:10px;letter-spacing:.14em;text-transform:uppercase;color:var(--muted);font-weight:700;margin-right:2px}
.abtn{background:var(--accent-soft);border:1px solid var(--accent);color:var(--accent-ink);border-radius:9px;
  padding:9px 16px;font-size:13px;font-weight:650;cursor:pointer;letter-spacing:-.01em}
.abtn:hover{background:var(--ink);color:var(--surface);border-color:var(--ink)}
#apback{position:fixed;inset:0;background:rgba(20,18,12,.35);z-index:65;display:none}
#apback.open{display:block}
#apanel{position:fixed;top:0;right:0;width:min(640px,96vw);height:100vh;background:var(--page);
  border-left:1px solid var(--hair);z-index:70;overflow-y:auto;transform:translateX(102%);
  transition:transform .22s ease;box-shadow:-18px 0 40px rgba(0,0,0,.12)}
#apanel.open{transform:none}
.aphead{position:sticky;top:0;background:var(--page);z-index:3;display:flex;align-items:center;gap:10px;
  padding:16px 20px 12px;border-bottom:1px solid var(--hair)}
.aphead #aptitle{flex:1;font-size:17px;font-weight:700;letter-spacing:-.01em}
.aphead button{background:var(--surface);border:1px solid var(--hair);border-radius:8px;width:32px;height:32px;
  font-size:14px;color:var(--ink2);cursor:pointer}
.apctx{display:flex;gap:10px;align-items:center;padding:10px 20px;border-bottom:1px solid var(--hair);
  font-size:12px;color:var(--muted);flex-wrap:wrap}
.apctx select{background:var(--surface);color:var(--ink);border:1px solid var(--hair);border-radius:8px;
  padding:6px 10px;font-size:12.5px}
.apbody{padding:14px 20px 80px}
.aphint{font-size:12px;color:var(--muted);margin:2px 0 12px}
.apsec{font-size:11px;letter-spacing:.08em;text-transform:uppercase;color:var(--muted);font-weight:700;margin:18px 0 8px}
.apcard{border:1px solid var(--hair);border-radius:10px;padding:11px 13px;margin-bottom:10px}
.apcard .fname{font-size:14.5px}
.apmeta{font-size:11.5px;color:var(--muted);margin-top:2px}
.appath{font-size:12.5px;margin-top:6px}
.appath b{font-weight:650}
.appath .via{color:var(--muted)}
.apacts{display:flex;gap:8px;margin-top:8px;flex-wrap:wrap}
.apacts a,.apacts button{font-size:12px;font-weight:600;border:1px solid var(--hair);border-radius:7px;
  padding:5px 11px;background:var(--surface);color:var(--ink);cursor:pointer;text-decoration:none}
.apacts a:hover,.apacts button:hover{border-color:var(--ink2)}
.apdraft{margin-top:10px;border-top:1px dashed var(--hair);padding-top:10px}
.apdraft textarea{width:100%;min-height:150px;border:1px solid var(--hair);border-radius:8px;background:var(--surface);
  color:var(--ink);font:12.5px/1.5 inherit;padding:10px;resize:vertical}
.aptog{display:inline-flex;border:1px solid var(--hair);border-radius:7px;overflow:hidden;margin-bottom:8px}
.aptog button{border:0;background:var(--surface);color:var(--ink2);font-size:11.5px;font-weight:650;padding:5px 12px;cursor:pointer}
.aptog button.on{background:var(--ink);color:var(--surface)}
.apcontact{font-size:11.5px;color:var(--ink2);margin:4px 0 8px}
.apcontact .guess{color:var(--thin-ink)}
.aprow{display:flex;align-items:baseline;gap:8px;padding:5px 0;border-bottom:1px solid var(--hair2);font-size:13px;flex-wrap:wrap}
.aprow .cc{font-size:11px}
@media(max-width:760px){.apbody{padding:12px 14px 80px}}
.subline{display:flex;align-items:baseline;gap:14px;flex-wrap:wrap}
.about summary{cursor:pointer;color:var(--accent-ink);font-size:12.5px;font-weight:600;list-style:none;white-space:nowrap}
.about summary::before{content:"ⓘ ";font-weight:400}
.about summary::-webkit-details-marker{display:none}
.about .aboutbody{margin-top:8px;max-width:860px;color:var(--ink2);font-size:13.5px;line-height:1.55;
  border:1px solid var(--hair);border-radius:10px;padding:12px 14px;background:var(--surface)}
.score{display:flex;align-self:end;margin:0 0 2px}
.score .s.go{cursor:pointer} .score .s.go:hover b{text-decoration:underline}
.score .s{padding:0 26px 0;border-left:1px solid var(--hair);max-width:200px}
.score .s:first-child{border-left:0;padding-left:0}
.score .s:last-child{padding-right:0}
.score b{display:block;font-size:30px;font-weight:650;font-variant-numeric:tabular-nums;letter-spacing:-.02em;line-height:1.05}
.score span{display:block;color:var(--muted);font-size:10px;text-transform:uppercase;letter-spacing:.09em;margin-top:4px;line-height:1.45}
.score .s.crit b{color:var(--gap-ink)} .score .s.warn b{color:var(--thin-ink)}
@media(max-width:1180px){
  .hero{grid-template-columns:1fr;gap:0}
  .score{align-self:start;width:100%;margin-top:18px;padding-top:14px;border-top:1px solid var(--hair)}
  .score .s{flex:1;max-width:none}
}
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
tbody td{padding:18px 14px;border-bottom:1px solid var(--hair2);vertical-align:middle}
tbody tr.mainrow{cursor:pointer}
tbody tr.mainrow:hover td{background:var(--hair2)}
tbody tr.mainrow td:first-child{box-shadow:inset 2px 0 0 transparent}
tbody tr.mainrow:hover td:first-child{box-shadow:inset 2px 0 0 var(--accent)}
thead th{position:sticky;top:0;background:var(--page);z-index:4}
tbody tr.mainrow:focus-visible{outline:2px solid var(--accent);outline-offset:-2px}
.fname{font-weight:650;font-size:15.5px;letter-spacing:-.01em;display:flex;align-items:center;gap:9px}
.fname .tdot{width:8px;height:8px;border-radius:50%;flex:none}
.fname a{color:inherit;text-decoration:none}
.fname a:hover{text-decoration:underline}
.fname.strong{color:var(--covered-ink)} .fname.strong .tdot{background:var(--covered)}
.fname.medium{color:var(--thin-ink)} .fname.medium .tdot{background:var(--thin)}
.fname.weak{color:var(--gap-ink)} .fname.weak .tdot{background:var(--gap)}
.fmeta{font-size:11.5px;color:var(--muted);margin-top:4px;padding-left:17px;display:flex;gap:0;flex-wrap:wrap;align-items:baseline}
.fmeta>*+*::before{content:"·";margin:0 7px;color:var(--hair)}
.fmeta .badge{background:none;padding:0;border-radius:0;letter-spacing:.08em;font-weight:600}
.fmeta .badge.co{color:var(--covered-ink);background:none;border:0}
.fmeta .badge.unt{color:var(--accent-ink);background:none;border:0;font-weight:600}
.fmeta .badge.ufq{color:var(--ink2);background:none;border:0;font-weight:600}
.fmeta .badge.ufq.hi{color:var(--c-lead-ink)}
.ufproof{margin-top:2px}
.ufproof a{color:inherit;text-decoration:none;font-weight:600}
.ufproof a:hover{text-decoration:underline}
.covtop{display:flex;align-items:center;gap:7px}
td.covtd{min-width:150px}
th.mytd{color:var(--accent-ink)}
td.covtd{padding:12px 8px}
.covcard{background:var(--raise);border:1px solid var(--hair2);border-radius:14px;
  padding:13px 16px 11px;width:252px;box-sizing:border-box}
.covcard.mine{background:var(--accent-soft);border-color:#c9cdf7}
.covhead{display:flex;align-items:baseline;gap:9px;margin-bottom:10px}
.covnum{font-size:21px;font-weight:700;letter-spacing:-.02em;font-variant-numeric:tabular-nums;line-height:1}
.covnum.strong{color:var(--covered-ink)} .covnum.medium{color:var(--thin-ink)} .covnum.weak{color:var(--gap-ink)}
.covcap{font-size:9.5px;font-weight:700;letter-spacing:.09em;text-transform:uppercase;color:var(--muted)}
.covcard.mine .covcap{color:var(--accent-ink)}
.covrow{display:flex;gap:7px}
.cst{flex:1;min-width:0;display:flex;flex-direction:column;align-items:center;gap:3px}
.cst b{font-size:12.5px;font-weight:700;font-variant-numeric:tabular-nums;color:var(--ink);line-height:1.1}
.cst i{display:block;width:100%;height:3px;border-radius:2px}
.cst span{font-size:7.5px;font-weight:650;letter-spacing:.05em;text-transform:uppercase;color:var(--muted);white-space:nowrap}
.cst.z b{color:var(--hair)} .cst.z i{background:var(--hair2)!important} .cst.z span{color:var(--hair)}
tr.detailrow td{background:none;box-shadow:none}
.chips.mini{gap:4px;max-width:210px}
.chips.mini .chip{font-size:10.5px;padding:2px 9px;white-space:nowrap}
.nochip{color:var(--muted);font-size:11.5px}
.pgroup{border:1px solid var(--hair2);border-radius:14px;padding:10px 14px;margin:8px 0;background:var(--raise)}
.pgroup.mine{background:var(--accent-soft);border-color:#c9cdf7}
.pglabel{font-size:10px;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:var(--muted);margin-bottom:7px}
.pgroup.mine .pglabel{color:var(--accent-ink)}
#whoback{position:fixed;inset:0;background:rgba(20,18,12,.45);z-index:90;display:none;align-items:center;justify-content:center}
#whoback.open{display:flex}
#whocard{background:var(--page);border:1px solid var(--hair);border-radius:14px;padding:26px 30px;
  max-width:440px;width:92%;box-shadow:0 14px 44px rgba(0,0,0,.2)}
#whocard .th{font-size:18px;font-weight:700}
#whocard p{font-size:13px;color:var(--ink2);margin:6px 0 16px;line-height:1.5}
#wholist{display:flex;flex-wrap:wrap;gap:8px}
#wholist button{border:1px solid var(--hair);background:var(--surface);border-radius:9px;padding:8px 14px;
  font-size:13.5px;font-weight:600;cursor:pointer;color:var(--ink)}
#wholist button:hover{border-color:var(--ink)}
#wholist button.on{background:var(--ink);color:var(--surface);border-color:var(--ink)}
.covword{font-size:10px;font-weight:700;letter-spacing:.04em;text-transform:uppercase;text-align:center;margin-top:2px}
.covword.strong{color:var(--covered-ink)} .covword.medium{color:var(--thin-ink)} .covword.weak{color:var(--gap-ink)}
.covcmp{font-size:10px;font-weight:700;letter-spacing:.04em;text-transform:uppercase;text-align:center;margin-top:2px;color:var(--muted);white-space:nowrap}
.covcmp .strong{color:var(--covered-ink)} .covcmp .medium{color:var(--thin-ink)} .covcmp .weak{color:var(--gap-ink)}
.nm{font-size:11.5px;font-weight:700;margin-bottom:4px}
.nm.live{color:var(--covered-ink)} .nm.warm{color:var(--thin-ink)} .nm.gap{color:var(--gap-ink)}
#starthere{margin:16px 0 2px}
.shhead{font-size:11px;letter-spacing:.08em;text-transform:uppercase;color:var(--muted);font-weight:700;margin-bottom:8px}
.shrow{display:grid;grid-template-columns:repeat(3,1fr);gap:10px}
.shcard{border:1px solid var(--hair);border-radius:10px;padding:10px 12px;cursor:pointer}
.shcard:hover,.shcard:focus-visible{border-color:var(--ink2);outline:none}
.shcard .fname{font-size:14px}
.shwhy{font-size:11.5px;color:var(--ink2);margin:3px 0 5px}
.shcard .nm{margin-bottom:0}
@media(max-width:760px){.shrow{grid-template-columns:1fr}}
.badge{font-size:10px;border-radius:9px;padding:1px 7px;background:var(--hair2);color:var(--ink2);white-space:nowrap;letter-spacing:.03em}
.badge.co{color:var(--covered-ink);border:1px solid var(--covered);background:transparent}
.badge.unt{color:var(--accent-ink);border:1px solid var(--accent);background:transparent}
.badge.ufq{color:var(--ink2);border:1px solid var(--hair2);background:transparent}
.badge.ufq.hi{color:var(--c-lead-ink);border-color:var(--c-lead)}
.covcell{position:relative;display:inline-flex;align-items:center;justify-content:center;font-variant-numeric:tabular-nums}
.covcell>b{position:absolute;inset:0;display:flex;align-items:center;justify-content:center}
.covcell svg{flex:none}
.covcell b{font-size:13.5px;font-weight:700}
.relcell{font-variant-numeric:tabular-nums}
.relcell b{font-size:14.5px;font-weight:620}
.relcell .rb{display:block;width:64px;height:3px;background:var(--hair);border-radius:2px;margin-top:5px;overflow:hidden}
.relcell .rb i{display:block;height:100%;background:var(--ink2);border-radius:2px}
.chips{display:flex;gap:6px;flex-wrap:wrap;max-width:430px}
.chip{font-size:11px;border-radius:999px;padding:3px 10px;cursor:pointer;border:1px solid transparent;
  font-variant-numeric:tabular-nums;white-space:nowrap;font-weight:550}
.chip b{font-weight:650}
.uvtag{font-size:9.5px;font-weight:700;letter-spacing:.05em;text-transform:uppercase;
  color:var(--thin-ink);background:var(--c-awaiting);border-radius:5px;padding:1px 5px;white-space:nowrap}
.ufb{font-size:10px;font-weight:700;border-radius:5px;padding:1px 5px;vertical-align:1px;font-variant-numeric:tabular-nums}
.ufb.hi{background:var(--c-lead);color:var(--c-lead-ink)}
.ufb.mid{background:var(--c-awaiting);color:var(--c-awaiting-ink)}
.ufb.lo{background:var(--hair2);color:var(--ink2)}
#changes{margin:16px 0 0}
.chgsec{background:var(--surface);border:1px solid var(--hair);border-radius:12px;padding:0 16px}
.chgsec summary{cursor:pointer;list-style:none;display:flex;align-items:baseline;gap:8px;padding:12px 0;
  font-size:11px;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:var(--ink2)}
.chgsec summary::-webkit-details-marker{display:none}
.chgsec summary::before{content:'▸';color:var(--muted);font-size:11px}
.chgsec[open] summary::before{content:'▾'}
.chgsec summary .cnt{color:var(--muted);font-weight:400;text-transform:none;letter-spacing:0;font-size:11.5px}
.chglist{display:grid;grid-template-columns:repeat(auto-fill,minmax(360px,1fr));gap:7px 24px;padding:2px 0 14px;font-size:12.5px;color:var(--ink2)}
.chg a{color:var(--ink);font-weight:620;text-decoration:none}
.chg a:hover{text-decoration:underline}
.chg .cc{color:var(--muted)}
.chg.up b{color:var(--covered-ink)} .chg.down b{color:var(--gap-ink)} .chg.add b{color:var(--accent-ink)}
.avi{display:inline-flex;width:19px;height:19px;border-radius:50%;align-items:center;justify-content:center;
  font-size:8.5px;font-weight:700;color:#fff;flex:none;letter-spacing:.02em;vertical-align:-4px;margin-right:2px}
.chip.prelead{background:var(--c-prelead);color:var(--c-prelead-ink)}
.chip.reachout{background:var(--c-reachout);color:var(--c-reachout-ink)}
.chip.awaiting{background:var(--c-awaiting);color:var(--c-awaiting-ink)}
.chip.lead{background:var(--c-lead);color:var(--c-lead-ink)}
.chip.hard{background:var(--c-hard);color:var(--c-hard-ink)}
.chip:hover{border-color:currentColor}
.chip .of{font-weight:400;opacity:.65;font-size:10.5px}
.chip.dim{opacity:.45}
.covcell .teamcov{color:var(--muted);font-size:10.5px;white-space:nowrap}
.pts{font-size:12.5px;color:var(--ink2);display:flex;flex-direction:column;gap:5px;min-width:260px;max-width:520px}
.pts .pt{display:flex;align-items:baseline;gap:8px}
.pts .pt .ptl{flex:1;min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.pts .pt .ptr{flex:none;display:flex;align-items:baseline;gap:7px;font-variant-numeric:tabular-nums}
.pts .pt .ptr .sbar{width:44px;height:3px;border-radius:2px;background:var(--hair);overflow:hidden;align-self:center}
.pts .pt .ptr .sbar i{display:block;height:100%;background:var(--covered);border-radius:2px}
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
.gpos{color:var(--covered-ink);font-weight:650}
#unttable .num{font-variant-numeric:tabular-nums}
#untview{overflow-x:auto}
.untbar{display:flex;gap:14px;align-items:center;margin:10px 0 2px;flex-wrap:wrap}
#untfilters label{margin-right:8px;font-size:12px}
#untfilters select{border:1px solid var(--hair);background:var(--surface);border-radius:8px;padding:3px 7px;font:inherit;font-size:12px;color:var(--ink)}
th.sk{cursor:pointer;user-select:none;white-space:nowrap}
th.sk:hover{color:var(--accent-ink)}
.ubak{max-width:140px;min-width:100px;white-space:normal !important;line-height:1.35}
.ufo{max-width:150px;white-space:normal !important;line-height:1.35}
.btnstack{display:inline-flex;flex-direction:column;gap:4px;align-items:stretch}
.btnstack .minibtn{text-align:center;justify-content:center}
.hc{color:var(--accent-ink);font-weight:650}
.udesc{font-size:11.5px;color:var(--ink2);max-width:185px;min-width:150px;white-space:normal !important;line-height:1.4}
#unttable .df td,#unttable.df td{padding-right:8px}
#unttable .df .minibtn,#unttable.df .minibtn{padding:3px 8px;font-size:11px;white-space:nowrap}
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
.minibtn.prep{background:var(--accent);color:#fff;border-color:var(--accent);font-weight:600}
.minibtn.prep:hover{opacity:.9;color:#fff}
.note{font-size:12.5px;color:var(--muted);margin-top:48px;line-height:1.65;max-width:1100px;
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
  #fundsview table, #fundsview .sechead, #htcview table, #htcview .sechead,
  #untview table, #untview .sechead{display:none}
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
  details.munt{background:var(--surface);border:1px solid var(--hair);border-radius:12px;margin-bottom:10px;overflow:hidden}
  details.munt summary{list-style:none;cursor:pointer;display:flex;align-items:center;gap:9px;padding:13px 14px}
  details.munt summary::-webkit-details-marker{display:none}
  details.munt summary::before{content:'▸';color:var(--muted);font-size:12px;flex:none}
  details.munt[open] summary::before{content:'▾'}
  details.munt summary .fname{flex:1;font-size:15px}
  details.munt summary:active{background:var(--hair2)}
  details.munt .muntbody{padding:2px 10px 10px;border-top:1px solid var(--hair)}
  details.munt .mcard{border:0;border-bottom:1px solid var(--hair);border-radius:0;margin:0;cursor:default;padding:11px 4px}
  details.munt .mcard:last-child{border-bottom:0}
  details.munt .mcard:active{background:none}
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
  .suntchip{cursor:pointer !important}
  .suntchip.on{background:var(--ink);color:var(--page);border-color:var(--ink)}
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
  <div class="seg" id="viewseg">
    <button data-v="funds" class="on">Investors</button><button data-v="htc">H2C paths</button><button data-v="unt">Untracked Dealflow</button>
  </div>
  <button class="btn ghost" id="whoami" title="Sonar is personalised to you — click to switch">👤</button>
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
<header class="hero">
  <div class="heroL">
    <div class="kicker" id="kick">Highland Europe · relationship intelligence · __GENERATED__</div>
    <h1 id="pagetitle"></h1>
    <p class="sub subline"><span id="subcount"></span>
    <details class="about"><summary>How to read this page</summary><div class="aboutbody">
    Read each fund left to right: <b>why they matter</b> — the top of their portfolio through our Unframe
    lens; <b>where we stand</b> — <b style="color:var(--covered-ink)">covered</b>,
    <b style="color:var(--thin-ink)">thin</b> or <b style="color:var(--gap-ink)">gap</b>, blending the
    team's Harmonic network with Affinity relationships and decayed by recency — a path untouched for over
    a year fades; and <b>your next move</b> — the warm path to use, the tie to re-warm, or the co-investor
    bridge to ask for. Click a row for the dossier; use <b>View as</b> to see it through one person's
    relationships.</div></details></p>
  </div>
  <div class="score" id="score"></div>
</header>

<div class="toolbar">
  <div id="regionseg" class="regionnav"></div>
  <div class="actionrow">
    <span class="actlabel" id="actlabel">Workflows</span>
    <button class="abtn" data-ap="htc">⚡ Solve my hard-to-cracks</button>
    <button class="abtn" data-ap="net">⇗ Build my network</button>
    <button class="abtn" data-ap="geo">✈ Geo visit</button>
  </div>
</div>
<div id="changes"></div>

<div id="fundsview">
<div id="starthere"></div>
<div class="filters" id="filters"></div>
<div class="sechead"><h2>Funds</h2><p id="fundhint">sort via column headers · click a row for detail</p></div>
<table id="fundtable"></table>
<div class="sechead"><h2>Super-angels</h2><p>vital upstream nodes — ranked by their own relevance blend</p></div>
<table id="angeltable"></table>
</div>

<div id="htcview" style="display:none">
<div class="sechead"><h2>H2C paths — hard-to-cracks reachable via mapped investors</h2><p id="htchint"></p></div>
<table id="htctable"></table>
</div>

<div id="untview" style="display:none">
<div class="sechead"><h2>Untracked dealflow — deals we have no CRM record for</h2>
<div class="untbar"><div class="seg" id="untmode"><button data-um="fund" class="on">By fund</button><button data-um="company">By company</button></div>
<span id="untfilters" hidden><label class="cc">Min FTE <select id="unthc"><option value="0">any</option><option value="10">10+</option><option value="25">25+</option><option value="50">50+</option><option value="100">100+</option></select></label>
<label class="cc">Growth <select id="untgr"><option value="">any</option><option value="0">&gt;0%</option><option value="25">&gt;25%</option><option value="50">&gt;50%</option><option value="100">&gt;100%</option></select></label></span></div>
<p id="unthint"></p></div>
<table id="unttable"></table>
</div>

<div id="mlist"></div>
<div id="whoback"><div id="whocard" role="dialog" aria-modal="true" aria-label="Who are you?">
  <div class="th">Who are you?</div>
  <p>Sonar personalises coverage, workflows and next moves to you.
  Pick yourself once — it's remembered on this device.</p>
  <div id="wholist"></div>
</div></div>
<div id="apback"></div>
<aside id="apanel" role="dialog" aria-modal="true" aria-label="Action panel">
  <div class="aphead"><div id="aptitle"></div><button id="apclose" aria-label="Close">✕</button></div>
  <div class="apctx" id="apctx"></div>
  <div class="apbody" id="apbody"></div>
</aside>

<div id="sheet" role="dialog" aria-modal="true">
  <div class="sheethead"><button id="sheetclose" aria-label="Close">←</button><div class="fname" id="sheetname"></div></div>
  <div class="sheetstats" id="sheetstats"></div>
  <div class="sheetbody"><div class="detail" id="sheetdetail"></div></div>
</div>

<p class="note" id="method"><b>Method.</b> Relevance (funds) = stage fit 25 · sector fit 25 · Europe share 20 ·
activity 15 · graduation 15. Relevance (angels) = deal velocity + unicorns + syndication with covered funds +
presence on our pipeline cap tables. Coverage = 55% Harmonic team-network + 45% Affinity partnership
relationships (incl. Laurence, Fergal, Ronan), multiplied by a recency decay (≤6m ×1.0 · ≤1y ×0.9 · ≤2y ×0.5 ·
older ×0.3); dormant ties floor the score and show as ⏱ re-warmable paths. Company badges and 40% of fund
relevance come from <b>Unframe combined priority</b> (brain score blended with note priority &amp; note sentiment;
green ≥85 · amber 70–84); fund relevance = 0.6 × thesis fit + portfolio quality. Pipeline chips = companies on the
Highland Companies list backed by the investor (Lead includes Qualified Lead and Deal; passed/deprioritised
excluded). “Untracked” = their post-Feb-2025 European deals absent from our pipeline list. ⚠ marks a contact
who appears to have left the fund. Percentages next to people are <b>Affinity relationship strength</b> (0–100%):
how warm that one-to-one connection is, driven by email &amp; meeting frequency and recency — 100% means an active
recent dialogue, 10% a thin or faded thread. It is not a probability or ownership figure. Hover any % for this
definition. Every fund dossier has a “Prep brief in Claude” button that opens Claude with the meeting-prep request prefilled.
<span id="fresh"></span></p>
</div>
<div class="toast" id="toast"></div>

<script>
const D = __DATA__;
const REGIONS = Object.keys(D.regions);
const BUCKETS = [["prelead","Pre-lead"],["reachout","Reach out"],["awaiting","Awaiting"],["lead","Lead"],["hard","Hard to crack"]];
const TIER = {strong:"var(--covered)", medium:"var(--thin)", weak:"var(--gap)"};
const state = {region: REGIONS[0], view:"funds", sort:"connectivity", q:"", person:"", cat:"", cc:"",
  untMode:"fund", untSort:{k:"date",d:-1}, untHC:0, untGR:null};
const E = () => D.regions[state.region].entities;
const affURL = id => `https://${D.affinityOrg}.affinity.co/companies/${id}`;
const isOwned = p => state.person && (p.own||[]).includes(state.person);  // exact — 'Will de Quant' must not match 'Will McMahon'
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

function ring(v, tier, sz){
  const S = sz||32, r = S===32?13:(S/2-3.5), c=2*Math.PI*r, o=c*(1-v/100), m=S/2;
  return `<svg width="${S}" height="${S}" viewBox="0 0 ${S} ${S}" role="img" aria-label="coverage ${v}">
    <circle cx="${m}" cy="${m}" r="${r}" fill="none" stroke="var(--hair)" stroke-width="3.5"/>
    <circle cx="${m}" cy="${m}" r="${r}" fill="none" stroke="${TIER[tier]}" stroke-width="3.5"
      stroke-dasharray="${c.toFixed(1)}" stroke-dashoffset="${o.toFixed(1)}"
      stroke-linecap="round" transform="rotate(-90 ${m} ${m})"/></svg>`;
}

function scoreboard(){
  const f = E().filter(e=>e.kind==='fund');
  const gaps = f.filter(e=>eff(e).tier==='weak' && e.relevance.total>=60);
  const hard = D.regions[state.region].htc.length;
  const unt = f.reduce((n,e)=>n+((e.untracked||[]).length),0);
  const al = document.getElementById('actlabel');
  if(al) al.textContent = state.person ? `For ${state.person.split(' ')[0]}` : 'Workflows';
  document.getElementById('score').innerHTML = `
    <div class="s crit go" data-go="gaps"><b>${gaps.length}</b><span>${state.person?'relevant funds '+state.person.split(' ')[0]+" can't reach":'relevant funds worth time — no warm path'}</span></div>
    <div class="s warn go" data-go="htc"><b>${hard}</b><span>hard-to-crack companies reachable via these funds</span></div>
    <div class="s warn go" data-go="unt"><b>${unt}</b><span>recent EU deals we're not tracking</span></div>`;
  document.querySelectorAll('#score .s.go').forEach(t=>t.addEventListener('click',()=>{
    const g=t.dataset.go;
    if(g==='gaps'){ state.view='funds'; state.sort='gap'; render();
      document.getElementById('starthere')?.scrollIntoView({behavior:'smooth',block:'start'}); }
    else { state.view=g; document.querySelectorAll('#viewseg button').forEach(x=>x.classList.toggle('on',x.dataset.v===g)); render(); updateHash(); }
  }));
}

// ---------- filters ----------
function filtersHTML(){
  const ccs = [...new Set(E().filter(e=>e.kind==='fund').map(e=>(e.city||'').split('·').pop().trim()).filter(Boolean))].sort();
  const cats = [...new Set(E().filter(e=>e.kind==='fund').map(e=>e.category))].sort();
  let h = `<span class="lbl">Type</span>`+cats.map(c=>`<button class="fchip${state.cat===c?' on':''}" data-cat="${c}">${c.toUpperCase()}</button>`).join('');
  if(ccs.length>1) h += `<span class="lbl">Country</span>`+ccs.map(c=>`<button class="fchip${state.cc===c?' on':''}" data-cc="${c}">${c}</button>`).join('');
  const SORTS=[["connectivity","Team coverage"],["mycov",(state.person?state.person.split(' ')[0]+"’s":'My')+" coverage"],["gap","Biggest gaps"],["relevance","Relevance"],["ufq","Portfolio quality (Unframe)"],["ufhigh","High-prio backed (Unframe)"],["name","Name"]];
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
  {k:"relevance", label:"Relevance", sortable:true, sort:(a,b)=>(b.relevance?.total||0)-(a.relevance?.total||0)},
  {k:"connectivity", label:"Team coverage", sortable:true, sort:(a,b)=>b.connectivity-a.connectivity},
  {k:"mycov", label:"My coverage", sortable:true, cls:"mytd",
   sort:(a,b)=>(state.person?personCov(b,state.person)-personCov(a,state.person):0)||b.connectivity-a.connectivity},
  {k:"gap", label:"Your next move", sortable:false, sort:(a,b)=>(eff(b).gap||0)-(eff(a).gap||0)||(b.relevance?.total||0)-(a.relevance?.total||0)},
];
// one-line verdict a partner can act on, computed from path evidence
function nextMove(e){
  if(e.kind!=='fund') return null;
  const first = n => (n||'').split(' ')[0];
  const pts = e.points||[];
  const best = pts.find(p=>p.meet) || pts.find(p=>p.pct!=null&&p.pct>=30) || null;
  if(best){
    const touch = best.meet||best.last;
    if(!isStale(touch))
      return {cls:'live', txt:`Keep warm — ${first(best.internal)} ↔ ${best.external}${best.meet?` (met ${fmtD(best.meet)})`:''}`};
    return {cls:'warm', txt:`Re-warm — ${first(best.internal)} ↔ ${best.external}, last touch ${fmtD(touch)}`};
  }
  if(pts.length) return {cls:'warm', txt:`Verify first — ties are email-only (${first(pts[0].internal)} ↔ ${pts[0].external})`};
  if(e.dormant) return {cls:'warm', txt:`Re-warm — ${e.dormant.internal[0]} knew them, last touch ${fmtD(e.dormant.last)}`};
  const b=(e.bridges||[])[0];
  if(b) return {cls:'gap', txt:`No warm path — ask ${first(b.internal)} to bridge via ${b.name}`};
  return {cls:'gap', txt:'No warm path — needs a cold door'};
}
// ---------- trip planner ----------
const METRO = {"Norrmalm":"Stockholm","Kongens Lyngby":"Copenhagen","Landshut":"Munich",
  "Bonn":"Cologne & Bonn","Cologne":"Cologne & Bonn","Saint-Jacques-de-la-Lande":"Rennes",
  "San Francisco":"SF Bay Area","Menlo Park":"SF Bay Area","Palo Alto":"SF Bay Area",
  "Mountain View":"SF Bay Area","Woodside":"SF Bay Area"};
const cityOf = e => { const c=(e.city||'').split('·')[0].trim(); return METRO[c]||c; };
const TRIPS = {};
REGIONS.forEach(r=>D.regions[r].entities.forEach(e=>{
  if(e.kind!=='fund'||!e.city) return;
  const c=cityOf(e); (TRIPS[c]=TRIPS[c]||[]).push({r,slug:e.slug});
}));
const ACCELCAT = {accelerator:1,accel:1,studio:1};

// ---------- action panel (Solve H2Cs / Build network / Geo visit) ----------
const MAILBOX = {"Gaj Rajanathan":"gajan","Harry Williams":"harry","Sam Brooks":"sam","Ronan Shally":"ronan",
  "Fergal Mullen":"fergal","David Blyghton":"david","Helena Richardson":"helena","Laurence Garrett":"laurence",
  "Irena Goldenberg":"irena","Will de Quant":"william"};
const hlMail = n => (MAILBOX[n]||(n||'').split(' ')[0].toLowerCase())+'@highlandeurope.com';
const guessEmail = (name, fmt) => {
  if(!name||!fmt||!fmt.includes('@')) return null;
  const parts=name.trim().toLowerCase().split(/\s+/); if(parts.length<2) return null;
  const first=parts[0].normalize('NFD').replace(/[̀-ͯ]/g,''),
        last=parts[parts.length-1].normalize('NFD').replace(/[̀-ͯ]/g,'').replace(/[^a-z-]/g,'');
  const [loc,dom]=fmt.split('@');
  const local=loc.replace(/first/g,first).replace(/last/g,last).replace(/\bf\b/g,first[0]).replace(/\bl\b/g,last[0]);
  return local+'@'+dom;
};
const ALLE = REGIONS.flatMap(r=>D.regions[r].entities.map(e=>({r,e})));
const metroOf = c => METRO[c]||c;
const ap = {mode:'', who:'', city:'', hsort:'uf'};

function openAP(mode){
  ap.mode=mode;
  if(!ap.who) ap.who=state.person||'';
  document.getElementById('apanel').classList.add('open');
  document.getElementById('apback').classList.add('open');
  renderAP();
}
function closeAP(){
  document.getElementById('apanel').classList.remove('open');
  document.getElementById('apback').classList.remove('open');
}
function renderAP(){
  const titles={htc:'Solve my hard-to-cracks', net:'Build my network', geo:'Geo visit'};
  document.getElementById('aptitle').textContent=titles[ap.mode]||'';
  const ctx=document.getElementById('apctx');
  ctx.innerHTML=`Acting as <select id="apwho"><option value="">All of Highland</option>`+
    D.roster.map(n=>`<option${ap.who===n?' selected':''}>${n}</option>`).join('')+`</select>`+
    (ap.mode==='geo'?` City <select id="apcity"><option value="">choose…</option>`+
      Object.keys(TRIPS).sort().map(c=>`<option${ap.city===c?' selected':''}>${c}</option>`).join('')+`</select>`:'')+
    (ap.mode==='htc'?` Sort <span class="aptog"><button data-hs="uf"${ap.hsort==='uf'?' class="on"':''}>Unframe priority</button><button data-hs="ease"${ap.hsort==='ease'?' class="on"':''}>Ease of access</button></span>`:'');
  ctx.querySelector('#apwho').addEventListener('change',ev=>{ap.who=ev.target.value;renderAP();});
  const cs=ctx.querySelector('#apcity');
  if(cs) cs.addEventListener('change',ev=>{ap.city=ev.target.value;renderAP();});
  ctx.querySelectorAll('[data-hs]').forEach(b=>b.addEventListener('click',()=>{ap.hsort=b.dataset.hs;renderAP();}));
  const body=document.getElementById('apbody');
  body.innerHTML = ap.mode==='htc'?apHtc():ap.mode==='net'?apNet():apGeo();
  body.querySelectorAll('[data-copy]').forEach(b=>b.addEventListener('click',()=>{
    navigator.clipboard?.writeText(decodeURIComponent(b.dataset.copy)); toast('Copied');}));
  body.querySelectorAll('[data-draft]').forEach(b=>b.addEventListener('click',()=>{
    const [kind,r,slug]=b.dataset.draft.split(':'); draftWidget(kind,r,slug);}));
}

function apHtc(){
  const who=ap.who, seen=new Set(), list=[];
  REGIONS.forEach(r=>(D.regions[r].htc||[]).forEach(c=>{
    if(seen.has(c.id)) return; seen.add(c.id);
    if(who && !(c.owners||[]).includes(who)) return;
    list.push({...c, region:r});
  }));
  (D.xhtc||[]).forEach(c=>{   // the rest of the Affinity H2C book — no tracked fund on the cap table
    if(seen.has(c.id)) return; seen.add(c.id);
    if(who && !(c.owners||[]).includes(who)) return;
    list.push({...c, region:null});
  });
  // ease of access = strongest live path via any backer (email-only paths count a little)
  const ease = c => Math.max(0, ...(c.investors||[]).map(i =>
    (i.best && !i.best.moved) ? (i.best.pct ?? 5) : 0));
  if(ap.hsort==='ease')
    list.sort((a,b)=> ease(b)-ease(a) || ((b.uf??-1)-(a.uf??-1)));
  else
    list.sort((a,b)=>((b.uf??-1)-(a.uf??-1)) || (ease(b)-ease(a)) || ((b.reachable?1:0)-(a.reachable?1:0)));
  if(!list.length) return `<div class="aphint">No hard-to-cracks owned by ${who||'anyone'} on the tracked lists.</div>`;
  const cards=list.slice(0,60).map(c=>{
    const best=(c.investors||[]).filter(i=>i.best&&i.best.internal)
      .map(i=>({...i.best,fund:i.name,region:i.region}))
      .sort((a,b)=>((b.pct||0)-(a.pct||0))).slice(0,3);
    const paths=best.map(p=>`<div class="appath"><b>${p.internal}</b> ↔ ${p.external||'?'} <span class="via">via ${p.fund}${p.region&&p.region!==c.region?` (${D.regions[p.region].label})`:''}${p.pct!=null?` · ${p.pct}%`:''}${p.unverified?' · unverified':''}</span></div>`).join('');
    const others=(c.others||[]).length?`<div class="apmeta">also on the cap table (untracked): ${c.others.slice(0,4).join(', ')}</div>`:'';
    const pSelf=who?best.find(p=>p.internal===who):null;   // acting user holds this door themselves
    const p0=pSelf||best.find(p=>!who||p.internal!==who)||best[0];
    let acts='';
    if(pSelf){
      const xf=(pSelf.external||'').split(' ')[0];
      const direct=`Hi ${xf} — hope all's well. We're digging into ${c.name}${c.city?` (${c.city})`:''} and I saw ${pSelf.fund} is on the cap table. Would love your read on them — and a warm line to the founders if you're open to it. Thanks!`;
      acts=`${pSelf.email?`<a href="mailto:${pSelf.email}?subject=${encodeURIComponent(c.name)}&body=${encodeURIComponent(direct)}">✉ Email ${pSelf.external} — you hold this door</a>`:''}
        <button data-copy="${encodeURIComponent(direct)}">Copy outreach</button>`;
    } else if(p0 && p0.internal){
      const ask=`Hey ${p0.internal.split(' ')[0]} — trying to crack ${c.name}${c.city?` (${c.city})`:''} and you hold our best path: ${p0.external} at ${p0.fund}${p0.pct!=null?` (${p0.pct}%)`:''}. Could you open a door / intro me?${c.uf?` Unframe rates them ${Math.round(c.uf)} combined priority.`:''} Thanks!`;
      acts=`<a href="mailto:${hlMail(p0.internal)}?subject=${encodeURIComponent('Intro to '+c.name+'?')}&body=${encodeURIComponent(ask)}">✉ Ask ${p0.internal.split(' ')[0]}</a>
        <button data-copy="${encodeURIComponent(ask)}">Copy Slack ask</button>`;
    }
    acts=`<div class="apacts">${acts}
        <a href="${affURL(c.id)}" target="_blank" rel="noopener">Affinity ↗</a></div>`;
    return `<div class="apcard"><div class="fname">${c.name}${ufBadge(c.uf)}</div>
      <div class="apmeta">${[c.city||c.country,(c.owners||[]).length?'owner: '+c.owners.map(o=>o.split(' ')[0]).join(', '):null].filter(Boolean).join(' · ')}</div>
      ${paths||'<div class="appath" style="color:var(--muted)">no warm path via any tracked backer yet</div>'}${others}${acts}</div>`;
  }).join('');
  return `<div class="aphint">${list.length} hard-to-crack compan${list.length>1?'ies':'y'}${who?` owned by ${who.split(' ')[0]}`:''}, ranked by ${ap.hsort==='ease'?'ease of access':'Unframe priority'}${list.length>60?' (showing top 60)':''} — your full Affinity hard-to-crack book, every backer matched against the 111 tracked funds. Backers we don't track yet are listed on each card; path mapping for those is coming.</div>`+cards;
}

function netAskBody(who,e,p){
  const wf=who.split(' ')[0];
  return `Hey ${p.internal.split(' ')[0]} — I'm trying to build my own line into ${e.name} and you hold our strongest path (${p.external}${p.pct!=null?`, ${p.pct}%`:''}). Could you intro me or bring me along next time? Thanks! — ${wf}`;
}
function apNet(){
  const who=ap.who;
  if(!who) return `<div class="aphint">Pick who you are above — this view is personal by design.</div>`;
  const funds=ALLE.filter(x=>x.e.kind==='fund'&&!ACCELCAT[x.e.category]);
  const byRel=(a,b)=>(b.e.relevance?.total||0)-(a.e.relevance?.total||0);
  const borrow=funds.filter(x=>personCov(x.e,who)<22&&x.e.connectivity>=50&&(x.e.points||[]).length).sort(byRel).slice(0,6);
  const ground=funds.filter(x=>x.e.connectivity<22).sort(byRel).slice(0,6);
  const bCards=borrow.map(({r,e})=>{
    const p=e.points[0];
    return `<div class="apcard"><div class="fname ${e.tier}"><span class="tdot"></span>${e.name} <span class="cc">· ${D.regions[r].label}</span></div>
      <div class="apmeta">relevance ${e.relevance?.total??'—'} · team ${e.connectivity}, you ${personCov(e,who)}</div>
      <div class="appath"><b>${p.internal}</b> holds ${p.external||'a contact'}${p.pct!=null?` <span class="via">· ${p.pct}%</span>`:''}</div>
      <div class="apacts">
        <a href="mailto:${hlMail(p.internal)}?subject=${encodeURIComponent('Intro to '+(p.external||e.name)+'?')}&body=${encodeURIComponent(netAskBody(who,e,p))}">✉ Ask ${p.internal.split(' ')[0]}</a>
        ${(p.email||p.linkedin)?`<button data-draft="b:${r}:${e.slug}">Draft direct outreach</button>`:''}
      </div><div class="apdraftwrap" id="dw-${e.slug}"></div></div>`;
  }).join('');
  const gCards=ground.map(({r,e})=>{
    const pk=(e.partners_unknown||[])[0];
    return `<div class="apcard"><div class="fname ${e.tier}"><span class="tdot"></span>${e.name} <span class="cc">· ${D.regions[r].label}</span></div>
      <div class="apmeta">relevance ${e.relevance?.total??'—'} · team coverage ${e.connectivity}</div>
      ${pk?`<div class="appath">Door: <b>${pk.name}</b>${pk.title?` <span class="via">· ${pk.title}</span>`:''}</div>`:''}
      <div class="apacts">${pk?`<button data-draft="g:${r}:${e.slug}">Draft outreach</button>`:''}
        ${(e.bridges||[]).length?`<span class="cc" style="align-self:center">or bridge via ${e.bridges[0].name} (${e.bridges[0].internal.split(' ')[0]})</span>`:''}</div>
      <div class="apdraftwrap" id="dw-${e.slug}"></div></div>`;
  }).join('');
  return `<div class="apsec">Raise your coverage — relevant funds the team can open for you</div>${bCards||'<div class="aphint">Nothing — your coverage already matches the team everywhere it matters.</div>'}
    <div class="apsec">Open new ground — relevant funds no one at Highland covers</div>${gCards||'<div class="aphint">None.</div>'}`;
}

function draftWidget(kind,r,slug){
  const e=D.regions[r].entities.find(x=>x.slug===slug); if(!e) return;
  const who=ap.who||'Will de Quant', wf=who.split(' ')[0];
  let contact='', email=null, li=null, guessed=false;
  if(kind==='b'){ const p=e.points[0]; contact=p.external||''; email=p.email||null; li=p.linkedin||null; }
  else { const pk=(e.partners_unknown||[])[0]||{}; contact=pk.name||''; li=pk.linkedin||null;
         email=guessEmail(pk.name,e.email_fmt); guessed=!!email; }
  const first=contact.split(' ')[0]||'there';
  const t0=e.uf&&(e.uf.top||[])[0];
  const emailTxt=`Hi ${first},\n\n${wf} here from Highland Europe. We follow ${e.name}'s portfolio closely${t0?` — ${t0.name} in particular has caught our eye`:''}${(e.coinvest||[]).length?`, and we've already co-invested together ${e.coinvest.length}×`:''}.\n\nWe invest €10–50m growth rounds across Europe and often follow on from your stage, so I'd love to compare notes on where our pipelines overlap. 20 minutes in the coming weeks?\n\nBest,\n${wf}`;
  const liTxt=`Hi ${first} — ${wf} @ Highland Europe (growth). We track ${e.name}'s book closely${t0?`, ${t0.name} especially`:''}, and often follow on from your stage. Would be great to connect.`;
  const wrap=document.getElementById('dw-'+slug); if(!wrap) return;
  const cline=[email?`<span>${email}${guessed?' <span class="guess">· guessed from '+e.email_fmt+'</span>':''}</span>`:null,
               li?`<a href="${li}" target="_blank" rel="noopener">LinkedIn ↗</a>`:null]
              .filter(Boolean).join(' · ')||'<span class="guess">no verified contact details</span>';
  wrap.innerHTML=`<div class="apdraft">
    <div class="aptog"><button class="on" data-m="email">Email</button><button data-m="li">LinkedIn</button></div>
    <div class="apcontact">To: <b>${contact||'—'}</b> · ${cline}</div>
    <textarea id="ta-${slug}">${emailTxt}</textarea>
    <div class="apacts" style="margin-top:6px">
      ${email?`<a id="ml-${slug}" href="#">✉ Open in email</a>`:''}
      <button id="cp-${slug}">Copy</button>
    </div></div>`;
  const ta=wrap.querySelector('#ta-'+CSS.escape(slug));
  let mode='email';
  const ml=wrap.querySelector('#ml-'+CSS.escape(slug));
  const syncMail=()=>{ if(ml) ml.href=`mailto:${email}?subject=${encodeURIComponent('Highland Europe ✕ '+e.name)}&body=${encodeURIComponent(ta.value)}`; };
  syncMail(); if(ta) ta.addEventListener('input',syncMail);
  wrap.querySelectorAll('.aptog button').forEach(b=>b.addEventListener('click',()=>{
    wrap.querySelectorAll('.aptog button').forEach(x=>x.classList.remove('on')); b.classList.add('on');
    mode=b.dataset.m; ta.value = mode==='email'?emailTxt:liTxt; syncMail();
    if(ml) ml.style.display = mode==='email'?'':'none';
  }));
  wrap.querySelector('#cp-'+CSS.escape(slug)).addEventListener('click',()=>{
    navigator.clipboard?.writeText(ta.value); toast('Copied');});
}

function apGeo(){
  const city=ap.city;
  if(!city) return `<div class="aphint">Pick a city above — e.g. Stockholm.</div>`;
  const who=ap.who;
  const anyCity = ALLE.some(({e})=>Object.values(e.buckets||{}).some(l=>l.some(p=>p.city)));
  const seen=new Map();
  ALLE.forEach(({r,e})=>{Object.values(e.buckets||{}).forEach(lst=>lst.forEach(p=>{
    if(!p.city||metroOf(p.city)!==city) return;
    if(who&&!(p.own||[]).includes(who)) return;
    const cur=seen.get(p.id);
    if(cur){cur.via.add(e.name); if(p.uf&&!cur.uf)cur.uf=p.uf;}
    else seen.set(p.id,{...p, via:new Set([e.name])});
  }));});
  const pipe=[...seen.values()].sort((a,b)=>(b.uf??-1)-(a.uf??-1)).slice(0,25);
  const rows=pipe.map(p=>`<div class="aprow"><a href="${affURL(p.id)}" target="_blank" rel="noopener"><b>${p.name}</b></a>${ufBadge(p.uf)}<span class="cc">${(p.funnel||'').replace(' (free for all)','')}</span>${!who&&(p.own||[]).length?`<span class="cc">${p.own.map(o=>o.split(' ')[0]).join(', ')}</span>`:''}</div>`).join('');
  const inCity=ALLE.filter(x=>x.e.kind==='fund'&&cityOf(x.e)===city);
  const know=[], cold=[];
  inCity.forEach(({r,e})=>{const pc=who?personCov(e,who):e.connectivity; (pc>0?know:cold).push({r,e,pc});});
  know.sort((a,b)=>b.pc-a.pc);
  cold.sort((a,b)=>((ACCELCAT[a.e.category]?1:0)-(ACCELCAT[b.e.category]?1:0))||((b.e.relevance?.total||0)-(a.e.relevance?.total||0)));
  const kRows=know.map(({e,pc})=>{
    const sig=who?personSignal(e,who):null; const k=sig&&sig.contacts&&sig.contacts[0];
    const line=k?`<b>${k.person}</b>${k.pct!=null?` <span class="via">· ${k.pct}%</span>`:''}${evidence(k)?` <span class="via">· ${evidence(k)}</span>`:''}`
      :(e.points&&e.points[0]?`<b>${e.points[0].external||''}</b> <span class="via">via ${e.points[0].internal}</span>`:'');
    return `<div class="apcard"><div class="fname ${e.tier}"><span class="tdot"></span>${e.name}</div>
      <div class="apmeta">relevance ${e.relevance?.total??'—'} · ${who?`your coverage ${pc}`:`team ${e.connectivity}`}</div>
      ${line?`<div class="appath">Reconnect: ${line}</div>`:''}</div>`;}).join('');
  const cRows=cold.map(({e})=>{
    const nm2=nextMove(e)||{cls:'gap',txt:''}; const pk=(e.partners_unknown||[])[0];
    return `<div class="apcard"><div class="fname ${e.tier}"><span class="tdot"></span>${e.name}${ACCELCAT[e.category]?' <span class="cc">· accelerator</span>':''}</div>
      <div class="apmeta">relevance ${e.relevance?.total??'—'}${who?` · team ${e.connectivity}`:''}</div>
      <div class="nm ${nm2.cls}">${nm2.txt}</div>
      ${pk?`<div class="apmeta">Door: ${pk.linkedin?`<a href="${pk.linkedin}" target="_blank" rel="noopener">${pk.name}</a>`:pk.name}${pk.title?` · ${pk.title}`:''}</div>`:''}</div>`;}).join('');
  return `<div class="apsec">${who?who.split(' ')[0]+"'s":'Our'} pipeline in ${city} — ranked by Unframe priority</div>
    ${rows||`<div class="aphint">${anyCity?`No ${who?who.split(' ')[0]+"'s":''} pipeline companies with a known ${city} HQ.`:'City data is still backfilling — check back shortly.'}</div>`}
    <div class="apsec">Investors ${who?'you know':'we know'} here — reconnect</div>${kRows||'<div class="aphint">None yet.</div>'}
    <div class="apsec">Funds ${who?"you don't know":'we barely know'} — prioritise</div>${cRows||'<div class="aphint">None.</div>'}`;
}
function headHTML(){
  return `<thead><tr>`+COLS.map(c=>{
    const label = c.k==='mycov' ? `${state.person?state.person.split(' ')[0]+"’s":'My'} coverage` : c.label;
    return `<th data-k="${c.k}" class="${c.sortable?'sortable':''} ${state.sort===c.k?'on':''} ${c.cls||''}">${label}</th>`;
  }).join('')+`</tr></thead>`;
}
function chipHTML(e, mode){
  if(mode==='mine'){  // only the person's own entries at this investor
    const chips = BUCKETS.map(([k,label])=>{
      const own = e.buckets[k].filter(isOwned).length;
      return own?`<span class="chip ${k}" data-k="${k}"><b>${own}</b> ${label}</span>`:'';
    }).join('');
    return chips || `<span class="nochip">none of yours</span>`;
  }
  if(mode!=='team' && state.person){  // mobile cards: own count vs team count, side by side
    const chips = BUCKETS.map(([k,label])=>{
      const team = e.buckets[k].length; if(!team) return '';
      const own = e.buckets[k].filter(isOwned).length;
      return `<span class="chip ${k}${own?'':' dim'}" data-k="${k}"><b>${own}</b><span class="of">/${team}</span> ${label}</span>`;
    }).join('');
    return chips || `<span class="nochip">no pipeline overlap</span>`;
  }
  return BUCKETS.map(([k,label])=>{
    const n = e.buckets[k].length;
    return n?`<span class="chip ${k}" data-k="${k}"><b>${n}</b> ${label}</span>`:'';
  }).join('') || `<span class="nochip">no pipeline overlap</span>`;
}
const liSearch = (n,f) => `https://www.linkedin.com/search/results/people/?keywords=${encodeURIComponent(n+' '+(f||''))}`;
const emIcon = p => {
  const em = p.email || p.email_guess;
  if(!em) return '';
  return `<span class="em${p.email?'':' guess'}" data-em="${em}"${p.email?'':' data-guess="1"'}>✉</span>`;
};
const evidence = o => o.meet?`met ${fmtD(o.meet)}`:(o.last?`em ${fmtD(o.last)}`:null);
function pathLine(p, ctx){
  const nm = `<a href="${p.linkedin||liSearch(p.external,ctx)}" target="_blank" rel="noopener"><b>${p.external}</b></a>`;
  const ev = evidence(p);
  const when = ev?`<span class="when">${ev}</span>`:'';
  const moved = p.moved?` <span class="flag" data-moved="${p.moved}">⚠</span>`:'';
  const stale = p.last && isStale(p.last) ? ' stale' : '';
  const uv = p.unverified?` <span class="uvtag">unverified · email-only</span>`:'';
  const bar = p.pct!=null?`<span class="sbar"><i style="width:${p.pct}%"></i></span>`:'';
  return `<span class="pt${stale}"><span class="ptl">${nm} <span class="via">↔ ${avi(p.internal)} ${p.internal}</span>${p.email?emIcon(p):''}${moved}${uv}</span><span class="ptr">${bar}${p.pct!=null?`<span class="pct">${p.pct}%</span>`:''}${when}</span></span>`;
}
function ptsHTML(e){
  const v = eff(e);
  if(state.person){
    const s = v.sig;
    const dormP = s.dorm ? `<span class="pt dorm" title="${s.dorm.context}">⏱ dormant · last touch ${s.dorm.last}</span>` : '';
    let mine = s.contacts.map(k=>{
      const nm = `<a href="${k.linkedin||liSearch(k.person,e.name)}" target="_blank" rel="noopener"><b>${k.person}</b></a>`;
      const extra = (k.email?emIcon(k):'')+(k.title?` <span class="via">· ${k.title}</span>`:'')+(k.pct!=null?` <span class="pct">${k.pct}%</span>`:'');
      const ev = evidence(k);
      const when = ev?` <span class="when">· ${ev}</span>`:'';
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
  const nm = nextMove(e);
  const nmH = nm ? `<div class="nm ${nm.cls}">${nm.txt}</div>` : '';
  if(!e.points.length && !dorm && !bridges) return `<div class="pts">${nmH||`<span style="color:var(--muted)">No mapped way in yet</span>`}</div>`;
  return `<div class="pts">`+nmH+e.points.map(p=>pathLine(p,e.name)).join('')+dorm+bridges+`</div>`;
}
function bridgeLines(e){
  return (e.bridges||[]).slice(0,2).map(b=>
    `<span class="pt bridge">↪ via <b>${b.name}</b> <span class="via">(${b.internal}${b.pct!=null?' · '+b.pct+'%':''})</span></span>`);
}
const ufBadge = s => s==null?'':` <span class="ufb ${s>=85?'hi':s>=70?'mid':'lo'}" title="Unframe combined priority ${Math.round(s)}/100">${Math.round(s)}</span>`;
const AVI_COLORS=['#2733f0','#0e7a4a','#a05a00','#7a2e8a','#b3403a','#11607a','#5a5a2e','#8a2e55'];
const avi = n => {
  const init=(n||'').split(' ').filter(Boolean).map(w=>w[0]).slice(0,2).join('').toUpperCase();
  let h=0; for(const ch of n||'') h=(h*31+ch.charCodeAt(0))>>>0;
  return `<span class="avi" style="background:${AVI_COLORS[h%AVI_COLORS.length]}" title="${n}">${init}</span>`;
};
const STAGE_SHORT = {prelead:'Pre-lead', reachout:'Reach', awaiting:'Await', lead:'Lead', hard:'H2C'};
function covCardHTML(e, mine){
  if(mine && !state.person) return `<span class="nochip">pick who you are ↑</span>`;
  const v = mine ? eff(e) : {cov:e.connectivity, tier:e.tier};
  const cols = BUCKETS.map(([k,label])=>{
    const n = mine ? e.buckets[k].filter(isOwned).length : e.buckets[k].length;
    return `<div class="cst${n?'':' z'}" title="${n} ${label}"><b>${n}</b><i style="background:var(--c-${k}-ink)"></i><span>${STAGE_SHORT[k]}</span></div>`;
  }).join('');
  return `<div class="covcard${mine?' mine':''}">
    <div class="covhead"><b class="covnum ${v.tier}">${v.cov}</b><span class="covcap">${mine?'my':'team'} coverage</span></div>
    <div class="covrow">${cols}</div></div>`;
}
function rowHTML(e){
  const v = eff(e);
  const rel = e.relevance? e.relevance.total : null;
  const co = e.coinvest.length?`<span class="badge co">✓ co-invested ×${e.coinvest.length}</span>`:'';
  const ufq = e.uf && e.uf.pts ? `<span class="badge ufq${e.uf.high?' hi':''}" title="Unframe portfolio quality ${e.uf.pts}/40 — ${e.uf.high} backed companies rated ≥85 combined priority, top-10 avg ${e.uf.avg10}">Unframe ${e.uf.pts}/40${e.uf.high?` · ${e.uf.high} high-prio`:''}</span>`:'';
  const unt = (e.untracked||[]).length?`<span class="badge unt">${e.untracked.length} untracked EU deals</span>`:'';
  const lastT = e.fund_last?`<span>last touch ${fmtD(e.fund_last)}</span>`:'';
  const noCrm = e.no_crm?`<a class="badge" href="${e.harmonic_url}" target="_blank" rel="noopener">no CRM record · Harmonic ↗</a>`:'';
  const known = e.kind==='angel' && (e.notable||[]).length
    ? `<span class="cc">known for: ${e.notable.slice(0,3).map(n=>n.name).join(', ')}</span>` : '';
  const meta = e.kind==='fund'
    ? `<span class="badge">${e.category.toUpperCase()}</span><span>${e.city||''}</span>${lastT}${co}${ufq}${unt}`
    : `<span>${e.note||''}</span>${known}${lastT}${noCrm}`;
  const nm = e.kind==='angel' && e.li ? `<a href="${e.li}" target="_blank" rel="noopener">${e.name}</a>`
    : e.website ? `<a href="https://${e.website}" target="_blank" rel="noopener">${e.name}</a>` : e.name;
  const relCell = `<b>${rel??'—'}</b><span class="rb"><i style="width:${rel||0}%"></i></span>`;
  const proof = e.kind==='fund' && e.uf && (e.uf.top||[]).length
    ? `<div class="fmeta ufproof"><span class="cc">Top of portfolio:</span>`+
      e.uf.top.map(t=>`<span class="ufco">${t.domain?`<a href="https://${t.domain}" target="_blank" rel="noopener">${t.name}</a>`:t.name}${ufBadge(t.score)}</span>`).join('')+`</div>` : '';
  return `<tr class="mainrow" data-slug="${e.slug}" tabindex="0">
    <td><div class="fname ${v.tier}"><span class="tdot"></span>${nm}</div><div class="fmeta">${meta}</div>${proof}</td>
    <td class="relcell">${relCell}</td>
    <td class="covtd">${covCardHTML(e, false)}</td>
    <td class="covtd mytd">${covCardHTML(e, true)}</td>
    <td>${ptsHTML(e)}</td>
  </tr>
  <tr class="detailrow" id="d-${e.slug}"><td colspan="5"><div class="detail"></div></td></tr>`;
}
function detailHTML(e){
  let h='';
  if(e.liveAt) h += `<div class="meta-line"><span class="livebadge">${liveLabel(e)}</span> <span class="cc">${window.claude?'pipeline refreshed from your Affinity connector':'checked live against Affinity & Harmonic just now'}</span></div>`;
  if(e.kind==='fund'){
    const r=e.relevance;
    h += `<div class="meta-line">Relevance ${r.total} (stage ${r.stage} · sector ${r.sector} · ${r.eu_deals!=null?`EU activity ${r.geo} · ${r.eu_deals} EU deals/24m`:`Europe ${r.geo} at ${Math.round(r.europe)}%`} · activity ${r.activity} · graduation ${r.grad})
      · ${e.num_investments??'—'} investments · ${e.unicorns??0} unicorns · last investment ${e.last_investment||'—'}
      ${e.coinvest.length?` · <b style="color:var(--covered-ink)">co-invested:</b> ${e.coinvest.join(', ')}`:''}</div>`;
    if(e.uf && (e.uf.top||[]).length){
      h += `<div class="meta-line"><b>Top of their portfolio</b> <span class="cc">· Unframe combined priority</span> &nbsp;`+
        e.uf.top.map(t=>`${t.domain?`<a href="https://${t.domain}" target="_blank" rel="noopener">${t.name}</a>`:`<b>${t.name}</b>`}${ufBadge(t.score)}${t.tracking==='not_tracked'?' <span class="cc">not in Affinity</span>':''}`).join(' &nbsp;·&nbsp; ')+`</div>`;
    }
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
  const pitem = (p,cls) => `<span${cls?` class="${cls}"`:''}><a href="${affURL(p.id)}" target="_blank" rel="noopener">${p.name}</a>${ufBadge(p.uf)}${(p.own||[]).length?` <span class="cc">${p.own.map(o=>o.split(' ')[0]).join(', ')}</span>`:''}</span>`;
  for(const [k,label] of secs){
    let list=e.buckets[k]; if(!list||!list.length) continue;
    list = list.slice().sort((a,b)=>(b.uf??-1)-(a.uf??-1));  // Unframe-rated first, highest priority leading
    if(state.person){
      const own = list.filter(isOwned), rest = list.filter(p=>!isOwned(p));
      const fn = state.person.split(' ')[0];
      h += `<details class="sec" id="sec-${e.slug}-${k}"><summary>${label} <b>${own.length}</b><span class="cnt">of ${list.length} team-wide owned by ${fn}</span></summary>`+
        (own.length?`<div class="pgroup mine"><div class="pglabel">${fn}'s</div><div class="plist">`+own.map(p=>pitem(p,'')).join('')+`</div></div>`:'')+
        (rest.length?`<div class="pgroup"><div class="pglabel">Rest of the team</div><div class="plist">`+rest.map(p=>pitem(p,'offr')).join('')+`</div></div>`:'')+
        `</details>`;
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
          const bits = [k.title, k.pct!=null?`${k.pct}%`:null, evidence(k)].filter(Boolean).join(' · ');
          const uv = k.unverified?` <span class="uvtag">unverified · email-only</span>`:'';
          return `<div>${nm}${k.email?emIcon(k):''}<span class="t">${bits?` · ${bits}`:''}</span>${uv}</div>`;
        }).join('')+`</div>`;
    }).join('')+`</div>`;
    if(e.former && e.former.length){
      h += `<div class="meta-line" style="color:var(--muted)">No longer at ${e.name}: `+
        e.former.map(f=>`${f.person} → ${f.now}`).join(' · ')+`</div>`;
    }
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
  {const pr = 'Use the fund-portfolio-prep skill: prep my meeting with '+e.name;
  h += `<div class="actionrow" style="margin-top:14px"><a class="minibtn prep" href="https://claude.ai/new?q=${encodeURIComponent(pr)}" target="_blank" rel="noopener">⚡ Prep brief in Claude</a><span class="cc" style="align-self:center">prefills the prep request — just hit send</span></div>`;}
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
  if(state.person) rows = rows.filter(c=>(c.owners||[]).includes(state.person));
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
  const nm = nextMove(e);
  if(nm) return `<div class="mpath nm ${nm.cls}">${nm.txt}</div>`;
  const p0 = e.points && e.points[0];
  if(p0) return `<div class="mpath"><b>${p0.external}</b>${p0.email?emIcon(p0):''} <span class="via">↔ ${p0.internal}</span>${p0.pct!=null?` <span class="pct">${p0.pct}%</span>`:''}${p0.moved?' <span class="flag">⚠</span>':''}</div>`;
  if(e.dormant) return `<div class="mpath dorm">⏱ <b>${e.dormant.internal.join(' + ')}</b> dormant · ${e.dormant.last}</div>`;
  if(e.bridges && e.bridges.length) return `<div class="mpath">↪ via <b>${e.bridges[0].name}</b> <span class="via">(${e.bridges[0].internal})</span></div>`;
  return `<div class="mpath" style="color:var(--muted)">No mapped way in yet</div>`;
}
function mCardHTML(e){
  const v = eff(e); const rel = e.relevance?e.relevance.total:null;
  const meta = e.kind==='fund'
    ? `<span class="badge">${e.category.toUpperCase()}</span><span>${(e.city||'').split('·')[0].trim()}</span>${rel!=null?`<span>rel ${rel}</span>`:''}${e.uf&&e.uf.pts?`<span class="badge ufq${e.uf.high?' hi':''}">UF ${e.uf.pts}/40${e.uf.high?` · ${e.uf.high} hi-prio`:''}</span>`:''}${(e.untracked||[]).length?`<span class="badge unt">${e.untracked.length} untracked</span>`:''}`
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
  if(state.view==='unt'){
    const seg = `<div class="seg" id="msegunt" style="display:inline-flex;margin-bottom:10px">
      <button data-um="fund"${state.untMode==='fund'?' class="on"':''}>By fund</button>
      <button data-um="company"${state.untMode==='company'?' class="on"':''}>By company</button></div>`;
    const bodyHtml = state.untMode==='company' ? mUntCompanyCards() : mUntCards();
    el.innerHTML = seg + (bodyHtml || '<div class="mpath" style="color:var(--muted)">Nothing matches.</div>');
    el.querySelectorAll('#msegunt button').forEach(b=>b.addEventListener('click',()=>{
      state.untMode=b.dataset.um; renderMobile();}));
    el.querySelectorAll('.suntchip').forEach(c=>c.addEventListener('click',()=>{
      const k=c.dataset.sk;
      if(state.untSort.k===k) state.untSort.d*=-1; else state.untSort={k,d:-1};
      renderMobile();}));
    bindAddAff(el);
    return;
  }
  if(state.view==='htc'){
    let rows = D.regions[state.region].htc;
    if(state.person) rows = rows.filter(c=>(c.owners||[]).includes(state.person));
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

// ---------- untracked dealflow view ----------
const fmtMoney = v => (v==null||v===0)?'\u2014':v>=995e6?('$'+(v/1e9).toFixed(1)+'B'):v>=1e6?('$'+Math.round(v/1e6)+'M'):('$'+Math.round(v/1e3)+'K');
const fmtStage = st => (st||'').replaceAll('_',' ').toLowerCase().replace(/(^|\s)\S/g, c=>c.toUpperCase()).replace('Pre Seed','Pre-seed') || '\u2014';
function untFunds(){
  let fs = E().filter(e=>e.kind==='fund' && (e.untracked||[]).length);
  if(state.q) fs = fs.filter(e=>e.name.toLowerCase().includes(state.q)
    || (e.untracked||[]).some(u=>(u.name||'').toLowerCase().includes(state.q)));
  return fs.sort((a,b)=>(b.untracked||[]).length-(a.untracked||[]).length);
}
const growthColor = pct => {
  const t = (Math.max(-25, Math.min(100, pct)) + 25) / 125;   // -25% -> 0, 100%+ -> 1
  return `hsl(${Math.round(8 + t*(145-8))},60%,30%)`;         // dark red -> dark green
};
const growthHTML = hg => hg&&hg.pct!=null
  ? ` <span style="color:${growthColor(hg.pct)};font-weight:650">${hg.pct>0?'+':''}${Math.round(hg.pct)}%</span>` : '';
const untURL = u => u.domain ? `https://${u.domain}`
  : `https://console.harmonic.ai/dashboard/company/${u.harmonic_company_id}`;
const harmBtn = u => `<a class="minibtn" href="https://console.harmonic.ai/dashboard/company/${u.harmonic_company_id}" target="_blank" rel="noopener">Harmonic ↗</a>`;
const affBtn = (p,u) => p.affinity_id
  ? `<a class="minibtn" href="https://${D.affinityOrg}.affinity.co/companies/${p.affinity_id}" target="_blank" rel="noopener">Affinity \u2197</a>`
  : `<button class="minibtn addaff" data-dom="${u.domain||''}" data-nm="${u.name}">\uff0b Affinity</button>`;
function untCompanyRows(e){
  const prof = D.untProfiles||{};
  return (e.untracked||[]).slice().sort((a,b)=>((b.uf??-1)-(a.uf??-1)) || (b.date||'').localeCompare(a.date||'')).map(u=>{
    const p = prof[u.harmonic_company_id]||prof[String(u.harmonic_company_id)]||{};
    const founders = (p.founders||[]).slice(0,3).map(f=>
      `${f.linkedin?`<a href="${f.linkedin}" target="_blank" rel="noopener">${f.name}</a>`:f.name}<span class="cc">${f.title?` \u00b7 ${f.title.replace('Co-Founder','Co-founder')}`:''}</span>`).join('<br>')||'<span class="cc">\u2014</span>';
    return `<tr>
      <td><a href="${untURL(u)}" target="_blank" rel="noopener"><b>${u.name}</b></a>${ufBadge(u.uf)}<div class="fmeta" style="padding-left:0">${p.hq||u.country||''}</div></td>
      <td class="udesc">${p.desc||''}</td>
      <td style="white-space:nowrap">${fmtStage(p.stage||u.round)}</td>
      <td class="num">${(u.date||'').slice(0,7)||'\u2014'}</td>
      <td class="num">${fmtMoney(p.funding_total_usd)}</td>
      <td class="num" style="white-space:nowrap">${p.headcount!=null?`<b class="hc">${p.headcount}</b>`:'\u2014'}${growthHTML(p.headcount_growth)}</td>
      <td>${founders}</td>
      <td><span class="btnstack">${harmBtn(u)}${affBtn(p,u)}</span></td>
    </tr>`;
  }).join('');
}
function untCompanies(){
  const prof = D.untProfiles||{};
  const by = new Map();
  E().filter(e=>e.kind==='fund'&&(e.untracked||[]).length).forEach(e=>{
    (e.untracked||[]).forEach(u=>{
      const id = u.harmonic_company_id;
      let r = by.get(id);
      if(!r){ r = {u, p: prof[id]||prof[String(id)]||{}, invs:[]}; by.set(id, r); }
      if(!r.invs.includes(e.name)) r.invs.push(e.name);
      if((u.date||'') > (r.u.date||'')) r.u = u;
    });
  });
  let rows = [...by.values()];
  if(state.q) rows = rows.filter(r=>(r.u.name||'').toLowerCase().includes(state.q)
    || (r.p.desc||'').toLowerCase().includes(state.q)
    || r.invs.some(n=>n.toLowerCase().includes(state.q)));
  if(state.untHC) rows = rows.filter(r=>(r.p.headcount||0)>=state.untHC);
  if(state.untGR!=null) rows = rows.filter(r=>r.p.headcount_growth && r.p.headcount_growth.pct>state.untGR);
  const key = r => ({date: r.u.date||'', raised: r.p.funding_total_usd||0,
    hc: r.p.headcount!=null?r.p.headcount:-1,
    gr: (r.p.headcount_growth&&r.p.headcount_growth.pct!=null)?r.p.headcount_growth.pct:-1e9,
    uf: r.u.uf??-1,
    name: (r.u.name||'').toLowerCase()})[state.untSort.k];
  rows.sort((a,b)=>{const ka=key(a),kb=key(b); return (ka<kb?-1:ka>kb?1:0)*state.untSort.d;});
  return rows;
}
function untCompanyTable(){
  const rows = untCompanies();
  document.getElementById('unthint').textContent =
    `${rows.length} untracked ${D.regions[state.region].label} companies \u2014 click a column header to sort`;
  const arrow = k => state.untSort.k===k ? (state.untSort.d<0?' \u25be':' \u25b4') : '';
  const th = (label,k) => `<th class="sk" data-sk="${k}">${label}${arrow(k)}</th>`;
  const body = rows.map(r=>{
    const p=r.p, u=r.u;
    const seenF = new Set();
    const founders = (p.founders||[]).filter(f=>f.name && !seenF.has(f.name) && seenF.add(f.name)).slice(0,2).map(f=>
      f.linkedin?`<a href="${f.linkedin}" target="_blank" rel="noopener">${f.name}</a>`:f.name).join(' \u00b7 ')||'<span class="cc">\u2014</span>';
    return `<tr>
      <td><a href="${untURL(u)}" target="_blank" rel="noopener"><b>${u.name}</b></a><div class="fmeta" style="padding-left:0">${p.hq||u.country||''}</div></td>
      <td class="udesc">${p.desc||''}</td>
      <td class="ubak" style="font-size:12px;color:var(--ink2)">${r.invs.join(', ')}</td>
      <td class="num">${ufBadge(u.uf)||'—'}</td>
      <td style="white-space:nowrap">${fmtStage(p.stage||u.round)}</td>
      <td class="num">${(u.date||'').slice(0,7)||'\u2014'}</td>
      <td class="num">${fmtMoney(p.funding_total_usd)}</td>
      <td class="num">${p.headcount!=null?`<b class="hc">${p.headcount}</b>`:'\u2014'}</td>
      <td class="num" style="white-space:nowrap">${growthHTML(p.headcount_growth)||'\u2014'}</td>
      <td class="ufo">${founders}</td>
      <td><span class="btnstack">${harmBtn(u)}${affBtn(p,u)}</span></td></tr>`;
  }).join('');
  const tbl = document.getElementById('unttable');
  tbl.className = 'df';
  tbl.innerHTML = `<thead><tr>${th('Company','name')}<th>What they do</th><th>Backed by</th>${th('Unframe','uf')}<th>Stage</th>${th('Latest round','date')}${th('Raised','raised')}${th('FTE','hc')}${th('Growth','gr')}<th>Founders / CEO</th><th></th></tr></thead>
    <tbody>${body||`<tr><td colspan="11" style="color:var(--muted)">Nothing matches.</td></tr>`}</tbody>`;
  tbl.querySelectorAll('th.sk').forEach(h=>h.addEventListener('click',()=>{
    const k = h.dataset.sk;
    if(state.untSort.k===k) state.untSort.d*=-1;
    else state.untSort = {k, d: k==='name'?1:-1};
    untCompanyTable();
  }));
  bindAddAff(tbl);
}
function untHTML(){
  document.getElementById('untfilters').hidden = state.untMode!=='company';
  if(state.untMode==='company'){ untCompanyTable(); return; }
  document.getElementById('unttable').className = '';
  const fs = untFunds();
  const total = fs.reduce((n,e)=>n+e.untracked.length,0);
  document.getElementById('unthint').textContent =
    `${total} recent deals by tracked ${D.regions[state.region].label} investors with no Affinity record \u2014 click a fund`;
  const body = fs.map(e=>{
    const v = eff(e);
    const latest = e.untracked.reduce((m,u)=>(u.date||'')>m?u.date:m,'');
    const preview = e.untracked.slice(0,3).map(u=>u.name).join(', ');
    return `<tr class="mainrow" data-uslug="${e.slug}" tabindex="0">
      <td><div class="fname ${v.tier}"><span class="tdot"></span>${e.name}</div>
        <div class="fmeta"><span class="badge">${e.category.toUpperCase()}</span><span>${(e.city||'').split('\u00b7')[0].trim()}</span></div></td>
      <td><span class="badge unt">${e.untracked.length} untracked</span></td>
      <td class="num">${latest?latest.slice(0,7):'\u2014'}</td>
      <td style="font-size:12px;color:var(--ink2)">${preview}${e.untracked.length>3?` <span class="cc">+${e.untracked.length-3} more</span>`:''}</td>
    </tr>
    <tr class="detailrow" id="ud-${e.slug}"><td colspan="4"><div class="detail"><div class="dfwrap"><table class="df">
      <thead><tr><th>Company</th><th>What they do</th><th>Stage</th><th>Latest round</th><th>Raised</th><th>Headcount</th><th>Founders / CEO</th><th></th></tr></thead>
      <tbody>${untCompanyRows(e)}</tbody></table></div></div></td></tr>`;
  }).join('');
  document.getElementById('unttable').innerHTML =
    `<thead><tr><th>Investor</th><th>Untracked deals</th><th>Most recent</th><th>Latest companies</th></tr></thead><tbody>${body||'<tr><td colspan="4" style="color:var(--muted)">Nothing matches.</td></tr>'}</tbody>`;
  const tbl = document.getElementById('unttable');
  tbl.querySelectorAll('tr.mainrow').forEach(r=>{
    const open = ev=>{ if(ev.target.closest('a')||ev.target.closest('.addaff')) return;
      const det = document.getElementById('ud-'+r.dataset.uslug);
      const was = det.classList.contains('open');
      tbl.querySelectorAll('tr.detailrow.open').forEach(x=>x.classList.remove('open'));
      if(!was) det.classList.add('open');
    };
    r.addEventListener('click', open);
    r.addEventListener('keydown', ev=>{ if(ev.key==='Enter') open(ev); });
  });
  bindAddAff(tbl);
}
function bindAddAff(root){
  root.querySelectorAll('.addaff').forEach(b=>b.addEventListener('click',ev=>{
    ev.stopPropagation();
    const v = b.dataset.dom || b.dataset.nm;
    navigator.clipboard?.writeText(v);
    toast(`Copied ${v} \u2014 paste into Affinity's Add Company`);
    window.open(`https://${D.affinityOrg}.affinity.co/lists/9387`,'_blank');
  }));
}
function mUntCards(){
  const prof = D.untProfiles||{};
  return untFunds().map(e=>{
    const cards = e.untracked.map(u=>{
      const p = prof[u.harmonic_company_id]||prof[String(u.harmonic_company_id)]||{};
      return `<div class="mcard">
        <div class="mtop"><div class="fname"><a href="${untURL(u)}" target="_blank" rel="noopener">${u.name}</a></div>
          <span class="cc">${(u.date||'').slice(0,7)}</span></div>
        ${p.desc?`<div class="mpath" style="color:var(--ink2)">${p.desc}</div>`:''}
        <div class="mmeta"><span>${p.hq||u.country||''}</span><span>${fmtStage(p.stage||u.round)}</span><span>${fmtMoney(p.funding_total_usd)}</span>${p.headcount!=null?`<span><b class="hc">${p.headcount}</b> ppl${growthHTML(p.headcount_growth)}</span>`:''}</div>
        ${(p.founders||[]).length?`<div class="mpath">${p.founders.map(f=>f.linkedin?`<a href="${f.linkedin}" target="_blank" rel="noopener">${f.name}</a>`:f.name).join(' \u00b7 ')}</div>`:''}
        <div class="actionrow">${harmBtn(u)} ${affBtn(p,u)}</div>
      </div>`;
    }).join('');
    return `<details class="munt"${state.q?' open':''}><summary><span class="fname">${e.name}</span><span class="badge unt">${e.untracked.length} untracked</span></summary><div class="muntbody">${cards}</div></details>`;
  }).join('');
}
function mUntCompanyCards(){
  const sorts = [['uf','Unframe'],['date','Newest'],['hc','FTE'],['gr','Growth'],['raised','Raised']];
  const chips = `<div class="mchips" style="padding-left:0;margin-bottom:12px">`+
    sorts.map(([k,l])=>`<span class="chip suntchip${state.untSort.k===k?' on':''}" data-sk="${k}">${l}${state.untSort.k===k?(state.untSort.d<0?' ▾':' ▴'):''}</span>`).join('')+`</div>`;
  const cards = untCompanies().map(r=>{
    const p=r.p, u=r.u;
    return `<div class="mcard" style="cursor:default">
      <div class="mtop"><div class="fname"><a href="${untURL(u)}" target="_blank" rel="noopener">${u.name}</a>${ufBadge(u.uf)}</div>
        <span class="cc">${(u.date||'').slice(0,7)}</span></div>
      ${p.desc?`<div class="mpath" style="color:var(--ink2)">${p.desc}</div>`:''}
      <div class="mmeta"><span>${p.hq||u.country||''}</span><span>${fmtStage(p.stage||u.round)}</span><span>${fmtMoney(p.funding_total_usd)}</span>${p.headcount!=null?`<span><b class="hc">${p.headcount}</b> ppl${growthHTML(p.headcount_growth)}</span>`:''}</div>
      <div class="mpath cc">Backed by ${r.invs.join(', ')}</div>
      <div class="actionrow">${harmBtn(u)} ${affBtn(p,u)}</div>
    </div>`;
  }).join('');
  return chips+cards;
}

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
  if(e.kind!=='fund') return;
  if(!window.claude || window.claude.mcp===undefined){ startWebLive(e); return; }
  if(!e.liveTerm) return;
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
// ---------- website live path: same-origin /api/live (Affinity + Harmonic) ----------
function startWebLive(e){
  if(location.protocol!=='https:' && location.protocol!=='http:') return;
  if(!e._baked) e._baked = JSON.parse(JSON.stringify(e.buckets));
  const tick = () => webLiveTick(e).catch(()=>{});
  tick();
  const iv = setInterval(()=>{ if(liveSub && liveSub.slug===e.slug) tick(); }, 120000);
  liveSub = {slug: e.slug, unsub: ()=>clearInterval(iv)};
}
async function webLiveTick(e){
  const idSet = new Set();
  for(const k in e.buckets) for(const p of e.buckets[k]) if(p.id) idSet.add(p.id);
  const ids = [...idSet].slice(0,60);
  const doms = [...new Set((e.untracked||[]).map(u=>u.domain).filter(Boolean))].slice(0,25);
  if(!ids.length && !doms.length) return;
  const r = await fetch(`/api/live?ids=${ids.join(',')}&domains=${encodeURIComponent(doms.join(','))}`);
  if(!r.ok){ if(r.status===401||r.status===503) e.liveOff = true; return; }
  const d = await r.json();
  if(!liveSub || liveSub.slug!==e.slug) return;
  let changed = false;
  const allItems = {};
  for(const k in e.buckets) for(const p of e.buckets[k]) allItems[p.id] = {k, p};
  for(const idS in (d.affinity||{})){
    const info = d.affinity[idS], cur = allItems[+idS];
    if(!cur || !info.tracked || !info.funnel) continue;
    const bk = LIVE_BUCKET[info.funnel];
    if(cur.p.funnel!==info.funnel){
      e.buckets[cur.k] = e.buckets[cur.k].filter(x=>x.id!==+idS);
      if(bk){ cur.p.funnel = info.funnel; e.buckets[bk].push(cur.p); }
      changed = true;
    }
    if(info.owners && info.owners.length) cur.p.own = info.owners;
  }
  const prof = D.untProfiles||{};
  for(const u of e.untracked||[]){
    const h = (d.harmonic||{})[u.domain];
    if(!h) continue;
    const p = prof[u.harmonic_company_id]||prof[String(u.harmonic_company_id)];
    if(!p) continue;
    if(h.headcount!=null && p.headcount!==h.headcount){ p.headcount = h.headcount; changed = true; }
    const raised = h.last_funding_at && h.last_funding_at.slice(0,10);
    if(raised && raised > (u.date||'')){
      u.date = raised; if(h.last_funding_type) u.round = h.last_funding_type;
      if(h.funding_total!=null) p.funding_total_usd = h.funding_total;
      changed = true;
    }
  }
  e.liveAt = Date.now(); e.liveOff = false;
  if(changed) rerenderOpen(e);
  else { const b = document.querySelector('.livebadge'); if(b) b.textContent = liveLabel(e); }
}
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
  if(row){
    const tds = row.querySelectorAll('td.covtd');
    if(tds[0]) tds[0].innerHTML = covCardHTML(e, false);
    if(tds[1]) tds[1].innerHTML = covCardHTML(e, true);
  }
}

// ---------- render ----------
function srt(list){
  if(state.sort==='ufq') return [...list].sort((a,b)=>((b.uf&&b.uf.pts)||0)-((a.uf&&a.uf.pts)||0)||(b.relevance?.total||0)-(a.relevance?.total||0));
  if(state.sort==='ufhigh') return [...list].sort((a,b)=>((b.uf&&b.uf.high)||0)-((a.uf&&a.uf.high)||0)||((b.uf&&b.uf.pts)||0)-((a.uf&&a.uf.pts)||0));
  const col = COLS.find(c=>c.k===state.sort)||COLS[4]; return [...list].sort(col.sort); }
function visible(){
  return E().filter(e=>(!state.q||e.name.toLowerCase().includes(state.q))
    && (!state.cat || e.kind!=='fund' || e.category===state.cat)
    && (!state.cc || e.kind!=='fund' || (e.city||'').endsWith(state.cc)));
}
function changesHTML(){
  const ch = (D.changes||{})[state.region];
  if(!ch || (!(ch.moves||[]).length && !(ch.added||[]).length)) return '';
  const items = (ch.moves||[]).map(m=>
      `<span class="chg ${m.up?'up':'down'}"><a href="${affURL(m.id)}" target="_blank" rel="noopener">${m.name}</a> <span class="cc">${m.from||'—'} →</span> <b>${m.to}</b> <span class="cc">· ${m.fund}</span></span>`)
    .concat((ch.added||[]).map(a=>
      `<span class="chg add"><a href="${affURL(a.id)}" target="_blank" rel="noopener">${a.name}</a> <b>new on our list</b>${a.funnel?` <span class="cc">as ${a.funnel}</span>`:''} <span class="cc">· ${a.fund}</span></span>`));
  return `<details class="chgsec"><summary>What's Changed since Last Week <b>${items.length}</b><span class="cnt">pipeline moves at tracked ${D.regions[state.region].label} investors · baseline ${ch.since}</span></summary><div class="chglist">${items.join('')}</div></details>`;
}
function render(){
  const mob = isMobile();
  if(!state.open) stopLive();
  const chEl = document.getElementById('changes');
  if(chEl) chEl.innerHTML = state.view==='funds' ? changesHTML() : '';
  document.getElementById('fundsview').style.display = state.view==='funds'?'':'none';
  document.getElementById('htcview').style.display = state.view==='htc'?'':'none';
  document.getElementById('untview').style.display = state.view==='unt'?'':'none';
  const sh = document.getElementById('starthere');
  if(mob){
    if(sh) sh.innerHTML='';
    if(state.view==='funds') filtersHTML();
    renderMobile(); updateHash(); return;
  }
  document.getElementById('sheet').classList.remove('open');
  if(state.view==='htc'){ htcHTML(); return; }
  if(state.view==='unt'){ untHTML(); return; }
  if(sh){
    sh.innerHTML='';
    if(state.view==='funds' && !state.q){
      const shCard=(e, verdict, why)=>`<div class="shcard" data-slug="${e.slug}" tabindex="0" role="button">
          <div class="fname ${e.tier}"><span class="tdot"></span>${e.name}</div>
          <div class="shwhy">${why}</div>
          <div class="nm ${verdict.cls}">${verdict.txt}</div></div>`;
      const whyLine=e=>{
        const t0=e.uf&&(e.uf.top||[])[0];
        return [e.relevance?`relevance ${e.relevance.total}`:null,
                e.uf&&e.uf.high?`backs ${e.uf.high} high-prio ${e.uf.high>1?'cos':'co'}`:null,
                t0?`top: ${t0.name}${ufBadge(t0.score)}`:null].filter(Boolean).join(' · ');
      };
      const funds=E().filter(e=>e.kind==='fund' && !ACCELCAT[e.category]);
      const byRel=(a,b)=>(b.relevance?.total||0)-(a.relevance?.total||0);
      let html='';
      if(!state.person){
        const top=funds.filter(e=>e.connectivity<50).sort(byRel).slice(0,3);
        if(top.length) html=`<div class="shhead">Start here — the most relevant funds we under-cover</div><div class="shrow">`+
          top.map(e=>shCard(e, nextMove(e)||{cls:'gap',txt:''}, whyLine(e))).join('')+`</div>`;
      } else {
        const fn=state.person.split(' ')[0];
        const borrow=funds.filter(e=>personCov(e,state.person)<22 && e.connectivity>=50 && (e.points||[]).length)
          .sort(byRel).slice(0,3);
        const ground=funds.filter(e=>e.connectivity<22).sort(byRel).slice(0,3);
        if(borrow.length) html+=`<div class="shhead">Raise your coverage, ${fn} — relevant funds the team can open for you</div><div class="shrow">`+
          borrow.map(e=>{const p=e.points[0];
            return shCard(e, {cls:'warm', txt:`Get introduced — ask ${p.internal.split(' ')[0]} (knows ${p.external}${p.pct!=null?` · ${p.pct}%`:''})`},
              `relevance ${e.relevance?e.relevance.total:'—'} · team ${e.connectivity}, you ${personCov(e,state.person)}`);
          }).join('')+`</div>`;
        if(ground.length) html+=`<div class="shhead" style="margin-top:14px">Open new ground — relevant funds no one at Highland covers yet</div><div class="shrow">`+
          ground.map(e=>shCard(e, nextMove(e)||{cls:'gap',txt:''}, whyLine(e))).join('')+`</div>`;
      }
      if(html){
        sh.innerHTML=html;
        sh.querySelectorAll('.shcard').forEach(c=>{
          const go=()=>{toggleRow(c.dataset.slug);
            document.querySelector(`tr.mainrow[data-slug="${CSS.escape(c.dataset.slug)}"]`)?.scrollIntoView({behavior:'smooth',block:'center'});};
          c.addEventListener('click',go);
          c.addEventListener('keydown',ev=>{if(ev.key==='Enter')go();});
        });
      }
    }
  }
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
  document.getElementById('pagetitle').textContent = `${D.regions[state.region].label} coverage`;
  document.getElementById('subcount').textContent = `The ${f} funds that matter most${a?` plus ${a} super-angels`:''}.`;
  document.getElementById('fresh').innerHTML = ' Data as of: '+Object.entries(D.freshness).map(([k,v])=>`${k} — ${v}`).join(' · ')+'.';
}
// ---------- hash routing ----------
function updateHash(){
  let h = '#'+state.region;
  if(state.view==='htc') h+='/htc';
  else if(state.view==='unt') h+='/unt';
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
  else if(m[2]==='unt') state.view='unt';
  else if(m[2]) state.pendingOpen = m[2];
}

addEventListener('hashchange',()=>{  // deep links work without a reload
  state.view = location.hash.includes('/htc') ? 'htc' : location.hash.includes('/unt') ? 'unt' : 'funds';
  state.open = '';
  readHash();
  document.querySelectorAll('#regionseg button').forEach(x=>x.classList.toggle('on', x.dataset.r===state.region));
  document.querySelectorAll('#viewseg button').forEach(x=>x.classList.toggle('on', x.dataset.v===state.view));
  if(typeof whoChip==='function') whoChip();
  labels(); scoreboard(); render();
  if(state.pendingOpen){ const s=state.pendingOpen; state.pendingOpen='';
    toggleRow(s); const el=document.querySelector(`tr[data-slug="${s}"]`); el&&el.scrollIntoView({block:'center'}); }
});
// ---------- boot ----------
readHash();
const seg = document.getElementById('regionseg');
REGIONS.forEach(r=>{const b=document.createElement('button');b.textContent=D.regions[r].label;b.dataset.r=r;
  if(r===state.region)b.classList.add('on');
  b.addEventListener('click',()=>{state.region=r;state.open='';
    seg.querySelectorAll('button').forEach(x=>x.classList.remove('on'));b.classList.add('on');labels();scoreboard();render();});
  seg.appendChild(b);});
document.querySelectorAll('#viewseg button').forEach(b=>b.addEventListener('click',()=>{
  document.querySelectorAll('#viewseg button').forEach(x=>x.classList.remove('on'));
  b.classList.add('on'); state.view=b.dataset.v; render(); updateHash();
}));
document.querySelectorAll('#untmode button').forEach(b=>b.addEventListener('click',()=>{
  document.querySelectorAll('#untmode button').forEach(x=>x.classList.remove('on'));
  b.classList.add('on'); state.untMode=b.dataset.um; untHTML();
}));
document.getElementById('unthc').addEventListener('change',ev=>{
  state.untHC = +ev.target.value; untHTML();});
document.getElementById('untgr').addEventListener('change',ev=>{
  state.untGR = ev.target.value===''?null:+ev.target.value; untHTML();});
// ---------- identity: Sonar is personalised to you ----------
function whoChip(){
  const w = document.getElementById('whoami');
  if(w) w.textContent = state.person ? `👤 ${state.person.split(' ')[0]} ▾` : '👤 Who are you?';
}
function setWho(n, rerender){
  state.person = n;
  try{ localStorage.setItem('sonar_who', n); }catch(err){}
  whoChip();
  document.getElementById('whoback').classList.remove('open');
  if(rerender){ scoreboard(); render(); }
}
function openWho(){
  const l = document.getElementById('wholist');
  l.innerHTML = D.roster.map(n=>`<button data-n="${n}"${n===state.person?' class="on"':''}>${n}</button>`).join('');
  l.querySelectorAll('button').forEach(b=>b.addEventListener('click',()=>setWho(b.dataset.n,true)));
  document.getElementById('whoback').classList.add('open');
}
document.getElementById('whoami').addEventListener('click',openWho);
document.getElementById('whoback').addEventListener('click',ev=>{
  if(ev.target.id==='whoback' && state.person) ev.target.classList.remove('open'); // backdrop closes once identified
});
if(!state.person){  // hash may already carry a person; otherwise use the remembered one
  let w=''; try{ w = localStorage.getItem('sonar_who')||''; }catch(err){}
  if(w && D.roster.includes(w)) state.person = w;
}
whoChip();
if(!state.person || !D.roster.includes(state.person)) openWho();
document.querySelectorAll('.abtn').forEach(b=>b.addEventListener('click',()=>openAP(b.dataset.ap)));
document.getElementById('apclose').addEventListener('click',closeAP);
document.getElementById('apback').addEventListener('click',closeAP);
document.addEventListener('keydown',ev=>{ if(ev.key==='Escape' && ap.mode) closeAP(); });
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
  const uf = r.unframe!=null ? `<br><b>Portfolio quality (Unframe) ${r.unframe}/40</b> <span style="color:var(--muted)">— ${(e.uf||{}).high||0} backed companies with combined priority ≥85, top-10 avg ${(e.uf||{}).avg10||0}</span>` : '';
  const thesis = r.thesis!=null ? `Thesis fit ${r.thesis}/100 × 0.6:<br>` : '';
  return `<div class="th">Relevance ${r.total}/100${r.unframe!=null?' — thesis × Unframe blend':''}</div>
    ${thesis}Stage fit <b>${r.stage}</b>/25 · Sector fit <b>${r.sector}</b>/25<br>
    ${r.eu_deals!=null?`European activity <b>${r.geo}</b>/20 <span style="color:var(--muted)">(${r.eu_deals} EU early-stage deals in 24m)</span>`:`Europe share <b>${r.geo}</b>/20 <span style="color:var(--muted)">(${Math.round(r.europe)}% of recent deals in Europe)</span>`}<br>
    Activity <b>${r.activity}</b>/15 · Graduation to growth rounds <b>${r.grad}</b>/15${uf}
    <div class="tf">How much this fund's portfolio should feed Highland's pipeline${r.unframe!=null?' — weighted by how many of their companies our brain model rates high-priority':''}</div>`;
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
