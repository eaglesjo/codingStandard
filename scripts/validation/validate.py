from __future__ import annotations

import ast
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

FORBIDDEN_HARDWARE_PATTERNS = [
    re.compile(r"RTX\s*3050", re.I),
    re.compile(r"3050\s*Ti", re.I),
    re.compile(r"4\s*GB\s*VRAM", re.I),
    re.compile(r"16\s*GB\s*(RAM|System RAM)", re.I),
]
REQUIRED_FILES = [
    "VERSION", "AGENTS.md", "CLAUDE.md", "GEMINI.md", "INSTALL.md",
    "core/common/AGENT.md", "core/common/SKILL.md", "core/common/ENVIRONMENT.md",
    "core/common/environment.py", "core/common/experiment.py",
    "domains/manus/PROJECT_INSTRUCTIONS.md", "domains/manus/SKILL.md", "domains/manus/README.md",
    "domains/llm/AGENT.md", "domains/llm/SKILL.md", "domains/llm/ENVIRONMENT.md",
    "domains/llm/environment.py", "domains/llm/memory_smoke_test.py", "domains/llm/experiment.py",
    "domains/vision/AGENT.md", "domains/vision/SKILL.md", "domains/vision/ENVIRONMENT.md",
    "domains/vision/memory_smoke_test.py", "domains/vision/README.md",
    "scripts/installers/install-domains.ps1", "scripts/installers/install-domains.sh",
    "scripts/validation/check_i18n.py", "scripts/installers/test_installers.py", "scripts/development/test_environment.py",
    "scripts/installers/test_installers_windows.ps1", ".github/workflows/windows-install-test.yml",
    "tests/colab/README.md", "tests/colab/codingstandard_colab_test.ipynb", "LICENSE",
]


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def check_required_files() -> None:
    missing = [path for path in REQUIRED_FILES if not (ROOT / path).is_file()]
    for path in ("i18n/ko/INSTALL.md", "i18n/ko/domains/manus/PROJECT_INSTRUCTIONS.md", "i18n/ko/domains/manus/SKILL.md", "i18n/ko/domains/manus/README.md"):
        if not (ROOT / path).is_file():
            missing.append(path)
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


def run_environment_tests() -> None:
    test_script = ROOT / "scripts" / "development" / "test_environment.py"
    proc = subprocess.run([sys.executable, str(test_script)], cwd=str(ROOT), capture_output=True, text=True, check=False)
    if proc.stdout: print(proc.stdout, end="")
    if proc.returncode != 0:
        if proc.stderr: print(proc.stderr, file=sys.stderr, end="")
        fail("Environment detection tests failed")


def check_notebook() -> None:
    path = ROOT / "tests" / "colab" / "codingstandard_colab_test.ipynb"
    try: notebook = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc: fail(f"Invalid Colab notebook JSON: {exc}")
    if notebook.get("nbformat") != 4: fail("Colab notebook must use nbformat 4")
    if not notebook.get("cells"): fail("Colab notebook has no cells")
    code = "\n".join("".join(cell.get("source", [])) for cell in notebook.get("cells", []) if cell.get("cell_type") == "code")
    for required in ("import subprocess", "import sys", "import platform", "subprocess.run", "sys.executable", "platform.platform", "DEFAULT_REPO_URL", "_normalize_repository", "GITHUB_TOKEN", "GIT_ASKPASS"):
        if required not in code: fail(f"Colab notebook missing required bootstrap/repository symbol: {required}")
    if "capture_output=True" not in code or "proc.stderr" not in code or "sys.stderr" not in code: fail("Colab notebook must expose subprocess stderr")


def check_hardware_neutrality() -> None:
    for root in (ROOT / "core", ROOT / "domains"):
        for path in root.rglob("*.md"):
            text = path.read_text(encoding="utf-8")
            for pattern in FORBIDDEN_HARDWARE_PATTERNS:
                if pattern.search(text): fail(f"Machine-specific hardware assumption in {path}: {pattern.pattern}")


def run_i18n_check() -> None:
    checker = ROOT / "scripts" / "validation" / "check_i18n.py"
    proc = subprocess.run([sys.executable, str(checker)], cwd=str(ROOT), capture_output=True, text=True, check=False)
    if proc.stdout: print(proc.stdout, end="")
    if proc.returncode != 0:
        if proc.stderr: print(proc.stderr, file=sys.stderr, end="")
        fail("English/Korean localization check failed")


def check_no_legacy_installer() -> None:
    for path in (ROOT / "scripts").glob("install-coding-standard.*"): fail(f"Legacy installer must not exist before release: {path.name}")


def check_windows_workflow() -> None:
    workflow = (ROOT / ".github" / "workflows" / "windows-install-test.yml").read_text(encoding="utf-8")
    if "runs-on: windows-latest" not in workflow: fail("Windows workflow must use the windows-latest runner")
    test_script = (ROOT / "scripts" / "installers" / "test_installers_windows.ps1").read_text(encoding="utf-8")
    haystack = workflow + "\n" + test_script
    for required in ("powershell", "pwsh", "-DryRun", "-ConflictAction Merge"):
        if required.lower() not in haystack.lower(): fail(f"Windows validation missing: {required}")


def check_version_consistency() -> None:
    version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
    if not re.fullmatch(r"\d+\.\d+\.\d+", version): fail(f"VERSION must use semantic versioning: {version!r}")
    common_env = (ROOT / "core" / "common" / "environment.py").read_text(encoding="utf-8")
    match = re.search(r'STANDARD_VERSION\s*=\s*["\']([^"\']+)["\']', common_env)
    if not match: fail("core/common/environment.py is missing STANDARD_VERSION")
    if match.group(1) != version: fail(f"Version mismatch: VERSION={version}, core/common/environment.py={match.group(1)}")


def main() -> None:
    check_required_files(); check_python(); run_environment_tests(); check_notebook(); check_hardware_neutrality(); check_no_legacy_installer(); check_windows_workflow(); check_version_consistency(); run_i18n_check(); print("codingStandard validation passed")


if __name__ == "__main__": main()
