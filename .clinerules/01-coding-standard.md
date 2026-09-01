# codingStandard

Follow the canonical project instructions in `AGENTS.md` and `core/common/`. Detect and apply only the relevant installed resources:

- `domains/ml/` for general ML/DL lifecycle work.
- `domains/llm/` for LLM/NLP/RAG/fine-tuning.
- `domains/vision/` for computer vision.
- `platform/colab/` for ephemeral Google Colab/cloud notebook execution.

Use shared ML Skills for data validation, experiment design, evaluation, training, inference, distributed training, HPO, and MLOps. Apply task-specific Skills only when relevant.

Detect and measure the real environment before coding or resource-sensitive execution. Resolve conservative settings, run a smoke test before long runs, lock the validated configuration, and preserve checkpoint/resume and reproducibility metadata.

Never hard-code a named machine or fixed accelerator/RAM capacity.