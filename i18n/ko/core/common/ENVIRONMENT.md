# 공통 실행환경 규칙

모든 도메인은 실제 실행환경을 source of truth로 사용합니다.

```text
Detect → Measure → Resolve → Smoke Test → Lock → Optimize
```

가능한 범위에서 CPU, RAM, 디스크, GPU/가속기, 가속기 메모리, framework capability, Python/runtime, IDE/kernel 상태를 측정합니다.

## Linux / Ubuntu / Colab

Linux는 지원 OS 계열이며 Ubuntu 24.04 LTS는 CI reference입니다. Google Colab은 사용자의 macOS/Windows가 아니라 실제 실행 중인 Python runtime 기준으로 Linux 기반 cloud/ephemeral 환경으로 분류합니다.

## Runtime 분류

- `os`: Python이 보고하는 실제 호스트/runtime 운영체제
- `execution_environment`: `local`, `jupyter`, `vscode`, `colab` 등의 실제 실행 환경
- `execution_type`: `local` 또는 `cloud`

특정 장비를 runtime 조건으로 고정하지 않습니다. OS/runtime, framework 및 background process를 위한 memory headroom을 남기고 100% 사용을 목표로 하지 않습니다.

Colab처럼 ephemeral한 runtime에서는 장시간 작업에 durable checkpoint와 artifact persistence, Resume 검증을 적용합니다.
