# Non-goals

This file lists things Lanternina will not do. They are not missing features, not a roadmap, and not subject to "it would be easy to add". Several of them would be easy to add — that is precisely why they are written down.

Lanternina is built for adolescents, without asking which ones. Interest, appetite for novelty and comfort with text on a page vary across the whole range of cognitive ability, and at both ends of it; none of that needs a diagnosis and none of it is recorded here. A parent curates what the system offers. Every item below prevents the system from turning differences in preference, communication or performance into labels about the person.

If you fork this project, these are the lines that make it Lanternina rather than a different project with the same name.

Some of them were loosened on 27 August 2026, and each carries the reason its line now sits where it does. A rule broad enough to forbid legitimate work is a rule that gets routed around, and a loosened rule with its reason next to it is stronger than a wide one nobody can follow. Which lines are **not** moving is stated at the end, because distinguishing them is what makes the relaxation credible.

That is the general practice and not an exception made once: **a line here may be moved when moving it makes the experience better, and the reason is written beside it.** Several were written before anybody had run an afternoon and turned out to forbid things nobody meant to forbid. The five at the end are the ones that do not move, because they are about the adolescent rather than about the design. `docs/EVIDENCE.md` holds the reading behind a revision when there is one.

The rules an agent works under are in `.github/copilot-instructions.md`, which states the same lines more briefly. Neither is generated from the other: revising one means revising the other.

---

## The camera does not analyse people

The camera is handheld: a battery, one button, no screen, carried around. Faces will be in frame — friends, rooms, whatever happens to be behind the thing being photographed. Nothing about the framing prevents that, and a rule that depended on framing would quietly stop being true the first time somebody turned round. So every rule below is about what may be inferred, and none of them depends on where the lens is pointed.

- **No facial recognition.** Not for identification, not for "knowing who is at the desk".
- **No face detection.** Including as an intermediate step, including "only to blur it", including a library that does it internally.
- **No person or body detection**, no pose estimation, no hand or gesture tracking.
- **No emotion, affect, mood, stress, engagement or attention inference**, from images, from text, from timing, or from anything else.
- **No gaze or eye tracking.**
- **No age or identity inference.**
- **No biometrics** of any kind.
- **No description or assessment of a photograph.** The picture is transformed into something else — never described ("I see a chair"), never judged ("nice framing"). No recognisable face is returned to a display. A photograph of something irrelevant is accepted and transformed like any other, with no comment and no correction.

What is kept lands in a gallery its owner can see and delete from. Content Safety runs on inbound photographs as it does on generated output. Being able to delete is the guarantee here; not keeping anything stopped being one when the camera left the desk.

### It captures anywhere; it uploads only at home

The rule used to be "the device joins the home network only". That was containment written as a ban on the object: a camera carried around that only works at home is not a camera carried around, and the one use it exists for — photographing a thing where the thing is — was ruled out to buy something the narrower rule buys just as well.

So capture and transmission are separated. The device captures wherever it is and holds the frame; it uploads when it next sees the home network. Credentials and content still never cross a network nobody vetted, which is the whole of what the old rule protected.

## Capture happens only when somebody presses the button

- **No continuous capture.** No timer, no polling loop, no auto-capture when a sheet is detected, no burst mode.
- **No motion trigger.** Movement in the room is not an event this system reacts to.
- **No remote streaming.** There is no video endpoint, no MJPEG preview, no WebRTC, no "just for debugging" preview in the parent panel.
- **No remote trigger.** Nothing in the cloud, and nothing in the parent's panel, can take a photograph. Holding the button is the only path to the sensor having power, and the activity light is wired in series on that rail rather than driven from a pin — a light firmware can lie about is not evidence of anything.

The only trigger is a physical button press. It is answered on the e-paper display within seconds; what is built out of the photograph is proposed minutes later.

## Nothing durable here is a verdict about a person

The system may learn from what it sees, and does. A system that cannot change what it offers on the basis of what came back would be a fixed system, and it would make the same afternoon every week.

The line is duration, not judgement. A judgement about an *answer*, in the moment, is the function: an afternoon in which nothing could be got wrong would not be worth the hour, and the seventh property requires that every moment has an answer that can be wrong. What does not exist anywhere is a durable statement about who somebody is.

- **No assessment or diagnostic function.** This system does not screen, evaluate, or characterise cognitive ability, and will not manufacture a proxy for a diagnosis.
- **No stored verdict.** No score, grade, rank, level, ability estimate or progress trend, in the types, the storage, the prompts, the logs or the panel. `tests/test_boundaries.py` checks the stored shape, the panel and the prompts for that vocabulary; elsewhere in the code the word is harmless, and since 27 August 2026 it is allowed there.
- **No judgement outliving the moment it belongs to.** Telling somebody a date is wrong is the afternoon working. Recording that they get dates wrong is not, and there is nowhere to record it.
- **No comparison** to peers, to norms, to age expectations.

### No inference about stable traits of a person

The old wording was "no inference adjacent to a diagnosis", which forbade the system's own reading: recognising handwriting is inference, and noticing that a sheet came back nearly empty is inference. Both are how the afternoon is written.

The line is narrower and it holds: **no inference about stable traits of a person.** What somebody wrote on one page, on one afternoon, may be read and acted on. Who they are, what they are capable of, how they are getting on — none of that may be inferred at all, in the moment or otherwise.

Vision output describes ink on paper: "cell 3 is empty", "cell 4 has a mark". What that means, if anything, is for the parent to decide.

## Nothing here optimises for engagement

- **No streaks, chains, or "don't break it" mechanics.**
- **No daily goals or completion quotas.**
- **No variable or intermittent reward schedules**, no loot-box pacing, no surprise rewards timed to pull somebody back.
- **No unlockables gated on continued use**, no XP, no levels, no badges tied to frequency.
- **No leaderboards or competition**, with anyone, including oneself.
- **No notifications triggered by inactivity.** The system never says "you haven't been here in a while".
- **No engagement metrics** — time spent, sessions completed, retention, daily actives — as a success signal, a stored field, or a UI element.

Stopping is a legitimate outcome. Every activity can be abandoned at any point with no consequence and no follow-up.

The evidence behind this list, and its limit, is in `docs/EVIDENCE.md §4`. In short: expected, tangible, task-contingent rewards are best attested to reduce intrinsic motivation exactly where initial interest is high, which is the cell this system sits in. The same literature reports that for an activity nobody wants to start, a reward can be the way in — so this list declines a tool that works in a case Lanternina has chosen not to be in, and would have to be rewritten rather than pointed at if that ever changed.

## Nothing here can be failed

The line is **consequence**, not the existence of a right answer. A moment may pose a thing to work out, a code to break, a shape that fits, and one of the properties an afternoon is checked against asks for exactly that. What may not exist is a cost for getting it wrong.

- **No countdown, no score, no lost attempt**, and no step that has to be got right before the next one arrives.
- **No ending that reports how it went.** An activity that reached its ending early and one that reached it in full finish the same way, with the same object and the same closing, and neither refers to what was not seen.
- **No announcement that the system adapted.** A change of course arrives as part of what is happening. The system does not explain it, apologise for it, or ask whether it is all right.
- **Nothing is left to be discovered that the afternoon needs.** Where something has to be worked out, the way through is written down and given. Minimally guided instruction is the format that fails hardest for whoever has least prior knowledge (`docs/EVIDENCE.md §3`), and "nothing can be failed" must not quietly become "nothing is ever told".

Every activity that starts carries a written way to reach its ending from wherever it has got to. That is a property of the plan, checked before anybody sees it, rather than care taken while it runs.

## The parent does not watch it happen

The person who did the thing is the only source on how it went. This is a product choice and not a missing feature: if the parent already knows, the question at dinner becomes a check, and the account loses its worth.

- **No progress view while it runs.** Not step by step, not which help was given, not what came back off the glass.
- **No timing of a person.** How long somebody took over a moment is a measurement of them, and it is neither stored nor shown. How long a *model* took is an operational figure and is measured — a page is read in 4.4–5.5 s, an afternoon devised in 76–100 s — because a runaway agent and a cost that has lost its mind are visible in nothing else. The two halves are different data about different subjects, and the old rule "no per-step timing" collapsed them.
- **No list of questions to ask afterwards.** That is the same monitor written as prose, and the person would work out that the parent had been told.
- **No judgement on the live channel.** What a parent sends while something is running is a fact or a constraint — a new end hour, a pause, a broken printer, a missing material — as a typed message rather than free text. A sentence about how somebody is doing would enter the tone of everything written after it.

Afterwards is a different question and the answer is the opposite one. The parent approves an idea; everything after that is written as the afternoon goes, by an agent nobody vetted move by move, because there is no way to stand between a generated page and the room without stopping the afternoon. So the trade is made in the open: no veto on each piece, and every piece readable in full once it is over — the script, and every page and line the system wrote, in the order it wrote them.

Only that half is kept. What came back off the glass is read, and acted on, and then it is gone: the reading lasts as long as the afternoon needs it and is written nowhere. So nothing about it can be shown — not the pages that came back, not what was on them, not whether anything was finished. `tests/test_trail.py` names the fields the record has and none of them is about a person; `shared/vision_contracts.WhatCameBack` closes the implicit routes out of memory, and `tests/test_boundaries.py` holds that.

**There is one exception, it is named here beside the promise, and it costs something.** While this is being built, a household an administrator names keeps the other half too, so that an afternoon that went wrong can be read against what it was answering — an afternoon whose page came back and whose continuation was refused is otherwise a record of one side of a conversation. `panel/keeping.py` is the whole of it. It is off unless somebody turned it on, and every household nobody is working on has no row at all. It is turned on from the administrator's own surface and against their own directory, never the parent's, so nothing a fault in the parent's write path could reach can grant it. It lapses fourteen days after it was last set rather than waiting to be turned off, and every row it let through carries the same instant and is deleted the first time the record is read past it.

What that costs, said plainly: for as long as a permission stands, that household's record is a record of a person and not only of a machine, and the guarantee for it is a configuration rather than a property of the code. Until then it was the second, which is the stronger of the two. The trade was made on 28 August 2026, knowing which way it goes, because the alternative was diagnosing the system from one side of what it was doing. It is bounded in time, bounded to one household, and it is the first thing to remove.

The only account of how an afternoon went is the paper. It was not destroyed, it was left where it was — on a table, in a room a parent can walk into.

The operational timestamps are the one place this is not clean. They are on the system's own calls, not on anybody's work, but a determined reader can subtract two of them and learn how long fell between two moves. That is the cost of measuring the models at all, stated here rather than left to be found.

What the parent sees while it runs: whether it is running, how long is left, the controls, and any device that has failed. Before it starts, an overview of what was devised, with the ending behind an explicit click. Afterwards, one line about what was made.

## The system does not decide for the parent

The old rule was "features whose value is *the parent no longer has to think about this* are rejected". That blocked things worth building: a weekly summary of what was offered, a note that something is waiting for approval, a digest. None of those replaces the parent's thinking — a parent who is told more is more in the loop, not less.

The rule is about decisions, not convenience. **No decision is taken on the parent's behalf.** Convenience is allowed; delegation is not.

- **No agent self-approval.** Nothing an agent generates is delivered without the parent greenlighting it.
- **No adaptation the parent cannot see.** The system may change what it offers on its own, but what it offers arrives as a proposal in words the parent can read and refuse. The settings remain the starting point and remain the parent's to change.
- **No memory the parent cannot read.** The household memory lives in the cloud, so locality is not what keeps it honest. The parent can read all of it, in plain language, in the panel — a store read as sentences by the person who steers cannot quietly become a dossier. It is a short document: what has been offered, and what was configured.
- **No dashboard-triggered work in the house.** A parent write persists state and returns. It does not enqueue generation, notify, wake the home server, or put anything in a room, and nothing in the panel can start an afternoon — only the home server can, when it chooses to come and ask.


There is one place a parent's own action calls a model, and it is stated here rather than left to be found. A parent can open an idea, or a blank page, and work on it in a conversation: they suggest, a model rewrites the text, and they can type into the text themselves. That spends money, so the monthly limit governs it like every other call. What it does not do is any of the things the rule above is actually about — it reaches no room, wakes nothing, and what it produces is an idea that still has to be approved and still waits for the house to come for it.

It is also the one place a parent's words are instructions rather than material. Everywhere text a parent typed is stored and reused later — their interests, the things to avoid, the house guidelines — it reaches prompts doing other work and arrives quoted as JSON, because a sentence that reads like a command should not become one. A draft is different: the parent wrote it as the thing to build, they are looking at the answer, and they can type over it. Their words shape that draft and reach no other prompt, and what comes out of it goes through the same format, the same checks and the same gate as an afternoon nobody steered.

## Open, deliberately

These are not settled, and are listed so nobody assumes the permissive answer:

- **Audio.** Text-to-speech may be added; it is genuinely useful for someone who reads slowly. A **microphone is not currently part of the system**, and if one is ever added, "the system does not listen when not explicitly asked to" has to become a guarantee with a test behind it, not a promise. TODO(hackathon): decide and record the outcome here.
- **Escalation to the guardian.** Alerting on system faults and blocked content is in scope. Inferring something concerning about *the person* from their work is not, and will not be added without an explicit, separately-documented decision.

## The five that are not loosening

Six rules were relaxed on 27 August 2026, and a reader is entitled to ask where that stops. It stops here. These five are not narrowed, not qualified, and not subject to a later pass:

1. **No facial recognition, face detection, or person detection** — including as an intermediate step, including inside a library that does it without saying so.
2. **No emotion, affect, attention or gaze inference**, from images, from text, from timing, or from anything else.
3. **No remote or continuous capture.** One press, one frame, by the person holding the device.
4. **No engagement optimisation.** No streak, no quota, no variable reward, no nudge triggered by inactivity, no metric of time spent.
5. **No assessment of a person.** No score, grade, rank, level, ability estimate or progress trend, anywhere durable.

They coincide with prohibitions in the EU AI Act — emotion inference in educational settings, exploitation of vulnerabilities tied to age or disability, and social scoring — which is a useful check on the reasoning rather than the reason for it. This project would draw all five without the regulation, and the coincidence is what makes them the right place to stop.

The six that were relaxed are relaxed because they were forbidding legitimate work under the cover of one of these five. That is the test for any future change: a rule may be narrowed to what it was actually protecting, and it may not be narrowed past it.

---

Several of these are enforced mechanically in `tests/test_boundaries.py`. If you change the code so that one of them no longer holds, that test fails. Please do not delete the test — change the product, or fork it under a different name.

