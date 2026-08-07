// The disposable tier: the Container Apps environment and the two apps.
//
// Two apps on purpose, because they scale on different signals:
//   api     HTTP rule. A request to a zero-scaled app triggers activation and is served;
//           no queue is needed to wake it, and a queue in front would force 202+polling.
//   worker  queue rule. Genuinely asynchronous work — generation, vision, content safety.

param projectName string
param environmentName string
param location string
param suffix string
param tags object

param infrastructureSubnetId string
param logAnalyticsCustomerId string
param logAnalyticsId string
param registryLoginServer string
param runtimeIdentityId string
param runtimeIdentityClientId string

param cosmosEndpoint string
param cosmosDatabaseName string
param storageAccountName string
param workQueueName string

@description('Image for the API. Defaults to a placeholder so the first deploy succeeds before any build exists.')
param apiImage string = 'mcr.microsoft.com/k8se/quickstart:latest'

@description('Image for the worker. Same placeholder rationale.')
param workerImage string = 'mcr.microsoft.com/k8se/quickstart:latest'

// MUST match the port the image in apiImage actually listens on, or ingress accepts the
// connection and then times out with no useful error. The default placeholder serves on
// 80; the real uvicorn image serves on 8000, so the two move together.
// scripts/build-and-deploy-images.ps1 passes both, which is what keeps them in step.
param apiTargetPort int = 80
param apiMaxReplicas int = 5
param workerMaxReplicas int = 3

@description('Trust the caller identity from a plain request header. Development only.')
param panelDevAuth bool = false

@description('The one address allowed to self-activate, and only while no account is active yet.')
param panelBootstrapContact string = ''

@description('Identity provider base URL. Empty leaves the panel closed to everyone.')
param panelOidcAuthority string = ''

@description('Audiences a token may carry, comma separated.')
param panelOidcAudience string = ''

var namePrefix = '${projectName}-${environmentName}'

resource environment 'Microsoft.App/managedEnvironments@2025-01-01' = {
  name: 'cae-${namePrefix}-${suffix}'
  location: location
  tags: tags
  properties: {
    appLogsConfiguration: {
      destination: 'log-analytics'
      logAnalyticsConfiguration: {
        customerId: logAnalyticsCustomerId
        sharedKey: listKeys(logAnalyticsId, '2023-09-01').primarySharedKey
      }
    }
    vnetConfiguration: {
      infrastructureSubnetId: infrastructureSubnetId
      // false: the ingress stays reachable from the internet. That is the product. The
      // data tier is what goes private, via the endpoints in modules/data.bicep.
      internal: false
    }
    workloadProfiles: [
      {
        name: 'Consumption'
        workloadProfileType: 'Consumption'
      }
    ]
    zoneRedundant: false
  }
}

var commonEnv = [
  {
    name: 'AZURE_CLIENT_ID'
    value: runtimeIdentityClientId
  }
  {
    name: 'LANTERNINA_COSMOS_ENDPOINT'
    value: cosmosEndpoint
  }
  {
    name: 'LANTERNINA_COSMOS_DATABASE'
    value: cosmosDatabaseName
  }
  {
    name: 'LANTERNINA_STORAGE_ACCOUNT'
    value: storageAccountName
  }
  {
    name: 'LANTERNINA_WORK_QUEUE'
    value: workQueueName
  }
]

// Only the API is reachable from outside, so only the API carries the settings that
// decide who may in.
var apiEnv = concat(commonEnv, [
  {
    name: 'LANTERNINA_DEV_AUTH'
    value: panelDevAuth ? '1' : '0'
  }
  {
    name: 'LANTERNINA_BOOTSTRAP_CONTACT'
    value: panelBootstrapContact
  }
  {
    name: 'LANTERNINA_OIDC_AUTHORITY'
    value: panelOidcAuthority
  }
  {
    name: 'LANTERNINA_OIDC_AUDIENCE'
    value: panelOidcAudience
  }
])

resource api 'Microsoft.App/containerApps@2025-01-01' = {
  name: 'ca-${namePrefix}-api'
  location: location
  tags: tags
  identity: {
    type: 'UserAssigned'
    userAssignedIdentities: {
      '${runtimeIdentityId}': {}
    }
  }
  properties: {
    environmentId: environment.id
    workloadProfileName: 'Consumption'
    configuration: {
      activeRevisionsMode: 'Single'
      ingress: {
        external: true
        targetPort: apiTargetPort
        transport: 'auto'
        allowInsecure: false
        traffic: [
          {
            latestRevision: true
            weight: 100
          }
        ]
      }
      registries: [
        {
          server: registryLoginServer
          identity: runtimeIdentityId
        }
      ]
    }
    template: {
      containers: [
        {
          name: 'api'
          image: apiImage
          resources: {
            cpu: json('0.5')
            memory: '1Gi'
          }
          env: apiEnv
        }
      ]
      scale: {
        minReplicas: 0
        maxReplicas: apiMaxReplicas
        rules: [
          {
            name: 'http'
            http: {
              metadata: {
                concurrentRequests: '20'
              }
            }
          }
        ]
      }
    }
  }
}

resource worker 'Microsoft.App/containerApps@2025-01-01' = {
  name: 'ca-${namePrefix}-worker'
  location: location
  tags: tags
  identity: {
    type: 'UserAssigned'
    userAssignedIdentities: {
      '${runtimeIdentityId}': {}
    }
  }
  properties: {
    environmentId: environment.id
    workloadProfileName: 'Consumption'
    configuration: {
      activeRevisionsMode: 'Single'
      registries: [
        {
          server: registryLoginServer
          identity: runtimeIdentityId
        }
      ]
    }
    template: {
      containers: [
        {
          name: 'worker'
          image: workerImage
          resources: {
            cpu: json('0.5')
            memory: '1Gi'
          }
          env: commonEnv
        }
      ]
      scale: {
        minReplicas: 0
        maxReplicas: workerMaxReplicas
        rules: [
          {
            name: 'queue'
            custom: {
              type: 'azure-queue'
              // Managed identity, so no connection string lives in the app config.
              identity: runtimeIdentityId
              metadata: {
                accountName: storageAccountName
                queueName: workQueueName
                queueLength: '1'
                cloud: 'AzurePublicCloud'
              }
            }
          }
        ]
      }
    }
  }
}

output environmentName string = environment.name
output apiAppName string = api.name
output apiFqdn string = api.properties.configuration.ingress.fqdn
output workerAppName string = worker.name
