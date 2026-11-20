$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest
Add-Type -AssemblyName UIAutomationTypes
Add-Type -AssemblyName UIAutomationClient

$parserErrors = $null
$tokens = $null
$script = Join-Path $PSScriptRoot '..\uia_adapter.ps1'
$tree = [Management.Automation.Language.Parser]::ParseFile($script,[ref]$tokens,[ref]$parserErrors)
if($parserErrors.Count){throw 'Windows adapter did not parse'}
foreach($name in @('Check-Project','Chat-FromUrl','Read-ChromeTurnSnapshot','Get-ChromeResponseId','Read-CurrentTurn','Find-PostedMessage')){
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
Check (Find-PostedMessage $target.window $snapshot.user '' $target.url) 'exact initial post has a saved destination'
$snapshot.previous=$null
$element.Payload=$snapshot | ConvertTo-Json -Compress
Check (-not (Find-PostedMessage $target.window $snapshot.user $first.response_id $target.url)) 'a missing preceding turn does not acknowledge a continuation'
