# Inference Skill

Use for batch or online inference, evaluation-time prediction, and local model execution.

## Before inference

- Load the saved model/config from a versioned artifact.
- Validate preprocessing/tokenization/feature ordering against the training contract.
- Resolve device and memory from the actual runtime.
- Run a representative warm-up and memory/latency smoke test.

## Record

```text
model revision
preprocessing revision
input shape / sequence length
batch size
throughput
latency (p50/p95 when relevant)
peak RAM / accelerator memory
device and framework versions
```

Prefer batching, streaming, bounded queues, and lazy loading when they reduce memory pressure without violating latency requirements. Keep training-only code out of inference paths.