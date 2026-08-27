# Manus 연동

Manus는 일반적인 개발툴처럼 저장소 루트의 `AGENTS.md`를 자동으로 읽는 방식을 공식 문서로 제공하지 않습니다. 대신 Manus Project Instructions와 파일 기반 Skill을 사용하는 방식으로 연동합니다.

## Project Instructions

`MANUS/PROJECT_INSTRUCTIONS.md`의 내용을 Manus 프로젝트의 Project Instructions에 복사해서 사용합니다. 프로젝트에서 실행되는 작업에 해당 지침이 적용됩니다.

## Skill

`MANUS/SKILL.md`는 재사용 가능한 codingStandard Skill입니다. Manus의 Skills 화면에서 GitHub로 가져오거나 파일/폴더 형태로 가져와 사용할 수 있습니다. 외부 Skill을 사용하기 전 `SKILL.md`와 포함된 scripts/resources를 검토합니다.

## 로컬 개발

Manus Desktop App의 My Computer 기능을 사용하는 경우 승인된 로컬 폴더에서 터미널 명령을 실행할 수 있으므로 필요한 최소 폴더 권한만 부여합니다.

## codingStandard와의 관계

```text
Manus Project Instructions
        ↓
COMMON
        ↓
LLM and/or VISION
        ↓
Task-specific Skill
```

환경 감지, 메모리 안전, Early Stopping, Checkpoint/Resume, Ablation, 재현성, 보안 규칙은 다른 지원 도구와 동일한 기준을 사용합니다.

공식 문서:
- https://manus.im/docs/ko/features/skills
- https://help.manus.im/ko/articles/14753565-manus%EC%97%90%EC%84%9C-%EC%8A%A4%ED%82%AC%EC%9D%84-%EA%B3%B5%EC%9C%A0%ED%95%98%EA%B3%A0-%EC%82%AC%EC%9A%A9%ED%95%98%EB%8A%94-%EB%B0%A9%EB%B2%95
- https://help.manus.im/ko/articles/14178443-%EB%82%B4-%EC%BB%B4%ED%93%A8%ED%84%B0-%EA%B8%B0%EB%8A%A5%EC%9C%BC%EB%A1%9C-%EB%AC%B4%EC%97%87%EC%9D%84-%ED%95%A0-%EC%88%98-%EC%9E%88%EB%82%98%EC%9A%94
