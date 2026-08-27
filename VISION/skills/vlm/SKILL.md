# Vision-Language Model Skill

Use for multimodal models that combine image and text inputs or outputs.

- Inspect both image and text sequence dimensions before resolving memory budgets.
- Treat image resolution, patch/token count, text length, batch size, cross-attention, and KV/cache memory as coupled variables.
- Keep preprocessing and tokenizer/image processor versions reproducible.
- Run a multimodal Memory Smoke Test using representative image and text sizes.
- Use mixed precision, gradient checkpointing, accumulation, quantization, or offload only when supported and validated.
- Apply validation metrics, Early Stopping, best checkpoint, and Resume for long training.
- Compare image size, text length, projector/adapter, and augmentation variants with controlled ablations.
- Record image/text dimensions, model/dataset revision, processor/tokenizer revision, seed, metrics, runtime, peak VRAM/RAM, and environment profile.

## Memory controls

```text
image size ↓
text length ↓
batch ↓
image/text worker and prefetch ↓
mixed precision
checkpointing
accumulation
quantization/offload
```
