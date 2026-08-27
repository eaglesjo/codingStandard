param(
    [Parameter(Mandatory = $false)]
    [string]$Target = ".",

    [Parameter(Mandatory = $false)]
    [ValidateSet("en", "ko")]
    [string]$Language
)

$ErrorActionPreference = "Stop"

$SourceRoot = Split-Path -Parent $PSScriptRoot
$TargetRoot = (Resolve-Path $Target).Path

if (-not $Language) {
    Write-Host "Select installation language:"
    Write-Host "  1) English (en)"
    Write-Host "  2) Korean  (ko)"
    $Selection = Read-Host "Language [1]"
    if ([string]::IsNullOrWhiteSpace($Selection) -or $Selection -eq "1") {
        $Language = "en"
    } elseif ($Selection -eq "2") {
        $Language = "ko"
    } else {
        throw "Invalid language selection. Use 1, 2, en, or ko."
    }
}

function Get-SourcePath([string]$RelativePath) {
    if ($Language -eq "ko") {
        $KoreanPath = Join-Path $SourceRoot (Join-Path "i18n/ko" $RelativePath)
        if (Test-Path -LiteralPath $KoreanPath) {
            return $KoreanPath
        }
    }
    return Join-Path $SourceRoot $RelativePath
}

function Install-LocalizedFile([string]$RelativePath, [string]$DestinationRelativePath) {
    $Source = Get-SourcePath $RelativePath
    $Destination = Join-Path $TargetRoot $DestinationRelativePath
    $Parent = Split-Path -Parent $Destination
    New-Item -ItemType Directory -Path $Parent -Force | Out-Null
    Copy-Item -LiteralPath $Source -Destination $Destination -Force
    Write-Host "Installed $DestinationRelativePath [$Language]"
}

Install-LocalizedFile "AGENTS.md" "AGENTS.md"
Install-LocalizedFile "CLAUDE.md" "CLAUDE.md"
Install-LocalizedFile "GEMINI.md" "GEMINI.md"
Install-LocalizedFile ".github/copilot-instructions.md" ".github/copilot-instructions.md"
Install-LocalizedFile ".github/instructions/llm.instructions.md" ".github/instructions/llm.instructions.md"
Install-LocalizedFile "LLM/AGENT.md" "LLM/AGENT.md"
Install-LocalizedFile "LLM/SKILL.md" "LLM/SKILL.md"
Install-LocalizedFile "LLM/ENVIRONMENT.md" "LLM/ENVIRONMENT.md"
Install-LocalizedFile "LLM/environment.py" "LLM/environment.py"
Install-LocalizedFile "LLM/README.md" "LLM/README.md"

Write-Host ""
Write-Host "AI coding standard installed into: $TargetRoot"
Write-Host "Language: $Language"
Write-Host "Environment profiler: python LLM/environment.py"
Write-Host "Supported entrypoints: AGENTS.md, CLAUDE.md, GEMINI.md, .github/copilot-instructions.md"
