$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest
$source = Join-Path $PSScriptRoot '..\uia_adapter.ps1'
$tokens = $null
$errors = $null
$ast = [System.Management.Automation.Language.Parser]::ParseFile($source, [ref]$tokens, [ref]$errors)
if($errors.Count -ne 0){ throw ('PS_PARSE_FAIL: ' + ($errors | ForEach-Object { $_.Message } | Out-String)) }
$functions = @($ast.FindAll({ param($node) $node -is [System.Management.Automation.Language.FunctionDefinitionAst] -and $node.Name -eq 'Assert-PrivateDispatchReceipt' }, $true))
if($functions.Count -ne 1){throw 'Exact action-check function not found once'}
Invoke-Expression $functions[0].Extent.Text
$PrepareAction = 'a2-action-id-1'
$RouteReceipt = ''
$OwnerInputPath = ''
$PendingResponseId = 'uia-turn-1-aaa00000000000000000'
$BootstrapRunId = ''
$BootstrapActionId = ''
$PrepareTargetPath = Join-Path $env:TEMP 'a2-ps-target-receipt-test.json'
$BootstrapIntentPath = ''
$ProjectId = 'g-p-TEST'
$Kind = 'CONTINUE_CURRENT'
$ChatId = 'worker-first'
$SourceResponse = 'uia-turn-1-aaa00000000000000000'
$WindowHandle = [long]222
$DocumentId = '42.222'
$Message = 'Okay, continue working.'
$Mode = 'Send'
$hash = [Security.Cryptography.SHA256]::Create()
try {
    $digest = [BitConverter]::ToString($hash.ComputeHash([Text.Encoding]::UTF8.GetBytes($Message))).Replace('-','').ToLowerInvariant()
} finally { $hash.Dispose() }
$record = [ordered]@{ action_id=$PrepareAction; project=$ProjectId; kind=$Kind; source=$ChatId; handle=$WindowHandle; document_id=$DocumentId; message_sha256=$digest; source_response=$SourceResponse; route_receipt=$RouteReceipt }
try {
  [IO.File]::WriteAllText($PrepareTargetPath, ($record | ConvertTo-Json -Compress), [Text.Encoding]::UTF8)
  Assert-PrivateDispatchReceipt
  $OwnerInputPath = [IO.Path]::GetTempFileName()
  $ownerReceipt = [IO.Path]::ChangeExtension($OwnerInputPath, '.sha256')
  try {
    [IO.File]::WriteAllText($OwnerInputPath, 'Synthetic scoped input')
    [IO.File]::WriteAllText($ownerReceipt, (Get-FileHash -LiteralPath $OwnerInputPath).Hash.ToLowerInvariant())
    Assert-PrivateDispatchReceipt
    [IO.File]::WriteAllText($OwnerInputPath, 'Substituted scope')
    $failed=$false
    try { Assert-PrivateDispatchReceipt } catch { $failed=$true }
    if(-not $failed){throw 'SUBSTITUTED_OWNER_INPUT_ACCEPTED'}
  } finally {
    Remove-Item -LiteralPath $OwnerInputPath,$ownerReceipt -ErrorAction SilentlyContinue
    $OwnerInputPath=''
  }
  $record['action_id']='stale-other-action'
  [IO.File]::WriteAllText($PrepareTargetPath, ($record | ConvertTo-Json -Compress), [Text.Encoding]::UTF8)
  $failed=$false
  try { Assert-PrivateDispatchReceipt } catch { $failed=$true }
  if(-not $failed){throw 'STALE_ACTION_WAS_ACCEPTED'}
  $record['action_id']=$PrepareAction
  $record['message_sha256']='0'*64
  [IO.File]::WriteAllText($PrepareTargetPath, ($record | ConvertTo-Json -Compress), [Text.Encoding]::UTF8)
  $failed=$false
  try { Assert-PrivateDispatchReceipt } catch { $failed=$true }
  if(-not $failed){throw 'WRONG_MESSAGE_DIGEST_ACCEPTED'}
  $record['message_sha256']=$digest
  $record['route_receipt']='different-route'
  [IO.File]::WriteAllText($PrepareTargetPath, ($record | ConvertTo-Json -Compress), [Text.Encoding]::UTF8)
  $failed=$false
  try { Assert-PrivateDispatchReceipt } catch { $failed=$true }
  if(-not $failed){throw 'CHANGED_ACCOUNT_ROUTE_ACCEPTED'}
  $record['route_receipt']=$RouteReceipt
  $record['source_response']='wrong-response'
  [IO.File]::WriteAllText($PrepareTargetPath, ($record | ConvertTo-Json -Compress), [Text.Encoding]::UTF8)
  $failed=$false
  try { Assert-PrivateDispatchReceipt } catch { $failed=$true }
  if(-not $failed){throw 'CHANGED_SUCCESSOR_SOURCE_ANCHOR_ACCEPTED'}
  $record['source_response']=$PendingResponseId
  $record['document_id']='42.333'
  [IO.File]::WriteAllText($PrepareTargetPath, ($record | ConvertTo-Json -Compress), [Text.Encoding]::UTF8)
  $failed=$false
  try { Assert-PrivateDispatchReceipt } catch { $failed=$true }
  if(-not $failed){throw 'CHANGED_DOCUMENT_ACCEPTED'}
  $BootstrapIntentPath = Join-Path $env:TEMP 'a2-ps-bootstrap-intent-test.json'
  $PrepareAction = ''
  $BootstrapRunId='a2-test-run-1'
  $BootstrapActionId='b'*32
  $record = [ordered]@{ action_id=$BootstrapActionId; project=$ProjectId; handle=$WindowHandle; document_id=$DocumentId; message=$Message; run_id=$BootstrapRunId; route_receipt=$RouteReceipt; message_sha256=$digest }
  [IO.File]::WriteAllText($BootstrapIntentPath, ($record | ConvertTo-Json -Compress), [Text.Encoding]::UTF8)
  Assert-PrivateDispatchReceipt
  $record['route_receipt']='wrong-bootstrap-route'
  [IO.File]::WriteAllText($BootstrapIntentPath, ($record | ConvertTo-Json -Compress), [Text.Encoding]::UTF8)
  $failed=$false
  try { Assert-PrivateDispatchReceipt } catch { $failed=$true }
  if(-not $failed){throw 'CHANGED_BOOTSTRAP_ROUTE_ACCEPTED'}
  $record['route_receipt']=$RouteReceipt
  $record['action_id']='c'*32
  [IO.File]::WriteAllText($BootstrapIntentPath, ($record | ConvertTo-Json -Compress), [Text.Encoding]::UTF8)
  $failed=$false
  try { Assert-PrivateDispatchReceipt } catch { $failed=$true }
  if(-not $failed){throw 'CHANGED_VALID_BOOTSTRAP_ACTION_ID_ACCEPTED'}
  $record.Remove('action_id')
  [IO.File]::WriteAllText($BootstrapIntentPath, ($record | ConvertTo-Json -Compress), [Text.Encoding]::UTF8)
  $failed=$false
  try { Assert-PrivateDispatchReceipt } catch { $failed=$true }
  if(-not $failed){throw 'BOOTSTRAP_WITHOUT_ACTION_ID_ACCEPTED'}
} finally {
  Remove-Item -LiteralPath $PrepareTargetPath -Force -ErrorAction SilentlyContinue
  if($BootstrapIntentPath){ Remove-Item -LiteralPath $BootstrapIntentPath -Force -ErrorAction SilentlyContinue }
}

foreach ($name in @('Get-ConversationRole', 'Get-ConversationTurns', 'Find-PostedMessage',
                   'Read-ConversationContent', 'Read-CurrentTurn')) {
  $definition = $ast.Find({
    param($node)
    $node -is [System.Management.Automation.Language.FunctionDefinitionAst] -and $node.Name -eq $name
  }, $true)
  if(-not $definition){throw "Missing native function $name"}
  . ([scriptblock]::Create($definition.Extent.Text))
}
Add-Type -AssemblyName UIAutomationTypes
function Desc($element){return $element.Children}
function Get-AccessibilityParent($element){return $element.Parent}
function Test-AssistantProse($element){return $element.Prose}
function Text-Leaf($name,[bool]$prose=$false){
  return @{Current=@{Name=$name; ControlType=[System.Windows.Automation.ControlType]::Text
                     LocalizedControlType='text'; ClassName=''}
           Prose=$prose; Parent=$null}
}
function Turn-Article([int]$index,[string]$label,[object[]]$body){
  $article=[pscustomobject]@{
    Current=@{Name=''; ControlType=[System.Windows.Automation.ControlType]::Group
              LocalizedControlType='article'; ClassName=''}
    Id=$index; Children=@(); Parent=$null
  }
  $article | Add-Member ScriptMethod GetRuntimeId { return @(42,$this.Id) }
  $heading=Text-Leaf $label
  $heading.Current.LocalizedControlType='heading'
  $heading.Current.ClassName='sr-only'
  $heading.Parent=$article
  $labelLeaf=Text-Leaf $label
  $labelLeaf.Parent=$heading
  foreach($leaf in $body){$leaf.Parent=$article}
  $article.Children=@($heading,$labelLeaf)+$body
  return $article
}
function Transcript-Window([object[]]$articles){
  $children=@(foreach($article in $articles){$article;$article.Children})
  return @{Children=$children+@(Text-Leaf 'Ask ChatGPT'; Text-Leaf 'Chrome text outside the articles')}
}
$initial=Turn-Article 1 'You said:' @((Text-Leaf $Message))
$assistant=Turn-Article 2 'ChatGPT said:' @((Text-Leaf 'CHAT_STATUS: NEED_MORE_TIME' $true))
$assistantTurn=Get-ConversationRole $assistant.Children[0]
$anchor=(Read-ConversationContent $assistantTurn 1).response_id
$history=Transcript-Window @($initial,$assistant)
if(Find-PostedMessage $history $Message $anchor){throw 'Older identical post acknowledged'}
$exact=Transcript-Window @($initial,$assistant,(Turn-Article 3 'You said:' @((Text-Leaf $Message))))
$longer=Transcript-Window @($initial,$assistant,(Turn-Article 3 'You said:' @(
  Text-Leaf 'Additional text'
  Text-Leaf $Message
)))
if(-not (Find-PostedMessage $exact $Message $anchor)){throw 'Exact anchored body rejected'}
if(-not (Find-PostedMessage $exact $Message)){throw 'Exact successor body rejected'}
if(Find-PostedMessage $longer $Message $anchor){throw 'Longer anchored body acknowledged'}
if(Find-PostedMessage $longer $Message){throw 'Longer successor body acknowledged'}
$labels=@('Ask ChatGPT','Latest response','You said:','ChatGPT said:',
          'ChatGPT can make mistakes. Check important info.')
foreach($label in $labels){
  $body=@(Text-Leaf $Message; Text-Leaf $label; Text-Leaf 'Discuss the sample only')
  $longer=Transcript-Window @($initial,$assistant,(Turn-Article 3 'You said:' $body))
  if(Find-PostedMessage $longer $Message $anchor){throw "Anchored message truncated at $label"}
  if(Find-PostedMessage $longer $Message){throw "Successor message truncated at $label"}
  $tail=@(Text-Leaf 'CHAT_STATUS: NEED_MORE_TIME' $true; Text-Leaf $label; Text-Leaf 'Further prose')
  $window=Transcript-Window @($initial,(Turn-Article 2 'ChatGPT said:' $tail))
  if((Read-CurrentTurn @{window=$window; chat=$ChatId}).ready){throw "Assistant message truncated at $label"}
}
$twoUserTurns=Transcript-Window @($initial,$assistant,
  (Turn-Article 3 'You said:' @((Text-Leaf 'Different message'))),
  (Turn-Article 4 'You said:' @((Text-Leaf $Message))))
if(Find-PostedMessage $twoUserTurns $Message $anchor){throw 'Non-adjacent user turn acknowledged'}
if(Find-PostedMessage @{Children=@(Text-Leaf 'You said:'; Text-Leaf $Message)} $Message){
  throw 'An unverified conversation structure acknowledged a post'
}
foreach($status in @('CHAT_STATUS: NEED_MORE_TIME','CHAT_STATUS: TASK_COMPLETE','ERROR')){
  $window=Transcript-Window @($initial,(Turn-Article 2 'ChatGPT said:' @((Text-Leaf $status))))
  if((Read-CurrentTurn @{window=$window; chat=$ChatId}).ready){throw 'Non-prose status became actionable'}
  $window=Transcript-Window @($initial,(Turn-Article 2 'ChatGPT said:' @((Text-Leaf $status $true))))
  if(-not (Read-CurrentTurn @{window=$window; chat=$ChatId}).ready){throw 'Verified prose status was rejected'}
}
Write-Output 'PASS: Windows PowerShell action, structurally bounded full turns, prose status and owner receipt checks.'
