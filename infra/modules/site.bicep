// The public page. A second Static Web App, deliberately not the one that serves the
// parent's panel.
//
// Separate because the two have nothing in common but the technology: this one is
// anonymous, cached, and read by people who have never heard of the project; the panel
// holds an identity provider, a linked API and one household's decisions. Sharing a
// resource would mean one deployment can take down the other, and it would put a
// marketing page behind the same custom-auth configuration as a dashboard.
//
// Free rather than Standard: nothing here needs a linked backend or custom auth. The
// limit that comes with it is custom domains, so a third hostname is a redirect at the
// DNS provider rather than a fourth name on this resource.

param projectName string
param environmentName string
param location string
param suffix string
param tags object

@allowed(['Free', 'Standard'])
param sku string = 'Free'

resource siteApp 'Microsoft.Web/staticSites@2024-04-01' = {
  name: 'swa-${projectName}-site-${environmentName}-${suffix}'
  location: location
  tags: tags
  sku: {
    name: sku
    tier: sku
  }
  properties: {
    // staticwebapp.config.json is committed beside the page, so the deployment carries it.
    allowConfigFileUpdates: true
    stagingEnvironmentPolicy: 'Disabled'
  }
}

output name string = siteApp.name
output defaultHostname string = siteApp.properties.defaultHostname
