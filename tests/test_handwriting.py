"""The simulated hand: what its bytes look like when they leave.

Nothing here pays for a page. The client is replaced, and what is asserted is the image
that would have gone up the wire — which is the only place the defect this covers lived.
"""

from __future__ import annotations

import base64
import io
from types import SimpleNamespace
from typing import Any

import pytest
from PIL import Image

from tools.handwriting import HANDS, asked_of, written_on


def a_page(mode: str) -> bytes:
    """A page the way `agents/page_maker.py` returns one: black lines on white."""
    page = Image.new(mode, (64, 96), 255 if mode == "L" else (255, 255, 255))
    kept = io.BytesIO()
    page.save(kept, format="PNG")
    return kept.getvalue()


@pytest.fixture
def sent(monkeypatch: pytest.MonkeyPatch) -> list[bytes]:
    """The bytes of every page handed to the image endpoint."""
    seen: list[bytes] = []

    def edit(**kwargs: Any) -> Any:
        images = kwargs["image"]
        seen.extend(image.read() for image in (images if isinstance(images, list) else [images]))
        return SimpleNamespace(
            data=[SimpleNamespace(b64_json=base64.b64encode(a_page("RGB")).decode())]
        )

    monkeypatch.setenv("LANTERNINA_FOUNDRY_ACCOUNT_ENDPOINT", "https://example.invalid")
    monkeypatch.setenv("LANTERNINA_FOUNDRY_IMAGE_DEPLOYMENT", "an-image-model")
    monkeypatch.setattr(
        "azure.identity.DefaultAzureCredential", lambda *a, **k: SimpleNamespace(close=lambda: None)
    )
    monkeypatch.setattr("azure.identity.get_bearer_token_provider", lambda *a, **k: str)
    monkeypatch.setattr(
        "openai.AzureOpenAI",
        lambda **k: SimpleNamespace(images=SimpleNamespace(edit=edit), close=lambda: None),
    )
    return seen


def test_a_page_of_one_channel_goes_up_as_three(sent: list[bytes]) -> None:
    """`images/edits` answers a one-channel page with a black rectangle, and the reader
    then reports a sheet nobody wrote on. Measured 7 September 2026."""
    blank = a_page("L")
    assert Image.open(io.BytesIO(blank)).mode == "L"

    written_on(blank)

    assert Image.open(io.BytesIO(sent[0])).mode == "RGB"


def test_a_page_that_is_already_three_channels_is_sent_untouched(sent: list[bytes]) -> None:
    blank = a_page("RGB")
    written_on(blank)
    assert sent[0] == blank


def test_every_hand_has_words() -> None:
    for hand in HANDS:
        assert asked_of(hand).strip()
    with pytest.raises(ValueError):
        asked_of("nobody")


def test_reference_sheets_follow_the_target_and_are_rgb(sent: list[bytes]) -> None:
    target, reference = a_page("RGB"), a_page("L")
    written_on(target, reference_pages=(reference,))
    assert sent[0] == target
    assert len(sent) == 2
    assert Image.open(io.BytesIO(sent[1])).mode == "RGB"
    assert "FIRST image" in asked_of("teenager", references=1)


def test_client_and_credential_close_after_image_error(monkeypatch, sent):
    from unittest.mock import Mock

    credential = Mock()
    client = Mock()
    client.images.edit.side_effect = RuntimeError("synthetic failure")
    monkeypatch.setattr("azure.identity.DefaultAzureCredential", lambda: credential)
    monkeypatch.setattr("openai.AzureOpenAI", lambda **kwargs: client)
    with pytest.raises(RuntimeError, match="synthetic failure"):
        written_on(a_page("L"))
    client.close.assert_called_once()
    credential.close.assert_called_once()
