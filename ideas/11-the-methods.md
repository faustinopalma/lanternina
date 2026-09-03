# 11. The methods: a child of the encyclopedia, for devising

Written 2 September 2026, the day the 395-entry compilation in [enciclopedia/](../enciclopedia/README.md) was made public and stopped growing. Nothing here is decided. It exists so that the next session starts from a written argument rather than from a chat window.

The numbers below come from `python tools/enciclopedia_censimento.py`, which can be run again.

**Reviewed the same evening, and three of its arguments did not survive.** They are corrected in place, with the correction said out loud rather than smoothed over: the ruts argument in §3, the 169 in §4's table, and the word *weighted* in §5. The conclusions mostly stand; two of the three reasons given for them were wrong.

**Corrected again on 3 September, and this one was mine.** That review concluded the artefact's job was to be a closed vocabulary for `drawn.mechanic`, so that a check which never fires would fire. It reached that conclusion because the defect was measurable and the purpose was not, which is the same failure it had just accused the first draft of one level up. The encyclopedia's own statement of purpose says what it is for: *chi deve proporre qualcosa da fare — un genitore, un insegnante, chi scrive un gioco — ne conosce una decina e usa sempre quelle. Qui ce ne sono 395,* and each entry is *la forma descritta in modo che si possa costruire*. That is a manual, and a list of names is not one. §1 leads with the manual again. The vocabulary survives as a by-product: every record has a `name`, and the name is what makes two afternoons comparable.

**And then it was built.** [methods/](../methods/README.md) holds 204 records written on 3 September 2026 from 323 of the 395 entries. What that cost and what it found is §12.

---

## 1. What it is

A second artefact, generated once from the encyclopedia and then living on its own: one small record per **method that can actually be run here**, holding what somebody needs in order to build one — how it is made, which parts of it move and what happens when they are moved, where the part that does the work sits, where it breaks on paper, and what it costs.

It is a child, not a view. Not one record per entry, no obligation to keep the count, no obligation to keep the shape. The encyclopedia becomes a dated witness of what was known on 2 September 2026 and is not maintained further.

**The by-product, which is worth having and is not the point.** `shared/experience.DIMENSIONS` already has a `mechanic` — *what they actually do* — and `shared/experience_checks.not_the_same_afternoon_again` already refuses an afternoon that shares more than two of the four decision dimensions with a recent one: mechanic, progress, tone, ending. The comparison is `shared_dimensions`, which folds with `_folded`, which is `" ".join(text.lower().split())`. Exact string equality on a free phrase of at most 60 characters, written each time by a model.

Measured 2 September 2026, by constructing two `Drawn` and calling the check: two afternoons that are the same crossword, in the same kitchen, with the same role, the same tone and the same ending — worded as one model would word them twice — produce **zero complaints**. The check whose docstring explains so carefully why two of the ten may recur and four may not is, on the four that may not, comparing snowflakes. It fires on nothing.

A record's `name` is at most 60 characters and is unique across the corpus, enforced by `tools/methods_check.py`. Two afternoons built from the same record can be written into the same name, and the check starts working. That is a real repair and it costs nothing extra, because a manual needs names anyway.

**The cost of it, said next to the claim.** Making `mechanic` a label picked from a list rather than a phrase written afterwards changes the type of a field on a load-bearing contract, and `Drawn`'s docstring calls the ten *one short phrase each*. Handing a model a label before it devises risks an afternoon built around the label rather than around the afternoon. Nothing has been changed in `shared/` and that decision is still open.

## 2. Why the encyclopedia cannot do this job itself

**It reaches nothing today.** `the_prompt` in `agents/experience_deviser.py` takes sixteen arguments — language, capabilities, interests, things to avoid, ground covered, how the last runs went, shape, distance, the parent's note. None of them is a form. The research feeds no generation at all.

**It does not fit.** The rendered prompt is 25 330 bytes (`docs/prompts/deviser.txt`); the encyclopedia is 5 324 kB. Even the flat list in `docs/EXERCISE-FORMS.md` is 37 068 bytes, larger than the whole prompt. Some intermediate artefact is not a preference, it is arithmetic.

**Most of it is scholarship.** Measured over the seven sections: «Che cosa se ne sa» is 22.4% of the text and «Da dove viene» 15.1%. Nearly 38% is provenance, dates and history — the part that makes it an encyclopedia rather than a memory, and dead weight in a prompt. What a generator needs is the 11.8% under «Che cos'è» and the 21.2% under «Un esempio giocabile».

## 3. Why not a search over it

The first shape proposed was an index the model searches at devise time. The conclusion — not at devise time — stands. The first reason given for it was wrong and is withdrawn.

**Withdrawn: «similarity would make ruts».** The draft argued that a search keyed on a household's interests returns the same neighbourhood every time, and would fight the three bands in `agents/experience_deviser.ground-covered.md`. It does not hold. Those bands are about **subjects** — the ground a house has been over is a list of what afternoons were about — and `DISTANCES["frequent"]` ends «and keep only the way it is made». The existing machinery does not merely tolerate a form recurring while the world changes; at the far end of the variety setting it asks for exactly that. Form and subject are different axes, and an argument that borrows the anti-rut machinery to rule out a search over forms has confused them.

**There is no query.** This is the argument that does hold, and it is simpler. Retrieval needs something to be similar to. At devise time the only text in hand is the parent's interests, and `agents/experience_deviser.household.md` words them as *a place to begin* — they are subject matter. Searching a corpus of forms with a query about subjects returns whatever the embedding happens to associate, which is neither a form that suits the house nor a form that suits the subject. It is not that the answers would be bad; it is that the question is not being asked.

**A neighbourhood has no name.** Given §1, this is decisive. What the artefact has to produce is a label that two afternoons can be compared on. A search returns a region of a corpus, and a region cannot be folded, written into a 60-character field, or asserted about in a test. Whatever else retrieval is good for, it cannot do the one job.

**The records are small enough that no search is needed.** A record fits in about 300 characters. Twenty of them are 6 kB, which sits beside a 25 kB prompt without argument. Selection can be done in code — filter to what this house can run, drop what is on closed ground, spread across chapters — which is deterministic, reproducible, and testable. A test can assert *an afternoon is never offered a form this house cannot run*; no test can assert that of a similarity search.

**Retrieval earns its place in one branch only.** When a parent has written an idea in `panel/drafts.py`, there is a real query in their own words, and matching a brief to methods is a genuine retrieval problem. That is the case to keep it for.

## 4. The cut is not chapter-shaped

The intuition was that whole chapters could be dropped. Measured against what the entries declare about themselves, that is true once.

| declared reason | entries | where |
| --- | --- | --- |
| the wall: a model cannot manipulate letters inside words | **58** | 27 in ch. 12, 19 in ch. 5, 7 in ch. 7 |
| needs a second person | **74** | spread across all fourteen |

**A third row was here and has been removed.** The census also reports 169 entries under «declares where it would break», and putting that number in this table invited it to be read as a count of forms that fail. It is not one. Measured 2 September 2026 by locating every match: «si romperebbe» occurs in exactly one section, «Un esempio giocabile», once per entry in 168 of the 169. It is a standing caveat paragraph about the worked example, not a verdict on the method. Six were read by hand, chosen at random with a fixed seed: three of them say the form works anyway — voce 279, «ma qui non serve: i dadi li tira chi legge»; voce 127, where the grid does not fit a display but one line of it does and «basta a sé stessa»; voce 394, where what breaks is the return path and not the form. A row that counts caveats cannot sit beside a row that counts failures.

The consequence is not only a correction. That paragraph is where the properties of §5 are already written, in prose, in 169 entries: *la verifica sta sul foglio e la fa chi scrive* is where the verification sits, *quello che torna indietro sono i numeri, non l'immagine* is what comes back, *i dadi li tira chi legge* is who pays. The child's source is that section, not the whole entry.

Chapter 12, classical Italian word puzzles, is the one that mostly dies: **27 entries of 48**, 56%, rest on an operation the entries themselves say does not work. Chapter 5 has 83 entries and 19 fall to the same wall, so **64 survive**. Cutting by chapter throws those 64 away and keeps the 21 of chapter 12 without looking at them.

The one genuinely chapter-shaped cut is **3, on what the request arrives on**: ten entries that are a taxonomy of supports — sheet, display, voice, video, body, time — rather than techniques to use. It leaves whole, and not because it fails: because it is of another kind. Its content becomes the schema of properties, not records.

**«Needs a second person» is a property, not a sentence.** Seventy-four entries. A house with two people runs them. Deleting them decides for every house; recording them lets the situation decide. Of the reasons found, one is a cut and the rest are labels.

**The union, which nobody had counted:** the letter wall and chapter 3 overlap in nothing, so 58 + 10 = 68 and **327 entries survive the two mechanical cuts**. That is a ceiling, not an estimate of the answer: everything the review removes by judgement comes off it, and — given §1 — the number that matters in the end is the count of distinct *names*, which is smaller again, because «Varianti e parenti» says many of the 327 are one another's variants.

## 5. The score: properties, not a verdict

The instinct is right — without weights, uniform sampling over a couple of hundred forms produces the oddity as often as the workhorse. A single number saying *how good this method is* has three faults that do not repair.

**There is no goodness outside the situation.** A form that is right for `stretch` is wrong for `gentle`. A scalar freezes a judgement about a context that is not present when the judgement is made.

**It has no provenance.** `.github/copilot-instructions.md` §2 asks for numbers with their provenance — measured, computed or estimated. A 4-out-of-5 assigned by whoever writes the record is a superlative in numeric costume, which is the thing the encyclopedia has just finished taking off.

**Used greedily it flattens the repertoire.** Always taking the high scores means the same twenty forms and never the other three hundred. The draft called this fighting the three bands and `DISTANCES`, and that is the same confusion §3 withdraws: those are about subjects, and `DISTANCES["frequent"]` positively asks for the form to stay while the world changes. The fault is real and it is narrower than the draft said — a scalar over forms decides once, for every house and every evening, which of them are ever seen.

Instead, a few declared properties, each decidable and checkable, used by the selector as **filters and never as weights**:

- **cost to the adult** — none · prepare beforehand · take part
- **where the verification sits** — in the sheet · needs a person · nowhere (the *control of error* axis the encyclopedia found running across chapters)
- **what comes back** — nothing · a sheet · a photograph
- **how many moments it needs at minimum** — one · two times · many
- **how many people** — one · two

**The draft said «weighted per request by the selector», and that sentence was the score coming back in.** Five properties combined with per-request weights is a scalar computed at request time; all that moved is where the judgement is written. The question «how many properties before they become a score» has the wrong shape: one property is already a score if it is weighted, and twenty are not if each is a hard predicate about whether this house can run this thing at all. The line is not a count, it is the difference between *can it be run here* and *is it any good*. Only the first belongs in the record.

**And the arithmetic the draft offered for them was invented.** It said «twenty forms remain instead of two hundred», with no provenance — the exact fault this section accuses the score of. Measured: the two properties that exist today are lopsided towards survival. 58 fall to the letter wall and 74 need a second person, they overlap in 5, and a one-person house with no letter manipulation is left with **268 of 395, 68%**. Filters of that shape do not cut two hundred to twenty. Either the remaining three properties bite far harder than these two, or selection has to do its narrowing some other way — by chapter spread, by covered ground, by what the afternoon already needs. Which of the two is true is not known, and cannot be known until the properties are written on real records.

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

**«The mechanical half» is almost empty, and this is the correction that hurts.** Measured 2 September 2026: «Che cos'è» averages 1 431 characters and «Un esempio giocabile» 2 578, so a 300-character record is a **13.4× compression** of its own source. Nothing at that ratio is extraction. Every record is written, by judgement, one at a time. What does regenerate is the citation back to the entry and the 2 448 cross-reference edges of §7 — useful, and not the record. So the cost is not «a drift check»; the cost is up to 327 acts of writing, and the drift check only guards them afterwards.

**The link back has to survive.** The moment it stops being one-to-one, the child cannot be checked against the parent by machine. Each record should name the entry or entries it came from — many-to-one allowed, zero allowed when it is new. It regenerates nothing; it answers, in a year, the question *did this line come from research or did somebody invent it*. Without it the child becomes indistinguishable from a list of opinions.

**The real cost is that this is the review.** `docs/NON-GOALS.md` says the design rules were taken out rather than patched, and will come from this research, form by form, with the reasoning attached. Deciding which methods survive **is** that review. Doing it inside a data file means taking the decisions one field at a time without writing why. That is not a reason to avoid it; it is a reason to do it as the review, with the reasoning here, and the artefact as its product.

## 9. Where it starts

`enciclopedia/`, frozen. `tools/enciclopedia_censimento.py` for the numbers. `agents/experience_deviser.py` and `shared/experience_checks.py` for what the output has to survive: four acts (`say`, `hand_over`, `collect`, `close`), four capabilities (`print_a4`, `scan_a4`, `photograph_table`, `show_800x480_1bit`), at most 12 moments.

## 10. Done when

An afternoon devised with the methods in the prompt is read side by side with one devised without, ten of each, by somebody who does not know which is which. If the difference cannot be seen, the artefact has not earned its place, however good the schema is.

**That test is second, not first.** It costs twenty devisings and a person's afternoon, and what it measures is taste. There is a cheaper one that comes before it and that §1 makes possible: **write the failing test first.** Two `Drawn` that are the same form in different words, handed to `not_the_same_afternoon_again`, must be refused. Today they are not — measured, zero complaints. The smallest vocabulary that turns that red test green is the smallest honest version of this artefact, and it can be found without a single model call.

If the vocabulary cannot be made to do that — if every candidate list is either too coarse to distinguish afternoons or too fine to be picked from — the artefact fails early and cheaply, and nobody has reviewed 395 entries to find out.

## 11. What was open, and what is decided now

Five questions were left open. Four move; the fifth turns out to have been the wrong question.

**Where does it live, and in what form? — decided by §1.** If the thing is a vocabulary that `shared_dimensions` compares and a test asserts on, it has to be read by code, so it is not Markdown. It goes in `shared/`, beside `DIMENSIONS`, and not in `catalogue/`: a blueprint is executed, a vocabulary is compared, and those are different kinds of file. Whether the prose that goes with each name lives in the same file or beside it is a smaller question and can wait.

**Who decides what survives, and against what criterion? — the criterion is now writable.** Not «does it work», which is a feeling. A form is in the vocabulary when it has **a name of at most 60 characters that two different afternoons using that form would both be written into**. A form nobody can name that way is out, however good it is — because an unnameable form cannot be compared, and comparing is the job. That is decidable per entry by one person reading it, and it is a much smaller decision than judging the method.

**How many make it across? — answered: 204, from 323 entries.** The ceiling reasoned out here was 327, and 323 of the 395 were in fact used. The collapse was smaller than expected: 112 of the 204 records come from a single entry, and only 34 from three or more. The one chapter that folded hard is 12, where nine entries naming nine letter operations became one record, because all nine give a builder the same three instructions. §12 has what else the counting found.

**Does the selector go in the deviser or beside it? — the question dissolves.** A vocabulary for `mechanic` is not a seventeenth argument to `the_prompt`. It enters where the mechanic is already spoken about, in `shared/experience_prompt.the-ten-dimensions.md`, and it is compared where comparison already happens, in `shared/experience_checks.py`. There is nothing new to keep in step. This is only true while the artefact stays a vocabulary; the moment it also carries the five properties of §5 and a selector filters on them, the question comes back, and it should be allowed to come back later rather than be answered now.

**What does a form do to the ten dimensions? — it is one of them.** The feared contradiction, between a method chosen from the artefact and a dimension already drawn, does not arise: a form is the value of `mechanic`, not an eleventh thing standing next to the ten. What replaces the question is a real one, and it is the tradeoff in §1: `mechanic` stops being a phrase the model writes about what it made and becomes a label it picks before making it. Whether an afternoon built from a label is worse than one described afterwards is not known, and it is exactly what §10's twenty afternoons would measure — which is the right order: cheap test first to find out whether the vocabulary can exist, expensive test second to find out whether it should.

**One question is new, and it is the largest.** §6 draws a line at a per-house score because it would be a model of a person. A closed vocabulary of forms draws a fainter one: covered ground already records which subjects a house has been over, and adding form names to it records which *methods* a house has been given. That is still a fact about afternoons and not about anybody — but it is one join away from *this house is given crosswords*, and the join would be easy and nobody would notice it being made. Worth writing down before the vocabulary exists, not after.

## 12. What building it found

The manual is [methods/](../methods/README.md): 204 records from 323 of the 395 entries, written 3 September 2026, one hand-written first and the rest in parallel. `tools/methods_check.py` accepts all of them. What the writing found is worth more than the count.

**The estimates in §3 and §5 of this file were wrong by about three times, in the same direction.** A record's prompt-facing half was estimated at 300 characters, then at 800; measured across 204 it is 2 316. Five records are 11.3 kB against a 25 330-byte prompt, which is 45% of it. Five was never the right number. The serving is two-tier: a long list of names, which cost about 40 characters each, and one or two records in full. This does not change the argument against retrieval — it strengthens it, because with only one or two arriving, the choice of which is nearly the whole design, and a choice that cannot be tested is worse the fewer it makes.

**Every length ceiling was set from the wrong constraint, twice.** They came from the prompt budget, which is about serving, not from what a record needs in order to teach. Across 157 records written under the first ceilings, `how` had a median of 643 against a cap of 700 and a ninetieth percentile of 697 — three characters under. The number was shaping the writing instead of catching it, which is the failure the prompt notes already record about stating a number of sheets. The ceilings now sit above the observed maximum.

**Two fields in §5 did not survive contact.** `moments` was removed: sixteen records were written and all sixteen said `one`, because nothing in the research says how long anything takes, and a field with one value is a guess in the grammar of a declaration. `needs_letters_inside_words` became four values, because a cryptarithm is solved by doing a sum and composed by searching inside words, and one boolean was wrong whichever way it was set. A fourth value was added to `verification`: `in_the_object`, for scissors, a compass, a ruler or a soap film settling it with no sheet and no person. Without it, records contradicted their own `breaks` field in the same file.

**The properties are lopsided, and §5's worry about filters was right.** 182 of 204 records cost the adult nothing, 183 work with one person, 180 need no letter work. Filtering on those removes almost nothing, exactly as the measured 268-of-395 predicted. The field that discriminates is `verification`: 93 in the sheet, 68 nowhere, 34 in the object, 9 needing a person. A house on an evening when nothing can be checked by a person has 195 to choose from, not 20. Narrowing has to come from covered ground and from spreading across chapters, not from the properties.

**The rule that made the records worth having is not in §5 at all.** A record describes the version worth building, not the family. It was found writing the third one by hand: a chain of estimates has its verification nowhere, and asking for the same quantity by two independent roads puts it inside the sheet for the cost of one line. Recording `nowhere` would have been true of the family and useless to somebody building one tonight. The encyclopedia is neutral on purpose; the manual must not be.

**Some entries are not forms, and the schema had nowhere to put them.** 68 of the 204 records are `move`: a thing applied to a form rather than a thing somebody does. A red herring, fading a sequence of sheets, asking for a prediction before the measurement. These are the most reusable records in the corpus and a schema with only forms in it would have thrown them away.

**Five records were refused on principle rather than for failing.** A run of days, a variable-ratio reward, an inactivity notice, a progress bar and a campaign across twelve afternoons all work by making it hard to stop, which the deviser's prompt refuses in as many words. One ending in chapter 11 went the same way. Writing them with the objection buried in `breaks` would have read as permission.

**And one entry was discarded that had already passed an automated check once.** Entry 289 is documentation of a product wearing the vocabulary of a form. It survived the encyclopedia's own checker at zero complaints and it survived this one too, because neither can tell. Somebody read it.

**What is thin, said plainly.** Chapter 4, how a request is packaged, has 17 of its 27 entries untaken, and chapter 7, formal constraints, has 13 of 18. Chapter 4 is the gap that matters, because it is the catalogue of wrappers and the deviser's prompt already asks for an afternoon that begins in the middle of something and has a way in that is a thing.

**Nothing reads it yet.** `the_prompt` still takes sixteen arguments and none of them is a form, `Drawn.mechanic` is still free text, and `not_the_same_afternoon_again` still fires on nothing. The manual is an artefact with no consumer, which is the state the encyclopedia was in yesterday. §10 is still the test, and it is now runnable.

## 13. The reading, in production, and which prompt wrote what

Written 3 September 2026. `agents/experience_judge.py` existed and was run by hand from `tools/judge_many.py` over folders in `experiments/`. Two things were missing and both matter for §10, which is a test that compares afternoons written under two prompts. Nothing read the afternoons a real house is actually offered, so the only material to compare was material generated for the comparison. And nothing anywhere said **which prompt wrote which afternoon**, so a change to a block could be argued about and not counted.

Three things now exist. `panel/judging.py` reads back every afternoon the panel devises, on both paths — the house asking, and a parent approving their own brief. The verdict is kept whole beside the afternoon and is filed into the trail next to the plan it judges when the house says it began, behind the parent's own login. One line per afternoon goes to the workspace: ids, a prompt fingerprint, the finding names, a latency, token counts, and no words.

**Measured in production, revision `--0000089`, 3 September 2026.** One afternoon devised for the real household in **137.9 s** and read back in **14.4 s** — 4 246 input tokens, 999 output of which 946 reasoning. No findings, and the reader could state the question the afternoon asks. The line it wrote:

```
afternoon judged {"household": "hh_9a6d6e38", "experience": "aftn-67586379",
"prompt": "d427131c594e", "canBeWrong": true, "findings": [], "contradictions": [],
"readTheQuestion": true, "degraded": false, "latencyS": 14.41, "inputTokens": 4246,
"outputTokens": 999, "reasoningTokens": 946}
```

and the query written in `panel/judging.py` returns one row: prompt `d427131c594e`, finding `none`, one afternoon. That is the whole point of the exercise working end to end — the question *how did the afternoons from this prompt go* now has an answer that is a query rather than a memory.

### The three open decisions, and what took them

**Inside the reply to the house, or after it? — after.** The ingress gives up at 240 s. Measured 3 September 2026: a devise costs **112.4–183.8 s** over ten runs, median 143.1 s, and 137.9 s in production; the reading costs **14.4 s**. Inside one reply, the slowest measured devise plus a reading leaves about 42 s of margin, which is 17% and is not comfortable — but the margin is not what decides it. What decides it is that the two failures are not worth the same. A reading that does not happen costs a row. A reply that runs out of time costs the afternoon, which was already written and already paid for. Putting a diagnostic inside the transaction it measures means a diagnostic failure can destroy the product.

What running it afterwards costs is written down rather than hidden: a replica shut down in the seconds following a reply loses a verdict, and a lost verdict is a missing row and nothing else.

**Who pays for the extra call? — the household, counted like every other, and skipped at the limit.** Two properties, and they are what make *an afternoon never fails because of its own reading* true rather than intended. Its own afternoon is safe because the reading runs after that afternoon is stored. The next one is safe because a household already at its limit is not read back at all, so the reading can never be the call that crosses.

The alternative — leaving the reading out of the figure the cap compares — was written first and then rejected with a number. A devising loop that has lost its mind is stopped at the limit; a reading outside the limit would make the real spend at that moment exactly **twice** what the limit says, because there is one reading per successful devise. A cap that a category of call can double is not a cap.

What counting it costs is small enough to state: at most one reading per devised afternoon, and `panel/usage.py` works an ordinary month out at 1 302 calls, of which devising is the rarest path. The month reaches its limit a few per cent sooner and nothing else changes.

**The fingerprint: where computed, where kept?** Computed in `agents/experience_deviser.py`, at import, over everything that agent can send a model which does not come from a house: every block, with the numbers the format fills them with, and the three shapes and three distances a parent's choice picks between. Today that is **31 366 characters** and `d427131c594e`.

Fingerprinting the *rendered* prompt was the obvious reading of the requirement and it is wrong twice over. It is useless, with a number: `already`, `happened` and `ground` differ on every call, so ten afternoons would carry ten fingerprints and no two could ever be counted together. And it is not allowed: the rendered prompt carries `$note`, what the parent wrote about their household, whose documented example in `experience_deviser.household.md` is a death in the family three weeks ago. `panel/observability.py` says that may not reach a workspace. Fingerprinting the standing instruction sidesteps both, and a test asserts that no block is left out of it — the failure that would make a prompt change invisible in the counts.

It is kept in three places, on purpose: the header of `docs/prompts/deviser.txt`, so a fingerprint in a log can be read against the text that produced it; the verdict row, in the store and in the trail, so a parent's record says which prompt wrote their afternoon; and the workspace line, which is what the query groups by. `tools/devise_many.py` writes it into `runs.json` and `tools/judge_many.py` reads it back out, so two folders in `experiments/` can be compared instead of merely both existing.

### The question that no number answers, so it stays a question

The verdict is shown to the parent, and `agents/experience_judge.py` says in its opening line that it is **never a gate**. It is not one in the code: nothing consults it to allow or refuse anything. But a parent who reads *this afternoon gives away its answer* while deciding whether to approve it has been handed a gate to operate — and one whose criteria come from a model that read a document knowing nothing about the house it is for.

The version built today takes the smaller side: the verdict is not in `OfferedExperience.to_public`, so it is absent from what a parent reads while deciding, and it appears in the trail once the afternoon has begun. That is a default, not an answer. **Should a parent see the reading before they decide?** Arguments exist both ways and neither has a measurement behind it. It is worth knowing that showing it is one line of code and un-showing it, after parents have relied on it, is not.

### What ten devisings found, and it is one limit and not several

Ten afternoons devised against the real service on 3 September 2026, prompt `d427131c594e`, in `experiments/12-giudice-in-produzione`. All ten came back. The counting was possible at all because `tools/devise_many.py` now configures logging: `panel/devising.py` writes every refusal and every repair at INFO and nothing in that tool had a handler, so a batch where the format refused half the answers and the repair loop quietly recovered them looked exactly like a batch where nothing went wrong.

**Five of ten were refused by the format, and all five name the same rule.** The illustration on a handed-over page is capped at 200 characters and came back at 201, 208, 209, 215 and 251. A sixth, in production, came back at 206. Nothing else was refused by the format: not a line, not a heading, not a title, not an overview, not a script. So the question the last batch left open — *do the new instructions push the model over the other limits* — has an answer, and it is **no**. One limit is being overrun, about half the time, by a median of nine characters. That is a prompt to tighten in one place, not a model to change. One further afternoon was refused by the checks, for a way out reaching for an object nothing before it mentioned.

**All ten were recovered by the repair loop**, which is what the loop is for and also what hid the rate until today.

**And then the limit was moved, because it turned out not to be one.** `MAX_ILLUSTRATION` capped a field that is never lettered on the paper and never passes the gate — `shared/page.Page.words` says so in as many words — so unlike every other ceiling beside it, it protected no physical space and no screening. What it did instead was refuse six documents in eleven and charge a second full devise call for each. Meanwhile the instruction it sits inside has grown about a dozen prohibitions — no diagram, no legend, no compass rose, no materials, nothing from this house — and satisfying them costs words. The number was fighting the paragraph around it, which is the correction §12 already recorded about the ceilings in `methods/`: *a ceiling set from the wrong constraint shapes the writing instead of catching it*. It is now 600, above the observed maximum of 251 by a wide margin, and it still catches a model returning a page of prose. The prompt fingerprint moves from `d427131c594e` to `7f732d0d28eb`.

**The thing this was hiding is worse than the cost.** Half the documents reaching production were *second attempts*. Every measurement of the prompt was therefore a measurement of the prompt plus its repair, including the research run above.

**The readings, against the earlier batches.** `does_not_end_on_the_object` 3 of 10 and `given_away` 1 of 10, against 2 of 5, 1 of 5, 5 findings across 5, and 0 of 4 in `experiments/07` to `10`. The `given_away` is a real one and was read by hand to check: it names `moments[1].help[2]`, the **third** rung, where «Cerchia il muro in entrambe» hands over the repeated detail before the fourth rung hands over the answer. The fourth rung was not named once in ten, which is the empirical confirmation that the line added to `experience_judge.instruction.md` today works — that finding used to be worth nothing because it reported the format doing its job.

**And the reader stated the question on all ten.** Zero afternoons where something can be got wrong and no reader could say what. That is the loudest thing this instrument produces and it stayed quiet, which is a result and not an absence of one.

### The other instrument says the afternoons got worse, and it should be believed first

`research/` is the apparatus that plays afternoons against a model standing in for an adolescent and gives eight axes a number from 1 to 5. It had not been run since 29 August. Run again on 3 September under prompt `d427131c594e` — same seed, same six households, four iterations, 24 afternoons — **every one of the eight axes is lower than the last run of 29 August**, and the mean across them falls from 3.49 to 2.93.

| asse | 29 Aug | 3 Sep | |
| --- | ---: | ---: | ---: |
| `questionHasAWrittenAnswer` | 2.79 | 1.75 | −1.04 |
| `canBeStarted` | 4.71 | 3.96 | −0.75 |
| `worthTheHour` | 3.17 | 2.54 | −0.63 |
| `notASchoolSheet` | 3.08 | 2.50 | −0.58 |
| `oneThingAtATime` | 3.46 | 3.04 | −0.42 |
| `sheetStandsAlone` | 2.88 | 2.46 | −0.42 |
| `canBeAbandoned` | 3.88 | 3.54 | −0.34 |
| `everyStepLeavesAMark` | 3.92 | 3.62 | −0.30 |

**The first confounder was checked and is not the explanation.** A run that ends `asked` is one the apparatus stopped rather than one the afternoon finished, so its appraisal reads a truncated transcript; more of those would move the means for a reason that is about the instrument. The ending mix is almost identical — 2 closed, 9 asked, 13 stopped on 29 August against 2, 8, 14 today — and within today's run the `asked` afternoons score *higher* than the `stopped` ones, 3.09 against 2.92, so having one fewer of them cannot produce a fall.

**What it is not safe to conclude.** Which prompt state the 29 August runs exercised is not recorded — fingerprints started today — so the comparison is *between two dates* and not between two named prompts. That gap closes from here: every run from now on carries its fingerprint.

**What it is safe to say.** Eight axes out of eight moving the same way is not the shape of noise, and −1.04 on `questionHasAWrittenAnswer` puts that axis below 2, which is the number the axis was given to catch: a question the system cannot answer, handed to somebody who believes there is one. That is the first thing to look at, and it sits oddly beside the judge, which could state a question on all ten afternoons it read. The two are not measuring the same failure — one asks whether a question can be *stated*, the other whether its answer is anywhere *written* — and a session that treats them as one number will lose the disagreement, which is the most informative thing either of them produced today.

### Where the next session starts

`panel/judging.py`, `agents/experience_deviser.PROMPT_FINGERPRINT`, `tests/test_judging.py`, and `experiments/12-giudice-in-produzione/judged.json` as the first batch whose prompt is written down beside it.

Three things are worth doing next and one of them is cheap. **Tighten the illustration** — done, and the other way round from what this said: the ceiling moved rather than the prose, because the field it capped protects nothing. What is left is to check it, and the check is written above as a prediction that can fail: under `7f732d0d28eb` the format refusals should go from 5 in 10 to none, and if they do not the diagnosis was wrong. **Then §10 becomes runnable for real**: twenty afternoons under two fingerprints, counted rather than remembered. **And the question above stays a question** until somebody with a parent's stake in it answers it.

**Before any of that, `questionHasAWrittenAnswer` at 1.75.** It is the largest measured fall and the axis furthest below the line, and a `research` run is an hour and about thirty-six cents — cheap enough to bisect the prompt changes of the last five days against, now that a run records which prompt it was. Note that the illustration ceiling has moved since that run, so the next one measures two changes at once unless it is done first.

**The trail survives a change of session now.** `experiments/**/judged.json` is committed — a hundred kilobytes of invented material carrying the findings, the question and the answer worked out per afternoon, and the fingerprint of the prompt that wrote them. Until today the only record of five judged batches was a table somebody had retyped into this file. `runs.json` stays out: it repeats every afternoon document in full, 560 kB against 100.

**Done when**, for the first: a batch of ten under `7f732d0d28eb` with no illustration refusal, compared against `d427131c594e` by `tools/judge_many.py` over the two folders.


