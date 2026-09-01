# 1.7.0 Development Release

This release expands the coding standard from LLM/Vision-centric training guidance to a reusable ML/DL lifecycle and makes Google Colab an explicit ephemeral execution target.

## Highlights

- Add `domains/ml/` for cross-domain data validation, experiment design, evaluation, training, distributed training, HPO, inference, and MLOps policy.
- Add `platform/colab/` for reproducible bootstrap, measured runtime configuration, durable checkpoints/artifacts, interruption recovery, and Resume validation.
- Add LLM Fine-Tuning, PEFT, and Quantization Skills.
- Normalize Claude, Gemini, Copilot, Cursor, Windsurf, Cline, Continue, Junie, and Amazon Q adapters to canonical `core/common` + `domains/*` paths.
- Extend installers and installer tests for `ml` and `colab` domains.
- Align Korean top-level Agent/installer documentation with the new canonical routing.
- Bump development version to `1.7.0`.

## Validation intent

Before tagging a release, repository validation, installer integration, localization checks, platform checks, and Colab notebook validation must pass. Long-running ML validation should also exercise the relevant data, smoke-test, evaluation, checkpoint/resume, and reproducibility contracts.

# 1.4.1 Release Candidate

Patch release following the 1.4.0 baseline. This release includes installer and localization parity fixes, complete Korean executable mirrors, Windows PowerShell 5.1/7 validation, and strengthened i18n checks.

Final pre-release validation covers repository checks, localization parity, installer integration, Windows PowerShell, LLM/Vision smoke tests, and Google Colab validation.
