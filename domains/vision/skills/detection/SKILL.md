# Object Detection Skill

Use for bounding-box and instance detection workloads.

- Keep train/validation/test splits reproducible.
- Record image size, box preprocessing, augmentation, and class mapping.
- Prefer task metrics such as mAP, precision, and recall; define IoU thresholds explicitly.
- Control multi-scale training and augmentation because they can multiply memory use.
- Run detection-specific Memory Smoke Tests before long runs.
- Use Early Stopping, best checkpoint, Resume, and controlled ablations.

## Memory controls

```text
image size ↓
batch ↓
workers/prefetch ↓
AMP
checkpointing
accumulation
multi-scale/cache reduction
```
