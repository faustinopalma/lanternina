"""Parent-only editing and retry of activity guidance."""

from __future__ import annotations

from typing import Any, Literal

from fastapi import APIRouter, BackgroundTasks, HTTPException, Request
from pydantic import BaseModel, ConfigDict, Field

from ..gate import CurrentAccount
from ..steering import SteeringConflict, SteeringStore

router = APIRouter()


class EditSteering(BaseModel):
    model_config = ConfigDict(extra="forbid")
    revision: int = Field(ge=0)
    instructions: str | None = None
    conduct: str | None = None
    review: str | None = None
    adaptive: str | None = None
    action: Literal[
        "save", "reset_adaptive", "restore_instructions", "restore_conduct", "restore_review"
    ] = "save"


@router.get("/api/steering")
def read_steering(account: CurrentAccount, request: Request) -> Any:
    household = str(account.household_id)
    language = request.app.state.preferences.get(household).language
    return request.app.state.steering.get(household, language).to_public(language)


@router.post("/api/steering")
def write_steering(new: EditSteering, account: CurrentAccount, request: Request) -> Any:
    from dataclasses import replace

    from shared.steering import Steering

    household = str(account.household_id)
    language = request.app.state.preferences.get(household).language
    store: SteeringStore = request.app.state.steering
    current = store.get(household, language)
    try:
        if new.action == "reset_adaptive":
            chosen = current.reset_adaptive(language)
        elif new.action.startswith("restore_"):
            field = new.action.removeprefix("restore_")
            chosen = replace(
                current,
                steering=replace(
                    current.steering, **{field: getattr(Steering.initial(language), field)}
                ),
            )
        else:
            chosen = current.edited(
                current.steering.instructions if new.instructions is None else new.instructions,
                current.steering.adaptive if new.adaptive is None else new.adaptive,
                conduct=new.conduct,
                review=new.review,
            )
        return store.save(chosen, new.revision).to_public(language)
    except SteeringConflict as exc:
        raise HTTPException(status_code=409, detail="guidance_changed") from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.post("/api/steering/synthesize")
def retry_synthesis(account: CurrentAccount, request: Request, afterwards: BackgroundTasks) -> Any:
    schedule_synthesis(afterwards, request, str(account.household_id))
    return {"queued": True}


def schedule_synthesis(afterwards: BackgroundTasks, request: Request, household: str) -> None:
    from ..steering_summary import synthesize_pending

    afterwards.add_task(
        synthesize_pending,
        store=request.app.state.steering,
        preferences=request.app.state.preferences,
        usage=request.app.state.usage,
        limits=request.app.state.limit,
        configured=request.app.state.settings.monthly_limit,
        household_id=household,
    )
