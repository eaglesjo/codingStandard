# Manus 연동

Manus는 일반적인 개발툴처럼 저장소 루트의 `AGENTS.md`를 자동으로 읽는 방식을 공식 문서로 제공하지 않습니다. 대신 Manus Project Instructions와 파일 기반 Skill을 사용하는 방식으로 연동합니다.

## Project Instructions

`domains/manus/PROJECT_INSTRUCTIONS.md`의 내용을 Manus 프로젝트의 Project Instructions에 복사해서 사용합니다. 프로젝트에서 실행되는 작업에 해당 지침이 적용됩니다.

## Skill

`domains/manus/SKILL.md`는 재사용 가능한 codingStandard Skill입니다. Manus의 Skills 화면에서 GitHub로 가져오거나 파일/폴더 형태로 가져와 사용할 수 있습니다. 외부 Skill을 사용하기 전 `SKILL.md`와 포함된 scripts/resources를 검토합니다.

## 로컬 개발

Manus Desktop App의 My Computer 기능을 사용하는 경우 승인된 로컬 폴더에서 터미널 명령을 실행할 수 있으므로 필요한 최소 폴더 권한만 부여합니다.

## codingStandard와의 관계

```text
Manus Project Instructions
        ↓
core/common
        ↓
domains/llm and/or domains/vision
        ↓
Task-specific Skill
```
