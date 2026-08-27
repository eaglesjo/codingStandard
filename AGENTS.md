# AGENTS.md

# Project Agent Instructions

This file is the top-level entrypoint for AI coding agents working in this repository.

## Instruction Sources

The canonical LLM development standards are:

- `LLM/AGENT.md` — general AI coding-agent rules
- `LLM/SKILL.md` — LLM/Jupyter/ML execution workflow
- `LLM/ENVIRONMENT.md` — environment detection and optimization
- `LLM/environment.py` — runtime environment profiler

When starting work, apply these in order:

1. This `AGENTS.md`
2. `LLM/AGENT.md`
3. `LLM/SKILL.md`
4. `LLM/ENVIRONMENT.md`
5. `LLM/environment.py`
6. More specific instructions in the target directory
7. Existing project README, dependency files, lock files, and tests

## Mandatory Behavior

- Inspect the real OS, Python, IDE/runtime, CPU, GPU, VRAM, RAM, and accelerator state before environment-dependent implementation.
- Run `python LLM/environment.py` when available and use its measurements as the source of truth.
- Resolve and record the runtime configuration before long-running execution.
- Never hard-code a specific machine's GPU, RAM, OS, or IDE as the required runtime.
- After the environment is validated, remove unused OS/device branches, duplicate detection, dead code, obsolete commented implementations, and unused imports from application/notebook execution code.
- Keep multi-platform branches only when they are required by an officially supported reusable component.
- Use conservative VRAM/RAM budgets and validate them with a Memory Smoke Test.
- Long-running training uses validation metrics, Early Stopping, best checkpoint, and Resume by default.
- Ablation studies use explicit configuration matrices and controlled evaluation conditions.
- Record seed, model/dataset revision, metrics, runtime, peak VRAM/RAM, and resolved environment profile.
- Use staged OOM recovery instead of repeating the same failing configuration indefinitely.
- New notebooks must run top-to-bottom from a clean kernel/runtime.

## Environment Optimization Contract

```text
Detect
  ↓
Measure
  ↓
Resolve
  ↓
Smoke Test
  ↓
Lock
  ↓
Clean unused branches
  ↓
Run optimized configuration
```

The final execution code should keep only the minimum diagnostics, locked runtime configuration, actual execution path, and reproducibility metadata needed for the project.
