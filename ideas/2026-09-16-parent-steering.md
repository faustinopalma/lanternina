# Parent-controlled activity guidance

On 16 September 2026 the owner requested two editable guidance texts shared by planning and execution. Both start from neutral defaults. One is changed only by the parent. The other accumulates a synthesis of rejection feedback and remains editable by the parent, with an explicit indication that later feedback can update it. This replaces hidden assumptions about difficulty or disability with visible instructions about what the activity should ask somebody to do.

The feedback reasons describe proposed activities: too difficult, too easy, too abstract, too closed, too open, unclear, too much reading, too much writing, too much adult help, and not interesting. A free comment supplies conditions and examples. Difficulty and openness are separate: a demanding task may still need a precise goal. Opposite directions on the same axis cannot be selected for one rejection. No diagnosis, scalar ability label or automatic assessment is needed to use these controls.

## State and synthesis

Guidance occupies one `steering-<household>` document in the existing `sources` container, partitioned by `familyId`. The stable text, adaptive text and pending feedback share a revision. Writes compare both the application revision and the Cosmos ETag. A synthesis computed before a parent edit or reset cannot replace the newer document. Empty text is an explicit parent choice; restoring a default is a separate action.

Rejections keep their decision before feedback synthesis starts. Feedback is persisted before calling the model; a failed call leaves it pending for retry. Saving a configuration never contacts a device. The synthesis calls the existing Foundry router, counts against household usage and is not an activity-generation call. It receives the current adaptive text and new feedback, preserves relevant earlier guidance, and outputs only a bounded text. The stable direction and safety constraints remain outside its write authority. A synthesis is fallible: the parent can inspect, edit or clear the result.

The pending queue accepts at most 50 feedback items. The summary carries accumulated guidance; the 50 most recently incorporated items remain as history. These are development bounds, not measures of learning. Identical retries are deduplicated while their items are retained. Resetting the adaptive field clears both pending items and retained history so old comments cannot regenerate the deleted guidance. A decision and a feedback record live in separate store documents: if feedback persistence fails after rejection, the API reports `rejected_feedback_not_saved` and the rejection remains in effect.

## Verification

The focused tests cover household separation, neutral defaults, edits and resets, Cosmos conditional writes, conflicting feedback directions, summary failure and a reset during synthesis. Production prompts and portal integration are the next implementation steps. No real household settings have been changed by these tests.
