from __future__ import annotations

"""LLM-facing adapter for the shared experiment metadata helper."""

from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
import sys

_COMMON = Path(__file__).resolve().parents[1] / "COMMON" / "experiment.py"
_spec = spec_from_file_location("codingstandard_common_experiment", _COMMON)
if _spec is None or _spec.loader is None:
    raise ImportError(f"Cannot load shared experiment helper: {_COMMON}")
_module = module_from_spec(_spec)
sys.modules[_spec.name] = _module
_spec.loader.exec_module(_module)

create_metadata = _module.create_metadata

if __name__ == "__main__":
    import argparse
    import json
    parser = argparse.ArgumentParser()
    parser.add_argument("experiment_id")
    parser.add_argument("variant")
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--config", default="{}")
    parser.add_argument("--model-revision")
    parser.add_argument("--dataset-revision")
    parser.add_argument("--environment-profile")
    parser.add_argument("--runtime-config")
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    result = create_metadata(args.experiment_id, args.variant, args.seed, json.loads(args.config), args.model_revision, args.dataset_revision, args.environment_profile, json.loads(args.runtime_config) if args.runtime_config else None)
    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    Path(args.output).write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
