"""The manual of forms, so that an afternoon is built from one rather than invented from nothing.

`methods/` holds one record per method that can actually be run in a house with a printer,
a scanner and a small display. Until now nothing read it: `ideas/11 §12` ends with *nothing
reads it yet*, and the deviser reached for the ten forms anybody reaches for. This module is
the consumer.

**What it is for.** Not variety for its own sake. A record carries the part a model does not
have — how one is built, which parts move and what happens when they are moved, where the
work sits, and where it breaks on paper. That is craft, and craft is what the prompt could
not supply by asking harder.

**Selection is code, not similarity.** `ideas/11 §3` argues it out: at devise time the only
text in hand is a list of subjects, and searching a corpus of forms with a query about
subjects returns whatever an embedding happens to associate. What is done here instead is a
filter — what this house can actually run — and then a draw. A test can assert *a house is
never handed a form it cannot run*; nothing can assert that of a search.

**Missing is not fatal.** The corpus is data outside the installed packages, so a container
built without it must still devise afternoons. :func:`load` returns nothing rather than
raising, and the prompt then carries no method block at all. The alternative — a lazy import
that raises on the first real request — is the failure this repository already paid for once
with `agents/`, where the app started, the route registered, and the defect waited for a
person to be standing in front of it.
"""

from __future__ import annotations

import json
import os
import random
from collections.abc import Sequence
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Any, Final

from .capabilities import HouseCapability

# Which side of a method rests on looking inside words. Only `no` is servable, and the two
# halves fail for different reasons: `to_compose` is the operation a language model cannot
# do, so it would write a broken puzzle; `to_solve` is the operation this project does not
# ask a reader for, which `shared/experience_prompt.only-what-you-can-answer.md` argues from
# W3C COGA rather than from what a model can manage. `both` is both.
_LETTERS_OK: Final = "no"

_FORM: Final = "form"
_MOVE: Final = "move"

# How many methods are put in front of the model at once. Not a budget: the whole catalogue
# is only 12 kB and would fit. It is what keeps two afternoons for the same household from
# being offered the same menu and therefore making the same choice, measured doing exactly
# that on 3 September 2026. Sixty leaves a real choice and changes enough between calls.
CATALOGUE: Final = 60


@dataclass(frozen=True, slots=True)
class Method:
    """One method, as the manual records it.

    The fields are `methods/README.md`'s contract. What is left out of this class is left
    out on purpose: `also`, `from_entries` and `goes_with` are how a person gets from an
    encyclopedia entry to a record and back, and none of them is worth prompt budget.
    """

    method_id: str
    kind: str
    name: str
    one_line: str
    how: str
    knobs: tuple[tuple[str, str], ...]
    where_the_work_is: str
    breaks: str
    adult_cost: str
    verification: str
    comes_back: str
    people: int
    letters_inside_words: str

    @property
    def is_a_move(self) -> bool:
        return self.kind == _MOVE

    def written(self) -> str:
        """The record as a model reads it.

        Every knob carries its effect at each setting, including the setting the `how` has
        just told you not to use. `methods/README.md` calls that deliberate: the reason a
        choice was made is the part that teaches, and a record describing only the chosen
        setting cannot be argued with — which matters here, because the model is allowed to
        argue with it.
        """
        parts = [
            f"{self.name}",
            f"{self.one_line}",
            f"How one is built: {self.how}",
        ]
        parts.extend(f"What moves — {knob}: {effect}" for knob, effect in self.knobs)
        parts.append(f"Where the work is: {self.where_the_work_is}")
        if self.breaks.strip():
            parts.append(f"Where it breaks: {self.breaks}")
        return "\n".join(parts)


def _a_method(said: Any) -> Method | None:
    """One record, or nothing when it is not one.

    A malformed file is skipped rather than raised on, for the reason in the module
    docstring: this corpus improves an afternoon and no afternoon depends on it.
    `tools/methods_check.py` is where a broken record is meant to be caught, loudly, before
    it is committed.
    """
    if not isinstance(said, dict):
        return None
    try:
        knobs = tuple(
            (str(one["knob"]), str(one["effect"]))
            for one in said["knobs"]
            if isinstance(one, dict) and "knob" in one and "effect" in one
        )
        return Method(
            method_id=str(said["method_id"]),
            kind=str(said["kind"]),
            name=str(said["name"]),
            one_line=str(said["one_line"]),
            how=str(said["how"]),
            knobs=knobs,
            where_the_work_is=str(said["where_the_work_is"]),
            breaks=str(said.get("breaks", "")),
            adult_cost=str(said["adult_cost"]),
            verification=str(said["verification"]),
            comes_back=str(said["comes_back"]),
            people=int(said["people"]),
            letters_inside_words=str(said["letters_inside_words"]),
        )
    except (KeyError, TypeError, ValueError):
        return None


def where_they_are() -> tuple[Path, ...]:
    """Everywhere the corpus might be, most deliberate first.

    The environment variable is what a test and a probe use. The second is a checkout, and
    it is also the image: the Dockerfile copies `methods/` next to `shared/`, so the same
    relative step finds it in both. The third covers a process started from the repository
    root with the package installed somewhere else.
    """
    said = os.environ.get("LANTERNINA_METHODS_DIR", "").strip()
    roots = [Path(said)] if said else []
    roots.append(Path(__file__).resolve().parent.parent / "methods")
    roots.append(Path.cwd() / "methods")
    return tuple(roots)


@lru_cache(maxsize=1)
def load() -> tuple[Method, ...]:
    """The whole corpus, read once, sorted by id so a draw from a seed is reproducible.

    Returns nothing at all when there is no corpus to read, which is a container built
    without it. Nothing here logs that: the caller knows whether it asked for methods, and a
    warning per devise would say the same thing every time.
    """
    for root in where_they_are():
        if not root.is_dir():
            continue
        found: list[Method] = []
        for path in sorted(root.glob("*.json")):
            try:
                said = json.loads(path.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError):
                continue
            one = _a_method(said)
            if one is not None:
                found.append(one)
        if found:
            return tuple(found)
    return ()


def runnable(
    methods: Sequence[Method],
    *,
    capabilities: frozenset[HouseCapability],
    people: int = 1,
    an_adult_takes_part: bool = False,
) -> tuple[Method, ...]:
    """The ones this house can actually run this afternoon.

    Every clause is a fact about the house or about what the format elsewhere refuses, and
    none of them is a judgement about whether a method is any good. `ideas/11 §5` is why:
    there is no goodness outside the situation, so what is written here can only be *can it
    be run here*.

    Measured 3 September 2026 over the 204 records: a one-person house with a printer, a
    scanner and a display, with no adult taking part, can run 154 of them. The properties do
    not narrow much, which `ideas/11 §12` had already found and said plainly.
    """
    can_print = HouseCapability.PRINT_A4 in capabilities
    can_scan = HouseCapability.SCAN_A4 in capabilities
    can_photograph = HouseCapability.PHOTOGRAPH_TABLE in capabilities
    kept: list[Method] = []
    for one in methods:
        if one.letters_inside_words != _LETTERS_OK:
            continue
        if one.people > people:
            continue
        if not an_adult_takes_part and one.adult_cost != "none":
            continue
        if not an_adult_takes_part and one.verification == "needs_a_person":
            continue
        if one.comes_back == "a_sheet" and not (can_print and can_scan):
            continue
        if one.comes_back == "a_photograph" and not can_photograph:
            continue
        kept.append(one)
    return tuple(kept)


def draw(
    methods: Sequence[Method],
    *,
    avoid: Sequence[str] = (),
    rand: random.Random | None = None,
) -> tuple[Method | None, Method | None]:
    """One form to build the afternoon from, and one move to apply to it.

    Two rather than one because they do different work. A form produces the thing somebody
    does; a move is applied to a form and changes it — a thing put where somebody will look
    that turns out to do nothing, a prediction asked for before the measurement. The moves
    are the most reusable records in the corpus and a serving with only forms in it would
    never reach them.

    This is the fallback rather than the usual path. What normally happens is that the model
    reads :func:`index` and asks for what it wants by name; a draw is what happens when that
    call fails or names nothing that exists, because an afternoon may not be lost over the
    way its form was chosen.

    ``avoid`` is the hook for not handing the same form twice running. Nothing records which
    method an afternoon was built from today, so nothing passes it yet; it is here because
    the alternative is discovering later that the caller has nowhere to say so.
    """
    picker = rand or random.Random()
    away = set(avoid)
    forms = [one for one in methods if not one.is_a_move and one.method_id not in away]
    moves = [one for one in methods if one.is_a_move and one.method_id not in away]
    return (
        picker.choice(forms) if forms else None,
        picker.choice(moves) if moves else None,
    )


def index(
    methods: Sequence[Method],
    *,
    sample: int = 0,
    rand: random.Random | None = None,
) -> str:
    """The catalogue: methods this house can run, as an id and a name and nothing else.

    This is the knowledge the model is given, and it is deliberately not the knowledge
    itself. A name is about 47 characters and a whole record is about 2 300, so the corpus in
    full is some 440 kB against a prompt of 27 kB — the arithmetic settles it before taste
    does. What a name buys is the one thing the model cannot supply for itself: that there
    are a hundred and eighty of these and not the ten anybody thinks of.

    ``sample`` is why this takes a random source, and it was added after measuring. Handed
    the whole catalogue twice for the same household on 3 September 2026, the model chose
    `plan-of-a-place-you-know` with `hand-over-the-wrong-version-to-be-corrected` **both
    times**, wording the reason differently and picking identically. That is worse than the
    random draw it replaced: a menu that never changes turns a good chooser into a fixed one,
    because the same judgement applied to the same list gives the same answer. Offering a
    different subset each time keeps the judgement and removes the fixity, and it is cheaper.

    The `move` records are marked, because a model choosing blindly from one list would take
    two forms and never learn that the second kind exists. Forms and moves are sampled
    separately so that a subset can never arrive without one of each.
    """
    chosen = list(methods)
    if sample > 0:
        picker = rand or random.Random()
        forms = [one for one in chosen if not one.is_a_move]
        moves = [one for one in chosen if one.is_a_move]
        # Two thirds forms: a form is what the afternoon is built out of and a move only
        # seasons it, so the choice that matters deserves the wider menu.
        want_forms = max(1, sample * 2 // 3)
        chosen = picker.sample(forms, min(want_forms, len(forms))) + picker.sample(
            moves, min(max(1, sample - want_forms), len(moves))
        )
        picker.shuffle(chosen)
    lines = []
    for one in chosen:
        mark = " (a move)" if one.is_a_move else ""
        lines.append(f"{one.method_id}: {one.name}{mark}")
    return "\n".join(lines)


def by_id(methods: Sequence[Method], wanted: Sequence[str]) -> tuple[Method, ...]:
    """The records named, in the order they were named, skipping what does not exist.

    A model that invents an id gets silence for it rather than an error: the caller has a
    draw to fall back on, and refusing the afternoon because one of two names was misspelt
    would be the diagnostic destroying the product.
    """
    known = {one.method_id: one for one in methods}
    found = [known[one] for one in wanted if one in known]
    return tuple(found)
