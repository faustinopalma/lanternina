# An experience, devised and run

The paper loop as it stands is: here is a task, do it, I will look at it. That is a worksheet with extra steps, and it is not what this is for. What it should be is an experience — thought up fresh, run across an afternoon, landing partly on a display and partly on paper, and coming back through the glass. It has a beginning and it ends.

This file is the design, and then the record of building it. The three decisions it turned on were taken on 21 August 2026 and are recorded below; §4 is the contract and the one afternoon written by hand in it, and §5 is the day it first ran on the house.

---

## 1. What dies, what moves, and what must not be thrown away

**What dies.** The cell geometry: a page is no longer a set of declared rectangles that a reader is asked about one at a time. With it goes the 50 mm ruler, which existed only to prove the print had not been scaled — and scaling mattered only because it broke the rectangle arithmetic.

**What moves rather than dies — decided 21 August 2026.** The ArUco markers and their detector stay in the codebase, with their tests, and come off the printed sheet. A flatbed gives a flat image at a known scale and needs no help; a camera does not, and the capture station of `06 §1` is where four corners in a photograph earn their keep. So the code is not museum material, it is early: a later experience whose sheet is meant to be photographed can carry markers again, and the machinery will be there and still tested.

**What goes to the museum.** `printing/layout.py`, the template that placed four questions of four choices, and the arithmetic that read ink out of a rectangle. Kept readable, out of packaging and out of the test run. They are good code and they answer a question nobody is asking any more.

**What survives out of the sheet path, and it is one thing.** A page comes back hours later, and the house has to know which experience it belongs to and which step. That is identity, and it does not need a QR: a short code printed in a corner, read by the same model that reads the rest.

**What must not be thrown away.** The ecology is not a matter of care, it is a mechanism, and it is independent of everything above. `shared/pagedesign.py` has no mark that fills an area — so a heavy page is unreachable rather than discouraged — and `printing/compose.py` measures the ink in square millimetres and refuses above a budget. Both were measured against real sheets on 20 August 2026, `03 §6`. Restarting the sheet code and keeping those two properties is a different thing from restarting and losing them.

**Pages are read by a model, and the local tier is given up on purpose.** Decided 21 August
2026. Reading ink out of declared rectangles on the hub kept the paper path alive without the cloud, and it bought that by making a sheet a form — the only pages it can read are pages made of boxes. That is too much to pay. The consequence is stated once so it is never a surprise: **no cloud, no reading.** A page that comes back while the cloud is unreachable waits; it is not guessed at, and nothing is said to anybody about it.

---

## 2. The three decisions, taken 21 August 2026

### Who decides what happens next, and when

The house asks, and the cloud thinks inside the answer to that request — the shape `POST /api/device/{household}/reminders` already has, where a sentence is read by a model inside the call the hub made on its own timer. An experience is a row the hub asks about: *this is what came back, what now*. Nothing is pushed, nothing is scheduled from outside, and an experience nobody continues simply stops.

This one was derived rather than chosen: it falls straight out of a write from the panel being inert. Of everything in the working rules this is the one to smooth last, and the reason is not philosophy — it is the property that stops something outside a house reaching into it. Smoothing it is a different kind of decision from smoothing the others and should be taken as one.

### What the parent approves

The experience, once, **from an overview at a general level** — not step by step, and not each thing an adolescent will see. And there is a second setting beside it: a mode with less intervention, for a parent who has decided they do not want to be asked each time.

What that costs is said plainly rather than discovered: inside an approved experience, what reaches the adolescent has not been seen by an adult. The content gate is then the only thing between a model and a person, and it is doing more work than it was designed to. This is the same trade a picture theme already makes — approve the subject, not each image — taken further.

**What it looks like, since 25 August 2026.** The card carries the title, the overview, and one line counted off the document: how long, how many sheets it will print, whether it wants the scanner. That line was added because the three fields above it say nothing about what will happen in the room, and "two sheets and the scanner" is what a parent decides on. The steps are behind a button labelled *if you want to see how it is built* — being able to look and being expected to read are different things, and only the first is designed for. Nothing in the panel may assume the second.

### Whether the thing that ends is allowed to be satisfying

Yes, and the general policy is below rather than a special case here.

---

## 2a. Rules get smoothed, and each one is written down

Decided 21 August 2026: where this work collides with a rule, the rule is smoothed rather than the work abandoned. There is a review at the end, and steps back are taken then.

A review needs something to review, so the price of smoothing a rule is one entry here: **which rule, what it blocked, what was done instead, and the date.** A rule bent without a line in this table is not freedom, it is drift — the kind nobody notices until it has already done harm, which is what the working rules say about themselves.

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

Not smoothed, and named so that it stays that way: **a write from the panel is inert.** Nothing in this work touched it. An experience is devised because a hub asked; a continuation arrives inside the answer to a request the hub made. Nothing is pushed.

The devising work of §6 tested that rule rather than bent it, and the shape it forced is worth writing down: **a parent cannot ask for an afternoon.** The obvious feature — a button that says "make me one" — is the exact thing the rule forbids, so what exists instead is a house that asks on its own rhythm and a parent who decides about what came back. That is slower and it is less satisfying to demonstrate. It is also the only version in which nothing outside a house can put words into it.

One line is worth keeping in view while smoothing, because it is the difference between this project and the thing it refuses to be: **an ending may be satisfying; nothing is built whose purpose is to make the next one more likely.** A reveal at the end of an afternoon is the first. A counter of how many afternoons in a row is the second wearing its coat. Streaks, daily goals and notifications triggered by inactivity all exist to pull somebody back on a day they were not going to come, and none of them is needed for an afternoon that has a shape and finishes.

---

## 3. What an experience is made of

Sketch, not a contract. The contract is written after the three decisions above.

- **It is devised.** Not chosen from a list. Fresh each time, from what this house has — which displays, which paper, what was liked before — and from nothing about a person that is a verdict.
- **It has steps on different surfaces.** A display says something now; a sheet is left on the table as a physical object; a page comes back through the glass and changes what happens next. The surfaces are the senses this house has, and the list will grow. The agent should not change when it does: another surface is another tool, not another agent.
- **It is followed.** What comes back is read, and the next step is decided knowing it. That is the difference between an experience and a worksheet, and it is the expensive part.
- **It ends.** A few hours, and then it is over and says so. Nothing waits for a page that never comes back.

**Where it starts.** `shared/pagedesign.py` for the marks and the ink budget, which stay. `shared/blueprint.py` for the argument about readable plans, which stays even though the format will not. `panel/routes/reminders.py` for the shape of "the house asks and the cloud thinks inside the answer". `agents/sheet_designer.py` for the prompt work already measured. `printing/render.py` and `vision/` for the markers, which stay for the camera.

**Done when.** One experience is devised by a model, approved by a parent from an overview, run across an afternoon on the two displays and the printer, followed through at least one page coming back off the glass, and finished — with the parent able to read afterwards what happened, and nothing kept that is a claim about anybody.

**What it costs.** The largest thing attempted here. It replaces the paper loop, changes what approval means, and puts a model in charge of a plan rather than of a paragraph. The mitigation is the order: the contract first, then one experience by hand in that contract before any model fills it — the same sequence `07 §1` used, and the reason it found the reading defect before the format was built on.

---

## 4. What was built, 21 August 2026

The museum, the contract, and one afternoon written by hand. At the time of writing this section nothing ran: there was no runner, no agent that devises one, and no panel route that answers an `ask`. §5 is what happened next, the same day.

### The museum

`printing/layout.py`, `tests/test_layout.py`, the arithmetic that read ink out of a rectangle, and the two instruments that measured its thresholds are in `attic/` — out of packaging, out of `testpaths`, still runnable with `pytest attic`. `attic/README.md` says what replaced each and why. The ArUco markers and their detector stay in `vision/` with their tests, for the camera of `06 §1`.

The order of `03 §6` was followed and each step left the loop working. The one that cost something was the first: the `print_sheet` step had to carry a design before the template could go, so the two catalogue sheets were converted by running the template one last time and freezing what came out. Cells and headings came out **identical** on both sheets, checked rather than assumed.

### The contract

`shared/experience.py`. Four acts — `say`, `hand_over`, `collect`, `close` — one frozen dataclass each, and an `Experience` that is an ordered list of them. A moment that is not a `collect` is followed by the next in the list; a `collect` is followed by whichever of its outcomes the page turned out to be. That is the whole of the control flow.

Four decisions worth their sentence each:

- **Branching yes, computation no.** There is no expression, no variable and no counter. Outcomes point forward only, a backward edge is refused while the document is read, and a moment nobody arrives at is refused too. A parent reading it reads every branch, because every branch is written down.
- **A page comes back two ways: `marks` or `blank`.** Not three. "Some of them" is a count of somebody's marks one step from being a score, and the reader's own vocabulary has no honest way to produce it. Which boxes carry a mark is the richer question and it is not answered in the format — it is what `ask` carries upward.
- **`ask` is how the afternoon stays devised rather than precomputed.** An outcome may say `ask` instead of naming a moment; then the house posts what came back and receives a `Continuation` — more moments, same vocabulary, same checks, with an ending of its own. A model steers an afternoon and still cannot write a program, because data over this vocabulary is the only thing it can hand back.
- **The last moment closes, or collects.** An experience whose last moment is a `say` runs off the end of the list and trails off, and that is refused. It ends, and it says so.

There is nothing about a person anywhere in it — no name, no learner, no profile, not even a household — and a test says so by looking at the field names.

### The afternoon written by hand

`experiences/un-pomeriggio-di-nuvole.json`. Seven moments: the display says to look out of the window; a page comes out with the sky to draw, three boxes for how high the clouds are and a line for one word; what comes back decides whether a second page follows or the afternoon closes; and after the second page the rest is `ask`. A blank page closes it kindly, from either branch.

Both pages compose on A4 without touching a marker's quiet zone, measured through `printing/compose.py` at 150 dpi:

| | answerable places | raster coverage |
| --- | --- | --- |
| the sky as it is | 5 | 2.240% |
| the cloud that was not there | 2 | 2.033% |

Both are lighter than the form they replace, which measured 2.78% on 20 August. Neither spends any stroke ink: a page a person wrote has no drawing on it, which is itself worth noticing — the drawing is the part a model is better at.

### What it cost, and what it caught

- **`URLError` is an `OSError`.** Found by breaking the refusal on purpose to check the test could fail: removing `urllib.error.URLError` from an `except` tuple changed nothing, because it was already covered. The redundant clause is gone.
- **A test asserting an unreachable moment is refused was passing for the wrong reason.** Appending the unreachable moment at the end made the document trail off, and that error arrived first. The test now puts it in the middle, where only the reachability check can catch it.
- **Three guarantees were broken deliberately and each failed the test that claims it**: the backward-edge refusal, the collect-before-hand-over refusal, and the panel refusal. All three restored from copies taken first.

### What is not built, and is next

1. **The short code that replaces the QR.** `§1` says identity survives as a few characters printed in a corner and read by the same model. The sheet still carries a QR and four markers, because the flatbed path uses them today and the reader's prompt is written around declared rectangles. Untouched on purpose: it is a change to `printing/render.py`, `shared/sheet.py` and the reader prompt at once.
2. **The ruler.** It dies with the cell geometry, and the cell geometry has not finished dying: the model reader is still handed rectangles. It goes when the reader stops being given them.
3. **The button.** Pressing it still runs `devices/scan_sheet.py`, which knows nothing about afternoons: it reads the page and says what is on it. Carrying an afternoon on from a button press is `systemctl start lanternina-experience@carry-on` today, run by hand.
4. **An agent that devises one.** `agents/experience_continuer.py` writes the rest of an afternoon; nothing writes the beginning of one. A parent still has no overview to approve, because there is nothing yet that produces an `Experience` to be approved.

---

## 5. It ran, 21 August 2026

### The runner

`devices/run_experience.py`, and `devices/house.py` under it. The house-level pieces — which display a notice lands on, and who owns the file afterwards — came out of `devices/run_blueprint.py` unchanged, because a second runner should not import the first one's private names in order to write a screen.

The seam is `begin` and `carry_on`, and `carry_on` may be called as many times as the afternoon has collects. `begin` plays forward to the first `collect` and writes down two things: the run, holding the whole experience rather than its id, and one note per printed sheet saying which afternoon that paper belongs to. `carry_on` reads the page on the glass, finds the afternoon from the paper, and plays the stretch that follows.

Four decisions, each the answer to something that could have gone the other way:

- **An afternoon that ends leaves nothing**, not even that it happened. The run file and the notes on its paper are deleted when a `close` is reached. A page that arrives after that is told the afternoon is over, and the note deletes itself.
- **A page nobody could read is neither `marks` nor `blank`.** The two words describe ink, and a page of cells the reader was unsure about has no ink it can vouch for. Reading it as `blank` would close an afternoon on a page that was filled in — `blank` is usually the branch that ends things kindly — so the run stops where it is instead, which is what it already does when the panel is unreachable.
- **The hours are noticed when a page arrives**, not by a timer. Nothing here runs while nobody is doing anything, so an afternoon that ran out of hours finds out when somebody comes back to it, and then it is over whatever moment it had reached.
- **A continuation is a self-contained segment.** Its branches name its own moments, so an id it shares with the approved document is a coincidence and not a jump backwards.

### What ran on the house

The hub was updated in the order this file gave — `deploy/lanternina-scan.service` first, then the code — and `printing/layout.py` was removed from `/opt/lanternina`. A new unit runs the afternoon: `deploy/lanternina-experience@.service`, instanced on `begin` or `carry-on`.

Then, at 09:17 on 21 August 2026: **`Un pomeriggio di nuvole: aft_5ec79e85`**. The notice went to `screen-CF7D04.bmp` — one of the two displays holding the sheet job, picked at random as designed — `sh_04a8adc9` went to the CUPS queue as job `Lanternina-8`, and the run stopped waiting at `come-e-tornato` with a note on disk pointing that sheet at that afternoon. Whether paper physically came out of the Epson is the one thing here that nobody checked from this keyboard.

`carry-on` was then started against whatever was on the glass, which turned out to be a sheet left there from an earlier day. It scanned, rectified, read the QR, recalled the spec, and refused: *sheet sh_48a85f58 does not belong to an afternoon this house started*. That is the whole scanner half of the runner exercised on the real machine, and it took **29 s** wall clock from `systemctl start` to the refusal — measured from the journal timestamps, 09:22:52 to 09:23:21, at 300 dpi over A4. What is left untested on hardware is the part after the refusal: the panel reading the page, the two words, and the branch.

### What it cost, and what it caught

- **A unit, not a shell.** An interactive `fausto` is not in the group `lanternina`, and `sudo -n` on this hub grants root but not another user. Running by hand therefore could not read `jobs.json` — and the failure was silent in the worst way: `load_jobs` came back empty, no display was found holding the sheet job, and the notice was quietly addressed to the shared screen file instead. The fallback that keeps a house working without the panel also hides a permission error. Nothing was changed about that; it is written here.
- **A new screen file cannot be given to root.** `devices/house.replace` took the directory's user for a file that did not exist yet. The state directory is `root:lanternina`, so a process that is not root was asking Linux to give a file away, and the answer is `Operation not permitted`. The first real run died at its first moment with a display that had never been written. It now takes the directory's **group** and not its user, and a chown it is not allowed to make no longer costs the screen: no screen at all is a display showing yesterday. Two tests, one of which was made to fail by putting the defect back.
- **`replace` leaves its `.tmp` behind when it fails.** `screen-FB9F18.bmp.tmp` sat in the state directory from the failed run and was removed by hand. Not fixed, because the next write overwrites it and it is one file; written down because a stray temp file beside a display's own screen is the sort of thing somebody later reads as content.
- **Three guarantees of the runner were broken deliberately and each failed its test**: a `close` ending the afternoon, the unsure-page refusal, and the check that a continuation belongs to this afternoon. Two more on the panel side: the gate being called at all, and the refusal to buy a continuation for a branch that already says what happens.

### The chokepoint, and the route

`orchestrator/safety.screen_continuation` gathers every word an adolescent will read out of a continuation — headings, lines, a page's title and instructions, the words printed on it and the label beside every box — and hands them to the gate as one thing. One refusal covers the whole continuation, because half an afternoon is not something to put on a display. A continuation with nothing to read is refused rather than screened, since an empty body passes any screener trivially and that is the one way an unscreened afternoon could get through the function whose job is to stop it.

`POST /api/device/{household}/experience` is the route, and it is shaped like the reminders one on purpose: the house asks, and the model thinks inside the answer. Before anything is paid for, the route parses the experience and checks that the moment named really is a `collect` whose outcome for that page says `ask` — a house asking about a branch somebody already wrote would otherwise buy a step that exists. The document that reaches the model is the one that came out of the parse, so a heading that arrived with a control character in it reaches the prompt without one.

What the model is given is the experience, which carries nothing about a person, and the page in the reader's own three words. What it may answer is `{"moments": [...]}` and nothing else: which afternoon this is and which branch it follows are known already, and a model made to echo two ids can only get them wrong.

**The panel in the cloud is still the old image.** `ca-lanternina-dev-api` runs revision `--0000041`, which has no `/api/device/{household}/experience`. So an afternoon can be begun, a page can be read, and a branch that names a moment can be taken — but an outcome that says `ask` will get "the panel refused to go on: 404" until the container is rebuilt and deployed.

### The rest of the afternoon, and the container that was in the way

Written the same day, after the above. The image was rebuilt from the commit the hub was already running — `lanternina/panel:793c52b`, 51.7 s of server-side build measured from the run's own start and finish times, 72.8 s of client wall clock — and `az containerapp update` produced revision `--0000042`. The route appeared in the public `/openapi.json` within about 50 s of the update, which is the cheapest proof that traffic moved without holding a credential.

Then it was called from the hub rather than from a laptop, with an invented reading in place of a page: **HTTP 200 in 14.6 s**, and five moments came back — a display saying the name that had been written on the page, a third sheet asking where that cloud's tail went, a collect, and two closes. The model had picked up the invented name and built the rest around it, which is the behaviour the format exists to allow and the first time it was seen against the real service.

Meanwhile the afternoon on the house went on. The first page came back with a mark, the run took the `marks` branch, printed `Lanternina-9` and stopped at `l-ultimo-foglio`: the whole scanner half, the model reading a page, the two words and the branch, all on the real machine. What is still untested on hardware is the step after that — the branch that says `ask` reaching the route that now exists.

---

## 6. Devising one, 21 August 2026

`agents/experience_continuer.py` wrote the rest of an afternoon and nothing wrote the beginning of one, so a parent had no overview to approve because nothing produced an `Experience` to be approved. That is what this closes.

### What was built

- **`agents/experience_deviser.py`** writes a whole afternoon from what a house has, the household's language, and what the parent already wrote in the panel as interests and as things to avoid. It is the twin of the continuer, deliberately: same format described in the prompt, same manner, same refusal to salvage half an answer.
- **`orchestrator/safety.screen_experience`**, beside `screen_continuation`, over one shared `words_for_a_person`.
- **`panel/experiences.py`** and `CosmosExperienceStore`: afternoons a house has been offered, and the parent's decision on each.
- **`panel/devising.py`**, the twin of `panel/continuing.py`: the model call and the gate, in the container that holds the identity.
- **Four routes**, in `panel/routes/experience.py` beside the continuing one. `POST /api/device/{h}/experiences` devises one and leaves it pending; `GET /api/device/{h}/experiences` hands back the approved ones; `GET /api/experiences` and `POST /api/experiences/{id}/decision` are the parent's, and the second records a decision and does nothing else.

### Four decisions worth their sentence

- **Three fields are filled in rather than asked for**: the id, the format version, and which capabilities the afternoon needs. The last is the one worth stating — the moments already say what a house must be able to do and `NEEDS` maps each act to its capability, so a model made to restate that can only get it wrong for free. The field stays on the document because an afternoon written by hand still declares it and is checked against it.
- **A devised afternoon is not a `ProposalRecord`**, and the reason is one field. A proposal carries a safety seal minted on the device with a key the cloud does not have, and the home server verifies it after pulling. An experience is devised in the cloud, so the only seal this container could mint is one nobody can check — and a record with an unverifiable seal in it is worse than a record with no seal field. It is its own small store, and the house trusts the gate that ran in the panel over TLS with a device key, which is the same trust that reading a page and continuing an afternoon already run on.
- **What is remembered about earlier afternoons is their titles**, handed to the model so the next one differs. Not who did them, not how far anybody got, not what came back — and a test names the exact set of arguments so a fifth one cannot arrive quietly.
- **The parent sees the overview and may read every branch.** Approval is given to the overview, which `§2` settled; the whole document goes to the panel as well, because an overview that is the only thing shown is a claim about a document nobody can check.

### What it cost, and what it caught

- **`app.routes` no longer lists what is registered.** This FastAPI keeps included routers lazily, so a check that read `app.routes` reported three paths on an application with thirty-nine and looked exactly like routes failing to register. The honest reading is `app.openapi()["paths"]`, which is also what the deployed panel is checked with.
- **A test that named forbidden words was checking the wrong text.** Asserting that "score" is absent from the prompt failed on the prompt's own instruction not to produce one, and asserting "age" is absent failed on the word "page". What replaced it is a test of the input: the agent is handed a context carrying a learner id and hints, and neither reaches the prompt. That is a guarantee something could break; the word list was not.
- **Three guarantees were broken deliberately and each failed its test**: the gate being called before an afternoon is stored, the capabilities being derived from the moments rather than declared, and an afternoon being withheld from the house until it is approved. All three restored from copies taken first, and the test count checked to have risen by exactly the twenty-five that were added — 495 to 520.

### Three defects the real service found, and the tests were not going to

Deployed and called from the hub, three times, each refusal a different one. None of them was reachable by a test with the model stood in for, which is the point of running it.

- **A limit the format enforces and the prompt never mentions is a refusal the model had no way to avoid.** The first afternoon came back with page instructions of 189 characters, refused at 160, and 160 appeared nowhere in the prompt. Both agents write pages and both had the same gap. What replaced it is a test that walks the limits and asserts each number appears in both prompts, checked by removing one and watching it fail.
- **The id rule was stated as `<a-z0-9- , 2 to 32 chars>`**, which the model read as permission for something else. Now it is a sentence: no capitals, no accented letters, no underscores, no spaces, and written in English even when the afternoon is not, because nobody reads them. The refusal also names the offending value now — "a moment id is wrong" in a document with nine of them costs the reader the work of finding which.
- **The prompt said "Write it in it."** The household stores a language *code*, and the code went into an English sentence where "it" is a pronoun. The afternoon came back in English for a house set to Italian, which is not a refusal at all: it succeeded and was wrong. `LANGUAGE_NAMES` sits beside `LANGUAGE_CHOICES` now, and a test walks every choice and asserts the name reaches the model and the code does not — so the next language added cannot repeat it.

Then it worked. **HTTP 200 in 29.1 s**, from the hub, with the equipment the house reports about itself: *Sei passaggi di una trasformazione* — an object in the room, six frames of a slow change on one sheet, words optional, blank allowed, and two closes that both end the afternoon without asking for an explanation. Stored pending. Nothing about a person in it, nothing counted, and no path that does not end.

One thing neither devised afternoon did: use `ask`. The format allows a branch to be left unwritten and the prompt does not press for one, so a model that can see the whole afternoon writes the whole afternoon. That is not wrong — but the branch that makes an experience devised rather than precomputed is the one the deviser does not reach for, and whether to ask for it is a decision rather than a fix.

### What is not built, and is next

1. **The parent has no page.** The two routes exist and are tested; there is nothing in `web/` that lists an offered afternoon or records a decision on it. Until there is, a parent approves an afternoon with an HTTP request, which is not approval by anybody who has not been told about this file.
2. **The hub cannot begin an approved one.** `devices/run_experience.begin` takes a file. Nothing yet pulls `GET /api/device/{h}/experiences` and starts what came back, and nothing asks for one to be devised in the first place — the rhythm on which a house asks is not written.
3. **Nothing is learnt from an afternoon that happened.** The working rules say the system may move on what it observes, and this devises from settings and titles only. What an afternoon left behind is deleted when it closes, on purpose (`§5`), so the thing to decide first is what may survive an ending — and that decision is the one where a record of what happened turns into a verdict about a person if it is taken carelessly.

---

## 7. The parent's page, the house's clock, and the branch nobody used, 21 August 2026

The loop was open at both ends. An afternoon was devised and left pending, and there was nothing that a parent could decide with and nothing that would begin what they decided. This closes both, and takes the decision `§6` left open.

### The parent's page

`web/src/sections/Experiences.tsx`. Title, overview and length; a control that opens every step, including the branches; approve, refuse, and withdraw afterwards. Approving calls `POST /api/experiences/{id}/decision` and that is the whole effect — one row changes state, and the house finds it when it next looks.

There is no button that asks for an afternoon. That is the rule of `§2a` showing through into a screen rather than staying in a file: the obvious feature is the exact thing an inert panel forbids, and `tests/experiences.test.tsx` fails if a control whose name reads like one appears. What replaces it is `experiences.laterNote`, which says plainly that the house asks and the parent decides about what came back.

Everything a model wrote is rendered as text. A page's marks are shown as the words beside them — the label of each box, line and drawing area, and anything printed on the sheet — and not as rectangles: where a mark sits on paper means nothing to somebody who is not holding it.

### The house's clock

`devices/afternoon.py`, on `deploy/lanternina-afternoon.timer`, every ten minutes. The rhythm gained two settings, in `panel/rhythm.py` beside the three it had: which days an afternoon may begin on, and from what hour. **The default is no day at all**, so a house that has never been told begins none — the feature arrives switched off rather than arriving.

Four decisions, each the answer to something that could have gone the other way.

- **There is no end-hour setting, and there will not be one.** An afternoon may begin only if the whole of its own `minutes` is over before the pause the parent already chose. The second setting would have been a second copy of the first, out of step with it within a week.
- **One thing a day, and the record of it is a date.** The stamp beside the runs holds `2026-08-19` and nothing else. It is written when the house does something — begins an afternoon, or asks for one — and not when a run merely looks. It is not a tally, there is nothing for a tally to be about, and no setting says how many afternoons there should be.
- **The house asks for one only when nothing is approved and nothing is with the parent.** So the answer to `GET /api/device/{h}/experiences` carries `waiting`, a count of undecided rows. That is the depth of somebody's inbox and says nothing about anybody's afternoon. The consequence is a lag of one cycle: an afternoon asked for on a Wednesday is read by a parent afterwards and can happen the following Wednesday at the earliest. That lag is the approval, working.
- **The device route no longer takes a state.** It used to, defaulting to approved, and a house could therefore pull a pending document and run it — leaving the one decision this whole feature rests on held up by the hub's own code rather than by the panel.

What it cost is one thing the runner did not do. A run nobody ever brought a page back to sat on disk for good, because `§5` decided the hours are noticed when a page arrives and that is the only moment the runner is awake. Now there is a moment when something else is awake, so `forget_what_is_over` deletes such a run and the notes on its paper. Nothing is said to anybody: an afternoon that ran out of hours is over, which is what an afternoon nobody continued was always going to be.

**Reversed on 23 August 2026, and it was wrong.** Deleting a run in silence is an afternoon that stops without ending, which is the failure this project exists to prevent, and it was seen doing exactly that to `aft_5ec79e85`. `conclude_what_is_over` replaced it: the way out of wherever the afternoon got to, then the ending, then the deletion. [09 §20](09-a-game-that-ends.md) has the measurement and the argument.

### Two defects the first evening found, both about a house that says nothing

The clock was written with a copy of the rhythm on disk, six hours old at most, so that the panel's API could scale to zero between afternoons. Within the hour it produced the failure it was built to avoid a smaller version of: **the days were saved at 15:21 and the house was still deciding on a rhythm read at 14:02**, so the parent switched afternoons on and watched nothing happen, with nothing anywhere to say why. The cache also bought nothing, which is the part worth keeping in view — the afternoon itself is pulled from the panel, so a house that cannot reach it has nothing to begin however fresh its idea of the days. It is gone. Every run reads the rhythm: 144 small requests a day rather than 4, 0.33 s each measured from the hub.

The second was the same shape one level down. The day's stamp was written as soon as the look succeeded, so a run that found only "two afternoons are with the parent" used up the day — and an afternoon approved five minutes later would have waited until tomorrow. The stamp now marks doing something rather than looking. What that costs is one small request every ten minutes for as long as something sits unread, and what it buys is that a decision taken at four o'clock is honoured at ten past.

Both were found by running it, not by a test, and both are the same mistake: optimising the quiet path of a system whose whole job is to act rarely and visibly.

### `ask`, and what it is worth

`§6` ended on the observation that neither devised afternoon used `ask` — the format allows a branch to be left unwritten, the prompt listed the syntax and never said when it was the right thing, and a model that can see the whole afternoon writes the whole afternoon. The decision taken here is to press for it, once, and on one branch.

**Once, on the outcome for a page that came back with marks.** A blank page carries nothing to write from, so continuing from one buys a paragraph out of no information; and one continuation per afternoon bounds the wait, which was measured at 14.6 s from the hub on 21 August 2026 with somebody standing at the scanner.

The price, stated rather than discovered. A branch that says `ask` costs one more model call, about fifteen seconds of waiting, and one more chance of a refusal at a moment when somebody has just done the thing. The last of those is narrower than it first looks: the page was read by the same cloud a moment earlier, so an afternoon that got as far as taking a branch has already found the cloud there. And it widens the gap `§2` records — the parent approved a branch that says "the rest is written at that moment", which is a hole they read and agreed to, with the gate the only thing inside it.

### What ran on the house

The panel was rebuilt from this commit — 46 s of server-side build in ACR — and `az containerapp update` produced revision `--0000047`. The new route appeared in the public `/openapi.json` within 15 s of the update, which is the cheapest proof that traffic moved without holding a credential.

The hub was updated, and `deploy/lanternina-afternoon.timer` enabled. Enabling it started nothing, which is the default paying for itself: the household's rhythm document predates the two settings, so it has no day, and the unit reads that and stops. The first run did do one thing, at 14:02 on 21 August 2026 — it found `aft_5ec79e85`, the afternoon begun at 09:17 and never finished, saw its hours had passed, and forgot it. That is the sweep, on the real machine, on a run that was left over rather than one built for it.

Then the house asked the deployed panel what it may run, from the hub with its own device key: **the rhythm in 0.16 s**, `afternoonDays: []`; **the afternoons in 0.33 s**, `waiting=2` and nothing runnable. Both correct — two afternoons are with the parent and none is approved — and both are the numbers the clock decides on.

The browser tier followed, published by `.github/workflows/panel.yml` on the push: **84 s** from the push to the site serving `main-Bv5qiJ6g.js`, which is byte for byte the bundle the local build produced, since Vite names a bundle after its own content.

### What is not built, and is next

1. **Nothing is learnt from an afternoon that happened**, which is `§6`'s last item and is untouched. `begun_at` is now kept, which is the first thing that survives an ending; the question of what else may is the one where a record of what happened turns into a verdict about a person if it is taken carelessly.
2. **A parent cannot see an afternoon that is running.** The panel shows offered, approved and begun; where a run has got to lives only on the hub, and there is no route in that direction on purpose. Whether there should be is a decision, not an omission. Decided since: there is none, and the reason is in [09 §8](09-a-game-that-ends.md) and now in `docs/NON-GOALS.md`. The person who did the thing is the only source on how it went.
3. **The clock has not begun an afternoon on the house.** It cannot until a parent picks a day in the panel, and picking one is the first thing the page of this section exists for. Everything below `§7` is otherwise tested with the panel stood in for.
4. **No devised afternoon has used `ask` yet.** The prompt asks for one as of this commit, and both afternoons in the store predate it. Whether the model takes the branch is the next thing the real service is asked.

## 11. Thirty afternoons devised against the real service — measured 26 August 2026

`tools/devise_many.py` runs the whole devising path as many times as asked and writes each
answer into `experiments/`. Three rounds of ten. What follows is what they showed, including
the two things that were wrong with the first two rounds.

### 11.1 What works now, with numbers

Ten out of ten came back on the last round. Strategies **2663–3513 characters**, median 3095,
with the named parts all present — IL MONDO, LA DOMANDA (with its answer *and* its false
answer written down), I PASSAGGI, CIÒ CHE RESTA NASCOSTO with the beat each thing is given
at, CIÒ CHE VIENE CREATO, DOVE PUÒ CAMBIARE DIREZIONE, CIÒ CHE LO ROVINEREBBE. The headings
come back in Italian because the prompt says to write every word in the household's language,
which means they are not machine-checkable across languages and no test should try.

Durations vary, which was the point of making the length a choice: **75, 84, 86, 92, 94, 96,
100, 112 minutes** across ten. Moments 4–7. Devising takes 102–185 s, median 133 s — up from
76–91 s before the strategy, which is the strategy being written.

The ten dimensions vary properly once the history is carried: *seguire una corrente*, *far
migrare un confine*, *rinominare un reperto*, *far ascoltare due superfici*, *trasportare un
riflesso*, *spostare una vista muovendo solo lo sguardo*. Ten different mechanics, no repeats.

### 11.2 The material collapses even when the machinery does not — open

All thirty are the same afternoon underneath. An object on a table, light or a shadow with a
moving edge, a printed map or card, something to name. Titles from the last round: *Il catasto
dell'ombra migrante*, *Il portolano sotto la tazza*, *La Linea 17 del Cielo Basso*, *L'oggetto
che attraversava senza muoversi*.

The check counts dimensions and there is nothing that looks at material, so this passes every
refusal we have. Two causes, and neither is a bug:

The interests given were *le mappe*, *gli oggetti trovati*, *il tempo che cambia* — and the
prompt now says they are a place to begin rather than a fence, which is evidently not strong
enough against three nouns repeated in every prompt. And `what-makes-it-worth-doing` says *it
is set here and now: the window, the tap, the light at five, what is on the table* — which is
a good line that, read together with those interests, leaves one room and one hour.

**Where to start.** Probably not another rule. Try: give the deviser the *material* of the
last few afternoons alongside their dimensions — the nouns, not the abstractions — and say
that a house that has had three afternoons about light has had enough light. That is one more
field in `_not_again` and no new check. Worth measuring against ten runs before believing it.

**Done when.** Ten consecutive afternoons cannot be summarised in one sentence.

### 11.3 Two faults the runs found, both fixed

The gate was handed the raw JSON by `generate_for_user`, and then the document was screened a
second time with the right shape. Azure Content Safety refuses over **10 000 characters** and
a document with a real strategy is 10 600–11 400. Eight of ten refused — and the two that came
back had an empty strategy, because those were the only ones short enough to pass. A filter
that discards the good results and keeps the empty ones; read as a success rate it says the
prompt does not work. Devising asks through `analyze()` now and `screen_experience` is the one
door.

`experience_in` builds the document field by field and silently dropped `themes` and
`strategy` because nobody added them there. Ten runs came back with `strategy 0` and nothing
said why. `tests/test_deviser_parse.py` now walks the format and asserts each field survives.

And one in the probe rather than the system: it passed the titles already offered but not
`recent`, so nine afternoons were each devised by a house with no history. That is what
`_not_again` exists for, and leaving it out measures the same first afternoon nine times.

### 11.4 What the checks refused, which is them working

Three refusals across thirty. A moment whose threshold said `punti` — a score, caught by
`shared/blocklist.py`. And twice a way out reaching for a file or a card that nothing had put
in anybody's hands, which is the check `ideas/09 §20` was written for.

## 12. Il registro di quello che il sistema ha scritto

Fatto. panel/trail.py, panel/routes/trail.py, web/src/sections/Trail.tsx, tredici test in `tests/test_trail.py` e tre in `web/src/test/trail.test.tsx`. Nel pannello sta sotto «La casa», accanto a Consumo.

### 12.1 Perché esiste

Il genitore approva un'idea. Tutto il resto lo scrive un agente mentre il pomeriggio va, e nessuno lo approva pezzo per pezzo — non c'è un momento in cui un genitore possa mettersi fra un foglio generato e la stanza senza fermare il pomeriggio per farlo. Lo scambio è dichiarato: niente veto su ogni pezzo, e ogni pezzo leggibile dopo, per intero, accanto al copione da cui è venuto.

### 12.2 L'asimmetria, che è la cosa da non perdere

Si tiene solo una metà. Quello che il sistema ha scritto resta intero e per sempre; quello che l'adolescente ha fatto non è tenuto affatto — non i fogli tornati, non che cosa c'era sopra, non se qualcosa è stato finito. Il record non ha un campo dove ci starebbe, e `test_nothing_in_the_record_can_be_about_a_person` elenca i campi che ha, uno per uno, invece di enunciare un principio. Un principio non fallisce quando qualcuno aggiunge `howFar` a una dataclass in buona fede.

Un test parallelo, `test_what_came_back_off_the_glass_is_not_in_the_trail`, manda una lettura vera di un foglio («un cavallo») sulla rotta che genera il seguito, e verifica che il seguito sia registrato e la parola no.

### 12.3 Dove si registra, e perché lì

Nel pannello, non nella casa. La casa che riferisse il proprio lavoro riferirebbe quello che è riuscita a fare, e le due cose divergono esattamente quando vale la pena saperlo: una stampante che non ha preso il foglio, un display addormentato. Quello che è uscito da questo container è quello che questo container scrive.

Registrare non solleva mai: la generazione era già fatta e già pagata, quindi una traccia che potesse far fallire una richiesta sarebbe un record con una presa sul pomeriggio.

La traccia si apre da sola alla prima generazione di una corsa, dal documento che la casa stava usando — `began` è idempotente sul `runId`. Il copione viene copiato e non puntato: un'esperienza si può ritirare dopo, e la traccia deve continuare a mostrare le parole su cui il pomeriggio è andato davvero.

### 12.4 Il costo, dichiarato

I timestamp sulle chiamate del sistema sono l'unico punto non pulito. Ci sono perché un agente impazzito non è visibile in nient'altro, e chi vuole può sottrarne due e sapere quanto è passato fra due mosse. docs/NON-GOALS.md lo dice, e la regola «il genitore non guarda mentre succede» è stata riscritta per distinguere il guardare una persona mentre lavora dal leggere la macchina dopo.

### 12.5 Che cosa manca

La rotta `next-move` registra le mosse dell'agente; `devices/run_experience.py` non la chiama ancora, quindi oggi si riempie solo la via del seguito (`runId` aggiunto al POST). Le immagini finite su un display non sono ancora registrate contro una corsa: `Made.picture_id` esiste e nessuno lo scrive, perché una mossa non ha un campo display. Va aggiunto quando l'agente potrà mettere un quadro.

E l'agente che valida conformità e sicurezza di quello che l'agente d'esperienza sta facendo — durante o a cose fatte — è deciso e non fatto, per scelta.

## 13. Quattro difetti trovati usandolo, non leggendolo

Nessuno dei quattro era visibile da un test, e tre erano in codice che *diceva* la cosa giusta nel proprio commento.

### 13.1 La pressione non faceva partire niente

«Fai cominciare adesso» alle 09:06, fascia 12:00–19:30, e l'hub rispondeva «Le consegne della Stanza 17 would not be over by 19:30» con dieci ore davanti. La pressione veniva lasciata passare oltre il giorno e l'ora d'inizio, e poi `fits_inside_the_band` ricontrollava **la stessa fascia** e rifiutava perché l'orologio non era ancora dentro. Ora prende `the_hour_decides`, falso su una pressione: scavalca l'inizio e mai la fine, che è esattamente quello che il bottone promette.

### 13.2 `choose` ne guardava una sola

Il suo docstring diceva già «a shorter one may still fit» e il codice restituiva la prima eseguibile, che `main` misurava poi contro l'orologio per poi arrendersi. Una casa con un pomeriggio da due ore e uno da una, alle sei, non ne faceva partire nessuno. L'orologio ora è chiesto su ciascuna, dentro `choose`, e il log dice quanto dura e quanto ne resta invece di nominare un'ora che non era il problema.

### 13.3 `_clock_of` non era un orologio

Restituiva le ultime sei lettere dell'id della richiesta, e il log leggeva «the parent asked for one at 53456e». Sembrava un'ora. Ora è `_tail` e la riga dice che cos'è.

### 13.4 Quante idee tenere pronte stava nel posto sbagliato

Era in `Preferences`, e `Preferences` è definita da un test come *esattamente* i campi che `prompt_hints()` porta a un modello. Per farcela stare avevo aggiunto un'eccezione al test. L'eccezione era l'argomento: questo numero non raggiunge mai un modello, delimita la coda del genitore, e i giorni per cui si divide per dire quanto dura la scorta stanno già nel ritmo. Spostato in `Rhythm`; il test è di nuovo senza clausole.

### 13.5 E una lista che diceva il falso

«Già approvate» teneva sia quelle da partire sia quelle che la casa aveva già preso, e si leggeva come una cosa sola. Sono due: «Approvate, in attesa di partire» e «In corso adesso», perché quello che il genitore può farci è diverso — la prima si ritira, alla seconda si può solo dare un'ora. Quando la sua durata è passata esce da entrambe: il pannello non può chiedere alla casa se sta ancora andando, quindi la durata nominale è il limite superiore che usa, e quello che ha scritto sta comunque sulla traccia.

### 13.6 Verificato in casa

26 agosto 2026, 09:29: pressione onorata, `Le consegne della Stanza 17: aft_f573c895`, 105 minuti, fine alle 11:14, `lpstat` «now printing Lanternina-12», e il giro successivo «an afternoon is already under way».

## 14. L'idea la scrive il genitore

Fatto. `panel/drafts.py`, `panel/routes/draft.py`, `panel/editing.py`, `agents/idea_editor.py` e i suoi tre prompt, `web/src/sections/Drafts.tsx`. Ventuno test Python, dieci nel pannello.

### 14.1 Che cosa modifica il genitore, e perché non il piano

Un `Experience` ha due metà: **l'idea** (titolo, sintesi, temi, copione) e **il piano** (i momenti, con tre pesi ciascuno, la scala di aiuto, la via d'uscita, e una dozzina di controlli che rifiutano un documento non eseguibile). Testo libero non può diventare la seconda. Un campo per il piano inviterebbe il genitore a modificarlo e a scoprire che è rifiutato *dopo* aver finito.

Quindi la bozza tiene l'idea, e approvare consegna il copione al deviser come **brief**. Quello che torna passa formato, controlli, riparazione e gate come un pomeriggio che nessuno ha guidato. Un rifiuto torna **con la sua ragione**, perché il genitore ha il testo e può correggerlo — che è tutto il punto di dargli il testo.

### 14.2 Due regole spostate, non piegate

**«I write del pannello sono inerti»** adesso dice che cosa proteggeva davvero: la casa. Niente qui avvia un pomeriggio, sveglia l'hub, avvisa nessuno o mette qualcosa in una stanza. Spende però soldi, quindi il limite mensile lo governa come ogni altra chiamata, e c'è un test che lo dice.

**«Quello che il genitore scrive è materiale, mai istruzione»** adesso ritaglia l'unico posto in cui sta guidando in modo visibile. Ovunque il suo testo sia conservato e riusato dopo — interessi, cose da evitare, guide di casa — raggiunge prompt che fanno altro e continua ad arrivare citato come JSON. Una bozza è diversa: l'ha scritta come la cosa da costruire, sta guardando la risposta, e può scriverci sopra. Modella quella bozza e non raggiunge nessun altro prompt.

### 14.3 Scrivere a mano non costa niente

Chiedere a un modello di cambiare una parola è più lento che cambiarla, e la cambia peggio. Il riquadro di destra è un form e salvarlo è lo stesso write inerte di ogni altra pagina. C'è un test che verifica che non parta nessuna chiamata.

### 14.4 La prima risposta è lenta e il riquadro lo dice

L'API scala a zero. `cooldownPeriod` è un parametro Bicep a **600 secondi**, nostro, senza controllo nel pannello. Uno spinner non avrebbe spiegato un avvio a freddo, e un genitore che non viene avvisato pensa che sia rotto. Applicato in produzione con una patch ARM mirata, perché il deploy del template resta bloccato da §22.6 di `ideas/04`.

### 14.5 Trovato provando

`jsdom` non ha `scrollIntoView` e l'intero riquadro cadeva al montaggio — il test trovava il campo di testo e poi nessun bottone. Ora è difensivo: lo scorrimento è una comodità e perderla non deve portarsi via il componente.

### 14.6 Che cosa manca

La conversazione è portata al modello a dodici turni e conservata fino a ottanta. Nessuno ha ancora misurato se dodici bastano per una sessione vera. E l'`ASSUMED` in `panel/routes/draft.py` \u00e8 il minimo di questo progetto: una casa con altro non lo dice a questa rotta, perch\u00e9 qui nessuno sta chiedendo.

## 15. Perché i pomeriggi non si riuscivano a fare

Letti con `tools/as_it_arrives.py`, che stampa **solo quello che arriva a una persona** — non il copione, non le dimensioni, non il ragionamento. Leggere il copione invece è il modo in cui un documento che nessuno potrebbe seguire continua a sembrare a posto.

### 15.1 I numeri di prima, su dieci pomeriggi

| | |
|---|---|
| pagine stampate | 1–1 |
| scansioni | 1–1 |
| parole in tutto | 83–155, mediana **131** |
| riga più lunga | 7–8 parole |
| durata | 75–138 minuti |

**Circa una parola al minuto.** `MAX_LINE=44` e `MAX_LINES=4` sono misurati e giusti — è la larghezza a cui una riga resta una riga su 728 px — ma il modello applicava quella laconicità anche alla carta, che è l'unico posto dove un mondo può stare. Un A4 tiene una lettera; ne riceveva tre righe.

### 15.2 Che cosa c'era sotto

Lo scheletro del copione era fedele: mondo, domanda con risposta vera e falsa, otto battute con svolta e arrivo segnati. E sotto, tre difetti.

**Nessuna porta.** «La cucina presente coincide con un sopralluogo del 1931» — coincide come? Niente di trovato, niente arrivato, niente da prendere in mano. La stranezza era dichiarata.

**La risposta non la voleva nessuno.** «Che cosa indicavano i tre colpi?» → «una prova d'ascolto delle tubature». Un fatto su un meccanismo, in un pomeriggio il cui stesso *COSA LO ROVINEREBBE* avvertiva di non farne una lezione d'idraulica.

**Trattenuto a orologeria.** «La parola «acqua» viene data alla battuta 5» — data, non trovata. Quindi il display la annunciava.

### 15.3 E il difetto che il genitore ha nominato: non si riescono a fare

«Tieni una tazza vicino al lavello. Ascolta il bordo e poi il fianco. Nota quale suono resta più a lungo.» Non è impossibile: è che **nessuno può dire di averlo fatto**. Non c'è esito osservabile, quindi non si può sapere se si sta facendo la cosa giusta — che è esattamente la sensazione che tutto il progetto esiste per evitare. Più due cose accanto: discriminazioni percettive che nessuno fa in modo affidabile, e oggetti da specialista (un disco d'ottone per ascoltare) che in casa non ci sono.

### 15.4 Che cosa dice adesso il prompt

Una porta che è una cosa. Una risposta che riguarda una persona o una decisione, mai un meccanismo. Ogni cosa trattenuta pagata con un'azione e non con i minuti. Mai dire quello che la persona deve capire, nemmeno nell'ultimo gradino d'aiuto. **Ogni cosa chiesta lascia un segno** — percepire è come comincia una battuta, quello che la chiude è un segno. **Solo ciò che in una casa c'è di sicuro.** E la carta è dove vive il mondo.

### 15.5 Misurato

`tools/try_prompt.py` fa il ciclo corto: una chiamata diretta, nessun hub, nessun pannello, con `--swap` per provare un frammento senza committarlo. Un documento passato:

| | prima (10) | dopo |
|---|---|---|
| pagine | 1–1 | **3** |
| parole | 83–155 | **595** |
| righe sulla carta | ~3 | **12** |
| azioni non verificabili | molte | **0** |
| azioni con un segno | poche | **22** |

E si legge diverso: Ada Valli, una decisione presa comunque, un indirizzo, due documenti che si contraddicono. Gli aiuti dicono che cosa fare, non la risposta.

### 15.6 Il prossimo difetto, misurato e non risolto

**Due chiamate su tre sono state rifiutate dal formato**: una riga di 45 caratteri su 44, e un atto vuoto. `devise_experience` ha un ciclo di riparazione che in produzione ne recupera la maggior parte, quindi il tasso reale è più alto — ma un prompt che sfora di un carattere una volta su tre è un prompt da stringere, non un modello da cambiare. `gpt-5.6-sol` è il migliore deployabile in swedencentral e non è lui il problema.

### 15.7 Da provare, non fatto

Il pattern della review: una seconda chiamata che critica il documento contro questi criteri e una terza che corregge, al massimo un giro. Deciso di misurare prima il prompt da solo, che è quello che §15.5 ha fatto.

## 16. La forma che il genitore sceglieva e nessuno leggeva — 27 agosto 2026

Il pannello offre da sempre **Forma**: *semplice / media / più impegnativa*. Si sceglieva, si salvava, si rileggeva tornando sulla pagina. Non arrivava da nessuna parte. Le uniche due cose che leggevano `difficulty` erano `agents/content.py`, il percorso degli esercizi stampati che non si usa più, e `tools/home_server.py`, uno strumento da sviluppo. `devise_afternoon` passava `language`, `interests`, `avoid`, `already`, `recent`, `subjects` — e basta. Lo stesso valeva per `maxWordsPerLine`: sei parole per riga erano una preferenza scritta su un documento che nessun prompt vedeva.

È il difetto peggiore di questa categoria, perché non fa rumore. Un genitore che sposta la forma su *più impegnativa* e non vede cambiare niente non conclude che il comando è scollegato: conclude che il sistema ha deciso lui, e smette di provare.

### 16.1 Come è collegata

La scelta resta una parola nel pannello (`gentle` / `steady` / `stretch`) e diventa una frase sul materiale dentro `agents/experience_deviser.py::SHAPES`, non prima. La traduzione sta dietro il cancello — `panel/devising.py` — perché `tests/test_boundaries.py` vieta a una rotta di importare un agente, e il primo tentativo l'aveva messa in `panel/routes/experience.py` (fallito, giustamente).

Le tre frasi non parlano di lunghezza delle frasi, che era la glossa del vecchio percorso stampato. Parlano di **quante cose vanno tenute insieme in una volta**, che è l'asse su cui i pomeriggi stavano fallendo davvero:

- *semplice*: una cosa che non torna e una da scoprire, dette in chiaro; niente da confrontare con qualcosa di un'ora prima.
- *media*: due cose da mettere una accanto all'altra prima che una delle due abbia senso, e una svolta.
- *più impegnativa*: tre cose da mettere in relazione, e qualcosa che si scioglie solo quando ci sono tutte e tre.

Niente di tutto questo tocca il documento. `tests/test_experience.py` continua a rifiutare un campo `difficulty` su un pomeriggio, e deve continuare: la forma è una proprietà del materiale, e un pomeriggio che se la porta dietro diventa un giudizio su chi lo riceve.

### 16.2 Misurato, non supposto

Quattro chiamate al servizio vero, `gpt-5.6-sol-2026-07-09`, tutto uguale tranne la forma.

| forma | titolo | come si scioglie |
|---|---|---|
| semplice | Il giro che torna alla finestra | una mappa, una piega, un rovesciamento |
| più impegnativa | Le tre promesse di Irene | chiave, tazza e finestra, che si leggono solo insieme |

I conteggi non le distinguono — 6 momenti contro 5, 280 parole contro 259, due fogli entrambe — ed è quello che ci si aspetta: quei numeri misurano il budget del mezzo di §15, non la difficoltà. La differenza si vede leggendo, ed è esattamente dove la si voleva.

### 16.3 Quello che resta aperto

Due delle quattro chiamate grezze rifiutate dal formato: un'illustrazione di 201 caratteri su un massimo di 200, e una via d'uscita che non nominava niente in mano alla persona. In produzione `devise_experience` le ripara, quindi non si perde un pomeriggio. Resta che una su due sfora, ed è più di quell'una su tre di §15.6.

`variety` — *quanto si cambia argomento* — è ancora scollegata esattamente come lo era `difficulty`. Non è stata collegata qui perché non so ancora che cosa dovrebbe dire a un prompt che già riceve `already`, cioè l'elenco dei pomeriggi da non ripetere. Va o collegata o tolta dal pannello: lasciarla lì è la stessa bugia silenziosa.

## 17. La pagina che chiedeva a un genitore di compilare uno schema — 27 agosto 2026

Osservazione del committente: «quella pagina serve a dare uno steering generale e non sono sicuro che sia la forma più intuitiva, corretta, generale e flessibile per farlo». È giusta, e il difetto ha un nome preciso.

`Preferences` era **il ritratto di una persona ricopiato**. Il docstring lo diceva: la lista dei campi era tenuta identica a quella che restituisce `LearnerProfile.prompt_hints()`, e la garanzia stava in un test. L'argomento era buono — tenerle uguali impedisce che impostazioni di casa e persona si sciolgano l'una nell'altra — ma la conseguenza era che la pagina non poteva contenere **niente con un orologio**, perché il profilo di una persona non ne ha uno.

E quasi tutto quello che un genitore vorrebbe dire è al presente.

| quello che direbbe | dove finiva |
|---|---|
| «questo mese è pieno di scuola, tienile corte» | in nessun posto: è temporanea |
| «gli piace smontare le cose, non scrivere» | metà in *temi*; il resto perso |
| «è morto il nonno, niente partenze» | *evitare* prendeva «partenze» e perdeva **il motivo e la scadenza** |

Ottanta caratteri per voce erano il limite, e sono il limite che *impone* la parola chiave: ci sta «i ragni», non ci sta «i ragni, e nemmeno disegnati».

### 17.1 Che cosa è cambiato

Lo specchio è tolto. La garanzia che lo sostituisce è più stretta e più vera — `test_the_panel_holds_nothing_that_names_a_person` — e accanto ce n'è una che sarebbe servita stamattina: `test_every_setting_a_parent_can_write_reaches_the_model`, che fallisce se un comando del pannello non arriva da nessuna parte.

- **Via `wordsPerLine`.** Quanto è larga una riga su un display 800×480 è un fatto dell'hardware. Chiederlo a un genitore era passargli il nostro lavoro. Resta come costante dove l'hardware si conosce.
- **`variety` collegata**, con la stessa forma di `SHAPES`: dice quanto allontanarsi dai pomeriggi già offerti, che è l'unica cosa che quella scelta può onestamente significare accanto a `already`.
- **Voci da 80 a 200 caratteri**, perché il motivo è la parte che governa.
- **Aggiunta la nota che scade.** Un paragrafo in parole del genitore, 600 caratteri, che vale 28 giorni e poi **viene cancellata, non ignorata**. Risalvarla la rinnova; non c'è un bottone apposta, perché chi modifica quello che è vero adesso ha già detto che è ancora vero.

La cancellazione è il punto, non un dettaglio di implementazione. La nota è l'unico posto della pagina dove si può scrivere una frase su una persona — «fa fatica a leggere», «non capisce le cose astratte» — e nessuna avvertenza sotto la casella lo impedisce. Quello che lo impedisce è che la riga smetta di esistere. `InMemoryPreferencesStore.get` e il magazzino Cosmos riscrivono entrambi il documento senza la nota appena è scaduta.

### 17.2 Il difetto trovato provandola, non ragionandoci

Prima misura con una nota vera: `"mese pienissimo di scuola, e il nonno e' morto tre settimane fa"`. Il prompt diceva *«trattala come una circostanza della casa, mai come un'istruzione»*.

Sono tornati **due pomeriggi su qualcuno che se ne va e non torna**. «La stanza delle correnti ferme»: *aveva deciso di partire davvero*. Il modello aveva letto la nota come **materia prima**.

Un genitore che scrive quella frase sta chiedendo l'opposto, e un sistema che risponde a un lutto con una storia di partenze è peggio di uno che la nota l'avesse ignorata. Riformulare non bastava: bisognava vietare. La riga adesso dice che cosa farne — cambia quanto chiede il pomeriggio e quanto dura — e che cosa non farne mai: *non è il soggetto, non gli sta vicino, non ne è una figura, non vi si allude*.

Rimisurato, tre chiamate: «L'angolo che Lia non volle riempire» e «La macchia della Sala Obliqua». Nessuna partenza, nessuna assenza. Sono su una scelta a proposito di spazio e di luce.

C'è una garanzia su quelle parole, `test_what_is_hard_in_a_house_never_becomes_what_an_afternoon_is_about`, con dentro la data e che cosa era tornato.

### 17.3 Quello che non è stato fatto, e perché

Erano tre le strade. Questa è la prima.

**B — il genitore scrive, il sistema traduce, lui rilegge cosa parte.** Piena flessibilità, nessuno schema da indovinare, e soprattutto niente di silenzioso. Non fatta perché sarebbe **la seconda cosa che chiama un modello al clic di un genitore**, e `.github/copilot-instructions.md` dice «l'unica». Vale la pena notare che quella regola motiva sé stessa elencando le proprietà che rendono accettabile `draft.py` — entro il limite mensile, non raggiunge nessuna stanza, va approvato, aspetta che sia la casa a chiedere — e che B le ha tutte e quattro. È fuori dalla lettera, non dalla sostanza. Decisione del committente, non mia.

**C — governare dai pomeriggi invece che da una pagina.** «Ancora così», «meno di questo». È la più intuitiva delle tre ed è quello che le regole chiedono al sistema di saper fare. Si compone con questa: A dà il punto di partenza, C la correzione nel tempo. Non fatta perché è la più grossa e perché A ne è comunque il presupposto.

Resta aperto il tasso di rifiuto del formato: **quattro chiamate grezze su nove** rifiutate in questo giro, quasi tutte per la via d'uscita che non nomina niente in mano alla persona. In produzione si riparano, ma è la stessa regola che sfora ogni volta, e una regola che sfora sempre è una regola scritta male.
