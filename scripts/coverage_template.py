# Multi-region coverage map template v5. Consumed by build_coverage.py.

TEMPLATE = r"""<meta charset="utf-8">
<title>Sonar</title>
<link rel="icon" type="image/svg+xml" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Crect width='24' height='24' rx='5.5' fill='%232733f0'/%3E%3Cg fill='none' stroke='%23fff' stroke-linecap='round'%3E%3Cpath d='M7 12.8 A4.2 4.2 0 0 1 11.2 17' stroke-width='1.7'/%3E%3Cpath d='M7 9.3 A7.7 7.7 0 0 1 14.7 17' stroke-width='1.7' opacity='.72'/%3E%3Cpath d='M7 5.8 A11.2 11.2 0 0 1 18.2 17' stroke-width='1.7' opacity='.45'/%3E%3C/g%3E%3Ccircle cx='7' cy='17' r='1.8' fill='%23fff'/%3E%3Ccircle cx='15.2' cy='8.8' r='1.5' fill='%23fff'/%3E%3C/svg%3E">
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
.appbar .in{max-width:none;display:flex;align-items:center;gap:14px;padding:12px 22px;flex-wrap:wrap}
.brand{font-weight:600;font-size:16px;letter-spacing:-.005em;white-space:nowrap;font-family:var(--display);
  display:flex;align-items:center;gap:8px}
.brand .mark{width:22px;height:22px;flex:none;display:inline-flex}
.brand .mark svg{width:100%;height:100%;display:block}
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
#shell{display:flex;align-items:flex-start}
#side{width:218px;flex:none;position:sticky;top:53px;height:calc(100vh - 53px);
  border-right:1px solid var(--hair);background:var(--surface);padding:16px 10px;box-sizing:border-box;
  overflow-y:auto;display:flex;flex-direction:column}
/* Ask Sonar: compact callout at the bottom of the left bar */
#sideask{margin-top:auto;padding-top:14px}
#sideask .askcard{margin:0;padding:12px;border-radius:12px}
#sideask .askrow{flex-direction:column;gap:6px}
#sideask .askrow input{font-size:12px;padding:8px 10px;min-width:0}
#sideask .askrow button{padding:7px 10px;font-size:12px}
#sideask .asklog{max-height:240px;margin:0 0 10px;font-size:12px}
#sideask .askchips{margin-top:8px;gap:5px}
#sideask .askchips button{font-size:10.5px;padding:4px 9px;text-align:left}
@media(max-width:860px){ #sideask{display:none} }
/* Ask Sonar big view: the same conversation, three-quarters of the screen */
#askmodal{position:fixed;inset:0;z-index:80;display:flex;align-items:center;justify-content:center}
#askmodal[hidden]{display:none}
.amback{position:absolute;inset:0;background:rgba(24,21,14,.42)}
.ambox{position:relative;width:min(1080px,80vw);height:min(760px,82vh);background:var(--raise);
  border:1px solid var(--hair);border-radius:18px;box-shadow:var(--shadow);padding:18px 22px;
  display:flex;flex-direction:column}
.amclose{position:absolute;top:14px;right:16px;background:transparent;border:1px solid var(--hair);
  border-radius:8px;color:var(--ink2);padding:5px 11px;font-size:12px;cursor:pointer;z-index:2;font-family:inherit}
.amclose:hover{border-color:var(--ink);color:var(--ink)}
.ambody{flex:1;min-height:0;display:flex}
#askmodal .askcard{flex:1;display:flex;flex-direction:column;margin:0;border:0;background:transparent;
  padding:2px 4px;min-height:0}
#askmodal .asklog{flex:1;max-height:none;font-size:14px}
#askmodal .askrow input{font-size:14px}
#askmodal #askbig{display:none}
#askbig{background:transparent;border:0;color:var(--muted);cursor:pointer;font-size:13px;padding:0 4px}
#askbig:hover{color:var(--ink)}
@media(max-width:860px){ .ambox{width:94vw;height:88vh;padding:14px} }
.slabel{font-size:9.5px;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:var(--muted);
  padding:0 12px;margin:4px 0 6px}
.sitem{display:flex;align-items:center;gap:10px;padding:9px 12px;border-radius:10px;font-size:13.5px;
  font-weight:600;color:var(--ink2);cursor:pointer;margin-bottom:2px;user-select:none}
.sitem:hover{background:var(--hair2);color:var(--ink)}
.sitem.on{background:var(--accent-soft);color:var(--accent-ink)}
.sitem .si{width:18px;text-align:center;flex:none}
#content{flex:1;min-width:0}
.page[hidden]{display:none}
.whead{display:flex;align-items:center;justify-content:space-between;gap:18px;flex-wrap:wrap;
  padding:26px 0 12px;border-bottom:1px solid var(--hair);margin-bottom:14px}
.whead h1{font-size:26px;margin:0}
.whead .apctx{border:0;padding:0}
#apmain{display:flex;gap:26px;align-items:flex-start}
#apscroll{flex:1;min-width:0}
#aprail{width:268px;flex:none;position:sticky;top:70px;max-height:calc(100vh - 92px);
  overflow-y:auto;padding:14px 16px;border:1px solid var(--hair);border-radius:14px;
  background:var(--surface);box-sizing:border-box}

.railh{font-size:11px;font-weight:700;letter-spacing:.09em;text-transform:uppercase;color:var(--muted);margin-bottom:4px}
.railsub{font-size:11px;color:var(--muted);margin-bottom:10px;line-height:1.45}
.railitem{display:flex;align-items:baseline;gap:7px;padding:6px 0;border-bottom:1px solid var(--hair2);font-size:12.5px}
.railitem b{font-weight:650;flex:1;min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.railitem .cc{flex:none}
.railitem button{border:0;background:none;color:var(--muted);cursor:pointer;font-size:12px;padding:0 2px}
.railitem button:hover{color:var(--gap-ink)}
.railacts{display:flex;gap:8px;margin-top:12px;flex-wrap:wrap}
.railacts button,.railacts a{font-size:11.5px;font-weight:600;border:1px solid var(--hair);border-radius:7px;
  padding:5px 10px;background:var(--raise);color:var(--ink);cursor:pointer;text-decoration:none}
.star{border:0;background:none;cursor:pointer;font-size:15px;color:var(--muted);padding:2px 4px;flex:none;line-height:1}
.star:hover{color:var(--thin-ink)} .star.on{color:var(--thin-ink)}
@media(max-width:1000px){
  #apmain{flex-direction:column}
  #aprail{position:static;width:auto;max-height:none;order:2;margin-top:6px}
}
.aphead{position:sticky;top:0;background:var(--page);z-index:3;display:flex;align-items:center;gap:10px;
  padding:16px 20px 12px;border-bottom:1px solid var(--hair)}
.aphead #aptitle{flex:1;font-size:17px;font-weight:700;letter-spacing:-.01em}
.aphead button{background:var(--surface);border:1px solid var(--hair);border-radius:8px;width:32px;height:32px;
  font-size:14px;color:var(--ink2);cursor:pointer}
.apctx{display:flex;gap:10px;align-items:center;padding:10px 20px;border-bottom:1px solid var(--hair);
  font-size:12px;color:var(--muted);flex-wrap:wrap}
.apctx select{background:var(--surface);color:var(--ink);border:1px solid var(--hair);border-radius:8px;
  padding:6px 10px;font-size:12.5px}
.apbody{padding:2px 0 80px}
.aphint{font-size:12px;color:var(--muted);margin:2px 0 12px}
.apsec{font-size:11px;letter-spacing:.08em;text-transform:uppercase;color:var(--muted);font-weight:700;margin:18px 0 8px}
.apcard{border:1px solid var(--hair);border-radius:14px;padding:14px 18px;margin-bottom:10px;background:var(--raise)}
.apcard .fname a{color:inherit;text-decoration:none}
.apcard .fname a:hover{text-decoration:underline}
.commline{color:var(--ink2)}
.apdesc{font-size:12.5px;color:var(--ink2);line-height:1.5;margin:6px 0 2px;max-width:860px;
  display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}
.gcard{padding:14px 16px}
.gflex{display:flex;gap:16px;align-items:flex-start}
.gbub{display:flex;flex-direction:column;align-items:center;flex:none;gap:3px}
.gbody{flex:1;min-width:0}
.apdesc.full{display:block;-webkit-line-clamp:unset;max-width:none}
.gstat{flex:none;font-size:11px;font-weight:650;color:var(--ink2);background:var(--surface);
  border:1px solid var(--hair2);border-radius:999px;padding:3px 10px;white-space:nowrap}
.apmeta b{font-weight:650}
.appath a{color:inherit;text-decoration:none;border-bottom:1px dotted var(--hair)}
.appath a:hover{border-bottom-color:var(--ink2)}
.apcard .fname{font-size:14.5px}
.aph2{display:flex;justify-content:space-between;align-items:flex-start;gap:12px}
.apstats{display:flex;gap:18px;flex:none}
.bub{width:46px;height:46px;border-radius:50%;display:inline-flex;align-items:center;justify-content:center;
  font-weight:750;font-size:15.5px;font-variant-numeric:tabular-nums;letter-spacing:-.02em}
.bub.big{width:56px;height:56px;font-size:18px}
.bub.strong,.mbub.strong{background:var(--c-lead);color:var(--covered-ink)}
.bub.medium,.mbub.medium{background:var(--c-awaiting);color:var(--thin-ink)}
.bub.low,.mbub.low{background:var(--hair2);color:var(--ink2)}
.bub.weak,.mbub.weak{background:var(--c-hard);color:var(--gap-ink)}
.bub.none,.mbub.none{background:var(--surface);border:1px dashed var(--hair);color:var(--muted)}
.mbub{flex:none;width:26px;height:26px;border-radius:50%;display:inline-flex;align-items:center;justify-content:center;
  font-size:10.5px;font-weight:750;font-variant-numeric:tabular-nums;letter-spacing:-.02em}
.apstat{display:flex;flex-direction:column;align-items:center;min-width:52px}
.apstat .covnum{font-size:23px}
.apstat .covcap{font-size:8.5px;margin-top:2px;white-space:nowrap}
.hcard{padding:16px 20px 14px}
.hcard .fname{font-size:17.5px}
.hmeta{font-size:13px;margin-top:5px;color:var(--ink2)}
.hmeta .psep{color:var(--hair);padding:0 7px}
.hmeta b{color:var(--ink)}
.hgrid{display:grid;grid-template-columns:minmax(0,7fr) minmax(0,5fr);gap:6px 36px;margin-top:9px;align-items:start}
.hcard .appath{font-size:15px;padding:4px 0}
.hcard .pathh{margin-top:2px}
.hinfo .apdesc{font-size:13.5px;color:var(--ink2);line-height:1.65}
.hstats{margin-top:10px;border-top:1px solid var(--hair2);padding-top:9px;display:flex;flex-direction:column;
  gap:4px;font-size:12.5px;color:var(--ink2)}
.hstats b{color:var(--ink)}
.ncard .fname{font-size:17px}
.ncard .appath{font-size:15px;padding:5px 0 2px}
.ncard .nchips{display:flex;align-items:center;gap:8px;margin-top:7px}
.ncard .nchips .chips{display:inline-flex}
.hleft .apdesc{font-size:13px;-webkit-line-clamp:3;margin:0 0 7px;line-height:1.55}
.hleft .biz{font-size:12.5px}
.pathh{font-size:9.5px;font-weight:700;letter-spacing:.09em;text-transform:uppercase;color:var(--muted);margin-bottom:5px}
.hcard .appath{font-size:13px;margin-top:5px}
.hcard .apacts{margin-top:12px}
@media(max-width:900px){.hgrid{grid-template-columns:1fr}}
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
@media(max-width:760px){.apbody{padding:2px 0 80px}}
body[data-page="h2c"] #fb,body[data-page="net"] #fb,body[data-page="geo"] #fb{margin-left:auto}
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
thead th.on{color:var(--ink)}
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
.dhero{padding:30px 0 6px}
.dhero h1{font-size:30px}
.dsec{font-size:11px;font-weight:700;letter-spacing:.09em;text-transform:uppercase;color:var(--muted);margin:26px 0 10px}
.dgrid{display:grid;gap:12px}
.dgrid.r4{grid-template-columns:repeat(4,minmax(0,1fr))}
.dgrid.r2{grid-template-columns:repeat(2,minmax(0,1fr))}
.dgrid.r5{grid-template-columns:repeat(5,minmax(0,1fr))}
.dtile{background:var(--raise);border:1px solid var(--hair2);border-radius:16px;padding:16px 18px}
.dtile.go,.dcity.go{cursor:pointer}
.dtile.go:hover,.dcity.go:hover{border-color:var(--ink2)}
.dtlabel{font-size:12px;font-weight:700;margin-bottom:10px}
.dtnum .covnum{font-size:30px}
.dring{display:flex;align-items:center;gap:14px;margin:4px 0 8px}
.covcell.big b{font-size:20px;font-weight:750}
.dringcap{display:flex;flex-direction:column}
.dlist{margin-top:11px;border-top:1px solid var(--hair2);padding-top:9px;display:flex;flex-direction:column;gap:5px}
.dlh{font-size:8.5px;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:var(--muted);margin-bottom:2px;
  display:flex;justify-content:space-between;align-items:flex-end;gap:8px}
.dli .bubs,.dlcols{display:flex;gap:6px;flex:none}
.dlcols i{font-style:normal;min-width:26px;text-align:center}
.dli{font-size:12px;font-weight:600;color:var(--ink);display:flex;align-items:center;gap:10px;justify-content:space-between;white-space:nowrap}
.dli .nm{flex:1;min-width:0;overflow:hidden;text-overflow:ellipsis}
.dli .cc{font-weight:500;flex:none;font-variant-numeric:tabular-nums;font-size:11px}
.dlib{min-width:26px;text-align:center;border-radius:999px;padding:1px 7px;font-size:10.5px;font-weight:700}
.dlib.strong{background:var(--c-lead);color:var(--covered-ink)}
.dlib.medium{background:var(--c-awaiting);color:var(--thin-ink)}
.dlib.low{background:var(--hair2);color:var(--ink2)}
.flags{display:inline-flex;vertical-align:-2px;margin-right:7px}
.flags svg{width:17px;height:12.5px;border-radius:2.5px;box-shadow:0 0 0 1px rgba(0,0,0,.1);margin-right:-6px;background:#fff}
.flags svg:last-child{margin-right:0}
.dtnum{display:inline-flex;flex-direction:column}
.dtduo{display:flex;gap:28px}
.askcard{background:var(--raise);border:1px solid var(--hair2);border-radius:16px;padding:16px 18px;margin:16px 0 2px}
.askrow{display:flex;gap:10px}
.askrow input{flex:1;padding:10px 14px;border:1px solid var(--hair);border-radius:10px;background:var(--surface);color:var(--ink);font-size:13.5px}
.askrow input:focus{outline:none;border-color:var(--ink2)}
.askrow button{padding:10px 20px;border:0;border-radius:10px;background:var(--ink);color:var(--surface);font-weight:700;font-size:13px;cursor:pointer}
.askrow button:disabled{opacity:.45;cursor:default}
.askchips{display:flex;gap:8px;flex-wrap:wrap;margin-top:10px}
.askchips button{border:1px solid var(--hair2);background:transparent;color:var(--ink2);border-radius:999px;padding:5px 13px;font-size:12px;cursor:pointer}
.askchips button:hover{border-color:var(--ink2);color:var(--ink)}
.glaunch{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px;margin-top:16px}
.gcity{background:var(--raise);border:1px solid var(--hair2);border-radius:16px;padding:16px 18px;cursor:pointer}
.gcity:hover{border-color:var(--ink2)}
.gcity .gcname{font-family:var(--display);font-size:19px;font-weight:650;letter-spacing:-.01em;
  display:flex;justify-content:space-between;align-items:center;gap:10px}
.gcity .gcstats{font-size:12.3px;color:var(--ink2);margin-top:7px;line-height:1.6}
.gcity .gcstats b{color:var(--ink)}
.gchips{display:flex;flex-wrap:wrap;gap:8px;margin-top:16px}
.gchips button{border:1px solid var(--hair2);background:var(--surface);border-radius:999px;padding:6px 14px;
  font-size:12.5px;font-weight:600;color:var(--ink2);cursor:pointer}
.gchips button:hover{border-color:var(--ink2);color:var(--ink)}
.gchips button b{color:var(--ink)}
.gback{margin:12px 0 2px}
@media(max-width:1100px){.glaunch{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media(max-width:640px){.glaunch{grid-template-columns:1fr}}
.askacts{display:flex;gap:8px;flex-wrap:wrap;margin-top:10px}
.askacts button{border:1px solid var(--accent);background:var(--accent-soft);color:var(--accent-ink);
  border-radius:999px;padding:5px 14px;font-size:12px;font-weight:650;cursor:pointer}
.askacts button:disabled{opacity:.55;cursor:default}
#askclear{border:0;background:none;color:var(--muted);font-size:11px;cursor:pointer;letter-spacing:.04em}
#askclear:hover{color:var(--ink)}
.asklog{display:flex;flex-direction:column;gap:10px;margin:0 0 14px;max-height:440px;overflow:auto}
.askq{align-self:flex-end;max-width:70%;background:var(--hair2);border-radius:14px 14px 4px 14px;padding:9px 14px;font-size:13px;font-weight:600}
.aska{align-self:flex-start;max-width:85%;background:var(--surface);border:1px solid var(--hair2);border-radius:14px 14px 14px 4px;padding:11px 15px;font-size:13.5px;line-height:1.55}
.aska.err{color:var(--gap-ink);background:var(--c-hard);border-color:transparent}
.aska ul{margin:6px 0;padding-left:18px}
.aska p{margin:0 0 8px}.aska p:last-child{margin-bottom:0}
.pend .dots i{font-style:normal;animation:blink 1.2s infinite}
.pend .dots i:nth-child(2){animation-delay:.2s}.pend .dots i:nth-child(3){animation-delay:.4s}
@keyframes blink{0%,100%{opacity:.2}50%{opacity:1}}
.dsplit{display:flex;gap:22px;align-items:center;margin-top:12px}
.dsplit .dtduo{flex:none}
.dsplit .dleft{flex:none;display:flex;flex-direction:column;gap:7px;max-width:46%}
.rtile .dsplit{gap:12px;margin-top:10px}
.rtile .dprev{padding-left:13px;gap:7px}
.rtile .dleft{max-width:41%}
.rtile .dli{font-size:11.5px;gap:7px}
.rtile .bubs,.rtile .dlcols{gap:4px}
.dprev{flex:1;min-width:0;border-left:1px solid var(--hair2);padding-left:22px;display:flex;flex-direction:column;
  gap:8px;align-self:stretch;justify-content:center}
.dph{font-size:8.5px;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:var(--muted)}
.dpli{font-size:12.5px;font-weight:650;color:var(--ink);display:flex;align-items:center;gap:10px;white-space:nowrap}
.dpli .nm{flex:none;max-width:34%;overflow:hidden;text-overflow:ellipsis}
.dpli .how{color:var(--ink2);font-weight:500;flex:1;min-width:0;overflow:hidden;text-overflow:ellipsis}
.dtnum .covcap{margin-top:3px}
.dtsub{font-size:11.5px;color:var(--muted);margin-top:8px;line-height:1.45}
.dtsub.warn{color:var(--gap-ink)}
.dcity{background:var(--raise);border:1px solid var(--hair2);border-radius:16px;padding:14px 16px}
.dcity .fname{font-size:15px}
@media(max-width:1100px){.dgrid.r4{grid-template-columns:repeat(2,1fr)}.dgrid.r5{grid-template-columns:repeat(2,1fr)}}
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
.uvtag.emp{color:var(--ink2);background:var(--hair2);cursor:help}
.ufb{font-size:10px;font-weight:700;border-radius:5px;padding:1px 5px;vertical-align:1px;font-variant-numeric:tabular-nums}
.ufb.hi{background:var(--c-lead);color:var(--c-lead-ink)}
.ufb.mid{background:var(--c-awaiting);color:var(--c-awaiting-ink)}
.ufb.lo{background:var(--hair2);color:var(--ink2)}
#changes{margin:16px 0 0}
#method{max-width:none;margin:44px 0 0}
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
body.mkmode{cursor:crosshair}
.mk-kill{outline:2px dashed var(--gap)!important;outline-offset:2px}
.mk-simplify{outline:2px dashed var(--thin)!important;outline-offset:2px}
#mkpop{position:fixed;z-index:95;background:var(--raise);border:1px solid var(--hair);border-radius:12px;
  box-shadow:var(--shadow);padding:12px 14px;width:290px}
#mkpop .th{font-size:9.5px;letter-spacing:.11em;text-transform:uppercase;color:var(--muted);font-weight:700;margin-bottom:4px;line-height:1.5}
#mkpop .mkbtns{display:flex;gap:8px;margin:8px 0}
#mkpop .mkbtns button{flex:1;border:1px solid var(--hair);background:var(--surface);border-radius:8px;
  padding:7px 0;font-size:12.5px;font-weight:650;cursor:pointer;color:var(--ink2)}
#mkpop .mkbtns button[data-mk="kill"].on{background:var(--c-hard);border-color:var(--gap);color:var(--gap-ink)}
#mkpop .mkbtns button[data-mk="simplify"].on{background:var(--c-awaiting);border-color:var(--thin);color:var(--thin-ink)}
#mknote{width:100%;border:1px solid var(--hair);border-radius:8px;background:var(--surface);color:var(--ink);
  padding:7px 10px;font-size:12.5px;margin-bottom:9px}
#mkpop .mkact{display:flex;gap:8px;align-items:center}
#mktray{position:fixed;bottom:18px;left:50%;transform:translateX(-50%);z-index:94;background:var(--ink);
  color:var(--page);border-radius:999px;padding:9px 18px;display:flex;gap:14px;align-items:center;font-size:12.5px;
  box-shadow:var(--shadow);white-space:nowrap}
#mktray[hidden]{display:none}
#mktray button{background:none;border:0;color:var(--page);text-decoration:underline;cursor:pointer;font-size:12px;padding:0}
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
/* graceful reflow when Sonar runs at half-screen or in a dragged window */
@media(max-width:1500px){
  .covcard{width:206px;padding:12px 13px 10px}
}
@media(max-width:1300px){
  .covcard{width:168px}
  .covrow .cst span{display:none}   /* keep counts + colour bars, drop the tiny labels */
  td.covtd{min-width:0;padding:12px 6px}
  .pts{width:270px;min-width:0}
  .chips.mini{max-width:170px}
}
@media(max-width:1140px){
  #side{width:164px;padding:14px 10px}
  .covcard{width:auto;min-width:104px;padding:11px 12px 9px}
  .covrow{display:none}             /* score only — full stage split lives in the expanded row */
  .covhead{margin-bottom:0;flex-direction:column;gap:3px;align-items:flex-start}
  .dgrid.r2{grid-template-columns:1fr}
  .pts{width:180px;min-width:0;font-size:12px}
  .badge{white-space:normal}
  table td:first-child{max-width:215px}
  .pts .pt .ptr .sbar{display:none}
  .relcell{min-width:0}
  .relcell .rb{width:40px}
  .tmcols{gap:16px}
  .namecell,.fname{overflow-wrap:anywhere}
}
@media(max-width:860px){
  /* sidebar becomes a horizontal nav strip — phones keep full navigation */
  #shell{display:block}
  #side{position:static;width:auto;height:auto;display:flex;align-items:center;gap:4px;
    overflow-x:auto;-webkit-overflow-scrolling:touch;padding:8px 12px;border-right:0;
    border-bottom:1px solid var(--hair)}
  #side .slabel{display:none}
  .sitem{flex:none;margin-bottom:0;padding:7px 12px;font-size:12.5px;white-space:nowrap}
}
@media(max-width:700px){
  .score{flex-wrap:wrap;gap:10px 0;width:100%}
  .score .s{flex:1 1 45%;max-width:none;padding:0 14px;box-sizing:border-box}
  .score .s:nth-child(odd){border-left:0;padding-left:0}
  .dgrid.r4,.dgrid.r5{grid-template-columns:1fr}
  .dsplit{flex-wrap:wrap}
  .dprev{border-left:0;padding-left:0;flex-basis:100%;margin-top:10px}
  .rtile .dleft{max-width:none}
  .askrow input{font-size:16px}  /* stops iOS zoom-on-focus */
  /* preview rows: let the "how" line wrap under the name instead of clipping */
  .dpli{flex-wrap:wrap;white-space:normal;row-gap:2px}
  .dpli .nm{max-width:calc(100% - 44px)}
  .dpli .how{flex-basis:100%;white-space:normal;overflow:visible;text-overflow:clip;padding-left:36px}
  .chgsec summary{flex-wrap:wrap}
  #method{padding:0 2px}
  /* app bar: brand + identity + feedback on one row */
  .appbar .in{row-gap:8px}
  #fb{order:1;margin-left:auto}
}

/* ===== Coverage Map ===== */
.cmtop{display:flex;gap:10px;flex-wrap:wrap;align-items:center;margin:0 0 10px}
.cmcrumb button{border:0;background:none;color:var(--accent-ink);font-weight:600;cursor:pointer;font-size:13.5px;padding:2px 2px;font-family:inherit}
.cmcrumb button[disabled]{color:var(--ink);cursor:default}
.cmall{font-size:12px;color:var(--muted);margin-left:auto;display:flex;gap:5px;align-items:center}
.cmflex{display:flex;gap:14px;align-items:stretch}
.cmmain{flex:1;min-width:0}
.cmback{font-weight:700}
.cmlegend{display:flex;gap:18px;flex-wrap:wrap;align-items:center;margin:0 0 10px;padding:7px 12px;
  background:var(--surface);border:1px solid var(--hair);border-radius:11px;font-size:11.5px;color:var(--ink2)}
.cmlgi{display:inline-flex;align-items:center;gap:6px}
.cmdot{width:10px;height:10px;border-radius:50%;display:inline-block;margin-right:2px}
.cmcards{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:10px}
.cmfcard{display:flex;gap:10px;align-items:center;background:var(--surface);border:1px solid var(--hair);
  border-radius:12px;padding:10px 12px;cursor:pointer}
.cmfcard:hover{border-color:var(--accent)}
.cmfcard.aff{cursor:default;border-style:dashed;background:none}
.cmfcard.aff:hover{border-color:var(--hair)}
.cmfg{flex:none}
.cmfi{min-width:0}
.cmfn{font-weight:700;font-size:14.5px}
.cmfm{font-size:12px;color:var(--ink2);margin-top:1px}
.cmdoor{color:var(--muted)}
.cmdet{background:var(--surface);border:1px solid var(--hair);border-radius:14px;padding:16px 18px}
.cmv2grid{display:grid;grid-template-columns:7fr 5fr;gap:18px;align-items:start;margin-top:4px}
@media(max-width:1000px){.cmv2grid{grid-template-columns:1fr}}
.cmspendcols{display:grid;grid-template-columns:1fr 1fr;gap:12px;align-items:start}
@media(max-width:1250px){.cmspendcols{grid-template-columns:1fr}}
.cmspend{background:var(--surface);border:1px solid var(--hair);border-radius:12px;padding:12px 14px;margin-bottom:10px}
.cmspend.go{cursor:pointer;transition:border-color .12s, box-shadow .12s}
.cmspend.go:hover{border-color:var(--accent);box-shadow:0 3px 14px rgba(39,51,240,.08)}
.cmbigs{display:flex;gap:8px;flex-wrap:wrap;margin-top:9px}
.cmbig{font-size:14px;font-weight:800;letter-spacing:.01em;padding:6px 12px;border-radius:9px;background:var(--hair2);color:var(--ink2)}
.cmbig.warm{background:#e4efe6;color:#2e6b44}
.cmbig.cold{background:#fbe9e2;color:#9c3c1e}
.cmbig.df{background:#eceafd;color:#3b36a8}
.cmbig.pipe{background:#fdf3dc;color:#8a6116}
.nettab td.nmc a,.dpli .nm a{color:inherit;text-decoration:none;border-bottom:1px dashed var(--hair)}
.nettab td.nmc a:hover,.dpli .nm a:hover{color:var(--accent-ink);border-bottom-color:var(--accent)}
.cmspend .cmfn{font-size:15px}
.cmdoor{padding:10px 13px;margin-bottom:8px}
.cmdoor .cmbig{font-size:12.5px;padding:4px 10px}
.cmdoor .cmfn a{color:inherit;text-decoration:none;border-bottom:1px dashed var(--hair)}
.cmdoor .cmfn a:hover{color:var(--accent-ink)}
.cmask{color:var(--ink);margin-top:5px}
.cmquiet{opacity:.72}
.cmminimap{background:var(--surface);border:1px solid var(--hair);border-radius:12px;overflow:hidden}
.cmminimap svg{display:block;width:100%;height:330px}
.cmacc{background:var(--surface);border:1px solid var(--hair);border-radius:11px;margin-top:10px;padding:0 14px}
.cmacc summary{cursor:pointer;padding:10px 0;font-size:13px;font-weight:700;color:var(--ink2);list-style:none}
.cmacc summary b{color:var(--ink);margin-left:4px}
.cmacc[open] summary{border-bottom:1px solid var(--hair2)}
.cmacc .dpli{padding:6px 0}
.cmnode{fill:var(--accent);fill-opacity:.72;stroke:#fff;stroke-width:1.2}
.cmswap .cmdisc{opacity:0;transition:opacity .2s}
.cmswap .cmbtn{transition:opacity .2s}
.cmswap:hover .cmdisc,.cmswap:focus .cmdisc{opacity:1}
.cmswap:hover .cmbtn,.cmswap:focus .cmbtn{opacity:0}
.cmdeth{display:flex;gap:14px;align-items:center;margin-bottom:12px}
.cmdetn{font-size:17px;font-weight:700}
.cmdett{margin-top:4px}
.cmego{max-width:520px}
.cmmapwrap.full #cmsvg{height:calc(100vh - 252px);min-height:520px}
.cmpanel.float{position:absolute;top:12px;left:12px;width:332px;max-height:calc(100% - 24px);
  overflow-y:auto;background:rgba(252,251,246,.96);box-shadow:0 8px 26px rgba(0,0,0,.1);z-index:3}
.cmexpl{line-height:1.5;margin:8px 0 2px}
@media(max-width:1000px){ .cmpanel.float{position:static;width:auto;max-height:none;margin-top:10px;box-shadow:none} }
.cmmapwrap{position:relative;background:var(--surface);border:1px solid var(--hair);border-radius:14px;overflow:hidden}
#cmsvg{display:block;width:100%;height:calc(100vh - 230px);min-height:460px}
.cmpanel{flex:none;width:360px;background:var(--surface);border:1px solid var(--hair);border-radius:14px;padding:16px 18px;overflow-y:auto;max-height:calc(100vh - 230px)}
.cmbg{fill:var(--hair2);stroke:var(--bg);stroke-width:.6}
.cmbg,.cmcty,.cmouter,.cmring2,.cmnode{vector-effect:non-scaling-stroke}
.cmcty{fill:#e7e2d4;stroke:var(--bg);stroke-width:.7;cursor:pointer}
.cmcty.on{stroke:#b9b2a0}
.cmreg text{text-anchor:middle;font-size:12px;font-weight:700;fill:var(--ink2)}
.cmsoonnode{fill:var(--accent);fill-opacity:.09;stroke:var(--accent);stroke-opacity:.3;stroke-width:1;vector-effect:non-scaling-stroke}
.cmreg.soon{cursor:default}
.cmreg.soon:hover .cmsoonnode{fill-opacity:.18;stroke-opacity:.5}
.cmreg.live{cursor:pointer}
.cmouter{fill:rgba(255,255,255,.55);stroke:#8b8578;stroke-width:1}
.cmteam{fill:#8a86c9;fill-opacity:.35}
.cmme{fill-opacity:.92}
.cment{cursor:pointer}
.cment:hover .cmouter{stroke:var(--accent);stroke-width:1.6}
.cmdim{opacity:.18}
.cmring2{fill:none;stroke:#c2452f;stroke-width:.7}
.cmbadge{font-size:7px;font-weight:800;fill:var(--ink2)}
.cmlab{text-anchor:middle;font-weight:600;fill:var(--ink);paint-order:stroke;stroke:#fcfbf6;stroke-width:2.4px}
.cmtray{position:absolute;right:10px;bottom:10px;font-size:11.5px;color:var(--muted);background:rgba(252,251,246,.92);border:1px solid var(--hair);border-radius:9px;padding:6px 10px;max-width:70%}
.cmcard{position:absolute;width:290px;background:var(--surface);border:1px solid var(--hair);border-radius:11px;box-shadow:0 6px 22px rgba(0,0,0,.13);padding:11px 13px;pointer-events:none;z-index:5}
.cmcn{font-size:13.5px}
.cmst{font-size:9.5px;font-weight:800;text-transform:uppercase;letter-spacing:.05em;padding:1px 6px;border-radius:7px;background:var(--hair2);color:var(--ink2)}
.cmst.build{background:#fbe9e2;color:#9c3c1e}
.cmst.maintain{background:#e4efe6;color:#2e6b44}
.cmwhy{font-size:11.5px;color:var(--ink2);margin-top:5px;line-height:1.45}
.cmnums{display:flex;gap:12px;font-size:11px;color:var(--muted);margin-top:7px}
.cmnums b{font-size:14px;color:var(--ink);display:block}
.cmhead{font-size:14.5px;line-height:1.5;margin-bottom:12px}
.cmquals{display:flex;gap:7px;margin:4px 0 10px}
.cmqual{font-size:11px;font-weight:700;letter-spacing:.03em;border:1px solid;border-radius:999px;padding:3px 10px}
.cmg{display:flex;align-items:center;gap:8px;margin:5px 0;font-size:12px}
.cmg .cmgl{width:36px;color:var(--muted)}
.cmgbar{flex:1;height:8px;background:var(--hair2);border-radius:5px;overflow:hidden}
.cmgbar i{display:block;height:100%;border-radius:5px}
.cml3t{font-size:11px;fill:var(--ink2)}
.cml3t.me{font-weight:700;fill:var(--accent-ink)}
body[data-page=map] #aprail{display:none}
body[data-page=map] .wrap{max-width:none}
body[data-page=map] #apmain{max-width:none}
@media(max-width:1000px){ .cmflex{flex-direction:column} .cmpanel{width:auto;max-height:none} #cmsvg{height:52vh;min-height:360px} }

/* Daily Network Actions: one recommendation at a time — action it or move on */
.ndkwrap{max-width:620px;margin:6px auto 0}
.ndkcount{font-size:10.5px;letter-spacing:.14em;text-transform:uppercase;color:var(--muted);font-weight:700;
  margin-bottom:12px;text-align:center}
.ndkstack{position:relative;padding-bottom:20px}
.ndkghost{position:absolute;left:0;right:0;height:100%;background:var(--surface);border:1px solid var(--hair);border-radius:16px}
.ndkghost.g1{top:9px;transform:scale(.97)}
.ndkghost.g2{top:18px;transform:scale(.94)}
.ndkcard{position:relative;border-radius:16px;padding:32px 34px 26px;text-align:center}
.ndkverb{font-size:12px;letter-spacing:.16em;text-transform:uppercase;color:var(--accent-ink);font-weight:750;margin-bottom:10px}
.ndkname{font-size:30px;font-weight:700;letter-spacing:-.02em;font-family:var(--display);line-height:1.15}
.ndksub{color:var(--ink2);font-size:14px;margin-top:11px;line-height:1.6;max-width:460px;margin-left:auto;margin-right:auto}
.ndkacts{margin-top:22px}
.ndkmain{display:inline-block;background:var(--accent);color:#fff;border-radius:10px;padding:11px 26px;
  font-size:14px;font-weight:650;text-decoration:none}
.ndkmain:hover{background:var(--accent-ink)}
.ndkskips{display:flex;justify-content:center;gap:8px;margin-top:18px}
.ndkskips button{background:transparent;border:1px solid var(--hair);color:var(--ink2);border-radius:8px;
  padding:7px 14px;font-size:12.5px;cursor:pointer;font-family:inherit}
.ndkskips button:hover{border-color:var(--accent);color:var(--accent-ink)}
.ndkdone{text-align:center;padding:38px 24px}
.ndkbig{font-size:24px;font-weight:700;font-family:var(--display);margin-bottom:8px}

/* My Network: segment bar, one-line people rows, cadence chips */
.segbar{display:flex;gap:6px;flex-wrap:wrap;margin:2px 0 14px}
.segbar button{border:1px solid var(--hair);background:var(--surface);color:var(--ink2);
  border-radius:999px;padding:6px 14px;font-size:13px;cursor:pointer;font-family:inherit}
.segbar button b{font-weight:700;margin-left:4px}
.segbar button.on{background:var(--accent);border-color:var(--accent);color:#fff}
.nrow{display:flex;align-items:center;gap:10px;padding:8px 2px;border-bottom:1px solid var(--hair2);font-size:14.5px}
.nrow:last-child{border-bottom:0}
.nrow .nm{font-weight:600;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.nrow .nf{color:var(--ink2);white-space:nowrap;overflow:hidden;text-overflow:ellipsis;flex:1;min-width:0}
.nrow .nl{color:var(--muted);font-size:12.5px;white-space:nowrap;flex:none}
.nrow .nmail{flex:none;text-decoration:none}
.cadchip{flex:none;border:1px solid var(--hair);background:none;color:var(--muted);border-radius:999px;
  padding:2px 9px;font-size:11px;cursor:pointer;font-family:inherit}
.cadchip.on{color:var(--ink2);border-color:var(--ink2)}
.nrow.cold .nl{color:var(--gap-ink);font-weight:600}
.ntfilt{display:flex;gap:6px;flex-wrap:wrap;align-items:center;margin:2px 0 12px}
.ntfilt input{padding:6px 10px;font-size:13px;border:1px solid var(--hair);border-radius:9px;
  background:var(--surface);color:var(--ink);width:170px}
.ntfilt input:focus{outline:none;border-color:var(--accent)}
.ntfilt select{padding:6px 8px;font-size:12.5px;border:1px solid var(--hair);border-radius:9px;
  background:var(--surface);color:var(--ink2);max-width:150px}
.ntfilt select.on{border-color:var(--accent);color:var(--accent-ink);background:var(--accent-soft)}
.ntcard{padding:0;overflow-x:auto}
table.nettab{width:100%;border-collapse:collapse;font-size:13.5px}
.nettab th{text-align:left;font-size:10.5px;font-weight:700;letter-spacing:.05em;text-transform:uppercase;
  color:var(--muted);padding:9px 10px;border-bottom:1px solid var(--hair);white-space:nowrap;user-select:none}
.thsort{cursor:pointer}
.thsort.on{color:var(--ink)}
.thfilt{appearance:none;-webkit-appearance:none;border:0;padding:0;margin:0 0 0 5px;width:16px;height:14px;
  vertical-align:-2px;cursor:pointer;color:transparent;
  background:transparent url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 12 12'%3E%3Cpath d='M1.5 2h9L7 6.6V10L5 8.6V6.6z' fill='none' stroke='%23a09a8c' stroke-width='1.3' stroke-linejoin='round'/%3E%3C/svg%3E") center/12px no-repeat}
.thfilt.on{background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 12 12'%3E%3Cpath d='M1.5 2h9L7 6.6V10L5 8.6V6.6z' fill='%232733f0' stroke='%232733f0' stroke-width='1.3' stroke-linejoin='round'/%3E%3C/svg%3E")}
.thfilt option{color:#1a1a1a;background:#fff}
.thval{margin-left:4px;color:var(--accent-ink);text-transform:none;letter-spacing:0;font-weight:600;
  display:inline-block;max-width:72px;overflow:hidden;text-overflow:ellipsis;vertical-align:bottom}
.nettab td{padding:7px 10px;border-bottom:1px solid var(--hair2);white-space:nowrap;color:var(--ink2)}
.nettab tbody tr:last-child td{border-bottom:0}
.nettab tbody tr:hover td{background:var(--hair2)}
.nettab td.nmc{font-weight:600;color:var(--ink)}
.nettab td.lt{color:var(--muted);font-size:12.5px}
.nettab tr.coldr td.lt{color:var(--gap-ink);font-weight:600}
@media(max-width:860px){
  table.nettab{min-width:760px}
  .ntcard{max-width:calc(100vw - 32px)}  /* viewport-bound: the table scrolls inside the card */
}
.t3row{display:flex;align-items:baseline;gap:8px;padding:7px 0;font-size:15px;flex-wrap:wrap}
.t3row .t3what{color:var(--muted);font-size:11px;font-weight:700;letter-spacing:.05em;text-transform:uppercase;flex:none;width:118px}
@media(max-width:700px){
  .nrow{flex-wrap:wrap;row-gap:2px}
  .nrow .nf{flex-basis:100%;padding-left:36px;white-space:normal}
  .t3row .t3what{width:auto;flex-basis:100%}
}
</style>

<div class="appbar"><div class="in">
  <span class="brand"><span class="mark"><svg viewBox="0 0 24 24"><rect width="24" height="24" rx="5.5" fill="#2733f0"/><g fill="none" stroke="#fff" stroke-linecap="round" stroke-width="1.7"><path d="M7 12.8 A4.2 4.2 0 0 1 11.2 17"/><path d="M7 9.3 A7.7 7.7 0 0 1 14.7 17" opacity=".72"/><path d="M7 5.8 A11.2 11.2 0 0 1 18.2 17" opacity=".45"/></g><circle cx="7" cy="17" r="1.8" fill="#fff"/><circle cx="15.2" cy="8.8" r="1.5" fill="#fff"/></svg></span><span>Sonar<span class="by">Highland Europe</span></span></span>
  <button class="btn ghost" id="whoami" title="Sonar is personalised to you — click to switch">👤</button>
  <button class="btn ghost" id="fb" title="Feedback & requests">💬 Feedback</button>
  <button class="btn" id="export" hidden>Export CSV</button>
  <div id="fbpop" hidden>
    <div class="th">Feedback &amp; requests</div>
    <p><b>Comment straight onto Sonar:</b> <a href="https://claude.ai/code/artifact/37aa2a39-f41a-42b4-b246-783d4b19c0ff" target="_blank" rel="noopener">open the comment copy ↗</a>,
    tap the <b>speech-bubble icon</b> in the black claude.ai bar at the top (next to your avatar),
    then tap or select anything on the page and write your note. Will &amp; Claude review every
    thread, and you'll get a reply on it when it ships.</p>
    <p>Prefer email? <a id="fbmail" href="mailto:william@highlandeurope.com?subject=Sonar%20feedback&body=What%20I%27d%20like%3A%0A%0AWhere%20(region%20%2F%20fund%20%2F%20view)%3A%0A">Send it to Will</a>.</p>
    <p><b>Or mark up this app directly:</b> markup mode lets you click anything on any page and tag it
    <b>Kill</b> or <b>Simplify</b> — then copy the report and paste it to Claude.</p>
    <button class="minibtn prep" id="mkstart" type="button">✎ Start markup mode</button>
    <button class="minibtn" id="fbclose">Got it</button>
  </div>
</div></div>

<div id="askmodal" hidden><div class="amback" data-amclose></div><div class="ambox">
  <button class="amclose" data-amclose title="Close (Esc) — the conversation stays">✕ close</button>
  <div class="ambody"></div>
</div></div>

<div id="shell">
<nav id="side">
  <div class="slabel">Sonar</div>
  <a class="sitem" data-page="map" id="simap"><span class="si">◍</span>Coverage Map</a>
  <a class="sitem" data-page="h2c"><span class="si">⚡</span>Solve my Hard to Cracks</a>
  <a class="sitem" data-page="geo"><span class="si">✈</span>Plan a City Trip</a>
  <a class="sitem" data-page="net"><span class="si">⇗</span>Network Actions</a>
  <div id="sideask"></div>
</nav>
<main id="content">


<section id="workpage" class="page" hidden><div class="wrap">
  <header class="whead"><h1 id="worktitle"></h1><div class="apctx" id="apctx"></div></header>
  <div id="apmain">
    <div id="apscroll"><div class="apbody" id="apbody"></div></div>
    <aside id="aprail"></aside>
  </div>
</div></section>

</main>
</div>
<div id="whoback"><div id="whocard" role="dialog" aria-modal="true" aria-label="Who are you?">
  <div class="th">Who are you?</div>
  <p>Sonar personalises coverage, workflows and next moves to you.
  Pick yourself once — it's remembered on this device.</p>
  <div id="wholist"></div>
</div></div>
<div id="sheet" role="dialog" aria-modal="true">
  <div class="sheethead"><button id="sheetclose" aria-label="Close">←</button><div class="fname" id="sheetname"></div></div>
  <div class="sheetstats" id="sheetstats"></div>
  <div class="sheetbody"><div class="detail" id="sheetdetail"></div></div>
</div>

</div>
<div class="toast" id="toast"></div>
<div id="mkpop" hidden>
  <div class="th" id="mkwhat"></div>
  <div class="mkbtns"><button type="button" data-mk="kill" class="on">🗑 Kill</button><button type="button" data-mk="simplify">✂ Simplify</button></div>
  <input id="mknote" placeholder="Optional note — why / what instead…" autocomplete="off">
  <div class="mkact"><button type="button" class="btn" id="mksave">Save mark</button><button type="button" class="minibtn" id="mkcancel">Cancel</button></div>
</div>
<div id="mktray" hidden><b id="mkcount"></b><button type="button" id="mkcopy">Copy report</button><button type="button" id="mkclearall">Clear</button><button type="button" id="mkexit">Exit markup</button></div>

<script>
const D = __DATA__;
const REGIONS = Object.keys(D.regions);
const BUCKETS = [["prelead","Pre-lead"],["reachout","Reach out"],["awaiting","Awaiting"],["lead","Lead"],["hard","Hard to crack"]];
const TIER = {strong:"var(--covered)", medium:"var(--thin)", weak:"var(--gap)"};
const state = {region: REGIONS[0], page:'map', view:"funds", sort:"connectivity", sortDir:1, q:"", person:"", cat:"", cc:"",
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



// ---------- filters ----------


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
  "Mountain View":"SF Bay Area","Woodside":"SF Bay Area","Oakland":"SF Bay Area","Berkeley":"SF Bay Area",
  "San Jose":"SF Bay Area","Redwood City":"SF Bay Area","Sunnyvale":"SF Bay Area","Santa Clara":"SF Bay Area",
  "South San Francisco":"SF Bay Area","Cupertino":"SF Bay Area","Brooklyn":"New York"};
const cityOf = e => { const c=(e.city||'').split('·')[0].trim(); return METRO[c]||c; };
// cities ranked by open pipeline x network strength x dealflow weight (shared: dashboard + trip launcher)
function cityScores(me){
  const cities={};
  const blank=()=>({funds:0,gapW:0,pipe:0,hiPipe:0,str:[],names:new Set(),topco:[],topf:[]});
  ALLE.forEach(({r,e})=>{
    const fc=cityOf(e);
    if(e.kind==='fund'&&fc&&(e.relevance?.total||0)>=55&&!ACCELCAT[e.category]){
      const c=cities[fc]=cities[fc]||blank();
      c.funds++; const pc=me?personCov(e,me):e.connectivity;
      c.gapW+=(e.relevance.total/100)*(1-pc/100); c.str.push(pc);
      c.topf.push({n:e.name, rel:e.relevance.total, pc, tc:e.connectivity});
    }
    Object.values(e.buckets||{}).forEach(l=>l.forEach(p=>{
      if(!p.city) return; const mc=metroOf(p.city); if(!mc) return;
      if(me&&!(p.own||[]).includes(me)) return;
      const c=cities[mc]=cities[mc]||blank();
      if(!c.names.has(p.id)){ c.names.add(p.id); c.pipe++; if((p.uf||0)>=70) c.hiPipe++;
        c.topco.push({n:p.name, uf:p.uf}); }
    }));
  });
  // London is home for everyone except Fergal, Irena and Tony — don't suggest it to Londoners
  const AWAY=['Fergal Mullen','Irena Goldenberg','Tony Zappala'];
  if(!me || !AWAY.includes(me)) delete cities['London'];
  return Object.entries(cities)
    .map(([city,c])=>({city,...c,score:c.pipe*0.6+c.hiPipe*1.2+c.gapW*1.6}))
    .sort((a,b)=>b.score-a.score);
}
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
const BYSLUG = {}; ALLE.forEach(({e})=>{ if(e.slug) BYSLUG[e.slug]=e; });
// the viewer's own best contact at a tracked fund (team paths dedupe these away)
const ownDoor=(slug,who)=>{ const e=who&&slug?BYSLUG[slug]:null; if(!e) return null;
  const tp=(e.top_people||[]).find(x=>x.name===who);
  const k=((tp&&tp.contacts)||[]).filter(c=>!c.moved&&(c.pct||0)>0).sort((a,b)=>(b.pct||0)-(a.pct||0))[0];
  return k?{internal:who,external:k.person,pct:k.pct}:null; };
// all live paths into an H2C company, the viewer's own edges included
const htcPaths=(c,who)=>{
  const all=(c.investors||[]).flatMap(i=>{
    const ps=(i.paths&&i.paths.length?i.paths:(i.best?[i.best]:[])).slice();
    const o=ownDoor(i.slug,who);
    if(o&&!ps.some(p=>p&&p.internal===who&&p.external===o.external)) ps.push(o);
    return ps.filter(p=>p&&p.internal&&!p.moved)
      .map(p=>({...p,fund:i.name,region:i.region,unt:i.untracked}));
  }).sort((a,b)=>(b.pct||0)-(a.pct||0));
  // per external contact: keep the viewer's own edge unless a teammate's is >30pts stronger
  const byX={}; all.forEach(p=>{const k=p.external||p.fund;(byX[k]=byX[k]||[]).push(p);});
  const team=Object.values(byX).map(l=>{
    const s=who?l.find(p=>p.internal===who):null;
    return (s&&(s.pct||0)>=((l[0].pct||0)-30))?s:l[0];
  }).sort((a,b)=>(b.pct||0)-(a.pct||0));
  const self=who?all.find(p=>p.internal===who&&(p.pct||0)>=25):null;
  return {all, team, self};
};
const metroOf = c => METRO[c]||c;
const ap = {mode:'', who:'', city:'', hsort:'ease', nseg:'target',
  nf:{q:'',ty:'',st:'',sr:'',ci:''}, ns:'p', nd:-1};
// ---------- shortlist: star anything in a workflow into a persistent "earmarked" rail ----------
let SHORT = [];
try{ SHORT = JSON.parse(localStorage.getItem('sonar_shortlist')||'[]'); }catch(err){}
const shKey = s => s.t+'|'+s.name;
const PROF = D.profiles||{};
const FLAGC = {germany:['de'], nordics:['se','dk','no','fi'], france:['fr'], us:['us']};
const FSVG = {
 de:'<rect width="18" height="4.33" fill="#1a1a1a"/><rect width="18" height="4.33" y="4.33" fill="#cc2b1d"/><rect width="18" height="4.34" y="8.66" fill="#f5c400"/>',
 fr:'<rect width="6" height="13" fill="#2443a3"/><rect x="6" width="6" height="13" fill="#fff"/><rect x="12" width="6" height="13" fill="#c8102e"/>',
 us:'<rect width="18" height="13" fill="#fff"/>'+[0,2,4,6,8,10,12].map(y=>`<rect y="${y}" width="18" height="1" fill="#b22234"/>`).join('')+'<rect width="8" height="7" fill="#3c3b6e"/>',
 se:'<rect width="18" height="13" fill="#1e5aa8"/><rect x="5" width="3" height="13" fill="#f5c400"/><rect y="5" width="18" height="3" fill="#f5c400"/>',
 dk:'<rect width="18" height="13" fill="#c8102e"/><rect x="5" width="3" height="13" fill="#fff"/><rect y="5" width="18" height="3" fill="#fff"/>',
 no:'<rect width="18" height="13" fill="#ba0c2f"/><rect x="4.5" width="4" height="13" fill="#fff"/><rect y="4.5" width="18" height="4" fill="#fff"/><rect x="5.5" width="2" height="13" fill="#00205b"/><rect y="5.5" width="18" height="2" fill="#00205b"/>',
 fi:'<rect width="18" height="13" fill="#fff" stroke="#e3ded0" stroke-width=".5"/><rect x="4.5" width="4" height="13" fill="#002f6c"/><rect y="4.5" width="18" height="4" fill="#002f6c"/>'
};
const flagsOf = r => `<span class="flags">${(FLAGC[r]||[]).map(c=>`<svg viewBox="0 0 18 13">${FSVG[c]}</svg>`).join('')}</span>`;
const ufTierOf = v => v==null?'none':v>=85?'strong':v>=70?'medium':'low';
const easeTierOf = v => !v?'none':v>=50?'strong':v>=22?'medium':'weak';
const bub = (v,tier,cap,big) => `<span class="apstat"><span class="bub${big?' big':''} ${tier}">${v??'—'}</span><span class="covcap">${cap}</span></span>`;
const profOf = o => PROF[((o&&o.domain)||'').toLowerCase().replace(/^www\./,'')] || {};
const hcBit = pr => pr.hc==null?null:`${pr.hc} FTE${pr.hg!=null?` <b style="color:${growthColor(pr.hg)}">${pr.hg>0?'+':''}${Math.round(pr.hg)}% YoY</b>`:''}`;
const bizBits = pr => [hcBit(pr),
  pr.fu?fmtMoney(pr.fu)+' raised':null,
  pr.st?String(pr.st).replaceAll('_',' ').toLowerCase():null,
  pr.f?'founded '+pr.f:null].filter(Boolean);
const shHas = (t,name) => SHORT.some(s=>s.t===t && s.name===name);
function shToggle(t,name,extra){
  if(shHas(t,name)) SHORT = SHORT.filter(s=>!(s.t===t&&s.name===name));
  else SHORT.push({t,name,extra:extra||''});
  try{ localStorage.setItem('sonar_shortlist', JSON.stringify(SHORT)); }catch(err){}
  renderRail();
  document.querySelectorAll(`[data-star="${CSS.escape(t+'|'+name)}"]`)
    .forEach(b=>{b.classList.toggle('on', shHas(t,name)); b.textContent = shHas(t,name)?'★':'☆';});
}
const starBtn = (t,name,extra) =>
  `<button class="star${shHas(t,name)?' on':''}" data-star="${t}|${name}" data-starx="${extra||''}"
    title="Earmark">${shHas(t,name)?'★':'☆'}</button>`;
function bindStars(root){
  root.querySelectorAll('[data-star]').forEach(b=>b.addEventListener('click',ev=>{
    ev.stopPropagation();
    const [t,...rest]=b.dataset.star.split('|');
    shToggle(t, rest.join('|'), b.dataset.starx);
  }));
}
function renderRail(){
  const rail=document.getElementById('aprail'); if(!rail) return;
  const grp={co:'Companies',fund:'Funds & investors',person:'People'};
  let h=`<div class="railh">★ Earmarked</div>
    <div class="railsub">${ap.mode==='geo'?'Your next-visit list — star companies and funds to plan the trip.':'Starred across workflows — saved on this device.'}</div>`;
  if(!SHORT.length) h+=`<div class="railsub" style="color:var(--muted)">Nothing starred yet. Tap ☆ on any card.</div>`;
  for(const [t,label] of Object.entries(grp)){
    const items=SHORT.filter(s=>s.t===t);
    if(!items.length) continue;
    h+=`<div class="railh" style="margin-top:12px">${label}</div>`+
      items.map(s=>`<div class="railitem"><b>${s.name}</b>${s.extra?`<span class="cc">${s.extra}</span>`:''}
        <button data-unstar="${s.t}|${s.name}" title="Remove">✕</button></div>`).join('');
  }
  if(SHORT.length){
    const city = ap.mode==='geo' && ap.city ? ap.city : '';
    const grp2={co:'Companies',fund:'Funds & investors',person:'People'};
    const body=Object.entries(grp2).map(([t,label])=>{
      const its=SHORT.filter(x=>x.t===t);
      return its.length?label+':\n'+its.map(x=>`- ${x.name}${x.extra?` (${x.extra})`:''}`).join('\n'):null;
    }).filter(Boolean).join('\n\n');
    const pr=`I'm planning an investor & company trip${city?` to ${city}`:''}. This is my earmarked shortlist from Sonar, Highland's relationship-intelligence tool:\n\n${body}\n\nPlease: 1) check Unframe for other high-priority pipeline companies${city?` in ${city}`:''} missing from this list, and Sonar's relevant funds there I should also see; 2) pull each company's latest status, news and any open Affinity reminders; 3) draft a short outreach email for each company and fund to set up a meeting during the trip, in my voice; 4) propose a day-by-day visit plan.`;
    h+=`<div class="railacts"><a class="minibtn prep" href="https://claude.ai/new?q=${encodeURIComponent(pr)}" target="_blank" rel="noopener">⚡ Draft trip brief in Claude</a></div>`;
    h+=`<div class="railacts"><button id="railcopy">Copy list</button><button id="railclear">Clear</button></div>`;
  }
  rail.innerHTML=h;
  rail.querySelectorAll('[data-unstar]').forEach(b=>b.addEventListener('click',()=>{
    const [t,...rest]=b.dataset.unstar.split('|'); shToggle(t,rest.join('|'));
    const body=document.getElementById('apbody'); if(body) bindStars(body);
  }));
  const cp=rail.querySelector('#railcopy');
  if(cp) cp.addEventListener('click',()=>{
    const txt=['Earmarked ('+new Date().toLocaleDateString()+')','']
      .concat(Object.entries(grp).flatMap(([t,label])=>{
        const its=SHORT.filter(s=>s.t===t);
        return its.length?[label+':',...its.map(s=>`- ${s.name}${s.extra?` (${s.extra})`:''}`),'']:[];
      })).join('\n');
    navigator.clipboard?.writeText(txt); toast('Copied');
  });
  const cl=rail.querySelector('#railclear');
  if(cl) cl.addEventListener('click',()=>{ SHORT=[]; try{localStorage.setItem('sonar_shortlist','[]');}catch(err){}
    renderRail(); const body=document.getElementById('apbody'); if(body){ body.querySelectorAll('[data-star]').forEach(b=>{b.classList.remove('on');b.textContent='☆';}); } });
}

// ---------- Ask Sonar: chat over the data via /api/ask ----------
let CHAT=[]; try{ CHAT=JSON.parse(sessionStorage.getItem('sonar_chat')||'[]'); }catch(e0){}
const ASK={busy:false};
const saveChat=()=>{ try{ sessionStorage.setItem('sonar_chat', JSON.stringify(CHAT.slice(-40))); }catch(e0){} };
const escH=s=>s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
function mdLite(t){
  return escH(t).replace(/\*\*([^*]+)\*\*/g,'<b>$1</b>').split(/\n{2,}/).map(p=>{
    const ls=p.split('\n'); let html='', list=[];
    const flush=()=>{ if(list.length){ html+='<ul>'+list.map(x=>'<li>'+x+'</li>').join('')+'</ul>'; list=[]; } };
    ls.forEach(l=>{ const m=l.match(/^\s*-\s+(.*)/); if(m) list.push(m[1]);
      else if(l.trim()){ flush(); html+=(html&&!html.endsWith('</ul>')?'<br>':'')+l; } });
    flush(); return '<p>'+html+'</p>';
  }).join('');
}
function askActsHTML(m,i){
  if(!m.actions||!m.actions.length) return '';
  return `<div class="askacts">`+m.actions.map((a,j)=>a.kind==='earmark'
    ?`<button type="button" data-act="${i}:${j}"${a.done?' disabled':''}>${a.done?'✓ Earmarked':`★ Earmark ${a.items.length} for ${escH(a.city)}`}</button>
      <button type="button" data-actopen="${escH(a.city)}">Open trip plan →</button>`:'').join('')+`</div>`;
}
function renderAskLog(){
  const log=document.getElementById('asklog'); if(!log) return;
  log.hidden=!CHAT.length&&!ASK.busy;
  log.innerHTML=CHAT.map((m,i)=>m.role==='user'
    ?`<div class="askq">${escH(m.text)}</div>`
    :`<div class="aska${m.err?' err':''}">${mdLite(m.text)}${askActsHTML(m,i)}</div>`).join('')
    +(ASK.busy?'<div class="aska pend">Sonar is checking your data<span class="dots"><i>.</i><i>.</i><i>.</i></span></div>':'');
  log.scrollTop=log.scrollHeight;
  const b=document.getElementById('askgo'); if(b) b.disabled=ASK.busy;
  const cl=document.getElementById('askclear'); if(cl) cl.hidden=!CHAT.length;
  log.querySelectorAll('[data-act]').forEach(bt=>bt.addEventListener('click',()=>{
    const [mi,aj]=bt.dataset.act.split(':').map(Number);
    const a=((CHAT[mi]||{}).actions||[])[aj]; if(!a||a.done) return;
    a.items.forEach(it=>{ const t=it.type==='fund'?'fund':'co';
      if(!shHas(t,it.name)) shToggle(t,it.name,it.note||a.city); });
    a.done=true; saveChat(); renderAskLog();
    toast(`${a.items.length} earmarked — open Plan a City Trip to see them`);
  }));
  log.querySelectorAll('[data-actopen]').forEach(bt=>bt.addEventListener('click',()=>{
    askSmall();
    ap.city=bt.dataset.actopen; goPage('geo',{city:bt.dataset.actopen});
  }));
}
async function sendAsk(q){
  if(ASK.busy) return;
  askBig();   // a real conversation deserves the big view; Esc shrinks it back, history stays
  CHAT.push({role:'user',text:q}); saveChat(); ASK.busy=true; renderAskLog();
  const inp=document.getElementById('askin'); if(inp) inp.value='';
  let ans, err;
  try{
    const r=await fetch('/api/ask',{method:'POST',headers:{'content-type':'application/json'},
      body:JSON.stringify({who:state.person||'',messages:CHAT.filter(m=>!m.err).map(m=>({role:m.role,content:m.text}))})});
    var jacts=null;
    const j=await r.json().catch(()=>({}));
    if(r.ok){ ans=j.answer; jacts=j.actions&&j.actions.length?j.actions:null; }
    else if(j.error==='not_configured') err='Chat isn\'t live yet — add ANTHROPIC_API_KEY in the Vercel project settings and redeploy.';
    else if(r.status===401) err='Your session expired — reload the page and sign in again.';
    else if(r.status===429) err='Rate limited — give it a few seconds and try again.';
    else err='Something went wrong answering that ('+(j.detail||j.error||r.status)+'). Try again.';
  }catch(e2){ err='Couldn\'t reach the chat service — this works on the deployed site.'; }
  CHAT.push(ans?{role:'assistant',text:ans,actions:jacts||undefined}:{role:'assistant',text:err,err:true});
  saveChat(); ASK.busy=false; renderAskLog();
}

const PAGES={h2c:'workpage',net:'workpage',geo:'workpage',map:'workpage'};
function askCard(){
  return `<div class="askcard">
      <div class="dph" style="margin-bottom:10px;display:flex;justify-content:space-between;align-items:center">\u2726 Ask Sonar
        <span><button type="button" id="askbig" title="Open big view">\u2922</button><button type="button" id="askclear" hidden title="Clear this conversation">\u21ba clear</button></span></div>
      <div class="asklog" id="asklog" hidden></div>
      <form class="askrow" id="askform">
        <input id="askin" placeholder="Ask about your network\u2026" autocomplete="off">
        <button type="submit" id="askgo">Ask</button>
      </form>
      <div class="askchips">${['Who should I build a relationship with next?',
          'Where are my biggest coverage gaps?',
          'Who on the team can open doors for me in London?']
        .map(q=>`<button type="button" data-q="${q.replace(/"/g,'&quot;')}">${q}</button>`).join('')}</div>
    </div>`;
}
function bindAsk(root){
  const af=root.querySelector('#askform');
  if(!af) return;
  af.addEventListener('submit',ev=>{ev.preventDefault();const v=document.getElementById('askin').value.trim();if(v)sendAsk(v);});
  root.querySelectorAll('.askchips button').forEach(b=>b.addEventListener('click',()=>sendAsk(b.dataset.q)));
  const cl=root.querySelector('#askclear');
  if(cl) cl.addEventListener('click',()=>{ CHAT=[]; saveChat(); renderAskLog(); });
  const bg=root.querySelector('#askbig');
  if(bg) bg.addEventListener('click',askBig);
  renderAskLog();
}
// the ask card lives in the sidebar; askBig moves it into a 3/4-screen overlay and askSmall puts it back.
// same DOM node either way, so the conversation (sessionStorage-backed) is never lost.
function askBig(){
  const am=document.getElementById('askmodal'), sa=document.getElementById('sideask');
  if(!am||!am.hidden||!sa) return;
  const card=sa.querySelector('.askcard'); if(!card) return;
  am.querySelector('.ambody').appendChild(card);
  am.hidden=false; renderAskLog();
  const i=document.getElementById('askin'); if(i) i.focus();
}
function askSmall(){
  const am=document.getElementById('askmodal'), sa=document.getElementById('sideask');
  if(!am||am.hidden) return;
  const card=am.querySelector('.askcard'); if(card&&sa) sa.appendChild(card);
  am.hidden=true; renderAskLog();
}
document.querySelectorAll('#askmodal [data-amclose]').forEach(b=>b.addEventListener('click',askSmall));
document.addEventListener('keydown',ev=>{
  const am=document.getElementById('askmodal');
  if(ev.key==='Escape'&&am&&!am.hidden){ ev.stopPropagation(); askSmall(); }
},true);

function goPage(p, opts){
  if(!PAGES[p]) p='map';
  state.page=p;
  document.body.dataset.page=p;
  document.getElementById('workpage').hidden = false;
  document.querySelectorAll('#side .sitem').forEach(a=>a.classList.toggle('on', a.dataset.page===p));
  const onItem=document.querySelector('#side .sitem.on');
  if(onItem&&matchMedia('(max-width:860px)').matches) onItem.scrollIntoView({block:'nearest',inline:'center'});
  ap.mode=p==='h2c'?'htc':p;
  if(opts&&opts.city) ap.city=opts.city;
  renderWork();
  updateHash();
  scrollTo(0,0);
}
function refresh(){ renderWork(); }  // re-render whatever page is active
function renderWork(){
  const titles={htc:'Solve my Hard to Cracks', net:'Daily Network Actions', geo:'Plan a City Trip', map:'Coverage Map'};
  document.getElementById('worktitle').textContent=titles[ap.mode]||'';
  const ctx=document.getElementById('apctx');
  ap.who=state.person||'';   // one identity source: the picker in the app bar
  ctx.innerHTML=(ap.mode==='geo'?` City <select id="apcity"><option value="">choose…</option>`+
      Object.keys(TRIPS).sort().map(c=>`<option${ap.city===c?' selected':''}>${c}</option>`).join('')+`</select>`:'')+
    (ap.mode==='htc'?` Sort <span class="aptog"><button data-hs="uf"${ap.hsort==='uf'?' class="on"':''}>Unframe priority</button><button data-hs="ease"${ap.hsort==='ease'?' class="on"':''}>Ease of access</button></span>`:'');
  const cs=ctx.querySelector('#apcity');
  if(cs) cs.addEventListener('change',ev=>{ap.city=ev.target.value;renderWork();updateHash();});
  ctx.querySelectorAll('[data-hs]').forEach(b=>b.addEventListener('click',()=>{ap.hsort=b.dataset.hs;renderWork();}));
  const body=document.getElementById('apbody');
  body.innerHTML = ap.mode==='map'?apMap():ap.mode==='htc'?apHtc():ap.mode==='net'?apNet():apGeo();
  if(ap.mode==='map') mapBind(body);
  if(ap.mode==='net') bindDeck(body);
  body.querySelectorAll('[data-gofund]').forEach(a=>a.addEventListener('click',ev=>{ev.preventDefault();ev.stopPropagation();goFund(a.dataset.gofund);}));
  body.querySelectorAll('[data-goh2c]').forEach(a=>a.addEventListener('click',ev=>{ev.preventDefault();goPage('h2c');}));
  body.querySelectorAll('[data-copy]').forEach(b=>b.addEventListener('click',()=>{
    navigator.clipboard?.writeText(decodeURIComponent(b.dataset.copy)); toast('Copied');}));
  body.querySelectorAll('[data-draft]').forEach(b=>b.addEventListener('click',()=>{
    const [kind,r,slug]=b.dataset.draft.split(':'); draftWidget(kind,r,slug);}));
  body.querySelectorAll('[data-gocity]').forEach(b=>b.addEventListener('click',()=>{
    ap.city=b.dataset.gocity; renderWork();
  }));
  body.querySelectorAll('[data-nseg]').forEach(b=>b.addEventListener('click',()=>{ap.nseg=b.dataset.nseg;renderWork();}));
  body.querySelectorAll('[data-nsort]').forEach(h=>h.addEventListener('click',()=>{
    const k=h.dataset.nsort;
    if(ap.ns===k) ap.nd*=-1; else {ap.ns=k; ap.nd=(k==='p'||k==='l')?-1:1;}
    renderWork();
  }));
  body.querySelectorAll('[data-nfs]').forEach(s=>s.addEventListener('change',()=>{
    ap.nf[s.dataset.nfs]=s.value; renderWork();
  }));
  const ncl=body.querySelector('#nclear');
  if(ncl) ncl.addEventListener('click',()=>{ap.nf={q:'',ty:'',st:'',sr:'',ci:''};renderWork();});
  const nq=body.querySelector('#nq');
  if(nq) nq.addEventListener('input',()=>{
    ap.nf.q=nq.value; clearTimeout(ap._nqt);
    ap._nqt=setTimeout(()=>{ renderWork();
      const el=document.getElementById('nq');
      if(el){ el.focus(); try{el.setSelectionRange(el.value.length,el.value.length);}catch(err){} }
    },300);
  });
  body.querySelectorAll('[data-cad]').forEach(b=>b.addEventListener('click',()=>{
    const k=decodeURIComponent(b.dataset.cad), cur=+b.dataset.cur||0;
    CAD[k]={0:4,4:6,6:12,12:0}[cur]??4; saveCad(); renderWork();
  }));
  bindStars(body);
  renderRail();
  document.getElementById('apscroll').scrollTop=0;
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
    const pd=htcPaths(c,who);
    let best=pd.team.slice(0,3);
    if(pd.self&&!best.some(p=>p.internal===who)) best=[pd.self,...best].slice(0,3);
    const paths=best.map(p=>`<div class="appath"><b>${p.internal===who?'you':p.internal}</b> ↔ <a href="${p.linkedin||liSearch(p.external||'',p.fund)}" target="_blank" rel="noopener">${p.external||'?'}</a> <span class="via">via ${cmFundLink(p.fund)}${p.pct!=null?` · ${p.pct}%`:''}${p.unverified?' · email-only':''}${p.ever===false?' · unverified':''}</span></div>`).join('');
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
    const eV=ease(c), eTier=eV>=50?'strong':eV>=22?'medium':'weak';
    const ufV=c.uf!=null?Math.round(c.uf):null, ufTier=ufV==null?'':ufV>=85?'strong':ufV>=70?'medium':'';
    const pr0=profOf(c);
    const m=c.meta||{};
    const since=d=>{ if(!d) return null; const mo=Math.round((Date.now()-new Date(d))/26298e5);
      return mo<1?'this month':mo+' mo'; };
    const statRows=[hcBit(pr0),
      [pr0.fu?fmtMoney(pr0.fu)+' raised':null, pr0.st?String(pr0.st).replaceAll('_',' ').toLowerCase():null,
       pr0.f?'founded '+pr0.f:null].filter(Boolean).join(' · ')||null,
      c.city||c.country,
      [(c.owners||[]).length?'owner: '+c.owners.map(o=>o.split(' ')[0]).join(', '):null,
       m.last_email?`last email ${fmtD(m.last_email)}`:null,
       m.last_meet?`met ${fmtD(m.last_meet)}`:null,
       m.status_since?`H2C for ${since(m.status_since)}`:null].filter(Boolean).join(' · ')||null
     ].filter(Boolean);
    return `<div class="apcard hcard"><div class="aph2"><div class="fname">${starBtn('co',c.name,c.city||c.country||'')}${c.domain?`<a href="https://${c.domain}" target="_blank" rel="noopener">${c.name}</a>`:c.name}</div>
      <div class="apstats">${bub(ufV, ufTierOf(ufV), 'unframe')}${bub(eV||null, easeTierOf(eV), 'ease of access')}</div></div>
      <div class="hgrid"><div class="hleft"><div class="pathh">Who can get you in</div>
        ${paths||'<div class="appath" style="color:var(--muted)">no warm path via any backer yet</div>'}
      </div><div class="hright hinfo">
        ${(pr0.d)?`<div class="apdesc">${pr0.d}</div>`:'<div class="apdesc" style="color:var(--muted)">No company profile yet.</div>'}
        <div class="hstats">${statRows.map(x=>`<div>${x}</div>`).join('')}</div>
      </div></div>${acts}</div>`;
  }).join('');
  return cards;
}


// per-contact cadence (localStorage): how often you want to touch each relationship
const CAD=(()=>{try{return JSON.parse(localStorage.getItem('sonar_cadence')||'{}');}catch(err){return {};}})();
function saveCad(){try{localStorage.setItem('sonar_cadence',JSON.stringify(CAD));}catch(err){}}
const moAgo=d=>d?(Date.now()-new Date(d).getTime())/26298e5:null;
const cadOf=e=>{const v=CAD[e.n+'|'+e.f]; return v!=null?v:(e.p>=60?4:0);};
const isCold=e=>{const c=cadOf(e), m=moAgo(e.l); return c>0&&m!=null&&m>c&&m<=24;};
function rewarmMail(e,who){
  const wf=(who||'').split(' ')[0];
  const body=`Hi ${e.n.split(' ')[0]} — been too long since we last caught up. Would love to hear what you are seeing at ${e.f} at the moment — coffee or a call in the next couple of weeks? — ${wf}`;
  return `mailto:${e.e}?subject=${encodeURIComponent('Catching up')}&body=${encodeURIComponent(body)}`;
}

/* ===== Coverage Map (flag: coverageMap) — spec docs/coverage-map/ ===== */
var CM = D.covmap||{};
var MAP = {lvl:'l0', reg:'nordics', cc:'', ent:'', lens:'both', basis:'pipe', all:false};
const CMTIER = v=>v>=70?'#2e7d4f':v>=40?'#c98a1b':v>=15?'#d96a2b':'#c2452f';
function cmU(e,me){
  if(me && e.u && e.u[me]) return e.u[me];
  const ou=Math.round(e.O*0.5*10)/10;
  return {cu:0, ou, gu:ou, g:e.O, m:Math.round(ou*(1+0.5*e.CT/100)*10)/10, st: e.O>=50?'build':'ignore', tag: e.O>=50?(e.CT>=60?'warm':e.CT<30?'cold':null):null};
}
function cmEnts(){ return (CM.ents||[]).filter(e=>!e.tray); }
function cmVisible(me){
  return cmEnts();
}
function goFund(slug){
  const e=(CM.ents||[]).find(x=>x.slug===slug); if(!e||!e.cc) return;
  MAP.reg=(CM.regOf||{})[e.cc]||MAP.reg; MAP.cc=e.cc; MAP.ent=slug; MAP.lvl='l3';
  if(state.page==='map'){ renderWork(); updateHash(); } else goPage('map');
}
function cmFundLink(name){
  if(!name) return name||'';
  const k=String(name).toLowerCase().replace(/[^a-z0-9]/g,'');
  const e=(CM.ents||[]).find(x=>x.cc&&String(x.name).toLowerCase().replace(/[^a-z0-9]/g,'')===k);
  return e?`<a href="#" data-gofund="${e.slug}">${name}</a>`:name;
}
function cmTierWord(v){ return v>=70?'Strong':v>=40?'Warm':v>=15?'Known':'Dormant'; }

function cmTeamBest(e){
  let best=null;
  (e.people||[]).forEach(p=>Object.entries(p.r).forEach(([u,r])=>{ if(!best||r>best.r) best={u, n:p.n, r:Math.round(r)}; }));
  return best;
}
function cmOpp(e,me){ return MAP.basis==='pipe'?cmU(e,me).ou:e.O; }
function cmGlyphSvg(e,me,px){
  // fixed-pixel glyph for cards and the legend: no zoom scaling, no clutter
  const u=cmU(e,me);
  const maxO=Math.max(...cmEnts().map(x=>cmOpp(x,me)),1);
  const R=(px/2-4)*(0.45+0.55*Math.sqrt(Math.max(cmOpp(e,me),1)/maxO));
  const rt=R*Math.sqrt(Math.min(e.CT,100)/100), rm=R*Math.sqrt(Math.min(u.cu,100)/100);
  const ring=u.tag==='warm'?`stroke-dasharray="${(R/4).toFixed(1)} ${(R/6).toFixed(1)}"`:'';
  const dbl=u.tag==='cold'?`<circle cx="${px/2}" cy="${px/2}" r="${(R*1.16).toFixed(1)}" class="cmring2"/>`:'';
  const shape=e.kind==='angel'
    ? `<rect x="${px/2-R}" y="${px/2-R}" width="${2*R}" height="${2*R}" transform="rotate(45 ${px/2} ${px/2})" class="cmouter" ${ring}/>`
    : `<circle cx="${px/2}" cy="${px/2}" r="${R}" class="cmouter" ${ring}/>`;
  return `<svg width="${px}" height="${px}" viewBox="0 0 ${px} ${px}">${dbl}${shape}
    <circle cx="${px/2}" cy="${px/2}" r="${rt.toFixed(1)}" class="cmteam"/>
    ${rm>0.6?`<circle cx="${px/2}" cy="${px/2}" r="${rm.toFixed(1)}" fill="${CMTIER(u.cu)}" class="cmme"/>`:''}</svg>`;
}
function cmLegend(me){
  return `<div class="cmlegend">
    <span class="cmlgi"><svg width="16" height="26" viewBox="0 0 16 26"><circle cx="8" cy="13" r="5" class="cmnode"/></svg><svg width="26" height="26" viewBox="0 0 26 26"><circle cx="13" cy="13" r="11" class="cmnode"/></svg>bigger = more of Highland's deal flow and pipeline runs through this area</span>
    <span class="cmlgi"><svg width="26" height="26" viewBox="0 0 26 26"><circle cx="13" cy="13" r="11" class="cmouter"/><circle cx="13" cy="13" r="8.5" class="cmteam"/><circle cx="13" cy="13" r="5.5" style="fill:var(--accent-ink)"/></svg>hover: pale ring = team coverage · solid centre = ${me?'yours':'mine'}</span>
  </div>`;
}
function apMap(){
  if(!CM.ents) return '<div class="aphint">Coverage map data has not been built yet.</div>';
  const me=ap.who||'';
  const regName=(CM.regions.find(r=>r.id===MAP.reg)||{}).name||MAP.reg;
  const solo=((CM.subsOf||{})[MAP.reg]||[]).length<=1;
  const crumbs=[`<button data-cmgo="l0"${MAP.lvl==='l0'?' disabled':''}>Map</button>`];
  if(MAP.lvl!=='l0'&&!solo) crumbs.push(`<button data-cmgo="l1"${MAP.lvl==='l1'?' disabled':''}>${regName}</button>`);
  if(MAP.cc) crumbs.push(`<button data-cmgo="l2"${!MAP.ent?' disabled':''}>${CM.ccName[MAP.cc]||MAP.cc}</button>`);
  if(MAP.ent){ const e=(CM.ents||[]).find(x=>x.slug===MAP.ent); if(e) crumbs.push(`<button disabled>${e.name}</button>`); }
  const back=MAP.lvl!=='l0'?`<button class="minibtn cmback" data-cmback>← Back</button>`:'';
  const isMapLvl=MAP.lvl==='l0'||MAP.lvl==='l1';
  let main;
  if(MAP.ent) main=cmDetail(me);
  else if(isMapLvl) main=`<div class="cmmapwrap full"><svg id="cmsvg" viewBox="${(CM.vb[MAP.lvl==='l0'?'l0':MAP.reg]||CM.vb.l0).join(' ')}" preserveAspectRatio="${MAP.lvl==='l0'?'xMidYMid slice':'xMidYMid meet'}">${cmSvg(me)}</svg><div id="cmhover" class="cmcard" hidden></div>${MAP.lvl==='l1'?`<div class="cmpanel float" id="cmpanel">${cmPanel(me)}</div>`:''}</div>`;
  else main=cmCountryPage(me);
  return `<div class="cmtop">
      ${back}<span class="cmcrumb">${crumbs.join('<span class="psep">›</span>')}</span>

    </div>
    ${isMapLvl&&!MAP.ent?cmLegend(me):''}
    ${main}`;
}
function cmSvg(me){
  const hl=new Set((CM.hl||{})[MAP.reg]||[]);
  const base=CM.countries.map(c=>{
    if(c.bg) return `<path d="${c.d}" class="cmbg"/>`;
    const a=CM.areas[c.id], covu=a&&me&&a.u[me]?a.u[me].covu:0;
    const on=(MAP.lvl!=='l0')&&hl.has(c.id);
    return `<path d="${c.d}" class="cmcty${on?' on':''}" data-cmcc="${c.id}" style="${on&&a?'fill:var(--accent);fill-opacity:.07':''}"/>`;
  }).join('');
  let layer='';
  if(MAP.lvl==='l0'){
    const liveR=CM.regions.filter(r=>r.active&&CM.areas[r.id]);
    const maxW0=Math.max(...liveR.map(r=>0.5*CM.areas[r.id].opp+0.5*(CM.areas[r.id].pw||0)),1);
    layer=CM.regions.map(r=>{
      if(!r.active||!CM.areas[r.id]) return `<g class="cmreg soon" data-cmsoon="${r.name}" transform="translate(${r.x},${r.y})"><circle r="7" class="cmsoonnode"/></g>`;
      const a=CM.areas[r.id], covu=me&&a.u[me]?a.u[me].covu:0;
      const w0=(0.5*a.opp+0.5*(a.pw||0))/maxW0;   // node weight = deal flow + team pipeline
      // one colour, size = how much the area matters; hover breaks out team ring + your centre
      const rb=(4+9*Math.sqrt(w0)), R=(16+13*Math.sqrt(w0));
      const rt=R*Math.sqrt(a.covT/100), rm=R*Math.sqrt(covu/100);
      return `<g class="cmreg live cmregbtn cmswap" ${r.solo?`data-cmcc2="${r.solo}"`:`data-cmgo="l1"`} data-cmreg="${r.id}" transform="translate(${r.x},${r.y})">
        <title>${r.name}</title>
        <g class="cmbtn"><circle r="${rb.toFixed(1)}" class="cmnode"/></g>
        <g class="cmdisc"><circle r="${R.toFixed(1)}" class="cmouter"/><circle r="${rt.toFixed(1)}" class="cmteam"/>
          ${rm>1?`<circle r="${rm.toFixed(1)}" class="cmme" style="fill:var(--accent-ink)"/>`:''}</g></g>`;
    }).join('');
  } else {
    const subs=(CM.subsOf||{})[MAP.reg]||[];
    const rvb=CM.vb[MAP.reg]||CM.vb.l0;
    // contain-fit: px per map unit ≈ min(width/vbW, height/vbH); size everything off that
    const sEst=Math.min(1500/rvb[2], 680/rvb[3]);
    const maxo=Math.max(...subs.map(sb=>CM.areas[sb.id]?CM.areas[sb.id].opp:0),1);
    const maxp=Math.max(...subs.map(sb=>CM.areas[sb.id]?CM.areas[sb.id].pw||0:0),1);
    const nodes=subs.filter(sb=>CM.areas[sb.id]).map(sb=>{
      const a=CM.areas[sb.id], covu=me&&a.u[me]?a.u[me].covu:0;
      const wgt=0.5*(a.opp/maxo)+0.5*((a.pw||0)/maxp);   // size = deal flow opportunity + the team's pipeline weight here
      const R=(12+50*Math.sqrt(wgt))/sEst, rb=(8+28*Math.sqrt(wgt))/sEst;
      const rt=R*Math.sqrt(a.covT/100), rm=R*Math.sqrt(covu/100);
      const exp=me&&a.u[me]&&a.u[me].exp>=15&&covu<50;
      return {sb,a,covu,R,rb,rt,rm,exp,x:sb.x,y:sb.y};
    });
    // satellite cities can sit inside a giant neighbour's disc (Cambridge/Oxford vs London):
    // push the smaller node out along the joining axis until the discs clear
    for(let it=0;it<3;it++) for(let i=0;i<nodes.length;i++) for(let j=i+1;j<nodes.length;j++){
      const A=nodes[i],B=nodes[j];
      const dx=B.x-A.x, dy=B.y-A.y, d=Math.hypot(dx,dy)||0.01, need=A.R+B.R+10/sEst;
      if(d<need){ const s=A.R>=B.R?B:A, dir=s===B?1:-1, push=need-d;
        s.x+=dx/d*push*dir; s.y+=dy/d*push*dir; }
    }
    layer=nodes.map(n=>`<g class="cmreg live cmswap" data-cmcc2="${n.sb.id}" transform="translate(${n.x.toFixed(1)},${n.y.toFixed(1)})">
        <g class="cmbtn"><circle r="${n.rb.toFixed(1)}" class="cmnode"/></g>
        <g class="cmdisc"><circle r="${n.R.toFixed(1)}" class="cmouter"/><circle r="${n.rt.toFixed(1)}" class="cmteam"/>
          ${n.rm>0.4?`<circle r="${n.rm.toFixed(1)}" class="cmme" style="fill:var(--accent-ink)"/>`:''}</g>
        <text y="${(n.y>rvb[1]+rvb[3]*0.8?-(n.R+8/sEst):(n.R+16/sEst)).toFixed(1)}" style="font-size:${(14.5/sEst).toFixed(2)}px">${n.sb.name}${n.exp?' ⚑':''}</text></g>`).join('');
  }
  return `<g class="cmbaseg">${base}</g><g class="cmlayer">${layer}</g>`;
}

const SRRANK={Partner:0,Director:1,Associate:2};

function cmTarget(e,me){
  const ppl=[...(e.people||[])].sort((a,b)=>(SRRANK[a.sr]??3)-(SRRANK[b.sr]??3));
  return ppl.find(p=>!me||(p.r[me]||0)<15)||ppl[0];
}
function cmSpendList(me,list){
  const cards=list.map(e=>{
      const u=cmU(e,me);
      const myN=(()=>{let n=0;Object.entries(e.pipe||{}).forEach(([bk,v])=>{if(bk!=='portfolio')v.forEach(co=>{if(co.o&&co.o.includes(me))n++;});});return n;})();
      const h2cN=((e.pipe||{}).hard||[]).length;
      const chips=[];
      if(u.st==='maintain'||u.st==='over'){
        const bl=(e.people||[]).filter(p=>me&&p.r[me]).map(p=>p.last||'').sort().pop()||'';
        const days=bl?Math.round((Date.now()-new Date(bl))/864e5):9e9;
        chips.push(days<=150?['warm',`Strong${bl?' · '+fmtD(bl):''}`]
                            :['cold',`Going quiet${bl?' · '+fmtD(bl):''}`]);
      }
      if(u.tag==='warm') chips.push(['warm','Warm path']);
      if(u.tag==='cold') chips.push(['cold','Cold start']);
      if((e.df12||0)>=6) chips.push(['df','High deal flow']);
      if(myN>0) chips.push(['pipe','Active in your pipe']);
      else if(h2cN>0) chips.push(['pipe',`Backs ${h2cN} H2C${h2cN>1?'s':''}`]);
      return `<div class="cmspend go" data-cment="${e.slug}" tabindex="0">
        <div class="cmfn">${e.name}</div>
        <div class="cmbigs">${chips.slice(0,3).map(([k,l])=>`<span class="cmbig ${k}">${l}</span>`).join('')||'<span class="cmbig">Top deal flow here</span>'}</div>
      </div>`;
    }).join('');
  return cards||'<div class="aphint">None right now.</div>';
}
function cmWhoRows(me){
  const rows=(CM.who||{})[MAP.cc]||[];
  const mine=!MAP.whoTeam;
  const SRW={Partner:1,Director:.8,Associate:.55};
  const list=rows.map(p=>{
    const best=Object.entries(p.r).sort((x,y)=>y[1]-x[1])[0];
    const r=mine?(me?(p.r[me]||0):0):(best?best[1]:0);
    if(r<15) return null;
    // door value: how strong the line is x how much the seat matters
    const val=(r/100)*(0.45+((p.o??40)/100)*0.55)*(SRW[p.sr]||0.7);
    return {p, r, val, holder: mine?null:(best?best[0]:null)};
  }).filter(Boolean).sort((a,b)=>b.val-a.val);
  const doors=list.slice(0,7).map(({p,r,holder})=>{
    const tc=r>=70?'warm':r>=40?'df':'pipe';
    return `<div class="cmspend cmdoor${p.slug?' go':''}"${p.slug?` data-cment="${p.slug}"`:''}>
      <div class="cmfn"><a href="${p.li||liSearch(p.n,p.org||'')}" target="_blank" rel="noopener">${p.n}</a>${p.sr?` <span class="cc">· ${p.sr}</span>`:''}</div>
      <div class="cmbigs">
        <span class="cmbig">${p.org||'—'}</span>
        <span class="cmbig ${tc}">${cmTierWord(r)}${p.last?` · ${fmtD(p.last)}`:''}</span>
        ${(p.o||0)>=70?`<span class="cmbig df">Top fund here</span>`:(p.df||0)>=6?`<span class="cmbig df">High deal flow</span>`:''}
        ${holder?`<span class="cmbig">via ${holder.split(' ')[0]}</span>`:''}
      </div></div>`;
  }).join('');
  const rest=list.slice(7);
  const restHtml=rest.length?(MAP.whoMore
    ?rest.map(({p,r,holder})=>`<div class="dpli"><b class="mbub ${r>=70?'strong':r>=40?'medium':'low'}">${Math.round(r)}</b><span class="nm"><a href="${p.li||liSearch(p.n,p.org||'')}" target="_blank" rel="noopener">${p.n}</a></span><span class="how">${p.org||''}${holder?` · via ${holder.split(' ')[0]}`:''}${p.last?` · ${fmtD(p.last)}`:''}</span></div>`).join('')+`<button class="minibtn" data-cmwhomore="0">Hide ↑</button>`
    :`<button class="minibtn" data-cmwhomore="1">+ ${rest.length} more</button>`):'';
  return {html:(doors||`<div class="dtsub">${mine?'Open ground — flip to Team and ask for an intro.':'No team edges here.'}</div>`)+restHtml, n:list.length};
}
function cmCountryPage(me){
  const cc=MAP.cc, A=CM.areas[cc]||{covT:0,u:{},known:{}};
  const covu=me&&A.u[me]?A.u[me].covu:0, exp=me&&A.u[me]?A.u[me].exp:null;
  const [qu]=cmQualU(covu), [qt]=cmQualT(A.covT);
  const known=me?(A.known&&A.known[me]||0):0;
  const sel=cmEnts().filter(e=>e.cc===cc&&e.sl&&!e.rm);
  const selAff=(CM.aff||[]).filter(e=>e.cc===cc&&e.sl&&!e.rm);
  const forceIn=me?cmEnts().filter(e=>e.cc===cc&&!e.sl&&!e.rm&&(e.pu&&e.pu[me])):[];
  const short=[...sel,...forceIn];
  const who=cmWhoRows(me);
  const over=short.filter(e=>cmU(e,me).st==='over').sort((a,b)=>cmU(b,me).cu-cmU(a,me).cu);
  const groups=[['build','Build'],['maintain','Maintain'],['over','Already strong']].map(([st,label])=>{
    const g=short.filter(e=>cmU(e,me).st===st);
    if(!g.length) return '';
    return `<div class="apsec">${label} — ${g.length}</div>${g.sort((a,b)=>cmU(b,me).gu-cmU(a,me).gu).map(e=>{
      const u=cmU(e,me);
      return `<div class="dpli" data-cment="${e.slug}"><b class="mbub ${u.cu>=70?'strong':u.cu>=40?'medium':u.cu>=15?'low':'weak'}">${Math.round(u.cu)}</b><span class="nm">${e.name}${e.pin?' ★':''}${!e.sl?' <span class="cc">· in via your pipeline</span>':''}</span><span class="how">${e.city||''} · team ${Math.round(e.CT)}${u.tag?' · '+(u.tag==='warm'?'warm path':'cold start'):''}</span></div>`;
    }).join('')}`;
  }).join('');
  const allN=cmEnts().filter(e=>e.cc===cc).length+(CM.aff||[]).filter(e=>e.cc===cc).length;
  // stage shape: one honest sentence when the viewer's early vs growth coverage diverge hard
  const stageLine=(()=>{
    if(!me) return '';
    const bucket=f=>/early|seed/i.test(f||'')?'e':/growth|late/i.test(f||'')?'g':null;
    const agg={e:[0,0,0],g:[0,0,0]};
    cmEnts().filter(e=>e.cc===cc&&!e.rm&&e.fs).forEach(x=>{
      const b=bucket(x.fs); if(!b) return;
      agg[b][0]+=x.O*((x.cu||{})[me]||0); agg[b][1]+=x.O; agg[b][2]++;
    });
    if(agg.e[2]<3||agg.g[2]<3) return '';
    const ce=agg.e[0]/agg.e[1], cg=agg.g[0]/agg.g[1];
    if(cg-ce>=25) return ` At the growth funds here your network is <b>${cmQualU(cg)[0]}</b> — the early-stage volume funds are your open ground.`;
    if(ce-cg>=25) return ` Early-stage is your strength here — the growth funds are your open ground.`;
    return '';
  })();
  const youBit=qu==='well covered'?`your network is <b>well covered</b>`
    :qu==='building'?`your network is <b>building</b>`
    :`<b>open ground</b> for you`;
  const teamBit=A.covT>=50&&covu<50?`the team is <b>${qt}</b> — ask for the intros`:`the team is ${qt}`;
  const tripBit=(()=>{
    const CITY_OF={SE:'Stockholm',DK:'Copenhagen',NO:'Oslo',FI:'Helsinki',FR:'Paris',BER:'Berlin',MUC:'Munich',CGN:'Cologne & Bonn',FRA:'Frankfurt',HAM:'Hamburg',LON:'London',CAM:'Cambridge',OXF:'Oxford',EDI:'Edinburgh',MAN:'Manchester',SF:'SF Bay Area',NYC:'New York',BOS:'Boston'};
    const tc=CITY_OF[cc]; if(!tc||typeof cityScores!=='function') return '';
    try{ if(!cityScores(me).some(x=>x.city===tc)) return ''; }catch(err){ return ''; }
    return `<div style="margin:8px 0 2px"><button class="minibtn" data-cmtrip="${tc}">\u2708 Plan a${tc==='SF Bay Area'?'n SF':' '+tc} trip</button></div>`;
  })();
  return `<div class="cmhead">${CM.ccName[cc]}: ${youBit}, ${teamBit}.${exp!=null?` ${Math.round(exp)}% of your pipeline in this region sits here.`:''} You know <b>${known}</b> people here.${stageLine}</div>${tripBit}
    <div class="cmv2grid">
      <div>
        ${(()=>{const all=[...short,...selAff].sort((a,b)=>cmU(b,me).m-cmU(a,me).m);
          const builds=all.filter(e=>cmU(e,me).st==='build').slice(0,6);
          const reng=all.filter(e=>cmU(e,me).st==='maintain').slice(0,6);
          return `<div class="cmspendcols">
            <div><div class="apsec">Build</div>${cmSpendList(me,builds)}</div>
            <div><div class="apsec">Keep close</div>${cmSpendList(me,reng)}</div>
          </div>`;})()}
      </div>
      <div>
        <div class="apsec">Your doors in ${CM.ccName[cc]} <span class="aptog" style="margin-left:8px"><button data-cmwho="me"${!MAP.whoTeam?' class="on"':''}>Mine</button><button data-cmwho="team"${MAP.whoTeam?' class="on"':''}>Team</button></span></div>
        <div class="dtsub" style="margin:-2px 0 8px">Strongest first — relationship × how much the seat matters.</div>
        <div>${who.html}</div>
        ${over.length?`<div class="apsec" style="margin-top:14px">Keep warm</div>
        <div class="apcard cmquiet">${over.slice(0,8).map(e=>`<div class="dpli" data-cment="${e.slug}"><b class="mbub low">${Math.round(cmU(e,me).cu)}</b><span class="nm">${e.name}</span><span class="how">strong relationship · little deal flow</span></div>`).join('')}</div>`:''}
      </div>
    </div>
    ${(()=>{const pinned=((CM.pinsIn||{})[cc]||[]);if(!pinned.length)return '';
      return `<div class="apsec" style="margin-top:16px">Also in ${CM.ccName[cc]} — teams based elsewhere with investors on the ground</div>
      <div class="apcard cmquiet">${pinned.slice(0,12).map(p=>`<div class="dpli"><span class="nm"><a href="#" data-gofund="${p.slug}">${p.name}</a></span><span class="how">${p.ppl.join(', ')} · HQ ${CM.ccName[p.cc]||p.cc}</span></div>`).join('')}</div>`;})()}
    <div style="margin-top:16px">${MAP.showAll?`<button class="minibtn" data-cmhideall>Hide the long tail ↑</button>${cmAffCards(me)}${cmPeopleIn(me)}<div style="margin-top:10px"><button class="minibtn" data-cmhideall>Hide ↑</button></div>`:`<button class="minibtn" data-cmshowall>Show all ${allN} investors in ${CM.ccName[cc]}</button>`}</div>`;
}
function cmAffCards(me){
  const sel=(CM.aff||[]).filter(e=>e.cc===MAP.cc&&!e.sl)
    .sort((a,b)=>((me&&b.cu[me])||0)-((me&&a.cu[me])||0)||b.CT-a.CT||a.name.localeCompare(b.name));
  if(!sel.length) return '';
  const known=sel.filter(e=>e.CT>0).length;
  const cards=sel.map(e=>{
    const cu=me?(e.cu[me]||0):0;
    const best=e.people&&e.people[0];
    return `<div class="cmfcard aff go" data-cment="${e.slug}">
      <div class="cmfi">
        <div class="cmfn">${e.name} <span class="cmst">untracked</span></div>
        <div class="cmfm">${e.city||'—'}${e.lc?` · last call ${fmtD(e.lc)}`:''}</div>
        <div class="cmfm">${e.CT>0?`team <b>${Math.round(e.CT)}</b>${me&&cu?` · you <b style="color:${CMTIER(cu)}">${Math.round(cu)}</b>`:''}${best?` · via ${best.n}`:''}`:'no relationship logged'}</div>
      </div></div>`;
  }).join('');
  return `<div class="apsec" style="margin-top:16px">Also in Affinity — every other ${CM.ccName[MAP.cc]}-based investor (${sel.length}, ${known} with a live relationship)</div>
    <div class="cmcards">${cards}</div>`;
}
function cmPeopleIn(me){
  const by=(CM.peopleIn||{})[MAP.cc];
  if(!by) return '';
  const mine=me?(by[me]||[]):[];
  const teamN=new Set(Object.values(by).flat().map(p=>p.n)).size;
  if(!mine.length&&!teamN) return '';
  const rows=mine.map(p=>`<div class="dpli"><b class="mbub ${p.p>=70?'strong':p.p>=40?'medium':'low'}">${p.p}</b><span class="nm">${p.n}</span><span class="how">${p.f||''}${p.c?' · '+p.c:''}</span></div>`).join('');
  return `<div class="apsec" style="margin-top:16px">People you know in ${CM.ccName[MAP.cc]} — beyond the tracked funds</div>
    <div class="apcard">${rows||`<div class="dtsub">None on your own book.</div>`}
    <div class="dtsub" style="margin-top:6px">${teamN} ${CM.ccName[MAP.cc]}-based investors known across the team — sourced from each person's live Harmonic location.</div></div>`;
}
function cmDetail(me){
  const A=(CM.aff||[]).find(x=>x.slug===MAP.ent);
  if(A&&!(CM.ents||[]).find(x=>x.slug===MAP.ent)){
    return `<div class="cmdet">
      <div class="cmdeth"><div style="min-width:0">
        <div class="cmdetn">${A.name} <span class="cmst">In Affinity · untracked</span></div>
        <div class="cmfm">${A.city||'—'}${A.ft?' · '+A.ft:''}${A.fs?' · '+A.fs:''}${A.lc?` · last Highland contact ${fmtD(A.lc)}`:''}</div>
        ${A.desc?`<div class="cmwhy">${A.desc}</div>`:''}
      </div></div>
      <div class="apsec">Team — from Harmonic</div>
      ${(A.team||[]).map(t=>`<div class="dpli"><span class="nm"><a href="${liSearch(t.n,A.name)}" target="_blank" rel="noopener">${t.n}</a></span><span class="how">${t.t||''}</span></div>`).join('')||'<div class="dtsub">No people mapped yet.</div>'}
      ${(A.people||[]).length?`<div class="apsec">Highland edges</div>${A.people.map(p=>{const bt=Object.entries(p.r).sort((x,y)=>y[1]-x[1])[0];return `<div class="dpli"><b class="mbub ${bt[1]>=70?'strong':bt[1]>=40?'medium':'low'}">${Math.round(bt[1])}</b><span class="nm">${p.n}</span><span class="how">via ${bt[0].split(' ')[0]}</span></div>`;}).join('')}`:''}
      <div class="dtsub" style="margin-top:10px">Not yet a tracked fund — relationship data here comes from the network graph alone.</div>
    </div>`;
  }
  const e=(CM.ents||[]).find(x=>x.slug===MAP.ent);
  if(!e) return '';
  const u=cmU(e,me), tb=cmTeamBest(e), tgt=cmTarget(e,me);
  const state=u.st==='build'?(u.tag==='warm'?'Build · warm path':u.tag==='cold'?'Build · cold start':'Build'):u.st==='maintain'?'Maintain':u.st==='over'?'Already strong':'Quiet';
  // why, as numbers, largest first
  const ORDER=[['lead','Lead'],['prelead','Pre-lead'],['awaiting','Awaiting lead'],['hard','Hard to crack'],['reachout','Reach out'],['portfolio','Portfolio']];
  const pipeAll=[]; ORDER.forEach(([bk,label])=>{(e.pipe&&e.pipe[bk]||[]).forEach(co=>pipeAll.push({n:co.n,st:label,mine:co.o&&co.o.includes(me)}));});
  const myN=pipeAll.filter(c=>c.mine).length, h2cN=(e.pipe&&e.pipe.hard||[]).length;
  const why=[[myN,`backs <b>${myN}</b> of your pipeline`],[e.df12||0,`<b>${e.df12||0}</b> new deals in 12 months`],[h2cN,`backs <b>${h2cN}</b> hard to crack${h2cN>1?'s':''}`],[pipeAll.length,`<b>${pipeAll.length}</b> pipeline links in all`]]
    .filter(x=>x[0]>0).sort((a,b)=>b[0]-a[0]).map(x=>x[1]);
  const topCos=[...pipeAll].sort((a,b)=>(a.mine===b.mine?0:a.mine?-1:1)).slice(0,3);
  const move=u.tag==='warm'&&tb?[`Ask ${tb.u.split(' ')[0]} for an intro to ${tb.n}`,`mailto:${hlMail(tb.u)}?subject=${encodeURIComponent('Intro to '+tb.n+' ('+e.name+')?')}&body=${encodeURIComponent('Hey '+tb.u.split(' ')[0]+' — could you introduce me to '+tb.n+' at '+e.name+'? — '+(me||'').split(' ')[0])}`,'✉ Draft intro request']:
    u.st==='over'?['Slow the cadence — little deal flow for the time spent',null,null]:
    tgt?[`Approach ${tgt.n}${tgt.sr?` (${tgt.sr})`:''} directly`,liSearch(tgt.n,e.name),'Draft outreach ↗']:['Map the team first',null,null];
  const ppl=[...(e.people||[])].sort((a,b)=>{
    const sr=(SRRANK[a.sr]??3)-(SRRANK[b.sr]??3); if(sr) return sr;
    const gap=p=>{const best=Math.max(...Object.values(p.r),0);return best-(me?(p.r[me]||0):0);};
    return gap(b)-gap(a);
  });
  const rows=ppl.map(p=>{
    const mr=me?Math.round(p.r[me]||0):0, bt=Object.entries(p.r).sort((x,y)=>y[1]-x[1])[0];
    return `<tr><td><b class="mbub ${mr>=70?'strong':mr>=40?'medium':mr>=15?'low':'weak'}">${mr}</b></td>
      <td class="nmc"><a href="${p.li||liSearch(p.n,e.name)}" target="_blank" rel="noopener">${p.n}</a></td><td>${p.sr||'—'}</td>
      <td>${bt?`${cmTierWord(bt[1])} · ${bt[0].split(' ')[0]}`:'—'}</td>
      <td class="lt">${p.last?fmtD(p.last):'—'}</td></tr>`;
  }).join('');
  const untracked=(e.dfl||[]).filter(d=>!d.aid);
  const others=pipeAll.filter(c=>['Reach out','Portfolio'].includes(c.st));
  const acc=(id,label,n,body,open)=>n?`<details class="cmacc"${open?' open':''}><summary>${label} <b>${n}</b></summary>${body}</details>`:'';
  const lnk=(txt,aid)=>aid?`<a href="${affURL(aid)}" target="_blank" rel="noopener">${txt}</a>`:txt;
  const pipeRows=bk=>((e.pipe&&e.pipe[bk])||[]).map(co=>`<div class="dpli"><span class="nm">${lnk(co.o&&co.o.includes(me)?`<b>${co.n}</b>`:co.n,co.aid)}</span><span class="how">${(co.o||[]).map(x=>x.split(' ')[0]).join(', ')}</span></div>`).join('');
  const topReason=why[0]||'';
  const openKey=topReason.includes('pipeline')?'pipe':topReason.includes('deals')?'df':topReason.includes('hard')?'h2c':'df';
  return `<div class="cmdet">
    <div class="cmdeth">${cmGlyphSvg(e,me,74)}<div style="min-width:0">
      <div class="cmdetn">${e.name} <span class="cmst ${u.st}">${state}</span></div>
      <div class="cmfm">${e.city||'—'} · ${e.cat||e.kind}${e.fs?' · '+e.fs:''} · team <b>${Math.round(e.CT)}</b>${me?` · you <b style="color:${CMTIER(u.cu)}">${Math.round(u.cu)}</b>`:''}</div>
      ${why.length?`<div class="cmfm">${why.join(' · ')}</div>`:''}
      ${topCos.length?`<div class="cmfm">${topCos.map(c=>`${c.mine?`<b>${c.n}</b>`:c.n} <span class="cc">(${c.st})</span>`).join(' · ')}</div>`:''}
      <div class="cmfm cmask">${move[0]}${move[1]?` — <a href="${move[1]}"${move[2].includes('↗')?' target="_blank" rel="noopener"':''}>${move[2]}</a>`:''}</div>
    </div></div>
    <div class="cmv2grid">
      <div>
        <div class="apsec">People</div>
        <table class="nettab cmdett"><thead><tr><th>You</th><th>Name</th><th>Role</th><th>Team best</th><th>Last touch</th></tr></thead>
        <tbody>${rows||`<tr><td colspan="6" class="lt" style="padding:12px">No people mapped yet.</td></tr>`}</tbody></table>
      </div>
      <div>${cmEgo(e,me)}</div>
    </div>
    ${acc('df','Recent deal flow',(e.dfl||[]).length,(e.dfl||[]).map(d=>`<div class="dpli"><span class="nm">${d.aid?`<a href="${affURL(d.aid)}" target="_blank" rel="noopener">${d.n}</a>`:d.n}</span><span class="how">${[d.r||null,d.d?fmtD(d.d):null,d.fu?`in pipeline: ${d.fu}`:null].filter(Boolean).join(' · ')}</span></div>`).join(''),openKey==='df')}
    ${acc('pl','Pre-lead',((e.pipe||{}).prelead||[]).length,pipeRows('prelead'),openKey==='pipe')}
    ${acc('aw','Awaiting lead',((e.pipe||{}).awaiting||[]).length,pipeRows('awaiting'),false)}
    ${acc('h2','Hard to crack portfolio',h2cN,pipeRows('hard')+(h2cN?`<div class="dtsub" style="margin-top:6px"><a href="#" data-goh2c>Work these in Solve my Hard to Cracks \u2192</a></div>`:''),openKey==='h2c')}
    ${acc('un','Recent deals we are not tracking',untracked.length,untracked.map(d=>`<div class="dpli"><span class="nm">${d.n}</span><span class="how">${[d.r||null,d.d?fmtD(d.d):null,d.do||null].filter(Boolean).join(' · ')}</span><button class="minibtn" data-copy="${encodeURIComponent(d.n+(d.do?' — '+d.do:''))}">Add to Affinity</button></div>`).join(''),false)}
    ${acc('ot','Other portfolio in Highland pipeline',others.length,others.map(c=>`<div class="dpli"><span class="nm">${c.mine?`<b>${c.n}</b>`:c.n}</span><span class="how">${c.st}</span></div>`).join(''),false)}
  </div>`;
}
function cmEgo(e,me){
  const ppl=(e.people||[]).slice(0,8);
  if(!ppl.length) return '';
  const ints=[...new Set(ppl.flatMap(p=>Object.keys(p.r)))].sort((a,b)=>Math.max(...ppl.map(p=>p.r[b]||0))-Math.max(...ppl.map(p=>p.r[a]||0))).slice(0,6);
  if(!ints.length) return '';
  const H=Math.max(ppl.length,ints.length)*32+36;
  const iy=i=>26+i*((H-36)/Math.max(ints.length-1,1)||0);
  const py=i=>26+i*((H-36)/Math.max(ppl.length-1,1)||0);
  const lines=ints.flatMap((u,ui)=>ppl.map((p,pi)=>{
    const r=p.r[u]||0; if(r<10) return '';
    return `<line x1="155" y1="${iy(ui)}" x2="305" y2="${py(pi)}" stroke="${CMTIER(r)}" stroke-width="${(0.6+r/40).toFixed(1)}" opacity="${u===me?0.95:0.3}"/>`;
  })).join('');
  return `<div class="apsec" style="margin-top:14px">Who holds the lines in</div>
    <svg class="cmego" width="100%" height="${H}" viewBox="0 0 470 ${H}">${lines}
      ${ints.map((u,i)=>`<text x="149" y="${iy(i)+4}" text-anchor="end" class="cml3t${u===me?' me':''}">${u}</text>`).join('')}
      ${ppl.map((p,i)=>`<text x="311" y="${py(i)+4}" class="cml3t">${p.n}${p.sr?` · ${p.sr}`:''}</text>`).join('')}
    </svg>`;
}

function cmYouLine(covu,covT){
  const [qu]=cmQualU(covu), [qt]=cmQualT(covT);
  if(covu>=50) return `Your network here is <b>${qu}</b>; the team's graph is ${qt}.`;
  if(covT>=50) return `<b>${qu==='building'?'Building':'Open ground'}</b> for you — the team's network here is <b>strong</b>, and the intros are one ask away.`;
  return `<b>${qu==='building'?'Building':'Open ground'}</b> — for you and the team. First-mover territory.`;
}
const cmQualU=v=>v<25?['open ground','#3a6fa5']:v<50?['building','#c98a1b']:['well covered','#2e7d4f'];
const cmQualT=v=>v<25?['early','#3a6fa5']:v<50?['growing','#c98a1b']:['strong','#2e7d4f'];
function cmQualRow(covu,covT,me){
  const [qu,cu]=cmQualU(covu), [qt,ct]=cmQualT(covT);
  return `<div class="cmquals">${me?`<span class="cmqual" style="color:${cu};border-color:${cu}">You · ${qu}</span>`:''}<span class="cmqual" style="color:${ct};border-color:${ct}">Team · ${qt}</span></div>`;
}

function cmTop5(me,pool){
  const rows=[...pool].sort((a,b)=>cmU(b,me).m-cmU(a,me).m).slice(0,5).map(e=>{
    const u=cmU(e,me), tb=cmTeamBest(e);
    const how=u.tag==='warm'&&tb?`ask ${tb.u.split(' ')[0]} → ${tb.n}`:u.tag==='cold'?'cold start':u.st==='maintain'?'keep warm':'build';
    return `<div class="dpli" data-cment="${e.slug}"><b class="mbub ${u.cu>=70?'strong':u.cu>=40?'medium':u.cu>=15?'low':'weak'}">${Math.round(u.cu)}</b><span class="nm">${e.name}</span><span class="how">${e.city||''} · ${how}</span></div>`;
  }).join('');
  return rows||'<div class="dtsub">Nothing to build here.</div>';
}
function cmPanel(me){
  const A=CM.areas, who=me||null;
  const regName=(CM.regions.find(r=>r.id===MAP.reg)||{}).name||'this region';
  const regSubs=((CM.subsOf||{})[MAP.reg]||[]).map(sb=>sb.id);
  const regPool=cmVisible(me).filter(e=>regSubs.includes(e.cc));
  if(MAP.lvl==='l0'){
    const a=A[MAP.reg]||A.nordics, covu=who&&a.u[who]?a.u[who].covu:0;
    const [qu]=cmQualU(covu), [qt]=cmQualT(a.covT);
    return `<div class="cmhead">${who?cmYouLine(covu,a.covT):`The team's ${regName} coverage is <b>${qt}</b>.`}</div>
      ${cmQualRow(covu,a.covT,who)}`;
  }
  if(MAP.lvl==='l1'){
    const a=A[MAP.reg], covu=who&&a.u[who]?a.u[who].covu:0;
    const biggest=regSubs.filter(c=>A[c]).sort((x,y)=>A[y].opp-A[x].opp)[0];
    const bcov=who&&A[biggest]&&A[biggest].u[who]?A[biggest].u[who].covu:0;
    const [qu]=cmQualU(covu), [qt]=cmQualT(a.covT);
    const borrow=a.covT>=50&&covu<50;
    return `<div class="cmhead">${who?(covu>=50
        ?`Your ${regName} network is <b>well covered</b>. ${CM.ccName[biggest]||''} drives the most opportunity here.`
        :`${['Germany','US tier-1'].includes(regName)?regName:'The '+regName} is where your network has the most room to grow: ${CM.ccName[biggest]||''} drives the most opportunity${borrow?` — and the team can already make the intros`:''}.`)
      :`The team's ${regName} coverage is <b>${qt}</b>.`}</div>
      ${cmQualRow(covu,a.covT,who)}`;
  }
  const cc=MAP.cc, a=A[cc]||{covT:0,u:{}};
  const sel=cmEnts().filter(e=>e.cc===cc);
  const builds=sel.filter(e=>cmU(e,me).st==='build');
  const warm=builds.filter(e=>cmU(e,me).tag==='warm').length;
  const cities={}; builds.forEach(e=>{cities[e.city]=(cities[e.city]||0)+1;});
  const topCity=Object.entries(cities).sort((x,y)=>y[1]-x[1])[0];
  const covu=who&&a.u[who]?a.u[who].covu:0, exp=who&&a.u[who]?a.u[who].exp:null;
  const tripBtn=(typeof TRIPS!=='undefined'&&topCity&&TRIPS[topCity[0]])?`<button class="minibtn" data-cmtrip="${topCity[0]}">Plan a ${topCity[0]} trip →</button>`:'';
  const [qu2]=cmQualU(covu), [qt2]=cmQualT(a.covT);
  return `<div class="cmhead">${who?`${CM.ccName[cc]}: your coverage is <b>${qu2}</b>; the team's is ${qt2}.`:`${CM.ccName[cc]}: team coverage is <b>${qt2}</b>.`} ${topCity?`${topCity[0]} holds ${topCity[1]} of the ${builds.length} funds worth building.`:''} ${warm?`${warm} have a warm path through the team.`:''}</div>
    ${cmQualRow(covu,a.covT,who)}
    ${exp!=null?`<div class="dtsub">${Math.round(exp)}% of your pipeline in this region sits here.</div>`:''}
    ${(CM.aff||[]).filter(e=>e.cc===cc).length?`<div class="dtsub">+${(CM.aff||[]).filter(e=>e.cc===cc).length} more ${CM.ccName[cc]}-based investors in Affinity, shown below the tracked funds.</div>`:''}
    ${tripBtn}
    <div class="apsec">Where to spend time</div>${cmTop5(me,sel)}`;
}

function cmAnimVB(svg,to){
  const from=svg.getAttribute('viewBox').split(' ').map(Number);
  const t0=performance.now(), dur=550;
  const step=t=>{
    const k=Math.min((t-t0)/dur,1), e=k<.5?2*k*k:1-Math.pow(-2*k+2,2)/2;
    svg.setAttribute('viewBox', from.map((v,i)=>v+(to[i]-v)*e).join(' '));
    if(k<1) requestAnimationFrame(step);
  };
  requestAnimationFrame(step);
}
function cmGo(lvl,cc,ent,reg){
  if(cc!==MAP.cc){ MAP.showAll=false; MAP.whoTeam=false; }
  const wasMap=(MAP.lvl==='l0'||MAP.lvl==='l1')&&!MAP.ent, toMap=(lvl==='l0'||lvl==='l1')&&!ent;
  if(reg) MAP.reg=reg;
  else if(cc&&CM.regOf&&CM.regOf[cc]) MAP.reg=CM.regOf[cc];
  MAP.lvl=lvl; MAP.cc=cc||''; MAP.ent=ent||'';
  const svg=document.getElementById('cmsvg');
  if(svg&&wasMap&&toMap){ cmAnimVB(svg, CM.vb[lvl==='l0'?'l0':MAP.reg]||CM.vb.l0); setTimeout(()=>{renderWork();updateHash();},300); }
  else { renderWork(); updateHash(); }
}
function cmBack(){
  const solo=((CM.subsOf||{})[MAP.reg]||[]).length<=1;
  if(MAP.ent) cmGo('l2',MAP.cc,'');
  else if(MAP.lvl==='l2') solo?cmGo('l0','',''):cmGo('l1','','');
  else if(MAP.lvl==='l1') cmGo('l0','','');
}
function mapBind(body){
  const me=ap.who||'';
  const bk=body.querySelector('[data-cmback]');
  if(bk) bk.addEventListener('click',cmBack);
  body.querySelectorAll('[data-cmwho]').forEach(b=>b.addEventListener('click',()=>{MAP.whoTeam=b.dataset.cmwho==='team';renderWork();}));
  const sa=body.querySelector('[data-cmshowall]');
  if(sa) sa.addEventListener('click',()=>{MAP.showAll=true;renderWork();});
  body.querySelectorAll('[data-cmhideall]').forEach(b=>b.addEventListener('click',()=>{MAP.showAll=false;renderWork();}));
  body.querySelectorAll('[data-cmwhomore]').forEach(b=>b.addEventListener('click',()=>{MAP.whoMore=b.dataset.cmwhomore==='1';renderWork();}));
  body.querySelectorAll('[data-cmgo]').forEach(b=>b.addEventListener('click',()=>{
    if(mapBind._dragged) return;
    const l=b.dataset.cmgo; cmGo(l, l==='l2'?MAP.cc:'', '', b.dataset.cmreg);
  }));
  body.querySelectorAll('[data-cmcc2]').forEach(g=>g.addEventListener('click',()=>{ if(!mapBind._dragged) cmGo('l2',g.dataset.cmcc2,''); }));
  body.querySelectorAll('path[data-cmcc]').forEach(p=>p.addEventListener('click',()=>{
    if(!mapBind._dragged && MAP.lvl!=='l0' && CM.areas[p.dataset.cmcc]) cmGo('l2',p.dataset.cmcc,'');
  }));
  body.querySelectorAll('[data-cmtrip]').forEach(b=>b.addEventListener('click',()=>goPage('geo',{city:b.dataset.cmtrip})));
  body.querySelectorAll('[data-cment]').forEach(g=>g.addEventListener('click',ev=>{
    if(ev.target.closest('a')||ev.target.closest('button:not([data-cment])')) return;
    const e=(CM.ents||[]).find(x=>x.slug===g.dataset.cment)||(CM.aff||[]).find(x=>x.slug===g.dataset.cment);
    if(!e) return;
    cmGo('l3', e.cc||MAP.cc, g.dataset.cment);
  }));
  // drag to pan the map levels
  const svg=body.querySelector('#cmsvg');
  if(svg){
    let drag=null;
    svg.addEventListener('pointerdown',ev=>{
      drag={x:ev.clientX,y:ev.clientY,id:ev.pointerId,cap:false,vb:svg.getAttribute('viewBox').split(' ').map(Number)};
      mapBind._dragged=false;
    });
    svg.addEventListener('pointermove',ev=>{
      if(!drag) return;
      const sc=drag.vb[2]/svg.clientWidth;
      const dx=(ev.clientX-drag.x)*sc, dy=(ev.clientY-drag.y)*sc;
      if(Math.abs(ev.clientX-drag.x)+Math.abs(ev.clientY-drag.y)>4&&!drag.cap){
        mapBind._dragged=true; drag.cap=true;
        try{svg.setPointerCapture(drag.id);}catch(err){}  // capture only once a real drag starts, so plain clicks reach the bubbles
      }
      if(!drag.cap) return;
      const L0=CM.vb.l0;
      const nx=Math.max(L0[0]-L0[2]*0.25, Math.min(drag.vb[0]-dx, L0[0]+L0[2]*1.25-drag.vb[2]));
      const ny=Math.max(L0[1]-L0[3]*0.25, Math.min(drag.vb[1]-dy, L0[1]+L0[3]*1.25-drag.vb[3]));
      svg.setAttribute('viewBox', `${nx} ${ny} ${drag.vb[2]} ${drag.vb[3]}`);
    });
    const up=()=>{ drag=null; setTimeout(()=>{mapBind._dragged=false;},50); };
    svg.addEventListener('pointerup',up); svg.addEventListener('pointercancel',up);
    svg.style.cursor='grab';
    svg.addEventListener('wheel',ev=>{   // ctrl+scroll (and trackpad pinch) zooms, like any map
      if(!ev.ctrlKey) return;
      ev.preventDefault();
      const vb=svg.getAttribute('viewBox').split(' ').map(Number);
      const L0=CM.vb.l0, k=Math.exp(ev.deltaY*0.002);
      const nw=Math.min(Math.max(vb[2]*k, L0[2]/16), L0[2]*1.8), nh=vb[3]*(nw/vb[2]);
      const r=svg.getBoundingClientRect();
      const px=vb[0]+(ev.clientX-r.left)/r.width*vb[2], py=vb[1]+(ev.clientY-r.top)/r.height*vb[3];
      svg.setAttribute('viewBox', `${px-(px-vb[0])*(nw/vb[2])} ${py-(py-vb[1])*(nh/vb[3])} ${nw} ${nh}`);
    },{passive:false});
  }
  const hov=body.querySelector('#cmhover');
  if(hov) body.querySelectorAll('g.cmregbtn').forEach(g=>{
    g.addEventListener('mouseenter',()=>{
      const rid=g.dataset.cmreg, a=CM.areas[rid]; if(!a) return;
      const covu=me&&a.u[me]?a.u[me].covu:0;
      const [qu]=cmQualU(covu), [qt]=cmQualT(a.covT);
      hov.innerHTML=`<div class="cmcn"><b>${(CM.regions.find(r=>r.id===rid)||{}).name||rid}</b></div>
        <div class="cmwhy">${me?cmYouLine(covu,a.covT):`Team coverage is <b>${qt}</b>.`}</div>`;
      hov.hidden=false;
    });
    g.addEventListener('mousemove',ev=>{
      const wrap=body.querySelector('.cmmapwrap'); if(!wrap) return;
      const r=wrap.getBoundingClientRect();
      hov.style.left=Math.min(ev.clientX-r.left+16, r.width-310)+'px';
      hov.style.top=Math.max(ev.clientY-r.top-10,4)+'px';
    });
    g.addEventListener('mouseleave',()=>{ hov.hidden=true; });
  });
  if(hov) body.querySelectorAll('g[data-cmsoon]').forEach(g=>{
    g.addEventListener('mouseenter',()=>{
      hov.innerHTML=`<div class="cmcn"><b>${g.dataset.cmsoon}</b></div><div class="cmwhy">Coming soon.</div>`;
      hov.hidden=false;
    });
    g.addEventListener('mousemove',ev=>{
      const wrap=body.querySelector('.cmmapwrap'); if(!wrap) return;
      const r=wrap.getBoundingClientRect();
      hov.style.left=Math.min(ev.clientX-r.left+16, r.width-310)+'px';
      hov.style.top=Math.max(ev.clientY-r.top-10,4)+'px';
    });
    g.addEventListener('mouseleave',()=>{ hov.hidden=true; });
  });
  if(hov) body.querySelectorAll('g[data-cment],g[data-cmcc2]').forEach(g=>{
    if(g.classList.contains('cmregbtn')) return;   // solo-region world buttons keep the region verdict card
    g.addEventListener('mouseenter',()=>{
      const cc=g.dataset.cmcc2;
      if(cc){ const a=CM.areas[cc]; if(!a) return;
        const covu=me&&a.u[me]?a.u[me].covu:0, kn=me&&a.known?a.known[me]||0:0;
        hov.innerHTML=`<div class="cmcn"><b>${CM.ccName[cc]}</b></div><div class="cmnums"><span>Shortlisted funds <b>${a.sln||0}</b></span><span>You know <b>${kn}</b></span><span>Team <b>${Math.round(a.covT)}%</b></span></div>`;
        hov.hidden=false; }
    });
    g.addEventListener('mousemove',ev=>{
      const wrap=body.querySelector('.cmmapwrap'); if(!wrap) return;
      const r=wrap.getBoundingClientRect();
      hov.style.left=Math.min(ev.clientX-r.left+14, r.width-300)+'px';
      hov.style.top=Math.max(ev.clientY-r.top-10,4)+'px';
    });
    g.addEventListener('mouseleave',()=>{ hov.hidden=true; });
  });
  if(!mapBind._esc){
    mapBind._esc=true;
    document.addEventListener('keydown',ev=>{
      if(ev.key!=='Escape'||state.page!=='map') return;
      cmBack();
    });
  }
}

function netApply(list){
  const F=ap.nf, q=(F.q||'').trim().toLowerCase();
  return list.filter(e=>(!q||e.n.toLowerCase().includes(q)||(e.f||'').toLowerCase().includes(q))
    &&(!F.ty||e.ft===F.ty)&&(!F.st||e.fs===F.st)&&(!F.sr||e.sr===F.sr)&&(!F.ci||e.c===F.ci));
}
const NCOLS=[['p','You'],['n','Name'],['sr','Role','sr'],['f','Fund'],['ft','Type','ty'],['fs','Stage','st'],['c','City','ci',30],['l','Last touch']];
function netTable(full,who){
  const list=netApply(full), F=ap.nf;
  const sk=ap.ns, dir=ap.nd;
  const sorted=[...list].sort((a,b)=>{
    const va=a[sk], vb=b[sk];
    if(va==null&&vb==null) return b.p-a.p;
    if(va==null) return 1; if(vb==null) return -1;
    const c=typeof va==='number'?va-vb:String(va).localeCompare(String(vb));
    return c*dir||b.p-a.p;
  });
  const counts=k=>{const m={};full.forEach(e=>{if(e[k])m[e[k]]=(m[e[k]]||0)+1;});return Object.entries(m).sort((a,b)=>b[1]-a[1]);};
  const head=NCOLS.map(([k,lab,fk,cap])=>{
    let filt='';
    if(fk){
      const vs=counts(k);
      if(vs.length) filt=`<select class="thfilt${F[fk]?' on':''}" data-nfs="${fk}" title="${F[fk]?`${lab}: ${F[fk]} — click to change`:`Filter by ${lab.toLowerCase()}`}">
        <option value="">All</option>${vs.slice(0,cap||99).map(([v,n])=>`<option value="${v.replace(/"/g,'&quot;')}"${F[fk]===v?' selected':''}>${v} (${n})</option>`).join('')}</select>`;
    }
    return `<th><span class="thsort${sk===k?' on':''}" data-nsort="${k}">${lab}${sk===k?(dir===1?' ↑':' ↓'):''}</span>${filt}${F[fk]?`<span class="thval">${F[fk]}</span>`:''}</th>`;
  }).join('');
  const body=sorted.map(e=>{
    const cad=cadOf(e), cold=isCold(e), mo=moAgo(e.l);
    return `<tr${cold?' class="coldr"':''}><td><b class="mbub ${easeTierOf(e.p)}">${e.p}</b></td>
      <td class="nmc"${e.t?` title="${e.t}"`:''}>${e.n}${everTag({ever:e.v})}${e.e?` <a class="nmail" href="${rewarmMail(e,who)}" title="Email ${e.n.split(' ')[0]}">✉</a>`:''}</td>
      <td>${e.sr||'—'}</td><td>${e.f||e.d||''}</td><td>${e.ft||'—'}</td><td>${e.fs||'—'}</td><td>${e.c||'—'}</td>
      <td class="lt">${e.l?`${fmtD(e.l)}${cold?` · ${Math.round(mo)} mo`:''}`:'—'}</td>
      <td><button class="cadchip${cad?' on':''}" data-cad="${encodeURIComponent(e.n+'|'+e.f)}" data-cur="${cad}" title="How often you want to touch this relationship — click to change">${cad?`every ${cad}mo`:'off'}</button></td></tr>`;
  }).join('');
  const active=['ty','st','sr','ci'].some(k=>F[k])||F.q;
  return `<div class="ntfilt">
      <input id="nq" type="search" placeholder="Name or fund…" value="${(F.q||'').replace(/"/g,'&quot;')}">
      ${active?`<button class="minibtn" id="nclear">Clear filters · showing ${list.length} of ${full.length}</button>`:''}
    </div>
    <div class="apcard ntcard"><table class="nettab"><thead><tr>${head}<th></th></tr></thead><tbody>${body||`<tr><td colspan="9" class="lt" style="padding:14px">No one matches these filters.</td></tr>`}</tbody></table></div>`;
}
function netAskBody(who,e,p){
  const wf=who.split(' ')[0];
  return `Hey ${p.internal.split(' ')[0]} — I'm trying to build my own line into ${e.name} and you hold our strongest path (${p.external}${p.pct!=null?`, ${p.pct}%`:''}). Could you intro me or bring me along next time? Thanks! — ${wf}`;
}
// --- Daily Network Actions: a deck of single recommendations — action each one or move on.
// Decisions persist per browser (localStorage): done/not-relevant never return, snooze hides for a week, skip is session-only.
let NDECK=[], NDI=0;
const ACTS=(()=>{try{return JSON.parse(localStorage.getItem('sonar_acts')||'{}');}catch(err){return {};}})();
function saveActs(){try{localStorage.setItem('sonar_acts',JSON.stringify(ACTS));}catch(err){}}
function actGone(id){
  const a=ACTS[id]; if(!a) return false;
  if(a.s==='snooze'){ if(a.until&&Date.now()>a.until){ delete ACTS[id]; saveActs(); return false; } return true; }
  return true;
}
const ROLE_OF=(()=>{const m={};(D.team||[]).forEach(t=>{m[t.full||t.name]=t.role;});
  m['Fergal Mullen']='partner'; m['Laurence Garrett']='partner'; return m;})();
const isPartner=n=>ROLE_OF[n]==='partner';
function buildDeck(who){
  const partner=isPartner(who);
  const funds=ALLE.filter(x=>x.e.kind==='fund'&&!ACCELCAT[x.e.category]);
  const byRel=(a,b)=>(b.e.relevance?.total||0)-(a.e.relevance?.total||0);
  const net=((D.mynet||{})[who]||[]);
  // 1 — congratulate: people you know who moved seats in the last 3 months
  const mv=(D.movers||[]).filter(m=>(m.k||[]).includes(who)&&m.since&&moAgo(m.since)<=3)
    .sort((a,b)=>new Date(b.since)-new Date(a.since))
    .map(m=>{const co=m.co||m.now||'a new firm';return {id:'mv:'+m.n, verb:'Congratulate', name:m.n,
      sub:`Just joined <b>${co}</b>${m.ti?` as ${m.ti}`:''} — moved from ${m.fr} · ${fmtD(m.since)}`,
      href:liSearch(m.n,co), hlabel:'Say congrats on LinkedIn ↗', ext:true};});
  // 2 — reconnect: relationships past their cadence, strongest first
  const rw=net.filter(isCold).sort((a,b)=>b.p-a.p).slice(0,12)
    .map(e=>({id:'rw:'+e.n+'|'+(e.f||''), verb:'Reconnect with', name:e.n,
      sub:`${e.f||'—'}${e.sr?' · '+e.sr:''} · strength ${e.p} · last touch ${fmtD(e.l)} (${Math.round(moAgo(e.l))} mo ago)`,
      href:e.e?rewarmMail(e,who):liSearch(e.n,e.f||''),
      hlabel:e.e?'✉ Email '+e.n.split(' ')[0]:'Find on LinkedIn ↗', ext:!e.e}));
  // 3 — team intro asks: relevant funds the team already covers but you don't.
  // Associates borrow the team's doors; partners don't replicate coverage a teammate
  // already holds, so this pool is theirs alone.
  const iv=(partner?[]:funds.filter(x=>personCov(x.e,who)<30&&x.e.connectivity>=50&&(x.e.points||[]).length)
    .sort(byRel).slice(0,12))
    .map(({r,e})=>{const p=e.points[0], f=p.internal.split(' ')[0];
      return {id:'in:'+e.slug, verb:`Ask ${f} for an intro to`, name:e.name,
      sub:`${p.internal} holds <b>${p.external||'a contact'}</b>${p.pct!=null?` (${p.pct}%)`:''} · ${D.regions[r].label} · relevance ${e.relevance?.total??'—'} · the intro is one ask away`,
      href:`mailto:${hlMail(p.internal)}?subject=${encodeURIComponent('Intro to '+(p.external||e.name)+'?')}&body=${encodeURIComponent(netAskBody(who,e,p))}`,
      hlabel:'✉ Ask '+f};});
  // 4 — first-mover: relevant funds nobody at Highland covers yet.
  // For partners this is the whole game — the firm's collective white space — so it gets more room.
  const co=funds.filter(x=>x.e.connectivity<22&&(x.e.relevance?.total||0)>=(partner?50:55)).sort(byRel).slice(0,partner?16:8)
    .map(({r,e})=>{const pk=(e.partners_unknown||[])[0];
      return {id:'co:'+e.slug, verb:'Reach out cold to', name:e.name,
      sub:`${D.regions[r].label} · relevance ${e.relevance?.total??'—'} · nobody at Highland has a line in — you'd be first${pk?` · door: <b>${pk.name}</b>${pk.title?' ('+pk.title+')':''}`:''}`,
      href:pk?(pk.linkedin||liSearch(pk.name,e.name)):liSearch(e.name,''),
      hlabel:pk?`Find ${pk.name.split(' ')[0]} on LinkedIn ↗`:'Find on LinkedIn ↗', ext:true};});
  // 5 — partners only: funds the team "covers" but only below partner level.
  // Lucinda knowing an associate there is real coverage for her book, not a GP line —
  // from the partnership's perspective that fund is still white space.
  let gp=[];
  if(partner){
    const gpKnown=new Set((CM.ents||[]).filter(e=>(e.people||[]).some(p=>p.sr==='Partner'&&Object.values(p.r||{}).some(v=>v>=40))).map(e=>e.slug));
    gp=funds.filter(x=>x.e.connectivity>=22&&(x.e.relevance?.total||0)>=55&&!gpKnown.has(x.e.slug))
      .sort(byRel).slice(0,8)
      .map(({r,e})=>{const pk=(e.partners_unknown||[])[0], p0=(e.points||[])[0];
        return {id:'gp:'+e.slug, verb:'Open a partner line into', name:e.name,
        sub:`${D.regions[r].label} · relevance ${e.relevance?.total??'—'} · the team knows them, but below partner level — no GP relationship yet${p0?` (current line: ${p0.internal.split(' ')[0]} ↔ ${p0.external||'a contact'})`:''}${pk?` · their GP: <b>${pk.name}</b>`:''}`,
        href:pk?(pk.linkedin||liSearch(pk.name,e.name)):liSearch(e.name,''),
        hlabel:pk?`Find ${pk.name.split(' ')[0]} on LinkedIn ↗`:'Find on LinkedIn ↗', ext:true};});
  }
  // interleave the kinds so the deck stays varied
  const pools=[mv,rw,iv,co,gp], deck=[];
  for(let i=0,more=true;more;i++){ more=false; pools.forEach(p=>{ if(p[i]){deck.push(p[i]); more=true;} }); }
  return deck.filter(c=>!actGone(c.id));
}
function deckCard(){
  const n=NDECK.length;
  if(!n) return `<div class="apcard ndkdone"><div class="ndkbig">All caught up.</div>
    <div class="aphint">No moves, lapsed relationships or intro asks waiting. Check back tomorrow.</div></div>`;
  if(NDI>=n){
    const done=NDECK.filter(c=>ACTS[c.id]&&ACTS[c.id].s==='done').length;
    return `<div class="apcard ndkdone"><div class="ndkbig">That's the deck.</div>
      <div class="aphint">${done} actioned · ${n-done} skipped for another day.</div>
      <div class="ndkskips" style="margin-top:14px"><button data-ndk="restart">Go through the skipped ones again</button></div></div>`;
  }
  const c=NDECK[NDI];
  return `<div class="ndkwrap"><div class="ndkcount">${NDI+1} of ${n}</div>
    <div class="ndkstack">
      ${NDI<n-2?'<div class="ndkghost g2"></div>':''}${NDI<n-1?'<div class="ndkghost g1"></div>':''}
      <div class="apcard ndkcard">
        <div class="ndkverb">${c.verb}</div>
        <div class="ndkname">${c.name}</div>
        <div class="ndksub">${c.sub}</div>
        <div class="ndkacts"><a class="ndkmain" href="${c.href}"${c.ext?' target="_blank" rel="noopener"':''} data-ndk="done">${c.hlabel}</a></div>
        <div class="ndkskips">
          <button data-ndk="skip" title="Come back to this another day">Skip →</button>
          <button data-ndk="snooze" title="Hide for a week">Snooze</button>
          <button data-ndk="never" title="Never suggest this again">Not relevant</button>
        </div>
      </div></div></div>`;
}
function bindDeck(root){
  const d=root.querySelector('#ndeck'); if(!d) return;
  d.addEventListener('click',ev=>{
    const b=ev.target.closest('[data-ndk]'); if(!b) return;
    const act=b.dataset.ndk;
    if(act==='restart'){ NDECK=NDECK.filter(c=>!actGone(c.id)); NDI=0; d.innerHTML=deckCard(); return; }
    const c=NDECK[NDI]; if(!c) return;
    if(act==='done'){ ACTS[c.id]={s:'done',t:Date.now()}; saveActs(); }
    else if(act==='snooze'){ ACTS[c.id]={s:'snooze',until:Date.now()+7*864e5}; saveActs(); toast('Snoozed for a week'); }
    else if(act==='never'){ ACTS[c.id]={s:'never',t:Date.now()}; saveActs(); toast('Gone — this one will not come back'); }
    NDI++;
    d.innerHTML=deckCard();
  });
}
function apNet(){
  const who=ap.who;
  if(!who) return `<div class="aphint">Pick who you are above — this view is personal by design.</div>`;
  NDECK=buildDeck(who); NDI=0;
  return `<div id="ndeck">${deckCard()}</div>`;
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
  if(!city){
    const all=cityScores(ap.who).filter(c=>c.pipe>0||c.funds>0);
    const main=all.slice(0,6), more=all.slice(6,30);
    const avg=a=>a.length?Math.round(a.reduce((x,y)=>x+y,0)/a.length):0;
    const cards=main.map(c=>{
      const top=c.topco.slice().sort((a,b)=>(b.uf??-1)-(a.uf??-1))[0];
      const stats=[c.pipe?`${c.pipe} open pipeline${c.hiPipe?` · <b>${c.hiPipe} high-prio</b>`:''}`:null,
        c.funds?`${c.funds} relevant fund${c.funds>1?'s':''} · your strength ${avg(c.str)}`:null,
        top?`top: ${top.n}${top.uf!=null?` · ${Math.round(top.uf)}`:''}`:null].filter(Boolean);
      const badge=c.hiPipe||c.pipe;
      return `<div class="gcity" data-gocity="${c.city}" tabindex="0">
        <div class="gcname">${c.city}<span class="mbub ${c.hiPipe?'strong':c.pipe?'medium':'low'}">${badge||c.funds}</span></div>
        <div class="gcstats">${stats.join('<br>')}</div></div>`;
    }).join('');
    const chips=more.map(c=>`<button type="button" data-gocity="${c.city}">${c.city} <b>${c.pipe||c.funds}</b></button>`).join('');
    return `<div class="aphint">Where should you go? Ranked by your open pipeline × network strength × dealflow weight — tap a city${ap.who?'':' (pick who you are for a personal ranking)'}.</div>
      <div class="glaunch">${cards||'<div class="aphint">No city signal yet.</div>'}</div>
      ${chips?`<div class="gchips">${chips}</div>`:''}`;
  }
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
  const rows=pipe.map(p=>{
    const pr=profOf(p);
    const meta=[...bizBits(pr), p.via&&p.via.size?'via '+[...p.via].slice(0,2).join(', '):null,
      !who&&(p.own||[]).length?p.own.map(o=>o.split(' ')[0]).join(', '):null].filter(Boolean).join(' · ');
    const ufR=p.uf!=null?Math.round(p.uf):null;
    return `<div class="apcard gcard"><div class="gflex">
    <span class="apstat gbub">${`<span class="bub big ${ufTierOf(ufR)}">${ufR??'—'}</span><span class="covcap">unframe</span>`}</span>
    <div class="gbody"><div class="aph2"><div class="fname">${starBtn('co',p.name,city)}<a href="${affURL(p.id)}" target="_blank" rel="noopener">${p.name}</a></div><span class="gstat">${(p.funnel||'').replace(' (free for all)','')}</span></div>
    ${pr.d?`<div class="apdesc full">${pr.d}</div>`:''}
    ${meta?`<div class="apmeta">${meta}</div>`:''}</div></div></div>`;}).join('');
  const inCity=ALLE.filter(x=>x.e.kind==='fund'&&cityOf(x.e)===city);
  const know=[], cold=[];
  inCity.forEach(({r,e})=>{const pc=who?personCov(e,who):e.connectivity; (pc>0?know:cold).push({r,e,pc});});
  know.sort((a,b)=>b.pc-a.pc);
  cold.sort((a,b)=>((ACCELCAT[a.e.category]?1:0)-(ACCELCAT[b.e.category]?1:0))||((b.e.relevance?.total||0)-(a.e.relevance?.total||0)));
  const kRows=know.map(({e,pc})=>{
    const sig=who?personSignal(e,who):null; const k=sig&&sig.contacts&&sig.contacts[0];
    const line=k?`<b>${k.person}</b>${k.pct!=null?` <span class="via">· ${k.pct}%</span>`:''}${evidence(k)?` <span class="via">· ${evidence(k)}</span>`:''}`
      :(e.points&&e.points[0]?`<b>${e.points[0].external||''}</b> <span class="via">via ${e.points[0].internal}</span>`:'');
    return `<div class="apcard"><div class="fname ${e.tier}"><span class="tdot"></span>${starBtn('fund',e.name,city)}${cmFundLink(e.name)}</div>
      <div class="apmeta">relevance ${e.relevance?.total??'—'} · ${who?`your coverage ${pc}`:`team ${e.connectivity}`}</div>
      ${line?`<div class="appath">Reconnect: ${line}</div>`:''}</div>`;}).join('');
  const cRows=cold.map(({e})=>{
    const nm2=nextMove(e)||{cls:'gap',txt:''}; const pk=(e.partners_unknown||[])[0];
    return `<div class="apcard"><div class="fname ${e.tier}"><span class="tdot"></span>${starBtn('fund',e.name,city)}${cmFundLink(e.name)}${ACCELCAT[e.category]?' <span class="cc">· accelerator</span>':''}</div>
      <div class="apmeta">relevance ${e.relevance?.total??'—'}${who?` · team ${e.connectivity}`:''}</div>
      <div class="nm ${nm2.cls}">${nm2.txt}</div>
      ${pk?`<div class="apmeta">Door: ${pk.linkedin?`<a href="${pk.linkedin}" target="_blank" rel="noopener">${pk.name}</a>`:pk.name}${pk.title?` · ${pk.title}`:''}</div>`:''}</div>`;}).join('');
  return `<div class="gback"><button type="button" class="minibtn" data-gocity="">← All cities</button></div>
    <div class="aphint">Star ☆ companies and funds as you scan — they land in the Earmarked rail on the right, your next-visit plan.</div>
    <div class="apsec">${who?who.split(' ')[0]+"'s":'Our'} pipeline in ${city} — ranked by Unframe priority</div>
    ${rows||`<div class="aphint">${anyCity?`No ${who?who.split(' ')[0]+"'s":''} pipeline companies with a known ${city} HQ.`:'City data is still backfilling — check back shortly.'}</div>`}
    <div class="apsec">Investors ${who?'you know':'we know'} here — reconnect</div>${kRows||'<div class="aphint">None yet.</div>'}
    <div class="apsec">Funds ${who?"you don't know":'we barely know'} — prioritise</div>${cRows||'<div class="aphint">None.</div>'}`;
}


const liSearch = (n,f) => `https://www.linkedin.com/search/results/people/?keywords=${encodeURIComponent(n+' '+(f||''))}`;
const emIcon = p => {
  const em = p.email || p.email_guess;
  if(!em) return '';
  return `<span class="em${p.email?'':' guess'}" data-em="${em}"${p.email?'':' data-guess="1"'}>✉</span>`;
};
const evidence = o => o.meet?`met ${fmtD(o.meet)}`:(o.last?`em ${fmtD(o.last)}`:null);
const everTag = o => o.ever===false?` <span class="uvtag emp" title="Not matched against a current Harmonic role — relationship shown from Affinity history alone">unverified</span>`:'';



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

function detailHTML(e){
  let h='';
  if(e.kind!=='fund' && e.relevance){
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
  if((e.untracked||[]).length){
    h += `<details class="sec"><summary>Recent EU deals we're not tracking <b>${e.untracked.length}</b>${e.recent_eu?`<span class="cnt">of ${e.recent_eu} recent EU deals</span>`:''}</summary><div class="plist">`+
      e.untracked.map(u=>`<span><span class="st">${(u.date||'').slice(0,7)} · ${(u.round||'').replaceAll('_',' ').toLowerCase()}</span><a href="https://console.harmonic.ai/dashboard/company/${u.harmonic_company_id}" target="_blank" rel="noopener">${u.name}</a> <span class="cc">${u.country||''}</span></span>`).join('')+`</div></details>`;
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
          const uv = (k.unverified?` <span class="uvtag">email-only</span>`:'')+everTag(k);
          return `<div>${nm}${k.email?emIcon(k):''}<span class="t">${bits?` · ${bits}`:''}</span>${uv}</div>`;
        }).join('')+`</div>`;
    }).join('')+`</div>`;
    if(false){
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



// ---------- mobile experience ----------
const isMobile = () => matchMedia('(max-width:700px)').matches;





// ---------- markup mode: tag anything to kill or simplify, copy a report for Claude ----------
let MARKS=[]; try{ MARKS=JSON.parse(localStorage.getItem('sonar_marks')||'[]'); }catch(e0){}
const MK={on:false, el:null, kind:'kill'};
const mkPersist=()=>{ try{ localStorage.setItem('sonar_marks', JSON.stringify(MARKS)); }catch(e0){} };
const mkPage=()=>({map:'Coverage Map',
  h2c:'Solve my H2Cs',net:'Network Actions',geo:'City Trip'+(ap.city?' · '+ap.city:'')}[state.page]||state.page);
function mkLabel(el){
  for(const sel of ['.fname','.dtlabel','.dlh','.dsec','.apsec','.sechead h2','.covcap','.th','h1','h2','summary']){
    const n=el.querySelector(sel)||el.closest(sel);
    if(n) { const t=(n.innerText||n.textContent||'').trim().replace(/\s+/g,' ');
      if(t) return t.slice(0,70); }
  }
  const t0=(el.innerText||el.textContent||'').trim().replace(/\s+/g,' ');
  return t0.slice(0,70)||('<'+el.tagName.toLowerCase()+'>');
}
function mkTray(){
  const t=document.getElementById('mktray'); if(!t) return;
  t.hidden=!(MK.on||MARKS.length);
  document.getElementById('mkcount').textContent=(MK.on?'✎ markup on · ':'')+MARKS.length+' mark'+(MARKS.length===1?'':'s');
  document.getElementById('mkexit').textContent=MK.on?'Exit markup':'Resume markup';
}
function mkStart(){ MK.on=true; document.body.classList.add('mkmode'); mkTray();
  toast('Markup on — click anything to tag it. Sidebar still navigates. Esc to finish.'); }
function mkStop(){ MK.on=false; document.body.classList.remove('mkmode');
  document.getElementById('mkpop').hidden=true; mkTray(); }
document.addEventListener('click',ev=>{
  if(!MK.on) return;
  if(ev.target.closest('#mkpop,#mktray,#fbpop,#whoback')) return;
  if(ev.target.closest('#side')) return;              // keep navigation usable while marking
  ev.preventDefault(); ev.stopPropagation();
  const el=ev.target.closest('.apcard,.dtile,.dcity,.gcity,.mcard,tr,.covcard,.dlist,.chgsec,.score .s,.askcard,#aprail,.seg,.filters,.pts,.chips,.note,.dprev,.hero,.whead,.aphint,.glaunch,.gchips,thead,details,button,a,select,input')||ev.target;
  MK.el=el; MK.kind='kill'; MK.label=mkLabel(el);
  const pop=document.getElementById('mkpop');
  pop.hidden=false;
  pop.style.left=Math.max(10,Math.min(innerWidth-305,ev.clientX-30))+'px';
  pop.style.top=Math.max(10,Math.min(innerHeight-185,ev.clientY+12))+'px';
  pop.querySelectorAll('[data-mk]').forEach(b=>b.classList.toggle('on',b.dataset.mk==='kill'));
  document.getElementById('mkwhat').textContent=mkPage()+' · '+MK.label;
  document.getElementById('mknote').value='';
},true);
document.addEventListener('keydown',ev=>{
  if(ev.key!=='Escape'||!MK.on) return;
  const pop=document.getElementById('mkpop');
  if(!pop.hidden) pop.hidden=true; else mkStop();
});
document.querySelectorAll('#mkpop [data-mk]').forEach(b=>b.addEventListener('click',()=>{
  MK.kind=b.dataset.mk;
  document.querySelectorAll('#mkpop [data-mk]').forEach(x=>x.classList.toggle('on',x===b));
}));
document.getElementById('mksave').addEventListener('click',()=>{
  MARKS.push({page:mkPage(), label:MK.label||'', kind:MK.kind,
    note:document.getElementById('mknote').value.trim(), when:new Date().toISOString().slice(0,16)});
  mkPersist();
  if(MK.el&&MK.el.classList) MK.el.classList.add('mk-'+MK.kind);
  document.getElementById('mkpop').hidden=true; mkTray(); toast('Marked — keep going or copy the report below');
});
document.getElementById('mkcancel').addEventListener('click',()=>{document.getElementById('mkpop').hidden=true;});
document.getElementById('mkcopy').addEventListener('click',()=>{
  const rep=['Sonar markup report — '+(state.person||'team')+' — '+new Date().toLocaleString('en-GB'),'']
    .concat(MARKS.map(m=>`[${m.kind.toUpperCase()}] ${m.page} · "${m.label}"${m.note?` — ${m.note}`:''}`)).join('\n');
  navigator.clipboard?.writeText(rep); toast('Report copied — paste it to Claude');
});
document.getElementById('mkclearall').addEventListener('click',()=>{ MARKS=[]; mkPersist(); mkTray(); toast('Marks cleared'); });
document.getElementById('mkexit').addEventListener('click',()=>{ MK.on?mkStop():mkStart(); });
mkTray();
const _mks=document.getElementById('mkstart');
if(_mks) _mks.addEventListener('click',()=>{ document.getElementById('fbpop').hidden=true; mkStart(); });

document.getElementById('fb').addEventListener('click',()=>{
  const p = document.getElementById('fbpop'); p.hidden = !p.hidden;
});
document.getElementById('fbclose').addEventListener('click',()=>{ document.getElementById('fbpop').hidden = true; });
document.getElementById('sheetclose').addEventListener('click',()=>{
  document.getElementById('sheet').classList.remove('open'); state.open=''; stopLive(); updateHash();
});
matchMedia('(max-width:700px)').addEventListener('change',()=>refresh());

// ---------- untracked dealflow view ----------
const fmtMoney = v => (v==null||v===0)?'\u2014':v>=995e6?('$'+(v/1e9).toFixed(1)+'B'):v>=1e6?('$'+Math.round(v/1e6)+'M'):('$'+Math.round(v/1e3)+'K');
const fmtStage = st => (st||'').replaceAll('_',' ').toLowerCase().replace(/(^|\s)\S/g, c=>c.toUpperCase()).replace('Pre Seed','Pre-seed') || '\u2014';

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








// ---------- live sync (viewer's Affinity connector via window.claude.mcp) ----------
const LIVE_BUCKET = {'Pre-lead':'prelead','Reach Out Now':'reachout','Awaiting Reply':'awaiting',
  'Lead':'lead','Qualified Lead':'lead','Deal':'lead','Hard to crack':'hard','Portfolio Company':'portfolio'};
let liveSub = null;   // {slug, unsub}
const nrmInv = s => (s||'').toLowerCase().normalize('NFKD').replace(/[̀-ͯ]/g,'')
  .replace(/[^a-z0-9 ]+/g,' ').replace(/\s+/g,' ').trim();

function stopLive(){ if(liveSub){ liveSub.unsub(); liveSub=null; } }

const liveLabel = e => `● live · Affinity · ${new Date(e.liveAt).toLocaleTimeString('en-GB',{hour:'2-digit',minute:'2-digit'})}`;
// ---------- website live path: same-origin /api/live (Affinity + Harmonic) ----------

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






// ---------- hash routing ----------
function updateHash(){
  let h;
  if(state.page==='h2c') h='#h2c';
  else if(state.page==='net') h='#net';
  else if(state.page==='geo') h='#geo'+(ap.city?'/'+encodeURIComponent(ap.city):'');
  else if(state.page==='map') h='#map'+(MAP.lvl==='l1'?'/'+MAP.reg:MAP.cc?'/'+MAP.cc+(MAP.ent?'/'+MAP.ent:''):'');
  else{
    h = '#'+state.region;
    if(state.view==='unt') h+='/unt';
    else if(state.open) h+='/'+state.open;
  }
  if(state.person) h+='?as='+encodeURIComponent(state.person);
  history.replaceState(null,'',h);
}
function readHash(){
  const m = location.hash.match(/^#([a-z0-9]+)(?:\/([^?]+))?(?:\?as=(.+))?$/i);
  if(!m){ state.page='map'; return; }
  if(m[3]) state.person = decodeURIComponent(m[3]);
  const head=m[1].toLowerCase();
  if(head==='dash'){ state.page='map'; MAP.lvl='l0'; MAP.cc=''; MAP.ent=''; return; }
  if(head==='h2c'){ state.page='h2c'; return; }
  if(head==='net'){ state.page='net'; return; }
  if(head==='geo'){ state.page='geo'; if(m[2]) ap.city=decodeURIComponent(m[2]); return; }
  if(head==='map'){ state.page='map';
    const p2=(m[2]||'').split('/')[0], p3=(location.hash.split('/')[2]||'').split('?')[0];
    if(p2==='nordics'||p2==='germany'||p2==='uk'||p2==='us'){ MAP.lvl='l1'; MAP.reg=p2; MAP.cc=''; MAP.ent=''; }
    else if(p2&&CM.ccName&&CM.ccName[p2.toUpperCase()]){ MAP.lvl=p3?'l3':'l2'; MAP.cc=p2.toUpperCase(); if(CM.regOf) MAP.reg=CM.regOf[MAP.cc]||MAP.reg; MAP.ent=p3||''; }
    else { MAP.lvl='l0'; MAP.cc=''; MAP.ent=''; }
    return; }
  if(REGIONS.includes(head)){           // legacy region links land on the map now
    state.page='map'; MAP.ent='';
    if(head==='france'){ MAP.lvl='l2'; MAP.cc='FR'; MAP.reg='france'; }
    else if(head==='us'){ MAP.lvl='l1'; MAP.reg='us'; MAP.cc=''; }
    else { MAP.lvl='l1'; MAP.reg=head; MAP.cc=''; }
    if(m[2]==='htc') state.page='h2c';           // legacy deep link
  } else state.page='map';
}

addEventListener('hashchange',()=>{  // deep links work without a reload
  readHash();
  if(typeof whoChip==='function') whoChip();
  goPage(state.page||'map');
});
// ---------- boot ----------
readHash();
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
  ap.who=n;
  if(rerender) refresh();
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
document.querySelectorAll('#side .sitem').forEach(a=>a.addEventListener('click',()=>goPage(a.dataset.page)));
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
// Ask Sonar lives in the left bar — rendered once, follows you across pages
const _sa=document.getElementById('sideask');
if(_sa){ _sa.innerHTML=askCard(); bindAsk(_sa); }
goPage(state.page||'map');
</script>
"""
