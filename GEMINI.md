# Gemini CLI Project Context

이 파일은 Gemini CLI가 프로젝트 컨텍스트를 자동으로 읽을 수 있도록 하는 진입점이다.

전체 규칙은 다음 파일을 읽고 적용한다.

@AGENTS.md
@LLM/AGENT.md
@LLM/SKILL.md
@LLM/ENVIRONMENT.md

작업 시작 시 가능하면 다음을 실행한다.

```bash
python LLM/environment.py
```

실제 환경 확인 → CPU/GPU/VRAM/RAM 측정 → runtime configuration 확정 → smoke test → 확정 환경에 최적화 → 사용하지 않는 실행 경로 제거 → 테스트 순서를 따른다.

학습/파인튜닝에는 Early Stopping, best checkpoint, Resume, Ablation Study, GPU/RAM budget 및 resolved environment profile 기록을 적용한다.
