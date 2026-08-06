// Committed defaults for the dev environment.
//
// Nothing here is tenant-specific on purpose: no tenant id, no subscription id, no object
// id, no email. The subscription comes from the CLI context and the two personal values
// (owner, budget contact) are supplied by scripts/deploy.ps1 at run time.
//
// A fork of this repository can deploy with this file unchanged.

using './main.bicep'

param projectName = 'lanternina'
param environmentName = 'dev'
param location = 'swedencentral'

// The only resource that cannot live in swedencentral: the Standard SKU is not offered
// there. Everything else stays out of westeurope, which has capacity constraints.
param webLocation = 'westeurope'

// Disabled is the intended posture. The private endpoints are created either way, so
// flipping this to 'Enabled' is how you reach Cosmos from a laptop during development.
param dataPublicNetworkAccess = 'Disabled'

param deployExternalId = true
param externalIdDisplayName = 'Lanternina External'
param externalIdCountryCode = 'IT'

// Left empty so the domain is derived from the project name plus a per-subscription
// hash. Set it only if you want a specific <prefix>.onmicrosoft.com. Max 10 characters.
param externalIdDomainPrefix = ''

param monthlyBudgetAmount = 50
