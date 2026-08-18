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

// The existing Static Web App was placed in eastus2 after the European region rejected
// creation for capacity. Its location cannot change without replacing the resource.
param webLocation = 'eastus2'

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

// Live catalog and quota measured in Sweden Central on 8 August 2026. Standard
// deployments are billed on use; these capacities allocate existing rate-limit quota.
param aiFrontierModelNames = [
	'gpt-5.6-sol'
	'gpt-5.6-terra'
	'gpt-5.6-luna'
]
param aiFrontierModelVersion = '2026-07-09'
param aiFrontierModelSku = 'GlobalStandard'
param aiFrontierModelCapacity = 1000

param aiImageModelName = 'gpt-image-2'
param aiImageModelVersion = '2026-04-21'
param aiImageModelSku = 'GlobalStandard'
param aiImageModelCapacity = 2
