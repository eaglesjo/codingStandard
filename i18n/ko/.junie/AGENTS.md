# codingStandard

프로젝트 코딩 표준은 `AGENTS.md`, `LLM/AGENT.md`, `LLM/SKILL.md`, `LLM/ENVIRONMENT.md`를 따른다.

구현 전에 실제 실행 환경을 측정하고 CPU, RAM, GPU, VRAM, 가속기, Python/runtime, workload로 runtime 설정을 결정한다. 장시간 학습 전 Memory Smoke Test를 수행한다. Environment Lock 후 다중 플랫폼 지원이 필요하지 않다면 사용하지 않는 실행 경로를 제거한다.

ML/LLM 학습에는 validation metric, Early Stopping, best checkpoint, Resume, 통제된 Ablation Study, 재현성/자원 사용량 추적을 적용한다.
