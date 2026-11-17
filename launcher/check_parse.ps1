# Pure parse check. Never executes the launcher or invokes any browser APIs.
$ErrorActionPreference = 'Stop'
$path = Join-Path $PSScriptRoot 'launch.ps1'
$parseErrors = $null
$tokens = $null
[void][System.Management.Automation.Language.Parser]::ParseFile(
    $path, [ref]$tokens, [ref]$parseErrors)
if (@($parseErrors).Count -ne 0) {
    foreach ($problem in $parseErrors) {
        Write-Output ('PARSE_ERROR: ' + $problem.Message)
    }
    exit 1
}
Write-Output 'PARSE_OK: launch.ps1'
