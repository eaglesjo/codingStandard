# AI Engineering Standard

<p align="center">
  <strong>AI Development, Training & Agent Engineering Standards</strong>
</p>

<p align="center">
  <a href="https://github.com/eaglesjo/codingStandard/releases"><img src="https://img.shields.io/github/v/release/eaglesjo/codingStandard?label=public%20release" alt="Public release"></a>
    <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-yellow.svg" alt="MIT License"></a>
  <a href="https://github.com/eaglesjo/codingStandard"><img src="https://img.shields.io/github/stars/eaglesjo/codingStandard?style=flat" alt="GitHub stars"></a>
</p>

> **Language:** English (default) · [한국어 README](README.ko.md) · [한국어 설치 가이드](i18n/ko/INSTALL.md)
>
> **Repository model:** `codingStandard-private` is the development source of truth. Validated releases are published to the public [`eaglesjo/codingStandard`](https://github.com/eaglesjo/codingStandard) repository.

## ✨ What is AI Engineering Standard?

`codingStandard` is a reusable engineering standard for AI-assisted development, model training, experimentation, LLM/Vision workflows, and AI coding agents.

It provides:

- shared project instructions and coding rules;
- LLM and Vision domain guidance;
- task-specific Skills;
- environment and resource detection;
- cross-platform installers;
- English/Korean localization;
- validation and installer test suites;
- Manus Project Instructions and Skills;
- reproducible training and experiment guidance.

## 🤖 Supported AI Development Tools

The repository provides project-level adapters, instruction files, Skills, or documented integration paths for a broad set of AI development tools.

<table>
  <tr>
    <td align="center">🧑‍💻<br><strong>OpenAI Codex</strong></td>
    <td align="center">🤖<br><strong>Claude Code</strong></td>
    <td align="center">✨<br><strong>Gemini CLI</strong></td>
    <td align="center">🐙<br><strong>GitHub Copilot</strong></td>
  </tr>
  <tr>
    <td align="center">⌨️<br><strong>Cursor</strong></td>
    <td align="center">🌊<br><strong>Windsurf</strong></td>
    <td align="center">🐙<br><strong>Cline</strong></td>
    <td align="center">🔄<br><strong>Continue</strong></td>
  </tr>
  <tr>
    <td align="center">🧩<br><strong>JetBrains Junie</strong></td>
    <td align="center">☁️<br><strong>Amazon Q Developer</strong></td>
    <td align="center">🛠️<br><strong>Aider</strong></td>
    <td align="center">🧠<br><strong>Manus</strong></td>
  </tr>
</table>

> Support means that the repository contains a documented adapter, instruction file, Skill, or integration path for the tool. Tool capabilities and integration details can differ by client and version.

## 🐍 Supported Development Environments

AI Engineering Standard is designed to work across local Python development, interactive notebook workflows, cloud notebooks, and AI-assisted IDE workflows.

| Environment / Tool | Support | Use case |
|---|---|---|
| 🐍 **Python** | ✅ Core | Runtime detection, environment configuration, training, inference, validation, and automation |
| 📓 **Jupyter Notebook** | ✅ Supported | Interactive experiments, analysis, training, debugging, and reproducible notebook workflows |
| ☁️ **Google Colab** | ✅ Validated | Cloud-based Python/Jupyter execution, resource-aware experiments, and GPU/accelerator workflows |
| 💻 **Visual Studio Code** | ✅ Supported | Python development, Jupyter notebooks, debugging, testing, and AI-assisted development |
| 🧪 **VS Code + Jupyter** | ✅ Supported | Notebook editing/execution, Python interactive workflows, and remote Jupyter workflows |

The repository includes a runnable Google Colab validation notebook and runtime/resource detection designed to account for notebook and Colab environments.

For VS Code, the standard can be used alongside the Python and Jupyter extensions. VS Code supports Python environments, testing, debugging, and Jupyter notebooks, making it a natural development environment for this standard. citeturn0search0turn0search1

> **Support scope:** Python, Jupyter, Colab, and VS Code are development/runtime environments rather than AI-agent adapters. Their support means that the standard's rules, installers, runtime detection, validation, and documented workflows are designed to work in those environments.

### Manus

Manus uses a different integration model from repository-root `AGENTS.md`-style agents. The repository provides:

```text
MANUS/
├── PROJECT_INSTRUCTIONS.md
├── SKILL.md
└── README.md
```

Copy `MANUS/PROJECT_INSTRUCTIONS.md` into the Manus Project Instructions for the target project. Import `MANUS/SKILL.md` as a Manus Skill when appropriate. Review Skills and bundled scripts before importing or executing them.

See [Manus Integration](MANUS/README.md) for details.

## 🚀 Quick Start

Clone the public distribution repository in the project you want to configure:

### Windows / PowerShell

```powershell
git clone https://github.com/eaglesjo/codingStandard.git
powershell -ExecutionPolicy Bypass -File .\codingStandard\scripts\install-domains.ps1 -Target .
```

Explicit installation:

```powershell
powershell -ExecutionPolicy Bypass -File .\codingStandard\scripts\install-domains.ps1 -Target . -Language en -Domain all
powershell -ExecutionPolicy Bypass -File .\codingStandard\scripts\install-domains.ps1 -Target . -Language ko -Domain vision
```

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

Arguments are:

```text
target language domain conflict-policy dry-run
```

Use `-DryRun` on PowerShell to preview changes. Existing files can use `-ConflictAction Ask|Merge|Overwrite|Skip`.

For the full Korean installation instructions, see [`i18n/ko/INSTALL.md`](i18n/ko/INSTALL.md).

## 📦 Installation Domains

| Domain | Installs |
|---|---|
| `common` | Common only |
| `llm` | Common + LLM |
| `vision` | Common + Vision |
| `all` | Common + LLM + Vision |

## 🧭 AI Development Workflow

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

## 🧠 Environment and Resource Optimization

Runtime decisions are based on measured capabilities rather than a named machine profile. The shared profiler considers OS, Python/runtime, CPU, RAM, disk, accelerators, VRAM, CUDA/ROCm/MPS/DirectML, precision capability, and Jupyter/Colab state.

Use `COMMON/environment.py` as the shared environment source. LLM and Vision expose adapters and policies on top of it.

For long-running ML work, use conservative runtime settings, Memory Smoke Tests, Early Stopping where meaningful, best Checkpoint, Resume, controlled Ablation Study, seed control, resource tracking, and staged recovery from resource failures.

## 🧩 Common / LLM / Vision

- `COMMON/` — shared rules and runtime utilities.
- `LLM/` — language-model and NLP workflows.
- `VISION/` — computer-vision workflows including classification, detection, segmentation, OCR, pose estimation, image generation, and VLM.

### Skills

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

Skills are task-specific and should be loaded only when relevant.

## 🧪 Validation

Run the relevant checks before publishing a release:

```bash
python scripts/validate.py
python scripts/check_i18n.py
python scripts/test_installers.py
```

For ML workloads, run the relevant LLM/Vision Memory Smoke Test before long-running training.

### Platform validation

GitHub Actions validates installers on Windows using both Windows PowerShell and PowerShell 7. The test matrix covers English/Korean, Common/LLM/Vision/All, dry-run, merge preservation, Unicode/space paths, and legacy-installer removal.

Google Colab validation is provided as a runnable notebook:

[Open the Colab validation notebook](https://colab.research.google.com/github/eaglesjo/codingStandard/blob/main/tests/colab/codingstandard_colab_test.ipynb)

## 📚 Documentation

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

## 📄 License

This project is released under the [MIT License](LICENSE).

## 🔗 Public Distribution

The validated public distribution is maintained separately:

**[`eaglesjo/codingStandard`](https://github.com/eaglesjo/codingStandard)**

Releases are published from this private development repository after validation.
