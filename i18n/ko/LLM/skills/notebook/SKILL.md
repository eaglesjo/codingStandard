# Notebook Skill

Jupyter Notebook, JupyterLab, VS Code Jupyter, Colab 및 local runtime 작업에 사용합니다.

새 Notebook은 fresh kernel에서 top-to-bottom 실행 가능해야 합니다. 시작 부분에서 환경 감지, hardware/resource profile, runtime configuration, Environment Lock을 수행합니다.

가능하면 데이터/모델/학습 로직은 재사용 모듈로 분리합니다. cell마다 환경을 반복 감지하지 않습니다. UTF-8, `pathlib.Path`, 활성 kernel 기준 dependency 설치, deterministic output, 임시 상태 정리를 적용합니다.

장시간 학습 전 Memory Smoke Test와 checkpoint/restart 동작을 확인합니다. 환경과 실행 경로가 확정되면 불필요한 branch와 주석 처리된 실험 코드를 제거합니다.
