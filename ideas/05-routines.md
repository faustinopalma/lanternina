# Routines, and activities that are easy to start

A note on the frame, because it decides the shape of everything below.

The request these ideas answer was "keep the adolescent engaged". Engagement as a goal is
the thing `docs/NON-GOALS.md` refuses: no streaks, no daily goals, no reward timed to pull
somebody back, no notification because time has passed. Those are not missing features; they
are the line that makes this project what it is.

What can be done instead is narrower and, we think, more useful. Three things:

- **Lower the cost of starting.** Most of what stops a person is the first step, not the
  activity. One step visible instead of six, a sheet already printed, a card already on the
  wardrobe.
- **Keep stopping free.** Every flow can be abandoned at any point, with nothing said about
  it afterwards.
- **Vary, and vary on evidence.** Topics and formats start inside the settings the parent
  and the adolescent agreed on, and the system may move them on what came back: what was
  left blank, what took a long time, what was picked again.

What the system concludes stays a description of what happened. Where something is counted,
it is a count of steps in a routine the parent wrote, and it never turns into a measure of a
person.

---

## 1. Reminders the parent writes in their own words

**What it is.** A page in the panel where the parent writes what should be remembered, in
ordinary sentences and not in fields — "lavarsi i denti dopo cena", "mercoledì porta fuori
il bidone". The house turns those sentences into reminders with a time attached, and shows
each one on a display when its moment comes. The adolescent presses the button and it goes
away.

**Why.** The routine is the part of the day that repeats, and repeating it is the part an
adult currently does out loud. A reminder at 07:30 is not a notification: it is the
schedule the household already has, written where it can be seen without asking. Free text
rather than a form because a parent knows the routine and does not know our vocabulary for
it, and a form is a quiz about the vocabulary.

**The constraint that shapes it, and it is not negotiable.** A write from the panel is
inert: it may persist state and nothing else — no model call, no work queued, no waking the
house. That rule is what makes "the panel is unreachable" mean reduced capability rather
than a stopped house, and it is why the panel cannot reach into the home at all. So the AI
cannot read what the parent typed at the moment they type it.

What survives the rule is the whole of the idea, one step later. The parent's sentences are
stored exactly as written, marked as not yet read. The hub asks — on the timer it already
has, the way it asks for a picture — whether there is anything new, and the interpreting
happens inside the answer to *that* request. The parent sees the result the next time they
open the panel. A reminder written at 14:00 becomes active at the next request, so at most
one interval late, which is the same trade already accepted for the rhythm.

**The clarification.** A sentence the model cannot place in time — "lavare i denti", with no
hour — does not become a reminder and does not fail silently either. It comes back as a
question against that line, and the panel shows it the next time the parent looks. The
parent answers by editing their own sentence, not by filling in a field: the text they
wrote stays the only copy, so there is never a version in the database that disagrees with
what is on their screen.

**What must not be built here, and this is the part that would be easy to get wrong.**
Nothing records whether a reminder was dismissed, or when, or how often one was not. That
would be an adherence score about a person under another name, and it is refused for the
same reason grades are. A reminder that nobody presses is shown until its window closes and
is then simply not shown; nothing is kept, nothing is repeated louder, and nothing is sent
because a button was not pressed — a notification triggered by inactivity is the one shape
this project will not build.

**The wording is the model's, the reminder is the parent's.** The text on the display is
generated, so that the same reminder does not arrive in the same words for the two
hundredth time. That means it is content reaching the adolescent and passes the safety
chokepoint like everything else. It cannot be approved sentence by sentence — nobody will
approve four sentences a day — so it takes the shape already used for pictures: the parent
approves the *theme*, and not each image. Here the parent approves the reminder, and the
wording varies inside it.

**One press, two meanings.** The button on a display currently means "read the sheet on the
glass", and a press while a reminder is showing must mean "seen" instead. So the press has
to be read against what the display was showing, and dismissing a reminder must not start a
37 s scan. This is the sharpest edge in the whole idea and it belongs to
`devices/scan_sheet.py`, which today treats every press the same way.

**The third role.** A display would carry "shows reminders when they are due" alongside the
two it can hold now. The role is deliberately absent from the panel until there is something
behind it: a job a parent can hand out that does nothing is worse than a job that is not
offered.

**Where it starts.** `panel/rhythm.py` as the pattern for a setting the hub reads; a store
beside it for the parent's text and the reminders derived from it; `panel/app.py` for the
route the hub calls; `devices/pull_picture.py` for the side that decides when; `agents/`
for the reading of the sentences; `web/` for the parent's page.

**Done when.** A parent writes three sentences, one of them without a time. With the hub's
clock moved across the hours named, each of the other two appears on a display holding the
reminder role and clears on a press; the third has produced a question in the panel and no
reminder. Nothing anywhere counts presses.

**What it costs.** A week, and most of it is not the parsing. The timer fires once a minute
but a reminder is only as fine as the interval at which the hub asks, so decide the
granularity before promising it in the panel. The second cost is the one above: the press
stops having a single meaning, and that is a change to the part of the system a person
touches with their hand.

---

## 2. One step at a time

**What it is.** The second display holds the step happening now. Not the list.

**Why.** A list of six things is a request to plan; one step is a request to do. This is the
cheapest thing in this file that changes how much has to be held in mind at once.

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

**What it costs.** It must stay a position in today's routine and never be shown as a
tally about a person — no "you finished 3 of 5 yesterday" on the display, no percentage
across days in front of anybody. Keeping the figure is allowed and may well be useful to
the system; showing it as a verdict is what stays out.

**Where it starts.** `devices/epaper.py`.

**Done when.** A four-step routine shows its position on each step, and nothing about it is
shown back to the reader afterwards.

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
it, one question for the parent that no amount of code answers: which pictogram system is
already known. A different one from school would be a second language to learn rather than
a continuation.

**Where it starts.** `printing/render.py`, and a local copy of the pictogram set.

**Done when.** A routine defined once produces both the display steps and a printable sheet
of cards, offline.

---

## 5. Learning a new routine

**What it is.** One new routine at a time, with the steps written in full at first and
shortened later.

**Why.** A routine that is being learned needs more words than one that is known. Deciding
when that stops being true is exactly the sort of choice the system is now allowed to make
on its own — the words got shorter because the full form stopped being used, not because
somebody was graded.

**How.** Two forms of the same routine — full and short — with the system free to move
between them, the panel showing which form is in use and why in one sentence, and the parent
able to pin it either way. Reversible in one click is the requirement; asking permission
first is not.

**What it costs.** The switch must not be presented as an achievement, on the display or in
the panel: not "you have learned this", which is a verdict about a person, but "showing the
short form since 12 September", which is a record of what the system did. The other cost is
that an automatic change is a change nobody asked for, so it has to be visible in the panel
rather than discovered on the wall.

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
and may take account of what came back when it was. The approval ledger already records what
was approved and when.

**What it costs.** The reason a thing comes round again is the system's business and stays
there. It is not rendered as "this is coming back because you got it wrong", which is a
verdict handed to the person it is about. Also needs a rule for content the parent has
withdrawn, which must never come round again.

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
