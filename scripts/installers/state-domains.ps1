param(
  [string]$Target='.',
  [switch]$Json
)
$ErrorActionPreference='Stop'
$Root=Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
$args=@('state',$Target)
if($Json){$args += '--json'}
& python (Join-Path $Root 'scripts/installers/installation.py') @args
if($LASTEXITCODE -ne 0){exit $LASTEXITCODE}
