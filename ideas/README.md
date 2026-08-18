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
