from __future__ import annotations

import io
from unittest.mock import AsyncMock

import pytest
from PIL import Image

from research.workbench import Recorder, repository_root, walk
from shared.experience import Continuation, Experience
from shared.vision_contracts import WhatCameBack
from tests.afternoons import a_continuation, an_afternoon, close, collect, hand_over


def operations():
    image = io.BytesIO()
    Image.new("RGB", (32, 48), "white").save(image, format="PNG")
    png = image.getvalue()
    return dict(
        draw=AsyncMock(return_value=(png, "synthetic page")),
        write=AsyncMock(return_value=png),
        read=AsyncMock(return_value=WhatCameBack(True, True, ("un ponte blu",), 1.0)),
        continue_from=AsyncMock(return_value=(Continuation.from_dict(a_continuation()), None)),
    )


@pytest.mark.asyncio
async def test_reading_reaches_continuation_and_segment_replaces_original(tmp_path):
    calls = operations()
    document = an_afternoon(moments=[hand_over(), collect(on_marks="ask"), close()])
    result = await walk(Experience.from_dict(document), folder=tmp_path, **calls)
    assert result.status == "concluded"
    sent = calls["continue_from"].call_args.kwargs
    assert sent["reading"]["describes"] == ["un ponte blu"]
    assert [event["moment"] for event in result.events] == [
        "il-foglio",
        "che-torna",
        "ancora",
        "fine",
    ]


@pytest.mark.asyncio
async def test_blank_is_read_but_not_written(tmp_path):
    calls = operations()
    calls["read"].return_value = WhatCameBack(False, True, (), 1.0)
    result = await walk(Experience.from_dict(an_afternoon()), blank=True, folder=tmp_path, **calls)
    assert result.status == "concluded"
    calls["write"].assert_not_called()
    assert next(event for event in result.events if "reading" in event)["branch"] == "blank"


@pytest.mark.asyncio
async def test_failed_print_uses_instead_and_if_no_page(tmp_path):
    calls = operations()
    result = await walk(
        Experience.from_dict(an_afternoon()), fail_print=True, folder=tmp_path, **calls
    )
    assert result.status == "concluded"
    assert result.events[1]["lines"] == ["Oggi il foglio non esce.", "Tienilo a mente."]
    assert result.events[2]["branch"] == "if_no_page"
    calls["read"].assert_not_called()
    calls["write"].assert_not_called()


@pytest.mark.asyncio
@pytest.mark.parametrize("degraded", [True, False])
async def test_failed_reading_never_becomes_blank(tmp_path, degraded):
    calls = operations()
    if degraded:
        calls["read"].return_value = WhatCameBack(False, True, (), 1.0, degraded=True)
    else:
        calls["read"].side_effect = RuntimeError("injected reader failure")
    result = await walk(Experience.from_dict(an_afternoon()), folder=tmp_path, **calls)
    assert result.status == "error"
    assert result.events[-1].get("branch") != "blank"
    calls["continue_from"].assert_not_called()


@pytest.mark.asyncio
async def test_two_sheets_remain_available_and_collection_names_one(tmp_path):
    calls = operations()
    document = an_afternoon(moments=[hand_over("first"), hand_over("second"), collect(), close()])
    result = await walk(Experience.from_dict(document), folder=tmp_path, **calls)
    assert result.status == "concluded"
    assert len(result.pages) == 2
    event = result.events[2]
    assert event["available"] == ["01-first", "02-second"]
    assert event["collected"] == "02-second"


@pytest.mark.asyncio
@pytest.mark.parametrize("options", [{"max_steps": 1}, {"stop_at_collect": True}])
async def test_interruption_is_not_a_conclusion(tmp_path, options):
    result = await walk(
        Experience.from_dict(an_afternoon()), folder=tmp_path, **operations(), **options
    )
    assert result.status == "interrupted"
    assert result.reason


@pytest.mark.asyncio
async def test_recorder_keeps_failed_calls_and_closes_idempotently(tmp_path):
    recorder = Recorder(tmp_path / "calls", synthetic=True, echo=False)
    with pytest.raises(RuntimeError, match="injected"):
        await recorder.call("probe", "synthetic", AsyncMock(side_effect=RuntimeError("injected")))
    recorder.close()
    recorder.close()
    assert recorder.calls[0]["status"] == "error"
    assert recorder.calls[0]["seconds"] >= 0


def test_root_search_terminates_outside_repository(tmp_path):
    with pytest.raises(FileNotFoundError):
        repository_root(tmp_path)


def test_reader_prompt_reloads_twice_in_the_same_process(monkeypatch):
    import agents.page_reader as reader
    from research.bench import reload_prompts
    from shared.prompts import Prompts

    original = Prompts.text
    marker = {"value": "first-synthetic-marker"}

    def text(self, name, **kwargs):
        value = original(self, name, **kwargs)
        return value + "\n" + marker["value"] if name == "instruction" else value

    try:
        with monkeypatch.context() as change:
            change.setattr(Prompts, "text", text)
            reload_prompts()
            assert marker["value"] in reader._INSTRUCTION
            marker["value"] = "second-synthetic-marker"
            reload_prompts()
            assert marker["value"] in reader._INSTRUCTION
            assert "first-synthetic-marker" not in reader._INSTRUCTION
    finally:
        reload_prompts()
