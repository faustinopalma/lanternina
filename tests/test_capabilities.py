"""The capability vocabulary, and the agreement it has with the parent's inventory.

The two lists are written twice on purpose — `shared` is imported by `panel` and imports
nothing back — so the thing worth testing is that they still say the same words.
"""

from __future__ import annotations

from dataclasses import replace

import pytest

from panel import devices
from shared.capabilities import HouseCapability, capabilities_of, provided_by


def test_the_two_sides_spell_the_kinds_and_jobs_the_same() -> None:
    from shared import capabilities

    assert capabilities.KIND_DISPLAY == devices.KIND_DISPLAY
    assert capabilities.KIND_PRINTER == devices.KIND_PRINTER
    assert capabilities.KIND_SCANNER == devices.KIND_SCANNER
    assert capabilities.JOB_PICTURE == devices.JOB_PICTURE
    assert capabilities.JOB_SHEET == devices.JOB_SHEET
    assert capabilities.JOB_PRINT == devices.JOB_PRINT
    assert capabilities.JOB_SCAN == devices.JOB_SCAN


def test_every_job_the_parent_can_hand_out_is_accounted_for() -> None:
    """A job the panel offers and this module has never heard of would be a silent hole:
    the parent would assign it and the catalogue would go on saying the house cannot."""
    for kind, jobs in devices.JOBS_BY_KIND.items():
        for job in jobs:
            assert provided_by(kind, job) is not None or (kind, job) == (
                devices.KIND_DISPLAY,
                devices.JOB_PICTURE,
            ), f"{kind}/{job} maps to no capability and is not the deliberate exception"


def test_an_unassigned_thing_contributes_nothing() -> None:
    assert provided_by(devices.KIND_PRINTER, devices.JOB_NONE) is None


def test_the_picture_display_is_not_offered_to_an_experience() -> None:
    """It can draw the image. Handing it over would take the pictures off the wall."""
    assert provided_by(devices.KIND_DISPLAY, devices.JOB_PICTURE) is None


@pytest.mark.parametrize(
    ("rows", "expected"),
    [
        ([], frozenset()),
        (
            [("printer", "print"), ("scanner", "scan")],
            frozenset({HouseCapability.PRINT_A4, HouseCapability.SCAN_A4}),
        ),
        (
            [("display", "sheet"), ("display", "picture")],
            frozenset({HouseCapability.SHOW_800X480_1BIT}),
        ),
    ],
)
def test_what_a_house_can_do(rows: list[tuple[str, str]], expected: frozenset) -> None:
    things = [
        devices.Thing(id=f"t{n}", household_id="hh", kind=kind, jobs=(job,))
        for n, (kind, job) in enumerate(rows)
    ]
    assert capabilities_of(things) == expected


def test_one_display_given_both_jobs_lends_itself_to_an_experience() -> None:
    """A house with one display had to choose between the pictures and everything else.
    The parent can now say it does both, and saying so is what makes the difference."""
    picture_only = devices.Thing(id="d", household_id="hh", kind="display", jobs=("picture",))
    assert capabilities_of([picture_only]) == frozenset()

    both = replace(picture_only, jobs=("picture", "sheet"))
    assert capabilities_of([both]) == frozenset({HouseCapability.SHOW_800X480_1BIT})


def test_a_silent_thing_still_counts() -> None:
    """Whether the printer answered this morning is a different question."""
    thing = devices.Thing(
        id="p", household_id="hh", kind="printer", jobs=("print",), last_seen=0.0
    )
    assert capabilities_of([thing]) == frozenset({HouseCapability.PRINT_A4})
