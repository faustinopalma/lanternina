# Lanternina

Lanternina invents an afternoon, gets a parent's agreement to it, and then runs it in a real
room — on paper, on e-paper displays, and on the clock — for one adolescent, with nobody
watching over their shoulder.

An afternoon is not a worksheet with a story on top. A model writes it as a whole document:
four or five moments, each in three lengths so the plan can be shortened without being cut,
a four-rung ladder of help that arrives whether or not anybody asked, and from every single
point a written way out that reaches the same ending. That document is checked against six
properties before a parent ever sees it, and a parent approves it once. Nothing in the cloud
can start it, extend it or redirect it: the house asks, and the answer arrives inside the
reply.

Then it happens. The house prints a page — a map, a dossier, a museum label, a leaf from a
field notebook, drawn whole by an image model from words that have already passed the safety
gate. Somebody writes on it and puts it back on the scanner glass. The page is read by
handing a model two images, the blank and what came back, and asking what is different: no
QR code, no corner markers, no grid of declared boxes, nothing printed on the paper that is
there for a machine. What comes back decides where the afternoon goes, and the rest of it is
written while the page is still on the table.

It ends. Thirty minutes before the hour the parent agreed to, whatever the afternoon has
reached, the way out begins — and the ending it arrives at is the same ending, never
announced as a shortened one.

It runs on a Linux mini-PC in a house, serving two e-paper displays, an inkjet and a flatbed
scanner. Every language and vision call goes to Azure AI Foundry in the EU; no model runs on
the device. Measured on the deployment: an afternoon is devised in **76–100 s**, a page is
drawn in **19–33 s** and covers **0.5–2.7 %** of the sheet in ink, and a page that comes back
is read in **4.4–5.5 s**.

## Who it is for

Any adolescent. What holds someone's interest differs, how much novelty they want differs,
and how much text on a page is comfortable differs — across the whole range of cognitive
ability, and at both ends of it. None of that requires a diagnosis, and Lanternina does not
ask for one: it has no notion of a condition, a need or a level, and nowhere to record one.

## What it remembers, and what it refuses to conclude

Lanternina keeps a memory and works from it, so nobody restates the same things every week.
The memory starts as what the household chose — subjects to offer, subjects to avoid, the
form of the material, how much variety, words per line, the content language — and grows
with what happened: what a sheet came back with, what was left blank, what took a long time,
what was picked again. The system may move within those settings and beyond them on that
evidence. A system that cannot do that is a fixed system, and a fixed system is the failure
this project is most likely to reach.

The limit sits next to the claim, and it is about what may be concluded rather than what may
be observed. What is kept is a record of what happened — this cell was empty, this took four
minutes. It is not turned into a claim about who somebody is: no score, no grade, no rank,
no ability estimate, no progress trend, in the types, the storage, the prompts, the logs or
the screen, and shown to nobody. The difference is not cosmetic. A record can be checked
against the paper it came from; a verdict cannot be checked against anything.

The tradeoff, stated plainly: adapting without concluding is slower than adapting with it,
and it keeps the parent in the loop where a scoring system would not need them. Every piece
of content still arrives as a proposal the parent can refuse, so an adaptation that went the
wrong way is visible before it is delivered rather than after.

## The parent steers

Anything an agent produces is a proposal until a parent approves it. The parent writes the
settings, reviews what was generated, refuses what does not fit, and decides what the system
should offer this week. No feature is built whose value is that the parent no longer has to
think about something.

## The dashboard is inert

Adding material or changing a setting only stores the new state. It does not generate
content, enqueue work, notify a device or make anything happen immediately. The server in
the home decides when to ask for work, and it is free to look later or to decline. Its
request may stay open while the cloud scales from zero; nobody is waiting in front of a
screen for it.

## Two consequences that run through the code

- It does not optimise for engagement. No streaks, no daily goals, no variable rewards, no
  nudge triggered by inactivity, no "time spent" anywhere. Engagement optimisation is easy
  to add here and would do harm, which is why it is a written rule rather than a matter of
  judgement.
- Nothing it produces is a verdict about a person. No scores, no grades, no ability
  estimates, no progress trends, no inference adjacent to a diagnosis — and no camera,
  radar or wearable pointed at anybody. What it learns from is the work, not the person.

[docs/NON-GOALS.md](docs/NON-GOALS.md) lists what will never be built, and why. It is worth
reading before contributing.

## Documentation

The overview page is the shortest route in: one screen, three diagrams, and each number
marked as measured or estimated.

| | |
| --- | --- |
| [docs/architecture-overview.html](docs/architecture-overview.html) | The whole system on one page, with diagrams. Start here. |
| [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) | Why each boundary exists, and what the design costs. |
| [docs/NON-GOALS.md](docs/NON-GOALS.md) | What will never be built, and why. |
| [docs/THREAT-MODEL.md](docs/THREAT-MODEL.md) | What leaves the device, and what is treated as hostile input. |
| [docs/DEPLOY.md](docs/DEPLOY.md) | Reproducing the cloud tier in your own subscription. |
| [docs/HARDWARE.md](docs/HARDWARE.md) | Hardware reasoning, with what is verified and what is a guess. |
| [ideas/](ideas/) | What is not built, ranked, each entry with its cost and a check somebody else can run. **What to do next is decided here**, in the "where to start" table of [ideas/README.md](ideas/README.md). |

## How the guarantees are enforced

By types, seals and tests rather than by convention, so that removing one is a deliberate
change rather than an omission.

| Guarantee | Mechanism | Test |
| --- | --- | --- |
| Agents cannot approve their own output | `Proposal` has no status field; `AgentContext` holds no ledger | `test_boundaries.py` |
| Generated output cannot skip Content Safety | `Proposal.payload` accepts only `ScreenedPayload`, which the gate signs | `test_delivery.py` |
| Approved content cannot be swapped afterwards | The approval seal covers the safety seal | `test_delivery.py` |
| Only one component talks to a model | Import-level check across every package | `test_boundaries.py` |
| Agents never reach each other | Import-level check | `test_boundaries.py` |
| Full camera frames are never persisted | `RawFrame` refuses to pickle, copy or serialise | `test_boundaries.py` |
| The camera never analyses people | Identifier-level check across `vision/` | `test_boundaries.py` |
| No engagement or assessment vocabulary exists | Identifier-level check across every package, and a text check across the panel | `test_boundaries.py` |
| The content language is a setting, not a property of the data | Field names are English; two readers may name the old Italian keys, nothing else | `test_boundaries.py` |

Each of those tests was mutation-checked: a deliberate violation was injected and the test
was watched to fail. If you change the design so one no longer holds, please change the
product rather than the test.

## Layout

```text
shared/         types and protocols every package depends on; depends on nothing itself
                  experience.py  — an afternoon: moments, weights, help, ways out, endings
                  page.py        — a page: a kind of object, its words, and what it draws
orchestrator/   planner + the three things nothing else may hold:
                  router.py    — the only door to a model backend
                  safety.py    — the only holder of the content-safety key
                  approval.py  — the only holder of the parent-approval key
agents/         one module per agent; no agent imports another
                  experience_deviser.py / experience_continuer.py — the afternoon
                  page_maker.py  — one prompt, one whole page
                  page_reader.py — the blank against what came back off the glass
printing/       paper.py: one image onto A4, and the ink it costs. Nothing lays anything out
panel/          the parent-facing API — the only place approval happens
web/            the panel in the browser, a React single-page application
devices/        what runs in the house: display server, runner, printing, scanning
                  pretend.py — the same house with the person simulated
tools/          the command-line paths, the probes, and the simulated hand
infra/          the cloud tier as Bicep; deploy/ is the mini-PC side
docs/           architecture, non-goals, threat model, hardware
ideas/          what is not built, ranked, with costs
experiments/    runs against the simulated house, kept whether they went well or badly
attic/          what was built, argued about and retired — kept for the argument
tests/          the boundary and delivery guarantees above
```

## Setup

Requires Python 3.11+.

```bash
python -m venv .venv
. .venv/bin/activate          # Windows: .venv\Scripts\Activate.ps1
pip install -e ".[dev]"

cp .env.example .env
python -c "import secrets; print(secrets.token_hex(32))"   # run twice
# paste into LANTERNINA_SAFETY_KEY and LANTERNINA_APPROVAL_KEY — two different values

pytest
```

Two different keys matter: sharing one would let the content-safety gate mint parent
approvals. Rotating them invalidates existing approvals by design — the parent re-approves
rather than inheriting state nobody can verify.

Optional extras, installed only where needed:

```bash
pip install -e ".[vision]"    # OpenCV with contrib (ArUco lives there), on the mini-PC
pip install -e ".[cloud]"     # Azure AI Foundry + Content Safety, Entra ID only
pip install -e ".[panel]"     # the parent panel
pip install -e ".[devices]"   # serial link to the ESP32s
```

## Status

An afternoon has run end to end in a house: devised, approved in the browser, printed,
filled in, scanned, continued from what came back, and closed on its own hour. Four defects
surfaced that day and none of them had been found by a test — they were found by somebody
standing next to the printer, and they are written up in [ideas/09](ideas/09-a-game-that-ends.md).

What is solid: the afternoon format and its checks, the parent panel and its approval, the
page drawn whole and read against its blank, the clock that guarantees an ending, and the
boundaries in the table above. What is not: a second house has never been provisioned, the
installer's `--install` has never been run, and the page format's ink budget is measured but
not yet decided against a printer somebody was watching.

The full table is at the end of [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md), and it is kept
honest rather than encouraging.

## Running it without a house

There is a simulated house: the same runner, the same panel, the same models, the same
printing and the same reading — with the equipment replaced by files and the person replaced
by an image model that fills the page in.

```bash
LANTERNINA_PRETEND=1 python -m tools.experiment run "what I am trying" --by teenager
```

Each run lands in `experiments/`, numbered, with the whole flow in order: every screen, every
page as it was handed over, every page as it came back, and notes on how it went. Runs that
failed are kept, because a run that failed is the only evidence of how it failed.

The switch is one word. `LANTERNINA_PRETEND=1` simulates; anything else, or nothing, is the
real house.

Running: the cloud tier, the parent panel and its API, the content agent, the model router
with real credentials, the safety gate, the hub services that serve the displays and pull an
hourly picture, the picture archive, and usage accounting with a per-household cap. The
sheet renderer is written and was checked on paper — a 50 mm ruler measures 50 mm. The paper
loop runs from the button and was measured with a finger on 19 August: a press puts "sto
leggendo" on the display in the same request, the scanner takes about twenty-six seconds,
and the reading lands on the next wake, so thirty-five seconds from the press.

Not written: the planner, the vision, scheduling and print agents. `firmware/` holds no
sources: the displays run the vendor's firmware with two patches of ours, one for mDNS and
one that takes the two credential-wiping presses off the button. Both units carry it as of
19 August 2026. What the house cannot yet be told is which display, printer or scanner is
for what: those are three constants in the hub's environment rather than choices in the
panel.

Stubs raise `NotImplementedError` or return obviously fake data. Nothing in this repository
pretends to work.

## Privacy

No personal data is in this repository and none should ever be added — not in fixtures,
tests, screenshots or example configuration. Demo material is synthetic. The repository is
public and a git history cannot be recalled.

Where the system processes what it holds is a separate question. The cloud tier runs in the
EU and is treated as holding personal material on the same terms as the house, so a prompt
may carry a name, a profile, or what came back before. One limit stays, and it is about the
camera rather than the cloud: only the rectified page crop inside the four markers is kept
or sent, never a full frame. See [docs/THREAT-MODEL.md](docs/THREAT-MODEL.md).

## Licence

[MIT](LICENSE). If you fork it and remove the constraints in
[docs/NON-GOALS.md](docs/NON-GOALS.md), please call it something else.
