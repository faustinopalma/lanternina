# Officina

This index collects the historical workbench and the numbered end-to-end synthetic game iterations. Keep completed notebooks with their outputs. Create the next numbered notebook for a different brief, prompt revision or experiment; clear its outputs before executing it. The historical notebook remains at its original path and is included in the table below.

| Iteration | Notebook | Result |
| --- | --- | --- |
| Historical | [Original workbench](../research/officina.ipynb) | Concluded on 7 September 2026: 2 sheets and 1 synthetic return. The executor measured 345.4 seconds; the model-path verification measured 335.6 seconds. |
| 001 | [Material correspondence](001-material-correspondence.ipynb) | Concluded on 15 September 2026: 4 sheets, 4 synthetic written returns, 3 continuations and 10 executed moments. |
| 002 | [Baseline](002-baseline.ipynb) | Stopped after the first return: continuation JSON cut at 9,000 characters. |
| 003 | [Concrete actions](003-concrete-actions.ipynb) | Stopped after the first return: slash-separated returned wording rejected by a text check. |
| 004 | [Distributed work](004-distributed-work.ipynb) | Concluded: 4 sheets, 3 returns and 3 continuations. The route and closing claims still have editorial defects. |
| 005 | [Visible evidence](005-visible-evidence.ipynb) | Stopped after the first return: safety request exceeded the service's 10,000-character maximum. |
| 006 | [Screened continuation](006-screened-continuation.ipynb) | Concluded: 2 sheets, 2 returns and 1 continuation. This misses the brief's three-exchange requirement. |

The [sequential comparison](comparison-002-004.md) evaluates every new run and records which prompt or code changed before the next. The [authored example](authored-example.md) proposes a complete four-sheet correspondence for comparison; it has not been rendered or physically tested. Each new notebook contains its editorial review after the execution cells. The failed assertions and images remain intact.

The first [verification](runs/001-material-correspondence-20260915T131106126755Z/verification.json) passed every notebook check, including the untouched-page control. The executor measured 655.8 seconds; the model-path verification measured 643.734 seconds. The notebook records a visual continuity issue: later illustrations introduced places absent from the first map. Passing the execution checks does not settle that issue. Full continuation documents are in the walk; this first run's call recorder kept some text responses only as length summaries, corrected for subsequent executions.

Run the cells in order with the repository Python environment, or execute the notebook from the repository root:

```powershell
python -m research.execute_officina officina/001-material-correspondence.ipynb
```

The executor saves notebook outputs even when a cell fails. Each execution creates a timestamped directory under `officina/runs/`. It holds the generated experience, full-size pages and synthetic returns, logical prompts and responses, measured durations, the walk and verification results. The notebook shows reduced images and a readable transcript. Rerunning calls paid services and creates another artifact directory; it replaces the notebook's displayed outputs.

The notebooks load the existing research configuration and credentials from the environment. They reuse production generation, drawing, reading and continuation functions. Household settings and handwriting are synthetic. They do not print, photograph physical paper, call the deployed device API, change approvals or reproduce the household clock. Declared minutes are document timings rather than elapsed human time.

Iteration 001 uses the existing scanner-style `PageReader` comparison between an original generated page and its synthetically marked image. It does not exercise perspective correction from a camera photograph. Later continuations receive the original approved plan, as in the current hub; they do not receive an accumulated execution history. Inspect the transcript for repetition, paper-budget drift and lost context.

An iteration passes only when its stated checks pass and the executed path reaches a `close` moment. Errors, degraded reads, exhausted step limits and interruptions remain visible. A successful software run does not establish printed legibility, physical pacing or comprehension.
