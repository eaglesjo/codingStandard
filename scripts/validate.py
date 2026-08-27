from __future__ import annotations

import ast
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_KO = {
    "AGENTS.md",
    "CLAUDE.md",
    "GEMINI.md",
    ".github/copilot-instructions.md",
    ".github/instructions/llm.instructions.md",
    ".cursor/rules/coding-standard.mdc",
    ".windsurf/rules/coding-standard.md",
    ".clinerules/01-coding-standard.md",
    ".continue/rules/01-coding-standard.md",
    ".junie/AGENTS.md",
    ".amazonq/rules/coding-standard.md",
    "CONVENTIONS.md",
    ".aider.conf.yml",
    "LLM/AGENT.md",
    "LLM/SKILL.md",
    "LLM/ENVIRONMENT.md",
    "LLM/README.md",
    "LLM/config/training.yaml",
    "LLM/config/ablation.yaml",
    "LLM/skills/environment/SKILL.md",
    "LLM/skills/training/SKILL.md",
    "LLM/skills/ablation/SKILL.md",
    "LLM/skills/notebook/SKILL.md",
    "LLM/skills/debugging/SKILL.md",
    "LLM/skills/release/SKILL.md",
}

FORBIDDEN_HARDWARE_PATTERNS = [
    re.compile(r"RTX\s*3050", re.I),
    re.compile(r"3050\s*Ti", re.I),
    re.compile(r"4\s*GB\s*VRAM", re.I),
    re.compile(r"16\s*GB\s*(RAM|System RAM)", re.I),
]


def fail(message: str) -> None:
    print(f"ERROR: {message}")
    raise SystemExit(1)


def check_python() -> None:
    for path in ROOT.rglob("*.py"):
        if ".git" in path.parts:
            continue
        try:
            ast.parse(path.read_text(encoding="utf-8"))
        except SyntaxError as exc:
            fail(f"Python syntax error in {path}: {exc}")


def check_language_parity() -> None:
    ko_root = ROOT / "i18n" / "ko"
    if not ko_root.exists():
        fail("Missing i18n/ko")
    missing = [p for p in sorted(REQUIRED_KO) if not (ko_root / p).is_file()]
    if missing:
        fail("Missing Korean templates: " + ", ".join(missing))


def check_hardware_neutrality() -> None:
    targets = [ROOT / "AGENTS.md", ROOT / "LLM"]
    for target in targets:
        paths = [target] if target.is_file() else list(target.rglob("*.md"))
        for path in paths:
            text = path.read_text(encoding="utf-8")
            for pattern in FORBIDDEN_HARDWARE_PATTERNS:
                if pattern.search(text):
                    fail(f"Machine-specific hardware assumption in {path}: {pattern.pattern}")


def check_required_files() -> None:
    required = [ROOT / "VERSION", ROOT / "LLM" / "environment.py", ROOT / "LLM" / "experiment.py"]
    missing = [str(p.relative_to(ROOT)) for p in required if not p.is_file()]
    if missing:
        fail("Missing required files: " + ", ".join(missing))


def main() -> None:
    check_required_files()
    check_language_parity()
    check_python()
    check_hardware_neutrality()
    print("codingStandard validation passed")


if __name__ == "__main__":
    main()
