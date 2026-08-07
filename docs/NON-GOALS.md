# Non-goals

This file lists things Lanternina will not do. They are not missing features, not a
roadmap, and not subject to "it would be easy to add". Several of them would be easy to
add — that is precisely why they are written down.

Lanternina is built for one teenager with significantly below-average cognitive
functioning, curated day to day by her parent. Every item below is here because doing it
would harm that specific person, or would quietly turn the system into something other
than what her parent agreed to.

If you fork this project, these are the lines that make it Lanternina rather than a
different project with the same name.

---

## The camera does not look at people

- **No facial recognition.** Not for identification, not for "knowing who is at the desk".
- **No face detection.** Including as an intermediate step, including "only to blur it",
  including a library that does it internally.
- **No person or body detection**, no pose estimation, no hand or gesture tracking.
- **No emotion, affect, mood, stress, engagement or attention inference**, from images,
  from text, from timing, or from anything else.
- **No gaze or eye tracking.**
- **No biometrics** of any kind.

The camera is on a fixed arm at 90° over a sheet of paper, with a field of view narrow
enough that her face is not in frame. The software backs this up: if the ArUco quadrilateral
is not found, the pipeline stops rather than analysing whatever else is in the picture.

## Capture is single-shot and local

- **No continuous capture.** No timer, no polling loop, no auto-capture when a sheet is
  detected, no burst mode.
- **No motion trigger.** Movement in the room is not an event this system reacts to.
- **No remote streaming.** There is no video endpoint, no MJPEG preview, no WebRTC, no
  "just for debugging" preview in the parent panel.
- **No full frames retained.** Only the rectified region inside the marker quadrilateral is
  kept. The full frame exists in memory for the duration of one capture and is never
  written to disk, serialised, logged, or transmitted.

The only trigger is a physical button press.

## Nothing here assesses her

- **No assessment or diagnostic function.** This system does not screen, evaluate, or
  characterise cognitive ability. She has no diagnosis and this project will not
  manufacture a proxy for one.
- **No scores, grades, ranks, percentages, ability estimates, mastery levels, or progress
  trends.** Not stored, not computed, not displayed, not sent to a model.
- **No automated decisions about the person.** The system can propose; the parent decides.
  Difficulty and pacing do not change silently in response to how she performed. Silent
  adaptation is assessment under another name: it builds a model of her ability and acts on
  it, without anyone having agreed to that.
- **No comparison** to peers, to norms, to age expectations, or to her own past.

Vision output describes ink on paper: "cell 3 is empty", "cell 4 has a mark". What that
means, if anything, is for her parent to decide.

## Nothing here optimises for engagement

- **No streaks, chains, or "don't break it" mechanics.**
- **No daily goals or completion quotas.**
- **No variable or intermittent reward schedules**, no loot-box pacing, no surprise
  rewards timed to pull her back.
- **No unlockables gated on continued use**, no XP, no levels, no badges tied to frequency.
- **No leaderboards or competition**, with anyone, including herself.
- **No notifications triggered by inactivity.** The system never says "you haven't been
  here in a while".
- **No engagement metrics** — time spent, sessions completed, retention, daily actives —
  as a success signal, a stored field, or a UI element.

Stopping is a legitimate outcome. Every activity can be abandoned at any point with no
consequence and no follow-up.

## The system does not replace the parent

- **No unattended operation as a goal.** Features whose value is "the parent no longer has
  to think about this" are rejected, not prioritised.
- **No agent self-approval.** Nothing an agent generates reaches her without the parent
  greenlighting it.
- **No hidden adaptation.** If the system thinks something should change, it proposes it in
  words the parent can read and refuse.

## Data does not leave the house

- **No learner data in the cloud.** Her profile, her routines, her history and her scanned
  pages stay on the mini-PC. Only content-generation prompts and rectified page crops are
  sent to Azure.
- **No personal identifiers in model prompts.** Not her name, not an id, not her history.
- **No telemetry, analytics, or crash reporting** that carries anything about her.
- **No learner data in this repository** — not in fixtures, tests, screenshots,
  documentation, or example configuration. Demo material is synthetic.
- **No account for her.** She does not sign in to anything.

## Open, deliberately

These are not settled, and are listed so nobody assumes the permissive answer:

- **Audio.** Text-to-speech may be added; it is genuinely useful for someone who reads
  slowly. A **microphone is not currently part of the system**, and if one is ever added,
  "the system does not listen when not explicitly asked to" has to become a guarantee with
  a test behind it, not a promise. TODO(hackathon): decide and record the outcome here.
- **Escalation to the guardian.** Alerting on system faults and blocked content is in
  scope. Inferring something concerning about *her* from her work is not, and will not be
  added without an explicit, separately-documented decision.

---

Several of these are enforced mechanically in `tests/test_boundaries.py`. If you change
the code so that one of them no longer holds, that test fails. Please do not delete the
test — change the product, or fork it under a different name.
