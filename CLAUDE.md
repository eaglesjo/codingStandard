# Claude Code Project Instructions

This file is the Claude Code project entrypoint.

Apply rules in this order:

@AGENTS.md
@COMMON/AGENT.md
@COMMON/SKILL.md
@COMMON/ENVIRONMENT.md

Then inspect the installed domain directories:

- `LLM/` for language-model and NLP work.
- `VISION/` for image/video/OCR/detection/segmentation/generation/VLM work.

Apply the relevant domain and task-specific Skills only when they are installed and applicable.

Before resource-sensitive work, inspect the actual runtime and use the available environment profiler. Before long-running training, run an appropriate Memory Smoke Test and lock the validated configuration.
