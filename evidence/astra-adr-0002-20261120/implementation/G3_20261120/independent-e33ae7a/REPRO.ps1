param([string]$RepoRoot)
$ErrorActionPreference='Stop'
Set-StrictMode -Version Latest
if(-not $RepoRoot){$RepoRoot=(Resolve-Path (Join-Path $PSScriptRoot '..\..\..\..\..')).Path}
. (Join-Path $RepoRoot 'integration\tests\test_a2_l03_ps_action_gate.ps1')
function Inject-UnknownTranscriptSibling($window,[bool]$withChangedHeading) {
 $thread=$window.Children[0]
 $rows=@()
 if($withChangedHeading) {
  $h=Text-Leaf 'ChatGPT said:'
  $h.Current.LocalizedControlType='heading'
  $h.Current.ClassName='visually-hidden changed-accessibility'
  $h.Parent=$thread
  $rows+=,$h
 }
 $newer=[pscustomobject]@{Current=@{Name=''; ControlType=[System.Windows.Automation.ControlType]::Group
                       LocalizedControlType='group';ClassName='opaque-message-row'}
                       Children=@((Text-Leaf 'Synthetic newer unclassified content'))
                       Parent=$thread}
 $rows+=,$newer
 $thread.Children=@($thread.Children)+$rows
 $window.Children=@($window.Children)+$rows
}
$oldUser=Turn-Article 1 'You said:' @((Text-Leaf 'Synthetic prior instruction'))
$oldAssistant=Turn-Article 2 'ChatGPT said:' @((Text-Leaf 'CHAT_STATUS: TASK_COMPLETE' $true))
foreach($withHeading in @($false,$true)) {
 $view=Transcript-Window @($oldUser,$oldAssistant)
 $before=Read-CurrentTurn @{window=$view;chat='synthetic-chat'} -IncludeUserAnchor
 if(-not $before.ready){throw 'Fixture baseline invalid: prior complete article not ready'}
 Inject-UnknownTranscriptSibling $view $withHeading
 $after=Read-CurrentTurn @{window=$view;chat='synthetic-chat'} -IncludeUserAnchor
 if(-not $after.ready -or $after.response_id -cne $before.response_id){throw 'Expected unsafe old status was not reproduced'}
 if($after.latest_user_digest -cne $before.latest_user_digest){throw 'Expected stale user anchor was not reproduced'}
 Write-Output ('REPRO_STALE_STATUS_READY=TRUE; CHANGED_HEADING='+$withHeading+'; RESPONSE_REUSED=TRUE; USER_ANCHOR_REUSED=TRUE')
}
$posted=Turn-Article 3 'You said:' @((Text-Leaf $Message))
$view2=Transcript-Window @($oldUser,$oldAssistant,$posted)
$prior=Get-ConversationRole $oldAssistant.Children[0]
$anchor=(Read-ConversationContent $prior 1).response_id
if(-not (Find-PostedMessage $view2 $Message $anchor)){throw 'Fixture baseline invalid: exact post not acknowledged'}
Inject-UnknownTranscriptSibling $view2 $false
$ack=Find-PostedMessage $view2 $Message $anchor
if(-not $ack){throw 'Expected false acknowledgement was not reproduced'}
Write-Output 'REPRO_FALSE_POSTED_ACK=TRUE; NEWER_OPAQUE_SIBLING_IGNORED=TRUE'
