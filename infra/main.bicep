// Lanternina — subscription-scope entry point.
//
// Nothing tenant-specific is hardcoded anywhere in this tree: no tenant id, no
// subscription id, no object id. That is what makes moving to a different tenant a
// redeploy rather than a migration — see docs/DEPLOY.md.
//
// Resource groups are split by LIFETIME, not by layer:
//   core     plumbing that outlives the app (network, registry, logs, identities)
//   data     the precious one (Cosmos, queue). Deleting this loses families.
//   app      disposable (Container Apps environment and the two apps)
//   web      the Static Web App, which must live outside swedencentral
//   identity the Entra External ID directory, which migrates differently from the rest

targetScope = 'subscription'

@description('Short project name. Becomes part of every resource name.')
@minLength(3)
@maxLength(12)
param projectName string = 'lanternina'

@description('Environment discriminator, e.g. dev / prod.')
@minLength(2)
@maxLength(6)
param environmentName string = 'dev'

@description('Region for everything except the Static Web App.')
param location string = 'swedencentral'

@description('Static Web App region. The Standard SKU is not offered in swedencentral.')
param webLocation string = 'westeurope'

@description('Who owns this deployment. Only used as a tag.')
param owner string = 'unknown'

@description('Public network access for the data tier. Disabled is the intended posture; the private endpoint is created either way.')
@allowed(['Enabled', 'Disabled'])
param dataPublicNetworkAccess string = 'Disabled'

@description('Create the Entra External ID directory. Set false when reusing an existing one.')
param deployExternalId bool = true

@description('Domain prefix for the External ID tenant. Must be globally unique; the tenant becomes <prefix>.onmicrosoft.com.')
param externalIdDomainPrefix string = ''

@description('Display name of the External ID tenant.')
param externalIdDisplayName string = 'Lanternina External'

@description('ISO 3166-1 alpha-2 country for the External ID tenant. Determines data residency and cannot be changed later.')
param externalIdCountryCode string = 'IT'

@description('Monthly budget in the billing currency. An alert fires at 50/80/100 per cent.')
param monthlyBudgetAmount int = 50

@description('Address that receives budget alerts. Empty disables the budget.')
param budgetContactEmail string = ''

// Deterministic across redeploys, and different per subscription+environment, so two
// forks of this repo never collide on a globally-unique name.
var suffix = take(uniqueString(subscription().id, projectName, environmentName), 5)

var tags = {
  project: projectName
  env: environmentName
  owner: owner
  managedBy: 'bicep'
  repo: 'github.com/faustinopalma/lanternina'
}

var rgCoreName = 'rg-${projectName}-${environmentName}-core'
var rgDataName = 'rg-${projectName}-${environmentName}-data'
var rgAppName = 'rg-${projectName}-${environmentName}-app'
var rgWebName = 'rg-${projectName}-${environmentName}-web'
var rgIdentityName = 'rg-${projectName}-${environmentName}-identity'

resource rgCore 'Microsoft.Resources/resourceGroups@2024-11-01' = {
  name: rgCoreName
  location: location
  tags: tags
}

resource rgData 'Microsoft.Resources/resourceGroups@2024-11-01' = {
  name: rgDataName
  location: location
  tags: tags
}

resource rgApp 'Microsoft.Resources/resourceGroups@2024-11-01' = {
  name: rgAppName
  location: location
  tags: tags
}

resource rgWeb 'Microsoft.Resources/resourceGroups@2024-11-01' = {
  name: rgWebName
  location: webLocation
  tags: tags
}

resource rgIdentity 'Microsoft.Resources/resourceGroups@2024-11-01' = if (deployExternalId) {
  name: rgIdentityName
  location: location
  tags: tags
}

module core 'modules/core.bicep' = {
  scope: rgCore
  name: 'core'
  params: {
    projectName: projectName
    environmentName: environmentName
    location: location
    suffix: suffix
    tags: tags
  }
}

module data 'modules/data.bicep' = {
  scope: rgData
  name: 'data'
  params: {
    projectName: projectName
    environmentName: environmentName
    location: location
    suffix: suffix
    tags: tags
    publicNetworkAccess: dataPublicNetworkAccess
    privateEndpointSubnetId: core.outputs.privateEndpointSubnetId
    cosmosDnsZoneId: core.outputs.cosmosDnsZoneId
    queueDnsZoneId: core.outputs.queueDnsZoneId
    runtimeIdentityPrincipalId: core.outputs.runtimeIdentityPrincipalId
  }
}

module app 'modules/app.bicep' = {
  scope: rgApp
  name: 'app'
  params: {
    projectName: projectName
    environmentName: environmentName
    location: location
    suffix: suffix
    tags: tags
    infrastructureSubnetId: core.outputs.acaSubnetId
    logAnalyticsCustomerId: core.outputs.logAnalyticsCustomerId
    logAnalyticsId: core.outputs.logAnalyticsId
    registryLoginServer: core.outputs.registryLoginServer
    runtimeIdentityId: core.outputs.runtimeIdentityId
    runtimeIdentityClientId: core.outputs.runtimeIdentityClientId
    cosmosEndpoint: data.outputs.cosmosEndpoint
    cosmosDatabaseName: data.outputs.cosmosDatabaseName
    storageAccountName: data.outputs.storageAccountName
    workQueueName: data.outputs.workQueueName
  }
}

module web 'modules/web.bicep' = {
  scope: rgWeb
  name: 'web'
  params: {
    projectName: projectName
    environmentName: environmentName
    location: webLocation
    suffix: suffix
    tags: tags
  }
}

module identity 'modules/identity.bicep' = if (deployExternalId) {
  scope: rgIdentity
  name: 'identity'
  params: {
    // Capped at 10 characters: see the note on domainPrefix in modules/identity.bicep.
    domainPrefix: empty(externalIdDomainPrefix)
      ? '${take(projectName, 5)}${suffix}'
      : externalIdDomainPrefix
    displayName: externalIdDisplayName
    countryCode: externalIdCountryCode
    tags: tags
  }
}

// A sponsored subscription has a hard credit cap and no policy to stop us reaching it.
module budget 'modules/budget.bicep' = if (!empty(budgetContactEmail)) {
  name: 'budget'
  params: {
    budgetName: 'budget-${projectName}-${environmentName}'
    amount: monthlyBudgetAmount
    contactEmail: budgetContactEmail
    resourceGroupNames: [rgCoreName, rgDataName, rgAppName, rgWebName]
  }
}

output resourceGroups object = {
  core: rgCoreName
  data: rgDataName
  app: rgAppName
  web: rgWebName
  identity: deployExternalId ? rgIdentityName : ''
}
output registryName string = core.outputs.registryName
output registryLoginServer string = core.outputs.registryLoginServer
output apiFqdn string = app.outputs.apiFqdn
output apiAppName string = app.outputs.apiAppName
output workerAppName string = app.outputs.workerAppName
output staticWebAppHostname string = web.outputs.defaultHostname
output staticWebAppName string = web.outputs.name
output cosmosEndpoint string = data.outputs.cosmosEndpoint
output runtimeIdentityClientId string = core.outputs.runtimeIdentityClientId
output deployIdentityClientId string = core.outputs.deployIdentityClientId
output externalIdTenantId string = deployExternalId ? identity!.outputs.tenantId : ''
output externalIdDomain string = deployExternalId ? identity!.outputs.domainName : ''
