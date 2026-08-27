from __future__ import annotations

import json
import os
import platform
import shutil
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any


STANDARD_VERSION = "1.1.0"


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
    disk_total_gb: float | None
    disk_free_gb: float | None
    gpu_vendor: str | None
    gpu_name: str | None
    vram_total_gb: float | None
    vram_free_gb: float | None
    cuda_available: bool
    cuda_version: str | None
    mps_available: bool
    rocm_available: bool
    directml_available: bool
    fp16_supported: bool
    bf16_supported: bool
    device: str
    recommended_batch_size: int
    recommended_gradient_accumulation_steps: int
    recommended_num_workers: int
    recommended_pin_memory: bool
    recommended_mixed_precision: str
    recommended_gradient_checkpointing: bool
    recommended_max_seq_length: int
    profile: str


def _detect_ide() -> str:
    env = os.environ
    if env.get("VSCODE_PID") or env.get("TERM_PROGRAM") == "vscode":
        return "vscode"
    if "JPY_PARENT_PID" in env:
        return "jupyter"
    if env.get("COLAB_RELEASE_TAG") or env.get("COLAB_GPU"):
        return "colab"
    if env.get("JETBRAINS_IDE"):
        return "jetbrains"
    return "unknown"


def _disk_info() -> tuple[float | None, float | None]:
    try:
        usage = shutil.disk_usage(Path.cwd())
        return (
            round(usage.total / 1024**3, 2),
            round(usage.free / 1024**3, 2),
        )
    except OSError:
        return None, None


def _detect_accelerators() -> dict[str, Any]:
    result: dict[str, Any] = {
        "gpu_vendor": None,
        "gpu_name": None,
        "vram_total_gb": None,
        "vram_free_gb": None,
        "cuda_available": False,
        "cuda_version": None,
        "mps_available": False,
        "rocm_available": False,
        "directml_available": False,
        "fp16_supported": False,
        "bf16_supported": False,
    }

    try:
        import torch

        result["cuda_available"] = bool(torch.cuda.is_available())
        result["cuda_version"] = getattr(torch.version, "cuda", None)
        result["rocm_available"] = bool(getattr(torch.version, "hip", None))

        if result["cuda_available"]:
            free, total = torch.cuda.mem_get_info()
            result["vram_total_gb"] = round(total / 1024**3, 2)
            result["vram_free_gb"] = round(free / 1024**3, 2)
            result["gpu_name"] = torch.cuda.get_device_name(0)
            result["gpu_vendor"] = "nvidia"
            major, minor = torch.cuda.get_device_capability(0)
            capability = major + minor / 10
            result["fp16_supported"] = capability >= 5.3
            result["bf16_supported"] = capability >= 8.0

        if hasattr(torch.backends, "mps"):
            result["mps_available"] = bool(torch.backends.mps.is_available())
            if result["mps_available"] and platform.system() == "Darwin":
                result["gpu_vendor"] = "apple"

    except (ImportError, RuntimeError, AttributeError):
        pass

    try:
        import torch_directml  # type: ignore

        result["directml_available"] = True
        if result["gpu_vendor"] is None:
            result["gpu_vendor"] = "directml"
    except ImportError:
        pass

    return result


def _resolve_device(acc: dict[str, Any]) -> str:
    if acc["cuda_available"]:
        return "cuda"
    if acc["mps_available"]:
        return "mps"
    if acc["directml_available"]:
        return "directml"
    return "cpu"


def _resolve_runtime(
    *,
    device: str,
    ram_available_gb: float | None,
    vram_free_gb: float | None,
    fp16_supported: bool,
    bf16_supported: bool,
    os_name: str,
    cpu_count: int | None,
) -> dict[str, Any]:
    ram = ram_available_gb or 0.0
    vram = vram_free_gb or 0.0

    if device == "cuda":
        if vram <= 2.5:
            batch, grad_accum, seq = 1, 16, 128
        elif vram <= 4.5:
            batch, grad_accum, seq = 1, 8, 256
        elif vram <= 8.5:
            batch, grad_accum, seq = 2, 4, 512
        else:
            batch, grad_accum, seq = 4, 2, 512
        if bf16_supported:
            precision = "bf16"
        elif fp16_supported:
            precision = "fp16"
        else:
            precision = "fp32"
        checkpointing = vram <= 8.5
        pin_memory = ram >= 4.0
    elif device == "mps":
        batch, grad_accum, seq = 1, 8, 256
        precision = "fp16" if fp16_supported else "fp32"
        checkpointing = True
        pin_memory = False
    elif device == "directml":
        batch, grad_accum, seq = 1, 8, 256
        precision = "fp16" if fp16_supported else "fp32"
        checkpointing = True
        pin_memory = False
    else:
        batch, grad_accum, seq = 1, 8, 128
        precision = "fp32"
        checkpointing = False
        pin_memory = False

    if os_name == "Windows":
        workers = 0 if (ram and ram < 8) else 1
    else:
        workers = 1 if (ram and ram < 8) else min(4, cpu_count or 1)

    if ram and ram < 4:
        workers = 0
        grad_accum = max(grad_accum, 16)

    return {
        "batch": batch,
        "grad_accum": grad_accum,
        "workers": workers,
        "pin_memory": pin_memory,
        "precision": precision,
        "checkpointing": checkpointing,
        "max_seq": seq,
    }


def _profile_name(
    *,
    device: str,
    vram_total_gb: float | None,
    ram_total_gb: float | None,
    disk_free_gb: float | None,
) -> str:
    vram = vram_total_gb or 0.0
    ram = ram_total_gb or 0.0
    disk = disk_free_gb or 0.0

    if device == "cuda" and vram and vram <= 4.5:
        return "accelerated-constrained-vram"
    if vram and vram <= 8.5:
        return "accelerated-limited-vram"
    if ram and ram <= 16:
        return "limited-system-memory"
    if disk and disk <= 20:
        return "limited-disk-space"
    return f"{device}-standard"


def inspect_environment() -> EnvironmentProfile:
    cpu_count = os.cpu_count()
    ram_total_gb: float | None = None
    ram_available_gb: float | None = None
    try:
        import psutil

        memory = psutil.virtual_memory()
        ram_total_gb = round(memory.total / 1024**3, 2)
        ram_available_gb = round(memory.available / 1024**3, 2)
    except ImportError:
        pass

    disk_total_gb, disk_free_gb = _disk_info()
    accelerators = _detect_accelerators()
    device = _resolve_device(accelerators)
    runtime = _resolve_runtime(
        device=device,
        ram_available_gb=ram_available_gb,
        vram_free_gb=accelerators["vram_free_gb"],
        fp16_supported=accelerators["fp16_supported"],
        bf16_supported=accelerators["bf16_supported"],
        os_name=platform.system(),
        cpu_count=cpu_count,
    )

    return EnvironmentProfile(
        standard_version=STANDARD_VERSION,
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
        disk_total_gb=disk_total_gb,
        disk_free_gb=disk_free_gb,
        gpu_vendor=accelerators["gpu_vendor"],
        gpu_name=accelerators["gpu_name"],
        vram_total_gb=accelerators["vram_total_gb"],
        vram_free_gb=accelerators["vram_free_gb"],
        cuda_available=accelerators["cuda_available"],
        cuda_version=accelerators["cuda_version"],
        mps_available=accelerators["mps_available"],
        rocm_available=accelerators["rocm_available"],
        directml_available=accelerators["directml_available"],
        fp16_supported=accelerators["fp16_supported"],
        bf16_supported=accelerators["bf16_supported"],
        device=device,
        recommended_batch_size=runtime["batch"],
        recommended_gradient_accumulation_steps=runtime["grad_accum"],
        recommended_num_workers=runtime["workers"],
        recommended_pin_memory=runtime["pin_memory"],
        recommended_mixed_precision=runtime["precision"],
        recommended_gradient_checkpointing=runtime["checkpointing"],
        recommended_max_seq_length=runtime["max_seq"],
        profile=_profile_name(
            device=device,
            vram_total_gb=accelerators["vram_total_gb"],
            ram_total_gb=ram_total_gb,
            disk_free_gb=disk_free_gb,
        ),
    )


def to_runtime_config(profile: EnvironmentProfile) -> dict[str, Any]:
    return {
        "standard_version": profile.standard_version,
        "device": profile.device,
        "batch_size": profile.recommended_batch_size,
        "gradient_accumulation_steps": profile.recommended_gradient_accumulation_steps,
        "num_workers": profile.recommended_num_workers,
        "pin_memory": profile.recommended_pin_memory,
        "mixed_precision": profile.recommended_mixed_precision,
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
