---
name: codingStandard
description: 프로젝트 전체 코딩 표준과 AI 개발 작업 흐름
alwaysApply: true
---

`AGENTS.md`와 `core/common/`을 기준으로 하고, 작업에 해당하는 `domains/ml/`, `domains/llm/`, `domains/vision/`, `platform/colab/`만 적용한다.

공통 ML lifecycle은 Data Validation, Experiment Design, Evaluation, Training, Inference, Distributed Training, HPO, MLOps Skill로 관리한다. Notebook/Colab에서는 해당 runtime 정책도 적용한다.

실제 환경을 측정하고 smoke test 후 configuration을 lock한다. 장시간 학습에는 validation, checkpoint/resume, 필요한 경우 Early Stopping, 재현성/자원 metadata를 적용한다.
