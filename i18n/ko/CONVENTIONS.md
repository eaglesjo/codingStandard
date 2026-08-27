# codingStandard

Aider용 코딩 규칙이다. `AGENTS.md`, `LLM/AGENT.md`, `LLM/SKILL.md`, `LLM/ENVIRONMENT.md`를 따른다.

코드 작성 전에 실제 실행 환경을 확인하고 CPU, RAM, GPU, VRAM, 가속기, Python/runtime, workload에 맞춰 설정한다. 장시간 학습 전 Memory Smoke Test를 수행한다. 환경 확정 후 불필요한 platform/device branch를 제거한다. 학습에는 validation metric, Early Stopping, best checkpoint, Resume, 통제된 Ablation Study, 재현성/자원 사용량 기록을 적용한다.
