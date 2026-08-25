"""Contracts shared by every other package in the monorepo.

``shared`` is the only package that all others may import. It contains **types and
protocols only** — no I/O, no model calls, no side effects. The dependency rule is
one-directional:

    orchestrator ─┐
    agents      ──┼──▶ shared
    vision      ──┤
    panel       ──┘

Nothing in ``shared`` may import ``orchestrator``, ``agents``, ``vision`` or ``panel``,
and no agent may import another agent. See docs/ARCHITECTURE.md.

Three invariants are expressed as *types* here, so that violating them is a type error
or a runtime seal-verification failure rather than a code-review oversight:

1. Model output that can reach the user exists only as :class:`~shared.safety.ScreenedPayload`.
2. Agent output exists only as :class:`~shared.proposal.Proposal` — there is no field an
   agent could set to mark its own work approved.
3. Delivery to the user requires an :class:`~shared.approval.ApprovedItem` carrying two
   valid seals (safety + parent approval).

:mod:`shared.vision_contracts` used to carry a fourth, restricting what an image could be.
It no longer holds: see that module.
"""

from __future__ import annotations

__all__ = [
    "agents",
    "approval",
    "blueprint",
    "capabilities",
    "delivery",
    "domain",
    "errors",
    "ids",
    "proposal",
    "routing",
    "safety",
    "seal",
    "sheet",
    "vision_contracts",
]
