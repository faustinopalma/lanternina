"""What the judge made of each afternoon this household was offered.

**Temporary, and here for the weeks the prompts are being changed.** The verdicts are read
in three other places already — `tools/judge_many.py` over a folder in `experiments/`, one
line per afternoon in the workspace, and the trail once an afternoon has begun — and none
of the three shows the words of a verdict on an afternoon that is still waiting for a
decision. Cosmos is not reachable from a laptop, so without this page that verdict is
written and read by nobody. Deleting this is one route module, one section and one block of
words.

It does not settle the question in `ideas/11 §13`. A parent looking at this page can read
*this afternoon gives away its answer* about one they have not decided on yet, which is
exactly the thing `OfferedExperience.to_public` leaves out. That is a property of a
development instrument and not a decision about the product; when the question is answered,
either this page goes or the field goes back into `to_public` and this page becomes
unnecessary.

Read-only, and inert like every other write here is inert: it consults a field that was
written after the afternoon was devised and starts nothing.
"""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Request

from ..experiences import ExperienceStore, OfferedExperience
from ..gate import CurrentAccount

router = APIRouter()


@router.get("/api/verdicts")
def the_readings(account: CurrentAccount, request: Request) -> Any:
    """Every afternoon that has been read back, newest first."""
    store: ExperienceStore = request.app.state.experiences
    rows = [row for row in store.list(str(account.household_id)) if row.verdict]
    rows.sort(key=lambda row: row.created_at, reverse=True)
    return {"verdicts": [_read(row) for row in rows]}


def _read(row: OfferedExperience) -> dict[str, Any]:
    """One reading, with the finding name unpacked from where it was found.

    `agents/experience_judge.py` keeps both in `where`, ahead of a colon, because
    `Complaint` is what a repair loop consumes and giving it a third field for this would
    change a contract six checks depend on. Splitting it here rather than in the browser
    keeps that encoding on this side of the wire.
    """
    verdict = row.verdict
    findings = [one for one in verdict.get("findings") or () if isinstance(one, dict)]
    return {
        "experienceId": row.id,
        "title": row.title,
        "createdAt": row.created_at,
        "state": row.state,
        "begunAt": row.begun_at,
        "prompt": str(verdict.get("prompt") or ""),
        "canBeWrong": bool(verdict.get("can_be_wrong", True)),
        "question": str(verdict.get("question") or ""),
        "answer": str(verdict.get("answer") or ""),
        "degraded": bool(verdict.get("degraded")),
        "findings": [_finding(one) for one in findings],
    }


def _finding(one: dict[str, Any]) -> dict[str, str]:
    name, _, where = str(one.get("where") or "").partition(":")
    return {
        "name": name.strip(),
        "where": where.strip(),
        "says": str(one.get("says") or ""),
    }
