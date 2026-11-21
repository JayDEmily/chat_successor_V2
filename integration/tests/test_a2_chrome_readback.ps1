$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest
Add-Type -AssemblyName UIAutomationTypes
Add-Type -AssemblyName UIAutomationClient

$parserErrors = $null
$tokens = $null
$script = Join-Path $PSScriptRoot '..\uia_adapter.ps1'
$tree = [Management.Automation.Language.Parser]::ParseFile($script,[ref]$tokens,[ref]$parserErrors)
if($parserErrors.Count){throw 'Windows adapter did not parse'}
foreach($name in @('Check-Project','Chat-FromUrl','Read-ChromeTurnSnapshot','Get-ChromeResponseId','Read-CurrentTurn',
                   'Find-PostedMessage','Compare-OwnerTurn','Get-VerifiedSuccessorSource','Maximize-ChromeWorkerWindow')){
 $nodes=@($tree.FindAll({
  param($node)
  $node -is [Management.Automation.Language.FunctionDefinitionAst] -and $node.Name -ceq $name
 },$false))
 if($nodes.Count -ne 1){throw "Missing or ambiguous function $name"}
 . ([scriptblock]::Create($nodes[0].Extent.Text))
}

$ProjectId='g-p-11111111111111111111111111111111'
$ChromeAppId='Chrome.UserData.Test'
$chat='11111111-1111-1111-1111-111111111111'
$target=@{url="https://chatgpt.com/g/$ProjectId/c/$chat";chat=$chat;window=@{}}
$element=[pscustomobject]@{
 Current=@{Name='Chat Succession Chrome readback';ClassName='chat-succession-readback'
           ControlType=[System.Windows.Automation.ControlType]::Edit}
 Payload=''
}
$element | Add-Member ScriptMethod GetCurrentPattern {
 param($pattern)
 return @{Current=@{Value=$this.Payload;IsReadOnly=$true}}
}
$script:elements=@($element)
function Desc($window){$script:elements}
function Get-Address($window){$target.url}
function Test-WindowProfile($window){$true}

function Check([bool]$condition,[string]$description){
 if(-not $condition){throw "FAIL: $description"}
 Write-Output "PASS: $description"
}
function Expect-Hold([scriptblock]$read,[string]$reason){
 $observedError=''
 try{$null=&$read}catch{$observedError=$_.Exception.Message}
 Check ($observedError -like "*$reason*") $reason
}

$snapshot=@{
 project=$ProjectId;chat=$chat;phase='observed';observedAt=[DateTimeOffset]::UtcNow.ToUnixTimeMilliseconds()
 key='22222222-2222-2222-2222-222222222222';user='Exact submitted text';userAfterAssistant=$false;previous=$null
 reply=@{id='33333333-3333-3333-3333-333333333333';text="Full reply.`nCHAT_STATUS: NEED_MORE_TIME";final=$true;handoff=$false}
}
$element.Payload=$snapshot | ConvertTo-Json -Compress
$first=Read-CurrentTurn $target -IncludeUserAnchor
Check ($first.ready -and $first.text -ceq $snapshot.reply.text -and $first.method -ceq 'CHROME_DOM') 'complete reply is exact'
Check ($first.response_id -ceq ('chrome-turn-' + $snapshot.key + '-' + $snapshot.reply.id)) 'stable user and assistant IDs establish the event'
Check ($null -eq $first.assistant_turn_count -and $null -eq $first.user_turn_count) 'visible rows give no absolute count'

$snapshot.key='44444444-4444-4444-4444-444444444444'
$snapshot.reply.id='55555555-5555-5555-5555-555555555555'
$element.Payload=$snapshot | ConvertTo-Json -Compress
$repeat=Read-CurrentTurn $target
Check ($repeat.ready -and $repeat.text -ceq $first.text -and $repeat.response_id -cne $first.response_id) 'identical text in another turn has another identity'
$snapshot.reply.final=$false
$element.Payload=$snapshot | ConvertTo-Json -Compress
Check (-not (Read-CurrentTurn $target).ready) 'a non-prose final line stays non-actionable'
$snapshot.reply=$null
$element.Payload=$snapshot | ConvertTo-Json -Compress
$partial=Read-CurrentTurn $target
Check (-not $partial.ready -and -not $partial.user_after_assistant -and -not $partial.response_id) 'partial hydration stays non-actionable'
$snapshot.phase='offscreen'
$element.Payload=$snapshot | ConvertTo-Json -Compress
Expect-Hold {Read-CurrentTurn $target} 'could not establish the latest visible turn'
$snapshot.chat='99999999-9999-9999-9999-999999999999'
$element.Payload=$snapshot | ConvertTo-Json -Compress
Expect-Hold {Read-CurrentTurn $target} 'different Project or saved chat'
$snapshot.chat=$chat
$snapshot.observedAt=[DateTimeOffset]::UtcNow.ToUnixTimeMilliseconds()-6000
$element.Payload=$snapshot | ConvertTo-Json -Compress
Expect-Hold {Read-CurrentTurn $target} 'sample has expired'
$script:elements=@($element,$element)
Expect-Hold {Read-CurrentTurn $target} 'ambiguous or has no verified saved destination'

$script:elements=@($element)
$snapshot.observedAt=[DateTimeOffset]::UtcNow.ToUnixTimeMilliseconds()
$snapshot.phase='observed'
$snapshot.userAfterAssistant=$true
$snapshot.previous=@{key='22222222-2222-2222-2222-222222222222'
                     reply=@{id='33333333-3333-3333-3333-333333333333'}}
$element.Payload=$snapshot | ConvertTo-Json -Depth 4 -Compress
Check (Find-PostedMessage $target.window $snapshot.user $first.response_id $target.url) 'exact continuation immediately after its verified reply'
Check (-not (Find-PostedMessage $target.window $snapshot.user $repeat.response_id $target.url)) 'identical text with a different reply anchor does not acknowledge'
Check (-not (Find-PostedMessage $target.window 'Exact submitted' $first.response_id $target.url)) 'matching fragment does not acknowledge'
Check (-not (Find-PostedMessage $target.window $snapshot.user $first.response_id "https://chatgpt.com/g/$ProjectId/c/local-chatgpt%3Afixture")) 'provisional URL does not acknowledge'
$snapshot.phase='unqualified'
$element.Payload=$snapshot | ConvertTo-Json -Depth 4 -Compress
Check (-not (Find-PostedMessage $target.window $snapshot.user '' $target.url)) 'unqualified rendered post cannot acknowledge on a saved URL'
$snapshot.phase='observed'
$element.Payload=$snapshot | ConvertTo-Json -Depth 4 -Compress
Check (Find-PostedMessage $target.window $snapshot.user '' $target.url) 'same exact initial post acknowledges after the rendered IDs qualify'
$snapshot.previous=$null
$element.Payload=$snapshot | ConvertTo-Json -Compress
Check (-not (Find-PostedMessage $target.window $snapshot.user $first.response_id $target.url)) 'a missing preceding turn does not acknowledge a continuation'

$legacy='uia-turn-1-aaaaaaaaaaaaaaaaaaaa'
$moving=@{ready=$false;user_after_assistant=$true;stop_control=$true;method='CHROME_DOM'}
Check ((Compare-OwnerTurn $moving $legacy) -ceq 'unknown') 'a legacy pending anchor holds even while Chrome is streaming'
$moving.method='UIA_ACCESSIBILITY_TEXT'
Check ((Compare-OwnerTurn $moving $first.response_id) -ceq 'unknown') 'a Chrome pending anchor holds if the native reader takes over'
$moving.method='CHROME_DOM'
Check ((Compare-OwnerTurn $moving $first.response_id) -ceq 'unknown') 'partial rendering does not establish Chrome advancement'
$moving.previous_response_id=$first.response_id
Check ((Compare-OwnerTurn $moving $first.response_id) -ceq 'advanced') 'Chrome advancement is bound to the exact prior reply'
Check (-not (Find-PostedMessage $target.window $snapshot.user '' $target.url $legacy)) 'a native pending successor cannot adopt a Chrome receipt'

function Get-ObservableSavedTarget {return $target}
function Get-TargetWindow($expectedChat,$handle){return $target}
function Open-ChromeWindow($url){throw 'Unexpected browser open in source validation test'}
function Read-CurrentTurn($view){return $moving}
function Invoke-AdapterMode([string]$name){
 $conditionText='$Mode -eq ' + "'" + $name + "'"
 $block=$tree.Find({
  param($node)
  $node -is [Management.Automation.Language.IfStatementAst] -and
    $node.Clauses[0].Item1.Extent.Text -ceq $conditionText
 },$false)
 if($null -eq $block){throw "Could not find adapter mode $name"}
 & ([scriptblock]::Create($block.Extent.Text.Replace('exit 0','return')))
}

$ChatId=$chat
$OwnerAnchor=$legacy
$Mode='ObserveReentry'
Expect-Hold {Invoke-AdapterMode $Mode} 'could not verify advancement from the saved reply anchor'
$moving.ready=$true
$moving.response_id=$first.response_id
Check ((Get-VerifiedSuccessorSource $first.response_id).chat -ceq $chat) 'a successor has an affirmative saved source proof'
$Mode='Prepare'
$Kind='LAUNCH_SUCCESSOR'
$ProjectUrl="https://chatgpt.com/g/$ProjectId/project"
$SourceResponse=$legacy
$Preflight=$false
foreach($WindowHandle in @(0,123)){
 Expect-Hold {Invoke-AdapterMode $Mode} 'no longer shows the verified completion'
}

$Mode='ObserveReentry'
$OwnerAnchor=$first.response_id
$moving.stop_control=$false
$moving.user_after_assistant=$false
$moving.response_id=$repeat.response_id
$element.Payload=''
function Find-Composer($window,$name){return $element}
function Read-ComposerText($editor,$value){return $value}
function Check-NoAttachments($window){return $true}
function Find-EnabledSendButtons($window){}
$visible=Invoke-AdapterMode $Mode | ConvertFrom-Json
Check ($visible.disposition -ceq 'advanced') 'verified completed advancement is observation-only in the existing view'

$fresh=[pscustomobject]@{Current=@{NativeWindowHandle=123};Closed=$false}
$fresh | Add-Member ScriptMethod GetCurrentPattern {param($pattern) return $this}
$fresh | Add-Member ScriptMethod Close {$this.Closed=$true}
function Read-CurrentTurn($view){
 if($view.window -eq $fresh){return $moving}
 return $first
}
function Get-TargetWindow($expectedChat,$handle){return @{window=$fresh;chat=$chat;url=$target.url}}
function Open-ChromeWindow($url){
 $element.Payload='Owner draft entered during the fresh read'
 return $fresh
}
function Start-Sleep([int]$Milliseconds){}
function Desc($window){throw 'Unexpected Reload lookup during owner re-entry'}
$freshResult=Invoke-AdapterMode $Mode | ConvertFrom-Json
Check ($freshResult.disposition -ceq 'advanced' -and $fresh.Closed) 'fresh advancement closes only its comparison view'
Check ($element.Payload -ceq 'Owner draft entered during the fresh read') 'advanced re-entry leaves the original draft intact'

$visualState=[System.Windows.Automation.WindowVisualState]
$pattern=[pscustomobject]@{Current=@{CanMaximize=$true;IsModal=$false;WindowVisualState=$visualState::Normal};Requests=0}
$script:changeRouteOnMaximize=$false
$script:observedProjectUrl=$ProjectUrl
$pattern | Add-Member ScriptMethod SetWindowVisualState {
 param($state)
 $this.Current.WindowVisualState=$state
 $this.Requests++
 if($script:changeRouteOnMaximize){
  $script:observedProjectUrl='https://chatgpt.com/g/g-p-00000000000000000000000000000000/project'
  throw [InvalidOperationException]::new('Window provider failed after changing geometry')
 }
}
$workerWindow=[pscustomobject]@{Current=@{NativeWindowHandle=124};Pattern=$pattern}
$workerWindow | Add-Member ScriptMethod TryGetCurrentPattern {
 param($kind,$result)
 $result.Value=$this.Pattern
 return ($kind -eq [System.Windows.Automation.WindowPattern]::Pattern -and $null -ne $this.Pattern)
}
$script:opens=0
function Open-ChromeWindow($url){$script:opens++;return $workerWindow}
function Get-Address($window){return $script:observedProjectUrl}
function Get-TargetWindow($expectedChat,$handle){return @{window=$workerWindow;chat=$null;url=$ProjectUrl}}
function Get-ComposerDocument($editor){return $editor}
function Get-DocumentIdentity($document){return 'worker-composer'}

$Mode='Prepare'
$ChatId=''
$SourceResponse=''
$WindowHandle=0
$ProjectName='Shoko fixture'
$element.Payload=''
$created=Invoke-AdapterMode $Mode | ConvertFrom-Json
Check ($created.private_window_handle -eq 124 -and $script:opens -eq 1 -and
       $pattern.Current.WindowVisualState -eq $visualState::Maximized -and $pattern.Requests -eq 1) 'fresh worker window is maximized once'
$pattern.Current.WindowVisualState=$visualState::Normal
$ChatId=$chat
$WindowHandle=124
$reused=Invoke-AdapterMode $Mode | ConvertFrom-Json
Check ($reused.private_window_handle -eq 124 -and $script:opens -eq 1 -and $pattern.Requests -eq 1) 'resuming a prepared window leaves its size alone'
$ChatId=''
$WindowHandle=0
$workerWindow.Pattern=$null
$unsupported=Invoke-AdapterMode $Mode | ConvertFrom-Json
Check ($unsupported.private_window_handle -eq 124 -and $script:opens -eq 2 -and $pattern.Requests -eq 1) 'fresh composer can still verify without a window pattern'

$workerWindow.Pattern=$pattern
$script:changeRouteOnMaximize=$true
Expect-Hold {Invoke-AdapterMode $Mode} 'Fresh Project composer not established'
