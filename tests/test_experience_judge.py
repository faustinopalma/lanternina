"""The judge, on the parts that would break the idea rather than the code.

It runs offline and is not a gate, so what matters is not that it refuses correctly — it
refuses nothing. What matters is that the reverse-solve is real: if the author's own words
ever reach the reader, it is no longer working the answer out, it is reading it, and every
run afterwards would look good and mean nothing.
"""

from __future__ import annotations

import json
from typing import Any

import afternoons as a

from agents.experience_judge import (
    FINDINGS,
    Verdict,
    _findings_in,
    contradictions,
    what_the_person_sees,
)
from shared.experience import Experience

AUTHOR_ONLY = ("title", "overview", "themes", "script", "drawn")


def an_experience(**changed: Any) -> Experience:
    return Experience.from_dict(a.an_afternoon(**changed))


def test_the_author_s_own_words_never_reach_the_reader() -> None:
    """The whole test is this. `script` holds what the afternoon is really about."""
    seen = json.loads(what_the_person_sees(an_experience()))
    assert not [name for name in AUTHOR_ONLY if name in seen]


def test_what_the_person_sees_still_carries_the_moments() -> None:
    seen = json.loads(what_the_person_sees(an_experience()))
    whole = an_experience().to_dict()
    assert seen["moments"] == whole["moments"]


def test_a_field_added_to_the_format_arrives_at_the_reader_by_default() -> None:
    """Dropping rather than selecting, so a new field has to be argued out, not in."""
    kept = set(json.loads(what_the_person_sees(an_experience())))
    assert kept == set(an_experience().to_dict()) - set(AUTHOR_ONLY)


def test_a_finding_the_judge_invented_is_dropped() -> None:
    got = _findings_in(
        [
            {"finding": "too_boring", "where": "experience", "says": "it did not grip me"},
            {"finding": "no_way_in", "where": "moments[0]", "says": "the world is declared"},
        ]
    )
    assert [one.where for one in got] == ["no_way_in: moments[0]"]


def test_a_finding_with_nothing_said_is_dropped() -> None:
    assert _findings_in([{"finding": "no_way_in", "where": "moments[0]", "says": " "}]) == ()


def test_a_finding_that_is_not_an_object_does_not_raise() -> None:
    assert _findings_in(["no_way_in", None, 3]) == ()
    assert _findings_in("no_way_in") == ()


def test_every_name_in_the_prompt_is_a_name_the_parser_accepts() -> None:
    """The two lists are in different files, and a word in one and not the other is silent."""
    from agents.experience_judge import SAYS

    said = SAYS.text("format", max_line=44)
    assert [name for name in FINDINGS if name not in said] == []


def test_no_findings_is_not_the_same_as_a_reader_that_failed() -> None:
    quiet = Verdict(
        can_be_wrong=True, question="chi ha scritto la lettera", answer="la nonna", findings=()
    )
    assert quiet.findings == () and not quiet.degraded


def test_a_finding_that_does_not_belong_to_the_kind_is_reported_not_hidden() -> None:
    """An open afternoon cannot have given its answer away; saying so means it misread."""
    verdict = Verdict(
        can_be_wrong=False,
        question="",
        answer="",
        findings=_findings_in(
            [{"finding": "given_away", "where": "moments[1]", "says": "la risposta è scritta"}]
        ),
    )
    assert contradictions(verdict) == ("given_away",)


def test_the_ordinary_case_contradicts_nothing() -> None:
    verdict = Verdict(
        can_be_wrong=True,
        question="chi ha scritto la lettera",
        answer="la nonna",
        findings=_findings_in(
            [{"finding": "no_way_in", "where": "experience", "says": "il mondo è dichiarato"}]
        ),
    )
    assert contradictions(verdict) == ()
