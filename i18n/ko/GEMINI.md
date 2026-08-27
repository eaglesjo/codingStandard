# Gemini CLI 프로젝트 지침

프로젝트 작업 전에 `AGENTS.md`, `LLM/AGENT.md`, `LLM/SKILL.md`, `LLM/ENVIRONMENT.md`와 `LLM/environment.py`를 확인합니다.

실제 실행 환경을 측정하고 runtime configuration을 결정한 뒤 Memory Smoke Test를 수행합니다. 환경이 확정되면 사용하지 않는 OS/device branch와 dead code를 제거합니다.

장시간 학습에는 validation, Early Stopping, best checkpoint, Resume을 적용합니다. Ablation Study는 동일한 평가 조건에서 수행하고 metric과 resource usage를 기록합니다.
