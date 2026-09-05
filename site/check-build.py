"""Check the built site: one document per language, agreeing hreflang, no dead links."""

from __future__ import annotations

import pathlib
import re
import sys

DIST = pathlib.Path("site/dist")
SITE = "https://lanternina.com"

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

print(f"\nen tree: {sorted(en)}")
print(f"it tree: {sorted(it)}")

if problems:
    print("\nPROBLEMS")
    for p in problems:
        print(f"  - {p}")
    sys.exit(1)

print("\nOK")
