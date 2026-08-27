# Environment Profile & Optimization

This document defines environment detection, runtime configuration resolution, Environment Lock, memory safety, and execution optimization.

## 1. Principle

Always optimize for the actual execution environment, not a named or assumed machine.

```text
Detect → Measure → Resolve → Smoke Test → Lock → Optimize → Execute
```

## 2. Profiler

Run:

```bash
python LLM/environment.py
```

Save a profile:

```bash
python LLM/environment.py .codingstandard/environment-profile.json
```

Measure when available:

- OS / architecture
- Python version / executable
- IDE / Jupyter / Colab
- CPU core count
- System RAM total / available
- GPU name / VRAM total / free
- CUDA / MPS availability
- resolved device

## 3. Runtime Resolution

The profiler derives conservative starting values for:

- device
- batch size
- gradient accumulation
- DataLoader workers
- pin memory
- FP16 / BF16 candidates
- gradient checkpointing
- maximum sequence length

Do not treat these recommendations as hard limits. The workload-specific smoke test determines the final configuration.

## 4. Environment Lock

```python
from environment import inspect_environment, to_runtime_config

PROFILE = inspect_environment()
RUNTIME_CONFIG = to_runtime_config(PROFILE)
```

After validation, reuse the locked profile and runtime configuration throughout the run.

## 5. Environment-Specific Code Cleanup

After the environment is validated:

```text
Detect
→ Measure
→ Resolve
→ Smoke Test
→ Lock
→ remove unused branches
→ execute
```

Remove unused OS/device branches, duplicate detection, obsolete code, and unused imports from application/notebook execution code.

Keep multi-platform branches only when a reusable component officially supports them.

## 6. GPU Optimization

Choose based on measured free VRAM and workload:

```text
batch ↓
sequence/input ↓
gradient accumulation
mixed precision
checkpointing
quantization when justified
offload when justified
tensor/reference cleanup
```

Leave VRAM headroom for the runtime and background allocations.

## 7. CPU / RAM Optimization

```text
streaming / chunking / memory mapping
conservative workers
controlled prefetch
avoid persistent workers unless justified
avoid duplicate dataset copies
control CPU/BLAS/OpenMP thread counts
```

Leave RAM headroom for the OS, IDE, runtime, and other processes.

## 8. Memory Smoke Test

Run a minimal representative workload before long training:

```text
load
→ forward
→ backward
→ optimizer step
→ validation
→ checkpoint
```

Record peak VRAM, peak RAM, metrics, runtime, and resolved environment.

A failed smoke test blocks the long run until configuration is reduced and the test passes.

## 9. OOM Recovery

```text
record failure
→ reduce batch
→ reduce sequence/input
→ reduce workers
→ verify precision
→ checkpointing
→ quantization/offload
→ repeat smoke test
```

Do not repeat the same failing configuration indefinitely.

## 10. Reproducibility

Persist the resolved environment profile with experiment results:

```text
environment profile
runtime configuration
device
gpu / accelerator
VRAM / RAM
CPU count
peak VRAM
peak RAM
runtime
```
