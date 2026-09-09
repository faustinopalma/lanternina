# Architecture

This describes the local code inspected on 7 September 2026. The workbench has exercised the model path; the installed hub, deployed API revision and cloud configuration were not inspected or changed. Historical deployment measurements remain historical. Decisions and measurements from this revision are in [ideas/13](../ideas/13-prompts-and-simulation.md).

## Hub, container and models

```text
Parent browser -> container API -> household stores
Hub -> container API -> model router -> Foundry
                    -> Content Safety
Hub <- generated document, page image or reading
Hub -> printer, scanner and display files
Display -> hub -> display image
```

The arrows show who initiates requests. The hub runs the equipment and activity clock; the container constructs model clients. The paper path does not run agents or a parent-approval ledger inside the hub. `devices/ask_panel.py` sends page and reading requests. `devices/run_experience.py::_ask` posts a continuation request. `panel/routes/paper.py` and `panel/routes/experience.py` authenticate device calls, apply usage limits and delegate to container functions.

The browser stores settings and decisions. The hub later retrieves them. The container does not open an inbound connection to the house. Model-assisted brief editing is a separate browser-initiated path in `panel/editing.py`; therefore not every panel action is a storage-only operation.

The production model transport lives in `orchestrator/router.py`. Agents receive `ModelRouter` through `AgentContext`. Research and CLI tools can have separate synthetic calls, notably `tools/handwriting.py`. Import checks in `tests/test_boundaries.py` apply to their named production packages, not to every Python file in the repository. The router is not the only Azure SDK consumer: storage and Content Safety have their own clients.

## Generation and repair

`panel/devising.py::devise_experience` performs the following operations:

1. Filter `methods/` by household capabilities and ask for a form and a move from a sampled catalogue. An unavailable or invalid choice falls back to a random selection; an empty catalogue yields no selected method.
2. Ask `ExperienceDeviser` for the complete activity document.
3. Parse it with the `Experience` contract. An unreadable answer gets one `repair_unreadable` call.
4. Run `shared/experience_checks.py::check`. Complaints get one separate `repair` call followed by another check. Remaining complaints raise `RefusedByTheChecks`.
5. Screen the activity's words with Content Safety before returning it.

There may be both a format repair and a checks repair. SDK transport retries are separate again. A fixed count of seven calls is therefore not the cost of every activity. Prompt blocks live beside their modules and are rendered into [prompts/](prompts/README.md) by `python -m tools.prompts --write`.

`panel/continuing.py::continue_experience` parses, checks and screens a continuation. It does not repair one. The experience judge supplies an additional fallible appraisal; its findings are not the parser, structural checks or safety decision. Background judging can be skipped at the usage limit and is not a guarantee that every stored activity has a verdict.

## Approval and safety

The activity path stores `OfferedExperience` and parent decisions in `panel/experiences.py` and `panel/routes/experience.py`. The device retrieval path selects approved records. The hub receives a document through authenticated HTTPS and snapshots the activity it starts. The current route is not the older `Proposal` -> `ApprovedItem` -> `shared.delivery` path.

The older path still has separate safety and approval HMAC seals and tests in `tests/test_delivery.py`. Those tests demonstrate that path's properties; they do not prove cryptographic binding of every current activity or continuation. Activity safety functions mint local screening seals, but the hub consumes moments, not those seals.

The parent approves the initial activity. Later page images and continuation moments are generated without a second parent review. `PageMaker` uses the image-generation screening path. Activity and continuation text is screened by their container functions. The read-page route invokes the reader and a separate page-placement task; it does not call an inbound-image Content Safety gate. The proposed camera's inbound screening is not an implemented scan guarantee.

`shared/blocklist.py` and `orchestrator/outgoing.py` reject named classes of text before storage or display. They reduce specific risks but do not prove complete semantic compliance. Handwriting is quoted as data in a prompt; quotation and instructions do not make prompt injection impossible. Generated images can also misletter or add marks despite the drawing instruction.

## Paper and continuation

`PageMaker` receives a `Page`: kind, title, notes, spaces and illustration. It does not receive the script, help ladder or neighboring moments. Information needed on paper must be present in that contract. The whole page is drawn in one image call; `printing/paper.py` places that image on A4 rather than laying out its words.

`devices/hands.py::_hand_over` requests the image, attempts printing, then shows the display instruction. Drawing or printing failure shows the predefined `instead` text and returns `Done(fault=...)`. CUPS acceptance alone is not treated as completion: the print path waits for the job to leave the pending queue. Disappearance from that queue is still weaker than proof that a physical sheet emerged.

The hub retains blank images and run pointers. Its real scan path expects the last handed-out sheet. `PageReader` compares a blank with the returned image and produces `WhatCameBack(written, same_sheet, describes, read_at, degraded, metadata)`. `came_back()` returns no branch for a degraded reading. `same_sheet=False` is informative and does not refuse a sheet.

An `ask` request carries `reading.to_dict()`. `ExperienceContinuer._ink` now includes `describes` and reading status, excluding metadata and timestamps. The current notebook run verified those descriptions in the actual sent prompt. A continuation replaces `Afternoon.segment`; identifiers are resolved within that segment rather than appended to the original graph. The original `run.experience` remains the request document. Repeated continuations whose `after` belongs only to a later segment are not established as supported by this design.

The contract contains `Collect.if_no_page`, but the standard runner does not use it. `_play` stops at a collection even when no sheet was printed. The workbench's injected print-failure test follows `instead` and `if_no_page` as an explicitly different simulation path. It is not evidence that the hub already handles that branch.

## Clock and interruption

`devices/afternoon.py` checks the household's rhythm, pending run and daily allowance before beginning an approved activity. `run_experience._weight_for` chooses standard or short according to remaining time. It does not choose extended, drop optional moments or merge moments.

`_play` executes consecutive non-collection moments immediately. `hands.py` contains no duration wait for `say` or `hand_over`. The declared minutes inform planning and end-time calculations but do not pace every visible instruction. Help belongs to the collection where the runner is waiting; listing all moment help in a notebook is not a demonstration of its timed delivery.

`conclude_what_is_over` begins the current way out at the first clock check at or after 30 minutes before the end. A later check shows the close after the way-out duration or by the end time. This relies on the timer and stored document. Unreadable run state can be removed without an ending; an unavailable service or failed display cannot satisfy an unconditional guarantee that every activity visibly ends.

The workbench reports `concluded`, `error` or `interrupted`. It preserves fallback events separately and reports a step limit as interruption. Its document-minute sum is not a measured human duration.

## Memory and retention

| Material | Owning code | Behavior and limits |
| --- | --- | --- |
| Preferences | `panel/preferences.py` | Interests, avoid list, language, simultaneous sheets and a note. Note expires after 28 days; reads remove expired content. |
| Rhythm and assignments | `panel/rhythm.py`, `panel/devices.py` | Household schedule, allowances and device roles. These are implemented controls, not hub-only constants. |
| Activity history | `panel/what_happened.py` | Endings, reported duration, returned or missing sheets and bounded reading-derived summaries inform later prompts. |
| Profile observations | `panel/profiles.py`, `shared/profile.py` | Up to 80 observations; profile computed from up to eight recent rows, with at least three usable placements per axis. `load` and `ink` use page observations; `span` uses planned versus reported duration and ending. |
| Generated material | `panel/trail.py`, `panel/pictures.py` | Plans, output, prompts and generated pages. Pages and display pictures have distinct archives. |
| Raw reading contract | `shared/vision_contracts.py` | Copy, pickle and explicit JSON serialization are supported during development. The owning store controls retention. |
| Camera photographs | `devices/photo_store.py`, `panel/photos.py` | Originals remain on the hub and synchronize to the authenticated parent panel. The family can delete one, a confirmed date range or all listed photographs. Tombstones prevent retries from restoring deletions. |
| Development readings | `panel/keeping.py`, continuation route | Administrator-only permission defaults off and lasts 14 days. Each permitted row lasts 14 days from its own write. Revocation prevents new retention; existing rows retain their own expiry. |

The read-page route schedules a separate placement call using the same images. It stores `Noticed`, including axis placements and a short explanation. This occurs independently of the optional development-retention permission. `_pitch_for` computes profile prose for devising and continuation. The raw reading and the derived observation are different records, but both originate in what came back.

The memory deletion route clears activity history and profile observations. Clearing the activity trail is a separate operation and uses a distinct store; it is not household deletion. A complete plain-language memory view and a verified tenant-wide erasure procedure are not established by these paths. Expiry code and Cosmos TTL configuration must not be confused with a measured deletion time in the deployed service.

## Failures and accounting

Model unavailability can raise `CloudUnavailable` or `NoCapacityError`; the router does not promise an always-available cached activity. A picture failure keeps the previous picture. A reading failure leaves the activity waiting. Continuation rejection returns an error to the hub, whose clock can still reach the way out.

Routes record usage and apply a monthly household limit. The research recorder measures logical calls, not SDK retry attempts or all safety requests. A last-usage value is not automatically a sum of selection, repair and generation costs. Neither its call count nor the automatic judges' findings are a complete billing or quality measure.

## Verified and unverified

The workbench completed one synthetic two-page activity on 7 September 2026. Its model path took 335.6 seconds and its notebook executor took 345.4 seconds. It read the target's synthetic handwriting, sent the descriptions in a continuation prompt, reached a close and read an untouched page as blank. The saved run is [here](../research/runs/2026-09-07-officina-104746-339138/verification.json).

Local tests cover blank, failed print, two sheets, failed and degraded reading, explicit stop, step limit, prompt reloading and resource closure. They do not establish that a printed activity is understood or that the distributed system runs the same revision. The handwriting model also colored a printed decorative pencil in the inspected output; the synthetic edit did not preserve every original pixel.

The handheld camera and multi-button response panel remain unimplemented in the activity path. Hardware wiring claims, current printer behavior, scan quality, display pacing and a second household installation require physical checks. No deployment was performed for this revision. Infrastructure and historical operational notes remain in [DEPLOY.md](DEPLOY.md), [HARDWARE.md](HARDWARE.md) and [WORKLOAD-IDENTITY.md](WORKLOAD-IDENTITY.md).