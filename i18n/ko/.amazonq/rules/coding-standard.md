# codingStandard 프로젝트 규칙

공통 정책의 원본은 `AGENTS.md`와 `core/common/`입니다.

작업에 해당하는 `domains/ml/`, `domains/llm/`, `domains/vision/`을 적용하고, Google Colab/ephemeral runtime이면 `platform/colab/`을 추가 적용합니다.

Data Validation, Experiment Design, Evaluation, Training, Inference, Distributed Training, HPO, MLOps는 `domains/ml/` 공통 Skill을 사용합니다.

실제 OS, Python/runtime, CPU, RAM, accelerator, VRAM, disk를 측정하고 smoke test 후 runtime 설정을 lock합니다. 장시간 학습에는 validation, checkpoint/resume, 필요한 경우 Early Stopping과 reproducibility/resource metadata를 적용합니다.
