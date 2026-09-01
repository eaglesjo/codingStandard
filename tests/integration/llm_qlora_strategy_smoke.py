#!/usr/bin/env python3
"""Network-independent validation of LLM PEFT/quantization strategy routing."""
from __future__ import annotations

import importlib.util
import json
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

PROFILES = {
    "cpu-small": {"ram_gb": 8.0, "vram_gb": 0.0, "accelerator": "none"},
    "gpu-constrained": {"ram_gb": 16.0, "vram_gb": 8.0, "accelerator": "cuda"},
    "gpu-mid": {"ram_gb": 32.0, "vram_gb": 24.0, "accelerator": "cuda"},
    "gpu-large": {"ram_gb": 64.0, "vram_gb": 48.0, "accelerator": "cuda"},
}


def choose_strategy(profile: dict[str, object]) -> str:
    vram = float(profile["vram_gb"])
    accelerator = str(profile["accelerator"])
    if accelerator == "cuda" and vram < 16:
        return "qlora-4bit"
    if accelerator == "cuda" and vram < 32:
        return "lora"
    if accelerator == "cuda":
        return "full-finetune-or-lora"
    return "cpu-inference-or-offload"


def lora_parameter_count(in_features: int, out_features: int, rank: int) -> int:
    return rank * (in_features + out_features)


def main() -> int:
    required = (
        ROOT / "domains/llm/AGENT.md",
        ROOT / "domains/llm/SKILL.md",
        ROOT / "domains/llm/skills/finetuning/SKILL.md",
        ROOT / "domains/llm/skills/peft/SKILL.md",
        ROOT / "domains/llm/skills/quantization/SKILL.md",
        ROOT / "platform/colab/SKILL.md",
    )
    for path in required:
        if not path.is_file():
            raise AssertionError(f"missing LLM resource: {path}")

    report = {name: {"profile": profile, "strategy": choose_strategy(profile)} for name, profile in PROFILES.items()}
    assert report["gpu-constrained"]["strategy"] == "qlora-4bit"
    assert report["gpu-mid"]["strategy"] == "lora"
    assert report["gpu-large"]["strategy"] == "full-finetune-or-lora"
    assert report["cpu-small"]["strategy"] == "cpu-inference-or-offload"

    base_params = 4096 * 4096
    adapter_params = lora_parameter_count(4096, 4096, 16)
    assert adapter_params < base_params * 0.02
    report["adapter_math"] = {
        "base_params": base_params,
        "lora_rank": 16,
        "adapter_params": adapter_params,
        "trainable_fraction": adapter_params / base_params,
    }

    report["optional_backend"] = {
        package: bool(importlib.util.find_spec(package))
        for package in ("transformers", "peft", "bitsandbytes")
    }

    with tempfile.TemporaryDirectory(prefix="codingstandard-qlora-") as tmp:
        output = Path(tmp) / "strategy-report.json"
        output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
        loaded = json.loads(output.read_text(encoding="utf-8"))
        assert loaded["gpu-constrained"]["strategy"] == "qlora-4bit"
        assert loaded["adapter_math"]["adapter_params"] == adapter_params

    print(json.dumps({"status": "passed", "strategies": report}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
