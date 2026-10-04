# Lanternina uses a shared Foundry

The owner requested centralization on 4 October 2026 so other projects can use the same model deployments. The shared account is `ai-shared-720467d019e0` in `rg-shared-ai`, Sweden Central. Sharing makes the allocated quota available to callers from several applications; it also lets one application's traffic consume capacity needed by another. It does not increase the subscription's quota.

The old account, `ai-lanternina-dev-ssveb`, held six deployments. The shared account already held equivalent copies of Astra and Cohere Embed. Their model versions, SKU, capacity, content filter and upgrade policy matched, so those copies were reused without an update. Sol, Terra, Luna and GPT Image 2 were deleted from the source and recreated sequentially on the destination, after saving their contracts locally. Each destination was read back and checked before the next transfer.

| Deployment | Version | SKU | Assigned capacity |
| --- | --- | --- | --- |
| `gpt-5.6-sol-2026-07-09` | `2026-07-09` | GlobalStandard | 1,000,000 tokens/minute |
| `gpt-5.6-terra-2026-07-09` | `2026-07-09` | GlobalStandard | 1,000,000 tokens/minute |
| `gpt-5.6-luna-2026-07-09` | `2026-07-09` | GlobalStandard | 1,000,000 tokens/minute |
| `gpt-image-2-2026-04-21` | `2026-04-21` | GlobalStandard | 2 requests/minute |
| `lab-gpt-6-astra-20260919` | `2026-09-03` | GlobalStandard | 100,000 tokens/minute |
| `embed-v-4-0` | `1` | GlobalStandard | 1,000 tokens/minute |

These are assigned rate limits read from Azure deployment and usage APIs, not measured sustained throughput. Sol, Terra, Luna and GPT Image 2 consumed their full quota before and after the move. Every deployment retained `Microsoft.DefaultV2`. OpenAI deployments retained `NoAutoUpgrade`; Cohere retained `OnceNewDefaultVersionAvailable`.

The runtime identity keeps its existing client ID. It receives OpenAI inference access at shared-account scope, a custom role for Content Safety and MaaS text and image embeddings, and Foundry User on the new `lanternina-dev` project. The owner's research identity receives the same access, preserving local inference that had been authorized on the source account. Neither identity receives account-key or cross-project-secret access through these account-level assignments. Authentication, household isolation, application images and model selections were left unchanged. The API kept Astra as its primary model; the worker kept Sol. The worker was already running the demonstration image, so its healthy revision is a configuration check rather than proof of a production worker implementation.

The API moved from revision `0000143` to `0000144`; the worker moved from `0000002` to `0000003`. A before/after comparison checked all unrelated environment values and secret references. Both revisions became healthy. Tests from the API container used its managed identity and the live environment: Astra, Sol, Terra and Luna answered synthetic chat requests; GPT Image 2 produced a valid 1024 by 1024 pixel PNG of 239,336 bytes; Content Safety returned its four categories at severity zero for both synthetic text and that image. These checks exercise connectivity and authentication, not the quality of generated activities or safety-classifier accuracy.

The Bicep AI module now references an existing account and manages only Lanternina's project and access. A future application deployment cannot recreate the dedicated account or reset shared deployment capacity. The research environment and embedding probe also point to the shared account. Local migration snapshots remain under the ignored `.azure/` directory.

Cohere initially rejected inference after the generic text and image embedding permissions were granted. Adding the provider's `Microsoft.CognitiveServices/accounts/MaaS/v1/embed/action` operation resolved that second authorization check. A text request from the owner's local identity and a synthetic image request from the API's managed identity each returned one vector with 1,536 dimensions. The custom role therefore includes all three embedding operations. Changing the token audience alone did not resolve the rejection.

Before deletion, the source project returned empty lists for connections, capability hosts, assistants, files and vector stores. The source account retained only its duplicate Astra and Cohere deployments. The project was deleted first, followed by the dedicated account. Fresh resource checks confirmed deletion; no purge was requested. The shared account and all six deployment contracts remained healthy, both Container Apps retained their shared endpoints, and the API health endpoint returned `ok` after deletion.

The first usage read after account deletion still counted 200 Astra capacity units and two Cohere units, although the shared deployments hold 100 and one respectively. Azure's [quota guidance](https://learn.microsoft.com/azure/foundry/openai/how-to/quota#resource-deletion) explains that programmatic account deletion retains deployment quota for 48 hours until purge. The duplicate allocations remain recoverable during that period. Sol, Terra, Luna and Image 2 were deleted individually before transfer, so their full allocations are already on the shared account. No immediate purge was needed for this migration.

Local checks passed: Bicep compilation, Ruff, 1,291 Python tests with two skips, 220 panel tests, and the panel production build. Prompt snapshots were regenerated before publication. These tests cover the current working tree, including application changes that preceded the migration; the live inference checks above used the application image that was running during the move.