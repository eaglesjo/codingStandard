# 공통 실행환경 규칙

모든 도메인은 실제 실행환경을 source of truth로 사용합니다.

```text
Detect → Measure → Resolve → Smoke Test → Lock → Optimize
```

가능한 범위에서 CPU, RAM, 디스크, GPU/가속기, 가속기 메모리, framework capability, Python/runtime, IDE/kernel 상태를 측정합니다.

## Runtime 분류

운영체제(OS)와 실행환경을 서로 다른 값으로 관리합니다. Google Colab 세션은 사용자가 macOS 또는 Windows에서 접속하더라도 일반적으로 Linux 기반 클라우드 runtime입니다.

따라서 프로파일은 다음 값을 구분해서 제공합니다.

- `os`: Python이 보고하는 실제 호스트/runtime 운영체제입니다.
- `execution_environment`: `local`, `jupyter`, `vscode`, `colab` 중 하나입니다.
- `execution_type`: `local` 또는 `cloud`입니다.

이 구분을 통해 Colab을 로컬 Linux 설치환경으로 잘못 판단하지 않고, workload가 사용자의 접속 OS를 하드코딩하지 않은 채 runtime별 동작을 선택할 수 있습니다.

특정 장비를 runtime 조건으로 고정하지 않습니다. OS와 runtime을 포함한 모든 결정은 측정값과 workload 요구사항을 기준으로 합니다.

OS, IDE/runtime, framework 및 background process를 위한 메모리 여유를 남기고 100% 사용을 목표로 하지 않습니다.
