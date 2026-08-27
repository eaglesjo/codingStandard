# codingStandard project rules

Follow the shared project standard:

- Read `AGENTS.md`, `LLM/AGENT.md`, `LLM/SKILL.md`, and `LLM/ENVIRONMENT.md` before environment-dependent work.
- Detect and measure the actual OS, Python/runtime, CPU, RAM, accelerator, and VRAM before selecting execution settings.
- Use `LLM/environment.py` when available and validate the resolved configuration with a Memory Smoke Test.
- Lock the validated environment and remove unused execution branches from application/notebook code.
- Long-running training requires validation metrics, Early Stopping, best checkpoint, and Resume where practical.
- Define ablations explicitly and record metrics, seeds, revisions, runtime, peak resource use, and environment profile.
