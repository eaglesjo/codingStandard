from __future__ import annotations

import argparse
import gc
import json
import time
from pathlib import Path


def _import_torch():
    try:
        import torch
        return torch
    except ImportError as exc:
        raise SystemExit("PyTorch is required for the vision memory smoke test.") from exc


def _device(torch, requested: str) -> str:
    if requested != "auto":
        return requested
    if torch.cuda.is_available():
        return "cuda"
    if hasattr(torch.backends, "mps") and torch.backends.mps.is_available():
        return "mps"
    return "cpu"


def main() -> int:
    parser = argparse.ArgumentParser(description="Run a minimal vision memory smoke test.")
    parser.add_argument("--device", default="auto")
    parser.add_argument("--image-size", type=int, default=224)
    parser.add_argument("--batch-size", type=int, default=1)
    parser.add_argument("--channels", type=int, default=3)
    parser.add_argument("--steps", type=int, default=2)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    torch = _import_torch()
    device_name = _device(torch, args.device)
    device = torch.device(device_name)

    model = torch.nn.Sequential(
        torch.nn.Conv2d(args.channels, 16, kernel_size=3, stride=2, padding=1),
        torch.nn.ReLU(),
        torch.nn.Conv2d(16, 32, kernel_size=3, stride=2, padding=1),
        torch.nn.ReLU(),
        torch.nn.AdaptiveAvgPool2d(1),
        torch.nn.Flatten(),
        torch.nn.Linear(32, 10),
    ).to(device)
    optimizer = torch.optim.AdamW(model.parameters(), lr=1e-3)
    x = torch.randn(args.batch_size, args.channels, args.image_size, args.image_size, device=device)
    y = torch.randint(0, 10, (args.batch_size,), device=device)
    loss_fn = torch.nn.CrossEntropyLoss()

    if device.type == "cuda":
        torch.cuda.reset_peak_memory_stats(device)

    start = time.perf_counter()
    model.train()
    for _ in range(args.steps):
        optimizer.zero_grad(set_to_none=True)
        logits = model(x)
        loss = loss_fn(logits, y)
        loss.backward()
        optimizer.step()

    if device.type == "cuda":
        torch.cuda.synchronize(device)
        peak_vram_gb = round(torch.cuda.max_memory_allocated(device) / 1024**3, 4)
    else:
        peak_vram_gb = None

    result = {
        "device": device_name,
        "image_size": args.image_size,
        "batch_size": args.batch_size,
        "channels": args.channels,
        "steps": args.steps,
        "loss": float(loss.detach().cpu()),
        "runtime_seconds": round(time.perf_counter() - start, 4),
        "peak_vram_gb": peak_vram_gb,
    }
    print(json.dumps(result, indent=2, ensure_ascii=False))
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")

    del model, optimizer, x, y
    gc.collect()
    if device.type == "cuda":
        torch.cuda.empty_cache()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
