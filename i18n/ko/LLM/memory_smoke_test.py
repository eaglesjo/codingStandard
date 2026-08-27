#!/usr/bin/env python3
"""Run a small representative training workload and measure memory headroom.

This intentionally uses a tiny synthetic model. Projects should run this before
long training and then repeat the same checks with the real model/configuration.
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import sys
import tempfile
import time
from pathlib import Path
from typing import Any


def _ram_gb() -> tuple[float | None, float | None]:
    try:
        import psutil
        m = psutil.virtual_memory()
        return m.total / 1024**3, m.available / 1024**3
    except ImportError:
        return None, None


def _cuda_memory() -> dict[str, float | None]:
    try:
        import torch
        if not torch.cuda.is_available():
            return {"total_gb": None, "free_gb": None, "allocated_gb": None, "reserved_gb": None}
        free, total = torch.cuda.mem_get_info()
        return {
            "total_gb": total / 1024**3,
            "free_gb": free / 1024**3,
            "allocated_gb": torch.cuda.memory_allocated() / 1024**3,
            "reserved_gb": torch.cuda.memory_reserved() / 1024**3,
        }
    except (ImportError, RuntimeError):
        return {"total_gb": None, "free_gb": None, "allocated_gb": None, "reserved_gb": None}


def run(args: argparse.Namespace) -> dict[str, Any]:
    try:
        import torch
        import torch.nn as nn
    except ImportError as exc:
        raise SystemExit("PyTorch is required for memory_smoke_test.py") from exc

    device = "cuda" if torch.cuda.is_available() and not args.cpu else "cpu"
    dtype = torch.float16 if device == "cuda" and args.precision == "fp16" else torch.float32
    torch.manual_seed(args.seed)

    model = nn.Sequential(
        nn.Linear(args.features, args.hidden),
        nn.GELU(),
        nn.Linear(args.hidden, args.classes),
    ).to(device=device, dtype=dtype)
    optimizer = torch.optim.AdamW(model.parameters(), lr=1e-3)
    criterion = nn.CrossEntropyLoss()

    ram_total_before, ram_available_before = _ram_gb()
    if device == "cuda":
        torch.cuda.empty_cache()
        torch.cuda.reset_peak_memory_stats()

    peak_ram_gb = ram_available_before
    started = time.perf_counter()
    checkpoint_path = Path(tempfile.gettempdir()) / "codingstandard-smoke-checkpoint.pt"

    model.train()
    for step in range(args.steps):
        x = torch.randn(args.batch_size, args.features, device=device, dtype=dtype)
        y = torch.randint(0, args.classes, (args.batch_size,), device=device)
        optimizer.zero_grad(set_to_none=True)
        logits = model(x)
        loss = criterion(logits.float(), y)
        loss.backward()
        optimizer.step()
        _, available = _ram_gb()
        if available is not None:
            peak_ram_gb = min(peak_ram_gb or available, available)

    torch.save({"model": model.state_dict(), "optimizer": optimizer.state_dict()}, checkpoint_path)
    checkpoint = torch.load(checkpoint_path, map_location=device, weights_only=False)
    model.load_state_dict(checkpoint["model"])
    optimizer.load_state_dict(checkpoint["optimizer"])
    checkpoint_path.unlink(missing_ok=True)

    if device == "cuda":
        torch.cuda.synchronize()
    elapsed = time.perf_counter() - started
    gpu = _cuda_memory()
    _, ram_available_after = _ram_gb()

    result: dict[str, Any] = {
        "status": "pass",
        "device": device,
        "precision": "fp16" if dtype == torch.float16 else "fp32",
        "steps": args.steps,
        "batch_size": args.batch_size,
        "features": args.features,
        "hidden": args.hidden,
        "classes": args.classes,
        "runtime_seconds": round(elapsed, 3),
        "ram_total_gb": round(ram_total_before, 3) if ram_total_before is not None else None,
        "ram_available_before_gb": round(ram_available_before, 3) if ram_available_before is not None else None,
        "ram_available_after_gb": round(ram_available_after, 3) if ram_available_after is not None else None,
        "ram_min_available_gb": round(peak_ram_gb, 3) if peak_ram_gb is not None else None,
        "gpu": {k: round(v, 3) if isinstance(v, float) else v for k, v in gpu.items()},
    }

    if ram_available_after is not None and ram_available_after < args.min_ram_free_gb:
        result["status"] = "fail"
        result["failure"] = f"RAM free space below {args.min_ram_free_gb} GB"
    if gpu["free_gb"] is not None and gpu["free_gb"] < args.min_vram_free_gb:
        result["status"] = "fail"
        result["failure"] = f"VRAM free space below {args.min_vram_free_gb} GB"
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--batch-size", type=int, default=1)
    parser.add_argument("--features", type=int, default=128)
    parser.add_argument("--hidden", type=int, default=256)
    parser.add_argument("--classes", type=int, default=8)
    parser.add_argument("--steps", type=int, default=8)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--precision", choices=["fp32", "fp16"], default="fp16")
    parser.add_argument("--cpu", action="store_true", help="Force CPU even when CUDA is available")
    parser.add_argument("--min-ram-free-gb", type=float, default=1.0)
    parser.add_argument("--min-vram-free-gb", type=float, default=0.25)
    parser.add_argument("--json", type=Path)
    args = parser.parse_args()

    result = run(args)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    if args.json:
        args.json.parent.mkdir(parents=True, exist_ok=True)
        args.json.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return 0 if result["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
