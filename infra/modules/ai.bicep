@minLength(3)
param projectName string

@minLength(2)
param environmentName string
param location string
param tags object
param existingAccountName string

param runtimeIdentityPrincipalId string
param researchUserPrincipalId string = ''

var principals = concat([
  {
    id: runtimeIdentityPrincipalId
    type: 'ServicePrincipal'
  }
], empty(researchUserPrincipalId) ? [] : [
  {
    id: researchUserPrincipalId
    type: 'User'
  }
])

@description('GA frontier multimodal models. All accept text and images.')
@minLength(3)
@maxLength(3)
param frontierModelNames array = [
  'gpt-5.6-sol'
  'gpt-5.6-terra'
  'gpt-5.6-luna'
]

param frontierModelVersion string = '2026-07-09'

@description('GA frontier model for image generation and editing.')
param imageModelName string = 'gpt-image-2'

param imageModelVersion string = '2026-04-21'

var frontierDeploymentNames = [for modelName in frontierModelNames: '${modelName}-${frontierModelVersion}']
var imageDeploymentName = '${imageModelName}-${imageModelVersion}'

resource account 'Microsoft.CognitiveServices/accounts@2025-06-01' existing = {
  name: existingAccountName
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
    description: 'Lanternina project using centrally managed model deployments.'
  }
}

var foundryUserRoleId = '53ca6127-db72-4b80-b1b0-d745d6d5456d'

resource foundryUser 'Microsoft.Authorization/roleAssignments@2022-04-01' = [for principal in principals: {
  scope: project
  name: guid(project.id, principal.id, foundryUserRoleId)
  properties: {
    roleDefinitionId: subscriptionResourceId(
      'Microsoft.Authorization/roleDefinitions',
      foundryUserRoleId
    )
    principalId: principal.id
    principalType: principal.type
  }
}]

var openAiUserRoleId = '5e0bd9bd-7b93-4f28-af87-19fc36ad61bd'

resource openAiUser 'Microsoft.Authorization/roleAssignments@2022-04-01' = [for principal in principals: {
  scope: account
  name: guid(account.id, principal.id, openAiUserRoleId)
  properties: {
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', openAiUserRoleId)
    principalId: principal.id
    principalType: principal.type
  }
}]

resource contentSafetyRole 'Microsoft.Authorization/roleDefinitions@2022-04-01' = {
  name: guid(resourceGroup().id, projectName, environmentName, 'content-safety-runtime')
  properties: {
    roleName: '${projectName}-${environmentName}-safety-embeddings-${uniqueString(resourceGroup().id)}'
    description: 'Call Content Safety and embedding APIs without account keys or project secrets.'
    type: 'CustomRole'
    assignableScopes: [resourceGroup().id]
    permissions: [
      {
        actions: []
        notActions: []
        dataActions: [
          'Microsoft.CognitiveServices/accounts/ContentSafety/*'
          'Microsoft.CognitiveServices/accounts/MaaS/embeddings/action'
          'Microsoft.CognitiveServices/accounts/MaaS/images/embeddings/action'
          'Microsoft.CognitiveServices/accounts/MaaS/v1/embed/action'
        ]
        notDataActions: []
      }
    ]
  }
}

resource contentSafetyUser 'Microsoft.Authorization/roleAssignments@2022-04-01' = [for principal in principals: {
  scope: account
  name: guid(account.id, principal.id, contentSafetyRole.id)
  properties: {
    roleDefinitionId: contentSafetyRole.id
    principalId: principal.id
    principalType: principal.type
  }
}]

output accountName string = account.name
output accountEndpoint string = account.properties.endpoint
output projectName string = project.name
output projectEndpoint string = 'https://${account.name}.services.ai.azure.com/api/projects/${project.name}'
output defaultDeploymentName string = frontierDeploymentNames[0]
output frontierDeploymentNames array = frontierDeploymentNames
output imageDeploymentName string = imageDeploymentName
