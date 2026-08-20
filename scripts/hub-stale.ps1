# Which files on the hub differ from what is committed here. Compares the git blob
# content, not the working copy: this machine checks out CRLF and the hub holds LF, so a
# plain hash of the working copy would report every file as stale and say nothing.
#
#   ssh fausto@lanternina.local 'cd /opt/lanternina && sha256sum devices/*.py shared/*.py |
#       sed "s|  |,|"' | Out-File -Encoding utf8 $env:TEMP\hub-hashes.txt
#   git archive HEAD devices shared | tar -x -C $env:TEMP\lnt-hub
#   powershell -NoProfile -File scripts\hub-stale.ps1
param([string]$Tmp = "$env:TEMP\lnt-hub", [string]$HubHashes = "$env:TEMP\hub-hashes.txt")

$hub = @{}
foreach ($line in Get-Content $HubHashes) {
    $parts = $line -split ','
    if ($parts.Count -eq 2) { $hub[$parts[1].Trim()] = $parts[0].Trim() }
}
foreach ($file in Get-ChildItem "$Tmp\devices\*.py", "$Tmp\shared\*.py") {
    $rel = "$($file.Directory.Name)/$($file.Name)"
    $mine = (Get-FileHash $file.FullName -Algorithm SHA256).Hash.ToLower()
    if (-not $hub.ContainsKey($rel)) { "MISSING  $rel" }
    elseif ($hub[$rel] -ne $mine) { "STALE    $rel" }
}
