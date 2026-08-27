# codingStandard

> **Language:** English (default) · [한국어 README](README.ko.md)

An AI-oriented coding standard repository for consistent software development across projects, with a focus on Python, LLM, ML, Jupyter, and Google Colab workflows.

It standardizes environment detection, hardware/resource profiling, runtime configuration, memory-safe execution, training reproducibility, Early Stopping, checkpoint/resume, and ablation studies.

## Installation

Clone the repository, then run the installer from the project root where you want to apply the standard.

### Windows / PowerShell

Interactive language selection:

```powershell
git clone https://github.com/eaglesjo/codingStandard.git
powershell -ExecutionPolicy Bypass -File .\codingStandard\scripts\install-coding-standard.ps1 -Target .
```

Install English explicitly:

```powershell
powershell -ExecutionPolicy Bypass -File .\codingStandard\scripts\install-coding-standard.ps1 -Target . -Language en
```

Install Korean explicitly:

```powershell
powershell -ExecutionPolicy Bypass -File .\codingStandard\scripts\install-coding-standard.ps1 -Target . -Language ko
```

### Linux / macOS

Interactive language selection:

```bash
git clone https://github.com/eaglesjo/codingStandard.git
bash ./codingStandard/scripts/install-coding-standard.sh .
```

Install English explicitly:

```bash
bash ./codingStandard/scripts/install-coding-standard.sh . en
```

Install Korean explicitly:

```bash
bash ./codingStandard/scripts/install-coding-standard.sh . ko
```

The installer places the selected language into the standard project filenames:

```text
AGENTS.md
CLAUDE.md
GEMINI.md
.github/copilot-instructions.md
.github/instructions/llm.instructions.md
LLM/AGENT.md
LLM/SKILL.md
LLM/ENVIRONMENT.md
LLM/environment.py
LLM/README.md
```

If any of these files already exist in the target project, review local changes first because the installer may overwrite them.

## Usage

After installation, run the environment profiler from the target project root:

```bash
python LLM/environment.py
```

To save the detected profile:

```bash
python LLM/environment.py .codingstandard/environment-profile.json
```

The profiler detects the current Python/runtime environment, OS, CPU, RAM, GPU, VRAM, CUDA/MPS, and IDE/Jupyter/Colab state, then resolves a conservative runtime configuration.

No specific GPU, RAM size, OS, or IDE is treated as a mandatory machine-specific prerequisite. Runtime decisions are based on measured resources and workload requirements.

## AI Development Workflow

```text
Load AI instructions
        ↓
Inspect repository / project
        ↓
Detect Python / kernel / IDE / runtime
        ↓
Measure CPU / RAM / GPU / VRAM / accelerator
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

The core principle is: **measure first, resolve second, validate third, then implement and run**.

## Automatic AI Instruction Loading

The canonical sources are:

```text
LLM/AGENT.md
LLM/SKILL.md
LLM/ENVIRONMENT.md
```

The installer selects either the English or Korean document set and copies it to the filenames expected by the supported AI tools.

## Environment Optimization

The standard is environment-agnostic. `LLM/environment.py` measures the real execution environment and calculates a conservative starting configuration instead of assuming a particular machine.

Recommended settings are treated as starting points only. The workload-specific Memory Smoke Test is the final gate before a long training run.

## ML / LLM Training Principles

- Keep VRAM and RAM headroom instead of targeting 100% utilization.
- Apply validation-based Early Stopping to long-running training.
- Save the best checkpoint and keep training resumable.
- Define baseline and ablation variants in an explicit configuration matrix.
- Keep evaluation conditions controlled across variants.
- Record seed, model/dataset revisions, metrics, runtime, peak VRAM/RAM, and the resolved environment profile.
- When OOM occurs, use staged memory recovery rather than repeating the same configuration indefinitely.

## Repository Structure

```text
codingStandard/
├── README.md                    # English default
├── README.ko.md                 # Korean guide
├── AGENTS.md
├── CLAUDE.md
├── GEMINI.md
├── .github/
│   ├── copilot-instructions.md
│   └── instructions/
│       └── llm.instructions.md
├── i18n/
│   ├── README.md
│   └── ko/
│       ├── AGENTS.md
│       ├── CLAUDE.md
│       ├── GEMINI.md
│       ├── .github/
│       └── LLM/
├── LLM/
│   ├── AGENT.md
│   ├── SKILL.md
│   ├── ENVIRONMENT.md
│   ├── environment.py
│   └── README.md
└── scripts/
    ├── install-coding-standard.ps1
    └── install-coding-standard.sh
```

## Documentation

- [LLM Agent Rules](LLM/AGENT.md)
- [LLM Skill](LLM/SKILL.md)
- [Environment Optimization](LLM/ENVIRONMENT.md)
- [LLM/Jupyter Guide](LLM/README.md)
- [Environment Profiler](LLM/environment.py)
- [한국어 README](README.ko.md)
