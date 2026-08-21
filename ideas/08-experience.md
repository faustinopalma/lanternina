# An experience, devised and run

The paper loop as it stands is: here is a task, do it, I will look at it. That is a
worksheet with extra steps, and it is not what this is for. What it should be is an
experience — thought up fresh, run across an afternoon, landing partly on a display and
partly on paper, and coming back through the glass. It has a beginning and it ends.

This file is the design, and then the record of building it. The three decisions it turned
on were taken on 21 August 2026 and are recorded below; §4 is the contract and the one
afternoon written by hand in it, and §5 is the day it first ran on the house.

---

## 1. What dies, what moves, and what must not be thrown away

**What dies.** The cell geometry: a page is no longer a set of declared rectangles that a
reader is asked about one at a time. With it goes the 50 mm ruler, which existed only to
prove the print had not been scaled — and scaling mattered only because it broke the
rectangle arithmetic.

**What moves rather than dies — decided 21 August 2026.** The ArUco markers and their
detector stay in the codebase, with their tests, and come off the printed sheet. A flatbed
gives a flat image at a known scale and needs no help; a camera does not, and the capture
station of `06 §1` is where four corners in a photograph earn their keep. So the code is
not museum material, it is early: a later experience whose sheet is meant to be
photographed can carry markers again, and the machinery will be there and still tested.

**What goes to the museum.** `printing/layout.py`, the template that placed four questions
of four choices, and the arithmetic that read ink out of a rectangle. Kept readable, out of
packaging and out of the test run. They are good code and they answer a question nobody is
asking any more.

**What survives out of the sheet path, and it is one thing.** A page comes back hours
later, and the house has to know which experience it belongs to and which step. That is
identity, and it does not need a QR: a short code printed in a corner, read by the same
model that reads the rest.

**What must not be thrown away.** The ecology is not a matter of care, it is a mechanism,
and it is independent of everything above. `shared/pagedesign.py` has no mark that fills an
area — so a heavy page is unreachable rather than discouraged — and `printing/compose.py`
measures the ink in square millimetres and refuses above a budget. Both were measured
against real sheets on 20 August 2026, `03 §6`. Restarting the sheet code and keeping those
two properties is a different thing from restarting and losing them.

**Pages are read by a model, and the local tier is given up on purpose.** Decided 21 August
2026. Reading ink out of declared rectangles on the hub kept the paper path alive without
the cloud, and it bought that by making a sheet a form — the only pages it can read are
pages made of boxes. That is too much to pay. The consequence is stated once so it is never
a surprise: **no cloud, no reading.** A page that comes back while the cloud is unreachable
waits; it is not guessed at, and nothing is said to anybody about it.

---

## 2. The three decisions, taken 21 August 2026

### Who decides what happens next, and when

The house asks, and the cloud thinks inside the answer to that request — the shape
`POST /api/device/{household}/reminders` already has, where a sentence is read by a model
inside the call the hub made on its own timer. An experience is a row the hub asks about:
*this is what came back, what now*. Nothing is pushed, nothing is scheduled from outside,
and an experience nobody continues simply stops.

This one was derived rather than chosen: it falls straight out of a write from the panel
being inert. Of everything in the working rules this is the one to smooth last, and the
reason is not philosophy — it is the property that stops something outside a house reaching
into it. Smoothing it is a different kind of decision from smoothing the others and should
be taken as one.

### What the parent approves

The experience, once, **from an overview at a general level** — not step by step, and not
each thing an adolescent will see. And there is a second setting beside it: a mode with
less intervention, for a parent who has decided they do not want to be asked each time.

What that costs is said plainly rather than discovered: inside an approved experience, what
reaches the adolescent has not been seen by an adult. The content gate is then the only
thing between a model and a person, and it is doing more work than it was designed to.
This is the same trade a picture theme already makes — approve the subject, not each image
— taken further.

### Whether the thing that ends is allowed to be satisfying

Yes, and the general policy is below rather than a special case here.

---

## 2a. Rules get smoothed, and each one is written down

Decided 21 August 2026: where this work collides with a rule, the rule is smoothed rather
than the work abandoned. There is a review at the end, and steps back are taken then.

A review needs something to review, so the price of smoothing a rule is one entry here:
**which rule, what it blocked, what was done instead, and the date.** A rule bent without a
line in this table is not freedom, it is drift — the kind nobody notices until it has
already done harm, which is what the working rules say about themselves.

| Date | Rule | What it blocked | What was done instead |
| --- | --- | --- | --- |
| 21 Aug 2026 | *Cloud unavailable means reduced capability, not a stopped system* (working rules §3) | Keeping a page readable with no network required the sheet to stay a template of declared rectangles, which is the shape a sheet has stopped being | The offline reader is in `attic/`. **No cloud, no reading**: `devices/read_page.py` raises, a run stops at its `collect`, and somebody who pressed the scan button gets one sentence that claims nothing about the page. Tested in `tests/test_read_page.py` |
| 21 Aug 2026 | *The parent is the point, not a bottleneck to remove* (working rules §1) | Approving each thing an adolescent sees makes an afternoon that changes course impossible to run — every branch would need a parent awake at the moment it was taken | The parent approves the experience once, from its overview. `Experience.overview` is the field approval is given to, and `Continuation` is what arrives unapproved. Recorded rather than argued: this is a real reduction in what an adult sees, and §2 above states its cost |
| 21 Aug 2026 | *One content-safety chokepoint before anything reaches the adolescent* (working rules §3) | Nothing yet — no experience runs, so nothing has reached anybody unscreened | Written down here because it stops being free the moment something runs one. `Continuation` is model-written text bound for a display, and it has to pass `orchestrator/safety.py` before the first afternoon, not after it. **Built the same day**: `screen_continuation`, called by `panel/continuing.py`, tested in `tests/test_continuation_safety.py` and held in place by `tests/test_boundaries.py` |
| 21 Aug 2026 | *One content-safety chokepoint* (working rules §3), read strictly | The gate had one caller — the model router — and a continuation is not routed through a proposal, so the router had nothing to screen | There are now two callers of one gate: `orchestrator/router.py` and `orchestrator/safety.screen_continuation`. Still one door, two ways up to it, and the second is named in the module docstring so a third does not arrive quietly. The boundary test refuses `panel/routes/experience.py` importing an agent, which is what a way round would look like |
| 21 Aug 2026 | *Cloud unavailable means reduced capability, not a stopped system* (working rules §3) | The rest of an afternoon has no reduced version. Half a continuation is moments that lead somewhere nobody wrote | `POST /api/device/{household}/experience` refuses — 429 at the cap, 503 with no cloud, 502 for an answer that is not a continuation, 422 when the gate says no — and the house treats every one of them the same way: it stops. That is not a degradation, it is the ordinary ending of an afternoon nobody continues, which costs nothing because nothing was waiting on it |
| 21 Aug 2026 | *One content-safety chokepoint* (working rules §3), a third time | Devising a whole afternoon produces model text that reaches a parent, and the two existing callers screen a proposal and a continuation. Neither covers a document that is stored where an adult reads it | Three callers of one gate now: `orchestrator/router.py`, `screen_continuation` and `screen_experience`. `words_for_a_person` is the single function both experience callers gather words with, so a field added to one and forgotten in the other fails a test rather than reaching somebody. Held by `tests/test_boundaries.py`, which refuses `panel/devising.py` that does not name `screen_experience` |
| 21 Aug 2026 | *Nothing here runs while nobody is doing anything* (`§5` of this file, the third of the runner's decisions) | Nothing began an afternoon. `begin` took a path on a command line, so an afternoon happened because somebody typed one, and the hours of a run nobody brought a page back to were noticed by nobody at all | `devices/afternoon.py`, on a timer every ten minutes. Almost every run reads a cached rhythm off the disk and stops without touching the network. What it may do is begin an afternoon on a day and at an hour the parent chose, and delete a run whose hours have passed. It notifies nobody and it is not triggered by anybody's inactivity — the distinction that matters is between a clock that offers something and a clock that chases somebody, and only the first is here |
| 21 Aug 2026 | *An afternoon that ends leaves nothing behind, not even that it happened* (`§5`) | An approved afternoon the house had already run was still approved, so it would be handed over again the next chosen day — an approval nobody gave, every day until the parent thought to withdraw it | `OfferedExperience.begun_at`, written by the house through `POST /api/device/{h}/experiences/{id}/begun`. One timestamp beside a title that was already kept. It is not a decision and does not become one: the parent's word stays in `state`, and nothing records who did the afternoon, how far it got or whether it finished. The run in the house still deletes itself and its paper when it closes |

Not smoothed, and named so that it stays that way: **a write from the panel is inert.**
Nothing in this work touched it. An experience is devised because a hub asked; a
continuation arrives inside the answer to a request the hub made. Nothing is pushed.

The devising work of §6 tested that rule rather than bent it, and the shape it forced is
worth writing down: **a parent cannot ask for an afternoon.** The obvious feature — a
button that says "make me one" — is the exact thing the rule forbids, so what exists
instead is a house that asks on its own rhythm and a parent who decides about what came
back. That is slower and it is less satisfying to demonstrate. It is also the only version
in which nothing outside a house can put words into it.

One line is worth keeping in view while smoothing, because it is the difference between
this project and the thing it refuses to be: **an ending may be satisfying; nothing is
built whose purpose is to make the next one more likely.** A reveal at the end of an
afternoon is the first. A counter of how many afternoons in a row is the second wearing its
coat. Streaks, daily goals and notifications triggered by inactivity all exist to pull
somebody back on a day they were not going to come, and none of them is needed for an
afternoon that has a shape and finishes.

---

## 3. What an experience is made of

Sketch, not a contract. The contract is written after the three decisions above.

- **It is devised.** Not chosen from a list. Fresh each time, from what this house has —
  which displays, which paper, what was liked before — and from nothing about a person that
  is a verdict.
- **It has steps on different surfaces.** A display says something now; a sheet is left on
  the table as a physical object; a page comes back through the glass and changes what
  happens next. The surfaces are the senses this house has, and the list will grow. The
  agent should not change when it does: another surface is another tool, not another agent.
- **It is followed.** What comes back is read, and the next step is decided knowing it.
  That is the difference between an experience and a worksheet, and it is the expensive
  part.
- **It ends.** A few hours, and then it is over and says so. Nothing waits for a page that
  never comes back.

**Where it starts.** `shared/pagedesign.py` for the marks and the ink budget, which stay.
`shared/blueprint.py` for the argument about readable plans, which stays even though the
format will not. `panel/routes/reminders.py` for the shape of "the house asks and the cloud
thinks inside the answer". `agents/sheet_designer.py` for the prompt work already measured.
`printing/render.py` and `vision/` for the markers, which stay for the camera.

**Done when.** One experience is devised by a model, approved by a parent from an overview,
run across an afternoon on the two displays and the printer, followed through at least one
page coming back off the glass, and finished — with the parent able to read afterwards what
happened, and nothing kept that is a claim about anybody.

**What it costs.** The largest thing attempted here. It replaces the paper loop, changes
what approval means, and puts a model in charge of a plan rather than of a paragraph. The
mitigation is the order: the contract first, then one experience by hand in that contract
before any model fills it — the same sequence `07 §1` used, and the reason it found the
reading defect before the format was built on.

---

## 4. What was built, 21 August 2026

The museum, the contract, and one afternoon written by hand. At the time of writing this
section nothing ran: there was no runner, no agent that devises one, and no panel route
that answers an `ask`. §5 is what happened next, the same day.

### The museum

`printing/layout.py`, `tests/test_layout.py`, the arithmetic that read ink out of a
rectangle, and the two instruments that measured its thresholds are in `attic/` — out of
packaging, out of `testpaths`, still runnable with `pytest attic`. `attic/README.md` says
what replaced each and why. The ArUco markers and their detector stay in `vision/` with
their tests, for the camera of `06 §1`.

The order of `03 §6` was followed and each step left the loop working. The one that cost
something was the first: the `print_sheet` step had to carry a design before the template
could go, so the two catalogue sheets were converted by running the template one last time
and freezing what came out. Cells and headings came out **identical** on both sheets,
checked rather than assumed.

### The contract

`shared/experience.py`. Four acts — `say`, `hand_over`, `collect`, `close` — one frozen
dataclass each, and an `Experience` that is an ordered list of them. A moment that is not
a `collect` is followed by the next in the list; a `collect` is followed by whichever of
its outcomes the page turned out to be. That is the whole of the control flow.

Four decisions worth their sentence each:

- **Branching yes, computation no.** There is no expression, no variable and no counter.
  Outcomes point forward only, a backward edge is refused while the document is read, and
  a moment nobody arrives at is refused too. A parent reading it reads every branch,
  because every branch is written down.
- **A page comes back two ways: `marks` or `blank`.** Not three. "Some of them" is a count
  of somebody's marks one step from being a score, and the reader's own vocabulary has no
  honest way to produce it. Which boxes carry a mark is the richer question and it is not
  answered in the format — it is what `ask` carries upward.
- **`ask` is how the afternoon stays devised rather than precomputed.** An outcome may say
  `ask` instead of naming a moment; then the house posts what came back and receives a
  `Continuation` — more moments, same vocabulary, same checks, with an ending of its own.
  A model steers an afternoon and still cannot write a program, because data over this
  vocabulary is the only thing it can hand back.
- **The last moment closes, or collects.** An experience whose last moment is a `say` runs
  off the end of the list and trails off, and that is refused. It ends, and it says so.

There is nothing about a person anywhere in it — no name, no learner, no profile, not even
a household — and a test says so by looking at the field names.

### The afternoon written by hand

`experiences/un-pomeriggio-di-nuvole.json`. Seven moments: the display says to look out of
the window; a page comes out with the sky to draw, three boxes for how high the clouds are
and a line for one word; what comes back decides whether a second page follows or the
afternoon closes; and after the second page the rest is `ask`. A blank page closes it
kindly, from either branch.

Both pages compose on A4 without touching a marker's quiet zone, measured through
`printing/compose.py` at 150 dpi:

| | answerable places | raster coverage |
| --- | --- | --- |
| the sky as it is | 5 | 2.240% |
| the cloud that was not there | 2 | 2.033% |

Both are lighter than the form they replace, which measured 2.78% on 20 August. Neither
spends any stroke ink: a page a person wrote has no drawing on it, which is itself worth
noticing — the drawing is the part a model is better at.

### What it cost, and what it caught

- **`URLError` is an `OSError`.** Found by breaking the refusal on purpose to check the
  test could fail: removing `urllib.error.URLError` from an `except` tuple changed nothing,
  because it was already covered. The redundant clause is gone.
- **A test asserting an unreachable moment is refused was passing for the wrong reason.**
  Appending the unreachable moment at the end made the document trail off, and that error
  arrived first. The test now puts it in the middle, where only the reachability check can
  catch it.
- **Three guarantees were broken deliberately and each failed the test that claims it**:
  the backward-edge refusal, the collect-before-hand-over refusal, and the panel refusal.
  All three restored from copies taken first.

### What is not built, and is next

1. **The short code that replaces the QR.** `§1` says identity survives as a few characters
   printed in a corner and read by the same model. The sheet still carries a QR and four
   markers, because the flatbed path uses them today and the reader's prompt is written
   around declared rectangles. Untouched on purpose: it is a change to `printing/render.py`,
   `shared/sheet.py` and the reader prompt at once.
2. **The ruler.** It dies with the cell geometry, and the cell geometry has not finished
   dying: the model reader is still handed rectangles. It goes when the reader stops being
   given them.
3. **The button.** Pressing it still runs `devices/scan_sheet.py`, which knows nothing
   about afternoons: it reads the page and says what is on it. Carrying an afternoon on
   from a button press is `systemctl start lanternina-experience@carry-on` today, run by
   hand.
4. **An agent that devises one.** `agents/experience_continuer.py` writes the rest of an
   afternoon; nothing writes the beginning of one. A parent still has no overview to
   approve, because there is nothing yet that produces an `Experience` to be approved.

---

## 5. It ran, 21 August 2026

### The runner

`devices/run_experience.py`, and `devices/house.py` under it. The house-level pieces —
which display a notice lands on, and who owns the file afterwards — came out of
`devices/run_blueprint.py` unchanged, because a second runner should not import the first
one's private names in order to write a screen.

The seam is `begin` and `carry_on`, and `carry_on` may be called as many times as the
afternoon has collects. `begin` plays forward to the first `collect` and writes down two
things: the run, holding the whole experience rather than its id, and one note per printed
sheet saying which afternoon that paper belongs to. `carry_on` reads the page on the glass,
finds the afternoon from the paper, and plays the stretch that follows.

Four decisions, each the answer to something that could have gone the other way:

- **An afternoon that ends leaves nothing**, not even that it happened. The run file and
  the notes on its paper are deleted when a `close` is reached. A page that arrives after
  that is told the afternoon is over, and the note deletes itself.
- **A page nobody could read is neither `marks` nor `blank`.** The two words describe ink,
  and a page of cells the reader was unsure about has no ink it can vouch for. Reading it
  as `blank` would close an afternoon on a page that was filled in — `blank` is usually the
  branch that ends things kindly — so the run stops where it is instead, which is what it
  already does when the panel is unreachable.
- **The hours are noticed when a page arrives**, not by a timer. Nothing here runs while
  nobody is doing anything, so an afternoon that ran out of hours finds out when somebody
  comes back to it, and then it is over whatever moment it had reached.
- **A continuation is a self-contained segment.** Its branches name its own moments, so an
  id it shares with the approved document is a coincidence and not a jump backwards.

### What ran on the house

The hub was updated in the order this file gave — `deploy/lanternina-scan.service` first,
then the code — and `printing/layout.py` was removed from `/opt/lanternina`. A new unit
runs the afternoon: `deploy/lanternina-experience@.service`, instanced on `begin` or
`carry-on`.

Then, at 09:17 on 21 August 2026: **`Un pomeriggio di nuvole: aft_5ec79e85`**. The notice
went to `screen-CF7D04.bmp` — one of the two displays holding the sheet job, picked at
random as designed — `sh_04a8adc9` went to the CUPS queue as job `Lanternina-8`, and the
run stopped waiting at `come-e-tornato` with a note on disk pointing that sheet at that
afternoon. Whether paper physically came out of the Epson is the one thing here that
nobody checked from this keyboard.

`carry-on` was then started against whatever was on the glass, which turned out to be a
sheet left there from an earlier day. It scanned, rectified, read the QR, recalled the
spec, and refused: *sheet sh_48a85f58 does not belong to an afternoon this house started*.
That is the whole scanner half of the runner exercised on the real machine, and it took
**29 s** wall clock from `systemctl start` to the refusal — measured from the journal
timestamps, 09:22:52 to 09:23:21, at 300 dpi over A4. What is left untested on hardware is
the part after the refusal: the panel reading the page, the two words, and the branch.

### What it cost, and what it caught

- **A unit, not a shell.** An interactive `fausto` is not in the group `lanternina`, and
  `sudo -n` on this hub grants root but not another user. Running by hand therefore could
  not read `jobs.json` — and the failure was silent in the worst way: `load_jobs` came back
  empty, no display was found holding the sheet job, and the notice was quietly addressed
  to the shared screen file instead. The fallback that keeps a house working without the
  panel also hides a permission error. Nothing was changed about that; it is written here.
- **A new screen file cannot be given to root.** `devices/house.replace` took the
  directory's user for a file that did not exist yet. The state directory is
  `root:lanternina`, so a process that is not root was asking Linux to give a file away,
  and the answer is `Operation not permitted`. The first real run died at its first moment
  with a display that had never been written. It now takes the directory's **group** and
  not its user, and a chown it is not allowed to make no longer costs the screen: no screen
  at all is a display showing yesterday. Two tests, one of which was made to fail by
  putting the defect back.
- **`replace` leaves its `.tmp` behind when it fails.** `screen-FB9F18.bmp.tmp` sat in the
  state directory from the failed run and was removed by hand. Not fixed, because the next
  write overwrites it and it is one file; written down because a stray temp file beside a
  display's own screen is the sort of thing somebody later reads as content.
- **Three guarantees of the runner were broken deliberately and each failed its test**: a
  `close` ending the afternoon, the unsure-page refusal, and the check that a continuation
  belongs to this afternoon. Two more on the panel side: the gate being called at all, and
  the refusal to buy a continuation for a branch that already says what happens.

### The chokepoint, and the route

`orchestrator/safety.screen_continuation` gathers every word an adolescent will read out of
a continuation — headings, lines, a page's title and instructions, the words printed on it
and the label beside every box — and hands them to the gate as one thing. One refusal
covers the whole continuation, because half an afternoon is not something to put on a
display. A continuation with nothing to read is refused rather than screened, since an
empty body passes any screener trivially and that is the one way an unscreened afternoon
could get through the function whose job is to stop it.

`POST /api/device/{household}/experience` is the route, and it is shaped like the reminders
one on purpose: the house asks, and the model thinks inside the answer. Before anything is
paid for, the route parses the experience and checks that the moment named really is a
`collect` whose outcome for that page says `ask` — a house asking about a branch somebody
already wrote would otherwise buy a step that exists. The document that reaches the model
is the one that came out of the parse, so a heading that arrived with a control character
in it reaches the prompt without one.

What the model is given is the experience, which carries nothing about a person, and the
page in the reader's own three words. What it may answer is `{"moments": [...]}` and
nothing else: which afternoon this is and which branch it follows are known already, and a
model made to echo two ids can only get them wrong.

**The panel in the cloud is still the old image.** `ca-lanternina-dev-api` runs revision
`--0000041`, which has no `/api/device/{household}/experience`. So an afternoon can be
begun, a page can be read, and a branch that names a moment can be taken — but an outcome
that says `ask` will get "the panel refused to go on: 404" until the container is rebuilt
and deployed.

### The rest of the afternoon, and the container that was in the way

Written the same day, after the above. The image was rebuilt from the commit the hub was
already running — `lanternina/panel:793c52b`, 51.7 s of server-side build measured from
the run's own start and finish times, 72.8 s of client wall clock — and
`az containerapp update` produced revision `--0000042`. The route appeared in the public
`/openapi.json` within about 50 s of the update, which is the cheapest proof that traffic
moved without holding a credential.

Then it was called from the hub rather than from a laptop, with an invented reading in
place of a page: **HTTP 200 in 14.6 s**, and five moments came back — a display saying the
name that had been written on the page, a third sheet asking where that cloud's tail went,
a collect, and two closes. The model had picked up the invented name and built the rest
around it, which is the behaviour the format exists to allow and the first time it was seen
against the real service.

Meanwhile the afternoon on the house went on. The first page came back with a mark, the
run took the `marks` branch, printed `Lanternina-9` and stopped at `l-ultimo-foglio`: the
whole scanner half, the model reading a page, the two words and the branch, all on the real
machine. What is still untested on hardware is the step after that — the branch that says
`ask` reaching the route that now exists.

---

## 6. Devising one, 21 August 2026

`agents/experience_continuer.py` wrote the rest of an afternoon and nothing wrote the
beginning of one, so a parent had no overview to approve because nothing produced an
`Experience` to be approved. That is what this closes.

### What was built

- **`agents/experience_deviser.py`** writes a whole afternoon from what a house has, the
  household's language, and what the parent already wrote in the panel as interests and as
  things to avoid. It is the twin of the continuer, deliberately: same format described in
  the prompt, same manner, same refusal to salvage half an answer.
- **`orchestrator/safety.screen_experience`**, beside `screen_continuation`, over one
  shared `words_for_a_person`.
- **`panel/experiences.py`** and `CosmosExperienceStore`: afternoons a house has been
  offered, and the parent's decision on each.
- **`panel/devising.py`**, the twin of `panel/continuing.py`: the model call and the gate,
  in the container that holds the identity.
- **Four routes**, in `panel/routes/experience.py` beside the continuing one.
  `POST /api/device/{h}/experiences` devises one and leaves it pending;
  `GET /api/device/{h}/experiences` hands back the approved ones;
  `GET /api/experiences` and `POST /api/experiences/{id}/decision` are the parent's, and
  the second records a decision and does nothing else.

### Four decisions worth their sentence

- **Three fields are filled in rather than asked for**: the id, the format version, and
  which capabilities the afternoon needs. The last is the one worth stating — the moments
  already say what a house must be able to do and `NEEDS` maps each act to its capability,
  so a model made to restate that can only get it wrong for free. The field stays on the
  document because an afternoon written by hand still declares it and is checked against
  it.
- **A devised afternoon is not a `ProposalRecord`**, and the reason is one field. A
  proposal carries a safety seal minted on the device with a key the cloud does not have,
  and the home server verifies it after pulling. An experience is devised in the cloud, so
  the only seal this container could mint is one nobody can check — and a record with an
  unverifiable seal in it is worse than a record with no seal field. It is its own small
  store, and the house trusts the gate that ran in the panel over TLS with a device key,
  which is the same trust that reading a page and continuing an afternoon already run on.
- **What is remembered about earlier afternoons is their titles**, handed to the model so
  the next one differs. Not who did them, not how far anybody got, not what came back —
  and a test names the exact set of arguments so a fifth one cannot arrive quietly.
- **The parent sees the overview and may read every branch.** Approval is given to the
  overview, which `§2` settled; the whole document goes to the panel as well, because an
  overview that is the only thing shown is a claim about a document nobody can check.

### What it cost, and what it caught

- **`app.routes` no longer lists what is registered.** This FastAPI keeps included routers
  lazily, so a check that read `app.routes` reported three paths on an application with
  thirty-nine and looked exactly like routes failing to register. The honest reading is
  `app.openapi()["paths"]`, which is also what the deployed panel is checked with.
- **A test that named forbidden words was checking the wrong text.** Asserting that
  "score" is absent from the prompt failed on the prompt's own instruction not to produce
  one, and asserting "age" is absent failed on the word "page". What replaced it is a test
  of the input: the agent is handed a context carrying a learner id and hints, and neither
  reaches the prompt. That is a guarantee something could break; the word list was not.
- **Three guarantees were broken deliberately and each failed its test**: the gate being
  called before an afternoon is stored, the capabilities being derived from the moments
  rather than declared, and an afternoon being withheld from the house until it is
  approved. All three restored from copies taken first, and the test count checked to have
  risen by exactly the twenty-five that were added — 495 to 520.

### Three defects the real service found, and the tests were not going to

Deployed and called from the hub, three times, each refusal a different one. None of them
was reachable by a test with the model stood in for, which is the point of running it.

- **A limit the format enforces and the prompt never mentions is a refusal the model had
  no way to avoid.** The first afternoon came back with page instructions of 189
  characters, refused at 160, and 160 appeared nowhere in the prompt. Both agents write
  pages and both had the same gap. What replaced it is a test that walks the limits and
  asserts each number appears in both prompts, checked by removing one and watching it
  fail.
- **The id rule was stated as `<a-z0-9- , 2 to 32 chars>`**, which the model read as
  permission for something else. Now it is a sentence: no capitals, no accented letters,
  no underscores, no spaces, and written in English even when the afternoon is not, because
  nobody reads them. The refusal also names the offending value now — "a moment id is
  wrong" in a document with nine of them costs the reader the work of finding which.
- **The prompt said "Write it in it."** The household stores a language *code*, and the
  code went into an English sentence where "it" is a pronoun. The afternoon came back in
  English for a house set to Italian, which is not a refusal at all: it succeeded and was
  wrong. `LANGUAGE_NAMES` sits beside `LANGUAGE_CHOICES` now, and a test walks every choice
  and asserts the name reaches the model and the code does not — so the next language added
  cannot repeat it.

Then it worked. **HTTP 200 in 29.1 s**, from the hub, with the equipment the house reports
about itself: *Sei passaggi di una trasformazione* — an object in the room, six frames of a
slow change on one sheet, words optional, blank allowed, and two closes that both end the
afternoon without asking for an explanation. Stored pending. Nothing about a person in it,
nothing counted, and no path that does not end.

One thing neither devised afternoon did: use `ask`. The format allows a branch to be left
unwritten and the prompt does not press for one, so a model that can see the whole
afternoon writes the whole afternoon. That is not wrong — but the branch that makes an
experience devised rather than precomputed is the one the deviser does not reach for, and
whether to ask for it is a decision rather than a fix.

### What is not built, and is next

1. **The parent has no page.** The two routes exist and are tested; there is nothing in
   `web/` that lists an offered afternoon or records a decision on it. Until there is, a
   parent approves an afternoon with an HTTP request, which is not approval by anybody who
   has not been told about this file.
2. **The hub cannot begin an approved one.** `devices/run_experience.begin` takes a file.
   Nothing yet pulls `GET /api/device/{h}/experiences` and starts what came back, and
   nothing asks for one to be devised in the first place — the rhythm on which a house asks
   is not written.
3. **Nothing is learnt from an afternoon that happened.** The working rules say the system
   may move on what it observes, and this devises from settings and titles only. What an
   afternoon left behind is deleted when it closes, on purpose (`§5`), so the thing to
   decide first is what may survive an ending — and that decision is the one where a record
   of what happened turns into a verdict about a person if it is taken carelessly.

---

## 7. The parent's page, the house's clock, and the branch nobody used, 21 August 2026

The loop was open at both ends. An afternoon was devised and left pending, and there was
nothing that a parent could decide with and nothing that would begin what they decided.
This closes both, and takes the decision `§6` left open.

### The parent's page

`web/src/sections/Experiences.tsx`. Title, overview and length; a control that opens every
step, including the branches; approve, refuse, and withdraw afterwards. Approving calls
`POST /api/experiences/{id}/decision` and that is the whole effect — one row changes state,
and the house finds it when it next looks.

There is no button that asks for an afternoon. That is the rule of `§2a` showing through
into a screen rather than staying in a file: the obvious feature is the exact thing an
inert panel forbids, and `tests/experiences.test.tsx` fails if a control whose name reads
like one appears. What replaces it is `experiences.laterNote`, which says plainly that the
house asks and the parent decides about what came back.

Everything a model wrote is rendered as text. A page's marks are shown as the words beside
them — the label of each box, line and drawing area, and anything printed on the sheet —
and not as rectangles: where a mark sits on paper means nothing to somebody who is not
holding it.

### The house's clock

`devices/afternoon.py`, on `deploy/lanternina-afternoon.timer`, every ten minutes. The
rhythm gained two settings, in `panel/rhythm.py` beside the three it had: which days an
afternoon may begin on, and from what hour. **The default is no day at all**, so a house
that has never been told begins none — the feature arrives switched off rather than
arriving.

Four decisions, each the answer to something that could have gone the other way.

- **There is no end-hour setting, and there will not be one.** An afternoon may begin only
  if the whole of its own `minutes` is over before the pause the parent already chose. The
  second setting would have been a second copy of the first, out of step with it within a
  week.
- **One look a day, and the record of it is a date.** The stamp beside the runs holds
  `2026-08-19` and nothing else. It stops two things: a second afternoon on the same day,
  and a devise request every ten minutes at a panel answering 503 — measured worst case
  without it, 42 calls between three o'clock and the pause. It is not a tally, there is
  nothing for a tally to be about, and no setting says how many afternoons there should be.
- **The house asks for one only when nothing is approved and nothing is with the parent.**
  So the answer to `GET /api/device/{h}/experiences` carries `waiting`, a count of
  undecided rows. That is the depth of somebody's inbox and says nothing about anybody's
  afternoon. The consequence is a lag of one cycle: an afternoon asked for on a Wednesday
  is read by a parent afterwards and can happen the following Wednesday at the earliest.
  That lag is the approval, working.
- **The device route no longer takes a state.** It used to, defaulting to approved, and a
  house could therefore pull a pending document and run it — leaving the one decision this
  whole feature rests on held up by the hub's own code rather than by the panel.

What it cost is one thing the runner did not do. A run nobody ever brought a page back to
sat on disk for good, because `§5` decided the hours are noticed when a page arrives and
that is the only moment the runner is awake. Now there is a moment when something else is
awake, so `forget_what_is_over` deletes such a run and the notes on its paper. Nothing is
said to anybody: an afternoon that ran out of hours is over, which is what an afternoon
nobody continued was always going to be.

### `ask`, and what it is worth

`§6` ended on the observation that neither devised afternoon used `ask` — the format allows
a branch to be left unwritten, the prompt listed the syntax and never said when it was the
right thing, and a model that can see the whole afternoon writes the whole afternoon. The
decision taken here is to press for it, once, and on one branch.

**Once, on the outcome for a page that came back with marks.** A blank page carries nothing
to write from, so continuing from one buys a paragraph out of no information; and one
continuation per afternoon bounds the wait, which was measured at 14.6 s from the hub on 21
August 2026 with somebody standing at the scanner.

The price, stated rather than discovered. A branch that says `ask` costs one more model
call, about fifteen seconds of waiting, and one more chance of a refusal at a moment when
somebody has just done the thing. The last of those is narrower than it first looks: the
page was read by the same cloud a moment earlier, so an afternoon that got as far as taking
a branch has already found the cloud there. And it widens the gap `§2` records — the parent
approved a branch that says "the rest is written at that moment", which is a hole they read
and agreed to, with the gate the only thing inside it.

### What ran on the house

The panel was rebuilt from this commit — 46 s of server-side build in ACR — and
`az containerapp update` produced revision `--0000047`. The new route appeared in the
public `/openapi.json` within 15 s of the update, which is the cheapest proof that traffic
moved without holding a credential.

The hub was updated, and `deploy/lanternina-afternoon.timer` enabled. Enabling it started
nothing, which is the default paying for itself: the household's rhythm document predates
the two settings, so it has no day, and the unit reads that and stops. The first run did do
one thing, at 14:02 on 21 August 2026 — it found `aft_5ec79e85`, the afternoon begun at
09:17 and never finished, saw its hours had passed, and forgot it. That is the sweep, on
the real machine, on a run that was left over rather than one built for it.

Then the house asked the deployed panel what it may run, from the hub with its own device
key: **the rhythm in 0.16 s**, `afternoonDays: []`; **the afternoons in 0.33 s**,
`waiting=2` and nothing runnable. Both correct — two afternoons are with the parent and
none is approved — and both are the numbers the clock decides on.

The browser tier followed, published by `.github/workflows/panel.yml` on the push: **84 s**
from the push to the site serving `main-Bv5qiJ6g.js`, which is byte for byte the bundle the
local build produced, since Vite names a bundle after its own content.

### What is not built, and is next

1. **Nothing is learnt from an afternoon that happened**, which is `§6`'s last item and is
   untouched. `begun_at` is now kept, which is the first thing that survives an ending; the
   question of what else may is the one where a record of what happened turns into a verdict
   about a person if it is taken carelessly.
2. **A parent cannot see an afternoon that is running.** The panel shows offered, approved
   and begun; where a run has got to lives only on the hub, and there is no route in that
   direction on purpose. Whether there should be is a decision, not an omission.
3. **The clock has not begun an afternoon on the house.** It cannot until a parent picks a
   day in the panel, and picking one is the first thing the page of this section exists for.
   Everything below `§7` is otherwise tested with the panel stood in for.
4. **No devised afternoon has used `ask` yet.** The prompt asks for one as of this commit,
   and both afternoons in the store predate it. Whether the model takes the branch is the
   next thing the real service is asked.





