# Google Colab Skill

Use for Google Colab and other ephemeral hosted notebook runtimes.

## Runtime bootstrap

```text
identify active Python/kernel
→ detect Colab
→ inspect accelerator/RAM/disk
→ install/verify dependencies in active kernel
→ resolve conservative runtime
→ smoke test
→ lock
```

## Persistence

Choose durable storage for anything required after a runtime reset:

```text
checkpoints
experiment metadata
model artifacts
important predictions
configuration
logs needed for recovery
```

Do not assume the notebook VM filesystem will persist across sessions.

## Training policy

For long-running runs:

- checkpoint often enough to bound lost work;
- write metadata atomically or with clear completion markers;
- validate checkpoint restore before expensive execution;
- record session/runtime profile with the experiment;
- use a lower-cost smoke test before full training.

## Resource policy

Treat GPU/TPU type, accelerator memory, system RAM, disk, and runtime lifetime as measured session properties. Do not name a particular Colab hardware tier as a prerequisite. Reduce batch, sequence/input size, workers, cache, or precision when the measured session cannot safely sustain the workload.

## Notebook policy

A clean kernel must run top-to-bottom. Minimize hidden state, duplicate installs, duplicate environment detection, and outputs that grow without bounds. Keep reusable code outside notebooks when practical.