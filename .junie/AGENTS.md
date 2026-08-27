# codingStandard

Follow the project coding standard in `AGENTS.md`, `LLM/AGENT.md`, `LLM/SKILL.md`, and `LLM/ENVIRONMENT.md`.

Before implementation, detect and measure the real execution environment and resolve runtime settings from CPU, RAM, GPU, VRAM, accelerator, Python/runtime, and workload. Run a Memory Smoke Test before long training. After Environment Lock, keep only the validated execution path unless the project intentionally supports multiple platforms.

For ML/LLM training, apply validation metrics, Early Stopping, best checkpoint, resume support, controlled ablation studies, and reproducibility/resource tracking.
