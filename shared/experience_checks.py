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
There is a seventh property in the README that no function here covers: every moment has an
answer that can be wrong, and the last moment produces something worth keeping. The six
above are about safety and shape, and a plan can pass all of them and still be a worksheet.
It is unchecked, and the README says so rather than implying otherwise."""

from __future__ import annotations

import re
from collections.abc import Sequence
from dataclasses import dataclass
from typing import Final

from .blocklist import blocked_in, fold
from .capabilities import Act
from .experience import (
    MAX_SHARED_DIMENSIONS,
    MAY_RECUR,
    SET_BY_THE_HOUSE,
    Continuation,
    Drawn,
    Experience,
    Moment,
    Weight,
    longest_at,
    shared_dimensions,
    sheets_at_once,
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
    # Two *words* with a spaced slash, which is how a model leaves a choice open. A number
    # on either side is a fraction or a date, and a pair like "bianco / nero" is a pair.
    (re.compile(r"\b[a-z]{3,} \/ [a-z]{3,}\b(?! *[,.])"), "two options with a slash between them"),
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
    plan: Experience | Continuation,
    *,
    recent: Sequence[Drawn] = (),
    already_said: Sequence[str] = (),
    sheets_at_most: int = 0,
) -> tuple[Complaint, ...]:
    """Everything wrong with this plan, or nothing.

    ``recent`` is what the last few afternoons in this house were drawn along. It is empty
    for a continuation and for the first afternoon a house ever gets, and an empty list
    makes :func:`not_the_same_afternoon_again` say nothing rather than refuse everything.

    ``already_said`` is what the afternoon put in front of somebody before this plan
    begins. Empty for a whole experience, which begins at its own beginning; for a
    continuation it is the stretch that came first, and leaving it out refuses an ending
    that reaches for the very page the earlier stretch handed over.

    ``sheets_at_most`` is what the parent set in the panel: how many sheets may be on the
    table at one time, not how many the afternoon spends. Zero means nobody said, and
    nothing is refused. A continuation is not bounded here even when a number is given:
    it begins in the middle and nothing tells it what is already on the table.
    TODO(poc): carry what the house has already handed over and not collected, and bound it.
    """
    complaints: list[Complaint] = []
    complaints.extend(the_way_out_starts_from_something(plan.moments, already_said))
    complaints.extend(the_ending_is_written_down(plan.moments))
    complaints.extend(nothing_from_the_block_list(plan))
    complaints.extend(no_placeholder_is_left(plan))
    if isinstance(plan, Experience):
        complaints.extend(the_short_version_fits(plan))
        complaints.extend(not_the_same_afternoon_again(plan.drawn, recent))
        complaints.extend(no_more_paper_than_the_house_wants(plan, sheets_at_most))
    return tuple(complaints)


def no_more_paper_than_the_house_wants(
    experience: Experience, at_most: int
) -> tuple[Complaint, ...]:
    """How many sheets can be on the table at one time, against what the parent allows.

    A ceiling and not a target, which is why the complaint only fires above it: an
    afternoon that needs one page and prints one page is the right afternoon, and a check
    that asked for the number to be met would be a check that produced padding.

    The unit is what is on the table at once and not what the afternoon spends in total —
    `shared/experience.sheets_at_once` says why the two are different and why the total
    needs no number of its own.
    """
    if at_most <= 0:
        return ()
    wanted = sheets_at_once(experience.moments)
    if wanted <= at_most:
        return ()
    return (
        Complaint(
            where="moments",
            says=(
                f"this afternoon puts {wanted} sheets on the table at once and this house "
                f"wants at most {at_most} there; join what belongs on one page, leave out "
                f"what only makes the first page shorter, or take one back before handing "
                f"over the next"
            ),
        ),
    )


def the_way_out_starts_from_something(
    moments: Sequence[Moment], already_said: Sequence[str] = ()
) -> tuple[Complaint, ...]:
    """The way out has to name an object the afternoon already put in somebody's hands.

    The parser checks that the way out names its object in its own text. That alone lets a
    model satisfy it by inventing an object in the last sentence — "take the little brass
    key and put it down" — which is exactly the generic goodbye it was meant to stop. So
    the object has to have been mentioned before: in this moment, or in one that comes
    earlier, on a display or on a page.

    ``already_said`` is what came before ``moments`` in the same afternoon, and it exists
    because this was written for a whole experience and then applied unchanged to a
    continuation. A continuation starts in the middle by definition, so its first moment
    had nothing before it and any ending reaching for a page handed over in the earlier
    stretch was refused — measured on 25 August 2026 on `aft_fd196b32`, one run in three.

    **What it checks and what it does not.** It checks that the words were said. It cannot
    check that the thing exists, that it is within reach, or that the sentence about it
    makes sense. That is the limit of a check against text, and the rest is what a parent
    reads the document for.
    """
    complaints: list[Complaint] = []
    said = fold(" ".join(already_said))
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
    """Nothing here is a remark about the person reading it, or about the machine.

    Praise, blame, hurry, a score and the machinery, each caught by the person in the
    sentence rather than by a word: *hai sbagliato* and not *errore*. `shared/blocklist.py`
    says why the second one was tried first and what it cost.

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
    """Not the last few afternoons with different nouns, and not a new world every time.

    A seed produces variety that cannot be checked. Recorded dimensions produce variety that
    can. But two of the ten are the world — where it is set and what the person is inside it
    — and those are allowed to come back: a house that liked a place wants to return to it,
    and nothing can be built across afternoons if nothing may recur. Four more are the
    channel, and a house does not choose those: it owns a printer and one display, or it
    does not.

    So the count is over the four that are decisions — mechanic, progress, tone, ending.
    Sharing more than two of them is refused, and the refusal names which, so a repair
    redraws those rather than the whole afternoon.
    """
    complaints: list[Complaint] = []
    ignored = MAY_RECUR | SET_BY_THE_HOUSE
    for before in recent:
        same = tuple(one for one in shared_dimensions(drawn, before) if one not in ignored)
        if len(same) > MAX_SHARED_DIMENSIONS:
            complaints.append(
                Complaint(
                    where="drawn",
                    says=(
                        f"this works the same way as an afternoon this house has already "
                        f"had ({', '.join(same)}); redraw those rather than the rest. Where "
                        f"it is set and who they are may come back"
                    ),
                )
            )
            # One complaint is enough to send it back; naming every past afternoon it
            # resembles would ask a model to satisfy several constraints at once.
            break
    return tuple(complaints)


def _joined(found: Sequence[object]) -> str:
    return ", ".join(str(entry) for entry in found)
