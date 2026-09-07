<!--
The shape of the answer. What follows it in the assembled prompt is the format describing itself — the shape of a moment, the acts, and what a page is — which lives with the format in shared/experience_prompt.*.md because the continuer sends it too.

`themes` and `script` are what the parent approves alongside the overview: what it is about, and how it should go. The script is also what whatever runs the activity reads, so it is written for somebody doing it rather than for somebody deciding about it — the limits it names are the ones that matter once the paper is already on the table.

The overview asked for the wrong thing until 3 September 2026, and it asked for it in one sentence: *say what it is like to be inside it*. It got exactly that. Measured on the fifteen overviews generated that day: eight of them open with the same two words — «Un pomeriggio quieto» or «Un'indagine quieta» — every one describes an atmosphere, none says what the person will do, what the house has to supply, or what is left at the end. A parent handed three of those reads the same fog three times. `panel/experiences.py::to_public` shows the overview, the themes and the script to the parent, and `ideas/08 §2` says approval is given to them, so this is the one string the whole gate rests on.
-->
Answer with JSON and nothing else, in this exact shape:
{"title": "<text>", "overview": "<text>", "themes": ["..."], "script": "<text>", "minutes": <whole number>, "drawn": { ... }, "moments": [ ... ]}
Do not write an id, a format version or a list of what the house needs: those are known already and are not yours to write.
  "overview": at most $max_overview characters, and it is what a parent sees at a glance. Five things, plainly, in this order:
    what the person actually does — the verbs, and the thing they do them to;
    what comes off the printer, and what that object is;
    what is in their hands when it is over;
    anything the house has to find beyond paper, a pencil and what is already on the table — or that there is nothing;
    and the one thing somebody might not want about it, said without softening.
    Write it so somebody holding three of these can say which one they want and why. What it is like to be inside it — «un pomeriggio quieto», «un'indagine quieta», «il tono è raccolto» — tells a parent nothing, and three activities that all begin that way cannot be told apart.
  "themes": at most $max_themes of them, each at most $max_theme characters. What it is about, a few words each, and the first thing the parent reads. Nouns, not sentences.
  "script": at most $MAX_SCRIPT characters. Explain the activity for the parent and for the agent that may continue it. The runner executes moments, not this script; the page maker receives only the page fields. Anything needed to act must therefore also appear in those fields. Write these parts, each headed by its own name on its own line:
    THE WORLD. The setting and the object somebody works with. Give the specific details that make it interesting. State which details are fictional. A real observation or construction can stay real.
    THE WAY IN. What somebody picks up, where it comes from, and the first action. Start with what the printer supplies or the household has declared. A fictional backstory does not put a box in a drawer or a mark on a wall in the real house.
    THE QUESTION. The question to settle, object to make, or choice to explore, in one sentence. Then give:
      The operation: the concrete action with the available material, such as comparing, ordering, drawing, folding or testing.
      The evidence or materials: name each required item and the page field or household input that supplies it.
      The result: for a closed question, write the answer and show why the supplied evidence establishes it. If several answers fit, accept them or change the evidence. For an open task, give one workable example and what makes the action complete; do not present that example as the only answer.
      The reason to do it: what can be discovered, changed or kept through this action.
    THE BEATS. One line per executable moment: what is available, what happens, and what finishes it. Let later actions develop what was discovered or made earlier. Use the number of moments the activity needs within the format limits. Every task must fit the short weight too; extra time permits exploration or another attempt, not a missing essential step.
    WHAT IS HELD BACK. Any later discoveries and the actual moments that deliver them, or none. Instructions and evidence needed now are available now. The runner cannot detect a fold, a glance or a turned page. A collect distinguishes marks from blank; use ask when the continuation must depend on what the marks say.
    WHAT IS MADE. Each printed sheet, what it contains and what somebody does to it. Name the title, note, space labels and illustration details that supply the task. Use another sheet when it adds a useful stage or object, respecting the household's simultaneous-sheet limit. The script cannot supply extra text to the page maker.
    WHERE IT CAN GO DIFFERENTLY. What happens if the paper comes back full, if it comes back untouched, and if somebody stops caring halfway. Concrete moves, not principles.
    WHAT WOULD SPOIL IT. Two or three, and they should be things you are actually tempted to do.
    Before returning the JSON, walk the moments using only their visible lines and page fields. Check that every referred object exists, every required instruction and clue is supplied before use, and the result follows without an invented fact. Repair the fields where that walk fails. A solution written only in help is not evidence that the unaided task is solvable.
