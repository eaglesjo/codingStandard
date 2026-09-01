# Experiment Skill

Use when designing experiments, comparing models, tuning configurations, or making performance claims.

## Before running

Define:

```text
hypothesis
baseline
primary metric + direction
controlled variables
changed variables
seed set
compute/time budget
evaluation protocol
artifact policy
```

## Comparison rules

- Change one meaningful factor at a time for ablations unless a factorial design is intentional.
- Keep splits, preprocessing, evaluation, budget, and seed policy controlled across variants.
- Do not compare results produced under materially different resource or data conditions without labeling the difference.
- Preserve raw metrics and configuration; do not overwrite the baseline.

## Lineage

Every run should be traceable to code/Git state, model revision, dataset revision/checksum, environment profile, configuration, seed, and produced artifacts.

## Conclusion

Record whether the hypothesis was supported, the primary metric delta, uncertainty/variation, resource cost, and known failure cases. A faster or smaller model may be preferable even when an accuracy improvement is marginal.