$ErrorActionPreference='Stop'
Set-StrictMode -Version Latest
$path=Join-Path $PSScriptRoot '..\uia_adapter.ps1'
$tokens=$null
$errors=$null
$tree=[Management.Automation.Language.Parser]::ParseFile($path,[ref]$tokens,[ref]$errors)
if($errors.Count -ne 0){throw 'UIA adapter PowerShell syntax failed'}
foreach($name in @('Test-SameWorkerTurn','Test-FreshWorkerCompletion','Test-ViewRecoveryPaused')){
 $found=@($tree.FindAll({param($n) $n -is [Management.Automation.Language.FunctionDefinitionAst] -and $n.Name -eq $name},$true))
 if($found.Count -ne 1){throw "Function definition missing or ambiguous: $name"}
 Invoke-Expression $found[0].Extent.Text
}
$old=@{response_id='old';ready=$false;stop_control=$true;user_after_assistant=$false;assistant_turn_count=1;user_turn_count=1;latest_user_digest='same-user'}
$new=@{response_id='new';ready=$true;stop_control=$false;user_after_assistant=$false;assistant_turn_count=1;user_turn_count=1;latest_user_digest='same-user'}
if(-not (Test-FreshWorkerCompletion $old $new)){throw 'Valid completed fresh view rejected'}
$stream=@{}+$new
$stream.ready=$false
if(Test-FreshWorkerCompletion $old $stream){throw 'Streaming fresh view incorrectly treated as completed'}
$other=@{}+$new
$other.latest_user_digest='other-user'
if(Test-FreshWorkerCompletion $old $other){throw 'Changed user turn incorrectly accepted'}
$otherCount=@{}+$new
$otherCount.user_turn_count=2
if(Test-FreshWorkerCompletion $old $otherCount){throw 'Changed user count incorrectly accepted'}
$stable=@{}+$new
if(-not (Test-SameWorkerTurn $new $stable)){throw 'Stable fresh double-read rejected'}
$changed=@{}+$new
$changed.response_id='another-reply'
if(Test-SameWorkerTurn $new $changed){throw 'Different response accepted as stable double-read'}
$PausePath=Join-Path $env:TEMP 'a2-l04-test-marker.pause'
try{
 if(Test-ViewRecoveryPaused){throw 'Unexpected marker before test'}
 [IO.File]::WriteAllText($PausePath,'pause marker test')
 if(-not (Test-ViewRecoveryPaused)){throw 'Durable marker not recognised'}
}finally{
 Remove-Item -LiteralPath $PausePath -Force -ErrorAction SilentlyContinue
}
Write-Output 'PASS: PS recovery helpers; positive newer completed same-user, negative streaming/user-anchor/count, stable fresh pair, rejected changed response, durable pause marker.'
