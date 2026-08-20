# Ideas for Lanternina

Project notes, not decisions. Every entry says four things: **what it is**, **why**,
**how it would be done**, **what it costs**. If one of those is missing, the idea is not
ready to be discussed yet.

Entries written from 18 August 2026 carry two more lines, so that any one of them can be
picked up on its own, in a session that starts from nothing: **where it starts**, the files
involved, and **done when**, a check somebody else can run. Older entries do not have them
yet, and gain them when they are next touched.

The order inside each file runs from most useful to least, by one criterion only: how much
the thing helps the person who will use it — the adolescent or the parent — divided by how
much work it asks for. It is not a ranking by elegance. Entries added later are appended and ranked
among themselves; no file has been re-ranked as a whole since.

## The files

| File | What it covers |
| --- | --- |
| [01-panel.md](01-panel.md) | The parent's panel |
| [02-display.md](02-display.md) | The two e-paper displays |
| [03-paper.md](03-paper.md) | What gets printed |
| [04-system.md](04-system.md) | Infrastructure, costs, things to close |
| [05-routines.md](05-routines.md) | Routines, and activities that are easy to start |
| [06-capture.md](06-capture.md) | The capture station, and what it is made of |
| [07-catalogue.md](07-catalogue.md) | Experiences designed once, for every house |

## Where to start

The order inside each file answers "which of these is worth most for the work". This table
answers a different question, and is ranked by a different rule: **what does the rest stand
on, and what is currently dangerous**. A thing that unblocks four others comes before a
thing that is merely useful, even when the useful one is cheaper.

The two are allowed to disagree. When they do, this table wins for choosing what to do next,
and the file wins for judging whether the thing is worth doing at all.

### First: the two that are dangerous today

| # | What | Where | Why here |
| --- | --- | --- | --- |
| 1 | ~~Close the drift between the templates and what is running~~ — **done, 18 August 2026** | 04 §3 | It was worse than recorded: the script passed no image, no port and no sign-in settings, so a plain run would have left the panel answering 404 and then 503. `deploy.ps1` now re-applies what is running and refuses without the device key. |
| 2 | Rebuild the hub from a blank card, once | 04 §5 | Still never restored, but no longer only a hope: on 18 August the keys were compared, the archive was read end to end, and the nine files a hub cannot start without were extracted and matched against the live ones, owner and mode included. Three of the four gaps found are closed. What is left needs a second card. |

### Then: the foundations

| # | What | Where | Why here |
| --- | --- | --- | --- |
| 3 | ~~Household settings, replacing the invented profile~~ — **done, 18 August 2026** | 01 §5 | The parent writes interests, things to avoid, difficulty, variety, words per line and the content language in the panel; the hub reads them on its next run. The settings hold exactly the fields `prompt_hints()` lets out, so a name has no field to sit in. |
| 4 | ~~Field names that are not Italian~~ — **done, 18 August 2026** | 04 §7 | The keys are English, and the content language is free to become what it was meant to be, a setting. Bodies approved before the change keep the Italian keys: the safety seal covers them byte for byte, so the readers accept both spellings and nothing stored was touched. |
| 5 | ~~The request channel, panel → hub~~ — **done, 20 August 2026** | 01 §7 | "Put this picture back" is its first user, and the shape it fixed is the one every later request copies: the parent presses, one row is written, and the hub finds it when it next asks. `panel/requests.py` holds the contract, `devices/pull_picture.py` the side that acts. |
| 6 | ~~The layout agent: exercise → sheet~~ — **done, 19 August 2026** | 03 §1 | An approved exercise becomes a printable sheet and comes out of the printer. |
| 7 | ~~Reading the sheet back~~ — **done, 19 August 2026** | 06 | The loop closes on real paper: a press on KEY3 scans the glass, finds the markers, decodes the code, and the display says what came back. `vision/read_sheet.py` holds the reading. |
| 8 | ~~A mark by hand reads as an empty box~~ — **closed, 19 August 2026** | 06 §0 | Both exit conditions were taken on one sheet. Four ticked boxes were reported empty, with certainty, in front of somebody; the thresholds moved to 0.010/0.003 and the same page then read correctly. Then the reader changed altogether: a vision model reads the page and the arithmetic is what the house says when the cloud is unreachable. |
| 9 | ~~Answer the press immediately~~ — **done, 19 August 2026** | 02 §4 | Measured with a finger on both units: the waiting screen lands in the response the press caused, and the reading follows in 35 s and 36 s, of which 26 s and 27 s are the scanner. Before the change the same chain took 65 s and 71 s. There is no longer a reason to hold the button down. |
| 10 | ~~Take the destructive presses out of the firmware~~ — **done, 19 August 2026** | 02 §5 | Both units flashed. Ten seconds of holding — twice the five at which the stock firmware wipes the Wi-Fi — leaves the display on the network, and the press starts a scan instead. |
| 11 | The capture station | 06 §1 | For what a flatbed cannot take: a model, a drawing too big for the glass. Not on the paper loop's critical path any more. |

### Then: what stands on them

| # | What | Where | Needs |
| --- | --- | --- | --- |
| 12 | How much approved content is left | 01 §6 | nothing — a count on routes that exist |
| 13 | Withdrawing an approval | 01 §3 | nothing — `withdraw` already exists in the ledger |
| 14 | Reminders at times the parent chose | 05 §1 | 3 |
| 15 | **Everything in the house, with a job and a name** | 01 §9, 02 §6 | nothing — and it is now blocking: one press on 19 August turned the picture display into the sheet display for good |
| 16 | One step at a time | 05 §2 | 11, and the second display in the house |
| 17 | The sheet that asks instead of assigning | 03 §3 | 6, 7 |
| 18 | "Another like this" and "something different" | 03 §5 | 6, 7 |
| 19 | A routine that shows how much is left | 05 §3 | 10 |
| 20 | Routine cards on paper | 05 §4, 03 §2 | 10 |
| 21 | Refusing with a reason | 01 §4 | 3 |
| 22 | Learning a new routine | 05 §5 | 10 |
| 23 | Offering approved content again, later | 05 §6 | 6 |
| 24 | Printing in batches | 03 §4 | 6 |
| 25 | ~~The vocabulary of capabilities, and the shape of a blueprint~~ — **done, 19 August 2026** | 07 §1 | Two hand-written experiences ran on the Epson and the FB9F18 display. A blueprint is a flat sequence over five verbs, one frozen dataclass each, so there is no expression to evaluate and an administrator who reads one has read all of it. It also found the reading defect that closed 8. |

### Last: hygiene, and things we do not know yet

| # | What | Where | Why last |
| --- | --- | --- | --- |
| 26 | A browser check for the panel | 04 §8 | Protects work already done rather than enabling new work — but move it up the day the panel breaks again. |
| 27 | ~~The text path's consumption~~ — **closed, 20 August 2026** | 04 §9 | The cap measured half the system and said so under a name that fitted the other half. `/api/usage` now reports the two kinds apart as well as together, and the cap is `monthly_call_cap`. The probe that checked it found the chat path had never reported its tokens at all. |
| 28 | ~~Retiring the diagnostics block~~ — **done, 18 August 2026** | 01 §8 | Removed with the rewrite of the panel as a React application. The claims, the raw `/api/me` body, the HTTP status in a refusal and MSAL's error code are all gone from what a parent sees. |
| 29 | Calibrating the battery | 02 §3 | One night of passive work turns an estimate into a measurement. |
| 30 | What an hourly picture costs | 04 §4 | Needed before raising the cadence, not before anything else. |
| 31 | The freshness mark | 02 §2 | Waiting on a decision that is the parent's, not a technical one. |
| 32 | Reading aloud | 05 §7 | Genuinely useful, and the only entry that touches a decision left open on purpose. |
| 33 | ~~app.lanternina.com returning 404~~ — **closed, 19 August 2026** | 04 §6 | It closed itself. 40 requests all answered 200, and the ingress that used to be deterministically 404 answered 200 six times out of six. Nothing was changed to achieve it. |

## What is already true

Because an idea is judged against what exists, not against nothing:

- The parent signs in to the panel, sees the proposals, approves or refuses. The decisions
  live in Cosmos and survive a restart.
- The panel is a React application built with Vite and published to the Static Web App by a
  workflow. Its words are two JSON catalogs; the identity library comes from npm, so the
  page loads scripts from its own origin and nothing else.
- The parent writes the picture themes. The home server asks the panel for them.
- The cloud paints when the house asks. The house holds no Azure credential.
- Every picture shown ends up in a storage account and can be restored byte for byte.
- Below 20% and below 10% charge the display shows two different images, generated in
  advance, and sleeps for longer.
- Generated text passes through Content Safety; so do the images, through image analysis.
- The panel shows the state of each display: charge, signal, when it was last heard from.
- A timer on the hub asks for a new picture once a minute, installs one when the spacing
  the parent chose has passed, and asks for nothing inside the pause.
- The pause and the spacing between pictures are chosen by the parent in the panel, in
  minutes. The hub reads them on its next run and decides for itself; saving them starts
  nothing.
- Interests, things to avoid, difficulty, variety, words per line and the content language
  are the parent's too, and travel the same way. The adolescent's name is not among them: it
  stays on the hub, and the panel has no field for it.
- Every model call is counted per household, with the tokens, the cache reads and the
  provider's request id, apart by kind as well as together, and a monthly cap refuses calmly
  once it is reached.
- A press on the display is answered in the request it caused: the screen says the sheet is
  being read, and the reading comes back about twenty-six seconds later instead of at the
  next ordinary poll.

## What is not true, and is worth remembering

- The battery percentage is **derived from volts**: the kit has no fuel gauge. It is an
  estimate from a standard LiPo curve, not measured on this cell.
- Picture approval is **per theme**, not per image: the pictures on the display have not
  been seen by an adult first.
- The name and the id live only on the hub, in the environment it reads at start. The
  invented profile is left in `tools/generate_batch.py`, which generates without a panel.
- The approval ledger in the cloud does not mint the delivery seal: that stays on the
  device. Losing the database costs the memory of the decisions, not the safety.
- The approval seal is minted and checked inside one process run, so `approval_key` can be
  replaced with a fresh random value at no cost. The safety seal is the one that outlives a
  process: `safety_key` is what already-screened content depends on.
- Reading a page is the one model call still counted nowhere. The picture path and the
  wording path both report what they consumed; the sheet reader does not, so the cap cannot
  see it and the parent is not told it happened.

## The timer

`timer.json` records when the working session started and every time it resumed. It exists
so that time can be reported as **measured** rather than estimated. It is not a stopwatch
that runs by itself: it moves only when the session resumes.
