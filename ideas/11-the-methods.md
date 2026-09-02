# 11. The methods: a child of the encyclopedia, for devising

Written 2 September 2026, the day the 395-entry compilation in [enciclopedia/](../enciclopedia/README.md) was made public and stopped growing. Nothing here is decided. It exists so that the next session starts from a written argument rather than from a chat window.

The numbers below come from `python tools/enciclopedia_censimento.py`, which can be run again.

---

## 1. What it is

A second artefact, generated once from the encyclopedia and then living on its own: one small record per **method that can actually be run here**, holding what a generator needs and nothing else — the movable parts, what it costs, where the verification sits, what comes back, and which forms it goes with.

It is a child, not a view. Not one record per entry, no obligation to keep the count, no obligation to keep the shape. The encyclopedia becomes a dated witness of what was known on 2 September 2026 and is not maintained further.

## 2. Why the encyclopedia cannot do this job itself

**It reaches nothing today.** `the_prompt` in `agents/experience_deviser.py` takes sixteen arguments — language, capabilities, interests, things to avoid, ground covered, how the last runs went, shape, distance, the parent's note. None of them is a form. The research feeds no generation at all.

**It does not fit.** The rendered prompt is 25 330 bytes (`docs/prompts/deviser.txt`); the encyclopedia is 5 324 kB. Even the flat list in `docs/EXERCISE-FORMS.md` is 37 068 bytes, larger than the whole prompt. Some intermediate artefact is not a preference, it is arithmetic.

**Most of it is scholarship.** Measured over the seven sections: «Che cosa se ne sa» is 22.4% of the text and «Da dove viene» 15.1%. Nearly 38% is provenance, dates and history — the part that makes it an encyclopedia rather than a memory, and dead weight in a prompt. What a generator needs is the 11.8% under «Che cos'è» and the 21.2% under «Un esempio giocabile».

## 3. Why not a search over it

The first shape proposed was an index the model searches at devise time. Three arguments against, in order of weight.

**Similarity works against the machinery already built.** `agents/experience_deviser.ground-covered.md` splits covered ground into three bands — *justUsed* closed, *usedLately* to be kept away from, *usedBefore* only as another visit — and `DISTANCES["frequent"]` says «go somewhere else: another place, another century, another kind of object». A search keyed on a household's interests returns the same neighbourhood every time. It would be a machine for making ruts standing next to a machine built to avoid them.

**The records are small enough that no search is needed.** A record fits in about 300 characters. Twenty of them are 6 kB, which sits beside a 25 kB prompt without argument. Selection can be done in code — filter to what this house can run, drop what is on closed ground, spread across chapters — which is deterministic, reproducible, and testable. A test can assert *an afternoon is never offered a form this house cannot run*; no test can assert that of a similarity search.

**Retrieval earns its place in one branch only.** When a parent has written an idea in `panel/drafts.py`, there is a real query in their own words, and matching a brief to methods is a genuine retrieval problem. That is the case to keep it for.

## 4. The cut is not chapter-shaped

The intuition was that whole chapters could be dropped. Measured against what the entries declare about themselves, that is true once.

| declared reason | entries | where |
| --- | --- | --- |
| the wall: a model cannot manipulate letters inside words | **58** | 27 in ch. 12, 19 in ch. 5, 7 in ch. 7 |
| needs a second person | **74** | spread across all fourteen |
| says where it would break | 169 | everywhere |

Chapter 12, classical Italian word puzzles, is the one that mostly dies: **27 entries of 48**, 56%, rest on an operation the entries themselves say does not work. Chapter 5 has 83 entries and 19 fall to the same wall, so **64 survive**. Cutting by chapter throws those 64 away and keeps the 21 of chapter 12 without looking at them.

The one genuinely chapter-shaped cut is **3, on what the request arrives on**: ten entries that are a taxonomy of supports — sheet, display, voice, video, body, time — rather than techniques to use. It leaves whole, and not because it fails: because it is of another kind. Its content becomes the schema of properties, not records.

**«Needs a second person» is a property, not a sentence.** Seventy-four entries. A house with two people runs them. Deleting them decides for every house; recording them lets the situation decide. Of the reasons found, one is a cut and the rest are labels.

## 5. The score: properties, not a verdict

The instinct is right — without weights, uniform sampling over a couple of hundred forms produces the oddity as often as the workhorse. A single number saying *how good this method is* has three faults that do not repair.

**There is no goodness outside the situation.** A form that is right for `stretch` is wrong for `gentle`. A scalar freezes a judgement about a context that is not present when the judgement is made.

**It has no provenance.** `.github/copilot-instructions.md` §2 asks for numbers with their provenance — measured, computed or estimated. A 4-out-of-5 assigned by whoever writes the record is a superlative in numeric costume, which is the thing the encyclopedia has just finished taking off.

**Used greedily it makes ruts.** Always taking the high scores is what the three bands and `DISTANCES` exist to prevent. It would be the third machine, fighting the first two.

Instead, a few declared properties, each decidable and checkable, weighted per request by the selector:

- **cost to the adult** — none · prepare beforehand · take part
- **where the verification sits** — in the sheet · needs a person · nowhere (the *control of error* axis the encyclopedia found running across chapters)
- **what comes back** — nothing · a sheet · a photograph
- **how many moments it needs at minimum** — one · two times · many
- **how many people** — one · two

With these, "favouring a method" stops being an opinion and becomes a question: *tonight the adult cannot prepare anything and the verification has to sit in the sheet* — and twenty forms remain instead of two hundred. The situation decides rather than the compiler, and a test can assert it.

**The only honest scalar is the earned one.** Every form starts at zero. `panel/what_happened.py` already records how afternoons went; if a record accumulates *offered N times, reached the end M*, that is a number with a real denominator. A score assigned before anything was tried is a preference; a count kept afterwards is a measurement.

## 6. The line, worth seeing before it is crossed

A **global** score — this form reached the end 12 times out of 30, across all houses — is a measurement about a method.

A **per-house** score — *this house prefers crosswords* — is a model of a person. The deviser's own docstring states it as a fact of type rather than a caution: *«There is nothing about a person in it: no name, no profile, no learner, and no record of what anybody did. That is not caution here, it is the type — an experience has no field that could hold one.»* `docs/NON-GOALS.md` and the product notes say the same. There is nowhere to put it today, and a per-house score would be the first thing to open somewhere — arriving sideways, as a side effect of an optimisation.

Covered ground already does the useful work expected of a per-house score. It says what not to offer again, **and it asserts nothing about anybody**.

## 7. What is already there and does not need inventing

**A graph.** 2 448 distinct «voce N, nome» edges, 6.2 per entry, only 7 entries never cited by another. Written by hand, one at a time. An afternoon is a sequence of moments; which forms sit well one after another is exactly what those edges answer. They extract with no judgement and no agent.

**The movable parts.** 1 803 of them, 4.6 per entry, 31 entries with none listed. That is the generative material: the parameters that make one form produce many afternoons.

## 8. What it costs

A second artefact to keep honest. The mechanical half regenerates; the judgement half does not, so a drift check must **flag** rather than silently rebuild. With the encyclopedia frozen, drift is mostly one-way and this is cheaper than it would have been a week ago.

**The link back has to survive.** The moment it stops being one-to-one, the child cannot be checked against the parent by machine. Each record should name the entry or entries it came from — many-to-one allowed, zero allowed when it is new. It regenerates nothing; it answers, in a year, the question *did this line come from research or did somebody invent it*. Without it the child becomes indistinguishable from a list of opinions.

**The real cost is that this is the review.** `docs/NON-GOALS.md` says the design rules were taken out rather than patched, and will come from this research, form by form, with the reasoning attached. Deciding which methods survive **is** that review. Doing it inside a data file means taking the decisions one field at a time without writing why. That is not a reason to avoid it; it is a reason to do it as the review, with the reasoning here, and the artefact as its product.

## 9. Where it starts

`enciclopedia/`, frozen. `tools/enciclopedia_censimento.py` for the numbers. `agents/experience_deviser.py` and `shared/experience_checks.py` for what the output has to survive: four acts (`say`, `hand_over`, `collect`, `close`), four capabilities (`print_a4`, `scan_a4`, `photograph_table`, `show_800x480_1bit`), at most 12 moments.

## 10. Done when

An afternoon devised with the methods in the prompt is read side by side with one devised without, ten of each, by somebody who does not know which is which. If the difference cannot be seen, the artefact has not earned its place, however good the schema is.

## 11. Open questions — decide these before writing anything

**Where does it live, and in what form?** Not inside `enciclopedia/`, which is prose for people. `catalogue/` is blueprints the software executes and is a different thing. One file or one per record; JSON that a program reads or Markdown that a person also reads.

**Who decides what survives, and against what written criterion?** «It does not work» has to be stated as a test, not as a feeling. The 58 of the letter wall are decidable. The rest are not, yet.

**How many make it across?** 395 minus 58, minus chapter 3's ten, minus whatever the review removes. Nobody has counted the union. The answer is somewhere under 300 and the shape of the work depends on whether it is 120 or 250.

**Does the selector go in the deviser or beside it?** Putting it in `the_prompt` makes a seventeenth argument. Putting it beside makes a second thing to keep in step.

**What does a form do to the ten dimensions?** `Experience.drawn` already carries ten axes along which an afternoon was conceived, and `ideas/10-the-page.md` §2 says none of them reaches the page. A method chosen from this artefact and a dimension already drawn could easily contradict each other, and nothing currently notices.
