# Repository-wide Copilot Instructions

This is the repository-wide GitHub Copilot entrypoint.

@../AGENTS.md

Apply the Common rules first, then use the domain-specific rules that are actually installed and relevant to the current task:

- `LLM/AGENT.md`, `LLM/SKILL.md`, `LLM/ENVIRONMENT.md` for LLM/NLP/RAG/fine-tuning work.
- `VISION/AGENT.md`, `VISION/SKILL.md`, `VISION/ENVIRONMENT.md` for computer-vision work.

Before resource-sensitive work, detect and measure the real execution environment. Resolve a conservative runtime configuration, run the appropriate Memory Smoke Test, and lock the validated configuration before long-running execution.

Do not hard-code a named machine, GPU, RAM size, OS, or IDE. Remove unused environment branches after validation unless multi-platform support is intentional.
