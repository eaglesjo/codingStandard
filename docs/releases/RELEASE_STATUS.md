Release development target: 1.13.0.

Status: final pre-release validation; complete repository, installer lifecycle, localization, platform, and RAG quality-gate checks before tagging.

Validation focus:
- canonical Agent adapter routing
- multilingual runtime resource parity
- ML/LLM/Vision domain resource completeness
- Colab runtime policy and notebook validation
- installer dry-run/merge/overwrite/skip behavior
- installation manifest creation and state inspection
- update and obsolete managed-file reconciliation
- safe uninstall with modification protection and force mode
- fresh-project installer E2E across runtime locales
- deterministic RAG regression and quality gate
- existing LLM/Vision regression coverage
