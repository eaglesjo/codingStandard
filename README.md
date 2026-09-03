# AI Engineering Standard

<p align="center">
  <strong>AI Development, Training & Agent Engineering Standards</strong>
</p>

<p align="center">
  <a href="https://github.com/eaglesjo/codingStandard/releases"><img src="https://img.shields.io/github/v/release/eaglesjo/codingStandard?label=public%20release" alt="Public release"></a>
    <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-yellow.svg" alt="MIT License"></a>
</p>

**Language:** English · [한국어](i18n/ko/README.md) · [Français](i18n/fr/README.md) · [Español](i18n/es/README.md) · [简体中文](i18n/zh-CN/README.md) · [日本語](i18n/ja/README.md) · [Русский](i18n/ru/README.md) · [Türkçe](i18n/tr/README.md)

> **Repository model:** `codingStandard-private` is the development source of truth. Validated releases are published to the public [`eaglesjo/codingStandard`](https://github.com/eaglesjo/codingStandard) repository.
>
> **Runtime resource languages:** English and Korean. Additional languages currently provide documentation entrypoints and will be added to installer/runtime-resource support only after translation and validation parity is complete.

## ✨ What is AI Engineering Standard?

`codingStandard` is a reusable engineering standard for AI-assisted development, model training, experimentation, LLM/Vision workflows, general ML/DL workflows, and AI coding agents.

It provides:

- canonical project instructions with thin per-tool adapters;
- common ML/DL lifecycle guidance;
- LLM and Vision domain guidance;
- task-specific Skills;
- environment and resource detection;
- Google Colab execution/recovery policy;
- cross-platform installers;
- multilingual documentation entrypoints;
- validation and installer test suites;
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
  </tr>
</table>

> Support means that the repository contains a documented adapter, instruction file, Skill, or integration path for the tool. Tool capabilities and integration details can differ by client and version.

## 🐍 Supported Development Environments

AI Engineering Standard is designed to work across local Python development, interactive notebook workflows, cloud notebooks, and AI-assisted IDE workflows.

| Environment / Tool | Support | Use case |
|---|---|---|
| 🐍 **Python** | ✅ Core | Runtime detection, environment configuration, training, inference, validation, and automation |
| 📓 **Jupyter Notebook** | ✅ Supported | Interactive experiments, analysis, training, debugging, and reproducible notebook workflows |
| ☁️ **Google Colab** | ✅ Supported | Ephemeral cloud notebook execution, resource-aware experiments, durable checkpoints, and recovery |
| 💻 **Visual Studio Code** | ✅ Supported | Python development, Jupyter notebooks, debugging, testing, and AI-assisted development |

### Platform support

| Platform | Role |
|---|---|
| **Linux** | Supported platform; the shell installer is designed for Linux-compatible environments |
| **Ubuntu 24.04 LTS** | Linux reference environment used by CI validation |
| **macOS** | Supported and validated by CI |
| **Windows** | Supported and validated with Windows PowerShell and PowerShell 7 |
| **Google Colab** | Supported as an ephemeral cloud execution target |

> **Important:** Linux is the supported platform category. **Ubuntu 24.04 LTS is the CI reference environment**, not a restriction that excludes other Linux distributions.

## 🚀 Quick Start

Clone the public distribution repository in the project you want to configure:

### Windows / PowerShell

```powershell
git clone https://github.com/eaglesjo/codingStandard.git
powershell -ExecutionPolicy Bypass -File .\codingStandard\scripts\installers\install-domains.ps1 -Target .
```

Explicit installation:

```powershell
powershell -ExecutionPolicy Bypass -File .\codingStandard\scripts\installers\install-domains.ps1 -Target . -Language en -Domain all
powershell -ExecutionPolicy Bypass -File .\codingStandard\scripts\installers\install-domains.ps1 -Target . -Language ko -Domain ml
powershell -ExecutionPolicy Bypass -File .\codingStandard\scripts\installers\install-domains.ps1 -Target . -Language en -Domain colab
```

### Linux / macOS

```bash
git clone https://github.com/eaglesjo/codingStandard.git
bash ./codingStandard/scripts/installers/install-domains.sh .
```

Explicit installation:

```bash
bash ./codingStandard/scripts/installers/install-domains.sh . en all ask false
bash ./codingStandard/scripts/installers/install-domains.sh . ko ml overwrite false
bash ./codingStandard/scripts/installers/install-domains.sh . en colab overwrite false
```

Arguments are:

```text
target language domain conflict-policy dry-run
```

Available domains:

```text
common | ml | llm | vision | colab | all
```

Use `-DryRun` on PowerShell to preview changes. Existing files can use `-ConflictAction Ask|Merge|Overwrite|Skip`.

For the full Korean installation instructions, see [`i18n/ko/INSTALL.md`](i18n/ko/INSTALL.md).

## 📦 Installation Domains

| Domain | Installs |
|---|---|
| `common` | Common only |
| `ml` | Common + general ML/DL lifecycle |
| `llm` | Common + LLM |
| `vision` | Common + Vision |
| `colab` | Common + Google Colab runtime policy |
| `all` | Common + ML + LLM + Vision + Colab |

## 🧭 Repository Structure

The repository uses a canonical layered structure. Tool-specific entrypoints are adapters; shared ML lifecycle policy lives in `domains/ml/`, LLM/Vision add domain-specific behavior, and `platform/colab/` adds ephemeral-runtime policy.

```text
.
├── core/
│   └── common/
├── domains/
│   ├── ml/
│   ├── llm/
│   └── vision/
├── platform/
│   └── colab/
├── examples/
│   └── colab/
├── docs/
│   ├── development/
│   └── releases/
├── i18n/
│   ├── ko/
│   ├── fr/
│   ├── es/
│   ├── zh-CN/
│   ├── ja/
│   ├── ru/
│   └── tr/
├── scripts/
│   ├── development/
│   ├── installers/
│   └── validation/
├── tests/
│   └── colab/
├── .github/
└── VERSION
```

Legacy root-level `COMMON/`, `LLM/`, `MANUS/`, `VISION/`, release marker files, and old script paths are not part of the supported layout.

## 🧠 Environment, ML, and Colab Policy

Runtime decisions are based on measured capabilities rather than a named machine profile. The shared profiler considers OS, Python/runtime, CPU, RAM, disk, accelerators, VRAM, CUDA/ROCm/MPS/DirectML, precision capability, and Jupyter/Colab state.

The ML domain adds a common lifecycle for data validation, experiment design, evaluation, training, inference, distributed training, HPO, and model/artifact lineage. LLM and Vision inherit these lifecycle controls and add domain-specific Skills.

For Google Colab, `platform/colab/` treats the notebook VM as ephemeral: dependency bootstrap, measured resource resolution, smoke testing, durable checkpointing, artifact persistence, and resume validation are first-class controls.

For long-running ML work, use conservative runtime settings, Memory Smoke Tests, Early Stopping where meaningful, best Checkpoint, Resume, controlled ablation/experiment design, seed control, evaluation gates, resource tracking, and staged recovery from resource failures.

## 🧩 Agent and Skill Routing

```text
Agent adapter
  ↓
AGENTS.md
  ↓
core/common
  ↓
ML / LLM / Vision domain
  ↓
Colab policy when applicable
  ↓
task-specific Skills
```

Cross-domain rules should be implemented once in `domains/ml/` rather than duplicated in each agent adapter or domain file.

## 🧪 Validation

Run the relevant checks before publishing a release:

```bash
python scripts/validation/validate.py
python scripts/validation/check_i18n.py
python scripts/installers/test_installers.py
```

For ML workloads, run the relevant domain Memory Smoke Test before long-running training. For Colab, use the one-click notebooks below from a fresh runtime.

### ☁️ Google Colab — one-click validation

Open the notebook directly from GitHub in Google Colab. No private-repository credentials are required for the public distribution repository.

| Validation | Purpose | Colab |
|---|---|---|
| Full codingStandard | Runtime, environment, LLM/Vision smoke tests and repository validation | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/eaglesjo/codingStandard/blob/main/tests/colab/codingstandard_colab_test.ipynb) |
| Clean runtime | Fresh-runtime environment and checkpoint/restore smoke test | [Open in Colab](https://colab.research.google.com/github/eaglesjo/codingStandard/blob/main/examples/colab/clean_runtime_validation.ipynb) |
| LLM QLoRA | 4-bit/NF4 + PEFT/LoRA runtime validation | [Open in Colab](https://colab.research.google.com/github/eaglesjo/codingStandard/blob/main/examples/colab/llm_qlora_validation.ipynb) |
| RAG | Dense embeddings + top-k retrieval + grounded prompt + generation | [Open in Colab](https://colab.research.google.com/github/eaglesjo/codingStandard/blob/main/examples/colab/rag_validation.ipynb) |

> Recommended first test: **Full codingStandard**. For the RAG capability specifically, run **RAG** in a fresh Colab runtime.

### Platform validation

GitHub Actions validates the repository on macOS and Ubuntu 24.04 LTS. Windows installer integration is validated using both Windows PowerShell and PowerShell 7. Installer tests cover English/Korean, Common/ML/LLM/Vision/Colab/All, dry-run, merge preservation, Unicode/space paths, and legacy-installer removal.

## 📚 Documentation

- [Installation Guide](INSTALL.md)
- [Korean Installation Guide](i18n/ko/INSTALL.md)
- [Repository Structure](docs/development/REPOSITORY_STRUCTURE.md)
- [Public Development Guide](docs/development/DEVELOPMENT_PUBLIC.md)
- [Common Agent Rules](core/common/AGENT.md)
- [ML Agent Rules](domains/ml/AGENT.md)
- [ML Skill](domains/ml/SKILL.md)
- [ML Environment](domains/ml/ENVIRONMENT.md)
- [LLM Agent Rules](domains/llm/AGENT.md)
- [LLM Skill](domains/llm/SKILL.md)
- [LLM Environment](domains/llm/ENVIRONMENT.md)
- [Vision Agent Rules](domains/vision/AGENT.md)
- [Vision Skill](domains/vision/SKILL.md)
- [Vision Environment](domains/vision/ENVIRONMENT.md)
- [Colab Agent Rules](platform/colab/AGENT.md)
- [Colab Skill](platform/colab/SKILL.md)
- [Windows Installer Test](scripts/installers/test_installers_windows.ps1)
- [Colab Validation](tests/colab/README.md)
- [Korean README](i18n/ko/README.md)
- [French README](i18n/fr/README.md)
- [Spanish README](i18n/es/README.md)
- [Simplified Chinese README](i18n/zh-CN/README.md)
- [Japanese README](i18n/ja/README.md)
- [Russian README](i18n/ru/README.md)
- [Turkish README](i18n/tr/README.md)

## 📄 License

This project is released under the [MIT License](LICENSE).

## 🔗 Public Distribution
