"""How a thing is drawn, drawn at random and written down.

Noticed by the parent on 24 August 2026, on the pictures: ask for the same theme twice and
the second picture is the first one again. The cause is not the model being unimaginative —
it is that the prompt was a pure function of the theme, so the same words went up both times
and the same drawing came back.

The fix is the one `shared/experience.Drawn` already makes for afternoons: **vary something,
and write down what was varied**, so that variety is a thing that can be looked at rather
than hoped for. Four dimensions of a few phrases each is about thirteen hundred combinations,
which is more than a house will see.

**A manner changes how something is drawn and never what it says.** That is the line that
lets this be applied to a page as well as to a picture: the words on the paper are decided by
the afternoon and screened before they get here, and nothing in this file can touch them.
"""

from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Any, Final

# Four dimensions rather than one long list, because a single list of adjectives collapses:
# a model reads three of them as one mood and draws the mood. These pull in different
# directions — the tool, the distance, the light and the temper of the line.
DRAWN_WITH: Final[tuple[str, ...]] = (
    "a fine dip pen",
    "a soft pencil",
    "a broad felt tip",
    "an etching needle",
    "a brush and ink",
    "a technical pen with an even line",
)

SEEN_FROM: Final[tuple[str, ...]] = (
    "close up, so that one part fills the paper",
    "from a little way off, with room around it",
    "from above, looking down",
    "from below, looking up",
    "from one side, in profile",
)

THE_LIGHT: Final[tuple[str, ...]] = (
    "flat daylight with no shadow",
    "late afternoon light coming from one side",
    "the light of a bright overcast day",
    "lamplight from close by",
)

THE_LINE: Final[tuple[str, ...]] = (
    "confident and unhurried",
    "quick and a little rough, as if drawn from life",
    "patient and exact, like a naturalist's plate",
    "sparse, leaving most of the paper alone",
    "decorative, with small repeated marks",
)

DIMENSIONS: Final[tuple[str, ...]] = ("drawn_with", "seen_from", "the_light", "the_line")


@dataclass(frozen=True, slots=True)
class Manner:
    """One way of drawing, in four short phrases. Recorded so it can be told apart."""

    drawn_with: str
    seen_from: str
    the_light: str
    the_line: str

    def as_sentence(self) -> str:
        """The manner as it goes into a prompt, after whatever the picture is of."""
        return (
            f"Drawn with {self.drawn_with}, seen {self.seen_from}, in {self.the_light}. "
            f"The line is {self.the_line}."
        )

    def to_dict(self) -> dict[str, Any]:
        return {name: getattr(self, name) for name in DIMENSIONS}

    def as_tuple(self) -> tuple[str, ...]:
        return tuple(getattr(self, name) for name in DIMENSIONS)


def a_manner(choose: random.Random | None = None) -> Manner:
    """One at random. Passing a seeded ``Random`` makes a test repeatable."""
    pick = choose or random.SystemRandom()
    return Manner(
        drawn_with=pick.choice(DRAWN_WITH),
        seen_from=pick.choice(SEEN_FROM),
        the_light=pick.choice(THE_LIGHT),
        the_line=pick.choice(THE_LINE),
    )


def how_many() -> int:
    """The combinations there are, for a test that says whether the space is big enough."""
    return len(DRAWN_WITH) * len(SEEN_FROM) * len(THE_LIGHT) * len(THE_LINE)
