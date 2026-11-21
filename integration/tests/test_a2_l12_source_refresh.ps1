$ErrorActionPreference='Stop'
Set-StrictMode -Version Latest
Add-Type -AssemblyName UIAutomationClient
Add-Type -AssemblyName UIAutomationTypes
$adapter=Join-Path $PSScriptRoot '..\uia_adapter.ps1'
$tokens=$null;$errs=$null
$tree=[Management.Automation.Language.Parser]::ParseFile($adapter,[ref]$tokens,[ref]$errs)
if($errs.Count){throw ('Parser errors: '+($errs|Out-String))}
foreach($name in @('Request-FreshSuccessorReadback','Get-VerifiedSuccessorSource','Get-SafeSourcePreClickReason')){
 $nodes=@($tree.FindAll({
  param($node)
  $node -is [Management.Automation.Language.FunctionDefinitionAst] -and $node.Name -ceq $name
 },$false))
 if($nodes.Count -ne 1){throw ('Missing source helper '+$name)}
 . ([scriptblock]::Create($nodes[0].Extent.Text))
}
$script:ProjectId='g-p-11111111111111111111111111111111'
$script:ChromeAppId='verified-profile'
$script:chat='11111111-1111-1111-1111-111111111111'
$script:url="https://chatgpt.com/g/$ProjectId/c/$chat"
$script:view=@{window=[pscustomobject]@{Name='source-window'};url=$url;chat=$chat}
$script:beforeTime=[DateTimeOffset]::UtcNow.ToUnixTimeMilliseconds()-10000
$script:readerPayload=@{project=$ProjectId;chat=$chat;observedAt=[long]$beforeTime;phase='observed'}
$script:current=[pscustomobject]@{Value=($readerPayload|ConvertTo-Json -Compress);IsReadOnly=$true}
$script:pattern=[pscustomobject]@{}
$script:invokeEnabled=$true
$pattern|Add-Member ScriptMethod Invoke {
 if($script:invokeEnabled){
  $script:readerPayload.observedAt=[DateTimeOffset]::UtcNow.ToUnixTimeMilliseconds()
  $script:current.Value=$script:readerPayload|ConvertTo-Json -Compress
 }
}
$script:button=[pscustomobject]@{Current=[pscustomobject]@{
 ControlType=[System.Windows.Automation.ControlType]::Button
 Name='Chat Succession refresh source readback'
 ClassName='chat-succession-source-refresh';IsEnabled=$true}}
$button|Add-Member ScriptMethod GetCurrentPattern {param($kind) return $script:pattern}
$script:field=[pscustomobject]@{Current=[pscustomobject]@{
 ControlType=[System.Windows.Automation.ControlType]::Edit
 Name='Chat Succession Chrome readback'
 ClassName='chat-succession-readback'}}
$field|Add-Member ScriptMethod GetCurrentPattern {param($kind) return [pscustomobject]@{Current=$script:current}}
$script:elements=@($button,$field)
function Desc($window) {$script:elements}
function Get-Address($window) {$script:url}
function Test-WindowProfile($window) {$true}
function Assert-Case([bool]$ok,[string]$description){
 if(-not $ok){throw ('FAILED: '+$description)}
 Write-Output ('PASS: '+$description)
}
function Expect-Failure([scriptblock]$call,[string]$pattern){
 $err=''
 try{$null=&$call}catch{$err=$_.Exception.Message}
 Assert-Case ($err -like ('*'+$pattern+'*')) $pattern
}
Request-FreshSuccessorReadback $view
$after=$current.Value|ConvertFrom-Json
Assert-Case ($after.observedAt -gt $beforeTime -and
 [DateTimeOffset]::UtcNow.ToUnixTimeMilliseconds() - $after.observedAt -le 5000) 'readback refreshed on-demand'
Assert-Case ((Get-SafeSourcePreClickReason 'On-demand source readback did not advance') -ceq 'source_refresh_stalled') 'fixed stale-reason label'
$script:elements=@($field)
Expect-Failure {Request-FreshSuccessorReadback $view} 'missing or ambiguous'
$script:elements=@($button,$button,$field)
Expect-Failure {Request-FreshSuccessorReadback $view} 'missing or ambiguous'
$script:elements=@($button,$field)
$readerPayload.project='g-p-deadbeef'
$current.Value=$readerPayload|ConvertTo-Json -Compress
Expect-Failure {Request-FreshSuccessorReadback $view} 'wrong origin'
$readerPayload.project=$ProjectId
$readerPayload.observedAt=[DateTimeOffset]::UtcNow.ToUnixTimeMilliseconds()-10000
$current.Value=$readerPayload|ConvertTo-Json -Compress
$script:invokeEnabled=$false
Expect-Failure {Request-FreshSuccessorReadback $view} 'did not advance'
$script:invokeEnabled=$true
$current.IsReadOnly=$false
Expect-Failure {Request-FreshSuccessorReadback $view} 'not readonly'
$current.IsReadOnly=$true
$script:url="https://chatgpt.com/g/$ProjectId/c/99999999-9999-9999-9999-999999999999"
Expect-Failure {Request-FreshSuccessorReadback $view} 'identity unavailable'
$script:url=$view.url
$script:readerPayload.project=$ProjectId
$script:readerPayload.observedAt=[DateTimeOffset]::UtcNow.ToUnixTimeMilliseconds()-10000
$script:current.Value=$readerPayload|ConvertTo-Json -Compress
$script:invokeEnabled=$true
$script:ChatId=$chat
$expectedReply='chrome-turn-11111111-1111-1111-1111-111111111111-22222222-2222-2222-2222-222222222222'
function Get-TargetWindow($expectedChat,$handle){
 if($expectedChat -cne $script:chat){throw 'Wrong saved worker'}
 return $script:view
}
function Read-CurrentTurn($source){
 return @{ready=$true;method='CHROME_DOM';chrome_read_at=[DateTimeOffset]::UtcNow.ToUnixTimeMilliseconds();response_id='chrome-turn-11111111-1111-1111-1111-111111111111-22222222-2222-2222-2222-222222222222'}
}
$validSource=Get-VerifiedSuccessorSource $expectedReply
Assert-Case ($validSource.chat -ceq $chat) 'fresh source retains exact response anchor'
$readerPayload.observedAt=[DateTimeOffset]::UtcNow.ToUnixTimeMilliseconds()-10000
$current.Value=$readerPayload|ConvertTo-Json -Compress
Expect-Failure {Get-VerifiedSuccessorSource ($expectedReply+'different')} 'verified completion'
# Source UIA Invoke can activate its window. Target binding MUST come after.
$adapterText=[IO.File]::ReadAllText((Resolve-Path $adapter).Path)
$tail=$adapterText.Substring($adapterText.IndexOf('# The read-only source refresh may foreground'))
$sourceOffset=$tail.IndexOf('Get-VerifiedSuccessorSource $PendingResponseId')
$targetOffset=$tail.IndexOf('$liveEditor=Find-Composer $target.window $editorName')
Assert-Case ($sourceOffset -ge 0 -and $targetOffset -gt $sourceOffset) 'source refreshed before final target document and Send binding'
$ageGate=$tail.IndexOf("Hold-ForChangedDestination 'source_sample_expired_after_target'")
Assert-Case ($ageGate -gt $targetOffset -and $ageGate -lt $tail.IndexOf('Assert-PrivateDispatchReceipt',$targetOffset)) 'source evidence age checked after destination rebind and before dispatch'
Write-Output 'SOURCE_REFRESH_NO_SEND_TEST_PASS'
