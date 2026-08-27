from __future__ import annotations

import json
import os
import platform
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class EnvironmentProfile:
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
    gpu_name: str | None
    vram_total_gb: float | None
    vram_free_gb: float | None
    cuda_available: bool
    mps_available: bool
    device: str
    recommended_batch_size: int
    recommended_gradient_accumulation_steps: int
    recommended_num_workers: int
    recommended_pin_memory: bool
    recommended_fp16: bool
    recommended_bf16: bool
    recommended_gradient_checkpointing: bool
    recommended_max_seq_length: int
    profile: str


def _detect_ide() -> str:
    env = os.environ
    if env.get("VSCODE_PID") or env.get("TERM_PROGRAM") == "vscode":
        return "vscode"
    if "JPY_PARENT_PID" in env:
        return "jupyter"
    if "COLAB_RELEASE_TAG" in env or "COLAB_GPU" in env:
        return "colab"
    return "unknown"


def inspect_environment() -> EnvironmentProfile:
    cpu_count = os.cpu_count()
    ram_total_gb: float | None = None
    ram_available_gb: float | None = None
    gpu_name: str | None = None
    vram_total_gb: float | None = None
    vram_free_gb: float | None = None
    cuda_available = False
    mps_available = False

    try:
        import psutil

        memory = psutil.virtual_memory()
        ram_total_gb = round(memory.total / 1024**3, 2)
        ram_available_gb = round(memory.available / 1024**3, 2)
    except ImportError:
        pass

    try:
        import torch

        cuda_available = bool(torch.cuda.is_available())
        if cuda_available:
            free, total = torch.cuda.mem_get_info()
            vram_total_gb = round(total / 1024**3, 2)
            vram_free_gb = round(free / 1024**3, 2)
            gpu_name = torch.cuda.get_device_name(0)

        mps_available = bool(
            hasattr(torch.backends, "mps")
            and torch.backends.mps.is_available()
        )
    except (ImportError, RuntimeError):
        pass

    if cuda_available:
        device = "cuda"
    elif mps_available:
        device = "mps"
    else:
        device = "cpu"

    # Conservative defaults. The profile is intentionally derived from measured resources.
    ram = ram_available_gb or 0.0
    vram = vram_free_gb or 0.0

    if device == "cuda":
        if vram <= 2.5:
            batch_size, grad_accum, max_seq = 1, 16, 128
        elif vram <= 4.5:
            batch_size, grad_accum, max_seq = 1, 8, 256
        else:
            batch_size, grad_accum, max_seq = 2, 4, 512
        fp16 = True
        bf16 = False
        checkpointing = vram <= 4.5
        pin_memory = ram >= 4.0
    elif device == "mps":
        batch_size, grad_accum, max_seq = 1, 8, 256
        fp16 = False
        bf16 = False
        checkpointing = True
        pin_memory = False
    else:
        batch_size, grad_accum, max_seq = 1, 8, 128
        fp16 = False
        bf16 = False
        checkpointing = False
        pin_memory = False

    if platform.system() == "Windows":
        num_workers = 0 if (ram and ram < 8) else 1
    else:
        num_workers = 1 if (ram and ram < 8) else min(4, cpu_count or 1)

    if ram and ram < 4:
        num_workers = 0
        grad_accum = max(grad_accum, 16)

    profile = _profile_name(
        device=device,
        vram_total_gb=vram_total_gb,
        ram_total_gb=ram_total_gb,
        os_name=platform.system(),
    )

    return EnvironmentProfile(
        os=platform.system(),
        architecture=platform.machine(),
        python=platform.python_version(),
        executable=sys.executable,
        ide=_detect_ide(),
        jupyter="ipykernel" in sys.modules,
        colab="google.colab" in sys.modules,
        cpu_count=cpu_count,
        ram_total_gb=ram_total_gb,
        ram_available_gb=ram_available_gb,
        gpu_name=gpu_name,
        vram_total_gb=vram_total_gb,
        vram_free_gb=vram_free_gb,
        cuda_available=cuda_available,
        mps_available=mps_available,
        device=device,
        recommended_batch_size=batch_size,
        recommended_gradient_accumulation_steps=grad_accum,
        recommended_num_workers=num_workers,
        recommended_pin_memory=pin_memory,
        recommended_fp16=fp16,
        recommended_bf16=bf16,
        recommended_gradient_checkpointing=checkpointing,
        recommended_max_seq_length=max_seq,
        profile=profile,
    )


def _profile_name(
    *,
    device: str,
    vram_total_gb: float | None,
    ram_total_gb: float | None,
    os_name: str,
) -> str:
    if device == "cuda" and vram_total_gb is not None and vram_total_gb <= 4.5:
        return "windows-low-vram" if os_name == "Windows" else "low-vram"
    if ram_total_gb is not None and ram_total_gb <= 16:
        return "low-system-memory"
    return f"{device}-standard"


def to_runtime_config(profile: EnvironmentProfile) -> dict[str, Any]:
    return {
        "device": profile.device,
        "batch_size": profile.recommended_batch_size,
        "gradient_accumulation_steps": profile.recommended_gradient_accumulation_steps,
        "num_workers": profile.recommended_num_workers,
        "pin_memory": profile.recommended_pin_memory,
        "fp16": profile.recommended_fp16,
        "bf16": profile.recommended_bf16,
        "gradient_checkpointing": profile.recommended_gradient_checkpointing,
        "max_seq_length": profile.recommended_max_seq_length,
    }


def print_profile(profile: EnvironmentProfile) -> None:
    print("=== Environment Profile ===")
    for key, value in asdict(profile).items():
        print(f"{key}: {value}")

    print("=== Recommended Runtime Config ===")
    for key, value in to_runtime_config(profile).items():
        print(f"{key}: {value}")


def save_profile(profile: EnvironmentProfile, path: str | Path) -> None:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(
        json.dumps(
            {
                "environment": asdict(profile),
                "runtime": to_runtime_config(profile),
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )


if __name__ == "__main__":
    profile = inspect_environment()
    print_profile(profile)
    if len(sys.argv) == 2:
        save_profile(profile, sys.argv[1])
        print(f"Saved profile: {sys.argv[1]}")
