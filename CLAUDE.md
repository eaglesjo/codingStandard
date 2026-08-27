# Claude Code Project Instructions

이 파일은 Claude Code의 프로젝트 메모리 자동 진입점이다.

전체 규칙은 다음 파일을 읽고 적용한다.

@AGENTS.md
@LLM/AGENT.md
@LLM/SKILL.md

Claude Code가 작업을 시작하면 환경 확인 → 환경 확정 → 실행 코드 정리 → 테스트 순서를 따른다.
학습/파인튜닝 작업에는 Early Stopping, best checkpoint, Resume, Ablation Study, GPU/RAM budget 규칙을 적용한다.
