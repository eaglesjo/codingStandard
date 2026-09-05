# AI Engineering Standard

<p align="center">
  <strong>AI Development, Training & Agent Engineering Standards</strong>
</p>

<p align="center">
  <a href="https://github.com/eaglesjo/codingStandard/releases"><img src="https://img.shields.io/github/v/release/eaglesjo/codingStandard?label=public%20release" alt="Public release"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-yellow.svg" alt="MIT License"></a>
</p>

**Language:** English · [한국어](i18n/ko/README.md) · [Français](i18n/fr/README.md) · [Español](i18n/es/README.md) · [简体中文](i18n/zh-CN/README.md) · [日本語](i18n/ja/README.md) · [Русский](i18n/ru/README.md) · [Türkçe](i18n/tr/README.md) · [Deutsch](i18n/de/README.md) · [Italiano](i18n/it/README.md) · [Português](i18n/pt/README.md) · [العربية](i18n/ar/README.md) · [हिन्दी](i18n/hi/README.md) · [Bahasa Indonesia](i18n/id/README.md) · [Tiếng Việt](i18n/vi/README.md) · [ไทย](i18n/th/README.md) · [Nederlands](i18n/nl/README.md) · [Polski](i18n/pl/README.md) · [Svenska](i18n/sv/README.md) · [Українська](i18n/uk/README.md)

> **v1.15.0:** codingStandard now provides validated runtime resources for **20 locales**. Non-English runtime locales use English as the fallback language when a localized resource is unavailable.
>
> **Repository model:** `codingStandard-private` is the development source of truth. Validated releases are promoted through `codingStandard-dev` to the stable public [`eaglesjo/codingStandard`](https://github.com/eaglesjo/codingStandard) repository.

## ✨ What is AI Engineering Standard?

`codingStandard` is a reusable engineering standard for AI-assisted development, model training, experimentation, LLM/Vision workflows, general ML/DL workflows, and AI coding agents.

It provides:

- canonical project instructions with thin per-tool adapters;
- common ML/DL lifecycle guidance;
- LLM and Vision domain guidance;
- task-specific Skills;
- measured environment and resource detection;
- Google Colab execution and recovery policy;
- cross-platform installers;
- multilingual documentation and runtime resources;
- validation and installer test suites;
- reproducible training and experiment guidance.

## 🌍 Language support

The v1.15 runtime resource set contains 20 locales:

| Locale | Language | Runtime |
|---|---|---|
| `en` | English | ✅ |
| `ko` | 한국어 | ✅ |
| `fr` | Français | ✅ |
| `es` | Español | ✅ |
| `zh-CN` | 简体中文 | ✅ |
| `ja` | 日本語 | ✅ |
| `ru` | Русский | ✅ |
| `tr` | Türkçe | ✅ |
| `de` | Deutsch | ✅ |
| `it` | Italiano | ✅ |
| `pt` | Português | ✅ |
| `ar` | العربية | ✅ |
| `hi` | हिन्दी | ✅ |
| `id` | Bahasa Indonesia | ✅ |
| `vi` | Tiếng Việt | ✅ |
| `th` | ไทย | ✅ |
| `nl` | Nederlands | ✅ |
| `pl` | Polski | ✅ |
| `sv` | Svenska | ✅ |
| `uk` | Українська | ✅ |

The canonical locale registry is [`i18n/languages.json`](i18n/languages.json). Runtime resources are checked by the i18n parity validator before release.

## 🤖 Supported AI Development Tools

The repository provides project-level adapters, instruction files, Skills, or documented integration paths for a broad set of AI development tools.

- OpenAI Codex
- Claude Code
- Gemini CLI
- GitHub Copilot
- Cursor
- Windsurf
- Cline
- Continue
- JetBrains Junie
- Amazon Q Developer
- Aider

Support means that the repository contains a documented adapter, instruction file, Skill, or integration path for the tool. Tool capabilities and integration details can differ by client and version.

## 🐍 Supported Development Environments

| Environment / Tool | Support | Use case |
|---|---|---|
| Python | ✅ Core | Runtime detection, environment configuration, training, inference, validation, and automation |
| Jupyter Notebook | ✅ Supported | Interactive experiments, analysis, training, debugging, and reproducible notebook workflows |
| Google Colab | ✅ Supported | Ephemeral cloud notebook execution, resource-aware experiments, durable checkpoints, and recovery |
| Visual Studio Code | ✅ Supported | Python development, Jupyter notebooks, debugging, testing, and AI-assisted development |

### Platform support

| Platform | Role |
|---|---|
| Linux | Supported platform; the shell installer is designed for Linux-compatible environments |
| Ubuntu 24.04 LTS | Linux reference environment used by CI validation |
| macOS | Supported and validated by CI |
| Windows | Supported and validated with Windows PowerShell and PowerShell 7 |
| Google Colab | Supported as an ephemeral cloud execution target |

> **Important:** Linux is the supported platform category. **Ubuntu 24.04 LTS is the CI reference environment**, not a restriction that excludes other Linux distributions.

## 🚀 Quick Start

Clone the stable public distribution repository in the project you want to configure:

### Windows / PowerShell

```powershell
git clone https://github.com/eaglesjo/codingStandard.git
powershell -ExecutionPolicy Bypass -File .\codingStandard\scripts\installers\install-domains.ps1 -Target .
```

Explicit language installation:

```powershell
powershell -ExecutionPolicy Bypass -File .\codingStandard\scripts\installers\install-domains.ps1 -Target . -Language de -Domain all
powershell -ExecutionPolicy Bypass -File .\codingStandard\scripts\installers\install-domains.ps1 -Target . -Language ko -Domain ml
powershell -ExecutionPolicy Bypass -File .\codingStandard\scripts\installers\install-domains.ps1 -Target . -Language ja -Domain llm
```

### Linux / macOS

```bash
git clone https://github.com/eaglesjo/codingStandard.git
bash ./codingStandard/scripts/installers/install-domains.sh .
```

Explicit installation:

```bash
bash ./codingStandard/scripts/installers/install-domains.sh . de all ask false
bash ./codingStandard/scripts/installers/install-domains.sh . ko ml overwrite false
bash ./codingStandard/scripts/installers/install-domains.sh . ja llm overwrite false
```

Arguments are:

```text
target language domain conflict-policy dry-run
```

Available domains:

```text
common | ml | llm | vision | colab | all
```

## 📦 Installation Domains

| Domain | Installs |
|---|---|
| `common` | Common only |
| `ml` | Common + general ML/DL lifecycle |
| `llm` | Common + LLM |
| `vision` | Common + Vision |
| `colab` | Common + Google Colab runtime policy |
| `all` | Common + ML + LLM + Vision + Colab |

Every successful install records ownership and hashes in `.codingstandard/installation.json`. See [`docs/development/INSTALLER_LIFECYCLE.md`](docs/development/INSTALLER_LIFECYCLE.md) for manifest and lifecycle behavior.

## 🧭 Repository Structure

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
│   ├── en/
│   ├── ko/
│   ├── fr/
│   ├── es/
│   ├── zh-CN/
│   ├── ja/
│   ├── ru/
│   ├── tr/
│   ├── de/
│   ├── it/
│   ├── pt/
│   ├── ar/
│   ├── hi/
│   ├── id/
│   ├── vi/
│   ├── th/
│   ├── nl/
│   ├── pl/
│   ├── sv/
│   └── uk/
├── scripts/
│   ├── development/
│   ├── installers/
│   └── validation/
├── tests/
│   └── colab/
├── .github/
└── VERSION
```

Tool-specific entrypoints are adapters; shared ML lifecycle policy lives in `domains/ml/`, LLM/Vision add domain-specific behavior, and `platform/colab/` adds ephemeral-runtime policy.

## 🧠 Environment, ML, and Colab Policy

Runtime decisions are based on measured capabilities rather than a named machine profile. The shared profiler considers OS, Python/runtime, CPU, RAM, disk, accelerators, VRAM, CUDA/ROCm/MPS/DirectML, precision capability, and Jupyter/Colab state.

For long-running ML work, use conservative runtime settings, Memory Smoke Tests, Early Stopping where meaningful, best Checkpoint, Resume, controlled ablation/experiment design, seed control, evaluation gates, resource tracking, and staged recovery from resource failures.

For Google Colab, `platform/colab/` treats the notebook VM as ephemeral: dependency bootstrap, measured resource resolution, smoke testing, durable checkpointing, artifact persistence, and resume validation are first-class controls.

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

The release gate also validates the architecture contract, environment contract, installers, and CPU LLM/Vision memory smoke tests.

### ☁️ Google Colab — one-click validation

Open the notebooks directly from GitHub in Google Colab. No private-repository credentials are required for the public distribution repository.

| Validation | Purpose |
|---|---|
| Full codingStandard | Runtime, environment, LLM/Vision smoke tests and repository validation |
| Clean runtime | Fresh-runtime environment and checkpoint/restore smoke test |
| LLM QLoRA | 4-bit/NF4 + PEFT/LoRA runtime validation |
| RAG | Dense embeddings + top-k retrieval + grounded prompt + generation |

## 📚 Documentation

- [Installation Guide](INSTALL.md)
- [Installer Lifecycle](docs/development/INSTALLER_LIFECYCLE.md)
- [Korean Installation Guide](i18n/ko/INSTALL.md)
- [Repository Structure](docs/development/REPOSITORY_STRUCTURE.md)
- [Public Development Guide](docs/development/DEVELOPMENT_PUBLIC.md)
- [Architecture Profiles](docs/development/ARCHITECTURE_PROFILES.md)
- [Policy Inheritance](docs/development/POLICY_INHERITANCE.md)
- [Project Profiles](docs/development/PROJECT_PROFILES.md)
- [Scalability Architecture](docs/development/SCALABILITY_ARCHITECTURE.md)
- [Language Registry](i18n/languages.json)

## 📄 License

This project is released under the [MIT License](LICENSE).

## 🔗 Public Distribution

Stable releases are published to [`eaglesjo/codingStandard`](https://github.com/eaglesjo/codingStandard) after validation and promotion from this development repository.
