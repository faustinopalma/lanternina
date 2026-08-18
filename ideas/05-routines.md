# Routines, and activities that are easy to start

A note on the frame, because it decides the shape of everything below.

The request these ideas answer was "keep her engaged". Engagement as a goal is the thing
`docs/NON-GOALS.md` refuses: no streaks, no daily goals, no reward timed to pull her back,
no notification because time has passed, no metric of attention anywhere. Those are not
missing features; they are the line that makes this project what it is.

What can be done instead is narrower and, we think, more useful. Three things:

- **Lower the cost of starting.** Most of what stops a person is the first step, not the
  activity. One step visible instead of six, a sheet already printed, a card already on the
  wardrobe.
- **Keep stopping free.** Every flow can be abandoned at any point, with nothing said about
  it afterwards.
- **Vary within what was chosen.** Topics and formats rotate inside settings the parent and
  she agreed on. Never in response to how she performed, how long she took, or what she
  left blank.

Nothing below observes her. Where something is counted, it is a count of steps in a routine
the parent wrote, not a measure of her.

---

## 1. Reminders at times the parent chose

**What it is.** The steps of the day appear on the display at hours the parent sets, the
same way the picture rhythm now works.

**Why.** The routine is the part of the day that repeats, and repeating it is the part an
adult currently does out loud. A reminder at 07:30 is not a notification: it is the
schedule the household already has, written where she can see it without asking.

**How.** The proposal kind exists — `routine_prompt` — and so does the shape to copy: a
setting written from the panel, read by the hub on its next run, with the hub deciding.
What is missing is a place to put the times and their steps, and a rule for what the
display shows when no step is due.

**What it costs.** The timer fires once an hour, so a reminder cannot be finer than that
without a faster timer, and a faster timer costs battery. Decide the granularity before
promising it in the panel. The other cost is a product one: a step that appears and stays
there after it is done is worse than nothing, so it needs a way to move on that does not
require her to confirm anything.

**Where it starts.** `panel/rhythm.py` as the pattern, a store beside it for the steps,
`devices/pull_picture.py` for the side that decides, `web/` for the parent's screen.

**Done when.** With the hub's clock moved forward across a set time, the step for that hour
is on the display, and outside those hours the display holds what it held before.

---

## 2. One step at a time

**What it is.** The second display holds the step happening now. Not the list.

**Why.** A list of six things is a request to plan; one step is a request to do. This is the
cheapest thing in this file that changes what she is asked to hold in her head.

**How.** The hub decides what each display is served, so the choice needs somewhere to
live: a `role` field on the device record. It does not exist yet — `panel/devices.py` holds
id, name, charge, signal and firmware, and nothing about what a display is for. The
renderer already draws text on e-paper.

**What it costs.** The second display is not connected yet, so today this is design against
nothing. Adding the field costs one line and is worth it; building the rest before the
hardware is in the house is not.

**Where it starts.** `panel/devices.py` for the role, `devices/trmnl_byos.py` for the
choice of what each display is served.

**Done when.** Two registered displays, given different roles, are served different images
from the same hub.

---

## 3. A routine that shows how much is left

**What it is.** The step also says where it sits: the second of four.

**Why.** Knowing when a thing ends is often what makes it possible to begin. It is also the
honest thing to show, because the parent wrote the routine and its length is a fact about
the routine.

**How.** The renderer already draws a title and a body; this is one more line, and the
number comes from the routine's own length.

**What it costs.** It must stay a count of steps and never become a count of her — no
percentage complete across days, no "you finished 3 of 5 yesterday", nothing that
accumulates. The moment it accumulates it is a progress trend, which is assessment with a
nicer name. The test that protects this is that nothing about it is stored after the day
ends.

**Where it starts.** `devices/epaper.py`.

**Done when.** A four-step routine shows its position on each step, and nothing about it
survives the day.

---

## 4. The same routine on paper and on screen

**What it is.** What the display shows can also be printed as cards: one pictogram, one
word, cut out and stuck where the step happens.

**Why.** A card goes on the wardrobe, in the bathroom, on the school bag — where the step
is, rather than where the screen is. It also keeps working when the network does not, which
is the case the whole system is meant to survive.

**How.** ARASAAC has a public API with Italian and turns a sentence into pictograms without
calling any model; the set can be kept locally. The printing path exists.

**What it costs.** The licence is CC BY-NC-SA: attribution required, non-commercial only,
and that belongs in the README when the first pictogram is used, not later. Before any of
it, one question for the parent that no amount of code answers: which pictogram system she
already knows. A different one from school would be a second language to learn rather than
a continuation.

**Where it starts.** `printing/render.py`, and a local copy of the pictogram set.

**Done when.** A routine defined once produces both the display steps and a printable sheet
of cards, offline.

---

## 5. Learning a new routine

**What it is.** One new routine at a time, with the steps written in full at first and
shortened later — when the parent decides, not when the system concludes.

**Why.** A routine that is being learned needs more words than one that is known, and the
transition is a judgement about a person. That judgement belongs to somebody who knows her.
The system's job is to make the change one setting away, and to make it reversible.

**How.** Two forms of the same routine — full and short — and a switch in the panel per
routine. No automatic promotion, no threshold, no counter that trips.

**What it costs.** The temptation is exactly here: a rule like "after ten times, shorten"
looks harmless and is the adaptive model we ruled out, built one condition at a time. It
has to be refused in the code and said plainly in the panel, so the next person to read it
knows the omission was deliberate.

**Where it starts.** Wherever routines end up living (see item 1), plus one control in the
panel.

**Done when.** Switching a routine to its short form changes the display on the next run,
and switching back restores it.

---

## 6. Offering approved content again, later

**What it is.** A sheet or an exercise already approved comes round again after some days.

**Why.** Coming back to something after a gap is useful, and it costs no generation. It also
uses the reserve of approved content the system already holds, which is the thing that keeps
working when the cloud does not.

**How.** Spacing is applied to the **content** — this item was last offered nine days ago —
and never to her. No estimate of what she remembers, no difficulty adjusted by result. The
approval ledger already records what was approved and when.

**What it costs.** The distinction above is the whole design, and it is easy to lose: a
"review because she got it wrong" is a model of her ability, and this is not that. Also
needs a rule for content the parent has withdrawn, which must never come round again.

**Where it starts.** `shared/approval.py` for what is valid, `tools/home_server.py` for what
gets offered.

**Done when.** With the cloud unreachable, the system still offers something to do, and a
withdrawn item is never among it.

---

## 7. Reading aloud

**What it is.** Text on paper or on the display can be heard instead of read.

**Why.** Reading slowly is a reason to be handed less text, not a reason to be handed the
same text louder. Speech makes the same approved content usable without changing it, and
`docs/NON-GOALS.md` leaves it deliberately open rather than ruled out.

**How.** Text to speech on already-screened content only, started by a physical action —
a button — and never on its own.

**What it costs.** The thing to be careful about is not the speaker but its neighbour: a
microphone is a different decision, and it is not part of this system. If one is ever added,
"the system does not listen unless asked" has to become a guarantee with a test behind it,
not a sentence in a file. Adding audio out does not add audio in, and the two should not
arrive in the same change.

**Where it starts.** The hub, on already-approved content; the cloud only if the voice
cannot be produced locally, and then with the same rule about what may leave the house.

**Done when.** A button plays an approved text, and nothing is recorded.
