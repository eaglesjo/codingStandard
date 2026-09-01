---
applyTo: "**/domains/ml/**,**/ml/**,**/dataset/**,**/datasets/**,**/training/**,**/train/**,**/evaluation/**,**/eval/**,**/experiments/**,**/experiment/**"
---
# 일반 ML / Deep Learning 작업 지침

`AGENTS.md` → `core/common/` → 관련 `domains/ml/` → task Skill 순서로 적용합니다.

Data Validation, Experiment Design, Evaluation, Training, Inference, Distributed Training, HPO, MLOps에 공통 ML Skill을 우선 적용하고 필요한 task Skill만 추가합니다.

장시간 작업 전 dataset contract, baseline, primary metric, 실제 runtime 측정, smoke test, environment lock, reproducibility/resource metadata를 확인합니다. 특정 장비나 accelerator capacity를 하드코딩하지 않습니다.