# 한국어 AI Coding Standard

이 디렉터리는 codingStandard의 한국어 리소스를 제공합니다.

핵심 문서:

- `AGENT.md` — 전체 AI Agent 개발 규칙
- `SKILL.md` — 공통 AI 실행 절차 및 작업 지침
- `ENVIRONMENT.md` — 실행환경 확인 및 자원 최적화 규칙
- `INSTALL.md` — 한국어 설치 가이드
- `COMMON/` — 공통 규칙 및 실행 유틸리티
- `LLM/` — LLM/ML 작업 규칙과 Skills
- `VISION/` — Computer Vision 작업 규칙과 Skills
- `MANUS/` — Manus Project Instructions와 Skill

## Google Colab

Colab 검증 Notebook은 원본 저장소뿐 아니라 fork 또는 이전된 저장소도 대상으로 실행할 수 있습니다.

저장소 입력란에는 다음 형식을 사용할 수 있습니다.

```text
https://github.com/owner/repository.git
owner/repository
owner
```

`owner`만 입력하면 저장소 이름을 `codingStandard`로 가정합니다. Private 저장소는 `GITHUB_TOKEN` Colab Secret 또는 보안 입력을 사용할 수 있습니다.

실행 Notebook:

`tests/colab/codingstandard_colab_test.ipynb`

실행 코드는 언어와 무관하게 유지하며, 설치기는 선택한 언어의 문서와 공통 실행 파일을 함께 배포합니다.
