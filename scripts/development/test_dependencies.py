#!/usr/bin/env python3
"""Tests for the Python/PyTorch dependency contract without changing the host environment."""
from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
MODULE_PATH = ROOT / "core" / "common" / "dependencies.py"


def load_module():
    spec = importlib.util.spec_from_file_location("codingstandard_dependencies_test", MODULE_PATH)
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot load dependency contract: {MODULE_PATH}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class DependencyContractTests(unittest.TestCase):
    def setUp(self) -> None:
        self.module = load_module()

    def test_supported_python_range(self) -> None:
        with patch.object(self.module.sys, "version_info", (3, 12, 0)):
            self.module.check_python_version()

    def test_rejects_old_python(self) -> None:
        with patch.object(self.module.sys, "version_info", (3, 9, 0)):
            with self.assertRaises(RuntimeError):
                self.module.check_python_version()

    def test_rejects_future_unsupported_python(self) -> None:
        with patch.object(self.module.sys, "version_info", (3, 15, 0)):
            with self.assertRaises(RuntimeError):
                self.module.check_python_version()

    def test_torchvision_pair_matrix(self) -> None:
        self.assertTrue(self.module._pair_is_compatible("2.13.0", "0.28.0"))
        self.assertTrue(self.module._pair_is_compatible("2.12.1", "0.27.1"))
        self.assertTrue(self.module._pair_is_compatible("2.11.0", "0.26.0"))
        self.assertFalse(self.module._pair_is_compatible("2.13.0", "0.27.0"))
        self.assertFalse(self.module._pair_is_compatible(None, "0.28.0"))

    def test_compatible_installation_is_preserved(self) -> None:
        status = self.module.DependencyStatus(True, True, "2.13.0", True, "0.28.0", True)
        with patch.object(self.module, "inspect_dependencies", return_value=status) as inspect:
            with patch.object(self.module, "_pip_install") as install:
                result = self.module.ensure_pytorch()
        self.assertEqual(result, status)
        inspect.assert_called_once()
        install.assert_not_called()

    def test_incompatible_installation_is_repaired(self) -> None:
        before = self.module.DependencyStatus(True, True, "2.9.0", True, "0.24.0", False)
        after = self.module.DependencyStatus(True, True, "2.13.0", True, "0.28.0", True)
        with patch.object(self.module, "inspect_dependencies", side_effect=[before, after]):
            with patch.object(self.module, "_pip_install") as install:
                result = self.module.ensure_pytorch()
        self.assertEqual(result, after)
        install.assert_called_once_with("torch==2.13.0", "torchvision==0.28.0")

    def test_repair_can_be_disabled(self) -> None:
        status = self.module.DependencyStatus(True, True, "2.9.0", True, "0.24.0", False)
        with patch.object(self.module, "inspect_dependencies", return_value=status):
            with self.assertRaises(RuntimeError):
                self.module.ensure_pytorch(repair=False)


if __name__ == "__main__":
    unittest.main()
