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
  Write-Output 'PASS: Windows PowerShell action checks, including changed document and substituted bootstrap ID.'
} finally {
  Remove-Item -LiteralPath $PrepareTargetPath -Force -ErrorAction SilentlyContinue
  if($BootstrapIntentPath){ Remove-Item -LiteralPath $BootstrapIntentPath -Force -ErrorAction SilentlyContinue }
}
