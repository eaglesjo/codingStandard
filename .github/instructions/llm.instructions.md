---
applyTo: "**/domains/llm/**,**/llm/**,**/training/**,**/train/**,**/nlp/**,**/rag/**,**/*.ipynb"
---
# LLM Task Instructions

@../../AGENTS.md

For LLM/NLP tasks, apply the installed `domains/ml/` lifecycle rules plus `domains/llm/AGENT.md`, `domains/llm/SKILL.md`, and `domains/llm/ENVIRONMENT.md`.

Select relevant shared ML Skills for data validation, experiment design, evaluation, training, inference, distributed training, HPO, and MLOps. Apply LLM task Skills such as fine-tuning, PEFT, quantization, RAG, or other installed capabilities when applicable.

Before resource-sensitive work:

- measure the actual Python/runtime, CPU, RAM, accelerator, VRAM, and disk when available;
- resolve a conservative runtime configuration;
- run a representative Memory Smoke Test;
- lock the validated configuration before long-running work.

Do not hard-code a specific machine or fixed resource capacity. Training should use explicit validation metrics, checkpoint/resume, controlled experiments, and reproducibility/resource tracking.