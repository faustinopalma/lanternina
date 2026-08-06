# Architecture

This document explains the boundaries in the codebase and **why each one exists**. The
"why" matters more than the "what": the constraints here are unusual, and without the
reasoning the next person will file them as ceremony and route around them.

Read [NON-GOALS.md](NON-GOALS.md) first. This document describes how the code makes those
non-goals structural rather than aspirational.

---

## 1. Shape

```
┌─────────────────────────────────────────────────────────────────────┐
│ Linux mini-PC (local orchestrator)                                  │
│                                                                     │
│   panel/  ──── parent decides ────┐                                 │
│                                   ▼                                 │
│   agents/ ──proposals──▶ orchestrator/approval.py ──approved──┐     │
│      │                          (ledger, key #2)              │     │
│      │ router only                                            ▼     │
│      ▼                                                 shared/      │
│   orchestrator/router.py ──▶ orchestrator/safety.py    delivery.py  │
│      │  (the only model door)     (gate, key #1)       verifies     │
│      │                                                        │     │
│   vision/ ── rectified page ──────────────────────────────────┘     │
│      ▲                                                        │     │
└──────┼────────────────────────────────────────────────────────┼─────┘
       │ single shot, button press                              ▼
   desk camera                                    e-paper / LCD / printer
                                                                 
       └────────────── only prompts + page crops ──────────▶ Azure AI Foundry
```

`shared/` holds types and protocols and nothing else. Everything else depends on it; it
depends on nothing. No agent imports another agent.

## 2. Why a single model router

`orchestrator/router.py` is the only module permitted to import an Azure SDK. No module
anywhere may import a local model runtime — there is no on-device inference. Everyone else
receives a `ModelRouter` protocol.

Concentrating it buys three things that are hard to get otherwise:

- **Screening cannot be routed around.** If any component could construct its own client,
  the content-safety chokepoint would be one forgotten call away from being bypassed.
- **Degradation is uniform.** The fallback ladder lives in one place instead of being
  re-implemented, differently and worse, at each call site.
- **Redaction is uniform.** The rule "her name never enters a prompt" is enforceable when
  there is one function that builds prompts.

The router exposes two methods with deliberately different return types:

| Method | Returns | For |
| --- | --- | --- |
| `generate_for_user()` | `ScreenedPayload` | anything she will see — screened and sealed on the way out |
| `analyze()` | `ModelResponse` | internal reasoning only; its text cannot enter a `Proposal` |

That difference is not stylistic. `Proposal.payload` is typed `ScreenedPayload`, so raw
model output is *structurally* unable to reach a user-facing path.

### Degradation: reduced, never dark

```
CLOUD_FOUNDRY  ──unreachable──▶  CACHED_FALLBACK
   full                            cached only
```

**No model runs on the device.** Every LLM and vision call goes to Azure AI Foundry; the
mini-PC runs conventional code only — OpenCV, the panel, the serial link. That is a
deliberate choice: one inference path instead of two, no model weights to ship or update,
no second set of failure modes, and a device small enough to be powered over Ethernet.

`DegradationLevel` has no "unavailable" member. Going dark is not a state the type system
can express, because for this user an unexplained dead device is worse than a simpler
activity. The router never raises because the cloud is down; it reports which tier served
the request and whether capability is reduced, and the parent panel shows it.

The consequence is sharper than it looks: `CACHED_FALLBACK` serves **previously approved**
content, and it is now the *only* offline path. If the parent has approved nothing in
reserve, "never dark" is a promise with nothing behind it. Keeping a reserve stocked is a
product requirement, not an implementation detail.

Reading degrades the same way. Without the cloud, only the cell kinds in
`sheet.LOCALLY_READABLE` — filled checkboxes and choice boxes, which are ink-coverage
measurements OpenCV can do on its own — are attempted. Handwriting is marked
`needs_review` rather than guessed.

## 3. Why content safety is a type, not a call

The rule is "every generated output passes Content Safety". Implemented as a call each
agent makes, that rule survives until someone adds an agent in a hurry.

Instead, the gate is the only thing that produces `ScreenedPayload`, and it **signs** what
it produces (`shared/seal.py`). Anything user-facing accepts only that type. There is no
user-facing type in `shared/` with a bare `str` field, and adding one is the single easiest
way to break this design — so don't.

A `BLOCK` verdict is a normal outcome, not an exception to swallow. The system falls back
and tells the parent; it never retries until something slips through.

## 4. Why agents can only propose

Agents return `Proposal`. Look at what `Proposal` does *not* have: no `status`, no
`approved`, no `publish()`. An agent has nowhere to record that its own output is
acceptable — not because it is trusted not to, but because the field does not exist.

Approval lives in `orchestrator/approval.py`, an append-only ledger that agents are never
handed. `AgentContext` contains a router, a learner id, redacted hints, and a clock. It
contains no ledger, no gate, and no key.

This is the commitment that keeps the parent in the loop, so it gets the strongest
enforcement in the repo.

## 5. Why two keys and HMAC seals

The obvious cheaper design is a `deliver()` function that checks the ledger. It works —
until a fork, or a rushed change, calls the renderer directly. Nothing notices.

So each chokepoint holds a device-local key and signs what it emits, and
`shared/delivery.py` re-verifies both signatures immediately before anything is rendered:

1. the **safety seal** proves this exact payload was screened;
2. the **approval seal** covers the proposal *and its safety seal*, so content approved by
   the parent cannot be swapped for different content afterwards.

The keys are separate on purpose: one key would let the safety gate mint approvals.

The honest cost: every rendering path needs both keys, and rotating them invalidates
existing approvals. The honest limit: this stops accident and casual bypass. It does not
stop a determined fork author, and it is not meant to — it means removing the guarantee
has to be a deliberate act rather than an omission.

`tests/test_delivery.py` contains the attacks: forged approval, content swapped after
approval, blocked content wrapped as screened, seal reused across purposes, expired
approval.

## 6. Why the camera is a scanner

The camera sits on a fixed 90° arm with a narrow field of view, framed so her face is not
in it. That is a hardware guarantee, and hardware guarantees do not survive someone
remounting the arm — so the software backs it up:

- `RawFrame` is not a dataclass, has no encoder, and raises `RetentionViolation` on
  `__getstate__`, `__reduce__`, `__copy__` and `__deepcopy__`. It cannot be pickled,
  copied, or written out, and it zeroes its buffer on scope exit.
- The only image type that crosses a package boundary is `RectifiedPage` — the crop inside
  the marker quadrilateral.
- `tests/test_boundaries.py` fails if anything in `vision/` references face/person/affect
  detection, a streaming response, or `cv2.imwrite`.
- If the four markers are not found, the pipeline raises `MarkersNotFound` rather than
  analysing whatever else is in the frame.

TODO(hackathon): add the frame-fill check — reject a capture where the marker quad covers
less than a set fraction of the frame, which turns "the camera points at paper" from a
mounting assumption into a runtime invariant.

## 7. Why the sheet spec is versioned

The print agent lays out a sheet; the vision pipeline reads it back. If the two drift,
answers get attributed to the wrong questions — a failure that looks like data rather than
a bug.

`shared/sheet.py` defines cells in **page coordinates**: normalised 0–1 over the
quadrilateral of the markers' inner corners. Cell positions are therefore independent of
paper size, printer margins, camera distance and DPI. Rectification maps that quadrilateral
onto a fixed canvas, after which a cell rectangle is a multiplication.

The QR code carries the spec version. A sheet whose version the reader does not understand
is **refused**, not guessed at.

Reading degrades honestly: without the cloud, only `LOCALLY_READABLE` cell kinds
(checkboxes, choice boxes) are attempted; everything else is marked `needs_review` and
`PageReading.degraded` is set. The system prefers "the parent should look at this" to a
confident wrong answer.

## 8. Trust boundaries

Treated as **data, never as instructions**:

- text recognised from her handwriting,
- free text the parent types,
- anything decoded from a QR code.

A worksheet is a piece of paper that a model reads. Anyone who can put text on a page can
attempt prompt injection, so recognised text is never concatenated into an instruction
position. See [THREAT-MODEL.md](THREAT-MODEL.md).

## 9. How the device learns there is something to fetch

The cloud tier is a mailbox and a user interface; the device in the home is the authority.
Nothing is approved until the device seals it. That leaves one mechanical question: **how
does the device find out that the parent approved something?**

### The device pulls. The cloud never calls the house.

Non-negotiable, and it is the same reason Azure Arc and IoT Edge were rejected earlier: an
inbound channel to a device in a minor's home is a liability whatever protocol wears it. So
the device opens an outbound request on a timer and asks. No open ports, no port forwarding,
no tunnel that lets anything dial in — and, incidentally, no NAT to fight.

### ✅ Decided: a fixed 10-minute poll

Nothing here is real-time. The parent approves a worksheet; a few minutes later it can be
printed. Ten minutes is invisible in that flow.

Two consequences, stated plainly rather than discovered later:

- **The API cannot be truly serverless while a device is online.** The Container Apps
  scale-down stabilisation window is 300 seconds. A poll every 10 minutes therefore wakes
  the app, keeps it up for ~5 minutes, and lets it sleep for ~5. It idles at roughly half
  duty cycle rather than at zero, so `minReplicas: 0` is honest but only half-effective.
- **A long-poll would be worse.** Holding the connection open is still traffic, so the app
  would never scale down at all. The interval is what buys the idle time.

### ⚠️ The constraint that shapes this

The Azure subscriptions available to this project **restrict publicly reachable
resources**. That is a legitimate governance rule and we design inside it rather than
around it — but it has a real cost, and pretending otherwise would make this document
useless to anyone reading it.

The natural design would be for the device to ask a *cheap, always-on* service — object
storage — rather than an *expensive, scale-to-zero* one. Under the restriction, storage is
private behind a private endpoint, and a device sitting on a home LAN cannot reach a private
endpoint. So the only thing the device can talk to is the one component that must be
publicly reachable anyway: the API. Which is precisely the component we wanted to leave
asleep.

**The constraint does not break anything. It costs us roughly half the idle savings.**

### 💡 Deferred: the doorbell blob

Recorded here so it is not rediscovered, and so the trade-off is visible to anyone
evaluating this design.

If a future subscription permits a publicly *routable* storage endpoint — still with no
anonymous access and no shared keys — the wake-up path becomes almost free:

1. One tiny blob per household, `signal/<householdId>`, holding a revision number and
   nothing else: `{"rev": 42}`.
2. When the parent approves something, the API — already warm, because the parent is using
   it at that moment — increments `rev`.
3. The device issues a conditional `GET` with `If-None-Match` every couple of minutes.
   **304 Not Modified** means nothing happened: no compute woke, and the request costs a
   fraction of a cent.
4. Only a **200** makes the device call the API, which then wakes because there is genuine
   work.

The API would sleep whenever nobody is doing anything, and the polling interval could drop
from ten minutes to two without costing more.

**Why it is safe to expose:** `allowBlobPublicAccess=false`, `allowSharedKeyAccess=false`,
and an Entra token required on every request, from an identity holding
`Storage Blob Data Reader` on that container alone. The payload is an opaque household id
and an integer — a total compromise of the blob would reveal only *"household X has
something pending"*. No name, no content, nothing about her.

**Revisit when:** the deployment subscription allows a storage account with
`publicNetworkAccess=Enabled`, **or** the Container Apps idle cost measurably exceeds the
free grant.

**Do not build it before then.** It is a second reachable surface and a second thing to
authenticate, bought to solve a cost problem that has not yet been shown to exist.

## 10. What is not built yet

Honest status, so nobody mistakes scaffolding for a system:

| Area | State |
| --- | --- |
| `shared/` contracts | written |
| seals, delivery boundary | written and tested |
| boundary tests | written and mutation-checked |
| `printing/` renderer | written, and **proven on real paper**: the 50 mm ruler measures 50 mm |
| `tools/check_scan.py` read-back | written, and proven end to end on a scanned sheet |
| `orchestrator/router.py` | written, with a stub backend; **never called with real credentials** |
| `infra/` cloud tier | deployed and verified — see [DEPLOY.md](DEPLOY.md) |
| orchestrator safety gate, ledger, planner | **not written** |
| `agents/` content, vision, scheduling, print | **not written** |
| `vision/` capture, ArUco, rectify, QR, cell read | **not written** as a package; the logic exists in `tools/` |
| `panel/` parent UI, API, worker | **not written** — the container apps run a placeholder image |
| `firmware/` e-paper, LCD, buttons | **not written** |

Stubs in this repository raise `NotImplementedError` or return obviously fake data. If
something looks like it works, it works.
