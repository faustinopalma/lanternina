"""A returned page reaches the continuation as material, without its diagnostic metadata."""

from __future__ import annotations

import json

from agents.experience_continuer import _ink, the_prompt
from shared.vision_contracts import WhatCameBack


def test_current_reader_descriptions_reach_the_continuation_prompt() -> None:
    reading = WhatCameBack(
        written=True,
        same_sheet=True,
        describes=("Una freccia unisce il porto alla torre.", "La nota dice: il ponte cede."),
        read_at=123456.0,
        metadata={"request_id": "private-diagnostic-id"},
    )
    prompt = the_prompt(experience={}, after="scan", came="marks", reading=reading.to_dict())

    for description in reading.describes:
        assert json.dumps(description, ensure_ascii=False) in prompt
    assert "private-diagnostic-id" not in prompt
    assert "123456" not in prompt


def test_blank_current_reading_preserves_its_status() -> None:
    reading = WhatCameBack(written=False, same_sheet=True, describes=(), read_at=1.0)
    material = _ink(reading.to_dict())

    assert material["written"] is False
    assert material["describes"] == []


def test_legacy_cells_remain_readable() -> None:
    material = _ink({"cells": [{"label": "Percorso", "value": "porto"}]})

    assert material == [{"place": "Percorso", "ink": "marks"}]