# Architecture

This document explains the boundaries in the codebase and why each one exists. The
reasoning matters more than the rule: the constraints here are unusual, and without the
reasoning the next person will read them as ceremony and route around them.

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
│   devices/ ── page vs blank ──────────────────────────────────┘     │
│      ▲                                                        │     │
└──────┼────────────────────────────────────────────────────────┼─────┘
       │ a page put on the glass                                ▼
   the scanner                                    e-paper / LCD / printer
                                                                 
       └──────────────── prompts and page pairs ──────────▶ Azure AI Foundry
```

`shared/` holds types and protocols and nothing else. Everything else depends on it; it
depends on nothing. No agent imports another agent.

Two names are used throughout, because "the device" and "the cloud" stopped being precise
once both grew parts:

- **Lanternina Hub** — the machine in the house. It holds the sealing keys, the ledger, the
  scanner and the link to the display. It is the only initiator of work.
- **Lanternina Cloud** — the Azure tier: the parent dashboard, the stored themes and
  approvals, and the single door to the models.

The diagram above is the paper loop, which lives entirely in the Hub. The picture loop,
added later, is described in section 10 and crosses the boundary in the other direction.

## 2. Why a single model router

`orchestrator/router.py` is the only module permitted to import an Azure SDK. No module
anywhere may import a local model runtime — there is no on-device inference. Everyone else
receives a `ModelRouter` protocol.

Concentrating it buys three things that are hard to get otherwise:

- **Screening cannot be routed around.** If any component could construct its own client,
  the content-safety chokepoint would be one forgotten call away from being bypassed.
- **Degradation is uniform.** The fallback ladder lives in one place instead of being
  re-implemented, differently and worse, at each call site.
- **What a prompt carries is decided once.** Whatever a prompt may include is decided in
  one place rather than at each call site.

What a prompt *says* is not in Python. Each block lives in a Markdown file beside the module
that sends it — `agents/experience_deviser.task.md` next to `agents/experience_deviser.py` —
read by `shared/prompts.py`, with the numbers filled in from the format's own constants. The
assembled result of every one of them is rendered into [docs/prompts/](prompts/README.md) and
a test refuses a change that has not been rendered.

The router exposes two methods with deliberately different return types:

| Method | Returns | For |
| --- | --- | --- |
| `generate_for_user()` | `ScreenedPayload` | anything the adolescent will see — screened and sealed on the way out |
| `analyze()` | `ModelResponse` | internal reasoning only; its text cannot enter a `Proposal` |

That difference is not stylistic. `Proposal.payload` is typed `ScreenedPayload`, so raw
model output is *structurally* unable to reach a user-facing path.

### Degradation: reduced, never dark

```
CLOUD_FOUNDRY  ──unreachable──▶  CACHED_FALLBACK
   full                            cached only
```

No model runs on the device. Every LLM and vision call goes to Azure AI Foundry; the
mini-PC runs conventional code only — OpenCV, the panel, the serial link. That is a
deliberate choice: one inference path instead of two, no model weights to ship or update,
no second set of failure modes, and a device small enough to be powered over Ethernet.

`DegradationLevel` has no "unavailable" member. Going dark is not a state the type system
can express, because for this user an unexplained dead device is worse than a simpler
activity. The router never raises because the cloud is down; it reports which tier served
the request and whether capability is reduced, and the parent panel shows it.

One consequence follows from it: `CACHED_FALLBACK` serves previously approved content, and
it is the only offline path. If the parent has approved nothing in reserve, "never dark"
is a promise with nothing behind it. Keeping a reserve stocked is a product requirement,
not an implementation detail.

Reading degrades the same way. Without the cloud, only the cell kinds in
`sheet.LOCALLY_READABLE` — filled checkboxes and choice boxes, which are ink-coverage
measurements OpenCV can do on its own — are attempted. Handwriting is marked
`needs_review` rather than guessed.

## 3. Why content safety is a type, not a call

The rule is "every generated output passes Content Safety". Implemented as a call each
agent makes, that rule survives until someone adds an agent in a hurry.

Instead, the gate is the only thing that produces `ScreenedPayload`, and it **signs** what
it produces (`shared/seal.py`). Anything user-facing accepts only that type. There is no
user-facing type in `shared/` with a bare `str` field, and adding one is the easiest way
to break this design.

A `BLOCK` verdict is a normal outcome, not an exception to swallow. The system falls back
and tells the parent; it never retries until something slips through.

## 4. Why agents can only propose

Agents return `Proposal`. Look at what `Proposal` does *not* have: no `status`, no
`approved`, no `publish()`. An agent has nowhere to record that its own output is
acceptable — not because it is trusted not to, but because the field does not exist.

Approval lives in `orchestrator/approval.py`, an append-only ledger that agents are never
handed. `AgentContext` contains a router, a learner id, redacted hints, and a clock. It
contains no ledger, no gate, and no key.

This is the commitment that keeps the parent in the loop, so it is the one enforced most
strictly.

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

## 6. Why the camera cannot be pointed at somebody by anyone but its owner

This section used to argue from framing: a fixed 90° arm, a narrow field of view, no face
in shot, and software that stopped if the four markers were missing. That argument is
retired along with the rig. The camera is handheld — a battery, one button, no screen — and
faces will be in frame.

A guarantee about framing would have had to be withdrawn the first time somebody turned
round, so what replaces it is about who can trigger a capture and what may be inferred:

- Nothing in the cloud and nothing in the parent's panel can take a photograph. There is no
  remote trigger, no stream, no timer and no motion trigger.
- Holding the button is the only path to the sensor having power, and the activity light is
  wired in series on that rail rather than driven from a pin. "It is off" is a property of
  the wiring.
- No facial recognition, no emotion or attention inference, no age or identity inference,
  at any step including an intermediate one. This carries more weight now, not less.
- Content Safety runs on inbound photographs as it does on generated output.
- What is kept lands in a gallery its owner can see and delete from. Deletion is the
  guarantee; not keeping anything stopped being one when the camera left the desk.

None of this is enforced by a test. `vision/` is an empty package and there is nothing to
enforce it against, which is where the README's Status section puts it. `RawFrame` and
`RectifiedPage` survive in `shared/vision_contracts.py` as a technique for sealing a type,
not as a rule the system still keeps.

## 7. Why nothing on the page is there for a machine

A page is read by handing a model two images — the blank as it was printed, and the same
sheet off the glass — and asking what is different. No QR code, no corner markers, no grid
of declared cells.

The design this replaced is in `attic/`: cells in page coordinates normalised over the
quadrilateral of four ArUco markers, a QR carrying the spec version, and a sheet whose
version the reader did not understand refused rather than guessed at. It solved a real
problem — print and read drifting apart, so answers get attributed to the wrong questions —
by making the paper carry its own description. The cost was that every page had to be laid
out by something that could also describe itself, which is why the pages all looked like
forms.

Reading is a model's job. Until 21 August 2026 there was a second reader underneath —
arithmetic over `LOCALLY_READABLE` cell kinds, used with no cloud and flagged
`PageReading.degraded` — and it is in `attic/` now: **no cloud, no reading**, and a page
that comes back while the panel is unreachable waits. What survives is the preference that
put it there in the first place: anything the model did not answer for, or answered for
with something outside what was asked, is marked `needs_review`. "The parent should look at
this" beats a confident wrong answer.

## 8. Trust boundaries

Treated as **data, never as instructions**:

- text recognised from handwriting,
- free text the parent types,
- anything decoded from a QR code, wherever one is still read.

A worksheet is a piece of paper that a model reads. Anyone who can put text on a page can
attempt prompt injection, so recognised text is never concatenated into an instruction
position. See [THREAT-MODEL.md](THREAT-MODEL.md).

## 9. Work begins in the house

The dashboard stores parent-authored content, approvals and configuration. A write ends
when that state is durable. It does not call a model, put a message on the work queue,
notify the device, create a timer or schedule processing for later. There is deliberately
no cloud-to-house wake-up path.

The server in the home is the sole initiator. From time to time it decides that it wants
something and opens an outbound request to the API. The rule for when it decides is not
designed yet; it belongs to local orchestration and will be built separately. The cloud
answers using the latest persisted state it can see.

### Scale from zero is part of the request

The API and worker may both be at zero replicas when the home server asks. The request is
not an interactive user action, so the server can wait through Container Apps activation,
model inference and content-safety checks. No browser returns `202`, no parent polls for a
result, and no adolescent sees a loading state caused by cloud cold start.

Container Apps HTTP ingress has a documented **240 second timeout**. Work expected to fit
inside it can return on the same request. Longer work needs a correlation id and durable
result. If the request times out, the home server waits according to its local policy and
contacts the API again with that correlation id. That is not dashboard polling, and
completion does not trigger a notification or an inbound call to the house.

This buys actual idle time: dashboard inactivity and device inactivity both allow compute
to remain at zero. It costs latency on a device-initiated request. That trade is acceptable
because the person does not experience the request as an immediate action.

### The queue has one permitted origin

The queue remains available for work that must outlive the HTTP process. A message may be
created only while handling an authenticated request from the home server. Dashboard
routes do not receive dispatch authority. Whether the first implementation waits on HTTP,
uses a queue with a correlation id, or combines both is still open; none of those choices
may change who initiated the work.

### Public mailbox options, measured 8 August 2026

The tenant policy forces Storage and Cosmos public access off. It does not currently
apply an equivalent `Deny` or `Modify` policy to Service Bus, IoT Hub, Event Grid or Front
Door. Two disposable probes confirmed the distinction; both resource groups were deleted
after the readback.

| Option | Idle list price | What was verified | Limit next to the claim |
| --- | ---: | --- | --- |
| Existing Container Apps API | No additional resource | The home server can wait through scale-from-zero, then contact the API again with a correlation id after the 240 second ingress timeout | Each retry can pay cold-start latency; the durable result remains behind the API |
| Service Bus Basic | No base charge listed; $0.05 per million operations | A Basic namespace and queue reached `Succeeded` with public access enabled and local/SAS authentication disabled; the public DNS name resolved | No sessions or duplicate detection. Direct device access needs an Entra application identity, preferably with a certificate. Household isolation requires queue-scoped RBAC and, for this design, a response queue per household |
| IoT Hub F1 | $0; 8,000 messages/day | An F1 hub in Germany West Central reached `Active` with public access enabled and device/module SAS disabled; its public endpoint resolved | Not available in Sweden Central. Cloud-to-device queues hold at most 50 messages per device, with TTL up to 2 days. HTTPS receive should not poll more often than every 25 minutes; MQTT/AMQP can wait on an outbound connection |
| Event Grid namespace MQTT | $0.04 per throughput-unit hour, about $29.20/month for one unit | Documentation supports X.509, Entra ID and external OAuth clients, persistent sessions and QoS 1 | More protocol and access-control machinery than this PoC needs; it is pub/sub, not a simple request/result queue |
| Front Door Standard | $35/month base | Public HTTP(S) proxy | No Private Link, so it cannot reach the private origin we are trying to expose |
| Front Door Premium | $330/month base | Private Link supports Container Apps, APIM, Blob and static website origins | Queue Storage is not a supported direct Private Link origin. Front Door is HTTP(S), not an AMQP or queue endpoint, and it does not support client mTLS |

Front Door is therefore not a way to make the private Storage queue public. It can expose
an API that mediates the queue, but Container Apps already provides that API without a
Front Door base fee.

### Dashboard startup is a separate path

Service Bus cannot make the browser's first authenticated read synchronous: the browser
still needs an HTTP endpoint for account and configuration data. The deployed dashboard
solves perceived startup without adding an always-on resource:

1. Static Web Apps serves the shell immediately.
2. Page load starts `/health` without awaiting it, overlapping Container Apps activation
  with MSAL initialization and token acquisition.
3. Once MSAL finds a session, the browser shows a neutral authenticated shell while
  `/api/me` loads account data.

Measured on 8 August 2026 with the API at zero replicas, `/health` took **25.99 seconds**
from cold and **0.21 seconds** immediately afterwards. The warm-up runs only when a browser
opens the dashboard, so compute can still stay at zero when nobody connects. It is allowed
to wake the dashboard API; it does not call a model, enqueue work or signal the house.

For the first implementation, keep the existing API and correlation-id retry because it
matches the functional contract with no new identity plane. If the 240 second boundary or
repeated cold starts become a measured problem, test Service Bus Basic next. IoT Hub F1 is
the stronger candidate if per-device provisioning, X.509 identity and fleet messaging are
needed together; adopting it only as a queue would buy more lifecycle machinery than the
PoC currently uses.

## 10. The picture loop

The display shows a picture that nobody in the house drew. The loop has four steps and one
initiator:

```
Hub timer (hourly) ──▶ POST /api/device/{household}/paint ──▶ Cloud
                                                               │
                            picture bytes ◀── screening ◀── model
                                 │
            install screen.bmp (atomic replace)
                                 │
        display asks the Hub ──▶ BYOS server serves those bytes
```

The Hub asks; the Cloud never calls the house. The pause (22:00–07:00 by default) and the
spacing between pictures are Hub-side decisions, so a sleeping house makes no requests for
pictures at all.

Painting happens in the Cloud rather than the house because the container already holds a
managed identity with access to the models, and nothing in the house then needs a
long-lived credential. The cost is stated where it is paid: a picture painted in the Cloud
carries no parent-approval seal, because that key lives on the device and stays there. Its
subject is a theme the parent approved and its bytes are screened, but the seal ceremony
is genuinely absent. That is why this path is only ever used for pictures, never for words.

A refusal from the safety gate returns `409`, and an unavailable Cloud returns `503` or
nothing at all. `devices/pull_picture.py` treats both as ordinary: it keeps the picture
already on the wall. Going blank is never the answer to a failure upstream.

### The link to the display is deliberately dumb

The display is a battery e-paper device running stock firmware. It wakes, asks the Hub what
to show, downloads a BMP, and sleeps. Two details in `devices/trmnl_byos.py` exist because
of measurements rather than preference:

- **The picture URL is built from the address the display just reached**, read off the
  socket of the request being served, not from a configured hostname. The hostname was
  `lanternina.local`, which forced an mDNS lookup at every download; on 17 August 2026 that
  lookup failed often enough that the server never saw the request arrive. An address the
  device has already connected on cannot fail to resolve, and it follows DHCP without a
  setting to keep in sync.
- **The mains cadence is 60 seconds.** It was 10, which had the display associating to the
  access point roughly 8,600 times a day. Sixty seconds still feels immediate to anyone
  watching and costs a sixth of the airtime.

What the link does *not* do is as deliberate: the Hub cannot push to the display, cannot
wake it, and holds no way to reach it between wakes. A display that stops asking simply
keeps its last picture — which is the open risk recorded at the end of this document.

## 11. Counting what the models cost

The Cloud panel is the only place where a model call happens on behalf of a household, so
it is the only place that can attribute a cost to one. Azure's own telemetry cannot do it:
from the platform's view every call comes from the same managed identity, so resource-level
diagnostics give totals, never per-household attribution.

What each call cost is read off the response rather than inferred from a price list. Three
figures measured on 17 August 2026 are the reason `ModelUsage` has the fields it has:

| Reported | Measured | Why it matters |
| --- | --- | --- |
| image usage | 12 input, 196 output tokens for 1024×1024 | a picture is billed in tokens, not per picture |
| `quality` | `"low"`, echoed back | we send none, so we are on a default nobody chose |
| `cached_tokens` | 2,816 of 3,325 on an identical second call | cache reads are billed at a discount |
| `reasoning_tokens` | 66 of 101 output tokens | two thirds of the output never appears in the text |
| `apim-request-id` | present on every response | the key to reconciling our figures with Azure's bill |

`panel/usage.py` holds the event and the cap; `CosmosUsageStore` writes one append-only
document per call to the `usage` container. Each event carries its own id, so a replayed
write cannot count twice. A call the safety gate refused is still counted, because it was
still paid for. A failed write is logged and swallowed: the picture was already paid for,
and failing there would spend the money and deliver nothing.

The cap is a monthly count of paid calls, defaulting to 1,000 — an hourly picture is at
most 744 a month, which leaves room for a parent asking for a few by hand while still
stopping a loop that has lost its mind. Reaching it returns `429`, which the hub already
treats like the other calm refusals: the display keeps the picture it has.

### Where the analysis goes, when it goes anywhere

Not built. The direction is recorded so the first implementation does not re-derive it.

Cosmos is the ledger, because a limit has to be checked inside the request it might refuse.
A Log Analytics workspace is the analytical surface: Fabric can read one directly — a KQL
queryset runs cross-service queries against it, and the Mirror Azure Monitor feature exposes
its tables to Eventhouse and Lakehouse through OneLake shortcuts without copying the data.

That decides the shape. Because the data stays in Azure Monitor, Fabric adds no second
ingestion charge and bills only for the capacity used to query it, so a Fabric capacity can
be paused between analyses without losing anything. Streaming into an Eventhouse through
Eventstream would invert that: the capacity would become part of the ingestion path, and
pausing it would drop events.

API Management is deliberately deferred. It buys a limit enforced outside our own code,
which matters at multi-tenant scale and not at one house. The event schema is what keeps
that option cheap: whoever produces it can change without disturbing anything downstream.

The limit next to the claim: Mirror Azure Monitor is in public preview, so its billing and
permissions may change; none of the analytical half is deployed; and only the image path
reports usage, because it is the only path the Cloud panel takes today.

## 12. Why there is no agent framework, and what is taken from libraries anyway

The question came up as two complaints, and both were right. The first: adding a device
touched a dozen places, so the design was fragile in exactly the way that gets worse with
every device. The second: writing our own retry, our own error unwrapping and our own HTTP
is rewriting what the community has already broken and fixed many times.

The reading behind this section is eight posts from Anthropic's engineering blog, fetched
on 25 August 2026 into `_reference/anthropic-agents/` — gitignored, because it is somebody
else's writing. What follows is what was taken from them and what was not.

### The loop is the part that does not apply

Anthropic's working definition of an agent is "LLMs autonomously using tools in a loop".
Every agent framework is built around that loop: the model picks a tool, the tool runs, the
result comes back, repeat.

Here the model never actuates anything. It writes a document; the parent approves it; the
house plays it, possibly days later, from its own clock. If a framework were adopted, its
central mechanism would be the first thing switched off — see section 4, and
[NON-GOALS.md](NON-GOALS.md).

So the frameworks were weighed for what remains, and what remains is not enough to import
one. Measured with pip's resolver on 25 August 2026, into this environment:

| Package | Transitive packages |
| --- | ---: |
| `agent-framework-core` | 9 |
| `pydantic-ai-slim` | 20 |
| `smolagents` | 27 |
| `openai-agents` | 42 |
| `atomic-agents` | 85 |

Nine packages is not a slow container, so the weight argument that was made earlier was
aimed at the wrong target: it was true of `agent-framework` with every provider extra, not
of the base package. The reason for not adopting one is the loop, not the size.

### The transport is not ours, and should never have been

`orchestrator/router.py` spoke REST to Foundry with `httpx` and a hand-threaded Entra
token. It now uses the `openai` client against the same endpoints. What that deleted, in
order of how much it was worth:

- **Retry with backoff, honouring `Retry-After`.** `gpt-image-2` is deployed at capacity 2
  and the region is at its ceiling, so 429 on the image path is ordinary rather than a
  fault. `max_retries=4` is set for that reason.
- **The reason inside a refusal.** There was a hand-written unwrapper, `_checked`, whose
  whole job was to pull `error.message` out of the body because `raise_for_status` throws
  it away. Verified against the real client on 25 August 2026: `str(exc)` already reads
  `Error code: 400 - {'error': ... 'message': 'Could not process image'}}`. The unwrapper
  and its test are gone.
- **Connection reuse, timeouts, and the `images/edits` path** the handwriting hand needs.

What it costs: one more package in the `cloud` and `panel` extras, and a version of the API
surface that can change under us. What it buys is that the two things this module still
does by hand — the shape of a message, and reading what a call cost — are the two things
nobody else can do for us.

The boundary is unchanged. `openai` is still a forbidden import everywhere except the
router and the safety gate, and `tests/test_boundaries.py` still enforces it by dotted
path.

### A device is a hand, and a hand is declared once

The idea worth taking is from the Managed Agents post: separate the brain, the hands and
the session, and give every hand one interface, so that "the harness doesn't know whether
the sandbox is a container, a phone, or a Pokémon emulator".

Here a hand is split the same way, along the line `shared/` already draws:

| Half | Where | What it holds |
| --- | --- | --- |
| the words | `shared/capabilities.py` | the verb, the capability it needs, which kind of object carries it, which job the parent gives it, and one sentence saying what it does in the room |
| the doing | `devices/hands.py` | one function, registered against the verb, that makes it happen |

Everything else is read off that table rather than written again: what each verb needs
(`NEEDS`), which job provides which capability (`_PROVIDED_BY`), what a pretend house can do
(`REACHABLE`), what dispatches a moment (`devices/hands.play`), and the paragraph of the
prompt that tells a deviser the verb exists (`THE_ACTS`).

Counted before the change, by tracing what `scan_a4` touched: **thirteen edit sites across
seven files** to add one device. After it: one entry in `HANDS`, one function in
`devices/hands.py`, and — for a verb that carries its own keys — a moment class and its
parser, which is the document format and genuinely needs code.

`tests/test_hands_registry.py` holds the guarantees, and each was checked by injecting the
break it is about rather than by passing on the fixed version:

| Half-finished device | What fails |
| --- | --- |
| registered, but nothing carries it out | `test_every_hand_is_carried_out_by_something` |
| carried out, but the deviser is never told | assembling `THE_ACTS` raises at import |
| wants a job no parent can hand out | `test_a_hands_job_is_one_a_parent_can_actually_hand_out` |

The limit, stated next to the claim: this makes a device cheap to *add*. It does nothing
about whether the device is a good idea, and nothing about the moment class a new verb
needs if it carries keys of its own. And `Act` moved from `shared/experience.py` down into
`shared/capabilities.py`, which is a real cost: the document format no longer owns its own
verb list, and a reader looking for it has to know that a verb and the equipment it needs
are one fact rather than two.

### What was not adopted, and might be

Progressive disclosure — a module that announces itself with a name and a description, and
is read in full only when it is relevant — is how `HANDS` works for devices. It is not yet
how agents work: `agents/` are still plain classes the panel wires up by hand, and adding
one still edits the module that calls it. Doing for agents what was done for devices is the
obvious next step and has not been taken.

Structured output with validation and repair is still hand-written, in
`agents/experience_deviser.py` and `shared/experience_checks.py`. That is the part
`pydantic-ai` would genuinely do better, and Pydantic is already installed underneath
FastAPI. It was left alone in this pass because the checks encode product rules, not
schema, and moving them is a change to what is enforced rather than to how.

## 13. What is not built yet

Honest status, so nobody mistakes scaffolding for a system:

| Area | State |
| --- | --- |
| `shared/` contracts | written |
| seals, delivery boundary | written and tested |
| boundary tests | written and mutation-checked |
| `printing/` renderer | written, and checked on real paper: the 50 mm ruler measures 50 mm |
| `tools/check_scan.py` read-back | written, and proven end to end on a scanned sheet |
| `orchestrator/router.py` | written, and called with real credentials from the Cloud panel; the transport is the `openai` client since 25 August 2026 |
| `shared/capabilities.py` + `devices/hands.py` | written: one entry and one function per device, everything else derived — see section 12 |
| `infra/` cloud tier | deployed and verified — see [DEPLOY.md](DEPLOY.md) |
| `panel/` parent dashboard and API | written and deployed: proposals, themes, pictures, devices |
| safety gate | written, and on the path of everything the Cloud paints |
| `devices/` Hub services | written: BYOS display server, hourly picture pull, status push |
| picture archive and restore | written: blob-backed, restores byte-identical |
| approval ledger, planner | not written |
| `agents/` vision, scheduling, print | not written |
| `vision/` handheld camera intake | not written; the package is empty, and the camera rules in section 6 are enforced by nothing |
| usage accounting and per-household cap | written and deployed — see section 11 |
| analytical surface for those figures | not written — direction in section 11 |
| agents announcing themselves the way devices do | not written — the gap named at the end of section 12 |
| `firmware/` | not written, and may never be: the display runs stock firmware and the Hub serves it |

Stubs in this repository raise `NotImplementedError` or return obviously fake data. If
something looks like it works, it works.
