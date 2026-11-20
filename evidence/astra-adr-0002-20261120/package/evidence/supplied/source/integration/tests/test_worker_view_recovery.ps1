$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest

$adapter = Join-Path (Split-Path -Parent $PSScriptRoot) 'uia_adapter.ps1'
$tokens = $null
$parseErrors = $null
$syntax = [System.Management.Automation.Language.Parser]::ParseFile($adapter, [ref]$tokens, [ref]$parseErrors)
if ($parseErrors) { throw ($parseErrors | Out-String) }

# Load only the pure comparisons to test the reload boundary without Chrome.
foreach ($name in @('Test-SameWorkerTurn', 'Test-FreshWorkerCompletion')) {
    $definition = $syntax.Find({
        param($node)
        $node -is [System.Management.Automation.Language.FunctionDefinitionAst] -and $node.Name -eq $name
    }, $false)
    if ($null -eq $definition) { throw "Missing recovery comparison $name" }
    . ([scriptblock]::Create($definition.Extent.Text))
}

$original = @{
    response_id = 'partial-turn'; ready = $false; stop_control = $true
    user_after_assistant = $false; assistant_turn_count = 3
    user_turn_count = 3; latest_user_digest = 'same-user-text'
}
$fresh = $original.Clone()
$fresh['ready'] = $true
$fresh['stop_control'] = $false
$fresh['response_id'] = 'completed-turn'
if (-not (Test-FreshWorkerCompletion $original $fresh)) { throw 'A completed rendering of the same user turn should allow reload' }
if (Test-SameWorkerTurn $original $fresh) { throw 'Original view advanced while probing' }
if (-not (Test-SameWorkerTurn $fresh ($fresh.Clone()))) { throw 'The stable fresh turn should match itself' }

$differentUserTurn = $fresh.Clone()
$differentUserTurn['latest_user_digest'] = 'edited-user-text'
if (Test-FreshWorkerCompletion $original $differentUserTurn) { throw 'An edited user turn must hold reload' }
$differentUserTurn['latest_user_digest'] = $fresh['latest_user_digest']
$differentUserTurn['user_turn_count']++
if (Test-FreshWorkerCompletion $original $differentUserTurn) { throw 'A later user turn with the same text must hold reload' }

$olderView = $fresh.Clone()
$olderView['assistant_turn_count']--
if (Test-FreshWorkerCompletion $original $olderView) { throw 'An older completed view must hold reload' }
$completedOriginal = $fresh.Clone()
$completedOriginal['response_id'] = 'already-consumed-turn'
if (Test-FreshWorkerCompletion $completedOriginal $fresh) { throw 'A different digest at the same assistant ordinal is insufficient' }
$fresh['assistant_turn_count']++
if (-not (Test-FreshWorkerCompletion $completedOriginal $fresh)) { throw 'A later completed assistant turn can refresh an unchanged consumed view' }

Write-Output 'Saved worker view recovery comparisons passed'
