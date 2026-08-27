from __future__ import annotations

"""Shared reproducibility metadata helper for LLM and Vision experiments."""

import argparse
import hashlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def _git(*args: str) -> str | None:
    try:
        return subprocess.check_output(["git", *args], text=True, stderr=subprocess.DEVNULL).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def _json_hash(value: Any) -> str:
    data = json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(data).hexdigest()[:16]


def create_metadata(experiment_id: str, variant: str, seed: int, config: Any, model_revision: str | None = None, dataset_revision: str | None = None, environment_profile: str | None = None, runtime_config: Any | None = None) -> dict[str, Any]:
    return {
        "standard_version": (Path(__file__).resolve().parents[1] / "VERSION").read_text(encoding="utf-8").strip(),
        "experiment_id": experiment_id,
        "variant": variant,
        "seed": seed,
        "config_hash": _json_hash(config),
        "config": config,
        "model_revision": model_revision,
        "dataset_revision": dataset_revision,
        "environment_profile": environment_profile,
        "runtime_config": runtime_config,
        "git": {"commit": _git("rev-parse", "HEAD"), "branch": _git("branch", "--show-current"), "dirty": bool(_git("status", "--porcelain"))},
        "created_at": datetime.now(timezone.utc).isoformat(),
    }


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("experiment_id")
    p.add_argument("variant")
    p.add_argument("--seed", type=int, default=42)
    p.add_argument("--config", default="{}")
    p.add_argument("--model-revision")
    p.add_argument("--dataset-revision")
    p.add_argument("--environment-profile")
    p.add_argument("--runtime-config")
    p.add_argument("--output", type=Path, required=True)
    args = p.parse_args()
    config = json.loads(args.config)
    runtime = json.loads(args.runtime_config) if args.runtime_config else None
    result = create_metadata(args.experiment_id, args.variant, args.seed, config, args.model_revision, args.dataset_revision, args.environment_profile, runtime)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Saved experiment metadata: {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
