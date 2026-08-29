"""The households a research run devises for. Invented, and obviously so.

Six, chosen to move the axes that actually change what comes back: what the parent named
as a starting point, what they asked to keep away from, how much an afternoon may hold at
once, how far it should travel from the last ones, how much paper, and whether there is a
standing note about the season.

No names, no ages, nothing about a person. That is not caution about a fixture — it is that
the real prompt has nowhere to put any of it, so a fixture with a name in it would be
testing a path that does not exist.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True, slots=True)
class Household:
    """One synthetic household's settings, in the shape `panel/preferences.py` holds."""

    name: str
    interests: tuple[str, ...] = ()
    avoid: tuple[str, ...] = ()
    difficulty: str = "gentle"
    variety: str = "balanced"
    language: str = "Italian"
    sheets: int = 2
    note: str = ""
    guidelines: tuple[str, ...] = ()


HOUSEHOLDS: tuple[Household, ...] = (
    Household(
        name="poco-e-vicino",
        interests=("i treni", "le mappe vecchie"),
        avoid=("i ragni",),
        difficulty="gentle",
        variety="familiar",
        sheets=1,
    ),
    Household(
        name="due-fogli-e-una-svolta",
        interests=("la cucina", "le cose che si rompono"),
        avoid=("la guerra",),
        difficulty="steady",
        variety="balanced",
        sheets=2,
    ),
    Household(
        name="lontano-e-lungo",
        interests=("il mare", "gli strumenti musicali", "gli orologi"),
        avoid=(),
        difficulty="stretch",
        variety="frequent",
        sheets=3,
    ),
    Household(
        name="un-mese-pesante",
        interests=("i gatti", "il disegno"),
        avoid=("la scuola",),
        difficulty="gentle",
        variety="balanced",
        sheets=1,
        note="mese pienissimo di scuola, e in casa si dorme poco",
    ),
    Household(
        name="niente-di-scritto",
        difficulty="steady",
        variety="balanced",
        sheets=2,
    ),
    Household(
        name="con-dei-limiti",
        interests=("le piante", "le costruzioni"),
        avoid=("i numeri",),
        difficulty="steady",
        variety="frequent",
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
