# LLM Environment Contract

The shared `core/common/environment.py` profiler is the source of truth for runtime detection and resource resolution. This document adds LLM-specific guidance only.

## Usage

```bash
python core/common/environment.py
python core/common/environment.py .codingstandard/environment-profile.json
```

Reuse the resolved profile/configuration throughout a run rather than re-detecting device settings in every cell.

## LLM resource controls

```text
model size
context length
batch size
gradient accumulation
precision
KV/cache behavior
gradient checkpointing
quantization/offload
```

Select settings from measured VRAM/RAM and the model workload. A representative load/forward/backward smoke test gates long-running training.

## Colab

When the runtime is Google Colab, additionally apply `platform/colab/AGENT.md` and `platform/colab/SKILL.md`. Treat the session as ephemeral and persist recovery artifacts durably.
