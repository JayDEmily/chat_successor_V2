$ErrorActionPreference='Stop'
Set-StrictMode -Version Latest
$path=Join-Path $PSScriptRoot '..\uia_adapter.ps1'
$tokens=$null
$errors=$null
$tree=[Management.Automation.Language.Parser]::ParseFile($path,[ref]$tokens,[ref]$errors)
if($errors.Count -ne 0){throw 'UIA adapter PowerShell syntax failed'}
foreach($name in @('Test-SameWorkerTurn','Test-FreshWorkerCompletion','Test-ViewRecoveryPaused',
                   'Check-Project','Chat-FromUrl','Find-TargetWindows','Get-TargetWindow')){
 $found=@($tree.FindAll({param($n) $n -is [Management.Automation.Language.FunctionDefinitionAst] -and $n.Name -eq $name},$true))
 if($found.Count -ne 1){throw "Function definition missing or ambiguous: $name"}
 Invoke-Expression $found[0].Extent.Text
}
$old=@{response_id='old';ready=$false;stop_control=$true;user_after_assistant=$false;assistant_turn_count=1;user_turn_count=1;latest_user_digest='same-user'}
$new=@{response_id='new';ready=$true;stop_control=$false;user_after_assistant=$false;assistant_turn_count=1;user_turn_count=1;latest_user_digest='same-user'}
if(-not (Test-FreshWorkerCompletion $old $new)){throw 'Valid completed fresh view rejected'}
if(Test-FreshWorkerCompletion $old $new @($new.response_id)){throw 'Consumed reply allows stale reload'}
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

# The wrapper pins the native profile. A matching URL and HWND alone are insufficient.
Add-Type -Path (Join-Path $PSScriptRoot '..\window_profile.cs')
$ProjectId='g-p-abc123'
$worker='00000000-0000-0000-0000-000000000001'
$url="https://chatgpt.com/g/$ProjectId/c/$worker"
$window=@{Current=@{NativeWindowHandle=55}; Profile='Chrome.Other'}
function Get-ChromeWindows { return $window }
function Get-Address($item) { return $url }
function Test-WindowProfile($item) { return ($item.Profile -ceq 'Chrome.Nominated') }
$wrongProfileHeld=$false
try { $null=Get-TargetWindow $worker 55 } catch {
    $wrongProfileHeld=$_.Exception.Message -like '*profile could not be verified*'
}
if(-not $wrongProfileHeld){throw 'Wrong Chrome profile selected by URL and handle'}
$window.Profile='Chrome.Nominated'
if((Get-TargetWindow $worker 55).chat -cne $worker){throw 'Verified profile target refused'}
if(Chat-FromUrl "https://chatgpt.com/g/$ProjectId/c/local-chatgpt"){throw 'Provisional successor treated as saved'}
Write-Output 'PASS: PS recovery comparisons and explicit holds for consumed replies, wrong Chrome profiles and provisional chat IDs.'
