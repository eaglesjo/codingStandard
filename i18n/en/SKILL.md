# SKILL.md

# Cross-Platform Python LLM / Jupyter / Google Colab Development Skill

This Skill defines the execution workflow for Python-based LLM/ML development in Jupyter Notebook, JupyterLab, VS Code Jupyter, Google Colab, and Colab Local Runtime.

## Scope

- Windows / Linux / macOS
- venv / virtualenv / conda / uv
- Jupyter / JupyterLab / VS Code Jupyter
- Google Colab / Colab Local Runtime
- CPU / CUDA / MPS
- constrained GPU VRAM and system RAM
- environment detection and runtime optimization
- environment lock and branch cleanup
- Early Stopping / Checkpoint / Resume
- Ablation Study / experiment tracking
- reproducibility / security

## 1. Start of Work

Before environment-dependent work:

```text
1. Python / active kernel
2. OS / architecture
3. IDE / Jupyter / Colab runtime
4. GPU / CUDA / VRAM
5. CPU / system RAM
6. dependencies
7. project root
8. experiment requirements
```

Run the shared profiler when available:

```bash
python LLM/environment.py
```

Optionally save the profile:

```bash
python LLM/environment.py .codingstandard/environment-profile.json
```

## 2. Environment Resolution

Do not stop at printing environment information. Convert the measurements into a runtime configuration and validate it.

```text
Detect
→ Measure
→ Resolve
→ Smoke Test
→ Lock
→ Optimize
→ Execute
```

Use:

```python
from environment import inspect_environment, to_runtime_config

PROFILE = inspect_environment()
RUNTIME_CONFIG = to_runtime_config(PROFILE)
```

The profile is the source of truth for the actual machine/runtime. Do not replace it with a fixed hardware profile.

## 3. Environment Lock and Cleanup

Once the execution environment and workload are validated:

- reuse the resolved device/configuration
- remove unused OS/device branches from application or notebook execution code
- remove duplicate detection
- remove dead imports and commented-out obsolete implementations
- keep multi-platform branches only in reusable components that actually support multiple platforms

Final notebooks should contain only the minimum diagnostics, locked configuration, actual execution path, and reproducibility metadata.

## 4. Notebook Bootstrap

Recommended order:

```text
Purpose
Environment Detection
Hardware / Memory Detection
Environment Profile Resolution
Environment Lock
UTF-8 / Path
Dependency Bootstrap
Imports
Resource Configuration
Experiment Configuration
Data
Model / Client
Training / Inference
Evaluation
Ablation
Visualization
Export
Reproducibility Metadata
```

A clean kernel/runtime must be able to run the notebook top-to-bottom.

## 5. Device and Precision

Default device priority:

```text
CUDA → MPS → CPU
```

Do not hard-code accelerator assumptions. Use the resolved profile.

For CUDA, evaluate FP16 AMP when supported. Evaluate BF16 only after checking actual hardware/framework support.

## 6. Resource Optimization

GPU memory controls, in order of consideration:

```text
batch size ↓
sequence/input size ↓
gradient accumulation
mixed precision
gradient checkpointing
quantization
optimizer memory reduction / offload
remove unnecessary tensors/references
```

CPU/RAM controls:

```text
avoid unnecessary full-dataset RAM loading
streaming / chunking / memory mapping
conservative DataLoader workers
avoid excessive prefetch/persistent workers
avoid duplicate DataFrame/list/tensor copies
control CPU/BLAS/OpenMP threads
```

Do not target 100% VRAM or RAM utilization.

## 7. Memory Smoke Test

Before long training, validate:

```text
model load
→ forward
→ backward
→ optimizer step
→ validation
→ checkpoint save
```

Record:

- peak VRAM
- peak RAM
- validation metric
- runtime
- resolved environment profile

If the test fails, lower the configuration before starting the main run.

## 8. OOM Recovery

```text
Record memory
→ reduce batch
→ reduce sequence/input
→ reduce workers
→ verify AMP
→ consider checkpointing
→ consider quantization/offload
→ repeat smoke test
→ run validated configuration
```

Never retry the same failing configuration indefinitely.

## 9. Training Configuration

Keep training settings in one explicit configuration section.

```python
TRAIN_CONFIG = {
    **RUNTIME_CONFIG,
    "learning_rate": 2e-5,
    "num_train_epochs": 10,
    "eval_strategy": "epoch",
    "save_strategy": "epoch",
}
```

Adapt these values to the actual project and workload.

## 10. Early Stopping

Long-running training uses validation-based Early Stopping by default.

```python
EARLY_STOPPING = {
    "enabled": True,
    "metric": "eval_loss",
    "mode": "min",
    "patience": 3,
    "min_delta": 0.0,
    "restore_best": True,
}
```

Require:

- validation dataset/split
- explicit metric and direction
- patience
- best checkpoint
- best checkpoint restoration
- early-stop event logging

## 11. Checkpoint / Resume

Save enough state to resume after interruption when practical:

```text
model
optimizer
scheduler
AMP scaler
epoch / global step
best metric
Early Stopping counter
training configuration
seed
model revision
dataset revision
resolved environment profile
```

## 12. Ablation Study

Define a baseline and an explicit variant matrix.

```python
ABLATION_CONFIG = {
    "study_name": "components",
    "baseline": {
        "feature_a": True,
        "feature_b": True,
    },
    "variants": {
        "no_feature_a": {"feature_a": False},
        "no_feature_b": {"feature_b": False},
    },
    "seeds": [42, 43, 44],
    "primary_metric": "eval_loss",
    "metric_mode": "min",
}
```

Keep controlled variables consistent across variants whenever possible:

```text
train/validation split
test set
metric
Early Stopping policy
maximum budget
checkpoint rule
seed set
resolved environment profile
```

## 13. Experiment Tracking

Record:

```text
experiment_id
variant
changed_parameters
seed
model_revision
dataset_revision
best_metric
best_epoch/step
early_stopped
peak_vram
peak_ram
runtime
checkpoint_path
resolved environment profile
```

## 14. Validation Workflow

```text
1. Restart kernel/runtime
2. Run environment profiler
3. Measure hardware/memory
4. Resolve runtime configuration
5. Run Memory Smoke Test
6. Lock validated environment
7. Clean unused branches
8. Run baseline
9. Verify Early Stopping
10. Verify checkpoint save/resume
11. Run ablations
12. Record metrics/resources
13. Final clean Run All
```

## 15. Definition of Done

```text
[ ] environment detected
[ ] resource profile generated
[ ] runtime configuration resolved
[ ] smoke test passed
[ ] environment locked
[ ] unused environment branches removed
[ ] memory recovery strategy available
[ ] validation metric defined
[ ] Early Stopping enabled
[ ] best checkpoint / Resume available
[ ] ablation matrix defined
[ ] controlled comparison completed
[ ] reproducibility metadata recorded
[ ] resource usage recorded
[ ] clean kernel Run All succeeds
```
