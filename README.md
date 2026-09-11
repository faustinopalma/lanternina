# Lanternina

Lanternina invents activities for adolescents, lets a parent review them and runs them on paper and e-paper displays. A Linux hub controls the equipment and the clock. The container API calls language, image and vision models through Microsoft Foundry. No model runs in the house.

An activity can ask somebody to build, observe, draw, compare or investigate. Instructions must say what to do; an open task can have several defensible outcomes. A valid document does not by itself establish that an activity is understandable or worth doing.

## How an activity runs

The hub asks the container for activities using the household's settings and recent history. A parent can also prepare a brief in the panel. The container chooses a method, generates the activity, validates it, repairs specified failures and screens the result with Content Safety. The offered activity waits for a parent decision. The hub retrieves approved activities and decides when one can begin within the configured hours and daily limit.

Each activity contains moments, three durations for each moment, help text and a way out. The hub asks the container for a page at `hand_over`. An image model draws the complete sheet from its page contract. The hub sends the image to the printer and retains its blank image for comparison. A button press starts the scan path. The container's reader compares the scan with the blank and returns descriptions of the added marks.

The runner branches on `marks` or `blank`. A degraded reading does not become a blank sheet. An `ask` outcome requests a continuation from the container. Its prompt receives the actual reading, the original activity and the household's bounds. The continuation is parsed, checked and screened, but it is not shown to the parent for a second approval and has no repair loop.

The hub begins the way out near the configured end time and later shows the close. This depends on functioning services and readable state. The runner advances immediately through consecutive non-collection moments; declared durations do not establish a real pause between each pair. Print failure shows `instead`, but the current runner does not execute the contract's `if_no_page` branch. These limits are detailed in [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md).

## What the parent controls

Content preferences include interests, subjects to avoid, Italian or English, a limit of one to three simultaneous sheets, and a note that expires after 28 days. Rhythm settings control days, hours and the number of activities. Device assignments, reminders and continuation guidelines also have panel controls. Words per line, difficulty and variety are not current parent settings.

Saving configuration stores state; it does not contact the hub. The hub reads changes on its next request. Brief editing has its own model-assisted API path, so the stronger claim that every dashboard action is model-free would be incorrect. An initial approval permits the activity; it does not preapprove every later generated word or image individually.

## What is remembered

The system stores configuration, offered activities, generated pages and the activity trail. It also stores how activities ended, their reported duration, returned or missing sheets and bounded reading-derived summaries. A separate model places returned pages on the `load` and `ink` axes. Arithmetic combines recent observations with activity duration to compute the `span` axis. The resulting profile steers generation and continuation; the panel does not expose the profile as a score.

This is durable adaptation from observed activity, not merely a list of material the system generated. The profile uses up to eight recent observations and requires at least three placements for an axis. Its observations and interpretation can be wrong. They are not a clinical assessment or a demonstrated measure of ability. The parent can clear the activity memory and profile observations through the memory route.

`WhatCameBack` blocks implicit copying and pickling, but its explicit `to_dict()` is an HTTP request body. Those restrictions do not prohibit all retention. Administrators can enable development retention for one household for 14 days. A reading retained while permission stands has its own 14-day lifetime; withdrawing permission stops new records but does not immediately erase existing ones. A complete plain-language view of all household memory is not implemented.

## Verification and status

The local model path was exercised on 7 September 2026 with an invented railway activity. The notebook completed in 345.4 seconds, measured by its executor; generation, drawing, handwriting, reading, continuation and the blank-page control took 335.6 seconds inside that run. Two pages were drawn, one was synthetically filled and read, and one continuation reached a close. The actual continuation prompt contains the returned descriptions. [The artifacts](research/runs/2026-09-07-officina-104746-339138/verification.json) and [the workbench](research/officina.ipynb) preserve the evidence. These are software and model-path results, not a physical trial or a quality score.

Earlier physical trials are documented in [ideas/09-a-game-that-ends.md](ideas/09-a-game-that-ends.md). Hardware availability and the deployed code version were not checked in this session, and no deployment was performed.

Local code includes the panel, device assignments, activity approval, generation, reading, continuation, help and end-time handling, picture and page archives, reminders, usage limits, memory and profile computation. The handheld camera and multi-button panel remain unimplemented as activity inputs. The optional-moment dropping and merging policy is not implemented in the standard runner. A second household installation and current printed legibility still need physical verification.

## Development

Python 3.11 or later is required. Install the extras needed for the work being done:

```bash
python -m venv .venv
python -m pip install -e ".[dev,bench,panel]"
python -m research.execute_officina
```

Use the repository interpreter. The notebook loads the research model configuration from `research/env.ps1` and uses the existing Azure login; credentials must not be placed in notebook cells or outputs. It deliberately calls cloud models and costs money. Its own branch tests remove inherited cloud variables. For the complete suite, run pytest in an environment without the `LANTERNINA_*` Foundry and Content Safety settings; otherwise some tests can call real services.

Prompt blocks live beside their Python modules. After editing one, run `python -m tools.prompts --write`. The notebook reloads these modules before a run and retains synthetic artifacts in a new directory. Historical automatic judges have false positives and incomplete transcripts; their counts are not evidence of quality improvement.

The separate simulated-house path uses the device runner with file-backed equipment. It has different coverage from the local workbench:

```bash
LANTERNINA_PRETEND=1 python -m tools.experiment run "what I am trying" --by teenager
```

Only the value `1` selects pretend mode. Do not run equipment commands against a real household as though they were harmless simulations.

## Documentation

| Document | Contents |
| --- | --- |
| [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) | Current control paths, approval, safety, memory and implementation limits |
| [docs/RESPONSIBLE-AI.md](docs/RESPONSIBLE-AI.md) | Risks, controls, evaluation and responsibility throughout an activity |
| [docs/architecture-overview.html](docs/architecture-overview.html) | Illustrated overview with dated implementation notes |
| [docs/an-afternoon.html](docs/an-afternoon.html) | Activity walkthrough and clock illustration |
| [docs/ILLUSTRATED.md](docs/ILLUSTRATED.md) | Historical photographs, printed pages and screenshots |
| [docs/prompts/README.md](docs/prompts/README.md) | Rendered prompts |
| [research/README.md](research/README.md) | Synthetic research, workbench and limitations |
| [ideas/13-prompts-and-simulation.md](ideas/13-prompts-and-simulation.md) | Decisions, measurements and remaining checks from this revision |
| [docs/DEPLOY.md](docs/DEPLOY.md) | Deployment procedure |
| [docs/HARDWARE.md](docs/HARDWARE.md) | Hardware and physical measurements |
| [docs/macchina-fotografica/README.md](docs/macchina-fotografica/README.md) | Handheld camera miniproject: XIAO Sense, photographs, button and LED wiring, planned behaviour and physical tests |

`shared/` contains contracts; `agents/` contains model instructions and parsers; `orchestrator/` contains model transport and safety. `panel/` hosts the API, `devices/` runs the house, `printing/` prepares paper, `web/` is the parent panel and `site/` is the public site. `research/` and `tools/` include synthetic apparatus that is not a production privacy boundary. `attic/` contains retired implementations.

## Privacy

The repository is public. Fixtures, notebook outputs and screenshots must contain synthetic material only. Household storage and model processing are remote; retention, access control and deployment location must be checked at the service as well as in code. This local verification does not establish a tenant-wide deletion procedure, provider retention policy or current data residency. The current stored categories and deletion paths are listed in the architecture document.

## Licence

[MIT](LICENSE).
