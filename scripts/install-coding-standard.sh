#!/usr/bin/env bash
set -euo pipefail

TARGET="${1:-.}"
LANGUAGE="${2:-}"
SOURCE_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TARGET_ROOT="$(cd "$TARGET" && pwd)"

if [[ -z "$LANGUAGE" ]]; then
  printf 'Select installation language:\n'
  printf '  1) English (en)\n'
  printf '  2) Korean  (ko)\n'
  read -r -p 'Language [1]: ' SELECTION
  case "${SELECTION:-1}" in
    1) LANGUAGE="en" ;;
    2) LANGUAGE="ko" ;;
    *) printf 'Invalid language selection. Use 1 or 2.\n' >&2; exit 1 ;;
  esac
fi

case "$LANGUAGE" in
  en|ko) ;;
  *) printf 'Invalid language: %s. Use en or ko.\n' "$LANGUAGE" >&2; exit 1 ;;
esac

get_source() {
  local relative="$1"
  if [[ "$LANGUAGE" == "ko" && -f "$SOURCE_ROOT/i18n/ko/$relative" ]]; then
    printf '%s\n' "$SOURCE_ROOT/i18n/ko/$relative"
  else
    printf '%s\n' "$SOURCE_ROOT/$relative"
  fi
}

install_localized() {
  local source_relative="$1"
  local destination_relative="$2"
  local source
  source="$(get_source "$source_relative")"
  mkdir -p "$(dirname "$TARGET_ROOT/$destination_relative")"
  cp "$source" "$TARGET_ROOT/$destination_relative"
  printf 'Installed %s [%s]\n' "$destination_relative" "$LANGUAGE"
}

install_localized "AGENTS.md" "AGENTS.md"
install_localized "CLAUDE.md" "CLAUDE.md"
install_localized "GEMINI.md" "GEMINI.md"
install_localized ".github/copilot-instructions.md" ".github/copilot-instructions.md"
install_localized ".github/instructions/llm.instructions.md" ".github/instructions/llm.instructions.md"
install_localized "LLM/AGENT.md" "LLM/AGENT.md"
install_localized "LLM/SKILL.md" "LLM/SKILL.md"
install_localized "LLM/ENVIRONMENT.md" "LLM/ENVIRONMENT.md"
install_localized "LLM/environment.py" "LLM/environment.py"
install_localized "LLM/README.md" "LLM/README.md"

printf '\nAI coding standard installed into: %s\n' "$TARGET_ROOT"
printf 'Language: %s\n' "$LANGUAGE"
printf 'Environment profiler: python LLM/environment.py\n'
printf 'Supported entrypoints: AGENTS.md, CLAUDE.md, GEMINI.md, .github/copilot-instructions.md\n'
