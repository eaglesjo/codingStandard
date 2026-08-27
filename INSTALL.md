# Installation

The domain-aware installer is now the recommended installation path.

## Windows

```powershell
powershell -ExecutionPolicy Bypass -File .\codingStandard\scripts\install-domains.ps1 -Target . -Language ko -Domain all
```

Choose one domain:

```text
common = common rules only
llm    = common + LLM rules
vision = common + Vision rules
all    = common + LLM + Vision rules
```

Preview first:

```powershell
... -DryRun
```

Existing files use `Ask`, `Merge`, `Overwrite`, or `Skip`.

## Linux / macOS

```bash
bash ./codingStandard/scripts/install-domains.sh . ko all ask false
```

Arguments are:

```text
TARGET LANGUAGE DOMAIN CONFLICT_POLICY DRY_RUN
```

Example for Vision only:

```bash
bash ./codingStandard/scripts/install-domains.sh . en vision overwrite false
```
