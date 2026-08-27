# codingStandard

Aider coding conventions. Follow `AGENTS.md`, `LLM/AGENT.md`, `LLM/SKILL.md`, and `LLM/ENVIRONMENT.md`.

Before coding, inspect the real runtime environment and workload. Resolve resource settings from measured CPU, RAM, GPU, VRAM, accelerator, Python/runtime, and workload requirements. Run a Memory Smoke Test before long training. After Environment Lock, remove unused platform/device branches unless multi-platform support is required.

Training uses validation metrics, Early Stopping, best checkpoints, resume support, controlled ablation studies, and reproducibility/resource metadata.
