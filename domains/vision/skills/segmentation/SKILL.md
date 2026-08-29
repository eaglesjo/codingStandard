# Image Segmentation Skill

Use for semantic, instance, and panoptic segmentation.

- Record image size, mask encoding, class count, ignore index, and split strategy.
- Treat full-resolution masks and feature maps as major memory consumers.
- Prefer tiled/cropped training or lower resolution when memory is constrained.
- Use IoU/Dice and task-appropriate class-wise metrics.
- Apply Early Stopping, best checkpoint, Resume, and controlled ablations.

## Memory controls

```text
resolution ↓
mask/feature-map footprint ↓
batch ↓
workers/prefetch/cache ↓
AMP
checkpointing
accumulation
tiling/cropping
```
