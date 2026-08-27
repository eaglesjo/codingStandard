# Environment Skill

Use for environment detection, hardware profiling, and runtime optimization.

## Workflow

```text
Detect → Measure → Resolve → Smoke Test → Lock → Optimize → Execute
```

Run `python LLM/environment.py` when available. Treat measured capabilities as the source of truth.

Measure CPU, RAM, disk, accelerator, VRAM, CUDA/MPS/ROCm/DirectML where available, Python/runtime, and IDE/Jupyter/Colab state.

Resolve conservative settings for device, batch size, gradient accumulation, workers, pin memory, mixed precision, checkpointing, and input length.

Before long runs, perform a representative Memory Smoke Test. If it fails, reduce resource demands and test again.

After Environment Lock, remove unnecessary platform/device branches from application and notebook execution code. Keep branches in reusable multi-platform libraries when required.
