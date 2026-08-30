#!/usr/bin/env python3
"""Validate the canonical public repository layout and reject legacy paths."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

REQUIRED_DIRECTORIES = (
    "core/common",
    "domains/llm",
    "domains/manus",
    "domains/vision",
    "docs/releases",
    "scripts/development",
    "scripts/installers",
    "scripts/validation",
    "tests/colab",
)

LEGACY_PATHS = (
    "COMMON", "LLM", "MANUS", "VISION",
    "DEVELOPMENT.md", "RELEASE.md", "RELEASE_CANDIDATE.md",
    "RELEASE_NOTES.md", "RELEASE_STATUS.md", "FINAL_VERSION.txt",
    "VERSION-1.4.0", "scripts/validate.py", "scripts/check_i18n.py",
    "scripts/test_environment.py", "scripts/test_installers.py",
    "scripts/install-domains.sh", "scripts/install-domains.ps1",
)


def main() -> int:
    errors = []
    for rel in REQUIRED_DIRECTORIES:
        if not (ROOT / rel).is_dir():
            errors.append(f"Missing canonical directory: {rel}")
    for rel in LEGACY_PATHS:
        if (ROOT / rel).exists():
            errors.append(f"Legacy path must not exist: {rel}")
    if errors:
        print("Repository structure validation failed:")
        for error in errors:
            print(f"  - {error}")
        return 1
    print("Repository structure validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
