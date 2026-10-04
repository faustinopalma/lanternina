"""Write and review standalone instructions against the activity that will run."""

from __future__ import annotations

import asyncio
import base64
import io
import json
from typing import Any, Literal

from PIL import Image
from pydantic import BaseModel, ConfigDict, Field, model_validator

from shared.agents import AgentContext
from shared.ids import new_request_id
from shared.page import Page
from shared.prompts import beside
from shared.routing import Capability, ModelRequest, PageImage
from shared.safety import ContentKind

SAYS = beside(__file__)


class Diagram(BaseModel):
    model_config = ConfigDict(extra="forbid")
    kind: Literal["grid", "table"]
    columns: int = Field(default=1, ge=1, le=24)
    row_count: int = Field(default=1, ge=1, le=24)
    split_at: int = Field(default=0, ge=0, le=24)
    labels: list[str] = Field(default_factory=list, max_length=8)
    rows: list[list[str]] = Field(default_factory=list, max_length=20)

    @model_validator(mode="after")
    def consistent(self) -> Diagram:
        if self.kind == "grid" and (self.split_at > self.columns or not self.labels):
            raise ValueError("a grid needs valid zone boundaries and explicit labels")
        if self.kind == "table":
            if not self.rows or not 1 <= len(self.rows[0]) <= 6:
                raise ValueError("a table needs one to six columns")
            if any(len(row) != len(self.rows[0]) for row in self.rows):
                raise ValueError("every table row needs the same number of cells")
        return self


class Draft(BaseModel):
    model_config = ConfigDict(extra="forbid")
    language: Literal["it", "en"]
    paragraphs: list[str] = Field(min_length=1, max_length=12)
    steps: list[str] = Field(min_length=1, max_length=16)
    note: list[str] = Field(default_factory=list, max_length=8)
    field_coverage: list[str]
    diagram: Diagram | None = None
    illustration: bool = False
    asset_blockers: list[str]


class Review(BaseModel):
    model_config = ConfigDict(extra="forbid")
    text_pass: bool
    issues: list[str]
    asset_blockers: list[str]


async def prepare(
    context: AgentContext, page: Page, plan: dict[str, Any], *, gate: Any,
    trace: list[dict[str, Any]], usages: list[Any],
) -> tuple[dict[str, Any], bytes | None]:
    material = json.dumps({"page": page.to_dict(), "plan": plan}, ensure_ascii=False)
    prompt = SAYS.text("write") + "\nSOURCE DATA\n" + material

    async def call(text: str, purpose: str, images: tuple[PageImage, ...] = ()) -> str:
        response = await asyncio.wait_for(context.router.analyze(ModelRequest(
            capability=Capability.PLANNING, prompt=text, request_id=new_request_id(),
            purpose=purpose, max_output_chars=24000, content_kind=ContentKind.PLAIN_TEXT,
            images=images,
        )), timeout=240)
        usages.append(getattr(context.router, "last_usage", None))
        trace.append({"purpose": purpose, "prompt": text, "response": response.text,
                      "truncated": response.truncated})
        if response.truncated:
            raise ValueError("document response was truncated")
        return response.text

    for attempt in range(2):
        raw = await call(prompt, "writing printable instructions")
        try:
            draft = Draft.model_validate_json(raw)
            labels = [space.label for space in page.spaces]
            printed = "\n".join(draft.paragraphs + draft.steps + draft.note)
            if draft.field_coverage != labels or any(label not in printed for label in labels):
                raise ValueError("instructions must name and explain every response field")
            if draft.diagram is not None and draft.illustration:
                raise ValueError("a diagram replaces the decorative illustration")
            image = None
            if draft.illustration:
                asked = SAYS.text("illustration") + "\nSUBJECT\n" + page.illustration
                payload = await context.router.generate_for_user(ModelRequest(
                    capability=Capability.IMAGE_GENERATION, prompt=asked,
                    request_id=new_request_id(), purpose="printable illustration",
                    content_kind=ContentKind.IMAGE_PNG, metadata={"size": "1024x1536"},
                ))
                usages.append(getattr(context.router, "last_usage", None))
                image = base64.b64decode(payload.body, validate=True)
                trace.append({"purpose": "printable illustration", "prompt": asked})
            review_prompt = SAYS.text("review") + "\nSOURCE DATA\n" + material
            review_prompt += "\nCANDIDATE\n" + draft.model_dump_json()
            images = ()
            if image:
                with Image.open(io.BytesIO(image)) as picture:
                    images = (PageImage(png=image, width=picture.width, height=picture.height),)
            review = Review.model_validate_json(await call(
                review_prompt, "reviewing printable instructions", images,
            ))
            if (
                not review.text_pass or review.issues
                or review.asset_blockers or draft.asset_blockers
            ):
                raise ValueError(json.dumps({"review": review.model_dump(),
                                             "assets": draft.asset_blockers}))
            source = {"version": 1, "title": page.title, "spaces": [
                space.to_dict() for space in page.spaces], **draft.model_dump()}
            words = [page.title, *draft.paragraphs, *draft.steps, *draft.note, *labels]
            if draft.diagram:
                words.extend(draft.diagram.labels)
                words.extend(cell for row in draft.diagram.rows for cell in row)
            await gate.screen(ContentKind.PLAIN_TEXT, "\n".join(words),
                              context="final printable document strings")
            return source, image
        except ValueError as exc:
            if attempt == 1:
                raise ValueError(f"document needs content review: {exc}") from exc
            prompt += "\nPREVIOUS CANDIDATE\n" + raw + "\nREPAIR\n" + str(exc)
    raise AssertionError("bounded document preparation ended without a result")