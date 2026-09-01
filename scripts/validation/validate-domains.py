from __future__ import annotations

import ast
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
REQUIRED = [
    "core/common/AGENT.md",
    "core/common/SKILL.md",
    "core/common/ENVIRONMENT.md",
    "domains/ml/AGENT.md",
    "domains/ml/SKILL.md",
    "domains/ml/ENVIRONMENT.md",
    "domains/ml/README.md",
    "domains/llm/AGENT.md",
    "domains/llm/SKILL.md",
    "domains/llm/ENVIRONMENT.md",
    "domains/llm/memory_smoke_test.py",
    "domains/vision/AGENT.md",
    "domains/vision/SKILL.md",
    "domains/vision/ENVIRONMENT.md",
    "domains/vision/memory_smoke_test.py",
    "platform/colab/AGENT.md",
    "platform/colab/SKILL.md",
]
for rel in REQUIRED:
    p = ROOT / rel
    if not p.is_file():
        raise SystemExit(f"Missing: {rel}")

for domain in ("ml", "llm", "vision"):
    for p in (ROOT / "domains" / domain).rglob("*.py"):
        ast.parse(p.read_text(encoding="utf-8"))

print("domain validation passed")
