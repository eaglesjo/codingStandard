# 通用 Environment Contract

所有领域都以真实运行环境作为唯一依据。

```text
Detect → Measure → Resolve → Smoke Test → Lock → Optimize
```

测量可用 CPU、系统 RAM、磁盘、加速器/GPU、加速器内存、框架能力、Python/runtime，以及在可用时的 IDE/kernel 状态。

## Linux 与 Ubuntu 策略

**Linux 是受支持的操作系统系列；Ubuntu 是参考发行版。**

- runtime contract 必须保持对不同 Linux 发行版的可移植性。
- Ubuntu LTS 作为主要开发和 CI baseline，因为它得到广泛支持、行为可预测，并可直接作为 GitHub-hosted runner 使用。
- CI 固定使用 **Ubuntu 24.04 LTS**，而不是 `ubuntu-latest`，避免 runner image 迁移悄然改变 validation baseline。
- Ubuntu 特有的 package 或 filesystem 假设，除非明确属于 installer/CI 实现，否则不得泄漏到共享 Python 环境契约。
- 其他能提供所需 Python 和 framework 能力的 Linux 发行版，在 Python/runtime contract 层面仍受支持，不要求单独加入标准 CI matrix。

```text
Supported platform family: Linux
Reference implementation:  Ubuntu 24.04 LTS
CI baseline:              ubuntu-24.04
```

## OS 与 runtime 分类

将 operating system 与 execution environment 分开。`os` 字段描述实际执行 Python 的 machine/runtime，不描述用户的客户端设备。

支持的 OS 系列应根据 Python runtime 信息检测，而不是依赖硬编码的机器 profile。

- **Linux**：本地 Linux 主机和 Google Colab 等云 runtime。Ubuntu 24.04 LTS 是 CI reference distribution。
- **macOS**：Apple Silicon 和 Intel Mac；当 framework 提供且启用 MPS 时使用 Apple MPS，否则回退到 CPU。
- **Windows**：本地 Windows 主机；可用时使用 DirectML，否则进行 CUDA/CPU resolution。

Google Colab session 即使用户从 macOS 或 Windows 连接，本身仍是 Linux-based cloud runtime。不能根据浏览器或客户端 OS 将 Colab 误判为本地 macOS 或 Windows 环境。

profile 报告：

- `os`：Python 报告的 host/runtime OS
- `architecture`：例如 `x86_64` 或 `arm64`
- `execution_environment`：`local`、`jupyter`、`vscode` 或 `colab`
- `execution_type`：`local` 或 `cloud`
- `device`：解析后的执行设备 (`cpu`、`cuda`、`mps`、`directml`)

这样可以让相同 domain code 在 Linux、macOS、Windows、Jupyter、VS Code 和 Colab 上运行，而不把命名硬件 profile 当作 runtime requirement。

## Platform-specific accelerator policy

优先使用实测 framework capability，而不是操作系统假设。

1. `torch.cuda.is_available()` 为 true 时使用 CUDA。
2. framework 暴露可用的 MPS backend 时使用 Apple MPS。
3. `torch_directml` 已安装并可用于 runtime 时使用 DirectML。
4. CPU 是通用 fallback。

在 Linux 中，即使 PyTorch 通过 CUDA API surface 暴露 ROCm，也应将 ROCm 与 CUDA 单独报告。在 macOS 中单独报告 Apple MPS，并始终保留 CPU fallback。在 Windows 中绝不能假定 DirectML 存在。

runtime 建议必须保守，为 OS、IDE/runtime、framework allocation 和后台进程保留余量，不以 100% utilization 为目标。

## Validation contract

repository CI 将 **Ubuntu 24.04 LTS 作为 Linux reference baseline** 并直接验证 macOS。Windows 由 Windows installer workflow 覆盖。runtime classification test 会模拟 Linux、macOS、Windows、Jupyter、VS Code 和 Colab，因此无需在每个 CI runner 上提供每种 accelerator，也能验证平台逻辑。

CI baseline 有意小于 support contract：直接验证一个稳定的 Linux distribution，同时保持共享代码对发行版无关。固定的 Ubuntu LTS runner label 让 baseline 可复现。
