// Plumbing that outlives the application: network, registry, logs, identities.
//
// The subnet delegation and the private DNS zones are the part that makes the data tier
// reachable ONLY from inside the Container Apps environment.

param projectName string
param environmentName string
param location string
param suffix string
param tags object

@description('Address space. A /23 leaves room for the ACA subnet to grow.')
param vnetAddressPrefix string = '10.60.0.0/23'

@description('Container Apps requires a /27 or larger for a workload-profile environment.')
param acaSubnetPrefix string = '10.60.0.0/26'

param privateEndpointSubnetPrefix string = '10.60.0.64/27'

@description('Days of log retention. Log Analytics is the quiet cost driver in a Container Apps setup.')
param logRetentionDays int = 30

@description('Hard ceiling on daily log ingestion, in GB. -1 removes the cap.')
param logDailyQuotaGb int = 1

var namePrefix = '${projectName}-${environmentName}'

resource vnet 'Microsoft.Network/virtualNetworks@2024-05-01' = {
  name: 'vnet-${namePrefix}-${suffix}'
  location: location
  tags: tags
  properties: {
    addressSpace: {
      addressPrefixes: [vnetAddressPrefix]
    }
    subnets: [
      {
        name: 'snet-aca'
        properties: {
          addressPrefix: acaSubnetPrefix
          delegations: [
            {
              name: 'aca-delegation'
              properties: {
                serviceName: 'Microsoft.App/environments'
              }
            }
          ]
        }
      }
      {
        name: 'snet-pe'
        properties: {
          addressPrefix: privateEndpointSubnetPrefix
          privateEndpointNetworkPolicies: 'Disabled'
        }
      }
    ]
  }
}

// One zone per data service that gets a private endpoint.
var privateDnsZoneNames = [
  'privatelink.documents.azure.com'
  'privatelink.queue.${environment().suffixes.storage}'
  'privatelink.blob.${environment().suffixes.storage}'
]

resource privateDnsZones 'Microsoft.Network/privateDnsZones@2024-06-01' = [
  for zoneName in privateDnsZoneNames: {
    name: zoneName
    location: 'global'
    tags: tags
  }
]

resource privateDnsLinks 'Microsoft.Network/privateDnsZones/virtualNetworkLinks@2024-06-01' = [
  for (zoneName, i) in privateDnsZoneNames: {
    parent: privateDnsZones[i]
    name: 'link-${vnet.name}'
    location: 'global'
    tags: tags
    properties: {
      registrationEnabled: false
      virtualNetwork: {
        id: vnet.id
      }
    }
  }
]

resource logAnalytics 'Microsoft.OperationalInsights/workspaces@2023-09-01' = {
  name: 'log-${namePrefix}-${suffix}'
  location: location
  tags: tags
  properties: {
    sku: {
      name: 'PerGB2018'
    }
    retentionInDays: logRetentionDays
    workspaceCapping: {
      dailyQuotaGb: logDailyQuotaGb
    }
    features: {
      enableLogAccessUsingOnlyResourcePermissions: true
    }
  }
}

// Workspace-based, so the traces land in the same workspace as the container logs and one
// query can join them: a request that failed and the line the code wrote about it are the
// two halves of the same story, and they used to be in different places.
//
// What this buys that stdout does not is the part nobody writes down - how long a request
// took, which model call was slow inside it, which Cosmos query, and which of them failed
// together. Retention and the daily cap are the workspace's, already set above, so this
// adds a surface and not a second bill.
resource insights 'Microsoft.Insights/components@2020-02-02' = {
  name: 'appi-${namePrefix}-${suffix}'
  location: location
  tags: tags
  kind: 'web'
  properties: {
    Application_Type: 'web'
    WorkspaceResourceId: logAnalytics.id
    // No key in a URL and no anonymous write: the container proves who it is with the
    // same managed identity it uses for everything else.
    DisableLocalAuth: true
    IngestionMode: 'LogAnalytics'
    publicNetworkAccessForIngestion: 'Enabled'
    publicNetworkAccessForQuery: 'Enabled'
  }
}

// Basic and public on purpose: a private-linked registry needs Premium, and the registry
// holds no personal data. Access is by RBAC, never by the admin user.
resource registry 'Microsoft.ContainerRegistry/registries@2025-04-01' = {
  #disable-next-line BCP334 // projectName is minLength(3) and suffix is always 5, so this cannot be too short.
  name: take('acr${replace(namePrefix, '-', '')}${suffix}', 50)
  location: location
  tags: tags
  sku: {
    name: 'Basic'
  }
  properties: {
    adminUserEnabled: false
    anonymousPullEnabled: false
  }
}

// Two identities with different jobs. The runtime one never gets deploy rights; the
// deploy one never runs application code.
resource runtimeIdentity 'Microsoft.ManagedIdentity/userAssignedIdentities@2024-11-30' = {
  name: 'id-${namePrefix}-runtime'
  location: location
  tags: tags
}

resource deployIdentity 'Microsoft.ManagedIdentity/userAssignedIdentities@2024-11-30' = {
  name: 'id-${namePrefix}-deploy'
  location: location
  tags: tags
}

var acrPullRoleId = '7f951dda-4ed3-4680-a7ca-43fe172d538d'
var acrPushRoleId = '8311e382-0749-4cb8-b61a-304f252e45ec'
// Monitoring Metrics Publisher. The component refuses local auth, so telemetry is written
// with the same managed identity everything else here proves itself with, and there is no
// ingestion key anywhere for a leaked environment variable to carry.
var metricsPublisherRoleId = '3913510d-42f4-4e42-8a64-420c390055eb'

resource acrPull 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  scope: registry
  name: guid(registry.id, runtimeIdentity.id, acrPullRoleId)
  properties: {
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', acrPullRoleId)
    principalId: runtimeIdentity.properties.principalId
    principalType: 'ServicePrincipal'
  }
}

resource acrPush 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  scope: registry
  name: guid(registry.id, deployIdentity.id, acrPushRoleId)
  properties: {
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', acrPushRoleId)
    principalId: deployIdentity.properties.principalId
    principalType: 'ServicePrincipal'
  }
}

resource metricsPublisher 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  scope: insights
  name: guid(insights.id, runtimeIdentity.id, metricsPublisherRoleId)
  properties: {
    roleDefinitionId: subscriptionResourceId(
      'Microsoft.Authorization/roleDefinitions',
      metricsPublisherRoleId
    )
    principalId: runtimeIdentity.properties.principalId
    principalType: 'ServicePrincipal'
  }
}

output acaSubnetId string = vnet.properties.subnets[0].id
output privateEndpointSubnetId string = vnet.properties.subnets[1].id
output cosmosDnsZoneId string = privateDnsZones[0].id
output queueDnsZoneId string = privateDnsZones[1].id
output blobDnsZoneId string = privateDnsZones[2].id
output logAnalyticsId string = logAnalytics.id
output logAnalyticsCustomerId string = logAnalytics.properties.customerId
output insightsConnectionString string = insights.properties.ConnectionString
output insightsId string = insights.id
output registryName string = registry.name
output registryLoginServer string = registry.properties.loginServer
output runtimeIdentityId string = runtimeIdentity.id
output runtimeIdentityClientId string = runtimeIdentity.properties.clientId
output runtimeIdentityPrincipalId string = runtimeIdentity.properties.principalId
output deployIdentityId string = deployIdentity.id
output deployIdentityClientId string = deployIdentity.properties.clientId
output deployIdentityPrincipalId string = deployIdentity.properties.principalId
