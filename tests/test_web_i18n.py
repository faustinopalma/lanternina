"""The panel's translation catalogs.

Adding a language is meant to be adding one JSON file and one entry in `CATALOGS`. That
claim only holds if two things stay true, and both fail silently in a browser: every catalog
has to carry the same keys, and every key the panel asks for has to exist. A missing string
shows the key itself to a parent, which is exactly the kind of fault nobody reports.

TypeScript says the second thing too, from inside — `MessageKey` is `keyof typeof it`. These
tests say it from outside, on the shipped files, so the guarantee survives a build that is
never run and a type that is loosened.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

WEB = Path(__file__).resolve().parent.parent / "web"
SRC = WEB / "src"
CATALOGS = SRC / "i18n"

# Fixtures and assertions are allowed to hold Italian: they are content and expectations,
# not words the panel puts on a screen.
TESTS = SRC / "test"

USED = re.compile(r'\bt\(\s*"([\w.]+)"')

# Which files in `i18n/` are catalogues of the panel's own words. Named rather than
# globbed: `cities.json` lives there too and is CLDR place names keyed by IANA zone, so a
# glob read it as a language whose every key was missing.
CATALOG_NAMES = ("it", "en")


def sources() -> list[Path]:
    """Every file the panel is built from, minus its own tests."""
    return [
        path
        for path in SRC.rglob("*.ts*")
        if TESTS not in path.parents and not path.name.endswith(".d.ts")
    ]


def catalogs() -> dict[str, dict[str, str]]:
    found = {
        name: json.loads((CATALOGS / f"{name}.json").read_text(encoding="utf-8"))
        for name in CATALOG_NAMES
    }
    assert found, f"no catalogs in {CATALOGS}"
    return found


def test_every_catalog_carries_the_same_keys() -> None:
    found = catalogs()
    assert len(found) >= 2, f"expected at least two languages, found {sorted(found)}"
    reference = sorted(found)[0]
    for language, table in found.items():
        missing = set(found[reference]) - set(table)
        extra = set(table) - set(found[reference])
        assert not missing, f"{language} is missing {sorted(missing)}"
        assert not extra, f"{language} has keys no other catalog has: {sorted(extra)}"


def test_no_catalog_is_empty_or_holds_an_empty_string() -> None:
    for language, table in catalogs().items():
        assert len(table) > 20, f"{language} looks truncated: {len(table)} keys"
        blank = sorted(key for key, text in table.items() if not str(text).strip())
        assert not blank, f"{language} has nothing to say for {blank}"


def used_keys() -> set[str]:
    keys: set[str] = set()
    for path in sources():
        keys |= set(USED.findall(path.read_text(encoding="utf-8")))
    return keys


def test_every_key_the_panel_asks_for_exists() -> None:
    known = set().union(*(set(table) for table in catalogs().values()))
    unknown = sorted(key for key in used_keys() if key not in known)
    assert not unknown, f"the panel asks for keys no catalog has: {unknown}"


def test_the_computed_keys_are_all_present() -> None:
    """`kind.*`, `job.*` and `level.*` are built from a value, so nothing else catches a gap.

    The values come from Python, which is where the panel and the hub read them: a job
    added to `shared.capabilities` with no word for the parent fails here. The battery
    levels have no single home yet — `devices/trmnl_byos.py` names three of them and the
    hub adds "mains" — so they are stated here instead, which is a test doing its job
    rather than a fourth copy of a vocabulary.
    """
    from shared.capabilities import JOBS_BY_KIND, KINDS

    levels = ("mains", "ok", "low", "critical")
    expected = {
        *(f"kind.{kind}" for kind in KINDS),
        *(f"job.{job}" for jobs in JOBS_BY_KIND.values() for job in jobs),
        *(f"level.{level}" for level in levels),
    }
    for language, table in catalogs().items():
        missing = sorted(key for key in expected if key not in table)
        assert not missing, f"{language} has no word for {missing}"


def test_the_panel_keeps_no_italian_sentences() -> None:
    """The words live in the catalogs. A sentence left in the code cannot be translated."""
    marker = re.compile(
        r"(?i)(?<![\w-])(perch\u00e9|gi\u00e0|della|delle|questo|questa|sono|viene|"
        r"nessun\w*|caricando|riesco|riprova)(?![\w-])"
    )
    offences: list[str] = []
    for path in [*sources(), WEB / "index.html"]:
        body = path.read_text(encoding="utf-8")
        found = sorted({match.group(0) for match in marker.finditer(body)})
        if found:
            offences.append(f"{path.relative_to(WEB)}: {found}")
    assert not offences, "Italian left in the sources:\n" + "\n".join(offences)


def test_the_content_language_is_not_the_language_of_the_page() -> None:
    """The one wiring that must not exist.

    The household's content language is what arrives on paper and on the display. The
    page's language is a display preference of whoever is holding the phone. If the second
    ever writes the first, a parent switching their phone changes what arrives at home, and
    content approved in one language becomes content shown in another.
    """
    module = (CATALOGS / "index.tsx").read_text(encoding="utf-8")
    for reach in ("/api/preferences", "savePreferences", "useApi"):
        assert reach not in module, (
            f"web/src/i18n/index.tsx mentions {reach}. The page's language selector must "
            "not reach the settings; see the note at the head of that file."
        )

    # And from the other side: saving the settings must not change this page.
    settings = (SRC / "sections" / "Preferences.tsx").read_text(encoding="utf-8")
    assert "setLanguage" not in settings, (
        "web/src/sections/Preferences.tsx calls setLanguage. Saving the content language "
        "must not change the language of this page either."
    )


def test_relative_times_are_not_written_down() -> None:
    """Intl already says "5 minuti fa" in every language, plurals included."""
    module = (CATALOGS / "index.tsx").read_text(encoding="utf-8")
    assert "Intl.RelativeTimeFormat" in module, "relative times no longer come from Intl"
    for language, table in catalogs().items():
        stale = sorted(
            key
            for key, text in table.items()
            if re.search(r"(?i)\b(minuti fa|ore fa|minutes ago|hours ago)\b", str(text))
        )
        assert not stale, f"{language} writes relative times by hand: {stale}"
