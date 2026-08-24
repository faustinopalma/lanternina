"""The door an afternoon passes, and what it would let through if it were not there.

The gate itself is Azure's and is not exercised here. What is checked is the part this
repository owns: that everything an adolescent will read is handed to the screener, that
a refusal stops the whole thing rather than part of it, and that something with nothing to
read does not pass by having nothing to object to.

Both ways up to the door are here — a whole experience before a parent is offered it, and
a continuation before a house plays it — because they share the function that gathers the
words, and a field added to one and forgotten in the other is exactly the defect these
tests exist to catch.
"""

from __future__ import annotations

import asyncio
from typing import Any

import afternoons as a
import pytest

from orchestrator.safety import screen_continuation, screen_experience, words_for_a_person
from shared.errors import SafetyBlocked
from shared.experience import ExperienceError
from shared.safety import (
    ContentKind,
    SafetyVerdict,
    ScreenedPayload,
    ScreeningRecord,
)
from shared.seal import Sealer, SealPurpose

A_PAGE: dict[str, Any] = {
    "title": "La nuvola di domani",
    "instructions": "Disegnala come vuoi.",
    "marks": [
        {
            "mark": "words",
            "rect": {"x": 0.04, "y": 0.04, "w": 0.66, "h": 0.045},
            "text": "La nuvola di domani",
            "size_mm": 6.5,
        },
        {
            "mark": "draw_area",
            "id": "il-disegno",
            "rect": {"x": 0.05, "y": 0.2, "w": 0.9, "h": 0.5},
            "label": "Disegnala qui",
            "group": "domani",
        },
    ],
}

MOMENTS: list[dict[str, Any]] = [
    a.say(
        moment_id="ancora-una",
        heading="Ancora una cosa",
        weights=a.weights(lines=("Sta uscendo un foglio.",)),
    ),
    a.hand_over(moment_id="il-terzo", heading="Esce un foglio", design=A_PAGE),
    a.close(moment_id="finita", heading="Finita qui", weights=a.weights(lines=("A domani.",))),
]

CONTINUATION: dict[str, Any] = {
    "format_version": 2,
    "experience_id": "un-pomeriggio-di-nuvole",
    "after": "l-ultimo-foglio",
    "moments": MOMENTS,
}


def a_continuation(**changes: Any) -> Any:
    from shared.experience import Continuation

    payload = dict(CONTINUATION)
    payload.update(changes)
    return Continuation.from_dict(payload)


class Screener:
    """Stands in for Azure. Records what it was given and answers as it was told to."""

    def __init__(self, *, refuse: bool = False) -> None:
        self.refuse = refuse
        self.seen: list[str] = []

    async def screen(
        self, kind: ContentKind, body: str, *, context: str = ""
    ) -> ScreenedPayload:
        self.seen.append(body)
        if self.refuse:
            raise SafetyBlocked("refused at severity 4: violence")
        record = ScreeningRecord(verdict=SafetyVerdict.ALLOW, screener="a test")
        sealer = Sealer(SealPurpose.CONTENT_SAFETY, b"k" * 32, "test")
        draft = {"kind": str(kind), "body": body, "record": record.to_dict()}
        return ScreenedPayload(kind=kind, body=body, record=record, seal=sealer.seal(draft))


def test_everything_a_person_will_read_is_handed_to_the_screener() -> None:
    """Each of these is a place a model writes and an adolescent reads. A field missing
    here is a sentence that reaches somebody without passing anything."""
    words = words_for_a_person(a_continuation())

    for line in (
        "Ancora una cosa",
        "Sta uscendo un foglio.",
        "La nuvola di domani",
        "Disegnala come vuoi.",
        "Disegnala qui",
        "Finita qui",
        "A domani.",
    ):
        assert line in words, f"{line!r} would reach somebody unscreened"


def test_nothing_the_reader_never_sees_is_screened() -> None:
    """Moment ids and rectangles are not text anybody reads, and a screener asked about
    them reports on the wrong thing."""
    words = words_for_a_person(a_continuation())

    assert "il-terzo" not in words
    assert "0.9" not in words


def test_a_screened_continuation_comes_back_sealed() -> None:
    screener = Screener()

    payload = asyncio.run(screen_continuation(screener, a_continuation(), context="test"))

    assert payload.record.verdict is SafetyVerdict.ALLOW
    assert payload.seal.purpose is SealPurpose.CONTENT_SAFETY
    assert len(screener.seen) == 1, "one refusal covers the whole continuation, not a moment"


def test_a_refusal_stops_the_whole_continuation() -> None:
    with pytest.raises(SafetyBlocked, match="severity 4"):
        asyncio.run(screen_continuation(Screener(refuse=True), a_continuation()))


def test_a_continuation_with_nothing_to_read_cannot_be_built_at_all() -> None:
    """The one way an unscreened afternoon could get through, closed one layer earlier.

    An empty body clears any screener, so :func:`screen_continuation` refuses one. In
    format 1 that guard was the only thing standing there and this test built a silent
    moment to prove it. Format 2 will not carry a silent moment: a heading is required, and
    so is at least one line in every weight, in every rung of help and in the way out. So
    what is asserted now is the refusal that comes first. The guard in the gate stays, and
    it is now a belt rather than the braces.
    """
    from shared.experience import Continuation

    with pytest.raises(ExperienceError, match="has no heading|says nothing"):
        Continuation.from_dict(
            {
                **CONTINUATION,
                "moments": [a.say(moment_id="muto", heading=""), a.close()],
            }
        )


# ── The same door, for a whole afternoon ─────────────────────────────────────────────


AN_EXPERIENCE: dict[str, Any] = {
    "format_version": 2,
    "experience_id": "un-pomeriggio-di-ombre",
    "title": "Un pomeriggio di ombre",
    "overview": "Il display dice di cercare un'ombra, poi esce un foglio da riempire.",
    "minutes": 120,
    "requires": ["print_a4", "scan_a4", "show_800x480_1bit"],
    "drawn": a.drawn(),
    "moments": [
        MOMENTS[0],
        MOMENTS[1],
        a.collect(
            moment_id="com-e-andata",
            heading="Mettilo sul vetro",
            on_marks="finita",
            on_blank="finita",
            if_no_page="finita",
        ),
        MOMENTS[2],
    ],
}


def an_experience(**changes: Any) -> Any:
    from shared.experience import Experience

    payload = dict(AN_EXPERIENCE)
    payload.update(changes)
    return Experience.from_dict(payload)


def test_the_title_and_the_overview_are_screened_too() -> None:
    """The parent reads these, and a model wrote them. That is the only qualification
    this door asks for."""
    words = words_for_a_person(an_experience())

    assert "Un pomeriggio di ombre" in words
    assert "cercare un'ombra" in words
    assert "Disegnala qui" in words, "the pages inside it are screened as well"


def test_a_devised_afternoon_comes_back_sealed() -> None:
    screener = Screener()

    payload = asyncio.run(screen_experience(screener, an_experience(), context="test"))

    assert payload.record.verdict is SafetyVerdict.ALLOW
    assert len(screener.seen) == 1, "one refusal covers the whole afternoon, not a moment"


def test_a_refusal_stops_the_whole_afternoon() -> None:
    with pytest.raises(SafetyBlocked, match="severity 4"):
        asyncio.run(screen_experience(Screener(refuse=True), an_experience()))
