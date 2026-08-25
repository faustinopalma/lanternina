"""The stock a parent leaves behind them.

A parent sits down once, approves several, and may not open the panel for a week. What they
need before closing it is one number: does the house have enough. These are the two halves
of that — the count, and deciding about a handful in one request.

What is deliberately absent: anything about what was run. The backlog counts afternoons
waiting and minutes waiting, and there is no field anywhere for how many happened, how often,
or how long anybody spent. `docs/NON-GOALS.md` is the reason, and a test is how it stays true.
"""

from __future__ import annotations

import time

from panel.experiences import OfferedExperience, backlog_of
from shared.approval import ApprovalState


def an_offer(offered_id: str, *, state: str, minutes: int = 60, begun: float = 0.0):
    return OfferedExperience(
        id=offered_id,
        household_id="hh_1",
        experience={"title": offered_id, "minutes": minutes},
        created_at=time.time(),
        state=state,
        begun_at=begun,
    )


def test_only_what_is_approved_and_not_yet_begun_is_stock() -> None:
    rows = [
        an_offer("a", state=ApprovalState.APPROVED.value),
        an_offer("b", state=ApprovalState.APPROVED.value, minutes=90),
        an_offer("c", state=ApprovalState.PENDING.value),
        an_offer("d", state=ApprovalState.REJECTED.value),
        an_offer("e", state=ApprovalState.APPROVED.value, begun=time.time()),
    ]

    stock = backlog_of(rows, days_a_week=2)

    assert stock.approved == 2
    assert stock.minutes == 150


def test_how_far_it_carries_is_a_floor_and_not_a_promise() -> None:
    """Four approved, two days a week: a fortnight. Rounded down, always."""
    rows = [an_offer(str(i), state=ApprovalState.APPROVED.value) for i in range(4)]

    assert backlog_of(rows, days_a_week=2).days == 14
    assert backlog_of(rows, days_a_week=7).days == 4
    # Three a week does not divide four evenly, and the answer must not flatter.
    assert backlog_of(rows, days_a_week=3).days == 9


def test_a_house_that_chose_no_day_is_carried_nowhere() -> None:
    """Not an error, and not infinity: a stock that will never be spent carries nothing."""
    rows = [an_offer("a", state=ApprovalState.APPROVED.value)]

    assert backlog_of(rows, days_a_week=0).days == 0


def test_nothing_that_happened_is_counted() -> None:
    """The shape of the answer is the guarantee: four keys, and none of them is a tally."""
    said = backlog_of([an_offer("a", state=ApprovalState.APPROVED.value)], days_a_week=2)

    assert set(said.to_public()) == {"approved", "minutes", "perWeek", "days"}
