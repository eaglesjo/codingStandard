# Vision Domain Skill

`domains/ml/`과 함께 사용하며 이미지/영상 기반 AI 구현·학습·추론·평가에 적용합니다.

## 공통 lifecycle

필요한 `domains/ml/` Skill을 먼저 적용합니다.

```text
Data Validation
Experiment Design
Evaluation
Training
Inference
Distributed Training
HPO
MLOps
```

## Vision task routing

필요한 task Skill을 추가합니다.

```text
Classification
Detection
Segmentation
OCR
Pose Estimation
Image Generation
VLM
```

## Environment / Memory

실제 실행환경과 메모리를 기준으로 image resolution, channels, batch, feature-map/activation memory, augmentation worker, cache, prefetch를 결정합니다. 대표 Vision workload의 Memory Smoke Test 통과 후 configuration을 lock합니다.

장시간 학습에는 validation, best checkpoint, Resume, 필요한 경우 Early Stopping과 재현성/자원 metadata를 사용합니다.
