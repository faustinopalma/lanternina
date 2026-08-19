# Lanternina

A home system that offers activities to an adolescent — sheets to print, short games on two
buttons, and reminders on an e-paper display. A parent steers it, and the design does not
try to remove that role.

It runs on a Linux mini-PC in the house. Today it serves two e-paper displays and draws
sheets for a printer; reading a finished sheet back has been done end to end from the
command line and is not yet a package. Every language and vision model call goes to Azure AI
Foundry. No model runs on the device, and offline means serving what the parent has already
approved.

## Who it is for

Any adolescent. What holds someone's interest differs, how much novelty they want differs,
and how much text on a page is comfortable differs — across the whole range of cognitive
ability, and at both ends of it. None of that requires a diagnosis, and Lanternina does not
ask for one: it has no notion of a condition, a need or a level, and nowhere to record one.

## What it remembers, and what it refuses to infer

Lanternina keeps a memory and works from it, so nobody restates the same things every week.
The memory holds what the household chose — subjects to offer, subjects to avoid, the form
of the material, how much variety, words per line, the content language — and what has
already been produced, shown and approved. Generation runs against that memory, and varies
topics and formats within it without being asked each time.

The limit sits next to the claim. That memory is made of what was chosen and what was
already offered. It is not made of how anybody did. Nothing here scores an answer, estimates
an ability, tracks a trend, ranks anything or infers boredom or attention — not in the
types, the storage, the prompts, the logs or the screen. What the camera reports is ink on
paper: cell 3 is empty. What that means is for the household to say, not for the system to
conclude.

That is a tradeoff, and it costs something. A system that scored answers could tune itself
faster and would need the parent less. This one asks the parent instead, because a wrong
conclusion about a person is paid for by the person.

## The parent steers

Anything an agent produces is a proposal until a parent approves it. The parent writes the
settings, reviews what was generated, refuses what does not fit, and decides what the system
should offer this week. No feature is built whose value is that the parent no longer has to
think about something.

## The dashboard is inert

Adding material or changing a setting only stores the new state. It does not generate
content, enqueue work, notify a device or make anything happen immediately. The server in
the home decides when to ask for work, and it is free to look later or to decline. Its
request may stay open while the cloud scales from zero; nobody is waiting in front of a
screen for it.

## Two consequences that run through the code

- It does not optimise for engagement. No streaks, no daily goals, no variable rewards, no
  nudge triggered by inactivity, no "time spent" anywhere. Engagement optimisation is easy
  to add here and would do harm, which is why it is a written rule rather than a matter of
  judgement.
- Nothing it produces is a judgement about a person. No scores, no grades, no ability
  estimates, no progress trends, no inference adjacent to a diagnosis.

[docs/NON-GOALS.md](docs/NON-GOALS.md) lists what will never be built, and why. It is worth
reading before contributing.

## Documentation

The overview page is the shortest route in: one screen, three diagrams, and each number
marked as measured or estimated.

| | |
| --- | --- |
| [docs/architecture-overview.html](docs/architecture-overview.html) | The whole system on one page, with diagrams. Start here. |
| [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) | Why each boundary exists, and what the design costs. |
| [docs/NON-GOALS.md](docs/NON-GOALS.md) | What will never be built, and why. |
| [docs/THREAT-MODEL.md](docs/THREAT-MODEL.md) | What leaves the device, and what is treated as hostile input. |
| [docs/DEPLOY.md](docs/DEPLOY.md) | Reproducing the cloud tier in your own subscription. |
| [docs/HARDWARE.md](docs/HARDWARE.md) | Hardware reasoning, with what is verified and what is a guess. |
| [ideas/](ideas/) | What is not built, ranked, each entry with its cost and a check somebody else can run. |

## How the guarantees are enforced

By types, seals and tests rather than by convention, so that removing one is a deliberate
change rather than an omission.

| Guarantee | Mechanism | Test |
| --- | --- | --- |
| Agents cannot approve their own output | `Proposal` has no status field; `AgentContext` holds no ledger | `test_boundaries.py` |
| Generated output cannot skip Content Safety | `Proposal.payload` accepts only `ScreenedPayload`, which the gate signs | `test_delivery.py` |
| Approved content cannot be swapped afterwards | The approval seal covers the safety seal | `test_delivery.py` |
| Only one component talks to a model | Import-level check across every package | `test_boundaries.py` |
| Agents never reach each other | Import-level check | `test_boundaries.py` |
| Full camera frames are never persisted | `RawFrame` refuses to pickle, copy or serialise | `test_boundaries.py` |
| The camera never analyses people | Identifier-level check across `vision/` | `test_boundaries.py` |
| No engagement or assessment vocabulary exists | Identifier-level check across every package, and a text check across the panel | `test_boundaries.py` |
| The content language is a setting, not a property of the data | Field names are English; two readers may name the old Italian keys, nothing else | `test_boundaries.py` |

Each of those tests was mutation-checked: a deliberate violation was injected and the test
was watched to fail. If you change the design so one no longer holds, please change the
product rather than the test.

## Layout

```text
shared/         types and protocols every package depends on; depends on nothing itself
orchestrator/   planner + the three things nothing else may hold:
                  router.py    — the only door to a model backend
                  safety.py    — the only holder of the content-safety key
                  approval.py  — the only holder of the parent-approval key
agents/         one module per agent; no agent imports another
vision/         single-shot capture, ArUco detection, rectification, QR, cell reading
printing/       the sheet renderer: markers, QR and cell outlines at exact millimetres
panel/          the parent-facing API — the only place approval happens
web/            the panel in the browser, a React single-page application
devices/        what runs in the house: display server, picture pull, status push
tools/          the home server, and the command-line paths that are not a package yet
infra/          the cloud tier as Bicep; deploy/ is the mini-PC side
docs/           architecture, non-goals, threat model, hardware
ideas/          what is not built, ranked, with costs
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

Parts of this are running in a house; parts do not exist. The full table is at the end of
[docs/ARCHITECTURE.md](docs/ARCHITECTURE.md), and it is kept honest rather than encouraging.

Running: the cloud tier, the parent panel and its API, the content agent, the model router
with real credentials, the safety gate, the hub services that serve the displays and pull an
hourly picture, the picture archive, and usage accounting with a per-household cap. The
sheet renderer is written and was checked on paper — a 50 mm ruler measures 50 mm.

Not written: the planner, the vision, scheduling and print agents, and `vision/` as a
package — that logic lives in `tools/` and has read one scanned sheet end to end.
`firmware/` may stay empty: the displays run stock firmware and the hub serves them.

Stubs raise `NotImplementedError` or return obviously fake data. Nothing in this repository
pretends to work.

## Privacy

No personal data is in this repository and none should ever be added — not in fixtures,
tests, screenshots or example configuration. Demo material is synthetic.

At runtime, only two things leave the device: content-generation prompts and rectified page
crops. No full camera frames, no identifiers, no profile, no history, and no name in a
prompt. See [docs/THREAT-MODEL.md](docs/THREAT-MODEL.md).

## Licence

[MIT](LICENSE). If you fork it and remove the constraints in
[docs/NON-GOALS.md](docs/NON-GOALS.md), please call it something else.
