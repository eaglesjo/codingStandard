---
name: codingStandard
description: Project-wide coding standard and AI development workflow
alwaysApply: true
---

Follow the canonical project instructions in `AGENTS.md` and `core/common/`. Detect and apply only the relevant installed resources:

- `domains/ml/` for general ML/DL lifecycle work.
- `domains/llm/` for LLM/NLP/RAG/fine-tuning.
- `domains/vision/` for computer vision.
- `platform/colab/` for ephemeral Google Colab/cloud notebook execution.

Use shared ML Skills for data validation, experiment design, evaluation, training, inference, distributed training, HPO, and MLOps. Apply task-specific Skills only when relevant.

Before coding or resource-sensitive execution, measure the actual runtime, resolve conservative settings, and run a representative smoke test before long-running work. Lock validated configuration and preserve checkpoint/resume and reproducibility metadata.

Never hard-code a named machine, GPU, RAM capacity, OS, or IDE.