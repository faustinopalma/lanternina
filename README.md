# Lanternina

A home system that generates daily activity — interactive games, printed exercises,
routine prompts — for a teenager with cognitive disabilities, **with her parent steering
it rather than being freed from it**.

It runs on a Linux mini-PC in the house, drives e-paper displays, an LCD, physical buttons
and a printer over ESP32 microcontrollers, and reads completed worksheets back through a
desk camera. Every language and vision model call goes to Azure AI Foundry — **no model
runs on the device**; offline means serving content the parent already approved.

## The point

Software for this situation is either clinical — assuming a diagnosis — or built for small
children, which is humiliating for a teenager. So there is usually nothing, and the whole
load falls on a parent.

Lanternina is not built to reduce that load by removing the parent. **It succeeds if the
parent uses it actively** — reviewing, correcting, deciding what it should offer this week.
Anything an agent produces is a proposal until a parent greenlights it.

Two consequences run through the whole codebase:

- **It never optimises for engagement.** No streaks, no daily goals, no variable rewards,
  no nudges triggered by inactivity, no "time spent" anywhere. For this user, engagement
  optimisation is the easy failure mode and the one that does real harm.
- **Nothing it produces is a judgement about her.** No scores, no grades, no ability
  estimates, no progress trends, no diagnosis-adjacent inference. Vision output describes
  ink on paper; what it means is for her parent to decide.

Read [docs/NON-GOALS.md](docs/NON-GOALS.md) before contributing. It is the most important
file here.

## Documentation

Start with the overview page — one screen, three diagrams, and the numbers that were
actually measured rather than estimated.

| | |
| --- | --- |
| [docs/architecture-overview.html](docs/architecture-overview.html) | **Start here.** The whole system on one page, with diagrams. |
| [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) | Why each boundary exists, and what the design costs. |
| [docs/NON-GOALS.md](docs/NON-GOALS.md) | What will never be built, and why. |
| [docs/THREAT-MODEL.md](docs/THREAT-MODEL.md) | What leaves the device, and what is treated as hostile input. |
| [docs/DEPLOY.md](docs/DEPLOY.md) | Reproducing the cloud tier in your own subscription. |
| [docs/HARDWARE.md](docs/HARDWARE.md) | Hardware reasoning, with what is verified and what is a guess. |

## How the guarantees are enforced

Not by convention — by types, seals and tests, so they survive a fork whose author never
read the docs.

| Guarantee | Mechanism | Test |
| --- | --- | --- |
| Agents cannot approve their own output | `Proposal` has no status field; `AgentContext` holds no ledger | `test_boundaries.py` |
| Generated output cannot skip Content Safety | `Proposal.payload` accepts only `ScreenedPayload`, which the gate signs | `test_delivery.py` |
| Approved content cannot be swapped afterwards | The approval seal covers the safety seal | `test_delivery.py` |
| Only one component talks to a model | Import-level check across every package | `test_boundaries.py` |
| Agents never reach each other | Import-level check | `test_boundaries.py` |
| Full camera frames are never persisted | `RawFrame` refuses to pickle, copy or serialise | `test_boundaries.py` |
| The camera never analyses people | Identifier-level check across `vision/` | `test_boundaries.py` |
| No engagement or assessment vocabulary exists | Identifier-level check across every package | `test_boundaries.py` |

Each of those tests was mutation-checked: a deliberate violation was injected and the test
failed. If you change the design so one no longer holds, please change the product rather
than the test.

## Layout

```
shared/         types and protocols every package depends on; depends on nothing itself
orchestrator/   planner + the three things nothing else may hold:
                  router.py    — the only door to a model backend
                  safety.py    — the only holder of the content-safety key
                  approval.py  — the only holder of the parent-approval key
agents/         one module per agent (content, vision, scheduling, print)
                no agent imports another; the planner composes them
vision/         single-shot capture, ArUco detection, rectification, QR, cell reading
panel/          parent-facing web control surface — the only place approval happens
firmware/       ESP32 code for the e-paper displays, LCD and buttons
docs/           architecture, non-goals, threat model
tests/          the boundary and delivery guarantees above
```

## Setup

Requires Python 3.11+.

```bash
python -m venv .venv
. .venv/bin/activate          # Windows: .venv\Scripts\Activate.ps1
pip install -e ".[dev]"

cp .env.example .env
python -c "import secrets; print(secrets.token_hex(32))"   # run twice
# paste into LANTERNINA_SAFETY_KEY and LANTERNINA_APPROVAL_KEY — two different values

pytest
```

Two different keys matter: sharing one would let the content-safety gate mint parent
approvals. Rotating them invalidates existing approvals by design — the parent re-approves
rather than inheriting state nobody can verify.

Optional extras, installed only where needed:

```bash
pip install -e ".[vision]"    # OpenCV with contrib (ArUco lives there), on the mini-PC
pip install -e ".[cloud]"     # Azure AI Foundry + Content Safety, Entra ID only
pip install -e ".[panel]"     # the parent panel
pip install -e ".[devices]"   # serial link to the ESP32s
```

## Status

Early scaffolding. The contracts, the seals, the delivery boundary and the tests are
written and green. The router, agents, vision pipeline, panel and firmware are **not
written yet** — see the table at the end of [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md).

Stubs raise `NotImplementedError` or return obviously fake data. Nothing in this repository
pretends to work.

## Privacy

No personal data is in this repository and none should ever be added — not in fixtures,
tests, screenshots or example configuration. Demo material is synthetic.

At runtime, only two things leave the device: content-generation prompts and rectified page
crops. No full camera frames, no identifiers, no profile, no history. See
[docs/THREAT-MODEL.md](docs/THREAT-MODEL.md).

## Licence

[MIT](LICENSE). If you fork it and remove the constraints in
[docs/NON-GOALS.md](docs/NON-GOALS.md), please call it something else.
