# Vision Environment Optimization

Vision workloads are sensitive to image resolution, batch size, channels, activation/feature-map memory, decode/augmentation concurrency, cache, and prefetching.

## Resolution strategy

Measure actual accelerator memory and workload shape before selecting image size. Keep memory headroom for framework/runtime allocations.

```text
resolution ↓
→ batch ↓
→ workers/prefetch/cache ↓
→ mixed precision
→ activation/gradient checkpointing
→ accumulation
→ model/optimizer memory reduction
→ offload / tiling / cropping
```

## Data pipeline

Prefer lazy loading, streaming, bounded caches, memory mapping where applicable, and conservative worker counts. Avoid duplicate decoded images or tensor copies.

## CPU/RAM

Do not compensate for GPU limits by creating an unbounded CPU queue or prefetch buffer. Measure RAM before increasing workers.

## Smoke test

The representative test should include:

```text
load model
→ decode representative image
→ preprocess/augmentation
→ forward
→ backward (training)
→ optimizer step (training)
→ validation/inference
→ checkpoint save/reload
```

Record peak VRAM, peak RAM, image size, batch size, precision, throughput/latency, and runtime configuration.

## Environment neutrality

Never assume a particular GPU, CPU, RAM, OS, framework version, or image resolution. Resolve settings from actual capabilities and workload requirements.
