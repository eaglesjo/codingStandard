#!/usr/bin/env bash
set -euo pipefail

TARGET="${1:-.}"
LANGUAGE="${2:-}"
CONFLICT_ACTION="${3:-ask}"
DRY_RUN="${4:-false}"
CONFLICT_CHOICE=""
SOURCE_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TARGET_ROOT="$(cd "$TARGET" && pwd)"

if [[ -z "$LANGUAGE" ]]; then
  printf 'Select installation language:\n  1) English (en)\n  2) Korean  (ko)\n'
  read -r -p 'Language [1]: ' SELECTION
  case "${SELECTION:-1}" in 1|en) LANGUAGE="en" ;; 2|ko) LANGUAGE="ko" ;; *) printf 'Invalid language selection.\n' >&2; exit 1 ;; esac
fi
case "$LANGUAGE" in en|ko) ;; *) printf 'Invalid language: %s. Use en or ko.\n' "$LANGUAGE" >&2; exit 1 ;; esac
case "$CONFLICT_ACTION" in ask|merge|overwrite|skip) ;; *) printf 'Invalid conflict action: %s.\n' "$CONFLICT_ACTION" >&2; exit 1 ;; esac
case "$DRY_RUN" in true|false) ;; *) printf 'Invalid dry-run value: %s.\n' "$DRY_RUN" >&2; exit 1 ;; esac

get_source() {
  local relative="$1"
  local localized="$SOURCE_ROOT/i18n/ko/$relative"
  local english="$SOURCE_ROOT/$relative"
  if [[ "$LANGUAGE" == "ko" && -f "$localized" ]]; then printf '%s\n' "$localized"; return; fi
  if [[ ! -f "$english" ]]; then printf 'Template not found: %s\n' "$relative" >&2; exit 1; fi
  printf '%s\n' "$english"
}

conflict_choice() {
  local destination="$1"
  CONFLICT_CHOICE="$CONFLICT_ACTION"
  [[ "$CONFLICT_ACTION" != "ask" ]] && return
  printf '\nFile already exists: %s\n  m = merge\n  o = overwrite\n  s = skip\n  a = merge all\n  w = overwrite all\n  k = skip all\n' "$destination" >&2
  while true; do
    read -r -p 'Action [m/o/s]: ' choice
    case "${choice:-m,,}" in
      m) CONFLICT_CHOICE="merge"; return ;; o) CONFLICT_CHOICE="overwrite"; return ;; s) CONFLICT_CHOICE="skip"; return ;;
      a) CONFLICT_ACTION="merge"; CONFLICT_CHOICE="merge"; return ;; w) CONFLICT_ACTION="overwrite"; CONFLICT_CHOICE="overwrite"; return ;; k) CONFLICT_ACTION="skip"; CONFLICT_CHOICE="skip"; return ;;
      *) printf 'Use m, o, s, a, w, or k.\n' >&2 ;;
    esac
  done
}

merge_aider_config() {
  local existing="$1"
  if grep -qE '^read:[[:space:]]*\[' <<< "$existing"; then
    grep -q 'CONVENTIONS.md' <<< "$existing" && { printf '%s\n' "$existing"; return; }
    awk '/^read:[[:space:]]*\[/ { sub(/\][[:space:]]*$/, ", CONVENTIONS.md]"); print; next } { print }' <<< "$existing"
    return
  fi
  if grep -qE '^read:[[:space:]]*$' <<< "$existing"; then
    grep -q 'CONVENTIONS.md' <<< "$existing" && { printf '%s\n' "$existing"; return; }
    awk 'BEGIN{added=0} /^read:[[:space:]]*$/ && !added {print; print "  - CONVENTIONS.md"; added=1; next} {print}' <<< "$existing"
    return
  fi
  printf '%s\n\n# BEGIN CODINGSTANDARD MANAGED BLOCK\nread:\n  - CONVENTIONS.md\n# END CODINGSTANDARD MANAGED BLOCK\n' "${existing%$'\n'}"
}

merge_text() {
  local existing="$1" incoming="$2" destination="$3"
  [[ "$destination" == ".aider.conf.yml" ]] && { merge_aider_config "$existing"; return; }
  local start='<!-- BEGIN CODINGSTANDARD MANAGED BLOCK -->' end='<!-- END CODINGSTANDARD MANAGED BLOCK -->'
  case "$destination" in *.yml|*.yaml|*.py|*.sh|*.bash) start='# BEGIN CODINGSTANDARD MANAGED BLOCK'; end='# END CODINGSTANDARD MANAGED BLOCK';; esac
  if grep -Fq "$start" <<< "$existing"; then
    awk -v start="$start" -v end="$end" -v incoming="$incoming" '$0==start{print;print incoming;inblock=1;next}$0==end{print;inblock=0;next}!inblock{print}' <<< "$existing"
  else
    printf '%s\n\n%s\n%s\n%s\n' "${existing%$'\n'}" "$start" "$incoming" "$end"
  fi
}

install_file() {
  local source_relative="$1" destination_relative="$2"
  local source destination source_text existing_text action
  source="$(get_source "$source_relative")"; destination="$TARGET_ROOT/$destination_relative"
  if [[ ! -e "$destination" ]]; then
    if [[ "$DRY_RUN" == "true" ]]; then printf '[DRY-RUN] CREATE %s [%s]\n' "$destination_relative" "$LANGUAGE"; return; fi
    mkdir -p "$(dirname "$destination")"; cat "$source" > "$destination"; printf 'Installed %s [%s]\n' "$destination_relative" "$LANGUAGE"; return
  fi
  if [[ "$DRY_RUN" == "true" ]]; then printf '[DRY-RUN] EXIST %s [%s] (policy=%s)\n' "$destination_relative" "$LANGUAGE" "$CONFLICT_ACTION"; return; fi
  conflict_choice "$destination_relative"; action="$CONFLICT_CHOICE"
  case "$action" in
    skip) printf 'Skipped %s\n' "$destination_relative" ;;
    overwrite) cat "$source" > "$destination"; printf 'Overwritten %s [%s]\n' "$destination_relative" "$LANGUAGE" ;;
    merge) source_text="$(cat "$source")"; existing_text="$(cat "$destination")"; merge_text "$existing_text" "$source_text" "$destination_relative" > "$destination"; printf 'Merged %s [%s]\n' "$destination_relative" "$LANGUAGE" ;;
  esac
}

INSTALL_MAP=(
  'AGENTS.md|AGENTS.md' 'CLAUDE.md|CLAUDE.md' 'GEMINI.md|GEMINI.md'
  '.github/copilot-instructions.md|.github/copilot-instructions.md'
  '.github/instructions/llm.instructions.md|.github/instructions/llm.instructions.md'
  '.cursor/rules/coding-standard.mdc|.cursor/rules/coding-standard.mdc'
  '.windsurf/rules/coding-standard.md|.windsurf/rules/coding-standard.md'
  '.clinerules/01-coding-standard.md|.clinerules/01-coding-standard.md'
  '.continue/rules/01-coding-standard.md|.continue/rules/01-coding-standard.md'
  '.junie/AGENTS.md|.junie/AGENTS.md'
  '.amazonq/rules/coding-standard.md|.amazonq/rules/coding-standard.md'
  'CONVENTIONS.md|CONVENTIONS.md' '.aider.conf.yml|.aider.conf.yml'
  'LLM/AGENT.md|LLM/AGENT.md' 'LLM/SKILL.md|LLM/SKILL.md' 'LLM/ENVIRONMENT.md|LLM/ENVIRONMENT.md'
  'LLM/environment.py|LLM/environment.py' 'LLM/README.md|LLM/README.md'
  'LLM/config/training.yaml|LLM/config/training.yaml' 'LLM/config/ablation.yaml|LLM/config/ablation.yaml'
)
for skill in environment training ablation notebook debugging release; do INSTALL_MAP+=("LLM/skills/$skill/SKILL.md|LLM/skills/$skill/SKILL.md"); done
for item in "${INSTALL_MAP[@]}"; do install_file "${item%%|*}" "${item#*|}"; done
printf '\nAI coding standard installed into: %s\nLanguage: %s\nConflict policy: %s\nDry run: %s\n' "$TARGET_ROOT" "$LANGUAGE" "$CONFLICT_ACTION" "$DRY_RUN"
