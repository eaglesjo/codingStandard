# Vision AI Skill

Use this skill for image-based AI implementation, training, inference, and evaluation.

## Before implementation

```text
1. Identify vision task
2. Inspect Python/runtime
3. Measure CPU/RAM/disk/accelerator/VRAM
4. Resolve capabilities
5. Set image resolution and batch budget
6. Configure data pipeline
7. Run Memory Smoke Test
8. Lock runtime configuration
```

## Vision task selection

Select the smallest task-specific pipeline that solves the requirement:

- classification
- detection
- segmentation
- OCR/document vision
- pose estimation
- image generation
- VLM

## Data pipeline

Prefer lazy decoding and bounded memory. Avoid loading an oversized image dataset into RAM. Control worker count, prefetching, cache size, image decode concurrency, and augmentation placement.

## GPU memory

Treat image resolution as a primary memory variable. Reduce resolution and batch before assuming more hardware is required. Use mixed precision, checkpointing, accumulation, and model/optimizer memory reduction when supported.

## Training

Long-running training requires a validation metric, Early Stopping, best checkpoint, and Resume when supported. Save the resolved environment profile and runtime configuration with experiment results.

## Evaluation

Select task-appropriate metrics:

```text
classification: accuracy / precision / recall / F1
 detection: precision / recall / mAP
segmentation: IoU / Dice
OCR: CER / WER / task accuracy
image generation: task-specific quality metrics + human/benchmark evaluation
VLM: task-specific multimodal benchmark metrics
```

## Ablation

Keep dataset split, evaluation protocol, resource budget, Early Stopping policy, and seed matrix controlled across variants. Record resolution, preprocessing, augmentation, model configuration, metrics, runtime, and peak resources.

## Memory failure

```text
record failure
→ reduce image resolution
→ reduce batch
→ reduce workers/prefetch/cache
→ verify precision
→ checkpointing/accumulation
→ model/optimizer memory reduction
→ offload/tiling/cropping
→ smoke test again
```
