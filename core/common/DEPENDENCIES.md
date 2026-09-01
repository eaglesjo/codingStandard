# Python and PyTorch Dependency Contract

## Python

`codingStandard` 1.6 supports Python **3.10 through 3.14**. Python 3.15+ is intentionally rejected until the runtime contract is validated for that release line.

## PyTorch

The dependency contract uses a small compatibility matrix instead of blindly installing the newest package on every machine:

| torch | torchvision |
| --- | --- |
| 2.10.x | 0.25.x |
| 2.11.x | 0.26.x |
| 2.12.x | 0.27.x |

The bootstrap default is `torch==2.12.1` with `torchvision==0.27.1`.

Behavior:

1. If a compatible pair is already installed, it is preserved.
2. If PyTorch or torchvision is missing, the bootstrap installs the known stable default pair.
3. If the installed pair is incompatible, the bootstrap repairs it to the known stable default pair.
4. `repair=False` can be used by validation tooling when mutation of the current environment is not allowed.
5. Installation always uses `sys.executable -m pip`, so the active venv/Jupyter/Colab interpreter is the one being modified.

Accelerator-specific wheels remain an installation concern. The common contract does not assume CUDA, ROCm, MPS, or DirectML; the runtime profiler detects the actual backend after installation.

## Colab policy

Colab uses the same dependency contract as local Python. It must inspect the active interpreter and should only repair an incompatible environment. It should not unconditionally reinstall PyTorch on every notebook start.
