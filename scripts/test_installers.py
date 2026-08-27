#!/usr/bin/env python3
"""Integration-test the installers in disposable temporary projects."""
from __future__ import annotations

import os
import shutil
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PS1 = ROOT / "scripts" / "install-coding-standard.ps1"
SH = ROOT / "scripts" / "install-coding-standard.sh"
EXPECTED = [
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
    "LLM/environment.py",
    "LLM/README.md",
    "LLM/config/training.yaml",
    "LLM/config/ablation.yaml",
]


def check_expected(target: Path) -> None:
    missing = [p for p in EXPECTED if not (target / p).is_file()]
    if missing:
        raise AssertionError(f"missing installed files: {missing}")


def run_bash(language: str) -> None:
    with tempfile.TemporaryDirectory() as tmp:
        target = Path(tmp) / "project"
        target.mkdir()
        subprocess.run(
            ["bash", str(SH), str(target), language, "overwrite"],
            cwd=ROOT,
            check=True,
            text=True,
            capture_output=True,
        )
        check_expected(target)

        # Conflict behavior: merge should preserve an existing custom marker and
        # replace the managed block on a second installation.
        agents = target / "AGENTS.md"
        existing = "# Local project rule\n\n<!-- BEGIN CODINGSTANDARD MANAGED BLOCK -->\nold\n<!-- END CODINGSTANDARD MANAGED BLOCK -->\n"
        agents.write_text(existing, encoding="utf-8")
        subprocess.run(
            ["bash", str(SH), str(target), language, "merge"],
            cwd=ROOT,
            check=True,
            text=True,
            capture_output=True,
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
            [executable, "-NoProfile", "-File", str(PS1), "-Target", str(target), "-Language", language, "-ConflictAction", "Overwrite"],
            cwd=ROOT,
            check=True,
            text=True,
            capture_output=True,
        )
        check_expected(target)
    return True


def main() -> int:
    for language in ("en", "ko"):
        run_bash(language)
    powershell_available = any(run_powershell(lang) for lang in ("en", "ko"))
    print("installer tests passed (bash; powershell tested={} )".format(powershell_available))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
