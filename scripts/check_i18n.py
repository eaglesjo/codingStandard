#!/usr/bin/env python3
"""Check that English and Korean template sets contain the same files and headings."""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EN = ROOT / "i18n" / "en"
KO = ROOT / "i18n" / "ko"

SKIP_DIRS = {"__pycache__"}

def files(root: Path) -> set[str]:
    return {
        p.relative_to(root).as_posix()
        for p in root.rglob("*")
        if p.is_file() and not (set(p.parts) & SKIP_DIRS)
    }

def headings(path: Path) -> list[str]:
    if path.suffix.lower() != ".md":
        return []
    text = path.read_text(encoding="utf-8")
    return [m.group(2).strip() for m in re.finditer(r"^(#{1,6})\s+(.+?)\s*$", text, re.MULTILINE)]

def normalized_headings(values: list[str]) -> list[str]:
    # Compare structure, not translated wording.
    return [re.sub(r"[^a-z0-9]+", " ", value.lower()).strip() for value in values]

def main() -> int:
    if not EN.is_dir() or not KO.is_dir():
        print("ERROR: i18n/en and i18n/ko are required", file=sys.stderr)
        return 1

    en_files = files(EN)
    ko_files = files(KO)
    missing_ko = sorted(en_files - ko_files)
    extra_ko = sorted(ko_files - en_files)
    if missing_ko or extra_ko:
        if missing_ko:
            print("Missing in i18n/ko:", *missing_ko, sep="\n  ")
        if extra_ko:
            print("Extra in i18n/ko:", *extra_ko, sep="\n  ")
        return 1

    errors = 0
    for rel in sorted(en_files):
        en_path = EN / rel
        ko_path = KO / rel
        if en_path.suffix.lower() == ".md":
            en_h = headings(en_path)
            ko_h = headings(ko_path)
            if len(en_h) != len(ko_h):
                print(f"Heading count mismatch: {rel} (en={len(en_h)}, ko={len(ko_h)})")
                errors += 1

    if errors:
        return 1
    print(f"i18n parity OK: {len(en_files)} files")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
