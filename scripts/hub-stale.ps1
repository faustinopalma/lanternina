# Which files on the hub differ from what is committed here, and which are not there at
# all. Compares the git blob content, not the working copy: this machine checks out CRLF
# and the hub holds LF, so a plain hash of the working copy would report every file as
# stale and say nothing.
#
# The packages are listed rather than discovered, because the question is "is the hub
# behind on what it runs" and not "does the hub hold the repository". On 24 August 2026 the
# list was devices and shared alone, and it reported a clean hub while `orchestrator/` was
# missing entirely — `devices/run_experience.py` imports it, so nothing there could begin
# an afternoon. A check that looks at two directories can only answer about two.
#
#   $p = "devices shared orchestrator printing vision"
#   ssh fausto@lanternina.local "cd /opt/lanternina && find $p -name '*.py' | sort |
#       xargs sha256sum | sed 's|  |,|'" | Out-File -Encoding utf8 $env:TEMP\hub-hashes.txt
#   git archive HEAD devices shared orchestrator printing vision | tar -x -C $env:TEMP\lnt-hub
#   powershell -NoProfile -File scripts\hub-stale.ps1
param(
    [string]$Tmp = "$env:TEMP\lnt-hub",
    [string]$HubHashes = "$env:TEMP\hub-hashes.txt",
    [string[]]$Packages = @("devices", "shared", "orchestrator", "printing", "vision")
)

$hub = @{}
foreach ($line in Get-Content $HubHashes) {
    $parts = $line -split ','
    if ($parts.Count -eq 2) { $hub[$parts[1].Trim() -replace '\\', '/'] = $parts[0].Trim() }
}

$found = 0
# Relative paths come from Resolve-Path rather than from subtracting one string length
# from another: $env:TEMP can be the 8.3 short form while FullName is the long one, and
# the arithmetic then eats the first characters of every path and calls them all missing.
Push-Location $Tmp
try {
    foreach ($package in $Packages) {
        if (-not (Test-Path $package)) { continue }
        foreach ($file in Get-ChildItem $package -Recurse -Filter *.py) {
            $rel = (Resolve-Path -Relative $file.FullName) -replace '^\.\\', '' -replace '\\', '/'
            $mine = (Get-FileHash $file.FullName -Algorithm SHA256).Hash.ToLower()
            if (-not $hub.ContainsKey($rel)) { "MISSING  $rel"; $found++ }
            elseif ($hub[$rel] -ne $mine) { "STALE    $rel"; $found++ }
        }
    }
}
finally { Pop-Location }
# Said out loud, because "nothing to report" and "the check did not run" look the same.
if ($found -eq 0) { "the hub matches this commit on: $($Packages -join ', ')" }
