# 프로젝트 AI Agent 지침

이 파일은 AI coding agent가 프로젝트를 작업할 때 사용하는 최상위 진입점입니다.

## 기본 규칙

- 작업 시작 전에 현재 OS, Python, IDE/runtime, CPU, GPU, VRAM, RAM, accelerator를 확인합니다.
- 가능하면 `python LLM/environment.py`를 실행하여 실제 자원을 측정합니다.
- 측정 결과와 workload를 기준으로 runtime configuration을 확정합니다.
- 환경 확정 후 사용하지 않는 OS/device 분기, dead code, 구식 구현, 불필요한 import를 제거합니다.
- 공식적으로 여러 환경을 지원하는 reusable library는 필요한 분기를 유지합니다.
- 제한된 VRAM/RAM에서는 보수적인 memory budget을 사용하여 메모리 사용량을 관리합니다.
- 장시간 학습에는 validation metric, Early Stopping, best checkpoint, Resume을 적용합니다.
- 실험에는 명시적인 configuration과 Ablation Study matrix를 사용합니다.
- OOM 발생 시 동일 설정을 반복하지 않고 단계별 memory recovery를 적용합니다.
- 새 Notebook은 fresh kernel/runtime에서 위에서 아래까지 실행 가능해야 합니다.

## 표준 순서

```text
Detect → Measure → Resolve → Smoke Test → Lock → Clean → Optimize → Implement → Validate
```

상세 규칙은 `LLM/AGENT.md`, `LLM/SKILL.md`, `LLM/ENVIRONMENT.md`를 따릅니다.
