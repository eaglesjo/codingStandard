#!/usr/bin/env python3
"""Validate the localized Korean project-rule set against the English source tree."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
KO = ROOT / "i18n" / "ko"

REQUIRED_LOCALIZED = {
    "AGENTS.md", "CLAUDE.md", "GEMINI.md",
    ".github/copilot-instructions.md",
    ".github/instructions/llm.instructions.md",
    ".cursor/rules/coding-standard.mdc",
    ".windsurf/rules/coding-standard.md",
    ".clinerules/01-coding-standard.md",
    ".continue/rules/01-coding-standard.md",
    ".junie/AGENTS.md",
    ".amazonq/rules/coding-standard.md",
    "CONVENTIONS.md", ".aider.conf.yml",
    "COMMON/AGENT.md", "COMMON/SKILL.md", "COMMON/ENVIRONMENT.md",
    "LLM/AGENT.md", "LLM/SKILL.md", "LLM/ENVIRONMENT.md", "LLM/README.md",
    "VISION/AGENT.md", "VISION/SKILL.md", "VISION/ENVIRONMENT.md", "VISION/README.md",
    "VISION/config/training.yaml", "VISION/config/ablation.yaml",
}

REQUIRED_ENGLISH_SOURCE = {Path(path) for path in REQUIRED_LOCALIZED}
CORE_CONCEPTS = ("environment", "memory", "early stopping", "checkpoint", "ablation")


def main() -> int:
    if not KO.is_dir():
        print("ERROR: i18n/ko is required", file=sys.stderr)
        return 1

    missing_en = [str(path) for path in sorted(REQUIRED_ENGLISH_SOURCE) if not (ROOT / path).is_file()]
    missing_ko = [str(path) for path in sorted(REQUIRED_LOCALIZED) if not (KO / path).is_file()]
    if missing_en or missing_ko:
        if missing_en:
            print("Missing English source files:", *missing_en, sep="\n  ")
        if missing_ko:
            print("Missing Korean files:", *missing_ko, sep="\n  ")
        return 1

    errors = 0
    for rel in sorted(REQUIRED_ENGLISH_SOURCE):
        en = (ROOT / rel).read_text(encoding="utf-8").lower()
        ko = (KO / rel).read_text(encoding="utf-8").lower()
        for concept in CORE_CONCEPTS:
            if concept not in en or concept not in ko:
                print(f"Missing core concept '{concept}' in {rel}")
                errors += 1

    if errors:
        return 1
    print("i18n parity OK: English source and Korean localized files verified")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
