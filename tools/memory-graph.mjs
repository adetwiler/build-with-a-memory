#!/usr/bin/env node
//
// memory-graph: build a local, Obsidian-style interactive graph of a memory
// network. Nodes = markdown files, edges = [[wikilinks]]. Self-contained
// output: one HTML file you open in a browser. No build step, no server.
//
//   node memory-graph.mjs [notes-dir] [out-dir]
//   node memory-graph.mjs ./docs ./memory-graph
//   open ./memory-graph/index.html
//
// First run only: downloads force-graph.min.js (MIT) from unpkg into the
// output dir so the generated page works fully offline afterwards.
// Add the output dir to .gitignore.
//
// Node links resolve by frontmatter `name:` first, then by filename slug.
// Node colors group by frontmatter `type:` first, then by top-level folder.

import {
  readdirSync, readFileSync, writeFileSync, mkdirSync, existsSync,
} from "node:fs";
import { join, basename, extname, relative } from "node:path";

const MEM = process.argv[2] || ".";
const OUT = process.argv[3] || "./memory-graph";
if (!existsSync(OUT)) mkdirSync(OUT, { recursive: true });

const LIB_PATH = join(OUT, "force-graph.min.js");
if (!existsSync(LIB_PATH)) {
  const url = "https://unpkg.com/force-graph@1/dist/force-graph.min.js";
  console.log(`[memory-graph] first run: fetching ${url}`);
  const res = await fetch(url);
  if (!res.ok) {
    console.error(`[memory-graph] could not fetch force-graph (${res.status}). Download it manually into ${OUT}/ and re-run.`);
    process.exit(1);
  }
  writeFileSync(LIB_PATH, await res.text());
}
const LIB = readFileSync(LIB_PATH, "utf8");

const SKIP_DIRS = new Set(["node_modules", "__pycache__", basename(OUT), ".git"]);

function walk(dir, acc = []) {
  for (const e of readdirSync(dir, { withFileTypes: true })) {
    if (e.isDirectory()) {
      if (SKIP_DIRS.has(e.name)) continue;
      walk(join(dir, e.name), acc);
    } else if (extname(e.name) === ".md") {
      acc.push(join(dir, e.name));
    }
  }
  return acc;
}

const files = walk(MEM);

const byId = new Map();
const byFileSlug = new Map();

for (const p of files) {
  const raw = readFileSync(p, "utf8");
  const fm = raw.match(/^---\r?\n([\s\S]*?)\r?\n---/);
  const fileSlug = basename(p, ".md");
  let name = null;
  let description = "";
  let type = "";
  if (fm) {
    name = (fm[1].match(/^name:\s*(.+)$/m)?.[1] || "").trim() || null;
    description = (fm[1].match(/^description:\s*["']?(.+?)["']?\s*$/m)?.[1] || "").trim();
    type = (fm[1].match(/^\s*type:\s*(\w+)/m)?.[1] || "").trim();
  }
  const id = name || fileSlug;
  if (!description) {
    const body = fm ? raw.slice(fm[0].length) : raw;
    description =
      (body.split("\n").find((l) => l.trim() && !l.startsWith("#") && !l.startsWith(">")) || "")
        .trim()
        .replace(/\*\*/g, "")
        .slice(0, 220);
  }
  const links = [...raw.matchAll(/\[\[([^\]|#]+)(?:[|#][^\]]*)?\]\]/g)].map((m) => m[1].trim());
  const rel = relative(MEM, p);
  const node = { id, label: id, fileSlug, rel, path: p, description, type, links };
  byId.set(id, node);
  byFileSlug.set(fileSlug, id);
}

// edges: resolve [[X]] to a node id (frontmatter name) or a filename slug.
const edges = [];
const seen = new Set();
for (const n of byId.values()) {
  for (const l of n.links) {
    const target = byId.has(l) ? l : byFileSlug.get(l) || null;
    if (target && target !== n.id) {
      const key = n.id + " " + target;
      if (!seen.has(key)) {
        seen.add(key);
        edges.push({ source: n.id, target });
      }
    }
  }
}

const deg = new Map();
for (const e of edges) {
  deg.set(e.source, (deg.get(e.source) || 0) + 1);
  deg.set(e.target, (deg.get(e.target) || 0) + 1);
}

function groupOf(n) {
  if (n.type) return n.type;
  const top = n.rel.includes("/") ? n.rel.split("/")[0] : "";
  if (top) return top;
  return "note";
}

const nodes = [...byId.values()].map((n) => ({
  id: n.id,
  label: n.label,
  rel: n.rel,
  path: n.path,
  description: n.description,
  group: groupOf(n),
  deg: deg.get(n.id) || 0,
}));

const data = { nodes, links: edges };
const stats = {
  nodes: nodes.length,
  links: edges.length,
  orphans: nodes.filter((n) => n.deg === 0).length,
};

const html = renderHtml(data, stats);
writeFileSync(join(OUT, "index.html"), html);
console.log(
  `[memory-graph] ${stats.nodes} nodes, ${stats.links} links (${stats.orphans} orphans) -> ${join(OUT, "index.html")}`,
);

function renderHtml(data, stats) {
  // <-escape so note content (which is user markdown) can never break
  // out of the inline <script> block, even if it contains "</script>".
  const json = JSON.stringify(data).replace(/</g, "\\u003c");
  const memLabel = String(MEM).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
  // Inline SVG icons (stroke follows currentColor).
  const ic = {
    net: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="4.5" r="2.5"/><path d="m10.2 6.3-3.9 3.9"/><circle cx="4.5" cy="12" r="2.5"/><path d="M7 12h10"/><circle cx="19.5" cy="12" r="2.5"/><path d="m13.8 17.7 3.9-3.9"/><circle cx="12" cy="19.5" r="2.5"/></svg>',
    search: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/></svg>',
    x: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 6 6 18"/><path d="m6 6 12 12"/></svg>',
    file: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M15 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7Z"/><path d="M14 2v4a2 2 0 0 0 2 2h4"/><path d="M16 13H8"/><path d="M16 17H8"/><path d="M10 9H8"/></svg>',
    copy: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="14" height="14" x="8" y="8" rx="2"/><path d="M4 16c-1.1 0-2-.9-2-2V4c0-1.1.9-2 2-2h10c1.1 0 2 .9 2 2"/></svg>',
    link: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"/><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"/></svg>',
  };
  return `<!doctype html><html lang="en"><head><meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>Memory Network</title>
<style>
  :root{ --bg:#0e0c0a; --panel:#171310; --edge:#2a231d; --ink:#f2ead9; --dim:#a79a86; --accent:#ff8352; --accent2:#ffc27a; }
  *{box-sizing:border-box} html,body{margin:0;height:100%;background:var(--bg);color:var(--ink);
    font-family: ui-rounded,"SF Pro Rounded",Nunito,system-ui,sans-serif;overflow:hidden}
  #graph{position:fixed;inset:0}
  .chrome{position:fixed;z-index:5}
  .topbar{top:16px;left:16px;display:flex;align-items:center;gap:12px}
  .brand{display:flex;align-items:center;gap:9px;background:rgba(23,19,16,.82);backdrop-filter:blur(8px);
    border:1px solid var(--edge);border-radius:12px;padding:9px 13px;font-weight:800;letter-spacing:-.01em}
  .brand svg{width:19px;height:19px;color:var(--accent)}
  .brand small{color:var(--dim);font-weight:600;font-size:12px;margin-left:4px}
  .searchbox{display:flex;align-items:center;gap:8px;background:rgba(23,19,16,.82);backdrop-filter:blur(8px);
    border:1px solid var(--edge);border-radius:12px;padding:8px 12px;width:260px}
  .searchbox svg{width:16px;height:16px;color:var(--dim);flex:none}
  .searchbox input{background:none;border:none;color:var(--ink);font:inherit;font-size:14px;width:100%;outline:none}
  .legend{bottom:16px;left:16px;display:flex;flex-wrap:wrap;gap:6px 12px;max-width:60vw;
    background:rgba(23,19,16,.82);backdrop-filter:blur(8px);border:1px solid var(--edge);border-radius:12px;padding:9px 13px}
  .legend b{color:var(--dim);font-weight:700;font-size:11px;letter-spacing:.1em;text-transform:uppercase;width:100%}
  .lg{display:inline-flex;align-items:center;gap:6px;font-size:12.5px;color:var(--dim);cursor:default}
  .lg i{width:10px;height:10px;border-radius:50%;display:inline-block}
  .stat{bottom:16px;right:16px;color:var(--dim);font-size:12px;background:rgba(23,19,16,.82);
    border:1px solid var(--edge);border-radius:10px;padding:7px 11px;font-variant-numeric:tabular-nums}
  .panel{position:fixed;z-index:6;top:16px;right:16px;width:340px;max-height:calc(100vh - 32px);overflow:auto;background:var(--panel);
    border:1px solid var(--edge);border-radius:16px;padding:0;transform:translateX(380px);opacity:0;
    transition:transform .22s cubic-bezier(.2,.8,.2,1),opacity .2s;pointer-events:none}
  .panel.open{transform:none;opacity:1;pointer-events:auto}
  .phead{display:flex;align-items:flex-start;gap:10px;padding:16px 16px 10px}
  .pdot{width:12px;height:12px;border-radius:50%;margin-top:5px;flex:none;box-shadow:0 0 12px currentColor}
  .ptitle{font-size:16.5px;font-weight:800;line-height:1.25;word-break:break-word}
  .ptype{font-size:11px;letter-spacing:.1em;text-transform:uppercase;color:var(--dim);font-weight:700;margin-top:3px}
  .pclose{margin-left:auto;background:none;border:none;color:var(--dim);cursor:pointer;padding:4px;border-radius:8px}
  .pclose:hover{color:var(--ink);background:var(--edge)} .pclose svg{width:17px;height:17px;display:block}
  .pbody{padding:0 16px 16px}
  .pdesc{color:#e7ddca;font-size:13.5px;line-height:1.5;margin:2px 0 14px}
  .prow{display:flex;align-items:center;gap:8px;font-size:12px;color:var(--dim);margin:7px 0}
  .prow svg{width:14px;height:14px;flex:none}
  .ppath{font-family:ui-monospace,monospace;font-size:11.5px;color:var(--accent2);word-break:break-all}
  .copy{margin-left:auto;background:var(--edge);border:none;color:var(--ink);border-radius:7px;padding:4px 6px;cursor:pointer}
  .copy svg{width:13px;height:13px;display:block}
  .plabel{font-size:11px;letter-spacing:.1em;text-transform:uppercase;color:var(--dim);font-weight:700;margin:14px 0 6px}
  .links{display:flex;flex-direction:column;gap:2px}
  .links button{text-align:left;background:none;border:none;color:var(--accent2);font:inherit;font-size:13px;
    cursor:pointer;padding:5px 7px;border-radius:8px;display:flex;align-items:center;gap:7px}
  .links button:hover{background:var(--edge);color:var(--accent)}
  .links button svg{width:12px;height:12px;flex:none;opacity:.7}
  .hint{position:fixed;bottom:52px;left:50%;transform:translateX(-50%);color:var(--dim);font-size:12px;opacity:.7;z-index:4}
</style></head>
<body>
<div id="graph"></div>
<div class="chrome topbar">
  <div class="brand">${ic.net}<span>Memory Network</span><small>${memLabel}</small></div>
  <div class="searchbox">${ic.search}<input id="q" placeholder="Search nodes..." autocomplete="off"/></div>
</div>
<div class="chrome legend" id="legend"><b>Groups</b></div>
<div class="chrome stat">${stats.nodes} nodes &middot; ${stats.links} links</div>
<div class="hint">scroll to zoom &middot; drag to pan &middot; click a node</div>
<aside class="panel" id="panel">
  <div class="phead"><span class="pdot" id="pdot"></span>
    <div><div class="ptitle" id="ptitle"></div><div class="ptype" id="ptype"></div></div>
    <button class="pclose" id="pclose" title="close">${ic.x}</button></div>
  <div class="pbody">
    <div class="pdesc" id="pdesc"></div>
    <div class="prow">${ic.file}<span class="ppath" id="ppath"></span>
      <button class="copy" id="pcopy" title="copy path">${ic.copy}</button></div>
    <div class="plabel">Connections</div>
    <div class="links" id="plinks"></div>
  </div>
</aside>
<script>${LIB.replace(/<\/script/gi, "<\\/script")}</script>
<script>
const DATA = ${json};
const IC_LINK = ${JSON.stringify(ic.link)};
const PALETTE = ["#ff8352","#7bd88f","#7aa2ff","#ffc27a","#c792ea","#ff6b9d","#5ec8d8","#8a7f6e"];
const groups = [...new Set(DATA.nodes.map(n=>n.group))].sort();
const COLORS = Object.fromEntries(groups.map((g,i)=>[g, PALETTE[i % PALETTE.length]]));
const color = g => COLORS[g] || "#8a7f6e";

const adj = new Map(); DATA.nodes.forEach(n=>adj.set(n.id,new Set()));
DATA.links.forEach(l=>{ const s=l.source.id||l.source, t=l.target.id||l.target;
  adj.get(s)?.add(t); adj.get(t)?.add(s); });

const el = document.getElementById("graph");
const Graph = ForceGraph()(el)
  .graphData(DATA)
  .backgroundColor("#0e0c0a")
  .nodeRelSize(4)
  .nodeVal(n => 1 + n.deg * 0.9)
  .linkColor(()=> "rgba(120,105,88,.28)")
  .linkWidth(l => (hoverId && ((l.source.id||l.source)===hoverId || (l.target.id||l.target)===hoverId)) ? 1.6 : 0.6)
  .linkDirectionalParticles(0)
  .enableNodeDrag(false)
  .d3VelocityDecay(0.4)
  .cooldownTicks(140)
  .onNodeClick(n => { lastSelectAt = Date.now(); select(n); })
  .onNodeHover(n => { hoverId = n ? n.id : null; el.style.cursor = n ? "pointer":"default"; })
  .onBackgroundClick(()=> { if (Date.now() - lastSelectAt > 250) closePanel(); })
  .nodeCanvasObject((n, ctx, globalScale) => {
    // radius in GRAPH units (force-graph pre-transforms ctx by zoom) so the
    // drawn node and its hit-area (below) live in the same coordinate space.
    const r = nodeR(n);
    const active = !hoverId || n.id===hoverId || adj.get(hoverId)?.has(n.id) || n.id===selId;
    ctx.globalAlpha = active ? 1 : 0.15;
    ctx.beginPath(); ctx.arc(n.x, n.y, r, 0, 2*Math.PI);
    ctx.fillStyle = color(n.group); ctx.fill();
    if (n.id===selId){ ctx.lineWidth = 2/globalScale; ctx.strokeStyle="#fff"; ctx.stroke(); }
    if (globalScale > 1.3 || n.deg >= 6 || n.id===hoverId || n.id===selId){
      const fs = 12/globalScale;
      ctx.font = \`\${fs}px ui-rounded, system-ui\`;
      ctx.fillStyle = active ? "#f2ead9" : "rgba(242,234,217,.25)";
      ctx.textAlign="center"; ctx.textBaseline="top";
      ctx.fillText(n.label, n.x, n.y + r + 2/globalScale);
    }
    ctx.globalAlpha = 1;
  })
  .nodePointerAreaPaint((n, col, ctx) => {
    ctx.beginPath(); ctx.arc(n.x, n.y, nodeR(n) + 2, 0, 2*Math.PI);
    ctx.fillStyle = col; ctx.fill();
  });
function nodeR(n){ return Math.sqrt(n.deg + 1) * 2 + 2; }

Graph.d3Force("charge").strength(-140);
Graph.d3Force("link").distance(38);

// Kill the built-in double-click-to-zoom: it flings the view and fights node
// selection. Capture phase so it runs before the library's own handler.
el.addEventListener("dblclick", (e) => { e.stopPropagation(); e.preventDefault(); }, true);

let hoverId=null, selId=null, lastSelectAt=0;
const byId = new Map(DATA.nodes.map(n=>[n.id,n]));

function select(n){
  selId = n.id;
  document.getElementById("panel").classList.add("open");
  document.getElementById("pdot").style.color = color(n.group);
  document.getElementById("ptitle").textContent = n.label;
  document.getElementById("ptype").textContent = n.group;
  document.getElementById("pdesc").textContent = n.description || "(no description)";
  document.getElementById("ppath").textContent = n.rel;
  const wrap = document.getElementById("plinks"); wrap.innerHTML="";
  const nbrs = [...(adj.get(n.id)||[])].map(id=>byId.get(id)).filter(Boolean)
    .sort((a,b)=>b.deg-a.deg);
  if (!nbrs.length) wrap.innerHTML = '<span style="color:var(--dim);font-size:12.5px;padding:4px 7px">No links yet.</span>';
  nbrs.forEach(t=>{ const b=document.createElement("button");
    b.innerHTML = IC_LINK;
    const sp=document.createElement("span"); sp.textContent=t.label; b.appendChild(sp);
    b.onclick=()=>{ const node=byId.get(t.id); select(node); if(node.x!=null) Graph.centerAt(node.x,node.y,500); };
    wrap.appendChild(b); });
}
function closePanel(){ selId=null; document.getElementById("panel").classList.remove("open"); }
document.getElementById("pclose").onclick=closePanel;
document.getElementById("pcopy").onclick=()=>{ const n=byId.get(selId); if(n) navigator.clipboard?.writeText(n.path); };

const q=document.getElementById("q");
q.addEventListener("input",()=>{ const s=q.value.trim().toLowerCase(); if(!s){hoverId=null;return;}
  const hit=DATA.nodes.filter(n=>n.label.toLowerCase().includes(s)||(n.description||"").toLowerCase().includes(s))
    .sort((a,b)=>b.deg-a.deg)[0];
  if(hit){ hoverId=hit.id; if(hit.x!=null){ Graph.centerAt(hit.x,hit.y,500); Graph.zoom(3,500);} } });
q.addEventListener("keydown",e=>{ if(e.key==="Enter"){ const s=q.value.trim().toLowerCase();
  const hit=DATA.nodes.filter(n=>n.label.toLowerCase().includes(s)).sort((a,b)=>b.deg-a.deg)[0];
  if(hit) select(hit); } });

const legend=document.getElementById("legend");
groups.forEach(g=>{ const s=document.createElement("span"); s.className="lg";
  const i=document.createElement("i"); i.style.background=color(g); s.appendChild(i);
  s.appendChild(document.createTextNode(g)); legend.appendChild(s); });

// Size to the CONTAINER and OBSERVE it, so the graph re-measures if embedded
// in a tab/iframe that becomes visible later; a hidden 0-size canvas maps
// clicks to the wrong coordinates.
const fit = () => { const r = el.getBoundingClientRect(); if (r.width > 0 && r.height > 0) Graph.width(r.width).height(r.height); };
new ResizeObserver(fit).observe(el);
addEventListener("resize", fit);
fit();
setTimeout(() => { fit(); Graph.zoomToFit(500, 60); }, 400);
</script></body></html>`;
}
