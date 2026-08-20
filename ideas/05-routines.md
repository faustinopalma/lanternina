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

**What is built, on 19 August 2026.** Both halves of the panel's side. `panel/reminders.py`
holds the sentences with a mark saying whether the house has read them and what it made of
each one; `GET/POST /api/reminders`, `POST /api/reminders/{id}` and `/remove` are the
parent's half. `POST /api/device/{household}/reminders` is the house's: the hub calls it on
its own timer, and every sentence nobody has read yet is placed in the day **inside the
answer to that call** — `agents/reminder_reader.py` through `panel/reading.py`, which is the
same door the sheet reader uses. What comes back is the reminders that have an hour, with
the days they apply to; the house owns the clock and decides when a moment has come.

Three things that follow from the rule rather than from taste. A sentence is read once: the
second call has nothing to send, so the hub asking every five minutes does not pay for the
same sentence twelve times an hour. A sentence the model cannot place gets a question
instead, shown against that line in the panel, and answering it is an edit to the parent's
own words — which clears the reading, because what the house made of the old wording was
made of words that are no longer there. And a cloud that will not answer leaves the
reminders already placed in the hub's hands and says `degraded`: reduced capability, not a
stopped house.

What a model says about time is checked rather than believed. An hour that is not an hour
is dropped, a day that is not a day is dropped, and a question is one line long — the
sentences are a parent's free text and reach the model as material, so an instruction
written inside one must not be able to write into the household's schedule.

**What is built, on 20 August 2026.** The third role and the press that means "seen", which
had to arrive together: a job a parent can hand out and that does nothing is worse than a
job that is not offered. `remind` is a third job a display can hold, written once in
`shared/capabilities.py` and read from there by the panel, the hub and the parent's page.
`devices/show_reminders.py` runs on the hub once a minute, asks the panel when its local
copy of the reminders is more than five minutes old, decides whether this minute falls
inside a reminder's half hour, and writes the screen into a file of its own beside the
display's picture. `devices/trmnl_byos.py` shows that file above whatever the display was
holding, so taking it away is the whole of putting the display back — nobody keeps a copy
of the picture underneath.

Two measured numbers behind those choices. The window is 30 minutes, which is a decision
and not a measurement: long enough that somebody walking past a few minutes later still
sees it, short enough that it does not become the wallpaper. The five minutes is the
spacing the status push already makes, so this adds no new order of magnitude to how often
the cloud is woken; what it costs is that a sentence written just now becomes a reminder up
to five minutes later.

**Where the second meaning of the press ended up, and why not where this file said.** It is
in `devices/trmnl_byos.py`, not in `devices/scan_sheet.py`. The display server is the only
side that knows what a display is showing at the instant the button is pressed, and it
answers in the request the press caused. Deciding in `scan_sheet.py` would have meant the
press was written down, the scan unit started, and the waiting screen already up before
anything could say the press meant something else — a scan refused after the display had
told somebody it was reading. So the server records a press only when the press means "read
the sheet", and `scan_sheet.py` is unchanged: it still acts on every press it is given,
because it is now only given the ones that mean that.

Nothing counts. The hub keeps one line per display saying which showing it last drew there,
which is what a thing that draws needs in order not to draw twice, and it is cleared when
the window closes. A reminder taken down by a press and one still standing leave the same
bytes in that file — `tests/test_show_reminders.py` asserts exactly that, byte for byte,
so there is nowhere an adherence score could accumulate even by accident.

Still missing: the wording being generated rather than the parent's own sentence shown as
written. Today the display shows the hour and the sentence exactly as it was typed, which
is the parent speaking to their own child and needs no screening; the day the words are a
model's, they pass the safety chokepoint before they reach the renderer.

**Distributed and measured, 20 August 2026.** Image `lanternina/panel:b3d28a8` on revision
`--0000037`, and the served `/openapi.json` carries a string only the new build has, which
is how the revision was shown to be the one answering rather than assumed. The page went
out on the workflow after that, and the chunk it serves carries both new words. On the hub,
seven files were behind — the comparison is `build/hub_stale.ps1`, which hashes what git
stores rather than the working copy, because this machine checks out CRLF and the hub holds
LF — and all seven now match byte for byte, with `lanternina-reminders.timer` enabled.

Three sentences a parent had written were read by the panel with `degraded: false`:
"lavarsi i denti dopo pranzo (circa alle 13:30)" placed at 13:30, "dopo cena, circa alle
20:00" at 20:00, and "di mattina prima di uscire alle 7:00 …" at 07:00, all days. The hub's
render path was proved in `/tmp` against a synthetic house: 48.062 bytes, 800x480, one bit,
and the reserved palette byte at 0 — the byte the firmware silently refuses a file over.

What is not done is not code: no display holds the reminder job yet, so the timer runs each
minute and says "no display shows reminders: nothing to do". And the cache shows FB9F18,
the one called "un bel quadro che cambia", still holding `sheet` and not `picture`.

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
