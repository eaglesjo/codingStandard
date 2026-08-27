param(
    [Parameter(Mandatory = $false)]
    [string]$Target = ".",

    [Parameter(Mandatory = $false)]
    [ValidateSet("en", "ko")]
    [string]$Language,

    [Parameter(Mandatory = $false)]
    [ValidateSet("Ask", "Merge", "Overwrite", "Skip")]
    [string]$ConflictAction = "Ask"
)

$ErrorActionPreference = "Stop"
$SourceRoot = Split-Path -Parent $PSScriptRoot
$TargetRoot = (Resolve-Path $Target).Path
$script:GlobalConflictAction = $ConflictAction

if (-not $Language) {
    Write-Host "Select installation language:"
    Write-Host "  1) English (en)"
    Write-Host "  2) Korean  (ko)"
    $Selection = Read-Host "Language [1]"
    if ([string]::IsNullOrWhiteSpace($Selection) -or $Selection -eq "1" -or $Selection -eq "en") {
        $Language = "en"
    } elseif ($Selection -eq "2" -or $Selection -eq "ko") {
        $Language = "ko"
    } else {
        throw "Invalid language selection. Use 1, 2, en, or ko."
    }
}

function Get-SourcePath([string]$RelativePath) {
    if ($Language -eq "ko") {
        $KoreanPath = Join-Path $SourceRoot (Join-Path "i18n/ko" $RelativePath)
        if (Test-Path -LiteralPath $KoreanPath) { return $KoreanPath }
    }
    $EnglishPath = Join-Path $SourceRoot $RelativePath
    if (-not (Test-Path -LiteralPath $EnglishPath)) { throw "Template not found: $RelativePath" }
    return $EnglishPath
}

function Get-Markers([string]$Path) {
    if ($Path -match "\.(py|ya?ml|sh|bash)$") {
        return @("# BEGIN CODINGSTANDARD MANAGED BLOCK", "# END CODINGSTANDARD MANAGED BLOCK")
    }
    return @("<!-- BEGIN CODINGSTANDARD MANAGED BLOCK -->", "<!-- END CODINGSTANDARD MANAGED BLOCK -->")
}

function Merge-AiderConfig([string]$Existing) {
    if ($Existing -match "(?m)^read:\s*\[([^\]]*)\]\s*$") {
        if ($Existing -match "CONVENTIONS\.md") { return $Existing }
        return [regex]::Replace($Existing, "(?m)^read:\s*\[([^\]]*)\]\s*$", {
            param($m)
            $items = $m.Groups[1].Value.Trim()
            if ($items) { "read: [$items, CONVENTIONS.md]" } else { "read: [CONVENTIONS.md]" }
        })
    }

    if ($Existing -match "(?ms)^read:\s*\r?\n((?:[ \t]+-.*\r?\n)*)") {
        if ($Existing -match "CONVENTIONS\.md") { return $Existing }
        return [regex]::Replace($Existing, "(?ms)^read:\s*\r?\n((?:[ \t]+-.*\r?\n)*)", {
            param($m)
            "read:`r`n$($m.Groups[1].Value)  - CONVENTIONS.md`r`n"
        }, 1)
    }

    $Markers = Get-Markers ".aider.conf.yml"
    return "$($Existing.TrimEnd())`r`n`r`n$($Markers[0])`r`nread:`r`n  - CONVENTIONS.md`r`n$($Markers[1])`r`n"
}

function Merge-Text([string]$Existing, [string]$Incoming, [string]$DestinationPath) {
    if ($DestinationPath -eq ".aider.conf.yml") { return Merge-AiderConfig $Existing }
    $Markers = Get-Markers $DestinationPath
    $Start = [regex]::Escape($Markers[0])
    $End = [regex]::Escape($Markers[1])
    $Pattern = "(?ms)^$Start.*?$End\s*"
    if ($Existing -match $Pattern) {
        return [regex]::Replace($Existing, $Pattern, "$($Markers[0])`r`n$Incoming`r`n$($Markers[1])`r`n")
    }
    return "$($Existing.TrimEnd())`r`n`r`n$($Markers[0])`r`n$Incoming`r`n$($Markers[1])`r`n"
}

function Resolve-Conflict([string]$DestinationRelativePath) {
    if ($script:GlobalConflictAction -ne "Ask") { return $script:GlobalConflictAction }
    Write-Host ""
    Write-Host "File already exists: $DestinationRelativePath" -ForegroundColor Yellow
    Write-Host "  M = Merge"
    Write-Host "  O = Overwrite"
    Write-Host "  S = Skip"
    Write-Host "  A = Merge all remaining files"
    Write-Host "  W = Overwrite all remaining files"
    Write-Host "  K = Skip all remaining files"
    do {
        $Choice = (Read-Host "Action [M/O/S]").Trim().ToUpperInvariant()
    } while ($Choice -notin @("M", "O", "S", "A", "W", "K"))
    switch ($Choice) {
        "A" { $script:GlobalConflictAction = "Merge"; return "Merge" }
        "W" { $script:GlobalConflictAction = "Overwrite"; return "Overwrite" }
        "K" { $script:GlobalConflictAction = "Skip"; return "Skip" }
        "M" { return "Merge" }
        "O" { return "Overwrite" }
        "S" { return "Skip" }
    }
}

function Install-File([string]$SourceRelativePath, [string]$DestinationRelativePath) {
    $Source = Get-SourcePath $SourceRelativePath
    $Destination = Join-Path $TargetRoot $DestinationRelativePath
    New-Item -ItemType Directory -Path (Split-Path -Parent $Destination) -Force | Out-Null
    $SourceText = [System.IO.File]::ReadAllText($Source, [System.Text.UTF8Encoding]::new($false))

    if (-not (Test-Path -LiteralPath $Destination)) {
        [System.IO.File]::WriteAllText($Destination, $SourceText, [System.Text.UTF8Encoding]::new($false))
        Write-Host "Installed $DestinationRelativePath [$Language]"
        return
    }

    $Action = Resolve-Conflict $DestinationRelativePath
    switch ($Action) {
        "Skip" { Write-Host "Skipped $DestinationRelativePath" }
        "Overwrite" {
            [System.IO.File]::WriteAllText($Destination, $SourceText, [System.Text.UTF8Encoding]::new($false))
            Write-Host "Overwritten $DestinationRelativePath [$Language]"
        }
        "Merge" {
            $ExistingText = [System.IO.File]::ReadAllText($Destination, [System.Text.UTF8Encoding]::new($false))
            $MergedText = Merge-Text $ExistingText $SourceText $DestinationRelativePath
            [System.IO.File]::WriteAllText($Destination, $MergedText, [System.Text.UTF8Encoding]::new($false))
            Write-Host "Merged $DestinationRelativePath [$Language]"
        }
    }
}

$InstallMap = @(
    @{ Source = "AGENTS.md"; Destination = "AGENTS.md" },
    @{ Source = "CLAUDE.md"; Destination = "CLAUDE.md" },
    @{ Source = "GEMINI.md"; Destination = "GEMINI.md" },
    @{ Source = ".github/copilot-instructions.md"; Destination = ".github/copilot-instructions.md" },
    @{ Source = ".github/instructions/llm.instructions.md"; Destination = ".github/instructions/llm.instructions.md" },
    @{ Source = ".cursor/rules/coding-standard.mdc"; Destination = ".cursor/rules/coding-standard.mdc" },
    @{ Source = ".windsurf/rules/coding-standard.md"; Destination = ".windsurf/rules/coding-standard.md" },
    @{ Source = ".clinerules/01-coding-standard.md"; Destination = ".clinerules/01-coding-standard.md" },
    @{ Source = ".continue/rules/01-coding-standard.md"; Destination = ".continue/rules/01-coding-standard.md" },
    @{ Source = ".junie/AGENTS.md"; Destination = ".junie/AGENTS.md" },
    @{ Source = "CONVENTIONS.md"; Destination = "CONVENTIONS.md" },
    @{ Source = ".aider.conf.yml"; Destination = ".aider.conf.yml" },
    @{ Source = "LLM/AGENT.md"; Destination = "LLM/AGENT.md" },
    @{ Source = "LLM/SKILL.md"; Destination = "LLM/SKILL.md" },
    @{ Source = "LLM/ENVIRONMENT.md"; Destination = "LLM/ENVIRONMENT.md" },
    @{ Source = "LLM/environment.py"; Destination = "LLM/environment.py" },
    @{ Source = "LLM/README.md"; Destination = "LLM/README.md" }
)

foreach ($Item in $InstallMap) { Install-File $Item.Source $Item.Destination }

Write-Host ""
Write-Host "AI coding standard installed into: $TargetRoot"
Write-Host "Language: $Language"
Write-Host "Conflict policy: $ConflictAction"
Write-Host "Environment profiler: python LLM/environment.py"
Write-Host "Supported AI integrations: Codex/AGENTS.md, Claude Code, Gemini CLI, GitHub Copilot, Cursor, Windsurf, Cline, Continue, Junie, Aider"
