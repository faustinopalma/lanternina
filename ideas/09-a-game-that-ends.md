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

**§20 is what was built on 23 August 2026.** Everything above it is the design as it was
written; that section says what of it now runs, what it cost, and where it turned out to be
wrong. The two are kept apart on purpose — a design edited to match what got built stops
being a thing anybody can be held to.

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

## 20. What was built, 23 August 2026

Steps 1, 2, 5 and 6 of `§19`, plus the output filter of `§7`. Step 3 — the record the
runner rebuilds from — got the half it needs and no more. Steps 4 and 7 are untouched.

### Format 2, and why it is a version

`shared/experience.py` is at `EXPERIENCE_FORMAT_VERSION = 2`. Every moment now carries
five things instead of two: an `id`, a `heading`, three `weights`, four rungs of `help`,
and a `way_out`. A `hand_over` also carries `instead`, and a `collect` also carries
`if_no_page`. An `Experience` also carries `drawn`, the ten dimensions of `§16`.

Four decisions inside that, each of which could have gone the other way.

- **The weight changes the minutes and the words, not the page.** A `hand_over` hands over
  the same design at all three weights. Three page designs per moment is three times the
  drawing for a difference nobody has asked for; what is lost is the short version of a
  page, and `§2` wanted one. Written where the field is, not here.
- **`in_hand` is a field, not a sentence.** The parser checks the way out names it in its
  own lines; `shared/experience_checks.py` checks that something earlier said it too. Two
  checks rather than one because the first alone can be satisfied by inventing the object
  in the last sentence, which is exactly the generic goodbye `§3` is about.
- **The version with no printer is two fields, not one.** `instead` is what a paper moment
  says when nothing came out; `if_no_page` is where the `collect` after it goes. Without
  the second, a house with no printer reaches a moment whose whole job is to read a sheet
  and has nowhere to go.
- **The walk that proves the ending is reachable from everywhere was written and taken
  out.** Edges only point forward and the last moment closes or asks, so no document this
  parser accepts can strand — there is no failing case to write, and a check nobody can
  fail is a claim. What is left over is the plan whose every ending says `ask`, and that is
  refused by name.

`experiences/un-pomeriggio-di-nuvole.json` was rewritten by hand into format 2 rather than
converted: weights, ladders and ways out are prose, and a script would have produced seven
copies of one sentence. It went from 3 123 compact characters to 10 543, the same seven
moments — 1 060 characters more per moment. Its longest path is 90 minutes short, 136
standard, 163 extended, against the 180 it says it lasts.

Format 1 did not go to `attic/`: it is the same module at a lower version, and there is no
document anywhere written in it.

### The checks, and one test per check

`shared/experience_checks.py` returns a list of `Complaint`, each naming a field the way
the document names it, so a repair can ask for that field back. Six of them:
the way out starts from something already in hand; the short version fits the window; there
is an ending somebody wrote; nothing from the block list; no placeholder left; not the same
afternoon again. `tests/test_experience_checks.py` has one test per check, and each one
takes a document that passes everything, breaks one thing, and asserts the refusal.

The block list is `shared/blocklist.py`, in five groups — praise, blame, hurry, score,
machinery — and it is used at both of `§1`'s two times, which is what keeps them one policy
rather than two. What it costs is false refusals, and the cost is bounded by where they
land: at devise time a repair round, at run time the pre-written text.

### The ending that starts by itself

`devices/run_experience.conclude_what_is_over`, called by the house's own ten-minute timer
before it does anything else. At thirty minutes before an afternoon's end hour the way out
of wherever it got to goes on the display; when that way out's own minutes are up, or the
end hour arrives, the ending follows and the run is deleted. `carry_on` does the same when
a page arrives after the ending is due.

Thirty minutes is what it has to be: the longest way out a document may carry is twenty,
and the timer may take ten to notice, so an ending that starts as late as T-20 still has
its twenty minutes and the close lands on the hour rather than after it.

**What this replaced was demonstrably wrong.** `forget_what_is_over` unlinked a run whose
hours had passed and said nothing to anybody — measured on the house at 14:02 on 21 August
2026, on `aft_5ec79e85`, begun at 09:17 and never finished. That is an afternoon that stops
without ending, which is the failure this project exists to prevent. The test asserts what
went on the display and in what order, so it fails on the old behaviour rather than merely
passing on the new one.

The weight is chosen in code, at every moment boundary: standard unless the longest path at
standard no longer fits, then short. That is the first of `§5`'s four steps and the only one
built. Extended is never chosen automatically — choosing to make an afternoon longer because
there is room is a decision about what somebody wants, and the runner does not know that.

### The filter on the way out

`orchestrator/outgoing.py`, beside the safety gate and not inside it: the gate asks whether
a text is harmful, over a network, and this asks whether it is the kind of thing this house
says, locally, in microseconds. A refused text is replaced by the pre-written text from the
plan, which is why the written texts are mandatory. Refusals are counted by slot and the
tally goes to the journal when the afternoon ends — a slot refused often is a defect in the
devising prompt, and a filter nobody reads the numbers off hides a bad prompt for months.

### The prompt, against the real service

`shared/experience_prompt.py` holds the format described once for both agents, generated
from the format's own constants. The devising prompt gained the ten dimensions, the recent
combinations as a negative constraint, the six things to refuse by default, and the six
properties of the text. `ExperienceDeviser.repair` sends the document back with the
complaints; `repair_unreadable` sends it back when it did not parse at all.

**Fifteen calls to the deployed Foundry deployment `gpt-5.6-sol-2026-07-09` on 23 August
2026, from this machine, through `tools/probe_devise.py`.** Three defects, and none of them
was visible to a test with a fake model.

1. **Every way out had the same `in_hand`, and it was not an object.** The first afternoon
   used "il bordo dello schermo" — the edge of the screen — for all five moments. The prompt
   had said "the object they are holding" and left what an object is to the model. It now
   says: a thing that exists in the room, a sheet, a pencil, a cup; never part of a screen,
   never an idea; and two moments usually have different things in hand.
2. **The repair reworded instead of repairing.** Handed the five complaints, the model
   returned "bordo dello schermo" — the same phrase without its article — and the fault was
   exactly where it had been. The repair prompt now says to change what the complaint names
   until the complaint stops being true, and that rewording is not a repair. Every repair
   after that change fixed what it was sent.
3. **A document the format would not read had no way back.** Two of the first seven answers
   were refused outright — a line of 45 characters against 44, and a fifth line on a screen
   that holds four — and the house was simply offered no afternoon. `repair_unreadable`
   hands the answer back with the parser's own message, which is why those messages name
   the rule *and* the offending number.

What it costs, measured. A first answer takes **71.4 to 103.2 s** (n = 12), against 29.1 s
for format 1 — the document is three times the size. It is **5 955 to 7 408 compact
characters** against a 20 000 cap, and **4 to 5 moments** against a range of 3 to 12, so the
model writes short afternoons and the cap is not what binds. A repair takes **15.6 to
35.3 s**, so a refused afternoon costs 87 to 135 s in all.

With everything above in place, **eight of eight afternoons ended usable**: three passed
first time, three were refused by the parser, two by the checks, and every one of the five
was fixed by a single repair. Before the two repairs existed it was five of seven.

Every one of the five parser refusals was a limit overshot by a small margin — 45 against
44, 5 against 4, 43 against 40. Stating the limits again inline, where the lines are asked
for, did not stop it; the repair is what stops it. That is worth knowing before anyone
spends an afternoon rewording a prompt.

### What is not built

1. **`§5`'s other three steps.** Optional moments are not dropped, adjacent moments are not
   merged, and there is no path backwards when there is more time than needed. Only the
   short weight and the way out are reached for.
2. **The record is `§6`, whole.** A run keeps which moment, which weight, which sheets have
   been printed, whether the ending has begun, how many rungs of help this moment has given,
   and the current end hour. All of it is deleted when the afternoon ends.
3. **Asking for help is not built.** The ladder is written in every moment, checked, shown
   to the parent, and now reached — but by the clock, not by a person. `§22` has what was
   decided and what `§17` still leaves open.
4. **The parent's channel is half built.** The afternoon obeys an end hour that moved; there
   is no route by which a parent can move it. `§23` says where it starts.
5. **The camera.** `§9`, untouched.
5. **Nothing has run on the house.** The hub has not been updated and the panel has not been
   rebuilt, so no adolescent has seen a way out. What has run is `§21`.

## 21. A house with no person in it, 24 August 2026

`devices/pretend.py`, `tools/pretend.py`, and one field on `House`. The division it is for
is the one the work now splits along: whether the toner is in and the scanner answers is
checked by standing in the room, and whether the afternoon reads well is checked without
leaving the desk.

**The boundary is the person, not the hardware, and that is what makes it worth having.**
When it is on, the model is the real one, the page is composed and rasterised from the same
`Drawing` the PDF comes from, its markers are found, it is rectified, its QR is decoded, and
**the crop goes to the vision model in the cloud over the same device-key route the hub
uses**. One thing is injected: where the ink is. Everything else that a simulator usually
throws away is still there, and it is exactly the half this repository's defects have come
from — the ink arithmetic that passed its synthetic test and produced 12 false positives out
of 13 on real paper, three devising defects the real service found and the fake-model tests
did not.

What is not exercised: paper, the print queue, the scanner, a display that has to wake up.

**Measured on 24 August 2026.** An afternoon devised against `gpt-5.6-sol` in **90.7 s**
(2 189 input tokens, 6 281 output, of which 4 569 reasoning). Played from its first display
to its close in **2.4 s**, of which 2.2 s was the cloud reading the page. The same afternoon
taken to the ending that starts by itself — three hours of clock — in **2.5 s**, by moving
the clock by hand twice. Against that: a scan alone is 37 s, and an afternoon is three
hours.

The reading was right, which is the part worth stating rather than assuming. Ink was drawn
in one of the sheet's two places, and the model reported ink in that place and not in the
other.

**One flag, not two, and the recording is why.** A transcript of an afternoon on disk is a
durable record of what somebody did, which `§6` and the working rules both forbid. It is
written here because the person on the other side is whoever typed the command, and it is
bound to the simulated house rather than being a setting of its own — a real house has no
`pretend` directory, so there is nothing for a real run to record into. `tests/test_pretend.py`
asserts that, and asserts that no transcript line carries a word for a verdict.

**What it found on its first run.** Two things, both real.

- The deployed panel is still serving format 1, so an afternoon that reaches `ask` is
  refused by its own continuation route with `an experience carries ['drawn'], which this
  format does not define`. That is not a defect in the design; it is the deployment being
  behind the commit, and it is now visible instead of waiting to be discovered in the house.
- `MAX_DIMENSION` was 40 characters and was too tight: the real service was refused twice in
  a row over it, at 41 and 43 characters, for phrases like "un tavolo di casa nel tardo
  pomeriggio". A dimension is compared with other dimensions and never shown to anybody, so
  the limit was arbitrary and is now 60.

### What is next, and where it starts

Two things, and neither is design work. **Both were done on 24 August 2026**; what follows
is kept because the reasoning and the traps are worth more than the tick.

**1. The panel was behind the commit.** `panel/routes/experience.py` and everything under it
had been at format 2 since `7ec527c`; the running revision was built before that, so an
afternoon that reached `ask` was refused by the panel's own continuation route with
`an experience carries ['drawn'], which this format does not define`.

*Done:* image `panel:5da465c`, built in ACR in **59 s** server-side with `--no-logs`, then
`az containerapp update --image` rather than a full deploy, because a full deploy demands
parameters that reset the access configuration if they are guessed wrong. Revision
`--0000048`, traffic 100%.

*The proof:* `python -m tools.pretend play --hand marks` now reaches a close. The house
asked, the panel wrote three more moments in **46.7 s**, and the runner played them — a
whole afternoon, devise excluded, in **49.3 s** with nobody in the room.

**2. The device key was exposed and is now rotated.** On 24 August 2026 a PowerShell command
that was setting environment variables failed part-way and printed the value it was setting.
The key grants the device routes — reading a page, asking for an afternoon, continuing one.

*Done:* a new 48-character key in three places, in this order, because the hub is what breaks
if the three disagree: the container app secret, `secrets.local.yaml`, and
`/etc/lanternina/panel.env` on the hub. Verified by fingerprint rather than by value —
`tools/key_fingerprint.py` prints a salted digest — and then by asking the panel: the new key
answers 200, the exposed one answers 403, and the hub's own `lanternina-afternoon.service`
runs clean.

*Two traps, both paid for.* A container app secret does not take effect until the revision is
restarted, and `az containerapp secret set` says so in a warning that is easy to scroll past;
the old key went on working for 20 s after the restart. And a multi-line rotation is the wrong
shape: this one broke after its first line, leaving the hub and the local file on the new key
and the panel on the old, which reads exactly like a bad key rather than like a half-finished
job. Do it in one command, or check all three fingerprints before believing any of them.

The lesson is worth keeping separately from the incident: a secret read from a file must be
read inside the process that needs it. `tools/pretend.py` does that now. A shell that fails
while setting an environment variable prints what it was setting, and there is no way to
un-print it.

## 22. The ladder reaches somebody, 24 August 2026

`devices/run_experience.offer_help`, on `deploy/lanternina-help.timer`, once a minute.

Until today every moment carried four rungs of help that nothing could reach. That is a
third of what a model writes, refused by the format when it is missing, read by the parent,
and going nowhere. It was the largest piece of dead weight in the design.

**A rung arrives because minutes passed, and it is the same words somebody would have got
for asking.** That is `§4`'s own rule, and it is why building the clock half first is not a
compromise: the asking half, whenever it arrives, calls the same function with the same
text. What `§17` still leaves open is only which surface the asking lands on.

`after_minutes` counts from arriving at the moment, not from the rung before. 3, 6, 10, 15
means the answer at fifteen minutes, not at thirty-four, and that reading is what makes the
format's refusal of a ladder that does not go up mean anything.

**Its own unit, at one minute, with no network.** The afternoon's unit keeps its ten-minute
rhythm because everything it does is a request to the panel and none of it is due to the
minute; a rung written to arrive after three minutes is not honoured by a timer that runs
every ten. The ladder is in the run file on the local disk and a rung is words on a display,
so a house that cannot reach the panel still gets its help.

**Two lines it does not cross, and both are decisions rather than omissions.**

- *After the last rung, nothing.* `§4` says the moment is over and the afternoon moves on.
  Here the only moment an afternoon waits at is a `collect`, so moving on would mean ending
  the afternoon because nobody came back — an action triggered by silence, which is the
  shape the working rules forbid outright. The ending stays where it is: the clock at T-30,
  which is about the hour and not about the person.
- *Nothing says that time passed.* A rung can only be the same words as an answer to a
  question if it never mentions the question not having been asked.

**What is kept, and what it may not become.** The run gains two fields: when the afternoon
arrived at the moment it is waiting at, and how many rungs that moment has given. Arriving
at the next moment resets both, which is what keeps them facts about a moment rather than
the beginning of a tally — there is nowhere to write how much help an afternoon needed in
total, and both are deleted with the run.

**Watched in the simulator**, which is what it is for. An afternoon begun and left alone for
sixteen minutes drew its four rungs at 2, 5, 9 and 13 minutes: *turn the map towards the
glass*, *find the side with the pencil line*, *put that side against the glass*, *the screen
shows the sheet on the glass*. Each one a step further into the thing itself, the last
handing the answer over as something the story gives. Sixteen minutes of afternoon in 1.4 s.

**One defect, and it is the kind a test catches only if it is written the right way round.**
The first version treated `waited_since` as absent when it was falsy, and zero is a
legitimate instant — so a ladder counted from zero never arrived at all. Seven of the twelve
tests failed on it. A test that had checked only the bookkeeping would have passed.

## 23. The end hour can move, 24 August 2026

`shared/message.py` and `devices/run_experience.hear`.

`§8` says a parent may send facts and constraints into a running afternoon, as typed
messages and never as free text, and the reason is not prompt injection: a sentence like
"he is being lazy, push him" enters the model's context and colours the tone of everything
written after it. The defence that works is not screening the sentence. It is having nowhere
to put one, and that is what this format is — a closed list with a number where a number is
needed, read by code, never by a model.

**Two things a parent may say, and the shortness is the design.** The afternoon is over by
this hour, or the ending comes forward to now. `§8` lists more — pause, this device is
broken, this material is missing, an interruption — and each of those needs the runner to do
something it cannot do yet. Writing them into the vocabulary now would be words with no
verbs behind them, so they are named as not built rather than declared and ignored.

**Moving the hour later is the same message with a later number.** There is no separate
"more time", because two ways of saying one thing is how they drift apart.

**Closing now is not stopping.** It sets the end hour to this instant plus the thirty minutes
the ending needs, so the afternoon finishes the way it always would have: the way out of
wherever it got to, then its close. Reusing the one path to an ending means there is no
second way to finish, and therefore no second way to finish badly.

**Applied at once, felt at a seam.** `§8` says a message is applied at the end of the current
moment and never in the middle of an instruction. That holds here without any waiting,
because moving the end hour changes nothing anybody can see — what it changes is when the
clock next decides the ending is due. The one place it bites is an afternoon already on its
way out: the way out is in somebody's hands, and moving the hour under it would either cut
it short or leave it hanging, so a message arriving then is ignored.

**Nothing announces it.** `§8` is explicit that no text a parent sends may reveal the channel
exists, and the way to be sure is that the function draws nothing at all. A test counts the
screens before and after.

**The end hour is now a field on the run** rather than arithmetic on when it began, which is
the last of the three things `§6` says a runner must be able to rebuild from. A run written
before today still has one: it falls back to the length the document declares.

**Watched in the simulator.** An afternoon begun, two rungs of help given, the parent saying
*close now* — nothing on the display at that instant — the ladder carrying on to its fourth
rung, and then the way out. The person sees an afternoon that ended; there is nothing in it
about an hour having moved.

**The acceptance test of `§19` is met, less two things.** `tests/test_message.py` runs an
afternoon that is begun, helped, has its end hour pulled forward halfway through, and
reaches its written close, and then walks every screen it drew past the block list. What is
still missing from `§19`'s sentence is the parent themselves: approval, and the channel.

### What is next, and where it starts

**The channel.** Nothing sends a message yet. The house has to pull them, because a dashboard
write is inert and only a request the home server makes starts anything.

*Where it starts:* a store beside `panel/reminders.py`, which is the closest thing and holds
something a parent typed; two device routes in `panel/routes/`, one to hand over what is
pending and one to say it was heard; the ten-minute look in `devices/afternoon.py`, which is
already the place the house asks the panel things; and a control in
`web/src/sections/Experiences.tsx`, next to the afternoon it belongs to.

*Done when:* a parent moves the end hour in the panel, and the afternoon in the house ends by
it without anything on any display saying so.

*The trap to expect:* an in-memory store on a container app that scales to zero loses a
message written a minute before, and a message meant to be picked up within ten minutes is
exactly the thing that failure hides in.

*Done 24 August 2026,* in `§24`.

## 24. The channel, 24 August 2026

`panel/messages.py`, `panel/routes/messages.py`, `devices/afternoon.listen`, and a control
in `web/src/sections/Experiences.tsx`. The order above was followed as written and nothing
in it turned out to be wrong.

**A row the panel holds, and the house coming for it.** Four routes: the parent writes one
and reads what is still waiting; the house collects and says which one it heard. There is no
route the other way and the panel is not given one, so what a parent presses takes effect on
the house's next look rather than at the moment they press.

**The trap was real and the answer was not the interesting part.** `CosmosMessageStore` sits
beside the in-memory twin the tests run against, exactly as every other store here does. What
was worth deciding is what the store holds.

- **A list, not one row per household.** `hear` takes a sequence and folds it in order.
  Keeping only the last would give the same answer today, because both things a parent may
  say assign the end hour outright — but that is a property of this vocabulary and not of the
  channel, and it stops being true of the first message that is not an assignment.
- **Cleared by id, by the house.** A message the parent writes while the house is midway
  through the one before it is still there afterwards.
- **An hour, and then it is gone** — six looks of the house's ten-minute timer. What it buys
  is that a message cannot reach an afternoon it was not written about. What it costs is that
  one written while the house is off is lost rather than reported, and the parent sees it
  disappear. `tests/test_message_channel.py` reads the interval out of
  `deploy/lanternina-afternoon.timer`, so changing the timer and not the lifetime fails.

**Asked before the ending is decided, and that is the only ordering that matters.** The
timer's next act is to ask whether an afternoon's hour has come; an hour that moved after that
question would wait ten minutes, and "close now" that takes ten minutes is not what the words
say.

**A message the house cannot read is left rather than cleared.** It means the two sides
disagree about what may be said, which is ours to fix; saying it was heard would hide that,
and it stops being offered within the hour anyway.

**The control is a time field and two buttons, beside an afternoon the house has begun.**
There is no box to type in, which is `shared/message.py`'s whole argument rather than an
omission, and a test asserts the page has no text field at all. Until today the same place
said an afternoon already begun was out of reach; it now offers an hour, and nothing else.

**Measured on 24 August 2026.** Image `panel:9ee9c7b` built in ACR in **55 s** server-side
with `--no-logs`, then `az containerapp update --image` rather than a full deploy. Revision
`--0000049`, traffic 100 %. The house's own route answered **200 in 0.33 s** against the real
Cosmos store, and clearing a message that does not exist answered `{"heard": false}` — the
read and the delete both exercised in the deployment rather than only in a twin. 655 tests,
17 of them new; 51 in the panel.

**What is still unproven, and it is one thing.** The parent's write reaches Cosmos through
`create_item`, and that path needs a signed-in parent, so nothing above touched it. The panel
front end publishes itself from `main`; the first press in a browser is the proof.

**In the house, the same afternoon.** The hub was three sections behind: `shared/message.py`
was not there at all, `devices/afternoon.py` had no `listen`, and `shared/experience.py` was
still at format 1 — so the panel was devising documents the house could not read, with two
afternoons sitting unapproved and a timer saying `2 waiting for the parent` every ten minutes.
Installed by shipping what `git archive` holds, extracted as `root:root 644` to match the tree
it lands in, and `lanternina-help.{service,timer}` enabled, which is `§22` reaching a room for
the first time. The house then asked the panel on the real route with its own key: **200 in
0.148 s**, `{"messages":[]}`. The once-a-minute help run costs **1.1 s of CPU** and touches no
network.

**One defect found, and it is in the tool that exists to prevent it.** `scripts/hub-stale.ps1`
compared `devices/*.py` and `shared/*.py` and reported a clean hub while `orchestrator/` was
missing entirely — `devices/run_experience.py` imports `orchestrator.outgoing`, so the import
failed on the first try. A check that looks at two directories can only answer about two
directories. It now takes the list of packages the hub runs, walks them, says so out loud when
there is nothing to report, and was made to fail on this morning's hub before being believed.

**The hub is not containerised, and that is now the largest gap between the two halves.** The
panel is an image in a registry; the house is a tar extracted into `/opt/lanternina`, run by
`/usr/bin/python3` under seventeen systemd units, with its Python dependencies satisfied by
whatever the machine happens to have. There is no declared list of what a new machine needs.

`deploy/hub-install.sh` is that list, written the same day: nine packages, the tree, the
units, and a `--check` that says whether a machine has them. Verified against the working hub,
where it found nothing, and then against a copy of itself naming a package that does not exist
and a variable that is not set, where it reported both and exited 1. `--install` has never
been run, because that takes a second card.

**Containerising was considered and deferred, with numbers rather than taste.** The recursive
dependency closure of what the code imports is **597 packages and 1378 MB installed** on
aarch64 Debian 13; the card is 14 GB with 5.3 GB free. An image would carry the same weight,
need building for arm64, and run a `podman` per oneshot for a unit that fires once a minute
and costs 1.1 s of CPU. It would also give up most of what a container is for: `lp`,
`scanimage` and `avahi-browse` reach cupsd, the scanner and the avahi socket, so it would want
host networking and the host's D-Bus, while the units already have `ProtectSystem=strict` and
`ReadOnlyPaths=/opt/lanternina`. And it would not remove the list — cupsd, avahi-daemon and a
scanner on the network are requirements of the machine either way. What it buys is Python
versions independent of Debian's and one artefact instead of two steps. The answer changes
when there is a second machine, or a platform that is not Debian.

**One test broke itself, and the lesson is worth more than the fix.** Two of the seventeen
built messages at a fixed calendar instant, 14:00 on 24 August 2026, and asserted the store
hands them over. They passed at 13:41 and failed at 14:30, because a message is only offered
for an hour and the wall clock had walked past it. A test that measures something with a
lifetime has to be written from the running clock, or it is a test with an expiry date.

### What is next, and where it starts

**Approval.** `§19`'s sentence asked for an afternoon devised, approved by a parent, and run
to its ending, and the approval is the half that has never been walked end to end in one
sitting: the simulator devises and plays but decides for itself, and the panel decides but
cannot run anything.

*Where it starts:* `tools/pretend.py`, which already has every verb except the one that waits
for a decision the panel recorded.

*Done when:* one command devises an afternoon, stops until a parent approves it in the
browser, and then plays it to its close.

*The trap to expect:* the simulator holds the device key and the parent holds a bearer token,
and they are different credentials for the same household. A command that quietly used the
device key to approve would pass its own test and prove nothing.

**The language of the house reaches one agent out of four.** Noticed by the parent on
24 August 2026: of the two afternoons waiting to be approved, one was written in English.
`panel/preferences.py` has held the household's content language since the beginning, and
`web/src/i18n/index.tsx` states the rule at length — the display and the paper follow the
household's setting and must never follow a browser preference, because content approved in
one language is not approved in another. The rule is right and it is not carried.

Where it actually goes today:

* **Devising** is correct. `panel/routes/experience.py` reads the household's preferences and
  passes `LANGUAGE_NAMES[...]`, so the deviser is told "Write every word of it in Italian" —
  the name, not the code, which is the fix `§20` already paid for once.
* **Continuing is not told at all.** `agents/experience_continuer.py` says "in the same
  language as the experience", and `panel/continuing.py` never mentions preferences. The rest
  of an afternoon inherits whatever the first half happened to be, so a document that drifted
  once stays drifted for the rest of its life.
* **The wording of a reminder is not told either.** `agents/reminder_wording.py` says "the
  same language as the sentence" and `panel/wording.py` does not read preferences. That one
  is defensible — the parent wrote the sentence — but it is inference, not the setting.
* **The content agent passes the code and not the name.** `agents/content.py` writes
  `Lingua: it`, which is the exact shape of the defect `§20` records: a two-letter code inside
  a sentence, where `it` is also an English pronoun.

*Where it starts:* the three call sites that build a prompt without a language —
`panel/continuing.py`, `panel/wording.py` and `agents/content.py` — and the one place that
already does it right, `panel/routes/experience.py`, which is the shape to copy.

*Done when:* a household set to Italian cannot be handed anything in another language by any
path, and the check is a test that walks every prompt this repository builds and fails on one
that carries no language.

*The trap to expect:* the language belongs to the household and not to the document, but a
continuation that is told "Italian" while holding an English document is being asked to do two
things at once. Whether the setting corrects a drifted afternoon or only prevents the next one
is a decision, not a detail, and it has to be made before the code is written.

**An afternoon that ended leaves its last screen in the room.** Found in the house on
24 August 2026, from the other end: the parent said both displays had been showing old text
for days and no picture had appeared. `devices/house.show` writes `screen-<label>.bmp` and
nothing ever removes it. `_forget` deletes the run file and the pages — "an afternoon that
ended leaves nothing behind, not even that it happened" — and leaves the screens, so the words
of a moment stay up until some later afternoon happens to overwrite them.

Measured on the hub: `screen-CF7D04.bmp` last written **21 August 09:17** and
`screen-FB9F18.bmp` **21 August 10:49**, three days earlier, both from the run
`conclude_what_is_over` was written to replace. A picture had been painted for CF7D04 that
same afternoon at **14:23** and nobody had seen it, because `devices/trmnl_byos.py` chooses
remind, then sheet, then picture, and a sheet layer that never ends outranks a picture
forever. This is the defect the picture layer's own comment describes one storey down —
FB9F18 showed a picture for a day and a half after it stopped being the picture display — and
the sheet layer was given no ending at the time.

The second display is not a fault: the parent gave FB9F18 `sheet` and `remind` and no
`picture`, so it has nothing to paint. Only the stale text is wrong.

*Where it starts:* `devices/house.py`, which is the one module that knows which files are
sheet layers — `sheet_file` already computes them to pick one at random — and
`conclude_what_is_over`, which is where an afternoon is known to be over.

*Done when:* an afternoon that reaches its ending leaves no screen behind, and a house whose
display holds both jobs is back to its picture by the next turn of the picture timer.

*The trap to expect:* `sheet_file` picks a display at random **per process**, so the moments of
one afternoon can be spread over every display that holds the job. Clearing only the one this
run happens to have resolved would leave the others exactly as they are now, and the test would
pass on a house with one display.

**The button does not reach the afternoon.** Found by running one, on 24 August 2026, and it is
the largest of the three. A page came back from the glass, was scanned and read correctly —
`read sh_3efc270b: mappa=segno, titolo=segno, vicini=segno, separati=segno, incrociati=segno`,
in 29 s — the display said something about it, and the afternoon did not move. It stayed at its
`collect` and would have stood there until the clock ended it.

The wiring goes to the wrong reader. The display server writes `button.json`,
`lanternina-scan.path` starts `lanternina-scan.service`, and that runs `devices/scan_sheet.py`,
which is the standalone-sheet path: it reads the page, describes it, deletes the button file
and stops. The afternoon's own reader, `run_experience.carry_on`, exists and has a unit —
`lanternina-experience@carry-on.service` — and **nothing anywhere starts it**. `grep -rl` over
`/opt/lanternina` and every unit finds no caller. The simulator has never shown this because
`tools/pretend.py hand` calls `carry_on` directly.

*Where it starts:* `devices/scan_sheet.py`, before it scans. `waiting_runs(sheets_dir)` already
answers "is an afternoon under way", and it is the only thing that can be known before a page
is on the glass.

*Done when:* a sheet put on the glass during an afternoon moves that afternoon on, and a sheet
put there with no afternoon running is still described the way it is today.

*The trap to expect:* both readers scan, and a scan is 29 s of a person standing at the
scanner. Deciding after the scan means scanning twice; deciding before it means deciding from
"a run is waiting" rather than from what is actually on the glass, so the run's own QR check
has to stay the thing that refuses a sheet from somewhere else.

**A way out told the person to read the screen they were reading it on.** The afternoon that
ran on 24 August left by `send-map`, and its way out said: *Riprendi il foglio dal vetro.
Posalo accanto alla tazza. **Leggi la chiusura sullo schermo.** Il pomeriggio è finito.* The
closing then arrived on that same display, replacing those words up to 60 s later, with
nothing to say that the new text was the closing the old text had promised. The parent read it
and asked what it meant, which is the only test that matters.

Two different things are wrong in one sentence.

* **A way out may not send somebody to a surface it is itself occupying.** `shared/experience.py`
  already refuses a way out that does not name an object in hand, because `§20` measured that
  models write "the edge of the screen" when asked for an object. Nothing yet refuses a way out
  that treats a display as a place to go and look.
* **"The screen" is not one thing in this house.** `devices/house.sheet_file` picks among the
  displays holding the job **at random, per process**, so the early moments went to CF7D04 and
  the way out and the closing to FB9F18. The words of one afternoon scattered across two
  objects in the room, and a sentence naming "the screen" stopped having a referent. The random
  choice is written down as a deliberate cost — a notice appears on one of them and somebody at
  the other does not see it — and this is the first time the cost has been paid where it hurts.

*Where it starts:* `shared/experience_checks.py`, which is where a rule about what a way out may
say already lives, and `devices/house.sheet_file`, which is where "which display" is decided.

*Done when:* an afternoon cannot be saved whose way out points at a display, and the moments of
one run all reach the same display.

*The trap to expect:* refusing the word "schermo" is not the rule — a moment may legitimately
say what is on a display. What may not happen is a way out deferring the ending to somewhere
else. A check written against the word will refuse good documents and pass bad ones.

## 20. What was built, 23 August 2026

Steps 1, 2 and 6 of the order above, plus the output filter, the ten dimensions and the
first half of 3. The order was changed on purpose: the three weights were meant to come
sixth, and they came first, because the way out and the ending that starts by itself are
both arithmetic over minutes, and minutes per moment is what a weight is. Building the
checks first and the weights sixth would have meant checking a document that could not yet
express what the checks are about.

### Format 2 of `shared/experience.py`

Every moment now carries five things instead of two: an `id`, a `heading`, three
`weights`, four rungs of `help` and a `way_out`. A `hand_over` also carries `instead` — the
words for the same moment with no printer — and a `collect` also carries `if_no_page`,
which is where the afternoon goes when nothing came out of the printer at all.

Four decisions inside that, each of which could have gone the other way.

- **The weight changes the minutes and the words, not the page.** A `hand_over` hands over
  the same design at all three weights. Three page designs per moment is three times the
  drawing for a difference nobody has asked for, and it is the kind of thing that can be
  added later without a third format version.
- **`in_hand` is a field, not a sentence.** The way out has to name the object, the object
  has to be in the way out's own text, and something at or before that moment has to have
  mentioned it. The first two are refused by the parser; the third needs the whole document
  and is a check. `§20`'s measurements below are the reason this is three separate rules
  rather than one line of prompt.
- **Format 1 was not moved to the attic.** It is the same module at version 2, and the
  version number is the thing that refuses an old document. An `attic/` copy would be a
  second definition of a word that already has one.
- **The walk that proves an ending is reachable from every moment was written and then
  taken out.** With forward-only edges and a last moment that closes or asks, no document
  this parser accepts can strand — so it was a check nobody could write a failing test for.
  What is left over is the plan whose every branch says `ask`, and that is a check that can
  fail. The argument is in `_check_graph` and the test that stands in its place is
  `test_a_branch_cannot_be_written_that_strands`.

The hand-written afternoon in `experiences/` was rewritten rather than converted: the three
weights, the four rungs and the seven ways out are new prose and no script could have
invented them. It went from **3 123 to 10 543 characters** of compact JSON — measured, the
same seven moments — which is 1 060 characters more per moment.

### The checks that refuse before saving

`shared/experience_checks.py`, six of them, each returning a list rather than raising,
because what is done with a refusal is a repair request naming the fields that failed.
`tests/test_experience_checks.py` has one test per check and each takes a document that
passes everything, breaks one thing, and asserts the refusal.

The block list is in `shared/blocklist.py` and is used twice, which is the whole reason it
is its own module: before saving, over every pre-written word, and again at run time over
whatever is about to be shown. Two copies of that list would be two policies.

### The ending that starts by itself, and the sweep that concludes

`conclude_what_is_over` in `devices/run_experience.py`, called by the house's ten-minute
timer before it does anything else. At thirty minutes before an afternoon's end hour the
way out of wherever it got to goes on the display; when that way out's own minutes are up,
or the end hour arrives, the ending follows and the run is deleted.

**What this replaced was demonstrably wrong.** `forget_what_is_over` unlinked a run whose
hours had passed and said nothing to anybody — measured on the house at 14:02 on 21 August
2026, on `aft_5ec79e85`, begun at 09:17 and never finished. An afternoon that stops without
ending is the failure this project exists to prevent, and it was the actual behaviour for
two days. The test asserts what went on the display and in what order, so it fails on the
old code rather than merely passing on the new.

The arithmetic of the thirty minutes: a way out is at most twenty minutes, refused above
that by the format, and the timer runs every ten. So an ending noticed as late as T-20
still has its twenty minutes and the close lands on the hour rather than after it.

### The filter on the way out

`orchestrator/outgoing.py`, beside `safety.py` and not inside it. The safety gate asks
whether a text is harmful, over a network, with a model behind it; this asks whether a text
is the kind of thing this house says, locally, with nothing to be unavailable. A refused
text is replaced by the pre-written text from the plan, which is why the written texts are
mandatory in the first place.

Refusals are counted by slot and the counts go to the journal when the run ends. Nothing is
kept: the counter holds places in a document, never afternoons or people.

### The prompt, against the real service

Eleven calls to `gpt-5.6-sol-2026-07-09` through `tools/probe_devise.py`, 23 August 2026,
from this machine rather than from the hub.

| | format 1, 21 Aug | format 2, 23 Aug |
| --- | --- | --- |
| one devise call | 29.1 s | 76.3–91.4 s |
| document that came back | ~3 100 characters | 5 955–7 408 characters |
| moments | 7 | 4–5 |

**Three defects, and all three came from the real service.** The tests with a stood-in model
were blind to every one of them, which is now the sixth time that has happened here.

1. **Every way out named the same thing, and the thing was not an object.** The first run
   put `'il bordo dello schermo'` — the edge of the screen — in all five moments. The prompt
   said "the object they are holding"; that was not concrete enough. It now says what an
   object is, that it is never part of a screen, and that two moments usually hold different
   things.
2. **The repair reworded instead of repairing.** Handed five complaints, the model returned
   `'bordo dello schermo'` — the same phrase without its article — and the fault was exactly
   where it had been. The complaint said what was wrong and never what to do. The repair
   prompt now says: change what the complaint names so it stops being true, rewording is not
   a repair, and if a way out reaches for something nothing mentions, put that object into
   an earlier moment. After that, one run came back with a single complaint and the repair
   cleared it in **35.3 s**.
3. **Two answers in seven were refused by the parser and there was no way back.** A line of
   45 characters against a limit of 44, and a fifth line on a screen that holds four. The
   limits were stated in the prompt, and restating them beside the field they apply to did
   not stop it. So `repair_unreadable` exists: the answer that would not parse goes back up
   with the parser's own refusal, which names the rule and the offending number. That is why
   the parser's messages are worded the way they are — `a line is 45 characters; at most 44`
   is already an instruction.

The ten dimensions varied on their own across the runs — a railway timetable, a coastline
made of a cup and a pencil, a domestic radio, a cartography of household sound — and none
of them was a treasure hunt, an escape room or a quiz. That is one observation over a
handful of runs, not a measurement of variety, and the thing that will actually keep it
varied is the negative constraint, which has not yet run against a house with a history.

### What is not built, and is next

1. **The durable record and the replanning of `§5` and `§6` are half done.** The run file
   holds the weight, what has been printed and whether the ending has begun, and the runner
   picks a weight by asking whether the standard one still fits. The other three moves —
   dropping optional moments, merging adjacent pairs, and the same order run backwards when
   there is more time — are not built. Neither is the pause.
2. **Nothing runs the whole thing end to end on the house yet.** Everything above was tested
   against the real model or in the suite; the afternoon that is devised, refused, repaired,
   approved and then run to an early ending on the actual printer and the actual display is
   `§19`'s "done when", and it has not happened.
3. **The parent's typed messages, the history that moves the starting weight, and the
   camera** are untouched, in that order of cost.
