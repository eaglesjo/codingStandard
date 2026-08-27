# codingStandard

> **Language:** English (default) · [한국어 README](README.ko.md)

An AI-oriented development standard for projects that use AI coding agents, LLM/ML workflows, and computer-vision workloads.

## Installation

Clone the repository, then run the domain installer from the project you want to configure.

### Windows / PowerShell

Interactive selection of language and domain:

```powershell
git clone https://github.com/eaglesjo/codingStandard.git
powershell -ExecutionPolicy Bypass -File .\codingStandard\scripts\install-domains.ps1 -Target .
```

Explicit installation:

```powershell
powershell -ExecutionPolicy Bypass -File .\codingStandard\scripts\install-domains.ps1 -Target . -Language en -Domain all
powershell -ExecutionPolicy Bypass -File .\codingStandard\scripts\install-domains.ps1 -Target . -Language ko -Domain vision
```

Use `-DryRun` to preview changes and `-ConflictAction Ask|Merge|Overwrite|Skip` to control existing-file handling.

### Linux / macOS

Interactive selection:

```bash
git clone https://github.com/eaglesjo/codingStandard.git
bash ./codingStandard/scripts/install-domains.sh .
```

Explicit installation:

```bash
bash ./codingStandard/scripts/install-domains.sh . en all ask false
bash ./codingStandard/scripts/install-domains.sh . ko vision overwrite false
```

Arguments are: `target language domain conflict-policy dry-run`.

## Installation Domains

```text
Common
LLM
Vision
All = Common + LLM + Vision
```

Common provides the project/AI-agent baseline. LLM and Vision add domain-specific rules, Skills, configuration, and validation tools.

## Existing File Handling

When a file already exists, choose:

```text
Merge      keep existing content and replace only the codingStandard-managed block
Overwrite  replace the complete file
Skip       leave the existing file unchanged
Ask        decide per file
```

Use dry-run before a large installation when integrating into an existing project.

## Supported AI Development Tools

The installer provisions project-level adapters for:

| Tool | Project entrypoint |
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

## AI Development Workflow

```text
Load project instructions
        ↓
Detect installed domains
        ↓
Inspect repository and workload
        ↓
Measure runtime capabilities/resources
        ↓
Resolve runtime configuration
        ↓
Run domain-appropriate Memory Smoke Test
        ↓
Lock validated environment
        ↓
Apply task-specific Skills
        ↓
Implement / Train / Infer
        ↓
Validate / Early Stop / Checkpoint
        ↓
Ablation / Experiment Metadata
        ↓
Final clean run
```

Core rule: **measure first, validate second, implement third, record everything needed for reproducibility**.

## Common Layer

`COMMON/` contains rules shared by all project types:

- environment inspection
- resource safety
- configuration and reproducibility
- security and secret handling
- testing and validation
- environment-specific cleanup
- training/experiment lifecycle principles

## LLM Layer

`LLM/` covers language-model, NLP, RAG, fine-tuning, Jupyter, and Colab workflows.

It includes environment profiling, memory-safe execution, Early Stopping, best Checkpoint, Resume, Ablation Study configuration, experiment metadata, and task-specific Skills.

Run the profiler:

```bash
python LLM/environment.py
```

Run the LLM memory smoke test:

```bash
python LLM/memory_smoke_test.py --cpu --steps 2
```

## Vision Layer

`VISION/` covers computer-vision workloads:

```text
classification
object detection
segmentation
OCR
pose estimation
image generation
vision-language models
```

Vision-specific optimization considers image resolution, batch size, channels, activation/feature-map memory, augmentation workers, cache, and prefetching.

Run the Vision smoke test:

```bash
python VISION/memory_smoke_test.py --device auto --image-size 224 --batch-size 1 --steps 2
```

## Environment Optimization

The environment policy is machine-agnostic. Runtime decisions come from measured capabilities instead of a named hardware profile.

The profiler may consider:

```text
OS / architecture
Python / framework
CPU / thread capacity
system RAM
free disk space
accelerator vendor / model
VRAM
CUDA / ROCm / MPS / DirectML
FP16 / BF16 support
IDE / Jupyter / Colab
```

Resource-sensitive settings are conservative starting points. A workload-specific smoke test is the final gate before long execution.

## Training and Experiment Rules

Long-running training should normally use:

```text
validation
Early Stopping
best checkpoint
Resume
baseline + ablation matrix
seed control
resource tracking
Git/environment/config metadata
```

Shared configurations:

```text
LLM/config/training.yaml
LLM/config/ablation.yaml
VISION/config/training.yaml
VISION/config/ablation.yaml
```

## Skills

Task-specific Skills live under both domains.

```text
LLM/skills/
├── environment/
├── training/
├── ablation/
├── notebook/
├── debugging/
└── release/

VISION/skills/
├── classification/
├── detection/
├── segmentation/
├── ocr/
├── pose-estimation/
├── image-generation/
└── vlm/
```

Use only Skills relevant to the current task.

## Reproducibility

Experiment metadata should capture at least:

```text
coding-standard version
experiment_id
Git commit / branch / dirty state
configuration hash
seed
model revision
dataset revision
environment profile
runtime configuration
metrics
runtime
peak RAM / VRAM
checkpoint path
```

## Platform Validation

The repository validates the installer on a real GitHub-hosted Windows runner using both Windows PowerShell and PowerShell 7. The workflow covers English/Korean installation, Common/LLM/Vision/All domains, dry-run behavior, merge preservation, Unicode/space paths, and legacy-installer removal.

Google Colab validation is provided as a runnable notebook:

[Open the Colab validation notebook](https://colab.research.google.com/github/eaglesjo/codingStandard/blob/main/tests/colab/codingstandard_colab_test.ipynb)

The notebook clones the repository into a clean Colab runtime, measures the runtime environment, runs the LLM and Vision memory smoke tests, runs repository validation, and writes a JSON result bundle.

## Validation

Run repository validation locally:

```bash
python scripts/validate.py
python scripts/check_i18n.py
python scripts/test_installers.py
```

For an ML/LLM project also run the relevant Memory Smoke Test before a long training job.

GitHub Actions validates the repository and installer behavior on pushes to `main` and pull requests.

## Versioning

The current standard version is stored in `VERSION`. Installed experiment metadata should record it so results remain traceable as the standard evolves.

## Repository Structure

```text
codingStandard/
├── README.md
├── README.ko.md
├── VERSION
├── AGENTS.md
├── CLAUDE.md
├── GEMINI.md
├── COMMON/
├── LLM/
├── VISION/
├── i18n/
├── .github/
├── .amazonq/
├── .cursor/
├── .windsurf/
├── .clinerules/
├── .continue/
├── .junie/
├── .aider.conf.yml
├── CONVENTIONS.md
├── tests/
│   └── colab/
└── scripts/
    ├── install-domains.ps1
    ├── install-domains.sh
    ├── validate.py
    ├── check_i18n.py
    ├── test_installers.py
    └── test_installers_windows.ps1
```

## Documentation

- [Installation Guide](INSTALL.md)
- [Common Agent Rules](COMMON/AGENT.md)
- [LLM Agent Rules](LLM/AGENT.md)
- [LLM Skill](LLM/SKILL.md)
- [LLM Environment](LLM/ENVIRONMENT.md)
- [Vision Agent Rules](VISION/AGENT.md)
- [Vision Skill](VISION/SKILL.md)
- [Vision Environment](VISION/ENVIRONMENT.md)
- [LLM Memory Smoke Test](LLM/memory_smoke_test.py)
- [Vision Memory Smoke Test](VISION/memory_smoke_test.py)
- [Experiment Metadata Helper](LLM/experiment.py)
- [Windows Installer Test](scripts/test_installers_windows.ps1)
- [Colab Validation](tests/colab/README.md)
- [Korean README](README.ko.md)
