param([Parameter(Mandatory=$true)][string]$Candidate)
$ErrorActionPreference='Stop'
Set-StrictMode -Version Latest
Add-Type -AssemblyName UIAutomationTypes
$tokens=$null
$errors=$null
$ast=[Management.Automation.Language.Parser]::ParseFile((Join-Path $Candidate 'integration\uia_adapter.ps1'),[ref]$tokens,[ref]$errors)
if($errors.Count){throw 'Candidate PowerShell parser failed'}
foreach($name in @('Get-ConversationRole','Get-ConversationTurns','Read-ConversationContent','Find-PostedMessage','Read-CurrentTurn')){
    $fn=$ast.Find({param($node) $node -is [Management.Automation.Language.FunctionDefinitionAst] -and $node.Name -ceq $name},$true)
    if(!$fn){throw "Missing $name"}
    . ([scriptblock]::Create($fn.Extent.Text))
}
function Desc($node) {
    foreach($child in $node.Children){ $child; Desc $child }
}
function Get-AccessibilityParent($node) { return $node.Parent }
function Test-AssistantProse($node) { return $node.IsProse }
function Node($name,$kind='text',$className='',[bool]$prose=$true) {
    $control=if($kind -in @('text','heading')){[System.Windows.Automation.ControlType]::Text}else{[System.Windows.Automation.ControlType]::Group}
    return [pscustomobject]@{Current=@{Name=$name;ControlType=$control;LocalizedControlType=$kind;ClassName=$className}
        Parent=$null;Children=@();IsProse=$prose;RuntimeNumber=0}
}
function Attach($parent,$child){
    $child.Parent=$parent
    $parent.Children+=@($child)
}
function New-Article([int]$serial,[string]$role,[object[]]$body,[bool]$recognized=$true) {
    $article=Node '' 'article'
    $article.RuntimeNumber=$serial
    $article | Add-Member ScriptMethod GetRuntimeId { return @(42,$this.RuntimeNumber) }
    $roleClass=if($recognized){'sr-only'}else{''}
    $heading=Node $role 'heading' $roleClass
    Attach $heading (Node $role)
    Attach $article $heading
    foreach($leaf in $body){Attach $article $leaf}
    return $article
}
function Transcript([object[]]$articles){
    $root=Node 'Latest response' 'region' 'thread-scroll-container'
    foreach($article in $articles){Attach $root $article}
    $window=Node '' 'window'
    Attach $window $root
    Attach $window (Node 'Ask ChatGPT')
    return $window
}
$ProjectId='g-p-abc123'
$chat='00000000-0000-0000-0000-000000000001'
$expected='Okay, continue working.'
$status='CHAT_STATUS: NEED_MORE_TIME'
$initial=New-Article 1 'You said:' @((Node 'Initial fixture instruction'))
$assistant=New-Article 2 'ChatGPT said:' @((Node $status))
$history=Transcript @($initial,$assistant)
$prior=Read-CurrentTurn @{window=$history; chat=$chat}
$exactUser=New-Article 3 'You said:' @((Node $expected))
$exact=Transcript @($initial,$assistant,$exactUser)
$exactAnchored=Find-PostedMessage $exact $expected $prior.response_id
$exactUnanchored=Find-PostedMessage $exact $expected
$labels=@('Ask ChatGPT','Latest response','You said:','ChatGPT said:','ChatGPT can make mistakes. Check important info.')
$cases=@(foreach($label in $labels){
    $differentUser=New-Article 3 'You said:' @((Node $expected),(Node $label),(Node 'Discuss this sample only'))
    $different=Transcript @($initial,$assistant,$differentUser)
    $nonFinalAssistant=New-Article 2 'ChatGPT said:' @((Node $status),(Node $label),(Node 'The earlier status was only an example'))
    $unready=Read-CurrentTurn @{window=(Transcript @($initial,$nonFinalAssistant)); chat=$chat}
    [ordered]@{literal_label=$label
        anchored_wrong_body_accepted=(Find-PostedMessage $different $expected $prior.response_id)
        unanchored_wrong_body_accepted=(Find-PostedMessage $different $expected)
        assistant_non_final_marked_ready=$unready.ready
        assistant_tail_retained=($unready.text -match 'only an example')}
})
$unrecognized=New-Article 4 'You said:' @((Node 'A newer unverified message')) $false
$withNewerUnverified=Transcript @($initial,$assistant,$exactUser,$unrecognized)
$withUnverifiedAfterStatus=Transcript @($initial,$assistant,$unrecognized)
$statusWithNewUnverified=Read-CurrentTurn @{window=$withUnverifiedAfterStatus; chat=$chat}
[ordered]@{
 exact_anchored_accepted=$exactAnchored
 exact_unanchored_accepted=$exactUnanchored
 final_prose_status_ready=$prior.ready
 literal_label_cases=$cases
 anchored_receipt_despite_newer_unverified_article=(Find-PostedMessage $withNewerUnverified $expected $prior.response_id)
 unanchored_receipt_despite_newer_unverified_article=(Find-PostedMessage $withNewerUnverified $expected)
 earlier_status_ready_despite_newer_unverified_article=$statusWithNewUnverified.ready
} | ConvertTo-Json -Depth 5
