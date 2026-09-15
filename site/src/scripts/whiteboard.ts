type InkColor = "accent" | "link" | "success" | "warning" | "text";
type Point = { x: number; y: number };
type Stroke = { color: InkColor; width: number; points: Point[] };
type Gesture = { pointerId: number; mode: "pen" | "eraser"; stroke?: Stroke };

const namespace = "http://www.w3.org/2000/svg";
const palette: InkColor[] = ["accent", "link", "success", "warning", "text"];

export function createWhiteboard(slides: HTMLElement[]) {
  const storageKey = `lanternina-presentation-ink-v1:${document.documentElement.lang}`;
  const pages: Record<string, Stroke[]> = Object.fromEntries(slides.map(slide => [slide.id, []]));
  const undoHistory: Record<string, Stroke[][]> = Object.fromEntries(slides.map(slide => [slide.id, []]));
  const overlays = new Map<HTMLElement, SVGSVGElement>();
  const root = document.documentElement;
  const tools = document.querySelector<HTMLElement>("#whiteboard-tools")!;
  const toggle = document.querySelector<HTMLButtonElement>("#toggle-whiteboard")!;
  const mouse = document.querySelector<HTMLInputElement>("#mouse-draw")!;
  const widthInput = document.querySelector<HTMLInputElement>("#ink-width")!;
  const undo = document.querySelector<HTMLButtonElement>("#ink-undo")!;
  const clear = document.querySelector<HTMLButtonElement>("#ink-clear")!;
  const clearDialog = document.querySelector<HTMLDialogElement>("#clear-ink-dialog")!;
  let active = slides[0];
  let color: InkColor = "accent";
  let width = 3;
  let gesture: Gesture | null = null;
  let pointerType = "mouse";
  let contentWidth = 1;
  let contentHeight = 1;
  let eraserChanged = false;

  function validStroke(value: unknown): value is Stroke {
    if (!value || typeof value !== "object") return false;
    const stroke = value as Stroke;
    return palette.includes(stroke.color) && Number.isFinite(stroke.width)
      && stroke.width >= 1 && stroke.width <= 21 && Array.isArray(stroke.points)
      && stroke.points.length > 0 && stroke.points.length <= 100000
      && stroke.points.every(point => point && Number.isFinite(point.x)
        && Number.isFinite(point.y) && point.x >= 0 && point.x <= 1
        && point.y >= 0 && point.y <= 1);
  }

  try {
    const saved = JSON.parse(localStorage.getItem(storageKey) ?? "null");
    if (saved && typeof saved === "object") {
      for (const slide of slides) {
        const savedPage = saved[slide.id];
        if (Array.isArray(savedPage) && savedPage.length <= 10000) {
          pages[slide.id] = savedPage.filter(validStroke);
        }
      }
    }
  } catch {}

  function persist() {
    try { localStorage.setItem(storageKey, JSON.stringify(pages)); } catch {}
  }

  function updateTools() {
    undo.disabled = undoHistory[active.id].length === 0 && pages[active.id].length === 0;
    clear.disabled = pages[active.id].length === 0;
  }

  function checkpoint() {
    undoHistory[active.id].push(structuredClone(pages[active.id]));
    if (undoHistory[active.id].length > 50) undoHistory[active.id].shift();
  }

  function pathData(points: Point[]) {
    const pixels = points.map(point => ({ x: point.x * contentWidth, y: point.y * contentHeight }));
    const first = pixels[0];
    if (pixels.length === 1) return `M ${first.x} ${first.y} l 0.01 0`;
    let path = `M ${first.x} ${first.y}`;
    for (let index = 1; index < pixels.length - 1; index++) {
      const point = pixels[index];
      const next = pixels[index + 1];
      path += ` Q ${point.x} ${point.y} ${(point.x + next.x) / 2} ${(point.y + next.y) / 2}`;
    }
    const last = pixels[pixels.length - 1];
    return `${path} L ${last.x} ${last.y}`;
  }

  function render() {
    const ink = overlays.get(active)!;
    ink.replaceChildren(...pages[active.id].map(stroke => {
      const path = document.createElementNS(namespace, "path");
      path.setAttribute("d", pathData(stroke.points));
      path.setAttribute("stroke", `var(--cp-${stroke.color})`);
      path.setAttribute("stroke-width", String(stroke.width));
      return path;
    }));
    updateTools();
  }

  function sizeInk() {
    const ink = overlays.get(active)!;
    ink.setAttribute("height", "0");
    contentWidth = active.clientWidth;
    contentHeight = active.scrollHeight;
    ink.setAttribute("width", String(contentWidth));
    ink.setAttribute("height", String(contentHeight));
    ink.setAttribute("viewBox", `0 0 ${contentWidth} ${contentHeight}`);
    render();
  }

  function setArmed() {
    const isPen = pointerType === "pen" || pointerType === "eraser";
    const available = !document.querySelector("dialog[open]");
    const armed = available && (isPen || (pointerType === "mouse" && mouse.checked));
    overlays.get(active)!.classList.toggle("is-armed", armed);
    root.classList.toggle("pen-in-range", available && isPen);
  }

  function armOverlay(event: PointerEvent) {
    if (gesture) return;
    pointerType = event.pointerType;
    setArmed();
  }

  function pointAt(event: PointerEvent): Point {
    const bounds = overlays.get(active)!.getBoundingClientRect();
    return {
      x: Math.max(0, Math.min(1, (event.clientX - bounds.left) / contentWidth)),
      y: Math.max(0, Math.min(1, (event.clientY - bounds.top) / contentHeight)),
    };
  }

  function isEraser(event: PointerEvent) {
    return event.pointerType === "eraser"
      || (event.pointerType === "pen" && ((event.buttons & 32) !== 0 || event.button === 5));
  }

  function segmentDistance(point: Point, start: Point, end: Point) {
    const deltaX = (end.x - start.x) * contentWidth;
    const deltaY = (end.y - start.y) * contentHeight;
    const pointX = (point.x - start.x) * contentWidth;
    const pointY = (point.y - start.y) * contentHeight;
    const lengthSquared = deltaX * deltaX + deltaY * deltaY;
    const fraction = lengthSquared ? Math.max(0, Math.min(1,
      (pointX * deltaX + pointY * deltaY) / lengthSquared)) : 0;
    return Math.hypot(pointX - fraction * deltaX, pointY - fraction * deltaY);
  }

  function eraseAt(point: Point) {
    const before = pages[active.id];
    const remaining = before.filter(stroke => !stroke.points.some((start, index) => {
      const end = stroke.points[index + 1] ?? start;
      return segmentDistance(point, start, end) <= Math.max(stroke.width, 10) + 10;
    }));
    if (remaining.length === before.length) return;
    if (!eraserChanged) checkpoint();
    eraserChanged = true;
    pages[active.id] = remaining;
    render();
  }

  function finish(event?: PointerEvent) {
    if (!gesture || (event && event.pointerId !== gesture.pointerId)) return;
    const ink = overlays.get(active)!;
    const pointerId = gesture.pointerId;
    gesture = null;
    if (ink.hasPointerCapture(pointerId)) ink.releasePointerCapture(pointerId);
    persist();
    updateTools();
    setArmed();
  }

  function onDown(event: PointerEvent) {
    if (gesture || event.pointerType === "touch") return;
    if (event.pointerType === "mouse" && (!mouse.checked || event.button !== 0)) return;
    if (!["mouse", "pen", "eraser"].includes(event.pointerType)) return;
    event.preventDefault();
    const ink = overlays.get(active)!;
    try { ink.setPointerCapture(event.pointerId); } catch {}
    const point = pointAt(event);
    eraserChanged = false;
    if (isEraser(event)) {
      gesture = { pointerId: event.pointerId, mode: "eraser" };
      eraseAt(point);
      return;
    }
    checkpoint();
    const pressure = event.pressure > 0 ? event.pressure : 0.5;
    const stroke: Stroke = { color, width: Math.max(1, width * (0.55 + 0.9 * pressure)), points: [point] };
    pages[active.id].push(stroke);
    gesture = { pointerId: event.pointerId, mode: "pen", stroke };
    render();
  }

  function onMove(event: PointerEvent) {
    if (!gesture || gesture.pointerId !== event.pointerId) return;
    event.preventDefault();
    const points = typeof event.getCoalescedEvents === "function" ? event.getCoalescedEvents() : [];
    for (const sample of points.length ? points : [event]) {
      const point = pointAt(sample);
      if (gesture.mode === "eraser") { eraseAt(point); continue; }
      const stroke = gesture.stroke!;
      const last = stroke.points[stroke.points.length - 1];
      if (Math.hypot((point.x - last.x) * contentWidth, (point.y - last.y) * contentHeight) < 1.2) continue;
      stroke.points.push(point);
    }
    if (gesture.mode === "pen") {
      overlays.get(active)!.lastElementChild!.setAttribute("d", pathData(gesture.stroke!.points));
    }
  }

  for (const slide of slides) {
    const ink = document.createElementNS(namespace, "svg");
    ink.classList.add("ink-overlay");
    ink.setAttribute("aria-hidden", "true");
    slide.appendChild(ink);
    overlays.set(slide, ink);
    ink.addEventListener("pointerdown", onDown);
    ink.addEventListener("pointermove", onMove);
    ink.addEventListener("pointerup", finish);
    ink.addEventListener("pointercancel", finish);
    ink.addEventListener("lostpointercapture", finish);
  }
  window.addEventListener("pointerover", armOverlay, { passive: true });
  window.addEventListener("pointermove", armOverlay, { passive: true });
  window.addEventListener("pointerup", finish);
  window.addEventListener("blur", () => {
    finish();
    pointerType = "touch";
    setArmed();
  });

  toggle.addEventListener("click", () => {
    tools.hidden = !tools.hidden;
    toggle.setAttribute("aria-expanded", String(!tools.hidden));
  });
  mouse.addEventListener("change", setArmed);
  document.querySelectorAll<HTMLButtonElement>("[data-ink-color]").forEach(button => {
    button.addEventListener("click", () => {
      color = button.dataset.inkColor as InkColor;
      document.querySelectorAll("[data-ink-color]").forEach(swatch => {
        swatch.setAttribute("aria-pressed", String(swatch === button));
      });
    });
  });
  widthInput.addEventListener("input", () => {
    width = Number(widthInput.value);
    document.querySelector<HTMLOutputElement>("#ink-width-value")!.value = String(width);
  });
  undo.addEventListener("click", () => {
    finish();
    const previous = undoHistory[active.id].pop();
    pages[active.id] = previous ?? pages[active.id].slice(0, -1);
    render();
    persist();
  });
  clear.addEventListener("click", () => {
    finish();
    clearDialog.showModal();
    setArmed();
  });
  document.querySelector("#cancel-clear")!.addEventListener("click", () => clearDialog.close());
  document.querySelector("#confirm-clear")!.addEventListener("click", () => {
    checkpoint();
    pages[active.id] = [];
    render();
    persist();
    clearDialog.close();
  });
  clearDialog.addEventListener("close", setArmed);
  document.addEventListener("keydown", event => {
    if (document.querySelector("dialog[open]")) return;
    if (event.target instanceof HTMLElement && event.target.closest("input, textarea, select, [contenteditable]")) return;
    if ((event.ctrlKey || event.metaKey) && !event.shiftKey && event.key.toLowerCase() === "z") {
      event.preventDefault();
      undo.click();
    }
  });
  const observer = new ResizeObserver(() => { if (active.clientWidth > 0) sizeInk(); });
  slides.forEach(slide => {
    observer.observe(slide);
    slide.querySelectorAll("img").forEach(image => image.addEventListener("load", sizeInk));
  });

  return {
    activate(slide: HTMLElement) {
      finish();
      overlays.get(active)!.classList.remove("is-armed");
      active = slide;
      sizeInk();
      setArmed();
    },
  };
}