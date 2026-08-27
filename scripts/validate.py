from __future__ import annotations

import ast
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_KO = {
    "AGENTS.md", "CLAUDE.md", "GEMINI.md", "CONVENTIONS.md", ".aider.conf.yml",
    ".github/copilot-instructions.md", ".github/instructions/llm.instructions.md",
    ".cursor/rules/coding-standard.mdc", ".windsurf/rules/coding-standard.md",
    ".clinerules/01-coding-standard.md", ".continue/rules/01-coding-standard.md",
    ".junie/AGENTS.md", ".amazonq/rules/coding-standard.md",
    "LLM/AGENT.md", "LLM/SKILL.md", "LLM/ENVIRONMENT.md", "LLM/README.md",
    "LLM/config/training.yaml", "LLM/config/ablation.yaml",
    *{f"LLM/skills/{name}/SKILL.md" for name in ("environment", "training", "ablation", "notebook", "debugging", "release")},
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
    checker = ROOT / "scripts" / "check_i18n.py"
    if not checker.is_file():
        fail("Missing scripts/check_i18n.py")
    namespace: dict[str, object] = {}
    exec(compile(checker.read_text(encoding="utf-8"), str(checker), "exec"), namespace)
    main = namespace.get("main")
    if not callable(main) or main() != 0:
        fail("English/Korean localization parity check failed")


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
    required = [
        ROOT / "VERSION",
        ROOT / "LLM" / "environment.py",
        ROOT / "LLM" / "memory_smoke_test.py",
        ROOT / "LLM" / "experiment.py",
        ROOT / "scripts" / "test_installers.py",
    ]
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
