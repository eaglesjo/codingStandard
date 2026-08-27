param(
  [string]$Target='.',
  [ValidateSet('en','ko')][string]$Language='en',
  [ValidateSet('common','llm','vision','all')][string]$Domain='all',
  [ValidateSet('Ask','Merge','Overwrite','Skip')][string]$ConflictAction='Ask',
  [switch]$DryRun
)
$ErrorActionPreference='Stop'
$Root=Split-Path -Parent $PSScriptRoot
$Target=(Resolve-Path $Target).Path
if($Language -eq 'ko' -and (Test-Path "$Root/i18n/ko")){ $SrcRoot="$Root/i18n/ko" } else { $SrcRoot=$Root }
$script:Policy=$ConflictAction
function MergeText($old,$new,$path){
  $comment = if($path -match '\.(py|ya?ml|sh|bash)$'){'#'}else{'<!--'}
  if($comment -eq '#'){ $s='# BEGIN CODINGSTANDARD MANAGED BLOCK';$e='# END CODINGSTANDARD MANAGED BLOCK' } else { $s='<!-- BEGIN CODINGSTANDARD MANAGED BLOCK -->';$e='<!-- END CODINGSTANDARD MANAGED BLOCK -->' }
  if($old -match [regex]::Escape($s)){ return [regex]::Replace($old,"(?ms)^$([regex]::Escape($s)).*?$([regex]::Escape($e))\s*","$s`r`n$new`r`n$e`r`n") }
  return "$($old.TrimEnd())`r`n`r`n$s`r`n$new`r`n$e`r`n"
}
function Conflict($path){ if($script:Policy -ne 'Ask'){return $script:Policy}; do{$c=(Read-Host "Existing $path [M]erge [O]verwrite [S]kip [A]llMerge [W]allOverwrite [K]allSkip").ToUpperInvariant()}while($c -notin 'M','O','S','A','W','K'); switch($c){'A'{$script:Policy='Merge';return'Merge'}'W'{$script:Policy='Overwrite';return'Overwrite'}'K'{$script:Policy='Skip';return'Skip'}'M'{return'Merge'}'O'{return'Overwrite'}default{return'Skip'}} }
$files=@('AGENTS.md','CLAUDE.md','GEMINI.md','.github/copilot-instructions.md','.github/instructions/llm.instructions.md','.cursor/rules/coding-standard.mdc','.windsurf/rules/coding-standard.md','.clinerules/01-coding-standard.md','.continue/rules/01-coding-standard.md','.junie/AGENTS.md','.amazonq/rules/coding-standard.md','CONVENTIONS.md','.aider.conf.yml','COMMON/AGENT.md','COMMON/SKILL.md','COMMON/ENVIRONMENT.md')
if($Domain -in 'llm','all'){$files+=@('LLM/AGENT.md','LLM/SKILL.md','LLM/ENVIRONMENT.md','LLM/environment.py','LLM/experiment.py','LLM/memory_smoke_test.py','LLM/README.md','LLM/config/training.yaml','LLM/config/ablation.yaml');$files+=Get-ChildItem "$SrcRoot/LLM/skills" -Recurse -Filter SKILL.md|%{$_.FullName.Substring($SrcRoot.Length+1)}}
if($Domain -in 'vision','all'){$files+=@('VISION/AGENT.md','VISION/SKILL.md','VISION/ENVIRONMENT.md','VISION/memory_smoke_test.py','VISION/README.md','VISION/config/training.yaml','VISION/config/ablation.yaml');$files+=Get-ChildItem "$SrcRoot/VISION/skills" -Recurse -File|?{$_.Name -eq 'SKILL.md'}|%{$_.FullName.Substring($SrcRoot.Length+1)}}
foreach($rel in $files){$src=Join-Path $SrcRoot $rel;$dst=Join-Path $Target $rel;if(!(Test-Path $src)){throw "Missing template: $rel"};if($DryRun){Write-Host "[DRY-RUN] $(if(Test-Path $dst){'EXIST'}else{'CREATE'}) $rel";continue};New-Item -ItemType Directory -Force -Path (Split-Path $dst)|Out-Null;$new=[IO.File]::ReadAllText($src,[Text.UTF8Encoding]::new($false));if(!(Test-Path $dst)){[IO.File]::WriteAllText($dst,$new,[Text.UTF8Encoding]::new($false));continue};$a=Conflict $rel;if($a -eq 'Skip'){continue};if($a -eq 'Overwrite'){[IO.File]::WriteAllText($dst,$new,[Text.UTF8Encoding]::new($false));continue};$old=[IO.File]::ReadAllText($dst,[Text.UTF8Encoding]::new($false));[IO.File]::WriteAllText($dst,(MergeText $old $new $rel),[Text.UTF8Encoding]::new($false))}
Write-Host "Installed: language=$Language domain=$Domain dryRun=$DryRun"
