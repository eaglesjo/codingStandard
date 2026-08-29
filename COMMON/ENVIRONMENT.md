# Common Environment Contract

All domains use the real execution environment as the source of truth.

```text
Detect → Measure → Resolve → Smoke Test → Lock → Optimize
```

Measure available CPU, system RAM, disk, accelerator/GPU, accelerator memory, framework capabilities, Python/runtime, and relevant IDE/kernel state when available.

## Linux vs Ubuntu policy

**Linux is the supported OS family; Ubuntu is the reference distribution.**

This distinction is intentional:

- The runtime contract must remain portable across Linux distributions.
- Ubuntu LTS is the primary development and CI baseline because it is widely supported, predictable, and directly available as a first-class GitHub-hosted runner.
- CI is pinned to **Ubuntu 24.04 LTS** rather than `ubuntu-latest` so a runner-image migration cannot silently change the validation baseline.
- Ubuntu-specific package or filesystem assumptions must not leak into the shared Python environment contract unless they are explicitly part of an installer/CI implementation.
- Other Linux distributions remain supported at the Python/runtime-contract level when they provide the required Python and framework capabilities. They are not required to be individually represented in the standard CI matrix.

In short:

```text
Supported platform family: Linux
Reference implementation:  Ubuntu 24.04 LTS
CI baseline:              ubuntu-24.04
```

This gives us a stable baseline without incorrectly turning "Ubuntu" into the definition of Linux.

## OS and runtime classification

Keep the operating system separate from the execution environment. The `os` field describes the machine/runtime actually executing Python; it does not describe the user's client device.

Supported OS families are detected from Python's runtime information rather than from hard-coded machine profiles:

- **Linux**: standard local Linux hosts and cloud runtimes such as Google Colab. Ubuntu 24.04 LTS is the CI reference distribution.
- **macOS**: Apple Silicon and Intel Macs; Apple MPS is used when the installed framework exposes it, otherwise CPU fallback is used.
- **Windows**: local Windows hosts; DirectML is used when available, otherwise CUDA/CPU resolution applies.

A Google Colab session is a Linux-based cloud runtime even when the user connects from macOS or Windows. Colab must therefore never be classified as a local macOS or Windows execution environment based on the user's browser/client OS. Colab notebooks commonly interact with Ubuntu/Linux tooling such as `apt`, but the project should detect the actual runtime rather than assume a particular Ubuntu release.

The profile reports:

- `os`: the host/runtime operating system reported by Python (`Linux`, `Darwin`, `Windows`, etc.).
- `architecture`: the runtime CPU architecture, such as `x86_64` or `arm64`.
- `execution_environment`: `local`, `jupyter`, `vscode`, or `colab`.
- `execution_type`: `local` or `cloud`.
- `device`: resolved execution device (`cpu`, `cuda`, `mps`, or `directml`).

This allows the same domain code to run across Linux, macOS, Windows, Jupyter, VS Code, and Colab without treating a named hardware profile as a runtime requirement.

## Platform-specific accelerator policy

Prefer measured framework capabilities over OS assumptions:

1. CUDA when `torch.cuda.is_available()` is true.
2. Apple MPS when the framework exposes an available MPS backend.
3. DirectML when `torch_directml` is installed and available to the runtime.
4. CPU as the universal fallback.

On Linux, ROCm is reported separately from CUDA even though the PyTorch runtime exposes it through the CUDA API surface. On macOS, Apple MPS is reported separately and CPU remains the required fallback. On Windows, DirectML is optional and must never be assumed to exist.

Runtime recommendations must remain conservative. Keep headroom for the OS, IDE/runtime, framework allocations, and background processes. Do not target 100% utilization.

## Validation contract

The repository CI validates **Ubuntu 24.04 LTS as the Linux reference baseline** and macOS directly. Windows remains covered by the Windows installer workflow. Runtime classification tests simulate Linux, macOS, Windows, Jupyter, VS Code, and Colab so that platform-specific logic can be verified without requiring every accelerator on every CI runner.

The CI baseline is intentionally narrower than the support contract: we validate one stable Linux distribution directly while keeping the shared code distribution-agnostic. Explicit Ubuntu LTS runner labels make this baseline reproducible.
