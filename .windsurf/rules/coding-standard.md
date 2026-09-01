# codingStandard

Follow the canonical project instructions in `AGENTS.md` and `core/common/`. Detect and apply only the relevant installed resources:

- `domains/ml/` for general ML/DL lifecycle work.
- `domains/llm/` for LLM/NLP/RAG/fine-tuning.
- `domains/vision/` for computer vision.
- `platform/colab/` for ephemeral Google Colab/cloud notebook execution.

Use shared ML Skills for data validation, experiment design, evaluation, training, inference, distributed training, HPO, and MLOps. Apply task-specific Skills only when relevant.

Measure the real runtime before resource-sensitive work. Resolve conservative settings, run a representative smoke test, lock the configuration, and preserve checkpoint/resume and reproducibility metadata for long-running training.

Never hard-code a named machine, GPU, RAM capacity, OS, or IDE. Keep train/validation/test boundaries explicit.