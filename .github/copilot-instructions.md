# Repository-wide Copilot Instructions

이 파일은 GitHub Copilot이 저장소 전체에서 자동 적용할 공통 지침이다.

@../AGENTS.md
@../LLM/AGENT.md
@../LLM/SKILL.md
@../LLM/ENVIRONMENT.md

반드시 실제 작업 환경을 먼저 확인하고 다음 순서로 처리한다.

```text
Detect → Measure → Resolve → Smoke Test → Lock → Optimize → Implement
```

가능하면 작업 시작 시 다음을 실행한다.

```bash
python LLM/environment.py
```

실제 환경이 확정되면 resolved configuration을 사용하고, 사용하지 않는 OS/device branch와 dead code를 제거한다.

현재 PC의 특정 GPU/운영체제/RAM 용량을 하드코딩하지 않는다. 실제 CPU/GPU/VRAM/RAM/IDE/runtime 측정 결과를 source of truth로 사용한다.

Python/LLM/ML 작업에서는 다음을 기본 적용한다.
- 실제 측정된 VRAM/RAM에 맞춰 batch size, sequence length, workers, precision 등을 결정한다.
- 환경에 따른 권장값을 실제 Memory Smoke Test로 검증한다.
- 학습에는 validation metric, Early Stopping, best checkpoint, Resume를 적용한다.
- Ablation Study는 명시적 configuration matrix와 동일한 평가 기준으로 실행한다.
- 결과에는 metric뿐 아니라 seed, model/dataset revision, runtime, peak VRAM/RAM, early-stopped 여부, resolved environment profile을 기록한다.
