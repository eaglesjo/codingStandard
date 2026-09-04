#!/usr/bin/env python3
"""End-to-end installer checks against genuinely empty disposable projects."""
from __future__ import annotations

import json
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
INSTALLER = ROOT / "scripts" / "installers" / "install-domains.sh"
CATALOG = json.loads((ROOT / "i18n" / "languages.json").read_text(encoding="utf-8"))
RUNTIME_LOCALES = [item["locale"] for item in CATALOG["runtime_resources"]]
DOMAINS = ["common", "ml", "llm", "vision", "colab"]
COMMON_PROBES = ["AGENTS.md", "core/common/AGENT.md", "core/common/SKILL.md", "core/common/ENVIRONMENT.md"]
DOMAIN_PROBES = {
    "common": "core/common/AGENT.md",
    "ml": "domains/ml/AGENT.md",
    "llm": "domains/llm/AGENT.md",
    "vision": "domains/vision/AGENT.md",
    "colab": "platform/colab/AGENT.md",
}


def run(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(["bash", str(INSTALLER), *args], cwd=ROOT, check=True, text=True, capture_output=True)


def snapshot(root: Path) -> dict[str, bytes]:
    return {str(path.relative_to(root)): path.read_bytes() for path in sorted(root.rglob("*")) if path.is_file()}


def assert_common(target: Path) -> None:
    for rel in COMMON_PROBES:
        assert (target / rel).is_file(), f"missing common resource: {rel}"


def assert_domain(target: Path, domain: str) -> None:
    probe = DOMAIN_PROBES[domain]
    assert (target / probe).is_file(), f"missing domain resource: {probe}"


def test_empty_project_all_locales() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        for locale in RUNTIME_LOCALES:
            target = root / locale
            result = run(str(target), locale, "all", "overwrite", "false")
            assert f"language={locale}" in result.stdout
            assert_common(target)
            for domain in DOMAINS:
                assert_domain(target, domain)


def test_locale_fallback_and_reinstall_idempotence() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        target = Path(tmp) / "ru"
        run(str(target), "ru", "all", "overwrite", "false")
        english_source = (ROOT / "platform/colab/AGENT.md").read_bytes()
        assert (target / "platform/colab/AGENT.md").read_bytes() == english_source
        before = snapshot(target)
        run(str(target), "ru", "all", "overwrite", "false")
        assert before == snapshot(target), "reinstall changed the installed project"


def test_conflict_policies() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)

        overwrite_target = root / "overwrite"
        overwrite_target.mkdir()
        agents = overwrite_target / "AGENTS.md"
        agents.write_text("local", encoding="utf-8")
        run(str(overwrite_target), "en", "common", "overwrite", "false")
        assert agents.read_text(encoding="utf-8") == (ROOT / "AGENTS.md").read_text(encoding="utf-8")

        skip_target = root / "skip"
        skip_target.mkdir()
        skip_agents = skip_target / "AGENTS.md"
        skip_agents.write_text("local", encoding="utf-8")
        run(str(skip_target), "en", "common", "skip", "false")
        assert skip_agents.read_text(encoding="utf-8") == "local"
        assert (skip_target / "core/common/AGENT.md").is_file()

        merge_target = root / "merge"
        merge_target.mkdir()
        merge_agents = merge_target / "AGENTS.md"
        merge_agents.write_text("# Local rule\n\n<!-- BEGIN CODINGSTANDARD MANAGED BLOCK -->\nold managed content\n<!-- END CODINGSTANDARD MANAGED BLOCK -->\n", encoding="utf-8")
        run(str(merge_target), "en", "common", "merge", "false")
        merged = merge_agents.read_text(encoding="utf-8")
        assert "# Local rule" in merged
        assert "old managed content" not in merged
        assert "CODINGSTANDARD MANAGED BLOCK" in merged


def main() -> int:
    test_empty_project_all_locales()
    test_locale_fallback_and_reinstall_idempotence()
    test_conflict_policies()
    print("fresh-project installer E2E passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
