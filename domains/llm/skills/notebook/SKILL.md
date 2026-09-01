# Notebook Skill

Use for Jupyter Notebook, JupyterLab, VS Code Jupyter, and Colab work.

## Workflow

Keep notebooks top-to-bottom runnable from a fresh kernel/runtime. Use this order:

```text
Purpose
→ Environment / Runtime Detection
→ Resource Profile
→ Data Contract
→ Runtime Configuration
→ Baseline / Experiment Configuration
→ Data
→ Model
→ Training / Inference
→ Evaluation
→ Analysis / Visualization
→ Export
→ Reproducibility Metadata
```

Keep reusable data/model/training logic in modules when practical. Do not duplicate environment detection across cells.

For Colab, also apply `platform/colab/AGENT.md` and `platform/colab/SKILL.md`, including durable checkpoint/artifact persistence and resume validation for long-running work.

Use explicit UTF-8 paths, deterministic outputs, active-kernel dependency installation, bounded output, and cleanup of temporary state.