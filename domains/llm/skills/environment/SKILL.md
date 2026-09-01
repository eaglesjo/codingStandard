# Environment Skill

Use for environment detection, hardware profiling, and runtime optimization.

## Workflow

```text
Detect → Measure → Resolve → Smoke Test → Lock → Optimize → Execute
```

Use `core/common/environment.py` as the shared profiler source of truth when available.

Measure CPU, RAM, disk, accelerator, VRAM, CUDA/ROCm/MPS/DirectML where available, Python/runtime, and IDE/Jupyter/Colab state.

Resolve conservative settings for device, batch size, gradient accumulation, workers, pin memory, mixed precision, checkpointing, and input length. Validate them with a representative Memory Smoke Test before long runs.

After Environment Lock, reuse the resolved configuration instead of independently re-detecting resources across notebook cells. Remove unnecessary platform/device branches from application paths while preserving intentionally reusable multi-platform components.
