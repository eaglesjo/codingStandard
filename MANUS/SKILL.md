---
name: codingstandard-project
version: 1.0.0
description: Apply codingStandard Common, LLM, and Vision development rules to a Manus project.
---

# codingStandard Project Skill for Manus

## Purpose

Apply the repository's validated development workflow to Manus tasks without assuming a specific machine, operating system, or accelerator.

## Workflow

1. Inspect the repository and determine the installed domains.
2. Load `COMMON/AGENT.md`, `COMMON/SKILL.md`, and `COMMON/ENVIRONMENT.md`.
3. Load the relevant `LLM/` or `VISION/` domain rules.
4. Measure the actual runtime and resolve resource-safe settings.
5. Run the appropriate Memory Smoke Test before long-running ML work.
6. Implement or modify the smallest correct change.
7. Validate tests, training metrics, and resource usage.
8. Use Early Stopping, best Checkpoint, Resume, and controlled Ablation Study for long-running training.
9. Record experiment metadata needed for reproducibility.

## Resource Safety

- Do not hard-code a named machine or fixed VRAM/RAM assumption.
- Prefer conservative batch size, worker count, cache, prefetch, and image/token dimensions.
- Treat free RAM, free VRAM, and free disk as dynamic constraints.
- Use staged recovery for out-of-memory or other resource failures.

## Manus Safety

- Review repository scripts before executing them when the task involves local command execution.
- Use only authorized project folders and the minimum required permissions.
- Never print or commit secrets, tokens, credentials, or unrelated private files.
- Review community-provided Skills and bundled scripts before importing or executing them.
