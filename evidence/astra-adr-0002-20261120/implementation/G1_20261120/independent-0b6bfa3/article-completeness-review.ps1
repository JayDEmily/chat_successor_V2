param([Parameter(Mandatory=$true)][string]$Candidate)
$ErrorActionPreference='Stop'
Set-StrictMode -Version Latest
Add-Type -AssemblyName UIAutomationTypes
$tokens=$null
$errors=$null
$ast=[Management.Automation.Language.Parser]::ParseFile((Join-Path $Candidate 'integration\uia_adapter.ps1'),[ref]$tokens,[ref]$errors)
if($errors.Count){throw 'Candidate PowerShell parser failed'}
foreach($name in @('Test-TranscriptRegion','Get-ConversationRole','Get-ConversationTurns','Read-ConversationContent','Find-PostedMessage','Read-CurrentTurn')){
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
function Role-Heading([int]$serial,[string]$role,[string]$roleClass){
    $heading=Node $role 'heading' $roleClass
    $heading.RuntimeNumber=$serial
    $heading | Add-Member ScriptMethod GetRuntimeId { return @(42,$this.RuntimeNumber) }
    Attach $heading (Node $role)
    return $heading
}
function New-Article([int]$serial,[string]$role,[object[]]$body,[bool]$recognized=$true) {
    $article=Node '' 'article'
    $article.RuntimeNumber=$serial
    $article | Add-Member ScriptMethod GetRuntimeId { return @(42,$this.RuntimeNumber) }
    $roleClass=if($recognized){'sr-only'}else{''}
    Attach $article (Role-Heading ($serial+1000) $role $roleClass)
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
function Read-Held($window,$expectedReason){
    try { $null=Read-CurrentTurn @{window=$window;chat=$chat}; return $false }
    catch { return $_.Exception.Message -like $expectedReason }
}
function Attach-Stop($window){
    $stop=Node 'Stop' 'button'
    $stop.Current.ControlType=[System.Windows.Automation.ControlType]::Button
    $stop.Current.IsEnabled=$true
    Attach $window $stop
}
$unverifiedHeld=Read-Held $withUnverifiedAfterStatus '*no verified role heading*'
$malformed=New-Article 2 'ChatGPT said:' @((Node $status))
Attach $malformed (Role-Heading 2000 'ChatGPT said:' 'sr-only')
$duplicateHeading=Transcript @($initial,$malformed)
$conflicting=New-Article 2 'ChatGPT said:' @((Node $status))
Attach $conflicting (Role-Heading 2001 'You said:' 'sr-only')
$conflictingHeading=Transcript @($initial,$conflicting)
$multiple=Transcript @($initial,$assistant,$exactUser)
Attach $multiple (Node 'Another thread' 'region' 'thread-scroll-container')
$streaming=Transcript @($initial,$assistant)
Attach-Stop $streaming
$validStream=Read-CurrentTurn @{window=$streaming; chat=$chat}
$streamingIncomplete=Transcript @($initial,$assistant,$unrecognized)
Attach-Stop $streamingIncomplete
$unknownStream=Read-CurrentTurn @{window=$streamingIncomplete; chat=$chat}
[ordered]@{
 exact_anchored_accepted=$exactAnchored
 exact_unanchored_accepted=$exactUnanchored
 final_prose_status_ready=$prior.ready
 literal_label_cases=$cases
 anchored_receipt_despite_newer_unverified_article=(Find-PostedMessage $withNewerUnverified $expected $prior.response_id)
 unanchored_receipt_despite_newer_unverified_article=(Find-PostedMessage $withNewerUnverified $expected)
 unverified_article_holds_earlier_status=$unverifiedHeld
 duplicate_same_role_heading_holds=(Read-Held $duplicateHeading '*multiple role headings*')
 conflicting_role_headings_hold=(Read-Held $conflictingHeading '*multiple role headings*')
 multiple_transcripts_refuse_acknowledgement=(-not (Find-PostedMessage $multiple $expected))
 multiple_transcripts_hold_status=(Read-Held $multiple '*single conversation transcript*')
 known_streaming_status_remains_unready=($validStream.stop_control -and -not $validStream.ready)
 incomplete_streaming_waits=($unknownStream.stop_control -and -not $unknownStream.ready -and $unknownStream.reason -like '*incomplete*')
} | ConvertTo-Json -Depth 5
