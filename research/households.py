"""The households a research run devises for. Invented, and obviously so.

Six, chosen to move the axes that actually change what comes back: what the parent named
as a starting point, what they asked to keep away from, where the house sits on the three
pitch axes, how much paper, and whether there is a standing note about the season.

No names, no ages, nothing about a person. That is not caution about a fixture — it is that
the real prompt has nowhere to put any of it, so a fixture with a name in it would be
testing a path that does not exist.

The three bands were two settings a parent chose, ``difficulty`` and ``variety``, until
4 September 2026. ``variety`` reaches no prompt at all now, so it is gone rather than kept
as a field nothing reads; ``difficulty`` became :attr:`shared.profile.Axis.LOAD`, and the
other two axes came with it.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any, Final

from panel.what_happened import as_material, how_it_has_gone, the_ground
from shared.capabilities import HouseCapability
from shared.experience import Drawn, ExperienceError
from shared.profile import Axis, Band, Profile


@dataclass(frozen=True, slots=True)
class Household:
    """One synthetic household's settings, in the shape `panel/preferences.py` holds."""

    name: str
    interests: tuple[str, ...] = ()
    avoid: tuple[str, ...] = ()
    #: Where this house sits on each axis: ``low``, ``middle``, ``high``, or empty for an
    #: axis with too little behind it to say anything about.
    load: str = ""
    ink: str = ""
    span: str = ""
    language: str = "Italian"
    sheets: int = 2
    note: str = ""
    guidelines: tuple[str, ...] = ()

    def pitch(self) -> str:
        """The sentences the prompt is handed, built the way a real house's are.

        Through :class:`shared.profile.Profile` rather than by writing the sentences here,
        so that a run exercises the text the product sends and not a copy of it.
        """
        where = {
            axis: Band(said)
            for axis, said in (
                (Axis.LOAD, self.load),
                (Axis.INK, self.ink),
                (Axis.SPAN, self.span),
            )
            if said
        }
        return Profile(where=where).as_material()


HOUSEHOLDS: tuple[Household, ...] = (
    Household(
        name="poco-e-vicino",
        interests=("i treni", "le mappe vecchie"),
        avoid=("i ragni",),
        load="low",
        ink="low",
        span="low",
        sheets=1,
    ),
    Household(
        name="due-fogli-e-una-svolta",
        interests=("la cucina", "le cose che si rompono"),
        avoid=("la guerra",),
        load="middle",
        ink="middle",
        span="middle",
        sheets=2,
    ),
    Household(
        name="lontano-e-lungo",
        interests=("il mare", "gli strumenti musicali", "gli orologi"),
        avoid=(),
        load="high",
        ink="high",
        span="high",
        sheets=3,
    ),
    # Two axes and not three: an axis with too little behind it says nothing, and a house
    # that is partly known is the ordinary case rather than the exception.
    Household(
        name="un-mese-pesante",
        interests=("i gatti", "il disegno"),
        avoid=("la scuola",),
        load="low",
        span="low",
        sheets=1,
        note="mese pienissimo di scuola, e in casa si dorme poco",
    ),
    # Nothing known at all: no interests and no pitch. This is the prompt as it stood for
    # the whole of August, and the one every house gets on its first afternoon.
    Household(
        name="niente-di-scritto",
        sheets=2,
    ),
    Household(
        name="con-dei-limiti",
        interests=("le piante", "le costruzioni"),
        avoid=("i numeri",),
        load="middle",
        ink="high",
        sheets=2,
        guidelines=(
            "non deve uscire di casa",
            "niente forbici o lame",
        ),
    ),
)


@dataclass(frozen=True, slots=True)
class Memory:
    """What one synthetic household has been through, in this run only.

    A run starts every household empty and fills this as it goes, so the second and third
    iterations exercise `panel/what_happened.py` rather than only the first-afternoon path.
    """

    offered: list[list[str]] = field(default_factory=list)
    ran: list[object] = field(default_factory=list)


# What every synthetic house can do. The same three the real houses declare.
CAN: Final = frozenset(
    {
        HouseCapability("print_a4"),
        HouseCapability("scan_a4"),
        HouseCapability("show_800x480_1bit"),
    }
)

# How many afternoons back the drawn dimensions are quoted from. `panel/what_happened.py`
# holds the same number for the rows; this is the one the deviser is told not to repeat.
RECENT_DRAWN: Final = 5


def _drawn(memory: Memory) -> tuple[Drawn, ...]:
    """The dimensions of the last few afternoons, skipping any that cannot be read."""
    out: list[Drawn] = []
    for one in memory.ran[-RECENT_DRAWN:]:
        try:
            out.append(Drawn.from_dict(getattr(one, "drawn", None)))
        except (ExperienceError, AttributeError):
            continue
    return tuple(out)


def arguments(house: Household, memory: Memory) -> dict[str, Any]:
    """Everything that decides one afternoon for this house, as one dictionary.

    One place, because there are two callers and they must not drift: `research/run.py`
    sends it to `panel.devising.devise_experience`, and the workbench notebook sends the
    same dictionary to `agents.experience_deviser.the_prompt` to read what would go out
    before paying for it. A second copy of this list is what broke the loop in September —
    ``difficulty`` and ``variety`` went on being passed for two days after the deviser
    stopped taking them.

    ``now`` and ``built_from`` are not in it: one is the clock and the other is a sink the
    caller owns.
    """
    ran = list(memory.ran)
    going = how_it_has_gone(ran)  # type: ignore[arg-type]
    ground = the_ground(memory.offered)
    return {
        "capabilities": CAN,
        "language": house.language,
        "interests": house.interests,
        "avoid": house.avoid,
        "pitch": house.pitch(),
        "sheets": house.sheets,
        "note": house.note,
        "already": tuple(one.title for one in ran if getattr(one, "title", "")),  # type: ignore[attr-defined]
        "recent": _drawn(memory),
        "happened": as_material(ran),  # type: ignore[arg-type]
        "counts": json.dumps(going.to_dict(), ensure_ascii=False),
        "direction": going.direction(),
        "ground": json.dumps(ground.to_dict(), ensure_ascii=False) if ground.anything() else "",
    }
