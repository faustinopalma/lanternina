"""The checks an afternoon has to pass before it is saved, each one refusing one thing.

Two times with opposite properties, and this is the slow one. Devising is offline,
repeatable and has no audience, so a devise → check → repair → recheck loop costs waiting
rather than risk. Running is reactive and has no second chance. Everything that can be
decided and checked while devising must be, and this module is where "must be" is written
down.

**Why this is not all in :mod:`shared.experience`.** The parser raises on the first thing
it cannot read, which is right for a shape — a document with a malformed weight is not a
document. These are different: they are properties of a whole plan that reads perfectly,
and the answer to one of them is a repair request naming the fields that failed. So they
return a list, and the list is what a repair prompt is built from. Sending a model the
whole document back and asking for a new one changes an afternoon that was already mostly
right.

The table in `ideas/09 §7` is split across the two. What the parser refuses: a moment with
no way out, a way out over twenty minutes, a rung ladder that is not four rungs going up,
a cycle, a branch that leads nowhere, a paper moment with no version that runs without
printing. What is here:

============================================ ==========================================
check                                        refuses
============================================ ==========================================
:func:`the_way_out_starts_from_something`    the goodbye that is felt as a cut
:func:`the_short_version_fits`               the plan that never fitted its own window
:func:`the_ending_is_written_down`           the afternoon whose only ending is unwritten
:func:`nothing_from_the_block_list`          the praise and the blame, before they are said
:func:`no_placeholder_is_left`               the document that reads as finished and is not
:func:`not_the_same_afternoon_again`         the fifth afternoon that is the first one
============================================ ==========================================
"""

from __future__ import annotations

import re
from collections.abc import Sequence
from dataclasses import dataclass
from typing import Final

from .blocklist import blocked_in, fold
from .capabilities import Act
from .experience import (
    MAX_SHARED_DIMENSIONS,
    Continuation,
    Drawn,
    Experience,
    Moment,
    Weight,
    longest_at,
    shared_dimensions,
)

# What a document that is not finished looks like. Deliberately not "..." — an ellipsis is
# ordinary Italian and one is printed on a page in `experiences/` — and deliberately not a
# bare slash, because a date carries one. What is left is the shapes a model reaches for
# when it has not decided: a bracketed blank, a brace, a marker word, and a spaced slash
# between two options.
_PLACEHOLDERS: Final[tuple[tuple[re.Pattern[str], str], ...]] = (
    (re.compile(r"<[^>]{1,40}>"), "something in angle brackets"),
    (re.compile(r"\[[^\]]{1,40}\]"), "something in square brackets"),
    (re.compile(r"\{"), "a brace"),
    (re.compile(r"\b(todo|tbd|xxx|fixme|placeholder|lorem ipsum)\b"), "a marker word"),
    (re.compile(r"\S \/ \S"), "two options with a slash between them"),
)


@dataclass(frozen=True, slots=True)
class Complaint:
    """One thing wrong, and where.

    ``where`` names a field the way the document names it — ``moments[3].way_out`` — so a
    repair request can ask for that field back and nothing else. ``says`` is written for
    the model that has to fix it and for the person reading the log, in that order.
    """

    where: str
    says: str

    def __str__(self) -> str:
        return f"{self.where}: {self.says}"


def check(
    plan: Experience | Continuation, *, recent: Sequence[Drawn] = ()
) -> tuple[Complaint, ...]:
    """Everything wrong with this plan, or nothing.

    ``recent`` is what the last few afternoons in this house were drawn along. It is empty
    for a continuation and for the first afternoon a house ever gets, and an empty list
    makes :func:`not_the_same_afternoon_again` say nothing rather than refuse everything.
    """
    complaints: list[Complaint] = []
    complaints.extend(the_way_out_starts_from_something(plan.moments))
    complaints.extend(the_ending_is_written_down(plan.moments))
    complaints.extend(nothing_from_the_block_list(plan))
    complaints.extend(no_placeholder_is_left(plan))
    if isinstance(plan, Experience):
        complaints.extend(the_short_version_fits(plan))
        complaints.extend(not_the_same_afternoon_again(plan.drawn, recent))
    return tuple(complaints)


def the_way_out_starts_from_something(moments: Sequence[Moment]) -> tuple[Complaint, ...]:
    """The way out has to name an object the afternoon already put in somebody's hands.

    The parser checks that the way out names its object in its own text. That alone lets a
    model satisfy it by inventing an object in the last sentence — "take the little brass
    key and put it down" — which is exactly the generic goodbye it was meant to stop. So
    the object has to have been mentioned before: in this moment, or in one that comes
    earlier, on a display or on a page.

    **What it checks and what it does not.** It checks that the words were said. It cannot
    check that the thing exists, that it is within reach, or that the sentence about it
    makes sense. That is the limit of a check against text, and the rest is what a parent
    reads the document for.
    """
    complaints: list[Complaint] = []
    said = ""
    for index, moment in enumerate(moments):
        said = f"{said} {fold(' '.join(moment.words_before_the_way_out))}"
        if fold(moment.way_out.in_hand) not in said:
            complaints.append(
                Complaint(
                    where=f"moments[{index}].way_out.in_hand",
                    says=(
                        f"the way out of {moment.id!r} starts from "
                        f"{moment.way_out.in_hand!r}, which nothing before it ever "
                        f"mentions; an ending that reaches for an object nobody was given "
                        f"is the goodbye that is felt as a cut"
                    ),
                )
            )
    return tuple(complaints)


def the_short_version_fits(experience: Experience) -> tuple[Complaint, ...]:
    """The longest run at the short weight has to be over before the afternoon is.

    At the short weight, because that is the last thing the runner can do before it takes
    a way out: a plan whose shortest form does not fit is a plan that was never going to
    fit, and no amount of replanning saves it. The longest path and not the sum — branches
    are alternatives, and adding them together refuses documents that run fine.
    """
    shortest = longest_at(experience.moments, Weight.SHORT)
    if shortest <= experience.minutes:
        return ()
    return (
        Complaint(
            where="minutes",
            says=(
                f"the shortest way through this afternoon takes {shortest} minutes and it "
                f"says it lasts {experience.minutes}; there is nothing left to shorten"
            ),
        ),
    )


def the_ending_is_written_down(moments: Sequence[Moment]) -> tuple[Complaint, ...]:
    """Somewhere in here there is an ending somebody read.

    The parser already refuses a plan a branch can strand in, but it treats ``ask`` as
    reaching an ending, because a continuation is held to these same rules. That leaves one
    document it lets through: every branch says ``ask``, so the only ending in the approved
    plan is one nobody has written yet. A parent approving that has approved a beginning.
    """
    if any(moment.act is Act.CLOSE for moment in moments):
        return ()
    return (
        Complaint(
            where="moments",
            says=(
                "no moment here closes; every path leaves the ending to be written later, "
                "so there is no ending in what the parent reads"
            ),
        ),
    )


def nothing_from_the_block_list(plan: Experience | Continuation) -> tuple[Complaint, ...]:
    """No praise, no blame, no hurry, no score, and no word about the machinery.

    Checked over the pre-written text because the pre-written text is the runtime fallback.
    A filter that replaces a bad sentence with a stored one is worth nothing if the stored
    one was never looked at.
    """
    complaints: list[Complaint] = []
    if isinstance(plan, Experience):
        for field, text in (("title", plan.title), ("overview", plan.overview)):
            found = blocked_in(text)
            if found:
                complaints.append(
                    Complaint(where=field, says=f"it says {_joined(found)}")
                )
    for index, moment in enumerate(plan.moments):
        found = blocked_in("\n".join(moment.words))
        if found:
            complaints.append(
                Complaint(
                    where=f"moments[{index}]",
                    says=f"{moment.id!r} says {_joined(found)}",
                )
            )
    return tuple(complaints)


def no_placeholder_is_left(plan: Experience | Continuation) -> tuple[Complaint, ...]:
    """Nothing in here is still waiting to be decided.

    A document that reads as finished and is not is the worst of the failures a parent
    cannot catch: the overview is complete, the moments are complete, and the fourth one
    says ``[nome dell'oggetto]``. It goes on a display exactly like that.
    """
    complaints: list[Complaint] = []
    everything: list[tuple[str, str]] = []
    if isinstance(plan, Experience):
        everything.extend((("title", plan.title), ("overview", plan.overview)))
    for index, moment in enumerate(plan.moments):
        everything.extend((f"moments[{index}]", text) for text in moment.words)
    seen: set[tuple[str, str]] = set()
    for where, text in everything:
        for pattern, what in _PLACEHOLDERS:
            if not pattern.search(fold(text)):
                continue
            # The same sentence appears in all three weights of a moment, so without this a
            # single unfinished line arrives as three identical things to fix.
            if (where, text) in seen:
                break
            seen.add((where, text))
            complaints.append(Complaint(where=where, says=f"{text!r} still carries {what}"))
            break
    return tuple(complaints)


def not_the_same_afternoon_again(
    drawn: Drawn, recent: Sequence[Drawn]
) -> tuple[Complaint, ...]:
    """Not the last few afternoons with different nouns.

    A seed produces variety that cannot be checked. Ten recorded dimensions produce variety
    that can: sharing more than two of them with something recent is refused, and the
    refusal names which ones, so a repair can redraw those rather than the whole afternoon.
    """
    complaints: list[Complaint] = []
    for before in recent:
        same = shared_dimensions(drawn, before)
        if len(same) > MAX_SHARED_DIMENSIONS:
            complaints.append(
                Complaint(
                    where="drawn",
                    says=(
                        f"this shares {len(same)} of the ten dimensions with an afternoon "
                        f"this house has already had ({', '.join(same)}); redraw those "
                        f"rather than the rest"
                    ),
                )
            )
            # One complaint is enough to send it back; naming every past afternoon it
            # resembles would ask a model to satisfy several constraints at once.
            break
    return tuple(complaints)


def _joined(found: Sequence[object]) -> str:
    return ", ".join(str(entry) for entry in found)
