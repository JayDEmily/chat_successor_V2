# Task 2 Windows UIA launcher. Without -ExecuteSend this is STATIC preflight only.
# Do not set -ExecuteSend before a separately authorised three-chat trial.
[CmdletBinding()]
param(
    [Parameter(Mandatory=$true)][ValidatePattern('^[a-z0-9][a-z0-9-]{0,63}$')][string]$RunId,
    [Parameter(Mandatory=$true)][ValidateSet(2,3)][int]$NextStep,
    [Parameter(Mandatory=$true)][ValidatePattern('^[0-9a-f]{40}$')][string]$AssignmentSha,
    [Parameter(Mandatory=$true)][string]$ProjectUrl,
    [Parameter(Mandatory=$true)][string]$ProjectName,
    [Parameter(Mandatory=$true)][string]$ChromeProfileDirectory,
    [string]$JournalPath = '',
    [string]$RepoUnixPath = '/home/jds/chat_successor',
    [string]$PythonExe = 'C:\Program Files\Python313\python.exe',
    [string]$ChromeExe = 'C:\Program Files\Google\Chrome\Application\chrome.exe',
    [switch]$ExecuteSend
)
Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

function Assert-StaticConfig {
    param([string]$UriText, [string]$Project, [string]$Profile)
    $uri = $null
    if (-not [Uri]::TryCreate($UriText, [UriKind]::Absolute, [ref]$uri)) {
        throw 'Project URL is not an absolute URI'
    }
    if ($uri.Scheme -cne 'https' -or $uri.Host -cne 'chatgpt.com' -or
        $uri.AbsolutePath -cnotmatch '^/g/g-p-[A-Za-z0-9-]+/project/?$' -or
        $uri.Query -ne '' -or $uri.Fragment -ne '') {
        throw 'Project URL must identify one HTTPS ChatGPT Project, with no query or fragment'
    }
    if ($Project -notmatch '^[\p{L}\p{N}_ -]{1,80}$') {
        throw 'Project name must be one explicit safe accessibility name'
    }
    if ($Profile -notmatch '^(Default|Profile|Profile [0-9]+)$') {
        throw 'Chrome profile must be explicitly named Default or Profile N'
    }
    if ($RepoUnixPath -cne '/home/jds/chat_successor') {
        throw 'Unexpected Ubuntu Git working directory'
    }
    if (-not (Test-Path -LiteralPath $PythonExe -PathType Leaf)) {
        throw 'Windows Python path not found'
    }
    if (-not (Test-Path -LiteralPath $ChromeExe -PathType Leaf)) {
        throw 'Chrome executable not found'
    }
    $profilePath = Join-Path (Join-Path $env:LOCALAPPDATA 'Google\Chrome\User Data') $Profile
    if (-not (Test-Path -LiteralPath $profilePath -PathType Container)) {
        throw 'Configured Chrome profile directory not found'
    }
    return $uri
}
function New-PinnedPrompt {
    param([string]$Run, [int]$Step, [string]$Sha)
    $role = if ($Step -eq 2) { 'reviewer' } else { 'auditor' }
    $number = '{0:D3}' -f $Step
    $message = 'Chat Succession. Repository JayDEmily/chat_successor. ' +
        "Run $Run. Step $Step. Role $role. " +
        'Read AGENTS.md README.md and linked design and plan. ' +
        "Read runs/$Run/run.json and runs/$Run/steps/$number/assignment.json " +
        "at immutable commit $Sha. " +
        'Complete only assigned work and verified Git handover. ' +
        'Do not return to any earlier chat. Never create a fourth chat.'
    # Explicit safe subset of SendKeys (no braces, +, ^, %, ~ or brackets).
    if ($message -cnotmatch '^[A-Za-z0-9 .,/_:-]+$') {
        throw 'Prompt includes untested SendKeys metacharacters'
    }
    return $message
}
$project = Assert-StaticConfig $ProjectUrl $ProjectName $ChromeProfileDirectory
$prompt = New-PinnedPrompt $RunId $NextStep $AssignmentSha
$editorName = "New chat in $ProjectName"
if (-not $ExecuteSend) {
    Write-Output 'STATIC_PREFLIGHT_PASS: parameters and SendKeys-safe pinned prompt'
    Write-Output 'NO_SEND: no Git, browser, journal or ChatGPT mutation performed'
    return
}
if ([string]::IsNullOrWhiteSpace($JournalPath) -or
    -not (Test-Path -LiteralPath $JournalPath -PathType Leaf)) {
    throw 'Journal missing; do not initialise a new database during launch'
}
# Fetch and inspect exactly the current run branch before reserving a launch.
$fetchRef = "refs/heads/trial/$RunId" + ":refs/remotes/origin/trial/$RunId"
& wsl.exe -d Ubuntu --exec /usr/bin/git -C $RepoUnixPath fetch origin $fetchRef
if ($LASTEXITCODE -ne 0) { throw 'Git fetch failed before any browser effect' }
$validatorUnix = "$RepoUnixPath/tools/validate_packet.py"
$validateOutput = & wsl.exe -d Ubuntu --exec /usr/bin/python3 $validatorUnix --repo-dir $RepoUnixPath --run-id $RunId --step $NextStep --assignment-sha $AssignmentSha
if ($LASTEXITCODE -ne 0) { throw 'Pinned packet validation failed before any browser effect' }
$validation = $validateOutput | ConvertFrom-Json
if ($validation.ok -ne $true -or $validation.assignment_sha -cne $AssignmentSha) {
    throw 'Pinned assignment mismatch before any browser effect'
}
$journalScript = Join-Path $PSScriptRoot 'journal.py'
if (-not (Test-Path -LiteralPath $journalScript -PathType Leaf)) {
    throw 'Local journal script missing'
}
$reserveOutput = & $PythonExe $journalScript reserve --db $JournalPath --run $RunId --step $NextStep --sha $AssignmentSha
if ($LASTEXITCODE -ne 0) { throw "Journal reservation HELD: $reserveOutput" }
$reservation = $reserveOutput | ConvertFrom-Json
if ($reservation.state -cne 'reserved') { throw 'No first-use reservation was granted' }

function Set-LaunchOutcome {
    param([string]$NewState, [hashtable]$Receipt)
    $receiptFile = [IO.Path]::GetTempFileName()
    try {
        $json = ConvertTo-Json -InputObject $Receipt -Compress -Depth 5
        [IO.File]::WriteAllText($receiptFile, $json,
            (New-Object System.Text.UTF8Encoding($false)))
        $output = & $PythonExe $journalScript mark --db $JournalPath --run $RunId --step $NextStep --sha $AssignmentSha --state $NewState --receipt-file $receiptFile
        if ($LASTEXITCODE -ne 0) { throw "Journal mark failed: $output" }
    }
    finally {
        Remove-Item -LiteralPath $receiptFile -Force -ErrorAction SilentlyContinue
    }
}
$sendAttempted = $false
$receipt = @{
    run_id = $RunId; step = $NextStep; assignment_sha = $AssignmentSha
    project_name = $ProjectName; distinct_window = $false
    draft_readback = $false; send_attempted = $false
    message_observed = $false; conversation_url = $null
}
try {
    Add-Type -AssemblyName UIAutomationClient
    Add-Type -AssemblyName UIAutomationTypes
    Add-Type -AssemblyName System.Windows.Forms
    Add-Type -TypeDefinition @'
using System;
using System.Runtime.InteropServices;
public static class ChatSuccessionFocus {
    [DllImport("user32.dll")] public static extern bool SetForegroundWindow(IntPtr hwnd);
    [DllImport("user32.dll")] public static extern IntPtr GetForegroundWindow();
}
'@
    function Get-ChromeWindows {
        $root = [System.Windows.Automation.AutomationElement]::RootElement
        $items = $root.FindAll(
            [System.Windows.Automation.TreeScope]::Children,
            [System.Windows.Automation.Condition]::TrueCondition)
        $windows = @()
        foreach ($item in $items) {
            try {
                if ($item.Current.NativeWindowHandle -ne 0 -and
                    $item.Current.Name -like '*Google Chrome*') {
                    $windows += $item
                }
            } catch { }
        }
        return $windows
    }
    function Find-ProjectEditors {
        param($Window)
        $items = $Window.FindAll(
            [System.Windows.Automation.TreeScope]::Descendants,
            [System.Windows.Automation.Condition]::TrueCondition)
        $editors = @()
        foreach ($item in $items) {
            try {
                if ($item.Current.ControlType -eq [System.Windows.Automation.ControlType]::Edit -and
                    $item.Current.Name -ceq $editorName -and
                    $item.Current.IsEnabled -and -not $item.Current.IsOffscreen) {
                    $editors += $item
                }
            } catch { }
        }
        return $editors
    }
    function Get-ConversationUrl {
        param($Window)
        $items = $Window.FindAll(
            [System.Windows.Automation.TreeScope]::Descendants,
            [System.Windows.Automation.Condition]::TrueCondition)
        foreach ($item in $items) {
            try {
                if ($item.Current.ControlType -eq [System.Windows.Automation.ControlType]::Edit -and
                    $item.Current.Name -eq 'Address and search bar') {
                    $value = $item.GetCurrentPattern(
                        [System.Windows.Automation.ValuePattern]::Pattern).Current.Value
                    if ($value -match '^chatgpt.com/') { return "https://$value" }
                    return $value
                }
            } catch { }
        }
        return $null
    }

    $existingHandles = @((Get-ChromeWindows) | ForEach-Object {
        $_.Current.NativeWindowHandle
    })
    # Open a brand-new window, without touching an existing authenticated draft.
    Start-Process -FilePath $ChromeExe -ArgumentList @(
        '--new-window', ('--profile-directory="' + $ChromeProfileDirectory + '"'), $ProjectUrl
    )
    $target = $null
    $editor = $null
    for ($i = 0; $i -lt 50; $i++) {
        Start-Sleep -Milliseconds 400
        $newWindows = @((Get-ChromeWindows) | Where-Object {
            ($existingHandles -notcontains $_.Current.NativeWindowHandle) -and
            ($_.Current.Name -like "*$ProjectName*Google Chrome*")
        })
        if ($newWindows.Count -gt 1) { throw 'Multiple new matching Project windows' }
        if ($newWindows.Count -eq 1) {
            $available = @(Find-ProjectEditors -Window $newWindows[0])
            if ($available.Count -gt 1) { throw 'Multiple enabled Project editors' }
            if ($available.Count -eq 1) {
                $target = $newWindows[0]
                $editor = $available[0]
                break
            }
        }
    }
    if ($null -eq $target -or $null -eq $editor) {
        throw 'Fresh target Project composer not uniquely identified'
    }
    $receipt.distinct_window = $true
    $initial = $editor.GetCurrentPattern(
        [System.Windows.Automation.ValuePattern]::Pattern).Current.Value
    if ($initial -cne '') { throw 'Existing draft detected; preserve it' }
    $hwnd = [IntPtr]$target.Current.NativeWindowHandle
    if (-not [ChatSuccessionFocus]::SetForegroundWindow($hwnd)) {
        throw 'Unable to focus new Project window'
    }
    $editor.SetFocus()
    if ([ChatSuccessionFocus]::GetForegroundWindow() -ne $hwnd) {
        throw 'Foreground window mismatch before typing'
    }
    [System.Windows.Forms.SendKeys]::SendWait($prompt)
    $afterTyping = $target.FindAll(
        [System.Windows.Automation.TreeScope]::Descendants,
        [System.Windows.Automation.Condition]::TrueCondition)
    $exactDrafts = @()
    $sendButtons = @()
    foreach ($item in $afterTyping) {
        try {
            if ($item.Current.ControlType -eq [System.Windows.Automation.ControlType]::Edit -and
                $item.Current.IsEnabled -and -not $item.Current.IsOffscreen) {
                $value = $item.GetCurrentPattern(
                    [System.Windows.Automation.ValuePattern]::Pattern).Current.Value
                if ($value -ceq $prompt) { $exactDrafts += $item }
            }
            if ($item.Current.ControlType -eq [System.Windows.Automation.ControlType]::Button -and
                $item.Current.Name -ceq 'Send' -and $item.Current.IsEnabled -and
                -not $item.Current.IsOffscreen) {
                $sendButtons += $item
            }
        } catch { }
    }
    if ($exactDrafts.Count -ne 1) { throw 'Composer did not read back the exact prompt' }
    $receipt.draft_readback = $true
    if ($sendButtons.Count -ne 1) { throw 'Enabled Send button not unique' }
    if ([ChatSuccessionFocus]::GetForegroundWindow() -ne $hwnd) {
        throw 'Foreground changed before Send'
    }

    $sendAttempted = $true
    $receipt.send_attempted = $true
    [System.Windows.Forms.SendKeys]::SendWait('{ENTER}')
    $posted = $false
    $conversationUrl = $null
    $projectPrefix = $project.AbsolutePath.TrimEnd('/') -replace '/project$', ''
    for ($i = 0; $i -lt 50; $i++) {
        Start-Sleep -Milliseconds 400
        $conversationUrl = Get-ConversationUrl -Window $target
        $items = $target.FindAll(
            [System.Windows.Automation.TreeScope]::Descendants,
            [System.Windows.Automation.Condition]::TrueCondition)
        $messageSeen = $false
        foreach ($item in $items) {
            try {
                if ($item.Current.ControlType -ne [System.Windows.Automation.ControlType]::Edit) {
                    $name = $item.Current.Name
                    if ($name -ceq $prompt -or $name -ceq "You said: $prompt") {
                        $messageSeen = $true
                        break
                    }
                }
            } catch { }
        }
        if ($messageSeen -and $null -ne $conversationUrl -and
            $conversationUrl.StartsWith("https://chatgpt.com$projectPrefix/") -and
            $conversationUrl -cne $ProjectUrl) {
            $posted = $true
            break
        }
    }
    if (-not $posted) {
        throw 'Posted message and distinct saved Project conversation not both observed'
    }
    $receipt.message_observed = $true
    $receipt.conversation_url = $conversationUrl
    Set-LaunchOutcome -NewState 'posted' -Receipt $receipt
    Write-Output 'POSTED_OBSERVED: private conversation receipt persisted in journal'
}
catch {
    $receipt.error = $_.Exception.Message
    $state = if ($sendAttempted) { 'effect_unknown' } else { 'blocked' }
    try {
        Set-LaunchOutcome -NewState $state -Receipt $receipt
    } catch {
        Write-Error ('Journal mark failed; reservation remains held: ' +
            $_.Exception.Message)
    }
    throw "Launch $state. No retry is permitted. $($receipt.error)"
}
