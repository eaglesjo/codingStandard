# Image Generation Skill

Use for diffusion, autoregressive image generation, image-to-image, and related generative vision workloads.

- Separate training, validation, sampling, and inference resource budgets.
- Treat resolution, batch size, number of generated samples, denoising steps, attention memory, and latent size as primary resource variables.
- Prefer micro-batching and controlled sample counts.
- Use mixed precision only after validating numerical stability and actual accelerator support.
- Use checkpointing, gradient accumulation, and memory-efficient attention when supported.
- Never retain generated image tensors or decoded images unnecessarily; write bounded outputs and release references.
- Use validation metrics or a fixed evaluation protocol and Early Stopping where training supports it.
- Record seed, prompts/configuration when applicable, model revision, dataset revision, resolution, steps, metrics, peak VRAM/RAM, and runtime.

## Memory controls

```text
resolution ↓
batch/sample count ↓
denoising/sequence budget ↓
attention memory optimization
mixed precision
checkpointing
accumulation
CPU offload when justified
```
