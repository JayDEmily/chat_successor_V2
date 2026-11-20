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
$PrepareTargetPath = Join-Path $env:TEMP 'a2-ps-target-receipt-test.json'
$BootstrapIntentPath = ''
$ProjectId = 'g-p-TEST'
$Kind = 'CONTINUE_CURRENT'
$ChatId = 'worker-first'
$SourceResponse = 'uia-turn-1-aaa00000000000000000'
$WindowHandle = [long]222
$Message = 'Okay, continue working.'
$Mode = 'Send'
$hash = [Security.Cryptography.SHA256]::Create()
try {
    $digest = [BitConverter]::ToString($hash.ComputeHash([Text.Encoding]::UTF8.GetBytes($Message))).Replace('-','').ToLowerInvariant()
} finally { $hash.Dispose() }
$record = [ordered]@{ action_id=$PrepareAction; project=$ProjectId; kind=$Kind; source=$ChatId; handle=$WindowHandle; message_sha256=$digest; source_response=$SourceResponse }
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
  $BootstrapIntentPath = Join-Path $env:TEMP 'a2-ps-bootstrap-intent-test.json'
  $PrepareAction = ''
  $record = [ordered]@{ action_id=('b'*32); project=$ProjectId; handle=$WindowHandle; message=$Message }
  [IO.File]::WriteAllText($BootstrapIntentPath, ($record | ConvertTo-Json -Compress), [Text.Encoding]::UTF8)
  Assert-PrivateDispatchReceipt
  $record.Remove('action_id')
  [IO.File]::WriteAllText($BootstrapIntentPath, ($record | ConvertTo-Json -Compress), [Text.Encoding]::UTF8)
  $failed=$false
  try { Assert-PrivateDispatchReceipt } catch { $failed=$true }
  if(-not $failed){throw 'BOOTSTRAP_WITHOUT_ACTION_ID_ACCEPTED'}
  Write-Output 'PASS: Windows PowerShell AST parse; 1 positive follow-up action; 2 negative target identities; 1 positive bootstrap; 1 negative bootstrap.'
} finally {
  Remove-Item -LiteralPath $PrepareTargetPath -Force -ErrorAction SilentlyContinue
  if($BootstrapIntentPath){ Remove-Item -LiteralPath $BootstrapIntentPath -Force -ErrorAction SilentlyContinue }
}
