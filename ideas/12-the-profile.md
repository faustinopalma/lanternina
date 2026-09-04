# 12 — the profile that pitches an afternoon

Written 4 September 2026, after the rule that nothing about a person may be kept anywhere was withdrawn. [docs/NON-GOALS.md](../docs/NON-GOALS.md) holds the decision; this holds the reasoning, the measurements, and the three things it found that nobody was looking for.

## 1. What was actually wrong

The old rule was not costing a feature. It was costing the product. An afternoon written with no idea of the level it should be pitched at is an afternoon pitched at nobody, and every mechanism the system had for calibrating was a proxy for the thing it refused to hold: a parent's one-off choice between three words, a list of subjects already covered, a direction computed from six counts and thrown away.

And the proxies were worse than nothing in a way that is worth naming, because it is the failure mode of every rule of this shape. **A rule that forbids the honest version does not stop the dishonest one; it makes it arrive sideways.** `SHAPES` was a verdict about a person, chosen by a parent in three steps and sent to the model as a sentence — the only thing the rule bought was that nobody called it one.

## 2. What was found while looking, and it is the largest thing in this file

**The route that files how an afternoon went had never been called.** `POST /api/device/{household}/what-happened/{run}` was written on 28 August 2026, `panel/what_happened.py` was written and tested behind it, and on 4 September the string `what-happened/` appeared exactly once in the repository: on the line defining the route. The house talks to the panel in six places and none of them was that one.

So both prompt blocks that read those rows — `what-happened`, the last few afternoons as evidence, and `how-it-has-gone`, which way to move on how much to ask for — are conditional on a store that was never written to. **Every afternoon devised in production since 28 August was written with no history and no direction at all.** Seven days of a mechanism that was tested, deployed, documented and inert.

Two lessons, and the second is the one to keep. The first is small: a route with no caller is not a feature. The second is that `devices/run_experience._forget` said, in its own docstring, *«An afternoon that ended leaves nothing behind, not even that it happened»* — which was the withdrawn rule, stated as behaviour rather than as a comment, in the one package nobody thought to search. The rule had been removed from four docstrings and was still running.

**A test that can pass on zero must fail on zero.** `how_it_has_gone` returns zeroes for an empty history and zeroes mean *stay put*, which is a legitimate answer. There was no way to tell it apart from *nothing was ever recorded*. `Profile.seen` carries the denominator beside every band for this reason.

## 3. The axes

Three, and the bar each had to pass is that it changes a sentence in the prompt. An axis that would not is a number kept for its own sake.

- **load** — how many things have to be held together at once before the afternoon makes sense. It is what `SHAPES` meant when a parent chose it, and it is the only one of the three with evidence that it changes the output, because it has been in the prompt since 27 August.
- **ink** — how much of what a sheet offers ends up used, and of what kind. It changes what a `hand_over` asks for: something to mark, a few words, a page to fill.
- **span** — how long the afternoon runs before it wants to be over. Distinct from load, and the distinction is the correction: `LESS` said *ask for fewer things at once* when the evidence was *they stopped after forty minutes*, which are two different repairs.

One was proposed and rejected with a number. **A per-house record of which methods work here** has evidence — `Drawn.mechanic` joined with how the afternoon ended — and no denominator: 204 records in `methods/`, roughly one afternoon a day, so the count per house per method is 0 or 1 for years. `ideas/11 §5` already had the answer and it is *the only honest scalar is the earned one*; the honest denominator here is global, not per house.

One is wanted and cannot be had. **How soon a rung of help arrives** would change the prompt, and there is no evidence for it: the house does not report which rung was reached. It would cost one field in the report and it is not built.

## 4. The split, which is the design

The parent's instruction was that the roles are always divided, and it resolved a question this file had been circling.

**One model reads one page and is shown nothing else.** `agents/page_judge.py` gets the blank, the sheet off the glass, and what that sheet asked for. No profile, no history, no household, no other afternoon. That is not politeness: a model shown the current state and asked whether it still holds will agree with it, because agreeing with its context is what a model does — and a series of agreements is a state that stopped being measured after its first entry. `tests/test_profile.py` asserts the absence on the prompt text rather than trusting the comment.

**Arithmetic reads the series.** `shared/profile.read_from` has no model in it. It is a mean over the last eight placements per axis, banded into three by cutting the 1–5 scale in thirds, and it says nothing at all below three placements. That is where the judgement becomes a state, and it is a function anybody can run by hand — which is the property a second model call would have destroyed.

It also settles the smoothing question without inventing anything. The state is recomputed from the window every time and nothing is carried over, so one page moves an axis by at most one part in eight. Hysteresis is the usual answer and it cannot be checked by hand.

**And `span` has no model in it at all**, because no page shows how long anybody sat. It is the minutes the plan asked for against the minutes the house reported, and whether the afternoon reached its own ending. Measured on the arithmetic as written: of 120 planned minutes, all of them and its own ending is 5; all of them ended by the clock is 4; two thirds and its own ending is 4; two thirds ended by the clock is 3; a quarter is 2 either way.

## 5. A sheet that never came back

The parent's second instruction, and the one that needed a guard rather than a feature.

It is **not** a page that came back blank, and folding the two together was the first thing the code wanted to do. Blank is an act: somebody carried the sheet to the glass and put nothing on it. `never` covers the sheet still on the table, the sheet in the bin, the afternoon walked away from — and the scanner in another room, unplugged, or that nobody has been shown.

Nothing in this system can tell the last one apart from the others. So a sheet that did not come back is read as the bottom of the ink axis **only in a house that has had at least one come back**. Without that rule a house with a dead scanner is pitched at the bottom of every axis inside a week, and there is no symptom anybody could read: the afternoons just get smaller. It is in `shared/profile._placed`, it has a test, and the test was watched to fail with the clause removed.

## 6. What the parent no longer chooses

Both stepped settings left the panel, and for two different reasons.

**The shape** — *simple, medium, harder* — asked a parent to say in three steps how much somebody can take. That is a verdict, it is the one thing the panel refuses to ask for, and the system can now work it out from what comes back off the glass. What a parent may still say is in the note, in their own words, where it arrives as a circumstance and is not filtered: *questo mese chiedi meno* reaches the prompt and always did.

**The variety** asked a question nobody can answer before seeing an afternoon. It did not move anywhere: an afternoon now travels as far from the recent ones as `not_the_same_afternoon_again` allows, which is a bound that can be checked, unlike a preference that could only be honoured or ignored.

The cost, stated because it is real: a house with no history now gets no pitch sentence at all, where before it got one of three from the first afternoon onwards. `SHAPES` was added on 27 August precisely because afternoons were failing on that axis. Saying nothing is the honest answer to *we do not know yet*, and it is what the deviser did for the whole of August, but the first few afternoons in a new house are less steered than they were yesterday.

## 7. The gate

`docs/NON-GOALS.md` says the prompt asking for this is not the protection and the gate is, so the gate had to be a sixth family in `shared/blocklist.py` rather than a sentence in a prompt.

**Fitted**: a sentence telling the reader the afternoon was sized for them, or referring to how their last one went. It is the narrowest family in that file, because second person with a past tense is most of the dialogue in most fiction, and a rule catching that would take every speaking character out of every afternoon — which is exactly what the list of 78 literal phrases did to `errore`, `livello` and `mamma` before patterns replaced it. So every pattern carries the sizing itself: *pensato apposta per te*, *più facile del solito*, *l'ultima volta hai*, *sei pronto per*.

Measured on nine sentences a model handed a pitch would plausibly write and eight ordinary ones: nine caught, zero false refusals. It runs where the block list already runs — over the title, the overview and every word of every moment, at devise time with a repair loop behind it, and again on every string heading for a display while the afternoon runs.

## 8. What it costs

**One extra vision call per returned sheet.** The same two images the reader gets, in a second call, because one answer carrying both the description and the placement would let a judgement into the text by the shortest route there is: `describes` goes straight into the continuer's prompt and from there onto a display.

It runs after the reply, never inside it. A page reading was measured at 14.4 s on 3 September 2026 and somebody is standing at the scanner; the precedent and the arithmetic are `panel/judging.py`'s. It counts against the household's monthly cap and is skipped at the limit, for the reason that file already gives with a number: there is exactly one placing per reading, so a placing exempt from the cap would make the real spend at that moment exactly twice what the cap says, and a cap a category of call can double is not a cap. It has its own usage kind for the same reason a reading is kept apart from a wording — folded together, *how many pages were read* would be permanently twice the truth.

## 9. Where it starts, and what is not done

`shared/profile.py` for the arithmetic, `agents/page_judge.py` for the model, `panel/profiles.py` for the series, `tests/test_profile.py` and `tests/test_how_it_went.py` for the guarantees. Three of those tests were mutation-checked: the scanner guard, the fitted family, and the reporting of a sheet that never came back.

**Nothing has run against the real service yet.** Every number in this file is arithmetic or a measurement of something else; not one afternoon has been devised with a pitch in its prompt, and no page has been placed by the model that is supposed to place it. The first house to accumulate three placements is the first evidence that any of this works.

**And the bench run that would have measured the prompt rewriting of 3–4 September was not made.** Fingerprint `e071f1d93168` has no scores against it, the prompts have now moved again, and that window is closed. `research/scores.json` has the earlier runs. The next run measures two changes at once, which is what the attribution was there to prevent.

**Open, and written down rather than settled.** The profile is per household, because `household_id` is the key everywhere and there is no field for who is in the house. A house with two adolescents gets one profile, and their pages average together. Nobody has designed the version where that is not true, and inventing a per-person key would be inventing the record this project spent a month refusing.
