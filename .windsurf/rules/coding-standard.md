# codingStandard

Follow `AGENTS.md`, `LLM/AGENT.md`, `LLM/SKILL.md`, and `LLM/ENVIRONMENT.md` as the project coding standard.

Always measure the real execution environment before implementation. Resolve runtime settings from CPU, RAM, GPU, VRAM, accelerator, Python/runtime, and workload. Run a Memory Smoke Test before long training. After environment lock, remove unused platform/device branches unless multi-platform support is required.

Training must use validation metrics, Early Stopping, best checkpoint, resume support, controlled ablation studies, and reproducibility/resource metadata.
