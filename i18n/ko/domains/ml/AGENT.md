# ML / Deep Learning Agent 규칙

일반 머신러닝과 딥러닝 프로젝트에 적용합니다.

- 실제 repository, runtime, dependency, dataset contract를 먼저 확인합니다.
- CPU/RAM/disk/accelerator/VRAM과 framework capability를 측정한 뒤 resource-sensitive 설정을 결정합니다.
- dataset schema, missingness, label/target, duplicate, leakage, split을 학습 전에 검증합니다.
- baseline, hypothesis, primary metric, 변경/고정 변수, seed, budget을 명시합니다.
- baseline 이후 통제된 Ablation Study와 비교 실험을 수행합니다.
- 장시간 학습은 validation, best checkpoint, Resume, 필요한 경우 Early Stopping을 사용합니다.
- evaluation은 train/validation/test 경계를 유지하고 error/slice analysis를 수행합니다.
- Git 상태, environment profile, model/dataset revision, seed, metric, artifact, peak resource를 기록합니다.
- 특정 장비나 고정 resource capacity를 요구하지 않습니다.

```text
Repository → Data Validate → Environment → Baseline
→ Smoke Test → Lock → Train/Infer → Evaluate
→ Compare / Ablation → Record Lineage → Reproducibility Check
```