# codingStandard

**AI Development Standard for ML / LLM / Vision / Colab**

> v1.16 focuses on multilingual quality: resource completeness, semantic policy parity, and runtime/documentation consistency across 20 runtime locales.

**English** is the canonical documentation language, and `en` is one of the 20 validated runtime locales.

## 🎯 Goal

codingStandard is a repository-level engineering standard designed to make AI development **portable, reproducible, hardware-neutral, and validation-driven**.

## 🧩 Supported Domains

- **ML** — data, evaluation, experiment, training, distributed training, HPO, inference, MLOps
- **LLM** — fine-tuning, PEFT, quantization, RAG
- **Vision** — computer vision workflows and memory validation
- **Colab** — runtime validation and reproducible notebook workflows

## 🌍 Language selector

Runtime resources are validated for 20 locales:

`en` · `ko` · `fr` · `es` · `zh-CN` · `ja` · `ru` · `tr` · `de` · `it` · `pt` · `ar` · `hi` · `id` · `vi` · `th` · `nl` · `pl` · `sv` · `uk`

## 📚 Documentation

- [Installation](INSTALL.md)
- [Development](docs/development/)
- [Architecture Profiles](docs/development/ARCHITECTURE_PROFILES.md)
- [Policy Inheritance](docs/development/POLICY_INHERITANCE.md)
- [Project Profiles](docs/development/PROJECT_PROFILES.md)
- [Scalability Architecture](docs/development/SCALABILITY_ARCHITECTURE.md)
- [Repository Structure](docs/development/REPOSITORY_STRUCTURE.md)
- [i18n Quality](docs/development/I18N_QUALITY.md)
- [i18n Semantic Parity](docs/development/I18N_SEMANTIC_PARITY.md)
- [i18n Runtime / Documentation Consistency](docs/development/I18N_CONSISTENCY.md)

## 🔧 Installation

```bash
./scripts/installers/install-domains.sh
```

Windows:

```powershell
./scripts/installers/install-domains.ps1
```

## 🧪 Validation

The release gate validates architecture, repository structure, environment contracts, installers, i18n resource completeness, semantic parity, runtime/documentation consistency, and CPU smoke tests.

```bash
python scripts/validation/validate.py
```

## 📦 Release

The stable public repository is promoted from the validated development repository. v1.16 uses the development repository as the CI gate and the private repository as the source of truth.
