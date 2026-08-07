<#
.SYNOPSIS
    Deploy the Lanternina cloud tier. Idempotent: safe to run repeatedly.

.DESCRIPTION
    Creates every Azure resource from infra/main.bicep. Nothing tenant-specific is
    baked into the templates, so pointing this at a different subscription or tenant is a
    fresh deploy rather than a migration.

    The Azure CLI session is kept in a workspace-local, gitignored folder so it never
    disturbs az logins in other terminals.

.EXAMPLE
    ./scripts/deploy.ps1 -Login
    ./scripts/deploy.ps1 -SubscriptionId <guid> -Owner fausto -BudgetContactEmail me@example.com

.EXAMPLE
    ./scripts/deploy.ps1 -WhatIf
#>
[CmdletBinding()]
param(
    [string]$SubscriptionId,
    [string]$EnvironmentName = 'dev',
    [string]$Location = 'swedencentral',
    [string]$Owner = $env:USERNAME,
    [string]$BudgetContactEmail = '',

    [switch]$Login,

    # Required when the account is a guest: without it az lands on the account's home tenant.
    [string]$Tenant = '',

    # Show the plan without changing anything.
    [switch]$WhatIf
)

$ErrorActionPreference = 'Stop'
$sw = [Diagnostics.Stopwatch]::StartNew()

$repoRoot = Split-Path -Parent $PSScriptRoot
$templateFile = Join-Path $repoRoot 'infra/main.bicep'
$parameterFile = Join-Path $repoRoot 'infra/main.bicepparam'

# An isolated CLI config so this script cannot log other terminals in or out.
$env:AZURE_CONFIG_DIR = Join-Path $repoRoot '.azure'
New-Item -ItemType Directory -Force -Path $env:AZURE_CONFIG_DIR | Out-Null

# az crashes streaming non-ASCII output through the Windows console default encoding.
$env:PYTHONUTF8 = '1'

function Write-Step($message) {
    Write-Host "==> $message" -ForegroundColor Cyan
}

if ($Login) {
    Write-Step 'Signing in (device code)'
    # The WAM broker often fails to surface its window; disable it for this config only.
    az config set core.enable_broker_on_windows=false --only-show-errors | Out-Null
    $loginArgs = @('login', '--use-device-code', '--allow-no-subscriptions', '--only-show-errors')
    if ($Tenant) { $loginArgs += @('--tenant', $Tenant) }
    # Not silenced: this is where the device code is printed.
    az @loginArgs
}

$account = az account show -o json 2>$null | ConvertFrom-Json
if (-not $account) {
    throw 'Not signed in. Run: ./scripts/deploy.ps1 -Login'
}

if ($SubscriptionId) {
    Write-Step "Selecting subscription $SubscriptionId"
    az account set --subscription $SubscriptionId
    $account = az account show -o json | ConvertFrom-Json
}

Write-Step "Subscription: $($account.name) [$($account.id)]"
Write-Step "Tenant:       $($account.tenantId)"

Write-Step 'Registering resource providers (no-op when already registered)'
$providers = @(
    'Microsoft.App'
    'Microsoft.ContainerRegistry'
    'Microsoft.DocumentDB'
    'Microsoft.KeyVault'
    'Microsoft.ManagedIdentity'
    'Microsoft.Network'
    'Microsoft.OperationalInsights'
    'Microsoft.Storage'
    'Microsoft.Web'
    'Microsoft.AzureActiveDirectory'
)
foreach ($p in $providers) {
    $state = az provider show --namespace $p --query registrationState -o tsv 2>$null
    if ($state -ne 'Registered') {
        Write-Host "    registering $p (was: $state)"
        az provider register --namespace $p --only-show-errors | Out-Null
    }
}

$deploymentName = "lanternina-$EnvironmentName-$(Get-Date -Format 'yyyyMMdd-HHmmss')"

$parameters = @(
    "environmentName=$EnvironmentName"
    "location=$Location"
    "owner=$Owner"
)
if ($BudgetContactEmail) {
    $parameters += "budgetContactEmail=$BudgetContactEmail"
}

$command = if ($WhatIf) { 'what-if' } else { 'create' }
Write-Step "Running az deployment sub $command"

$argumentList = @(
    'deployment', 'sub', $command,
    '--name', $deploymentName,
    '--location', $Location,
    '--template-file', $templateFile,
    '--parameters', $parameterFile,
    '--parameters'
) + $parameters

& az @argumentList
if ($LASTEXITCODE -ne 0) {
    throw "Deployment failed with exit code $LASTEXITCODE"
}

if (-not $WhatIf) {
    Write-Step 'Outputs'
    az deployment sub show --name $deploymentName --query properties.outputs -o json

    Write-Host ''
    Write-Step 'Next: build and push the images, then point the apps at them'
    Write-Host '    ./scripts/build-and-deploy-images.ps1'
}

Write-Host ''
Write-Host "elapsed: $([math]::Round($sw.Elapsed.TotalSeconds, 1))s" -ForegroundColor DarkGray
