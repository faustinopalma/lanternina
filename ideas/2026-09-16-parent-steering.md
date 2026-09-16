# Parent-controlled activity guidance

On 16 September 2026 the owner requested two editable guidance texts shared by planning and execution. Both start from neutral defaults. One is changed only by the parent. The other accumulates a synthesis of rejection feedback and remains editable by the parent, with an explicit indication that later feedback can update it. This replaces hidden assumptions about difficulty or disability with visible instructions about what the activity should ask somebody to do.

The feedback reasons describe proposed activities: too difficult, too easy, too abstract, too closed, too open, unclear, too much reading, too much writing, too much adult help, and not interesting. A free comment supplies conditions and examples. Difficulty and openness are separate: a demanding task may still need a precise goal. Opposite directions on the same axis cannot be selected for one rejection. No diagnosis, scalar ability label or automatic assessment is needed to use these controls.

## State and synthesis

Guidance occupies one `steering-<household>` document in the existing `sources` container, partitioned by `familyId`. The stable text, adaptive text and pending feedback share a revision. Writes compare both the application revision and the Cosmos ETag. A synthesis computed before a parent edit or reset cannot replace the newer document. Empty text is an explicit parent choice; restoring a default is a separate action.

Rejections keep their decision before feedback synthesis starts. Feedback is persisted before calling the model; a failed call leaves it pending for retry. Saving a configuration never contacts a device. The synthesis calls the existing Foundry router, counts against household usage and is not an activity-generation call. It receives the current adaptive text and new feedback, preserves relevant earlier guidance, and outputs only a bounded text. The stable direction and safety constraints remain outside its write authority. A synthesis is fallible: the parent can inspect, edit or clear the result.

The pending queue accepts at most 50 feedback items. The summary carries accumulated guidance; the 50 most recently incorporated items remain as history. These are development bounds, not measures of learning. Identical retries are deduplicated while their items are retained. Resetting the adaptive field clears both pending items and retained history so old comments cannot regenerate the deleted guidance. A decision and a feedback record live in separate store documents: if feedback persistence fails after rejection, the API reports `rejected_feedback_not_saved` and the rejection remains in effect.

## Agent integration

The same two texts now reach method selection, activity planning, continuation, the next-action runner and parent-authored draft editing and approval. `shared/steering.context.md` gives stable parent instructions precedence over the adaptive synthesis. Returned material cannot change those instructions. Safety, household bounds, available equipment, approved scope and output contracts still apply.

Current production routes no longer render the historical profile pitch or infer task load from completion counts. Returned-page reading remains available; the automatic second call that assigned load and ink levels has been removed from that route. Legacy function arguments and historical profile calculations remain for older callers, but they do not enter current activity prompts. Explicit parent guidance can request prerequisites, support, arithmetic, extended writing, closed problems or open work. The neutral defaults prescribe none of those as a property of a person.

Planning no longer requires a returned page or a model-written continuation. An activity can complete without either. The existing limit of one deferred continuation remains a bound on model calls. A blank page alone does not mean that the participant wants to stop. These changes allow more activity forms; the existing page and runner contracts still limit how an activity can be represented and delivered.

## Operational defaults

The owner found that the first stable default read as guidance for the parent rather than a usable model prompt. The Italian and English defaults now instruct the model to design and conduct the activity. They specify a meaningful goal, a starting action, complete task material, declared prerequisites, checked solutions, criteria for open work, evidence-based feedback, relevant help and closure. They leave genre, knowledge requirements and response form open to the task and explicit parent choices. They do not require a story, a photographed return or a continuation.

Putting these decisions in the visible default gives the parent an editable starting prompt; it also makes that field longer to inspect. The static context continues to establish precedence and preserve safety, equipment, household bounds and approved scope. A default update does not overwrite saved household instructions. Restoring the stable default explicitly adopts the new text while preserving the feedback synthesis. These are prompt-design decisions, not measured improvements in model output.

## Parent interface

The configuration section is called Activity guidance, or Indicazioni per le attività. It contains the two editable texts, default restoration, adaptive reset and the existing household context and bounds. Saving sends only deliberately changed fields. A revision conflict leaves the parent's draft intact. Refresh preserves edited fields and updates untouched fields; the parent can inspect the newly saved version before retrying. Reset and default restoration require confirmation and are disabled while unsaved changes exist.

Single and bulk rejection collect reason checkboxes and an optional comment. Rejection also works without either. Opposing reasons exclude each other. Failed writes retain the form. Pending feedback has an explicit synthesis retry control; a subsequent refresh reads the result. The interface does not poll for synthesis completion. Comments are limited to 2,000 characters; stable and adaptive texts are limited to 6,000 and 3,000 characters respectively. These bounds are storage and generation controls, not recommended text lengths.

## Verification

The full offline Python regression passed 1,146 tests with two skips in 145.24 seconds before the final optional-continuation wording change. After that change, the focused planning and steering check passed 38 tests in 2.38 seconds. All 16 rendered prompts were regenerated, and their 17 snapshot checks passed in 0.57 seconds. Focused tests cover household separation, neutral defaults, guidance propagation, edits and resets, Cosmos conditional writes, conflicting feedback directions, summary failure and a reset during synthesis. No real household settings were changed by these tests.

The frontend regression passed 166 tests in 30.12 seconds. A subsequent API response-shape check passed with the guidance editor tests, 14 tests in 4.27 seconds. The production TypeScript and Vite build passed. Vite still warns that the shared JavaScript chunk exceeds its 500 kB warning threshold.

Local Edge checks used the dev-only synthetic preview at 1440 by 1000 pixels and 390 by 844 pixels. They exercised editing, saving, refreshing, adaptive reset, navigation, opposite rejection reasons, and single and bulk rejection. Screenshot inspection found a mobile overflow in the bulk-decision buttons. Allowing those buttons to wrap removed it; the repeated browser check passed with no JavaScript errors or horizontal page overflow. These checks do not verify a real authenticated household session, live synthesis quality, image generation or physical delivery.

## Varied references

Four additional authored references in `officina/authored-examples/` pair explicit stable instructions with invented adaptive guidance. They cover a minimum-cost calculation, a unique ordering problem, the limits of a causal inference from numerical data, and an 80-120-word scene with a local revision. The first two have finite answer checks. The third separates exact arithmetic from an underdetermined cause. The fourth gives writing a clear goal while preserving several valid outcomes. Each uses one printed brief and permits completion without returning a photograph; the example continuations apply only when feedback is requested.

The checker now validates 14 references and 26 page/prompt pairs. It also checks the new examples' minimum cost, unique order, means and word count. It caught a mistaken 87-word claim in the authored scene; the measured count is 88. The original ten examples retain their declared assumptions and are not injected into production prompts. None of these references establishes how a live model or participant will respond.

## Publication

Commit `500cebf` published persistence and synthesis. Commit `9b89a26` published the agent and portal integration. Its GitHub Actions runs completed successfully on 16 September 2026: Python ran 1,148 tests in 35.52 seconds and Ruff passed; the panel ran 167 tests in 19.12 seconds and completed its production build and Static Web Apps deployment. The API workflow confirmed the image tag `9b89a26` and an HTTP 200 health response. Deployment does not establish that a real household has exercised the new controls or that live synthesis has the intended quality.
