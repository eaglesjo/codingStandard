# codingStandard

> **Language:** English (default) · [한국어 README](README.ko.md)

An AI-oriented coding standard repository for consistent software development across projects, with a focus on Python, LLM, ML, Jupyter, and Google Colab workflows.

It standardizes environment detection, capability/resource profiling, runtime configuration, memory-safe execution, training reproducibility, Early Stopping, checkpoint/resume, ablation studies, and AI-tool project instructions.

## Installation

Clone the repository, then run the installer from the root of the project where you want to apply the standard.

### Windows / PowerShell

Interactive language selection:

```powershell
git clone https://github.com/eaglesjo/codingStandard.git
powershell -ExecutionPolicy Bypass -File .\codingStandard\scripts\install-coding-standard.ps1 -Target .
```

Explicit language:

```powershell
... -Language en
... -Language ko
```

Preview without changing files:

```powershell
... -Language en -DryRun
```

Choose existing-file policy:

```powershell
... -ConflictAction Ask
... -ConflictAction Merge
... -ConflictAction Overwrite
... -ConflictAction Skip
```

### Linux / macOS

Interactive language selection:

```bash
git clone https://github.com/eaglesjo/codingStandard.git
bash ./codingStandard/scripts/install-coding-standard.sh .
```

Explicit language:

```bash
bash ./codingStandard/scripts/install-coding-standard.sh . en
bash ./codingStandard/scripts/install-coding-standard.sh . ko
```

Conflict policy is the third argument and dry-run is the fourth:

```bash
bash ./codingStandard/scripts/install-coding-standard.sh . ko merge
bash ./codingStandard/scripts/install-coding-standard.sh . ko overwrite
bash ./codingStandard/scripts/install-coding-standard.sh . ko skip
bash ./codingStandard/scripts/install-coding-standard.sh . ko ask true
```

## Existing File Handling

The installer never needs to overwrite an existing file silently. With `Ask`, each conflict can be handled as:

```text
M = Merge
O = Overwrite
S = Skip
A = Merge all remaining
W = Overwrite all remaining
K = Skip all remaining
```

`Merge` preserves existing content and replaces only the clearly marked codingStandard-managed block on subsequent runs. Structured Aider configuration is merged conservatively rather than treated as arbitrary Markdown.

Use `DryRun` / `true` to preview the installation plan before making changes.

## Supported AI Development Tools

| Tool | Installed project entrypoint |
| --- | --- |
| OpenAI Codex / compatible agents | `AGENTS.md` |
| Claude Code | `CLAUDE.md` |
| Gemini CLI | `GEMINI.md` |
| GitHub Copilot | `.github/copilot-instructions.md` + `.github/instructions/` |
| Cursor | `.cursor/rules/coding-standard.mdc` |
| Windsurf | `.windsurf/rules/coding-standard.md` |
| Cline | `.clinerules/01-coding-standard.md` |
| Continue | `.continue/rules/01-coding-standard.md` |
| JetBrains Junie | `.junie/AGENTS.md` |
| Amazon Q Developer | `.amazonq/rules/coding-standard.md` |
| Aider | `CONVENTIONS.md` + `.aider.conf.yml` |

Tool-specific files are thin adapters. The shared behavior remains defined by the common project standard.

## Usage

After installation, run the environment profiler from the target project root:

```bash
python LLM/environment.py
```

To save the detected profile:

```bash
python LLM/environment.py .codingstandard/environment-profile.json
```

The profiler measures the actual Python/runtime environment, OS, CPU, RAM, disk, GPU/accelerator, VRAM, CUDA/MPS/ROCm/DirectML capabilities, and IDE/Jupyter/Colab state. It then resolves a conservative starting runtime configuration.

No specific GPU, RAM size, OS, or IDE is treated as a mandatory machine-specific prerequisite.

## Memory Smoke Test

Before a long training run, execute the standardized synthetic smoke test:

```bash
python LLM/memory_smoke_test.py --cpu --steps 2
```

On an accelerator-enabled machine, omit `--cpu` and use a conservative workload. The runner validates a minimal `load → forward → backward → optimizer step → checkpoint save/reload` path and records runtime, RAM, and GPU memory information. Use the same pattern with the real model before starting a full training job.

## AI Development Workflow

```text
Load AI instructions
        ↓
Inspect repository / project
        ↓
Detect Python / kernel / IDE / runtime
        ↓
Measure CPU / RAM / disk / accelerator / VRAM / capabilities
        ↓
Generate Environment Profile
        ↓
Resolve Runtime Configuration
        ↓
Run Memory Smoke Test
        ↓
Lock the validated environment
        ↓
Remove unused OS / device branches
        ↓
Implement / train / infer
        ↓
Evaluate with Early Stopping / Checkpoint
        ↓
Run Ablation / record reproducibility + resources
        ↓
Final clean run
```

Core principle: **measure first, resolve second, validate third, then implement and run**.

## Skills

Task-specific skills are available under `LLM/skills/`:

```text
LLM/skills/
├── environment/SKILL.md
├── training/SKILL.md
├── ablation/SKILL.md
├── notebook/SKILL.md
├── debugging/SKILL.md
└── release/SKILL.md
```

Agents should use the relevant skill for the current task instead of applying unrelated rules indiscriminately.

## Training and Ablation Configuration

Reusable starting configurations are provided:

```text
LLM/config/training.yaml
LLM/config/ablation.yaml
```

Training defaults include validation, Early Stopping, best checkpoint, Resume, environment-driven resource settings, and reproducibility metadata.

Ablation defaults include a baseline, explicit variants, seed matrix, primary metric, controlled evaluation conditions, and resource tracking.

## Experiment Metadata

Use `LLM/experiment.py` to create reproducible experiment metadata including coding-standard version, config hash, Git commit/branch/dirty state, seed, model/dataset revision, and timestamp.

Example:

```bash
python LLM/experiment.py baseline baseline --seed 42 --config '{"feature_a":true}' --output experiments/baseline.json
```

## Automatic AI Instruction Loading

The main project entrypoints are:

```text
AGENTS.md
CLAUDE.md
GEMINI.md
.github/copilot-instructions.md
```

The installer also provisions tool-specific adapters for Cursor, Windsurf, Cline, Continue, Junie, Amazon Q Developer, and Aider.

The common LLM rules are maintained in:

```text
LLM/AGENT.md
LLM/SKILL.md
LLM/ENVIRONMENT.md
```

## Environment Optimization

The standard is environment-agnostic. `LLM/environment.py` measures capabilities instead of assuming a particular machine.

Recommended settings are starting points only. A workload-specific Memory Smoke Test is the final gate before long training.

The optimization policy may use, where supported and justified:

- small batches with gradient accumulation
- mixed precision
- gradient checkpointing
- quantization
- CPU offload
- controlled DataLoader workers/prefetching
- streaming/chunking/memory mapping
- CPU thread limits
- inference mode

VRAM, RAM, and disk headroom are preserved instead of targeting 100% utilization.

## Validation and CI

Run local repository validation:

```bash
python scripts/validate.py
python scripts/check_i18n.py
python scripts/test_installers.py
python LLM/memory_smoke_test.py --cpu --steps 2
```

GitHub Actions runs repository validation, installer integration tests, and a CPU memory smoke test on pushes to `main` and pull requests.

## Versioning

The current coding standard version is stored in `VERSION`.

Runtime profiles and experiment metadata should record the coding-standard version so results remain traceable after the standard evolves.

## Repository Structure

```text
codingStandard/
├── README.md
├── README.ko.md
├── VERSION
├── AGENTS.md
├── CLAUDE.md
├── GEMINI.md
├── CONVENTIONS.md
├── .aider.conf.yml
├── .amazonq/rules/
├── .cursor/rules/
├── .windsurf/rules/
├── .clinerules/
├── .continue/rules/
├── .junie/
├── .github/
├── i18n/ko/
├── LLM/
│   ├── AGENT.md
│   ├── SKILL.md
│   ├── ENVIRONMENT.md
│   ├── environment.py
│   ├── memory_smoke_test.py
│   ├── experiment.py
│   ├── config/
│   └── skills/
├── scripts/
│   ├── install-coding-standard.ps1
│   ├── install-coding-standard.sh
│   ├── validate.py
│   ├── check_i18n.py
│   └── test_installers.py
└── .github/workflows/validate-coding-standard.yml
```

## Documentation

- [LLM Agent Rules](LLM/AGENT.md)
- [LLM Skill](LLM/SKILL.md)
- [Environment Optimization](LLM/ENVIRONMENT.md)
- [LLM/Jupyter Guide](LLM/README.md)
- [Environment Profiler](LLM/environment.py)
- [Memory Smoke Test](LLM/memory_smoke_test.py)
- [Experiment Metadata Helper](LLM/experiment.py)
- [Korean README](README.ko.md)
