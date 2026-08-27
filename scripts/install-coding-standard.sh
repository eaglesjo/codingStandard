#!/usr/bin/env bash
set -euo pipefail

TARGET="${1:-.}"
LANGUAGE="${2:-}"
CONFLICT_ACTION="${3:-ask}"
CONFLICT_CHOICE=""
SOURCE_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TARGET_ROOT="$(cd "$TARGET" && pwd)"

if [[ -z "$LANGUAGE" ]]; then
  printf 'Select installation language:\n'
  printf '  1) English (en)\n'
  printf '  2) Korean  (ko)\n'
  read -r -p 'Language [1]: ' SELECTION
  case "${SELECTION:-1}" in
    1|en) LANGUAGE="en" ;;
    2|ko) LANGUAGE="ko" ;;
    *) printf 'Invalid language selection.\n' >&2; exit 1 ;;
  esac
fi

case "$LANGUAGE" in
  en|ko) ;;
  *) printf 'Invalid language: %s. Use en or ko.\n' "$LANGUAGE" >&2; exit 1 ;;
esac

case "$CONFLICT_ACTION" in
  ask|merge|overwrite|skip) ;;
  *) printf 'Invalid conflict action: %s. Use ask, merge, overwrite, or skip.\n' "$CONFLICT_ACTION" >&2; exit 1 ;;
esac

get_source() {
  local relative="$1"
  local korean="$SOURCE_ROOT/i18n/ko/$relative"
  local english="$SOURCE_ROOT/$relative"
  if [[ "$LANGUAGE" == "ko" && -f "$korean" ]]; then
    printf '%s\n' "$korean"
    return
  fi
  if [[ ! -f "$english" ]]; then
    printf 'Template not found: %s\n' "$relative" >&2
    exit 1
  fi
  printf '%s\n' "$english"
}

conflict_choice() {
  local destination="$1"
  CONFLICT_CHOICE="$CONFLICT_ACTION"
  if [[ "$CONFLICT_ACTION" != "ask" ]]; then
    return
  fi

  printf '\nFile already exists: %s\n' "$destination" >&2
  printf '  m = merge\n  o = overwrite\n  s = skip\n  a = merge all remaining\n  w = overwrite all remaining\n  k = skip all remaining\n' >&2
  while true; do
    read -r -p 'Action [m/o/s]: ' choice
    choice="${choice:-m}"
    case "${choice,,}" in
      m) CONFLICT_CHOICE="merge"; return ;;
      o) CONFLICT_CHOICE="overwrite"; return ;;
      s) CONFLICT_CHOICE="skip"; return ;;
      a) CONFLICT_ACTION="merge"; CONFLICT_CHOICE="merge"; return ;;
      w) CONFLICT_ACTION="overwrite"; CONFLICT_CHOICE="overwrite"; return ;;
      k) CONFLICT_ACTION="skip"; CONFLICT_CHOICE="skip"; return ;;
      *) printf 'Use m, o, s, a, w, or k.\n' >&2 ;;
    esac
  done
}

merge_aider_config() {
  local existing="$1"
  if grep -qE '^read:[[:space:]]*\[' <<< "$existing"; then
    if grep -q 'CONVENTIONS.md' <<< "$existing"; then
      printf '%s\n' "$existing"
      return
    fi
    awk '
      /^read:[[:space:]]*\[/ {
        sub(/\][[:space:]]*$/, ", CONVENTIONS.md]")
        print
        next
      }
      { print }
    ' <<< "$existing"
    return
  fi

  if grep -qE '^read:[[:space:]]*$' <<< "$existing"; then
    if grep -q 'CONVENTIONS.md' <<< "$existing"; then
      printf '%s\n' "$existing"
      return
    fi
    awk '
      BEGIN { added=0 }
      /^read:[[:space:]]*$/ && !added { print; print "  - CONVENTIONS.md"; added=1; next }
      { print }
    ' <<< "$existing"
    return
  fi

  printf '%s\n\n# BEGIN CODINGSTANDARD MANAGED BLOCK\nread:\n  - CONVENTIONS.md\n# END CODINGSTANDARD MANAGED BLOCK\n' "${existing%$'\n'}"
}

merge_text() {
  local existing="$1"
  local incoming="$2"
  local destination="$3"
  if [[ "$destination" == ".aider.conf.yml" ]]; then
    merge_aider_config "$existing"
    return
  fi

  local start='<!-- BEGIN CODINGSTANDARD MANAGED BLOCK -->'
  local end='<!-- END CODINGSTANDARD MANAGED BLOCK -->'
  if [[ "$destination" == *.yml || "$destination" == *.yaml ]]; then
    start='# BEGIN CODINGSTANDARD MANAGED BLOCK'
    end='# END CODINGSTANDARD MANAGED BLOCK'
  fi

  if grep -Fq "$start" <<< "$existing"; then
    awk -v start="$start" -v end="$end" -v incoming="$incoming" '
      $0 == start { print; print incoming; inblock=1; next }
      $0 == end { print; inblock=0; next }
      !inblock { print }
    ' <<< "$existing"
  else
    printf '%s\n\n%s\n%s\n%s\n' "${existing%$'\n'}" "$start" "$incoming" "$end"
  fi
}

install_file() {
  local source_relative="$1"
  local destination_relative="$2"
  local source
  local destination
  local source_text
  local existing_text
  local action

  source="$(get_source "$source_relative")"
  destination="$TARGET_ROOT/$destination_relative"
  mkdir -p "$(dirname "$destination")"
  source_text="$(cat "$source")"

  if [[ ! -e "$destination" ]]; then
    printf '%s\n' "$source_text" > "$destination"
    printf 'Installed %s [%s]\n' "$destination_relative" "$LANGUAGE"
    return
  fi

  conflict_choice "$destination_relative"
  action="$CONFLICT_CHOICE"
  case "$action" in
    skip)
      printf 'Skipped %s\n' "$destination_relative"
      ;;
    overwrite)
      printf '%s\n' "$source_text" > "$destination"
      printf 'Overwritten %s [%s]\n' "$destination_relative" "$LANGUAGE"
      ;;
    merge)
      existing_text="$(cat "$destination")"
      merge_text "$existing_text" "$source_text" "$destination_relative" > "$destination"
      printf 'Merged %s [%s]\n' "$destination_relative" "$LANGUAGE"
      ;;
  esac
}

INSTALL_MAP=(
  'AGENTS.md|AGENTS.md'
  'CLAUDE.md|CLAUDE.md'
  'GEMINI.md|GEMINI.md'
  '.github/copilot-instructions.md|.github/copilot-instructions.md'
  '.github/instructions/llm.instructions.md|.github/instructions/llm.instructions.md'
  '.cursor/rules/coding-standard.mdc|.cursor/rules/coding-standard.mdc'
  '.windsurf/rules/coding-standard.md|.windsurf/rules/coding-standard.md'
  '.clinerules/01-coding-standard.md|.clinerules/01-coding-standard.md'
  '.continue/rules/01-coding-standard.md|.continue/rules/01-coding-standard.md'
  '.junie/AGENTS.md|.junie/AGENTS.md'
  'CONVENTIONS.md|CONVENTIONS.md'
  '.aider.conf.yml|.aider.conf.yml'
  'LLM/AGENT.md|LLM/AGENT.md'
  'LLM/SKILL.md|LLM/SKILL.md'
  'LLM/ENVIRONMENT.md|LLM/ENVIRONMENT.md'
  'LLM/environment.py|LLM/environment.py'
  'LLM/README.md|LLM/README.md'
)

for item in "${INSTALL_MAP[@]}"; do
  source_relative="${item%%|*}"
  destination_relative="${item#*|}"
  install_file "$source_relative" "$destination_relative"
done

printf '\nAI coding standard installed into: %s\n' "$TARGET_ROOT"
printf 'Language: %s\n' "$LANGUAGE"
printf 'Conflict policy: %s\n' "$CONFLICT_ACTION"
printf 'Environment profiler: python LLM/environment.py\n'
printf 'Supported AI integrations: Codex/AGENTS.md, Claude Code, Gemini CLI, GitHub Copilot, Cursor, Windsurf, Cline, Continue, Junie, Aider\n'
