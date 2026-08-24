"""The switch, and the promise that turning it off changes nothing about the afternoon.

A simulated house exists so that the loop can be run dozens of times without a person, a
printer and an hour. That is only worth anything if it is the *same* loop: the moment a
runner learns to tell the two apart, there are two ways of running an afternoon and they
drift at whatever speed nobody is watching.

So the branch lives in exactly two places — `devices/house.show` and `devices/house.hand_over`,
where the equipment is — and this file holds that down by reading the source of everything
above them.

`shared/manner.py` is here too, for a different reason: it is the answer to *the same theme
gives the same picture every time*, and what makes it checkable is that a manner is recorded
rather than only applied.
"""

from __future__ import annotations

import random
from pathlib import Path

import pytest

from devices.pretend import PRETEND_DIR_ENV, PRETEND_ENV, WHERE_BY_DEFAULT, pretend_in
from shared.manner import DIMENSIONS, a_manner, how_many

# ── The switch ───────────────────────────────────────────────────────────────────────


def test_nothing_set_is_the_real_house() -> None:
    """The default has to be the one that touches a printer, or a house would quietly
    simulate itself and nobody would see anything come out."""
    assert pretend_in({}) is None


def test_one_word_turns_it_on() -> None:
    assert pretend_in({PRETEND_ENV: "1"}) == Path(WHERE_BY_DEFAULT)
    assert pretend_in({PRETEND_ENV: "true"}) == Path(WHERE_BY_DEFAULT)


@pytest.mark.parametrize("said", ["false", "0", "no", "off", "", "  "])
def test_a_false_word_is_the_real_house_and_reads_like_one(said: str) -> None:
    """`LANTERNINA_PRETEND=false` has to mean what it says. A switch that is only off when
    it is absent is a switch nobody is sure about."""
    assert pretend_in({PRETEND_ENV: said}) is None


def test_a_named_folder_still_works_and_wins() -> None:
    """The older way, kept: it is how two experiments run side by side without colliding."""
    assert pretend_in({PRETEND_DIR_ENV: "somewhere"}) == Path("somewhere")
    assert pretend_in({PRETEND_DIR_ENV: "somewhere", PRETEND_ENV: "1"}) == Path("somewhere")


# ── Turning it off changes nothing about the afternoon ───────────────────────────────

# Everything between an approved document and the equipment. If one of these learns to ask
# whether the house is simulated, the two houses have started to be different systems.
ABOVE_THE_EQUIPMENT = (
    "devices/run_experience.py",
    "devices/afternoon.py",
    "devices/print_page.py",
    "devices/ask_panel.py",
    "printing/paper.py",
    "agents/page_maker.py",
    "agents/page_reader.py",
    "agents/experience_deviser.py",
    "agents/experience_continuer.py",
)


@pytest.mark.parametrize("path", ABOVE_THE_EQUIPMENT)
def test_no_module_above_the_equipment_knows_the_house_is_simulated(path: str) -> None:
    """Read rather than reasoned about: an import of the simulator, or a look at the flag,
    is the shape this failure takes, and both are visible in the text."""
    source = Path(path).read_text(encoding="utf-8")
    code = "\n".join(
        line for line in source.splitlines() if not line.strip().startswith("#")
    )
    assert "LANTERNINA_PRETEND" not in code, f"{path} reads the switch"
    assert "pretend_in" not in code, f"{path} asks whether the house is simulated"


def test_the_branch_is_where_the_equipment_is() -> None:
    """Two places, and they are the two that hold a printer and a display: `show` and
    `hand_over`. Naming the count here means adding a third is a change to this test rather
    than a thing that happens quietly."""
    house = Path("devices/house.py").read_text(encoding="utf-8")

    assert house.count("pretending is not None") == 2


def test_the_runner_plays_a_simulated_afternoon_with_the_same_call() -> None:
    """`carry_on` and `begin` take a house and nothing else. A simulated run reaches them by
    the same door, which is why the simulator can be trusted to be a rehearsal."""
    import inspect

    from devices.run_experience import begin, carry_on

    for one in (begin, carry_on):
        assert list(inspect.signature(one).parameters)[0] == "house"


# ── Why two pictures of the same thing are not the same picture ──────────────────────


def test_a_manner_is_four_phrases_and_all_of_them_are_written_down() -> None:
    """Recorded rather than only applied: variety drawn from a seed cannot be checked, and
    variety written down as four phrases can."""
    drawn = a_manner(random.Random(1))

    assert set(drawn.to_dict()) == set(DIMENSIONS)
    assert all(drawn.to_dict().values())


def test_there_are_more_manners_than_a_house_will_see() -> None:
    """The defect this fixes: the picture prompt was a pure function of the theme, so a
    household with three themes saw the same three pictures for as long as it kept them."""
    assert how_many() >= 500


def test_two_draws_differ_more_often_than_not() -> None:
    """Not a guarantee that two are different — that would need memory of what came before —
    but that the space is wide enough for repetition to be rare."""
    seen = {a_manner(random.Random(seed)).as_tuple() for seed in range(50)}

    assert len(seen) >= 45


def test_the_picture_prompt_carries_the_manner_and_the_theme() -> None:
    from panel.painting import PICTURE_PROMPT

    drawn = a_manner(random.Random(3))
    said = f"{PICTURE_PROMPT.format(theme='gatti che dormono')} {drawn.as_sentence()}"

    assert "gatti che dormono" in said
    assert drawn.drawn_with in said
    assert "No text" in said, "the manner must not push the refusals off the end"


def test_a_manner_says_how_it_is_drawn_and_never_what_it_says() -> None:
    """The line that lets this be applied to a page as well as to a picture. The words on a
    page came through the safety gate; nothing that varies may touch them."""
    from agents.page_maker import asked_for
    from shared.page import Page, PageKind

    page = Page(kind=PageKind.LABEL, title="Nuvola", illustration="one cloud")
    drawn = a_manner(random.Random(7))

    plain = asked_for(page)
    varied = asked_for(page, drawn)

    assert '"Nuvola"' in plain and '"Nuvola"' in varied
    assert drawn.as_sentence() in varied
    assert drawn.as_sentence() not in plain
