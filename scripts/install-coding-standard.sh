#!/usr/bin/env bash
set -euo pipefail

TARGET="${1:-.}"
SOURCE_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TARGET_ROOT="$(cd "$TARGET" && pwd)"

install_file() {
  local source="$1"
  local destination="$2"
  mkdir -p "$(dirname "$destination")"
  cp "$source" "$destination"
  printf 'Installed %s\n' "${destination#$TARGET_ROOT/}"
}

install_file "$SOURCE_ROOT/AGENTS.md" "$TARGET_ROOT/AGENTS.md"
install_file "$SOURCE_ROOT/CLAUDE.md" "$TARGET_ROOT/CLAUDE.md"
install_file "$SOURCE_ROOT/GEMINI.md" "$TARGET_ROOT/GEMINI.md"
install_file "$SOURCE_ROOT/.github/copilot-instructions.md" "$TARGET_ROOT/.github/copilot-instructions.md"
install_file "$SOURCE_ROOT/.github/instructions/llm.instructions.md" "$TARGET_ROOT/.github/instructions/llm.instructions.md"
install_file "$SOURCE_ROOT/LLM/AGENT.md" "$TARGET_ROOT/LLM/AGENT.md"
install_file "$SOURCE_ROOT/LLM/SKILL.md" "$TARGET_ROOT/LLM/SKILL.md"
install_file "$SOURCE_ROOT/LLM/ENVIRONMENT.md" "$TARGET_ROOT/LLM/ENVIRONMENT.md"
install_file "$SOURCE_ROOT/LLM/environment.py" "$TARGET_ROOT/LLM/environment.py"
install_file "$SOURCE_ROOT/LLM/README.md" "$TARGET_ROOT/LLM/README.md"

printf '\nAI coding instructions installed into: %s\n' "$TARGET_ROOT"
printf 'Environment profiler: python LLM/environment.py\n'
printf 'Supported entrypoints: AGENTS.md, CLAUDE.md, GEMINI.md, .github/copilot-instructions.md\n'
