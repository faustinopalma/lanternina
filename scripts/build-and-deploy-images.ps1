# Builds the panel image in ACR and redeploys the infrastructure pointing at it.
#
# The image is built server-side: no Docker needed locally, and the ARM64 laptop never
# has to produce an amd64 image.
#
# apiImage and apiTargetPort are passed together on purpose. They are the pair that broke
# the first deploy — ingress accepts the connection on a wrong port and then times out
# with no useful error, which is indistinguishable from a slow cold start.

[CmdletBinding()]
param(
    [string]$SubscriptionId = '',
    [string]$Owner = 'unknown',
    [string]$BudgetContactEmail = '',

    # Off by default, and it must stay off on anything reachable from the internet: with
    # it on the panel believes whatever X-Dev-Subject header it is handed.
    [switch]$DevAuth,

    [string]$BootstrapContact = '',

    # Both empty leaves the panel closed to everyone, which is the safe direction: the
    # audience is read from a real token rather than derived, so it arrives late.
    [string]$OidcAuthority = '',
    [string]$OidcAudience = '',

    [string]$Location = 'swedencentral'
)

$ErrorActionPreference = 'Stop'
$stopwatch = [Diagnostics.Stopwatch]::StartNew()

$repoRoot = Split-Path -Parent $PSScriptRoot
$env:AZURE_CONFIG_DIR = Join-Path $repoRoot '.azure'

# az acr build streams the server-side log, which contains non-ASCII. Without this the
# local CLI process dies on a UnicodeEncodeError while the build itself succeeds.
$env:PYTHONUTF8 = '1'
[Console]::OutputEncoding = [Text.Encoding]::UTF8

function Write-Step($message) {
    Write-Host "[$([math]::Round($stopwatch.Elapsed.TotalSeconds,1))s] $message" -ForegroundColor Cyan
}

if ($SubscriptionId) { az account set --subscription $SubscriptionId | Out-Null }

Write-Step 'Locating the registry'
$registries = az acr list -o json | ConvertFrom-Json
$registry = $registries | Where-Object { $_.name -like '*lanternina*' }
if (-not $registry) { throw 'No Lanternina container registry found. Run scripts/deploy.ps1 first.' }
Write-Step "Registry: $($registry.loginServer)"

# Tagged by commit so a running revision can always be traced back to a source tree.
$gitSha = (git -C $repoRoot rev-parse --short HEAD).Trim()
$dirty = (git -C $repoRoot status --porcelain)
$tag = if ($dirty) { "$gitSha-dirty-$(Get-Date -Format 'yyyyMMddHHmmss')" } else { $gitSha }
$image = "lanternina/panel:$tag"

Write-Step "Building $image in ACR"
az acr build --registry $registry.name --image $image --file Dockerfile $repoRoot

# The CLI can die while streaming logs even though the server-side build succeeded, so
# the image is confirmed to exist rather than trusted to the exit code.
Write-Step 'Confirming the image was pushed'
$tags = az acr repository show-tags --name $registry.name --repository 'lanternina/panel' -o json | ConvertFrom-Json
if ($tags -notcontains $tag) { throw "Tag $tag is not in the registry. The build did not push." }
Write-Step "Confirmed: $($registry.loginServer)/$image"

Write-Step 'Deploying infrastructure against the new image'
$deploymentName = "lanternina-panel-$(Get-Date -Format 'yyyyMMddHHmmss')"
az deployment sub create `
    --name $deploymentName `
    --location $Location `
    --template-file (Join-Path $repoRoot 'infra/main.bicep') `
    --parameters `
        owner=$Owner `
        budgetContactEmail=$BudgetContactEmail `
        apiImage="$($registry.loginServer)/$image" `
        apiTargetPort=8000 `
        panelDevAuth=$($DevAuth.IsPresent.ToString().ToLower()) `
        panelBootstrapContact=$BootstrapContact `
        panelOidcAuthority=$OidcAuthority `
        panelOidcAudience=$OidcAudience `
    --output none

Write-Step 'Verifying'
$fqdn = az containerapp show --name ca-lanternina-dev-api --resource-group rg-lanternina-dev-app --query 'properties.configuration.ingress.fqdn' -o tsv
$health = Invoke-WebRequest -Uri "https://$fqdn/health" -TimeoutSec 90 -UseBasicParsing
Write-Host "health: HTTP $($health.StatusCode) $($health.Content)" -ForegroundColor Green
Write-Host "panel:  https://$fqdn" -ForegroundColor Green
Write-Host "elapsed: $([math]::Round($stopwatch.Elapsed.TotalSeconds,1))s"
