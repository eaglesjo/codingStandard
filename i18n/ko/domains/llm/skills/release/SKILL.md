# Release Skill

릴리스 준비, 패키징, 최종 정리에 사용합니다.

가능하면 clean environment에서 프로젝트를 검증합니다. 테스트, lint/type check, 문서/링크 검증, 최종 build 또는 설치 테스트를 수행합니다.

coding-standard 버전, Git commit, dependency lock 상태, environment profile, 생성 artifact를 확인합니다. secret이나 개인 장비 경로를 배포하지 않습니다.

Notebook이나 model이 포함된 경우 재현성 metadata, checkpoint, 임시/debug 코드 제거 여부를 확인합니다.
