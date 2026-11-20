param([Parameter(Mandatory=$true)][string]$Candidate)
$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest
$tokens = $null
$errors = $null
$ast = [Management.Automation.Language.Parser]::ParseFile(
    (Join-Path $Candidate 'integration\uia_adapter.ps1'), [ref]$tokens, [ref]$errors)
if ($errors.Count) { throw 'Failed to parse pinned adapter' }
foreach ($name in @('Assert-PrivateDispatchReceipt','Test-FreshWorkerCompletion',
                    'Check-Project','Chat-FromUrl','Find-TargetWindows','Get-TargetWindow',
                    'Find-PostedMessage')) {
    $definition = $ast.Find({
        param($node)
        $node -is [Management.Automation.Language.FunctionDefinitionAst] -and $node.Name -eq $name
    }, $true)
    if (-not $definition) { throw "Missing function $name" }
    . ([scriptblock]::Create($definition.Extent.Text))
}
$ProjectId = 'g-p-abc123'
$Mode = 'Send'
$Kind = 'LAUNCH_SUCCESSOR'
$PrepareAction = ''
$BootstrapRunId = '000000000000000000000001'
$RouteReceipt = 'a' * 64
$Message = 'Synthetic initial message.'
$WindowHandle = [long]55
$hasher = [Security.Cryptography.SHA256]::Create()
try {
    $digest = [BitConverter]::ToString(
        $hasher.ComputeHash([Text.Encoding]::UTF8.GetBytes($Message))).Replace('-','').ToLowerInvariant()
} finally { $hasher.Dispose() }
$BootstrapIntentPath = [IO.Path]::GetTempFileName()
$intent = [ordered]@{
    action_id = 'b' * 32; project = $ProjectId; handle = $WindowHandle
    message = $Message; run_id = $BootstrapRunId; route_receipt = $RouteReceipt
    message_sha256 = $digest
}
try {
    [IO.File]::WriteAllText($BootstrapIntentPath, ($intent | ConvertTo-Json -Compress))
    Assert-PrivateDispatchReceipt
    $intent.action_id = 'c' * 32
    [IO.File]::WriteAllText($BootstrapIntentPath, ($intent | ConvertTo-Json -Compress))
    $substituteAccepted = $true
    try { Assert-PrivateDispatchReceipt } catch { $substituteAccepted = $false }
} finally { Remove-Item -LiteralPath $BootstrapIntentPath }

# Supply a synthetic window descriptor. No live UIA tree is read.
$chat = '00000000-0000-0000-0000-000000000001'
$chatUrl = "https://chatgpt.com/g/$ProjectId/c/$chat"
$env:CHAT_SUCCESSION_CHROME_PROFILE_PATH = 'C:\Mock Chrome\Expected'
$mockWindow = @{
    Current = @{ NativeWindowHandle = 55 }
    Profile = 'C:\Mock Chrome\Other'
    Address = $chatUrl
}
function Get-ChromeWindows { return $mockWindow }
function Get-Address($window) { return $window.Address }
$wrongProfileSelected = $false
try {
    $selected = Get-TargetWindow $chat $WindowHandle
    $wrongProfileSelected = $selected.window.Profile -ne $env:CHAT_SUCCESSION_CHROME_PROFILE_PATH
} catch {}

# Original is an old spinning rendering of the same response already consumed
# before this observer reattached. The fixture labels that response explicitly.
$consumed = 'uia-turn-1-aaaaaaaaaaaaaaaaaaaa'
$old = @{response_id=$consumed; ready=$false; stop_control=$true; user_after_assistant=$false
         assistant_turn_count=1; user_turn_count=1; latest_user_digest='same-user'}
$fresh = $old.Clone()
$fresh.ready = $true
$fresh.stop_control = $false
$consumedEligible = Test-FreshWorkerCompletion $old $fresh
$differentUser = $fresh.Clone()
$differentUser.latest_user_digest = 'other-user'

# Read-back controls for exact same-chat anchoring.
Add-Type -AssemblyName UIAutomationTypes
function Desc($window) { return $window }
function Text-Element($name, $id='') {
    return @{Current=@{Name=$name; ControlType=[System.Windows.Automation.ControlType]::Text}
             response_id=$id}
}
function Read-AssistantContent($elements, $index, $ordinal) {
    return @{response_id=$elements[$index].response_id}
}
$anchor = 'uia-turn-2-bbbbbbbbbbbbbbbbbbbb'
$continuation = 'Okay, continue working.'
$before = @(Text-Element 'ChatGPT said:' $consumed
            Text-Element 'You said:'
            Text-Element $continuation
            Text-Element 'ChatGPT said:' $anchor)
$after = $before + @(Text-Element 'You said:'; Text-Element $continuation)
$provisional = "https://chatgpt.com/g/$ProjectId/c/local-chatgpt"

[ordered]@{
    S09_original_bootstrap_receipt_accepted = $true
    S09_substituted_valid_bootstrap_action_id_accepted = $substituteAccepted
    R02_V05_synthetic_wrong_profile_window_selected = $wrongProfileSelected
    S06_provisional_suffix_matches_project = (Check-Project $provisional)
    S06_provisional_suffix_treated_as_chat_id = (Chat-FromUrl $provisional)
    V04_already_consumed_same_reply_eligible_for_reload = $consumedEligible
    V04_changed_user_eligible_for_reload = (Test-FreshWorkerCompletion $old $differentUser)
    S05_older_identical_prompt_matches = (Find-PostedMessage $before $continuation $anchor)
    S05_prompt_after_exact_anchor_matches = (Find-PostedMessage $after $continuation $anchor)
} | ConvertTo-Json
