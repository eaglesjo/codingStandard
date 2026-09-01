# Vision Domain Agent 규칙

`domains/ml/` 위에 적용하는 Computer Vision/VLM 전용 규칙입니다.

## Vision 고유 규칙

1. 이미지/영상 resolution, channels, batch size, activation/feature-map memory, augmentation workers, cache, prefetch를 주요 자원 변수로 관리합니다.
2. 요구사항에 맞는 최소 pipeline을 선택합니다: classification, detection, segmentation, OCR/document vision, pose estimation, image generation, VLM.
3. 대규모 dataset은 lazy decoding, bounded cache, streaming/chunking, 보수적 workers/prefetch를 우선합니다.
4. 장시간 학습 전 대표 Vision workload의 Memory Smoke Test를 수행합니다.
5. task-appropriate metric과 image/error-slice analysis를 활용합니다.
6. model/dataset revision, preprocessing/augmentation, image size, configuration, seed, metric, runtime, peak VRAM/RAM, environment profile을 기록합니다.
7. generation/VLM은 evaluation prompt/template와 benchmark/task configuration도 기록합니다.

## 공통 정책

Data Validation, Experiment Design, Evaluation, Training, Inference, Distributed Training, HPO, MLOps, Environment, Checkpoint/Resume, Reproducibility는 `domains/ml/` 공통 정책과 Skill을 사용합니다.

Colab 또는 다른 ephemeral hosted notebook이면 `platform/colab/` 정책도 적용합니다.