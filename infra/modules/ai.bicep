@minLength(3)
param projectName string

@minLength(2)
param environmentName string
param location string
param suffix string
param tags object

param runtimeIdentityPrincipalId string

@description('GA frontier multimodal models. All accept text and images.')
@minLength(3)
@maxLength(3)
param frontierModelNames array = [
  'gpt-5.6-sol'
  'gpt-5.6-terra'
  'gpt-5.6-luna'
]

param frontierModelVersion string = '2026-07-09'
param frontierModelSku string = 'GlobalStandard'

@description('Thousands of tokens per minute assigned from existing quota.')
@minValue(1)
param frontierModelCapacity int = 1000

@description('GA frontier model for image generation and editing.')
param imageModelName string = 'gpt-image-2'

param imageModelVersion string = '2026-04-21'
param imageModelSku string = 'GlobalStandard'

@description('Images per minute assigned from existing quota.')
@minValue(1)
param imageModelCapacity int = 2

var namePrefix = '${projectName}-${environmentName}'
var frontierDeploymentNames = [for modelName in frontierModelNames: '${modelName}-${frontierModelVersion}']
var imageDeploymentName = '${imageModelName}-${imageModelVersion}'

resource account 'Microsoft.CognitiveServices/accounts@2025-06-01' = {
  name: 'ai-${namePrefix}-${suffix}'
  location: location
  tags: tags
  kind: 'AIServices'
  sku: {
    name: 'S0'
  }
  properties: {
    allowProjectManagement: true
    customSubDomainName: 'ai-${namePrefix}-${suffix}'
    disableLocalAuth: true
    publicNetworkAccess: 'Enabled'
    networkAcls: {
      defaultAction: 'Allow'
    }
  }
}

resource project 'Microsoft.CognitiveServices/accounts/projects@2025-09-01' = {
  parent: account
  name: '${projectName}-${environmentName}'
  location: location
  tags: tags
  identity: {
    type: 'SystemAssigned'
  }
  properties: {
    displayName: 'Lanternina ${environmentName}'
    description: 'Private Foundry project for parent-controlled worksheet generation and reading.'
  }
  dependsOn: [imageDeployment]
}

resource frontierSol 'Microsoft.CognitiveServices/accounts/deployments@2025-06-01' = {
  parent: account
  name: frontierDeploymentNames[0]
  sku: {
    name: frontierModelSku
    capacity: frontierModelCapacity
  }
  properties: {
    model: {
      format: 'OpenAI'
      name: frontierModelNames[0]
      version: frontierModelVersion
    }
    versionUpgradeOption: 'NoAutoUpgrade'
  }
}

resource frontierTerra 'Microsoft.CognitiveServices/accounts/deployments@2025-06-01' = {
  parent: account
  name: frontierDeploymentNames[1]
  sku: {
    name: frontierModelSku
    capacity: frontierModelCapacity
  }
  properties: {
    model: {
      format: 'OpenAI'
      name: frontierModelNames[1]
      version: frontierModelVersion
    }
    versionUpgradeOption: 'NoAutoUpgrade'
  }
  dependsOn: [frontierSol]
}

resource frontierLuna 'Microsoft.CognitiveServices/accounts/deployments@2025-06-01' = {
  parent: account
  name: frontierDeploymentNames[2]
  sku: {
    name: frontierModelSku
    capacity: frontierModelCapacity
  }
  properties: {
    model: {
      format: 'OpenAI'
      name: frontierModelNames[2]
      version: frontierModelVersion
    }
    versionUpgradeOption: 'NoAutoUpgrade'
  }
  dependsOn: [frontierTerra]
}

resource imageDeployment 'Microsoft.CognitiveServices/accounts/deployments@2025-06-01' = {
  parent: account
  name: imageDeploymentName
  sku: {
    name: imageModelSku
    capacity: imageModelCapacity
  }
  properties: {
    model: {
      format: 'OpenAI'
      name: imageModelName
      version: imageModelVersion
    }
    versionUpgradeOption: 'NoAutoUpgrade'
  }
  dependsOn: [frontierLuna]
}

var foundryUserRoleId = '53ca6127-db72-4b80-b1b0-d745d6d5456d'

resource foundryUser 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  scope: project
  name: guid(project.id, runtimeIdentityPrincipalId, foundryUserRoleId)
  properties: {
    roleDefinitionId: subscriptionResourceId(
      'Microsoft.Authorization/roleDefinitions',
      foundryUserRoleId
    )
    principalId: runtimeIdentityPrincipalId
    principalType: 'ServicePrincipal'
  }
}

output accountName string = account.name
output accountEndpoint string = account.properties.endpoint
output projectName string = project.name
output projectEndpoint string = 'https://${account.name}.services.ai.azure.com/api/projects/${project.name}'
output defaultDeploymentName string = frontierSol.name
output frontierDeploymentNames array = frontierDeploymentNames
output imageDeploymentName string = imageDeployment.name
