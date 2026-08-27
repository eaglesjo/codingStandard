# Gemini CLI Project Context

이 파일은 Gemini CLI가 프로젝트 컨텍스트를 자동으로 읽을 수 있도록 하는 진입점이다.

전체 규칙은 다음 파일을 읽고 적용한다.

@AGENTS.md
@LLM/AGENT.md
@LLM/SKILL.md

작업 시작 시 환경 확인 → 환경 확정 → 사용하지 않는 실행 경로 제거 → 테스트를 수행한다.
학습/파인튜닝에는 Early Stopping, best checkpoint, Resume, Ablation Study, GPU/RAM budget 규칙을 적용한다.
