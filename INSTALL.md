# Installation Guide

`install-domains.ps1` and `install-domains.sh` are the only supported installers before the first public release.

## 1. Clone

```bash
git clone https://github.com/eaglesjo/codingStandard.git
```

Run the installer from the repository root of the project you want to configure.

## 2. Choose Language and Domain

The installer supports English and Korean and four domains:

```text
Language
  en = English
  ko = Korean

Domain
  common = common rules only
  llm    = common + LLM
  vision = common + Vision
  all    = common + LLM + Vision
```

### Windows / PowerShell

Interactive mode:

```powershell
powershell -ExecutionPolicy Bypass -File .\codingStandard\scripts\install-domains.ps1 -Target .
```

Explicit mode:

```powershell
powershell -ExecutionPolicy Bypass -File .\codingStandard\scripts\install-domains.ps1 -Target . -Language ko -Domain vision
```

### Linux / macOS

Interactive mode:

```bash
bash ./codingStandard/scripts/install-domains.sh .
```

Explicit mode:

```bash
bash ./codingStandard/scripts/install-domains.sh . ko vision ask false
```

Arguments are:

```text
TARGET LANGUAGE DOMAIN CONFLICT_POLICY DRY_RUN
```

## 3. Preview Before Installing

PowerShell:

```powershell
... -Language en -Domain all -DryRun
```

Bash:

```bash
bash ./codingStandard/scripts/install-domains.sh . en all ask true
```

Dry-run never writes installation files.

## 4. Existing Files

When a target file already exists:

```text
Ask       choose per file
Merge     preserve existing content and update the codingStandard-managed block
Overwrite replace the complete target file
Skip      keep the existing target file
```

Use `Merge` for project-owned instruction files when preserving local rules is important. Use `Overwrite` for files fully owned by the standard.

## 5. What Common Installs

The Common layer installs the AI-agent entrypoints and shared rules used by supported tools:

```text
AGENTS.md
CLAUDE.md
GEMINI.md
.github/*
.cursor/*
.windsurf/*
.clinerules/*
.continue/*
.junie/*
.amazonq/*
CONVENTIONS.md
.aider.conf.yml
COMMON/*
```

## 6. What LLM Adds

LLM installs:

```text
LLM/AGENT.md
LLM/SKILL.md
LLM/ENVIRONMENT.md
LLM/environment.py
LLM/memory_smoke_test.py
LLM/experiment.py
LLM/config/*
LLM/skills/*
```

## 7. What Vision Adds

Vision installs:

```text
VISION/AGENT.md
VISION/SKILL.md
VISION/ENVIRONMENT.md
VISION/memory_smoke_test.py
VISION/README.md
VISION/config/*
VISION/skills/*
```

Vision Skills cover classification, detection, segmentation, OCR, pose estimation, image generation, and VLM.

## 8. Validation After Installation

```bash
python LLM/environment.py
python scripts/validate.py
```

For LLM:

```bash
python LLM/memory_smoke_test.py --cpu --steps 2
```

For Vision:

```bash
python VISION/memory_smoke_test.py --device auto --image-size 224 --batch-size 1 --steps 2
```
