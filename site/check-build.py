"""Check the built site: one document per language, agreeing hreflang, no dead links."""

from __future__ import annotations

import pathlib
import re
import sys
from html.parser import HTMLParser


class PresentationCheck(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.slides = 0
        self.slide_order: list[tuple[str | None, str | None]] = []
        self.notes = 0
        self.note_indices: list[str | None] = []
        self.slide_links: list[str | None] = []
        self.links: list[str] = []
        self.scripts: list[str | None] = []
        self.ids: set[str] = set()

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attributes = dict(attrs)
        if tag == "section" and "data-slide" in attributes:
            self.slides += 1
            self.slide_order.append((attributes.get("id"), attributes.get("class")))
        if tag == "template" and "data-notes" in attributes:
            self.notes += 1
            self.note_indices.append(attributes["data-notes"])
        if tag == "a" and "data-go" in attributes:
            self.slide_links.append(attributes.get("href"))
        if tag == "a" and attributes.get("href"):
            self.links.append(attributes["href"])
        if tag == "script":
            self.scripts.append(attributes.get("src"))
        if attributes.get("id"):
            self.ids.add(attributes["id"])

DIST = pathlib.Path("site/dist")
SITE = "https://lanternina.com"
PRESENTATIONS = {
    "present": ["opening", "technology", "principles"],
    "present4": ["opening", "technology", "paper", "principles"],
}

pages = sorted(p for p in DIST.rglob("*.html"))
problems: list[str] = []

print(f"pages built: {len(pages)}\n")

for page in pages:
    html = page.read_text(encoding="utf-8")
    rel = page.relative_to(DIST).as_posix()

    lang = re.search(r'<html[^>]*\blang="([^"]+)"', html)
    canonical = re.search(r'<link rel="canonical" href="([^"]+)"', html)
    alts = dict(
        re.findall(r'<link rel="alternate" hreflang="([^"]+)" href="([^"]+)"', html)
    )
    title = re.search(r"<title>([^<]*)</title>", html)

    print(f"{rel:26} lang={lang.group(1) if lang else '-':3} alts={sorted(alts) or '-'}")

    parsed = PresentationCheck()
    parsed.feed(html)
    presentation_name = page.parent.name
    if presentation_name in PRESENTATIONS:
        kinds = PRESENTATIONS[presentation_name]
        count = len(kinds)
        if parsed.slides != count or parsed.notes != count:
            problems.append(f"{rel}: expected {count} slides and {count} speech paragraphs")
        expected_order = [
            (f"slide-{index}", f"slide {kind}") for index, kind in enumerate(kinds, start=1)
        ]
        if parsed.slide_order != expected_order:
            problems.append(f"{rel}: expected slide order {kinds}")
        if parsed.note_indices != [str(index) for index in range(count)]:
            problems.append(f"{rel}: speech indices must follow slide positions")
        if parsed.slide_links != [f"#{index}" for index in range(1, count + 1)]:
            problems.append(f"{rel}: navigation must link to each slide in order")
        if any(not href.startswith(f"/{language}/{presentation_name}/")
               for language in ("en", "it")
               for href in parsed.links if href.startswith(f"/{language}/")):
            problems.append(f"{rel}: language links must keep the presentation version")
        required = {
            "previous", "next", "toggle-whiteboard", "mouse-draw", "ink-width",
            "ink-undo", "ink-clear", "clear-ink-dialog", "speaker-notes",
        }
        if not required.issubset(parsed.ids):
            problems.append(f"{rel}: missing controls {required - parsed.ids}")
        if not parsed.scripts or any(not src or not src.startswith("/_astro/")
                                     for src in parsed.scripts):
            problems.append(f"{rel}: presentation scripts must obey the self-only CSP")
        if 'name="robots" content="noindex, nofollow"' not in html:
            problems.append(f"{rel}: presentation must opt out of indexing")
    elif any(f"/{name}/" in href for name in PRESENTATIONS for href in parsed.links):
        problems.append(f"{rel}: public site links to the unlisted presentation")
    elif "toggle-whiteboard" in parsed.ids:
        problems.append(f"{rel}: whiteboard leaked into the main site")

    if rel == "404.html":
        continue

    if not lang:
        problems.append(f"{rel}: no lang attribute")
    if not title or not title.group(1).strip():
        problems.append(f"{rel}: no title")

    if rel == "index.html":
        if sorted(alts) != ["en", "it", "x-default"]:
            problems.append(f"{rel}: root must carry all three hreflang, got {sorted(alts)}")
        continue

    if not canonical:
        problems.append(f"{rel}: no canonical")
        continue

    # The canonical has to be the directory this file was actually written to.
    expected = f"{SITE}/{rel.removesuffix('index.html')}"
    if canonical.group(1) != expected:
        problems.append(f"{rel}: canonical is {canonical.group(1)}, expected {expected}")

    if sorted(alts) != ["en", "it", "x-default"]:
        problems.append(f"{rel}: hreflang set is {sorted(alts)}")
    else:
        # The alternate for this page's own language must be this page.
        mine = alts.get(lang.group(1))
        if mine != expected:
            problems.append(f"{rel}: its own hreflang points at {mine}, not itself")
        # And the other language's alternate must exist as a built file.
        other = "it" if lang.group(1) == "en" else "en"
        target = DIST / alts[other].removeprefix(f"{SITE}/") / "index.html"
        if not target.exists():
            problems.append(f"{rel}: alternate {alts[other]} was never built")

    # Local links must resolve to something on disk.
    for href in re.findall(r'href="(/[^"]*)"', html):
        clean = href.split("#")[0].split("?")[0]
        if not clean or clean.startswith("//"):
            continue
        cand = DIST / clean.lstrip("/")
        if cand.is_dir():
            cand = cand / "index.html"
        if not cand.exists():
            problems.append(f"{rel}: dead local link {href}")

    for src in re.findall(r'src="(/[^"]*)"', html):
        if not (DIST / src.lstrip("/")).exists():
            problems.append(f"{rel}: dead asset {src}")

# The two trees must have the same shape, or one language is quietly missing a page.
en = {p.relative_to(DIST / "en").as_posix() for p in (DIST / "en").rglob("*.html")}
it = {p.relative_to(DIST / "it").as_posix() for p in (DIST / "it").rglob("*.html")}
if en != it:
    problems.append(f"trees differ: only in en {en - it}, only in it {it - en}")

for language in ("en", "it"):
    for name in PRESENTATIONS:
        if not (DIST / language / name / "index.html").exists():
            problems.append(f"missing {language}/{name} presentation")
for sitemap in DIST.glob("sitemap*.xml"):
    if any(f"/{name}/" in sitemap.read_text(encoding="utf-8") for name in PRESENTATIONS):
        problems.append(f"{sitemap.name}: unlisted presentation is in the sitemap")

print(f"\nen tree: {sorted(en)}")
print(f"it tree: {sorted(it)}")

if problems:
    print("\nPROBLEMS")
    for p in problems:
        print(f"  - {p}")
    sys.exit(1)

print("\nOK")
