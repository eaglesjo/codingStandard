# Manus 프로젝트 지침

이 파일은 Manus Project의 프로젝트 지침에 복사하여 사용할 수 있는 템플릿입니다.

## 지침 적용 순서

1. 저장소에 설치된 `COMMON/AGENT.md`, `COMMON/SKILL.md`, `COMMON/ENVIRONMENT.md`를 적용합니다.
2. 설치된 도메인 중 관련 영역을 확인합니다: `LLM/`, `VISION/`.
3. 관련 도메인의 `AGENT.md`, `SKILL.md`, `ENVIRONMENT.md`를 적용합니다.
4. 현재 작업과 관련된 Skill만 적용합니다.
5. 수정하기 전에 README, 의존성, lock 파일, 테스트, 보안 제약, 기존 프로젝트 규칙을 확인합니다.

## 환경 및 자원 규칙

- 자원 민감한 작업 전에 실제 runtime, CPU, RAM, disk, accelerator, VRAM, framework 버전 및 precision capability를 측정합니다.
- 설치된 공용 환경 프로파일러를 source of truth로 사용합니다.
- 보수적인 runtime 설정을 계산하고 관련 Memory Smoke Test를 실행한 뒤 장시간 작업 전에 환경을 확정합니다.
- 특정 장비 이름이나 고정된 VRAM/RAM 용량을 전제로 하지 않습니다.
- 환경 검증 후 application 또는 notebook 경로에서 사용하지 않는 실행 분기와 오래된 코드를 제거합니다. 단, 의도적인 멀티플랫폼 지원은 유지합니다.

## 학습 규칙

- 의미가 있는 경우 validation과 Early Stopping을 사용합니다.
- 장시간 학습은 best Checkpoint 저장/복원과 Resume을 지원합니다.
- baseline, controlled ablation, seed, primary metric, resource tracking을 정의합니다.
- Git 상태, coding-standard 버전, configuration, environment profile, model/dataset revision, 자원 사용량을 기록합니다.
- OOM 또는 자원 오류는 실패한 설정을 반복하지 않고 단계적인 설정 완화로 복구합니다.

## Manus 전용 안전 규칙

- Manus Desktop App / My Computer에서 로컬 명령을 실행할 수 있으므로 저장소 스크립트를 실행하기 전에 내용을 검토합니다.
- 필요한 최소 로컬 폴더만 권한을 부여합니다.
- API key, token, credential, private path 및 관련 없는 개인정보를 출력하거나 commit하지 않습니다.
- 반복 가능한 작업 흐름은 Manus Skill로 만들고 가능한 경우 Skill 안에 필요한 리소스를 포함합니다.
- 외부 또는 커뮤니티 Skill을 가져오기 전에 `SKILL.md`와 포함된 scripts/resources를 검토합니다.

## 최종 검증

1. 관련 테스트를 실행합니다.
2. ML 작업이면 관련 LLM/Vision Memory Smoke Test를 실행합니다.
3. 사용하지 않는 environment branch와 임시 debugging code가 남지 않았는지 확인합니다.
4. 실험이라면 재현성 metadata를 기록합니다.
5. 환경별 제한 사항을 명시합니다.
