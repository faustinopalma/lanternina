"""What a house can do, named once so that a designed experience can ask for it.

``panel/devices.py`` holds the same list from the other side: one row per object in the
house, with the job the parent gave it. This module is that list seen from the direction
of the experience. It does not name the Epson in the hall; it names "somewhere to put A4
on paper", because an experience designed for every house cannot know which machine is in
this one.

The names are deliberately concrete. ``SHOW_800X480_1BIT`` says the size and the depth
rather than saying "a display", and that costs a new name the day a second panel size
arrives. It buys the thing that matters more: a house whose display cannot show that image
does not claim it can, so an experience is never offered and then found unrunnable in
front of the person who was going to do it.

Nothing here is about a person. A capability is a property of the house — what equipment
is present and what job the parent gave it — and it stays true when nobody is home.
"""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from enum import StrEnum
from typing import Final, Protocol


class HouseCapability(StrEnum):
    """One thing a house can do. The list is closed, and grows by a person adding a name."""

    PRINT_A4 = "print_a4"
    SHOW_800X480_1BIT = "show_800x480_1bit"
    SCAN_A4 = "scan_a4"
    # Named, and not yet reachable: no verb asks for it, so no blueprint can require it
    # today. It is here so that the capture station has a name waiting when the verb is
    # written, and so that the name is agreed before an agent gets to invent one.
    PHOTOGRAPH_TABLE = "photograph_table"


# The kinds and jobs as ``panel/devices.py`` spells them. Repeated rather than imported:
# `shared` is what every other package imports, and it imports none of them back.
# ``tests/test_capabilities.py`` fails if the two spellings ever drift apart.
KIND_DISPLAY: Final = "display"
KIND_PRINTER: Final = "printer"
KIND_SCANNER: Final = "scanner"

JOB_PICTURE: Final = "picture"
JOB_SHEET: Final = "sheet"
JOB_PRINT: Final = "print"
JOB_SCAN: Final = "scan"

# A display given the picture job is absent from this table on purpose. It can draw the
# same 800x480 image, but it is the frame on the wall: handing it to an experience would
# take the pictures away for as long as the experience runs, which is the failure found on
# 19 August 2026 when one button press converted the picture display into the sheet one.
# The cost is that a house with a single display must choose a job before it can be
# offered anything, and choosing is the parent's to do.
_PROVIDED_BY: Final[Mapping[tuple[str, str], HouseCapability]] = {
    (KIND_PRINTER, JOB_PRINT): HouseCapability.PRINT_A4,
    (KIND_SCANNER, JOB_SCAN): HouseCapability.SCAN_A4,
    (KIND_DISPLAY, JOB_SHEET): HouseCapability.SHOW_800X480_1BIT,
}


class Assigned(Protocol):
    """A row of the household inventory: something with a kind and a job."""

    @property
    def kind(self) -> str: ...

    @property
    def job(self) -> str: ...


def provided_by(kind: str, job: str) -> HouseCapability | None:
    """What one object contributes, or ``None`` if it has no job or the job is unknown."""
    return _PROVIDED_BY.get((kind, job))


def capabilities_of(things: Iterable[Assigned]) -> frozenset[HouseCapability]:
    """What this house can do, from what is in it and what the parent decided it is for.

    A thing that is present but silent still counts. Whether a printer answered this
    morning is a question about now; this answers what the house is equipped to do, and
    conflating the two would make a catalogue flicker with the network.
    """
    found = (provided_by(thing.kind, thing.job) for thing in things)
    return frozenset(capability for capability in found if capability is not None)
