#!/usr/bin/env python3
"""Focused tests for the shared environment profiler's runtime classification."""
from __future__ import annotations

import importlib.util
import os
import platform
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "COMMON" / "environment.py"


def load_environment_module():
    spec = importlib.util.spec_from_file_location("codingstandard_test_environment", MODULE_PATH)
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot load environment profiler: {MODULE_PATH}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class EnvironmentDetectionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.module = load_environment_module()
        self.env = os.environ.copy()
        for key in ("COLAB_RELEASE_TAG", "COLAB_GPU", "VSCODE_PID", "TERM_PROGRAM", "JETBRAINS_IDE", "JPY_PARENT_PID"):
            os.environ.pop(key, None)
        sys.modules.pop("google.colab", None)
        sys.modules.pop("ipykernel", None)

    def tearDown(self) -> None:
        os.environ.clear()
        os.environ.update(self.env)

    def test_local_execution_is_distinct_from_os(self) -> None:
        with patch.object(platform, "system", return_value="Darwin"):
            profile = self.module.inspect_environment()
        self.assertEqual(profile.os, "Darwin")
        self.assertEqual(profile.execution_environment, "local")
        self.assertEqual(profile.execution_type, "local")

    def test_linux_local_execution(self) -> None:
        with patch.object(platform, "system", return_value="Linux"):
            profile = self.module.inspect_environment()
        self.assertEqual(profile.os, "Linux")
        self.assertEqual(profile.execution_environment, "local")
        self.assertEqual(profile.execution_type, "local")

    def test_windows_local_execution(self) -> None:
        with patch.object(platform, "system", return_value="Windows"):
            profile = self.module.inspect_environment()
        self.assertEqual(profile.os, "Windows")
        self.assertEqual(profile.execution_environment, "local")
        self.assertEqual(profile.execution_type, "local")

    def test_colab_is_cloud_even_when_os_is_linux(self) -> None:
        os.environ["COLAB_RELEASE_TAG"] = "release-test"
        with patch.object(platform, "system", return_value="Linux"):
            profile = self.module.inspect_environment()
        self.assertEqual(profile.os, "Linux")
        self.assertEqual(profile.ide, "colab")
        self.assertTrue(profile.colab)
        self.assertEqual(profile.execution_environment, "colab")
        self.assertEqual(profile.execution_type, "cloud")

    def test_jupyter_is_local_runtime(self) -> None:
        sys.modules["ipykernel"] = object()
        profile = self.module.inspect_environment()
        self.assertTrue(profile.jupyter)
        self.assertEqual(profile.execution_environment, "jupyter")
        self.assertEqual(profile.execution_type, "local")

    def test_vscode_is_local_runtime(self) -> None:
        os.environ["TERM_PROGRAM"] = "vscode"
        profile = self.module.inspect_environment()
        self.assertEqual(profile.ide, "vscode")
        self.assertEqual(profile.execution_environment, "vscode")
        self.assertEqual(profile.execution_type, "local")

    def test_colab_takes_priority_over_jupyter_and_vscode(self) -> None:
        os.environ["COLAB_RELEASE_TAG"] = "release-test"
        os.environ["TERM_PROGRAM"] = "vscode"
        sys.modules["ipykernel"] = object()
        profile = self.module.inspect_environment()
        self.assertEqual(profile.execution_environment, "colab")
        self.assertEqual(profile.execution_type, "cloud")


if __name__ == "__main__":
    unittest.main()
