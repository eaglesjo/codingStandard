# Notebook Skill

Use for Jupyter Notebook/JupyterLab/VS Code Jupyter/Colab work.

Keep notebooks top-to-bottom runnable from a fresh kernel. Start with environment detection, hardware/resource profiling, runtime configuration, and Environment Lock.

Keep data/model/training logic in reusable modules when practical. Avoid repeated environment detection across cells. Use explicit UTF-8, `pathlib.Path`, active-kernel dependency installation, deterministic outputs, and cleanup of temporary state.

Before long training, run a Memory Smoke Test and verify checkpoint/restart behavior. Remove obsolete branches and commented-out experiments after the environment and execution path are finalized.
