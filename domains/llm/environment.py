from __future__ import annotations

"""LLM-facing adapter for the shared environment profiler."""

from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
import sys

_COMMON = Path(__file__).resolve().parents[2] / "core" / "common" / "environment.py"
_spec = spec_from_file_location("codingstandard_common_environment", _COMMON)
if _spec is None or _spec.loader is None: raise ImportError(f"Cannot load shared environment profiler: {_COMMON}")
_module = module_from_spec(_spec); sys.modules[_spec.name] = _module; _spec.loader.exec_module(_module)
EnvironmentProfile = _module.EnvironmentProfile
inspect_environment = _module.inspect_environment
to_runtime_config = _module.to_runtime_config
save_profile = _module.save_profile
print_profile = _module.print_profile

if __name__ == "__main__":
    profile = inspect_environment(); print_profile(profile)
    if len(sys.argv) == 2: save_profile(profile, sys.argv[1]); print(f"Saved profile: {sys.argv[1]}")
