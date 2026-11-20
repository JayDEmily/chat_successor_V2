param([Parameter(Mandatory=$true)][string]$Candidate)
$ErrorActionPreference='Stop'
Set-StrictMode -Version Latest
Add-Type -AssemblyName UIAutomationTypes
$tokens=$null
$errors=$null
$ast=[Management.Automation.Language.Parser]::ParseFile((Join-Path $Candidate 'integration\uia_adapter.ps1'),[ref]$tokens,[ref]$errors)
if($errors.Count){throw 'Cannot parse'}
foreach($name in @('Find-PostedMessage','Read-AssistantContent','Read-CurrentTurn')){
 $fn=$ast.Find({param($node) $node -is [Management.Automation.Language.FunctionDefinitionAst] -and $node.Name -eq $name},$true)
 . ([scriptblock]::Create($fn.Extent.Text))
}
function Desc($nodes){return $nodes}
function Test-AssistantProse($node){return $true}
function Text-Node($value,$role){
 return @{Current=@{Name=$value;ControlType=[System.Windows.Automation.ControlType]::Text}; FixtureRole=$role}
}
$expected='Okay, continue working.'
$history=@(
 Text-Node 'You said:' 'user header'
 Text-Node 'Previous turn' 'user body'
 Text-Node 'ChatGPT said:' 'assistant header'
 Text-Node 'CHAT_STATUS: NEED_MORE_TIME' 'assistant body'
)
$anchor=(Read-AssistantContent $history 2 1 -Strict).response_id
$exact=$history+@(Text-Node 'You said:' 'user header'; Text-Node $expected 'user body')
$withinBody=$exact+@(Text-Node 'Ask ChatGPT' 'user body'; Text-Node 'Discuss the sample only' 'user body')
$ordinaryLonger=$exact+@(Text-Node 'Discuss the sample only' 'user body')
$ProjectId='g-p-abc123'
$worker='00000000-0000-0000-0000-000000000001'
$nonFinal=$history+@(Text-Node 'Ask ChatGPT' 'assistant body'; Text-Node 'The line above was an example' 'assistant body')
$observed=Read-CurrentTurn @{window=$nonFinal;chat=$worker}
[ordered]@{
  non_final_status_marked_ready=$observed.ready
  assistant_tail_seen=($observed.text -match 'was an example')
  exact_anchored_accepted=(Find-PostedMessage $exact $expected $anchor)
  ordinary_longer_rejected=(-not (Find-PostedMessage $ordinaryLonger $expected $anchor))
  body_with_literal_ask_chatgpt_accepted_anchored=(Find-PostedMessage $withinBody $expected $anchor)
  body_with_literal_ask_chatgpt_accepted_unanchored=(Find-PostedMessage $withinBody $expected)
  body_text_seen_at_acknowledgement=(Read-AssistantContent $withinBody 4 0 -Strict).text
  total_synthetic_user_body_text_nodes=3
}|ConvertTo-Json
