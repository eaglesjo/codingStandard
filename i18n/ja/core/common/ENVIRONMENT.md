# 共通 Environment Contract

すべてのドメインでは、実際の実行環境を真実の情報源として扱います。

```text
Detect → Measure → Resolve → Smoke Test → Lock → Optimize
```

利用可能な CPU、システム RAM、ディスク、アクセラレータ/GPU、アクセラレータメモリ、フレームワーク機能、Python/runtime、および利用可能な場合は IDE/kernel の状態を計測します。

## Linux と Ubuntu のポリシー

**Linux はサポート対象 OS ファミリーであり、Ubuntu はリファレンスディストリビューションです。**

この区別は意図的です。

- runtime contract は Linux の各ディストリビューションで移植可能に保つ。
- Ubuntu LTS は広くサポートされ、予測可能で、GitHub-hosted runner で直接利用できるため、主要な開発・CI baseline とする。
- CI は `ubuntu-latest` ではなく **Ubuntu 24.04 LTS** に固定し、runner image の移行で validation baseline が暗黙に変わらないようにする。
- Ubuntu 固有の package や filesystem 前提を、installer/CI 実装の明示的要件でない限り、共通 Python 環境契約へ持ち込まない。
- 必要な Python と framework 機能を提供する他の Linux ディストリビューションも、Python/runtime contract の範囲ではサポートする。標準 CI matrix に個別に含める必要はない。

要するに:

```text
Supported platform family: Linux
Reference implementation:  Ubuntu 24.04 LTS
CI baseline:              ubuntu-24.04
```

## OS と runtime の分類

OS と execution environment を分離します。`os` フィールドは Python を実行している実際の machine/runtime を表し、ユーザーの client device は表しません。

サポート対象 OS は hard-coded machine profile ではなく、Python runtime 情報から検出します。

- **Linux**: 通常の local Linux host と Google Colab などの cloud runtime。Ubuntu 24.04 LTS は CI reference distribution。
- **macOS**: Apple Silicon と Intel Mac。framework が MPS を提供して利用可能な場合は Apple MPS を使用し、それ以外は CPU fallback。
- **Windows**: local Windows host。DirectML が利用可能なら使用し、それ以外は CUDA/CPU resolution。

Google Colab session はユーザーが macOS または Windows から接続していても Linux-based cloud runtime です。そのため、browser/client OS を理由に Colab を local macOS や Windows と分類してはいけません。

profile には次を出力します。

- `os`: Python が報告する host/runtime OS
- `architecture`: `x86_64` や `arm64` などの runtime CPU architecture
- `execution_environment`: `local`, `jupyter`, `vscode`, `colab`
- `execution_type`: `local` または `cloud`
- `device`: 解決された execution device (`cpu`, `cuda`, `mps`, `directml`)

これにより、named hardware profile を runtime requirement にすることなく、同じ domain code を Linux、macOS、Windows、Jupyter、VS Code、Colab で実行できます。

## Platform-specific accelerator policy

OS の仮定より、framework の実測 capability を優先します。

1. `torch.cuda.is_available()` が true なら CUDA。
2. framework が利用可能な MPS backend を公開していれば Apple MPS。
3. `torch_directml` が runtime で利用可能なら DirectML。
4. universal fallback は CPU。

Linux では PyTorch が CUDA API surface を通じて扱う場合でも ROCm を CUDA と別に報告します。macOS では Apple MPS を別に報告し、CPU fallback を必須とします。Windows では DirectML の存在を仮定してはいけません。

runtime recommendation は conservative にします。OS、IDE/runtime、framework allocation、background process 用の余裕を確保し、100% utilization を目標にしません。

## Validation contract

repository CI は **Ubuntu 24.04 LTS を Linux reference baseline** として検証し、macOS を直接検証します。Windows は Windows installer workflow でカバーします。runtime classification test は Linux、macOS、Windows、Jupyter、VS Code、Colab を simulation し、すべての accelerator を各 CI runner で用意せずに platform-specific logic を検証できます。

CI baseline は support contract より狭く、1つの安定した Linux distribution を直接検証しながら、共通 code は distribution-agnostic に保ちます。
