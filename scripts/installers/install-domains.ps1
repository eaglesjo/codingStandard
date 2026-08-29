param(
  [string]$Target='.',
  [ValidateSet('en','ko')][string]$Language,
  [ValidateSet('common','llm','vision','all')][string]$Domain,
  [ValidateSet('Ask','Merge','Overwrite','Skip')][string]$ConflictAction='Ask',
  [switch]$DryRun
)
$ErrorActionPreference='Stop'
$Root=Split-Path -Parent (Split-Path -Parent $PSScriptRoot)

if(-not $Language){
  Write-Host 'Language: 1) English  2) Korean'
  $choice=Read-Host 'Language [1]'
  $Language=if([string]::IsNullOrWhiteSpace($choice)-or $choice -in @('1','en')){'en'}elseif($choice -in @('2','ko')){'ko'}else{throw 'Invalid language'}
}
if(-not $Domain){
  Write-Host 'Domain: 1) Common  2) LLM  3) Vision  4) All'
  $choice=Read-Host 'Domain [4]'
  $Domain=switch($choice){'1'{'common'}'2'{'llm'}'3'{'vision'}'4'{'all'}default{'all'}}
}
$resolvedTarget=[System.IO.Path]::GetFullPath($Target)
if(-not (Test-Path -LiteralPath $resolvedTarget)){ New-Item -ItemType Directory -Force -Path $resolvedTarget | Out-Null }
$Target=$resolvedTarget
$SrcRoot=$Root
if($Language -eq 'ko' -and (Test-Path "$Root/i18n/ko")){ $SrcRoot="$Root/i18n/ko" }
$script:Policy=$ConflictAction

function MergeText($old,$new,$path){
  if($path -match '\.(py|ya?ml|sh|bash)$'){ $s='# BEGIN CODINGSTANDARD MANAGED BLOCK';$e='# END CODINGSTANDARD MANAGED BLOCK' }
  else{ $s='<!-- BEGIN CODINGSTANDARD MANAGED BLOCK -->';$e='<!-- END CODINGSTANDARD MANAGED BLOCK -->' }
  $pattern="(?ms)^$([regex]::Escape($s)).*?$([regex]::Escape($e))\s*"
  if($old -match $pattern){ return [regex]::Replace($old,$pattern,"$s`r`n$new`r`n$e`r`n") }
  return "$($old.TrimEnd())`r`n`r`n$s`r`n$new`r`n$e`r`n"
}
function Conflict($path){
  if($script:Policy -ne 'Ask'){return $script:Policy}
  do{$c=(Read-Host "Existing $path [M]erge [O]verwrite [S]kip [A]llMerge [W]allOverwrite [K]allSkip").ToUpperInvariant()}while($c -notin @('M','O','S','A','W','K'))
  switch($c){'A'{$script:Policy='Merge';return'Merge'}'W'{$script:Policy='Overwrite';return'Overwrite'}'K'{$script:Policy='Skip';return'Skip'}'M'{return'Merge'}'O'{return'Overwrite'}default{return'Skip'}}
}
function AddFiles([System.Collections.Generic.List[string]]$list,[string]$domain){
  if($domain -eq 'common'){
    $list.AddRange([string[]]@('AGENTS.md','CLAUDE.md','GEMINI.md','.github/copilot-instructions.md','.cursor/rules/coding-standard.mdc','.windsurf/rules/coding-standard.md','.clinerules/01-coding-standard.md','.continue/rules/01-coding-standard.md','.junie/AGENTS.md','.amazonq/rules/coding-standard.md','docs/development/CONVENTIONS.md','.aider.conf.yml','core/common/AGENT.md','core/common/SKILL.md','core/common/ENVIRONMENT.md','core/common/environment.py','core/common/experiment.py','domains/manus/PROJECT_INSTRUCTIONS.md','domains/manus/SKILL.md','domains/manus/README.md'))
  } elseif($domain -eq 'llm'){
    $list.AddRange([string[]]@('.github/instructions/llm.instructions.md','domains/llm/AGENT.md','domains/llm/SKILL.md','domains/llm/ENVIRONMENT.md','domains/llm/environment.py','domains/llm/experiment.py','domains/llm/memory_smoke_test.py','domains/llm/README.md','domains/llm/config/training.yaml','domains/llm/config/ablation.yaml'))
    Get-ChildItem "$SrcRoot/domains/llm/skills" -Recurse -Filter SKILL.md | ForEach-Object {$list.Add($_.FullName.Substring($SrcRoot.Length+1))}
  } elseif($domain -eq 'vision'){
    $list.AddRange([string[]]@('.github/instructions/vision.instructions.md','domains/vision/AGENT.md','domains/vision/SKILL.md','domains/vision/ENVIRONMENT.md','domains/vision/memory_smoke_test.py','domains/vision/README.md','domains/vision/config/training.yaml','domains/vision/config/ablation.yaml'))
    Get-ChildItem "$SrcRoot/domains/vision/skills" -Recurse -Filter SKILL.md | ForEach-Object {$list.Add($_.FullName.Substring($SrcRoot.Length+1))}
  }
}
$files=[System.Collections.Generic.List[string]]::new(); AddFiles $files 'common'
if($Domain -eq 'llm'){AddFiles $files 'llm'}elseif($Domain -eq 'vision'){AddFiles $files 'vision'}elseif($Domain -eq 'all'){AddFiles $files 'llm';AddFiles $files 'vision'}
foreach($rel in $files){
  $src=Join-Path $SrcRoot $rel;$dst=Join-Path $Target $rel
  if(!(Test-Path $src)){throw "Missing template: $rel"}
  if($DryRun){Write-Host "[DRY-RUN] $(if(Test-Path $dst){'EXIST'}else{'CREATE'}) $rel";continue}
  New-Item -ItemType Directory -Force -Path (Split-Path $dst)|Out-Null
  $new=[IO.File]::ReadAllText($src,[Text.UTF8Encoding]::new($false))
  if(!(Test-Path $dst)){[IO.File]::WriteAllText($dst,$new,[Text.UTF8Encoding]::new($false));continue}
  $a=Conflict $rel
  if($a -eq 'Skip'){continue}; if($a -eq 'Overwrite'){[IO.File]::WriteAllText($dst,$new,[Text.UTF8Encoding]::new($false));continue}
  $old=[IO.File]::ReadAllText($dst); [IO.File]::WriteAllText($dst,(MergeText $old $new $rel),[Text.UTF8Encoding]::new($false))
}
Write-Host "Installed: language=$Language domain=$Domain dryRun=$DryRun"
