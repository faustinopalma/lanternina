// Lanternina — subscription-scope entry point.
//
// Nothing tenant-specific is hardcoded anywhere in this tree: no tenant id, no
// subscription id, no object id. That is what makes moving to a different tenant a
// redeploy rather than a migration — see docs/DEPLOY.md.
//
// Resource groups are split by LIFETIME, not by layer:
//   core  plumbing that outlives the app (network, registry, logs, identities)
//   data  the precious one. Deleting this loses families: their records in Cosmos, and
//         the External ID directory that holds the parents' sign-ins.
//   app   disposable. Container Apps and the Static Web App can be rebuilt from the
//         repository in minutes, and are the tier you would tear down to stop spending.
//
// Three, not one per layer: a group whose only job is to hold a single resource buys
// nothing, and a group per region buys nothing either, since a group's location is only
// metadata about the group.

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

@description('Static Web App region. The existing dev resource was created in eastus2.')
param webLocation string = 'eastus2'

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

@description('Container image for the API. Left at the placeholder, the first deploy succeeds before any build exists.')
param apiImage string = 'mcr.microsoft.com/k8se/quickstart:latest'

@description('Container image for the worker. Left at the placeholder for the first deploy.')
param workerImage string = 'mcr.microsoft.com/k8se/quickstart:latest'

@description('Port the API image listens on. Moves together with apiImage: the placeholder serves on 80, the uvicorn image on 8000.')
param apiTargetPort int = 80

@description('Trust the caller identity from a plain request header. Development only — on an internet-reachable app this lets anyone claim to be anyone.')
param panelDevAuth bool = false

@description('The one address allowed to self-activate, and only while no account is active yet.')
param panelBootstrapContact string = ''

@description('Identity provider base URL. Its discovery document supplies issuer and keys. Empty leaves the panel closed to everyone.')
param panelOidcAuthority string = ''

@description('Exact audience the API accepts. Read this value from a token issued by the configured user flow.')
param panelOidcAudience string = ''

@description('Comma-separated browser origins allowed to call the panel API. Empty allows none.')
param panelAllowedOrigins string = ''

@description('Identity provider for administrators. The workforce tenant, deliberately not the parents\' directory. Empty closes the administration routes.')
param panelAdminOidcAuthority string = ''

@description('Audience the administration routes accept. Comma-separated: Entra emits the bare application id for some configurations and its api:// form for others.')
param panelAdminOidcAudience string = ''

@description('App role an administrator\'s token must carry. Assigned in the directory, so nothing this application writes can grant it.')
param panelAdminRole string = 'Lanternina.Admin'

@description('Shared key the home server presents. Empty closes the device routes, which is the safe direction: the house keeps the picture it has.')
@secure()
param deviceKey string = ''

param aiFrontierModelNames array = [
  'gpt-5.6-sol'
  'gpt-5.6-terra'
  'gpt-5.6-luna'
]

param aiFrontierModelVersion string = '2026-07-09'
param aiFrontierModelSku string = 'GlobalStandard'

@description('Thousands of tokens per minute assigned from existing quota.')
@minValue(1)
param aiFrontierModelCapacity int = 1000

param aiImageModelName string = 'gpt-image-2'
param aiImageModelVersion string = '2026-04-21'
param aiImageModelSku string = 'GlobalStandard'

@description('Images per minute assigned from existing quota.')
@minValue(1)
param aiImageModelCapacity int = 2

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

// The Static Web App lives here too, in a different region. A resource group's location
// is metadata about the group, not a constraint on what it can hold.
resource rgApp 'Microsoft.Resources/resourceGroups@2024-11-01' = {
  name: rgAppName
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
    blobDnsZoneId: core.outputs.blobDnsZoneId
    runtimeIdentityPrincipalId: core.outputs.runtimeIdentityPrincipalId
  }
}

module ai 'modules/ai.bicep' = {
  scope: rgApp
  name: 'ai'
  params: {
    projectName: projectName
    environmentName: environmentName
    location: location
    suffix: suffix
    tags: tags
    runtimeIdentityPrincipalId: core.outputs.runtimeIdentityPrincipalId
    frontierModelNames: aiFrontierModelNames
    frontierModelVersion: aiFrontierModelVersion
    frontierModelSku: aiFrontierModelSku
    frontierModelCapacity: aiFrontierModelCapacity
    imageModelName: aiImageModelName
    imageModelVersion: aiImageModelVersion
    imageModelSku: aiImageModelSku
    imageModelCapacity: aiImageModelCapacity
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
    insightsConnectionString: core.outputs.insightsConnectionString
    registryLoginServer: core.outputs.registryLoginServer
    runtimeIdentityId: core.outputs.runtimeIdentityId
    runtimeIdentityClientId: core.outputs.runtimeIdentityClientId
    cosmosEndpoint: data.outputs.cosmosEndpoint
    cosmosDatabaseName: data.outputs.cosmosDatabaseName
    storageAccountName: data.outputs.storageAccountName
    workQueueName: data.outputs.workQueueName
    blobEndpoint: data.outputs.blobEndpoint
    picturesContainerName: data.outputs.picturesContainerName
    foundryEndpoint: ai.outputs.projectEndpoint
    foundryDeployment: ai.outputs.defaultDeploymentName
    foundryFrontierDeployments: join(ai.outputs.frontierDeploymentNames, ',')
    foundryImageDeployment: ai.outputs.imageDeploymentName
    aiAccountEndpoint: ai.outputs.accountEndpoint
    deviceKey: deviceKey
    apiImage: apiImage
    apiTargetPort: apiTargetPort
    panelDevAuth: panelDevAuth
    panelBootstrapContact: panelBootstrapContact
    panelOidcAuthority: panelOidcAuthority
    panelOidcAudience: panelOidcAudience
    panelAllowedOrigins: panelAllowedOrigins
    panelAdminOidcAuthority: panelAdminOidcAuthority
    panelAdminOidcAudience: panelAdminOidcAudience
    panelAdminRole: panelAdminRole
    workerImage: workerImage
  }
}

module web 'modules/web.bicep' = {
  scope: rgApp
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
  scope: rgData
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
    resourceGroupNames: [rgCoreName, rgDataName, rgAppName]
  }
}

output resourceGroups object = {
  core: rgCoreName
  data: rgDataName
  app: rgAppName
}
output registryName string = core.outputs.registryName
output registryLoginServer string = core.outputs.registryLoginServer
output apiFqdn string = app.outputs.apiFqdn
output apiAppName string = app.outputs.apiAppName
output workerAppName string = app.outputs.workerAppName
output staticWebAppHostname string = web.outputs.defaultHostname
output staticWebAppName string = web.outputs.name
output cosmosEndpoint string = data.outputs.cosmosEndpoint
output aiAccountName string = ai.outputs.accountName
output aiProjectName string = ai.outputs.projectName
output aiProjectEndpoint string = ai.outputs.projectEndpoint
output aiDefaultDeploymentName string = ai.outputs.defaultDeploymentName
output aiFrontierDeploymentNames array = ai.outputs.frontierDeploymentNames
output aiImageDeploymentName string = ai.outputs.imageDeploymentName
output runtimeIdentityClientId string = core.outputs.runtimeIdentityClientId
output deployIdentityClientId string = core.outputs.deployIdentityClientId
output externalIdTenantId string = deployExternalId ? identity!.outputs.tenantId : ''
output externalIdDomain string = deployExternalId ? identity!.outputs.domainName : ''
