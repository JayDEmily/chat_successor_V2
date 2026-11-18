# L07 test-only composer inspector: no message Send, no draft clearing.
[CmdletBinding()]
param(
 [ValidateSet('Inspect','StageText','Inventory','OpenAttachmentPicker')][string]$Mode='Inspect',
 [Parameter(Mandatory=$true)][long]$WindowHandle,
 [string]$DraftText='',
 [string]$ScreenshotPath=''
)
Set-StrictMode -Version Latest
$ErrorActionPreference='Stop'
Add-Type -AssemblyName UIAutomationClient
Add-Type -AssemblyName UIAutomationTypes
Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing
Add-Type -TypeDefinition @'
using System;
using System.Runtime.InteropServices;
public static class L07Foreground {
 [DllImport("user32.dll")] public static extern bool SetForegroundWindow(IntPtr h);
 [DllImport("user32.dll")] public static extern IntPtr GetForegroundWindow();
}
'@
$projectId='g-p-6afbfc5e59248191a8c690296b24c8ef'
$root=[System.Windows.Automation.AutomationElement]::RootElement
$wins=$root.FindAll([System.Windows.Automation.TreeScope]::Children,[System.Windows.Automation.Condition]::TrueCondition)
$window=$null
foreach($w in $wins) {
 try {if($w.Current.NativeWindowHandle -eq $WindowHandle -and $w.Current.Name -like '*Google Chrome*'){$window=$w;break}}catch{}
}
if($null -eq $window){throw 'Chrome window handle not observed'}
$all=$window.FindAll([System.Windows.Automation.TreeScope]::Descendants,[System.Windows.Automation.Condition]::TrueCondition)
$url=''
foreach($e in $all) {
 try{
  if($e.Current.ControlType -eq [System.Windows.Automation.ControlType]::Edit -and $e.Current.Name -eq 'Address and search bar'){
   $url=$e.GetCurrentPattern([System.Windows.Automation.ValuePattern]::Pattern).Current.Value
   break
  }
 }catch{}
}
if($url -notmatch ('^chatgpt[.]com/g/'+[regex]::Escape($projectId)+'(?:-[^/]+)?/project(?:[/?#]|$)')){throw ('Not an unsaved nominated Project composer: '+$url)}
$editor=$null
foreach($e in $all) {
 try {
  if($e.Current.ControlType -eq [System.Windows.Automation.ControlType]::Edit -and
     $e.Current.Name -ceq 'New chat in Chat succession folder' -and
     $e.Current.IsEnabled -and -not $e.Current.IsOffscreen) {
   if($null -ne $editor){throw 'Multiple editors'}
   $editor=$e
  }
 }catch{}
}
if($null -eq $editor){throw 'Expected composer editor not observed'}
function Read-Actual {
 $original=[System.Windows.Forms.Clipboard]::GetDataObject()
 $sentinel='L07_CLIPBOARD_SENTINEL_'+[guid]::NewGuid().ToString('N')
 try{
  [System.Windows.Forms.Clipboard]::SetText($sentinel)
  if(-not [L07Foreground]::SetForegroundWindow([IntPtr]$WindowHandle)){throw 'Focus failed'}
  $editor.SetFocus()
  Start-Sleep -Milliseconds 150
  if([L07Foreground]::GetForegroundWindow().ToInt64() -ne $WindowHandle){throw 'Foreground changed'}
  [System.Windows.Forms.SendKeys]::SendWait('^a')
  [System.Windows.Forms.SendKeys]::SendWait('^c')
  Start-Sleep -Milliseconds 150
  $clip=[System.Windows.Forms.Clipboard]::GetText()
  if($clip -ceq $sentinel){return ''}
  return $clip
 } finally {
  if($null -ne $original){[System.Windows.Forms.Clipboard]::SetDataObject($original,$true)}else{[System.Windows.Forms.Clipboard]::Clear()}
 }
}
function Get-Buttons {
 $items=@()
 foreach($el in $all) {
  try {
   if($el.Current.ControlType -eq [System.Windows.Automation.ControlType]::Button -and
      -not $el.Current.IsOffscreen) {
    $items+=@{name=$el.Current.Name;enabled=$el.Current.IsEnabled;automation_id=$el.Current.AutomationId}
   }
  }catch{}
 }
 return ,$items
}
$before=Read-Actual
if($Mode -eq 'StageText'){
 if($before -cne ''){throw 'Refusing to overwrite existing draft'}
 if(-not $DraftText -or $DraftText -match '[\r\n{}+^~%]'){throw 'Unsafe or empty draft string'}
 if(-not [L07Foreground]::SetForegroundWindow([IntPtr]$WindowHandle)){throw 'Foreground focus failed before typing'}
 $editor.SetFocus()
 if([L07Foreground]::GetForegroundWindow().ToInt64() -ne $WindowHandle){throw 'Foreground changed before typing'}
 [System.Windows.Forms.SendKeys]::SendWait($DraftText)
 Start-Sleep -Milliseconds 300
}
if($Mode -eq 'OpenAttachmentPicker'){
 if($before -cne ''){throw 'Refusing to touch composer with draft'}
 $found=@()
 foreach($el in $all){
  try{
   if($el.Current.ControlType -eq [System.Windows.Automation.ControlType]::Button -and -not $el.Current.IsOffscreen -and
      $el.Current.Name -match '(?i)(add files|attach|upload|add photos|files and more)'){
    $found+=$el
   }
  }catch{}
 }
 if($found.Count -ne 1){throw ('Attachment button not unique: '+$found.Count)}
 $pattern=$found[0].GetCurrentPattern([System.Windows.Automation.InvokePattern]::Pattern)
 $pattern.Invoke()
 Start-Sleep -Milliseconds 500
}
$after=if($Mode -eq 'OpenAttachmentPicker'){$before}else{Read-Actual}
$uia=$editor.GetCurrentPattern([System.Windows.Automation.ValuePattern]::Pattern).Current.Value
$buttons=Get-Buttons
$attachmentButtons=@($buttons | Where-Object { $_.name -match '(?i)(remove attachment|remove file|delete attachment|remove uploaded file)' })
$rect=$editor.Current.BoundingRectangle
if($ScreenshotPath -and $Mode -ne 'OpenAttachmentPicker'){
 $x=[Math]::Max(0,[int]$rect.X - 20)
 $y=[Math]::Max(0,[int]$rect.Y - 90)
 $width=[Math]::Min(1300,[int]$rect.Width + 40)
 $height=[Math]::Min(360,[int]$rect.Height + 150)
 $bmp=New-Object System.Drawing.Bitmap($width,$height)
 try{
  $g=[System.Drawing.Graphics]::FromImage($bmp)
  try{$g.CopyFromScreen($x,$y,0,0,$bmp.Size)}finally{$g.Dispose()}
  $bmp.Save($ScreenshotPath,[System.Drawing.Imaging.ImageFormat]::Png)
 }finally{$bmp.Dispose()}
}
@{
 mode=$Mode
 window_handle=$WindowHandle
 observed_url=('https://'+$url)
 editable_before=$before
 editable_after=$after
 uia_value=$uia
 attachment_remove_buttons=$attachmentButtons
 visible_button_inventory=$(if($Mode -eq 'Inventory' -or $Mode -eq 'OpenAttachmentPicker'){$buttons}else{@()})
 editor_bounds=@{x=[int]$rect.X;y=[int]$rect.Y;width=[int]$rect.Width;height=[int]$rect.Height}
 screenshot=$ScreenshotPath
}|ConvertTo-Json -Compress -Depth 5
