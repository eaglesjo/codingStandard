# codingStandard 프로젝트 규칙

공통 프로젝트 표준을 따릅니다.

- 환경 의존 작업 전에 `AGENTS.md`, `LLM/AGENT.md`, `LLM/SKILL.md`, `LLM/ENVIRONMENT.md`를 확인합니다.
- 실제 OS, Python/runtime, CPU, RAM, accelerator, VRAM을 측정한 후 실행 설정을 결정합니다.
- 가능하면 `LLM/environment.py`를 실행하고 Memory Smoke Test로 설정을 검증합니다.
- 검증된 환경을 Lock하고 애플리케이션/Notebook에서 사용하지 않는 실행 branch를 제거합니다.
- 장시간 학습에는 validation metric, Early Stopping, best checkpoint, Resume을 적용합니다.
- Ablation Study를 명시적으로 구성하고 metric, seed, revision, runtime, peak resource, environment profile을 기록합니다.
