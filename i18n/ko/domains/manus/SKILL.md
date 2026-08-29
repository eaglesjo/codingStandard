---
name: codingstandard-project
version: 1.0.0
description: Manus 프로젝트에 codingStandard의 Common, LLM, Vision 개발 규칙을 적용합니다.
---

# Manus용 codingStandard Project Skill

## 목적

특정 컴퓨터, 운영체제, accelerator를 전제로 하지 않고 검증된 codingStandard 개발 흐름을 Manus 작업에 적용합니다.

## 작업 흐름

1. 저장소를 분석하고 설치된 도메인을 확인합니다.
2. `core/common/AGENT.md`, `core/common/SKILL.md`, `core/common/ENVIRONMENT.md`를 적용합니다.
3. 관련 `domains/llm/` 또는 `domains/vision/` 규칙을 적용합니다.
4. 실제 runtime과 자원을 측정하고 안전한 설정을 계산합니다.
5. 장시간 ML 작업 전에 적절한 Memory Smoke Test를 실행합니다.
6. 필요한 최소 변경을 구현합니다.
7. 테스트, 학습 metric, 자원 사용량을 검증합니다.
8. 장시간 학습에는 Early Stopping, best Checkpoint, Resume, 통제된 Ablation Study를 사용합니다.
9. 재현성에 필요한 experiment metadata를 기록합니다.

## 자원 안전

- 특정 장비 이름이나 고정 VRAM/RAM을 하드코딩하지 않습니다.
- batch size, worker 수, cache, prefetch, image/token 크기는 보수적으로 시작합니다.
- free RAM, free VRAM, free disk를 동적인 제약으로 취급합니다.
- OOM 및 자원 실패는 단계적으로 설정을 완화하여 복구합니다.
- 실제 실행 환경을 확인하고 메모리 여유를 확보한 뒤 장시간 작업을 수행합니다.

## Manus 안전

- 로컬 명령 실행이 필요한 경우 repository script를 먼저 검토합니다.
- 필요한 최소 프로젝트 폴더 권한만 사용합니다.
- 비밀키, token, credential 및 관련 없는 개인 파일을 출력하거나 commit하지 않습니다.
- 커뮤니티 Skill은 가져오기 전에 `SKILL.md`와 번들 scripts/resources를 검토합니다.
