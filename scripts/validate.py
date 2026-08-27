from __future__ import annotations

import ast
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

FORBIDDEN_HARDWARE_PATTERNS = [
    re.compile(r"RTX\s*3050", re.I),
    re.compile(r"3050\s*Ti", re.I),
    re.compile(r"4\s*GB\s*VRAM", re.I),
    re.compile(r"16\s*GB\s*(RAM|System RAM)", re.I),
]
REQUIRED_FILES = [
    "VERSION",
    "AGENTS.md", "CLAUDE.md", "GEMINI.md", "INSTALL.md",
    "COMMON/AGENT.md", "COMMON/SKILL.md", "COMMON/ENVIRONMENT.md",
    "COMMON/environment.py", "COMMON/experiment.py",
    "LLM/AGENT.md", "LLM/SKILL.md", "LLM/ENVIRONMENT.md",
    "LLM/environment.py", "LLM/memory_smoke_test.py", "LLM/experiment.py",
    "VISION/AGENT.md", "VISION/SKILL.md", "VISION/ENVIRONMENT.md",
    "VISION/memory_smoke_test.py", "VISION/README.md",
    "scripts/install-domains.ps1", "scripts/install-domains.sh",
    "scripts/check_i18n.py", "scripts/test_installers.py",
    "scripts/test_installers_windows.ps1",
    ".github/workflows/windows-install-test.yml",
    "tests/colab/README.md", "tests/colab/codingstandard_colab_test.ipynb",
    "LICENSE",
]


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def check_required_files() -> None:
    missing = [path for path in REQUIRED_FILES if not (ROOT / path).is_file()]
    missing += ["i18n/ko/INSTALL.md"] if not (ROOT / "i18n/ko/INSTALL.md").is_file() else []
    if missing:
        fail("Missing required files: " + ", ".join(missing))


def check_python() -> None:
    for path in ROOT.rglob("*.py"):
        if ".git" in path.parts:
            continue
        try:
            ast.parse(path.read_text(encoding="utf-8"))
        except SyntaxError as exc:
            fail(f"Python syntax error in {path}: {exc}")


def check_notebook() -> None:
    path = ROOT / "tests" / "colab" / "codingstandard_colab_test.ipynb"
    try:
        notebook = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        fail(f"Invalid Colab notebook JSON: {exc}")
    if notebook.get("nbformat") != 4:
        fail("Colab notebook must use nbformat 4")
    if not notebook.get("cells"):
        fail("Colab notebook has no cells")


def check_hardware_neutrality() -> None:
    for root in (ROOT / "COMMON", ROOT / "LLM", ROOT / "VISION"):
        for path in root.rglob("*.md"):
            text = path.read_text(encoding="utf-8")
            for pattern in FORBIDDEN_HARDWARE_PATTERNS:
                if pattern.search(text):
                    fail(f"Machine-specific hardware assumption in {path}: {pattern.pattern}")


def run_i18n_check() -> None:
    checker = ROOT / "scripts" / "check_i18n.py"
    namespace: dict[str, object] = {}
    exec(compile(checker.read_text(encoding="utf-8"), str(checker), "exec"), namespace)
    main = namespace.get("main")
    if not callable(main) or main() != 0:
        fail("English/Korean localization check failed")


def check_no_legacy_installer() -> None:
    for path in (ROOT / "scripts").glob("install-coding-standard.*"):
        fail(f"Legacy installer must not exist before release: {path.name}")


def check_windows_workflow() -> None:
    workflow = (ROOT / ".github" / "workflows" / "windows-install-test.yml").read_text(encoding="utf-8")
    if "runs-on: windows-latest" not in workflow:
        fail("Windows workflow must use the windows-latest runner")
    for required in ("powershell", "pwsh", "DryRun", "Merge"):
        if required not in workflow:
            fail(f"Windows workflow missing validation for: {required}")


def main() -> None:
    check_required_files()
    check_python()
    check_notebook()
    check_hardware_neutrality()
    check_no_legacy_installer()
    check_windows_workflow()
    run_i18n_check()
    print("codingStandard validation passed")


if __name__ == "__main__":
    main()
