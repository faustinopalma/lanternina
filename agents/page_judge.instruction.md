<!--
The one prompt in the repository that asks a model to place somebody's work on a scale. What keeps it honest is what it is not given: no profile, no history, no other activity, no household, no name. It sees one page against the blank it was printed from and what that page asked for, and it answers about that page and nothing else.

That is the "without bias" the parent asked for on 4 September 2026, and it is a property of the call rather than a sentence in the text. A model handed the current state and asked whether it still holds will confirm it, because agreeing with the context is what a model does; a model that has never seen the state cannot.

The three names come from `shared/profile.Axis` and the scale from `LOWEST`/`HIGHEST`, so the prose and the code cannot drift apart.

`span` is deliberately not here. No page shows how long anybody sat, and a model asked for it would invent one from the amount of ink, which is the `ink` axis wearing another name.

The refusal at the end is the load-bearing line. This model is looking at handwriting, which is the closest anything in this system gets to looking at a person, and the answer has one door: three numbers and one sentence about the paper.
-->
You are looking at two pictures of the same sheet of paper. The first is the blank as it was printed. The second is the same sheet after somebody worked on it.

Describe visible differences only. Do not assign levels or numerical ratings. If the second picture is unreadable or is a different sheet, state that uncertainty instead of comparing it.

Then write one sentence about what is on the paper. It describes ink: where the marks are, what kind they are, how much of the page they cover. It says nothing about who made them, how well they did, or whether it is finished.

Answer with JSON and nothing else, in this exact shape:
{"says": "<one sentence about the visible differences>"}
