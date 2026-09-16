# Responsible AI documentation

On 11 September 2026, the owner requested Microsoft responsible generative AI guidance in the documentation and a final page in the site's navigation, without constraining code development. After the source review, the owner asked for a contextualized chapter rather than a comparison of frameworks or a research proposal.

The [chapter](../docs/RESPONSIBLE-AI.md) is a preliminary assessment of activities, participation, readings, memory and household data. It records the concerns considered, the controls present and the evidence still needed. The owner clarified that distinguishing errors from harm belongs in evaluation criteria, rather than an opening argument addressed to a reader who has made no such claim. The chapter begins with the application and the scope of the assessment.

The public page follows the existing English and Italian routes and shared layout, after current implementation. The documentation includes implementation references and further evaluation considerations; the public page presents the assessment more briefly. This gives each reader a suitable level of detail, at the cost of maintaining consistency between them. No application behavior, prompt, retention rule or deployment gate changes. Publication to the live site remains a separate action.

Completion checks cover local document links, the Astro build, the existing site link and language-metadata checker, and desktop and mobile inspection. These verify the documentation delivery, not the safety of generated activities.

## Learning and dependency, 16 September 2026

The owner asked for the educational purpose to appear at the beginning of the Responsible AI chapter. Lanternina aims to help refine cognitive skills. Engaging experiences should support learning through a balanced level of effort, with difficulty and support suited to the participant. Their appeal must not become an end in itself or be used to create another dependency.

The English documentation and both public language versions now state this purpose before the risk assessment. They connect it to observation, reasoning, decision-making and the freedom to stop. The wording preserves the educational ambition while leaving its effectiveness open to assessment: enjoyment and time spent alone do not demonstrate a cognitive benefit.

This update changes documentation only. Publication uses the existing `site` workflow on a push to `main`, followed by a check of both live language versions. The local Astro build completed with no errors or warnings, and the existing build checker passed for all 16 generated pages.
