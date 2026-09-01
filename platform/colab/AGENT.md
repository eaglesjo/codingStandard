# Google Colab Agent Rules

Apply when the executing Python runtime is Google Colab or another ephemeral hosted notebook runtime.

1. Detect the actual runtime; never infer the runtime from the user's browser or client OS.
2. Treat accelerator type, memory, uptime, and availability as dynamic capabilities.
3. Assume the session can be interrupted or reclaimed; long-running work must be resumable.
4. Store checkpoints, experiment metadata, and important artifacts on durable storage when appropriate.
5. Bootstrap dependencies reproducibly and verify that packages are installed into the active kernel/runtime.
6. Run an environment/profile check and workload-specific smoke test after dependency setup.
7. Resolve conservative batch/input/worker/precision settings from the measured session, not from a named Colab GPU tier.
8. Prefer frequent, bounded checkpointing for long runs and validate restore before expensive execution.
9. Keep notebook cells top-to-bottom runnable from a fresh runtime.
10. Do not rely on local machine paths, background services, or state surviving a runtime reset.

## Colab lifecycle

```text
Detect runtime
→ Bootstrap reproducibly
→ Inspect resources
→ Resolve runtime
→ Smoke Test
→ Lock
→ Checkpoint policy
→ Execute
→ Persist artifacts/metadata
→ Validate Resume
```
