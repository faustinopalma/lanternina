# The prompts, whole

Every prompt this system sends a model, rendered as the model receives it. One file per
prompt, generated:

    python -m tools.prompts --write

Nothing here is edited by hand. `tests/test_prompts_rendered.py` compares these files with
what the code assembles, so a prompt changed in the code and not rendered fails the test.
What is here is what is being sent.

## Where the words actually live

Beside the module that sends them, as Markdown:

    agents/experience_deviser.py
    agents/experience_deviser.task.md
    agents/experience_deviser.format.md
    agents/experience_deviser.rules-head.md
    ...

`shared/prompts.py` reads them. A file may carry `<!-- ... -->` comments — what was measured,
why a sentence is worded the way it is — and those are stripped before anything is sent.
`$name` placeholders are filled from the format's own constants, so a number in a prompt is
never a number typed twice.

## Why the whole thing is rendered as well

The Markdown files can be read on their own. What cannot is the join: the order the blocks go
in, what the numbers came out as, where the parent's typed words land. That is what these
files show.

## The household material is invented

`docs/NON-GOALS.md` and the working rules both say no personal data lives in this repository.
Where a real call would carry a real house, these carry two interests, one thing to avoid,
and a sentence about brushing teeth. Each file says at the top what was invented for it.
