# An experience, devised and run

The paper loop as it stands is: here is a task, do it, I will look at it. That is a
worksheet with extra steps, and it is not what this is for. What it should be is an
experience — thought up fresh, run across an afternoon, landing partly on a display and
partly on paper, and coming back through the glass. It has a beginning and it ends.

This file is the design. Nothing in it is built. The three decisions it turned on were
taken on 21 August 2026 and are recorded below; what is left is a contract, and then one
experience written by hand in it before a model fills it.

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
| 21 Aug 2026 | *One content-safety chokepoint before anything reaches the adolescent* (working rules §3) | Nothing yet — no experience runs, so nothing has reached anybody unscreened | Written down here because it stops being free the moment something runs one. `Continuation` is model-written text bound for a display, and it has to pass `orchestrator/safety.py` before the first afternoon, not after it |

Not smoothed, and named so that it stays that way: **a write from the panel is inert.**
Nothing in this work touched it. An experience is devised because a hub asked; a
continuation arrives inside the answer to a request the hub made. Nothing is pushed.

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

The museum, the contract, and one afternoon written by hand. Nothing runs yet: there is no
runner, no agent that devises one, and no panel route that answers an `ask`.

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

1. **A runner.** Nothing executes an `Experience`. `devices/run_blueprint.py` is the shape
   to copy and the seam is different: a blueprint had two halves, an experience has one per
   page that comes back.
2. **The short code that replaces the QR.** `§1` says identity survives as a few characters
   printed in a corner and read by the same model. The sheet still carries a QR and four
   markers, because the flatbed path uses them today and the reader's prompt is written
   around declared rectangles. Untouched on purpose: it is a change to `printing/render.py`,
   `shared/sheet.py` and the reader prompt at once.
3. **The ruler.** It dies with the cell geometry, and the cell geometry has not finished
   dying: the model reader is still handed rectangles. It goes when the reader stops being
   given them.
4. **The safety chokepoint on a continuation**, before anything runs. See the table in §2a.

