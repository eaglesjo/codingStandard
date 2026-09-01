# codingStandard project rules

Follow the canonical project standard:

- Read `AGENTS.md` and `core/common/` before environment-dependent work.
- Detect and apply the installed relevant resources under `domains/ml/`, `domains/llm/`, `domains/vision/`, and `platform/colab/`.
- Use shared ML Skills for data validation, experiment design, evaluation, training, inference, distributed training, HPO, and MLOps.
- Use domain/task Skills only when applicable.
- Detect and measure the actual OS, Python/runtime, CPU, RAM, accelerator, VRAM, and disk before selecting execution settings.
- Validate resource settings with a representative smoke test and lock the validated configuration before long-running work.
- Long-running training should use validation, best checkpoint, resume support, and Early Stopping where meaningful.
- Record dataset/model revisions, seeds, metrics, runtime, peak resources, artifacts, environment profile, and Git state.
- Never hard-code a named machine or fixed resource capacity.