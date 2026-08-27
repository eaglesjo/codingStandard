# GitHub Copilot 프로젝트 지침

이 파일은 저장소 전체에서 사용하는 Copilot 진입점입니다.

@../AGENTS.md

공통 규칙을 먼저 적용한 뒤 현재 설치되어 있고 작업에 해당하는 도메인 규칙만 적용합니다.

- `LLM/AGENT.md`, `LLM/SKILL.md`, `LLM/ENVIRONMENT.md`: LLM/NLP/RAG/파인튜닝 작업
- `VISION/AGENT.md`, `VISION/SKILL.md`, `VISION/ENVIRONMENT.md`: 이미지/비디오/OCR/검출/세그멘테이션/생성/VLM 작업

자원에 민감한 작업 전 실제 실행환경을 측정하고 runtime configuration을 결정합니다. 적절한 Memory Smoke Test를 통과하여 메모리 사용량을 확인한 뒤 확정된 설정을 장시간 실행에 사용합니다.

특정 장비, GPU, RAM, OS, IDE를 하드코딩하지 않습니다. 환경 확정 후 의도된 다중 플랫폼 지원이 아닌 미사용 branch와 dead code를 제거합니다.
