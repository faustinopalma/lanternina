"""Typed identifiers.

`NewType` over `str` gives static separation (a `SheetId` cannot be passed where an
`ExerciseId` is expected) with zero runtime cost.
"""

from __future__ import annotations

import secrets
from typing import NewType

LearnerId = NewType("LearnerId", str)
ExerciseId = NewType("ExerciseId", str)
SheetId = NewType("SheetId", str)
CellId = NewType("CellId", str)
ProposalId = NewType("ProposalId", str)
SessionId = NewType("SessionId", str)
RequestId = NewType("RequestId", str)
RoutineId = NewType("RoutineId", str)
BlueprintId = NewType("BlueprintId", str)

# A household is what the cloud knows about. It is deliberately NOT a LearnerId: the
# mapping from a household to a real person exists only on the device in the home.
HouseholdId = NewType("HouseholdId", str)
AccountId = NewType("AccountId", str)

_ID_BYTES = 8


def new_id(prefix: str) -> str:
    """Return a short, collision-resistant, human-greppable id such as ``ex_9f2c1a4b``."""
    return f"{prefix}_{secrets.token_hex(_ID_BYTES // 2)}"


def new_exercise_id() -> ExerciseId:
    return ExerciseId(new_id("ex"))


def new_sheet_id() -> SheetId:
    return SheetId(new_id("sh"))


def new_proposal_id() -> ProposalId:
    return ProposalId(new_id("pr"))


def new_session_id() -> SessionId:
    return SessionId(new_id("se"))


def new_request_id() -> RequestId:
    return RequestId(new_id("rq"))


def new_household_id() -> HouseholdId:
    return HouseholdId(new_id("hh"))


def new_account_id() -> AccountId:
    return AccountId(new_id("ac"))


def new_blueprint_id() -> BlueprintId:
    return BlueprintId(new_id("bp"))
