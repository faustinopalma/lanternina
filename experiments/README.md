# Experiments

Runs of a whole afternoon against the simulated house: the same runner, the same panel, the same models, the same printing and the same reading, with the equipment replaced by files and the person replaced by an image model that fills the page in.

```bash
LANTERNINA_PRETEND=1 python -m tools.experiment run "what I am trying" --by teenager --times 3
```

One folder per experiment, numbered so they read in order. Inside each, `flow/` holds the whole afternoon in sequence — every screen the display showed, every page as it was handed over, every page as it came back — and `notes.md` holds what was measured and what somebody thought of it.

**Nothing here is deleted, including the runs that went badly.** A run that failed is the only evidence of how it failed, and this project has more than once been saved by looking at one.

**The pixels are not committed and the notes are.** A page is roughly a megabyte and a soak is dozens of them; what is worth having in six months is the measurement and the judgement, not the file. Nothing in a run is about a real person — the afternoons are invented and the handwriting is a model's — so this is a decision about size, not about privacy.

## What to look for

- **The pages, one after another.** Whether they look like objects somebody would pick up, and whether two runs of the same afternoon produced two different-looking pages.
- **What the hand wrote.** The reading is a model looking at handwriting, and it is only exercised honestly if the handwriting is real handwriting.
- **The screens.** Whether the words read as somebody who is also interested, and never as a teacher.
- **The ink.** Under `## Ink` in the notes, as a share of the sheet. A home inkjet is the constraint the whole page format is shaped by.
