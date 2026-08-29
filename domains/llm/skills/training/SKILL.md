# Training Skill

Use for model training and fine-tuning.

Training configuration must consume the resolved environment profile instead of hard-coded hardware assumptions.

Required for long-running training:

- validation dataset and explicit primary metric
- Early Stopping with metric, direction, patience, and minimum improvement
- best checkpoint saving and best-checkpoint restoration
- resumable training state
- peak VRAM/RAM and runtime recording

Start with a Memory Smoke Test covering model load, forward, backward, optimizer step, validation, and checkpoint save.

On OOM, reduce resource demand in stages and repeat the smoke test. Never loop indefinitely on the same failing configuration.
