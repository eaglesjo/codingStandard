# Vision AI Coding Standard

This domain covers computer-vision and image-based AI workflows while reusing the common environment, memory, reproducibility, training, and ablation standards.

## Supported Workloads

- image classification
- object detection
- image segmentation
- OCR and document vision
- pose estimation
- image generation
- vision-language models (VLM)

## Workflow

```text
Detect environment
→ Resolve capabilities/resources
→ Resolve vision workload
→ Choose image size / batch / precision
→ Memory Smoke Test
→ Lock configuration
→ Train / infer
→ Early Stopping + Checkpoint/Resume
→ Evaluation
→ Ablation Study
→ Record metrics + resources
→ Clean final run
```

## Vision-specific resource rules

Image resolution, batch size, input channels, feature-map memory, augmentation workers, cache, and prefetching must be treated as first-class resource controls.

Reduce memory pressure in this order where appropriate:

```text
image resolution ↓
batch size ↓
augmentation/cache workers ↓
mixed precision
activation/gradient checkpointing
gradient accumulation
model/optimizer memory reduction
offload/tiling/cropping
```

Never assume a particular GPU, VRAM size, CPU, RAM size, or OS. Use the measured environment profile.
