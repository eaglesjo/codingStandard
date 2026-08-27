from __future__ import annotations

import ast
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REQUIRED = [
    "VISION/AGENT.md",
    "VISION/SKILL.md",
    "VISION/ENVIRONMENT.md",
    "VISION/memory_smoke_test.py",
    "VISION/config/training.yaml",
    "VISION/config/ablation.yaml",
]

SKILLS = ["classification", "detection", "segmentation", "ocr", "image-generation", "vlm", "pose-estimation"]


def main() -> int:
    missing = [p for p in REQUIRED if not (ROOT / p).is_file()]
    missing += [f"VISION/skills/{s}/SKILL.md" for s in SKILLS if not (ROOT / f"VISION/skills/{s}/SKILL.md").is_file()]
    if missing:
        print("Missing Vision files:", *missing, sep="\n  ")
        return 1
    for p in [ROOT / "VISION/memory_smoke_test.py"]:
        ast.parse(p.read_text(encoding="utf-8"))
    print("Vision domain validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
