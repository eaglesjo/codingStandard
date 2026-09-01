---
applyTo: "**/domains/vision/**,**/vision/**,**/cv/**,**/ocr/**,**/detection/**,**/segmentation/**"
---
# Vision Task Instructions

@../../AGENTS.md

For Vision tasks, apply the installed `domains/ml/` lifecycle rules plus `domains/vision/AGENT.md`, `domains/vision/SKILL.md`, and `domains/vision/ENVIRONMENT.md`.

Select relevant shared ML Skills for data validation, experiment design, evaluation, training, inference, distributed training, HPO, and MLOps. Apply vision task Skills such as classification, detection, segmentation, OCR, pose estimation, image generation, or VLM when applicable.

Before resource-sensitive work:

- measure the actual Python/runtime, CPU, RAM, accelerator, VRAM, and disk when available;
- account for image resolution, channels, batch size, activation/feature-map memory, workers, cache, and prefetch;
- run a representative Vision Memory Smoke Test;
- lock the validated configuration before long-running training.

Do not hard-code a specific machine or fixed resource capacity. Training should use validation, best checkpoints, Resume, controlled experiments, and reproducibility/resource tracking.