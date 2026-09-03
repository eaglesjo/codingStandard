# codingStandard Development Guide

This document describes the public development and contribution model for `codingStandard`.

## Repository model

The public distribution repository is the release artifact for `codingStandard`. Development work is validated in the project source repository before publication.

## Development flow

```text
feature work / fixes
  ↓
CI GREEN
  ↓
final validation
  ↓
release
  ↓
public distribution
```

## Canonical structure

Shared resources live under `core/common/`, domain resources live under `domains/`, human-facing documentation lives under `docs/`, and executable tooling lives under `scripts/`.

Avoid recreating legacy top-level domain directories such as `COMMON/`, `LLM/`, `VISION/`, or `MANUS/` and obsolete release staging files.

## Validation

Before proposing a release or substantial documentation change, run the repository validation and installer tests described in `INSTALL.md` and the project README.

## Documentation and localization

English is the canonical source of truth. Localized documentation may be provided for supported documentation locales. Runtime resource support is tracked separately and must not be inferred from documentation availability.
