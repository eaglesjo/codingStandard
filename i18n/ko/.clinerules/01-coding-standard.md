# codingStandard

`AGENTS.md`와 `core/common/`을 기준으로 하며, 작업에 해당하는 `domains/ml/`, `domains/llm/`, `domains/vision/`, `platform/colab/`만 적용한다.

공통 ML lifecycle은 Data Validation, Experiment Design, Evaluation, Training, Inference, Distributed Training, HPO, MLOps Skill로 관리한다.

실제 runtime을 측정하고 smoke test 후 configuration을 lock한다. 장시간 학습은 validation, checkpoint/resume, 필요한 경우 Early Stopping과 reproducibility/resource metadata를 사용한다.
