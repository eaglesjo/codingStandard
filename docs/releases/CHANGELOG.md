# Changelog

## 1.7.0 - 2026-09-01

### Added
- Cross-domain `domains/ml/` lifecycle for data, experiments, evaluation, training, distributed training, HPO, inference, and MLOps.
- Google Colab execution policy for ephemeral runtimes, persistence, recovery, and resume.
- LLM fine-tuning, PEFT, quantization, and RAG Skills.
- Expanded installer and validation coverage for ML/Colab.

### Changed
- Canonicalized AI-agent routing around `AGENTS.md`, `core/common/`, and `domains/*`.
- Updated Korean localization/runtime resources.
- Updated stable PyTorch/torchvision dependency baseline to 2.13.0/0.28.0.
- Removed reliance on obsolete `COMMON/`, `LLM/`, `VISION/`, and legacy script paths.

### Validation
- Ubuntu 24.04: repository, environment, installers, LLM CPU smoke, Vision CPU smoke — passed.
- macOS: repository, environment, installers — passed.
- Windows PowerShell 5.1 and 7: installer integration — passed.
