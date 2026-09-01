---
applyTo: "**/*.ipynb"
---
# Notebook Runtime Instructions

@../../AGENTS.md

When the executing Python runtime is Google Colab or another ephemeral hosted notebook runtime, also apply `platform/colab/AGENT.md` and `platform/colab/SKILL.md`.

Detect the runtime from Python/kernel state rather than the client OS. For Colab work, assume interruption and runtime reset are possible: use reproducible dependency bootstrap, measured resource resolution, representative smoke tests, durable checkpoints/artifacts, and validated resume behavior for long-running jobs.

For non-Colab Jupyter work, keep the common ML/Jupyter rules and do not assume Colab-specific persistence constraints.