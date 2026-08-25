# Non-goals

This file lists things Lanternina will not do. They are not missing features, not a
roadmap, and not subject to "it would be easy to add". Several of them would be easy to
add — that is precisely why they are written down.

Lanternina is built for adolescents, without asking which ones. Interest, appetite for
novelty and comfort with text on a page vary across the whole range of cognitive ability,
and at both ends of it; none of that needs a diagnosis and none of it is recorded here. A
parent curates what the system offers. Every item below prevents the system from turning
differences in preference, communication or performance into labels about the person.

If you fork this project, these are the lines that make it Lanternina rather than a
different project with the same name.

The rules an agent works under are in `.github/copilot-instructions.md`, which states the
same lines more briefly. Neither is generated from the other: revising one means revising
the other.

---

## The camera does not analyse people

The camera is handheld: a battery, one button, no screen, carried around. Faces will be in
frame — friends, rooms, whatever happens to be behind the thing being photographed. Nothing
about the framing prevents that, and a rule that depended on framing would quietly stop
being true the first time somebody turned round. So every rule below is about what may be
inferred, and none of them depends on where the lens is pointed.

- **No facial recognition.** Not for identification, not for "knowing who is at the desk".
- **No face detection.** Including as an intermediate step, including "only to blur it",
  including a library that does it internally.
- **No person or body detection**, no pose estimation, no hand or gesture tracking.
- **No emotion, affect, mood, stress, engagement or attention inference**, from images,
  from text, from timing, or from anything else.
- **No gaze or eye tracking.**
- **No age or identity inference.**
- **No biometrics** of any kind.
- **No description or assessment of a photograph.** The picture is transformed into
  something else — never described ("I see a chair"), never judged ("nice framing"). No
  recognisable face is returned to a display. A photograph of something irrelevant is
  accepted and transformed like any other, with no comment and no correction.

What is kept lands in a gallery its owner can see and delete from. Content Safety runs on
inbound photographs as it does on generated output. Being able to delete is the guarantee
here; not keeping anything stopped being one when the camera left the desk.

## Capture happens only when somebody presses the button

- **No continuous capture.** No timer, no polling loop, no auto-capture when a sheet is
  detected, no burst mode.
- **No motion trigger.** Movement in the room is not an event this system reacts to.
- **No remote streaming.** There is no video endpoint, no MJPEG preview, no WebRTC, no
  "just for debugging" preview in the parent panel.
- **No remote trigger.** Nothing in the cloud, and nothing in the parent's panel, can take
  a photograph. Holding the button is the only path to the sensor having power, and the
  activity light is wired in series on that rail rather than driven from a pin — a light
  firmware can lie about is not evidence of anything.

The only trigger is a physical button press. It is answered on the e-paper display within
seconds; what is built out of the photograph is proposed minutes later.

## Nothing here is a verdict about a person

The system may learn from what it sees. A system that cannot change what it offers on the basis of what came back is a fixed system, and a fixed system is the more likely failure. What follows bounds what it may conclude, not whether it may adapt.

- **No assessment or diagnostic function.** This system does not screen, evaluate, or
  characterise cognitive ability, and will not manufacture a proxy for a diagnosis.
- **No judgement reaching anybody.** Adaptation happens inside; it does not surface as a
  statement about how somebody is doing, on a display, on paper, or in the parent's panel.
  The parent sees what the system proposes to offer, and can refuse it.
- **No comparison** to peers, to norms, to age expectations.

Vision output describes ink on paper: "cell 3 is empty", "cell 4 has a mark". What that
means, if anything, is for the parent to decide.

## Nothing here optimises for engagement

- **No streaks, chains, or "don't break it" mechanics.**
- **No daily goals or completion quotas.**
- **No variable or intermittent reward schedules**, no loot-box pacing, no surprise
  rewards timed to pull somebody back.
- **No unlockables gated on continued use**, no XP, no levels, no badges tied to frequency.
- **No leaderboards or competition**, with anyone, including oneself.
- **No notifications triggered by inactivity.** The system never says "you haven't been
  here in a while".
- **No engagement metrics** — time spent, sessions completed, retention, daily actives —
  as a success signal, a stored field, or a UI element.

Stopping is a legitimate outcome. Every activity can be abandoned at any point with no
consequence and no follow-up.

## Nothing here can be failed

- **No countdown, no score, no lost attempt**, and no step that has to be got right before
  the next one arrives.
- **No ending that reports how it went.** An activity that reached its ending early and one
  that reached it in full finish the same way, with the same object and the same closing,
  and neither refers to what was not seen.
- **No announcement that the system adapted.** A change of course arrives as part of what
  is happening. The system does not explain it, apologise for it, or ask whether it is all
  right.

Every activity that starts carries a written way to reach its ending from wherever it has
got to. That is a property of the plan, checked before anybody sees it, rather than care
taken while it runs.

## The parent does not watch it happen

The person who did the thing is the only source on how it went. This is a product choice
and not a missing feature: if the parent already knows, the question at dinner becomes a
check, and the account loses its worth.

- **No progress view.** Not step by step, not which help was given, not what came back off
  the glass, not how long each part took.
- **No list of questions to ask afterwards.** That is the same monitor written as prose,
  and the person would work out that the parent had been told.
- **No judgement on the live channel.** What a parent sends while something is running is a
  fact or a constraint — a new end hour, a pause, a broken printer, a missing material — as
  a typed message rather than free text. A sentence about how somebody is doing would enter
  the tone of everything written after it.

What the parent does see: whether it is running, how long is left, the controls, and any
device that has failed. Before it starts, an overview of what was devised, with the ending
behind an explicit click. Afterwards, one line about what was made.

## The system does not replace the parent

- **No unattended operation as a goal.** Features whose value is "the parent no longer has
  to think about this" are rejected, not prioritised.
- **No agent self-approval.** Nothing an agent generates is delivered without the parent
  greenlighting it.
- **No adaptation the parent cannot see.** The system may change what it offers on its own,
  but what it offers arrives as a proposal in words the parent can read and refuse. The
  settings remain the starting point and remain the parent's to change.
- **No memory the parent cannot read.** The household memory lives in the cloud, so
  locality is not what keeps it honest. The parent can read all of it, in plain language,
  in the panel — a store read as sentences by the person who steers cannot quietly become a
  dossier.
- **No dashboard-triggered work.** A parent write persists state and returns. It does not
  call a model, enqueue generation, notify or wake the home server, or schedule work for
  later. Only the home server can initiate processing, when it chooses to make a request.

## Open, deliberately

These are not settled, and are listed so nobody assumes the permissive answer:

- **Audio.** Text-to-speech may be added; it is genuinely useful for someone who reads
  slowly. A **microphone is not currently part of the system**, and if one is ever added,
  "the system does not listen when not explicitly asked to" has to become a guarantee with
  a test behind it, not a promise. TODO(hackathon): decide and record the outcome here.
- **Escalation to the guardian.** Alerting on system faults and blocked content is in
  scope. Inferring something concerning about *the person* from their work is not, and will
  not be added without an explicit, separately-documented decision.

---

Several of these are enforced mechanically in `tests/test_boundaries.py`. If you change
the code so that one of them no longer holds, that test fails. Please do not delete the
test — change the product, or fork it under a different name.
