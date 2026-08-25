<!--
The afternoon as it stands, appended to the standing instruction. Everything here is a fact, and everything in it is quoted as JSON so that nothing a model wrote earlier can be read as an instruction now.

`what_happened` is the memory. It is a list of things that occurred — a display said this, a page was printed, a page came back with ink in one place and none in another, this long passed — and never a claim about the person who was there. That distinction is the whole reason this field is built by `agents/experience_agent.py::a_memory` out of typed events rather than being written by anything.
-->
The strategy this afternoon is run against, which the parent approved: $strategy
What it is about: $themes
The plan as it was written, for reference — you may depart from it: $plan
What this house can do right now: $tools
What has happened so far, oldest first: $what_happened
Minutes left before it must be over: $minutes_left
Decide the next move.
