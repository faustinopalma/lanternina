"""The loader that puts prompt text outside Python, and the promises it makes.

Three of them matter. A name that has no file must say so loudly rather than send a model an
empty string. A `<!-- -->` comment must never reach a model — the files carry the record of
what was measured and why a sentence is worded the way it is, and none of that is an
instruction. And a placeholder left unfilled must raise, because a prompt reading
`at most $max_moments moments` is worse than one that never got sent.
"""

from __future__ import annotations

import pytest

from shared.prompts import beside


def test_a_name_with_no_file_says_what_there_is(tmp_path) -> None:
    (tmp_path / "thing.one.md").write_text("first\n", encoding="utf-8")
    (tmp_path / "thing.two.md").write_text("second\n", encoding="utf-8")
    says = beside(str(tmp_path / "thing.py"))

    with pytest.raises(FileNotFoundError) as raised:
        says.text("three")

    said = str(raised.value)
    assert "one" in said and "two" in said


def test_a_comment_never_reaches_the_model(tmp_path) -> None:
    (tmp_path / "thing.block.md").write_text(
        "<!--\nwhy this is worded this way, measured 24 August 2026\n-->\nWhat is said.\n",
        encoding="utf-8",
    )
    says = beside(str(tmp_path / "thing.py"))

    assert says.text("block") == "What is said.\n"


def test_a_placeholder_left_unfilled_raises(tmp_path) -> None:
    (tmp_path / "thing.block.md").write_text("at most $how_many.\n", encoding="utf-8")
    says = beside(str(tmp_path / "thing.py"))

    with pytest.raises(KeyError):
        says.text("block", something_else=3)


def test_json_braces_survive_a_fill(tmp_path) -> None:
    """The reason for `$name` and not `{name}`: the prompts are full of literal braces."""
    (tmp_path / "thing.block.md").write_text(
        '{"moments": [ ... ]}, at most $how_many\n', encoding="utf-8"
    )
    says = beside(str(tmp_path / "thing.py"))

    assert says.text("block", how_many=6) == '{"moments": [ ... ]}, at most 6\n'


def test_every_live_prompt_loads() -> None:
    """Importing the agents resolves every name and every placeholder, or raises."""
    from agents import (  # noqa: F401
        experience_continuer,
        experience_deviser,
        page_maker,
        page_reader,
        reminder_reader,
        reminder_wording,
    )
    from panel import painting  # noqa: F401

    assert experience_deviser._INSTRUCTION.strip()
    assert "$" not in experience_deviser._INSTRUCTION
    assert "<!--" not in experience_deviser._INSTRUCTION
