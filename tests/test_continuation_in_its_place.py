"""A continuation is judged in its place in the afternoon, not from a standing start.

`the_way_out_starts_from_something` was written for a whole experience: it walks the
moments and refuses a way out that reaches for something nothing before it mentions. A
continuation begins in the middle by definition, so its first moment has nothing before it
and any ending reaching for the page the earlier stretch handed over was refused.

Measured on 25 August 2026, one run in three against the deployed panel — `aft_fd196b32`,
refused with *the way out of 'join-the-skies' starts from 'il secondo foglio', which
nothing before it ever mentions*, where the second sheet was the one the afternoon had
printed twelve minutes earlier. The words below are that run's.

Both tests fail on the version that takes no `already_said`.
"""

from __future__ import annotations

from shared.experience import Moment, moment_from_dict
from shared.experience_checks import the_way_out_starts_from_something
from tests.afternoons import say, way_out, weights

EARLIER = ("Sul tavolo c'è il secondo foglio.", "Inventa una nuvola che oggi non c'era.")


def _carrying_on(in_hand: str) -> tuple[Moment, ...]:
    return (
        moment_from_dict(
            say(
                "join-the-skies",
                "Guarda",
                weights=weights(lines=("Guarda cosa hai disegnato.",)),
                way_out=way_out(in_hand),
            )
        ),
    )


def test_a_way_out_may_reach_for_something_the_stretch_before_handed_over() -> None:
    assert the_way_out_starts_from_something(_carrying_on("il secondo foglio"), EARLIER) == ()


def test_a_way_out_reaching_for_something_nobody_was_given_is_still_refused() -> None:
    """The check it was there to make. Widening it must not turn it off."""
    refused = the_way_out_starts_from_something(_carrying_on("la chiavetta di ottone"), EARLIER)

    assert len(refused) == 1
    assert refused[0].where == "moments[0].way_out.in_hand"
    assert "chiavetta di ottone" in refused[0].says
