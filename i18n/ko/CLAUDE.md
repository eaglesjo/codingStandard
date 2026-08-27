# Claude Code 프로젝트 지침

작업 시작 시 다음을 읽고 적용합니다.

1. `AGENTS.md`
2. `LLM/AGENT.md`
3. `LLM/SKILL.md`
4. `LLM/ENVIRONMENT.md`
5. `LLM/environment.py`

실제 환경을 먼저 측정하고, resolved configuration과 Memory Smoke Test를 통과한 메모리 사용량이 검증된 설정으로 구현합니다.
환경 확정 후 사용하지 않는 실행 경로와 dead code를 제거합니다.

장시간 학습에는 Early Stopping, best checkpoint, Resume을 적용하고 Ablation Study 결과와 resource usage를 기록합니다.
