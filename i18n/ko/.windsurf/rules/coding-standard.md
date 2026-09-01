# codingStandard

`AGENTS.md`와 `core/common/`을 기준으로 하고, 작업에 해당하는 `domains/ml/`, `domains/llm/`, `domains/vision/`, `platform/colab/`만 적용한다.

공통 ML lifecycle은 Data Validation, Experiment Design, Evaluation, Training, Inference, Distributed Training, HPO, MLOps Skill로 관리한다.

코드 작성 전 실제 실행 환경을 측정하고 runtime 설정을 결정한다. 장시간 학습 전 smoke test를 수행하고 configuration을 lock한다. validation, checkpoint/resume, 필요한 경우 Early Stopping, 재현성/자원 사용량을 기록한다.
