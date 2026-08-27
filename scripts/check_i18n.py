#!/usr/bin/env python3
"""Validate required English/Korean documents and core rule coverage."""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EN = ROOT / "i18n" / "en"
KO = ROOT / "i18n" / "ko"
REQUIRED_LOCALIZED = {"AGENT.md", "SKILL.md", "ENVIRONMENT.md", "README.md"}
CORE_TERMS = (
    "environment",
    "memory",
    "early stopping",
    "checkpoint",
    "ablation",
)


def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text.lower())


def main() -> int:
    if not EN.is_dir() or not KO.is_dir():
        print("ERROR: i18n/en and i18n/ko are required", file=sys.stderr)
        return 1

    missing = []
    for rel in sorted(REQUIRED_LOCALIZED):
        en_path = EN / rel
        ko_path = KO / rel
        if not en_path.is_file():
            missing.append(f"i18n/en/{rel}")
        if not ko_path.is_file():
            missing.append(f"i18n/ko/{rel}")
    if missing:
        print("Missing localized files:", *missing, sep="\n  ", file=sys.stderr)
        return 1

    errors = 0
    for rel in sorted(REQUIRED_LOCALIZED):
        en_text = normalize((EN / rel).read_text(encoding="utf-8"))
        ko_text = normalize((KO / rel).read_text(encoding="utf-8"))
        for term in CORE_TERMS:
            if term not in en_text:
                print(f"Missing core term in English {rel}: {term}")
                errors += 1
            if term not in ko_text:
                print(f"Missing core term in Korean {rel}: {term}")
                errors += 1

    if errors:
        return 1
    print("i18n parity OK: required files and core rule coverage verified")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
