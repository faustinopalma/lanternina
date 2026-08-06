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

// One zone per service that gets a private endpoint. Foundry, when it arrives, needs
// three of its own (cognitiveservices + openai + services.ai).
var privateDnsZoneNames = [
  'privatelink.documents.azure.com'
  'privatelink.queue.${environment().suffixes.storage}'
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

output acaSubnetId string = vnet.properties.subnets[0].id
output privateEndpointSubnetId string = vnet.properties.subnets[1].id
output cosmosDnsZoneId string = privateDnsZones[0].id
output queueDnsZoneId string = privateDnsZones[1].id
output logAnalyticsId string = logAnalytics.id
output logAnalyticsCustomerId string = logAnalytics.properties.customerId
output registryName string = registry.name
output registryLoginServer string = registry.properties.loginServer
output runtimeIdentityId string = runtimeIdentity.id
output runtimeIdentityClientId string = runtimeIdentity.properties.clientId
output runtimeIdentityPrincipalId string = runtimeIdentity.properties.principalId
output deployIdentityId string = deployIdentity.id
output deployIdentityClientId string = deployIdentity.properties.clientId
output deployIdentityPrincipalId string = deployIdentity.properties.principalId
