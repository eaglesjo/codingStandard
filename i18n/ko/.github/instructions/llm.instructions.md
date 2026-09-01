---
applyTo: "**/domains/llm/**,**/llm/**,**/training/**,**/train/**,**/nlp/**,**/rag/**,**/*.ipynb"
---
# LLM/ML 경로별 지침

`AGENTS.md` → `core/common/` → `domains/ml/` → `domains/llm/` → task Skill 순서로 적용합니다.

공통 ML 작업은 Data Validation, Experiment Design, Evaluation, Training, Inference, Distributed Training, HPO, MLOps Skill을 우선 사용합니다. LLM 작업에서는 Fine-Tuning, PEFT, Quantization, RAG 등 관련 Skill을 추가 적용합니다.

실제 Python kernel/runtime, CPU, RAM, accelerator, VRAM, disk를 측정하고 smoke test 후 runtime configuration을 lock합니다. 장시간 학습에는 validation, best checkpoint, Resume, 필요한 경우 Early Stopping을 적용하고 metric, revision, resource metadata를 기록합니다.
