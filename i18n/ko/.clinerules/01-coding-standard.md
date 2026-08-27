# codingStandard

`AGENTS.md`, `LLM/AGENT.md`, `LLM/SKILL.md`, `LLM/ENVIRONMENT.md`를 따른다.

코드 작성 전에 실제 환경을 측정하고 CPU, RAM, GPU, VRAM, 가속기, Python/runtime, workload에 맞춰 설정한다. 장시간 학습 전 Memory Smoke Test를 수행하여 메모리 사용량을 검증한다. 환경 확정 후 미사용 platform/device branch와 dead code를 제거한다. 단, 공식 다중 플랫폼 코드는 유지한다.

학습에는 validation metric, Early Stopping, best checkpoint, Resume, 통제된 Ablation Study, 재현성/자원 사용량 기록을 적용한다.
