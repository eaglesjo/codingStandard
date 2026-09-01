# Repository-wide Copilot Instructions

This is the repository-wide GitHub Copilot entrypoint.

@../AGENTS.md

Apply the common rules first, then use only the installed and relevant resources:

- `core/common/` for shared policy and environment validation.
- `domains/ml/` for general machine learning and deep learning.
- `domains/llm/` for language-model, NLP, RAG, and LLM fine-tuning work.
- `domains/vision/` for computer-vision work.
- `platform/colab/` for Google Colab or other ephemeral hosted notebook runtimes.

Prefer shared ML Skills for cross-domain data validation, evaluation, experiment design, training, inference, distributed training, hyperparameter optimization, and MLOps. Apply domain/task Skills only when they add task-specific constraints.

Before resource-sensitive work, detect and measure the real execution environment, resolve a conservative runtime configuration, run the appropriate smoke test, and lock the validated configuration before long-running execution.

Do not hard-code a named machine, GPU, RAM size, OS, or IDE. Preserve explicit data/evaluation boundaries, reproducibility metadata, checkpoint/resume support, and resource tracking.