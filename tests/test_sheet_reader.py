"""The vision reader: what it does with a good answer, and with every bad one.

The bad answers matter more. This reader replaced arithmetic whose failure was reporting
an empty box with certainty, so the thing worth pinning down is that it never converts a
model's silence, or its confusion, into a confident statement about the paper.
"""

from __future__ import annotations

import pytest

from agents.sheet_reader import SheetReader
from orchestrator.router import StubRouter
from shared.agents import AgentContext
from shared.ids import CellId, ExerciseId, LearnerId, SheetId
from shared.sheet import CellKind, CellSpec, Rect, SheetSpec
from shared.vision_contracts import ReadConfidence, RectifiedPage

CELLS = ("q1c1", "q1c2", "q1c3")


def a_spec() -> SheetSpec:
    return SheetSpec(
        sheet_id=SheetId("sh_test"),
        exercise_id=ExerciseId("ex_test"),
        title="Tre caselle",
        cells=tuple(
            CellSpec(
                id=CellId(name),
                kind=CellKind.CHOICE_BOX,
                rect=Rect(0.1 + 0.3 * n, 0.5, 0.2, 0.05),
                label=word,
                group="q1",
            )
            for n, (name, word) in enumerate(
                zip(CELLS, ("sole", "nuvole", "pioggia"), strict=True)
            )
        ),
        qr_rect=Rect(0.78, 0.025, 0.18, 0.118),
    )


def a_page() -> RectifiedPage:
    return RectifiedPage(
        sheet_id=SheetId("sh_test"),
        exercise_id=ExerciseId("ex_test"),
        png=b"\x89PNG\r\n\x1a\n",
        width=1240,
        height=1754,
        captured_at=1.0,
        spec_version=1,
    )


async def read_with(reply: str) -> tuple[StubRouter, object]:
    router = StubRouter(replies=[reply])
    context = AgentContext(
        router=router, learner_id=LearnerId(""), learner_hints={}, now=99.0
    )
    reading = await SheetReader().read_page(context, page=a_page(), spec=a_spec())
    return router, reading


async def test_a_clean_answer_becomes_a_reading() -> None:
    _, reading = await read_with(
        '{"cells": [{"id": "q1c1", "mark": "marked"}, '
        '{"id": "q1c2", "mark": "empty"}, {"id": "q1c3", "mark": "empty"}]}'
    )
    assert [c.value for c in reading.cells] == ["sole", None, None]
    assert not reading.needs_review
    assert not reading.degraded


async def test_json_wrapped_in_prose_or_fences_is_still_read() -> None:
    """Models add a fence or a sentence. Refusing that would mean refusing most answers."""
    _, reading = await read_with(
        'Here is what I see:\n```json\n{"cells": [{"id": "q1c1", "mark": "marked"}, '
        '{"id": "q1c2", "mark": "marked"}, {"id": "q1c3", "mark": "empty"}]}\n```'
    )
    assert [c.value for c in reading.cells] == ["sole", "nuvole", None]


async def test_a_box_the_model_was_unsure_about_goes_to_the_parent() -> None:
    _, reading = await read_with(
        '{"cells": [{"id": "q1c1", "mark": "unsure"}, '
        '{"id": "q1c2", "mark": "empty"}, {"id": "q1c3", "mark": "empty"}]}'
    )
    doubtful = [c for c in reading.cells if c.needs_review]
    assert [str(c.cell_id) for c in doubtful] == ["q1c1"]
    assert doubtful[0].value is None
    assert doubtful[0].confidence is ReadConfidence.UNSURE


async def test_a_box_the_model_skipped_is_not_reported_as_empty() -> None:
    """The failure the arithmetic had: silence turned into a confident "nothing there"."""
    _, reading = await read_with('{"cells": [{"id": "q1c1", "mark": "marked"}]}')
    skipped = [c for c in reading.cells if c.needs_review]
    assert [str(c.cell_id) for c in skipped] == ["q1c2", "q1c3"]
    assert all("skipped" in c.note for c in skipped)


@pytest.mark.parametrize(
    "reply",
    [
        "I am sorry, I cannot look at images.",
        "{",
        '{"cells": "all of them are marked"}',
        "[]",
        "",
    ],
)
async def test_an_answer_in_the_wrong_shape_reads_nothing_at_all(reply: str) -> None:
    """Nothing is salvaged from a partial answer: half a reading looks exactly like a
    whole one by the time it reaches a display."""
    _, reading = await read_with(reply)
    assert all(c.needs_review for c in reading.cells)
    assert all(c.value is None for c in reading.cells)


async def test_an_answer_cut_off_by_the_length_limit_is_thrown_away() -> None:
    long_enough = '{"cells": [' + ", ".join(
        f'{{"id": "{name}", "mark": "marked", "note": "{"x" * 200}"}}' for name in CELLS
    )
    _, reading = await read_with(long_enough)
    assert all(c.needs_review for c in reading.cells)
    assert all("cut short" in c.note for c in reading.cells)


async def test_the_prompt_carries_the_page_the_boxes_and_nothing_about_a_person() -> None:
    router, _ = await read_with('{"cells": []}')
    sent = router.seen[0]
    assert sent.images and sent.images[0].png == a_page().png
    for name in CELLS:
        assert name in sent.prompt
    assert "sole" in sent.prompt
    # The three words it is allowed to answer with, and no fourth.
    assert "marked|empty|unsure" in sent.prompt
