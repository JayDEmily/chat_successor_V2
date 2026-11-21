$ErrorActionPreference='Stop'
Set-StrictMode -Version Latest
$path=Join-Path $PSScriptRoot '..\uia_adapter.ps1'
$tokens=$null
$errors=$null
$tree=[Management.Automation.Language.Parser]::ParseFile($path,[ref]$tokens,[ref]$errors)
if($errors.Count -ne 0){throw 'UIA adapter PowerShell syntax failed'}
foreach($name in @('Test-SameWorkerTurn','Test-FreshWorkerCompletion','Test-ViewRecoveryPaused',
                   'Check-Project','Chat-FromUrl','Find-TargetWindows','Get-TargetWindow',
                   'Test-TranscriptRegion','Get-VirtualizedSavedUserHeading',
                   'Read-SavedWorkerIdentity','Wait-VerifiedSavedWorker','Read-ComposerText')){
 $found=@($tree.FindAll({param($n) $n -is [Management.Automation.Language.FunctionDefinitionAst] -and $n.Name -eq $name},$true))
 if($found.Count -ne 1){throw "Function definition missing or ambiguous: $name"}
 Invoke-Expression $found[0].Extent.Text
}
$old=@{response_id='old';ready=$false;stop_control=$true;user_after_assistant=$false;assistant_turn_count=1;user_turn_count=1;latest_user_digest='same-user'}
$new=@{response_id='new';ready=$true;stop_control=$false;user_after_assistant=$false;assistant_turn_count=1;user_turn_count=1;latest_user_digest='same-user'}
if(-not (Test-FreshWorkerCompletion $old $new)){throw 'Valid completed fresh view rejected'}
if(Test-FreshWorkerCompletion $old $new @($new.response_id)){throw 'Consumed reply allows stale reload'}
$stream=@{}+$new
$stream.ready=$false
if(Test-FreshWorkerCompletion $old $stream){throw 'Streaming fresh view incorrectly treated as completed'}
$other=@{}+$new
$other.latest_user_digest='other-user'
if(Test-FreshWorkerCompletion $old $other){throw 'Changed user turn incorrectly accepted'}
$otherCount=@{}+$new
$otherCount.user_turn_count=2
if(Test-FreshWorkerCompletion $old $otherCount){throw 'Changed user count incorrectly accepted'}
$stable=@{}+$new
if(-not (Test-SameWorkerTurn $new $stable)){throw 'Stable fresh double-read rejected'}
$changed=@{}+$new
$changed.response_id='another-reply'
if(Test-SameWorkerTurn $new $changed){throw 'Different response accepted as stable double-read'}
$PausePath=Join-Path $env:TEMP 'a2-l04-test-marker.pause'
try{
 if(Test-ViewRecoveryPaused){throw 'Unexpected marker before test'}
 [IO.File]::WriteAllText($PausePath,'pause marker test')
 if(-not (Test-ViewRecoveryPaused)){throw 'Durable marker not recognised'}
}finally{
 Remove-Item -LiteralPath $PausePath -Force -ErrorAction SilentlyContinue
}

# The wrapper pins the native profile. A matching URL and HWND alone are insufficient.
Add-Type -Path (Join-Path $PSScriptRoot '..\window_profile.cs')
$ProjectId='g-p-abc123'
$worker='00000000-0000-0000-0000-000000000001'
$url="https://chatgpt.com/g/$ProjectId/c/$worker"
$window=@{Current=@{NativeWindowHandle=55}; Profile='Chrome.Other'}
function Get-ChromeWindows { return $window }
function Get-Address($item) { return $url }
function Test-WindowProfile($item) { return ($item.Profile -ceq 'Chrome.Nominated') }
$wrongProfileHeld=$false
try { $null=Get-TargetWindow $worker 55 } catch {
    $wrongProfileHeld=$_.Exception.Message -like '*profile could not be verified*'
}
if(-not $wrongProfileHeld){throw 'Wrong Chrome profile selected by URL and handle'}
$window.Profile='Chrome.Nominated'
if((Get-TargetWindow $worker 55).chat -cne $worker){throw 'Verified profile target refused'}
if(Chat-FromUrl "https://chatgpt.com/g/$ProjectId/c/local-chatgpt"){throw 'Provisional successor treated as saved'}

$ChatId=$worker
$ChromeAppId='Chrome.Nominated'
$script:targetWindows=@($window)
function Get-ChromeWindows { return $script:targetWindows }
function Saved-ViewNode($kind,$class,$identity,$name='',[object[]]$children=@()){
 return @{Current=@{LocalizedControlType=$kind; ClassName=$class; Name=$name}
          Identity=$identity; Children=$children}
}
$userHeading=Saved-ViewNode 'heading' 'sr-only print:not-sr-only' 'user-label' 'You said:'
$userBody=Saved-ViewNode 'group' 'bg-user-message text-user-message rounded-2xl' 'user-body'
$messageGroup=Saved-ViewNode 'group' 'relative shrink-0' 'turns' -children @($userHeading,$userBody)
$layout=Saved-ViewNode 'group' 'relative flex transcriptContent-kMyLayout w-full' 'content' -children @($messageGroup)
$thread=Saved-ViewNode 'region' 'thread-scroll-container' 'thread' -children @($layout)
$document=Saved-ViewNode 'document' '' 'first-document' -children @($thread)
$script:documentReads=0
function Desc($element){return $element.Children}
function Get-AccessibilityChildren($element){return $element.Children}
function Find-Composer($item,$name){return @{window=$item;expectation=$name}}
function Get-ComposerDocument($editor){
 $script:documentReads++
 $document.Identity=if($script:documentReads -eq 1){'first-document'}else{'stable-document'}
 return $document
}
function Get-DocumentIdentity($node){return $node.Identity}
function Read-SavedWorkerView {throw 'The strict turn reader was called on a loaded virtualized view'}
function Start-Sleep([int]$Milliseconds){ }

$target=Get-TargetWindow $worker 55
$read=Read-SavedWorkerIdentity $target
if($read.user_heading_id -cne 'user-label' -or $read.ContainsKey('response_id')){
 throw 'Loaded view identity was confused with a response receipt'
}
$messageGroup.Children=@($userHeading)
$missingBodyHeld=$false
try{$null=Read-SavedWorkerIdentity $target}catch{
 $missingBodyHeld=$_.Exception.Message -like '*loaded user message could not be verified*'
}
if(-not $missingBodyHeld){throw 'A standalone role label established a loaded view'}
$messageGroup.Children=@($userHeading,$userBody)
$ChromeAppId=''
$unboundHeld=$false
try{$null=Read-SavedWorkerIdentity $target}catch{
 $unboundHeld=$_.Exception.Message -like '*needs a verified Chrome profile*'
}
if(-not $unboundHeld){throw 'An unbound virtualized view was accepted'}
$ChromeAppId='Chrome.Nominated'
$script:documentReads=0
$restored=Wait-VerifiedSavedWorker 55
if($restored.recovery_status -cne 'restored' -or $script:documentReads -ne 3){
 throw 'Changed document was accepted before two stable identity reads'
}
$script:targetWindows=@($window,@{Current=@{NativeWindowHandle=56}; Profile='Chrome.Nominated'})
$duplicateHeld=$false
try{$null=Wait-VerifiedSavedWorker 55}catch{
 $duplicateHeld=$_.Exception.Message -like '*not the unique accessible saved worker*'
}
if(-not $duplicateHeld){throw 'A duplicate saved window was accepted at final validation'}
$script:targetWindows=@($window)
$script:pauseChecks=0
function Test-ViewRecoveryPaused {$script:pauseChecks++;return $script:pauseChecks -ge 3}
if((Wait-VerifiedSavedWorker 55).recovery_status -cne 'paused'){
 throw 'A pause before recovery completion was ignored'
}
Write-Output 'PASS: PS recovery comparisons, stable loaded-view recovery, and pause/duplicate/identity holds.'

Add-Type -AssemblyName UIAutomationTypes
$label='New chat in a disposable Project with a long label'
$placeholderText=Saved-ViewNode 'text' '' 'placeholder-text' $label
$placeholderText.Current.ControlType=[System.Windows.Automation.ControlType]::Text
$placeholder=Saved-ViewNode 'group' '' 'placeholder' -children @($placeholderText)
$break=Saved-ViewNode 'text' 'ProseMirror-trailingBreak' 'break'
$paragraph=Saved-ViewNode 'group' 'placeholder before:composer-placeholder' 'empty-paragraph' -children @($placeholder,$break)
$editor=Saved-ViewNode 'edit' 'ProseMirror' 'editor' $label -children @($paragraph)
$plainValue=$label+[char]10
$clippedValue=$label+$label.Substring(0,$label.Length-2)+[char]0x2026+[char]10
if((Read-ComposerText $editor $plainValue) -cne ''){throw 'Original empty composer rejected'}
if((Read-ComposerText $editor $clippedValue) -cne ''){throw 'Clipped duplicate placeholder rejected'}
if($null -ne (Read-ComposerText $editor ($clippedValue+'x'))){throw 'Unrecognised value accepted as empty'}
foreach($clippedBy in @(1,3)){
 $otherValue=$label+$label.Substring(0,$label.Length-$clippedBy)+[char]0x2026+[char]10
 if($null -ne (Read-ComposerText $editor $otherValue)){throw 'Unrecognised clipping length accepted as empty'}
}
$editor.Children=@($paragraph,(Saved-ViewNode 'group' '' 'extra-paragraph'))
if($null -ne (Read-ComposerText $editor $clippedValue)){throw 'Extra composer child accepted as empty'}
$editor.Children=@($paragraph)
$placeholder.Children=@($placeholderText,(Saved-ViewNode 'text' '' 'extra-text'))
if($null -ne (Read-ComposerText $editor $clippedValue)){throw 'Extra placeholder text accepted as empty'}
$placeholder.Children=@($placeholderText)
$paragraph.Current.ClassName=''
foreach($draft in @($label,$clippedValue)){
 if((Read-ComposerText $editor $draft) -cne $draft){throw 'Draft mistaken for a placeholder'}
}
Write-Output 'PASS: Original and clipped placeholders, unknown composer shapes, and placeholder-like drafts.'
