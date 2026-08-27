from __future__ import annotations

"""Shared runtime environment profiler for all codingStandard domains."""

import json
import os
import platform
import shutil
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

STANDARD_VERSION = "1.4.1"


@dataclass(frozen=True)
class EnvironmentProfile:
    standard_version: str
    os: str
    architecture: str
    python: str
    executable: str
    ide: str
    jupyter: bool
    colab: bool
    cpu_count: int | None
    ram_total_gb: float | None
    ram_available_gb: float | None