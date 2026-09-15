# Sequential Material-Correspondence Trials

This study ran notebooks 002 through 006 sequentially on 15 September 2026. The original request was for at least three iterations; two further runs investigated failures found in those trials. The synthetic household and brief stayed the same. Iteration 002 used the starting prompts. Later prompts changed only after review of the preceding output; 005 and 006 used identical prompts. Model sampling and automatic method selection varied, so these observations cannot isolate the effect of a prompt change. The filename retains the original three-run range so earlier notebook links remain valid.

## Review criteria

Each review reads the actual printed images, synthetic written returns, displayed messages and executed transitions. It checks whether the first action is understandable without the script, whether names and objects remain consistent, whether a returned detail changes the next task, whether successive actions differ in a useful way, and whether the closing response follows from the work. A printed task must provide its own evidence and instructions.

The review distinguishes an execution result from an editorial judgement. Sheet counts, returned pages, continuation calls and elapsed seconds come from saved artifacts. Statements about likely confusion or repetition name the offending page or sentence. They are not measurements of adolescent enjoyment, ability or comprehension. Synthetic handwriting may fail to follow instructions and cannot stand in for human feedback.

The same workbench compares generated originals with synthetic marked images. It does not exercise camera perspective, a physical printer, display delivery or household waits. Continuations receive the original approved document rather than accumulated execution history. These limits stay in force across the runs.

## Iteration records

### 002: Unchanged Baseline

The run stopped after one printed page and one return. Both continuation responses were cut at exactly 9,000 characters, inside a JSON string. The measured model-path run took 316.597 seconds; the whole notebook took 331.7 seconds. The blank-page control passed. The failed notebook and output are retained in [002-baseline.ipynb](002-baseline.ipynb) and [its run directory](runs/002-baseline-20260915T141413362771Z/verification.json).

The first page, "Il confine senza luogo", asks for "metà; otto tratti; due impronte; un varco" without explaining those choices. It then asks for a pact and a deviation. The large decorative sea leaves the actual tracing box small. The synthetic return does not visibly select an option and interprets the pact as a territorial rule. The eastern rock and the calm moving water could support a reply, but none reached the page. Coherence across exchanges, variety and closure cannot be assessed from the promised script.

Before 003, the continuation transport ceiling was raised from 9,000 to 20,000 characters, matching the deviser's existing budget. The deviser prompt was changed to spell out operations and preserve established names, positions and rules. This addresses a transport failure separately from editorial quality.

### 003: Concrete Actions

The run stopped after one printed page and one return. The continuation parsed, but the text check rejected "strada / percorso", wording copied from the return. The measured model-path run took 288.771 seconds; the notebook took 300.7 seconds. The blank-page control passed. Evidence is retained in [003-concrete-actions.ipynb](003-concrete-actions.ipynb) and [its run directory](runs/003-concrete-actions-20260915T142416846842Z/walk.json).

"Carta del Canale Stretto" makes the drawing tasks more explicit, but combines three places, two symbols, meanings and a limitation of the code on the first sheet. The large canal is almost untouched; the actual drawings go in three boxes below it. The returned image writes meanings but does not clearly draw the two requested symbols. The reader reports those meanings without symbol shapes. A continuation that assumes the code already exists would skip unfinished work. Again, no second page or ending was delivered.

Before 004, the deviser prompt was changed to distribute work across exchanges and put the contribution on the useful drawing surface. The continuer was asked to distinguish reported symbol shapes from written meanings, preserve established details, and express slash-separated alternatives in prose. The slash heuristic remains a brittle application check: this prompt adjustment avoids its known rejection without establishing that every future quotation will pass.

### 004: Distributed Work

The run concluded with four sheets, three synthetic returns, three continuations and nine executed moments. The model-path measurement was 498.611 seconds; notebook execution took 510.1 seconds. All notebook checks passed, including the blank control. Evidence is in [004-distributed-work.ipynb](004-distributed-work.ipynb) and [its verification](runs/004-distributed-work-20260915T143118602766Z/verification.json).

The first sheet gives the drawing most of the page and asks for a boundary with an opening. The next sheet uses the returned name "La Fessura Azul". The chosen R1 rule, entering along a curve, becomes a route task on the third sheet. "Punta del Faro" and the drawn lighthouse and pier reappear. These are real links between contributions and replies, although the illustrations do not preserve exact geography. The sequence changes from boundary to nearby place to route, then closes.

The result still has substantive defects. The first sheet offers "Vero / Non del tutto" without a proposition. Its returned boundary has no visible opening; the reader describes a continuous line, but the next sheet treats an opening as established. The third sheet puts both endpoints inside a boundary while asking to test its three entrances, without saying whether paths can be invented or why leaving the boundary is required. The synthetic return checks a box and claims success without drawing a route. The closing sheet depicts a completed route and says the map allows passage. That upgrades a claim into visible evidence which the reader never reported.

The progression is more usable than the preceding first pages, but completing the software path does not make this a well-posed route puzzle. Before an additional 005 run, the prompts were changed to require complete propositions and route rules, and to distinguish reported claims from visible work, including in the final illustration. This additional run was added because the third trial revealed defects after technically successful completion.

### 005: Evidence And Complete Tasks

The run stopped after one sheet and one return. Azure Content Safety rejected a 10,181-character request against its 10,000-code-point service maximum. Nothing unscreened was delivered. Model-path time was 258.919 seconds; notebook time was 267.5 seconds. Evidence is in [005-visible-evidence.ipynb](005-visible-evidence.ipynb) and [its walk](runs/005-visible-evidence-20260915T144144613823Z/walk.json).

The first page names the left and right gates, asks for an invented road through at least three zones, and gives a useful drawing surface. The returned "Borgo al Sole" uses that surface and supplies a road and named places. The first action is clearer, but three places and a legend still concentrate work on the first sheet. The plan uses one content-driven continuation and prewrites later exchanges. This limits responsiveness to later material, but those later pages were never delivered and are not scored as observed output.

Before 006, the safety gate was changed to examine long text in windows of at most 10,000 Unicode code points, overlapping by 512. It retains the maximum severity for each category and seals the unchanged full body only after every request succeeds. A refusal or service failure prevents delivery. The overlap preserves local context at boundaries but cannot give the service unlimited cross-document context. The cost is additional screening requests for long documents. A separate live probe subsequently screened 10,181 neutral characters successfully in 4.0 seconds of measured command time. Local tests cover full coverage, Unicode, boundary and tail refusals, and an error in a later request.

### 006: Screened Continuation

The run concluded with two sheets, two synthetic returns, one continuation and five executed moments. Model-path time was 361.797 seconds; notebook time was 375.1 seconds. Evidence is in [006-screened-continuation.ipynb](006-screened-continuation.ipynb) and [its verification](runs/006-screened-continuation-20260915T144851952272Z/verification.json). All current assertions passed, but they accept two returns; the brief asked for at least three meaningful exchanges. This is software completion, not full brief compliance.

The first task measures a known room instead of starting with an invented place. The second page preserves the reported door at right, window at top and table. It develops three marks on the table into a fictional restriction. This is a concrete response, but "margine invalicabile" and "se serve, apri un varco" leave that restriction unclear. The last message was generated before the second return and does not mention the new name "ISOLA". The synthetic redraw also simplifies the original room. The workbench's references are original pages rather than previous filled images, which limits conclusions about that drift.

## Results

The measurements below come from saved walks, verification records and executor output. Returns count written synthetic pages; continuation counts include only accepted continuations. Blank-page controls passed in every run. Notebook time includes its local checks and output handling. No time is an estimate of human play duration.

| Run | Execution | Sheets | Returns | Continuations | Model-Path Seconds | Notebook Seconds |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| 002 | Stopped: truncated JSON | 1 | 1 | 0 | 316.597 | 331.7 |
| 003 | Stopped: slash heuristic | 1 | 1 | 0 | 288.771 | 300.7 |
| 004 | Concluded; editorial defects remain | 4 | 3 | 3 | 498.611 | 510.1 |
| 005 | Stopped: safety request too long | 1 | 1 | 0 | 258.919 | 267.5 |
| 006 | Concluded; only two exchanges | 2 | 2 | 1 | 361.797 | 375.1 |

The five new runs contain two concluded paths and three retained failures. Including the earlier 001 notebook, Officina now contains three concluded paths in six executions, but 001 predates this iterative study and 006 falls short of this brief's exchange count. The study must not be described as three successful new games.

## Authored Comparison

[L'isola della strada sommersa](authored-example.md) supplies complete printed text, four display messages, three hypothetical returns and an explicit final response. A road leads to a workshop; flooding makes that route unusable; the participant proposes a boat; a cargo choice develops that proposal; the closing cover records the design. The text keeps proposed work distinct from completed events. It has not been rendered or tried with a person.

| Criterion | 002 | 003 | 004 | Authored Example |
| --- | --- | --- | --- | --- |
| First action | Unexplained options and abstract terms | Concrete drawing requests, too many at once | Clear boundary action; unexplained truth checkbox | One route and one invented place |
| Consequence of a return | Not delivered | Not delivered | Returned name, landmark and rule change later pages | Workshop, boat and packing choice each determine a reply |
| Coherence | Only one page observed | Only one page observed | Recognisable sequence; an unreported opening and route are supplied | Original map remains intact; later sheets are explicit working notes |
| Variety | Unobserved | Unobserved | Boundary, place, route, cover | Geography, transport, construction choice, cover |
| Closure | Not reached | Not reached | Explicit but overstates visible work | Closes a proposed design without claiming a completed delivery |

The later 005 first page approaches the example's concrete instructions, but its continuation was not delivered. The 006 run shows a different problem: it keeps some spatial facts yet compresses the correspondence and closes before responding to the latest named contribution. More words about continuity in a prompt do not reliably solve that.

## Assessment

The strongest observed moment is in 004: "Punta del Faro" and the chosen entry rule become material for the next page. This demonstrates a useful correspondence mechanism. The weakest recurring pattern is that the generated game asks for names, rules, legends and forms before giving those contributions a necessary consequence. Some attractive pages still contain an undefined question or an assumed result.

I prefer the authored example as a candidate for a physical trial because the choices have an immediate purpose and the ending accounts for the actual proposed work. That is an editorial preference, not evidence that an adolescent would enjoy it more. The example benefits from having all replies written in advance and narrows the activity around a practical problem; a person wanting free map-making may prefer more latitude.

The prompt revisions produced some clearer pages but not a monotonic improvement, reliable compliance with the brief or a consistently responsive ending. The current workbench needs stronger evaluation of the requested exchange count and of replies that actually use the latest material. Runtime history remains a separate limitation. Further model sampling alone would not establish enjoyment. A physical trial of a concrete candidate would now provide evidence these synthetic runs cannot.
