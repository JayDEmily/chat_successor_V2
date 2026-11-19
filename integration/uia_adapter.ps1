# Astra UIA adapter. One browser actor. Never invoke -Mode Send without a persisted
# reference-controller 'sending' state. No automatic retries or reset.
[CmdletBinding()]
param(
 [Parameter(Mandatory=$true)][ValidateSet('ResolveProject','Observe','ObserveReentry','Prepare','Send','Reconcile')][string]$Mode,
 [string]$ProjectId = '',
 [Parameter(Mandatory=$true)][string]$ProjectName,
 [string]$ProjectUrl = '',
 [string]$ChatId = '',
 [ValidateSet('CONTINUE_CURRENT','LAUNCH_SUCCESSOR')][string]$Kind = 'CONTINUE_CURRENT',
 [long]$WindowHandle = 0,
 [string]$Message = '',
 [string]$OwnerAnchor = '',
 [string]$SourceResponse = '',
 [string]$PrepareAction = '',
 [string]$PrepareTargetPath = '',
 [string]$L09Fault = '',
 [string]$PausePath = '',
 [string]$ChromeExe = 'C:\Program Files\Google\Chrome\Application\chrome.exe',
 [switch]$AlreadyTyped
)
Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
# The detached Python controller reads JSON as UTF-8.
[Console]::OutputEncoding = [System.Text.UTF8Encoding]::new($false)
Add-Type -AssemblyName UIAutomationClient
Add-Type -AssemblyName UIAutomationTypes
if($Mode -ne 'ResolveProject' -and -not $ProjectId){throw 'Nominated Project ID required'}

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
function Open-ChromeWindow([string]$url) {
 if(-not (Test-Path -LiteralPath $ChromeExe -PathType Leaf)){throw 'Chrome executable missing'}
 # Each Chat Succession launch must observe its own new window handle.
 $mutex=[System.Threading.Mutex]::new($false,'Local\ChatSuccession.OpenChromeWindow')
 $acquired=$false
 try {
  try {$acquired=$mutex.WaitOne(30000)}
  catch [System.Threading.AbandonedMutexException] {$acquired=$true}
  if(-not $acquired){throw 'Timed out waiting to open a Chrome window'}
  $before=@((Get-ChromeWindows) | ForEach-Object {$_.Current.NativeWindowHandle})
  Start-Process -FilePath $ChromeExe -ArgumentList @('--new-window',$url)
  for($i=0;$i -lt 50;$i++){
   Start-Sleep -Milliseconds 400
   $candidates=@((Get-ChromeWindows) | Where-Object {$before -notcontains $_.Current.NativeWindowHandle})
   if($candidates.Count -gt 1){throw 'Ambiguous new Chrome windows'}
   if($candidates.Count -eq 1){return $candidates[0]}
  }
  throw 'Fresh Chrome window was not uniquely observed'
 } finally {
  if($acquired){$mutex.ReleaseMutex()}
  $mutex.Dispose()
 }
}
function Get-Address($window) {
 foreach($el in (Desc $window)) {
  try {
   if($el.Current.ControlType -eq [System.Windows.Automation.ControlType]::Edit -and
      $el.Current.Name -eq 'Address and search bar') {
    $v=$el.GetCurrentPattern([System.Windows.Automation.ValuePattern]::Pattern).Current.Value
    if($v -match '^chatgpt[.]com(?:/|$)') {return 'https://' + $v}
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
function Find-PostedMessage($window,$expected,[string]$afterResponse='') {
 # Only text under a user turn is a posted message. The assistant may quote
 # the exact continuation string. A repeated continuation also needs a user
 # turn after the specific assistant response that triggered this action.
 $afterOrdinal=0
 if($afterResponse){
  if($afterResponse -cnotmatch '^uia-turn-([1-9][0-9]*)-[a-f0-9]{20}$'){return $false}
  $afterOrdinal=[int]$Matches[1]
 }
 $all=Desc $window
 $assistantCount=0
 $anchorSeen=($afterOrdinal -eq 0)
 $inUserTurn=$false
 $latestUserMatches=$false
 for($i=0;$i -lt $all.Count;$i++) {
  $el=$all[$i]
  try{
   if($el.Current.ControlType -ne [System.Windows.Automation.ControlType]::Text){continue}
   $name=$el.Current.Name
   if($name -ceq 'You said:'){
    $inUserTurn=$anchorSeen
    $latestUserMatches=$false
   }elseif($name -ceq 'ChatGPT said:'){
    $inUserTurn=$false
    $assistantCount++
    if($afterOrdinal -gt 0){
     $anchorSeen=($assistantCount -eq $afterOrdinal -and
        (Read-AssistantContent $all $i $assistantCount).response_id -ceq $afterResponse)
    }
   }elseif($inUserTurn -and $name -ceq $expected){
    $latestUserMatches=$true
   }
  }catch{}
 }
 return $latestUserMatches
}

if($Mode -eq 'ResolveProject') {
 $window=Open-ChromeWindow 'https://chatgpt.com/'
 $resolutionWindow=$window.GetCurrentPattern([System.Windows.Automation.WindowPattern]::Pattern)
 try {
 for($i=0;$i -lt 25;$i++){
  if((Get-Address $window) -match '^https://chatgpt[.]com(?:/|$)'){
   $items=Desc $window
   $lists=@($items | Where-Object {
    $_.Current.ControlType -eq [System.Windows.Automation.ControlType]::List -and
    $_.Current.Name -ieq ('Chats in ' + $ProjectName)
   })
   if($lists.Count -gt 1){throw 'The Project name matched multiple sidebar lists'}
   if($lists.Count -eq 0){
    $sections=@($items | Where-Object {
     $_.Current.ControlType -eq [System.Windows.Automation.ControlType]::Button -and
     $_.Current.Name -ceq 'Projects'
    })
    $expand=$null
    if($sections.Count -eq 1 -and $sections[0].TryGetCurrentPattern(
       [System.Windows.Automation.ExpandCollapsePattern]::Pattern,[ref]$expand) -and
       $expand.Current.ExpandCollapseState -eq [System.Windows.Automation.ExpandCollapseState]::Collapsed){
     $expand.Expand()
    }
   }
   if($lists.Count -eq 1){
    $list=$lists[0]
    $name=$list.Current.Name.Substring(9)
    # Read the link address so a status lookup cannot open a second worker view.
    foreach($item in (Desc $list)){
     $address=$null
     if($item.Current.ControlType -eq [System.Windows.Automation.ControlType]::Hyperlink -and
        $item.Current.IsEnabled -and
        $item.TryGetCurrentPattern([System.Windows.Automation.ValuePattern]::Pattern,[ref]$address) -and
        $address.Current.Value -match '^(https://chatgpt[.]com/g/(g-p-[a-f0-9]+)(?:-[A-Za-z0-9-]+)?)/c/[A-Za-z0-9_-]+(?:[/?#]|$)'){
      @{project=$Matches[2];project_name=$name;project_url=($Matches[1]+'/project')} | ConvertTo-Json -Compress
      exit 0
     }
    }
   }
  }
  Start-Sleep -Milliseconds 400
 }
 throw 'Could not read a saved chat address in the exact Project sidebar list'
 } finally {$resolutionWindow.Close()}
}

function Test-AssistantProse($element) {
 $walker=[System.Windows.Automation.TreeWalker]::RawViewWalker
 $paragraph=$false
 $renderer=$false
 for($i=0;$i -lt 24 -and $null -ne $element;$i++){
  $kind=$element.Current.LocalizedControlType
  $class=$element.Current.ClassName
  if($kind -match 'code|quote|tool' -or $class -match 'codeblock|inlinecode|block.?quote|tool-output|(?:^|\s)(?:pre|code)(?:\s|$)'){
   return $false
  }
  if($kind -eq 'paragraph' -or
     ($class -match '(?:^|\s)TextBase-\w+' -and $class -match '(?:^|\s)Text-\w+')){$paragraph=$true}
  if($class -match '(?:^|\s)(?:markdown(?:\s|$)|Renderer-\w+)'){$renderer=$true}
  if($kind -eq 'region' -and $class -match '(?:^|\s)thread-scroll-container(?:\s|$)'){
   return ($paragraph -and $renderer)
  }
  $element=$walker.GetParent($element)
 }
 return $false
}

function Compare-OwnerTurn($turn,[string]$anchor) {
 if($turn.stop_control -or $turn.user_after_assistant){return 'advanced'}
 if(-not $turn.ready -or -not $turn.user_turn_seen){return 'unknown'}
 if($turn.response_id -ceq $anchor){return 'idle'}
 if($anchor -cmatch '^uia-turn-(\d+)-([a-f0-9]+)$'){
  $count=[int]$Matches[1]
  $digest=$Matches[2]
  if($turn.response_id -cmatch '^uia-turn-(\d+)-([a-f0-9]+)$' -and
     [int]$Matches[1] -gt $count -and $Matches[2] -cne $digest){return 'advanced'}
 }
 return 'unknown'
}

function Read-AssistantContent($all,[int]$header,[int]$ordinal) {
 $parts=@()
 $locatorProse=$false
 $finalProse=$false
 for($i=$header+1;$i -lt $all.Count;$i++){
  $el=$all[$i]
  try {
   if($el.Current.ControlType -eq [System.Windows.Automation.ControlType]::Text) {
    $name=$el.Current.Name
    if($name -ceq 'You said:' -or $name -ceq 'ChatGPT said:' -or
       $name -ceq 'ChatGPT can make mistakes. Check important info.' -or
       $name -ceq 'Latest response' -or $name -ceq 'Ask ChatGPT'){break}
    if($name){
     $parts+= $name
     if($name -cmatch '^CHAT_HANDOFF_BRANCH: '){$locatorProse=Test-AssistantProse $el}
     if($name -ceq 'CHAT_STATUS: TASK_COMPLETE'){$finalProse=Test-AssistantProse $el}
    }
   }
  }catch{}
 }
 $body=$parts -join [Environment]::NewLine
 $sha=[Security.Cryptography.SHA256]::Create()
 try{$digest=[BitConverter]::ToString($sha.ComputeHash([Text.Encoding]::UTF8.GetBytes($body))).Replace('-','').ToLowerInvariant()}finally{$sha.Dispose()}
 $final=if($parts.Count){$parts[-1]}else{''}
 return @{text=$body;final=$final;response_id=('uia-turn-' + $ordinal + '-' + $digest.Substring(0,20))
          handoff_locator_verified=($locatorProse -and $finalProse)}
}

function Read-CurrentTurn($target) {
 $all=Desc $target.window
 $last=-1
 $lastUser=-1
 $assistantCount=0
 $stop=$false
 for($i=0;$i -lt $all.Count;$i++){
  $el=$all[$i]
  try{
   if($el.Current.ControlType -eq [System.Windows.Automation.ControlType]::Text -and
      $el.Current.Name -ceq 'ChatGPT said:'){$assistantCount++;$last=$i}
   if($el.Current.ControlType -eq [System.Windows.Automation.ControlType]::Text -and
      $el.Current.Name -ceq 'You said:'){$lastUser=$i}
   if($el.Current.ControlType -eq [System.Windows.Automation.ControlType]::Button -and
      $el.Current.Name -ceq 'Stop' -and $el.Current.IsEnabled){$stop=$true}
  }catch{}
 }
 if($last -lt 0){
  return @{ready=$false;reason='No assistant turn observed';chat_id=$target.chat
           stop_control=$stop;user_after_assistant=$false;user_turn_seen=$false}
 }
 $content=Read-AssistantContent $all $last $assistantCount
 # No automatic turn completion until a final status line and no active Stop.
 $terminal=($content.final -cmatch '^(?:CHAT_STATUS: )?(?:NEED_MORE_TIME|TASK_COMPLETE|ERROR)$')
 $ready=$terminal -and -not $stop -and $last -gt $lastUser
 return @{
  ready=$ready;chat_id=$target.chat;project=$ProjectId;role='assistant'
  response_id=$content.response_id
  text=$content.text;complete=$ready;reason=$(if($stop){'Streaming/Stop control present'}elseif(-not $terminal){'No final standalone status leaf'}else{'Completed marker candidate; UIA hierarchy validation pending'})
  method='UIA_ACCESSIBILITY_TEXT';stop_control=$stop
  user_after_assistant=($lastUser -gt $last);user_turn_seen=($lastUser -ge 0)
  handoff_locator_verified=$content.handoff_locator_verified
 }
}

function Get-ProjectNavigation($source) {
 $links=@(foreach($el in (Desc $source.window)){
  if($el.Current.ControlType -ne [System.Windows.Automation.ControlType]::Hyperlink -or
     $el.Current.Name -cne $ProjectName -or $el.Current.IsOffscreen -or -not $el.Current.IsEnabled){continue}
  $linkValue=$null
  $invoke=$null
  if($el.TryGetCurrentPattern([System.Windows.Automation.ValuePattern]::Pattern,[ref]$linkValue) -and
     (Check-Project $linkValue.Current.Value) -and $linkValue.Current.Value -cmatch '/project$' -and
     $el.TryGetCurrentPattern([System.Windows.Automation.InvokePattern]::Pattern,[ref]$invoke)){$invoke}
 })
 if($links.Count -eq 1){return $links[0]}
 return $null
}

function Test-SourceComposerForNavigation($source) {
 $turn=Read-CurrentTurn $source
 if(-not $turn.ready -or $turn.response_id -cne $SourceResponse){
  throw 'The saved worker no longer shows the verified completion for this successor'
 }
 $editor=Find-Composer $source.window 'Ask ChatGPT'
 $value=$editor.GetCurrentPattern([System.Windows.Automation.ValuePattern]::Pattern).Current.Value
 return ((Read-ComposerText $editor $value) -ceq '' -and (Check-NoAttachments $source.window) -and
         @(Find-EnabledSendButtons $source.window).Count -eq 0)
}

function Save-NavigationTarget($source) {
 $record=@{kind='LAUNCH_SUCCESSOR';source=$ChatId;handle=[long]$source.window.Current.NativeWindowHandle
           action_id=$PrepareAction} | ConvertTo-Json -Compress
 $temp=$PrepareTargetPath + '.' + [guid]::NewGuid().ToString('N') + '.tmp'
 try {
  $bytes=[Text.Encoding]::UTF8.GetBytes($record)
  $stream=[IO.File]::Open($temp,[IO.FileMode]::CreateNew,[IO.FileAccess]::Write)
  try {$stream.Write($bytes,0,$bytes.Length);$stream.Flush($true)} finally {$stream.Dispose()}
  if([IO.File]::Exists($PrepareTargetPath)){[IO.File]::Replace($temp,$PrepareTargetPath,[NullString]::Value)}
  else{[IO.File]::Move($temp,$PrepareTargetPath)}
 } finally {
  if([IO.File]::Exists($temp)){[IO.File]::Delete($temp)}
 }
}

if($Mode -eq 'Observe') {
 if(-not $ChatId){throw 'Observe needs a known saved chat ID'}
 Read-CurrentTurn (Get-TargetWindow $ChatId 0) | ConvertTo-Json -Compress -Depth 5
 exit 0
}

if($Mode -eq 'ObserveReentry') {
 if(-not $ChatId -or -not $OwnerAnchor){throw 'Owner re-entry needs a saved worker and hold anchor'}
 $existing=Get-TargetWindow $ChatId 0
 $turn=Read-CurrentTurn $existing
 if($turn.stop_control -or $turn.user_after_assistant){
  @{disposition='advanced';project=$ProjectId;chat_id=$ChatId} | ConvertTo-Json -Compress
  exit 0
 }
 $editor=Find-Composer $existing.window 'Ask ChatGPT'
 $value=$editor.GetCurrentPattern([System.Windows.Automation.ValuePattern]::Pattern).Current.Value
 if((Read-ComposerText $editor $value) -cne '' -or -not (Check-NoAttachments $existing.window) -or
    @(Find-EnabledSendButtons $existing.window).Count){throw 'Re-entry held to preserve the existing draft or attachments'}
 $fresh=Open-ChromeWindow $existing.url
 $freshHandle=$fresh.Current.NativeWindowHandle
 $windowPattern=$fresh.GetCurrentPattern([System.Windows.Automation.WindowPattern]::Pattern)
 $verdict=$null
 try {
  for($i=0;$i -lt 25;$i++){
   Start-Sleep -Milliseconds 400
   try {$target=Get-TargetWindow $ChatId $freshHandle} catch {continue}
   $snapshot=Read-CurrentTurn $target
   $comparison=Compare-OwnerTurn $snapshot $OwnerAnchor
   if($comparison -eq 'advanced'){
    $verdict='advanced'
    break
   }
   if($comparison -eq 'idle'){
    $freshEditor=Find-Composer $target.window 'Ask ChatGPT'
    $freshValue=$freshEditor.GetCurrentPattern([System.Windows.Automation.ValuePattern]::Pattern).Current.Value
    if((Read-ComposerText $freshEditor $freshValue) -cne '' -or
       -not (Check-NoAttachments $target.window) -or @(Find-EnabledSendButtons $target.window).Count){
     throw 'Fresh re-entry view has an existing draft, attachments or unknown composer'
    }
    $verdict='idle'
    break
   }
  }
 } finally {$windowPattern.Close()}
 if(-not $verdict){throw 'A fresh view of the exact held worker could not be verified'}
 if($verdict -eq 'advanced'){
  # Refresh only the same desktop view and only while its composer is empty.
  $editor=Find-Composer $existing.window 'Ask ChatGPT'
  $value=$editor.GetCurrentPattern([System.Windows.Automation.ValuePattern]::Pattern).Current.Value
  if((Read-ComposerText $editor $value) -cne '' -or -not (Check-NoAttachments $existing.window)){
   throw 'The current worker advanced but the desktop view contains a draft or attachment'
  }
  $reload=@((Desc $existing.window) | Where-Object {
   $_.Current.ControlType -eq [System.Windows.Automation.ControlType]::Button -and
   $_.Current.Name -cmatch '^Reload(?: this page)?$'
  })
  if($reload.Count -ne 1){throw 'The worker advanced but Chrome reload was not uniquely available'}
  $reload[0].GetCurrentPattern([System.Windows.Automation.InvokePattern]::Pattern).Invoke()
 }
 @{disposition=$verdict;project=$ProjectId;chat_id=$ChatId} | ConvertTo-Json -Compress
 exit 0
}

if($Mode -eq 'Prepare') {
 if($Kind -eq 'CONTINUE_CURRENT') {
  if(-not $ChatId){throw 'Continuation needs current saved chat'}
  $target=Get-TargetWindow $ChatId 0
  $editor=Find-Composer $target.window 'Ask ChatGPT'
 }else{
  # In this Chrome installation the Project-specific sidebar control
  # was found but remained offscreen after ScrollIntoView. Reuse the observed
  # authenticated /project URL instead; never construct or guess a Project URL.
   if($ProjectUrl){
    if(-not (Check-Project $ProjectUrl) -or $ProjectUrl -cnotmatch '/project$'){
     throw 'Configured Project URL does not match the nominated Project landing page'
    }
    $projectPage=$ProjectUrl
   }else{
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
    $projectPage=$uniquePages[0]
   }
  $new=$null
  if($ChatId -and $WindowHandle -gt 0){
   try {
    $prepared=Get-TargetWindow '' $WindowHandle
    if($null -eq $prepared.chat -and $prepared.url -cmatch '/project$'){
     $new=$prepared.window
    }
   }catch{}
  }
  if($ChatId -and $SourceResponse -and $PrepareAction -and $PrepareTargetPath -and $null -eq $new){
   $source=$null
   $navigation=$null
   try {
    $source=Get-TargetWindow $ChatId 0
    $navigation=Get-ProjectNavigation $source
   }catch{}
   if($null -ne $navigation -and (Test-SourceComposerForNavigation $source)){
    # The prior worker is saved. Follow its verified Project link in-place
    # so a new chat does not require a new Chrome renderer.
    Save-NavigationTarget $source
    $navigation.Invoke()
    $new=$source.window
   }
  }
  if($null -eq $new){$new=Open-ChromeWindow $projectPage}
  $target=$null
  for($i=0;$i -lt 50;$i++){
   Start-Sleep -Milliseconds 400
   $url=Get-Address $new
   if((Check-Project $url) -and $url -cmatch '/project$'){
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

function Hold-ForChangedDestination {
 @{destination_changed_before_click=$true} | ConvertTo-Json -Compress
 exit 0
}

if($Mode -eq 'Send') {
 Hold-IfOwnerPaused
 if($WindowHandle -le 0){throw 'Saved prepared window handle required'}
 if($Message -cnotmatch '^[A-Za-z0-9 .,/_:-]+$'){throw 'Unsupported message characters'}
 if(-not $Message){throw 'Empty message'}
 if($Kind -eq 'CONTINUE_CURRENT' -and
    (-not $ChatId -or $SourceResponse -cnotmatch '^uia-turn-[1-9][0-9]*-[a-f0-9]{20}$')){
  throw 'Continuation needs the saved chat and triggering response'
 }
 $target=Get-TargetWindow $(if($Kind -eq 'CONTINUE_CURRENT'){$ChatId}else{''}) $WindowHandle
 if($Kind -eq 'CONTINUE_CURRENT'){
  $turn=Read-CurrentTurn $target
  $comparison=Compare-OwnerTurn $turn $SourceResponse
  if($comparison -eq 'advanced'){
   @{worker_advanced_before_click=$true} | ConvertTo-Json -Compress
   exit 0
  }
  if($comparison -ne 'idle'){
   throw 'Triggering assistant response could not be confirmed before typing'
  }
 }
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
  if((Get-Address $target.window) -cne $target.url){Hold-ForChangedDestination}
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
 Hold-IfOwnerPaused
 if($Kind -eq 'CONTINUE_CURRENT'){
  $turn=Read-CurrentTurn $target
  $comparison=Compare-OwnerTurn $turn $SourceResponse
  if($comparison -eq 'advanced'){
   @{worker_advanced_before_click=$true} | ConvertTo-Json -Compress
   exit 0
  }
  if($comparison -ne 'idle'){
   throw 'The triggering response could not be verified after typing. Preserve the composer and reconcile.'
  }
 }
 # Bind the button to the same document as the exact verified composer. A
 # tab switch after typing must not select the new tab's Send button.
 try {
  $liveEditor=Find-Composer $target.window $editorName
  $liveValue=$liveEditor.GetCurrentPattern([System.Windows.Automation.ValuePattern]::Pattern).Current.Value
  if(-not [System.Windows.Automation.Automation]::Compare($editor,$liveEditor) -or
     $liveValue.TrimEnd([char]13,[char]10) -cne $Message -or
     -not (Check-NoAttachments $target.window)){Hold-ForChangedDestination}
  $walker=[System.Windows.Automation.TreeWalker]::RawViewWalker
  $document=$walker.GetParent($liveEditor)
  while($null -ne $document -and $document.Current.ControlType -ne [System.Windows.Automation.ControlType]::Document){
   $document=$walker.GetParent($document)
  }
  if($null -eq $document){Hold-ForChangedDestination}
  $sendButtons=@(Find-EnabledSendButtons $document)
  if($sendButtons.Count -ne 1){Hold-ForChangedDestination}
  $send=$sendButtons[0].GetCurrentPattern([System.Windows.Automation.InvokePattern]::Pattern)
  if((Get-Address $target.window) -cne $target.url){Hold-ForChangedDestination}
 } catch {Hold-ForChangedDestination}
 Hold-IfOwnerPaused
 # One native UIA Invoke. Reconcile if its acknowledgement is lost.
 $send.Invoke()
 if($L09Fault -eq 'after_click'){
  throw 'L09 injected after single click before acknowledgement; reconcile, never retry blindly'
 }
 for($i=0;$i -lt 60;$i++){
  Start-Sleep -Milliseconds 400
  $url=Get-Address $target.window
  $chat=Chat-FromUrl $url
  if($chat -and (Check-Project $url) -and ($Kind -ne 'CONTINUE_CURRENT' -or $chat -ceq $ChatId) -and
     (Find-PostedMessage $target.window $Message $SourceResponse)){
   @{project=$ProjectId;chat_id=$chat;submitted_text=$Message;posted_message_observed=$true;window_handle=$WindowHandle} | ConvertTo-Json -Compress
   exit 0
  }
 }
 throw 'Send attempted but exact posted message + saved ID not both observed'
}
if($Mode -eq 'Reconcile') {
 if($Kind -eq 'CONTINUE_CURRENT' -and -not ($ChatId -and $SourceResponse)){
  throw 'Reconcile needs the saved chat and triggering response'
 }
 $target=Get-TargetWindow $(if($Kind -eq 'CONTINUE_CURRENT'){$ChatId}else{''}) $WindowHandle
 $chat=Chat-FromUrl (Get-Address $target.window)
 $posted= $chat -and ($Kind -ne 'CONTINUE_CURRENT' -or $chat -ceq $ChatId) -and
          (Find-PostedMessage $target.window $Message $SourceResponse)
 @{project=$ProjectId;chat_id=$chat;submitted_text=$(if($posted){$Message}else{$null});posted_message_observed=[bool]$posted} | ConvertTo-Json -Compress
 exit 0
}
throw 'Unknown mode'
