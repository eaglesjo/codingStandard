#!/usr/bin/env python3
"""Integration-test the installers in disposable temporary projects."""
from __future__ import annotations

import shutil
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PS1 = ROOT / "scripts" / "install-coding-standard.ps1"
SH = ROOT / "scripts" / "install-coding-standard.sh"
EXPECTED = [
    "AGENTS.md", "CLAUDE.md", "GEMINI.md", "CONVENTIONS.md", ".aider.conf.yml",
    ".github/copilot-instructions.md", ".github/instructions/llm.instructions.md",
    ".cursor/rules/coding-standard.mdc", ".windsurf/rules/coding-standard.md",
    ".clinerules/01-coding-standard.md", ".continue/rules/01-coding-standard.md",
    ".junie/AGENTS.md", ".amazonq/rules/coding-standard.md",
    "LLM/AGENT.md", "LLM/SKILL.md", "LLM/ENVIRONMENT.md", "LLM/environment.py",
    "LLM/memory_smoke_test.py", "LLM/experiment.py", "LLM/README.md",
    "LLM/config/training.yaml", "LLM/config/ablation.yaml",
]
EXPECTED += [f"LLM/skills/{name}/SKILL.md" for name in (
    "environment", "training", "ablation", "notebook", "debugging", "release"
)]


def check_expected(target: Path) -> None:
    missing = [path for path in EXPECTED if not (target / path).is_file()]
    if missing:
        raise AssertionError(f"missing installed files: {missing}")


def run_bash(language: str) -> None:
    with tempfile.TemporaryDirectory() as tmp:
        target = Path(tmp) / "project"
        target.mkdir()
        dry = subprocess.run(
            ["bash", str(SH), str(target), language, "overwrite", "true"],
            cwd=ROOT, check=True, text=True, capture_output=True,
        )
        if "DRY-RUN" not in dry.stdout or any(target.iterdir()):
            raise AssertionError("bash dry-run changed the target or produced no dry-run output")

        subprocess.run(
            ["bash", str(SH), str(target), language, "overwrite", "false"],
            cwd=ROOT, check=True, text=True, capture_output=True,
        )
        check_expected(target)

        agents = target / "AGENTS.md"
        agents.write_text(
            "# Local project rule\n\n"
            "<!-- BEGIN CODINGSTANDARD MANAGED BLOCK -->\nold\n"
            "<!-- END CODINGSTANDARD MANAGED BLOCK -->\n",
            encoding="utf-8",
        )
        subprocess.run(
            ["bash", str(SH), str(target), language, "merge", "false"],
            cwd=ROOT, check=True, text=True, capture_output=True,
        )
        merged = agents.read_text(encoding="utf-8")
        if "# Local project rule" not in merged or "old" in merged:
            raise AssertionError("merge did not preserve local content or replace managed block")


def run_powershell(language: str) -> bool:
    executable = shutil.which("pwsh") or shutil.which("powershell")
    if not executable:
        return False
    with tempfile.TemporaryDirectory() as tmp:
        target = Path(tmp) / "project"
        target.mkdir()
        subprocess.run(
            [executable, "-NoProfile", "-File", str(PS1), "-Target", str(target),
             "-Language", language, "-ConflictAction", "Overwrite", "-DryRun"],
            cwd=ROOT, check=True, text=True, capture_output=True,
        )
        if any(target.iterdir()):
            raise AssertionError("PowerShell dry-run modified the target")
        subprocess.run(
            [executable, "-NoProfile", "-File", str(PS1), "-Target", str(target),
             "-Language", language, "-ConflictAction", "Overwrite"],
            cwd=ROOT, check=True, text=True, capture_output=True,
        )
        check_expected(target)
    return True


def main() -> int:
    for language in ("en", "ko"):
        run_bash(language)
    ps = shutil.which("pwsh") or shutil.which("powershell")
    powershell_available = bool(ps) and all(run_powershell(lang) for lang in ("en", "ko"))
    print(f"installer tests passed (bash; powershell tested={powershell_available})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
