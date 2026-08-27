param(
    [Parameter(Mandatory = $false)]
    [string]$Target = "."
)

$ErrorActionPreference = "Stop"

$SourceRoot = Split-Path -Parent $PSScriptRoot
$TargetRoot = (Resolve-Path $Target).Path

$Files = @(
    "AGENTS.md",
    "CLAUDE.md",
    "GEMINI.md"
)

foreach ($RelativePath in $Files) {
    $Source = Join-Path $SourceRoot $RelativePath
    $Destination = Join-Path $TargetRoot $RelativePath
    Copy-Item -LiteralPath $Source -Destination $Destination -Force
    Write-Host "Installed $RelativePath"
}

$GithubDir = Join-Path $TargetRoot ".github"
New-Item -ItemType Directory -Path $GithubDir -Force | Out-Null

$CopilotSource = Join-Path $SourceRoot ".github/copilot-instructions.md"
$CopilotDestination = Join-Path $GithubDir "copilot-instructions.md"
Copy-Item -LiteralPath $CopilotSource -Destination $CopilotDestination -Force
Write-Host "Installed .github/copilot-instructions.md"

$InstructionDir = Join-Path $GithubDir "instructions"
New-Item -ItemType Directory -Path $InstructionDir -Force | Out-Null
$PathSource = Join-Path $SourceRoot ".github/instructions/llm.instructions.md"
$PathDestination = Join-Path $InstructionDir "llm.instructions.md"
Copy-Item -LiteralPath $PathSource -Destination $PathDestination -Force
Write-Host "Installed .github/instructions/llm.instructions.md"

$LlmDestination = Join-Path $TargetRoot "LLM"
New-Item -ItemType Directory -Path $LlmDestination -Force | Out-Null
$LlmFiles = @(
    "AGENT.md",
    "SKILL.md",
    "ENVIRONMENT.md",
    "environment.py",
    "README.md"
)

foreach ($RelativePath in $LlmFiles) {
    $Source = Join-Path $SourceRoot (Join-Path "LLM" $RelativePath)
    $Destination = Join-Path $LlmDestination $RelativePath
    Copy-Item -LiteralPath $Source -Destination $Destination -Force
    Write-Host "Installed LLM/$RelativePath"
}

Write-Host ""
Write-Host "AI coding instructions installed into: $TargetRoot"
Write-Host "Environment profiler: python LLM/environment.py"
Write-Host "Supported entrypoints: AGENTS.md, CLAUDE.md, GEMINI.md, .github/copilot-instructions.md"
