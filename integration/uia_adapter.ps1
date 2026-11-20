# Astra UIA adapter. One browser actor. Never invoke -Mode Send without a persisted
# reference-controller 'sending' state. No automatic retries or reset.
[CmdletBinding()]
param(
 [Parameter(Mandatory=$true)][ValidateSet('ResolveProject','Observe','ObserveReentry','RecoverView','Prepare','Send','Reconcile')][string]$Mode,
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
 [string]$BootstrapIntentPath = '',
 [string]$BootstrapActionId = '',
 [string]$RouteReceipt = '',
 [string]$PendingResponseId = '',
 [string]$BootstrapRunId = '',
 [string]$DocumentId = '',
 [string]$ChromeAppId = '',
 [string]$WorkerJournalPath = '',
 [string]$OwnerInputPath = '',
 [string]$L09Fault = '',
 [string]$PausePath = '',
 [ValidateSet('missing','stale')][string]$Recovery,
 [string]$ChromeExe = 'C:\Program Files\Google\Chrome\Application\chrome.exe',
 [switch]$AlreadyTyped,
 [switch]$Preflight
)
Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
# The detached Python controller reads JSON as UTF-8.
[Console]::OutputEncoding = [System.Text.UTF8Encoding]::new($false)
Add-Type -AssemblyName UIAutomationClient
Add-Type -AssemblyName UIAutomationTypes
if($ChromeAppId){Add-Type -Path (Join-Path $PSScriptRoot 'window_profile.cs')}
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
function Test-WindowProfile($window) {
 if(-not $ChromeAppId){return $true}
 try {
  $observed=[ChatSuccession.WindowProfile]::ReadAppId([IntPtr][long]$window.Current.NativeWindowHandle)
  return ($observed -ceq $ChromeAppId)
 }catch{return $false}
}
function Open-ChromeWindow([string]$url) {
 if(-not (Test-Path -LiteralPath $ChromeExe -PathType Leaf)){throw 'Chrome executable missing'}
 $launchArgs=@('--new-window',$url)
 if($env:CHAT_SUCCESSION_CHROME_PROFILE_PATH){
  $chromeProfileDirectory=Get-Item -LiteralPath $env:CHAT_SUCCESSION_CHROME_PROFILE_PATH
  if(-not $chromeProfileDirectory.PSIsContainer -or $null -eq $chromeProfileDirectory.Parent -or
     -not (Test-Path -LiteralPath (Join-Path $chromeProfileDirectory.Parent.FullName 'Local State') -PathType Leaf)){
   throw 'The nominated existing Chrome profile directory was not verified'
  }
  $launchArgs=@(('--user-data-dir="{0}"' -f $chromeProfileDirectory.Parent.FullName),
                ('--profile-directory="{0}"' -f $chromeProfileDirectory.Name)) + $launchArgs
 }
 # Each Chat Succession launch must observe its own new window handle.
 $mutex=[System.Threading.Mutex]::new($false,'Local\ChatSuccession.OpenChromeWindow')
 $acquired=$false
 try {
  try {$acquired=$mutex.WaitOne(30000)}
  catch [System.Threading.AbandonedMutexException] {$acquired=$true}
  if(-not $acquired){throw 'Timed out waiting to open a Chrome window'}
  $before=@((Get-ChromeWindows) | ForEach-Object {$_.Current.NativeWindowHandle})
  Start-Process -FilePath $ChromeExe -ArgumentList $launchArgs
  for($i=0;$i -lt 50;$i++){
   Start-Sleep -Milliseconds 400
   $candidates=@((Get-ChromeWindows) | Where-Object {$before -notcontains $_.Current.NativeWindowHandle})
   if($candidates.Count -gt 1){throw 'Ambiguous new Chrome windows'}
   if($candidates.Count -eq 1 -and (Test-WindowProfile $candidates[0])){return $candidates[0]}
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
 if($url -match ('^https://chatgpt[.]com/g/' + [regex]::Escape($ProjectId) + '(?:-[^/]+)?/c/([a-f0-9]{8}(?:-[a-f0-9]{4}){3}-[a-f0-9]{12})(?:[/?#]|$)')) {
  return $Matches[1]
 }
 return $null
}
function Find-TargetWindows([string]$expectedChat,[long]$handle) {
 $targets=@()
 $wrongProfile=$false
 foreach($w in (Get-ChromeWindows)) {
  try{
   if($handle -ne 0 -and $w.Current.NativeWindowHandle -ne $handle){continue}
   $url=Get-Address $w
   if(-not (Check-Project $url)){continue}
   $chat=Chat-FromUrl $url
   if($expectedChat -and $chat -cne $expectedChat){continue}
   if(Test-WindowProfile $w){$targets+= @{window=$w;url=$url;chat=$chat}}
   else{$wrongProfile=$true}
  }catch{}
 }
 if($wrongProfile -and $targets.Count -eq 0){throw 'Target Chrome window profile could not be verified'}
 return $targets
}
function Get-TargetWindow([string]$expectedChat,[long]$handle) {
 $hits=@(Find-TargetWindows $expectedChat $handle)
 if($hits.Count -ne 1){throw ('Expected exactly one active Project target, found ' + $hits.Count)}
 return $hits[0]
}
function Get-ObservableSavedTarget {
 $hits=@(Find-TargetWindows $ChatId 0)
 if($hits.Count -ne 1){
  $status=if($hits.Count -eq 0){'missing'}else{'ambiguous'}
  return @{view_status=$status;project=$ProjectId;chat_id=$ChatId;ready=$false}
 }
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
function Get-ComposerDocument($editor) {
 $walker=[System.Windows.Automation.TreeWalker]::RawViewWalker
 $document=$walker.GetParent($editor)
 while($null -ne $document -and $document.Current.ControlType -ne [System.Windows.Automation.ControlType]::Document){
  $document=$walker.GetParent($document)
 }
 if($null -eq $document){throw 'Composer document could not be observed'}
 return $document
}
function Get-DocumentIdentity($document) {
 $identity=$document.GetRuntimeId() -join '.'
 if(-not $identity){throw 'Composer document identity could not be observed'}
 return $identity
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
function Get-AccessibilityParent($element) {
 return [System.Windows.Automation.TreeWalker]::RawViewWalker.GetParent($element)
}

function Get-AccessibilityChildren($element) {
 $walker=[System.Windows.Automation.TreeWalker]::RawViewWalker
 for($child=$walker.GetFirstChild($element);$null -ne $child;$child=$walker.GetNextSibling($child)){
  $child
 }
}

function Test-TranscriptRegion($element) {
 $current=$element.Current
 return ($current.LocalizedControlType -eq 'region' -and
         $current.ClassName -match '(?:^|\s)thread-scroll-container(?:\s|$)')
}

function Get-ConversationRole($element) {
 $name=$element.Current.Name
 if($name -cnotin @('You said:','ChatGPT said:')){return}
 $heading=$null
 # Only the application's role heading establishes a turn. Identical text
 # in a message body remains content.
 for($i=0;$i -lt 24 -and $null -ne $element;$i++){
  $current=$element.Current
  if($current.LocalizedControlType -eq 'heading' -and
     $current.ClassName -match '(?:^|\s)sr-only(?:\s|$)' -and $current.Name -ceq $name){
   $heading=$element
  }
  if($current.LocalizedControlType -eq 'article'){
   if(-not $heading){return}
   $id=$element.GetRuntimeId() -join '.'
   $headingId=$heading.GetRuntimeId() -join '.'
   if(-not $id -or -not $headingId){throw 'Conversation article or heading identity unavailable'}
   return @{article=$element; id=$id; heading_id=$headingId
            role=$(if($name -ceq 'You said:'){'user'}else{'assistant'})}
  }
  $element=Get-AccessibilityParent $element
 }
 if($heading){throw 'Conversation role heading has no verified article'}
}

function Get-VirtualizedConversationTurns($thread) {
 # Chrome's visible-message groups do not expose absolute history ordinals.
 # Recognise only bounded, immediate heading/body pairs; never certify a
 # response/Send receipt from this view without a separately proven history.
 $layouts=@((Get-AccessibilityChildren $thread) | Where-Object {
  $_.Current.LocalizedControlType -ceq 'group' -and
  $_.Current.ClassName -cmatch '(?:^|\s)transcriptContent-[\w-]+(?:\s|$)'
 })
 if($layouts.Count -ne 1){throw 'Virtualized transcript layout is not unique'}
 $wrappers=@(Get-AccessibilityChildren $layouts[0])
 if($wrappers.Count -ne 1 -or $wrappers[0].Current.LocalizedControlType -cne 'group' -or
    $wrappers[0].Current.ClassName -cne 'relative shrink-0'){
  throw 'Virtualized transcript message wrapper is unverified'
 }
 $children=@(Get-AccessibilityChildren $wrappers[0])
 $turns=@()
 for($i=0;$i -lt $children.Count;$i++){
  $current=$children[$i].Current
  if($current.LocalizedControlType -ceq 'heading' -and
     $current.Name -cin @('You said:','ChatGPT said:')){
   if($current.ClassName -cnotmatch '(?:^|\s)sr-only(?:\s|$)' -or
      $i+1 -ge $children.Count){throw 'Virtualized role heading is unpaired'}
   $role=if($current.Name -ceq 'You said:'){'user'}else{'assistant'}
   $body=$children[$i+1]
   $bodyCurrent=$body.Current
   if($bodyCurrent.LocalizedControlType -cne 'group'){throw 'Virtualized role has no direct body group'}
   if($role -ceq 'user'){
    if($bodyCurrent.ClassName -cnotmatch '(?:^|\s)bg-user-message(?:\s|$)' -or
       $bodyCurrent.ClassName -cnotmatch '(?:^|\s)text-user-message(?:\s|$)'){
     throw 'Virtualized user body is not verified'
    }
   }elseif($bodyCurrent.ClassName -cnotmatch '(?:^|\s)Renderer-[\w-]+(?:\s|$)'){
    throw 'Virtualized assistant renderer is not verified'
   }
   $nestedHeadings=@((Desc $body) | Where-Object {
    $_.Current.LocalizedControlType -ceq 'heading' -and
    $_.Current.ClassName -cmatch '(?:^|\s)sr-only(?:\s|$)' -and
    $_.Current.Name -cin @('You said:','ChatGPT said:')
   })
   if($nestedHeadings.Count){throw 'Nested virtualized application role heading'}
   if($turns.Count -and $turns[-1].role -ceq $role){
    throw 'Consecutive virtualized headings have the same role'
   }
   $turns+=@{role=$role;article=$body;virtualized=$true}
   $i++
   continue
  }
  if(($current.LocalizedControlType -ceq 'heading' -and
      $current.ClassName -cmatch '(?:^|\s)sr-only(?:\s|$)') -or
     ($current.LocalizedControlType -ceq 'group' -and
      $current.ClassName -cmatch '(?:^|\s)(?:Renderer-[\w-]+|bg-user-message)(?:\s|$)')){
   throw 'Unpaired virtualized heading or message body'
  }
  if($current.LocalizedControlType -cnotin @('separator','button','toggle button','group')){
   throw 'Unexpected virtualized transcript sibling'
  }
  $buriedHeadings=@((Desc $children[$i]) | Where-Object {
   $_.Current.LocalizedControlType -ceq 'heading' -and
   $_.Current.ClassName -cmatch '(?:^|\s)sr-only(?:\s|$)'
  })
  if($buriedHeadings.Count){throw 'Unverified role heading outside message body'}
 }
 if(-not $turns.Count -or $turns[0].role -cne 'user'){
  throw 'Virtualized transcript has no verified leading user turn'
 }
 $turns
}

function Get-ConversationTurns($all) {
 $threads=@($all | Where-Object {Test-TranscriptRegion $_})
 if($threads.Count -ne 1){throw 'A single conversation transcript could not be established'}
 $descendants=@(Desc $threads[0])
 $articles=@($descendants | Where-Object {
  $_.Current.LocalizedControlType -ceq 'article'
 })
 if($articles.Count -eq 0){
  Get-VirtualizedConversationTurns $threads[0]
  return
 }
 # Article ancestors establish layout. Any other node outside an article
 # can hide a newer turn, regardless of its accessibility control type.
 foreach($element in $descendants){
  $insideArticle=$false
  for($node=$element;$null -ne $node;$node=Get-AccessibilityParent $node){
   if($node.Current.LocalizedControlType -ceq 'article'){$insideArticle=$true;break}
   if(Test-TranscriptRegion $node){break}
  }
  if($insideArticle){continue}
  $articleContainer=$false
  foreach($article in $articles){
   for($parent=Get-AccessibilityParent $article;$null -ne $parent;$parent=Get-AccessibilityParent $parent){
    if($parent -eq $element){$articleContainer=$true;break}
    if(Test-TranscriptRegion $parent){break}
   }
   if($articleContainer){break}
  }
  if(-not $articleContainer){throw 'Article transcript has an unverified non-article row'}
 }
 foreach($article in $articles){
  for($parent=Get-AccessibilityParent $article; $null -ne $parent; $parent=Get-AccessibilityParent $parent){
   if($parent.Current.LocalizedControlType -eq 'article' -or (Test-TranscriptRegion $parent)){break}
  }
  if($null -eq $parent){throw 'Conversation article left the transcript during observation'}
  if($parent.Current.LocalizedControlType -eq 'article'){continue}
  $id=$article.GetRuntimeId() -join '.'
  $verified=$null
  foreach($element in (Desc $article)){
   $turn=Get-ConversationRole $element
   if($null -eq $turn -or $turn.id -cne $id){continue}
   if($null -ne $verified -and ($verified.heading_id -cne $turn.heading_id -or
                                $verified.role -cne $turn.role)){
    throw 'Conversation article has multiple role headings'
   }
   $verified=$turn
  }
  if($null -eq $verified){throw 'Conversation article has no verified role heading'}
  $verified
 }
}

function Find-PostedMessage($window,$expected,[string]$afterResponse='',[string]$url='',[string]$pendingAnchor='') {
 # The complete latest user turn must match. For continuation, also bind
 # the immediately preceding assistant turn to the triggering response.
 try{
  $all=Desc $window
  if($url){
   $chat=Chat-FromUrl $url
   if(-not $chat -or -not (Check-Project $url)){return $false}
   $snapshot=Read-ChromeTurnSnapshot $all $chat
   if($null -ne $snapshot){
    if($pendingAnchor -and $pendingAnchor -cnotmatch '^chrome-turn-'){return $false}
    if($snapshot.phase -cne 'observed' -or $snapshot.user -cne $expected){return $false}
    if($afterResponse -and ($null -eq $snapshot.previous -or
       (Get-ChromeResponseId $snapshot.previous) -cne $afterResponse)){return $false}
    return ((Get-Address $window) -ceq $url -and (Test-WindowProfile $window))
   }
  }
  if($pendingAnchor -cmatch '^chrome-turn-'){return $false}
  $afterOrdinal=0
  if($afterResponse){
   if($afterResponse -cnotmatch '^uia-turn-([1-9][0-9]*)-[a-f0-9]{20}$'){return $false}
   $afterOrdinal=[int]$Matches[1]
  }
  $turns=@(Get-ConversationTurns $all)
  $lastUser=-1
  $assistantCount=0
  $userAnchorOrdinal=0
  for($i=0;$i -lt $turns.Count;$i++){
   if($turns[$i].role -ceq 'assistant'){$assistantCount++}
   else{$lastUser=$i;$userAnchorOrdinal=$assistantCount}
  }
  if($lastUser -lt 0 -or @($turns | Where-Object {$_.ContainsKey('virtualized') -and $_['virtualized']}).Count){return $false}
  if($afterOrdinal -gt 0 -and ($lastUser -eq 0 -or $userAnchorOrdinal -ne $afterOrdinal -or
     $turns[$lastUser-1].role -cne 'assistant' -or
     (Read-ConversationContent $turns[$lastUser-1] $afterOrdinal).response_id -cne $afterResponse)){
   return $false
  }
  return ((Read-ConversationContent $turns[$lastUser] 0).text -ceq $expected)
 }catch{return $false}
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
  if(Test-TranscriptRegion $element){
   return ($paragraph -and $renderer)
  }
  $element=$walker.GetParent($element)
 }
 return $false
}

function Compare-OwnerTurn($turn,[string]$anchor) {
 $chrome=$anchor -cmatch '^chrome-turn-'
 if($anchor -and ($chrome -ne ($turn['method'] -ceq 'CHROME_DOM'))){
  return 'unknown'
 }
 if($chrome){
  if($turn.ready -and $turn['response_id'] -ceq $anchor){return 'idle'}
  if($turn['previous_response_id'] -ceq $anchor){return 'advanced'}
  return 'unknown'
 }
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

function Read-ConversationContent($turn,[int]$ordinal) {
 $parts=@()
 $locatorProse=$false
 $finalProse=$false
 # Article membership bounds the body. Browser labels and role-like strings
 # inside that article cannot truncate it.
 foreach($el in (Desc $turn.article)){
  if($el.Current.ControlType -ne [System.Windows.Automation.ControlType]::Text){continue}
  $name=$el.Current.Name
  if(-not $name -or (-not $turn.ContainsKey('virtualized') -and (Get-ConversationRole $el))){continue}
  $parts+= $name
  $finalProse=$false
  if($turn.role -ceq 'assistant'){
   if($name -cmatch '^CHAT_HANDOFF_BRANCH: '){$locatorProse=Test-AssistantProse $el}
   if($name -cmatch '^(?:CHAT_STATUS: )?(?:NEED_MORE_TIME|TASK_COMPLETE|ERROR)$'){
    $finalProse=Test-AssistantProse $el
   }
  }
 }
 $body=$parts -join [Environment]::NewLine
 $sha=[Security.Cryptography.SHA256]::Create()
 try{$digest=[BitConverter]::ToString($sha.ComputeHash([Text.Encoding]::UTF8.GetBytes($body))).Replace('-','').ToLowerInvariant()}finally{$sha.Dispose()}
 $shortDigest=$digest.Substring(0,20)
 return @{text=$body;final_status_verified=$finalProse;response_id=('uia-turn-' + $ordinal + '-' + $shortDigest);digest=$shortDigest
          handoff_locator_verified=($locatorProse -and $finalProse)}
}

function Read-ChromeTurnSnapshot($all,[string]$expectedChat) {
 $readers=@($all | Where-Object {
  $_.Current.ControlType -eq [System.Windows.Automation.ControlType]::Edit -and
  $_.Current.Name -ceq 'Chat Succession Chrome readback' -and
  $_.Current.ClassName -ceq 'chat-succession-readback'
 })
 if($readers.Count -eq 0){return}
 if($readers.Count -ne 1 -or -not $ChromeAppId -or -not $expectedChat){
  throw 'Chrome readback is ambiguous or has no verified saved destination'
 }
 $value=$readers[0].GetCurrentPattern([System.Windows.Automation.ValuePattern]::Pattern).Current
 if(-not $value.IsReadOnly -or -not $value.Value){throw 'Chrome readback field is not ready'}
 try{$snapshot=$value.Value | ConvertFrom-Json}
 catch{throw 'Chrome readback field does not contain a complete observation'}
 if($snapshot.project -cne $ProjectId -or $snapshot.chat -cne $expectedChat){
  throw 'Chrome readback belongs to a different Project or saved chat'
 }
 if($snapshot.observedAt -isnot [long]){throw 'Chrome readback has no valid sample time'}
 $age=[DateTimeOffset]::UtcNow.ToUnixTimeMilliseconds() - $snapshot.observedAt
 if($age -lt 0 -or $age -gt 5000){throw 'Chrome readback sample has expired'}
 if($snapshot.phase -ceq 'observed' -and ($snapshot.user -isnot [string] -or -not $snapshot.user -or
    $snapshot.key -cnotmatch '^[a-f0-9]{8}(?:-[a-f0-9]{4}){3}-[a-f0-9]{12}$')){
  throw 'Chrome readback has no verified user turn'
 }
 return $snapshot
}

function Get-ChromeResponseId($snapshot) {
 $idPattern='^[a-f0-9]{8}(?:-[a-f0-9]{4}){3}-[a-f0-9]{12}$'
 if($snapshot.key -cnotmatch $idPattern -or $snapshot.reply.id -cnotmatch $idPattern){
  throw 'Chrome readback has no stable user or reply identity'
 }
 return ('chrome-turn-' + $snapshot.key + '-' + $snapshot.reply.id)
}

function Read-CurrentTurn($target,[switch]$IncludeUserAnchor) {
 $all=Desc $target.window
 $stop=$false
 foreach($el in $all){
  try{
   if($el.Current.ControlType -eq [System.Windows.Automation.ControlType]::Button -and
      $el.Current.Name -ceq 'Stop' -and $el.Current.IsEnabled){$stop=$true}
  }catch{}
 }
 if($target['url']){
  $snapshot=Read-ChromeTurnSnapshot $all $target.chat
  if($null -ne $snapshot){
   $observed=$snapshot.phase -ceq 'observed'
   if($snapshot.phase -cnotin @('observed','loading') -and -not $stop){
    throw 'Chrome readback could not establish the latest visible turn'
   }
   $reply=if($observed){$snapshot.reply}
   $ready=$null -ne $reply -and $reply.text -is [string] -and $reply.text -and
          $reply.final -is [bool] -and $reply.final -and -not $stop
   $result=@{
    ready=$ready;complete=$ready;role='assistant';chat_id=$target.chat;project=$ProjectId
    method='CHROME_DOM';chrome_read_at=$snapshot.observedAt;stop_control=$stop
    reason=$(if($ready){'Completed status observed in Chrome prose'}else{'Waiting for a completed Chrome reply'})
    response_id=$(if($null -ne $reply){Get-ChromeResponseId $snapshot})
    text=$(if($null -ne $reply){$reply.text}else{''})
    handoff_locator_verified=($ready -and $reply.handoff -is [bool] -and $reply.handoff)
    user_turn_seen=$observed;user_after_assistant=($observed -and $snapshot.userAfterAssistant -eq $true)
    previous_response_id=$(if($observed -and $null -ne $snapshot.previous){Get-ChromeResponseId $snapshot.previous})
   }
   if($IncludeUserAnchor){$result['assistant_turn_count']=$null;$result['user_turn_count']=$null}
   return $result
  }
 }
 try{$turns=@(Get-ConversationTurns $all)}
 catch{
  if(-not $stop){throw}
  return @{ready=$false;chat_id=$target.chat;stop_control=$true
           user_turn_seen=$false;user_after_assistant=$false
           reason='Streaming conversation structure is incomplete'}
 }
 $virtualized=@($turns | Where-Object {$_.ContainsKey('virtualized') -and $_['virtualized']}).Count -gt 0
 $assistant=@($turns | Where-Object {$_.role -ceq 'assistant'})
 $user=@($turns | Where-Object {$_.role -ceq 'user'})
 if(-not $assistant.Count){
  $turn=@{ready=$false;reason='No assistant turn observed';chat_id=$target.chat
          stop_control=$stop;user_after_assistant=$false;user_turn_seen=($user.Count -gt 0)}
 }else{
  $content=Read-ConversationContent $assistant[-1] $assistant.Count
  # No automatic turn completion until a final status line and no active Stop.
  $terminal=$content.final_status_verified
  $userAfter=$turns[-1].role -ceq 'user'
  $ready=$terminal -and -not $stop -and -not $userAfter -and -not $virtualized
  $turn=@{
   ready=$ready;chat_id=$target.chat;project=$ProjectId;role='assistant'
   response_id=$(if($virtualized){$null}else{$content.response_id})
   text=$(if($virtualized){''}else{$content.text});complete=$ready
   reason=$(if($virtualized){'Virtualized view lacks verified absolute turn identity'}elseif($stop){'Streaming/Stop control present'}elseif(-not $terminal){'No final status in verified assistant prose'}else{'Completed status observed in assistant prose'})
   method=$(if($virtualized){'UIA_VIRTUALIZED_UNQUALIFIED'}else{'UIA_ACCESSIBILITY_TEXT'});stop_control=$stop
   user_after_assistant=$userAfter;user_turn_seen=($user.Count -gt 0)
   handoff_locator_verified=$content.handoff_locator_verified
  }
 }
 if($IncludeUserAnchor){
  # Visible virtualized rows may omit prior user/assistant turns. Do not
  # infer absolute ordinals or a user anchor for the journal/stale timer.
  $turn['assistant_turn_count']=if($virtualized){$null}else{$assistant.Count}
  $turn['user_turn_count']=if($virtualized){$null}else{$user.Count}
  if($user.Count -and -not $virtualized){
   $lastUserContent=Read-ConversationContent $user[-1] $user.Count
   if($lastUserContent.text){$turn['latest_user_digest']=$lastUserContent.digest}
  }
 }
 return $turn
}

function Read-SavedWorkerView($target) {
 $null=Find-Composer $target.window 'Ask ChatGPT'
 $turn=Read-CurrentTurn $target -IncludeUserAnchor
 if(-not $turn.user_turn_seen -or (Get-Address $target.window) -cne $target.url){
  throw 'Exact saved worker conversation has not loaded'
 }
 return $turn
}

function Get-VirtualizedSavedUserHeading($document) {
 $threads=@((Desc $document) | Where-Object {Test-TranscriptRegion $_})
 if($threads.Count -ne 1){throw 'A single saved conversation transcript could not be established'}
 $layouts=@((Get-AccessibilityChildren $threads[0]) | Where-Object {
  $_.Current.LocalizedControlType -ceq 'group' -and
  $_.Current.ClassName -cmatch '(?:^|\s)transcriptContent-[\w-]+(?:\s|$)'
 })
 if($layouts.Count -eq 0){return}
 if($layouts.Count -ne 1){throw 'The saved conversation layout is ambiguous'}
 $groups=@(Get-AccessibilityChildren $layouts[0])
 if($groups.Count -ne 1 -or $groups[0].Current.LocalizedControlType -cne 'group' -or
    $groups[0].Current.ClassName -cne 'relative shrink-0'){
  throw 'The saved conversation message group could not be verified'
 }
 $children=@(Get-AccessibilityChildren $groups[0])
 for($i=0;$i+1 -lt $children.Count;$i++){
  $heading=$children[$i].Current
  $body=$children[$i+1].Current
  if($heading.LocalizedControlType -ceq 'heading' -and $heading.Name -ceq 'You said:' -and
     $heading.ClassName -cmatch '(?:^|\s)sr-only(?:\s|$)' -and
     $body.LocalizedControlType -ceq 'group' -and
     $body.ClassName -cmatch '(?:^|\s)bg-user-message(?:\s|$)' -and
     $body.ClassName -cmatch '(?:^|\s)text-user-message(?:\s|$)'){
   return $children[$i]
  }
 }
 throw 'A loaded user message could not be verified in the saved conversation'
}

function Read-SavedWorkerIdentity($target) {
 $document=Get-ComposerDocument (Find-Composer $target.window 'Ask ChatGPT')
 $heading=Get-VirtualizedSavedUserHeading $document
 $marker=''
 if($null -eq $heading){
  $null=Read-SavedWorkerView $target
 }else{
  if(-not $ChromeAppId){throw 'The virtualized saved conversation needs a verified Chrome profile'}
  $marker=Get-DocumentIdentity $heading
 }
 $documentId=Get-DocumentIdentity $document
 $address=Get-Address $target.window
 if($address -cne $target.url -or (Chat-FromUrl $address) -cne $ChatId -or
    -not (Test-WindowProfile $target.window)){
  throw 'Saved worker address or profile changed during recovery'
 }
 return @{url=$address;document_id=$documentId;user_heading_id=$marker}
}

function Wait-VerifiedSavedWorker([long]$handle) {
 $prior=$null
 for($i=0;$i -lt 25;$i++){
  Start-Sleep -Milliseconds 400
  if(Test-ViewRecoveryPaused){return @{recovery_status='paused'}}
  try {
   $identity=Read-SavedWorkerIdentity (Get-TargetWindow $ChatId $handle)
  }catch{
   $prior=$null
   continue
  }
  if($null -ne $prior -and $identity.url -ceq $prior.url -and
     $identity.document_id -ceq $prior.document_id -and
     $identity.user_heading_id -ceq $prior.user_heading_id){
   $active=@(Find-TargetWindows $ChatId 0)
   if($active.Count -ne 1 -or $active[0].window.Current.NativeWindowHandle -ne $handle -or
      $active[0].url -cne $identity.url){
    throw 'The recovered view is not the unique accessible saved worker'
   }
   if(Test-ViewRecoveryPaused){return @{recovery_status='paused'}}
   return @{recovery_status='restored';window_handle=$handle}
  }
  $prior=$identity
 }
 throw 'The exact saved chat did not load in the recovery window'
}

function Test-SameWorkerTurn($first,$second) {
 return ($first['response_id'] -ceq $second['response_id'] -and
         $first.ready -eq $second.ready -and $first.stop_control -eq $second.stop_control -and
         $first.user_after_assistant -eq $second.user_after_assistant -and
         $first.assistant_turn_count -eq $second.assistant_turn_count -and
         $first.user_turn_count -eq $second.user_turn_count -and
         $first['latest_user_digest'] -ceq $second['latest_user_digest'])
}

function Test-FreshWorkerCompletion($original,$fresh,[string[]]$consumedResponses=@()) {
 if(-not $fresh.ready -or -not $original['latest_user_digest'] -or
    -not $fresh['response_id'] -or $consumedResponses -ccontains $fresh['response_id'] -or
    $original['latest_user_digest'] -cne $fresh['latest_user_digest'] -or
    $original.user_turn_count -ne $fresh.user_turn_count){return $false}
 if($original.ready){return $fresh.assistant_turn_count -gt $original.assistant_turn_count}
 # An unfinished rendering may already contain the final text but still show Stop.
 return $fresh.assistant_turn_count -ge $original.assistant_turn_count
}

function Test-ViewRecoveryPaused {
 return ($PausePath -and (Test-Path -LiteralPath $PausePath))
}

function Assert-EmptyWorkerComposer($target) {
 $editor=Find-Composer $target.window 'Ask ChatGPT'
 $value=$editor.GetCurrentPattern([System.Windows.Automation.ValuePattern]::Pattern).Current.Value
 if((Read-ComposerText $editor $value) -cne '' -or -not (Check-NoAttachments $target.window) -or
    @(Find-EnabledSendButtons $target.window).Count){
  throw 'Saved worker reload held to preserve a draft, attachment or unverified composer'
 }
}

function Recover-SavedWorkerView {
 if($ChatId -cnotmatch '^[A-Fa-f0-9]{8}(?:-[A-Fa-f0-9]{4}){3}-[A-Fa-f0-9]{12}$' -or -not $Recovery){
  throw 'Recovery needs a registered saved chat UUID and recovery mode'
 }
 if(Test-ViewRecoveryPaused){return @{recovery_status='paused'}}
 $savedUrl=$null
 if($ProjectUrl -cmatch '^(https://chatgpt[.]com/g/(g-p-[a-f0-9]+)(?:-[A-Za-z0-9-]+)?)/project/?$' -and
    $Matches[2] -ceq $ProjectId){
  $savedUrl=$Matches[1]+'/c/'+$ChatId
 }elseif($ProjectUrl -or $Recovery -eq 'missing'){
  throw 'Recovery needs the verified Project landing URL for the saved worker'
 }
 $matchesFound=@(Find-TargetWindows $ChatId 0)
 if($matchesFound.Count -gt 1){throw 'Multiple accessible Chrome views show the saved worker'}
 $original=$null
 $originalTurn=$null
 if($Recovery -eq 'missing' -and $matchesFound.Count -eq 1){
  return (Wait-VerifiedSavedWorker $matchesFound[0].window.Current.NativeWindowHandle)
 }
 if($Recovery -eq 'stale'){
  if(-not $WorkerJournalPath -or -not [IO.File]::Exists($WorkerJournalPath)){
   throw 'Stale recovery needs the registered worker journal'
  }
  $journal=[IO.File]::ReadAllText($WorkerJournalPath,[Text.Encoding]::UTF8) | ConvertFrom-Json
  if($journal.state.current_chat_id -cne $ChatId -or $journal.state.pending){
   throw 'Stale recovery requires the current worker without a pending Send'
  }
  $consumedResponses=@(foreach($anchor in $journal.state.consumed_responses){
   if($anchor[0] -ceq $ChatId){[string]$anchor[1]}
  })
  if($WindowHandle -le 0){throw 'Stale view recovery needs the original window handle'}
  if($matchesFound.Count -ne 1 -or $matchesFound[0].window.Current.NativeWindowHandle -ne $WindowHandle){
   return @{recovery_status='waiting';reason='Original saved worker window changed'}
  }
  $original=$matchesFound[0]
  $originalTurn=Read-SavedWorkerView $original
  if([string]$originalTurn['response_id'] -cne $SourceResponse -or -not $originalTurn['latest_user_digest']){
   return @{recovery_status='waiting';reason='Original worker turn changed or its latest user turn is unavailable'}
  }
  Assert-EmptyWorkerComposer $original
 }
 if(-not $savedUrl){
  if($original.url -cmatch ('^(https://chatgpt[.]com/g/g-p-[a-f0-9]+(?:-[A-Za-z0-9-]+)?/c/'+[regex]::Escape($ChatId)+')(?:[/?#]|$)')){
   $savedUrl=$Matches[1]
  }else{
   throw 'The original saved worker address is unavailable for recovery'
  }
 }
 if(Test-ViewRecoveryPaused){return @{recovery_status='paused'}}
 $probe=Open-ChromeWindow $savedUrl
 $probeHandle=[long]$probe.Current.NativeWindowHandle
 $probeWindow=$probe.GetCurrentPattern([System.Windows.Automation.WindowPattern]::Pattern)
 $retainProbe=$false
 $provedCompletion=$false
 try {
  if($Recovery -eq 'missing'){
   $result=Wait-VerifiedSavedWorker $probeHandle
   $retainProbe=$result.recovery_status -ceq 'restored'
   return $result
  }
  $priorFresh=$null
  for($i=0;$i -lt 25;$i++){
   Start-Sleep -Milliseconds 400
   if(Test-ViewRecoveryPaused){return @{recovery_status='paused'}}
   try {
    $candidate=Get-TargetWindow $ChatId $probeHandle
    $fresh=Read-SavedWorkerView $candidate
   }catch{
    $priorFresh=$null
    continue
   }
   if(Test-FreshWorkerCompletion $originalTurn $fresh $consumedResponses){
    if($null -ne $priorFresh -and (Test-SameWorkerTurn $priorFresh $fresh)){
     $provedCompletion=$true
     break
    }
    $priorFresh=$fresh
    Start-Sleep -Milliseconds 800
   }else{$priorFresh=$null}
  }
 } finally {
  if(-not $retainProbe){$probeWindow.Close()}
 }
 if(-not $provedCompletion){return @{recovery_status='waiting';reason='Fresh view did not verify a completed reply to the same user turn'}}
 if(Test-ViewRecoveryPaused){return @{recovery_status='paused'}}
 # Close the duplicate first. Only the original, still unchanged target may reload.
 $active=@(Find-TargetWindows $ChatId 0)
 if($active.Count -ne 1 -or $active[0].window.Current.NativeWindowHandle -ne $WindowHandle -or
    $active[0].url -cne $original.url){
  return @{recovery_status='waiting';reason='Original saved worker view changed during recovery'}
 }
 $reload=@((Desc $original.window) | Where-Object {
  $_.Current.ControlType -eq [System.Windows.Automation.ControlType]::Button -and
  $_.Current.Name -cmatch '^Reload(?: this page)?$' -and $_.Current.IsEnabled
 })
 if($reload.Count -ne 1){throw 'Chrome Reload was not uniquely available in the saved worker window'}
 $reloadPattern=$reload[0].GetCurrentPattern([System.Windows.Automation.InvokePattern]::Pattern)
 if(-not (Test-SameWorkerTurn $originalTurn (Read-SavedWorkerView $active[0]))){
  return @{recovery_status='waiting';reason='Original worker turn changed before reload'}
 }
 Assert-EmptyWorkerComposer $original
 if(Test-ViewRecoveryPaused){return @{recovery_status='paused'}}
 if((Get-Address $original.window) -cne $original.url -or -not (Test-WindowProfile $original.window)){
  return @{recovery_status='waiting';reason='Original saved worker address changed before reload'}
 }
 $reloadPattern.Invoke()
 return @{recovery_status='refreshed';window_handle=$WindowHandle}
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

function Get-VerifiedSuccessorSource([string]$responseId) {
 $source=Get-TargetWindow $ChatId 0
 $turn=Read-CurrentTurn $source
 if(-not $turn.ready -or $turn.response_id -cne $responseId -or
    (Get-Address $source.window) -cne $source.url -or -not (Test-WindowProfile $source.window)){
  throw 'The saved worker no longer shows the verified completion for this successor'
 }
 return $source
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
 $target=Get-ObservableSavedTarget
 if($target['view_status']){$target | ConvertTo-Json -Compress;exit 0}
 $turn=Read-CurrentTurn $target -IncludeUserAnchor
 if((Get-Address $target.window) -cne $target.url){throw 'Saved worker address changed during observation'}
 $turn['project']=$ProjectId
 $turn['view_status']='observed'
 $turn['window_handle']=[long]$target.window.Current.NativeWindowHandle
 $turn | ConvertTo-Json -Compress -Depth 5
 exit 0
}

if($Mode -eq 'RecoverView') {
 $receipt=Recover-SavedWorkerView
 $receipt['project']=$ProjectId
 $receipt['chat_id']=$ChatId
 $receipt | ConvertTo-Json -Compress
 exit 0
}

if($Mode -eq 'ObserveReentry') {
 if(-not $ChatId -or -not $OwnerAnchor){throw 'Owner re-entry needs a saved worker and hold anchor'}
 $existing=Get-ObservableSavedTarget
 if($existing['view_status']){$existing | ConvertTo-Json -Compress;exit 0}
 $turn=Read-CurrentTurn $existing
 if($turn.stop_control -or $turn.user_after_assistant){
  if((Compare-OwnerTurn $turn $OwnerAnchor) -cne 'advanced'){
   throw 'The active reader could not verify advancement from the saved reply anchor'
  }
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
  if((Get-Address $existing.window) -cne $existing.url -or -not (Test-WindowProfile $existing.window)){
   throw 'The saved worker destination changed before re-entry reload'
  }
  $reload[0].GetCurrentPattern([System.Windows.Automation.InvokePattern]::Pattern).Invoke()
 }
 @{disposition=$verdict;project=$ProjectId;chat_id=$ChatId} | ConvertTo-Json -Compress
 exit 0
}

if($Mode -eq 'Prepare') {
 if($Preflight -and ($Kind -ne 'LAUNCH_SUCCESSOR' -or $ChatId -or $WindowHandle -or
                    $SourceResponse -or $PrepareAction -or $PrepareTargetPath)){
  throw 'Preflight only inspects a fresh Project composer'
 }
 $preflightWindow=$null
 try {
 if($Kind -eq 'CONTINUE_CURRENT') {
  if(-not $ChatId){throw 'Continuation needs current saved chat'}
  $target=Get-ObservableSavedTarget
  if($target['view_status']){$target | ConvertTo-Json -Compress;exit 0}
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
  $source=if($ChatId -and $SourceResponse){Get-VerifiedSuccessorSource $SourceResponse}
  $new=$null
  if($ChatId -and $WindowHandle -gt 0){
   try {
    $prepared=Get-TargetWindow '' $WindowHandle
    if($null -eq $prepared.chat -and $prepared.url -cmatch '/project$'){
     $new=$prepared.window
    }
   }catch{}
  }
  if($null -ne $source -and $SourceResponse -cmatch '^uia-turn-' -and
     $PrepareAction -and $PrepareTargetPath -and $null -eq $new){
   $navigation=$null
   try {
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
  if($Preflight){$preflightWindow=$new.GetCurrentPattern([System.Windows.Automation.WindowPattern]::Pattern)}
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
  document_id=(Get-DocumentIdentity (Get-ComposerDocument $editor))
  editable_text=$actual;uia_value=$value
  attachments_present=$attachments
  observed_url=$target.url
 } | ConvertTo-Json -Compress -Depth 5
 } finally {
  if($null -ne $preflightWindow){$preflightWindow.Close()}
 }
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

function Assert-PrivateDispatchReceipt {
 # Revalidate the exact persisted action at the actual native browser
 # boundary. An old handle/source pair is never sufficient to authorize Send.
 if($Mode -eq 'Send' -and $OwnerInputPath){
  $expectedInput=[IO.File]::ReadAllText([IO.Path]::ChangeExtension($OwnerInputPath, '.sha256'),
                                      [Text.Encoding]::ASCII).Trim()
  $actualInput=(Get-FileHash -LiteralPath $OwnerInputPath -Algorithm SHA256).Hash.ToLowerInvariant()
  if($actualInput -cne $expectedInput){throw 'Private owner input changed before browser dispatch'}
 }
 if($PrepareAction){
  if(-not $PrepareTargetPath -or -not [IO.File]::Exists($PrepareTargetPath)){
   throw 'Prepared action record unavailable'
  }
  $receipt=[IO.File]::ReadAllText($PrepareTargetPath,[Text.Encoding]::UTF8) | ConvertFrom-Json
  $hasher=[Security.Cryptography.SHA256]::Create()
  try{
   $digest=[BitConverter]::ToString($hasher.ComputeHash([Text.Encoding]::UTF8.GetBytes($Message))).Replace('-','').ToLowerInvariant()
  }finally{$hasher.Dispose()}
  if($receipt.action_id -cne $PrepareAction -or $receipt.project -cne $ProjectId -or
     $receipt.kind -cne $Kind -or $receipt.source -cne $ChatId -or
     [long]$receipt.handle -ne $WindowHandle -or
     $receipt.message_sha256 -cne $digest -or
     [string]$receipt.route_receipt -cne $RouteReceipt -or
     $receipt.source_response -cne $PendingResponseId -or
     -not $DocumentId -or $receipt.document_id -cne $DocumentId){
   throw 'Prepared action identity or route changed before browser dispatch'
  }
  if(-not $PendingResponseId -or ($Kind -eq 'CONTINUE_CURRENT' -and
      $receipt.source_response -cne $SourceResponse)){
   throw 'Prepared source response changed before browser dispatch'
  }
  return
 }
 if($BootstrapIntentPath){
  if(-not [IO.File]::Exists($BootstrapIntentPath)){throw 'Bootstrap intent unavailable'}
  $intent=[IO.File]::ReadAllText($BootstrapIntentPath,[Text.Encoding]::UTF8) | ConvertFrom-Json
  if($intent.project -cne $ProjectId -or [long]$intent.handle -ne $WindowHandle -or
     $intent.message -cne $Message){throw 'Bootstrap intent identity changed'}
  if($BootstrapRunId){
   $hasher=[Security.Cryptography.SHA256]::Create()
   try{$digest=[BitConverter]::ToString($hasher.ComputeHash([Text.Encoding]::UTF8.GetBytes($Message))).Replace('-','').ToLowerInvariant()}
   finally{$hasher.Dispose()}
   if($intent.run_id -cne $BootstrapRunId -or
      [string]$intent.route_receipt -cne $RouteReceipt -or
      $intent.message_sha256 -cne $digest -or
      $BootstrapActionId -cnotmatch '^[0-9a-f]{32}$' -or $intent.action_id -cne $BootstrapActionId){
    throw 'Bootstrap run, action, route or message digest changed'
   }
  }elseif($Mode -eq 'Send'){
   throw 'New initial Send requires a bound durable request identity'
  }
  if($Mode -eq 'Send' -and (-not $DocumentId -or $intent.document_id -cne $DocumentId)){
   throw 'Bootstrap dispatch requires the same prepared document'
  }
  return
 }
 throw 'No persisted dispatch action identity at browser boundary'
}

if($Mode -eq 'Send') {
 Assert-PrivateDispatchReceipt
 Hold-IfOwnerPaused
 if($WindowHandle -le 0){throw 'Saved prepared window handle required'}
 if($Message -cnotmatch '^[A-Za-z0-9 .,/_:-]+$'){throw 'Unsupported message characters'}
 if(-not $Message){throw 'Empty message'}
 if($Kind -eq 'CONTINUE_CURRENT' -and
    (-not $ChatId -or ($SourceResponse -cnotmatch '^uia-turn-[1-9][0-9]*-[a-f0-9]{20}$' -and
                       $SourceResponse -cnotmatch '^chrome-turn-[a-f0-9-]{73}$'))){
  throw 'Continuation needs the saved chat and triggering response'
 }
 $target=Get-TargetWindow $(if($Kind -eq 'CONTINUE_CURRENT'){$ChatId}else{''}) $WindowHandle
 $chromeSuccessor=$Kind -eq 'LAUNCH_SUCCESSOR' -and $PendingResponseId -cmatch '^chrome-turn-'
 if($chromeSuccessor){
  try{$null=Get-VerifiedSuccessorSource $PendingResponseId}catch{Hold-ForChangedDestination}
 }
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
 if($Kind -eq 'LAUNCH_SUCCESSOR' -and $target.url -cnotmatch '/project/?$'){
  throw 'The prepared successor is no longer on a fresh Project composer'
 }
 $editorName=if($Kind -eq 'CONTINUE_CURRENT'){'Ask ChatGPT'}else{'New chat in ' + $ProjectName}
 $editor=Find-Composer $target.window $editorName
 if((Get-DocumentIdentity (Get-ComposerDocument $editor)) -cne $DocumentId){Hold-ForChangedDestination}
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
  if((Get-Address $target.window) -cne $target.url -or -not (Test-WindowProfile $target.window)){
   Hold-ForChangedDestination
  }
  if($chromeSuccessor){$null=Get-VerifiedSuccessorSource $PendingResponseId}
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
  $document=Get-ComposerDocument $liveEditor
  if((Get-DocumentIdentity $document) -cne $DocumentId){Hold-ForChangedDestination}
  $sendButtons=@(Find-EnabledSendButtons $document)
  if($sendButtons.Count -ne 1){Hold-ForChangedDestination}
  $send=$sendButtons[0].GetCurrentPattern([System.Windows.Automation.InvokePattern]::Pattern)
  if((Get-Address $target.window) -cne $target.url -or -not (Test-WindowProfile $target.window)){
   Hold-ForChangedDestination
  }
 } catch {Hold-ForChangedDestination}
 Assert-PrivateDispatchReceipt
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
     (Find-PostedMessage $target.window $Message $SourceResponse $url $PendingResponseId)){
   @{project=$ProjectId;chat_id=$chat;submitted_text=$Message;posted_message_observed=$true;window_handle=$WindowHandle} | ConvertTo-Json -Compress
   exit 0
  }
 }
 throw 'Send attempted but exact posted message + saved ID not both observed'
}
if($Mode -eq 'Reconcile') {
 Assert-PrivateDispatchReceipt
 if($Kind -eq 'CONTINUE_CURRENT' -and -not ($ChatId -and $SourceResponse)){
  throw 'Reconcile needs the saved chat and triggering response'
 }
 $target=Get-TargetWindow $(if($Kind -eq 'CONTINUE_CURRENT'){$ChatId}else{''}) $WindowHandle
 $url=Get-Address $target.window
 $chat=Chat-FromUrl $url
 $posted= $chat -and ($Kind -ne 'CONTINUE_CURRENT' -or $chat -ceq $ChatId) -and
          (Find-PostedMessage $target.window $Message $SourceResponse $url $PendingResponseId)
 @{project=$ProjectId;chat_id=$chat;submitted_text=$(if($posted){$Message}else{$null});posted_message_observed=[bool]$posted} | ConvertTo-Json -Compress
 exit 0
}
throw 'Unknown mode'
