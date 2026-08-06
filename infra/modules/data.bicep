// The data tier. This is the resource group that must never be deleted casually.
//
// RULE, enforced by review and by tests/test_boundaries.py: no container here may hold a
// field about the learner. The cloud stores households as opaque ids; the mapping from an
// id to a real person exists only on the device in her home. See docs/ARCHITECTURE.md.

param projectName string
param environmentName string
param location string
param suffix string
param tags object

@allowed(['Enabled', 'Disabled'])
param publicNetworkAccess string

param privateEndpointSubnetId string
param cosmosDnsZoneId string
param queueDnsZoneId string

@description('Principal that the running containers use. Gets data-plane access, never control-plane.')
param runtimeIdentityPrincipalId string

param databaseName string = 'lanternina'

var namePrefix = '${projectName}-${environmentName}'
var workQueueName = 'work'

// Serverless: a handful of households does not justify provisioned throughput, and
// provisioned throughput bills whether or not anyone opens the panel.
resource cosmos 'Microsoft.DocumentDB/databaseAccounts@2024-11-15' = {
  name: 'cos-${namePrefix}-${suffix}'
  location: location
  tags: tags
  kind: 'GlobalDocumentDB'
  properties: {
    databaseAccountOfferType: 'Standard'
    locations: [
      {
        locationName: location
        failoverPriority: 0
        isZoneRedundant: false
      }
    ]
    capabilities: [
      {
        name: 'EnableServerless'
      }
    ]
    consistencyPolicy: {
      defaultConsistencyLevel: 'Session'
    }
    // Keys are all-powerful and cannot be scoped. Entra only.
    disableLocalAuth: true
    publicNetworkAccess: publicNetworkAccess
    minimalTlsVersion: 'Tls12'
  }
}

resource database 'Microsoft.DocumentDB/databaseAccounts/sqlDatabases@2024-11-15' = {
  parent: cosmos
  name: databaseName
  properties: {
    resource: {
      id: databaseName
    }
  }
}

// familyId as the partition key makes tenant isolation structural rather than a WHERE
// clause somebody eventually forgets.
var containers = [
  { name: 'families', partitionKey: '/familyId' }
  { name: 'proposals', partitionKey: '/familyId' }
  { name: 'outbox', partitionKey: '/familyId' }
  { name: 'sources', partitionKey: '/familyId' }
]

resource sqlContainers 'Microsoft.DocumentDB/databaseAccounts/sqlDatabases/containers@2024-11-15' = [
  for c in containers: {
    parent: database
    name: c.name
    properties: {
      resource: {
        id: c.name
        partitionKey: {
          paths: [c.partitionKey]
          kind: 'Hash'
        }
      }
    }
  }
]

// Built-in "Cosmos DB Built-in Data Contributor". Data plane only: this principal cannot
// read keys, change firewall rules, or delete the account.
var cosmosDataContributorId = '00000000-0000-0000-0000-000000000002'

resource cosmosDataRole 'Microsoft.DocumentDB/databaseAccounts/sqlRoleAssignments@2024-11-15' = {
  parent: cosmos
  name: guid(cosmos.id, runtimeIdentityPrincipalId, cosmosDataContributorId)
  properties: {
    roleDefinitionId: '${cosmos.id}/sqlRoleDefinitions/${cosmosDataContributorId}'
    principalId: runtimeIdentityPrincipalId
    scope: cosmos.id
  }
}

// The queue is what lets the interactive API stay fast: it hands long work (generation,
// vision, content safety) to the worker instead of making the parent wait.
resource storage 'Microsoft.Storage/storageAccounts@2024-01-01' = {
  // Storage account names are capped at 24 characters and allow no dashes.
  #disable-next-line BCP334 // projectName is minLength(3) and suffix is always 5, so this cannot be too short.
  name: take('st${replace(namePrefix, '-', '')}${suffix}', 24)
  location: location
  tags: tags
  sku: {
    name: 'Standard_LRS'
  }
  kind: 'StorageV2'
  properties: {
    minimumTlsVersion: 'TLS1_2'
    allowBlobPublicAccess: false
    allowSharedKeyAccess: false
    publicNetworkAccess: publicNetworkAccess
    supportsHttpsTrafficOnly: true
    networkAcls: {
      bypass: 'AzureServices'
      defaultAction: 'Deny'
    }
  }
}

resource queueService 'Microsoft.Storage/storageAccounts/queueServices@2024-01-01' = {
  parent: storage
  name: 'default'
}

resource workQueue 'Microsoft.Storage/storageAccounts/queueServices/queues@2024-01-01' = {
  parent: queueService
  name: workQueueName
}

var storageQueueDataContributorId = '974c5e8b-45b9-4653-ba55-5f855dd0fb88'

resource queueDataRole 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  scope: storage
  name: guid(storage.id, runtimeIdentityPrincipalId, storageQueueDataContributorId)
  properties: {
    roleDefinitionId: subscriptionResourceId(
      'Microsoft.Authorization/roleDefinitions',
      storageQueueDataContributorId
    )
    principalId: runtimeIdentityPrincipalId
    principalType: 'ServicePrincipal'
  }
}

resource cosmosPrivateEndpoint 'Microsoft.Network/privateEndpoints@2024-05-01' = {
  name: 'pe-cosmos-${namePrefix}-${suffix}'
  location: location
  tags: tags
  properties: {
    subnet: {
      id: privateEndpointSubnetId
    }
    privateLinkServiceConnections: [
      {
        name: 'cosmos'
        properties: {
          privateLinkServiceId: cosmos.id
          groupIds: ['Sql']
        }
      }
    ]
  }
}

resource cosmosPrivateDns 'Microsoft.Network/privateEndpoints/privateDnsZoneGroups@2024-05-01' = {
  parent: cosmosPrivateEndpoint
  name: 'default'
  properties: {
    privateDnsZoneConfigs: [
      {
        name: 'cosmos'
        properties: {
          privateDnsZoneId: cosmosDnsZoneId
        }
      }
    ]
  }
}

resource queuePrivateEndpoint 'Microsoft.Network/privateEndpoints@2024-05-01' = {
  name: 'pe-queue-${namePrefix}-${suffix}'
  location: location
  tags: tags
  properties: {
    subnet: {
      id: privateEndpointSubnetId
    }
    privateLinkServiceConnections: [
      {
        name: 'queue'
        properties: {
          privateLinkServiceId: storage.id
          groupIds: ['queue']
        }
      }
    ]
  }
}

resource queuePrivateDns 'Microsoft.Network/privateEndpoints/privateDnsZoneGroups@2024-05-01' = {
  parent: queuePrivateEndpoint
  name: 'default'
  properties: {
    privateDnsZoneConfigs: [
      {
        name: 'queue'
        properties: {
          privateDnsZoneId: queueDnsZoneId
        }
      }
    ]
  }
}

output cosmosAccountName string = cosmos.name
output cosmosEndpoint string = cosmos.properties.documentEndpoint
output cosmosDatabaseName string = databaseName
output storageAccountName string = storage.name
output workQueueName string = workQueueName
