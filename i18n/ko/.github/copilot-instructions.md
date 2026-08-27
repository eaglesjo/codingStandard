# GitHub Copilot 프로젝트 지침

@../AGENTS.md
@../LLM/AGENT.md
@../LLM/SKILL.md
@../LLM/ENVIRONMENT.md

작업 전 실제 환경을 측정합니다.

```text
Detect → Measure → Resolve → Smoke Test → Lock → Optimize → Implement
```

특정 GPU/RAM/OS를 하드코딩하지 않습니다. `LLM/environment.py`의 실측값을 기준으로 batch, sequence length, workers, precision 등을 결정합니다.

환경 확정 후 미사용 branch와 dead code를 제거합니다. 장시간 학습에는 validation, Early Stopping, best checkpoint, Resume을 적용합니다. Ablation Study는 동일 조건에서 수행하고 재현성/자원 사용량을 기록합니다.
