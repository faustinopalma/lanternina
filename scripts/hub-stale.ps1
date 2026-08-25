# Which files on the hub differ from what is committed here, and which are not there at
# all. Compares the git blob content, not the working copy: this machine checks out CRLF
# and the hub holds LF, so a plain hash of the working copy would report every file as
# stale and say nothing.
#
#   powershell -NoProfile -File scripts\hub-stale.ps1
#
# The packages are listed rather than discovered, because the question is "is the hub
# behind on what it runs" and not "does the hub hold the repository". On 24 August 2026 the
# list was devices and shared alone, and it reported a clean hub while `orchestrator/` was
# missing entirely — `devices/run_experience.py` imports it, so nothing there could begin
# an afternoon. A check that looks at two directories can only answer about two.
#
# Three ways this has read "clean" while the hub was days behind, all closed here:
#
# 1. `git archive HEAD ... | tar -x` does not work. A PowerShell pipeline carries text, so
#    the tar stream is re-encoded and arrives corrupt; tar extracts nothing and the script
#    compares nothing. The archive is written to a file and extracted from the file.
# 2. Comparing nothing read the same as finding nothing. Both counts are guarded below.
# 3. Measured 25 August 2026: run on its own, it compared the leftovers of an earlier run
#    and reported a match against yesterday's commit while three files were missing from
#    the hub. So it now collects both sides itself, into a directory it makes and removes,
#    and trusts nothing it did not just write.
param(
    [string]$Hub = "fausto@lanternina.local",
    [string[]]$Packages = @("devices", "shared", "orchestrator", "printing", "vision")
)
$ErrorActionPreference = 'Stop'

$work = Join-Path ([IO.Path]::GetTempPath()) "lnt-hub-$(Get-Random)"
$tree = Join-Path $work 'tree'
New-Item -ItemType Directory -Path $tree -Force | Out-Null
try {
    $names = $Packages -join ' '
    $listing = ssh $Hub "cd /opt/lanternina && find $names -name '*.py' | sort | xargs sha256sum | sed 's|  |,|'"
    if ($LASTEXITCODE -ne 0) { throw "could not list the hub's files" }

    $archive = Join-Path $work 'hub.tar'
    git archive -o $archive HEAD @Packages
    if ($LASTEXITCODE -ne 0) { throw "could not archive HEAD" }
    tar -x -f $archive -C $tree
    if ($LASTEXITCODE -ne 0) { throw "could not extract the archive" }

    # Not `$hub`: PowerShell variable names are case-insensitive, so it would be the same
    # variable as the -Hub parameter and this would try to index a string.
    $there = @{}
    foreach ($line in $listing) {
        $parts = "$line" -split ','
        if ($parts.Count -eq 2) { $there[$parts[1].Trim() -replace '\\', '/'] = $parts[0].Trim() }
    }

    $found = 0
    $compared = 0
    # Relative paths come from Resolve-Path rather than from subtracting one string length
    # from another: the temp directory can be the 8.3 short form while FullName is the long
    # one, and the arithmetic then eats the first characters of every path.
    Push-Location $tree
    try {
        foreach ($package in $Packages) {
            if (-not (Test-Path $package)) { continue }
            foreach ($file in Get-ChildItem $package -Recurse -Filter *.py) {
                $compared++
                $rel = (Resolve-Path -Relative $file.FullName) -replace '^\.\\', '' -replace '\\', '/'
                $mine = (Get-FileHash $file.FullName -Algorithm SHA256).Hash.ToLower()
                if (-not $there.ContainsKey($rel)) { "MISSING  $rel"; $found++ }
                elseif ($there[$rel] -ne $mine) { "STALE    $rel"; $found++ }
            }
        }
        foreach ($name in ($there.Keys | Sort-Object)) {
            if (-not (Test-Path $name)) { "RETIRED  $name"; $found++ }
        }
    }
    finally { Pop-Location }

    # A check that compared nothing must not read as a check that found nothing.
    if ($compared -eq 0) { throw "compared 0 files: nothing was extracted, so this proves nothing" }
    if ($there.Count -eq 0) { throw "the hub listed 0 files, so this proves nothing" }
    # Said out loud, because "nothing to report" and "the check did not run" look the same.
    if ($found -eq 0) {
        "the hub matches $(git rev-parse --short HEAD) on $compared files: $($Packages -join ', ')"
    }
    else { "`n$found file(s) to put right, against $(git rev-parse --short HEAD)" }
}
finally { Remove-Item -Recurse -Force $work -ErrorAction SilentlyContinue }
