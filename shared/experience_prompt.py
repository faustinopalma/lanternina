"""The format, described for a model, generated from the format itself.

Two agents ask a model for moments — :mod:`agents.experience_deviser` writes a whole
afternoon and :mod:`agents.experience_continuer` writes the rest of one — and until format
2 each carried its own copy of the shape. Two copies of a description of one thing is a
thing that drifts, and format 2 roughly tripled what a moment carries, so the drift would
have been expensive rather than annoying.

**Nothing here enforces anything.** :class:`~shared.experience.Experience` refuses what it
cannot read, and this text is only what a model is told so that it has a chance of writing
something that parses. It lives beside the format rather than inside it because a contract
should not have prose about prompting in it, and it is generated from the format's own
constants so that a limit changed in one place cannot go on being described the old way.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Final

from .capabilities import HANDS, Act
from .experience import (
    DIMENSIONS,
    HELP_LEVELS,
    MAX_HEADING,
    MAX_HELP_AFTER,
    MAX_IN_HAND,
    MAX_LINE,
    MAX_LINES,
    MAX_WAY_OUT_MINUTES,
    MAX_WEIGHT_MINUTES,
    MIN_WEIGHT_MINUTES,
)
from .page import (
    MAX_ILLUSTRATION,
    MAX_LABEL,
    MAX_NOTE_LINE,
    MAX_NOTE_LINES,
    MAX_SPACES,
    MAX_TITLE,
    PageKind,
)
from .prompts import beside

SAYS: Final = beside(__file__)

_KINDS: Final = ", ".join(f'"{kind}"' for kind in PageKind)

_LINES: Final = f"a list of at most {MAX_LINES} lines, each at most {MAX_LINE} characters"

THE_SHAPE_OF_A_MOMENT: Final = SAYS.text(
    "the-shape-of-a-moment",
    max_heading=MAX_HEADING,
    help_levels=HELP_LEVELS,
    lines=_LINES,
)

# What each verb looks like written down, and whatever its own keys need saying. The
# sentence about what it does in the room is not here: that is on the hand in
# `shared/capabilities.py`, said once, and this walks the registry to assemble the two. A
# device added there with no shape written here raises at import rather than quietly
# leaving the deviser a verb it was never told about.
_WRITTEN_AS: Final[Mapping[Act, str]] = {
    Act.SAY: '{"act": "say", ...}',
    Act.HAND_OVER: (
        '{"act": "hand_over", ..., "page": {"kind": "...", "title": "<text>", '
        '"note": [ ... ], "spaces": [ ... ], "illustration": "<text>"}, '
        f'"instead": [{_LINES}]}}'
    ),
    Act.COLLECT: (
        '{"act": "collect", ..., "outcomes": ['
        '{"when": "marks", "then": "<a later moment id, or ask>"}, '
        '{"when": "blank", "then": "<a later moment id, or ask>"}], '
        '"if_no_page": "<a later moment id, or ask>"}'
    ),
    Act.CLOSE: '{"act": "close", ...}',
}

# A note under two of the shapes, for the key a reader of the JSON would not guess. Only
# these two have one, so the mapping is by act and not by every act.
_ABOUT_ITS_KEYS: Final[Mapping[Act, str]] = {
    Act.HAND_OVER: SAYS.text("about-hand-over").rstrip("\n"),
    Act.COLLECT: SAYS.text("about-if-no-page").rstrip("\n"),
}


def _the_acts() -> str:
    written = [SAYS.text("the-acts-head")]
    for hand in HANDS:
        shape = _WRITTEN_AS.get(hand.act)
        if shape is None:
            raise KeyError(f"the {hand.act} hand has no written form in this prompt")
        written.append(f"  {shape}\n     It {hand.describe}.\n")
        about = _ABOUT_ITS_KEYS.get(hand.act)
        if about:
            written.append(f"     {about}\n")
    return "".join(written)


THE_ACTS: Final = _the_acts()


THE_MARKS_ON_A_PAGE: Final = SAYS.text(
    "the-marks-on-a-page",
    kinds=_KINDS,
    max_title=MAX_TITLE,
    max_note_lines=MAX_NOTE_LINES,
    max_note_line=MAX_NOTE_LINE,
    max_spaces=MAX_SPACES,
    max_label=MAX_LABEL,
    max_illustration=MAX_ILLUSTRATION,
)

THE_LIMITS: Final = SAYS.text(
    "the-limits",
    max_line=MAX_LINE,
    max_lines=MAX_LINES,
    min_weight_minutes=MIN_WEIGHT_MINUTES,
    max_weight_minutes=MAX_WEIGHT_MINUTES,
    max_help_after=MAX_HELP_AFTER,
    max_way_out_minutes=MAX_WAY_OUT_MINUTES,
    max_in_hand=MAX_IN_HAND,
    max_title=MAX_TITLE,
    max_note_line=MAX_NOTE_LINE,
    max_label=MAX_LABEL,
    max_note_lines=MAX_NOTE_LINES,
    max_spaces=MAX_SPACES,
)

HOW_THE_TEXT_READS: Final = SAYS.text("how-the-text-reads")

WHAT_TO_REFUSE_BY_DEFAULT: Final = SAYS.text("what-to-refuse-by-default")

WHAT_MAKES_IT_WORTH_DOING: Final = SAYS.text("what-makes-it-worth-doing")

_DRAWN_SHAPE: Final = ", ".join(f'"{name}": "<a short phrase>"' for name in DIMENSIONS)

THE_TEN_DIMENSIONS: Final = SAYS.text("the-ten-dimensions", drawn_shape=_DRAWN_SHAPE)
