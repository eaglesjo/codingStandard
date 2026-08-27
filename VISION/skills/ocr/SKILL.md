# OCR and Document Vision Skill

Use for text extraction, document understanding, layout analysis, and OCR workloads.

- Record input resolution, preprocessing, rotation/cropping policy, language/script assumptions, and evaluation set.
- Preserve original images and deterministic preprocessing metadata.
- Avoid loading all high-resolution pages into RAM; prefer streaming and bounded caches.
- Use CER/WER and task-specific accuracy where appropriate.
- For document batches, control decode concurrency and page size before increasing workers.
- Apply Early Stopping, best checkpoint, Resume, and controlled ablations for training.

## Memory controls

```text
page/image resolution ↓
page batch ↓
decode workers ↓
prefetch/cache ↓
AMP
checkpointing
micro-batching / tiling
```
