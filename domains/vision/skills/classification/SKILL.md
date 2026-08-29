# Image Classification Skill

Use for single-label, multi-label, and multi-class image classification.

## Rules

- Inspect class balance and dataset split before training.
- Resolve image size and batch size from the common environment profile and Memory Smoke Test.
- Use validation metrics appropriate to the class distribution; consider macro F1 when accuracy is misleading.
- Keep augmentation policy explicit and reproducible.
- Use Early Stopping and best checkpoint for long runs.
- Compare augmentation, image size, and backbone choices with controlled ablations.

## Resource priorities

```text
image size → batch → workers/prefetch → precision → checkpointing → accumulation
```
