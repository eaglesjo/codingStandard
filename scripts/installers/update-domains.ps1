param(
  [string]$Target='.',
  [ValidateSet('ask','merge','overwrite','skip')][string]$Policy='merge',
  [switch]$DryRun
)
$ErrorActionPreference='Stop'
$Root=Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
$args=@('update',$Target,'--policy',$Policy)
if($DryRun){$args += '--dry-run'}
& python (Join-Path $Root 'scripts/installers/installation.py') @args
if($LASTEXITCODE -ne 0){exit $LASTEXITCODE}
