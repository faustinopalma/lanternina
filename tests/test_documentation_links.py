"""Every local link and every named test file in the documentation resolves.

Two sessions edited the repository at once on 25 August 2026: one changed behaviour, the
other rewrote the documentation around it. What that can leave behind is a document that
reads well and points at a file somebody moved, which nothing else here would catch.

Only local targets. An http link is somebody else's uptime, not ours.
"""

from __future__ import annotations

import re
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
# Where prose lives. `attic/` is included on purpose: it is meant to stay readable.
PROSE = [
    *REPO.glob("*.md"),
    *(REPO / "docs").rglob("*.md"),
    *(REPO / "ideas").glob("*.md"),
    *(REPO / "attic").glob("*.md"),
    *(REPO / "experiments").glob("*.md"),
    *(REPO / "firmware").glob("*.md"),
]

LINK = re.compile(r"\[[^\]]*\]\(([^)\s]+)\)")
# A path in backticks that looks like a file we ship, so a renamed module is caught too.
MENTION = re.compile(r"`((?:tests|shared|panel|devices|agents|orchestrator|printing)/[\w./]+\.py)`")

# Which prose describes the system as it is now. `ideas/` and `attic/` are records of what
# was: naming `devices/run_blueprint.py` there is the point, not a mistake, and a check
# that refused it would be asking history to be rewritten every time something is retired.
AS_IT_IS_NOW = [page for page in PROSE if page.parent in (REPO, REPO / "docs")]


def test_every_local_link_in_the_prose_points_at_something() -> None:
    missing: list[str] = []
    for page in PROSE:
        for target in LINK.findall(page.read_text(encoding="utf-8")):
            if target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            path = (page.parent / target.split("#")[0]).resolve()
            if not path.exists():
                missing.append(f"{page.relative_to(REPO)} -> {target}")

    assert not missing, "links with nothing behind them:\n" + "\n".join(missing)


def test_every_module_the_current_documentation_names_exists() -> None:
    """A document describing today must not name a module that went to the attic."""
    missing: list[str] = []
    for page in AS_IT_IS_NOW:
        for named in MENTION.findall(page.read_text(encoding="utf-8")):
            if not (REPO / named).exists():
                missing.append(f"{page.relative_to(REPO)} -> {named}")

    assert not missing, "modules named that are not there:\n" + "\n".join(missing)


def test_the_prose_was_actually_read() -> None:
    """The lesson from the hub check that reported a clean tree having compared nothing."""
    assert len(PROSE) > 15, f"only found {len(PROSE)} documents; the globs are wrong"
    assert len(AS_IT_IS_NOW) > 4, f"only found {len(AS_IT_IS_NOW)} current documents"
