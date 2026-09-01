# Evaluation Skill

Use for model evaluation, regression checks, benchmark comparisons, and error analysis.

## Protocol

1. Freeze the evaluation dataset and protocol.
2. Declare the primary metric, direction, and threshold/decision rule.
3. Evaluate baseline and candidate with the same preprocessing and split.
4. Record secondary metrics and resource cost.
5. Perform error and slice analysis where meaningful.
6. Treat statistically meaningful differences separately from ordinary run-to-run noise.

## Rules

- Never tune on the final test set.
- Do not change metric definitions between compared variants.
- Keep prediction artifacts reproducible and versioned.
- Report confidence intervals or repeated-seed variation when decision impact warrants it.
- For classification, consider class-wise precision/recall/F1 and calibration when probabilities matter.
- For regression, inspect residual/error distributions rather than a single aggregate score.
- For ranking, retrieval, generation, or multimodal tasks, use task-specific benchmark definitions and document them explicitly.

## Regression gate

A model change is not considered an improvement until the baseline comparison, evaluation protocol, metric direction, and relevant failure slices have been checked.