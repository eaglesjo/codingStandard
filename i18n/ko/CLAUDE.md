# Claude Code 프로젝트 지침

이 파일은 Claude Code용 adapter입니다. 정책의 원본은 `AGENTS.md`와 `core/common/`에 있습니다.

다음 순서로 적용합니다.

1. `AGENTS.md`
2. `core/common/AGENT.md`
3. `core/common/SKILL.md`
4. `core/common/ENVIRONMENT.md`
5. 관련 `domains/ml/`, `domains/llm/`, `domains/vision/` 리소스
6. Colab runtime이면 `platform/colab/AGENT.md`, `platform/colab/SKILL.md`
7. 관련 task-specific Skills

실제 Python/runtime, CPU, RAM, accelerator, VRAM, disk를 먼저 측정하고 resolved configuration과 Memory Smoke Test로 장시간 실행 가능 여부를 검증합니다.

ML 작업에서는 dataset 검증, baseline/experiment 설계, evaluation protocol, checkpoint/resume, Early Stopping, reproducibility/resource metadata를 적용합니다. 특정 장비나 고정 resource capacity를 전제로 하지 않습니다.
