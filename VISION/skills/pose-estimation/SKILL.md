# Pose Estimation Skill

Use for keypoint, landmark, and human/object pose estimation.

- Record keypoint schema, visibility rules, image size, augmentation, and split policy.
- Control resolution and batch size because heatmaps/feature maps can dominate memory.
- Use task metrics such as PCK/AP and define thresholds explicitly.
- Apply Early Stopping, best checkpoint, Resume, and controlled ablations.
- Prefer bounded workers, prefetch, and lazy image decoding.
