$ErrorActionPreference='Stop'
Set-StrictMode -Version Latest
$source=Join-Path $PSScriptRoot '..\uia_adapter.ps1'
$tokens=$null
$errors=$null
$ast=[Management.Automation.Language.Parser]::ParseFile($source,[ref]$tokens,[ref]$errors)
if($errors.Count){throw ('UIA parser errors: '+($errors|Out-String))}
foreach($name in @('Test-TranscriptRegion','Get-VirtualizedConversationTurns',
 'Get-ConversationTurns','Find-PostedMessage','Read-ConversationContent','Read-CurrentTurn')){
 $defs=@($ast.FindAll({param($n)
  $n -is [Management.Automation.Language.FunctionDefinitionAst] -and $n.Name -ceq $name
 },$true))
 if($defs.Count -ne 1){throw ('Missing or duplicate function '+$name)}
 Invoke-Expression $defs[0].Extent.Text
}
Add-Type -AssemblyName UIAutomationTypes
function Node($kind,$class,$name='',[object[]]$children=@(),[bool]$prose=$false){
 $control=if($kind -eq 'text') {[System.Windows.Automation.ControlType]::Text}
          elseif($kind -eq 'button'){[System.Windows.Automation.ControlType]::Button}
          else{[System.Windows.Automation.ControlType]::Group}
 return @{Current=@{LocalizedControlType=$kind;ClassName=$class;Name=$name
                    ControlType=$control;IsEnabled=$false}
          Children=$children;Prose=$prose}
}
function Desc($node){
 foreach($child in $node.Children){
  $child
  Desc $child
 }
}
function Get-AccessibilityChildren($node){return $node.Children}
function Test-AssistantProse($node){return $node.Prose}
function Expect-Hold([scriptblock]$probe,[string]$reason){
 $held=$false
 try{& $probe}catch{$held=$true}
 if(-not $held){throw ('Accepted invalid virtualized structure: '+$reason)}
}
$expected='Complete exact user instruction'
$userHeading=Node 'heading' 'sr-only print:not-sr-only' 'You said:'
$userText=Node 'text' '' $expected
$userBody=Node 'group' 'bg-user-message text-user-message rounded-2xl' '' @($userText)
$assistantHeading=Node 'heading' 'sr-only print:not-sr-only' 'ChatGPT said:'
$status=Node 'text' '' 'CHAT_STATUS: TASK_COMPLETE' -prose $true
$quotedRole=Node 'text' '' 'You said:'
$tail=Node 'text' '' 'Additional explanation after a literal role-like label'
$assistantBody=Node 'group' 'relative Renderer-aBcd12' '' @($status,$quotedRole,$tail)
$actions=Node 'button' 'button-icon' ''
$wrapper=Node 'group' 'relative shrink-0' '' @(
 (Node 'separator' 'flex justify-center py-4'),
 $userHeading,$userBody,$actions,
 (Node 'group' 'text-size-chat text-secondary'),
 $assistantHeading,$assistantBody,$actions
)
$layout=Node 'group' 'relative transcriptContent-exact w-full' '' @($wrapper)
$thread=Node 'region' 'thread-scroll-container' '' @($layout)
$window=Node 'window' 'Chrome' '' @($thread)
$target=@{window=$window;chat='00000000-0000-0000-0000-000000000001'}
$ProjectId='g-p-valid'
$turns=@(Get-ConversationTurns (Desc $window))
if($turns.Count -ne 2 -or $turns[0].role -cne 'user' -or
   $turns[1].role -cne 'assistant' -or -not $turns[0].virtualized -or
   -not $turns[1].virtualized){throw 'Verified direct virtualized pair not extracted'}
$body=Read-ConversationContent $turns[1] 1
if($body.text -cnotmatch 'You said:' -or $body.text -cnotmatch 'Additional explanation'){
 throw 'Literal role-labelled body content was truncated'
}
$observed=Read-CurrentTurn $target -IncludeUserAnchor
if($observed.ready -or $observed.response_id -or
   $observed.text -cne '' -or $observed.ContainsKey('latest_user_digest') -or
   $observed.assistant_turn_count -or $observed.user_turn_count -or
   $observed.method -cne 'UIA_VIRTUALIZED_UNQUALIFIED' -or
   $observed.reason -cnotmatch 'lacks verified absolute turn identity'){
 throw 'Virtualized body incorrectly produced an actionable response or history anchor'
}
if(-not $observed.user_turn_seen -or
   (Find-PostedMessage $window $expected) -or
   (Find-PostedMessage $window $expected 'uia-turn-1-aaaaaaaaaaaaaaaaaaaa')){
 throw 'Virtualized user message was wrongly acknowledged as a Send receipt'
}
$stream=Node 'button' 'streaming' 'Stop'
$stream.Current.IsEnabled=$true
$window.Children+=,$stream
if((Read-CurrentTurn $target -IncludeUserAnchor).ready){
 throw 'Streaming virtualized assistant became actionable'
}
$window.Children=@($thread)
# An unseen trailing assistant, an unpaired heading or new body must block.
$original=@($wrapper.Children)
$wrapper.Children+=,(Node 'heading' 'sr-only' 'ChatGPT said:')
Expect-Hold {Get-ConversationTurns (Desc $window)|Out-Null} 'unpaired trailing assistant'
$wrapper.Children=@($original)
$wrapper.Children+=,(Node 'group' 'Renderer-bad' '' @($status))
Expect-Hold {Get-ConversationTurns (Desc $window)|Out-Null} 'orphan assistant renderer'
$wrapper.Children=@($original)
$assistantBody.Current.ClassName='opaque-container'
Expect-Hold {Get-ConversationTurns (Desc $window)|Out-Null} 'changed assistant body identity'
$assistantBody.Current.ClassName='relative Renderer-aBcd12'
$userBody.Current.ClassName='text-user-message only'
Expect-Hold {Get-ConversationTurns (Desc $window)|Out-Null} 'changed user body identity'
$userBody.Current.ClassName='bg-user-message text-user-message rounded-2xl'
$wrapper.Children=@($original)+@($assistantHeading,$assistantBody)
Expect-Hold {Get-ConversationTurns (Desc $window)|Out-Null} 'duplicate assistant role'
$wrapper.Children=@($original)
$nested=Node 'heading' 'sr-only' 'You said:'
$assistantBody.Children=@($status,$nested,$tail)
Expect-Hold {Get-ConversationTurns (Desc $window)|Out-Null} 'nested application label'
$assistantBody.Children=@($status,$quotedRole,$tail)
$wrapper.Children=@($original)+@((Node 'heading' 'sr-only' 'Unknown application role'))
Expect-Hold {Get-ConversationTurns (Desc $window)|Out-Null} 'unverified trailing role heading'
$wrapper.Children=@($original)
$layout.Children+=,(Node 'group' 'transcriptContent-duplicate' '' @($wrapper))
Expect-Hold {Get-ConversationTurns (Desc $window)|Out-Null} 'duplicate transcript layout'
$layout.Children=@($wrapper)
$window.Children=@($thread,(Node 'region' 'thread-scroll-container' '' @($layout)))
Expect-Hold {Get-ConversationTurns (Desc $window)|Out-Null} 'duplicate transcript region'
Write-Output 'PASS: virtualized direct heading/body structure; non-actionable and absent receipt; negative ambiguity and streaming cases.'
