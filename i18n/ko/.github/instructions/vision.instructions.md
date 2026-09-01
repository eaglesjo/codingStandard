---
applyTo: "**/domains/vision/**,**/vision/**,**/cv/**,**/ocr/**,**/detection/**,**/segmentation/**"
---
# Vision / Computer Vision 작업 지침

`AGENTS.md` → `core/common/` → `domains/ml/` → `domains/vision/` → task Skill 순서로 적용합니다.

공통 ML 작업은 Data Validation, Experiment Design, Evaluation, Training, Inference, Distributed Training, HPO, MLOps Skill을 사용합니다. Vision에서는 Classification, Detection, Segmentation, OCR, Pose Estimation, Image Generation, VLM 등 필요한 task Skill을 추가 적용합니다.

자원 민감한 작업 전 실제 Python/runtime, CPU, RAM, accelerator, VRAM, disk와 이미지 resolution/channel/batch/activation/workers/cache/prefetch를 측정합니다. 대표 입력으로 Memory Smoke Test를 실행하고 검증된 configuration을 lock합니다.

특정 장비나 고정 자원 용량을 하드코딩하지 않습니다. 학습에는 validation, best Checkpoint, Resume, 필요한 경우 Early Stopping, 통제된 실험과 재현성/자원 사용량 기록을 적용합니다.
