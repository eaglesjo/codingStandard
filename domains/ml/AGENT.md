# Machine Learning / Deep Learning Agent Rules

Apply these rules to general ML/DL projects, including scikit-learn, XGBoost, LightGBM, PyTorch, TensorFlow, JAX, tabular ML, time-series, and custom training pipelines.

## Scope

- Classical ML and deep learning
- Local, Jupyter, VS Code, cloud, and Google Colab execution
- CPU and accelerator-backed workloads
- Training, fine-tuning, evaluation, experimentation, inference, and model lifecycle

## Rules

1. Inspect the actual repository, runtime, dependencies, dataset contract, and security constraints before implementation.
2. Measure available CPU, RAM, disk, accelerator, accelerator memory, framework capabilities, and kernel/runtime state before resource-sensitive work.
3. Keep reusable data/model/training logic in modules; notebooks remain orchestration and analysis surfaces.
4. Treat dataset quality and data leakage as first-class validation concerns.
5. Define a baseline, controlled variables, primary metrics, seeds, budget, and evaluation protocol before comparing experiments.
6. Use representative smoke tests before long-running training and staged recovery after resource failures.
7. Long-running training uses validation, best checkpoint, resume, and Early Stopping where meaningful.
8. Evaluation must keep train/validation/test boundaries explicit and use task-appropriate metrics and error analysis.
9. Record experiment lineage: code/Git state, environment profile, configuration, model revision, dataset revision/checksum, seed, metrics, artifacts, and resource usage.
10. Do not hard-code a named machine or resource capacity. Resolve execution settings from measured capabilities and workload requirements.
11. Prefer deterministic paths, explicit configuration, and reproducible dependency sources.
12. Do not expose credentials, private data, or sensitive artifacts.

## Standard ML lifecycle

```text
Repository
  ↓
Environment
  ↓
Data Contract / Data Validation
  ↓
Baseline / Experiment Design
  ↓
Runtime Resolution
  ↓
Memory Smoke Test
  ↓
Environment Lock
  ↓
Train / Fine-tune
  ↓
Evaluate / Error Analysis
  ↓
Ablation / Comparison
  ↓
Artifact + Lineage Record
  ↓
Reproducibility Validation
```
