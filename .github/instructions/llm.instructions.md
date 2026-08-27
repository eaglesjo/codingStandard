---
applyTo: "**/LLM/**,**/llm/**,**/training/**,**/train/**,**/nlp/**,**/rag/**,**/*.ipynb"
---
# LLM / ML Task Instructions

@../../AGENTS.md

For LLM/NLP/ML tasks, apply the installed `LLM/AGENT.md`, `LLM/SKILL.md`, and `LLM/ENVIRONMENT.md`.

Before resource-sensitive work:

- measure the actual Python/runtime, CPU, RAM, accelerator, VRAM, and disk when available;
- resolve a conservative runtime configuration;
- run a representative Memory Smoke Test;
- lock the validated configuration before long-running work.

Do not hard-code a specific machine or fixed resource capacity. After environment validation, remove unused execution branches and obsolete code.

Training should use validation, Early Stopping where meaningful, best Checkpoint, Resume, controlled Ablation Study, and reproducibility/resource tracking.
