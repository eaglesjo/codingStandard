# Distributed Training Skill

Use for multi-GPU or multi-node training and large-model execution.

## Preconditions

- Confirm accelerator count, topology, backend, framework support, and available memory.
- Start with the smallest representative distributed smoke test before a long run.
- Make data sharding, sampler behavior, random seeds, and logging rank-aware.

## Training

For PyTorch workloads, select the simplest supported strategy that meets the requirement, such as DDP or FSDP. Use the framework launcher and distributed APIs rather than custom process management unless required.

## Checkpoint / Resume

Checkpointing must be rank-safe and preserve the state needed for optimizer/scheduler/AMP restoration. Prefer sharded/distributed checkpoint formats for workloads that require them. Validate restore before committing to a long run.

## Rules

- Do not infer global batch size from per-rank batch size; record both.
- Keep evaluation and metric aggregation correct across ranks.
- Avoid every rank writing the same artifact unless intentionally coordinated.
- Record world size, rank topology, backend, precision, effective batch size, and checkpoint format in experiment metadata.
- On distributed OOM or timeout, capture the failing topology/configuration and change one resource dimension before retrying.