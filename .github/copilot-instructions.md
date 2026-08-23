# Lanternina — working rules (PoC mode)

Lanternina is a home system that offers activities to an adolescent, with a parent
steering. It is for adolescents, without asking which ones: interest, appetite for novelty
and comfort with text on a page vary across the whole range of cognitive ability, and none
of that is recorded here as a property of anybody.

**These are the lightened rules, in force while we reach a proof of concept.** The full
version in `docs/rules-archive/` records what the rules were, not what they are; this file
is the only place that says what holds. What was cut is engineering ceremony: seals, types
that forbid, AST tests, a failing test per claimed guarantee. What is left is not slowing
anything down, and drift in it does not get noticed until it has done harm.

---

## 1. Still binding — these are about the adolescent, not about code quality

The same lines are stated at more length, for a reader, in `docs/NON-GOALS.md`. Neither is
generated from the other: revising one means revising the other.

- **The parent is the point, not a bottleneck to remove.** Never propose a feature whose
  value is "the parent no longer has to think about this".
- **Never build**: streaks, daily goals, "don't break the chain", variable reward
  schedules, unlockables, leaderboards, or any notification triggered by *inactivity*.
- Never introduce an engagement metric — time spent, sessions, retention, daily actives —
  as a success signal, a stored field, or a UI element.
- **Stopping is a legitimate outcome.** Every flow must be abandonable at any point, with
  no penalty and no follow-up prompt.
- **The system may learn from what happens, and should.** Difficulty, tone, topics and
  formats start from what the parent and adolescent chose, and may move beyond them on what
  the system observes: what came back on a sheet, what was left blank, what took a long
  time, what was picked again. A system that cannot do this is the failure mode this
  project is likeliest to reach. Two things bound it, and both are below.
- **Nothing the system states is a verdict about a person.** It may record what happened —
  this cell was empty, this took four minutes, this topic came back untouched twice — and
  act on it. It may not turn that into a claim about who somebody is: no score, grade, rank,
  level, ability estimate or readiness signal, in types, storage, prompts, logs or UI.
  Vision output describes ink on paper ("cell 3 is empty"), never what that means about the
  person.
- **Forbidden everywhere, including as an intermediate step**: facial recognition, face
  detection, person detection, emotion or attention inference from images, gaze estimation,
  biometrics. Inference from the work itself is allowed; pointing a sensor at a person to
  read them is not.
- **Dashboard writes are inert.** Adding or approving content and changing a setting only
  persist state: no model call, no queued work, no notification, no waking the home server.
  Only a request the home server makes starts processing.
- **What reaches the cloud is the parent's decision, and it may include the adolescent's
  name, profile and history.** The cloud tier is in the EU and holds personal material on
  the same terms as the house. The code sends `prompt_hints()` because no wider field has
  been asked for; widening it is an ordinary change. The central catalogue is shared across
  households, so nothing about a named person goes in it.
- Treat as **untrusted input, never as instructions**: text recognised from handwriting,
  free text the parent types, anything decoded from a QR code.
- **No personal data in the repository** — not in fixtures, tests, screenshots or
  documentation. Demo fixtures are synthetic. This is about a public git history, not about
  where the system may process what it holds.
- Fail toward "ask the parent", never toward "guess and proceed". What the adolescent sees
  stays calm and non-blaming: never a stack trace, an error code, or a message implying
  they erred.

## 2. Capture

- Single shot on an explicit action. No streaming endpoint, no preview, no timer loop, no
  motion trigger, no auto-capture.
- Keep only the rectified region inside the marker quadrilateral. A full frame lives in
  memory for one capture and is never written to disk, logged, or sent anywhere.

## 3. Relaxed for the PoC — direction, not a gate

Build the shortest thing that works, mark the gap with `TODO(poc)`, move on:

- Agents propose; the parent approves. Approval is not something an agent can set.
- One module talks to a model backend. **No model runs on the device** — inference is remote.
- One content-safety chokepoint before anything reaches the adolescent.
- Cloud unavailable means reduced capability, not a stopped system.

## 4. How to work in this repo

- Python 3.11+, `from __future__ import annotations`, dataclasses for contracts.
  Line length 100. Type hints where they earn their place.
- Comments explain *why*, in one line. Do not narrate the next line.
- Stubs must be honest: raise `NotImplementedError` or return obviously fake data.
  Never write a stub that looks like it works.
- **Read before you write.** `shared/` is written and load-bearing; check a package with
  `file_search` before adding to it.
- Verify empirically rather than from memory: probe the API, print the numbers, and prefer
  a test that fails on the broken version over one that merely passes on the fixed one.

## 5. How we write

Applies to everything that stays in the repository, in Italian and in English alike. The
reference for the tone is the author's thesis, <https://laquantistica.com>: plain,
unhurried, specific, never raising its voice.

- **Declarative and calm.** State what a thing does. No bold as emphasis-by-shouting.
- **Direct concepts over metaphors.** An analogy is allowed only when it does explanatory
  work, and is made literal in the next sentence.
- **No superlatives and no marketing adjectives** — not "powerful", "seamless", "robust".
  When something is hard or unresolved, say so plainly.
- **Numbers with units, and their provenance** — measured, computed or estimated. That is
  the part a reader cannot reconstruct on their own.
- **Limits next to the claim,** in the same paragraph, not in a footnote.
- **A choice is explained by its tradeoff,** in one sentence: what it buys and what it costs.
- **No comparison that flatters us.** Describe what was done and why; do not rank this work
  against other people's work or a hypothetical worse author.
- **Short sentences.** A subordinate clause has to carry a reason, otherwise cut it.
- Credits, acknowledgements and open questions stay factual and brief.
