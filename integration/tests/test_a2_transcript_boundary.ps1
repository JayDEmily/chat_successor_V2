# Regression assertions, not a reproducer that passes when unsafe behavior occurs.
# Windows PowerShell required. Function-only synthetic UIA; never runs an adapter mode.
param([string]$RepoRoot = (Join-Path $PSScriptRoot '..\..'))
$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest
Add-Type -AssemblyName UIAutomationTypes
$RepoRoot = (Resolve-Path -LiteralPath $RepoRoot).Path

function Read-FunctionAst([string]$path) {
    $tokens=$null; $errors=$null
    $tree=[Management.Automation.Language.Parser]::ParseFile($path,[ref]$tokens,[ref]$errors)
    if($errors.Count){throw ('Parse failure: '+$path+' '+($errors | Out-String))}
    return $tree
}
$production=Read-FunctionAst (Join-Path $RepoRoot 'integration\uia_adapter.ps1')
$fixture=Read-FunctionAst (Join-Path $RepoRoot 'integration\tests\test_a2_l03_ps_action_gate.ps1')
# Read definitions, NOT the fixture's top-level test runner or the adapter's Send blocks.
foreach($entry in @(
    @{tree=$production; names=@('Test-TranscriptRegion','Get-ConversationRole',
      'Get-VirtualizedConversationTurns','Get-ConversationTurns','Read-ConversationContent',
      'Read-CurrentTurn','Find-PostedMessage')},
    @{tree=$fixture; names=@('Desc','Get-AccessibilityParent','Test-AssistantProse',
      'Text-Leaf','Turn-Article','Transcript-Window')}
)) {
    foreach($name in $entry.names) {
        $definitions=@($entry.tree.FindAll({
            param($node)
            $node -is [Management.Automation.Language.FunctionDefinitionAst] -and $node.Name -ceq $name
        },$true))
        if($definitions.Count -ne 1){throw ('Missing/duplicate function: '+$name)}
        . ([scriptblock]::Create($definitions[0].Extent.Text))
    }
}
function Get-AccessibilityChildren($node){return $node.Children}
$ProjectId='g-p-abc123'
$ChatId='00000000-0000-0000-0000-000000000001'
$expected='Okay, continue working.'
$script:failures=@()
$script:checks=0

function Check([string]$name,[bool]$condition) {
    $script:checks++
    if($condition){Write-Output ('PASS '+$name)}
    else {
        $script:failures+=@($name)
        Write-Output ('FAIL '+$name)
    }
}
function New-LeanHistory([bool]$posted=$false) {
    $first=Turn-Article 1 'You said:' @((Text-Leaf $expected))
    $reply=Turn-Article 2 'ChatGPT said:' @((Text-Leaf 'CHAT_STATUS: NEED_MORE_TIME' $true))
    $articles=@($first,$reply)
    if($posted){$articles+=@(Turn-Article 3 'You said:' @((Text-Leaf $expected)))}
    return (Transcript-Window $articles)
}
function Add-OpaqueRow($window,[string]$kind,[bool]$changedHeading=$false) {
    $thread=$window.Children[0]
    $rows=@()
    if($changedHeading) {
        $heading=Text-Leaf 'ChatGPT said:'
        $heading.Current.LocalizedControlType='heading'
        $heading.Current.ClassName='visually-hidden changed-accessibility'
        $heading.Parent=$thread
        $rows+=@($heading)
    }
    # No Text descendant is needed: an opaque control may expose its own Name.
    # A type-filter over only group/heading/text must not certify this old history.
    $control=switch($kind){
        'pane' {[System.Windows.Automation.ControlType]::Pane}
        'list' {[System.Windows.Automation.ControlType]::List}
        'custom' {[System.Windows.Automation.ControlType]::Custom}
        default {[System.Windows.Automation.ControlType]::Group}
    }
    $row=[pscustomobject]@{
        Current=@{Name='Newer unclassified content'; LocalizedControlType=$kind
                  ClassName='opaque-row';ControlType=$control}
        Parent=$thread;Children=@()
    }
    $rows+=@($row)
    $thread.Children=@($thread.Children)+$rows
    $window.Children=@($window.Children)+$rows
}
function No-ActionableTurn($window) {
    try {
        $turn=Read-CurrentTurn @{window=$window;chat=$ChatId} -IncludeUserAnchor
        return (-not $turn.ready -and
                (-not $turn.ContainsKey('response_id') -or -not $turn['response_id']) -and
                (-not $turn.ContainsKey('latest_user_digest') -or -not $turn['latest_user_digest']))
    } catch {
        # A random missing fixture method is NOT a passing safety hold.
        if($_.Exception.Message -like 'Article transcript has an unverified*'){return $true}
        throw
    }
}

$baseline=New-LeanHistory
$before=Read-CurrentTurn @{window=$baseline;chat=$ChatId} -IncludeUserAnchor
Check 'positive_final_prose' ([bool]$before.ready)
Check 'positive_anchor_present' ([bool]$before['response_id'] -and [bool]$before['latest_user_digest'])
Check 'older_identical_user_not_acknowledged' (-not (Find-PostedMessage $baseline $expected $before.response_id))
$posted=New-LeanHistory $true
Check 'positive_exact_anchored_post' ([bool](Find-PostedMessage $posted $expected $before.response_id))
Check 'positive_exact_unanchored_post' ([bool](Find-PostedMessage $posted $expected))

foreach($shape in @(
    @{label='F1a_opaque_group';kind='group';heading=$false},
    @{label='F1b_changed_heading';kind='group';heading=$true},
    @{label='unknown_pane';kind='pane';heading=$false},
    @{label='unknown_custom';kind='custom';heading=$false},
    @{label='unknown_list';kind='list';heading=$false}
)) {
    $window=New-LeanHistory
    Add-OpaqueRow $window $shape.kind $shape.heading
    Check ($shape.label+'_no_old_status_or_anchor') (No-ActionableTurn $window)
    $window=New-LeanHistory $true
    Add-OpaqueRow $window $shape.kind $shape.heading
    Check ($shape.label+'_no_anchored_ack') (-not (Find-PostedMessage $window $expected $before.response_id))
    Check ($shape.label+'_no_unanchored_ack') (-not (Find-PostedMessage $window $expected))
}

# Body words are not delimiters. These controls must continue to pass after a repair.
foreach($literal in @('You said:','ChatGPT said:','Ask ChatGPT')) {
    $first=Turn-Article 1 'You said:' @((Text-Leaf 'Initial disposable instruction'))
    $reply=Turn-Article 2 'ChatGPT said:' @((Text-Leaf 'CHAT_STATUS: NEED_MORE_TIME' $true))
    $long=Turn-Article 3 'You said:' @((Text-Leaf $expected),(Text-Leaf $literal),(Text-Leaf 'Extra content'))
    $window=Transcript-Window @($first,$reply,$long)
    Check ('literal_'+$literal+'_full_body_not_ack') (-not (Find-PostedMessage $window $expected $before.response_id))
    $reply=Turn-Article 2 'ChatGPT said:' @(
        (Text-Leaf 'CHAT_STATUS: NEED_MORE_TIME' $true),(Text-Leaf $literal),(Text-Leaf 'Extra content'))
    $turn=Read-CurrentTurn @{window=(Transcript-Window @($first,$reply));chat=$ChatId}
    Check ('literal_'+$literal+'_nonfinal_status_not_ready') (-not $turn.ready)
}
$stream=New-LeanHistory
$stream.Children+=@{Current=@{Name='Stop';ControlType=[System.Windows.Automation.ControlType]::Button
                               IsEnabled=$true;LocalizedControlType='button';ClassName=''}}
Check 'streaming_not_ready' (-not (Read-CurrentTurn @{window=$stream;chat=$ChatId}).ready)

# The ancestry of verified articles establishes the role of a layout pane.
$wrapped=New-LeanHistory $true
$thread=$wrapped.Children[0]
$layout=[pscustomobject]@{
    Current=@{Name=''; LocalizedControlType='pane'; ClassName=''
              ControlType=[System.Windows.Automation.ControlType]::Pane}
    Parent=$thread; Children=$thread.Children
}
foreach($row in $thread.Children){
    if($row.Current.LocalizedControlType -ceq 'article'){$row.Parent=$layout}
}
$thread.Children=@($layout)+$thread.Children
$wrapped.Children+=@($layout)
Check 'positive_article_layout_pane' ([bool](Find-PostedMessage $wrapped $expected $before.response_id))
Write-Output ('Checks='+$script:checks+' Failures='+$script:failures.Count)
if($script:failures.Count){throw ('Transcript regressions failed: '+($script:failures -join ', '))}
