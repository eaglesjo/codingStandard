# ML Environment Contract

Use the actual execution runtime as the source of truth. A machine name is never a requirement.

```text
Detect → Measure → Resolve → Smoke Test → Lock → Optimize
```

## Measure

When available, capture:

- OS and architecture
- Python executable/version
- framework versions and accelerator support
- CPU count and available RAM
- disk capacity/free space
- GPU/accelerator name, memory total/free, and backend
- Jupyter/VS Code/Colab runtime state

## Runtime resolution

Resolve conservative values for the workload, such as:

```text
device
batch size
gradient accumulation
input/sequence size
workers/prefetch
precision
cache policy
checkpoint frequency
```

Workload-specific smoke tests decide final values.

## Platform policy

Linux is the supported OS family and Ubuntu 24.04 LTS remains the CI reference distribution. macOS and Windows use capability detection. Google Colab is a cloud Linux runtime and must be classified from the executing Python runtime, not the client device.

## Accelerator policy

Prefer a measured and framework-supported accelerator. CUDA, ROCm, MPS, DirectML, and CPU are capabilities, not assumptions. Keep fallback behavior in reusable platform-neutral components.

## Environment lock

After a representative workload passes, persist the resolved profile and configuration with the experiment and reuse it during the run. Remove diagnostic and execution branches that are no longer relevant to the locked target unless the component intentionally remains multi-platform.
