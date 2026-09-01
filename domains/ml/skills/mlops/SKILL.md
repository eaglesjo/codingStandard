# MLOps Skill

Use when a trained model or experiment moves toward durable artifacts, reproducible execution, or deployment.

## Lineage

Track the relationship between:

```text
code/Git state
→ environment
→ dataset
→ configuration
→ experiment
→ checkpoint/model
→ evaluation
→ deployment artifact
```

## Rules

- Model artifacts must have an explicit revision or immutable identifier.
- Keep training and production inference dependencies distinguishable.
- Store metrics and artifacts in a durable location when the runtime is ephemeral.
- Never publish secrets or private datasets through artifacts or logs.
- Validate a promoted artifact with the same preprocessing and evaluation contract used to select it.
- Keep rollback to the previous known-good artifact possible.

A tracking backend is optional. The repository contract must remain implementable with local structured metadata when external tracking is not available.