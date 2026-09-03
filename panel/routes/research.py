"""Every research run there has been, oldest first.

**Temporary, and beside `panel/routes/verdicts.py` for the same reason.** `research/` is an
apparatus and not part of the product: it devises afternoons with the real prompts, plays
them against a model standing in for an adolescent, and gives each of eight axes a number
from 1 to 5. Its runs are committed, so the history is a file rather than a query — and
until this route existed it could only be read by opening JSON in an editor.

Nothing here is about a household. The six households in `research/households.py` are
invented, the transcripts are two models talking to each other, and what this serves is the
means of eight axes over two dozen afternoons apiece. The vocabulary of assessment is
allowed in `research/` and not in this package — `tests/test_boundaries.py` draws that line
and it has no exceptions — so the file this reads is named there and the names here are not.

The file is built by `research/scores.py` from the run directories, which are the
definition; if the two disagree the directories are right. Only that one file is shipped:
the transcripts beside it are 200 kB a run and belong nowhere near the product image.
"""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any

from fastapi import APIRouter, Request

from ..gate import CurrentAccount

router = APIRouter()

# `panel/routes/x.py` → the repository root in development, `/app` in the image.
HISTORY = Path(__file__).resolve().parents[2] / "research" / "scores.json"


@router.get("/api/research")
def the_runs(account: CurrentAccount, _: Request) -> Any:
    """Every run there has been. Empty when the file was not shipped, never an error."""
    del account
    return {"runs": _history()}


def _history() -> list[dict[str, Any]]:
    if not HISTORY.is_file():
        return []
    try:
        rows = json.loads(HISTORY.read_text(encoding="utf-8"))
    except ValueError as exc:
        logging.getLogger(__name__).warning("the run history is not readable: %s", exc)
        return []
    return [_one(row) for row in rows if isinstance(row, dict)]


def _one(row: dict[str, Any]) -> dict[str, Any]:
    """One run. `prompt` is empty on the three from 29 August, which predate fingerprints."""
    axes = row.get("axes") if isinstance(row.get("axes"), dict) else {}
    endings = row.get("endings") if isinstance(row.get("endings"), dict) else {}
    return {
        "run": str(row.get("run") or ""),
        "at": str(row.get("at") or ""),
        "label": str(row.get("label") or ""),
        "prompt": str(row.get("prompt") or ""),
        "afternoons": int(row.get("afternoons") or 0),
        "refused": int(row.get("refused") or 0),
        "minutes": float(row.get("minutes") or 0.0),
        "endings": {str(k): int(v or 0) for k, v in endings.items()},
        "axes": {str(k): float(v) for k, v in axes.items() if isinstance(v, (int, float))},
    }
