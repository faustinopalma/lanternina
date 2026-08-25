---
name: 'Orchestrator chokepoints' description: 'Rules for the router, content-safety gate, approval ledger and planner — the three keys and the degradation ladder.' applyTo: 'orchestrator/**'
---

# Orchestrator rules

This package holds the three things nothing else may hold: the model backends, the content-safety sealing key, and the parent-approval sealing key. Concentrating them here is what makes the guarantees checkable.

## Router (`router.py`)

- The only module in the repo that may import an Azure SDK. **No model runs on the device**: if something needs inference, it goes to Foundry through the router. Never add a local runtime — `tests/test_boundaries.py` fails if one is imported anywhere.
- `generate_for_user()` must screen before returning. There is no code path that returns unscreened text to a caller, and no flag that disables screening.
- `analyze()` returns raw text for internal reasoning only. Never hand its output to a display or a proposal payload.
- Must never raise because the cloud is unreachable. Fall back to `CACHED_FALLBACK` (previously approved content) and report the tier and degradation level on every response. Only when the reserve is empty too may it raise `NoCapacityError`.
- Report degradation honestly to the parent panel. Never present degraded output as if it were full capability.
- Redact before sending: prompts may contain `learner_hints`, never a name, id, or history.

## Safety gate (`safety.py`)

- Sole holder of the `CONTENT_SAFETY` sealer. Never pass the sealer or its key outward.
- Called by the router only. If an agent or the panel needs to call it directly, that is a design smell — raise it rather than widening access.
- A `BLOCK` verdict is a normal outcome, not an exception to swallow: log it, fall back, and tell the parent. Never retry until something passes.
- Screen inputs as well as outputs where they are attacker-controlled: parent free text and handwriting-derived text are untrusted.

## Approval ledger (`approval.py`)

- Sole holder of the `PARENT_APPROVAL` sealer. Append-only: corrections are new entries, never edits or deletions of history.
- `decide()` is reachable only from an authenticated parent action in the panel. Never from an agent, a scheduler, a timer, or a "convenience" auto-approve — including in tests outside `tests/`, and including for the demo.
- Withdrawal takes effect before the next delivery. Anything already approved must become undeliverable immediately, not at the next refresh.
- Keep a reserve of approved items for the offline path. If the reserve is empty the system has nothing to fall back to, which is the "dark" state the design forbids.

## Planner

- The only component that may hold more than one agent. It composes them through the protocols in `shared.agents`; it never reaches inside one.
- It may not approve, screen, or render. It sequences work and submits proposals.
- Scheduling is wall-clock and parent-configured. Never schedule based on her past behaviour, and never fire anything triggered by her *inactivity*.
