from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from scripts.validation.validate_profiles import check_dependency_edge, imported_modules, layer_for_path


class ProfileContractTests(unittest.TestCase):
    def test_project_profile_is_repository_standard(self) -> None:
        value = json.loads((ROOT / "profiles" / "project.json").read_text(encoding="utf-8"))
        self.assertEqual(value["profile_version"], 1)
        self.assertEqual(value["project_type"], "developer-standard")
        self.assertEqual(value["architecture_profile"], "repository-standard")
        self.assertEqual(value["policy_profile"], "repository-default")
        self.assertEqual(set(value["runtime"]["os"]), {"linux", "macos", "windows"})

    def test_repository_standard_dependency_contract(self) -> None:
        value = json.loads(
            (ROOT / "profiles" / "architecture" / "repository-standard.json").read_text(encoding="utf-8")
        )
        self.assertIn("interface -> domain", value["dependency_direction"])
        self.assertIn("domain -> interface", value["forbidden_dependencies"])
        self.assertNotIn("domain -> interface", value["dependency_direction"])
        self.assertEqual(value["path_roots"]["domain"], ["domains"])
        self.assertEqual(value["path_roots"]["infrastructure"], ["platform"])

    def test_repository_policy_prevents_weakening(self) -> None:
        value = json.loads(
            (ROOT / "profiles" / "policies" / "repository-default.json").read_text(encoding="utf-8")
        )
        self.assertEqual(value["scope"], "repository")
        self.assertTrue(value["inheritance"]["child_scopes_may_not_weaken_parent"])
        self.assertEqual(value["inheritance"]["conflict_resolution"], "stricter-wins")

    def test_layer_mapping_uses_declared_roots(self) -> None:
        roots = {
            "interface": ["scripts/installers"],
            "policy": [],
            "validation": ["scripts/validation", "tests/validation"],
            "domain": ["domains"],
            "infrastructure": ["platform"],
        }
        self.assertEqual(layer_for_path(ROOT / "domains" / "llm" / "environment.py", roots), "domain")
        self.assertEqual(layer_for_path(ROOT / "platform" / "colab" / "validate_runtime.py", roots), "infrastructure")
        self.assertEqual(layer_for_path(ROOT / "scripts" / "validation" / "validate_profiles.py", roots), "validation")

    def test_import_parser_reads_python_imports(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "sample.py"
            path.write_text("import json\nfrom domains.llm import environment\n", encoding="utf-8")
            self.assertIn("json", imported_modules(path))
            self.assertIn("domains.llm", imported_modules(path))

    def test_strict_dependency_edge_contract(self) -> None:
        allowed = {("validation", "domain")}
        forbidden = {("domain", "infrastructure")}
        self.assertEqual(check_dependency_edge("validation", "domain", allowed, forbidden), "allowed")
        self.assertEqual(check_dependency_edge("domain", "infrastructure", allowed, forbidden), "forbidden")
        self.assertEqual(check_dependency_edge("interface", "domain", allowed, forbidden), "undeclared")
        self.assertEqual(check_dependency_edge("domain", "domain", allowed, forbidden), "undeclared")

    def test_stdlib_import_is_not_local_dependency(self) -> None:
        from scripts.validation.validate_profiles import local_module_exists, resolve_local_module

        self.assertFalse(local_module_exists("platform"))
        self.assertIsNone(resolve_local_module("platform"))

    def test_validator_passes(self) -> None:
        proc = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "validation" / "validate_profiles.py")],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertIn("repository dependency validation passed", proc.stdout)
        self.assertIn("validation passed", proc.stdout)


if __name__ == "__main__":
    unittest.main()
