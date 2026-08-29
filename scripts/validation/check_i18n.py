#!/usr/bin/env python3
"""Validate the localized Korean project-rule set against the English source tree."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
KO = ROOT / "i18n" / "ko"

REQUIRED_LOCALIZED = {
    "AGENTS.md", "CLAUDE.md", "GEMINI.md", "INSTALL.md",
    ".github/copilot-instructions.md", ".github/instructions/llm.instructions.md", ".github/instructions/vision.instructions.md",
    ".cursor/rules/coding-standard.mdc", ".windsurf/rules/coding-standard.md", ".clinerules/01-coding-standard.md", ".continue/rules/01-coding-standard.md", ".junie/AGENTS.md", ".amazonq/rules/coding-standard.md",
    "docs/development/CONVENTIONS.md", ".aider.conf.yml",
    "core/common/AGENT.md", "core/common/SKILL.md", "core/common/ENVIRONMENT.md", "core/common/environment.py", "core/common/experiment.py",
    "domains/llm/AGENT.md", "domains/llm/SKILL.md", "domains/llm/ENVIRONMENT.md", "domains/llm/README.md", "domains/llm/environment.py", "domains/llm/experiment.py", "domains/llm/memory_smoke_test.py",
    "domains/vision/AGENT.md", "domains/vision/SKILL.md", "domains/vision/ENVIRONMENT.md", "domains/vision/README.md", "domains/vision/memory_smoke_test.py", "domains/vision/config/training.yaml", "domains/vision/config/ablation.yaml",
    "domains/manus/PROJECT_INSTRUCTIONS.md", "domains/manus/SKILL.md", "domains/manus/README.md",
}
SEMANTIC_DOCUMENTS = {p for p in REQUIRED_LOCALIZED if p.endswith(".md") and p not in {"domains/llm/README.md", "domains/vision/README.md", "domains/manus/README.md"}}
CONCEPT_ALTERNATIVES = {
    "environment": {"en": ("environment", "runtime"), "ko": ("환경", "실행환경", "런타임")},
    "memory": {"en": ("memory", "ram", "vram"), "ko": ("메모리", "램", "브이램")},
    "early stopping": {"en": ("early stopping",), "ko": ("early stopping", "얼리 스토핑", "조기 종료")},
    "checkpoint": {"en": ("checkpoint",), "ko": ("checkpoint", "체크포인트")},
    "ablation": {"en": ("ablation", "ablation study"), "ko": ("ablation", "ablation study", "어브레이션", "어브레이션 스터디")},
}

def contains_any(text: str, alternatives: tuple[str, ...]) -> bool:
    return any(term in text for term in alternatives)

def main() -> int:
    if not KO.is_dir():
        print("ERROR: i18n/ko is required", file=sys.stderr); return 1
    missing_en = [p for p in sorted(REQUIRED_LOCALIZED) if not (ROOT / p).is_file()]
    missing_ko = [p for p in sorted(REQUIRED_LOCALIZED) if not (KO / p).is_file()]
    if missing_en or missing_ko:
        if missing_en: print("Missing English source files:", *missing_en, sep="\n  ", file=sys.stderr)
        if missing_ko: print("Missing Korean files:", *missing_ko, sep="\n  ", file=sys.stderr)
        return 1
    errors = 0
    for rel in sorted(SEMANTIC_DOCUMENTS):
        en_text = (ROOT / rel).read_text(encoding="utf-8").lower(); ko_text = (KO / rel).read_text(encoding="utf-8").lower()
        for concept, alternatives in CONCEPT_ALTERNATIVES.items():
            if contains_any(en_text, alternatives["en"]) and not contains_any(ko_text, alternatives["ko"]):
                print(f"Missing localized core concept '{concept}' in {rel}"); errors += 1
    if errors: return 1
    print("i18n parity OK: English/Korean file presence and document-specific rule anchors verified"); return 0

if __name__ == "__main__": raise SystemExit(main())
