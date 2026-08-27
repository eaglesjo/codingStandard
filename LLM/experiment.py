from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

STANDARD_VERSION = "1.1.0"


def git_value(*args: str) -> str | None:
    try:
        result = subprocess.run(
            ["git", *args],
            check=True,
            capture_output=True,
            text=True,
        )
        return result.stdout.strip() or None
    except (OSError, subprocess.CalledProcessError):
        return None


def canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def config_hash(config: Any) -> str:
    return hashlib.sha256(canonical_json(config).encode("utf-8")).hexdigest()[:16]


def build_metadata(
    *,
    experiment_id: str,
    variant: str,
    seed: int,
    config: dict[str, Any],
    environment_profile: dict[str, Any] | None = None,
    model_revision: str | None = None,
    dataset_revision: str | None = None,
) -> dict[str, Any]:
    return {
        "standard_version": STANDARD_VERSION,
        "experiment_id": experiment_id,
        "variant": variant,
        "seed": seed,
        "config_hash": config_hash(config),
        "git_commit": git_value("rev-parse", "HEAD"),
        "git_branch": git_value("branch", "--show-current"),
        "git_dirty": bool(git_value("status", "--porcelain")),
        "model_revision": model_revision,
        "dataset_revision": dataset_revision,
        "environment_profile": environment_profile,
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "config": config,
    }


def save_metadata(metadata: dict[str, Any], path: str | Path) -> None:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(
        json.dumps(metadata, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Create reproducible experiment metadata")
    parser.add_argument("experiment_id")
    parser.add_argument("variant")
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--config", default="{}", help="JSON configuration")
    parser.add_argument("--output", default="experiments/metadata.json")
    args = parser.parse_args()

    config = json.loads(args.config)
    metadata = build_metadata(
        experiment_id=args.experiment_id,
        variant=args.variant,
        seed=args.seed,
        config=config,
    )
    save_metadata(metadata, args.output)
    print(json.dumps(metadata, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
