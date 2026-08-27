# codingStandard

> **Language:** English (default) · [한국어 README](README.ko.md) · [한국어 설치 가이드](i18n/ko/INSTALL.md)

An AI-oriented development standard for projects that use AI coding agents, LLM/ML workflows, and computer-vision workloads.

## Installation

Clone the repository, then run the domain installer from the project you want to configure.

### Windows / PowerShell

The installer creates the target directory when it does not exist. Omit language/domain to choose interactively.

```powershell
git clone https://github.com/eaglesjo/codingStandard.git
powershell -ExecutionPolicy Bypass -File .\codingStandard\scripts\install-domains.ps1 -Target .
```

Explicit installation:

```powershell
powershell -ExecutionPolicy Bypass -File .\codingStandard\scripts\install-domains.ps1 -Target . -Language en -Domain all
powershell -ExecutionPolicy Bypass -File .\codingStandard\scripts\install-domains.ps1 -Target . -Language ko -Domain vision
```

Preview changes with `-DryRun`. Existing files use `-ConflictAction Ask|Merge|Overwrite|Skip`.

### Linux / macOS

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

For the full Korean installation instructions, see [`i18n/ko/INSTALL.md`](i18n/ko/INSTALL.md).

## Installation Domains

```text
common = Common only
llm    = Common + LLM
vision = Common + Vision
all    = Common + LLM + Vision
```

## Supported AI Development Tools

The installer provisions project-level adapters for common coding agents and AI development tools, including OpenAI Codex-compatible agents, Claude Code, Gemini CLI, GitHub Copilot, Cursor, Windsurf, Cline, Continue, JetBrains Junie, Amazon Q Developer, and Aider.

### Manus

Manus uses a different integration model. It currently documents Project Instructions and file-system-based Skills rather than a repository-root `AGENTS.md`-style automatic instruction file.

The installer therefore also provides:

```text
MANUS/PROJECT_INSTRUCTIONS.md
MANUS/SKILL.md
MANUS/README.md
```

Copy `MANUS/PROJECT_INSTRUCTIONS.md` into the Manus Project Instructions for the project. Import `MANUS/SKILL.md` using Manus Skills when appropriate. Review Skills and bundled scripts before importing or executing them.

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

## Environment and Resource Optimization

Runtime decisions are based on measured capabilities rather than a named machine profile. The shared profiler considers OS, Python/runtime, CPU, RAM, disk, accelerators, VRAM, CUDA/ROCm/MPS/DirectML, precision capability, and Jupyter/Colab state.

Use `COMMON/environment.py` as the shared environment source. LLM and Vision expose adapters/policies on top of it.

## Common / LLM / Vision

`COMMON/` provides shared rules and runtime utilities. `LLM/` provides language-model and NLP workflows. `VISION/` provides computer-vision workflows including classification, detection, segmentation, OCR, pose estimation, image generation, and VLM.

## Skills

Skills are task-specific and should be loaded only when relevant.

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

## Training and Experiments

Long-running training should use validation, Early Stopping where meaningful, best Checkpoint, Resume, controlled Ablation Study, seed control, resource tracking, Git/environment/config metadata, and staged recovery from resource failures.

Shared experiment metadata is implemented in `COMMON/experiment.py` and exposed through the LLM adapter.

## Platform Validation

GitHub Actions validates the installer on a real `windows-latest` runner using Windows PowerShell and PowerShell 7. The test matrix covers English/Korean, Common/LLM/Vision/All, dry-run, merge preservation, Unicode/space paths, and removal of legacy installers.

Google Colab validation is provided as a runnable notebook:

[Open the Colab validation notebook](https://colab.research.google.com/github/eaglesjo/codingStandard/blob/main/tests/colab/codingstandard_colab_test.ipynb)

The notebook can validate the original repository or a fork/moved copy. Enter a full GitHub URL, `owner/repository`, or just a GitHub owner name; an owner name automatically uses the `codingStandard` repository name. Private repositories can use a `GITHUB_TOKEN` Colab Secret or secure token prompt.

## Validation

```bash
python scripts/validate.py
python scripts/check_i18n.py
python scripts/test_installers.py
```

Run the relevant LLM/Vision Memory Smoke Test before long training.

## License

This project is released under the MIT License. See `LICENSE`.

## Documentation

- [Installation Guide](INSTALL.md)
- [Korean Installation Guide](i18n/ko/INSTALL.md)
- [Common Agent Rules](COMMON/AGENT.md)
- [LLM Agent Rules](LLM/AGENT.md)
- [LLM Skill](LLM/SKILL.md)
- [LLM Environment](LLM/ENVIRONMENT.md)
- [Vision Agent Rules](VISION/AGENT.md)
- [Vision Skill](VISION/SKILL.md)
- [Vision Environment](VISION/ENVIRONMENT.md)
- [Manus Integration](MANUS/README.md)
- [Windows Installer Test](scripts/test_installers_windows.ps1)
- [Colab Validation](tests/colab/README.md)
- [Korean README](README.ko.md)
