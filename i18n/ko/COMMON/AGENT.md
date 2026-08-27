# 공통 AI Agent 규칙

모든 프로젝트에 적용되는 공통 규칙입니다.

1. 변경 전 저장소, 실행환경, 의존성, 테스트, 보안 제약을 확인합니다.
2. 자원에 민감한 설정은 실제 실행환경을 측정한 뒤 결정합니다.
3. 특정 장비, OS, CPU, RAM, GPU, 가속기, IDE를 필수 조건으로 하드코딩하지 않습니다.
4. 재사용 로직은 모듈로 분리하고 Notebook/스크립트는 orchestration에 집중합니다.
5. 설정과 재현성 metadata를 명시적으로 관리합니다.
6. 비밀정보를 소스에 저장하지 않습니다.
7. 작은 의미있는 테스트 후 전체 검증을 수행합니다.
8. 환경이 확정되면 의도된 다중 플랫폼 지원이 아닌 불필요한 branch/dead code를 제거합니다.
9. 장시간 작업은 validation, Early Stopping, best checkpoint, Resume을 기본 적용합니다.
10. 실험은 baseline, variant, seed, metric, 자원 사용량을 기록합니다.

## 표준 흐름

```text
Discover → Detect → Measure → Resolve → Smoke Test → Lock → Implement → Validate → Record
```
