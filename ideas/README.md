# Ideas for Lanternina

Project notes, not decisions. Every entry says four things: **what it is**, **why**,
**how it would be done**, **what it costs**. If one of those is missing, the idea is not
ready to be discussed yet.

Entries written from 18 August 2026 carry two more lines, so that any one of them can be
picked up on its own, in a session that starts from nothing: **where it starts**, the files
involved, and **done when**, a check somebody else can run. Older entries do not have them
yet, and gain them when they are next touched.

The order inside each file runs from most useful to least, by one criterion only: how much
the thing helps the person who will use it — her or the parent — divided by how much work
it asks for. It is not a ranking by elegance. Entries added later are appended and ranked
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
| 2 | Rebuild the hub from a blank card, once | 04 §5 | The backup has never been restored, so it is a hope rather than a backup. Less dire than first written: the keys also exist in `secrets.local.yaml`, and the device key there is verified to be the live one. Start by checking whether the other two match the hub's. |

### Then: the foundations

| # | What | Where | Why here |
| --- | --- | --- | --- |
| 3 | Household settings, replacing the invented profile | 01 §5 | Routines, content language, difficulty and tone all need somewhere to live. Four later entries are blocked on this one. |
| 4 | Field names that are not Italian | 04 §7 | Cheapest now and dearer every week: the language is baked into the data, and every new piece of content code inherits it. |
| 5 | The request channel, panel → hub | 01 §7 | "Put this picture back" is its first user, but the pattern — the parent records, the house collects and decides — is what every later request needs. |
| 6 | The layout agent: exercise → sheet | 03 §1 | The missing half of the paper loop. Two entries that give her the initiative cannot exist without it. |
| 7 | The capture station | 06 | Reading a sheet back. `vision/` is empty; the contracts are written and nothing produces a frame. |

### Then: what stands on them

| # | What | Where | Needs |
| --- | --- | --- | --- |
| 8 | How much approved content is left | 01 §6 | nothing — a count on routes that exist |
| 9 | Withdrawing an approval | 01 §3 | nothing — `withdraw` already exists in the ledger |
| 10 | Reminders at times the parent chose | 05 §1 | 3 |
| 11 | A role per display | 02 §4 | nothing — one field |
| 12 | One step at a time | 05 §2 | 11, and the second display in the house |
| 13 | The sheet that asks instead of assigning | 03 §3 | 6, 7 |
| 14 | "Another like this" and "something different" | 03 §5 | 6, 7 |
| 15 | A routine that shows how much is left | 05 §3 | 10 |
| 16 | Routine cards on paper | 05 §4, 03 §2 | 10 |
| 17 | Refusing with a reason | 01 §4 | 3 |
| 18 | Learning a new routine | 05 §5 | 10 |
| 19 | Offering approved content again, later | 05 §6 | 6 |
| 20 | Printing in batches | 03 §4 | 6 |

### Last: hygiene, and things we do not know yet

| # | What | Where | Why last |
| --- | --- | --- | --- |
| 21 | A browser check for the panel | 04 §8 | Protects work already done rather than enabling new work — but move it up the day the panel breaks again. |
| 22 | The text path's consumption | 04 §9 | The cap measures half the system. Nobody is near the cap yet. |
| 23 | Retiring the diagnostics block | 01 §8 | Must happen before anyone outside this project uses the panel. |
| 24 | Calibrating the battery | 02 §3 | One night of passive work turns an estimate into a measurement. |
| 25 | What an hourly picture costs | 04 §4 | Needed before raising the cadence, not before anything else. |
| 26 | The freshness mark | 02 §2 | Waiting on a decision that is the parent's, not a technical one. |
| 27 | Reading aloud | 05 §7 | Genuinely useful, and the only entry that touches a decision left open on purpose. |
| 28 | app.lanternina.com returning 404 | 04 §6 | Measure again first; it may have closed itself. |

## What is already true

Because an idea is judged against what exists, not against nothing:

- The parent signs in to the panel, sees the proposals, approves or refuses. The decisions
  live in Cosmos and survive a restart.
- The parent writes the picture themes. The home server asks the panel for them.
- The cloud paints when the house asks. The house holds no Azure credential.
- Every picture shown ends up in a storage account and can be restored byte for byte.
- Below 20% and below 10% charge the display shows two different images, generated in
  advance, and sleeps for longer.
- Generated text passes through Content Safety; so do the images, through image analysis.
- The panel shows the state of each display: charge, signal, when it was last heard from.
- A timer on the hub asks for a new picture every hour and installs it, quiet hours aside.
- The quiet window and the spacing between pictures are chosen by the parent in the panel.
  The hub reads them on its next run and decides for itself; saving them starts nothing.
- Every model call is counted per household, with the tokens, the cache reads and the
  provider's request id, and a monthly cap refuses calmly once it is reached.

## What is not true, and is worth remembering

- The battery percentage is **derived from volts**: the kit has no fuel gauge. It is an
  estimate from a standard LiPo curve, not measured on this cell.
- Picture approval is **per theme**, not per image: she sees pictures no adult has seen
  before.
- Her profile is invented and lives in the code (`DEMO_PROFILE`).
- The approval ledger in the cloud does not mint the delivery seal: that stays on the
  device. Losing the database costs the memory of the decisions, not the safety.
- Only the image path reports what it consumed. The text path is not instrumented.

## The timer

`timer.json` records when the working session started and every time it resumed. It exists
so that time can be reported as **measured** rather than estimated. It is not a stopwatch
that runs by itself: it moves only when the session resumes.
