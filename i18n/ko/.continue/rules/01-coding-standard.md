---
name: codingStandard
description: 프로젝트 전체 코딩 표준과 AI 개발 작업 흐름
alwaysApply: true
---

`AGENTS.md`, `LLM/AGENT.md`, `LLM/SKILL.md`, `LLM/ENVIRONMENT.md`를 따른다.

코드 작성 전에 실제 환경을 측정하고 CPU, RAM, GPU, VRAM, 가속기, Python/runtime, workload로 runtime 설정을 결정한다. 장시간 학습 전 Memory Smoke Test를 수행한다. Environment Lock 후 불필요한 platform/device branch를 제거한다. 다중 플랫폼 지원이 필요한 코드는 분기를 유지한다.

학습에는 validation metric, Early Stopping, best checkpoint, Resume, 통제된 Ablation Study, 재현성/자원 사용량 기록을 적용한다.
