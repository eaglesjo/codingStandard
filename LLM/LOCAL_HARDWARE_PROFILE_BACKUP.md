# Local Hardware Profile Backup

> Historical reference only. This file is not the source of truth for runtime detection.
>
> The actual development environment must be detected at runtime by `LLM/environment.py`.

## Previous Explicit Local Profile

```text
OS: Windows
IDE: VS Code
GPU: NVIDIA GeForce RTX 3050 Ti Laptop GPU
GPU VRAM: 4 GB
System RAM: 16 GB
CUDA: NVIDIA CUDA runtime / PyTorch CUDA execution
```

## Previous Conservative Training Defaults

```text
batch_size = 1
gradient_accumulation_steps = 8
max_seq_length = 256
num_workers = 0
FP16 = enabled for CUDA when supported
gradient_checkpointing = enabled/considered for low VRAM
```

## Important

These values are preserved as a backup of the previous local-development target only.

Do not use this file to determine the current machine.

Current runtime configuration must be resolved from:

```text
LLM/environment.py
    ↓
actual CPU / RAM / GPU / VRAM / CUDA / IDE / runtime
    ↓
resolved runtime configuration
```
