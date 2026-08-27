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

## Common Layer

`COMMON/` contains environment inspection, resource safety, configuration, reproducibility, security, testing, and shared lifecycle rules.

## LLM Layer

`LLM/` covers language models, NLP, RAG, fine-tuning, Jupyter, and Colab. It provides domain Skills, training/ablation configuration, memory smoke testing, and adapters to the shared profiler and experiment metadata helper.

## Vision Layer

`VISION/` covers classification, detection, segmentation, OCR, pose estimation, image generation, and VLM. Vision resource policy considers image resolution, batch size, channels, activation/feature-map memory, workers, cache, and prefetching.

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

The notebook runs in a clean Colab runtime, measures the environment, runs LLM and Vision smoke tests, and performs repository validation.

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
- [Windows Installer Test](scripts/test_installers_windows.ps1)
- [Colab Validation](tests/colab/README.md)
- [Korean README](README.ko.md)
