"""The panel's translation catalogs.

Adding a language is meant to be adding one object to `CATALOGS` and nothing else. That
claim only holds if two things stay true, and both fail silently in a browser: every
catalog has to carry the same keys, and every key the panel asks for has to exist. A missing
string shows the key itself to a parent, which is exactly the kind of fault nobody reports.

These tests read the shipped files rather than a copy, so they break when the panel drifts.
"""

from __future__ import annotations

import re
from pathlib import Path

WEB = Path(__file__).resolve().parent.parent / "web"

# A catalog entry: two spaces of indent inside `strings: {`, a quoted key, a quoted value.
ENTRY = re.compile(r'^\s{6}"([\w.]+)":', re.MULTILINE)
LANGUAGE = re.compile(r'^  (\w+): \{$', re.MULTILINE)
USED_IN_JS = re.compile(r'\bt\(\s*"([\w.]+)"')
# The three attribute forms i18n.js knows how to fill.
USED_IN_HTML = re.compile(r'data-i18n(?:-placeholder|-label)?="([\w.]+)"')
# Built at runtime from a value, so the literal key never appears in the source.
COMPUTED_PREFIXES = ("kind.", "level.")


def catalogs() -> dict[str, set[str]]:
    source = (WEB / "i18n.js").read_text(encoding="utf-8")
    head, _, tail = source.partition("const CATALOGS = {")
    assert tail, "i18n.js no longer declares CATALOGS"
    blocks = LANGUAGE.split(tail)
    # split() gives [before, name, body, name, body, ...]
    found: dict[str, set[str]] = {}
    for index in range(1, len(blocks) - 1, 2):
        found[blocks[index]] = set(ENTRY.findall(blocks[index + 1]))
    return found


def test_every_catalog_carries_the_same_keys() -> None:
    found = catalogs()
    assert len(found) >= 2, f"expected at least two languages, found {sorted(found)}"
    reference = sorted(found)[0]
    for language, keys in found.items():
        missing = found[reference] - keys
        extra = keys - found[reference]
        assert not missing, f"{language} is missing {sorted(missing)}"
        assert not extra, f"{language} has keys no other catalog has: {sorted(extra)}"


def test_no_catalog_is_empty() -> None:
    for language, keys in catalogs().items():
        assert len(keys) > 20, f"{language} looks truncated: {len(keys)} keys"


def used_keys() -> set[str]:
    keys = set(USED_IN_JS.findall((WEB / "app.js").read_text(encoding="utf-8")))
    keys |= set(USED_IN_HTML.findall((WEB / "index.html").read_text(encoding="utf-8")))
    return keys


def test_every_key_the_panel_asks_for_exists() -> None:
    known = set().union(*catalogs().values())
    unknown = {key for key in used_keys() if key not in known}
    assert not unknown, f"the panel asks for keys no catalog has: {sorted(unknown)}"


def test_the_computed_keys_are_all_present() -> None:
    """`kind.*` and `level.*` are built from a value, so nothing else would catch a gap."""
    known = set().union(*catalogs().values())
    app = (WEB / "app.js").read_text(encoding="utf-8")
    for prefix in COMPUTED_PREFIXES:
        listed = re.search(rf'KNOWN_{prefix[:-1].upper()}S = \[([^\]]+)\]', app)
        assert listed, f"app.js no longer lists the {prefix} values"
        for value in re.findall(r'"(\w+)"', listed.group(1)):
            assert f"{prefix}{value}" in known, f"no catalog entry for {prefix}{value}"


def test_the_panel_keeps_no_italian_sentences() -> None:
    """The words live in the catalogs. A sentence left in the code cannot be translated."""
    marker = re.compile(
        r'(?i)(?<![\w-])(perch\u00e9|gi\u00e0|della|delle|questo|questa|sono|viene|'
        r'nessun\w*|caricando|riesco|riprova)(?![\w-])'
    )
    for name in ("app.js", "index.html"):
        text = (WEB / name).read_text(encoding="utf-8")
        found = sorted({match.group(0) for match in marker.finditer(text)})
        assert not found, f"{name} still holds Italian words: {found}"


def test_the_translation_module_keeps_its_names_to_itself() -> None:
    """i18n.js and app.js are classic scripts sharing one global scope.

    Measured on 17 August 2026: a bare `function t()` in i18n.js collided with
    `const { t } = ...` in app.js, and the resulting SyntaxError stopped app.js from running
    at all — the page rendered its words and then did nothing, which reads like a network
    problem rather than a syntax one. The wrapper is what prevents it; only the exported
    object is allowed out.
    """
    source = (WEB / "i18n.js").read_text(encoding="utf-8").strip()
    assert "(function () {" in source, "i18n.js no longer wraps its declarations"
    assert source.endswith("})();"), "i18n.js no longer closes its wrapper"

    exported = set(
        re.findall(
            r'const \{([^}]+)\} = window\.LanterninaI18n',
            (WEB / "app.js").read_text(encoding="utf-8"),
        )
    )
    assert exported, "app.js no longer takes its names from the exported object"


def test_the_panel_touches_only_the_exported_object() -> None:
    """One global, so the two files cannot collide again through a second one."""
    source = (WEB / "i18n.js").read_text(encoding="utf-8")
    globals_assigned = set(re.findall(r'^\s*window\.(\w+)\s*=', source, re.MULTILINE))
    assert globals_assigned == {"LanterninaI18n"}, f"i18n.js sets {sorted(globals_assigned)}"
