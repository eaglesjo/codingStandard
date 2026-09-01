# Hyperparameter Optimization Skill

Use for systematic parameter search or automated tuning.

## Rules

- Establish a strong baseline before tuning.
- Define the search space, budget, objective metric, direction, and stopping policy explicitly.
- Keep the evaluation protocol fixed and do not tune against the final test set.
- Prefer resource-aware and early-terminating search when many candidates are possible.
- Persist trial configuration, seed, metrics, runtime, peak memory, status, and artifacts.
- Reproduce the selected configuration in a clean run before promoting it.

## Budget

The search budget must be compatible with the measured runtime and accelerator capacity. On ephemeral environments, use resumable trial metadata and avoid assuming a single uninterrupted session.