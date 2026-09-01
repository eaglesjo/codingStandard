# GitHub Copilot 프로젝트 지침

이 파일은 저장소 전체에서 사용하는 Copilot adapter입니다.

@../AGENTS.md

공통 규칙을 먼저 적용한 뒤 작업에 해당하는 설치 리소스만 적용합니다.

- `core/common/`: 공통 정책과 environment validation
- `domains/ml/`: 일반 ML/DL lifecycle
- `domains/llm/`: LLM/NLP/RAG/fine-tuning
- `domains/vision/`: Computer Vision/VLM
- `platform/colab/`: Colab ephemeral runtime

Data Validation, Experiment Design, Evaluation, Training, Inference, Distributed Training, HPO, MLOps는 `domains/ml/`의 공통 Skill을 우선 사용하고, 필요한 domain/task Skill만 추가합니다.

자원 민감한 작업 전 실제 runtime을 측정하고 smoke test 후 configuration을 lock합니다. 장시간 학습에는 checkpoint/resume, validation, 필요한 경우 Early Stopping, reproducibility/resource metadata를 적용합니다.
