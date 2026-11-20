param([Parameter(Mandatory=$true)][string] $Candidate)
$ErrorActionPreference='Stop'
Set-StrictMode -Version Latest
Add-Type -AssemblyName UIAutomationTypes
$tokens=$null
$errors=$null
$ast=[Management.Automation.Language.Parser]::ParseFile(
    (Join-Path $Candidate 'integration\uia_adapter.ps1'), [ref]$tokens, [ref]$errors)
if($errors.Count){ throw 'Candidate script does not parse' }
foreach($name in @('Find-PostedMessage','Read-AssistantContent','Read-CurrentTurn','Test-FreshWorkerCompletion')){
    $definition=$ast.Find({
        param($node)
        $node -is [Management.Automation.Language.FunctionDefinitionAst] -and $node.Name -eq $name
    },$true)
    . ([scriptblock]::Create($definition.Extent.Text))
}
function Desc($nodes){ return $nodes }
function Test-AssistantProse($node){ return [bool]$node.IsProse }
function Text-Node($text,[bool]$prose=$true){
    return @{Current=@{Name=$text;ControlType=[System.Windows.Automation.ControlType]::Text}
             IsProse=$prose}
}
$ProjectId='g-p-abc123'
$worker='00000000-0000-0000-0000-000000000001'
$continuation='Okay, continue working.'
$anchor=@(
    Text-Node 'You said:'
    Text-Node 'Initial fixture instruction'
    Text-Node 'ChatGPT said:'
    Text-Node 'CHAT_STATUS: NEED_MORE_TIME'
)
$prior=Read-CurrentTurn @{window=$anchor;chat=$worker}
$exact=$anchor + @(
    Text-Node 'You said:'
    Text-Node $continuation
    Text-Node 'ChatGPT said:'
    Text-Node 'Synthetic next reply'
)
$longer=$anchor + @(
    Text-Node 'You said:'
    Text-Node 'Inspect this sample without applying it.'
    Text-Node $continuation
    Text-Node 'ChatGPT said:'
    Text-Node 'Synthetic next reply'
)
$nonProse=@(
    Text-Node 'You said:'
    Text-Node 'Show the status as quoted sample text.'
    Text-Node 'ChatGPT said:'
    Text-Node 'Here is the sample.'
    Text-Node 'CHAT_STATUS: NEED_MORE_TIME' $false
)
$quoted=Read-CurrentTurn @{window=$nonProse;chat=$worker}
$nonProse[-1] = Text-Node 'CHAT_STATUS: TASK_COMPLETE' $false
$quotedComplete=Read-CurrentTurn @{window=$nonProse;chat=$worker}
[ordered]@{
    S05_anchor_verified=$prior.ready
    S05_exact_post_accepted=(Find-PostedMessage $exact $continuation $prior.response_id)
    S05_fragment_from_different_body_accepted=(Find-PostedMessage $longer $continuation $prior.response_id)
    S06_fragment_from_different_body_accepted=(Find-PostedMessage $longer $continuation)
    S01_non_prose_status_marked_ready=$quoted.ready
    S01_non_prose_status_kept_in_response=($quoted.text -match 'CHAT_STATUS: NEED_MORE_TIME$')
    S01_complete_status_ready_with_prose_flag_false=($quotedComplete.ready -and -not $quotedComplete.handoff_locator_verified)
} | ConvertTo-Json
