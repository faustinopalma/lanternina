// The browser-facing tier. Static assets only: the API lives in Container Apps.
//
// This is the one resource that cannot sit in swedencentral — the Standard SKU is not
// offered there. It is a globally distributed service, so the region only decides where
// the metadata lives, not where users are served from.

param projectName string
param environmentName string
param location string
param suffix string
param tags object

@description('Standard is required for linked backends and custom auth. Free cannot do either.')
@allowed(['Free', 'Standard'])
param sku string = 'Standard'

resource staticWebApp 'Microsoft.Web/staticSites@2024-04-01' = {
  name: 'swa-${projectName}-${environmentName}-${suffix}'
  location: location
  tags: tags
  sku: {
    name: sku
    tier: sku
  }
  properties: {
    // The build is driven from CI, not from a repository link created by ARM.
    allowConfigFileUpdates: true
    stagingEnvironmentPolicy: 'Enabled'
  }
}

output name string = staticWebApp.name
output defaultHostname string = staticWebApp.properties.defaultHostname
