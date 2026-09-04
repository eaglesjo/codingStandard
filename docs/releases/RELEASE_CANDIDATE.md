# Release Candidate

This file marks the repository as ready for final pre-release validation. Do not publish a version tag until the required CI and platform checks pass.

## Required checks

- repository validation
- multilingual i18n parity
- installer integration, lifecycle, and fresh-project E2E tests
- Windows PowerShell validation on `windows-latest`
- deterministic RAG integration and quality gate
- LLM QLoRA strategy and CPU memory smoke tests
- Vision CPU memory smoke test
- Google Colab runtime and notebook validation

## v1.13.0 focus

- installation manifest creation and ownership hashes
- installation state and modified/missing file detection
- update and obsolete-file reconciliation
- safe uninstall and explicit force mode

## Release version

1.13.0
