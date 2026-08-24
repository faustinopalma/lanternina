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

from typing import Final

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
from .pagedesign import (
    MAX_INSTRUCTIONS,
    MAX_LABEL,
    MAX_READABLE,
    MAX_TITLE,
    MAX_WORDS,
    MIN_BOX_SIDE,
)

_LINES: Final = f"a list of at most {MAX_LINES} lines, each at most {MAX_LINE} characters"

THE_SHAPE_OF_A_MOMENT: Final = (
    "Every moment, whatever it does, carries these five keys and then whatever its act "
    "adds:\n"
    '  "id": 2 to 32 characters of lowercase a-z, digits and hyphens. No capitals, no '
    "accented letters, no underscores and no spaces. Ids are never shown to anybody, so "
    "write them in English even when the afternoon is not.\n"
    f'  "heading": at most {MAX_HEADING} characters, on the display.\n'
    f'  "weights": {{"short": W, "standard": W, "extended": W}} — the same moment at three '
    "costs, reaching the same point in the story. W is "
    f'{{"minutes": <whole number>, "lines": [{_LINES}]}}. The short one takes about a third '
    "of the time of the standard one: one step, with what is already to hand. The extended "
    "one adds an optional step. The three must take different numbers of minutes, short "
    "fewest.\n"
    f'  "help": exactly {HELP_LEVELS} rungs, each '
    f'{{"after_minutes": <whole number>, "lines": [{_LINES}]}}, and after_minutes goes up '
    "along the list. The first is a nudge inside the story, the second a concrete clue, "
    "the third an almost explicit instruction, the fourth hands the answer over as "
    "something the story gives. The same words are used whether somebody asked for help or "
    "whether the time simply passed, so never write them as an answer to a question.\n"
    '  "way_out": {"in_hand": "<a physical object they are holding>", "heading": "<text>", '
    f'"lines": [{_LINES}], "minutes": <whole number>}} — how to reach the ending from '
    "exactly this moment.\n"
    "     in_hand is a thing that exists in the room: a printed sheet, a pencil, a cup, "
    "something the afternoon already put on the table. It is never part of a screen, never "
    "an idea, and never the afternoon itself. Two different moments usually have different "
    "things in hand, because by then something else has happened.\n"
    "     The same words must appear, word for word, in a line of this moment or of one "
    "before it. So write the object into the story first, and then write a way out that "
    "reaches for it. A way out that names something nobody was given is refused.\n"
    "     It never says that anything is being shortened, skipped or cut short.\n"
)

THE_FOUR_ACTS: Final = (
    "A moment is one of these four, and carries no key other than the five above and the "
    "ones shown here:\n"
    '  {"act": "say", ...}\n'
    '  {"act": "hand_over", ..., "design": {"title": "<text>", "instructions": "<text>", '
    f'"marks": [ ... ]}}, "instead": [{_LINES}]}}\n'
    "     instead is what the display says when there is no printer, so that this moment "
    "still reaches the same point in the story with no paper at all. It is not an apology "
    "and it does not mention the printer.\n"
    '  {"act": "collect", ..., "outcomes": ['
    '{"when": "marks", "then": "<a later moment id, or ask>"}, '
    '{"when": "blank", "then": "<a later moment id, or ask>"}], '
    '"if_no_page": "<a later moment id, or ask>"}\n'
    "     if_no_page is where the afternoon goes when nothing was printed at all.\n"
    '  {"act": "close", ...}\n'
)

THE_MARKS_ON_A_PAGE: Final = (
    "A mark on a page is one of these four, and carries no other key:\n"
    '  {"mark": "words", "rect": {...}, "text": "<printed on the page>", '
    '"size_mm": 2.5 to 8.0}\n'
    '  {"mark": "tick_box", "id": "...", "rect": {...}, "label": "<beside the box>", '
    '"group": "<boxes that answer one thing>"}\n'
    '  {"mark": "write_line", "id": "...", "rect": {...}, "label": "...", "group": "..."}\n'
    '  {"mark": "draw_area", "id": "...", "rect": {...}, "label": "...", "group": "..."}\n'
    '  A rect is {"x": .., "y": .., "w": .., "h": ..}, fractions of the page from the '
    "top left.\n"
)

THE_LIMITS: Final = (
    f"A line is at most {MAX_LINE} characters and there are at most {MAX_LINES} lines in "
    f"any list of lines. Every list of lines has at least one line in it.\n"
    f"A weight takes {MIN_WEIGHT_MINUTES} to {MAX_WEIGHT_MINUTES} minutes. A rung of help "
    f"arrives after 1 to {MAX_HELP_AFTER} minutes. A way out takes at most "
    f"{MAX_WAY_OUT_MINUTES} minutes, and what is in_hand is at most {MAX_IN_HAND} "
    f"characters.\n"
    f"On a page: its title is at most {MAX_TITLE} characters, its instructions at most "
    f"{MAX_INSTRUCTIONS}, any words printed on it at most {MAX_WORDS}, and a label at most "
    f"{MAX_LABEL}. These are refused, not trimmed.\n"
    f"At most {MAX_READABLE} boxes, lines and drawing areas on a page, none smaller than "
    f"{MIN_BOX_SIDE} of the page on a side, and none overlapping another.\n"
    "Leave the top right of the page clear from x 0.74 to 1.0 above y 0.16: the code that "
    "says which sheet this is is printed there.\n"
    "Keep every mark inside x 0.04 to 0.96 and below y 0.03.\n"
)

# `ideas/09 §16`. Six properties, and they are the ones that get lost first: they describe
# how a sentence is built rather than what it is about, so a model that is concentrating on
# the story drops them without noticing.
HOW_THE_TEXT_READS: Final = (
    "How every sentence you write has to read:\n"
    "  One instruction at a time, saying what to do, with what, and where.\n"
    "  Everything that matters exists on two surfaces — on a sheet and on a screen — so "
    "that missing one is not missing it.\n"
    "  Nothing asks for speed, fine dexterity, strength, reading aloud, a phone call, "
    "going outside, or something learnt at school.\n"
    "  Every action moves the story on. An approximate answer is a valid one: what is "
    "recognised is the intention, never the precision.\n"
    "  The register is for an adolescent. Never childish, never school-like, never a "
    "tutorial. No remark on how the person did, and no question about themselves.\n"
    "  The plan does not contain its own reasons. No reference to difficulty, to "
    "simplifying, to adapting, to age, or to anything about the person. It has to read as "
    "good design for anybody, because that is what it is.\n"
)

# `ideas/09 §16` again. Named rather than described, because a model asked for "something
# original" produces one of these, and a list of six is cheaper than any amount of prose
# about originality.
WHAT_TO_REFUSE_BY_DEFAULT: Final = (
    "Do not write any of these, whatever else you do: a pirate treasure hunt, an escape "
    "room with a countdown, a question-and-answer quiz, a murder mystery, an apocalypse, "
    "or a computer that has gone mad.\n"
)

_DRAWN_SHAPE: Final = ", ".join(f'"{name}": "<a short phrase>"' for name in DIMENSIONS)

# `ideas/09 §10`. The dimensions are written down for one reason: variety drawn from a seed
# cannot be checked, and variety recorded as ten phrases can.
THE_TEN_DIMENSIONS: Final = (
    "Draw this afternoon along ten dimensions, and write down what you drew:\n"
    f'  "drawn": {{{_DRAWN_SHAPE}}}\n'
    "  frame: where and when the afternoon is set.\n"
    "  role: what the person is, inside it.\n"
    "  mechanic: what they actually do.\n"
    "  progress: how it moves from one moment to the next.\n"
    "  paper: what the printed sheets are for.\n"
    "  glass: what putting a sheet on the scanner is for.\n"
    "  displays: what the screens are for.\n"
    "  camera: what a photograph would be for, or that there is none.\n"
    "  tone: how it sounds.\n"
    "  ending: what shape the ending has.\n"
    "Never take the option that comes to you first, and never the one that would be the "
    "obvious default. When a combination does not hold together, redraw one dimension "
    "rather than all of them.\n"
    "Every one of the ten describes the afternoon. None of them is about the person, and "
    "there is nowhere to write anything about them.\n"
)
