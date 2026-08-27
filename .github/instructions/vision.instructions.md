---
applyTo: "**/VISION/**,**/vision/**,**/cv/**,**/ocr/**,**/detection/**,**/segmentation/**"
---
# Vision / Computer Vision Task Instructions

@../../AGENTS.md

For Vision tasks, apply the installed `VISION/AGENT.md`, `VISION/SKILL.md`, and `VISION/ENVIRONMENT.md`.

Before resource-sensitive work:

- measure the actual Python/runtime, CPU, RAM, accelerator, VRAM, and disk when available;
- account for image resolution, channels, batch size, activation/feature-map memory, workers, cache, and prefetch;
- run a representative Vision Memory Smoke Test;
- lock the validated configuration before long-running training.

Do not hard-code a specific machine or fixed resource capacity. After validation, remove unused execution branches and obsolete code.

Training should use validation, Early Stopping where meaningful, best Checkpoint, Resume, controlled Ablation Study, and reproducibility/resource tracking.
