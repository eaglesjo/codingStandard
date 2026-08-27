# Language Resources

This directory stores localized Markdown documentation used by the installer.

- English is maintained in the repository root and `LLM/` directories.
- `ko/` contains the Korean document set.

The installer selects `en` or `ko` and copies the selected language into the standard project entrypoint filenames such as `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, and the `LLM/` documentation files.

The executable environment profiler (`LLM/environment.py`) is language-neutral and is shared by both installations.
