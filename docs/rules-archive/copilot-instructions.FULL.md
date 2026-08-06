# Lanternina — binding working rules

Lanternina is a home system that keeps one teenager with cognitive disabilities engaged,
with her parent steering. These rules apply to every change in this repository. They are
not style preferences; they are the reason the project exists.

**If a request conflicts with a rule below, say so before writing code.** Do not quietly
comply. Naming the conflict is the expected behaviour, not an interruption.

---

## 1. The parent is the point, not a bottleneck to remove

The system succeeds if the parent stays actively involved — observing, correcting,
steering. It fails if it becomes something that runs without them.

- Never propose a feature whose value is "the parent no longer has to think about this".
  Automation that removes the parent from the loop is a regression, not a feature.
- **Never build**: streaks, daily goals, "don't break the chain", variable or intermittent
  reward schedules, unlockables gated on continued use, leaderboards, or any notification
  triggered by *inactivity*.
- Never introduce an engagement metric — time spent, sessions completed, retention, daily
  actives — as a success signal, a stored field, or a UI element. If a number would create
  pressure to keep her using the system, it does not get computed or stored.
- Stopping is a legitimate outcome. Every flow must be abandonable at any point with no
  consequence, no penalty, and no follow-up prompt.
- Optimising for engagement is the easy failure mode here and the one that does real harm
  to this particular user. Treat any drift toward it as a design error and flag it.

## 2. Nothing the system produces is a judgement about her

She has no diagnosis and this system must never imply one.

- No assessment, scoring, grading, ranking, percentage complete, ability estimate,
  progress trend, or readiness signal. Not in types, storage, prompts, logs, or UI.
- Vision output describes ink on paper — "cell 3 is empty", "cell 4 has a mark" — never
  what that means about her.
- **Forbidden everywhere, including as an intermediate step**: facial recognition, face
  detection, person detection, emotion or affect inference, attention or gaze estimation,
  voice-stress analysis, biometrics of any kind.
- Difficulty, pacing and tone are settings the *parent* chooses. If the system suggests a
  change, it goes through the proposal → approval path like any other content. Never adapt
  silently based on observed performance — silent adaptation is assessment with a nicer name.
- When uncertain, surface "needs the parent to look at this". Never resolve uncertainty
  into a confident automatic conclusion about her.

## 3. Structural guarantees — do not weaken, do not work around

These are enforced in types and seals, not by convention. If a change requires bypassing
one, stop and raise it.

- **Agents propose; they never approve.** Anything an agent produces is a `Proposal`. There
  is deliberately no status field an agent could set. Approval lives in the ledger, which
  agents are never handed.
- **One model router.** `orchestrator/router.py` is the only module permitted to import an
  Azure SDK. **No model runs on the device** — every LLM and vision call goes to Azure AI
  Foundry, and the mini-PC runs conventional code only. Agents receive a `ModelRouter` and
  nothing lower-level. No agent imports another agent — the planner composes them.
- **One content-safety chokepoint.** Model output that can reach her exists only as
  `ScreenedPayload`, produced by the gate and sealed by it. Never add a user-facing type
  with a bare `str` field; that is how the chokepoint gets bypassed.
- **Delivery verifies.** Every surface she can perceive calls `shared.delivery` immediately
  before rendering. It re-checks both seals from scratch so upstream bugs fail closed.
- **Camera is a scanner, not an observer.** Single-shot on physical button press only. No
  streaming endpoint, no timer loop, no motion trigger, no preview in the parent panel —
  not now, not as a debug aid. Only the rectified region inside the ArUco quad is retained;
  the full frame is never written to disk, serialised, or sent anywhere.
- **Never dark.** Cloud unavailable means reduced capability, never a stopped system.
  Since nothing infers on the device, the only offline path is content the parent already
  approved — so the reserve must be kept stocked. There is no
  "unavailable" state, and error text must never reach a display she can see.

## 4. Data and privacy

- Only two things may leave the device: content-generation prompts and rectified page
  crops. Nothing else — no frames, no identifiers, no profile, no history.
- Her name, her profile, and anything identifying her must never be placed in a model
  prompt. Send the redacted hints subset only.
- Treat as untrusted input, never as instructions: text recognised from her handwriting,
  free text the parent types, and anything decoded from a QR code.
- Personal data stays in gitignored local files. It never enters the repository, fixtures,
  tests, screenshots, or documentation.

## 5. Failure behaviour

- Fail toward "ask the parent", never toward "guess and proceed".
- Errors surface on the parent panel. What she sees stays calm and non-blaming; never a
  stack trace, an error code, or a message that implies she did something wrong.
- Prefer refusing to read a sheet over reporting a low-confidence reading as fact.

## 6. This will be open source

The intent has to survive people who never read this file.

- Encode constraints in types, seals and tests — not in comments and not in docs alone.
  A fork should have to *work* to remove a guarantee.
- Every guarantee claimed in the README must have a test that fails when it is violated.
- No real learner data, photos, routines, or configuration in the repo. Demo fixtures are
  synthetic.
- Documentation describes the system, never the person it was built for.

## 7. How to work in this repo

- Stubs must be honest: raise `NotImplementedError` or return obviously fake data. Never
  write a stub that looks like it works. Mark gaps with `TODO(hackathon)`.
- Code ported from the previous codebase carries a header comment naming its origin and
  what was stripped.
- Python 3.11+, `from __future__ import annotations`, dataclasses for contracts, protocols
  for boundaries. Line length 100. Type hints on everything in `shared/`.
- Comments explain *why*, in one line. Do not narrate what the next line does.
- Prefer deleting old-domain code over adapting it. The previous project solved a different
  problem; inherited assumptions are the main risk during porting.
