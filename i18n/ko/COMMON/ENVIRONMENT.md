# 공통 실행환경 규칙

모든 도메인은 실제 실행환경을 source of truth로 사용합니다.

```text
Detect → Measure → Resolve → Smoke Test → Lock → Optimize
```

가능한 범위에서 CPU, RAM, 디스크, GPU/가속기, 가속기 메모리, framework capability, Python/runtime, IDE/kernel 상태를 측정합니다.

특정 장비를 runtime 조건으로 고정하지 않습니다. OS와 runtime을 포함한 모든 결정은 측정값과 workload 요구사항을 기준으로 합니다.

OS, IDE/runtime, framework 및 background process를 위한 메모리 여유를 남기고 100% 사용을 목표로 하지 않습니다.
