# 1.12.0 Release

This release strengthens codingStandard's runtime quality gates, multilingual resource integrity, and installer reliability for fresh projects.

## Highlights

- Align README documentation with the actual five-locale runtime resource contract.
- Add deterministic RAG evaluation thresholds and regression quality gating.
- Expand multilingual i18n runtime resource parity validation across `en`, `ko`, `zh-CN`, `ja`, and `ru`.
- Add fresh-project installer end-to-end coverage for all runtime locales and installer domains.
- Validate installer fallback, reinstall idempotence, and merge/overwrite/skip conflict behavior.
- Run installer E2E validation across Ubuntu, macOS, and Windows PowerShell CI paths.
- Bump development version to `1.12.0`.

## Validation

Final validation covers repository structure, language catalog, multilingual parity, routing, Colab runtime/notebooks, installer integration and fresh-project E2E, deterministic RAG evaluation, LLM/Vision smoke tests, and Windows PowerShell installer validation.

## Scope

No installer runtime behavior changes are included in this release preparation; the installer work is validation-focused.

## v1.13.0

- Introduce a cross-platform installation manifest at `.codingstandard/installation.json`.
- Record the installed version, locale, domain, source hashes, and installed file hashes.
- Add installation state inspection with modified/missing file detection.
- Add update commands that reapply the recorded installation configuration and refresh managed resources.
- Add safe uninstall with modification protection and explicit `--force` recovery.
- Keep the existing install CLI positional arguments compatible while routing both shell and PowerShell through one lifecycle engine.
