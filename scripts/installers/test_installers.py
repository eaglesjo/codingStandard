#!/usr/bin/env python3
"""Integration-test the domain installer in disposable projects."""
from __future__ import annotations

import re
import shutil
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PS1 = ROOT / "scripts" / "installers" / "install-domains.ps1"
SH = ROOT / "scripts" / "installers" / "install-domains.sh"
COMMON = [
    "AGENTS.md", "CLAUDE.md", "GEMINI.md", ".github/copilot-instructions.md",
    ".cursor/rules/coding-standard.mdc", ".windsurf/rules/coding-standard.md",
    ".clinerules/01-coding-standard.md", ".continue/rules/01-coding-standard.md",
    ".junie/AGENTS.md", ".amazonq/rules/coding-standard.md", "docs/development/CONVENTIONS.md", ".aider.conf.yml",
    "core/common/AGENT.md", "core/common/SKILL.md", "core/common/ENVIRONMENT.md", "core/common/environment.py", "core/common/experiment.py", "core/common/dependencies.py",
]
ML = [".github/instructions/ml.instructions.md", "domains/ml/AGENT.md", "domains/ml/SKILL.md", "domains/ml/ENVIRONMENT.md", "domains/ml/README.md"]
LLM = [".github/instructions/llm.instructions.md", "domains/llm/AGENT.md", "domains/llm/SKILL.md", "domains/llm/ENVIRONMENT.md", "domains/llm/environment.py", "domains/llm/experiment.py", "domains/llm/memory_smoke_test.py", "domains/llm/README.md"]
VISION = [".github/instructions/vision.instructions.md", "domains/vision/AGENT.md", "domains/vision/SKILL.md", "domains/vision/ENVIRONMENT.md", "domains/vision/memory_smoke_test.py", "domains/vision/README.md"]
COLAB = ["platform/colab/AGENT.md", "platform/colab/SKILL.md"]


def run(cmd: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, cwd=ROOT, check=True, text=True, capture_output=True)


def check(target: Path, paths: list[str]) -> None:
    missing = [p for p in paths if not (target / p).is_file()]
    if missing: raise AssertionError(f"missing installed files: {missing}")


def test_bash() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        target = Path(tmp) / "new-project"
        dry = run(["bash", str(SH), str(target), "en", "all", "overwrite", "true"])
        if target.exists() and any(target.iterdir()): raise AssertionError("bash dry-run modified target")
        if "DRY-RUN" not in dry.stdout: raise AssertionError("bash dry-run output missing")
        run(["bash", str(SH), str(target), "en", "all", "overwrite", "false"]); check(target, COMMON + ML + LLM + VISION + COLAB)
        agents = target / "AGENTS.md"
        agents.write_text("# Local\n\n<!-- BEGIN CODINGSTANDARD MANAGED BLOCK -->\nold managed content\n<!-- END CODINGSTANDARD MANAGED BLOCK -->\n", encoding="utf-8")
        run(["bash", str(SH), str(target), "en", "common", "merge", "false"])
        text = agents.read_text(encoding="utf-8")
        if "# Local" not in text or re.search(r"(?m)^old managed content$", text): raise AssertionError("bash merge failed")

        ml_target = Path(tmp) / "ml-project"
        run(["bash", str(SH), str(ml_target), "en", "ml", "overwrite", "false"]); check(ml_target, COMMON + ML)

        colab_target = Path(tmp) / "colab-project"
        run(["bash", str(SH), str(colab_target), "en", "colab", "overwrite", "false"]); check(colab_target, COMMON + COLAB)


def test_powershell() -> None:
    executable = shutil.which("pwsh") or shutil.which("powershell")
    if not executable: return
    with tempfile.TemporaryDirectory() as tmp:
        target = Path(tmp) / "new-project"
        run([executable, "-NoProfile", "-File", str(PS1), "-Target", str(target), "-Language", "ko", "-Domain", "all", "-ConflictAction", "Overwrite", "-DryRun"])
        if target.exists() and any(target.iterdir()): raise AssertionError("PowerShell dry-run modified target")
        run([executable, "-NoProfile", "-File", str(PS1), "-Target", str(target), "-Language", "ko", "-Domain", "ml", "-ConflictAction", "Overwrite"]); check(target, COMMON + ML)


def main() -> int:
    test_bash(); test_powershell(); print("domain installer tests passed"); return 0


if __name__ == "__main__": raise SystemExit(main())