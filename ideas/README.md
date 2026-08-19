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
| 5 | The request channel, panel → hub | 01 §7 | "Put this picture back" is its first user, but the pattern — the parent records, the house collects and decides — is what every later request needs. |
| 6 | ~~The layout agent: exercise → sheet~~ — **done, 19 August 2026** | 03 §1 | An approved exercise becomes a printable sheet and comes out of the printer. |
| 7 | ~~Reading the sheet back~~ — **done, 19 August 2026** | 06 | The loop closes on real paper: a press on KEY3 scans the glass, finds the markers, decodes the code, and the display says what came back. `vision/read_sheet.py` holds the reading. |
| 8 | **A mark by hand reads as an empty box** | 06 §0 | Measured, not suspected: an ordinary tick reads 0.0121 and a cross 0.0196, both under the 0.02 that separates empty from doubtful. So a real answer is reported as no answer — the one failure a person cannot see, because an unread answer looks like an unanswered question. |
| 9 | Answer the press immediately | 02 §4 | The reason somebody holds the button down, and holding is what wipes the Wi-Fi credentials. It goes before the firmware change, not after. |
| 10 | Take the destructive presses out of the firmware | 02 §5 | Five seconds of holding wipes the Wi-Fi, fifteen the credentials. Needs a rebuild and a reflash of both units, so it waits until the loop is running — which it now is. |
| 11 | The capture station | 06 §1 | For what a flatbed cannot take: a model, a drawing too big for the glass. Not on the paper loop's critical path any more. |

### Then: what stands on them

| # | What | Where | Needs |
| --- | --- | --- | --- |
| 12 | How much approved content is left | 01 §6 | nothing — a count on routes that exist |
| 13 | Withdrawing an approval | 01 §3 | nothing — `withdraw` already exists in the ledger |
| 14 | Reminders at times the parent chose | 05 §1 | 3 |
| 15 | A role per display | 02 §6 | nothing — one field |
| 16 | One step at a time | 05 §2 | 11, and the second display in the house |
| 17 | The sheet that asks instead of assigning | 03 §3 | 6, 7 |
| 18 | "Another like this" and "something different" | 03 §5 | 6, 7 |
| 19 | A routine that shows how much is left | 05 §3 | 10 |
| 20 | Routine cards on paper | 05 §4, 03 §2 | 10 |
| 21 | Refusing with a reason | 01 §4 | 3 |
| 22 | Learning a new routine | 05 §5 | 10 |
| 23 | Offering approved content again, later | 05 §6 | 6 |
| 24 | Printing in batches | 03 §4 | 6 |

### Last: hygiene, and things we do not know yet

| # | What | Where | Why last |
| --- | --- | --- | --- |
| 25 | A browser check for the panel | 04 §8 | Protects work already done rather than enabling new work — but move it up the day the panel breaks again. |
| 26 | The text path's consumption | 04 §9 | The cap measures half the system. Nobody is near the cap yet. |
| 27 | ~~Retiring the diagnostics block~~ — **done, 18 August 2026** | 01 §8 | Removed with the rewrite of the panel as a React application. The claims, the raw `/api/me` body, the HTTP status in a refusal and MSAL's error code are all gone from what a parent sees. |
| 28 | Calibrating the battery | 02 §3 | One night of passive work turns an estimate into a measurement. |
| 29 | What an hourly picture costs | 04 §4 | Needed before raising the cadence, not before anything else. |
| 30 | The freshness mark | 02 §2 | Waiting on a decision that is the parent's, not a technical one. |
| 31 | Reading aloud | 05 §7 | Genuinely useful, and the only entry that touches a decision left open on purpose. |
| 32 | app.lanternina.com returning 404 | 04 §6 | Measure again first; it may have closed itself. |

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
  provider's request id, and a monthly cap refuses calmly once it is reached.

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
- Only the image path reports what it consumed. The text path is not instrumented.

## The timer

`timer.json` records when the working session started and every time it resumed. It exists
so that time can be reported as **measured** rather than estimated. It is not a stopwatch
that runs by itself: it moves only when the session resumes.
