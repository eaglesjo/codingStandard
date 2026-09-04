param(
  [string]$Target='.',
  [switch]$Force,
  [switch]$DryRun
)
$ErrorActionPreference='Stop'
$Root=Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
$args=@('uninstall',$Target)
if($Force){$args += '--force'}
if($DryRun){$args += '--dry-run'}
& python (Join-Path $Root 'scripts/installers/installation.py') @args
if($LASTEXITCODE -ne 0){exit $LASTEXITCODE}
