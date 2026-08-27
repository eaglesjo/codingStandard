---
name: codingStandard
description: Project-wide coding standard and AI development workflow
alwaysApply: true
---

Follow `AGENTS.md`, `LLM/AGENT.md`, `LLM/SKILL.md`, and `LLM/ENVIRONMENT.md`.

Before coding, detect and measure the real environment and resolve runtime settings from CPU, RAM, GPU, VRAM, accelerator, Python/runtime, and workload. Run a Memory Smoke Test before long training. After the environment is locked, remove unused platform/device branches unless multi-platform support is required.

Training must include validation metrics, Early Stopping, best checkpoint, resume support, controlled ablation studies, and reproducibility/resource metadata.
