"""The home server's half of the loop: what comes back from the cloud must still verify.

The risk this covers is quiet: the payload travels to Cosmos as JSON and comes back as
JSON, and any change to how it is serialised would break the digest the safety seal
covers. That failure would look like "the display stopped updating", far from its cause.
"""

from __future__ import annotations

import base64
import json
import time
from io import BytesIO

import pytest
from PIL import Image

from devices.epaper import render_picture_bmp
from orchestrator.safety import AzureContentSafetyGate, ContentSafetyConfig
from shared.delivery import assert_deliverable, is_deliverable
from shared.safety import ContentKind, SafetyCategory, ScreenedPayload
from shared.seal import Sealer, SealPurpose
from tools.home_server import _approved_item, _picture_item

SAFETY_KEY = b"safety-key-for-tests"
APPROVAL_KEY = b"approval-key-for-tests"


def _gate() -> AzureContentSafetyGate:
    async def analyzer(text: str) -> dict[SafetyCategory, int]:
        return {SafetyCategory.HATE: 0, SafetyCategory.VIOLENCE: 0}

    return AzureContentSafetyGate(
        ContentSafetyConfig(endpoint="https://example.invalid"),
        Sealer(SealPurpose.CONTENT_SAFETY, SAFETY_KEY, "test-gate"),
        analyzer=analyzer,
        image_analyzer=analyzer,
    )


async def _screened(body: str) -> ScreenedPayload:
    return await _gate().screen(ContentKind.ROUTINE_PROMPT, body)


async def _screened_image(body: str) -> ScreenedPayload:
    return await _gate().screen(ContentKind.IMAGE_PNG, body)


def _row(payload: ScreenedPayload) -> dict[str, object]:
    """Exactly what the panel stores and hands back, including the JSON round trip."""
    return json.loads(
        json.dumps(
            {
                "id": "pr_roundtrip",
                "kind": "routine_prompt",
                "agent": "content",
                "rationale": "promemoria della sera",
                "createdAt": 1.0,
                "payload": payload.sealable(),
                "payloadSeal": payload.seal.to_dict(),
                "decidedBy": "ac_parent",
                "decidedAt": time.time(),
            }
        )
    )


async def test_an_approved_proposal_survives_the_cloud_round_trip() -> None:
    payload = await _screened("Verso le 17:30, puoi sistemare lo zaino.")
    item = _approved_item(_row(payload), APPROVAL_KEY)
    assert_deliverable(item, safety_key=SAFETY_KEY, approval_key=APPROVAL_KEY)
    assert item.proposal.payload.body.startswith("Verso le 17:30")


async def test_content_altered_in_the_cloud_is_refused_at_the_device() -> None:
    """The cloud stores the record; it cannot change the words without being caught."""
    payload = await _screened("Verso le 17:30, puoi sistemare lo zaino.")
    row = _row(payload)
    row["payload"]["body"] = "vai a letto subito"  # type: ignore[index]

    item = _approved_item(row, APPROVAL_KEY)
    assert not is_deliverable(item, safety_key=SAFETY_KEY, approval_key=APPROVAL_KEY)


async def test_a_seal_from_another_key_does_not_pass() -> None:
    """The approval key stays on the device, so a cloud-minted seal is worth nothing."""
    payload = await _screened("Verso le 11, puoi bere un bicchiere d'acqua.")
    item = _approved_item(_row(payload), b"a-key-the-device-does-not-have")
    assert not is_deliverable(item, safety_key=SAFETY_KEY, approval_key=APPROVAL_KEY)


async def test_a_picture_is_rendered_at_the_panel_size_and_depth() -> None:
    picture = Image.new("L", (1536, 1024))
    for x in range(1536):  # a gradient, so the dither has something to work with
        for y in range(0, 1024, 8):
            picture.putpixel((x, y), x % 256)
    buffer = BytesIO()
    picture.save(buffer, format="PNG")

    payload = await _screened_image(base64.b64encode(buffer.getvalue()).decode())
    item = _picture_item(payload, "prova", APPROVAL_KEY)
    rendered = Image.open(
        BytesIO(render_picture_bmp(item, safety_key=SAFETY_KEY, approval_key=APPROVAL_KEY))
    )

    assert rendered.size == (800, 480)
    assert rendered.mode == "1"
    assert rendered.format == "BMP"


async def test_a_sentence_is_not_a_picture() -> None:
    """The renderers are not interchangeable: text dithered would only be blurred."""
    payload = await _screened("Verso le 17:30, puoi sistemare lo zaino.")
    item = _approved_item(_row(payload), APPROVAL_KEY)
    with pytest.raises(ValueError):
        render_picture_bmp(item, safety_key=SAFETY_KEY, approval_key=APPROVAL_KEY)
