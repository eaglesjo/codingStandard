# Data Skill

Use before model training, fine-tuning, or evaluation when a dataset is involved.

## Validate before training

```text
schema
→ file readability
→ missingness
→ label validity
→ duplicates
→ leakage indicators
→ class / target balance
→ split strategy
→ distribution sanity
```

## Rules

- Keep train/validation/test boundaries explicit.
- Do not fit transforms, vocabularies, statistics, or imputers on validation/test data.
- Detect duplicate or near-duplicate records across splits when practical.
- Treat dataset revisions and checksums as lineage identifiers.
- Prefer streaming, chunking, memory mapping, and lazy loading for datasets that do not fit safely in memory.
- Keep preprocessing deterministic and versioned.
- Record filtering, sampling, augmentation, and label transformations.

## Completion criteria

A dataset is training-ready only when its schema, split policy, leakage checks, preprocessing, revision/checksum, and expected resource footprint are recorded.