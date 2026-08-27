# Gemini CLI Project Context

This file is the Gemini CLI project entrypoint.

Apply:

@AGENTS.md
@COMMON/AGENT.md
@COMMON/SKILL.md
@COMMON/ENVIRONMENT.md

Then inspect the installed domain directories:

- `LLM/` for language-model and NLP work.
- `VISION/` for image/video/OCR/detection/segmentation/generation/VLM work.

Use only the relevant domain and task-specific Skills.

Before resource-sensitive work, inspect the actual runtime and use the environment profiler when available. Before long-running training, run a Memory Smoke Test, lock the validated configuration, and record reproducibility/resource metadata.
