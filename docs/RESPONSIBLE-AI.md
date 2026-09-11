# Responsible generative AI

Lanternina uses generative AI to propose activities for an adolescent, produce printed pages and interpret returned material. This preliminary assessment considers the effects on the adolescent, the parent and other people whose information may appear in that material. It draws on Microsoft's responsible AI guidance and the implementation documented on 11 September 2026.

## Activities and participation

Generated instructions can ask someone to handle tools or materials. Their physical safety depends on the action, the available equipment and the conditions in the home. Parental approval and content screening address parts of this risk, with different scopes.

The assessment also considers participation and treatment of the adolescent. Reading, visual and motor demands can make an activity inaccessible. Generated feedback can introduce stereotypes, humiliation or pressure to continue. Reviewing the proposed material can reveal some of these problems; observing an afternoon is needed to understand how the person experiences it.

## Mitigations in place

| Concern | Implemented mitigation | Scope and limit |
| --- | --- | --- |
| An activity reaches the home without parental agreement. | The device retrieval route returns only approved activities that have not begun. Withdrawing approval removes an activity from that list. | This controls initial delivery. It does not recall downloaded material or add parental review of later pages and continuations. |
| Generated text contains harmful content. | Activity and continuation text passes through Content Safety before it is returned. A refusal blocks the whole result. The configured detectors cover hate, self-harm, sexual content and violence. | Screening includes the words collected from the activity's moments and, for an initial activity, its title and overview. These categories do not assess the physical suitability of tools or materials in a home. |
| Text directs blame or pressure at the adolescent. | Local pattern checks reject identified formulations of blame, hurry and personal judgments before storage. The outgoing display-text check substitutes text already written in the plan when a proposed string is refused. | These are targeted language checks. They can miss equivalent wording and do not assess every meaning in an image or sentence. |
| A photograph reaches another household or reappears after deletion. | The parent photo routes use the authenticated household. Deletion records prevent a later upload of the same photograph from restoring it. The parent can delete one photo, a confirmed date range or the current selection of all photos. | This protection concerns the photo archive. It does not establish erasure of every derived reading or household record. |

The implementation is in [activity retrieval](../panel/routes/experience.py), [content screening](../orchestrator/safety.py), [continuation generation](../panel/continuing.py), [language patterns](../shared/blocklist.py), [outgoing text](../orchestrator/outgoing.py) and [photo routes](../panel/routes/photos.py). These controls are already part of the software; their effectiveness in household use remains to be measured.

## Readings and memory

Lanternina interprets returned material and uses the reading in continuations and memory. Photographs and handwriting can be ambiguous. Retained originals allow a reading to be checked against its source and traced into later proposals.

A relevant concern is whether a description of one sheet becomes an unsupported judgment about the adolescent's ability, intent or wellbeing. The material documents a particular activity and provides limited grounds for such conclusions. Evaluation of the reading therefore includes how it is used in subsequent interactions.

## Household data

Photographs can include people, words or belongings unrelated to the activity. The archive's access and deletion controls protect that material. Retained originals also allow the family to compare a model interpretation with what was actually returned.

During development, photographs, returned material, readings and diagnostics may be retained and shown to the authenticated family, as authorized on 9 September 2026. This supports comparison of original material with generated interpretations. Retention policy will be reviewed after development.

## Evidence and further assessment

The [activity-route tests](../tests/test_experience_route.py) cover approval, withdrawal and refusal of blocked generations. The [screening tests](../tests/test_continuation_safety.py) cover the text sent to the gate and rejection of the whole result. The [photo tests](../tests/test_photos.py) cover cross-household access and deletion followed by an upload retry. These tests exercise application behavior with test clients and substitutes, rather than measuring the live detector's accuracy.

The [workbench](../research/README.md) and [architecture record](ARCHITECTURE.md#verified-and-unverified) document further functional and synthetic checks. The remaining assessment concerns detection coverage, physical suitability, participation and consequences during household use. The available evidence does not quantify their likelihood or severity.

Further evaluation would examine complete activities, from the approved proposal to the continuation, against the concerns described above. Useful records include the household conditions, generated material, controls that intervened and consequences observed. Quality defects, potentially harmful outputs and observed harms would be recorded separately, with the evaluated cases and software and model versions stated.

Response during use also needs examination. A dangerous instruction already printed remains with the family after a software correction. Handling that situation includes identifying the affected material and informing the family. The [deployment procedure](DEPLOY.md) covers technical operations; an exercised AI incident response procedure remains undocumented.

## Sources

Microsoft's guidance informed the identification of concerns, the review of controls and the assessment of remaining evidence. Sources consulted on 11 September 2026:

- [Microsoft Learn, Map potential harms][map]: context and consequences.
- [Measure potential harms][measure] and [Mitigate potential harms][mitigate]: evaluation criteria and controls.
- [Azure OpenAI responsible AI guidance][overview]: application safeguards and operation.

[map]: https://learn.microsoft.com/en-us/training/modules/responsible-ai-studio/3-identify-harms
[measure]: https://learn.microsoft.com/en-us/training/modules/responsible-ai-studio/4-measure-harms
[mitigate]: https://learn.microsoft.com/en-us/training/modules/responsible-ai-studio/5-mitigate-harms
[overview]: https://learn.microsoft.com/en-us/azure/foundry/responsible-ai/openai/overview
