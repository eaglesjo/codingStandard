# codingStandard

> **Language:** English (default) · [한국어 README](README.ko.md)

An AI-oriented coding standard repository for consistent software development across projects, with a focus on Python, LLM, ML, Jupyter, and Google Colab workflows.

It standardizes environment detection, resource profiling, runtime configuration, memory-safe execution, training reproducibility, Early Stopping, checkpoint/resume, and ablation studies.

## Installation

Clone the repository, then run the installer from the root of the project where you want to apply the standard.

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

You can also choose the conflict policy in advance:

```powershell
# Ask when an installed file already exists
... -ConflictAction Ask

# Merge the selected standard into existing text files
... -ConflictAction Merge

# Replace existing files
... -ConflictAction Overwrite

# Keep existing files unchanged
... -ConflictAction Skip
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

Conflict policy can be passed as the third argument:

```bash
bash ./codingStandard/scripts/install-coding-standard.sh . en merge
bash ./codingStandard/scripts/install-coding-standard.sh . ko overwrite
bash ./codingStandard/scripts/install-coding-standard.sh . ko skip
```

### Existing file handling

When a target file already exists and the conflict policy is `Ask`, the installer offers:

```text
M = Merge
O = Overwrite
S = Skip
A = Merge all remaining
W = Overwrite all remaining
K = Skip all remaining
```

Merge preserves the existing file and maintains a clearly marked codingStandard-managed block. Re-running the installer updates that managed block instead of endlessly appending duplicate content.

Structured files are handled conservatively. For the Aider configuration, merge adds `CONVENTIONS.md` to the existing `read` setting when it can do so safely; otherwise keep the existing config or choose overwrite.

## Supported AI Development Tools

The installer can provision project-level instruction files for multiple AI coding tools. The shared standard remains centered on the common `AGENTS.md` entrypoint, while tool-specific adapters are installed where the tool has its own rule format.

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
| Aider | `CONVENTIONS.md` + `.aider.conf.yml` |

The installed adapters follow each tool's documented project-rule location and format while pointing back to the common project standard.

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

The installer selects either the English or Korean document set and copies it to the filenames expected by the supported AI tools. Tool-specific adapters are kept small and point the agent toward the canonical project rules.

## Environment Optimization

The standard is environment-agnostic. `LLM/environment.py` measures the real execution environment and calculates a conservative starting configuration instead of assuming a particular machine.

Recommended settings are treated as starting points only. The workload-specific Memory Smoke Test is the final gate before a long training run.

The optimization policy may use, where supported and justified:

- small batch sizes with gradient accumulation
- mixed precision
- gradient checkpointing
- quantization
- CPU offload
- controlled DataLoader workers/prefetching
- streaming/chunking/memory mapping
- explicit CPU thread limits
- inference mode for evaluation/inference

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
├── CONVENTIONS.md               # Aider conventions
├── .aider.conf.yml              # Aider auto-read configuration
├── .cursor/rules/               # Cursor
├── .windsurf/rules/             # Windsurf
├── .clinerules/                 # Cline
├── .continue/rules/             # Continue
├── .junie/AGENTS.md             # Junie
├── .github/
│   ├── copilot-instructions.md
│   └── instructions/
├── i18n/
│   ├── README.md
│   └── ko/                      # Korean installer templates
├── LLM/
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
- [Korean README](README.ko.md)
