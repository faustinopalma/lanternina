<!--
The judge. It reads one played afternoon and scores it on eight axes.

Every axis comes from something already written down rather than from taste: five of them from `docs/EVIDENCE.md`, which is the reading behind the working rules, and three from the rules themselves. The wording of each is the criterion, so changing a score means arguing with a sentence rather than with a number.

**Evidence is required and it is the point.** A score with nothing quoted is worth nothing for tuning a prompt: what makes a run useful is a line from the afternoon and a sentence saying what is wrong with it, because that is what a prompt can be changed against. The instruction to quote is repeated at the end because it is the first thing a model drops.

**It scores the afternoon and never the person.** That has to be said out loud to a model that has just been handed a transcript of somebody not finishing something. A sheet that came back blank is evidence about a sheet.
-->
Read this afternoon as it was actually played and score it. It was written by a system for one adolescent at home, and it was played against a simulation, so what you are judging is the design and never the person.

$transcript

Score each axis from 1 to 5, where 3 is "does the job", 1 is "this is the failure the axis exists to catch" and 5 is "this is what it looks like when it is right". For every axis quote one line from the afternoon and say in one sentence what that line shows. Quote, do not paraphrase. If nothing in the afternoon bears on an axis, score it 3 and say that nothing bore on it.

The eight axes:

  "canBeStarted": can somebody begin from what they were given? The first thing has to put a situation in front of them and name a physical first step. A moment that announces what the afternoon is called or what it is for is a 1.
  "sheetStandsAlone": could somebody who missed a screen use the sheet? A screen is gone when the next one comes and paper stays on the table, so anything needed later has to be on the paper. A sheet that only makes sense with a screen that has passed is a 1.
  "oneThingAtATime": how many things have to be held together at the same time? Short chunks, generous space, one idea per instruction. Not the same as short: an afternoon that says four things quickly is worse than one that says two things slowly.
  "everyStepLeavesAMark": is what is asked for something that can be done and seen — written, drawn, cut, folded, counted, moved, named on paper? A beat whose whole content is *notice which one lasts longer* is a 1, because nobody can tell whether they did it.
  "questionHasAWrittenAnswer": is there something to find out, and is the answer written down in the last rung of help? A question the system cannot answer, handed to somebody who believes there is an answer, is the one thing an afternoon cannot absorb. No question at all is a 2, not a 5.
  "canBeAbandoned": can this be put down at any point with no cost, and does the way out reach for something that is actually in the person's hands? Anything that has to be got right before the next thing arrives is a 1.
  "worthTheHour": is it strange, specific, and does it end with something made or found out that did not exist before? Generic, tidy, and about nothing in particular is a 2. One impossible thing plainly told is a 5.
  "notASchoolSheet": the voice. Somebody who is also interested, never a teacher. No praise, no blame, no remark on how it went, no explaining the point, nothing that reads as marking.

Then say, outside the axes:
  "worstLine": the single line from the afternoon most worth changing, quoted exactly.
  "whatToChangeInThePrompt": one sentence naming what the prompt that wrote this should say differently. Not a fix for this afternoon — a change that would have made a class of afternoons better. If nothing, an empty string.
  "howItWentInAWord": one of "carried through", "ended early", "stopped", "never started".

Answer with JSON and nothing else, in this shape, and with no text before or after it:
{"axes": {"<name>": {"score": <1-5>, "quote": "<a line from the afternoon>", "says": "<one sentence>"}, ...}, "worstLine": "<text>", "whatToChangeInThePrompt": "<text>", "howItWentInAWord": "<text>"}

Every axis needs a quote taken word for word from the afternoon above. An axis with a paraphrase instead of a quote is the answer being useless for what this is for.
