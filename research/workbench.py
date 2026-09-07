"""Synthetic activity execution. Hardware and elapsed household time are not simulated."""

from __future__ import annotations

import asyncio
import io
import json
import time
from collections.abc import Callable
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any
from unittest.mock import patch

from PIL import Image

from devices.run_experience import came_back
from shared.experience import ASK, Close, Collect, Experience, HandOver, Weight
from shared.routing import PageImage


def repository_root(start: Path) -> Path:
    for candidate in (start.resolve(), *start.resolve().parents):
        if (candidate / "pyproject.toml").is_file() and (candidate / "research").is_dir():
            return candidate
    raise FileNotFoundError("Run this notebook inside the Lanternina repository")


def as_image(png: bytes) -> PageImage:
    with Image.open(io.BytesIO(png)) as image:
        return PageImage(png=png, width=image.width, height=image.height)


class Recorder:
    """Record synthetic prompts, responses and failed calls, never credentials or headers."""

    def __init__(self, folder: Path, *, synthetic: bool, echo: bool = True):
        if not synthetic:
            raise ValueError("This recorder may only retain synthetic material")
        folder.mkdir(parents=True, exist_ok=False)
        self.folder = folder
        self.echo = echo
        self.calls: list[dict[str, Any]] = []
        self._patches: list[Any] = []

    def save(self) -> None:
        (self.folder / "calls.json").write_text(
            json.dumps(self.calls, ensure_ascii=False, indent=2), encoding="utf-8", newline=""
        )

    async def call(self, purpose: str, prompt: str, operation: Callable, *args, **kwargs):
        began = time.perf_counter()
        record: dict[str, Any] = {"purpose": purpose, "sent": prompt, "status": "running"}
        self.calls.append(record)
        if self.echo:
            print(f"\n--- SENT: {purpose} ---\n{prompt}", flush=True)
        try:
            result = await operation(*args, **kwargs)
            record["came"] = getattr(result, "text", None)
            if record["came"] is None:
                body = result if isinstance(result, bytes) else getattr(result, "body", b"")
                record["came"] = f"<{len(body)} bytes>"
            record["status"] = "ok"
            return result
        except BaseException as exc:
            record.update(status="error", error_type=type(exc).__name__, error=str(exc))
            raise
        finally:
            record["seconds"] = round(time.perf_counter() - began, 3)
            self.save()
            if self.echo:
                print(f"--- RETURNED: {purpose} ({record['seconds']} s) ---", flush=True)
                print(record.get("came", record.get("error", "interrupted")), flush=True)

    def start(self) -> None:
        from orchestrator.router import FoundryRouter

        if self._patches:
            raise RuntimeError("Recorder already started")
        for name in ("analyze", "generate_for_user"):
            original = getattr(FoundryRouter, name)

            def wrapped(original):
                async def invoke(router, request):
                    return await self.call(
                        request.purpose, request.prompt, original, router, request
                    )

                return invoke

            replacement = patch.object(FoundryRouter, name, wrapped(original))
            replacement.start()
            self._patches.append(replacement)

    def close(self) -> None:
        for replacement in reversed(self._patches):
            replacement.stop()
        self._patches.clear()
        self.save()


@dataclass
class WalkResult:
    status: str = "running"
    reason: str = ""
    steps: int = 0
    declared_minutes: int = 0
    seconds: float = 0.0
    events: list[dict[str, Any]] = field(default_factory=list)
    pages: dict[str, bytes] = field(default_factory=dict, repr=False)

    def save(self, folder: Path) -> None:
        value = {
            "status": self.status,
            "reason": self.reason,
            "steps": self.steps,
            "declared_minutes": self.declared_minutes,
            "seconds": self.seconds,
            "events": self.events,
            "pages": list(self.pages),
            "scope": "synthetic; local model path; no hardware or household clock",
        }
        (folder / "walk.json").write_text(
            json.dumps(value, ensure_ascii=False, indent=2), encoding="utf-8", newline=""
        )


async def walk(
    experience: Experience,
    *,
    draw: Callable,
    write: Callable,
    read: Callable,
    continue_from: Callable,
    folder: Path,
    max_steps: int = 24,
    blank: bool = False,
    fail_print: bool = False,
    stop_at_collect: bool = False,
    show: Callable = lambda png: None,
) -> WalkResult:
    folder.mkdir(parents=True, exist_ok=True)
    result = WalkResult()
    began = time.perf_counter()
    active = experience.moments
    index = 0
    latest: str | None = None
    available: list[str] = []
    try:
        while result.steps < max_steps:
            moment = active[index]
            result.steps += 1
            weight = moment.at(Weight.STANDARD)
            result.declared_minutes += weight.minutes
            event: dict[str, Any] = {
                "moment": moment.id,
                "act": str(moment.act),
                "lines": list(weight.lines),
                "help": [rung.to_dict() for rung in moment.help],
            }
            result.events.append(event)
            print(f"[{result.steps}] {moment.act}: {moment.heading}", flush=True)
            if isinstance(moment, HandOver):
                latest = None
                if fail_print:
                    event.update(status="fallback", fault="injected print failure")
                else:
                    png, prompt = await draw(moment.page)
                    key = f"{result.steps:02d}-{moment.id}"
                    result.pages[key] = png
                    available.append(key)
                    latest = key
                    (folder / f"{key}.png").write_bytes(png)
                    event.update(status="simulated_print", page=key, prompt=prompt)
                    show(png)
                if latest is None:
                    event["lines"] = list(moment.instead)
            if isinstance(moment, Collect):
                event["available"] = list(available)
                if stop_at_collect:
                    result.status, result.reason = "interrupted", "synthetic stop at collect"
                    break
                if latest is None:
                    target = moment.if_no_page
                    event.update(status="fallback", branch="if_no_page", target=target)
                else:
                    paper = result.pages[latest]
                    references = tuple(result.pages[key] for key in available if key != latest)
                    filled = paper if blank else await write(paper, references)
                    (folder / f"{result.steps:02d}-{moment.id}-filled.png").write_bytes(filled)
                    show(filled)
                    reading = await read(as_image(paper), as_image(filled))
                    event.update(collected=latest, reading=reading.to_dict())
                    came = came_back(reading)
                    if came is None:
                        raise ValueError("The reading is degraded; it is not a blank sheet")
                    target = next(
                        outcome.then for outcome in moment.outcomes if outcome.when == came
                    )
                    event.update(branch=str(came), target=target)
                    if target == ASK:
                        more, _usage = await continue_from(
                            experience=experience.to_dict(),
                            after=moment.id,
                            came=str(came),
                            reading=reading.to_dict(),
                            now=time.time(),
                        )
                        if (
                            more.experience_id != experience.experience_id
                            or more.after != moment.id
                        ):
                            raise ValueError("Continuation belongs to another activity or moment")
                        if not more.requires <= experience.requires:
                            raise ValueError("Continuation requires unavailable equipment")
                        active = more.moments
                        event["continuation"] = more.to_dict()
                        index = 0
                        continue
                index = next(position for position, item in enumerate(active) if item.id == target)
                continue
            if isinstance(moment, Close):
                result.status = "concluded"
                break
            index += 1
        else:
            result.status, result.reason = "interrupted", "step limit reached"
    except Exception as exc:
        result.status, result.reason = "error", f"{type(exc).__name__}: {exc}"
    except BaseException as exc:
        result.status, result.reason = "interrupted", type(exc).__name__
        raise
    finally:
        result.seconds = round(time.perf_counter() - began, 3)
        result.save(folder)
    return result


async def live_activity(
    folder: Path, arguments: dict[str, Any], *, show: Callable = lambda png: None
) -> WalkResult:
    import os
    import secrets

    from agents.page_maker import PageMaker
    from agents.page_reader import PageReader
    from orchestrator.router import FoundryConfig, FoundryRouter
    from orchestrator.safety import AzureContentSafetyGate, ContentSafetyConfig
    from panel.continuing import continue_experience
    from panel.devising import devise_experience
    from shared.agents import AgentContext
    from shared.ids import LearnerId
    from shared.seal import Sealer, SealPurpose
    from tools.handwriting import asked_of, written_on

    recorder = Recorder(folder, synthetic=True)
    gate = AzureContentSafetyGate(
        ContentSafetyConfig.from_env(dict(os.environ)),
        Sealer(SealPurpose.CONTENT_SAFETY, secrets.token_bytes(32), "orchestrator.safety"),
    )
    router = FoundryRouter(FoundryConfig.from_env(dict(os.environ)), gate=gate)
    context = AgentContext(
        router=router, learner_id=LearnerId(""), learner_hints={}, now=time.time()
    )
    built_from: dict[str, str] = {}
    recorder.start()
    began = time.perf_counter()
    try:
        experience, _usage = await devise_experience(
            **arguments, built_from=built_from, now=time.time()
        )
        (folder / "experience.json").write_text(
            json.dumps(experience.to_dict(), ensure_ascii=False, indent=2),
            encoding="utf-8",
            newline="",
        )

        async def draw(page):
            return await PageMaker().draw(context, page)

        async def write(paper, references):
            return await recorder.call(
                "synthetic handwriting",
                asked_of("teenager", references=len(references)),
                asyncio.to_thread,
                written_on,
                paper,
                reference_pages=references,
            )

        async def read(blank, filled):
            return await PageReader().read(
                context, blank=blank, came_back=filled, about=experience.title
            )

        async def continue_from(**kwargs):
            return await continue_experience(**kwargs, pitch=arguments.get("pitch", ""))

        result = await walk(
            experience,
            draw=draw,
            write=write,
            read=read,
            continue_from=continue_from,
            folder=folder,
            show=show,
        )
        verification: dict[str, Any] = {
            "status": result.status,
            "reason": result.reason,
            "built_from": built_from,
        }
        if result.pages:
            png = next(iter(result.pages.values()))
            blank_reading = await read(as_image(png), as_image(png))
            verification["blank_reading"] = blank_reading.to_dict()
        continuations = [event for event in result.events if "continuation" in event]
        prompts = [call["sent"] for call in recorder.calls if "continu" in call["purpose"]]
        descriptions = [
            description for event in continuations for description in event["reading"]["describes"]
        ]
        verification["reading_in_continuation_prompt"] = bool(descriptions) and all(
            any(
                description in prompt or json.dumps(description)[1:-1] in prompt
                for prompt in prompts
            )
            for description in descriptions
        )
        verification["continuations"] = len(continuations)
        verification["seconds"] = round(time.perf_counter() - began, 3)
        (folder / "verification.json").write_text(
            json.dumps(verification, ensure_ascii=False, indent=2), encoding="utf-8", newline=""
        )
        print(json.dumps(verification, ensure_ascii=False, indent=2))
        return result
    except BaseException as exc:
        (folder / "error.json").write_text(
            json.dumps(
                {
                    "type": type(exc).__name__,
                    "error": str(exc),
                    "seconds": round(time.perf_counter() - began, 3),
                }
            ),
            encoding="utf-8",
            newline="",
        )
        raise
    finally:
        await gate.aclose()
        recorder.close()
