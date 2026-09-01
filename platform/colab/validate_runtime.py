from __future__ import annotations

import argparse
import json
import os
import platform
import shutil
import sys
from pathlib import Path


def detect() -> dict[str, object]:
    try:
        import psutil
        ram_gb = round(psutil.virtual_memory().total / (1024 ** 3), 2)
        disk = shutil.disk_usage(Path.cwd())
        disk_free_gb = round(disk.free / (1024 ** 3), 2)
    except Exception:
        ram_gb = None
        disk_free_gb = None

    colab = False
    try:
        import google.colab  # type: ignore
        colab = True
    except Exception:
        colab = bool(os.environ.get("COLAB_RELEASE_TAG") or os.environ.get("COLAB_GPU"))

    accelerator = "none"
    torch_version = None
    try:
        import torch
        torch_version = torch.__version__
        if torch.cuda.is_available():
            accelerator = f"cuda:{torch.cuda.get_device_name(0)}"
        elif getattr(torch.backends, "mps", None) is not None and torch.backends.mps.is_available():
            accelerator = "mps"
    except Exception:
        pass

    return {
        "is_colab": colab,
        "python": sys.version.split()[0],
        "executable": sys.executable,
        "os": platform.system(),
        "architecture": platform.machine(),
        "accelerator": accelerator,
        "torch": torch_version,
        "ram_gb": ram_gb,
        "disk_free_gb": disk_free_gb,
        "cwd": str(Path.cwd()),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--durable-dir", type=Path)
    args = parser.parse_args()

    report = detect()
    if args.durable_dir:
        args.durable_dir.mkdir(parents=True, exist_ok=True)
        probe = args.durable_dir / ".colab_validation_probe"
        probe.write_text("ok\n", encoding="utf-8")
        report["durable_storage"] = str(args.durable_dir)
        report["durable_storage_writable"] = probe.read_text(encoding="utf-8").strip() == "ok"
        probe.unlink(missing_ok=True)

    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        for key, value in report.items():
            print(f"{key}: {value}")


if __name__ == "__main__":
    main()
