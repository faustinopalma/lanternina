"""The delivery boundary: the single function that says "this may reach the learner".

Every surface the learner can perceive — e-paper, LCD, printer, sound — must call
:func:`assert_deliverable` immediately before rendering. It re-verifies both chokepoints
from scratch, so a bug anywhere upstream fails closed.

This is deliberately the smallest, most boring module in the repo. Read it in full before
changing it.
"""

from __future__ import annotations

import time

from .approval import ApprovedItem
from .errors import NotApprovedError, SealVerificationError
from .seal import SealPurpose, verify_seal


def assert_deliverable(
    item: ApprovedItem,
    *,
    safety_key: bytes,
    approval_key: bytes,
    now: float | None = None,
) -> None:
    """Raise unless ``item`` is genuinely screened, genuinely approved, and still valid.

    Checks, in order:

    1. the safety seal really covers this payload (content unaltered since screening);
    2. the approval seal really covers this proposal *and* its safety seal, so an
       approved payload cannot be swapped for a different one afterwards;
    3. the approval has not expired.

    Raises:
        SealVerificationError: a seal is missing, forged, or covers different content.
        NotApprovedError: the approval has expired.
    """
    verify_seal(
        item.proposal.payload.seal,
        item.proposal.payload.sealable(),
        safety_key,
        SealPurpose.CONTENT_SAFETY,
    )
    verify_seal(item.seal, item.sealable(), approval_key, SealPurpose.PARENT_APPROVAL)

    expires_at = item.proposal.expires_at
    if expires_at is not None and (now or time.time()) > expires_at:
        raise NotApprovedError(f"approval for proposal {item.proposal.id} expired")


def is_deliverable(item: ApprovedItem, *, safety_key: bytes, approval_key: bytes) -> bool:
    """Non-raising variant, for UI that wants to grey out an item rather than fail."""
    try:
        assert_deliverable(item, safety_key=safety_key, approval_key=approval_key)
    except (SealVerificationError, NotApprovedError):
        return False
    return True
