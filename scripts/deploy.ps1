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

    # Static Web Apps exist in five regions only, and a subscription may be barred from any
    # of them; westeurope is the sole European one, so overriding this leaves the EU.
    [string]$WebLocation = 'eastus2',

    [string]$Owner = $env:USERNAME,
    [string]$BudgetContactEmail = '',

    [switch]$Login,

    # Required when the account is a guest: without it az lands on the account's home tenant.
    [string]$Tenant = '',

    # Deploy knowing the home server will lose its only credential. The device routes then
    # answer 503 and the display keeps the picture it has.
    [switch]$WithoutDeviceKey,

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
    'Microsoft.CognitiveServices'
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
    "webLocation=$WebLocation"
    "owner=$Owner"
)

$dataResourceGroup = "rg-lanternina-$EnvironmentName-data"
$dataGroupExists = az group exists --name $dataResourceGroup | ConvertFrom-Json
$externalIdCount = if ($dataGroupExists) {
    $externalIdResources = az resource list `
        --resource-group $dataResourceGroup `
        --resource-type Microsoft.AzureActiveDirectory/ciamDirectories `
        -o json | ConvertFrom-Json
    @($externalIdResources).Count
} else {
    0
}
$deployExternalId = [int]$externalIdCount -eq 0
$parameters += "deployExternalId=$($deployExternalId.ToString().ToLowerInvariant())"

if ($BudgetContactEmail) {
    $parameters += "budgetContactEmail=$BudgetContactEmail"
}

# Bicep is declarative: anything the template does not carry is reset to its default. A
# plain run would therefore replace the API with the placeholder image and blank the
# sign-in configuration. Read what is running and hand it back in.
$appResourceGroup = "rg-lanternina-$EnvironmentName-app"
$liveApi = az containerapp show --name "ca-lanternina-$EnvironmentName-api" --resource-group $appResourceGroup -o json 2>$null | ConvertFrom-Json

if ($liveApi) {
    Write-Step 'Preserving what the API is already running'
    $liveEnv = @{}
    foreach ($item in $liveApi.properties.template.containers[0].env) { $liveEnv[$item.name] = $item.value }

    $parameters += "apiImage=$($liveApi.properties.template.containers[0].image)"
    $parameters += "apiTargetPort=$($liveApi.properties.configuration.ingress.targetPort)"
    $parameters += "panelDevAuth=$(if ($liveEnv['LANTERNINA_DEV_AUTH'] -eq '1') { 'true' } else { 'false' })"

    $carried = @{
        panelOidcAuthority   = 'LANTERNINA_OIDC_AUTHORITY'
        panelOidcAudience    = 'LANTERNINA_OIDC_AUDIENCE'
        panelAllowedOrigins  = 'LANTERNINA_ALLOWED_ORIGINS'
        panelBootstrapContact = 'LANTERNINA_BOOTSTRAP_CONTACT'
        panelAdminOidcAuthority = 'LANTERNINA_ADMIN_OIDC_AUTHORITY'
        panelAdminOidcAudience  = 'LANTERNINA_ADMIN_OIDC_AUDIENCE'
        panelAdminRole          = 'LANTERNINA_ADMIN_ROLE'
    }
    foreach ($name in $carried.Keys) {
        $value = $liveEnv[$carried[$name]]
        if ($value) { $parameters += "$name=$value" }
    }

    $liveWorker = az containerapp show --name "ca-lanternina-$EnvironmentName-worker" --resource-group $appResourceGroup -o json 2>$null | ConvertFrom-Json
    if ($liveWorker) { $parameters += "workerImage=$($liveWorker.properties.template.containers[0].image)" }
} else {
    Write-Step 'No API app yet: this is a first deploy'
}

# The key is the only credential the house holds, and it is not in the repository.
$secretsFile = Join-Path $repoRoot 'secrets.local.yaml'
$deviceKey = ''
if (Test-Path $secretsFile) {
    $found = Select-String -Path $secretsFile -Pattern '^\s*device_key\s*:\s*(.+)$' | Select-Object -First 1
    if ($found) { $deviceKey = $found.Matches[0].Groups[1].Value.Trim().Trim('"').Trim("'") }
}
if (-not $deviceKey -and -not $WithoutDeviceKey) {
    throw "No device_key in $secretsFile. Deploying without it removes the home server's only credential. Add it, or pass -WithoutDeviceKey to accept that."
}
# Inline, because az refuses a JSON parameter file alongside a .bicepparam file. The cost
# is that the key appears in this process's command line while the deployment runs.
if ($deviceKey) { $parameters += "deviceKey=$deviceKey" }

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
