# WHITEBOARD — pen/annotation engine (portable)

A self-contained, dependency-free SVG ink overlay that turns any HTML page into an
annotatable "whiteboard". Designed for **Wacom / active pens** but works with mouse and
touch. This is the reference implementation to copy into other projects.

## What it does / design goals

- **Pen front tip draws, back tip erases** — automatically, no tool to pick.
- **Mouse navigates** (clicks, scroll, links) and never draws, unless the user turns on a
  "Mouse draws" toggle.
- **Touch scrolls** (never draws) so the page stays usable on touch screens.
- Pressure-sensitive stroke width; quadratic-smoothed strokes.
- Stroke-level erase (removes whole strokes near the eraser, not pixels).
- Undo / clear; **ink persisted to `localStorage`** (survives reload).
- Works from `file://` (localStorage may be blocked there — engine still works in-memory).

## The one bug that matters (and the fix)

Naive overlays capture all pointer events, which breaks mouse scrolling/clicking; or, if
the overlay is always transparent, the pen strokes get eaten by the page's scroll/pan and
the pen "jumps after a few millimetres".

**Reliable fix (used here):** keep the overlay `pointer-events:none` by default, and
*arm* it only while a pen/eraser is in proximity:

- On `window` `pointerover`/`pointermove` (passive), inspect `e.pointerType`:
  - `pen`/`eraser` → set the overlay `pointer-events:auto` **and**
    `document.documentElement.style.touchAction = "none"` (this is what stops the page
    from panning/scrolling the pen stroke).
  - `mouse` → overlay `auto` only if the "Mouse draws" toggle is on, else `none`; restore
    `touchAction`.
  - `touch` → overlay `none`; restore `touchAction`.
- Draw handlers on the overlay use `setPointerCapture(e.pointerId)` and the overlay CSS has
  `touch-action:none`.

This combination (arm-on-proximity + `setPointerCapture` + `touch-action:none` on the
overlay and, while the pen is near, on `<html>`) is what makes pen drawing rock-solid.
A previous window-level-capture + `stopImmediatePropagation` approach was unreliable and
was abandoned.

## Eraser detection

```js
function isEraserTip(e){
  return e.pointerType === "eraser" ||
         (e.pointerType === "pen" && (((e.buttons||0) & 32) || e.button === 5));
}
```

Some pens report the back/barrel eraser as `pointerType:"eraser"`; others report a
`pen` with the eraser button bit (`buttons & 32`) or `button === 5`.

## Minimal HTML + CSS

Put the overlay as the **last child of the scroll container** you want to annotate
(`#app`), so it can be absolutely positioned over the full content height.

```html
<div id="app">
  <!-- ...page content... -->
  <svg id="ink" xmlns="http://www.w3.org/2000/svg"></svg>
</div>

<!-- toolbar (optional) -->
<div id="wbbar">
  <button class="tbtn" id="mousedraw">🖱 Mouse draws</button>
  <div id="colors"></div>
  <input type="range" id="width" min="1" max="14" value="3" />
  <button class="tbtn" id="undo">↶ Undo</button>
  <button class="tbtn" id="clear">🗑 Clear</button>
</div>
```

```css
#app{position:relative}
#ink{position:absolute;left:0;top:0;width:100%;touch-action:none;z-index:30;pointer-events:none}
#ink path{fill:none;stroke-linecap:round;stroke-linejoin:round}
```

(For a fixed toolbar, add `top`/`padding-top` offsets; if `#ink` starts below a fixed bar,
set `#ink{top:<barHeight>px}` and size it to the content below.)

## Engine (single-page variant)

```html
<script>
(function(){
  "use strict";
  const NS="http://www.w3.org/2000/svg";
  const app=document.getElementById("app");
  const ink=document.getElementById("ink");
  const STORE_KEY="wb-v1";                 // change per page/run to avoid ink collisions
  const COLORS=[{c:"#b11f4b"},{c:"#0078d4"},{c:"#16a34a"},{c:"#f59e0b"},{c:"#242424"}];
  let color=COLORS[0].c, width=3, mouseDraw=false;
  let cur=null, drawing=false;
  let strokes=[];                          // {color,width,pts:[{x,y}],el}

  function persist(){ try{ localStorage.setItem(STORE_KEY, JSON.stringify(strokes.map(s=>({c:s.color,w:s.width,p:s.pts})))); }catch(e){} }
  function loadPersisted(){ try{ const r=localStorage.getItem(STORE_KEY); if(r){ strokes=JSON.parse(r).map(s=>({color:s.c,width:s.w,pts:s.p,el:null})); } }catch(e){} }

  function pathD(pts){
    if(!pts.length) return "";
    if(pts.length===1){ const p=pts[0]; return `M ${p.x} ${p.y} L ${p.x+0.01} ${p.y}`; }
    let d=`M ${pts[0].x} ${pts[0].y}`;
    for(let i=1;i<pts.length-1;i++){ const mx=(pts[i].x+pts[i+1].x)/2, my=(pts[i].y+pts[i+1].y)/2; d+=` Q ${pts[i].x} ${pts[i].y} ${mx} ${my}`; }
    const l=pts[pts.length-1]; d+=` L ${l.x} ${l.y}`; return d;
  }
  function makeEl(s){ const p=document.createElementNS(NS,"path"); p.setAttribute("d",pathD(s.pts)); p.setAttribute("stroke",s.color); p.setAttribute("stroke-width",s.width); ink.appendChild(p); s.el=p; return p; }
  function render(){ while(ink.firstChild) ink.removeChild(ink.firstChild); strokes.forEach(makeEl); }
  function sizeInk(){ const h=app.offsetHeight; ink.style.height=h+"px"; ink.setAttribute("width", ink.clientWidth); ink.setAttribute("height", h); }

  function segDist2(px,py,ax,ay,bx,by){ const dx=bx-ax,dy=by-ay,l2=dx*dx+dy*dy; let t=l2?((px-ax)*dx+(py-ay)*dy)/l2:0; t=Math.max(0,Math.min(1,t)); const x=ax+t*dx,y=ay+t*dy,ex=px-x,ey=py-y; return ex*ex+ey*ey; }
  function eraseAt(x,y){
    for(let i=strokes.length-1;i>=0;i--){
      const s=strokes[i], r=Math.max(s.width,10)+10, r2=r*r, pts=s.pts; let hit=false;
      if(pts.length===1){ hit=((pts[0].x-x)**2+(pts[0].y-y)**2)<=r2; }
      for(let j=0;j<pts.length-1 && !hit;j++){ if(segDist2(x,y,pts[j].x,pts[j].y,pts[j+1].x,pts[j+1].y)<=r2) hit=true; }
      if(hit){ if(s.el&&s.el.parentNode) s.el.parentNode.removeChild(s.el); strokes.splice(i,1); persist(); }
    }
  }
  function pt(e){ const r=ink.getBoundingClientRect(); return {x:+(e.clientX-r.left).toFixed(1), y:+(e.clientY-r.top).toFixed(1)}; }

  // ---- ARM-ON-PROXIMITY: the core of the reliable behaviour ----
  const root=document.documentElement;
  function armOverlay(e){
    const t=e.pointerType;
    if(t==="pen"||t==="eraser"){ ink.style.pointerEvents="auto"; root.style.touchAction="none"; }
    else if(t==="mouse"){ ink.style.pointerEvents = mouseDraw ? "auto" : "none"; root.style.touchAction=""; }
    else { ink.style.pointerEvents="none"; root.style.touchAction=""; }
  }
  window.addEventListener("pointerover", armOverlay, {passive:true});
  window.addEventListener("pointermove", armOverlay, {passive:true});

  function isEraserTip(e){ return e.pointerType==="eraser" || (e.pointerType==="pen" && (((e.buttons||0)&32) || e.button===5)); }
  function onDown(e){
    if(e.pointerType==="touch") return;
    if(e.pointerType==="mouse" && !mouseDraw) return;
    e.preventDefault();
    try{ ink.setPointerCapture(e.pointerId); }catch(_){}
    drawing=true; const p=pt(e);
    if(isEraserTip(e)){ cur={mode:"eraser"}; eraseAt(p.x,p.y); return; }
    const pr=(e.pressure&&e.pressure>0)?e.pressure:0.5; const w=Math.max(1, width*(0.55+0.9*pr));
    const s={color:color,width:+w.toFixed(2),pts:[p],el:null}; strokes.push(s); makeEl(s); cur={mode:"pen",stroke:s};
  }
  function onMove(e){
    if(!drawing||!cur) return; e.preventDefault(); const p=pt(e);
    if(cur.mode==="eraser"){ eraseAt(p.x,p.y); return; }
    const s=cur.stroke, last=s.pts[s.pts.length-1];
    if(Math.hypot(p.x-last.x,p.y-last.y)<1.2) return;          // min-distance de-noise
    s.pts.push(p); s.el.setAttribute("d",pathD(s.pts));
  }
  function onUp(){ if(!drawing) return; drawing=false; persist(); cur=null; }
  ink.addEventListener("pointerdown",onDown);
  ink.addEventListener("pointermove",onMove);
  ink.addEventListener("pointerup",onUp);
  ink.addEventListener("pointercancel",onUp);
  window.addEventListener("pointerup",onUp);

  // ---- toolbar wiring ----
  const mdBtn=document.getElementById("mousedraw");
  if(mdBtn) mdBtn.addEventListener("click",()=>{ mouseDraw=!mouseDraw; mdBtn.classList.toggle("on",mouseDraw); });
  const colWrap=document.getElementById("colors");
  if(colWrap) COLORS.forEach((co,i)=>{ const b=document.createElement("button"); b.className="sw"+(i===0?" on":""); b.style.background=co.c;
    b.addEventListener("click",()=>{ color=co.c; document.querySelectorAll("#colors .sw").forEach(s=>s.classList.remove("on")); b.classList.add("on"); }); colWrap.appendChild(b); });
  const wEl=document.getElementById("width"); if(wEl) wEl.addEventListener("input",e=>{ width=+e.target.value; });
  const uEl=document.getElementById("undo"); if(uEl) uEl.addEventListener("click",()=>{ if(strokes.length){ const s=strokes.pop(); if(s.el&&s.el.parentNode) s.el.parentNode.removeChild(s.el); persist(); } });
  const cEl=document.getElementById("clear"); if(cEl) cEl.addEventListener("click",()=>{ if(!strokes.length) return; if(!confirm("Clear all ink?")) return; strokes=[]; render(); persist(); });
  window.addEventListener("keydown",e=>{ if(e.target.tagName==="INPUT"||e.target.tagName==="SELECT") return; if((e.ctrlKey||e.metaKey)&&e.key.toLowerCase()==="z"){ uEl&&uEl.click(); e.preventDefault(); } });

  // ---- keep overlay sized to (animated) content ----
  const ro=new ResizeObserver(()=>sizeInk()); ro.observe(app);
  window.addEventListener("resize",sizeInk);
  window.addEventListener("load",()=>{ sizeInk(); setTimeout(sizeInk,400); setTimeout(sizeInk,1400); });

  loadPersisted(); render(); sizeInk();
})();
</script>
```

## SPA (multi-page) variant differences

For a single-file SPA with several "views" (only one visible at a time) — as in
`briefings-whiteboard.html` — change three things:

1. **Ink is per view.** Replace the single `strokes[]` with `const pages = {};` keyed by
   the active view id: `pages[activeId] = [ ...strokes ]`. `persist()` serialises the whole
   map; `loadPersisted()` rebuilds it.
2. **Re-render on navigation.** When routing changes the active view, call `renderPage()`
   (clears `#ink`, redraws `pages[active]`) and `sizeInk()` for the new view's height.
3. **Offset the overlay** below a fixed toolbar: `#ink{top:64px}` and size to the active
   view's `offsetHeight`.

Everything else (arm-on-proximity, `isEraserTip`, draw handlers, eraser math) is identical.

## Per-run storage keys

Give each page/run a **unique `STORE_KEY`** (e.g. `tub-pipeline-wb-<YYYYMMDD>`,
`tub-whiteboard-<YYYYMMDD>`) so annotations from different reports never collide in
`localStorage`.

## Verifying it (Playwright / DOM)

Screenshots have been flaky in this environment — assert on the DOM instead. Dispatch
synthetic `PointerEvent`s with `pointerType` set and check `#ink path` counts:

```js
// pen draws 1 path
window.dispatchEvent(new PointerEvent('pointerover',{pointerId:1,pointerType:'pen',clientX,clientY}));
ink.dispatchEvent(new PointerEvent('pointerdown',{pointerId:1,pointerType:'pen',buttons:1,clientX,clientY,pressure:.5}));
// ...pointermove x N...
ink.dispatchEvent(new PointerEvent('pointerup',{pointerId:1,pointerType:'pen'}));
// assert: ink.querySelectorAll('path').length === 1
// mouse (toggle off) adds 0; eraser removes; localStorage[STORE_KEY] set.
```

Key assertions: pen path count increments, `getComputedStyle(ink).pointerEvents` is
`auto` for pen and `none` for mouse (toggle off), eraser reduces the count to 0, and the
`STORE_KEY` entry exists.
