import { createWhiteboard } from "./whiteboard";

(() => {
  const param = new URLSearchParams(window.location.search).get("scoutTheme");
  const theme =
    param || (window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light");
  document.documentElement.setAttribute("data-theme", theme);
})();

const slides = Array.from(document.querySelectorAll<HTMLElement>("[data-slide]"));
const links = Array.from(document.querySelectorAll<HTMLAnchorElement>("[data-go]"));
const previous = document.querySelector<HTMLButtonElement>("#previous")!;
const next = document.querySelector<HTMLButtonElement>("#next")!;
const counter = document.querySelector<HTMLElement>("#current-slide")!;
const notes = document.querySelector<HTMLDialogElement>("#speaker-notes")!;
const notesContent = document.querySelector<HTMLElement>("#notes-content")!;
const fullscreen = document.querySelector<HTMLButtonElement>("#fullscreen")!;
let current = 0;
let touchStart: { x: number; y: number } | null = null;
const whiteboard = createWhiteboard(slides);

function readHash() {
  const value = Number(location.hash.slice(1));
  return Number.isInteger(value) && value >= 1 && value <= slides.length ? value - 1 : 0;
}

function updateNotes() {
  const source = document.querySelector<HTMLTemplateElement>(`[data-notes="${current}"]`)!;
  notesContent.replaceChildren(source.content.cloneNode(true));
  notes.querySelector(".notes-position")!.textContent =
    `${String(current + 1).padStart(2, "0")} / 05`;
}

function showSlide(index: number) {
  current = Math.max(0, Math.min(slides.length - 1, index));
  slides.forEach((slide, position) => {
    const active = position === current;
    slide.hidden = !active;
    slide.inert = !active;
    slide.classList.toggle("is-current", active);
    if (active) slide.scrollTop = 0;
  });
  links.forEach((link, position) => {
    if (position === current) link.setAttribute("aria-current", "step");
    else link.removeAttribute("aria-current");
  });
  previous.disabled = current === 0;
  next.disabled = current === slides.length - 1;
  counter.textContent = String(current + 1).padStart(2, "0");
  document.querySelectorAll<HTMLAnchorElement>("[data-language]").forEach((link) => {
    const target = new URL(link.href);
    target.hash = String(current + 1);
    const theme = new URLSearchParams(location.search).get("scoutTheme");
    if (theme === "light" || theme === "dark") target.searchParams.set("scoutTheme", theme);
    link.href = target.href;
  });
  updateNotes();
  whiteboard.activate(slides[current]);
}

function goTo(index: number) {
  const bounded = Math.max(0, Math.min(slides.length - 1, index));
  if (bounded === current) return;
  location.hash = String(bounded + 1);
}

previous.addEventListener("click", () => goTo(current - 1));
next.addEventListener("click", () => goTo(current + 1));
window.addEventListener("hashchange", () => showSlide(readHash()));
document.addEventListener("keydown", (event) => {
  if (document.querySelector("dialog[open]") || event.altKey || event.ctrlKey || event.metaKey) return;
  if (event.target instanceof HTMLElement && event.target.closest("input, textarea, select, [contenteditable]")) return;
  let target: number | undefined;
  if (["ArrowRight", "PageDown"].includes(event.key)) target = current + 1;
  if (["ArrowLeft", "PageUp"].includes(event.key)) target = current - 1;
  if (event.key === "Home") target = 0;
  if (event.key === "End") target = slides.length - 1;
  if (event.key === " " && event.target === document.body) target = current + 1;
  if (target !== undefined) {
    event.preventDefault();
    goTo(target);
  }
});

const deck = document.querySelector<HTMLElement>(".deck")!;
deck.addEventListener("touchstart", (event) => {
  touchStart = null;
  if (event.touches.length !== 1) return;
  if (event.target instanceof Element && event.target.closest("a, button")) return;
  touchStart = { x: event.touches[0].clientX, y: event.touches[0].clientY };
}, { passive: true });
deck.addEventListener("touchend", (event) => {
  if (!touchStart) return;
  const horizontal = event.changedTouches[0].clientX - touchStart.x;
  const vertical = event.changedTouches[0].clientY - touchStart.y;
  touchStart = null;
  if (Math.abs(horizontal) >= 70 && Math.abs(horizontal) > Math.abs(vertical) * 1.5) {
    goTo(current + (horizontal < 0 ? 1 : -1));
  }
}, { passive: true });
deck.addEventListener("touchcancel", () => { touchStart = null; });

document.querySelector("#open-notes")!.addEventListener("click", () => notes.showModal());
document.querySelector("#close-notes")!.addEventListener("click", () => notes.close());
notes.addEventListener("click", (event) => {
  if (event.target !== notes) return;
  const bounds = notes.getBoundingClientRect();
  if (event.clientX < bounds.left || event.clientX > bounds.right || event.clientY < bounds.top || event.clientY > bounds.bottom) notes.close();
});

fullscreen.disabled = !document.fullscreenEnabled;
fullscreen.addEventListener("click", async () => {
  try {
    if (document.fullscreenElement) await document.exitFullscreen();
    else await document.documentElement.requestFullscreen();
  } catch {
    fullscreen.disabled = true;
  }
});
document.addEventListener("fullscreenchange", () => {
  const label = document.fullscreenElement ? fullscreen.dataset.exit! : fullscreen.dataset.enter!;
  fullscreen.setAttribute("aria-label", label);
  fullscreen.title = label;
  fullscreen.setAttribute("aria-pressed", String(Boolean(document.fullscreenElement)));
});

showSlide(readHash());
document.body.dataset.ready = "true";