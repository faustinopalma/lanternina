"""The manual, and the three ways serving it could go wrong quietly.

Two of these are about the corpus and one is about the image it has to arrive in. The last
matters most: `methods/` is not inside any installed package, so the only thing standing
between a working deployment and afternoons devised without craft is a line in the
Dockerfile. Nothing else in the repository would notice it missing — the panel would start,
the route would register, and every afternoon would quietly be the worse for it.
"""

from __future__ import annotations

import json
import os
import random
from pathlib import Path

from shared.capabilities import HouseCapability
from shared.methods import Method, draw, load, runnable, where_they_are

EVERYTHING = frozenset(
    {
        HouseCapability.PRINT_A4,
        HouseCapability.SCAN_A4,
        HouseCapability.SHOW_800X480_1BIT,
    }
)


def a_method(**over: object) -> Method:
    said: dict[str, object] = {
        "method_id": "a-thing",
        "kind": "form",
        "name": "a thing somebody does",
        "one_line": "one line about it",
        "how": "how one is built",
        "knobs": (("a knob", "what it does"),),
        "where_the_work_is": "in the sheet",
        "breaks": "",
        "adult_cost": "none",
        "verification": "in_the_sheet",
        "comes_back": "a_sheet",
        "people": 1,
        "letters_inside_words": "no",
    }
    said.update(over)
    return Method(**said)  # type: ignore[arg-type]


def test_the_corpus_reads() -> None:
    """The records on disk are the ones `tools/methods_check.py` accepts, so this asserts a
    floor rather than the count: a number here would fail every time one is written."""
    corpus = load()

    assert len(corpus) > 150
    assert all(one.name for one in corpus)
    assert len({one.method_id for one in corpus}) == len(corpus)


def test_a_house_is_never_handed_a_form_it_cannot_run() -> None:
    """The whole reason selection is code rather than similarity: this is assertable.

    Each clause is checked against a record that fails only that clause, so a filter
    deleted from `runnable` fails here rather than reaching a house.
    """
    only_a_screen = frozenset({HouseCapability.SHOW_800X480_1BIT})
    refused = (
        a_method(letters_inside_words="to_compose"),
        a_method(letters_inside_words="to_solve"),
        a_method(people=2),
        a_method(adult_cost="take_part"),
        a_method(verification="needs_a_person", adult_cost="none"),
    )
    for one in refused:
        assert runnable([one], capabilities=EVERYTHING) == ()

    on_paper = a_method(comes_back="a_sheet")
    assert runnable([on_paper], capabilities=only_a_screen) == ()
    assert runnable([on_paper], capabilities=EVERYTHING) == (on_paper,)

    photographed = a_method(comes_back="a_photograph")
    assert runnable([photographed], capabilities=EVERYTHING) == ()


def test_an_adult_who_takes_part_opens_what_needs_one() -> None:
    """A property, not a cut: `ideas/11 §4` says deleting these decides for every house."""
    helped = a_method(adult_cost="take_part", verification="needs_a_person")

    assert runnable([helped], capabilities=EVERYTHING) == ()
    assert runnable([helped], capabilities=EVERYTHING, an_adult_takes_part=True) == (helped,)


def test_the_draw_gives_one_form_and_one_move() -> None:
    form, move = draw(runnable(load(), capabilities=EVERYTHING), rand=random.Random(0))

    assert form is not None and not form.is_a_move
    assert move is not None and move.is_a_move


def test_a_draw_from_an_empty_corpus_is_two_absences_and_not_a_crash() -> None:
    """A container built without `methods/` devises afternoons with no method block."""
    assert draw(()) == (None, None)


def test_a_record_written_for_the_prompt_carries_the_craft() -> None:
    """The knobs are the half that teaches, so a serving without their effects is a name."""
    one = a_method(breaks="it breaks here")
    said = one.written()

    assert one.name in said
    assert "how one is built" in said
    assert "a knob" in said and "what it does" in said
    assert "it breaks here" in said


def test_a_broken_record_is_skipped_and_the_rest_still_load(tmp_path: Path) -> None:
    """`tools/methods_check.py` is where a malformed record is meant to fail, loudly and
    before it is committed. Here it may not take the corpus down with it."""
    (tmp_path / "broken.json").write_text("{not json", encoding="utf-8")
    (tmp_path / "half.json").write_text(json.dumps({"method_id": "x"}), encoding="utf-8")
    whole = json.loads(next(iter(_the_real_corpus())).read_text(encoding="utf-8"))
    (tmp_path / "whole.json").write_text(json.dumps(whole), encoding="utf-8")

    load.cache_clear()
    try:
        os.environ["LANTERNINA_METHODS_DIR"] = str(tmp_path)
        assert len(load()) == 1
    finally:
        os.environ.pop("LANTERNINA_METHODS_DIR", None)
        load.cache_clear()


def _the_real_corpus() -> list[Path]:
    for root in where_they_are():
        found = sorted(root.glob("*.json")) if root.is_dir() else []
        if found:
            return found
    raise AssertionError("no corpus on disk to take a record from")


def test_the_image_carries_the_corpus() -> None:
    """The packaging trap, and the only thing that would catch it before production.

    `methods/` is outside every installed package, and `shared/methods.py` finds it one step
    up from itself — which is `/app/methods` in the image only because the Dockerfile puts it
    there. Deleting that line breaks no import and no test but this one.
    """
    dockerfile = (Path(__file__).resolve().parent.parent / "Dockerfile").read_text(
        encoding="utf-8"
    )

    assert "COPY methods/" in dockerfile
