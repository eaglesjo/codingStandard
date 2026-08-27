# AGENT.md

# Cross-Platform Python LLM / Jupyter / Google Colab Development

This document defines common rules for AI coding agents working on Python LLM/ML projects in Jupyter Notebook, JupyterLab, VS Code Jupyter, Google Colab, and Colab Local Runtime.

## 1. Supported Scope

- Windows / Linux / macOS
- venv / virtualenv / conda / uv
- Jupyter / JupyterLab / VS Code Jupyter
- Google Colab / Colab Local Runtime
- CPU / CUDA / MPS environments
- local GPUs and constrained system memory

## 2. Core Principles

1. Inspect the actual execution environment first.
2. Do not hard-code GPU, CPU, RAM, OS, Python, or IDE/runtime assumptions.
3. Keep reusable logic in `src/` or equivalent modules; keep notebooks focused on orchestration.
4. Use `pathlib.Path` for paths.
5. Specify file encodings explicitly.
6. Never place API keys, tokens, or passwords in source code.
7. Measure available VRAM/RAM before deciding resource usage.
8. Do not target 100% GPU/RAM utilization.
9. Do not retry OOM failures indefinitely with the same configuration.
10. Keep experiments in explicit configuration objects/sections.
11. Long-running training uses validation metrics, Early Stopping, and Checkpoint/Resume by default.
12. Record reproducibility metadata and resource usage.

## 3. Detect → Measure → Resolve → Smoke Test → Lock

All environment-dependent work follows this sequence:

```text
Detect
  ↓
Measure
  ↓
Resolve
  ↓
Smoke Test
  ↓
Environment Lock
  ↓
Optimize
  ↓
Implement / Execute
```

Run the shared profiler when available:

```bash
python LLM/environment.py
```

Save a profile:

```bash
python LLM/environment.py .codingstandard/environment-profile.json
```

## 4. Environment Profile

`LLM/environment.py` measures:

- OS / architecture
- Python version / executable
- IDE / Jupyter / Colab state
- CPU core count
- System RAM total / available
- NVIDIA GPU / VRAM total / free
- CUDA / MPS availability
- resolved device

It also derives a conservative starting runtime configuration:

- device
- batch size
- gradient accumulation steps
- DataLoader workers
- pin memory
- FP16 / BF16 candidates
- gradient checkpointing
- maximum sequence length

Profiler output is a starting point. Workload-specific Memory Smoke Tests decide the final settings.

## 5. Environment Neutrality

Do not document a specific machine as the required runtime environment. Runtime decisions must be based on measured resources and workload requirements.

## 6. Environment Lock

```python
from environment import inspect_environment, to_runtime_config

PROFILE = inspect_environment()
RUNTIME_CONFIG = to_runtime_config(PROFILE)
```

Reuse the locked configuration across training/inference. Do not independently re-detect device, worker count, or precision in every cell or function.

Reusable libraries that officially support multiple platforms may keep the required branches, but detection and execution should remain separated.

## 7. Final Code Cleanup

After the environment is validated and the target execution path is known, remove unused alternatives from application/notebook execution code.

Remove when no longer needed:

- unused CPU/CUDA/MPS paths
- duplicate environment detection
- commented-out old implementations
- failed temporary experiments
- unused imports

Keep branches only when they are required by an officially supported reusable or multi-platform component.

## 8. Notebook Structure

Recommended order:

1. Purpose Markdown
2. Environment Detection
3. Hardware / Memory Detection
4. Environment Profile Resolution
5. Environment Lock
6. UTF-8 / Path
7. Dependency Bootstrap
8. Imports
9. Resource Configuration
10. Experiment Configuration
11. Data
12. Model / Client
13. Training / Inference
14. Evaluation
15. Ablation
16. Visualization
17. Export
18. Reproducibility Metadata

A new notebook must run top-to-bottom from a fresh kernel/runtime.

## 9. Dependency

In notebooks, install into the active kernel when required:

```python
import importlib
import subprocess
import sys


def ensure_package(import_name: str, package_name: str | None = None):
    package_name = package_name or import_name
    try:
        return importlib.import_module(import_name)
    except ImportError:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", package_name
        ])
        return importlib.import_module(import_name)
```

The project dependency source of truth is `pyproject.toml`, `requirements.txt`, or the lock file.

## 10. Path / UTF-8

Use `pathlib.Path` and explicit UTF-8 encoding.

```python
from pathlib import Path

DATA_DIR = ROOT / "data"
OUTPUT_DIR = ROOT / "outputs"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
```

## 11. Device Detection

Default priority is CUDA → MPS → CPU.

```python
def detect_device():
    try:
        import torch
        if torch.cuda.is_available():
            return "cuda"
        if hasattr(torch.backends, "mps") and torch.backends.mps.is_available():
            return "mps"
    except ImportError:
        pass
    return "cpu"
```

After Profile Resolution, reuse the resolved device.

## 12. GPU / RAM Optimization

Tune from measured resources and workload:

```text
batch size ↓
sequence/input size ↓
gradient accumulation
AMP / mixed precision
gradient checkpointing
quantization when appropriate
offload when appropriate
remove unnecessary tensors/references
```

CPU/RAM principles:

```text
Do not load an oversized dataset into RAM unnecessarily.
Prefer streaming / chunking / memory mapping.
Start DataLoader workers conservatively.
Avoid excessive persistent workers or prefetching.
Avoid duplicate DataFrame/list/tensor copies.
Do not increase CPU thread counts without measurement.
```

## 13. Mixed Precision

When supported by the actual accelerator, evaluate mixed precision.

```python
USE_AMP = PROFILE.recommended_fp16
```

Use BF16 only after verifying hardware and framework support.

## 14. Gradient Accumulation

```python
BATCH_SIZE = RUNTIME_CONFIG["batch_size"]
GRADIENT_ACCUMULATION_STEPS = RUNTIME_CONFIG[
    "gradient_accumulation_steps"
]

loss = loss / GRADIENT_ACCUMULATION_STEPS
loss.backward()

if (step + 1) % GRADIENT_ACCUMULATION_STEPS == 0:
    optimizer.step()
    optimizer.zero_grad(set_to_none=True)
```

Record effective batch size.

## 15. Memory Smoke Test

Before long training, run:

```text
model load
→ forward
→ backward
→ optimizer step
→ validation
→ checkpoint save
```

Record peak VRAM, peak RAM, metrics, runtime, and resolved environment profile. If it fails, lower the configuration before starting the main run.

## 16. OOM / Memory Recovery

```text
Record VRAM/RAM
→ reduce batch
→ reduce sequence/input
→ reduce workers
→ verify AMP
→ consider checkpointing
→ consider quantization/offload
→ repeat smoke test
→ run with the validated configuration
```

Do not retry the same failing configuration indefinitely.

## 17. Training / Early Stopping

Long-running training uses validation-based Early Stopping by default.

```python
EARLY_STOPPING = {
    "enabled": True,
    "metric": "eval_loss",
    "mode": "min",
    "patience": 3,
    "min_delta": 0.0,
    "restore_best": True,
}
```

Required:

- validation split or evaluation dataset
- explicit metric and direction
- patience
- best checkpoint saving
- best checkpoint restoration
- early-stop event logging

## 18. Checkpoint / Resume

Store, when applicable:

```text
model
optimizer
scheduler
AMP scaler
epoch / global step
best metric
Early Stopping counter
training config
seed
model revision
dataset revision
resolved environment profile
```

## 19. Ablation Study

Define the baseline first and isolate individual components.

```python
ABLATION_CONFIG = {
    "study_name": "components",
    "baseline": {
        "feature_a": True,
        "feature_b": True,
    },
    "variants": {
        "no_feature_a": {"feature_a": False},
        "no_feature_b": {"feature_b": False},
    },
    "seeds": [42, 43, 44],
    "primary_metric": "eval_loss",
    "metric_mode": "min",
}
```

Keep controlled variables consistent across variants whenever possible.

## 20. Experiment Tracking

Record experiment ID, variant, changed parameters, seed, model/dataset revisions, best metrics, early-stopped status, peak VRAM/RAM, runtime, checkpoint path, and resolved environment profile.

## 21. Notebook Idempotency

Repeated execution must not cause uncontrolled accumulation. Reset state when appropriate, use deterministic output paths, clean temporary files, and define overwrite behavior.

## 22. Validation Workflow

```text
1. Restart kernel/runtime
2. Run environment profiler
3. Measure hardware/memory
4. Generate runtime configuration
5. Lock environment
6. Run Memory Smoke Test
7. Run baseline training/inference
8. Verify Early Stopping
9. Verify checkpoint save/resume
10. Run ablations
11. Record metrics + resources
12. Remove dead code
13. Final clean Run All
```

## 23. Completion Criteria

```text
[ ] actual environment checked
[ ] resource profile generated
[ ] runtime configuration resolved
[ ] smoke test passed
[ ] environment locked
[ ] unused environment branches removed
[ ] OOM recovery verified
[ ] validation metric defined
[ ] Early Stopping enabled
[ ] best checkpoint / Resume available
[ ] ablation matrix defined
[ ] controlled comparison completed
[ ] reproducibility metadata recorded
[ ] resource usage recorded
[ ] clean kernel Run All succeeds
```
