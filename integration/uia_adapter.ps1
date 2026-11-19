# Astra UIA adapter. One browser actor. Never invoke -Mode Send without a persisted
# reference-controller 'sending' state. No automatic retries or reset.
[CmdletBinding()]
param(
 [Parameter(Mandatory=$true)][ValidateSet('Observe','Prepare','Send','Reconcile')][string]$Mode,
 [Parameter(Mandatory=$true)][string]$ProjectId,
 [Parameter(Mandatory=$true)][string]$ProjectName,
 [string]$ChatId = '',
 [ValidateSet('CONTINUE_CURRENT','LAUNCH_SUCCESSOR')][string]$Kind = 'CONTINUE_CURRENT',
 [long]$WindowHandle = 0,
 [string]$Message = '',
 [string]$L09Fault = '',
 [string]$PausePath = '',
 [string]$ChromeExe = 'C:\Program Files\Google\Chrome\Application\chrome.exe',
 [switch]$AlreadyTyped
)
Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName UIAutomationClient
Add-Type -AssemblyName UIAutomationTypes

function Desc($element) {
 return $element.FindAll([System.Windows.Automation.TreeScope]::Descendants,
                         [System.Windows.Automation.Condition]::TrueCondition)
}
function Get-ChromeWindows {
 $all=[System.Windows.Automation.AutomationElement]::RootElement.FindAll(
  [System.Windows.Automation.TreeScope]::Children,
  [System.Windows.Automation.Condition]::TrueCondition)
 $found=@()
 foreach($item in $all) {
  try {
   if($item.Current.NativeWindowHandle -ne 0 -and $item.Current.Name -like '*Google Chrome*') {
    $found+= $item
   }
  }catch{}
 }
 return $found
}
function Get-Address($window) {
 foreach($el in (Desc $window)) {
  try {
   if($el.Current.ControlType -eq [System.Windows.Automation.ControlType]::Edit -and
      $el.Current.Name -eq 'Address and search bar') {
    $v=$el.GetCurrentPattern([System.Windows.Automation.ValuePattern]::Pattern).Current.Value
    if($v -match '^chatgpt[.]com/') {return 'https://' + $v}
    return $v
   }
  }catch{}
 }
 return ''
}
function Check-Project($url) {
 return ($url -match ('^https://chatgpt[.]com/g/' + [regex]::Escape($ProjectId) + '(?:-[^/]+)?/(?:project|c/[A-Za-z0-9_-]+)(?:[/?#]|$)'))
}
function Chat-FromUrl($url) {
 if($url -match ('^https://chatgpt[.]com/g/' + [regex]::Escape($ProjectId) + '(?:-[^/]+)?/c/([A-Za-z0-9_-]+)(?:[/?#]|$)')) {
  return $Matches[1]
 }
 return $null
}
function Get-TargetWindow([string]$expectedChat,[long]$handle) {
 $hits=@()
 foreach($w in (Get-ChromeWindows)) {
  try{
   if($handle -ne 0 -and $w.Current.NativeWindowHandle -ne $handle){continue}
   $url=Get-Address $w
   if(-not (Check-Project $url)){continue}
   $chat=Chat-FromUrl $url
   if($expectedChat -and $chat -cne $expectedChat){continue}
   $hits+=@{window=$w;url=$url;chat=$chat}
  }catch{}
 }
 if($hits.Count -ne 1){throw ('Expected exactly one active Project target, found ' + $hits.Count)}
 return $hits[0]
}
function Find-Composer($window,$expectedName) {
 $editors=@()
 foreach($el in (Desc $window)){
  try{
   if($el.Current.ControlType -eq [System.Windows.Automation.ControlType]::Edit -and
      $el.Current.Name -ceq $expectedName -and
      $el.Current.IsEnabled -and -not $el.Current.IsOffscreen){$editors+= $el}
  }catch{}
 }
 if($editors.Count -ne 1){throw ('Project editor not uniquely observed, count=' + $editors.Count)}
 return $editors[0]
}
function Find-ProjectButton($window) {
 $matches=@()
 foreach($el in (Desc $window)){
  try {
   if($el.Current.ControlType -eq [System.Windows.Automation.ControlType]::Button -and
      $el.Current.Name -ceq ('New chat in ' + $ProjectName) -and $el.Current.IsEnabled) {
    $p=$null
    if($el.TryGetCurrentPattern([System.Windows.Automation.InvokePattern]::Pattern,[ref]$p)) {
     $matches+= $el
    }
   }
  }catch{}
 }
 if($matches.Count -ne 1){throw ('Project New Chat button not unique, count=' + $matches.Count)}
 return $matches[0]
}
function Check-NoAttachments($window) {
 # Conservative: expose positive attachment controls; no file-selection action.
 foreach($el in (Desc $window)) {
  try {
   if($el.Current.IsOffscreen){continue}
   if($el.Current.ControlType -eq [System.Windows.Automation.ControlType]::Button -and
      $el.Current.Name -match '^(Remove(?: |$)|Delete attachment)') {
    return $false
   }
  }catch{}
 }
 return $true
}
function Read-ComposerText($editor,[string]$value) {
 # ProseMirror marks its empty paragraph independently of the UIA Value.
 # Unknown structure stays unknown. A real draft may match the placeholder text.
 if(($editor.Current.ClassName -csplit '\s+') -cnotcontains 'ProseMirror'){return $null}
 $walker=[System.Windows.Automation.TreeWalker]::RawViewWalker
 $paragraph=$walker.GetFirstChild($editor)
 if($null -eq $paragraph){return $null}
 if(($paragraph.Current.ClassName -csplit '\s+') -cnotcontains 'before:composer-placeholder'){
  if($value){return $value}
  return $null
 }
 if($null -ne $walker.GetNextSibling($paragraph) -or
    $value -cne ($editor.Current.Name + [char]10)){return $null}
 $placeholder=$walker.GetFirstChild($paragraph)
 if($null -eq $placeholder){return $null}
 $text=$walker.GetFirstChild($placeholder)
 $trailingBreak=$walker.GetNextSibling($placeholder)
 if($null -ne $text -and $null -ne $trailingBreak -and
    $text.Current.ControlType -eq [System.Windows.Automation.ControlType]::Text -and
    $text.Current.Name -ceq $editor.Current.Name -and
    $null -eq $walker.GetNextSibling($text) -and
    $trailingBreak.Current.ClassName -ceq 'ProseMirror-trailingBreak' -and
    $null -eq $walker.GetNextSibling($trailingBreak)){
  return ''
 }
 return $null
}
function Find-EnabledSendButtons($window) {
 foreach($el in (Desc $window)){
  try {
   if($el.Current.ControlType -eq [System.Windows.Automation.ControlType]::Button -and
      $el.Current.Name -ceq 'Send' -and $el.Current.IsEnabled -and
      -not $el.Current.IsOffscreen){$el}
  }catch{}
 }
}
function Find-PostedMessage($window,$expected) {
 # Only text under a user turn is a posted message. The assistant may quote
 # the exact continuation string while instructing the operator to send it.
 $all=Desc $window
 $inUserTurn=$false
 $latestUserMatches=$false
 foreach($el in $all) {
  try{
   if($el.Current.ControlType -ne [System.Windows.Automation.ControlType]::Text){continue}
   $name=$el.Current.Name
   if($name -ceq 'You said:'){
    $inUserTurn=$true
    $latestUserMatches=$false
   }elseif($name -ceq 'ChatGPT said:'){
    $inUserTurn=$false
   }elseif($inUserTurn -and $name -ceq $expected){
    $latestUserMatches=$true
   }
  }catch{}
 }
 return $latestUserMatches
}

if($Mode -eq 'Observe') {
 if(-not $ChatId){throw 'Observe needs a known saved chat ID'}
 $target=Get-TargetWindow $ChatId 0
 $all=Desc $target.window
 $last=-1
 $assistantCount=0
 $stop=$false
 for($i=0;$i -lt $all.Count;$i++){
  $el=$all[$i]
  try{
   if($el.Current.ControlType -eq [System.Windows.Automation.ControlType]::Text -and
      $el.Current.Name -ceq 'ChatGPT said:'){$assistantCount++;$last=$i}
   if($el.Current.ControlType -eq [System.Windows.Automation.ControlType]::Button -and
      $el.Current.Name -ceq 'Stop' -and $el.Current.IsEnabled){$stop=$true}
  }catch{}
 }
 if($last -lt 0){
  @{ready=$false;reason='No assistant turn observed';chat_id=$ChatId} | ConvertTo-Json -Compress
  exit 0
 }
 $parts=@()
 for($i=$last+1;$i -lt $all.Count;$i++){
  $el=$all[$i]
  try {
   if($el.Current.ControlType -eq [System.Windows.Automation.ControlType]::Text) {
    $name=$el.Current.Name
    if($name -ceq 'You said:' -or $name -ceq 'ChatGPT said:' -or
       $name -ceq 'ChatGPT can make mistakes. Check important info.' -or
       $name -ceq 'Latest response' -or $name -ceq 'Ask ChatGPT'){break}
    if($name){$parts+= $name}
   }
  }catch{}
 }
 $body=$parts -join [Environment]::NewLine
 $sha=[Security.Cryptography.SHA256]::Create()
 try{$digest=[BitConverter]::ToString($sha.ComputeHash([Text.Encoding]::UTF8.GetBytes($body))).Replace('-','').ToLowerInvariant()}finally{$sha.Dispose()}
 $final=if($parts.Count){$parts[-1]}else{''}
 # No automatic turn completion until a final status line and no active Stop.
 $terminal=($final -cmatch '^(?:CHAT_STATUS: )?(?:NEED_MORE_TIME|TASK_COMPLETE|ERROR)$')
 $ready=$terminal -and -not $stop
 @{
  ready=$ready;chat_id=$ChatId;project=$ProjectId;role='assistant'
  response_id=('uia-turn-' + $assistantCount + '-' + $digest.Substring(0,20))
  text=$body;complete=$ready;reason=$(if($stop){'Streaming/Stop control present'}elseif(-not $terminal){'No final standalone status leaf'}else{'Completed marker candidate; UIA hierarchy validation pending'})
  method='UIA_ACCESSIBILITY_TEXT';stop_control=$stop
 } | ConvertTo-Json -Compress -Depth 5
 exit 0
}

if($Mode -eq 'Prepare') {
 if($Kind -eq 'CONTINUE_CURRENT') {
  if(-not $ChatId){throw 'Continuation needs current saved chat'}
  $target=Get-TargetWindow $ChatId 0
  $editor=Find-Composer $target.window 'Ask ChatGPT'
 }else{
  if(-not (Test-Path -LiteralPath $ChromeExe -PathType Leaf)){throw 'Chrome executable missing'}
  # In this Chrome installation the Project-specific sidebar control
  # was found but remained offscreen after ScrollIntoView. Reuse the observed
  # authenticated /project URL instead; never construct or guess a Project URL.
  $projectPages=@()
  foreach($existing in (Get-ChromeWindows)){
   try{
    $observedUrl=Get-Address $existing
    if((Check-Project $observedUrl) -and $observedUrl -match '/project$'){
     $projectPages+= $observedUrl
    }
   }catch{}
  }
  $uniquePages=@($projectPages | Select-Object -Unique)
  if($uniquePages.Count -ne 1){throw 'No unique independently observed target Project URL'}
  $before=@((Get-ChromeWindows) | ForEach-Object {$_.Current.NativeWindowHandle})
  Start-Process -FilePath $ChromeExe -ArgumentList @('--new-window', $uniquePages[0])
  $new=$null
  for($i=0;$i -lt 50;$i++){
   Start-Sleep -Milliseconds 400
   $candidates=@((Get-ChromeWindows) | Where-Object {$before -notcontains $_.Current.NativeWindowHandle})
   if($candidates.Count -gt 1){throw 'Ambiguous new Chrome windows'}
   if($candidates.Count -eq 1){$new=$candidates[0];break}
  }
  if($null -eq $new){throw 'Fresh Chrome window was not uniquely observed'}
  $target=$null
  for($i=0;$i -lt 50;$i++){
   Start-Sleep -Milliseconds 400
   $url=Get-Address $new
   if((Check-Project $url) -and $null -eq (Chat-FromUrl $url)){
    try {$editor=Find-Composer $new ('New chat in ' + $ProjectName)
         $target=@{window=$new;url=$url;chat=$null};break}catch{}
   }
  }
  if($null -eq $target){throw 'Fresh Project composer not established'}
 }
 $value=$editor.GetCurrentPattern([System.Windows.Automation.ValuePattern]::Pattern).Current.Value
 $actual=Read-ComposerText $editor $value
 $attachments=-not (Check-NoAttachments $target.window)
 if(-not $attachments -and $actual -ceq '' -and @(Find-EnabledSendButtons $target.window).Count){
  $attachments=$null
 }
 @{
  project=$ProjectId;current_chat_id=$target.chat
  private_window_handle=[long]$target.window.Current.NativeWindowHandle
  editable_text=$actual;uia_value=$value
  attachments_present=$attachments
  observed_url=$target.url
 } | ConvertTo-Json -Compress -Depth 5
 exit 0
}

function Hold-IfOwnerPaused {
 if($PausePath -and (Test-Path -LiteralPath $PausePath)) {
  @{paused_before_click=$true} | ConvertTo-Json -Compress
  exit 0
 }
}

if($Mode -eq 'Send') {
 Hold-IfOwnerPaused
 if($WindowHandle -le 0){throw 'Saved prepared window handle required'}
 if($Message -cnotmatch '^[A-Za-z0-9 .,/_:-]+$'){throw 'Unsupported message characters'}
 if(-not $Message){throw 'Empty message'}
 $target=Get-TargetWindow $(if($Kind -eq 'CONTINUE_CURRENT'){$ChatId}else{''}) $WindowHandle
 if($Kind -eq 'LAUNCH_SUCCESSOR' -and $null -ne $target.chat){throw 'Successor composer already saved before Send'}
 $editorName=if($Kind -eq 'CONTINUE_CURRENT'){'Ask ChatGPT'}else{'New chat in ' + $ProjectName}
 $editor=Find-Composer $target.window $editorName
 if(-not (Check-NoAttachments $target.window)){throw 'Attachment exists; hold before typing'}
 if($AlreadyTyped){
  # Explicit manual recovery after positive evidence of no prior click.
  # Verify the exact existing text and leave it untouched. No keyboard
  # focus is needed for the later native UIA Send Invoke.
  $actual=$editor.GetCurrentPattern([System.Windows.Automation.ValuePattern]::Pattern).Current.Value.TrimEnd([char]13,[char]10)
  if($actual -cne $Message){throw 'Pretyped draft does not exactly match expected message'}
 }else{
  $pattern=$editor.GetCurrentPattern([System.Windows.Automation.ValuePattern]::Pattern)
  $actual=Read-ComposerText $editor $pattern.Current.Value
  if($actual -cne '' -or @(Find-EnabledSendButtons $target.window).Count){
   throw 'Composer is not verified empty; hold before typing'
  }
  Hold-IfOwnerPaused
  $pattern.SetValue($Message)
 }
 $typed=''
 for($i=0;$i -lt 25;$i++){
  Start-Sleep -Milliseconds 100
  $typed=$editor.GetCurrentPattern([System.Windows.Automation.ValuePattern]::Pattern).Current.Value
  if($typed.TrimEnd([char]13,[char]10) -ceq $Message){break}
 }
 if($typed.TrimEnd([char]13,[char]10) -cne $Message){
  throw ('Exact typed prompt readback failed; observed_len=' + $typed.Length + ', expected_len=' + $Message.Length + '; do not Send')
 }
 $sendButtons=@(Find-EnabledSendButtons $target.window)
 if($sendButtons.Count -ne 1){throw 'Send button not unique and enabled'}
 # ONE and only one UIA Send. Native Invoke acts on the already verified
 # target control and does not depend on whichever window is in foreground.
 # If acknowledgement is lost, reconcile; never click again automatically.
 $send = $sendButtons[0].GetCurrentPattern([System.Windows.Automation.InvokePattern]::Pattern)
 Hold-IfOwnerPaused
 $send.Invoke()
 if($L09Fault -eq 'after_click'){
  throw 'L09 injected after single click before acknowledgement; reconcile, never retry blindly'
 }
 for($i=0;$i -lt 60;$i++){
  Start-Sleep -Milliseconds 400
  $url=Get-Address $target.window
  $chat=Chat-FromUrl $url
  if($chat -and (Check-Project $url) -and (Find-PostedMessage $target.window $Message)){
   @{project=$ProjectId;chat_id=$chat;submitted_text=$Message;posted_message_observed=$true;window_handle=$WindowHandle} | ConvertTo-Json -Compress
   exit 0
  }
 }
 throw 'Send attempted but exact posted message + saved ID not both observed'
}
if($Mode -eq 'Reconcile') {
 $target=Get-TargetWindow '' $WindowHandle
 $chat=Chat-FromUrl (Get-Address $target.window)
 $posted= $chat -and (Find-PostedMessage $target.window $Message)
 @{project=$ProjectId;chat_id=$chat;submitted_text=$(if($posted){$Message}else{$null});posted_message_observed=[bool]$posted} | ConvertTo-Json -Compress
 exit 0
}
throw 'Unknown mode'
