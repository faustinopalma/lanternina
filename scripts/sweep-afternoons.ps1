# Remove the afternoon documents for one household, from inside the container app --
# Cosmos is behind a private endpoint and nothing outside the app can reach it.
#
# Pictures are blobs in Storage, not documents in Cosmos, so they are not reachable from
# this script at all. That is the shape of the system, not a precaution taken here.
#
# Run without -remove first: it lists what it would delete and touches nothing.
#     .\scripts\sweep-afternoons.ps1 hh_9a6d6e38
#     .\scripts\sweep-afternoons.ps1 hh_9a6d6e38 -remove
$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
$env:AZURE_CONFIG_DIR = Join-Path $root '.azure'

$household = $args[0]
if (-not $household) { throw "usage: sweep-afternoons.ps1 <household-id> [-remove]" }
$remove = $args -contains '-remove'
$app = 'ca-lanternina-dev-api'
$group = 'rg-lanternina-dev-app'

$python = @"
import os, json
from azure.cosmos import CosmosClient
from azure.identity import DefaultAzureCredential
c = CosmosClient(os.environ["LANTERNINA_COSMOS_ENDPOINT"], credential=DefaultAzureCredential()).get_database_client(os.environ["LANTERNINA_COSMOS_DATABASE"]).get_container_client("sources")
h = "$household"
rows = list(c.query_items(query="SELECT c.id, c.state FROM c WHERE c.type='experience' AND c.familyId=@f", parameters=[{"name":"@f","value":h}], enable_cross_partition_query=True))
print("AFTERNOONS", json.dumps(rows))
if $(if ($remove) { 'True' } else { 'False' }):
    for r in rows:
        c.delete_item(item=r["id"], partition_key=h)
    print("REMOVED", len(rows))
"@

$b64 = [Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes($python))

# `containerapp exec --command` splits on whitespace AND strips every quote, interior ones
# included. Measured: `python -c "import base64,sys;..."` arrived as the single word
# `import`, and `__import__("base64")` arrived as `__import__(base64)`. So the program can
# contain neither a space nor a quote, and the module names are spelled with chr().
function Spell($word) {
    ($word.ToCharArray() | ForEach-Object { "chr($([int][char]$_))" }) -join '+'
}
$program = "exec(__import__($(Spell 'base64')).b64decode(__import__($(Spell 'sys')).argv[1]))"
$command = "python -c $program $b64"

Write-Output "household: $household   remove: $remove   payload: $($b64.Length) chars"
# The az launcher on Windows is a .cmd, and cmd.exe re-parses the arguments and breaks on
# the inner double quotes. Calling the module keeps PowerShell's argv intact.
$azPython = "C:\Program Files\Microsoft SDKs\Azure\CLI2\python.exe"
& $azPython -IBm azure.cli containerapp exec -n $app -g $group --command $command
