"""Synthesize durable parent feedback without overwriting concurrent edits."""

from __future__ import annotations

import hashlib
import json
import logging
import os
from typing import Any

from shared.ids import new_id, new_request_id
from shared.prompts import beside
from shared.routing import Capability, ModelRequest
from shared.safety import ContentKind
from shared.steering import MAX_SUMMARY_CHARS, clean_text

from .steering import REASONS, Guidance, SteeringConflict, SteeringStore
from .usage import FAILED, KIND_TEXT, SERVED, at_the_limit, event_from

SAYS = beside(__file__)


def summary_prompt(value: Guidance, language: str) -> str:
    return (
        SAYS.text("instruction", limit=MAX_SUMMARY_CHARS)
        + "\n"
        + json.dumps(
            {
                "language": language,
                "parentInstructions": value.steering.instructions,
                "currentSummary": value.steering.adaptive,
                "newFeedback": [entry.to_dict() for entry in value.pending],
                "reasonMeanings": REASONS,
            },
            ensure_ascii=False,
        )
    )


async def summarize(value: Guidance, language: str) -> tuple[str, Any]:
    from orchestrator.router import FoundryConfig, FoundryRouter

    router = FoundryRouter(FoundryConfig.from_env(dict(os.environ)))
    response = await router.analyze(
        ModelRequest(
            capability=Capability.PLANNING,
            prompt=summary_prompt(value, language),
            request_id=new_request_id(),
            kind=ContentKind.TEXT,
        )
    )
    text = clean_text(response.text, MAX_SUMMARY_CHARS)
    if not text:
        raise ValueError("empty guidance summary")
    return text, router.last_usage


async def synthesize_pending(
    *,
    store: SteeringStore,
    preferences: Any,
    usage: Any,
    limits: Any,
    configured: float,
    household_id: str,
) -> None:
    for _attempt in range(3):
        language = preferences.get(household_id).language
        current = store.get(household_id, language)
        if not current.pending or at_the_limit(usage, limits, household_id, configured):
            return
        spent = None
        outcome = FAILED
        try:
            text, spent = await summarize(current, language)
            outcome = SERVED
            try:
                store.save(current.summarized(text), current.revision)
            except SteeringConflict:
                continue
            return
        except Exception as exc:  # noqa: BLE001
            logging.getLogger(__name__).warning("guidance synthesis failed: %s", type(exc).__name__)
            return
        finally:
            try:
                usage.record(
                    event_from(household_id, KIND_TEXT, outcome, spent, event_id=str(new_id("use")))
                )
            except Exception as exc:  # noqa: BLE001
                logging.getLogger(__name__).warning("guidance usage failed: %s", type(exc).__name__)


def record_feedback(
    request: Any, household: str, row: Any, reasons: list[str], comment: str
) -> None:
    from .steering import clean_feedback

    store: SteeringStore = request.app.state.steering
    language = request.app.state.preferences.get(household).language
    identifier = hashlib.sha256(
        json.dumps([row.id, sorted(set(reasons)), comment.strip()], ensure_ascii=False).encode()
    ).hexdigest()
    feedback = clean_feedback(identifier, row.id, row.title, reasons, comment)
    for _attempt in range(3):
        current = store.get(household, language)
        try:
            store.save(current.receive(feedback), current.revision)
            return
        except SteeringConflict:
            continue
    raise SteeringConflict("guidance_changed")
