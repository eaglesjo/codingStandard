#!/usr/bin/env python3
"""Validate the required English/Korean documentation pairs."""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EN = ROOT / "i18n" / "en"
KO = ROOT / "i18n" / "ko"

REQUIRED_LOCALIZED = {"AGENT.md", "SKILL.md", "ENVIRONMENT.md", "README.md"}


def headings(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    return re.findall(r"^#{1,6}\s+.+$", text, re.MULTILINE)


def main() -> int:
    if not EN.is_dir() or not KO.is_dir():
        print("ERROR: i18n/en and i18n/ko are required", file=sys.stderr)
        return 1

    missing = []
    for rel in sorted(REQUIRED_LOCALIZED):
        if not (EN / rel).is_file():
            missing.append(f"i18n/en/{rel}")
        if not (KO / rel).is_file():
            missing.append(f"i18n/ko/{rel}")
    if missing:
        print("Missing localized files:", *missing, sep="\n  ", file=sys.stderr)
        return 1

    errors = 0
    for rel in sorted(REQUIRED_LOCALIZED):
        en_h = headings(EN / rel)
        ko_h = headings(KO / rel)
        if len(en_h) != len(ko_h):
            print(f"Heading count mismatch: {rel} (en={len(en_h)}, ko={len(ko_h)})")
            errors += 1

    print("i18n parity OK: " + ", ".join(sorted(REQUIRED_LOCALIZED)))
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
