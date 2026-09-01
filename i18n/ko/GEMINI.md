# Gemini CLI 프로젝트 지침

이 파일은 Gemini CLI용 adapter입니다. 정책의 원본은 `AGENTS.md`와 `core/common/`에 있습니다.

`AGENTS.md` → `core/common/` → 관련 `domains/*` → Colab이면 `platform/colab/` → task Skill 순서로 적용합니다.

관련 domain:

- `domains/ml/`: 일반 머신러닝/딥러닝
- `domains/llm/`: LLM/NLP/RAG/fine-tuning
- `domains/vision/`: Vision/VLM/OCR/detection/segmentation

실제 실행 환경을 측정하고 runtime configuration과 Memory Smoke Test로 검증합니다. 장시간 학습에는 validation, best checkpoint, Resume, 필요한 경우 Early Stopping을 적용합니다.

실험은 baseline, primary metric, seed, dataset/model revision, resource usage, artifact와 Git 상태를 기록합니다. Colab에서는 runtime reset/중단을 전제로 durable checkpoint와 resume 검증을 사용합니다.
