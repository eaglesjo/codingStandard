---
applyTo: "**/domains/ml/**,**/ml/**,**/dataset/**,**/datasets/**,**/training/**,**/train/**,**/evaluation/**,**/eval/**,**/experiments/**,**/experiment/**"
---
# General ML / Deep Learning Task Instructions

@../../AGENTS.md

Apply `domains/ml/AGENT.md`, `domains/ml/SKILL.md`, and `domains/ml/ENVIRONMENT.md`, then only the relevant task Skills.

Prefer shared Skills for data validation, experiment design, evaluation, training, inference, distributed training, hyperparameter optimization, and MLOps. Do not duplicate these rules in project-specific notebooks or scripts.

Before long-running execution, validate the data contract, define a baseline and primary metric, measure the runtime, run a representative smoke test, lock the validated configuration, and persist reproducibility/resource metadata.

Keep train/validation/test boundaries explicit and never hard-code a named machine or fixed accelerator capacity.