"""What a house can do, named once so that a designed experience can ask for it.

``panel/devices.py`` holds the same list from the other side: one row per object in the
house, with the job the parent gave it. This module is that list seen from the direction
of the experience. It does not name the Epson in the hall; it names "somewhere to put A4
on paper", because an experience designed for every house cannot know which machine is in
this one.

The words for the kinds and the jobs live here too, and only here. The panel and the hub
import them; the browser cannot, so `tests/test_web_i18n.py` fails if a job has no word a
parent can read.

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
from dataclasses import dataclass
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


class Act(StrEnum):
    """The verb an experience writes down. One per hand, and no others.

    Lives here rather than beside the document format because an act and the equipment it
    needs are the same fact said twice, and they used to be written in two files.
    """

    SAY = "say"
    HAND_OVER = "hand_over"
    COLLECT = "collect"
    CLOSE = "close"


# Not an act, and here for the same reason the acts are: it is a word both sides of the
# wire have to spell the same way. A house files it when something it was told to do did
# not happen — the printer took no page, the panel was not there — and `panel/trail.py`
# keeps it beside the acts so a parent reading an afternoon sees where it diverged.
WENT_WRONG: Final = "fault"



# The kinds and the jobs, written once. `shared` is what every other package imports and
# it imports none of them back, so this is the only direction the vocabulary can live in:
# `panel/devices.py` and `devices/inventory.py` read it from here. Until 19 August 2026 all
# three spelled it out separately and a test compared the spellings, which caught drift and
# did nothing about the cost of adding a job.
KIND_DISPLAY: Final = "display"
KIND_PRINTER: Final = "printer"
KIND_SCANNER: Final = "scanner"
KINDS: Final = (KIND_DISPLAY, KIND_PRINTER, KIND_SCANNER)

# No job at all, which is not the same as never having been named — see `panel/devices.py`.
JOB_NONE: Final = ""
JOB_PICTURE: Final = "picture"
JOB_SHEET: Final = "sheet"
JOB_REMIND: Final = "remind"
JOB_PRINT: Final = "print"
JOB_SCAN: Final = "scan"

# The jobs the parent can hand out, by kind. A thing holds as many as the parent gives it,
# and a job may be held by several things at once: a house with two displays and three
# things to show cannot work any other way, and when more than one thing can do something
# the house picks between them, which is where the variation comes from.
JOBS_BY_KIND: Final[Mapping[str, tuple[str, ...]]] = {
    KIND_DISPLAY: (JOB_PICTURE, JOB_SHEET, JOB_REMIND),
    KIND_PRINTER: (JOB_PRINT,),
    KIND_SCANNER: (JOB_SCAN,),
}

# A display given only the picture job is absent from this table on purpose. It can draw
# the same 800x480 image, but it is the frame on the wall: handing it to an experience
# would take the pictures away for as long as the experience runs, which is the failure
# found on 19 August 2026 when one button press converted the picture display into the
# sheet one. A parent who wants one display to do both says so by giving it both jobs,
# which is a sentence the panel can now write. The reminder job is absent for the same
# reason and one more: a reminder appears at an hour the household chose, so a display
# lent to an experience would either lose the reminder or interrupt the experience.
#
# The table is not written out any more. It is derived from `HANDS` below, which is the
# only place a device is described, so a job that provides a capability and a verb that
# asks for one cannot disagree.


@dataclass(frozen=True, slots=True)
class Hand:
    """One thing the house can be asked to do, and the equipment that does it.

    This is the half of a device that has to be said in words: the verb an experience
    writes, the capability it needs, which object in the house carries it, and the
    sentence the deviser is given so it knows the verb exists. How a hand actually moves
    is the other half and lives in :mod:`devices.hands`, because a house is not something
    ``shared`` is allowed to know about.

    The split is the point. Adding a device is adding one entry here and one function
    there; nothing else in the repository is edited, because everything else — what a
    house can do, which job provides it, what dispatches the verb, and what the deviser is
    told — is read off this table.
    """

    act: Act
    needs: HouseCapability
    kind: str
    job: str
    # One line, addressed to whoever is writing an afternoon. Plain, and about the room.
    describe: str


HANDS: Final[tuple[Hand, ...]] = (
    Hand(
        act=Act.SAY,
        needs=HouseCapability.SHOW_800X480_1BIT,
        kind=KIND_DISPLAY,
        job=JOB_SHEET,
        describe="puts words on the display and waits for however long they take to read",
    ),
    Hand(
        act=Act.HAND_OVER,
        needs=HouseCapability.PRINT_A4,
        kind=KIND_PRINTER,
        job=JOB_PRINT,
        describe="prints one page and leaves it where it can be picked up",
    ),
    Hand(
        act=Act.COLLECT,
        needs=HouseCapability.SCAN_A4,
        kind=KIND_SCANNER,
        job=JOB_SCAN,
        describe="takes a page back and reads what was added to it",
    ),
    Hand(
        act=Act.CLOSE,
        needs=HouseCapability.SHOW_800X480_1BIT,
        kind=KIND_DISPLAY,
        job=JOB_SHEET,
        describe="ends the afternoon on the display, from wherever it got to",
    ),
)

# What each act needs the house to be able to do. The document does not get to say: a
# moment that puts paper on the table needs a printer whatever its author wrote.
NEEDS: Final[Mapping[Act, HouseCapability]] = {hand.act: hand.needs for hand in HANDS}

# Two acts share the display, so this is smaller than HANDS and that is not a mistake.
_PROVIDED_BY: Final[Mapping[tuple[str, str], HouseCapability]] = {
    (hand.kind, hand.job): hand.needs for hand in HANDS
}

# Every capability an experience can ask for, which is the set a pretend house claims.
REACHABLE: Final[frozenset[HouseCapability]] = frozenset(NEEDS.values())



class Assigned(Protocol):
    """A row of the household inventory: something with a kind and the jobs it was given."""

    @property
    def kind(self) -> str: ...

    @property
    def jobs(self) -> tuple[str, ...]: ...


def provided_by(kind: str, job: str) -> HouseCapability | None:
    """What one object contributes, or ``None`` if it has no job or the job is unknown."""
    return _PROVIDED_BY.get((kind, job))


def capabilities_of(things: Iterable[Assigned]) -> frozenset[HouseCapability]:
    """What this house can do, from what is in it and what the parent decided it is for.

    A thing that is present but silent still counts. Whether a printer answered this
    morning is a question about now; this answers what the house is equipped to do, and
    conflating the two would make a catalogue flicker with the network.
    """
    found = (provided_by(thing.kind, job) for thing in things for job in thing.jobs)
    return frozenset(capability for capability in found if capability is not None)
