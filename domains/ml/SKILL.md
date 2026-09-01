# Machine Learning / Deep Learning Skill

Use for general ML/DL implementation, training, evaluation, experimentation, inference, and model lifecycle work.

## Workflow

```text
Discover
→ Inspect Data Contract
→ Detect Environment
→ Measure Resources
→ Resolve Runtime
→ Define Baseline
→ Smoke Test
→ Lock
→ Implement / Train
→ Evaluate
→ Compare
→ Record Lineage
```

## Required controls

- Reusable logic belongs in modules; notebooks orchestrate.
- Configuration is explicit and centrally defined.
- Dataset schema, labels, duplicates, leakage, missingness, and split strategy are checked before training.
- Baselines precede optimization claims.
- Train/validation/test boundaries are preserved.
- Primary metric and optimization direction are explicit.
- Resource usage and runtime are recorded.
- Long-running jobs support best checkpoint and resume; Early Stopping is enabled when meaningful.

## Experiment contract

Every meaningful experiment should record:

```text
experiment_id
hypothesis
baseline_id
variant
changed_parameters
fixed_parameters
seed
model_revision
dataset_revision_or_checksum
primary_metric
secondary_metrics
best_step_or_epoch
runtime
peak_ram
peak_accelerator_memory
artifact_paths
environment_profile
Git commit / dirty state
```

## Evaluation contract

Use a clean evaluation dataset and protocol. Compare variants under the same split, metric definition, preprocessing, seed policy, and budget whenever possible. Include error analysis and slice-level checks when the task has heterogeneous populations or failure modes.

## Resource contract

Resolve device, batch size, workers, precision, input size, accumulation, checkpointing, and caching from measured resources. A successful smoke test is the gate for long execution.

## Failure contract

On OOM or runtime resource failure:

```text
capture profile + failure
→ reduce workload demand
→ smoke test
→ lock new configuration
→ continue
```

Never repeat an unchanged failing configuration indefinitely.
