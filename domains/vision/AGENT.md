# Vision Domain Agent Rules

Apply on top of `domains/ml/` for computer-vision and image-based AI projects.

## Vision-specific rules

1. Treat image/video resolution, channels, batch size, activation/feature-map memory, augmentation workers, cache, and prefetch as primary resource variables.
2. Select the smallest vision pipeline that satisfies the requirement: classification, detection, segmentation, OCR/document vision, pose estimation, image generation, or VLM.
3. Prefer lazy decoding, bounded caches, streaming/chunking, conservative workers, and controlled prefetching for large datasets.
4. Run a representative vision Memory Smoke Test before long-running training.
5. For evaluation, use task-appropriate metrics and retain image-level/error-slice analysis where meaningful.
6. Record model/dataset revision, preprocessing/augmentation, image size, configuration, seed, metrics, runtime, peak VRAM/RAM, and environment profile.
7. For generation/VLM work, record the evaluation prompt/template and benchmark/task configuration.

## Shared policy

Use `domains/ml/` for data validation, experiment design, evaluation, training, inference, distributed execution, HPO, MLOps, environment resolution, checkpoint/resume, and reproducibility.

For Google Colab or other ephemeral hosted notebooks, also apply `platform/colab/`.
