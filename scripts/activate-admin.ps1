<#
.SYNOPSIS
    Activates an eligible Entra directory role through PIM, for this process only.

.DESCRIPTION
    PIM activation expires, so this is not a one-off: it has to be repeated at the start
    of any session that configures the directory.

    The connection uses -ContextScope Process, so nothing is written to the shared MSAL
    cache under %LOCALAPPDATA%\.IdentityService. The cost is that the activated context
    dies with this process; anything that needs it must run inside the same script.

.EXAMPLE
    ./scripts/activate-admin.ps1 -TenantId 937847db-d3f9-4c7b-9991-510e5c42f777
#>
[CmdletBinding()]
param(
    [Parameter(Mandatory)]
    [string]$TenantId,

    [string]$RoleName = 'Global Administrator',

    # Entra clamps this to whatever the role policy allows; the request fails if it is over.
    [ValidateRange(1, 8)]
    [int]$Hours = 4,

    [string]$Justification = 'Automated Lanternina directory setup'
)

$ErrorActionPreference = 'Stop'
$sw = [Diagnostics.Stopwatch]::StartNew()

function Write-Step($message) { Write-Host "==> $message" -ForegroundColor Cyan }

Import-Module Microsoft.Graph.Authentication

$scopes = @(
    'RoleEligibilitySchedule.Read.Directory'
    'RoleAssignmentSchedule.ReadWrite.Directory'
    'RoleManagement.ReadWrite.Directory'
)

Write-Step 'Signing in to Microsoft Graph (device code, nothing persisted)'
Connect-MgGraph -TenantId $TenantId -Scopes $scopes -UseDeviceCode -ContextScope Process -NoWelcome

$ctx = Get-MgContext
Write-Step "Signed in as $($ctx.Account)"

$me = Invoke-MgGraphRequest -Method GET -Uri 'v1.0/me?$select=id,userPrincipalName'
$principalId = $me.id

Write-Step "Looking for an eligible '$RoleName'"
$filter = [uri]::EscapeDataString("principalId eq '$principalId'")
$eligible = (Invoke-MgGraphRequest -Method GET `
    -Uri "v1.0/roleManagement/directory/roleEligibilityScheduleInstances?`$filter=$filter&`$expand=roleDefinition").value

if (-not $eligible) {
    throw "No eligible directory roles for $($ctx.Account). Nothing to activate."
}

Write-Host '    eligible:' -ForegroundColor DarkGray
$eligible | ForEach-Object { Write-Host "      - $($_.roleDefinition.displayName)" -ForegroundColor DarkGray }

$target = $eligible | Where-Object { $_.roleDefinition.displayName -eq $RoleName } | Select-Object -First 1
if (-not $target) {
    throw "'$RoleName' is not among the eligible roles listed above."
}

$body = @{
    action           = 'selfActivate'
    principalId      = $principalId
    roleDefinitionId = $target.roleDefinitionId
    directoryScopeId = $target.directoryScopeId
    justification    = $Justification
    scheduleInfo     = @{
        startDateTime = (Get-Date).ToUniversalTime().ToString('o')
        expiration    = @{ type = 'AfterDuration'; duration = "PT${Hours}H" }
    }
}

Write-Step "Requesting activation for $Hours hour(s)"
$request = Invoke-MgGraphRequest -Method POST `
    -Uri 'v1.0/roleManagement/directory/roleAssignmentScheduleRequests' `
    -Body ($body | ConvertTo-Json -Depth 10) -ContentType 'application/json'

Write-Step "Request $($request.id): $($request.status)"

# Activation is not always immediate, and "Granted" is the only status that means anything.
$deadline = (Get-Date).AddMinutes(3)
do {
    $state = (Invoke-MgGraphRequest -Method GET `
        -Uri "v1.0/roleManagement/directory/roleAssignmentScheduleRequests/$($request.id)").status
    Write-Host ("    [{0}] {1:N0}s  status={2}" -f (Get-Date -Format 'HH:mm:ss'), $sw.Elapsed.TotalSeconds, $state)
    if ($state -in @('Provisioned', 'Granted')) { break }
    if ($state -in @('Failed', 'Canceled', 'Denied')) { throw "Activation ended as $state." }
    Start-Sleep -Seconds 15
} while ((Get-Date) -lt $deadline)

Write-Host ''
Write-Host "VERDICT: $state" -ForegroundColor Green
Write-Host "elapsed: $([math]::Round($sw.Elapsed.TotalSeconds, 1))s" -ForegroundColor DarkGray
