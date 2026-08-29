# Vision AI Agent Rules

Apply these rules to computer-vision and image-based AI projects.

1. Inspect the real runtime before choosing device, image size, batch size, workers, precision, or cache behavior.
2. Reuse the shared environment profile and memory safety rules; never hard-code a named machine.
3. Treat image resolution, channels, batch size, feature-map/activation memory, augmentation workers, cache, and prefetch as resource controls.
4. Run a representative Memory Smoke Test before long training.
5. Use validation metrics, Early Stopping, best checkpoint, and Resume for long-running training by default.
6. Define baseline and controlled ablation variants explicitly.
7. Record model/dataset revision, configuration, seed, metrics, runtime, peak VRAM/RAM, image size, and resolved environment profile.
8. After the environment is locked, remove unused platform/device branches from project execution code unless the component officially supports multiple platforms.
9. Prefer lazy image loading, streaming/chunking, bounded caches, conservative workers, and controlled prefetching.
10. On memory failure, reduce image size/batch/workers before retrying and never loop indefinitely on the same failing configuration.

## Task flow

```text
Repository → Environment → Capability/Resource Profile → Vision Task → Runtime Config
→ Memory Smoke Test → Environment Lock → Implement → Train/Infer → Evaluate
→ Early Stopping/Checkpoint → Ablation → Resource/Reproducibility Record → Clean Run
```
