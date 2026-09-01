# Claude Code Project Instructions

This file is the Claude Code project entrypoint.

Apply rules in this order:

@AGENTS.md
@core/common/AGENT.md
@core/common/SKILL.md
@core/common/ENVIRONMENT.md

Then detect and apply the installed, relevant domain resources:

- `domains/ml/` for general ML/DL work.
- `domains/llm/` for language-model, NLP, RAG, and LLM fine-tuning work.
- `domains/vision/` for image/video/OCR/detection/segmentation/generation/VLM work.

For Google Colab or another ephemeral hosted notebook runtime, also apply `platform/colab/AGENT.md` and `platform/colab/SKILL.md`.

Apply only relevant task Skills. Shared ML Skills own cross-domain data, evaluation, experiment, training, inference, distributed training, HPO, and MLOps policy.

Before resource-sensitive work, inspect the actual runtime and use the available profiler. Before long-running training, run an appropriate Memory Smoke Test, lock the validated configuration, and record reproducibility/resource metadata.
