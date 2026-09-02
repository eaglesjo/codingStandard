# Repository Structure Contract

This document defines the canonical layout of `codingStandard-private` and the public distribution boundary.

## Canonical layout

```text
.
├── core/
│   └── common/                 # shared rules and common environment tooling
├── domains/
│   ├── ml/                    # cross-domain ML/DL lifecycle resources
│   ├── llm/                   # LLM/NLP domain resources
│   └── vision/                # vision/VLM domain resources
├── platform/
│   └── colab/                 # ephemeral Google Colab/cloud notebook execution policy
├── docs/
│   ├── development/           # development and architecture guidance
│   └── releases/              # release planning, status, and notes
├── i18n/
│   ├── ko/                    # Korean localized distribution tree
│   └── README.md              # localization guidance
├── scripts/
│   ├── development/           # developer utilities
│   ├── installers/            # installation and installer integration tests
│   └── validation/            # repository and localization validation
├── tests/
│   └── colab/                 # Colab-specific validation assets
├── VERSION                    # current development version; single source of truth
├── README.md                  # English entrypoint
└── LICENSE
```

## Directory ownership

| Path | Responsibility |
| --- | --- |
| `core/common/` | Shared rules, environment contracts, and common tooling used across domains. |
| `domains/ml/` | Cross-domain ML/DL rules and Skills for data, experiments, evaluation, training, inference, distributed execution, HPO, and model lifecycle. |
| `domains/llm/` | LLM/NLP instructions, environment, skills, experiments, configuration, and smoke tests. |
| `domains/vision/` | Vision/VLM instructions, environment, skills, experiments, configuration, and smoke tests. |
| `platform/colab/` | Execution policy for ephemeral hosted notebook runtimes such as Google Colab. |
| `docs/development/` | Human-facing development, architecture, and repository-structure documentation. |
| `docs/releases/` | Release notes, release status, candidate planning, and release procedure. |
| `i18n/ko/` | Korean mirror of resources included in the localization contract. |
| `scripts/development/` | Non-installation developer utilities. |
| `scripts/installers/` | Cross-platform installation scripts and installer integration tests. |
| `scripts/validation/` | Repository, localization, and structure validation. |
| `tests/colab/` | Notebook and test assets specific to Google Colab validation. |

## Agent routing

AI tool-specific entrypoints are adapters only. The canonical policy chain is:

```text
Agent adapter
  ↓
AGENTS.md
  ↓
core/common
  ↓
relevant domain(s)
  ↓
platform policy when applicable
  ↓
task-specific Skills
```

Cross-domain ML lifecycle policy belongs under `domains/ml/` rather than being duplicated inside LLM, Vision, or tool-specific adapter files.

## Root-level compatibility rule

Some dot-directories and root files must remain at conventional locations because external tools discover them by name, including `.github/`, `.cursor/`, `.clinerules/`, `.continue/`, `.junie/`, `.windsurf/`, `.amazonq/`, `.aider.conf.yml`, `AGENTS.md`, `CLAUDE.md`, and `GEMINI.md`.

These are compatibility entrypoints, not general project content. They must not be moved into an arbitrary grouping directory unless the consuming tool explicitly supports the new location.

## Release boundary

The public repository is a distribution artifact, not a second development tree. Private development-only documentation under `docs/development/` and private agent/tooling resources are excluded by the publish workflow.

`VERSION` is the only mutable version source. Historical releases are represented by Git tags and release documentation; files such as `VERSION-1.4.0` or `FINAL_VERSION.txt` must not be recreated.

## Legacy paths

The following paths are prohibited in new changes:

```text
COMMON/
LLM/
MANUS/
VISION/
DEVELOPMENT.md
RELEASE.md
RELEASE_CANDIDATE.md
RELEASE_NOTES.md
RELEASE_STATUS.md
FINAL_VERSION.txt
VERSION-*
scripts/validate.py
scripts/check_i18n.py
scripts/test_installers.py
scripts/test_installers_windows.ps1
```

Validation and installer code must use the canonical paths above. If a compatibility shim is ever required, it must be explicitly documented and tested rather than silently recreating the legacy tree.
