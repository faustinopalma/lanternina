# A game that ends

[08-experience.md](08-experience.md) is the log of what was built: the contract, the
devising agent, the runner, the clock. This file is a design for the same afternoon, taken
further than anything built so far, and it is not a decision. It was written outside this
repository as five documents — an architecture, a generation prompt, a JSON schema, an
executor contract and a validator, 51 KB in Italian — and the raw source is kept in
`_reference/afternoon-game/`, out of git.

This is meant to stand in for that source rather than summarise it: everything from it that
bears on what gets built is here, read against `shared/experience.py`, which is the contract
that actually runs. The one thing deliberately not carried across is its JSON schema, and
§18 says why.

The single idea underneath all of it: **an afternoon must be unable to end badly**, and
the way to get that is not care at runtime but structure decided before the afternoon
starts.

---

## 1. Two times with opposite properties

Devising is slow, repeatable, and can be checked before anybody sees it. Running is
reactive, sparse — thirty to eighty real events across an afternoon, one every several
minutes — and has no second chance.

Everything that can be decided and checked while devising must be. The runner should never
have to invent structure; it invents words inside a structure already known to be valid.

This is already the shape here: `shared/experience.py` parses a document a model wrote,
and `orchestrator/safety.py` screens the words. What the design adds is that the document
should be checked for *properties*, not only parsed for *syntax*. That difference is §7.

## 2. A moment with three weights

Today a moment is one thing. The design gives each one three versions with the same
narrative outcome and different cost: short, about a third of the time, one step and
material already to hand; standard; extended, with optional steps and one more object.

The weight is chosen on entering the moment and does not change until the next one. That
one sentence is what makes an afternoon shortenable without anybody noticing, and it is
worth more than any runtime cleverness: shortening becomes picking a column that was
written with the same care as the others.

**Limit:** three versions of every moment is three times the devising, and the model is
being asked to write the short one as well as the standard. Whether a model does that, or
writes the short one as a summary of the standard, is not known — it has not been tried.

## 3. The way out that exists everywhere

Every moment carries a written way to reach the ending from exactly that point, in under
twenty minutes, and the text of it must name a physical object the person has in their
hands at that moment.

This is the strongest idea in the whole set. It makes "the afternoon always ends" a
property of the document rather than a hope about the runner: whatever happens, there is a
written path to a complete ending, and the ending reached that way is the same ending —
same object, same closing, no reference to what was not seen.

The source says the generic exit is the recurring defect of generated plans: "the
character says goodbye and it is over". If the way out is not anchored to something already
built, the shortening is felt. It also says the fix is a check, not another line of prompt.
That claim is worth taking seriously because it is the same lesson `07 §1` and `08 §6`
learnt here: three defects were found by the real service and none by a test with a fake
model.

## 4. Help that is part of the story

Four levels per moment: a narrative nudge, a concrete clue, an almost explicit
instruction, and then the answer handed over as a gift inside the fiction. Each level
carries the number of minutes after which the next one arrives.

Two properties that matter more than the ladder itself:

- The same text is used whether the person asked for help or whether the time passed.
  Two voices for the same thing is how a system tells somebody it noticed they were stuck.
- After the last level the moment is over and the afternoon moves on. No further wait, no
  second attempt, nothing that has to be got right before continuing.

Help is always available, in every moment, and is not a concession. Here that means the
help path belongs to the runner rather than to the moment being run — otherwise a moment
can be written that has no way to ask.

## 5. Replanning, and the ending that starts by itself

The runner recomputes at every moment boundary and at fixed checkpoints before the end
hour. Time left, minus the cost of the ending, against the sum of the short weights of
what remains. If it does not fit, four things are applied in order: everything remaining
goes to its short weight; optional moments are dropped; adjacent mergeable pairs are
merged; and finally the way out of §3 is taken. The last one is always available, which is
what makes the guarantee hold rather than usually hold.

If there is more time than needed, the same order runs backwards.

**At thirty minutes before the end hour, the ending starts regardless.** In code, not as
something a model decides. Nothing is announced: no change of course is ever explained to
the person it happens to.

## 6. What is kept while it runs, and what is forgotten after

An afternoon is long and something will fail — the process, the network, the power. What
the runner needs in order to survive that is a record it can rebuild from: which moment,
which weight, what has already been printed, which help has already been given, the
current end hour, whether it is paused.

Not the history of a conversation. The concrete failure the source names is precise: if
you restart from nothing at 16:40 and print sheet three again, the person notices, and the
thing they were inside of breaks.

**This is the point where the design meets a rule here and has to be read carefully.**
`shared/experience.py` says nothing counts and nothing waits. The design counts minutes
and waits for them. The two are compatible, but only if the line is drawn where it belongs:
what may be counted is what is happening now, and it is discarded when the afternoon ends.
What may never exist is a number about a person that outlives the session. Help level three
in this moment, at 16:12, is a fact about an afternoon. "Usually needs level three" is a
verdict, and it is the field this project must never grow.

## 7. A filter on the way out, and a check before the start

Two mechanisms, at the two times of §1.

**Before saving**, a validator refuses a document that cannot be run well. The checks worth
their place, in order of what they buy:

| Check | Refuses |
| --- | --- |
| A way out of every moment, twenty minutes or less | the afternoon that cannot be shortened |
| The way out names an object already in hand | the goodbye that is felt as a cut |
| Short weights plus the ending fit the window | the plan that never fitted |
| The ending is reachable from every moment, and no cycles | the afternoon that loops or strands |
| Four help levels, increasing, the last one present | the moment with no way out of being stuck |
| Nothing from the block list in any written text | the praise and the blame, before they are said |
| No leftover placeholder, no open alternative | the document that reads as finished and is not |

`shared/experience.py` already refuses cycles while reading, which is one of these. The
rest are unwritten. The source calls the validator the best ratio of cost to benefit in the
whole system, and the argument is the same one that holds here: devising is offline, so a
devise → check → repair → recheck loop costs waiting, not risk.

Repair sends the model only the fields that failed, with the validator's message, and asks
for those fields back. A full regeneration changes the whole afternoon and reopens what was
already right.

**While running**, every string heading for a display or a printer passes one filter: a
length limit, a block list of words that praise, blame, hurry or score, and a ban on any
reference to the machinery — adaptation, shortening, time remaining, the parent, the
system, the model. If the filter rejects a text, the pre-written text from the document is
used instead. That fallback is why the written texts are mandatory in the first place.

Rejections should be counted by slot. A slot that is rejected often is a defect in the
devising prompt, not a case to handle at runtime. That makes the filter a measuring
instrument as well as a guard.

## 8. What the parent sends in, and what the parent sees

Two channels with different rules, and the design is emphatic that they must not be joined.

**Before**, anything: constraints, materials, themes, what to avoid, how long there is.
That is the legitimate place for whatever a parent wants to say.

**During**, facts and constraints only, as typed messages — a new end hour, more time,
pause, close now, this device is broken, this material is missing, an interruption. Not
free text. The reason is specific and is not about prompt injection: a sentence like "he is
being lazy, push him" enters the model's context and colours the tone of everything written
afterwards. A free text field aimed at the runner is the most dangerous thing on the whole
panel. If it is kept, a classifier maps it onto one of the types and the rest is dropped.

Nothing the parent sends produces a text that reveals the channel exists, and it is applied
at the end of the current moment, never in the middle of an instruction.

**What the parent sees is the harder half, and it answers the open decision left in
`08 §7`.** The design's answer is that the parent does not watch the afternoon happen: the
person who did it is the only source of how it went. That is a product choice and not a
missing feature — if the parent already knows, the question at dinner becomes a check, and
the account loses its worth.

So: the state of things, the time left, the controls, and any device that is broken, always.
An overview of what was devised, always — frame, roughly what gets built, how long, what
must be in the house, how many sheets — with the ending behind an explicit click and a
warning that it is the ending. Afterwards, one line about what was made.

And not: moment by moment progress, which help was given, what came back off the glass,
how long each moment took, which weight is running. Not a list of questions to ask, either
— that is the same monitor written as prose, and the person would work out that the parent
had been told.

The thing that starts the conversation is the object on the table, not the panel. That is
the load the artefact has to carry, and it is why it must be self-explanatory and orderable
— something that can be laid out and shown in sequence by somebody who does not remember
all of it.

## 9. The camera with no screen

A camera with no screen cannot be aimed badly and its result cannot be judged. The delay
between pressing and the picture appearing is technically a defect and narratively the film
developing.

Three rules, and they are stricter than the ones already written here because the existing
ones are about the scanner:

- The photograph is **transformed, never described and never assessed**. Not "I see a
  chair", not "nice framing". It is raw material for an image, not a subject of
  conversation.
- No person is identified and no recognisable face is returned to a display. The original
  does not outlive the session, and no photograph appears in the panel.
- A photograph of something irrelevant is accepted and transformed like any other, with no
  comment and no correction. There is no rejected-photograph path.

The display is one bit, or a few greys, at low resolution. An image generated without that
in mind arrives as a smudge: high contrast, large shapes, thick strokes, no gradients, and
that belongs in the image prompt rather than in hope. `HouseCapability.PHOTOGRAPH_TABLE` is
already named in `shared/capabilities.py` and no verb asks for it yet, which is the right
order — the rules above should be written before the verb is.

## 10. Variety by exclusion

A seed alone flattens after a few afternoons. What produces real variety is passing the
last N combinations to the devising agent as an explicit negative constraint, and refusing
a combination that matches a recent one on more than two dimensions. The difference that
matters is that the exclusion is checkable and the seed is not.

The same history moves the starting weight quietly: if the last three afternoons ended on
the short branch, the next one starts there. That is `§1` of the working rules — the system
may learn from what happens — and it stays on the right side of the line as long as it
appears in no text, is never called calibration, and is not shown anywhere.

## 11. One agent while it runs, decomposed by function and not by concurrency

Across an afternoon there are thirty to eighty real events, one every several minutes.
There is no concurrency to exploit. More agents at run time add only surfaces on which to
lose the thread: two voices writing the same character diverge within hours.

So the split is by function inside one loop, not by parallelism. The deterministic part
holds the moments, the timers, the counters, the print queue and the trigger for the
ending. The model proposes; the state machine disposes. The practical gain is that a
connection dropping halfway through an afternoon does not stop it: the timers keep running
locally, and every moment with pre-written text stays runnable with no model at all.

This is not what `agents/` looks like today, and it does not have to be: devising can stay
as many agents as it likes, because it happens once and offline. The rule is about the
running afternoon.

## 12. What the model may invent, and the points where it is called

"Poetic licence" with no stated boundary is not freedom, it is drift. The boundary:

**It may invent** the character's words inside the tone the plan fixes; the text of a
display that was not pre-written, within the length limit; the reading of what came back
off the glass or out of the camera; a detail of colour that adds no new task; which weight
to take on entering a moment; and a re-wording of help for somebody who has already seen it.

**It may not invent** new moments, new objects to build, new rules, new conditions for
going on, or an ending other than the one written.

The call points are few and each one is separate:

| Called for | Gives back |
| --- | --- |
| A page or object that came back | a narrative hook, and acceptance that is never refusal |
| A photograph | a prompt for the image, and a caption that does not describe it |
| Entering a moment | which of the three weights |
| A text slot not pre-written | the words, inside the tone |
| An ambiguous parent message | which typed message it is, if free text is kept at all |

Everything else is code: help escalation, transitions, replanning, printing, the ending,
the pause.

**Each call gets the minimum context it needs.** If every event makes the model re-read
everything and decide again, it reopens decisions already taken and the afternoon
oscillates. That is a specific failure with a specific cause, and it is cheaper to avoid by
construction than to detect.

## 13. What wins when two things disagree

In order, and the order is the whole point:

1. The invariants of §14.
2. The household's own constraints: what it will not have, what is not in the house, which
   rooms are out.
3. What the parent sent.
4. The text written in the plan.
5. What the model proposed.

When a parent's message is ambiguous, or pulls against the ending arriving safely, the
reading that leads to a complete and shorter conclusion is the one taken.

## 14. The invariants, as a list to check against

These are not requests to a model. They are properties the code applies: if what comes back
violates one, the runner drops it and uses the fallback written in the plan.

| # | Property | Where it is applied |
| --- | --- | --- |
| 1 | The ending always arrives, before the end hour | the trigger in code, never a model's decision |
| 2 | There is no terminal state that is a failure | the graph has no end node but the ending |
| 3 | Nothing is asked for that this house cannot receive | the set of possible inputs is closed |
| 4 | Nothing comments on how the person is doing | the filter on every text going out |
| 5 | Every moment has a way out under twenty minutes | checked before saving |
| 6 | Asking for help works in every moment | help belongs to the runner, not to the moment |
| 7 | No moment is repeated or redone | transitions only move forward |
| 8 | The parent's channel is never revealed | no generated text may carry a trace of it |
| 9 | Every photograph is accepted | there is no rejected-photograph branch |
| 10 | At most one change of weight every two moments | a counter in the runner |
| 11 | After the last help level the moment is over | a timer in the runner, and no further wait |
| 12 | Nothing already printed is printed again | the record of what was printed |

## 15. When a device is missing

The printer is the single point of failure of an afternoon made largely of paper: the toner
runs out at 15:30 and everything stops.

- The printer is asked whether it is well **before the afternoon starts**, not at the first
  failure.
- Every moment carries the version of itself that runs without printing, with its text
  already written and checked. Not error handling improvised by a model at the moment it
  fails.
- A plan whose moments do not all carry that version is refused before it is saved.

## 16. The ten dimensions, and what the written text has to be like

Variety is drawn along ten dimensions, and recording which was drawn is what makes the
non-repetition of §10 checkable: frame, the person's role, the mechanic, how it progresses,
what the paper is for, what the glass is for, what the displays are for, what the camera is
for, the tone, and the shape of the ending. The source lists a dozen candidates under each
and says two useful things about drawing from them: never take the option that comes first
or that would be the default, and when a combination does not hold together, redraw one
dimension rather than all of them.

It also names what to refuse by default, because they are what a model reaches for: pirate
treasure hunts, escape rooms with a countdown, question-and-answer quizzes, murder
mysteries, apocalypses, and the computer that has gone mad.

What the text itself must be like, and these are the lines that are easy to lose:

- One instruction at a time, saying what to do, with what, and where.
- Everything that matters exists on two surfaces — a sheet and a screen, or a screen and a
  button — so that missing one is not missing it.
- Nothing asks for speed, fine dexterity, strength, reading aloud, a phone call, going
  outside, or a specific thing learnt at school.
- Every action moves the story on. An approximate answer is taken as a valid one: what is
  recognised is the intention, not the precision.
- The register is for an adolescent — never childish, never school-like, never a tutorial.
  No remark on how the person did, and no question about themselves.
- **The plan does not contain its own reasons.** No reference to difficulty, to
  simplification, to adapting, to age, or to anything about the person. The text has to read
  as good design for anybody, because that is what it is.

## 17. Two things this design leaves open

**Who holds the button for help.** The source fixes one of three buttons as the help button
for the whole game, unchanging. Here a button belongs to a display, and there are two
displays. Either help moves to a surface that is always there, or an afternoon declares
which button it is and the runner enforces it for the duration.

**Whether approval stays where it is.** The source keeps approve-every-time as the default
but warns that it makes an afternoon depend on the parent being available at an unplanned
moment, and that the real risk is that nothing ever starts. Its answer is that the move to
running unattended should be something the system *proposes* after several afternoons that
ended well, not a setting buried in a page. That is in tension with the rule that the parent
approves, which is not up for quiet erosion. It is written here because leaving it unsaid
would let it arrive later as a convenience.

## 18. Where this disagrees with what is built

Stated rather than smoothed over, because these are the places where taking the design
whole would break something that works.

- **The hardware is not this hardware.** The design assumes three displays, three buttons
  with fixed roles for the whole game, a flatbed and a screenless camera. The house has two
  displays, a button per display, a printer and a scanner; the camera exists as a name. The
  fixed help button for the whole afternoon has no home yet.
- **`shared/experience.py` has four acts and no timers.** Weights, help ladders and minute
  thresholds do not fit the four moment types as they stand. Adding them is a format
  version, not a field.
- **A second contract must not appear.** The JSON schema in the source is a competing
  format for the same thing. Anything taken from it is taken as a change to
  `shared/experience.py`, never as a second document type.
- **The design is written for a game.** The house also runs reminders and sheets, and those
  are not games. The parts about tone and endings are about the afternoon, not about
  everything.

## 19. Where it starts, done when, what it costs

**Where it starts.** `shared/experience.py` for the contract and its reader.
`agents/experience_deviser.py` for the prompt already measured at 29.1 s from the hub.
`orchestrator/safety.py` for the chokepoint the output filter would sit beside.
`panel/routes/experience.py` for what the parent is shown, and `panel/rhythm.py` for the
clock. `_reference/afternoon-game/` for the raw source, if the wording of a check is needed.

**Done when.** An afternoon is devised, refused once by a check and repaired, approved, and
run to a complete ending in a session where the end hour is moved forward halfway through —
with nothing in what the person saw that says anything was shortened.

**What it costs.** The order below is the mitigation. Each step is worth having on its own
and none requires the next.

1. **The checks, and the refusal to save.** Nothing else in the repository has to change,
   and it is where every other step gets its safety from.
2. **The way out of every moment, and the ending that starts by itself.** This is what makes
   the worst failure impossible — an afternoon that does not finish.
3. **The record it can rebuild from.** Moves the running state out of whatever is holding
   it now, and makes a long pause implementable.
4. **Typed messages from the parent.** Replaces free text before free text exists.
5. **History, and variety by exclusion.**
6. **The three weights.** Needs the checks already standing.
7. **The camera.** Last, because it has the most surface, and only once §9 is written down
   and tested.

If it stops halfway, stopping after 3 leaves a system that never leaves an afternoon
without an ending.
