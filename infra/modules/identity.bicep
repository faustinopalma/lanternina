// The Entra External ID (CIAM) directory, created as an ARM resource.
//
// Worth knowing: this is a real Azure resource, so no manual portal step is needed to
// create the tenant. What ARM does NOT create is what lives INSIDE it — app
// registrations, user flows, users. Those are tenant-scoped and are the reason a tenant
// move is a rebuild rather than a migration. See docs/DEPLOY.md.
//
// The shape below was read off a directory that already exists in this subscription
// rather than taken from documentation.

@description('Becomes <prefix>.onmicrosoft.com. Globally unique across all of Entra.')
@minLength(3)
// The RESOURCE name is '<prefix>.onmicrosoft.com' and ARM caps it at 26 characters, so
// the prefix itself cannot exceed 10. The Bicep compiler caught this; the docs did not.
@maxLength(10)
param domainPrefix string

param displayName string

@description('Sets data residency for the directory. It cannot be changed after creation.')
param countryCode string

param tags object

@description('Directories are placed in a geography, not an Azure region.')
@allowed(['Europe', 'United States', 'Asia Pacific', 'Australia', 'Japan'])
param geography string = 'Europe'

resource ciamDirectory 'Microsoft.AzureActiveDirectory/ciamDirectories@2023-05-17-preview' = {
  name: '${domainPrefix}.onmicrosoft.com'
  location: geography
  tags: tags
  sku: {
    name: 'Base'
    tier: 'A0'
  }
  properties: {
    createTenantProperties: {
      displayName: displayName
      countryCode: countryCode
    }
  }
}

output tenantId string = ciamDirectory.properties.tenantId
output domainName string = ciamDirectory.properties.domainName
