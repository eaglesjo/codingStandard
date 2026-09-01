# Training Skill

Use for supervised, self-supervised, unsupervised, and custom model training.

## Before training

1. Validate the dataset contract and split.
2. Establish a baseline.
3. Resolve runtime settings from measured resources.
4. Run a representative Memory Smoke Test.
5. Lock the validated configuration.

## Long-running training

Require, when meaningful:

```text
validation dataset
primary metric + direction
Early Stopping
best checkpoint
resume state
seed policy
resource monitoring
```

Persist model, optimizer, scheduler, scaler, global step/epoch, best metric, configuration, seed, dataset/model revisions, and environment metadata as applicable.

## Recovery

On OOM, timeout, preemption, or storage failure, preserve the failure metadata, reduce or change the relevant resource dimension, re-run the smoke test, and only then resume or restart.