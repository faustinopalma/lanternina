"""How each hand actually moves, in this house.

:mod:`shared.capabilities` says what a hand is called and what equipment it takes. That
half has to be words, because it goes into a document a model writes and into a prompt a
model reads. This half is the other one: what happens in the room when the verb arrives.

Adding a device is adding a :class:`~shared.capabilities.Hand` there and a function here.
Nothing dispatches on the act any more — the runner looks the verb up — so a device that
is registered is a device that works, and a verb with no hand says so at the moment it is
reached rather than falling through to whatever branch was last.

Nothing here knows whether the house is real. ``devices/house.py`` holds that single
branch, so a hand written for the printer works in a pretend house without being told.
"""

from __future__ import annotations

from collections.abc import Callable, Sequence

from devices.ask_panel import PanelUnreachable, draw_page
from devices.house import CannotRun, House, hand_over, show
from orchestrator.outgoing import Outgoing
from shared.capabilities import Act
from shared.experience import HandOver, Moment, Weight
from shared.ids import new_sheet_id

# What a hand is handed, and what it gives back: the id of the sheet it printed, if it
# printed one. Everything a hand needs about the afternoon is on the moment.
Moves = Callable[[House, Moment, Weight, Outgoing, bool], "str | None"]

_MOVES: dict[Act, Moves] = {}


def moves(act: Act) -> Callable[[Moves], Moves]:
    """Register how one verb is carried out. One hand per act, and the last one wins."""

    def keep(how: Moves) -> Moves:
        _MOVES[act] = how
        return how

    return keep


def play(
    house: House, moment: Moment, weight: Weight, said: Outgoing, send: bool
) -> str | None:
    """Carry out one moment at one weight, whichever verb it is."""
    how = _MOVES.get(moment.act)
    if how is None:
        raise CannotRun(f"nothing in this house knows how to {moment.act}")
    return how(house, moment, weight, said, send)


def registered() -> frozenset[Act]:
    """Which verbs have a hand. Read by the tests that keep the two halves in step."""
    return frozenset(_MOVES)


def say(house: House, heading: str, lines: Sequence[str]) -> None:
    """Words on the display that are not a moment: a help rung, or a way out.

    Here rather than in the runner so that everything an afternoon puts in front of
    somebody leaves through this module, whatever prompted it.
    """
    show(house, heading, list(lines))


def _spoken(said: Outgoing, moment: Moment, weight: Weight) -> list[str]:
    lines = moment.at(weight).lines
    return list(said.lines(f"{moment.id}.{weight}", lines, written=lines))


@moves(Act.SAY)
def _say(
    house: House, moment: Moment, weight: Weight, said: Outgoing, send: bool
) -> str | None:
    show(house, moment.heading, _spoken(said, moment, weight))
    return None


@moves(Act.CLOSE)
def _close(
    house: House, moment: Moment, weight: Weight, said: Outgoing, send: bool
) -> str | None:
    show(house, moment.heading, _spoken(said, moment, weight))
    return None


@moves(Act.HAND_OVER)
def _hand_over(
    house: House, moment: Moment, weight: Weight, said: Outgoing, send: bool
) -> str | None:
    """Print one page, or say the words written for the case where no page arrives.

    A ``hand_over`` plays its ``instead`` when there is no printer, and also when the page
    could not be drawn: the words are already written and were already checked, so nothing
    is improvised at the moment something breaks. It returns no sheet, and the ``collect``
    that follows takes its ``if_no_page`` branch.
    """
    if not isinstance(moment, HandOver):
        raise CannotRun("a hand_over moment is the only thing that can print a page")
    drawn = None
    if house.printer or house.pretend is not None:
        try:
            drawn = draw_page(
                moment.page.to_dict(),
                panel=house.panel,
                household=house.household,
                key=house.device_key,
            )
        except PanelUnreachable as exc:
            # Loud in the journal, silent in the room: the afternoon has words for this.
            print(f"the page was not drawn: {exc}")
    if drawn is None:
        instead = said.lines(f"{moment.id}.instead", moment.instead, written=moment.instead)
        show(house, moment.heading, list(instead))
        return None
    show(house, moment.heading, _spoken(said, moment, weight))
    sheet_id = new_sheet_id()
    hand_over(house, drawn, sheet_id=sheet_id, send=send)
    return str(sheet_id)


@moves(Act.COLLECT)
def _collect(
    house: House, moment: Moment, weight: Weight, said: Outgoing, send: bool
) -> str | None:
    """A collect is not played. It is the seam where one stretch ends and the next is asked
    for, and reaching it here means the runner lost track of where it was."""
    raise CannotRun("a collect is the seam between two stretches of an afternoon")
