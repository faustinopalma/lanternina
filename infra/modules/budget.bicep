// A sponsored subscription has a hard credit cap and no policy that stops us reaching it.
// This is the cheapest possible smoke alarm.

targetScope = 'subscription'

param budgetName string
param amount int
param contactEmail string
param resourceGroupNames array

@description('Budgets need a start date on the first of a month, in the future or the current month.')
param startDate string = '${utcNow('yyyy-MM')}-01'

resource budget 'Microsoft.Consumption/budgets@2024-08-01' = {
  name: budgetName
  properties: {
    category: 'Cost'
    amount: amount
    timeGrain: 'Monthly'
    timePeriod: {
      startDate: startDate
    }
    filter: {
      dimensions: {
        name: 'ResourceGroupName'
        operator: 'In'
        values: resourceGroupNames
      }
    }
    notifications: {
      half: {
        enabled: true
        operator: 'GreaterThan'
        threshold: 50
        contactEmails: [contactEmail]
        thresholdType: 'Actual'
      }
      most: {
        enabled: true
        operator: 'GreaterThan'
        threshold: 80
        contactEmails: [contactEmail]
        thresholdType: 'Actual'
      }
      all: {
        enabled: true
        operator: 'GreaterThan'
        threshold: 100
        contactEmails: [contactEmail]
        thresholdType: 'Actual'
      }
    }
  }
}
