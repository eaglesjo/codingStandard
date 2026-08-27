# Claude Code Project Instructions

이 파일은 Claude Code의 프로젝트 메모리 자동 진입점이다.

전체 규칙은 다음 파일을 읽고 적용한다.

@AGENTS.md
@LLM/AGENT.md
@LLM/SKILL.md
@LLM/ENVIRONMENT.md

작업 시작 시 `python LLM/environment.py`로 실제 실행환경을 확인할 수 있으면 먼저 확인한다.

환경 확인 → 자원 측정 → runtime configuration 확정 → Memory Smoke Test → 실행 → 사용하지 않는 branch/dead code 정리 → 테스트 순서를 따른다.

학습/파인튜닝에는 Early Stopping, best checkpoint, Resume, Ablation Study, GPU/RAM budget 및 resolved environment profile 기록을 적용한다.
