#!/usr/bin/env python3
"""Integration-test the domain installer in disposable projects."""
from __future__ import annotations

import shutil
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PS1 = ROOT / "scripts" / "install-domains.ps1"
SH = ROOT / "scripts" / "install-domains.sh"
COMMON = [
    "AGENTS.md", "CLAUDE.md", "GEMINI.md",
    ".github/copilot-instructions.md",
    ".github/instructions/llm.instructions.md",
    ".github/instructions/vision.instructions.md",
    "COMMON/AGENT.md", "COMMON/SKILL.md", "COMMON/ENVIRONMENT.md",
]
LLM = ["LLM/AGENT.md", "LLM/SKILL.md", "LLM/ENVIRONMENT.md", "LLM/environment.py", "LLM/experiment.py", "LLM/memory_smoke_test.py"]
VISION = ["VISION/AGENT.md", "VISION/SKILL.md", "VISION/ENVIRONMENT.md", "VISION/memory_smoke_test.py"]


def run(cmd: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, cwd=ROOT, check=True, text=True, capture_output=True)


def check(target: Path, paths: list[str]) -> None:
    missing = [p for p in paths if not (target / p).is_file()]
    if missing:
        raise AssertionError(f"missing installed files: {missing}")


def test_bash() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        target = Path(tmp) / "project"
        target.mkdir()
        dry = run(["bash", str(SH), str(target), "en", "all", "overwrite", "true"])
        if any(target.iterdir()) or "DRY-RUN" not in dry.stdout:
            raise AssertionError("bash dry-run modified target")
        run(["bash", str(SH), str(target), "en", "all", "overwrite", "false"])
        check(target, COMMON + LLM + VISION)

        agents = target / "AGENTS.md"
        agents.write_text("# Local\n\n<!-- BEGIN CODINGSTANDARD MANAGED BLOCK -->\nold\n<!-- END CODINGSTANDARD MANAGED BLOCK -->\n", encoding="utf-8")
        run(["bash", str(SH), str(target), "en", "common", "merge", "false"])
        text = agents.read_text(encoding="utf-8")
        if "# Local" not in text or "old" in text:
            raise AssertionError("merge did not preserve local content or replace managed block")


def test_powershell() -> None:
    executable = shutil.which("pwsh") or shutil.which("powershell")
    if not executable:
        return
    with tempfile.TemporaryDirectory() as tmp:
        target = Path(tmp) / "project"
        target.mkdir()
        run([executable, "-NoProfile", "-File", str(PS1), "-Target", str(target), "-Language", "ko", "-Domain", "vision", "-ConflictAction", "Overwrite", "-DryRun"])
        if any(target.iterdir()):
            raise AssertionError("PowerShell dry-run modified target")
        run([executable, "-NoProfile", "-File", str(PS1), "-Target", str(target), "-Language", "ko", "-Domain", "vision", "-ConflictAction", "Overwrite"])
        check(target, COMMON + VISION)


def main() -> int:
    test_bash()
    test_powershell()
    print("domain installer tests passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
